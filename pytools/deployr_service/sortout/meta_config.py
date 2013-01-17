# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
from deployr_service.lib.singleton_type import SingletonType

class MetaConfig(object):
    """
        Config SINGLETON class
    """
    __metaclass__ = SingletonType

    def __init__(self):
        super(MetaConfig, self).__init__()


