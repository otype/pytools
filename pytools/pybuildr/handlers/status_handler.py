# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
import tornado
import tornado.web
from tornado import gen
from pybuildr.handlers.base_handler import BaseHandler


class StatusHandler(BaseHandler):
    """
        Show status of buildr
    """

    def __init__(self, application, request, app_details, **kwargs):
        super(StatusHandler, self).__init__(application, request, **kwargs)
        self.app_details = app_details

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, *args, **kwargs):
        """
            Provides a basic hash with information for this app.
        """
        self.require_accept_header()
        self.write({'info': self.app_details, 'status': 'OK'})
        self.finish()
