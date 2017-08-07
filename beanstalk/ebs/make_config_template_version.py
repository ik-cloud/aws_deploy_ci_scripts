#!/usr/bin/env python
'''
  Create Elastic BeanStalk Application Configuration template

  Usage example
  chmod +x make_config_template_version.py
  ./make_config_template_version.py --application "label-service-eb-test" --appEnvironment "label-service-dev-env" \
   --envConfFile "../files/env/dev.conf.json" --appversion "v6" --region "eu-west-1"
'''

import argparse
import json

import boto3
from ebcli.lib import aws


def __create_versioned_configuration_template(app_name, app_environment, version, env_conf_file):
    eb = boto3.client('elasticbeanstalk')
    env_options = json.loads(open(env_conf_file).read())
    print("Configuration added \n{}".format(json.dumps(env_options, indent=4, sort_keys=True, default=str)))
    response = eb.create_configuration_template(
        ApplicationName=app_name,
        TemplateName="{}:{}".format(app_environment, version),
        Description='Template created from the CI using "boto3"',
        # REVIEW Can be parametrized
        PlatformArn='arn:aws:elasticbeanstalk:eu-west-1::platform/Docker running on 64bit Amazon Linux/2.6.0',
        # can be specified instead of platform
        # SolutionStackName='64bit Amazon Linux 2017.03 v2.6.0 running Multi-container Docker 1.12.6 (Generic)',
        # REVIEW Can we have static and dynamic option settings?
        OptionSettings=env_options
    )
    print("Create Configuration Template".format(app_environment, version))
    print(json.dumps(response, indent=4, sort_keys=True, default=str))


def __delete_duplicate_version(app_name, app_environment, version):
    '''
    Feature branch version is static.
    This require to delete same version.
    '''
    eb = boto3.client('elasticbeanstalk')
    try:
        eb.delete_configuration_template(
            ApplicationName=app_name,
            TemplateName="{}:{}".format(app_environment, version)
        )
    except Exception:
        print 'No template found to delete'
        pass

parser = argparse.ArgumentParser(description='Process Arguments.')
parser.add_argument('--application', type=str, required=True, dest='app')
parser.add_argument('--appEnvironment', type=str, required=True, dest='app_environment')
parser.add_argument('--appversion', type=str, required=True, dest='version')
parser.add_argument('--envConfFile', type=str, required=True, dest='config_file')
parser.add_argument('--region', type=str, required=True, dest='region')

if __name__ == "__main__":
    args = parser.parse_args()
    aws.set_region(args.region)
    __delete_duplicate_version(app_name=args.app, app_environment=args.app_environment, version=args.version)
    __create_versioned_configuration_template(app_name=args.app, app_environment=args.app_environment, version=args.version,
                                              env_conf_file=args.config_file)
