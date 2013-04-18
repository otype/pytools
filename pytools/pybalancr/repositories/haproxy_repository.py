# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 27.11.12, 00:33 CET
    
    Copyright (c) 2012 apitrary

"""
import subprocess

def reload_haproxy():
    """
        Reload the haproxy server
    """
    return subprocess.call(['/etc/init.d/haproxy', 'reload'])

