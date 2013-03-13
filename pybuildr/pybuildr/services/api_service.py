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
from pydeployr.api.deploy import deploy_api
from pydeployr.api.undeploy import undeploy_api

def validate_json(jobj, keys):
    """
        Validate a given JSON by checking for given keys
    """
    for key in keys:
        assert key in jobj


def read_json(request_body):
    """
        Read a request body and convert it into JSON
    """
    obj_to_store = json.loads(tornado.escape.utf8(request_body), 'utf-8')
    logging.info("Retrieved new JSON task: {}".format(obj_to_store))
    return obj_to_store


def deploy(request_body):
    """
        Deploy an API from a given JSON request
    """
    obj_to_store = read_json(request_body)

    validate_json(obj_to_store, ['api_id', 'api_key', 'entities', 'db_host'])

    result = deploy_api(
        api_id=obj_to_store['api_id'],
        api_key=obj_to_store['api_key'],
        entities=obj_to_store['entities'],
        db_host=obj_to_store['db_host']
    )
    logging.info('Received result from deploy job: {}'.format(result))
    return result


def undeploy(request_body):
    """
        Undeploy an API from a given JSON request
    """
    obj_to_store = read_json(request_body=request_body)

    validate_json(obj_to_store, ['api_id', 'app_host'])

    result = undeploy_api(api_id=obj_to_store['api_id'], app_host=obj_to_store['app_host'])

    # find out on which host API is running

    # check if API is running

    # tell loadbalancer to de-register API

    # stop API on given host(-s)

    # remove API

    # delete supervisor config for API

    return {'UNDEPLOY': 'POST', 'status': result}
