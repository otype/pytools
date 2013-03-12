#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

    <application_name>    

    usage: python setup.py install

    created by hgschmidt on 26.12.12, 16:48 CET

    Copyright (c) 2012 apitrary

"""
import os
from setuptools import setup

def read(fname):
    """
        Read the README.md file
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def read_requirements():
    """
        Read the requirements.txt file
    """
    with open('requirements.txt') as f:
        requirements = f.readlines()
    return [element.strip() for element in requirements]

def scripts_list():
    return [
        'pyloggr/loggr.py'
    ]


setup(
    name="pyloggr",
    version='0.0.2',
    author='Hans-Gunther Schmidt',
    author_email='hgs@apitrary.com',
    description='pyloggr - apitrary\'s Loggr',
    long_description=read('README.md'),
    url='http://apitrary.com',
    install_requires=read_requirements(),
    keywords='pyloggr apitrary',
    scripts=scripts_list()
)
