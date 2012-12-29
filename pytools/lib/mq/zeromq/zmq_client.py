# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import zmq
import logging
from time import sleep
from lib.mq.zeromq.zeromq_config import REQUEST_RETRIES, LOG_FORMAT, RECONNECT_TIMEOUT
from lib.mq.zeromq.zeromq_config import REQUEST_TIMEOUT, BUILDR_DEPLOYR_SERVER_ENDPOINT
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

    def on_called(self):
        print "auto auto"

    def run(self):
        """
            Override this to implement the main loop.
        """
        retries_left = REQUEST_RETRIES
        sequence = 0

        while retries_left:
            sequence += 1
            request = str(sequence)
            self.log.info('Sending request={}'.format(request))
            self.client.send(request)

            expect_reply = True
            while expect_reply:
                socks = dict(self.poller.poll(REQUEST_TIMEOUT))
                if socks.get(self.client) == zmq.POLLIN:
                    reply = self.client.recv()
                    if not reply:
                        break
                    if int(reply) == sequence:
                        self.log.debug('Server replied OK (%s)' % reply)
                        retries_left = REQUEST_RETRIES
                        expect_reply = False
                        self.on_called()
                    else:
                        self.log.error('Malformed reply from server: %s' % reply)
                else:
                    self.log.error("No response from server, retrying ...")
                    self.close()
                    retries_left -= 1
                    self.log.info('Retries left = {}'.format(retries_left))
                    if not retries_left:
                        self.log.error('Server seems to be offline, sleeping for a while.')
                        sleep(RECONNECT_TIMEOUT)
                        retries_left = REQUEST_RETRIES

                    self.log.debug('Reconnecting')
                    self.establish()
                    self.client.send(request)


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    zmq_client = ZmqClient(zmq_socket_type=zmq.REQ, server_endpoint="tcp://localhost:5555")
    zmq_client.establish()
    try:
        zmq_client.run()
    except KeyboardInterrupt:
        zmq_client.close()

if __name__ == '__main__':
    main()