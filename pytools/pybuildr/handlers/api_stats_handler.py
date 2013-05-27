# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 27.05.2013, 22:33 CET

    Copyright (c) 2013 apitrary

"""
from pybuildr.handlers.base_handler import BaseHandler
from pybuildr.services.api_service import ApiService


class ApiStatsHandler(BaseHandler):
    """
        Handler for /apis/by_host
    """

    #noinspection PyMethodOverriding
    def initialize(self, riak_host, riak_pb_port, bucket_name, riak_rq, riak_wq, app_secrets):
        super(ApiStatsHandler, self).initialize()
        self.api_service = ApiService(
            riak_host=riak_host,
            riak_pb_port=riak_pb_port,
            bucket_name=bucket_name,
            riak_rq=riak_rq,
            riak_wq=riak_wq
        )
        self.app_secrets = app_secrets
        self.api_key = app_secrets['X-API-KEY']

    def get(self, bucket_name):
        """
            GET /apis/stats
        """
        self.require_accept_header()
        self.matches_api_key(self.api_key)
        resp = self.api_service.fetch_bucket_size(bucket_name=bucket_name)
        resp['bucket'] = bucket_name
        self.respond(payload=resp)
