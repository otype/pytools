# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import json
import logging
import uuid
from pybalancr.api.deploy import loadbalance_deploy
from pybalancr.api.undeploy import loadbalance_undeploy
from pybuildr.exceptions import RiakObjectNotFoundException, NoSuchApiFoundException
from pybuildr.services.api_base_service import ApiBaseService
from pydeployr.api.undeploy import undeploy_api
from pydeployr.api.deploy import deploy_api


class ApiService(ApiBaseService):
    """
        Provides service methods for pydeployr API
    """

    def __init__(self, riak_host, riak_pb_port, bucket_name, riak_rq, riak_wq):
        super(ApiService, self).__init__(riak_host, riak_pb_port, bucket_name, riak_rq, riak_wq)

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

    def fetch_all_by_app_host(self):
        """
            Fetch all APIs, sorted by app_host
        """
        entries = self.fetch_all()
        by_app_hosts = dict()
        for entry in entries:
            app_host = entry['data']['app_host']

            if app_host in by_app_hosts:
                app_host_entry = by_app_hosts[app_host]
            else:
                app_host_entry = []

            app_host_entry.append(entry['data'])
            by_app_hosts[app_host] = app_host_entry

        return by_app_hosts

    def fetch_by_app_host(self, app_host):
        """
            Fetch all APIs by app_host
        """
        entries = self.repository.search('app_host:{}'.format(app_host))
        by_app_hosts = dict()
        for entry in entries:
            app_host = entry['_data']['app_host']

            if app_host in by_app_hosts:
                app_host_entry = by_app_hosts[app_host]
            else:
                app_host_entry = []

            app_host_entry.append(entry['_data'])
            by_app_hosts[app_host] = app_host_entry

        return by_app_hosts

    def deploy(self, request_body):
        """
            Deploy an API from a given JSON request by calling pydeployr's API method
        """
        obj_to_store = self.read_json(request_body)
        self.validate_json(
            obj_to_store,
            ['api_id', 'api_key', 'entities', 'db_host', 'db_port', 'log_level', 'genapi_version']
        )

        deploy_result = deploy_api(
            api_id=obj_to_store['api_id'],
            api_key=obj_to_store['api_key'],
            entities=obj_to_store['entities'],
            db_host=obj_to_store['db_host'],
            db_port=obj_to_store['db_port'],
            genapi_version=obj_to_store['genapi_version'],
            log_level=obj_to_store['log_level']
        ).to_dict()
        logging.info('Received result from deploy job: {}'.format(deploy_result))

        db_result = self.repository.add(
            object_id=uuid.uuid1().hex,
            data={
                u'api_id': obj_to_store['api_id'],
                u'api_key': obj_to_store['api_key'],
                u'entities': obj_to_store['entities'],
                u'db_host': obj_to_store['db_host'],
                u'db_port': obj_to_store['db_port'],
                u'log_level': obj_to_store['log_level'],
                u'status': deploy_result['status'],
                u'genapi_version': deploy_result['genapi_version'],
                u'app_host': deploy_result['api_host'],
                u'app_port': deploy_result['api_port'],
                u'created_at': deploy_result['created_at']
            }
        )
        logging.info(
            "Received result from DB store: ID = {} -- DATA = {}".format(db_result._key, db_result.get_data()))

        if 'status' in db_result.get_data():
            assert db_result.get_data()['status'] == 0

        loadbalance_deploy_result = self.loadbalance_deploy(
            json.dumps(
                {
                    'api_id': obj_to_store['api_id'],
                    'api_host': deploy_result['api_host'],
                    'api_port': deploy_result['api_port']
                }
            )
        ).to_dict()

        deploy_result.update(loadbalance_deploy_result)
        logging.info('Merged result: {}'.format(deploy_result))
        return deploy_result

    def loadbalance_deploy(self, request_body):
        """
            Send deploy task to loadbalancer
        """
        obj_to_store = self.read_json(request_body)
        self.validate_json(obj_to_store, ['api_id', 'api_host', 'api_port'])

        loadbalance_deploy_result = loadbalance_deploy(
            api_id=obj_to_store['api_id'],
            api_host=obj_to_store['api_host'],
            api_port=obj_to_store['api_port']
        )
        logging.info("Loadbalance deploy result: {}".format(loadbalance_deploy_result.to_json()))
        return loadbalance_deploy_result

    def loadbalance_undeploy(self, request_body):
        """
            Remove loadbalancer configuration for a given API
        """
        obj_to_store = self.read_json(request_body)
        self.validate_json(obj_to_store, ['api_id'])

        loadbalance_undeploy_result = loadbalance_undeploy(api_id=obj_to_store['api_id'])
        logging.info('Loadbalance undeploy result: {}'.format(loadbalance_undeploy_result))
        return loadbalance_undeploy_result

    def redeploy(self, request_body):
        """
            Re-deploy an API by simply undeploying and deploying again.
        """
        obj_to_store = self.read_json(request_body)
        self.validate_json(obj_to_store, ['api_id'])

        db_obj = self.fetch_by_api_id(obj_to_store['api_id'])
        if db_obj is None or len(db_obj) == 0:
            raise NoSuchApiFoundException()

        logging.info('Received command to redeploy API ID:{}'.format(obj_to_store['api_id']))
        self.undeploy(api_id=obj_to_store['api_id'])    # TODO: BAD ONE HERE! Should make sure 'api_id' exists!
        self.deploy(request_body=request_body)

    def undeploy(self, api_id):
        """
            Undeploy an API from a given JSON request
        """
        logging.info('Received command to undeploy API ID:{}'.format(api_id))
        db_objects = self.fetch_by_api_id(api_id=api_id)

        if db_objects is None or len(db_objects) == 0:
            raise RiakObjectNotFoundException()

        logging.info("Ready to undeploy API:{}".format(api_id))
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

        logging.info("Ready to undeploy API:{} by host:{}".format(api['api_id'], api['app_host']))
        undeploy_result = undeploy_api(api_id=api['api_id'], api_host=api['app_host'])

        logging.info('Ready to undeploy API:{} from loadbalancer'.format(api['api_id']))
        loadbalance_undeploy_result = loadbalance_undeploy(api_id=api['api_id'])

        logging.debug('Deleting reference for API ID:{}'.format(api['api_id']))
        self.repository.remove(db_id).get_data()

        undeploy_result.update(loadbalance_undeploy_result)
        logging.info('Merged result: {}'.format(undeploy_result))
        return undeploy_result
