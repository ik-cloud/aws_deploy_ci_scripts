#!/usr/bin/env bash

BASEDIR=`dirname $0`/..
BUCKET="versions-123456"
KEY="appversion.csv"
APPLICATION_VERSION="3.2.11"
TEMPLATE_VERSION="11.2.45"
ACCOUNT="DEV"

${BASEDIR}/dsl/version_management.py --bucket ${BUCKET} --filename ${KEY} \
  --version ${APPLICATION_VERSION} --template ${TEMPLATE_VERSION} --account ${ACCOUNT}
