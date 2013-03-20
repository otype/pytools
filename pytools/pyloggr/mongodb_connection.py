# -*- coding: utf-8 -*-
"""

    loggr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
import logging
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from pyloggr.log_message import LogMessage

class MongoDBConnection(object):
    """
        Creates a connection to MongoDB
    """

    capped_collection_size = 10485760
    capped_collection_max = 10000

    def __init__(self, db_name='logging', db_host='127.0.0.1', db_port=27017):
        """
            Base initialization
        """
        super(MongoDBConnection, self).__init__()
        self.log = logging.getLogger(self.__class__.__name__)
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.max_pool_size = 10
        self.connect()

    def show_all_settings(self):
        """
            Simply display all settings
        """
        self.log.info("MongoDB host=%s" % self.db_host)
        self.log.info("MongoDB host=%r" % self.db_port)
        self.log.info("MongoDB database=%s" % self.db_name)

    def connect(self):
        """
            Create connection
        """
        self.connection = MongoClient(host=self.db_host, port=self.db_port, max_pool_size=self.max_pool_size)
        self.db = self.connection[self.db_name]
        self.show_all_settings()

    def create_db_collection(self, collection_name):
        """
            Create a capped collection for given collection name. Size is 10MB.
        """
        try:
            self.db.create_collection(
                name=collection_name,
                size=self.capped_collection_size,
                max=self.capped_collection_max,
                capped=True
            )
        except CollectionInvalid, e:
            self.log.debug("Capped Collection=%s already exists" % collection_name)

        self.collection = self.db[collection_name]

    def store_log(self, log_message):
        """
            Insert a given document (e.g. a log message) into MongoDB
        """
        if type(log_message) is not LogMessage:
            self.log.error("Invalid log message object!")
            return -1

        return self.collection.insert(log_message.as_dict())

