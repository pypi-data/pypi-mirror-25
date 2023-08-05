#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='Flask-RestClient',
    version='0.1.0',
    description='restful api client for flask extension',
    long_description=read('README.rst'),
    author='codeif',
    author_email='me@codeif.com',
    url='',
    license='MIT',
    packages=find_packages(),
    install_requires=['Flask', 'requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)
