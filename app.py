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
import rethinkdb as r

from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from tornado import httpserver, ioloop, web
from tornado.escape import json_encode

connection = dict(host=os.getenv('RBD_HOST') or 'localhost',
                  port=os.getenv('RDB_PORT') or '28015',
                  db='earthquakes')


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
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            autoreload=True,
            serve_traceback=True
        )
        web.Application.__init__(self, handlers, **settings)


class MapHandler(web.RequestHandler):
    """Returns homepage map and list of quakes in
    json
    """

    def get(self):
        self.render('index.html')


class QuakesHandler(web.RequestHandler):

    """Returns a list of quakes from the db near the
    users location in json
    """
    def prepare(self):
        try:
            r.connect(**connection)
        except RqlDriverError, e:
            print ('{}'.format(e))

    def on_finish(self):
        r.connect(**connection).close()

    def get(self):
        results = r.table('quakes').order_by(r.desc(
                                             r.row['properties']['mag'])
                                             ).run(r.connect(**connection))
        self.write(json_encode(results))


class NearestHandler(web.RequestHandler):

    """Returns the nearest quake based on the
    users location in json
    """

    def prepare(self):
        try:
            r.connect(**connection)
        except RqlDriverError, e:
            print ('{}'.format(e))

    def on_finish(self):
        r.connect(**connection).close()

    def get(self):

        latitude = float(self.get_argument('latitude'))
        longitude = float(self.get_argument('longitude'))

        if not latitude or not longitude:
            self.write(json_encode(dict(err='Invalid Point')))

        locations = [latitude, longitude]

        results = r.table('quakes').get_nearest(
            r.point(locations[0], locations[1]), index='geometry', unit='mi'
        ).run(r.connect(**connection))
        self.write(json_encode(results))


if __name__ == '__main__':
    server = create_app()
    server.listen(8080)
    ioloop.IOLoop.instance().start()
