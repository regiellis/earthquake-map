# -*- coding: utf-8 -*-

# === Project Helper Commands ===

"""
The manage.py file relies on the click library for
some quick setup managment tasks via cli

Earthquakes.helpers

:author: Regi E. <regi@persona.io>
:created: 20141123
:desc: Simple helper functions to use in the management
commands

Check requirements for all needed cheeseshop installs

Write your code as if the person maintaining it is a
Homicidal Maniac who knows where you live...

"""

import os

import modules

FEED_URL = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson'
CONNECTION = dict(host=os.getenv('RBD_HOST') or 'localhost', port=os.getenv('RDB_PORT') or '28015',
                  db=os.getenv('RBD_DB') or 'earthquakes')
APP_SETTINGS = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"),
                    static_path=os.path.join(os.path.dirname(__file__), "static"),
                    ui_modules=modules,
                    debug=True,
                    autoreload=True,
                    serve_traceback=True)
