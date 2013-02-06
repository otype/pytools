# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import sys
import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, logging
from tornado.options import options
from tornado.options import enable_pretty_logging
from buildr_service.handlers import StatusHandler
from buildr_service.handlers import DeployHandler
from buildr_service.handlers import UndeployHandler

enable_pretty_logging()

APP_DETAILS = {
    'name': 'buildr',
    'version': '0.0.1',
    'company': 'apitrary',
    'author': 'Hans-Gunther Schmidt',
    'author_email': 'hgs@apitrary.com',
    'support': 'http://apitrary.com/support',
    'contact': 'support@apitrary.com',
    'copyright': '2012 apitrary.com'
}

APP_SETTINGS = {
    'cookie_secret': 'eiFa5usoyohkahcoop0olahl0jaisi7yiec2Exievief9aethu',
    'xheaders': True
}

def main():
    """
        Run all steps and config checks, then start the server
    """
    define("port", default=9000, help="run on the given port", type=int)
    define("debug", default=False, help="Debugging flag", type=bool)

    options_dict = dict()
    all_routes = [
        (r"/", StatusHandler, dict(app_details=APP_DETAILS)),
        (r"/v1/deploy", DeployHandler, options_dict),
        (r"/v1/undeploy", UndeployHandler, options_dict),
    ]

    try:
        tornado.options.parse_command_line()
    except tornado.options.Error, e:
        sys.exit('ERROR: {}'.format(e))

    application = tornado.web.Application(handlers=all_routes, **APP_SETTINGS)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    logging.info('Starting Buildr on port {}'.format(options.port))
    tornado.ioloop.IOLoop.instance().start()


# MAIN
#
#
if __name__ == "__main__":
    main()
