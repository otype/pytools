# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 02.12.12, 20:01 CET
    
    Copyright (c) 2012 apitrary

"""

import tornado
from tornado.httpclient import HTTPRequest
from tornado import httpclient
from tornado.options import enable_pretty_logging
from deployr_service.event_reporter_service.event_reporter_config import EVENT_REPORTER_CONFIG
from deployr_service.lib.deployr_base import DeployrBase
from deployr_service.messages.deploy_message import DeployMessage
from deployr_service.messages.undeploy_message import UndeployMessage
from deployr_service.services.config_service import ConfigService

# Logger
enable_pretty_logging()

class EventReporter(DeployrBase):
    """
        Reports all events back to a defined API for later reference.
    """

    def __init__(self, config):
        """
            Initialize the EventReporter
        """
        super(EventReporter, self).__init__(config)
        self.env = EVENT_REPORTER_CONFIG[self.config['ENV']]
        self.loggr.debug("EventReporter env = {}".format(self.env))
        self.url = self.env['EVENT_REPORTER_URL']
        self.loggr.debug("EventReporter API BASE URL = {}".format(self.url))

        # Setup the Async HTTP client for calling Riak asynchronously
        self.http_client = tornado.httpclient.HTTPClient()

    def get_api_path_equivalent(self, message):
        if message is DeployMessage:
            return 'deploys'
        elif message is UndeployMessage:
            return 'undeploys'
        else:
            return 'deploys'

    def send(self, message):
        """
            Send a message to API URL
        """
        send_url = '{}/{}'.format(self.url, self.get_api_path_equivalent(message=message))
        self.loggr.debug("EventReporter API URL = {}".format(send_url))
        request = HTTPRequest(url=send_url)
        request.method = 'POST'
        request.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        request.body = message.to_json()

        response = None
        try:
            #noinspection PyTypeChecker
            response = self.http_client.fetch(request=request)
            self.loggr.debug("Response from Event Reporter: {}".format(response.body))
        except httpclient.HTTPError, e:
            self.loggr.error("Error when trying to contact Event Reporter! Error: {}".format(e))

        return response

##############################################################################
#
# FOR DEBUGGING
#
##############################################################################

if __name__ == '__main__':
    event_reporter = EventReporter(ConfigService.load_configuration())
    event_reporter.send('test')
