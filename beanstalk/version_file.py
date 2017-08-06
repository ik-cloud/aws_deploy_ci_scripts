#!/usr/bin/env python
'''

'''

import tempfile
import os
import shutil

DOCKERRUN = 'Dockerrun.aws.json'
EXTENSIONS = '.ebextensions/'


def create_version_file(label, dockerrun, ebextensions):
    '''
    Create configuration zip file
    '''
    print 'Entering method'
    temporary_directory = tempfile.mkdtemp()
    print temporary_directory
    try:
        deploy_dockerrun = os.path.join(temporary_directory, DOCKERRUN)
        print deploy_dockerrun
        deploy_extensions = os.path.join(temporary_directory, EXTENSIONS)
        shutil.copyfile(dockerrun, deploy_dockerrun)
        shutil.copytree(ebextensions, deploy_extensions)
        return shutil.make_archive(label, 'zip', root_dir=temporary_directory)
    finally:
        shutil.rmtree(temporary_directory)


if __name__ == "__main__":
    create_version_file('version_123', '../beanstalk_configs/Dockerrun.aws.json', '../beanstalk_configs/.ebextensions')
