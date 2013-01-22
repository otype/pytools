# -*- coding: utf-8 -*-
"""

    trackr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import zmq
import json
import logging
from google_tracking import send_analytics_data

TRACKR_BIND_ADDRESS = "tcp://*:5555"

context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.bind(TRACKR_BIND_ADDRESS)

logging.basicConfig()
log = logging.getLogger('trackr')
log.setLevel(logging.DEBUG)

log.debug("Starting trackr on: {}".format(TRACKR_BIND_ADDRESS))
while True:
    # Running a first recv() ... the second one will actually get the message!
    receiver.recv()
    message = receiver.recv()
    try:
        tracking_data = json.loads(message)

        log.debug("Contacting Google with data: {}".format(tracking_data))
        send_analytics_data(
            remote_ip=tracking_data['remote_ip'],
            user_agent=tracking_data['user_agent'],
            api_id=tracking_data['api_id'],
            api_version=tracking_data['api_version'],
            env=tracking_data['env'],
            entity_name=tracking_data['entity_name'],
            http_method=tracking_data['http_method']
        )
    except ValueError, e:
        # Simply neglect this one ... strangely, all first recv() will cause an error!
        pass
