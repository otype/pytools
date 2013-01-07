# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import logging
from time import sleep

import zmq

from archive.lib.mq.zmq.zeromq_config import LOG_FORMAT
from lib.mq.zeromq.zmq_base import ZmqBase


class SimpleClient(ZmqBase):
    """
        Handles all calls to Trackr.
    """

    def __init__(self, zmq_socket_type, server_endpoint, running_threads=1):
        """
            Simple init
        """
        super(SimpleClient, self).__init__(zmq_socket_type, server_endpoint, running_threads)
        self.setup_context()

    def pub(self, message):
        self.connect_client()
        self.log.debug('Message: {}'.format(message))
        self.client.send(message)
        self.disconnect_client()

def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    simple_client = SimpleClient(zmq_socket_type=zmq.PUSH, server_endpoint="tcp://localhost:5555")
    try:
        while True:
            simple_client.pub('Emitting message')
            sleep(0.4)
    except KeyboardInterrupt:
        simple_client.terminate()

if __name__ == '__main__':
    main()