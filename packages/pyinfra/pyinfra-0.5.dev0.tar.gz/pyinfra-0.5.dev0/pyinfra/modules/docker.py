# pyinfra
# File: pyinfra/modules/docker.py
# Desc: manage Docker containers/images/networks.

'''
Manage Docker containers, images and networks.
'''

from pyinfra.api import operation


@operation
def container(state, host):
    pass


@operation
def image(state, host):
    pass


@operation
def network(state, host):
    pass
