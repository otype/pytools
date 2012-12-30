# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import zmq
import logging
from lib.mq.zeromq.zeromq_config import LOG_FORMAT
from lib.mq.zeromq.zmq_client import ZmqClient

def start_consumer():
    zmq_client = ZmqClient(zmq_socket_type=zmq.REQ, server_endpoint="tcp://localhost:5555")
    zmq_client.establish()
    try:
        zmq_client.run()
    except KeyboardInterrupt:
        zmq_client.close()

def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    start_consumer()

if __name__ == '__main__':
    main()