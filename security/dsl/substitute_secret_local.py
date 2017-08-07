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
    localfile = json.loads(open(parameters).read())
    (fd, tempfile) = fileutils.mkstemp()
    sanitized = []
    with (open(tempfile, 'w')) as towrite:
        for data in localfile:
            for key in data.keys():
                value = data[key]
                if '{{' in value and '}}' in value:
                    value = re.sub('{{', '', value)
                    value = re.sub('}}', '', value)
                    values = value.split(':')
                    data[key] = __read_secret(values[BUCKET], environment, values[KEY], values[PLACEHOLDER])
            sanitized.append(data)
        towrite.write(json.dumps(sanitized, towrite, ensure_ascii=False, indent=4, sort_keys=True))
    shutil.copyfile(tempfile, parameters)


def __read_secret(bucket, environment, key, placeholder):
    '''
    Read remote file from location.
    :return: secret
    '''
    remotefile = json.loads(open(__read_s3(bucket=bucket, key="{}/{}".format(environment, key))).read())
    return remotefile[placeholder]


def __read_s3(bucket, key):
    (fd, versionfile) = fileutils.mkstemp()
    try:
        obj = s3.Bucket(name=bucket)
        obj.download_file(key, versionfile)
    except Exception as e:
        raise Exception(e.message)
    return versionfile


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Substitute placeholders.')
    parser.add_argument('--params', type=str, required=True, help='Local configuration file')
    parser.add_argument('--env', type=str, required=True, help='Current environment. DEV, SIT, PROD')
    args = parser.parse_args()
    __merge_data(parameters=args.params, environment=args.env)


    # print remotefile['authtoken']
    # print(json.dumps(localfile, indent=4, sort_keys=True, default=str))
    # print(json.dumps(remotefile, indent=4, sort_keys=True, default=str))

