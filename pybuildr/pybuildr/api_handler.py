# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import json
import tornado
from tornado import escape
from tornado.options import logging
from base_handler import BaseHandler
from pydeployr.api.deploy import deploy_api
from pydeployr.api.undeploy import undeploy_api

class ApiHandler(BaseHandler):
    """
        Handler for /apis
    """

    def get(self, *args, **kwargs):
        """
            GET /apis
        """
        if self.require_headers() == 1:
            return

        self.respond({'status': 'ok', 'method': 'GET'})

    def post(self, *args, **kwargs):
        """
            POST /apis
        """
        if self.require_headers() == 1:
            return

        # Load the JSON to see it's valid.
        obj_to_store = json.loads(tornado.escape.utf8(self.request.body), 'utf-8')
        logging.info(obj_to_store)

        result = deploy_api(
            api_id=obj_to_store['api_id'],
            api_key=obj_to_store['api_key'],
            entities=obj_to_store['entities'],
            db_host=obj_to_store['db_host']
        )
        logging.info('Received result from deploy job: {}'.format(result))
        self.respond(payload=result)

    def put(self, *args, **kwargs):
        """
            PUT /apis
        """
        if self.require_headers() == 1:
            return

        self.respond({'status': 'ok', 'method': 'PUT'})

    def delete(self, *args, **kwargs):
        """
            DELETE /apis
        """
        if self.require_headers() == 1:
            return

        # TODO: validate 'api_id' and 'app_host' in self.request.body

        # Load the JSON to see it's valid.
        obj_to_store = json.loads(tornado.escape.utf8(self.request.body), 'utf-8')
        logging.info("Retrieved new JSON task: {}".format(obj_to_store))

        result = undeploy_api(
            api_id=obj_to_store['api_id'],
            app_host=obj_to_store['app_host']
        )

        # find out on which host API is running

        # check if API is running

        # tell loadbalancer to de-register API

        # stop API on given host(-s)

        # remove API

        # delete supervisor config for API

        self.respond(payload={'UNDEPLOY': 'POST', 'status': result})
