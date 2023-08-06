# pyinfra
# File: pyinfra_cli/prints.py
# Desc: print utilities for the CLI

from __future__ import print_function, unicode_literals

import json
import traceback

import click
import six

from pyinfra import logger
from pyinfra.api.facts import get_fact_names
from pyinfra.api.operation import get_operation_names

from .util import json_encode


def _get_group_combinations(inventory):
    group_combinations = {}

    for host in inventory.iter_all_hosts():
        # Tuple for hashability, set to normalise order
        host_groups = tuple(set(host.groups))

        group_combinations.setdefault(host_groups, [])
        group_combinations[host_groups].append(host)

    return group_combinations


def dump_trace(exc_info):
    # Dev mode, so lets dump as much data as we have
    error_type, value, trace = exc_info
    print('----------------------')
    traceback.print_tb(trace)
    logger.critical('{0}: {1}'.format(error_type.__name__, value))
    print('----------------------')


def dump_state(state):
    print()
    print('--> Gathered facts:')
    print(json.dumps(state.facts, indent=4, default=json_encode))
    print()
    print('--> Proposed operations:')
    print(json.dumps(state.ops, indent=4, default=json_encode))
    print()
    print('--> Operation meta:')
    print(json.dumps(state.op_meta, indent=4, default=json_encode))
    print()
    print('--> Operation order:')
    print(json.dumps(state.op_order, indent=4, default=json_encode))


def print_groups_by_comparison(print_items, comparator=lambda item: item[0]):
    items = []
    last_name = None

    for name in print_items:
        # Keep all facts with the same first character on one line
        if last_name is None or comparator(last_name) == comparator(name):
            items.append(name)

        else:
            print('    {0}'.format(', '.join((
                click.style(name, bold=True)
                for name in items
            ))))

            items = [name]

        last_name = name

    if items:
        print('    {0}'.format(', '.join((
            click.style(name, bold=True)
            for name in items
        ))))


def print_facts_list():
    fact_names = sorted(get_fact_names())
    print_groups_by_comparison(fact_names)


def print_operations_list():
    operation_names = sorted(get_operation_names())
    print_groups_by_comparison(
        operation_names,
        comparator=lambda item: item.split('.')[0],
    )


def print_fact(fact_data):
    print(json.dumps(fact_data, indent=4, default=json_encode))


def print_inventory(inventory):
    for host in inventory:
        print()
        print('--> Data for: {0}'.format(click.style(host.name, bold=True)))
        print(json.dumps(host.data.dict(), indent=4, default=json_encode))


def print_facts(facts):
    for name, data in six.iteritems(facts):
        print()
        print('--> Fact data for: {0}'.format(
            click.style(name, bold=True),
        ))
        print_fact(data)


def print_meta(state, inventory):
    group_combinations = _get_group_combinations(inventory)

    for i, (groups, hosts) in enumerate(six.iteritems(group_combinations), 1):
        if groups:
            logger.info('Groups: {0}'.format(
                click.style(' / '.join(groups), bold=True),
            ))
        else:
            logger.info('Ungrouped:')

        for host in hosts:
            meta = state.meta[host.name]

            # Didn't connect to this host?
            if host.name not in state.connected_hosts:
                logger.info('[{0}]\tNo connection'.format(
                    click.style(host.name, 'red', bold=True),
                ))
                continue

            logger.info(
                '[{0}]\tOperations: {1}\t    Commands: {2}'.format(
                    click.style(host.name, bold=True),
                    meta['ops'], meta['commands'],
                ),
            )

        if i != len(group_combinations):
            print()


def print_results(state, inventory):
    group_combinations = _get_group_combinations(inventory)

    for i, (groups, hosts) in enumerate(six.iteritems(group_combinations), 1):
        if groups:
            logger.info('Groups: {0}'.format(
                click.style(' / '.join(groups), bold=True),
            ))
        else:
            logger.info('Ungrouped:')

        for host in hosts:
            # Didn't conenct to this host?
            if host.name not in state.connected_hosts:
                logger.info('[{0}]\tNo connection'.format(
                    click.style(host.name, 'red', bold=True),
                ))
                continue

            results = state.results[host.name]

            meta = state.meta[host.name]
            success_ops = results['success_ops']
            error_ops = results['error_ops']

            # If all ops got complete (even with ignored_errors)
            if results['ops'] == meta['ops']:
                # Yellow if ignored any errors, else green
                color = 'green' if error_ops == 0 else 'yellow'
                host_string = click.style(host.name, color)

            # Ops did not complete!
            else:
                host_string = click.style(host.name, 'red', bold=True)

            logger.info('[{0}]\tSuccessful: {1}\t    Errors: {2}\t    Commands: {3}/{4}'.format(
                host_string,
                click.style(six.text_type(success_ops), bold=True),
                error_ops
                if error_ops == 0
                else click.style(six.text_type(error_ops), 'red', bold=True),
                results['commands'], meta['commands'],
            ))

        if i != len(group_combinations):
            print()
