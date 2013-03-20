# -*- coding: utf-8 -*-
"""

    pybuildr

    by hgschmidt

    Copyright (c) 2012 - 2013 apitrary

"""

class HeaderService(object):
    """
        Base Processor settings
    """

    def __init__(self, headers):
        """
            Simple init method ...
        """
        super(HeaderService, self).__init__()
        self.headers = headers

    def has_valid_headers(self):
        """
            Requires all types:
            - Content-Type == application/json
            - Accept == application/json
        """
        return self.has_valid_content_type() and self.has_valid_accept_type()

    def has_valid_content_type(self):
        """
            Check if given request has content-type 'application/json'
        """
        keys = self.get_key_from_header('Content-Type')
        if keys is None:
            return False
        return 'application/json' in keys

    def has_valid_accept_type(self):
        """
            Check if given request has content-type 'application/json'
        """
        keys = self.get_key_from_header('Accept')
        if keys is None:
            return False
        return 'application/json' in keys

    def get_key_from_header(self, key_name):
        """
            Read a given key from header of given request
        """
        for k, v in self.headers.get_all():
            if k == key_name:
                return v
        return None
