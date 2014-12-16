/**
 * Earthquakes - Vuejs
 */


// Vuejs Configuration
Vue.config.prefix = 'data-';
Vue.config.delimiters = ['[[', ']]'];

(function(Vue, win, doc, undefined) {

    // Current Date or Quake Date

    var months = ["January", "February", "March", "April", "May", "June", "July", "August",
        "September", "October", "November", "December"],
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    var header_view = new Vue({

        el: 'header',
        // Grab that date container
        data: {
            title: "Earthquakes",
            date: undefined
        },
        created: function() {
            this.$watch('date', function(newVal, oldVal) {
                if (!newVal) return;
                quakes.__updateQuakeData(this.$data.date);
            });

        },
        computed: {
            currentDate: {
                get: function() {
                    formatter = (this.date) ? new Date(this.date) : undefined;
                    if (!formatter) return "Last 30 days";

                    var formatted =
                        days[formatter.getUTCDay()] + ', ' + months[formatter.getUTCMonth()] + ' ' +
                        formatter.getUTCDate() + ' ' + formatter.getFullYear();

                    return formatted
                }
            }
        }
    });

    // Instantiate the map and configure the tile layer
    // The map uses tiles provided by the OpenStreetMap project
    var map_view = new Vue({

        el: '#map',
        computed: {},
        created: function _created_map() {
            this.__init();
            this.__geolocate();
            // this.$watch('userLocation', function(newVal, oldVal) {
            //     if (!newVal) return;
            //     this.__geolocate(newVal, oldVal);
            // }, this);
        },
        methods: {
            __init: function __init_map() {
                map = L.map("map").setView([35.685, 139.751], 2);
                map.addLayer(L.tileLayer(
                  "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
                  {attribution: "<a href=\"http://osm.org/copyright\">OpenStreetMap</a>"}
                ));
                return map;
            },
            __geolocate: function __geolocate_map(newVal, oldVal) {

                view = this;

                // if (!newVal) return;

                if (!!navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(function(pos) {
                        var userLocated = [pos.coords.latitude,
                                           pos.coords.longitude];
                        view.$data = { 'userLocation': userLocated };

                        // if userLocated)

                        var location = L.latLng(userLocated[0], userLocated[1]);
                            userMarker = L.marker(location, {
                                icon: L.icon({ iconUrl: "/static/mark.png"})
                            });
                        map.setView(location, 4).addLayer(userMarker);
                        view.__nearest(userLocated);
                    });
                };
            },
            __nearest: function(userLocated) {
                // This function uses the browser geolocation APIs to fetch the user's
                // location. The coordinates are passed to the backend's `/nearest`
                // endpoint as URL query parameters. The `/nearest` endpoint returns
                // the closest earthquake and its distance, which are assigned to
                // variables within the current scope
                var dataWorker = new Worker('/static/data_worker.js'),
                    _url = 'http://localhost:8080/nearest',
                    userLocated = 'latitude=' + userLocated[0] + '&longitude=' + userLocated[1]

                dataWorker.postMessage([_url, 'post', userLocated]);

                dataWorker.onmessage = function __dataWorker_message_qaukes(msg) {
                   view.$data.nearest = {
                        dist: msg.data[0].dist,
                        quake: msg.data[0].doc.id
                    }
                    console.log('Data recieved from worker');
                }

            }
        }
    });

    // This function fetches the list of earthquakes from the backend's
    // `/quakes` endpoint. After fetching the quakes, it extracts the
    // coordinates and creates a place marker which is stored in a
    // property of the quake object. The actual place markers are applied
    // in the `$watchCollection` statement above
    var _url = 'http://localhost:8080/quakes';
    var quakes = new Vue({

        el: '#quakes',
        data: {},
        created: function _created_quakes() {
            (!!window.Worker) ? this.__dataWorker(this) : this.__dataFetch(this);
            this.$watch('quakes', function() {
                this.__markerQuakes(this.$data.quakes);
            });
        },
        filters: {
            formatDate: function _filter_formatDate_quakes(date) {
                var date = new Date(date);
                return date.toDateString();
            },
            formatMagnitude: function _filter_formatMagnitude_quakes(num) {
                return parseFloat(num).toFixed(1);
            }
        },
        methods: {
            __dataFetch: function __dataFetch_quakes(context) {

                var _fall_back = function(url, func, undefined) {
                    if (typeof XMLHttpRequest !== undefined) {
                        xhr = new XMLHttpRequest();
                    }
                    xhr.open('GET', url, true);
                    xhr.onreadystatechange = function() {
                        if (xhr.readyState == 4 && xhr.status == 200) {
                            func.apply(this, xhr);
                        }
                    }
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.send(null);
                }
                _fall_back(_url, function() {
                    context.$data = { 'quakes': JSON.parse(this.response) };
                });
            },
            __dataWorker: function __dataWorker_quakes(context) {
                var dataWorker = new Worker('/static/data_worker.js');

                dataWorker.postMessage([_url, 'get', {}]);

                dataWorker.onmessage = function __dataWorker_message_quakes(msg) {
                    var quakes = []
                    for ( item in msg.data) {
                        quakes.push(msg.data[item]);
                    }
                    context.$data = { 'quakes': quakes };
                    console.log('Data recieved from worker');
                }
            },
            __selectedQuake: function(quake) {
                quake.marker.setStyle({
                    fillColor: '#ff0000',
                    color: '#ff0000'
                });
                map.removeLayer(quake.marker).addLayer(quake.marker);
                map.setView(quake.point, 5, {animate: true});
            },
            __markerQuakes: function __markerQuakes(quakes) {
                // TODO: MOVE TO MAP VIEW
                var markers = new L.FeatureGroup();

                markers.clearLayers();
                for (var quake in quakes) {
                    quake = quakes[quake];
                    quake.point = L.latLng(
                      quake.geometry.coordinates[1],
                      quake.geometry.coordinates[0])

                    quake.marker = L.circleMarker(quake.point, {
                        radius: quake.properties.mag * 2,
                        fillColor: "#616161", color: "#616161"
                    });
                    markers.addLayer(quake.marker);
                }
                map.addLayer(markers);
            },
            __updateQuakeData: function __updateQuakeData(date) {
                var date = new Date(date).getTime(),
                    currentDate = new Date().getTime(),
                    quakes = this.$data.quakes,
                    newQuakes = []

                // console.log(date, this.$data.quakes);
                // console.log(currentDate);
                for (var quake in quakes) {
                    quake = quakes[quake]
                    if (quake.properties.time > date && quake.properties.time < currentDate) {
                        newQuakes.push(quake);
                    }
                    this.$data = { 'quakes': newQuakes}
                }

            }
        }
    });


})(Vue, window, document, undefined);










