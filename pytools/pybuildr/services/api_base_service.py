# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import json
import logging
import tornado
from tornado import escape
from pytools.pybuildr.repositories.riak_repository import RiakRepository


class ApiBaseService(object):
    """
        Provides service methods for pydeployr API
    """

    def __init__(self, riak_host, riak_pb_port, bucket_name, riak_rq, riak_wq):
        super(ApiBaseService, self).__init__()
        self.repository = RiakRepository(
            riak_host=riak_host,
            riak_pb_port=riak_pb_port,
            bucket_name=bucket_name,
            riak_rq=riak_rq,
            riak_wq=riak_wq
        )


    def validate_json(self, jobj, keys):
        """
            Validate a given JSON by checking for given keys
        """
        for key in keys:
            assert key in jobj


    def read_json(self, request_body):
        """
            Read a request body and convert it into JSON
        """
        assert request_body
        obj_to_store = json.loads(tornado.escape.utf8(request_body), 'utf-8')
        assert obj_to_store
        logging.debug("Retrieved new JSON task: {}".format(obj_to_store))
        return obj_to_store
