# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 26.11.12, 22:40 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
import os

def write_file(filename, content):
    """
        Write a given content to a file with given filename.
    """
    with open(filename, 'w') as f:
        f.write(content)
        f.write('\n')

def delete_file(filename):
    """
        Delete file with given filename
    """
    if os.path.isfile(filename):
        os.remove(filename)