# -*- coding: utf-8 -*-

"""Console script for xml_delta."""
import os
import click

@click.command()
@click.option('-e', 'endpoint', help='Checks if endpoint is responding.')
@click.option('-p', 'proxy', help='Proxy for request.')
@click.option('-t', 'timeout', default=10, help='Timeout for request.')
def check_network(endpoint, proxy, timeout):
    from network.ping import ping_url
    ping_result = ping_url(endpoint, timeout=timeout, proxy=proxy)
    if ping_result:
        click.echo('Ping success.')
    else:
        click.echo('Ping failed.')


@click.command()
@click.option('-v', 'verbose', is_flag=True, help='Will print verbose messages.')
@click.option('-type', 'type', required=True, help='Type of file parsed.')
@click.option('-tag', 'tag', required=True, help='Tag to extract from xml.')
@click.option('-pk', 'pk', required=True, help='Primary key tag to use for identification of records.')
@click.option('-file', 'file', type=click.Path(), required=True, help='File to parse.')
@click.option('-endpoint', 'endpoint', default=None, help='Endpoint to post data to.')
def xml_delta(verbose, file, type, tag, pk, endpoint):
    from delta_task import DeltaTask
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


