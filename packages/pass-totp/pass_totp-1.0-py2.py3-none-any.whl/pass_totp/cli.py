import base64
import os
import re
import subprocess
import sys
import textwrap

import click
import click_completion
import pyperclip

from passlib import totp
from pathlib import Path


CLIP_TIME = os.getenv("PASSWORD_STORE_CLIP_TIME", 30)


class PassNameChoice(click_completion.DocumentedChoice):
    name = "choice"

    def __init__(self):
        self.choices = {}

        store_path = os.getenv("PASSWORD_STORE_DIR")
        pass_name_re = re.compile("^\/(.*)\.gpg$")

        if store_path is None:
            store_path = Path.home().joinpath(".password-store")
        else:
            store_path = Path(store_path)

        pwd_files = [str(p).replace(str(store_path), "")
                     for p in store_path.glob("**/*.gpg")]

        for pwd_file in pwd_files:
            pass_name = pass_name_re.match(pwd_file)

            if pass_name:
                self.choices[pass_name.group(1)] = ""

    def get_metavar(self, param):
        return "[...]"

    def get_missing_message(self, param):
        return ""

    def __repr__(self):
        return "PassNameChoice([...])"

    def complete(self, ctx, incomplete):
        return [(c, "") for c in self.choices.keys() if incomplete in c]


click_completion.init()


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("-n", "--name", required=False,
              help="Password file to retrieve", type=PassNameChoice())
@click.option("-c", "--clip", default=False, is_flag=True,
              help="Copy TOTP token to clipboard")
def cli(ctx, clip, name):
    if ctx.invoked_subcommand is None and name != "":
        ctx.invoke(show, passfile=name, clip=clip)
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument("passfile", type=PassNameChoice())
@click.option("-c", "--clip", default=False, is_flag=True,
              help="Copy TOTP token to clipboard")
def show(passfile, clip):
    if passfile == "":
        click.secho("No valid pass-name", fg="red")
        sys.exit(1)

    try:
        output = subprocess.check_output(["pass", passfile])
    except subprocess.CalledProcessError as e:
        sys.exit(1)

    secret = None

    for line in output.splitlines():
        line = line.strip()

        if line.startswith(b"TOTP: "):
            secret = line.replace(b"TOTP: ", b"")

    if not secret:
        click.secho("No Secret TOTP token found", fg="red")
        sys.exit(1)

    token = totp.TOTP(key=secret.decode()).generate().token

    if clip:
        old_clip = base64.b64encode(pyperclip.paste().encode())
        pyperclip.copy(str(token))

        cmds = textwrap.dedent("""
        import pyperclip; import base64; import time; time.sleep({0});
        pyperclip.copy(base64.b64decode({1}).decode())
        """)

        subprocess.Popen([sys.executable, "-c", cmds.format(CLIP_TIME, old_clip)])

        msg = "Copied {0} TOTP to clipboard. Will clear in {1} seconds."
        click.secho(msg.format(passfile, CLIP_TIME), fg="yellow")
    else:
        click.secho("TOTP Token: " + str(token), fg="yellow")
