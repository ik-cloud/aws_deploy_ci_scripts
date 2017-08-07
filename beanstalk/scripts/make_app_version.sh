#!/usr/bin/env bash

BASEDIR=`dirname $0`/..
APPLICATION='application-eb'
APP_VERSION='0.2.3'
APP_ENVIRONMENT='environment-service'
DOCKERRUN=${BASEDIR}/beanstalk_configs/Dockerrun.aws.json
REGION='eu-west-1'
EXTENSIONS="${BASEDIR}/beanstalk_configs/.ebextensions/"

${BASEDIR}/ebs/make_app_version.py --application "${APPLICATION}" --appversion "${APP_VERSION}" --dockerrun "${DOCKERRUN}" \
  --ebextensions "${EXTENSIONS}" --appEnvironment "${APP_ENVIRONMENT}" --region "${REGION}"