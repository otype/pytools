# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 26.12.12, 22:02 CET
    
    Copyright (c) 2012 apitrary

"""
import json
import logging
from archive.lib.mq.rabbitmq.base_async_continuous_publisher import BaseAsyncContinuousPublisher
from archive.lib.mq.rabbitmq.rabbitmq_config import LOGGING_EXCHANGE
from archive.lib.mq.rabbitmq.rabbitmq_config import LOGGING_EXCHANGE_TYPE

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger('async_log_client')

class AsyncLogClient(BaseAsyncContinuousPublisher):
    """
        Asynchronous log client! Send messages via broker to Loggr.
    """

    exchange = LOGGING_EXCHANGE
    exchange_type = LOGGING_EXCHANGE_TYPE

    INFO = 'INFO'
    DEBUG = 'DEBUG'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


    def __init__(self, amqp_url, service_name, debug=False):
        super(AsyncLogClient, self).__init__(
            amqp_url,
            exchange=LOGGING_EXCHANGE,
            exchange_type=LOGGING_EXCHANGE_TYPE,
            debug=debug
        )
        self.service_name = service_name

    def log(self, log_level, message):
        """
            Send the log message
        """
        log_message = {
            'service': self.service_name,
            'level': log_level,
            'message': message
        }
        print(json.dumps(log_message))

    def info(self, message):
        self.log(self.INFO, message)

    def debug(self, message):
        self.log(self.DEBUG, message)

    def warning(self, message):
        self.log(self.WARNING, message)

    def error(self, message):
        self.log(self.ERROR, message)


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    # TODO: Remove debug flag once going into production
    async_log_client = AsyncLogClient(
        amqp_url='amqp://guest:guest@localhost:5672/%2F',
        service_name='async_log_client',
        debug=True
    )
    try:
        async_log_client.run()

        async_log_client.info("Testing this info")
        async_log_client.warning("And this warning")
        async_log_client.error("And this error")

    except KeyboardInterrupt:
        async_log_client.stop()


if __name__ == '__main__':
    main()