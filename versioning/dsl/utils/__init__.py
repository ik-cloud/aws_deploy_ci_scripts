#!/usr/bin/env python
# coding: utf-8

import boto3

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) -35s %(lineno) -5d: %(message)s')


def get_logger(name):
    import logging
    logging.basicConfig(level=logging.INFO, format=get_log_format())
    LOG = logging.getLogger(name)
    return LOG


def get_log_format():
    return LOG_FORMAT


def get_log_lvl(level_string):
    import logging
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "CRITICAL": logging.CRITICAL
    }
    return levels[level_string]


def get_client(type):
    return boto3.client(type)


def get_resource(type):
    return boto3.resource(type)
