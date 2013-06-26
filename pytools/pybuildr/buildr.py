# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 - 2013 apitrary

"""
import sys
import logging
import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.log import enable_pretty_logging
from tornado.options import define
from tornado.options import options
from pytools.pybuildr.handlers.api_handler import ApiHandler
from pytools.pybuildr.handlers.api_host_handler import ApiHostHandler
from pytools.pybuildr.handlers.api_stats_handler import ApiStatsHandler
from pytools.pybuildr.handlers.status_handler import StatusHandler

# Enable Tornado's pretty logging
enable_pretty_logging()

APP_DETAILS = {
    'name': 'pybuildr',
    'version': '0.2.1',
    'company': 'apitrary',
    'author': 'Hans-Gunther Schmidt',
    'author_email': 'hgs@apitrary.com',
    'support': 'http://apitrary.com/support',
    'contact': 'support@apitrary.com',
    'copyright': '2012 - 2013 apitrary.com'
}

APP_SETTINGS = {
    'cookie_secret': 'hie5oeyie7Oog6tohhai5ahzeexaequeidooch2ooqu2no0uafoh2OosoquahgahmaeChieng6iemei8',
    'xheaders': True
}

APP_SECRETS = {'X-API-KEY': 'gaebiRaiTh4iez8Ees4umaidooZ1ooNg6ohngeimahbaekahroh3xahjieleech6aevee7aiqua7mai9'}


def show_pre_commit_hook_warning():
    """
        Shows a message how to install the pre-commit hook for Riak KV buckets.
    """
    logging.info("*********************************************************")
    logging.info("*                                                       *")
    logging.info("* DO NOT FORGET TO INSTALL THE PRE-COMMIT HOOK:         *")
    logging.info("*                                                       *")
    logging.info("* riak_node> search-cmd install apitrary_base_buildr    *")
    logging.info("*                                                       *")
    logging.info("*********************************************************")


def main():
    """
        Run all steps and config checks, then start the server
    """
    define("port", default=9000, help="run on the given port", type=int)
    define("debug", default=False, help="Debugging flag", type=bool)
    define("riak_host", default='127.0.0.1', help="Riak database host", type=str)
    define("riak_pb_port", default=8087, help="Riak Protocol Buffer port", type=int)
    define("riak_rq", default=2, help="Riak READ QUORUM", type=int)
    define("riak_wq", default=2, help="Riak WRITE QUORUM", type=int)
    define("riak_bucket_name", default="apitrary_base_buildr", help="PyBuildr Riak bucket name", type=str)

    try:
        tornado.options.parse_command_line()
    except tornado.options.Error, e:
        sys.exit('ERROR: {}'.format(e))

    options_dict = dict(
        riak_host=options.riak_host,
        riak_pb_port=options.riak_pb_port,
        bucket_name=options.riak_bucket_name,
        riak_rq=options.riak_rq,
        riak_wq=options.riak_wq,
        app_secrets=APP_SECRETS
    )

    all_routes = [
        (r"/", StatusHandler, dict(app_details=APP_DETAILS)),
        (r"/v1/apis", ApiHandler, options_dict),
        (r"/v1/apis.json", ApiHandler, options_dict),
        (r"/v1/apis/([0-9a-zA-Z]+)", ApiHandler, options_dict),
        (r"/v1/apis/([0-9a-zA-Z]+).json", ApiHandler, options_dict),
        (r"/v1/apis/stats/([0-9a-zA-Z_]+)", ApiStatsHandler, options_dict),
        (r"/v1/apis/stats/([0-9a-zA-Z_]+).json", ApiStatsHandler, options_dict),
        (r"/v1/apis/by_host", ApiHostHandler, options_dict),
        (r"/v1/apis/by_host.json", ApiHostHandler, options_dict),
        (r"/v1/apis/by_host/([0-9a-zA-Z]+)", ApiHostHandler, options_dict),
        (r"/v1/apis/by_host/([0-9a-zA-Z]+).json", ApiHostHandler, options_dict),
    ]

    application = tornado.web.Application(handlers=all_routes, **APP_SETTINGS)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)

    show_pre_commit_hook_warning()
    logging.info('Starting Buildr on port:{}'.format(options.port))
    logging.info('Using RIAK host:{} on port:{}'.format(options.riak_host, options.riak_pb_port))

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logging.info('Process stopped by user interaction.')
    finally:
        tornado.ioloop.IOLoop.instance().stop()

# MAIN
#
#
if __name__ == "__main__":
    main()
