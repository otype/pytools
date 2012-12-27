# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 26.12.12, 14:22 CET
    
    Copyright (c) 2012 apitrary

"""
import uuid
import pika

class BlockingRPCPublisher(object):
    """
        Simple RPC via RabbitMQ
    """

    def __init__(self, amqp_url, rpc_queue):
        """
            Initialize broker address and queue name
        """
        self._stopping = False
        self._url = amqp_url
        self.rpc_queue = rpc_queue
        self.connect()

    def connect(self):
        """
            Connect to RabbitMQ
        """
        self._connection = pika.BlockingConnection(pika.URLParameters(self._url))
        self._channel = self._connection.channel()
        self.create_queue()

    def create_queue(self):
        """
            Declare and consume from exclusive queue
        """
        result = self._channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.consume()

    def consume(self):
        """
            Consume from queue
        """
        self._channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        """
            Callback for response
        """
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, msg):
        """
            Call the remote procedure
        """
        if self._stopping:
            return

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self._channel.basic_publish(
            exchange='',
            routing_key=self.rpc_queue,
            properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id, ),
            body=msg
        )
        while self.response is None:
            self._connection.process_data_events()
        return self.response

    def close(self):
        """
            Close the connection
        """
        self._stopping = True
        self._connection.close()
