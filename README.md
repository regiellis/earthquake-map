RethinkDB Earthquake Map
--------------

[![Build Status](https://api.shippable.com/projects/547485f8d46935d5fbbe8a30/badge?branchName=develop)](https://app.shippable.com/projects/547485f8d46935d5fbbe8a30/builds/latest)


OG Description:
---------------
This application uses [data from the USGS](http://earthquake.usgs.gov/earthquakes/feed/v1.0/) to display earthquakes detected over the last 30 days. The earthquakes are displayed in a list view and an interactive map. The backend is written with node.js and [RethinkDB](http://rethinkdb.com/), taking advantage of the new GeoJSON functionality introduced in RethinkDB 1.15. The frontend is built with AngularJS and the Leaflet mapping library, with map tiles provided by [OpenStreetMap project](http://www.openstreetmap.org/)

Changes:
--------
Since this was my own exploration of RethinkDB, I decided to make the following changes:
    * Tornado < Nodejs
    * Vuejs & Web Workers < Angularjs


![Earthquake Map](/screenshot/earthquake-map.png?raw=true)

Features
------------
    * CLI Intergration: `pip install --editable .` or 'python setup install'


Dependencies
------------
    * Tornado [http://www.tornadoweb.org/en/stable/]
    * Click [http://click.pocoo.org/3/]
    * RethinkDB > 1.15 [http://www.rethinkdb.com/]
    * Vuejs [http://vuejs.org/]


Usage
-----

Run `python setup install` and then `pip install -r requirements.txt`

1. Start RethinkDB
2. If CLI is installed, run `manage database earthquakes` then `manage table earthquakes quake -i geometry -g`
3. `manage import_database_feed earthquakes quakes`
4. `python app.py` or `manage app_server` to start server, navigate to http://localhost:8080/
5. Profit!


Database Tools:
-----

Run `manage [cmd]`:
    * app_server   Start development server
    * database     Options for creating/managing databases
    * import_feed  Imports feed into database and normalize it
    * table        Options for creating/managing tables

Documentation Tools:
-----

Run `manage [cmd]`:
    *  document  Uses pycco to document the current code base

Known Issues
------------


Thanks
------
segphault [https://github.com/segphault] - For original node implementation

