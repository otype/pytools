# -*- coding: utf-8 -*-
"""

    pybuildr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import sys
import json
import logging
import pika
from pika import BlockingConnection
from pika.exceptions import AMQPConnectionError
from pybuildr.returncodes import RETURNCODE


class BlockingMessageTx(object):
    """
        Creates a blocking message transmission object. Provide the necessary
        broker connection parameters and a message, then send a message.
    """

    # all messages should be persisted in the queue (= 2)
    default_delivery_mode = 2

    def __init__(self, broker_host, broker_port, broker_user, broker_password):
        """
            Initialize for message and broker parameters
        """
        self.broker_host = broker_host
        self.broker_port = int(broker_port)
        self.username = broker_user
        self.password = broker_password

        self.credentials = pika.PlainCredentials(username=self.username, password=self.password)
        self.parameters = pika.ConnectionParameters(
            host=self.broker_host,
            port=self.broker_port,
            credentials=self.credentials
        )
        logging.debug('Broker host = \'{}\', Broker port = {}, Broker user = {}'.format(
            self.broker_host,
            self.broker_port,
            self.username
        ))

    def setup(self):
        """
            Establish connection to broker.
        """
        try:
            self.connection = BlockingConnection(self.parameters)
        except AMQPConnectionError, e:
            logging.error("Could not connect to Message broker!")
            logging.error("Broker connection params: {}".format(self.parameters))
            logging.error("Error: {}".format(e))
            # TODO: Remove this as soon as possible
            logging.error("Exiting.")
            sys.exit(1)

        self.channel = self.connection.channel()
        logging.debug('Connection established to broker: {}'.format(self.broker_host))

    def setup_queue(self, queue_name):
        """
            Declaring exchange for sending the deployment confirmation messages
        """
        logging.debug('Declaring queue=\'{}\''.format(queue_name))
        self.channel.queue_declare(
            queue=queue_name,
            durable=True,
            auto_delete=False
        )

    def encoded_message(self):
        """
            Encode the message into the right format before sending.
        """
        logging.debug('Encoding message: {}'.format(self.message.to_dict()))
        return json.dumps(self.message.to_dict())

    def publish(self, routing_key):
        """
            Publish the message to the queue
        """
        self.routing_key = routing_key

        if not self.message:
            logging.error('Missing message to publish!')
            return RETURNCODE.OS_ERROR

        msg = self.encoded_message()

        logging.info("Sending message: {}".format(msg))
        self.channel.basic_publish(
            exchange='',
            routing_key=self.routing_key,
            body=msg,
            properties=pika.BasicProperties(
                content_type='application/json',
                delivery_mode=self.default_delivery_mode
            )
        )
        return RETURNCODE.OS_SUCCESS

    def tear_down(self):
        """
            Close the connection to the broker.
        """
        self.connection.close()
        logging.debug('Connection to broker: {} closed'.format(self.broker_host))

    def send(self, message):
        """
            Send the message
        """
        self.message = message
        self.setup()
        self.setup_queue(self.message.queue)
        status = self.publish(self.message.routing_key)
        self.tear_down()
        logging.debug('Message sent.')
        return status

