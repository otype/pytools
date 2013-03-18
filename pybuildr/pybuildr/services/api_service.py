# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import json
import logging
import tornado
from tornado import escape
from pybuildr.repositories.riak_repository import RiakRepository
from pydeployr.api.deploy import deploy_api
from pydeployr.api.undeploy import undeploy_api

class ApiService(object):
    """
        Provides service methods for pydeployr API
    """

    def __init__(self, riak_host, riak_pb_port, bucket_name, riak_rq, riak_wq):
        super(ApiService, self).__init__()
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
        logging.info("Retrieved new JSON task: {}".format(obj_to_store))
        return obj_to_store

    def fetch_all(self):
        """
            Fetch all deployed APIs from database
        """
        return self.repository.fetch_all()

    def fetch_api(self, api_id):
        """
            Fetch all entries with given API ID
        """
        return self.repository.search('api_id:{}'.format(api_id))

    def deploy(self, request_body):
        """
            Deploy an API from a given JSON request by calling pydeployr's API method
        """
        obj_to_store = self.read_json(request_body)
        self.validate_json(obj_to_store, ['api_id', 'api_key', 'entities', 'db_host'])

        deploy_result = deploy_api(
            api_id=obj_to_store['api_id'],
            api_key=obj_to_store['api_key'],
            entities=obj_to_store['entities'],
            db_host=obj_to_store['db_host']
        )
        logging.info('Received result from deploy job: {}'.format(deploy_result))

        db_result = self.repository.add(
            object_id=obj_to_store['api_id'],
            data={
                u'api_id': obj_to_store['api_id'],
                u'api_key': obj_to_store['api_key'],
                u'entities': obj_to_store['entities'],
                u'db_host': obj_to_store['db_host'],
                u'db_port': obj_to_store['db_port'],
                #                u'log_level': deploy_result['log_level'],
                #                u'environment': deploy_result['environment'],
                u'status': deploy_result['status'],
                u'genapi_version': deploy_result['genapi_version'],
                u'host': deploy_result['host'],
                u'port': deploy_result['port'],
                u'created_at': deploy_result['created_at']
            }
        )
        logging.info("Received result from DB store: ID = {} -- DATA = {}".format(db_result._key, db_result.get_data()))

        return deploy_result

    def redeploy(self, request_body):
        """
            Re-deploy an API by simply undeploying and deploying again.
        """
        self.undeploy(request_body=request_body)
        self.deploy(request_body=request_body)

    def undeploy(self, request_body):
        """
            Undeploy an API from a given JSON request
        """
        obj_to_store = self.read_json(request_body=request_body)
        self.validate_json(obj_to_store, ['api_id', 'app_host'])

        undeploy_result = undeploy_api(api_id=obj_to_store['api_id'], app_host=obj_to_store['app_host'])

        # find out on which host API is running

        # check if API is running

        # tell loadbalancer to de-register API

        # stop API on given host(-s)

        # remove API

        # delete supervisor config for API

        db_result = self.repository.remove(obj_to_store['api_id']).get_data()
        logging.info("Received result from DB store: {}".format(db_result))

        return {'UNDEPLOY': 'POST', 'status': undeploy_result, 'db_result': db_result}
