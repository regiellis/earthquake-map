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

from helpers import msg, database_check, table_check


# === RethinkDB Management Tasks ===

feed_url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson'


@click.group()
def rethinkdb_cli():

    """
    Simple sanity check before running any commands
    """
    try:
        r.connect('localhost', 28015).close()
        msg('Databases connection established')
    except RqlDriverError, e:
        msg('Database problem -> {}'.format(e), 'error')
        sys.exit(1)


@rethinkdb_cli.command()
@click.argument('database', nargs=-1)
@click.option('--drop', '-d', is_flag=True, help="Drop database[s]")
@click.option('--list', '-l', is_flag=True, help="List database[s]")
def database(database=None, **kwargs):

    """Manages database/s based on the provided name[s]
    and options passed.
    """

    conn = r.connect('localhost', 28015)

    if not database:
        database_check(conn=conn)

    try:
        for entry in database:

            if kwargs['drop']:
                r.db_drop(entry).run(conn)
                msg('Database[s] {} dropped ...'.format(entry), 'success')
            else:
                r.db_create(entry).run(conn)
                msg('Database[s] {} created ...'.format(entry), 'success')

        if kwargs['list']:
            msg('Current Databases -> {}'.format(r.db_list().run(conn)))

        conn.close()
    except (RqlClientError, RqlRuntimeError, RqlDriverError) as e:
        msg('Problem creating the database[s] -> {}'.format(e), 'error')
        sys.exit(1)


@rethinkdb_cli.command()
@click.argument('tables', nargs=-1)
@click.option('--database', '-db', help="Database to added tables")
@click.option('--drop', '-d', is_flag=True, help="Drop table[s]")
@click.option('--list', '-l', is_flag=True, help="List table[s]")
@click.option('--all', '-a', is_flag=True, help="Will drop all tables in selected database")
def create_tables(tables=None, **kwargs):

    """Manages table/s based on the provided name[s],
    database and options
    """

    conn = r.connect('localhost', 28015)
    database = kwargs['database']

    if not database:
        database_check(conn=conn)

    if kwargs['all']:
        #TODO: Prompt the user to make sure, they are sure
        try:
            tables = r.db(database).table_list().run(conn)
            for table in tables:
                r.db(database).table_drop(table).run(conn)
            msg('All tables dropped ...', 'success')
            conn.close()
            sys.exit()
        except (RqlClientError, RqlRuntimeError, RqlDriverError) as e:
            msg('Something went wrong -> {}'.format(e), 'error')
            sys.exit()

    if not tables:
        table_check(conn=conn, database=database)

    if kwargs['list']:
        msg('Current Table[s] -> {}'.format(r.db(database).table_list().run(conn)))

    try:
        for entry in tables:
            if kwargs['drop']:
                r.db(database).table_drop(entry).run(conn)
                msg('Table[s] {} dropped ...'.format(entry), 'success')
            else:
                r.db(database).table_create(entry).run(conn)
                msg('Table[s] {} created in {}...'.format(entry, database), 'success')

        if kwargs['list']:
            msg('Current Table[s] -> {}'.format(r.db(database).table_list().run(conn)))

        conn.close()
    except (RqlClientError, RqlRuntimeError, RqlDriverError) as e:
        msg('Problem creating the Table[s] -> {}'.format(e), 'error')
        sys.exit()


# This function is written only to work with this project and is
# brittle by design
@rethinkdb_cli.command()
@click.argument('database')
@click.argument('table')
@click.option('--index', '-i', help="Creates named index for the database")
@click.option('--geo', '-g', is_flag=True, help="Create index")
def import_database_feed(database=None, table=None, **kwargs):

    """Imports feed into database and normalize it
    """

    conn = r.connect('localhost', 28015)

    if not database:
        database_check(conn=conn)

    if not table:
        table_check(conn=conn, database=database)

    # Import the earthquake feed data
    r.db(database).table(table).insert(r.http(feed_url)['features'].
                                       merge(lambda quake: {'geometry':
                                       r.point(quake['geometry']['coordinates'][0],
                                       quake['geometry']['coordinates'][1])})).run(conn)

    # Add a index for the database
    if kwargs['index']:
        r.db(database).table(table).index_create(kwargs['index'], geo=kwargs['geo']).run(conn)
    conn.close()


### === Generate Documentation ===


@click.group()
def docs_cli():
    pass


@docs_cli.command()
def document():

    """Uses pycco to document the current code base
    """

    subprocess32.call('pycco -d docs/ manage.py app.py', shell=True)


if __name__ == '__main__':
    rethinkdb_cli()
    docs_cli()
