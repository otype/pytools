# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 26.12.12, 14:45 CET
    
    Copyright (c) 2012 apitrary

"""

class AsyncLogging(object):

    name = 'DEFAULT'

    def __init__(self, name=None):
        if name:
            self.name = name

    def info(self, msg):
        print("[%s]>>> INFO: %s" % (self.name, msg))
