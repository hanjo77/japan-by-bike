<template>
    <div class="lang-container">
        <button class="toggle-button lang-button" v-bind:title="toggleLangButtonHint" v-on:click="toggleLangSelect()">{{ toggleLangButtonLabel }}</button>
        <div class="overlay lang-selection" v-if="langOpen">
            <h2>{{ getTranslation('choose language') }}</h2>
            <ul>
                <li v-for="language in languages" :value="language.key" :key="language.key">
                    <a v-on:click="changeLanguage(language.key)">{{ language.name }}</a>
                </li>
            </ul>
        </div>
    </div>
    <button class="toggle-button detail-button" v-bind:title="toggleNavButtonHint" v-on:click="toggleNav()">{{ toggleNavButtonLabel }}</button>
    <div class="overlay overlay-container" v-if="navOpen">
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
                navOpen: false,
                langOpen: false,
                items: [],
                toggleNavButtonHint: 'open details',
                toggleNavButtonLabel: 'open details',
                toggleLangButtonHint: 'choose language',
                toggleLangButtonLabel: 'language',
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
                    name: 'Bärndütsch'
                }]
            };
        },
        mounted() {
            fetch('data/data.json').then((response) => {
                return response.json();
            }).then(data => {
                this.translations = data.translations;
                this.items = data.rides;
                this.toggleNavButtonHint = this.getTranslation(this.navOpen ? 'close' : 'open details');
                this.toggleNavButtonLabel = this.getTranslation(this.navOpen ? 'X' : 'open details');
                this.toggleLangButtonHint = this.getTranslation(this.langOpen ? 'close' : 'choose language');
                this.toggleLangButtonLabel = this.getTranslation(this.langOpen ? 'X' : 'language');
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
                this.navOpen = !this.navOpen;
                this.toggleNavButtonHint = this.getTranslation(this.navOpen ? 'close' : 'open details');
                this.toggleNavButtonLabel = this.getTranslation(this.navOpen ? 'X' : 'open details');
                if (!this.navOpen) {
                    this.$emit('open-kml', null);
                }
            },
            toggleLangSelect: function () {
                this.langOpen = !this.langOpen;
                this.toggleLangButtonHint = this.getTranslation(this.langOpen ? 'close' : 'choose language');
                this.toggleLangButtonLabel = this.getTranslation(this.langOpen ? 'X' : 'language');
            },
            translateTitle: function (title) {
                const places = title.split(' to ');
                const trackPatterns = {
                    'ja': '<<from>>から、<<to>>まで。',
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
            changeLanguage (language) {
                this.langOpen = false;
                this.language = language;
                this.toggleLangButtonHint = this.getTranslation(this.langOpen ? 'close' : 'choose language');
                this.toggleLangButtonLabel = this.getTranslation(this.langOpen ? 'X' : 'language');
                this.toggleNavButtonHint = this.getTranslation(this.navOpen ? 'close' : 'open details');
                this.toggleNavButtonLabel = this.getTranslation(this.navOpen ? 'X' : 'open details');
                this.$emit('change-language', this.language);
            }
        }
    }
</script>