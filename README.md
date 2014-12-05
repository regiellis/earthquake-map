RethinkDB Earthquake Map
--------------

[![Build Status](https://api.shippable.com/projects/547485f8d46935d5fbbe8a30/badge?branchName=develop)](https://app.shippable.com/projects/547485f8d46935d5fbbe8a30/builds/latest)

This application uses [data from the USGS](http://earthquake.usgs.gov/earthquakes/feed/v1.0/) to display earthquakes detected over the last 30 days. The earthquakes are displayed in a list view and an interactive map. The backend is written with node.js and [RethinkDB](http://rethinkdb.com/), taking advantage of the new GeoJSON functionality introduced in RethinkDB 1.15. The frontend is built with AngularJS and the Leaflet mapping library, with map tiles provided by [OpenStreetMap project](http://www.openstreetmap.org/)

![Earthquake Map](/static/earthquake-map.png?raw=true)

Features
------------
    * CLI Intergration: `pip install --editable .`


Dependencies
------------
    * Tornado [http://www.tornadoweb.org/en/stable/]
    * Click [http://click.pocoo.org/3/]
    * RethinkDB [http://www.rethinkdb.com/]


Usage
-----

Run `python setup install` or `pip install -r requirements.txt`
To install cli tools, run `pip install -e .`

1. Start RethinkDB
2. If CLI is installed, run `rethinkdb_cli database earthquakes` then `rethinkdb_cli -db earthquakes create_tables quake`
3. `rethinkdb_cli import_database_feed -i geometry -g earthquakes quakes`
4. `python app.py` to start server, navigate to http://localhost:8080/
5. Profit!


Database Tools:
-----

Run `rethinkdb_cli [cmd]`:
    * create_tables         Manages table/s based on the provided...
    * database              Manages database/s based on the provided...
    * import_database_feed  Imports feed into database and normalize it

Documentation Tools:
-----

Run `docs_cli [cmd]`:
    *  document  Uses pycco to document the current code base

Known Issues
------------


Thanks
------
segphault [https://github.com/segphault] - For original node implementation

