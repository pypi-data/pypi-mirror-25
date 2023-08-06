/* global $, buildRQL, L, cw */

'use strict';

cw.cubes.datacat = new Namespace('cw.cubes.datacat');

$.extend(cw.cubes.datacat, {
    // Initialize dependent form select fields and bind update event on
    // change on the master select.
    initDependentFormField: function(masterSelectId,
                                     dependentSelectInfo) {
        var masterSelect = cw.jqNode(masterSelectId);
        // XXX no sure .change is the best event here...
        masterSelect.change(function(){
            cw.cubes.datacat.updateDependentFormField(this, dependentSelectInfo);
        });
    },

    // Update dependent form select fields.
    updateDependentFormField: function(masterSelect,
                                       dependentSelectInfo) {
        let dependentSelectId;
        let groupId;
        let octetStreamId;
        for (let etype in dependentSelectInfo) {
            dependentSelectId = dependentSelectInfo[etype];
            // Clear previously selected value.
            var dependentSelect = cw.jqNode(dependentSelectId);
            $(dependentSelect).val('');
            // Hide all optgroups.
            $(dependentSelect).find('optgroup').hide();
            // But the one corresponding to the master select.
            groupId = '#' + etype.toLowerCase() + '_mediatype_' + $(masterSelect).val().replace('/', '-');
            $(groupId).show();
            // Always show application/octet-stream choices.
            octetStreamId = '#' + etype.toLowerCase() + '_mediatype_application-octet-stream';
            $(octetStreamId).show();
        }
    }
});

var jsonLayer, map;

$.extend(cw.cubes.datacat, {
    /**
     * Overrides cubicweb-leaflet JS functions with better handling of GeoJSON data.
     **/

    defaultStyle: function(data) {
        /**
         * Returns the default style for drawing polygons.
         */
        return {
            fillColor: '#800026',
            weight: 1,
            opacity: 1,
            color: '#760022',
            dashArray: '3',
            fillOpacity: 0.7
        };
    },

    valueStyle: function(feature) {
        return {
            fillColor: feature.color,
            weight: 0.5,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7
        };
    },

    defaultPointStyle: {
        radius: 6,
        fillColor: '#ff7800',
        weight: 1,
        opacity: 1,
        color: 'black',
        fillOpacity: 0.7
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

    _getMinMaxDelta: function(fCollection) {
        /**
         * Given a ``FeatureCollection`` object, returns an object with the following properties:
         *
         * * ``min``. The minimum value in the collection,
         * * ``max``. The maximum value in the collection,
         * * ``delta``. value amplitude in the collection (``max - min``).
         *
         * A value in the collection is either the first property of a ``Feature`` if it's a
         * number, or the ``Feature`` id if not.
         *
         */
        // search min/max values
        var value = 0;
        if (typeof(fCollection.features[0].properties[0]) === 'number') {
            value = fCollection.features[0].properties[0];
        } else {
            value = fCollection.features[0].id;
        }
        var min = value;
        var max = value;
        $.each(fCollection.features, function(_, feature) {
            if (typeof(feature.properties[0]) === 'number') {
                value = feature.properties[0];
            } else {
                value = feature.id;
            }
            if (value < min) {min = value;}
            if (value > max) {max = value;}
        });
        return {min: min,
            max: max,
            delta: (max - min)};
    },

    _addColors: function(fCollection) {
        /**
         * Set the ``color`` property of each ``Feature`` in the given ``FeatureCollection``
         * object.
         */
        var stats = cw.cubes.datacat._getMinMaxDelta(fCollection);
        var value = 0;
        // add normalized fCollection
        $.each(fCollection.features, function(_, feature) {
            if (typeof(feature.properties[0]) === 'number') {
                value = feature.properties[0];
            } else {
                value = feature.id;
            }
            feature.color = cw.cubes.datacat._getColor((value - stats.min) / stats.delta);
        });
    },

    _addLegend: function(fCollection, settings) {
        /**
         * Add a legend on the Leaflet map.
         *
         * The legend if about the given ``FeatureCollection`` object.
         *
         * ``settings`` is an object with must have at least one property:
         * ``legend_position`` which indicate where to put the legend (eg. ``bottomright``)
         */
        var stats = cw.cubes.datacat._getMinMaxDelat(fCollection);
        var legend = L.control({position: settings.legend_position});
        legend.onAdd = function(map) {
            var div = L.DomUtil.create('div', 'info legend');
            var grades = [1.0, 0.9, 0.75, 0.6, 0.5, 0.4, 0.25, 0.1, 0.0];
            // loop through value intervals and generate a label with colored
            // square for each one
            for (var i = 0; i < grades.length - 1; i++) {
                div.innerHTML += (
                        '<i style="background:' + cw.cubes.datacat._getColor(grades[i]) + '"></i> ' +
                        (stats.min + (grades[i + 1] * stats.delta)) +
                        '&ndash;' +
                        (stats.min + (grades[i] * stats.delta)) +
                        '</br>');
            }
            return div;
        };
        legend.addTo(map);
    },

    _addInfo: function(settings) {
        /**
         * Add an info box on the Leaflet map.
         *
         * ``settings`` is an object with must have at least one property:
         * ``infoposition`` which indicate where to put the info box (eg. ``topright``)
         */
        var info = L.control({position: settings.info_position});
        info.onAdd = function(map) {
            this._divholder = L.DomUtil.create('div', 'info');
            this.update();
            return this._divholder;
        };
        info.update = function(properties) {
            if (properties) {
                this._divholder.innerHTML = properties;
            } else {
                this._divholder.innerHTML = "";
            }
        };
        info.addTo(map);
        return info;
    },

    _addDraw: function(settings) {
        /**
         * Add draw controls on the Leaflet map.
         *
         * ``settings`` is an object with must have at least one property:
         * ``infoposition`` which indicate where to put the info box (eg. ``topright``)
         */
        var drawGroup = new L.FeatureGroup();
        var addToDrawGroup = function (e) {
            /**
             * On the given drawing event, add new layer to drawing group.
             * Replaces the previous one.
             */
            drawGroup.clearLayers();
            drawGroup.addLayer(e.layer);
        };
        var submitDrawGroup = function (e) {
            /**
             * On the given drawing event, submit the drawing group to the enclosing form.
             */
            // XXX: use OGC URNs instead of EPSG (see http://geojson.org/geojson-spec.html#named-crs)
            var geoms = {
                "type": "GeometryCollection",
                "crs": {"type": "name", "properties": {"name": "EPSG:4326"}}
            };
            geoms.geometries = new Array(0);
            drawGroup.eachLayer(function (layer) {
                var geom = layer.toGeoJSON().geometry;
                geoms.geometries.push(geom);
            });
            $('input[name="' + settings.inputName + '"]').val(JSON.stringify(geoms));
            var form = $('#' + settings.divid).closest('form');
            buildRQL.apply(null, cw.evalJSON(form.attr('cubicweb:facetargs')));
        };
        map.addLayer(drawGroup);
        settings.editSettings.featureGroup = drawGroup;
        var draw = new L.Control.Draw({
            draw: settings.drawSettings,
            edit: settings.editSettings
        });
        draw.addTo(map);
        map.on('draw:created', addToDrawGroup);
        map.on('draw:created', submitDrawGroup);
        map.on('draw:edited', submitDrawGroup);
        map.on('draw:deleted', submitDrawGroup);
    },

    pointToLayer: function(feature, latlng) {
        return L.circleMarker(latlng, cw.cubes.datacat.defaultPointStyle);
    },

    plotMap: function(data, settings) {
        /**
         * Plot the given GeoJSON data on the map (geometries only).
         */
        if (!$.isEmptyObject(data)) {
            jsonLayer = L.geoJson(data, {
                style: cw.cubes.datacat.defaultStyle,
                pointToLayer: cw.cubes.datacat.pointToLayer
            }).addTo(map);
            map.fitBounds(L.featureGroup([jsonLayer]).getBounds());
        }
    },

    plotMapProperties: function(data, settings) {
        /**
         * Plot the given GeoJSON data on the map and optionally show a legend and an info box for
         * each feature.
         *
         * ``settings`` is an object with a boolean ``info_visibility`` (resp.
         * ``legend_visibility``) property saying whether the info box (resp. the legend) will be
         * shown on the map.
         */
        if (!$.isEmptyObject(data)) {
            cw.cubes.datacat._addColors(data);
            var onEachFeature;
            if (settings.info_visibility === true) {
                var info = cw.cubes.datacat._addInfo(settings);
                onEachFeature = function(feature, layer) {
                    layer.on({mouseover: function(e) {info.update(e.target.feature.properties.html_info);},
                        mouseout: function(e) {info.update();}});
                };
            } else {
                onEachFeature = function(feature, layer) {};
            }
            jsonLayer = L.geoJson(data, {
                style: cw.cubes.datacat.valueStyle,
                pointToLayer: cw.cubes.datacat.pointToLayer,
                onEachFeature: onEachFeature
            }).addTo(map);
            if (settings.legend_visibility === true) {
                cw.cubes.datacat._addLegend(data, settings);
            }
            map.fitBounds(L.featureGroup([jsonLayer]).getBounds());
        }
    },

    plotDrawableMap: function(data, settings) {
        /**
         * Plot the given GeoJSON data on the map and show drawing controls.
         *
         * `settings` should have two specific members for this two work,
         * `draw_settings` and `edit_settings`, whose properties are the same
         * as those allowed by the Leaflet Draw plugin
         * (see https://github.com/Leaflet/Leaflet.draw#advanced-options).
         */
        cw.cubes.datacat.plotMap(data);
        cw.cubes.datacat._addDraw(settings);
    }
});
