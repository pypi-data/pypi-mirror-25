#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=invalid-name
"""
gstbasetransform is a module that provides a patched GstBase.BaseTransform that
makes the do_transform_size virtual method usable in python.
"""

import os
import re
import sys
from setuptools import setup


def find_version():
    """Read the package's version from gstbasetransform.py"""
    version_filename = os.path.abspath("gstbasetransform.py")
    with open(version_filename) as fileobj:
        version_content = fileobj.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()


with open('README.rst', 'r') as f:
    long_description = f.read()


setup(
    name="gstbasetransform",
    version=find_version(),
    description="A module that makes GstBase.BaseTransform python-compatible",
    long_description=long_description,
    license="LGPL",
    url="https://github.com/Muges/gstbasetransform",
    author="Muges",
    author_email="git@muges.fr",

    py_modules=["gstbasetransform"],

    install_requires=[
        "six",
    ],

    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Multimedia :: Sound/Audio"
    ]
)
