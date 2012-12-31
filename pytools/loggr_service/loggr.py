# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import zmq
import logging
import sys
import tornado

from tornado.options import options
from tornado.options import define
from tornado.options import enable_pretty_logging
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
from loggr_service.log_message import LogMessage
from loggr_service.mongodb import MongoDBConnection

# Enable pretty logging
enable_pretty_logging()


class Loggr(object):
    """
        Starts the Loggr, a subscriber for all log messages.
    """

    def __init__(self, publisher_endpoint, mongodb_host='127.0.0.1', topic="", debug=False, running_threads=1):
        """
            Base initialization
        """
        super(Loggr, self).__init__()
        self.log = logging.getLogger(self.__class__.__name__)

        self.zmq_socket_type = zmq.SUB
        self.publisher_endpoint = publisher_endpoint
        self.topic = topic
        self.debug = debug
        self.running_threads = running_threads
        self.mongodb_host = mongodb_host

    def connect_db(self):
        """
            Connect to underlying MongoDB
        """
        self.mongodb = MongoDBConnection(db_host=self.mongodb_host)
        self.mongodb.create_capped_db_collection(collection_name='testing')

    def show_all_settings(self):
        """
            Simply display all settings
        """
        self.log.info("ZMQ socket type = {}".format(self.zmq_socket_type))
        topic = 'ALL' if self.topic == '' else self.topic
        self.log.info("Subscribed topic = {}".format(topic))
        self.log.info("Publisher endpoint = {}".format(self.publisher_endpoint))
        self.log.info("Starting context with thread count = {}".format(self.running_threads))
        debug_mode = "ON" if self.debug == True else "OFF"
        self.log.info("Debug mode = {}".format(debug_mode))

    def setup_subscriber(self):
        """
            Setup the zmq subscriber and connect to publisher
        """
        self.context = zmq.Context(self.running_threads)
        self.subscriber = self.context.socket(self.zmq_socket_type)
        self.subscriber.connect(self.publisher_endpoint)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, self.topic)
        self.register_callback_in_stream()

    def register_callback_in_stream(self):
        """
            Setup the input stream
        """
        self.stream = ZMQStream(self.subscriber)
        self.stream.on_recv(callback=self.callback)

    def callback(self, message):
        """
            Callback when message has arrived from publisher
        """
        if len(message) != 4:
            self.log.error("Invalid message length!")
            return

        log_message = LogMessage(log_message=message)
        mongo_id = self.mongodb.store_log(log_message=log_message)

        if self.debug:
            self.log.info("Stored as MongoID=%s" % mongo_id)

    def close(self):
        """
            Close zmq connection and context
        """
        self.subscriber.close()
        self.context.term()
        self.log.info("Connection closed.")

    def run(self):
        """
            Run via ioloop
        """
        self.show_all_settings()
        self.connect_db()
        self.setup_subscriber()
        self.register_callback_in_stream()

        try:
            ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            self.log.warning("CTRL-C pressed, closing down ...")
            ioloop.IOLoop.instance().stop()
            self.close()


def main():
    """
        Run all steps and config checks, then start the server
    """
    define("endpoint", default="tcp://localhost:5555", help="Publisher's address", type=str)
    define("topic", default="", help="Topic to subscribe", type=str)
    define("debug", default=False, help="Debugging flag", type=bool)
    define("db_host", default="127.0.0.1", help="MongoDB host", type=str)

    # This needs to be done, first, before we do anything with tornado.
    ioloop.install()

    try:
        tornado.options.parse_command_line()
    except tornado.options.Error, e:
        sys.exit('ERROR: {}'.format(e))

    topic = options.topic if options.topic else ""
    loggr = Loggr(
        publisher_endpoint=options.endpoint,
        topic=topic,
        mongodb_host=options.db_host,
        debug=options.debug
    )
    loggr.run()


if __name__ == "__main__":
    main()
