# !/usr/bin/env python
'''
 Reads application config.

 chmod +x readconfig.py
 ./envhealth.py --application "service-eb" --env "service"
'''

import argparse
import json

import boto3


def __get_client(type):
    return boto3.client(type)


def __execute(env):
    response = __get_client('elasticbeanstalk').describe_environment_health(
        EnvironmentName=env,
        AttributeNames=[
            'ApplicationMetrics', 'InstancesHealth' , 'HealthStatus'
        ]
    )
    print(json.dumps(response, indent=4, sort_keys=True, default=str))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Substitute placeholders.')
    parser.add_argument('--application', type=str, required=True, help='Remote configuration file')
    parser.add_argument('--env', type=str, required=True, help='Current environment. DEV, SIT, PROD')
    args = parser.parse_args()
    __execute(env=args.env)

