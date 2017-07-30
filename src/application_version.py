#!/usr/bin/env python
'''

'''

import logging
import os

import boto3

from upload_app_version import upload_app_version
from version_file import create_version_file

logger = logging.getLogger('create_application_version')


def create_application_version(app_name, version, dockerrun, ebextensions):
    bundled_zip = create_version_file(version, dockerrun=dockerrun, ebextensions=ebextensions)
    try:
        bucket, key = upload_app_version(app_name, bundled_zip=bundled_zip)
        logger.info('Creating application version')
        eb = boto3.client('elasticbeanstalk')
        eb.create_application_version(
            ApplicationName=app_name,
            VersionLabel=version,
            SourceBundle={
                'S3Bucket': bucket,
                'S3Key': key
            }
        )
    finally:
        os.remove(bundled_zip)
