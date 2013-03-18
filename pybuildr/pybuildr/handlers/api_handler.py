# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
from pybuildr.handlers.base_handler import BaseHandler
from pybuildr.services.api_service import ApiService


class ApiHandler(BaseHandler):
    """
        Handler for /apis
    """

    #noinspection PyMethodOverriding
    def initialize(self, riak_host, riak_pb_port, bucket_name, riak_rq, riak_wq):
        super(ApiHandler, self).initialize()
        self.api_service = ApiService(
            riak_host=riak_host,
            riak_pb_port=riak_pb_port,
            bucket_name=bucket_name,
            riak_rq=riak_rq,
            riak_wq=riak_wq
        )

    def get(self, object_id=None):
        """
            GET /apis
        """
        self.require_accept_header()
        if object_id is None:
            # No object_id provided -> Get all entries
            payload = self.api_service.fetch_all()
        else:
            payload = self.api_service.fetch_api(api_id=object_id)

        self.respond(payload=payload)

    def post(self, *args, **kwargs):
        """
            POST /apis
        """
        self.require_accept_header()
        self.require_content_type()
        self.respond(payload=self.api_service.deploy(request_body=self.request.body))

    def put(self, *args, **kwargs):
        """
            PUT /apis
        """
        self.require_accept_header()
        self.require_content_type()
        self.respond(payload=self.api_service.redeploy(request_body=self.request.body))

    def delete(self, *args, **kwargs):
        """
            DELETE /apis
        """
        self.require_accept_header()
        self.respond(payload=self.api_service.undeploy(request_body=self.request.body))
