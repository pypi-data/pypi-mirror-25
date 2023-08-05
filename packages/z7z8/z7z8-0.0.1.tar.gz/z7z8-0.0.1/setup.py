#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='z7z8',
    version='0.0.1',
    description='Some python utils.',
    author='ll1l11',
    author_email='ll1l11@qq.com',
    url='https://github.com/ll1l11/z7z8',
    install_requires=['requests'],
    packages=find_packages(exclude=("tests", "tests.*")),
)
