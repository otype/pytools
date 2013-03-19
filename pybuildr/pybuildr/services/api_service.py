# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import json
import logging
import uuid
import tornado
from tornado import escape
from pybuildr.exceptions import RiakObjectNotFoundException
from pybuildr.repositories.riak_repository import RiakRepository
from pydeployr.api.undeploy import undeploy_api
from pydeployr.api.deploy import deploy_api


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

    def fetch_by_api_id(self, api_id):
        """
            Fetch all entries with given API ID
        """
        return self.repository.search('api_id:{}'.format(api_id))

    def fetch_by_api_id_and_app_host(self, api_id, app_host):
        """
            Fetch all APIs by API ID and APP_HOST
        """
        return self.repository.search('api_id:{} AND app_host:{}'.format(api_id, app_host))

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
            object_id=uuid.uuid1().hex,
            data={
                u'api_id': obj_to_store['api_id'],
                u'api_key': obj_to_store['api_key'],
                u'entities': obj_to_store['entities'],
                u'db_host': obj_to_store['db_host'],
                u'db_port': obj_to_store['db_port'],
                u'status': deploy_result['status'],
                u'genapi_version': deploy_result['genapi_version'],
                u'app_host': deploy_result['host'],
                u'app_port': deploy_result['port'],
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
        self.validate_json(obj_to_store, ['api_id'])

        if 'app_host' in obj_to_store:
            # Both api_id and app_host have been provided -> Only search this particular API
            db_objects = self.fetch_by_api_id_and_app_host(obj_to_store['api_id'], obj_to_store['app_host'])
        else:
            # Only api_id has been provided -> get ALL running instances of this API
            db_objects = self.fetch_by_api_id(api_id=obj_to_store['api_id'])

        if db_objects is None or len(db_objects) == 0:
            raise RiakObjectNotFoundException()

        undeploy_result = []
        for entry in db_objects:
            undeploy_result.append(self.undeploy_api_by_host(entry))

        return {'status': undeploy_result}

    def undeploy_api_by_host(self, db_object):
        """
            Undeploy a single API on given app host
        """
        self.validate_json(db_object, ['_id', '_data'])
        api = db_object['_data']
        db_id = db_object['_id']

        logging.info('Undeploying API with ID:{} on APP_HOST:{}'.format(api['api_id'], api['app_host']))
        undeploy_result = undeploy_api(api_id=api['api_id'], app_host=api['app_host'])

        # TODO: find out on which host API is running
        # TODO: check if API is running
        # TODO: tell loadbalancer to de-register API
        # TODO: stop API on given host(-s)
        # TODO: remove API
        # TODO: delete supervisor config for API

        logging.info('Deleting reference for API ID:{}'.format(api['api_id']))
        self.repository.remove(db_id).get_data()

        return undeploy_result
