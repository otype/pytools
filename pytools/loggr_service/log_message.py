# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import datetime
import json

class LogMessage(object):
    """
        Defines a log message to write to MongoDB
    """

    def __init__(self, log_level='', service_name='', host_name='', log_line='', log_message=None):
        """
            Base initialization
        """
        super(LogMessage, self).__init__()
        self.created_at = datetime.datetime.utcnow()

        if log_message is not None and len(log_message) == 4:
            [log_level, service_name, host_name, log_line] = log_message

        self.level = log_level
        self.service = service_name
        self.host = host_name
        self.message = log_line

    def as_dict(self):
        """
            Return this object as dictionary
        """
        return self.__dict__

    def as_json(self):
        """
            Return this object as JSON
        """
        return json.dumps(self.__dict__)
