#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import re
from setuptools import setup, find_packages

import sys
if not sys.version_info[0] == 3:
    sys.exit("\n \
              ****************************************************************\n \
              * The CLI has only been tested with Python 3+ at this time.    *\n \
              * Report any issues with Python 2 by emailing help@qio.io *\n \
              ****************************************************************\n")

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('cli/__init__.py').read(),
    re.M
    ).group(1)


# Get the long description from the relevant file
with open('README.rst') as f:
    long_description = f.read()

with open('/Users/fouadomri/Documents/data_science_training/pipelineio_as_of_06_09_2017/pipeline-master/cli/requirements.txt') as f:
    requirements = [line.rstrip() for line in f.readlines()]

setup(
    name = "foresight-model-cli",
    packages = ["cli"],
    entry_points = {
        "console_scripts": ['foresight = cli.__init__:main']
    },
    version = version,
    description = "Foresight CLI",
    long_description = "%s\n\nRequirements:\n%s" % (long_description, requirements),
    author = "Fouad Omri",
    author_email = "fouad.omri@qio.io",
    install_requires=requirements,
    dependency_links=[],
    package=find_packages(exclude=['concurrent', 'concurrent.*', '*.concurrent.*']),
 )
