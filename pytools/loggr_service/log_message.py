# -*- coding: utf-8 -*-
"""

    <application_name>    

    created by hgschmidt on 29.12.12, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import datetime
import json
from loggr_service.errors import InvalidMessageLengthError

class LogMessage(object):
    """
        Defines a log message to write to MongoDB
    """

    # required message length (number of frames to receive). Depends on the
    # number of parameters received in the constructor.
    required_length = 5

    def __init__(
            self,
            log_level='',
            incident_time=datetime.datetime.utcnow(),
            service_name='',
            host_name='',
            log_line='',
            log_message=None
    ):
        """
            Base initialization
        """
        super(LogMessage, self).__init__()
        self.created_at = str(datetime.datetime.utcnow())

        if log_message is not None and len(log_message) != self.required_length:
            raise InvalidMessageLengthError('Provided length is {}, it should be {}.'.format(
                len(log_message), self.required_length)
            )

        if log_message is not None and len(log_message) == self.required_length:
            [log_level, incident_time, service_name, host_name, log_line] = log_message

        self.level = log_level
        self.incident_time = str(incident_time)
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
