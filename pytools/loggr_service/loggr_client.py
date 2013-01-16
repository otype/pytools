# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import sys
import socket
from tornado.options import logging
from lib.zeromq.majordomo_client import MajorDomoClient
from loggr_service.log_message import LogMessage
from loggr_service.settings import ZMQ

class LoggrClient(object):
    """
        Loggr client. Provides simple log methods to send log messages to the
        Loggr service which stores all messages into MongoDB.
    """
    # Defined by MajorDomo! Should be inspected how to change that.
    service = ZMQ['SERVICE']

    def __init__(
            self,
            service_name,
            broker_address="tcp://localhost:5555",
            verbose=False,
            host=None
    ):
        """
            Init & connect
        """
        super(LoggrClient, self).__init__()
        self.zmq_connect_address = broker_address
        self.verbose = verbose
        self.message_counter = 0
        self.service_name = service_name

        if host is None:
            host = socket.gethostname()

        self.host = host
        self.connect()

    def connect(self):
        """
            Create the client connection the the Majordomo broker.
        """
        self.client = MajorDomoClient(self.zmq_connect_address, verbose=self.verbose)

    def _zlog(self, level, message):
        """
            Actual log sender! Sends the message through zmq to Loggr.
        """
        log_message = LogMessage(
            log_level=level,
            service_name=self.service_name,
            host_name=self.host,
            log_line=message
        )
        self.message_counter += 1
        self.client.send(service=self.service, request=log_message.as_json())
        self.client.recv()

    def info(self, message):
        """
            Sends an INFO-level message
        """
        self._zlog(level='INFO', message=message)

    def debug(self, message):
        """
            Sends a DEBUG-level message
        """
        self._zlog(level='DEBUG', message=message)

    def warning(self, message):
        """
            Sends a WARNING-level message
        """
        self._zlog(level='WARN', message=message)

    def error(self, message):
        """
            Sends an ERROR-level message
        """
        self._zlog(level='ERROR', message=message)


def main():
    log = LoggrClient(
        broker_address="tcp://localhost:5555",
        service_name='SampleLogClient'
    )
    for i in xrange(4000):
        try:
            log.info('an info message')
            log.debug('a debug message')
            log.warning('a warning message')
            log.error('an error message')
#            sleep(1.0)
        except KeyboardInterrupt:
            logging.warning("CTRL-C pressed, closing down ...")
            sys.exit(0)

if __name__ == '__main__':
    main()