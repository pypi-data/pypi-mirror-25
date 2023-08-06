# pyinfra
# File: pyinfra/facts/mysql.py
# Desc: facts for the MySQL server

import six

from pyinfra.api import FactBase


class MysqlDatabases(FactBase):
    '''
    Returns a list of existing MySQL databases.
    '''

    command = 'echo "SHOW DATABASES;" | mysql'
    default = list

    def process(self, output):
        return output[1:]


class MysqlUsers(FactBase):
    '''
    Returns a dict of MySQL user@host's and their associated data:

    .. code:: python

        'user@host': {
            'permissions': ['Alter', 'Grant'],
            'max_connections': 5,
            ...
        },
        ...
    '''

    command = 'echo "SELECT * FROM mysql.user;" | mysql'
    default = dict

    def process(self, output):
        users = {}

        # Get the titles
        titles = output[0]
        titles = titles.split('\t')

        for row in output[1:]:
            bits = row.split('\t')
            details = {}

            # Attach user columns by title
            for i, bit in enumerate(bits):
                details[titles[i]] = bit

            if 'Host' in details and 'User' in details:
                # Pop off any true permission values
                permissions = [
                    key.replace('_priv', '')
                    for key in list(six.iterkeys(details))
                    if key.endswith('_priv') and details.pop(key) == 'Y'
                ]
                details['permissions'] = permissions

                # Attach the user in the format user@host
                users['{0}@{1}'.format(
                    details.pop('User'), details.pop('Host'),
                )] = details

        return users
