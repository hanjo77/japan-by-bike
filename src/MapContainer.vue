<template>
  <div ref="map-root"
       style="width: 100vw; height: 100vh">
  </div>
</template>

<script>
  import View from 'ol/View';
  import Map from 'ol/Map';
  import { Vector as VectorSource } from 'ol/source';
  import { Tile as TileLayer, Vector as VectorLayer } from 'ol/layer';
  import { LineString } from 'ol/geom';
  import { Feature } from 'ol';
  import * as olExtent from 'ol/extent';
  import Stamen from 'ol/source/Stamen';
  import Overlay from 'ol/Overlay';
  import { transform as projTransform, fromLonLat } from 'ol/proj';
  import { Style, Stroke as StrokeStyle } from 'ol/style';

  // importing the OpenLayers stylesheet is required for having
  // good looking buttons!
  import 'ol/ol.css';

  export default {
    name: 'MapContainer',
    components: {},
    props: {
      isMobile: Boolean,
      resetView: Boolean,
      kmlUrl: String,
      overlayVisible: Boolean,
      doZoom: Boolean,
      languageCode: String,
      location: Array
    },
    methods: {
      toggleOverlay: function(value) {
        document.querySelectorAll('.marker-icon').forEach(elem => {
          elem.style.display = value ? 'block' : 'none';
        });
      },
      getLocationLabel: function(key, language) {
        if (this.translations.filter(elem => elem.key === key)[0]) {
          return this.translations.filter(elem => elem.key === key)[0][language];
        }
        return 'UNDEFINED';
      },
      centerView: function() {
        if (this.map) {
          this.map.getView().setZoom(5);
          this.map.getView().setCenter(projTransform([139.692101, 38.689634], 'EPSG:4326', 'EPSG:3857'));
        }
      },
      getMarker: function(latlon, title, type) {
        if (!this.markers[title] && latlon) {
          this.markers[title] = popup;

          var pos = fromLonLat(latlon);

          const content = document.createElement('div');
          const markerIcon = '<img class="icon" src="img/marker.png" />';
          const overlay = `<h4 class="title">${title}</h4>`;
          content.className = 'marker-icon';
          content.innerHTML = type === 'current' ? markerIcon : overlay;
          // content.onmouseup = function(overlay, markerIcon, content) {
          //   content.innerHTML = content.innerHTML.indexOf('marker.png') > -1 ? overlay : markerIcon;
          // }.bind(this, overlay, markerIcon, content);

          // Popup showing the position the user clicked
          var popup = new Overlay({
            position: pos,
            positioning: 'center-center',
            stopEvent: false,
            element: content
          });

          return popup;
        }
        return null;
      },
      updateMarkers: function() {
        this.map.getOverlays().clear();
        this.rideData.rides.forEach(ride => {
          const fromTo = ride.title.split(' to ');
          const coords = this.coords[ride.filename];
          const completed = parseFloat(ride.completed);

          if (coords) {
            const completedIndex = 0 < completed < 100
                ? Math.floor(completed * coords.length / 100)
                : coords.length;
            if (fromTo[1]) {
              this.markers[fromTo[0]] = this.map.addOverlay(this.getMarker(coords[0], this.getLocationLabel(fromTo[0], this.languageCode)));
              this.markers[fromTo[1]] = this.map.addOverlay(this.getMarker(coords[coords.length - 1], this.getLocationLabel(fromTo[1], this.languageCode)));
            }
            if (completed < 100 && !this.markers['ハンヨ']) {
              this.markers['ハンヨ'] = this.map.addOverlay(this.getMarker(
                completed === 0 ? coords[0] : coords[completedIndex],
                'ハンヨ',
                'current'
              ));
            }
          }
        });
        this.toggleOverlay(this.overlayVisible);
      },
      drawKmlData: function(ride, temp, setZoom) {
        if (ride) {
          fetch('data/' + ride.filename).then(response => {
            return response.text();
          }).then(kmlData => {

            const completed = parseFloat(ride.completed);

            const visitedStyle = new Style({
                  stroke: new StrokeStyle({
                    width: 5,
                    color: (temp ? "#00ff00" : "#009900")
                  }),
                });

            const newStyle = new Style({
                  stroke: new StrokeStyle({
                    width: 5,
                    color: (temp ? "#ff0000" : "#990000")
                  }),
                });

            const coordData = new DOMParser()
              .parseFromString(kmlData, "text/xml")
              .querySelector('coordinates')?.innerHTML
              .split(new RegExp('[,\\s]', 'g'))
              .filter(elem => !!elem)
              .map(elem => parseFloat(elem));

            const coords = [];
            const layers = [];

            for (let i = 0; i < coordData?.length; i += 3) {
              coords.push([coordData[i], coordData[i + 1]]);
            }

            this.coords[ride.filename] = coords;

            const completedIndex = 0 < completed < 100
              ? Math.floor(completed * coords.length / 100)
              : coords.length;

            (0 < completed < 100
              ? [{
                  coords: coords.slice(0, completedIndex),
                  style: visitedStyle
                }, {
                  coords: coords.slice(completedIndex, coords.length),
                  style: newStyle
              }]
              : [{
                  coords: coords,
                  style: (completed > 0 ? visitedStyle : newStyle)
              }]).forEach(layerData => {
              const coords = layerData.coords.map(coord => projTransform(coord, 'EPSG:4326', 'EPSG:3857'));

              const featureLine = new Feature({
                  geometry: new LineString(coords)
              });

              const vectorSource = new VectorSource();

              vectorSource.addFeature(featureLine)

              vectorSource.once('change', () => {
                if (vectorSource.getState() === 'ready') {
                    var extent = vectorSource.getExtent();
                    this.map.getView().fit(extent);
                }
              });

              layers.push(new VectorLayer({
                source: vectorSource,
                style: layerData.style
              }));
            });

            if (temp) {
              layers.forEach(layer => this.kmlLayers.push(layer));
              if (setZoom) {
                var myExtent = layers[0].getSource().getExtent();
                layers.forEach(function(layer) {
                  olExtent.extend(myExtent, layer.getSource().getExtent());
                });
                this.map.getView().fit(myExtent);
              }
            } else {
              this.updateMarkers();
            }
            layers.forEach(layer => this.map.addLayer(layer));
            this.toggleOverlay(this.overlayVisible);
          });            
        } else {
          // this.centerView();
        }
      }
    },
    watch: {
      location: function(newVal) {
        if (newVal) {
          this.map.getView().setZoom(13);
          this.map.getView().setCenter(projTransform([newVal[0], newVal[1]], 'EPSG:4326', 'EPSG:3857'));
        }
      },
      overlayVisible: function(newVal) {
        this.toggleOverlay(newVal);
      },
      kmlUrl: function(newVal) {
        this.kmlLayers.forEach(layer => this.map.removeLayer(layer));
        this.centerView();
        if (newVal && newVal !== 'void') {
          this.drawKmlData(this.rideData.rides.filter(elem => newVal.indexOf(elem.filename) > -1)[0], true, this.doZoom);
        }
      },
      doZoom: function(newVal) {
        this.kmlLayers.forEach(layer => this.map.removeLayer(layer));
        this.drawKmlData(this.rideData.rides.filter(elem => this.kmlUrl.indexOf(elem.filename) > -1)[0], true, newVal);
      },
      languageCode: function() {
        this.updateMarkers();
      }
    },
    data() {
      return {
        markerStarted: false,
        rideData: {},
        map: {},
        kmlLayers: [],
        markers: {},
        translations: [],
        overlay: {},
        coords: {}
      };
    },
    mounted() {
      fetch('data/data.json').then(response => {
          return response.json();
      }).then(data => {
        this.translations = data.translations;
        this.rideData = data;
        this.map = new Map({
          // the map will be created using the 'map-root' ref
          target: this.$refs['map-root'],
          layers: [
              'watercolor',
              'terrain-labels'
            ].map(layerName => new TileLayer({
              source: new Stamen({
                layer: layerName
              })
            })
          ),
          view: new View({
            zoom: 5,
            center: projTransform([139.692101, 38.689634], 'EPSG:4326', 'EPSG:3857'),
            constrainResolution: true
          })
        });
        this.currentPosReached = false;
        this.rideData.rides.forEach(ride => this.drawKmlData(ride));
      })
    }

  }
</script>