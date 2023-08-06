#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import setuptools

def main():

    setuptools.setup(
        name             = "AWRS",
        version          = "2017.09.29.1327",
        description      = "weather utilities",
        long_description = long_description(),
        url              = "https://github.com/wdbm/AWRS",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        py_modules       = [
                           "AWRS"
                           ],
        install_requires = [
                           "docopt"
                           ],
        entry_points     = """
                           [console_scripts]
                           AWRS = AWRS:AWRS
                           """
    )

def long_description(
    filename = "README.md"
    ):

    if os.path.isfile(os.path.expandvars(filename)):
        try:
            import pypandoc
            long_description = pypandoc.convert_file(filename, "rst")
        except ImportError:
            long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()
