# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import sys
from deployr_service.models.blocking_message_tx import BlockingMessageTx
from deployr_service.models.deploy_message import DeployMessage
from deployr_service.services import logging_service, deployr_config_service

#
# Logger
#
logger = logging_service.get_logger()

msg = DeployMessage(
    api_id='MANUAL_TASK_DEPLOY_API_ID',
    db_host='riak1.dev.apitrary.net',
    db_port=8098,
    genapi_version=1,
    log_level='debug',
    entities=['jedis', 'wookies', 'stormtroopers'],
    api_key='suchasecretapikeyyouwouldneverguess'
)

# Load the global configuration from config file
config = deployr_config_service.load_configuration()

def send(host, message):
    """
        Simply send the message
    """
    config['BROKER_HOST'] = host
    message_tx = BlockingMessageTx(config=config)
    message_tx.send(message=message)

# MAIN
#
#
if __name__ == '__main__':
    host = (len(sys.argv) > 1) and sys.argv[1] or '127.0.0.1'
    logger.info('Connecting to broker: {}'.format(host))

    logger.info('Sending message from manual task deploy script')
    send(host=host, message=msg)
