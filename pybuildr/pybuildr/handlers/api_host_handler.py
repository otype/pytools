# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
from pybuildr.handlers.base_handler import BaseHandler
from pybuildr.services.api_service import ApiService

class ApiHostHandler(BaseHandler):
    """
        Handler for /apis/by_host
    """

    #noinspection PyMethodOverriding
    def initialize(self, riak_host, riak_pb_port, bucket_name, riak_rq, riak_wq):
        super(ApiHostHandler, self).initialize()
        self.api_service = ApiService(
            riak_host=riak_host,
            riak_pb_port=riak_pb_port,
            bucket_name=bucket_name,
            riak_rq=riak_rq,
            riak_wq=riak_wq
        )

    def get(self):
        """
            GET /apis                       -> get a map of APIs by app_host
            GET /apis?app_host=<app_host>   -> get a map of APIs for a single app host
        """
        self.require_accept_header()
        app_host = self.get_argument('app_host', None)
        if app_host is None:
            # No app_host provided -> Get all entries, sorted by host
            payload = self.api_service.fetch_all_by_app_host()
        else:
            payload = self.api_service.fetch_by_app_host(app_host=app_host)

        self.respond(payload=payload)
