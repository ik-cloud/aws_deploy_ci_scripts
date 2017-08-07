#!/usr/bin/env bash

BASEDIR=`dirname $0`/..
APPLICATION='application-eb'
APP_VERSION='0.2.3'
APP_ENVIRONMENT='environment-service'
DOCKERRUN=${BASEDIR}/beanstalk_configs/Dockerrun.aws.json
REGION='eu-west-1'
EXTENSIONS="${BASEDIR}/beanstalk_configs/.ebextensions/"
TAG_CONFIG="${BASEDIR}/beanstalk_configs/env/dev.tag.json"
TEMPLATE="${APP_ENVIRONMENT}:${APP_VERSION}"

${BASEDIR}/ebs/make_environment.py --application "${APPLICATION}" --appEnvironment "${APP_ENVIRONMENT}" \
   --appversion "${APP_VERSION}" --region "${REGION}" --tags "${TAG_CONFIG}" --template "${TEMPLATE}"