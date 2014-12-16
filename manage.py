# -*- coding: utf-8 -*-

# === Project Management Task ===

"""
The manage.py file relies on the click library for
some quick setup managment tasks via cli

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

import sys
import subprocess32

import click
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError, RqlClientError

from settings import FEED_URL, msg


# === RethinkDB Management Tasks ===

@click.group()
def manage():

    """
    Simple CLI tools for managing the database interactions
    within the project
    """

    try:
        r.connect('localhost', 28015).close()
        msg('Databases connection established...')
    except RqlDriverError as e:
        msg('Database connection problem -> {}'.format(e), 'error')
        sys.exit(1)


@manage.command()
@click.argument('database', nargs=-1)
@click.option('--create', '-c', is_flag=True, help='Creates Database[s]')
@click.option('--drop', '-d', is_flag=True, help='Drops Database[s]')
@click.option('--list', '-l', is_flag=True, help="List Database[s]")
def database(database=None, **kwargs):

    """Options for creating/managing databases
    """

    conn = r.connect('localhost', 28015)

    if not kwargs['create'] and not kwargs['drop'] and not kwargs['list']:
        msg('You must provided at least one database option [-c, -d, -l]', 'error')
        sys.exit(1)

    if not database and not kwargs['list']:
        msg('You need to provided database[s] name', 'error')
        sys.exit(1)

    try:
        for entry in database:
            r.db_create(entry).run(conn) if kwargs['create'] else None
            r.db_drop(entry).run(conn) if kwargs['drop'] else None

        if not kwargs['list']:
            msg('Database[s] operation succeed...', 'success')

        if kwargs['list']:
            msg('Current Databases -> {}'.format(r.db_list().run(conn)))

        conn.close()

    except (RqlRuntimeError, RqlDriverError, RqlClientError) as e:
        msg('Database operation issue -> {}'.format(e), 'error')


@manage.command()
@click.argument('database', nargs=1)
@click.argument('table', nargs=-1)
@click.option('--create', '-c', is_flag=True, help='Creates Table[s]')
@click.option('--drop', '-d', is_flag=True, help='Drops Table[s]')
@click.option('--list', '-l', is_flag=True, help="List Table[s]")
@click.option('--index', '-i', help="[database] [table] -i [index]")
@click.option('--geo', '-g', is_flag=True, help="Make index geospaital")
def table(database=None, table=None, **kwargs):

    """Options for creating/managing tables
    """

    conn = r.connect('localhost', 28015)

    if not kwargs['create'] and not kwargs['drop'] and not kwargs['list'] \
            and not kwargs['index']:

        msg('You must provided at least one table option [-c, -d, -l]', 'error')
        sys.exit(1)

    if not database and not kwargs['list']:
        msg('You need to provided Database[s] name', 'error')
        sys.exit(1)

    if not table and not kwargs['list']:
        msg('You need to provided table[s] name', 'error')
        sys.exit(1)

    try:
        for entry in table:
            r.db(database).table_create(entry).run(conn) if kwargs['create'] else None
            r.db(database).table_drop(entry).run(conn) if kwargs['drop'] else None

        if kwargs['index']:
            r.db(database).table(table[0]).index_create(kwargs['index'], geo=kwargs['geo']).run(conn)
            msg('Table[s] index added...', 'success')

        if not kwargs['list'] and not kwargs['index']:
            msg('Table[s] operation succeed...', 'success')

        if kwargs['list']:
            msg('Current Databases -> {}'.format(r.db(database).table_list().run(conn)))

        conn.close()

    except (RqlRuntimeError, RqlDriverError, RqlClientError) as e:
        msg('Table operation issue -> {}'.format(e), 'error')


# This function is written only to work with this project and is
# brittle by design
@manage.command()
@click.argument('database')
@click.argument('table')
def import_feed(database=None, table=None):

    """Imports feed into database and normalize it
    """

    conn = r.connect('localhost', 28015)

    # Import the earthquake feed data
    r.db(database).table(table).insert(r.http(FEED_URL)['features'].
                                       merge(lambda quake: {'geometry':
                                       r.point(quake['geometry']['coordinates'][0],
                                       quake['geometry']['coordinates'][1])})).run(conn)

    conn.close()


### === Generate Documentation ===

@manage.command()
def document():

    """Uses pycco to document the current code base
    """

    subprocess32.call('pycco -d docs/ manage.py app.py', shell=True)


@manage.command()
def app_server():

    """Start development server
    """

    subprocess32.call('python app.py', shell=True)


if __name__ == '__main__':
    manage()
