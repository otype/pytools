# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 26.11.12, 23:33 CET
    
    Copyright (c) 2012 apitrary

"""

class ENVIRONMENT:
    """
        Self-defined enumeration for environment names
    """
    STAGING = 'staging'
    DEV = 'dev'
    LIVE = 'live'

class RETURNCODE:
    """
        All return codes
    """
    OS_SUCCESS = 0
    OS_ERROR = 1
    OS_MISUSE_ERROR = 2
    OS_CANNOT_INVOKE_COMMAND_ERROR = 126
    OS_COMMAND_NOT_FOUND_ERROR = 127
    OS_INVALID_ARGUMENT = 128
