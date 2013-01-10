#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

    <application_name>    

    usage: python setup.py install

    created by hgschmidt on 26.12.12, 16:48 CET

    Copyright (c) 2012 apitrary

"""
import os
from distutils.core import setup
from setuptools import find_packages
import sys


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
        'pytools/loggr_service/loggr.py',
        'pytools/trackr_service/trackr.py',
        'pytools/deployr_service/deployr.py',
        'archive/lib/mq/zmq/ioloop_env_subscriber.py',
        'archive/lib/mq/zmq/env_publisher.py'
    ]


setup(
    name='pytools',
    version='0.0.1',
    author='Hans-Gunther Schmidt',
    author_email='hgs@apitrary.com',
    description='pytools - apitrary python tool set',
    long_description=read('README.md'),
    url='http://apitrary.com',
    install_requires=read_requirements(),
    keywords='deployr buildr balancr loggr_service registr trackr apitrary application',
    packages=find_packages('pytools'),
    package_dir={'': 'pytools'},
    data_files=[
        (get_template_base_dir(), ['pytools/deployr_service/templates/genapi_base.tpl'])
    ],
    scripts=scripts_list()
)
