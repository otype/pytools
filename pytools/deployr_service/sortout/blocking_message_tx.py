# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import sys
import json
import pika
from pika.exceptions import AMQPConnectionError
from pika.adapters.blocking_connection import BlockingConnection
from deployr_service.sortout.environments import RETURNCODE
from deployr_service.models.deploy_confirmation_message import DeployConfirmationMessage
from deployr_service.models.deploy_message import DeployMessage
from deployr_service.models.undeploy_confirmation_message import UndeployConfirmationMessage
from deployr_service.models.undeploy_message import UndeployMessage
from deployr_service.lib.errors import UnacceptableMessageException
from deployr_service.services import logging_service

#
# Logger
#
logger = logging_service.get_logger()


class BlockingMessageTx(object):
    """
        Creates a blocking message transmission object. Provide the necessary
        broker connection parameters and a message, then send a message.
    """

    # Defines the topic exchange
    topic_type = 'topic'

    # content type of each message
    default_content_type = 'application/json'

    # set broker parameter durable
    durable = True

    # set broker parameter auto_delete
    auto_delete = False

    # all messages should be persisted in the queue (= 2)
    default_delivery_mode = 2

    # list of accepted message types
    accepted_message_types = [
        DeployMessage,
        DeployConfirmationMessage,
        UndeployMessage,
        UndeployConfirmationMessage
    ]

    def __init__(self, config):
        """
            Initialize for message and broker parameters
        """
        self.config = config
        self.broker_host = self.config['BROKER_HOST']
        self.broker_port = int(self.config['BROKER_PORT'])
        self.username = self.config['BROKER_USER']
        self.password = self.config['BROKER_PASSWORD']

        self.credentials = pika.PlainCredentials(username=self.username, password=self.password)
        self.parameters = pika.ConnectionParameters(
            host=self.broker_host,
            port=self.broker_port,
            credentials=self.credentials
        )
        logger.debug('Broker host = \'{}\', Broker port = {}, Broker user = {}'.format(
            self.broker_host,
            self.broker_port,
            self.username
        ))

    def is_valid_message(self):
        """
            Check if our message is one of our accepted types
        """
        if type(self.message) not in self.accepted_message_types:
            return False
        return True

    def setup(self):
        """
            Establish connection to broker.
        """
        try:
            self.connection = BlockingConnection(self.parameters)
        except AMQPConnectionError, e:
            logger.error("Could not connect to Message broker!")
            logger.error("Broker connection params: {}".format(self.parameters))
            logger.error("Error: {}".format(e))
            logger.error("Exiting.")
            sys.exit(1)

        self.channel = self.connection.channel()
        logger.debug('Connection established to broker: {}'.format(self.broker_host))

    def setup_queue(self, queue_name):
        """
            Declaring exchange for sending the deployment confirmation messages
        """
        logger.debug('Declaring queue=\'{}\''.format(queue_name))
        self.channel.queue_declare(
            queue=queue_name,
            durable=self.durable,
            auto_delete=self.auto_delete
        )

    def encoded_message(self):
        """
            Encode the message into the right format before sending.
        """
        logger.debug('Encoding message: {}'.format(self.message.to_dict()))
        return json.dumps(self.message.to_dict())

    def publish(self, routing_key):
        """
            Publish the message to the queue
        """
        # set the routing key
        self.routing_key = routing_key

        # do we have a message?
        if not self.message:
            logger.error('Missing message to publish!')
            return RETURNCODE.OS_ERROR

        # encode the message into correct format
        msg = self.encoded_message()

        logger.info("Sending message: {}".format(msg))
        self.channel.basic_publish(
            exchange='',
            routing_key=self.routing_key,
            body=msg,
            properties=pika.BasicProperties(
                content_type=self.default_content_type,
                delivery_mode=self.default_delivery_mode
            )
        )
        return RETURNCODE.OS_SUCCESS

    def tear_down(self):
        """
            Close the connection to the broker.
        """
        self.connection.close()
        logger.debug('Connection to broker: {} closed'.format(self.broker_host))

    def send(self, message):
        """
            Send the message
        """
        # set the message
        self.message = message

        # check if we have a valid message
        if not self.is_valid_message():
            raise UnacceptableMessageException('Not an acceptable message type: {}'.format(type(self.message)))

        # 1. setup everything for sending
        self.setup()

        # 2. setup the queue
        self.setup_queue(self.message.queue)

        # 3. publish the message to the broker
        status = self.publish(self.message.routing_key)

        # 4. tear down the connection
        self.tear_down()

        logger.debug('Message sent.')
        return status
