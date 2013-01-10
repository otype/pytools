# -*- coding: utf-8 -*-
"""

    deployr

    created by hgschmidt on 27.11.12, 01:14 CET
    
    Copyright (c) 2012 apitrary

"""
import logging
import logging.handlers
from deployr_service.config.logging_config import LOG_FORMAT
from deployr_service.models.log_levels import LOGGING_LEVEL
from deployr_service.services import deployr_config_service

def get_log_level_from_config(log_level):
    """
        Sets the log level (use colored logging output).
        This is a wrapper for python logging.
    """
    level = log_level.upper()
    if level == LOGGING_LEVEL.CRITICAL:
        return logging.CRITICAL
    if level == LOGGING_LEVEL.WARN:
        return logging.WARN
    if level == LOGGING_LEVEL.WARNING:
        return logging.WARN
    if level == LOGGING_LEVEL.DEBUG:
        return logging.DEBUG
    if level == LOGGING_LEVEL.ERROR:
        return logging.ERROR
    else:
        return logging.INFO


def setup_logging(log_level=None, file_writing_enabled=False):
    """
        Configure logging
    """
    if log_level is None:
        log_level = logging.DEBUG

    # create logger
    logger = logging.getLogger('deployr')
    logger.setLevel(log_level)

    if file_writing_enabled:
        # create console handler and set level to debug
        ch = logging.handlers.RotatingFileHandler(filename='deployr.log', encoding='UTF-8')
        ch.setLevel(log_level)

        # create formatter
        formatter = logging.Formatter(LOG_FORMAT)

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    return logger


def get_logger(log_level=None):
    """
        Get the logger object
    """
    # Load the global configuration from config file
    config = deployr_config_service.load_configuration()

    if log_level is None:
        # Extract the log level from the config object
        log_level = get_log_level_from_config(config['LOGGING'])

    return setup_logging(log_level)