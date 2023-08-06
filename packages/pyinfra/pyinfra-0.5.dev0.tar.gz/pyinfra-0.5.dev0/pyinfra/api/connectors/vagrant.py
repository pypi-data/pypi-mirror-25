from pyinfra import local, logger

VAGRANT_CONFIG = None


def _get_vagrant_config():
    global VAGRANT_CONFIG

    if VAGRANT_CONFIG is None:
        logger.info('Loading vagrant config...')
        VAGRANT_CONFIG = local.shell(
            'vagrant ssh-config',
            splitlines=True,
            # Annoyingly vagrant errors if any one machine isn't up - this doesn't
            # mean nothing's up!
            ignore_errors=True,
        )

    return VAGRANT_CONFIG


def _make_name_data(host):
    return (
        '@vagrant/{0}'.format(host['Host']),
        {
            'ssh_hostname': host['HostName'],
            'ssh_port': host['Port'],
            'ssh_user': host['User'],
            'ssh_key': host['IdentityFile'],
        },
    )


def make_names_data():
    vagrant_ssh_info = _get_vagrant_config()

    current_host = None

    for line in vagrant_ssh_info:
        if not line:
            # Vagrant outputs an empty line between each host
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

        if current_host:
            current_host[key] = value

    # yield any leftover host
    if current_host:
        yield _make_name_data(current_host)
