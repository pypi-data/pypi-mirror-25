import os

from importlib import import_module
from setuptools import setup, find_packages

utils = import_module("setup_utils")

###############################################################################

META_PATH = os.path.join("src", "pass_totp", "__init__.py")
META_FILE = utils.read(META_PATH)
PACKAGES = find_packages(where="src")
KEYWORDS = ("totp", "passwordstore", "extension")
CLASSIFIERS = (
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "License :: OSI Approved :: Apache Software License",
    "Environment :: Console"
)
INSTALL_REQUIRES = utils.read_requirements("requirements.txt")
ENTRY_POINTS = {
    "console_scripts": ["pass-totp=pass_totp.cli:cli"]
}

# Trove classifiers
# Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers


###############################################################################

setup(
    name=utils.find_meta(META_FILE, "name"),
    version=utils.check_version(utils.find_meta(META_FILE, "version")),
    author=utils.find_meta(META_FILE, "author"),
    author_email=utils.find_meta(META_FILE, "email"),
    classifiers=CLASSIFIERS,
    description=utils.find_meta(META_FILE, "description"),
    entry_points=ENTRY_POINTS,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    keywords=KEYWORDS,
    license=utils.find_meta(META_FILE, "license"),
    long_description=utils.read("README.md"),
    package_dir={"": "src"},
    packages=PACKAGES,
    url=utils.find_meta(META_FILE, "uri")
)
