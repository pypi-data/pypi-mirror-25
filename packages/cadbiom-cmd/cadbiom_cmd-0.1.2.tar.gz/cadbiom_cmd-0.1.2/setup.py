#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017  IRISA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The original code contained here was initially developed by:
#
#     Pierre Vignet.
#     IRISA
#     Dyliss team
#     IRISA Campus de Beaulieu
#     35042 RENNES Cedex, FRANCE

"""Definition of setup function for setuptools module."""

# Standard imports
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from sys import version_info

__PACKAGE_VERSION__ = "0.1.2"
__LIBRARY_VERSION__ = "0.1.0"

deps = []

if version_info[0] == 2:
    # Require backport of concurrent.futures on Python 2
    deps.append("futures")

################################################################################

class PyTest(TestCommand):
    """Call tests with the custom 'python setup.py test' command."""

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        errno = pytest.main()
        sys.exit(errno)

################################################################################

setup(

    # Library name & version
    name='cadbiom_cmd',
    version=__PACKAGE_VERSION__,

    # Search all packages recursively
    packages=find_packages(),

    # Authors
    author="pvignet",
    author_email="pierre.vignet@irisa.fr",

    # Description
    description="Command line tools using the Cadbiom library",
    long_description=open('README.md').read(),

    # Official page
    url = "https://gitlab.irisa.fr/0000B8EG/Cadbiom/tree/pypi_packaging",

    # Metadata
    classifiers=[
        "Environment :: Console",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: French",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],

    entry_points={
        'console_scripts': ['cadbiom_cmd = cadbiom_cmd.cadbiom_cmd:main'],
    },

    install_requires=deps + ["cadbiom"],
    # For graphs drawing manually
    extra_requires = ["matplotlib<2"],

    # Tests
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)
