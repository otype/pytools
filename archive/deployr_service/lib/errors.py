# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""

class UnacceptableMessage(Exception):
    """Thrown when a received message is of unknown type"""

    def __init__(self, message, *args, **kwargs):
        super(UnacceptableMessage, self).__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        return self.message


class UnknownTaskType(Exception):
    """Thrown in case of an unknown task type passed via a message"""

    def __init__(self, message, *args, **kwargs):
        super(UnknownTaskType, self).__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        return self.message


class InvalidTaskType(Exception):
    """Thrown in case of an invalid task type passed via a message"""

    def __init__(self, message, *args, **kwargs):
        super(InvalidTaskType, self).__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        return self.message


class MissingAttribute(Exception):
    """Thrown in case of a missing attribute within a JSON object"""

    def __init__(self, message, *args, **kwargs):
        super(MissingAttribute, self).__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        return self.message


class FileNotFound(Exception):
    """Thrown in case of not being able to find a given file"""

    def __init__(self, message, *args, **kwargs):
        super(FileNotFound, self).__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        return self.message