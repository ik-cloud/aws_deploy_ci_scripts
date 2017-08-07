#!/usr/bin/env python
'''
  Create/Update Elastic BeanStalk Environment.
  Support deploy different version of application and configuration.


  Usage example
  chmod +x make_environment.py
  ./make_environment.py --application "label-service-eb-test" --appEnvironment "label-service-dev-env-test" \
   --appversion "v5" --region "eu-west-1" --tags "../files/env/dev.tag.json" --template "label-service-dev-env:v3"
'''

import argparse
import json

import boto3
from ebcli.lib import aws

from status_check import app_status_block

eb = boto3.client('elasticbeanstalk')


def __create_environment(application, app_environment, version, tags_file, template):
    response = eb.create_environment(
        ApplicationName=application,
        EnvironmentName=app_environment,
        Description='Service Created with CI',
        Tier={
            'Name': 'WebServer',
            'Type': 'Standard'
        },
        Tags=json.loads(open(tags_file).read()),
        VersionLabel=version,
        TemplateName=template
    )
    print(json.dumps(response, indent=4, sort_keys=True, default=str))
    try:
        app_status_block(application=application, app_environment=app_environment)
    except EnvironmentError as e:
        print str(e)
        raise EnvironmentError("Failed To Create Environment. Manual Action required.")


def __update_environment(application, app_environment, version, template):
    response = eb.update_environment(
        ApplicationName=application,
        EnvironmentName=app_environment,
        VersionLabel=version,
        TemplateName=template
    )
    print(json.dumps(response, indent=4, sort_keys=True, default=str))
    try:
        app_status_block(application=application, app_environment=app_environment)
    except EnvironmentError as e:
        print str(e)
        raise EnvironmentError("Failed To Update Environment. Manual Rollback required.")


parser = argparse.ArgumentParser(description='Process Arguments.')
parser.add_argument('--application', type=str, required=True, dest='app')
parser.add_argument('--appEnvironment', type=str, required=True, dest='app_environment')
parser.add_argument('--appversion', type=str, required=True, dest='version')
parser.add_argument('--region', type=str, required=True, dest='region')
parser.add_argument('--tags', type=str, required=True, dest='tags')
parser.add_argument('--template', type=str, required=True, dest='template')

if __name__ == "__main__":
    '''
    Check if environment already exists.
    Note. There is no version check.
    '''
    args = parser.parse_args()
    aws.set_region(args.region)

    response = eb.describe_environments(
        ApplicationName=args.app,
        EnvironmentNames=[
            args.app_environment,
        ],
        IncludeDeleted=False
    )

    if response['Environments']:
        print 'Found Environment. Updating'
        __update_environment(application=args.app, app_environment=args.app_environment, version=args.version,
                             template=args.template)
    else:
        print 'Not Found Environment. Creating'
        __create_environment(application=args.app, app_environment=args.app_environment, version=args.version, tags_file=args.tags,
                             template=args.template)
