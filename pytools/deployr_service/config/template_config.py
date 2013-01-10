# -*- coding: utf-8 -*-
"""

    deployr

    All settings here are necessary for the deployment step:
    Within the deployment a template file for supervisor is written into
    filesystem in order to successfully start a deployed Genapi.

    These values here are used by the deploy_api() method in task/actions/deploy_service.py.

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
from deployr_service.services import os_service

GENAPI_TEMPLATES_CONFIG = {

    'GENAPI_BASE': {
        #
        # Supervisor-related template for pygenapi
        #
        'GENAPI_BASE_TEMPLATE': 'genapi_base.tpl',

        #
        # The python executable to use for running Pygenapi (evaluated on start of pygenapi)
        #
        'GENAPI_PYTHON_EXEC': os_service.python_interpreter_path(),

        #
        # Where to find the Pygenapi start script (depending on the pygenapi setup.py installation)
        #
        'GENAPI_START_SCRIPT': '/usr/bin/genapi_runner.py',

        #
        # Home directory used for log files
        #
        'GENAPI_HOME_DIRECTORY': '/home/genapi',

        #
        # The user running the pygenapi
        #
        'GENAPI_USER': 'genapi'
    },

    'GENAPI_BACKENDS': {
        #
        # Name of the backends template
        #
        'GENAPI_BACKENDS_TEMPLATE': 'genapi_backends.tpl'
    },

    'GENAPI_FRONTENDS': {
        #
        # Name of the frontends template
        #
        'GENAPI_FRONTENDS_TEMPLATE': 'genapi_frontends.tpl'
    }
}