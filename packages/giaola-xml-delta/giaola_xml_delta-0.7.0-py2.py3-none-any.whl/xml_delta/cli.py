# -*- coding: utf-8 -*-

"""Console script for xml_delta."""
import os

import click

import echo

from sqlalchemy_paginator import Paginator

@click.command()
@click.option('-e', 'endpoint', required=True, help='Checks if endpoint is responding.')
@click.option('-t', 'timeout', default=10, help='Timeout for request.')
@click.option('-v', 'verbose', is_flag=True, help='Verbose mode.')
def check_network(endpoint, timeout, verbose):
    from network.ping import ping_url
    echo.verbose = verbose

    ping_result = ping_url(endpoint, timeout=timeout)
    if ping_result:
        echo.echo('Ping success.')
    else:
        echo.echo('Ping failed.')


from xml_delta import settings


@click.command()
@click.option('-t', 'type', required=True, help='Type to delete records for.')
def cleanup_type(type):
    from storages import SqlAlchemyStorage
    storage = SqlAlchemyStorage(connection=settings.STORAGE_DATABASE_URL, type=type)
    storage.cleanup()

@click.command()
def clear_db():
    from storages import SqlAlchemyStorage
    storage = SqlAlchemyStorage(connection=settings.STORAGE_DATABASE_URL, type=type)
    storage.clear_all()



@click.command()
@click.option('-t', 'type', required=True, help='Type to fetch errors for.')
def errors(type):
    from storages import SqlAlchemyStorage
    storage = SqlAlchemyStorage(connection=settings.STORAGE_DATABASE_URL, type=type)
    errors = storage.fetch_errors()
    for error in errors:
        click.echo("error for listing with das_unique_id: {0}".format(error.dasUniqueId))


@click.command()
@click.option('-t', 'type', required=True, help='Type to fetch errors for.')
def errors_count(type):
    from storages import SqlAlchemyStorage
    storage = SqlAlchemyStorage(connection=settings.STORAGE_DATABASE_URL, type=type)
    click.echo("{0} : {1} errors".format(type, storage.fetch_errors().count()))


@click.command()
@click.option('-t', 'type', required=True, help='Type to sync errors for.')
@click.option('-endpoint', 'endpoint', required=True, help='Endpoint to post data to.')
@click.option('-page', 'page_size', default=10, help='Page size.')
def errors_sync(type, endpoint, page_size):
    from storages import SqlAlchemyStorage
    from network.rest import Rest
    storage = SqlAlchemyStorage(connection=settings.STORAGE_DATABASE_URL, type=type)
    errors_query = storage.fetch_errors()


    network = Rest(True,
                   endpoint,
                   {},
                   settings.NETWORK_RETRIES,
                   settings.NETWORK_CONNECTION_TIMEOUT)

    def send(errors):
        click.echo('Sending {0} error'.format(len(errors)))
        to_send = {error.dasUniqueId: error.data
                   for error in errors}
        network_errors = network.send(to_send)
        storage.bulk_update(to_send, network_errors)

    errors_to_send = []

    paginator = Paginator(errors_query, page_size)

    for page in paginator:
        click.echo("Sending page {0}/{1}".format(page.number, paginator.total_pages))
        send(page.object_list)

    send(errors_to_send)


@click.command()
@click.option('-t', 'type', required=True, help='Type to count')
def count_type(type):
    from storages import SqlAlchemyStorage
    storage = SqlAlchemyStorage(connection=settings.STORAGE_DATABASE_URL, type=type)
    count = storage.count()
    click.echo('{0} : {1} rows'.format(type, count))


@click.command()
@click.option('-file', 'file', type=click.Path(), required=True, help='File to parse.')
@click.option('-tag', 'tag', required=True, help='Tag to extract from xml.')
@click.option('-v', 'verbose', is_flag=True, help='Will print verbose messages.')
def xml_delta_parse(file, tag, verbose):
    from parsers import XMLToDictParser
    parser = XMLToDictParser(1)
    parser.parse(file, tag)

@click.command()
@click.option('-type', 'type', required=True, help='Type of file parsed.')
@click.option('-tag', 'tag', required=True, help='Tag to extract from xml.')
@click.option('-pk', 'pk', required=True, help='Primary key tag to use for identification of records.')
@click.option('-file', 'file', type=click.Path(), required=True, help='File to parse.')
@click.option('-endpoint', 'endpoint', default=None, help='Endpoint to post data to.')
@click.option('-v', 'verbose', is_flag=True, help='Will print verbose messages.')
def xml_delta(verbose, file, type, tag, pk, endpoint):
    from delta_task import DeltaTask
    echo.verbose = verbose
    delta_task = DeltaTask(type, file, tag, pk, endpoint)
    delta_task.execute()


@click.command()
@click.option('-path', 'path', type=click.Path(), required=True)
@click.option('-prefix', 'prefix', type=click.Path(), required=True)
@click.option('-type', 'type', required=True, help='Type of file parsed.')
@click.option('-tag', 'tag', required=True, help='Tag to extract from xml.')
@click.option('-pk', 'pk', required=True, help='Primary key tag to use for identification of records.')
@click.option('-endpoint', 'endpoint', default=None, help='Endpoint to post data to.')
def xml_delta_watcher(path, prefix, type, tag, pk, endpoint):
    from watchers import RegexWatcher
    watcher = RegexWatcher(path, prefix, type=type, tag=tag, pk=pk, endpoint=endpoint)
    watcher.start()

@click.command()
@click.option('-f', 'file', type=click.Path(), required=True, help='File to read deleted ids from.')
@click.option('-e', 'endpoint', required=True, default=None, help='Endpoint to delete data.')
def xml_delta_delete(file, endpoint):
    from xml_delta.network import Rest
    network_manager = Rest(True, endpoint)
    with open(file, 'r') as deletion_file:
        for id in deletion_file:
            network_manager.delete(id)
