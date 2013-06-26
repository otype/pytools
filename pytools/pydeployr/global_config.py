# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 - 2013 apitrary

"""


class ENVIRONMENT:
    """
        Self-defined enumeration for environment names
    """
    STAGING = 'staging'
    DEV = 'dev'
    LIVE = 'live'


GLOBAL_CONF = {

    ENVIRONMENT.STAGING: {
        'NAME': ENVIRONMENT.STAGING,
        'DEPLOYR_CONFIG_FILE': 'deployr.conf',
        'SUPERVISORD_HOST': '127.0.0.1',
        'SUPERVISORD_WEB_PORT': 9001,   # XML-RPC web API of a running supervisord.
        'SUPERVISOR_XML_RPC_USERNAME': 'UNSET',
        'SUPERVISOR_XML_RPC_PASSWORD': 'UNSET',
        'SUPERVISOR_XML_RPC_SERVER_ADDRESS': 'http://127.0.0.1:9001/RPC2'
    },

    ENVIRONMENT.DEV: {
        'NAME': ENVIRONMENT.DEV,
        'DEPLOYR_CONFIG_FILE': 'deployr.conf',
        'SUPERVISORD_HOST': 'app1.dev.apitrary.net',
        'SUPERVISORD_WEB_PORT': 9001,
        'SUPERVISOR_XML_RPC_USERNAME': 'UNSET',
        'SUPERVISOR_XML_RPC_PASSWORD': 'UNSET',
        'SUPERVISOR_XML_RPC_SERVER_ADDRESS': 'http://{}:{}@app1.dev.apitrary.net:9001/RPC2'.format(
            'UNSET',      # USER NAME (see Chef recipe "supervisor" and role "pythonenv")
            'UNSET'       # PASSWORD  (see Chef recipe "supervisor" and role "pythonenv")
        )
    },

    ENVIRONMENT.LIVE: {
        'NAME': ENVIRONMENT.LIVE,
        'DEPLOYR_CONFIG_FILE': '/etc/deployr/deployr.conf',
        'SUPERVISORD_HOST': '127.0.0.1',
        'SUPERVISORD_WEB_PORT': 9001,
        'SUPERVISOR_XML_RPC_USERNAME': 'UNSET',
        'SUPERVISOR_XML_RPC_PASSWORD': 'UNSET',
        'SUPERVISOR_XML_RPC_SERVER_ADDRESS': 'http://{}:{}@127.0.0.1:9001/RPC2'.format(
            'UNSET',     # USER NAME (see Chef recipe "supervisor" and role "pythonenv")
            'UNSET'      # PASSWORD  (see Chef recipe "supervisor" and role "pythonenv")
        )
    }
}
