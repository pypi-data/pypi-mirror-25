# pyinfra
# File: pyinfra/facts/lxd.py
# Desc: LXD containers facts

import json

from pyinfra.api import FactBase


class DockerFactBase(FactBase):
    abstract = True

    def process(self, output):
        output = ''.join(output)
        return json.loads(output)


class DockerContainers(DockerFactBase):
    '''
    Returns a list of all Docker containers.
    '''

    command = 'docker inspect `docker ps -qa`'


class DockerImages(DockerFactBase):
    '''
    Returns a list of all Docker images.
    '''

    command = 'docker inspect `docker images -q`'


class DockerNetworks(DockerFactBase):
    '''
    Returns a list of all Docker networks.
    '''

    command = 'docker inspect `docker network ls -q`'
