$.format = function(str, sub) { // found on stackoverflow, use http://archive.plugins.jquery.com/node/14683/release ? or http://code.google.com/p/jquery-utils/wiki/StringFormat#Formatting
    return str.replace(/\{(.+?)\}/g, function($0, $1) {
        return $1 in sub ? sub[$1] : $0;
    });
};

var geojson, map;


cw.cubes.leaflet = new Namespace('cw.cubes.leaflet');

$.extend(cw.cubes.leaflet, {
    /**
     * @param datasource either a list or leaflet markers or an url deferencing json markers
     * @param settings leaflet settings
     **/
    renderLeafLetMap: function(datasource, settings) {
        function _renderMarkers(markers, settings) {
            L.Icon.Default.imagePath = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/' + L.version + '/images';
            // center on first marker if no center is specified
            if (markers.length > 0) {
                var center = settings.center || [markers[0].latitude, markers[0].longitude];
            } else {
                var center = [0, 0];
            }
            var map = L.map(settings.divid, settings.map_options).setView(center, settings.initialZoom);
            var osm = new L.TileLayer(settings.provider.url, {
                minZoom: settings.minZoom,
                maxZoom: settings.maxZoom,
                attribution: settings.provider.attribution});
            map.addLayer(osm);
            if (settings.cluster) {
                var cluster = new L.MarkerClusterGroup();
            }
            var bounds = new L.LatLngBounds();
            $.each(markers, function(_, marker) {
                var options = {};
                if (marker.icon) {
                    cw.log('[leaflet-0.4.2] icon property is deprecated in marker definition, use icon_options instead');
                    options.icon = L.icon({iconUrl: marker.icon});
                } else if (marker.icon_options && marker.icon_options.iconUrl) {
                    options.icon = L.icon(marker.icon_options);
                }
                var mapMarker = L.marker([marker.latitude, marker.longitude],
                                         options, marker).bindPopup($.format(marker.popup, marker));
                if (!settings.initialZoom) {
                    bounds.extend(mapMarker.getLatLng());
                }
                if (settings.cluster) {
                    cluster.addLayer(mapMarker);
                } else {
                    mapMarker.addTo(map);
                }
            });
            if (!settings.initialZoom) {
                map.fitBounds(bounds);
            }
            if (settings.cluster) {
                map.addLayer(cluster);
            }
        }

        if ($.isArray(datasource)) {
            _renderMarkers(datasource, settings);
        } else {
            $.getJSON(datasource, function(markers) {
                _renderMarkers(markers, settings);
            });
        }
    },

    initMap: function(settings) {
        map = L.map(settings.divid, settings.map_options);
        L.tileLayer(settings.provider.url, {
            attribution: settings.provider.attribution,
            maxZoom: settings.maxZoom,
            minZoom: settings.minZoom,
            initialZoom: settings.initialZoom
        }).addTo(map);
    },


    defaultPolygoneStyle: function(data) {
        return {
            fillColor: '#800026',
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7
        };
    },


    defaultLineStyle: function(data) {
        return {
            weight: 2,
            color: 'red'
        };
    },

    valuePolyStyle: function(feature) {
        return {
            fillColor: feature.color,
            weight: 0.5,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7
        };
    },

    _getColor: function(val) {
        return val > 0.9 ? '#800026' :
            val > 0.75 ? '#BD0026' :
            val > 0.6  ? '#E31A1C' :
            val > 0.5  ? '#FC4E2A' :
            val > 0.4  ? '#FD8D3C' :
            val > 0.25  ? '#FEB24C' :
            val > 0.1  ? '#FED976' :
            '#FFEDA0';
    },

    /* Compute min/max/delta */
    _getBounds: function(data) {
        // search min/max values
        var value = 0;
        if (typeof(data.features[0].properties[0]) === 'number'){
            value = data.features[0].properties[0];
        }else{
            value = data.features[0].id;
        }
        var min = value;
        var max = value;
        $.each(data.features, function(_, feature) {
            if (typeof(feature.properties[0]) === 'number'){
                value = feature.properties[0];
            }else{
                value = feature.id;
            }
            if (value < min){min = value;};
            if (value > max){max = value;};
        });
        return {min: min,
                max: max,
                delta: (max - min)};
    },

    // Normalize the first property element of data
    _addColors: function(data){
        var bounds = cw.cubes.leaflet._getBounds(data);
        var value = 0;
        // add normalized data
        $.each(data.features, function(_, feature) {
            if (typeof(feature.properties[0]) === 'number'){
                value = feature.properties[0];
            }else{
                value = feature.id;
            }
            feature.color = cw.cubes.leaflet._getColor((value - bounds.min) / bounds.delta);
        });
    },


    _addLegend: function(data, settings){
        var bounds = cw.cubes.leaflet._getBounds(data);
        var legend = L.control({position: settings.legend_position});
        legend.onAdd = function(map) {
            var div = L.DomUtil.create('div', 'info legend');
            var grades = [1.0, 0.9, 0.75, 0.6, 0.5, 0.4, 0.25, 0.1, 0.0];
            // loop through value intervals and generate a label with colored
            // square for each one
            for (var i = 0; i < grades.length - 1; i++){
                div.innerHTML += (
                    '<i style="background:' + cw.cubes.leaflet._getColor(grades[i]) + '"></i> ' +
                        (bounds.min + (grades[i + 1] * bounds.delta)) +
                        '&ndash;' +
                        (bounds.min + (grades[i] * bounds.delta)) +
                    '</br>');
            }
            return div
        };
        legend.addTo(map);
    },

    _addInfo: function(settings){
        var info = L.control({position: settings.info_position});
        info.onAdd = function(map){
            this._divholder = L.DomUtil.create('div', 'info');
            this.update();
            return this._divholder
        };
        info.update = function(properties){
            if (properties){
                this._divholder.innerHTML = properties;
            }else{
                this._divholder.innerHTML = "";
            }
        };
        info.addTo(map);
        return info;
    },

    plotMap: function(data, settings) {
        geojson = L.geoJson(data).addTo(map);
        if (data[0].type == 'LineString')
        {geojson.setStyle(cw.cubes.leaflet.defaultLineStyle);}
        else{
            geojson.setStyle(cw.cubes.leaflet.defaultPolygoneStyle);}
        map.fitBounds(L.featureGroup([geojson]).getBounds());
    },

    plotMapValues: function(data, settings) {
        cw.cubes.leaflet._addColors(data);
        if (settings.info_visibility === true){
            var info = cw.cubes.leaflet._addInfo(settings);
            var onEachFeature = function(feature, layer){
                var infoContent = 'No information';
                if (typeof e.target.feature.properties === 'string') {
                    infoContent = e.target.feature.properties;
                }
                else if (e.target.feature.properties && e.target.feature.properties.htmlInfo) {
                    infoContent = e.target.feature.properties.htmlInfo;
                }
                layer.on({mouseover: function(e){info.update(infoContent);},
                          mouseout: function(e){info.update();}})
            };
        }else{
            var onEachFeature = function(feature, layer){};
        }

        geojson = L.geoJson(data, {style: cw.cubes.leaflet.valuePolyStyle,
                                   onEachFeature:onEachFeature}).addTo(map);
        if (settings.legend_visibility === true){
            cw.cubes.leaflet._addLegend(data, settings);
        }
        map.fitBounds(L.featureGroup([geojson]).getBounds());
    }

});
