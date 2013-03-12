# -*- coding: utf-8 -*-
"""

    loggr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""

class InvalidMessageLengthError(Exception):
    """
        Thrown when a received message is of unknown type
    """

    def __init__(self, message, *args, **kwargs):
        """
            Log the message
        """
        super(InvalidMessageLengthError, self).__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        """
            Message as string
        """
        return self.message

