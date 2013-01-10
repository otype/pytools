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
    TEST = 'test'
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

class TASKALIAS:
    """
        Task aliases (= names)
    """
    # Used for deploying GenAPIs
    DEPLOY_TASK = 'DEPLOY'

    # Used for responding back after a GenAPI deployment
    DEPLOY_CONFIRMATION_TASK = 'DEPLOY_CONFIRMATION'

    # Used for undeploying GenAPIs
    UNDEPLOY_TASK = 'UNDEPLOY'

    # Used for responding back after undeployment of a GenAPI
    UNDEPLOY_CONFIRMATION_TASK = 'UNDEPLOY_CONFIRMATION'

    # Used for registering a deployed GENAPI in the loadbalancer
    LOADBALANCE_UPDATE_TASK = 'LOADBALANCE_UPDATE'

    # Used for registering a deployed GENAPI in the loadbalancer
    LOADBALANCE_UPDATE_CONFIRMATION_TASK = 'LOADBALANCE_UPDATE_CONFIRMATION'

    # Used for deleting a deployed GENAPI in the loadbalancer
    LOADBALANCE_UNDEPLOY_TASK = 'LOADBALANCE_UNDEPLOY'

    # Used for deleting a deployed GENAPI in the loadbalancer
    LOADBALANCE_UNDEPLOY_CONFIRMATION_TASK = 'LOADBALANCE_UNDEPLOY_CONFIRMATION'