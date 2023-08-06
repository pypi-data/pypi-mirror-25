import subprocess
import os
from .common import DOCKER_REPO_URLS, big_print, get_project_root

FNULL = open(os.devnull, 'w')


DOCKER_NOT_RUNNING_ERROR = """Docker does not appear to be running. 
Please check if docker is running, or you can download docker from here: https://www.docker.com/get-docker"""

NO_DOCKER_URL_PROVIDED = """
Specified template has no matching docker url. If this is a private docker image, use config-project to set a remote url.
"""


class Docker(object):
    def __init__(self, arguments, config):
        self.template_name = arguments['<template-type>']
        self.project_path = arguments['<project-name>']
        self.abs_project_path = get_project_root(arguments)
        self.arguments = arguments
        self.config = config

    def docker_is_running(self):
        return 0 == subprocess.call(
            ['docker', 'version'], stdout=FNULL, stderr=subprocess.STDOUT
        )

    def download_image(self):
        if not self.docker_is_running():
            raise RuntimeError(DOCKER_NOT_RUNNING_ERROR)
        if self.config.get('CUSTOM_DOCKER_RULE', None):
            url = self.config.get('CUSTOM_DOCKER_RULE')
        else:
            url = DOCKER_REPO_URLS.get(self.template_name, None)
        if not url:
            raise RuntimeError(NO_DOCKER_URL_PROVIDED)
        big_print('Pulling Docker image...', first_print=True)
        subprocess.call(['docker', 'pull', url])

    def run(self, project_path=None):
        if not self.docker_is_running():
            raise RuntimeError(DOCKER_NOT_RUNNING_ERROR)
        if not project_path:
            project_path = self.project_path
        base_command = [
            'docker', 'run', '-it', '-p=8000:8000',
            '-e', 'DEV=true', '-e', 'FOLDER_OVERRIDE=' + project_path,
            '-v', '%s:/tmp/%s' % (self.abs_project_path, project_path),
            ]
        if self.arguments['<custom-docker-image>']:
            base_command.append(self.arguments['<custom-docker-image>'])
        else:
            base_command.append('dpbriggs/python3-generic')
        subprocess.call(base_command)



