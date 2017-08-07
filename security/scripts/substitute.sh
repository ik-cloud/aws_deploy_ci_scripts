#!/usr/bin/env bash

BASEDIR=`dirname $0`/..
REMOTECONFIG="secret.json"
PARAMETERS="parameters.json"
ENV="dev"

${BASEDIR}/dsl/substitute_secret.py  --env "${ENV}"  --params "${ENV}.${PARAMETERS}"
