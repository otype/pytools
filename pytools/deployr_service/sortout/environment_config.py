# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
from deployr_service.sortout.environments import ENVIRONMENT


# GLOBAL CONFIGURATION HASH
#
#
GLOBAL_CONF = {

    # TEST ENVIRONMENT
    #
    #
    ENVIRONMENT.STAGING: {
        # Name of this environment
        'NAME': ENVIRONMENT.STAGING,

        # Configuration file for deployr
        'DEPLOYR_CONFIG_FILE': 'deployr.conf',

        # SUPERVISORD HOST
        'SUPERVISORD_HOST': '127.0.0.1',

        # SUPERVISORD WEB PORT
        #
        # XML-RPC web API of a running supervisord.
        # NEEDS TO BE ACTIVATED IN THE CONFIGS!
        'SUPERVISORD_WEB_PORT': 9001,

        # Supervisor XML-RPC Credentials
        'SUPERVISOR_XML_RPC_USERNAME': 'UNSET',
        'SUPERVISOR_XML_RPC_PASSWORD': 'UNSET',

        # Contact XML-RPC on given address
        'SUPERVISOR_XML_RPC_SERVER_ADDRESS': 'http://127.0.0.1:9001/RPC2'
    },

    # DEV ENVIRONMENT
    #
    #
    ENVIRONMENT.DEV: {
        # Name of this environment
        'NAME': ENVIRONMENT.DEV,

        # Configuration file for deployr
        'DEPLOYR_CONFIG_FILE': 'deployr.conf',

        # SUPERVISORD HOST
        'SUPERVISORD_HOST': 'app1.dev.apitrary.net',

        # SUPERVISORD WEB PORT
        #
        # XML-RPC web API of a running supervisord.
        # NEEDS TO BE ACTIVATED IN THE CONFIGS!
        'SUPERVISORD_WEB_PORT': 9001,

        # Supervisor XML-RPC Credentials
        'SUPERVISOR_XML_RPC_USERNAME': 'UNSET',
        'SUPERVISOR_XML_RPC_PASSWORD': 'UNSET',

        # Contact XML-RPC on given address with given credentials
        'SUPERVISOR_XML_RPC_SERVER_ADDRESS': 'http://{}:{}@app1.dev.apitrary.net:9001/RPC2'.format(
            'UNSET', # USER NAME (see Chef recipe "supervisor" and role "pythonenv")
            'UNSET'       # PASSWORD  (see Chef recipe "supervisor" and role "pythonenv")
        )
    },

    # LIVE ENVIRONMENT
    #
    #
    ENVIRONMENT.LIVE: {
        # Name of this environment
        'NAME': ENVIRONMENT.LIVE,

        # Configuration file for deployr
        'DEPLOYR_CONFIG_FILE': '/etc/deployr/deployr.conf',

        # SUPERVISORD HOST
        'SUPERVISORD_HOST': '127.0.0.1',

        # SUPERVISORD WEB PORT
        #
        # XML-RPC web API of a running supervisord.
        # NEEDS TO BE ACTIVATED IN THE CONFIGS!
        'SUPERVISORD_WEB_PORT': 9001,

        # Supervisor XML-RPC Credentials
        'SUPERVISOR_XML_RPC_USERNAME': 'UNSET',
        'SUPERVISOR_XML_RPC_PASSWORD': 'UNSET',

        # Contact XML-RPC on given address with given credentials
        'SUPERVISOR_XML_RPC_SERVER_ADDRESS': 'http://{}:{}@127.0.0.1:9001/RPC2'.format(
            'UNSET', # USER NAME (see Chef recipe "supervisor" and role "pythonenv")
            'UNSET'      # PASSWORD  (see Chef recipe "supervisor" and role "pythonenv")
        )
    }
}
