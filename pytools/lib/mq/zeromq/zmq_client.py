# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import logging
from time import sleep

import zmq

from lib.mq.zeromq.zeromq_config import REQUEST_RETRIES, LOG_FORMAT, RECONNECT_TIMEOUT, PPP_PING
from lib.mq.zeromq.zeromq_config import REQUEST_TIMEOUT
from lib.mq.zeromq.zmq_base import ZmqBase


class ZmqClient(ZmqBase):
    """
        Setup the ZeroMQ client.
    """

    def __init__(self, zmq_socket_type, server_endpoint, running_threads=1):
        """
            Setup the zeromq client.
        """
        super(ZmqClient, self).__init__(zmq_socket_type, server_endpoint, running_threads)
        self.log = logging.getLogger(self.__class__.__name__)

    def on_received_message(self, message):
        print "Received reply: {}".format(message)

    def run(self):
        """
            Runs the main loop.
        """
        retries_left = REQUEST_RETRIES
        while True:
            socks = dict(self.poller.poll(REQUEST_TIMEOUT))
            if socks.get(self.client) == zmq.POLLIN:
                reply = self.client.recv()
                if not reply:
                    self.log.warning('Empty message received. Discarding.')
                    continue

                self.log.debug("Received reply: {}".format(reply))
                retries_left = REQUEST_RETRIES
                self.on_received_message(reply)
                self.client.send(PPP_PING)
            else:
                self.log.error("No response from server, retrying ...")
                self.close()
                retries_left -= 1
                self.log.warning('Retries left = {}'.format(retries_left))
                if not retries_left:
                    self.log.error('Server seems to be offline! Sleeping for {} seconds.'.format(RECONNECT_TIMEOUT))
                    sleep(RECONNECT_TIMEOUT)
                    retries_left = REQUEST_RETRIES
                    self.log.info('Enough sleep! Continuing ...')

                self.log.debug('Re-establishing connection.')
                self.establish()
                self.client.send(PPP_PING)


def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    zmq_client = ZmqClient(zmq_socket_type=zmq.REQ, server_endpoint="tcp://localhost:5555")
    zmq_client.establish()
    try:
        zmq_client.run()
    except KeyboardInterrupt:
        zmq_client.close()

if __name__ == '__main__':
    main()