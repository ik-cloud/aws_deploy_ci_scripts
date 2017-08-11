#!/usr/bin/env bash

APPLICATIOM="service-eb"
ENVIRONMENT="service"

./envhealth.py --application "${APPLICATIOM}" --env "${ENVIRONMENT}" > data_health.json