#!/usr/bin/env python
# coding: utf-8

import logging
import logging.config

import boto3

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) -35s %(lineno) -5d: %(message)s')


def get_logger(name):
    '''
     How to setup config file
     http://peak.telecommunity.com/DevCenter/PythonEggs#accessing-package-resources
    '''
    logging.basicConfig(level=logging.INFO, format=get_log_format())
    LOG = logging.getLogger(name)
    return LOG


def get_log_format():
    return LOG_FORMAT


def get_log_lvl(level_string):
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
