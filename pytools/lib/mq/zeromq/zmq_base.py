# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import logging
import zmq


class ZmqBase(object):
    """
        Base class for initiating zeromq connections.
    """

    def __init__(self, zmq_socket_type, server_endpoint, running_threads=1):
        """
            Setup the context and the socket type.
        """
        super(ZmqBase, self).__init__()
        self.zmq_socket_type = zmq_socket_type
        self.server_endpoint = server_endpoint
        self.running_threads = running_threads
        self.log = logging.getLogger(self.__class__.__name__)

    def setup_context(self):
        """
            Setup ZeroMQ context
        """
        self.log.info('Setting up context with threads count={}'.format(self.running_threads))
        self.context = zmq.Context(self.running_threads)

    def setup_poller(self):
        """
            Setup poller.
        """
        self.log.info('Setting up poller.')
        self.poller = zmq.Poller()

    def establish(self):
        """
            Connect! Can be used for initial connection establishment.
        """
        self.log.info('Connecting to endpoint={}'.format(self.server_endpoint))
        self.setup_context()
        self.setup_poller()
        self.connect_client()
        self.register_poll()
        self.log.info('Connected!')

    def connect_client(self, server_endpoint=None):
        """
            Connect to given server endpoint with pre-defined zmq socket type
        """
        if server_endpoint:
            self.log.info('Setting new server endpoint={}'.format(server_endpoint))
            self.server_endpoint = server_endpoint

        self.log.info('Establishing socket type={}'.format(self.zmq_socket_type))
        self.client = self.context.socket(self.zmq_socket_type)
        self.log.info('Connecting to server={}'.format(self.server_endpoint))
        self.client.connect(self.server_endpoint)

    def register_poll(self):
        """
            Setup the poller
        """
        self.log.info('Registering poller={}'.format(zmq.POLLIN))
        self.poller.register(self.client, zmq.POLLIN)

    def unregister_poller(self):
        """
            De-register the poller
        """
        self.log.info('De-registering poller.')
        self.poller.unregister(self.client)

    def run(self):
        """
            Override this to implement the main loop.
        """
        pass

    def on_called(self):
        """
            Override this method to run things in the mail loop.
        """
        pass

    def disconnect_client(self):
        """
            Disconnecting client.
        """
        self.log.info('Closing client connection')
        self.client.setsockopt(zmq.LINGER, 0)
        self.client.close()

    def terminate(self):
        """
            Disconnect from socket, destroy context.
        """
        self.log.info('Terminating context.')
        self.context.term()

    def close(self):
        """
            Close the whole connection.
        """
        self.log.info('Tearing down the connection and context.')
        self.unregister_poller()
        self.disconnect_client()
        self.terminate()
        del self.context
