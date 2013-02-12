# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 26.12.12, 18:14 CET
    
    Copyright (c) 2012 apitrary

"""
import json
import pika

class BlockingLogPublisher(object):
    """
        Blocking logging client based on PubSub. Logs all messages to our
        central logging server (and into MongoDB)
    """

    _exchange = 'base.exchange'
    _exchange_type = 'topic'

    def __init__(self, amqp_url, service_name):
        """
            Initialize the connection to RabbitMQ & setup the PubSub queue
        """
        self._url = amqp_url
        self._service_name = service_name
        self._stopping = False
        self._connect()

    def _connect(self):
        """
            Connect to rmq, declare an exchange with type 'topic'.
        """
        self._connection = pika.BlockingConnection(pika.URLParameters(self._url))
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=self._exchange, type=self._exchange_type)

    def send(self, log_level, message):
        """
            Send the log message
        """
        if self._stopping:
            return

        log_message = {'service': self._service_name, 'level': log_level, 'message': message}
        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=self._get_topic_key(log_level),
            body=json.dumps(log_message)
        )

    def _get_topic_key(self, log_level):
        if self._service_name == '':
            self._service_name = 'anonymous'

        if log_level == '':
            log_level = 'info'

        return "{}.{}".format(self._service_name, log_level)

    def close(self):
        """
            Close the connection
        """
        self._stopping = True
        self._connection.close()

    def info(self, message):
        self.send('INFO', message)

    def debug(self, message):
        self.send('DEBUG', message)

    def warning(self, message):
        self.send('WARNING', message)

    def error(self, message):
        self.send('ERROR', message)


def main():
    log_publisher = BlockingLogPublisher(
        amqp_url='amqp://guest:guest@localhost:5672/%2F',
        service_name='some.service'
    )
    #    log_publisher.send(log_level='INFO', message='testing log message')
    log_publisher.info(message='testing log message')
    log_publisher.close()


if __name__ == '__main__':
    main()