#!/usr/bin/env bash

APPLICATIOM="service-eb"
ENVIRONMENT="service"

./readconfig.py --application "${APPLICATIOM}" --env "${ENVIRONMENT}" > data.json