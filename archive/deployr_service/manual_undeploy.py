#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import uuid

import pika

from archive.deployr_service.messages.undeploy_message import UndeployMessage


msg = UndeployMessage(api_id='MANUAL_TASK_DEPLOY_API_ID')

class RmqBaseRpcPublisher(object):
    """
        RabbitMQ RPC Publisher
    """

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='deployr_rpc',
            properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id, ),
            body=str(message)
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response


if __name__ == "__main__":
    print ">>> Requesting {}".format(msg.to_json())
    rpc_client = RmqBaseRpcPublisher()
    print ">>> Sending call"
    response = rpc_client.call(msg.to_json())
    print ">>> Got: %s" % (response,)