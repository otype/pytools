# -*- coding: utf-8 -*-
"""

    GenAPI

    Copyright (c) 2012 - 2013 apitrary

"""
from time import strftime, gmtime

def get_current_time_formatted():
    """
        Create a nice time stamp of the current time
    """
    return strftime('%d %b %Y %H:%M:%S +0000', gmtime())


def validate_user_agent(request):
    """
        Checks if a request has a User-agent set. If not
        we need to set a default string.
    """
    if 'User-Agent' not in request.headers:
        return 'UNKNOWN'
    else:
        return request.headers['User-Agent']
