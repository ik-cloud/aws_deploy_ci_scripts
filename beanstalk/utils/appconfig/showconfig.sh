#!/usr/bin/env bash

APPLICATIOM="tablet-service-eb"
ENVIRONMENT="tablet-service-feature-pista-64-env"

./readconfig.py --application "${APPLICATIOM}" --env "${ENVIRONMENT}" > data.json