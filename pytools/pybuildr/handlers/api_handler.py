# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
from pytools.pybuildr.handlers.base_handler import BaseHandler
from pytools.pybuildr.services.api_service import ApiService


class ApiHandler(BaseHandler):
    """
        Handler for /apis
    """

    #noinspection PyMethodOverriding
    def initialize(self, riak_host, riak_pb_port, bucket_name, riak_rq, riak_wq, app_secrets):
        super(ApiHandler, self).initialize()
        self.api_service = ApiService(
            riak_host=riak_host,
            riak_pb_port=riak_pb_port,
            bucket_name=bucket_name,
            riak_rq=riak_rq,
            riak_wq=riak_wq
        )
        self.app_secrets = app_secrets
        self.api_key = app_secrets['X-API-KEY']

    def get(self, object_id=None):
        """
            GET /apis

            No object_id provided -> Get a list of all deployed APIs
            object_id provided -> Get information about API with given api_id
        """
        self.require_accept_header()
        self.matches_api_key(self.api_key)
        if object_id is None:
            # No object_id provided -> Get all entries
            payload = self.api_service.fetch_all()
        else:
            payload = self.api_service.fetch_by_api_id(api_id=object_id)

        self.respond(payload=payload)

    def post(self, *args, **kwargs):
        """
            POST /apis

            Deploy an API
        """
        self.require_accept_header()
        self.require_content_type()
        self.matches_api_key(self.api_key)
        self.respond(payload=self.api_service.deploy(request_body=self.request.body))

    def put(self, *args, **kwargs):
        """
            PUT /apis

            Re-deploy an API
        """
        self.require_accept_header()
        self.require_content_type()
        self.matches_api_key(self.api_key)
        self.respond(payload=self.api_service.redeploy(request_body=self.request.body))

    def delete(self, api_id):
        """
            DELETE /apis

            Undeploy an API
        """
        self.require_accept_header()
        self.matches_api_key(self.api_key)
        self.respond(payload=self.api_service.undeploy(api_id=api_id))
