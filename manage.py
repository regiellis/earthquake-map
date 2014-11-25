# !/usr/bin/env python
# -*- coding: utf-8 -*-

# === Project Management Task ===

"""
The manage.py file relies on the click library for
some quick setup managment tasks.

Earthquakes.manage

:author: Regi E. <regi@persona.io>
:created: 20141123
:desc: Manages shortcuts for initial development and database
       tasks and tools in a simple interface

:req: rethinkdb [http://rethinkdb.com]
:req: click [http://click.pocoo.org/3/]

Check requirements for all needed cheeseshop installs

Write your code as if the person maintaining it is a
Homicidal Maniac who knows where you live...

"""

import os
import sys
import subprocess32

import click
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError


# === RethinkDB Management Tasks ===

try:
    conn = r.connect(host='localhost', port=28015)
    click.echo(click.style('Databases connection established', fg='green'))
except RqlDriverError, e:
    click.echo(click.style('{}'.format(e), fg='red'))


feed_url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson'

RETHINK_CONTEXT = dict(
    default_map={
        'create_database': {'database': None},
        'drop_databse': {'database': None},
        'refresh_database': {'database': None},
        'import_database_feed':
        {'url': 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson'}
    }
)


@click.group(context_settings=RETHINK_CONTEXT)
def rethinkdb_cli():
    pass


@rethinkdb_cli.command()
@click.option('--database', '-d', default=None,
              help='Creates a Rethinkdb Databases (Production/Test)')
@click.option('--development', '-dev', default=False,
              help='Will create a development database')
def create_database(database=None, **kwargs):

    """Creates new database/test based on the provided name
    """

    database_set = ['{}'.format(database), '{}_test'.format(database)]

    if kwargs['development']:
        database_set.append('{}_dev'.format(database))

    try:
        for database in database_set:
            r.db_create(database).run(conn)
        click.echo(click.style('Databases Created', fg='green'))
    except RqlRuntimeError, e:
        click.echo(click.style('{}'.format(e), fg='red'))


@rethinkdb_cli.command()
@click.option('--database', '-d', default=None,
              help='Selects a Rethinkdb Databases (Production/Test)')
@click.option('--tables', '-t', default=None, help='Python list of tables')
@click.option('--all', '-a', default=False, help='Create tables in all databases')
def create_tables(database=None, **kwargs):

    """Creates new tables in the provided database
    """

    tables = kwargs['tables'].split(',')

    if not kwargs['tables']:
        click.echo(click.style('You need to provide a list of tables', fg='red'))
        sys.exit()

    for table in tables:
        r.db(database).table_create(table).run(conn)


@rethinkdb_cli.command()
@click.option('--database', '-d', default=None,
              help='Drop database based on name provided')
@click.option('--all', '-a', default=False,
              help='Will drop development and test databases')
def drop_database(database=None, **kwargs):

    """Drops databases based on the provided name and options
    """
    database_set = ['{}'.format(database)]

    if all:
        for item in ['{}_test'.format(database), '{}_dev'.format(database)]:
            database_set.append(item)

    try:
        for database in database_set:
            r.db_drop(database).run(conn)
        click.echo(click.style('Database Dropped', fg='green'))
    except RqlRuntimeError, e:
        click.echo(click.style('{}'.format(e), fg='red'))


@rethinkdb_cli.command()
@click.option('--database', '-d', default=None,
              help='Import into the provided database')
@click.option('--table', '-t', default=None,
              help="Table the the feed will be impoted into")
def import_database_feed(database=None, url=None, **kwargs):

    """Imports feed into database and normalize it
    """
    if not url:
        url = feed_url

    if not kwargs['table']:
        click.echo(click.style('You need to provide a list of tables', fg="red"))
        sys.exit()

    # Import the earthquake feed data
    r.db(database).table(kwargs['table']).insert(r.http(url)['features'].
                                                 merge(lambda quake:
                                                       {'geometry': r.point(quake['geometry']['coordinates'][0],
                                                                            quake['geometry']['coordinates'][1])})).run(conn)

    # Add a index for the qauke data
    r.db(database).table(kwargs['table']).index_create('geometry', geo=True).run(conn)
    conn.close()






### === Generate Documentation ===

if __name__ == '__main__':
    rethinkdb_cli()
