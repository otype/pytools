# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import sys
from time import sleep
from tornado.options import enable_pretty_logging, logging
from deployr_service.messages.deploy_message import DeployMessage
from lib.zeromq.majordomo_client import MajorDomoClient

enable_pretty_logging()

msg = DeployMessage(
    api_id='MANUAL_TASK_DEPLOY_API_ID',
    db_host='riak1.dev.apitrary.net',
    db_port=8098,
    genapi_version=1,
    log_level='debug',
    entities=['jedis', 'wookies', 'stormtroopers'],
    api_key='suchasecretapikeyyouwouldneverguess'
)

class ZmqClient(object):
    def __init__(self, broker, verbose):
        super(ZmqClient, self).__init__()
        self.client = MajorDomoClient(broker=broker, verbose=verbose)

    def send(self, message):
        self.client.send('deployr', message)


def main():
#    verbose = '-v' in sys.argv
    client = ZmqClient(broker="tcp://localhost:5557", verbose=True)
    while True:
        try:
            client.send(msg.to_json())
            sleep(20.0)
        except KeyboardInterrupt:
            logging.info("Pressed CTRL-C. Killing.")
            sys.exit(0)

if __name__ == '__main__':
    main()