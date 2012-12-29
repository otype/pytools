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
        'pytools/buildr/buildr.py',
        'pytools/loggr/loggr.py',
        'pytools/lib/mq/zeromq/zmq_client.py',
        'pytools/lpsim/lp_deploy.py',
#        'pytools/lpsim/zmq/zmq_client.py',
        'pytools/lpsim/zmq/zmq_queue.py',
        'pytools/lpsim/zmq/zmq_auto_queue.py',
        'pytools/lpsim/zmq/zmq_worker.py',
        'pytools/lib/mq/rabbitmq/base_async_continuous_publisher.py',
        'pytools/lib/mq/rabbitmq/base_async_consumer.py',
        'pytools/lib/mq/rabbitmq/base_async_combined.py'
    ]


setup(
    name='deployr',
    version='0.0.1',
    author='Hans-Gunther Schmidt',
    author_email='hgs@apitrary.com',
    description='pytools - apitrary python tool set',
    long_description=read('README.md'),
    url='http://apitrary.com',
    install_requires=read_requirements(),
    keywords='deployr buildr balancr loggr registr trackr apitrary application',
    packages=find_packages('pytools'),
    package_dir={'': 'pytools'},
    data_files=[],
    scripts=scripts_list()
)
