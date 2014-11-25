RethinkDB Earthquake Map
--------------

This application uses data from the USGS to display earthquakes detected over the last 30 days. The earthquakes are displayed in a list view and an interactive map. The backend is written with node.js and RethinkDB, taking advantage of the new GeoJSON functionality introduced in RethinkDB 1.15. The frontend is built with AngularJS and the Leaflet mapping library, with map tiles provided by OpenStreetMap project.

![Earthquake Map](/static/earthquake-map.png?raw=true)

Features:
  * Deploy Intergration: `./manage.py deploy`


Dependencies
------------
Tornado [http://www.tornadoweb.org/en/stable/]
Click [http://click.pocoo.org/3/]
RethinkDB [http://www.rethinkdb.com/]


Usage
-----

Database Tools:


Documentation Tools:



Known Issues
------------


Thanks
------
segphault [https://github.com/segphault] - For original node implementation

