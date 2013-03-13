# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""

class NoDictionaryException(BaseException):
    """
        Thrown when a received message is of unknown type
    """

    def __init__(self, message=None, *args, **kwargs):
        error_message = 'No dictionary provided!'
        if message:
            error_message = message
        super(NoDictionaryException, self).__init__(error_message, *args, **kwargs)
