import ast
import codecs
import os
import re
import subprocess


def read(path, *parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(path, *parts), "rb", "utf-8") as f:
        return f.read()


def find_meta(meta_file, meta):
    """Extract __*meta*__ from META_FILE."""
    meta_match = re.search(
        r"^__{meta}__ = [\"]([^\"]*)[\"]".format(meta=meta),
        meta_file, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


def read_requirements(filename):
    reqs = []

    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()

            if not line or line.startswith(('#', '--')):
                continue

            reqs.append(line.split()[0])

    return reqs


def check_version(version):
    "Returns a PEP 440-compliant version number."

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|c}N - for alpha, beta and rc releases

    version = ast.literal_eval(version)
    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(x) for x in version[:parts])

    sub = ''
    if len(version) != 5:
        raise Exception("Version tuple should consist of 5 indexes")
    elif version[3] == 'alpha':
        git_hash = git_changeset()
        if git_hash:
            sub = ".dev{0}+git{1}".format(version[4], git_hash)
        else:
            sub = ".dev{0}".format(version[4])
    elif version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[version[3]] + str(version[4])

    return str(main + sub)


def git_changeset():
    rev, err = subprocess.Popen(
        "git rev-parse --short HEAD",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()

    if err:
        return None
    else:
        return rev.decode().strip().replace("+", "")
