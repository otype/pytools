# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
from pybuildr.handlers.base_handler import BaseHandler
from pybuildr.services.api_service import deploy, undeploy

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

        self.respond(payload=deploy(request_body=self.request.body))

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

        self.respond(payload={'UNDEPLOY': 'POST', 'status': undeploy(request_body=self.request.body)})
