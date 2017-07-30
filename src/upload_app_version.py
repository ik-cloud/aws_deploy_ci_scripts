#!/usr/bin/env python
'''

'''

import logging
import os

from ebcli.lib import aws
from ebcli.lib import elasticbeanstalk
from ebcli.lib import s3
from ebcli.objects.exceptions import NotFoundError

logger = logging.getLogger('upload-application')


# TODO upload chosen version
def upload_app_version(app_name, bundled_zip):
    '''
    Uploading zip file of app version to S3
    '''
    bucket = elasticbeanstalk.get_storage_location()
    logger.info("Bucket to deploy '%s'", bucket)
    key = app_name + '/' + os.path.basename(bundled_zip)
    logger.info("File in bucket '%s'", key)
    try:
        s3.get_object_info(bucket, key)
    except NotFoundError:
        logger.info("Uploading archive to S3")
        s3.upload_application_version(bucket, key, bundled_zip)
    return bucket, key


if __name__ == "__main__":
    aws.set_region('eu-west-1')
    aws.set_profile('default')
    upload_app_version("app", "zip")
