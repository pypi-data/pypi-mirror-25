#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="convert2txt",
    version="0.1.1",
    author="zoae",
    author_email="gmzone@126.com",
    description="convert html,PDF,DOC file to txt",
    long_description=open("README.txt").read(),
    license="MIT",
    url="https://github.com/desion/tidy_page",
    packages=['html2txt'],
    install_requires=[
        "",

    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)