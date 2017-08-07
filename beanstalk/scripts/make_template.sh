#!/usr/bin/env bash

BASEDIR=`dirname $0`/..
APPLICATION='application-eb'
APP_VERSION='0.2.3'
APP_ENVIRONMENT='environment-service'
ENV_CONFIG=${BASEDIR}/beanstalk_configs/env/dev.conf.json
REGION='eu-west-1'

${BASEDIR}/ebs/make_config_template_version.py --application "${APPLICATION}" --appEnvironment "${APP_ENVIRONMENT}" \
   --envConfFile "${ENV_CONFIG}" --appversion "${APP_VERSION}" --region "${REGION}"