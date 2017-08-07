#!/usr/bin/env bash

PRIVATE_KEY="domain.pem"
CERTIFICATE="domain.crt"
CERTIFICATE_NAME="selfcertificate"

# This command creates a 2048-bit private key (domain.key) and a self signed certificate
openssl req -newkey rsa:2048 -nodes -keyout ${PRIVATE_KEY} \
  -x509 -days 365 -out ${CERTIFICATE}

aws iam upload-server-certificate --server-certificate-name selfcertificate \
 --private-key file://${PRIVATE_KEY} \
 --certificate-body file://${CERTIFICATE}