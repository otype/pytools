# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import logging
import zmq
from zmq.devices import monitored_queue
from lib.mq.zeromq.zeromq_config import LOG_FORMAT

class MonitorAutoQueue(object):
    """
        Uses ZeroMQ's Pre-defined Queue in order to create a queue with client and worker
        outlets + an additional outlet for a set of monitors.
    """

    def __init__(self, clients_endpoint, workers_endpoint, monitors_endpoint,
                 clients_socket_type=zmq.ROUTER, workers_socket_type=zmq.DEALER, monitors_socket_type=zmq.PUB,
                 running_threads=1):
        """
            Set all variables to establish the auto-queue
        """
        super(MonitorAutoQueue, self).__init__()
        self.clients_endpoint = clients_endpoint
        self.workers_endpoint = workers_endpoint
        self.monitors_endpoint = monitors_endpoint
        self.clients_socket_type = clients_socket_type
        self.workers_socket_type = workers_socket_type
        self.monitors_socket_type = monitors_socket_type
        self.running_threads = running_threads
        self.log = logging.getLogger(self.__class__.__name__)

    def setup_context(self):
        """
            Setup ZeroMQ context
        """
        self.log.info('Setting up context with threads count={}'.format(self.running_threads))
        self.context = zmq.Context(self.running_threads)

    def setup_sockets(self):
        """
            Setup all sockets for the queue.
        """
        self.clients = self.context.socket(self.clients_socket_type)
        self.workers = self.context.socket(self.workers_socket_type)
        self.monitors = self.context.socket(self.monitors_socket_type)

    def bind_all(self):
        """
            Bind all sockets to corresponding endpoints
        """
        self.clients.bind(self.clients_endpoint)
        self.workers.bind(self.workers_endpoint)
        self.monitors.bind(self.monitors_endpoint)

    def establish(self):
        """
            Establish everything to run the queue
        """
        self.log.info('Establishing context, sockets and bindings.')
        self.setup_context()
        self.setup_sockets()
        self.bind_all()
        self.log.info('Established!')

    def run(self):
        """
            Run this to start the zeromq queue
        """
        monitored_queue(self.clients, self.workers, self.monitors, in_prefix='in', out_prefix='out')

    def disconnect_clients(self):
        """
            Disconnecting client.
        """
        self.log.info('Closing socket connections')
        for client in [self.clients, self.workers, self.monitors]:
            client.setsockopt(zmq.LINGER, 0)
            client.close()

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
        self.disconnect_clients()
        self.terminate()
        del self.context


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    monitor_auto_queue = MonitorAutoQueue(
        clients_endpoint="tcp://*:5555",
        workers_endpoint="tcp://*:5556",
        monitors_endpoint="tcp://*:5557"
    )
    monitor_auto_queue.establish()
    try:
        monitor_auto_queue.run()
    except KeyboardInterrupt:
        monitor_auto_queue.close()

if __name__ == '__main__':
    main()