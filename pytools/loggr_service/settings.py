# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
ZMQ = {
    'LOGGR_CONNECT_ADDRESS': "tcp://localhost:5555",   # ZMQ_SERVER is running locally (for now).
#    'LOGGR_BIND_ADDRESS': "tcp://*:5555",   # ZMQ_SERVER is running locally (for now).
    'TOPIC': '' # We should listen to everything (= "")
}

MONGODB = {
    'HOST': '127.0.0.1'
}

DEBUG = False