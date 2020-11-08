<template>
    <select class="form-control" @change="changeLanguage($event)">
        <option value="" selected disabled>{{ getTranslation('language') }}</option>
        <option v-for="language in languages" :value="language.key" :key="language.key">{{ language.name }}</option>
    </select>
    <button class="detail-toggle-button" v-bind:title="toggleNavButtonHint" v-on:click="toggleNav()">{{ toggleNavButtonLabel }}</button>
    <div class="overlay-container" v-if="open">
        <fieldset class="toggle-overlay">
            <input type="checkbox" name="toggleOverlay" id="overlayVisible" v-model="overlayVisible" />
            <label for="overlayVisible">{{ getTranslation('show towns') }}</label>
        </fieldset>
        <ol id="ridelist" :class="`ridelist-${language}`">
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
                translations: [],
                language: 'en',
                languages: [{
                    key: 'ja',
                    name: '日本語'
                }, {
                    key: 'en',
                    name: 'English'
                }, {
                    key: 'de',
                    name: 'Deutsch'
                }, {
                    key: 'de-ch',
                    name: 'Schwiizerdütsch'
                }]
            };
        },
        mounted() {
            fetch('data/data.json').then((response) => {
                return response.json();
            }).then(data => {
                this.translations = data.translations;
                this.items = data.rides;
                this.toggleNavButtonHint = this.getTranslation(this.open ? 'close' : 'open details');
                this.toggleNavButtonLabel = this.getTranslation(this.open ? 'X' : 'open details');
            })
        },
        emits: ['open-kml', 'toggle-overlay', 'change-language'],
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
                const trackPatterns = {
                    'ja': '<<from>>から<<to>>まで。',
                    'en': 'From <<from>> to <<to>>',
                    'de': places[0].indexOf(' ko') > -1
                        ? 'Vom <<from>> nach <<to>>'
                        : places[1].indexOf(' ko') > -1
                            ? 'Von <<from>> zum <<to>>'
                            : 'Von <<from>> nach <<to>>',
                    'de-ch': places[0].indexOf(' ko') > -1
                        ? 'Vom <<from>> uf <<to>>'
                        : places[1].indexOf(' ko') > -1
                            ? 'Vo <<from>> zum <<to>>'
                            : 'Vo <<from>> uf <<to>>'
                }
                return trackPatterns[this.language]
                    .replace('<<from>>', this.getTranslation(places[0]))
                    .replace('<<to>>', this.getTranslation(places[1]));
            },
            getTranslation: function(key) {
                if (this.translations.filter(elem => elem.key === key)[0]) {
                  return this.translations.filter(elem => elem.key === key)[0][this.language];
                }
                return '...';
            },
            changeLanguage (event) {
                this.language = event.target.options[event.target.options.selectedIndex].value;
                this.toggleNavButtonHint = this.getTranslation(this.open ? 'close' : 'open details');
                this.toggleNavButtonLabel = this.getTranslation(this.open ? 'X' : 'open details');
                this.$emit('change-language', this.language);
            }
        }
    }
</script>