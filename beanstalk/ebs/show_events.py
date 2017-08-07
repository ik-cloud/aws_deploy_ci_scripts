#!/usr/bin/env python

from datetime import datetime
from datetime import timedelta

import boto3

client = boto3.client('elasticbeanstalk')


def __execute(application, app_environment, eventtype, seconds):
    time = datetime.now() - timedelta(seconds=seconds)
    response = client.describe_events(
        ApplicationName=application,
        EnvironmentName=app_environment,
        Severity=eventtype,
        MaxRecords=5,
        StartTime=datetime(year=time.year, month=time.month, day=time.day, hour=time.hour, minute=time.minute, second=time.second),
    )
    events = response['Events']
    if len(events):
        print "\n Events"
        for data in events:
            print "  -Severity- {}.\n  -Message- {}".format(data['Severity'], data['Message'])
        print "\n"


def show_events(application, app_environment, seconds, eventtype):
    '''
     Show all the events happens 20 minutes ago.
    '''
    __execute(application=application, app_environment=app_environment, eventtype=eventtype, seconds=seconds)
