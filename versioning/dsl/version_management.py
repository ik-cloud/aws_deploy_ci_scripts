#!/usr/bin/env python
'''
  Write data to CSV file.

  Production and pre-Production branches can be protected with pattern [*-Release].

  Usage Example
  chmod +x version_management.py
  version_management.py -h (HELP MENU)
  ./version_management.py --bucket "versions-123456" --filename "appversion.csv" --version "9.18.98" \
    --template "11.34.01" --account "PROD"
'''

import argparse
import csv
import shutil
import tempfile as fileutils
from datetime import datetime

from utils import get_logger, get_client, get_resource

FIELDNAMES = ['App Version', 'Template Version', 'Account', 'Timestamp']
TIMEPATTERN = "{:%d-%B-%Y %H:%M}"

s3 = get_resource('s3')
client = get_client('s3')
logger = get_logger('version-management')


class Row:
    def __init__(self, data):
        self.version = data['App Version']
        self.template = data['Template Version']
        self.account = data['Account']
        self.timestamp = data['Timestamp']

    def __str__(self):
        return "App Version: {}, Template Version: {}, Account: {}, Timestamp: {}".format(self.version, self.template, self.account,
                                                                                          self.timestamp)


def __update_data(file, version, template, account):
    '''
      Read current file, create temp file and write all values into it.
      Second line contains current update.
      Copy temporary file into file provided.
    '''
    (fd, tempfile) = fileutils.mkstemp()
    with open(file, 'r') as csvread, open(tempfile, 'w') as write:
        reader = csv.DictReader(csvread)
        writer = csv.DictWriter(write, fieldnames=FIELDNAMES)
        writer.writeheader()

        writer.writerow({'App Version': version, 'Template Version': template, 'Account': account,
                         'Timestamp': TIMEPATTERN.format(datetime.now())})

        for row in reader:
            data = Row(row)
            if data.account == account:
                # already written
                pass
            else:
                writer.writerow({'App Version': data.version, 'Template Version': data.template, 'Account': data.account,
                                 'Timestamp': data.timestamp})

    shutil.copyfile(tempfile, file)


def __bucket_exists(bucket):
    try:
        s3.meta.client.head_bucket(Bucket=bucket)
        logger.info('HEAD request to bucker {} PASS.'.format(bucket))
        return True
    except:
        logger.info('HEAD request to bucker {} FAIL.'.format(bucket))
        return False


def __read_s3(bucket, key):
    (fd, versionfile) = fileutils.mkstemp()
    try:
        obj = s3.Bucket(name=bucket)
        obj.download_file(key, versionfile)
    except Exception as e:
        raise Exception(e.message)
    return versionfile


def __upload_s3(bucket, key, file):
    obj = s3.Bucket(name=bucket)
    obj.upload_file(file, key)
    logger.info("File uploaded %s" % key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update version table.')
    parser.add_argument('--bucket', type=str, required=True, help='Bucket where version file stored')
    parser.add_argument('--filename', type=str, required=True, help='S3 key file name')
    parser.add_argument('--version', type=str, required=True, help='Application version')
    parser.add_argument('--template', type=str, required=True, help='Template version')
    parser.add_argument('--account', type=str, required=True, help='Account application being deployed')
    args = parser.parse_args()
    if __bucket_exists(args.bucket):
        downloadedfile = __read_s3(args.bucket, args.filename)
        __update_data(downloadedfile, args.version, args.template, args.account)
        __upload_s3(bucket=args.bucket, key=args.filename, file=downloadedfile)
    else:
        raise Exception('Bucket not found')
