# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""

# Request constants
#
#
REQUEST_TIMEOUT = 30000         # This should be longer than a normal worker task would take.
REQUEST_RETRIES = 5

# Heartbeat constants
#
#
HEARTBEAT_LIVENESS = 10
HEARTBEAT_INTERVAL = 7
INTERVAL_INIT = 1
INTERVAL_MAX = 32
RECONNECT_TIMEOUT = 30.0

# Paranoid Pirate Protocol constants
#
#
PPP_READY = "\x01"           # Signals worker is ready
PPP_HEARTBEAT = "\x02"       # Signals worker heartbeat
PPP_PING = 'ping'
PPP_PONG = 'pong'

# Connection constants
#
#
BUILDR_DEPLOYR_SERVER_ENDPOINT = "tcp://localhost:5555"

# LOG format
#
#
LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -20s %(funcName) -25s %(lineno) -5d: %(message)s'

