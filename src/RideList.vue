<template>
    <button class="detail-toggle-button" v-bind:title="toggleNavButtonHint" v-on:click="toggleNav()">{{ toggleNavButtonLabel }}</button>
    <div v-if="open">
        <fieldset class="toggle-overlay">
            <input type="checkbox" name="toggleOverlay" id="overlayVisible" v-model="overlayVisible" />
            <label for="overlayVisible">{{ getTranslation('show towns') }}</label>
        </fieldset>
        <ol id="ridelist">
            <li v-for="item in items" :key="item.filename">
                <a
                    v-on:click="openMap(item.filename, true)"
                    v-on:mousemove="openMap(item.filename, false)"
                    v-on:mouseout="openMap(null, false)">{{ translateTitle(item.title) }}</a>
            </li>
        </ol>
    </div>
</template>

<script>

    export default {
        name: 'RideList',
        components: {},
        props: {
            isMobile: Boolean
        },
        data() {
            return {
                open: false,
                items: [],
                toggleNavButtonHint: 'open details',
                toggleNavButtonLabel: 'open details',
                overlayVisible: false,
                translations: []
            };
        },
        mounted() {
            fetch('data/data.json').then((response) => {
                return response.json();
            }).then(data => {
                this.translations = data.translations;
                this.items = data.rides;
                this.toggleNavButtonHint = this.toggleNavButtonLabel = this.getTranslation('open details');
                this.toggleNavButtonHint = this.getTranslation(this.open ? 'close' : 'open details');
                this.toggleNavButtonLabel = this.getTranslation(this.open ? 'X' : 'open details');
            })
        },
        emits: ['open-kml', 'toggle-overlay'],
        watch: {
            overlayVisible: function(newVal) {
                this.$emit('toggle-overlay', newVal);
            }
        },
        methods: {
            openMap: function (filename, doZoom) {
                if (this.isMobile) {
                    doZoom = true;
                    this.open = false;
                    this.toggleNavButtonHint = this.toggleNavButtonLabel = this.getTranslation('open details');
                }
                this.$emit('open-kml', { filename: filename, doZoom: doZoom });
            },
            toggleNav: function () {
                this.open = !this.open;
                this.toggleNavButtonHint = this.getTranslation(this.open ? 'close' : 'open details');
                this.toggleNavButtonLabel = this.getTranslation(this.open ? 'X' : 'open details');
                if (!this.open) {
                    this.$emit('open-kml', null);
                }
            },
            translateTitle: function (title) {
                const places = title.split(' to ');
                return `${this.getTranslation(places[0])}から、${this.getTranslation(places[1])}まで。`;
            },
            getTranslation: function(key) {
                return this.translations.filter(elem => elem.key === key)[0]?.ja;
            },
        }
    }
</script>