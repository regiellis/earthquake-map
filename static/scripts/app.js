/**
 * Earthquakes - Application JS
 */


var PSONA = (function __PSONA__(_, win, doc, undefined) {

    'use strict';

    /**
     * DataHandler
     * Simple data collection helper for making AJAX calls to the database
     * which will return a JSON object.
     * [func][fn] : callback function to handle data
     * [options][obj] :
     *     - type[str] ~> POST/GET
     *     - url[str] ~> '/quakes'
     *     - params[array] ~> [41.87811, -87.62980]
     *
     */

    var DataView = function __data_handler() {

            var _request = function __data_hander_request(type, url, func) {

                var xhr = (!!XMLHttpRequest) ? new XMLHttpRequest : false;

                xhr.onreadystatechange = function __onreadystatechange() {
                    (xhr.readyState == 4 && xhr.status == 200) ? func.apply(this, [xhr]) : false;
                };

                xhr.open(type, url, true);
                return xhr;
            };

            this.post = function __data_post(func, options) {
                if (!func) (console.warn('Callback Object Needed ~> DataHandler'), false);
                var params = options.params || [], url = options.url || '/nearest',
                    xhr = _request('POST', url, func);

                    (xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'),
                     xhr.send(params));

            }.bind(this);

            this.get = function __data_get(func, options) {
                if (!func) (console.warn('Callback Object Needed ~> DataHandler'), false);
                var options = options || {},
                    url = options.url || '/quakes',
                    xhr = _request('GET', url, func);

                    (xhr.setRequestHeader('Content-Type', 'application/json'),
                     xhr.send(null));

            }.bind(this);

            return { get: this.get,
                     post: this.post }
     };

    /**
     * CalenderView
     * Simple date handler for controlling display and basic filtering
     * of the data on the frontend
     * [date][date obj] : expects a date obj
     * [options][obj] :
     *     - type[str] ~> POST/GET
     *     - url[str] ~> '/quakes'
     *     - params[array] ~> [41.87811, -87.62980]
     */

    var CalenderView = function __calander_handler(elem, dispatcher) {

        if (!elem) (console.warn('Element Needed ~> MapHandler'), false);
        var elem = elem || document.querySelector('header'),
            date_header = document.querySelector('.explain');


        this.update_calender = function __update_Calender(date) {
            var date = date || new date(), options = options || {},
                months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                'September', 'October', 'November', 'December'],
                compiled_date = _.template('<%= month %> <%= day %>, <%= year %>', {
                    'month': months[date.getUTCMonth()],
                    'day': date.getUTCDate(),
                    'year': date.getUTCFullYear()
                });

                date_header.textContent = compiled_date;
                this.date_filter(date);
                return compiled_date;
        }.bind(this);


        this.date_filter = function __date_filter(date) {
            var selected_ms = date.getTime(),
                current_ms = new Date().getTime();

            var _filter = function _filter(data) {
                var data = JSON.parse(data.response),
                    list = []

                 _.filter(data, function(quake) {
                    var time = quake['properties']['time']
                    if (time > selected_ms && time < current_ms)
                        list.push(_.pick(quake, 'id'));
                });
                dispatcher.emitEvent('filterList', [list]);
            };
            dispatcher.emitEvent('getData', [_filter]);


        }.bind(this);

    };

    /**
     * UserGeolocation
     * Locates user based on geolocation data provided by the
     * client.
     * [dispatcher][obj] - Global event handler object
     */

    var UserGeolocation = function __user_geolocation(dispatcher) {
        var location = function  __location(pos) {
            var user_position = [pos.coords.latitude,
                pos.coords.longitude];
                dispatcher.emitEvent('markLocation', [user_position, {
                    icon: L.icon({iconUrl: 'static/images/mark.png'}),
                    move_to: true
                }]);
        }.bind(this);

        var not_found = function __geolocation_not_found(error) {
            var msg = _.template("Can not locate User Position -> <'%= error =>", {'error': error});
            console.error(msg);
        };

        (!!navigator.geolocation) ? navigator.geolocation.getCurrentPosition(location, not_found) :
            console.warn("Geolocation not supported");
    };

    /**
     * MapHandler
     * Locates user based on geolocation data provided by the
     * client.
     * [elem][str] - Map container element
     * [options][obj] - Map/Marker rendering options
     *     - [circle][bool] - Circle Marker
     *     - [selected][bool] - Selected Marker
     *     - [move_to][bool] - Pan to marker
     */

    var MapHandler = function __map_handler(elem, options) {

        if (!elem) (console.warn('Element Needed ~> MapHandler'), false);
        var elem = document.querySelector(elem) || document.querySelector('#map'),
            options = options || {}, defaultColor = "#616161", selectedColor = '#ff0000';

            this.__init__ = function __map_init(elem, map, self) {
                self.map = L.map('map', { center: [41.87811, -87.62980], zoom: 3});
            }(elem, map, this);

            this.render_marker = function __render_marker(pos, options) {
                var data = (!data) ? data : console.error("Must have location data for marker"),
                    options = options || {}, marker;

                    marker = (!options.circle) ? L.marker(pos, options) :
                        L.circleMarker(pos, {
                            radius: options.size,
                            fillColor: (!options.selected) ? defaultColor : selectedColor,
                            color: (!options.selected) ? defaultColor : selectedColor
                        });

                    if (options.move_to) this.map.panTo(pos, {animate: true})

                    return (!options.group) ? this.map.addLayer(marker) : marker;

            }.bind(this);

            this.render_markers = function __render_markers(data) {
                var data = JSON.parse(data.response),
                    markers = new L.FeatureGroup(),
                    quakes = [],
                    self = this;

                    markers.clearLayers();

                    _.reduce(data, function(result, quake, itr) {
                        var result = {
                            mag: quake['properties']['mag'],
                            position: L.latLng(quake['geometry']['coordinates'].reverse())
                        };
                        markers.addLayer(self.render_marker(result.position, {
                            circle: true,
                            group: true,
                            size: result.mag * 2
                        }));
                    });

                    this.map.addLayer(markers);
                    return markers;
            }.bind(this);

            this.handle_selected = function __handled_selected(pos, mag) {

                this.map.setView(L.latLng(pos), 5, {animate: true});
                this.render_marker(L.latLng(pos), {
                    circle: true,
                    selected: true,
                    size: mag * 2
                });

            }.bind(this);

            this.handle_nearest = function __handle_nearest(pos) {

            }.bind(this);

            this.filter_data = function __filter_data(date) {
                var selectedDate = new Date(date);

            }.bind(this);

            // add an OpenStreetMap tile layer
            L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(this.map);

            return {
                renderMarker: this.render_marker,
                renderMarkers: this.render_markers,
                handleSelected: this.handle_selected,
                handleNearest: this.handle_nearest
            }
    };

    /**
     * List Handler
     * Handled quake list manipulation on the
     * client.
     *
     */


    var ListHandler = function __list_handler(elem, options) {
        if (!elem) (console.warn('Element Needed ~> ListHandler'), false),
            options = options || {};

        this.filter_list = function __filter_list(list) {
            console.log(list);
        }.bind(this);
    };

    /**
     * Process Handler
     * @param {object} payload preloaded data from server
     */

    var StartProcess = function __main_handler() {

        // Function Aliases
        var map_view = new MapHandler('#map'),
            dispatcher = new EventEmitter(),
            locate_user = new UserGeolocation(dispatcher),
            data_view = new DataView(),
            calendar_view =  new CalenderView('header', dispatcher),
            list_view = new ListHandler('#quakes'),

            nearest_location = map_view.handle_nearest,
            mark_location = map_view.renderMarker,
            mark_locations = map_view.renderMarkers,
            handle_selected = map_view.handleSelected,
            calendar_update = calendar_view.update_calender,
            filter_list = list_view.filter_list,

            quake_data = data_view.get(mark_locations),
            get_data = data_view.get,
            post_data = data_view.post;

        // Event Aliases
        dispatcher.addListeners({
            getData: get_data,
            postData: post_data,
            updateCalender: calendar_update,
            markLocation: mark_location,
            markLocations: mark_locations,
            nearestLocation: nearest_location,
            handleSelected: handle_selected,
            filterList: filter_list
        });

        // DOM Aliases
        var date_selector = document.querySelector('#date'),
            quake_list = document.querySelectorAll('.quake');

        // Events
        date_selector.addEventListener('input', function(evt) {
            var capturedDate = new Date(this.value);

            dispatcher.emitEvent('updateCalender', [capturedDate]);
            evt.preventDefault();
        }, false);

        // KLUGE: Converts and reverse the string pulled from the DOM quake list
        var hlp_str_pos_converter = function __hlp_str_pos_converter(str) {
            return str.slice(1,-1).split(',').reverse();
        },
        hlp_pos_converter = function __hlp_pos_converter(formatted_arr) {
            var position = [];
            _.map(formatted_arr, function(pos) {
                position.push(parseFloat(pos));
            });
            return position;
        },
        hlp_get_position =  _.compose(hlp_pos_converter, hlp_str_pos_converter);

        _.map(quake_list, function(quake) {
            quake.addEventListener('mousedown', function(evt) {
                var position = (hlp_get_position(this.getAttribute('data-position'))),
                    mag = parseFloat(this.children[0].textContent);

                dispatcher.emitEvent('handleSelected', [position, mag]);
                evt.preventDefault();
            });
        });

    };

    return {
        StartProcess:StartProcess
    }


}(_, window, document, undefined));


// DEBUG OBJECTS
var earthquakes = new PSONA.StartProcess();










