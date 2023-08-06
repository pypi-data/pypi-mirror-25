import json

from os import path

from pyinfra import local, logger

VAGRANT_CONFIG = None
VAGRANT_GROUPS = None


def _get_vagrant_config():
    global VAGRANT_CONFIG

    if VAGRANT_CONFIG is None:
        logger.info('Getting vagrant config...')

        VAGRANT_CONFIG = local.shell(
            'vagrant ssh-config',
            splitlines=True,
            # Annoyingly vagrant errors if any one machine isn't up - this doesn't
            # mean nothing's up!
            ignore_errors=True,
        )

    return VAGRANT_CONFIG


def _get_vagrant_groups():
    global VAGRANT_GROUPS

    if VAGRANT_GROUPS is None:
        if path.exists('@vagrant.json'):
            with open('@vagrant.json', 'r') as f:
                VAGRANT_GROUPS = json.loads(f.read()).get('groups', {})
        else:
            VAGRANT_GROUPS = {}

    return VAGRANT_GROUPS


def _make_name_data(host):
    host_to_group = _get_vagrant_groups()

    # Build data
    data = {
        'ssh_hostname': host['HostName'],
        'ssh_port': host['Port'],
        'ssh_user': host['User'],
        'ssh_key': host['IdentityFile'],
    }

    # Work out groups
    groups = host_to_group.get(host['Host'], [])

    if '@vagrant' not in groups:
        groups.append('@vagrant')

    return '@vagrant/{0}'.format(host['Host']), data, groups


def make_names_data():
    vagrant_ssh_info = _get_vagrant_config()

    logger.debug('Got Vagrant SSH info: \n{0}'.format(vagrant_ssh_info))

    current_host = None

    for line in vagrant_ssh_info:
        # Vagrant outputs an empty line between each host
        if not line:
            # yield any previous host
            if current_host:
                yield _make_name_data(current_host)

            current_host = None
            continue

        key, value = line.split(' ', 1)

        if key == 'Host':
            # yield any previous host
            if current_host:
                yield _make_name_data(current_host)

            # Set the new host
            current_host = {
                key: value,
            }

        elif current_host:
            current_host[key] = value

        else:
            logger.debug('Extra Vagrant SSH key/value ({0}={1})'.format(
                key, value,
            ))

    # yield any leftover host
    if current_host:
        yield _make_name_data(current_host)
