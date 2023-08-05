#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='lanfit-exceptions',
    version='0.1.0',
    description='api exceptions',
    long_description=read('README.rst'),
    author='ll1l11',
    author_email='ll1l11@qq.com',
    url='',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)
