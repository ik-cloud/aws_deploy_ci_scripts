#!/usr/bin/env python
'''
  Create Elastic BeanStalk Application

  Usage example
  chmod +x make_application.py
  ./make_application.py --application "label-service-eb-test" --servicerole "arn:aws:iam::179254640887:role/aws-elasticbeanstalk-service-role"
'''
import argparse
import json

import boto3


def __execute(APP_NAME, SERVICE_ROLE):
    '''
    Create new application without check that Application With Given name exists
    '''
    eb = boto3.client('elasticbeanstalk')
    response = eb.create_application(
        ApplicationName=APP_NAME,
        Description='CI Make application',
        ResourceLifecycleConfig={
            # The ARN of an IAM service role that Elastic Beanstalk has permission to assume.
            'ServiceRole': SERVICE_ROLE,
            'VersionLifecycleConfig': {
                'MaxCountRule': {
                    'Enabled': True,
                    'MaxCount': 123,
                    'DeleteSourceFromS3': True
                }
            }
        }
    )

    print(json.dumps(response, indent=4, sort_keys=True, default=str))


parser = argparse.ArgumentParser(description='Process Arguments.')
parser.add_argument('--application', type=str, required=True, dest='app')
parser.add_argument('--servicerole', type=str, required=True, dest='role')

if __name__ == "__main__":
    args = parser.parse_args()
    __execute(APP_NAME=args.app, SERVICE_ROLE=args.role)
