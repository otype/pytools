# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import json
import logging
import asyncmongo
import datetime
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

class AsyncMongoDBConnection(object):
    """
        Creates an asynchronous connection to MongoDB
    """

    def __init__(self, pool_id='apylogs', db_name='logging', db_host='127.0.0.1', db_port=27017):
        """
            Base initialization
        """
        super(AsyncMongoDBConnection, self).__init__()
        self.pool_id = pool_id
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.max_cached = 10
        self.max_connections = 50

    def connect(self):
        """
            Connect to MongoDB
        """
        self._db = asyncmongo.Client(
            pool_id=self.pool_id,
            host=self.db_host,
            port=self.db_port,
            maxcached=self.max_cached,
            maxconnections=self.max_connections,
            dbname=self.db_name
        )

    @property
    def db(self):
        """
            Provides eg. self.db.users.find() ...
        """
        if not hasattr(self, '_db'):
            self.connect()
        return self._db


class MongoDBConnection(object):
    """
        Creates a connection to MongoDB
    """

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

    def create_capped_db_collection(self, collection_name):
        """
            Create a capped collection for given collection name. Size is 10MB.
        """
        try:
            self.db.create_collection(name=collection_name, size=10485760, max=10000, capped=True)
        except CollectionInvalid, e:
            self.log.debug("Capped Collection=%s already exists" % collection_name)

        self.collection = self.db[collection_name]

    def store_log(self, log_level, service_name, host_name, log_line):
        """
            Insert a given document (e.g. a log message) into MongoDB
        """
        log_message = LogMessage(
            log_level=log_level,
            service_name=service_name,
            host_name=host_name,
            message=log_line
        )
        return self.collection.insert(log_message.as_dict())


class LogMessage(object):
    """
        Defines a log message to write to MongoDB
    """

    def __init__(self, log_level, service_name, host_name, message):
        """
            Base initialization
        """
        super(LogMessage, self).__init__()
        self.created_at = datetime.datetime.utcnow()
        self.level = log_level
        self.service = service_name
        self.host = host_name
        self.message = message

    def as_dict(self):
        """
            Return this object as dictionary
        """
        return self.__dict__

    def as_json(self):
        """
            Return this object as JSON
        """
        return json.dumps(self.__dict__)
