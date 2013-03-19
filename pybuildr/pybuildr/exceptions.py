# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
from tornado.web import HTTPError

class NoDictionaryException(BaseException):
    """
        Thrown when a received message is of unknown type
    """

    def __init__(self, message=None, *args, **kwargs):
        error_message = 'No dictionary provided'
        if message:
            error_message = message
        super(NoDictionaryException, self).__init__(error_message, *args, **kwargs)
        raise HTTPError(status_code=500, log_message=error_message)


class RiakObjectNotFoundException(BaseException):
    """
        Thrown when a received message is of unknown type
    """

    def __init__(self, message=None, *args, **kwargs):
        error_message = 'Object with given id not found'
        if message:
            error_message = message
        super(RiakObjectNotFoundException, self).__init__(error_message, *args, **kwargs)
        raise HTTPError(status_code=404, log_message=error_message)


class RiakObjectDuplicateFoundException(BaseException):
    """
        Thrown when a received message is of unknown type
    """

    def __init__(self, message=None, *args, **kwargs):
        error_message = 'Object with given id already exists. Content not modified.'
        if message:
            error_message = message
        super(RiakObjectDuplicateFoundException, self).__init__(error_message, *args, **kwargs)
        raise HTTPError(status_code=304, log_message=error_message)


class RiakObjectIdNotProvidedException(BaseException):
    """
        Thrown when an object ID was required but not provided
    """

    def __init__(self, message=None, *args, **kwargs):
        error_message = 'No object ID provided. Object ID required.'
        if message:
            error_message = message
        super(RiakObjectIdNotProvidedException, self).__init__(error_message, *args, **kwargs)
        raise HTTPError(status_code=400, log_message=error_message)
