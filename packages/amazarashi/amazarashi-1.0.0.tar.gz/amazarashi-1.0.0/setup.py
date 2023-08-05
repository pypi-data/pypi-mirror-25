#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
from amazarashi import (
    __author__, __version__
)

with open("LICENSE", "r") as fp:
    license_msg = fp.read()

setup(
    name="amazarashi",
    description=u"amazarashiの曲をpecoで選択して歌詞を表示するスクリプト",
    author=__author__,
    version=__version__,
    license=license_msg,
    install_requires=[
        "requests==2.13.0",
        "chardet==2.1.1",
        "beautifulsoup4==4.5.3"
    ],
    entry_points={
        "console_scripts": [
            "amazarashi=amazarashi.__main__:main"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Japanese",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only"
    ]
)
