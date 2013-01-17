# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import json
import logging
import datetime
from pymongo.errors import ConnectionFailure
import sys
from lib.zeromq.majordomo_worker import MajorDomoWorker
from loggr_service.log_message import LogMessage
from loggr_service.mongodb_connection import MongoDBConnection
from loggr_service.settings import ZMQ

class LoggrManager(object):
    """
        Starts the Loggr.
    """

    def __init__(self, loggr_broker, mongodb_host='127.0.0.1', service_name=ZMQ['SERVICE'], debug=False):
        """
            Base initialization
        """
        super(LoggrManager, self).__init__()
        self.log = logging.getLogger(self.__class__.__name__)
        self.loggr_broker = loggr_broker
        self.mongodb_host = mongodb_host
        self.service_name = service_name
        self.debug = debug

    def connect_db(self):
        """
            Connect to underlying MongoDB
        """
        try:
            self.mongodb = MongoDBConnection(db_host=self.mongodb_host)
            self.mongodb.create_capped_db_collection(collection_name='testing')
        except ConnectionFailure, e:
            self.log.error("MongoDB connection failed! Maybe you are not running mongod?")
            self.log.error("Error: {}".format(e))
            sys.exit(1)

    def show_all_settings(self):
        """
            Simply display all settings
        """
        self.log.info("Loggr ZMQ Broker address = {}".format(self.loggr_broker))
        debug_mode = "ON" if self.debug == True else "OFF"
        self.log.info("Debug mode = {}".format(debug_mode))

    def setup_worker(self):
        """
            Setup the zmq subscriber and connect to publisher
        """
        self.worker = MajorDomoWorker(
            broker=self.loggr_broker,
            service=self.service_name,
            verbose=self.debug
        )

    def store(self, message):
        """
            Callback when message has arrived from publisher
        """
        json_message = json.loads(message)

        log_message = LogMessage(
            log_level=json_message['level'],
            daemon_name=json_message['service'],
            created_at=json_message['created_at'],
            incident_time=json_message['incident_time'],
            host_name=json_message['host'],
            log_line=json_message['message']
        )
        mongo_id = self.mongodb.store_log(log_message=log_message)

        if self.debug:
            self.log.info("Stored as MongoID=%s" % mongo_id)

    def close(self):
        """
            Close the connection
        """
        self.worker.destroy()

    def run(self, interval_minutes=30):
        """
            Run via ioloop
        """
        self.show_all_settings()
        self.connect_db()
        self.setup_worker()

        try:
            reply = None
            counter = 0
            start = datetime.datetime.now()
            while True:
                request = self.worker.recv(reply)
                if request is None:
                    break # Worker was interrupted
                reply = request
                self.store(request[0])

                counter += 1
                delta = datetime.timedelta(minutes=interval_minutes)
                if start < (datetime.datetime.now() - delta):
                    self.log.info("Processed {counter} requests in last {delta}h.".format(
                        counter=counter,
                        delta=delta
                    ))
                    counter = 0
                    start = datetime.datetime.now()
        except KeyboardInterrupt:
            self.log.warning("CTRL-C pressed, closing down ...")
            self.close()
