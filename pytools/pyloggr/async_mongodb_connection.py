# -*- coding: utf-8 -*-
"""

    loggr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
import asyncmongo

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

