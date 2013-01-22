# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""
import json
from time import strftime, gmtime


class EventMessage(object):
    """
        An Event message
    """

    def __init__(self, task_message ):
        """
            Setting the base variables for this message object
        """
        self.created_at = self.get_current_time_formatted()
        self.updated_at = self.get_current_time_formatted()
        self.task_message = task_message

    def get_current_time_formatted(self):
        """
            Create a nice time stamp of the current time
        """
        return strftime('%d %b %Y %H:%M:%S +0000', gmtime())

    def to_dict(self):
        """
            Return a dictionary from this object
        """
        return {
            'task_message': self.task_message.to_dict(),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def to_json(self):
        """
            Return a JSON object
        """
        return json.dumps(self.to_dict())
