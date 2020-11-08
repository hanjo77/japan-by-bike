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

  select {
    position: fixed;
    left: 4rem;
    top: 2rem;
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

  .cell-edit {
    position: absolute;
    right: 1rem;
    top: 1rem;
    max-height: calc(100vh - 4rem);
    overflow-y: scroll;
  }

  .detail-toggle-button {
    position: fixed;
    right: 1rem;
    top: 1rem;
    padding: .5rem;
    margin: .5rem;
  }

  .map-overlay {
    background:rgba(255, 255, 255, 64);
  }

  .marker-icon .icon {
    max-height: 2rem;
  }

  .toggle-overlay {
    text-align: center;
    border: 0;
  }

  #overlayVisible {
    margin: 1.2rem .5rem 0 1.2rem;
  }

</style>