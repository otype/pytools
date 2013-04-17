# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 17.04.2013, 23:10 CET

    Copyright (c) 2012 - 2013 apitrary

"""
import logging
from blocking_message_tx import BlockingMessageTx
from pydeployr.conf.config_loader import ConfigLoader
from pydeployr.messages.loadbalance_update_confirmation_message import LoadbalanceUpdateConfirmationMessage
from pydeployr.messages.loadbalance_update_message import LoadbalanceUpdateMessage
from pydeployr.services import config_service


def loadbalance_update(api_id, api_host, api_port):
    loadbalance_update_message = LoadbalanceUpdateMessage(api_id=api_id, api_host=api_host, api_port=api_port)
    logging.debug("Received Loadbalance update message: {}".format(loadbalance_update_message.to_json()))

    config = ConfigLoader(config=config_service.load_configuration())
    message_tx = BlockingMessageTx(
        broker_host=config.rmq_broker_host,
        broker_port=config.rmq_broker_port,
        broker_user=config.rmq_broker_username,
        broker_password=config.rmq_broker_password
    )
    status = message_tx.send(message=loadbalance_update_message)
    logging.info(">>>>> status: {}".format(status))

    # TODO: Missing here the response (LoadbalanceUpdateConfirmationMessage) from lb_deployr (aka balancr)
    # TODO: This should maybe also go into celery

    loadbalance_update_confirmation_message = LoadbalanceUpdateConfirmationMessage(
        api_id=api_id,
        lb_host='some.host',
        lb_api_port=80,
        api_domainname='some.com'
    )

    logging.info(">>>>>>>>>> {}".format(loadbalance_update_confirmation_message.to_json()))

    # TODO: implement here

    return loadbalance_update_confirmation_message
