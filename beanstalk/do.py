#!/usr/bin/env python
'''

'''
from __future__ import absolute_import

import logging

logger = logging.getLogger('upload-application')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

from ebcli.lib import aws

from application_version import create_application_version
from application import create_application

if __name__ == "__main__":
    aws.set_region('eu-west-1')
    aws.set_profile('default')
    create_application(APP_NAME='my_app')
    create_application_version('my_app', 'version_124', '../beanstalk_configs/Dockerrun.aws.json', '../beanstalk_configs/.ebextensions')
