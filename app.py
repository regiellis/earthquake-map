# !/usr/bin/env python
# -*- coding: utf-8 -*-

# === Application : Earthquakes ===

"""
Application login file for for the Earthquakes
project

Earthquakes.app

:author: Regi E. <regi@persona.io>
:created: 20141123
:desc: Handles all application logic

:req: rethinkdb [http://rethinkdb.com]
:req: tornando [http://www.tornadoweb.org/en/stable/]

Check requirements for all needed cheeseshop installs

Write your code as if the person maintaining it is a
Homicidal Maniac who knows where you live...

"""

import os
import sched
import datetime
import time

import rethinkdb as r

from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from tornado import httpserver, ioloop, web, gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode


from settings import CONNECTION, APP_SETTINGS
from helpers import msg


def database_connect(connection=None):

    """Does a quick connection to the database, with error
    message"""

    try:
        r.connect(**CONNECTION)
    except RqlDriverError as e:
        msg('{}'.format(e), 'error')

    return None


class create_app(web.Application):

    """Create application instance with the following
    settings and handler

    :handler: = /        MapHandler
                /quakes  QuakesHandler, returns json
                /nearest NearestHandler, returns json

    """

    def __init__(self):
        handlers = [
            (r'/', MapHandler),
            (r'/quakes', QuakesHandler),
            (r'/nearest', NearestHandler)
        ]
        web.Application.__init__(self, handlers, **APP_SETTINGS)


class BaseHandler(web.RequestHandler):

    def prepare(self):
        database_connect(CONNECTION)
        self.conn = r.connect(**CONNECTION)

    def on_finish(self):
        self.conn.close()


class MapHandler(BaseHandler):

    """Returns homepage map and list of quakes in
    json
    """
    def get(self):
        current_date = datetime.date.today().strftime('%B %d, %Y')
        quakes = r.table('quakes') \
            .pluck('id', {'properties': ['mag', 'time', 'place']}, {'geometry': ['coordinates']}) \
            .order_by(r.desc(r.row['properties']['mag'])).run(self.conn)

        page_vars = dict(
            current_date=current_date,
            quakes=quakes
        )
        self.render('index.html', page_vars=page_vars)


class QuakesHandler(BaseHandler):

    """Returns a list of quakes from the db near the
    users location in json
    """

    def get(self):
        results = r.table('quakes') \
            .pluck('id', {'properties': ['mag', 'time', 'place']}, {'geometry': ['coordinates']}) \
            .order_by(r.desc(r.row['properties']['mag'])).run(self.conn)
        self.set_header('Content-Type', 'application/json')
        self.write(json_encode(results))


class NearestHandler(BaseHandler):

    """Returns the nearest quake based on the
    users location in json
    """

    def post(self):

        try:
            latitude = float(self.get_argument('latitude'), 'Invalid Point')
            longitude = float(self.get_argument('longitude'), 'Invalid Point')
        except ValueError:
            message = 'Invalid Point'
            self.send_error(400, message=message)

        location = [latitude, longitude]

        results = r.table('quakes').get_nearest(
            r.point(location[1], location[0]), index='geometry', unit='mi',
            max_dist=500).run(self.conn)

        self.set_header('Content-Type', 'application/json')
        self.write(json_encode(results))


if __name__ == '__main__':
    server = create_app()
    server.listen(8080)
    msg('Server Started on 8080 ...', 'success')
    ioloop.IOLoop.instance().start()
