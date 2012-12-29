# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""

# Request constants
#
#
REQUEST_TIMEOUT = 3000
REQUEST_RETRIES = 10

# Heartbeat constants
#
#
HEARTBEAT_LIVENESS = 10
HEARTBEAT_INTERVAL = 2
INTERVAL_INIT = 1
INTERVAL_MAX = 32
RECONNECT_TIMEOUT = 30.0

# Paranoid Pirate Protocol constants
#
#
PPP_READY = "\x01"           # Signals worker is ready
PPP_HEARTBEAT = "\x02"       # Signals worker heartbeat

# Connection constants
#
#
BUILDR_DEPLOYR_SERVER_ENDPOINT = "tcp://localhost:5555"

# LOG format
#
#
LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -20s %(funcName) -25s %(lineno) -5d: %(message)s'

