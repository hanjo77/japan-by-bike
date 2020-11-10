<template>
  <div class="cell cell-map">
    <MapContainer :languageCode="languageCode" :kmlUrl="kmlUrl" :overlayVisible="overlayVisible" :doZoom="doZoom" :isMobile="isMobile()"></MapContainer>
  </div>
  <div class="cell cell-edit">
    <RideList @open-kml="openKml($event)" @toggle-overlay="toggleOverlay($event)" @change-language="changeLanguage($event)" :isMobile="isMobile()"></RideList>
  </div>
</template>

<script>
  import MapContainer from './MapContainer';
  import RideList from './RideList';

  export default {
    name: 'App',
    components: {
      MapContainer,
      RideList
    },
    data() {
      return {
        kmlUrl: '/data/japan-by-bike.kml',
        overlayVisible: false,
        viewWidth: window.innerWidth,
        doZoom: true,
        languageCode: 'en'
      }
    },
    methods: {
      isMobile: function() {
        return (this.viewWidth < 700);
      },
      onResize: function() {
                this.viewWidth = window.innerWidth;
      },
      openKml(event) {
        if (event?.doZoom !== undefined) {
          this.doZoom = event.doZoom;
        }
        this.kmlUrl = `/data/${event?.filename}`;
      },
      toggleOverlay(visible) {
        this.overlayVisible = visible;
      },
      changeLanguage(language) {
        this.languageCode = language;
      }
    },
    mounted() {
      window.addEventListener('resize', this.onResize)
    },
    beforeUnmount() {
      window.removeEventListener('resize', this.onResize)
    }
  }
</script>

<style>
  html, body {
    height: 100%;
    margin: 0;
    padding: 0;
  }

  ol {
    margin: 1rem;
  }

  ol.ridelist-ja {
    margin-left: 2rem;
    list-style: cjk-ideographic;
  }

  @media only screen and (max-width: 600px) {
    select {
      left: .5rem;
      top: 5.5rem;
    }
  }

  option {
    padding: 1rem;
  }

  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    height: 100%;
    display: block;
    padding: 0;
    margin: 0;
    box-sizing: border-box;
  }

  .cell {
    border-radius: 4px;
    background-color: lightgrey;
  }

  .cell-map {
    width: 100vw;
    height: 100vh;
    position: fixed;
  }

  .overlay {
    position: fixed;
    background: #ccc;
    z-index: 3;
    border: 1px solid black;
    box-shadow: 0 0 1rem black;
  }

  .overlay-container {
    top: .5rem;
    right: .5rem;
    margin-left: .5rem;
    max-height: calc(100vh - 1rem);
  }

  .overlay-container p {
    margin: 2rem;
  }

  @media only screen and (min-width: 800px) {
    .overlay-container p {
      max-width: 50vw;
    }
  }

  .overlay-content {
    max-height: calc(100vh - 5rem);
    overflow-y: scroll;
  }

  .lang-selection {
    bottom: .5rem;
    left: .5rem;
    margin: 0;
    padding: .5rem;
    z-index: 0;
  }

  .lang-selection h2 {
    font-size: 1.5rem;
    padding: 0;
    margin: 0;
  }

  .lang-selection ul {
    list-style-type: none;
    margin-bottom: 0;
  }

  li a {
    display: block;
  }

  li a:hover {
    text-shadow: 0 0 .2rem #999;
  }

  li.ride-done a:hover {
    text-shadow: 0 0 .2rem #9f9;
  }

  li.ride-in-progress a:hover {
    text-shadow: 0 0 .2rem #ff9;
  }

  li.ride-open a:hover {
    text-shadow: 0 0 .2rem #f99;
  }

  .toggle-button {
    position: fixed;
    padding: .5rem;
    margin: .5rem;
    display: block;
    color: black;
    background: #ccc;
    border: 1px solid black;
    padding: .2rem .5rem;
  }

  .toggle-button:hover {
    color: #ccc;
    background: black;
  }

  .lang-button {
    left: .5rem;
    bottom: .5rem;
    z-index: 2;
  }

  .detail-button {
    right: .5rem;
    top: .5rem;
    z-index: 4;
  }

  .map-overlay {
    background:rgba(255, 255, 255, 64);
  }

  .marker-icon .icon {
    max-height: 2rem;
  }

  .marker-icon .title {
    text-shadow: 1px 1px white, -1px -1px white, 0 0 0.2em white;
  }

  .toggle-overlay {
    border: 0;
  }

  #overlayVisible {
    margin: 1.2rem .5rem 0 1.2rem;
  }

</style>