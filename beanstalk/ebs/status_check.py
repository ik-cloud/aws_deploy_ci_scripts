#!/usr/bin/env python
'''
 Check the application environment status.
'''
import time

import boto3

from call_service import call_service
from show_events import show_events

client = boto3.client('elasticbeanstalk')


def __retrieve_health_endpoint(application, appEnvironment):
    '''
    Find health check endpoint
    :return: healthcheck endpoint
    '''
    response = client.describe_configuration_settings(
        ApplicationName=application,
        EnvironmentName=appEnvironment
    )
    return next(endpoint['Value'] for endpoint in response['ConfigurationSettings'][0]['OptionSettings'] if
                endpoint['OptionName'] == 'HealthCheckPath')


def __execute(application, app_environment):
    response = client.describe_environments(
        ApplicationName=application,
        EnvironmentNames=[
            app_environment,
        ],
        IncludeDeleted=False
    )
    test_app = {'health_app': 'no CNAME found', 'status_app': 'no CNAME found'}
    try:
        if response['Environments'] and response['Environments'][0] and 'CNAME' in response['Environments'][0]:
            test_app = call_service(
                'http://{}{}'.format(response['Environments'][0]['CNAME'],
                                     __retrieve_health_endpoint(application, app_environment)))
    except Exception as e:
        pass

    health = response['Environments'][0]['Health'] if response['Environments'] else ''
    status = response['Environments'][0]['Status'] if response['Environments'] else ''
    return {'health_env': health, 'status_env': status, 'health_app': test_app['health_app'], 'status_app': test_app['status_app']}


def check_app_status(application, app_environment):
    check = __execute(application, app_environment)
    status = check['status_env']
    health = check['health_env']
    if ('Grey' == health):
        raise EnvironmentError(
            "Environment named {} is in invalid {} state for this operation . Must be Ready".format(app_environment, health))
    return status, health


def app_status_block(application, app_environment):
    status = ''
    health = ''
    timetowait = 20
    while 'Ready' != status and 'Green' != health:
        time.sleep(timetowait)
        check = __execute(application=application, app_environment=app_environment)
        status = check['status_env']
        health = check['health_env']
        print "Environment Status --{}-- and Health --{}--. Health Check Status --{}-- and Response --{}--" \
            .format(status, health, check['status_app'], check['health_app'])
        if 'Ready' == status and 'Green' == health:
            print 'Environment deployed'
            break
        elif health in {'Yellow', 'Red', ''} or ('Ready' == status and 'Grey' == health):
            show_events(application=application, app_environment=app_environment, eventtype='WARN', seconds=timetowait)
            print "Failed Deploy New Configuration. Health {}. Status {}".format(health, status)
            raise EnvironmentError()
        elif status in {'Updating', 'Launching'} or 'Grey' == health:
            pass
