import click

verbose = False

def echo(message=None, file=None, nl=True, err=False, color=None):
    if verbose:
        click.echo(message=message,
                   file=file,
                   nl=nl,
                   err=err,
                   color=color)
