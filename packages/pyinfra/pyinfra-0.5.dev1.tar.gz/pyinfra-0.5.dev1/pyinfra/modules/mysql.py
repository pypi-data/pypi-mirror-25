# pyinfra
# File: pyinfra/modules/mysql.py
# Desc: manage MySQL databases/users/permissions

'''
Manage MySQL databases, users and permissions.
'''

from pyinfra.api import operation


@operation
def sql(state, host, sql, database=None):
    '''
    Execute arbitrary SQL against MySQL.

    + sql: the SQL to send to MySQL
    + database: optional database to open the connection with
    '''

    target = 'mysql'
    if database:
        target = 'mysql {0}'.format(database)

    yield 'echo "{0}" | {1}'.format(sql, target)


@operation
def user(
    state, host, name,
    hostname='localhost', password=None, permissions=None,
    present=True,
):
    '''
    Manage the state of MySQL uusers.

    + name: the name of the user
    + hostname: the hostname of the user
    + password: the password of the user (if created)
    + permissions: the global permissions for this user
    + present: whether the user should exist or not
    '''

    current_users = host.fact.mysql_users
    user_host = '{0}@{1}'.format(name, hostname)

    # Don't do anything if the user already exists
    if user_host in current_users:
        return

    # Create the user
    yield 'echo "CREATE USER `{0}`@`{1}` | mysql'.format(name, hostname)


@operation
def database(
    state, host, name,
    collate=None, charset=None,
    user=None, user_permissions='ALL',
    present=True,
):
    '''
    Manage the state of MySQL databases.

    + name: the name of the database
    + collate: the collate to use when creating the database
    + charset: the charset to use when creating the database
    + user: MySQL user to grant privileges on this database to
    + user_permissions: permissions to grant the user
    + present: whether the database should exist or not

    Collate/charset:
        these will only be applied if the database does not exist - ie pyinfra
        will not attempt to alter the existing databases collate/character sets.
    '''

    current_databases = host.fact.mysql_databases

    # Don't do anything if the database already exists
    if name in current_databases:
        return

    # Create the database
    yield 'echo "CREATE DATABASE `{0}` | mysql'.format(name)


@operation
def permission(
    state, host, user, permissions,
    table=None,
):
    '''
    Manage MySQL permissions for users, either global or table specific.

    + user: name of the user to manage permissions for
    + permissions: list of permissions the user should have
    + table: name of the table to grant user permissions to (defaults to global)
    '''

    pass
