#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

    pydeployr

    usage: python setup.py install

    created by hgschmidt on 26.12.12, 16:48 CET

    Copyright (c) 2012 apitrary

"""
import sys
import os
from setuptools import setup, find_packages

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


def get_template_base_dir():
    if sys.platform == 'darwin':
        template_dir = "{}/.deployr/templates".format(os.getenv("HOME"))
    elif sys.platform == 'linux2':
        template_dir = "/etc/deployr/templates"
    else:
        template_dir = "{}/.deployr/templates".format(os.getenv("HOME"))

    return template_dir

def scripts_list():
    return [
        'pydeployr/pydeployr/tasks.py',
        'pybuildr/pybuildr/buildr.py',
        'pyloggr/pyloggr/loggr.py',
        'pytrackr/pytrackr/trackr.py'
    ]


setup(
    name='pytools',
    version='0.0.2',
    author='Hans-Gunther Schmidt',
    author_email='hgs@apitrary.com',
    description='pytools - apitrary pytools',
    long_description=read('README.md'),
    url='http://apitrary.com',
    install_requires=read_requirements(),
    keywords='pytools pybuildr pydeployr pybalancr pyloggr pytoolslib pytrackr apitrary application',
    packages=find_packages('pytools'),
    packagedir={'':'pytools'},
    data_files=[
        (get_template_base_dir(), ['pydeployr/pydeployr/templates/genapi_base.tpl'])
    ],
    scripts=scripts_list()
)
