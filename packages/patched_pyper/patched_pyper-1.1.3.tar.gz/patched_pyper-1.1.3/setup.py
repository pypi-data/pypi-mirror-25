# encoding: utf-8
from __future__ import print_function, division, absolute_import
import sys
import os
from setuptools import setup, find_packages, Distribution


setup(
    name="patched_pyper",
    version="1.1.3",
    author="Uwe Schmitt",
    author_email="uwe.schmitt@id.ethz.ch",
    license="BSD",
    description="a patched version of pyper for bridging Python to R",
    long_description="""
    this is a patched version of PypeR 1.1.1 with modifications to make
    it run more stable on Windows.

    The home page of the original module is at
    http://bioinfo.ihb.ac.cn/softwares/PypeR/

    Thanks to the original authors for this usefull and robust module !
    """,
    py_modules = ["patched_pyper"],
)
