# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import tornado
import tornado.web
from tornado.options import logging
from exceptions import NoDictionaryException
from pybuildr.handler_helpers import get_current_time_formatted
from pybuildr.header_service import HeaderService
from pybuildr.response import Response

class BaseHandler(tornado.web.RequestHandler):
    """
        The most general handler class. Should be sub-classed by all consecutive
        handler classes.
    """

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.header_service = HeaderService(headers=request.headers)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", '*')
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Depth, User-Agent, X-File-Size, "
                                                        "X-Requested-With, X-Requested-By, If-Modified-Since, "
                                                        "X-File-Name, Cache-Control, X-Api-Key")

    def options(self, *args, **kwargs):
        """
            Returning back the list of supported HTTP methods
        """
        self.set_status(200)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", ', '.join([str(x) for x in self.SUPPORTED_METHODS]))
        self.write("ok")

    def respond(self, payload, status_code=200, status_message='OK'):
        """
            The general responder for ALL cases (success response, error response)
        """
        if payload is None:
            payload = {}

        if type(payload) not in [dict, list]:
            logging.error('payload is: {}'.format(payload))
            logging.error('payload is type: {}'.format(type(payload)))
            raise NoDictionaryException()

        response = Response(result=payload).get_data()

        self.set_status(status_code)
        self.set_header("X-Calvin", "You know, Hobbes, some days even my lucky rocketship underpants don’t help.")
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(response)
        if status_code in [200, 201, 204, 300]:
            self.finish()


    def write_error(self, status_code, **kwargs):
        """
            Called automatically when an error occurred. But can also be used to
            respond back to caller with a manual error.
        """
        if 'exc_info' in kwargs:
            logging.error(repr(kwargs['exc_info']))

        message = 'Something went seriously wrong! Maybe invalid resource? Ask your admin for advice!'
        if 'message' in kwargs:
            message = kwargs['message']

        self.respond(
            status_code=status_code,
            status_message=message,
            payload={"incident_time": get_current_time_formatted()}
        )

    def require_headers(self, require_api_key=True, require_content_type=False, require_accept=True):
        """
            Helper for checking the required header variables
        """
        if self.header_service.headers is None:
            return 1
            #        # Authorize request by enforcing API key (X-API-Key)
        #        if require_api_key:
        #            if self.header_service.get_key_from_header('X-Api-Key') != self.api_key:
        #                self.write_error(status_code=401, message='Invalid API Key.')
        #                return 1

        # Enforce application/json as Accept
        if require_accept:
            if not self.header_service.has_valid_accept_type():
                self.write_error(status_code=406, message='Accept is not application/json.')
                return 1

        # Enforce application/json as content-type
        if require_content_type:
            if not self.header_service.has_valid_content_type():
                self.write_error(status_code=406, message='Content-Type is not set to application/json.')
                return 1

        return 0
