
import os
import json

import click

from storage import Storage
from mangastream import check_release

pass_storage = click.make_pass_decorator(Storage, ensure=True)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@pass_storage
def cli(storage):
    ctx = click.get_current_context()
    if ctx.invoked_subcommand is None:
        release = check_release(storage.config)
        if release:
            storage.update(release)

@click.command(help="")
@click.argument('name', type=click.STRING)
@click.argument('last_chapter', type=click.INT)
@pass_storage
def add(storage, name, last_chapter):
    click.echo("(mangastream-notifier) adding name=[{}] last_chapter=[{}]".format(name, last_chapter))
    storage.add(name, last_chapter)

@click.command()
@click.argument('name', type=click.STRING)
@pass_storage
def delete(storage, name):
    click.echo("(mangastream-notifier) deleting name=[{}]".format(manga))
    storage.delete(name)

# Generate click commands
cli.add_command(add)
cli.add_command(delete)

if __name__ == '__main__':
    cli()
