# -*- coding: utf-8 -*-
"""

    pybuildr

    Response object template

    Copyright (c) 2012 - 2013 apitrary

"""
import json


class Response(object):
    """
        Response template. Using get_data(), this method will deliver a
        response object with provided json object.
    """

    def __init__(self, result):
        """
            We need this value: result
        """
        self.result = result

    def __str__(self):
        """
            Provides a string representation of the Response
        """
        return 'Response(result="{}")'.format(self.result)

    def __repr__(self):
        """
            Provides a UTF-8 Response
        """
        return u'Response(result="{}")'.format(self.result)

    def get_data(self):
        """
            Provides a correctly encoding string of the response
        """
        return json.dumps(self.result).decode('unicode-escape')

