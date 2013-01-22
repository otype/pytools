# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 26.11.12, 22:40 CET
    
    Copyright (c) 2012 apitrary

"""
from deployr_service.deployr_base import DeployrBase

class FileSystemService(DeployrBase):

    @staticmethod
    def write_file(filename, content):
        """
            Write a given content to a file with given filename.
        """
        with open(filename, 'w') as f:
            f.write(content)
            f.write('\n')
