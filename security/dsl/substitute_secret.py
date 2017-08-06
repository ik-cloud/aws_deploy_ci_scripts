#!/usr/bin/env python
'''
 Reads file with secret data from S3.
 Substitute JSON object with any patern.

 Usage Example
 chmod +x substitute_secret.py
 ./substitute_secret.py --env "dev" --remoteconf "secret.json" \
   --params "parameters.json"
'''

import argparse
import json
import re
import shutil
import tempfile as fileutils

from utils import get_logger, get_resource

s3 = get_resource('s3')
logger = get_logger('simpleExample')

BUCKET = 0
KEY = 1
PLACEHOLDER = 2


def __merge_data(parameters, environment):
    '''
     Read parameters file. Check every line for placeholders.
     Write to temporary file and substitute them.
    '''
    logger.info('Hello')
    localfile = json.loads(open("../files/" + parameters).read())
    (fd, tempfile) = fileutils.mkstemp()
    sanitized = []

    with (open(tempfile, 'w')) as towrite:
        for data in localfile:
            for key in data.keys():
                value = data[key]
                if '{{' in value and '}}' in value:
                    value = re.sub('{{', '', value)
                    value = re.sub('}}', '', value)
                    # should read from bucket
                    filelocation = "../files/{}/{}/{}".format(value.split(':')[BUCKET], environment, value.split(':')[KEY])
                    remotefile = json.loads(open(filelocation).read())
                    secret = remotefile[value.split(':')[PLACEHOLDER]]
                    data[key] = secret
            sanitized.append(data)
        towrite.write(json.dumps(sanitized, towrite, ensure_ascii=False, indent=4, sort_keys=True))
    shutil.copyfile(tempfile, parameters)


def __remote_read():
    '''
     TODO
    '''
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Substitute placeholders.')
    parser.add_argument('--remoteconf', type=str, required=True, help='Remote configuration file')
    parser.add_argument('--params', type=str, required=True, help='Local configuration file')
    parser.add_argument('--env', type=str, required=True, help='Current environment. DEV, SIT, PROD')
    args = parser.parse_args()
    __merge_data(parameters="{0}.{1}".format(args.env, args.params), environment=args.env)
