#!/usr/bin/env python
'''
  Create Elastic BeanStalk Application environment version.
  Silently Create Application if one not exits.

  Usage example
  chmod +x make_application.py
  ./make_app_version.py --application "label-service-eb-test" --appversion "v6" --dockerrun "../files/Dockerrun.aws.json" \
  --ebextensions "../files/.ebextensions" --appEnvironment "label-service-dev-env" --region "eu-west-1"
'''

import argparse
import json
import os
import shutil
import tempfile

import boto3
from ebcli.lib import aws
from ebcli.lib import elasticbeanstalk
from ebcli.lib import s3
from ebcli.objects.exceptions import NotFoundError

DOCKERRUN = 'Dockerrun.aws.json'
EXTENSIONS = '.ebextensions/'
ARCHIVE = 'zip'


def __create_version_file(app_enviroment, version_label, dockerrun_location, ebextensions_location):
    '''
    Create versioned application zip file
    '''
    temporary_directory = tempfile.mkdtemp()
    print temporary_directory
    try:
        deploy_dockerrun = os.path.join(temporary_directory, DOCKERRUN)
        print deploy_dockerrun
        deploy_extensions = os.path.join(temporary_directory, EXTENSIONS)
        shutil.copyfile(dockerrun_location, deploy_dockerrun)
        shutil.copytree(ebextensions_location, deploy_extensions)
        return shutil.make_archive("{}:{}".format(app_enviroment, version_label), ARCHIVE, root_dir=temporary_directory)
    finally:
        shutil.rmtree(temporary_directory)


def __upload_app_version(app_name, bundled_file):
    '''
    Uploading zip file of app version to S3
    '''
    bucket = elasticbeanstalk.get_storage_location()
    print("Bucket to deploy bundle '{}'".format(bucket))
    key = app_name + '/' + os.path.basename(bundled_file)
    print("'{}' Location of the bundle ".format(key))
    try:
        s3.get_object_info(bucket, key)
    except NotFoundError:
        print ("Uploading archive to S3")
        s3.upload_application_version(bucket, key, bundled_file)
    finally:
        os.remove(bundled_zip)
    return bucket, key


def __create_app_version(app_name, version, bucket, key):
    '''
    Create application version.
    Preprocess and Validates configuration files
    '''
    eb = boto3.client('elasticbeanstalk')
    # remove app-version if exists
    response = eb.create_application_version(
        ApplicationName=app_name,
        VersionLabel=version,
        Description='CI Make application',
        SourceBundle={
            'S3Bucket': bucket,
            'S3Key': key
        },
        AutoCreateApplication=False,
        Process=True
    )
    print("Creates an '{}' version '{}'".format(app_name, version))
    print(json.dumps(response, indent=4, sort_keys=True, default=str))


def __delete_duplicate_version(app_name, version):
    '''
    Feature branch version is static.
    This require to delete same version.
    '''
    eb = boto3.client('elasticbeanstalk')
    response = eb.describe_application_versions(
        ApplicationName=app_name,
        VersionLabels=[
            version
        ],
        MaxRecords=10
    )
    print("Found application verions {} - {}".format(app_name, version))
    print(json.dumps(response, indent=4, sort_keys=True, default=str))
    if response['ApplicationVersions']:
        eb.delete_application_version(
            ApplicationName=app_name,
            DeleteSourceBundle=True,
            VersionLabel=version,
        )


parser = argparse.ArgumentParser(description='Process Arguments.')
parser.add_argument('--application', type=str, required=True, dest='app')
parser.add_argument('--appEnvironment', type=str, required=True, dest='app_environment')
parser.add_argument('--appversion', type=str, required=True, dest='version')
parser.add_argument('--dockerrun', type=str, required=True, dest='dockerrun')
parser.add_argument('--ebextensions', type=str, required=True, dest='ebextensions')
parser.add_argument('--region', type=str, required=True, dest='region')

if __name__ == "__main__":
    args = parser.parse_args()
    aws.set_region(args.region)
    __delete_duplicate_version(args.app, args.version)
    bundled_zip = __create_version_file(app_enviroment=args.app_environment, version_label=args.version,
                                        dockerrun_location=args.dockerrun,
                                        ebextensions_location=args.ebextensions)
    bucket, key = __upload_app_version(app_name=args.app, bundled_file=bundled_zip)
    __create_app_version(app_name=args.app, version=args.version, bucket=bucket, key=key)
