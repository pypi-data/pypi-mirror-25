#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="affine6p",
    version="0.4",
    description="To calculate affine transformation parameters with six free parameters.",
    long_description=long_description,
    url="https://gitlab.com/yoshimoto/affine6p-py",
    author="Masahiro Yoshimoto",
    author_email="yoshimoto@flab.phys.nagoya-u.ac.jp",
    license="MIT",
    keywords="calculate affine transformation six parameters",
    packages=["affine6p"],
    classifiers=[]
)