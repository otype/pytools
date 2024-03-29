# -*- coding: utf-8 -*-
"""

    loggr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
ZMQ = {
    'LOGGR_CONNECT_ADDRESS': "tcp://localhost:5555",   # All workers and clients connect to broker
    'LOGGR_BROKER_BIND_ADDRESS': "tcp://*:5555",   # Broker bind address
    'SERVICE': 'loggr'
}

MONGODB = {
    'HOST': '127.0.0.1'
}

DEBUG = False

LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'