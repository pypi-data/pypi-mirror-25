
import os
import json
import difflib

import click

from storage import Storage
from mangastream import check_release, get_all_manga

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

@click.command(help="Adding a manga to your favorites with the last released chapter")
@click.argument('name', type=click.STRING)
@click.argument('last_chapter', type=click.INT)
@pass_storage
def add(storage, name, last_chapter):
    database = get_all_manga()
    if name not in database:
        error_msg = "The manga [{}] did not exist".format(name)
        matches = difflib.get_close_matches(name, database, 3)
        error_msg += '\n\nDid you mean one of these?\n    %s' % '\n    '.join(matches)
        click.echo(error_msg)
        exit()

    click.echo("(mangastream-notifier) adding name=[{}] last_chapter=[{}]".format(name, last_chapter))
    storage.add(name, last_chapter)

@click.command(help="Deleting a manga from your favorites")
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
