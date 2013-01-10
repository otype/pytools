# -*- coding: utf-8 -*-
"""

    deployr

    by hgschmidt

    Copyright (c) 2012 apitrary

"""

class UnacceptableMessageException(Exception):
    """
        Thrown when a received message is of unknown type
    """

    def __init__(self, message, *args, **kwargs):
        """
            Log the message
        """
        super(UnacceptableMessageException, self).__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        """
            Message as string
        """
        return self.message


class UnknownTaskTypeException(Exception):
    """
        Thrown in case of an unknown task type passed via a message
    """

    def __init__(self, message, *args, **kwargs):
        """
            Log the message
        """
        super(UnknownTaskTypeException, self).__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        """
            Message as string
        """
        return self.message


class InvalidTaskTypeException(Exception):
    """
        Thrown in case of an invalid task type passed via a message
    """

    def __init__(self, message, *args, **kwargs):
        """
            Log the message
        """
        super(InvalidTaskTypeException, self).__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        """
            Message as string
        """
        return self.message


class MissingAttributeException(Exception):
    """
        Thrown in case of a missing attribute within a JSON object
    """

    def __init__(self, message, *args, **kwargs):
        """
            Log the message
        """
        super(MissingAttributeException, self).__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        """
            Message as string
        """
        return self.message


class FileNotFoundException(Exception):
    """
        Thrown in case of not being able to find a given file
    """

    def __init__(self, message, *args, **kwargs):
        """
            Log the message
        """
        super(FileNotFoundException, self).__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        """
            Message as string
        """
        return self.message