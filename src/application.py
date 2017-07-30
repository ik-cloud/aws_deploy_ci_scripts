#!/usr/bin/env python
'''

'''
import boto3


def create_application(APP_NAME):

    eb = boto3.client('elasticbeanstalk')
    # TODO we can get/create service role
    response = eb.create_application(
        ApplicationName=APP_NAME,
        Description='Application',
        ResourceLifecycleConfig={
            # The ARN of an IAM service role that Elastic Beanstalk has permission to assume.
            'ServiceRole': 'arn:aws:iam::575398778607:role/BeanstalkRole',
            'VersionLifecycleConfig': {
                'MaxCountRule': {
                    'Enabled': True,
                    'MaxCount': 123,
                    'DeleteSourceFromS3': True
                }
            }
        }
    )

    print response
