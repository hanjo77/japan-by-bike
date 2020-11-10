<template>
    <div class="lang-container">
        <a class="toggle-button lang-button" v-bind:title="toggleLangButtonHint" v-on:click="toggleLangSelect()">{{ toggleLangButtonLabel }}</a>
        <div class="overlay lang-selection" v-if="langOpen">
            <h2>{{ getTranslation('choose language') }}</h2>
            <ul>
                <li v-for="language in languages" :value="language.key" :key="language.key">
                    <a v-on:click="changeLanguage(language.key)">{{ language.name }}</a>
                </li>
            </ul>
        </div>
    </div>
    <a class="toggle-button detail-button" v-bind:title="toggleContentButtonHint" v-on:click="toggleContent()">{{ toggleContentButtonLabel }}</a>
    <div class="overlay overlay-container" v-if="contentOpen">
        <fieldset class="toggle-overlay">
            <input type="checkbox" name="toggleOverlay" id="overlayVisible" v-model="overlayVisible" />
            <label for="overlayVisible">{{ getTranslation('show towns') }}</label>
        </fieldset>
        <div class="overlay-content">
            <p>{{ texts.intro[language] }}</p>
            <p>{{ texts.followup[language]  }}</p>
            <ol id="ridelist" :class="`ridelist-${language}`">
                <li v-for="item in items" :key="item.filename" :class="completedClass(item)">
                    <a
                        v-on:click="openMap(item.filename, true)"
                        v-on:mousemove="openMap(item.filename, false)"
                        v-on:mouseout="openMap(null, false)">{{ translateTitle(item.title) }}</a>
                </li>
            </ol>
        </div>
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
                contentOpen: false,
                langOpen: false,
                items: [],
                toggleContentButtonHint: 'open details',
                toggleContentButtonLabel: 'open details',
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
                }],
                texts: {
                    intro: {
                        'ja': '2020、私はエアロバイク、Oculus Go、VZFit Explorerを購入して、Covidのためにブロックされた今年の意図された日本旅行を事実上実行しました。',
                        'en': '2020 I have bought a stationary bike, an Oculus Go and VZFit Explorer to virtually go on the intended Japan trip of this year that was blocked due to Covid.',
                        'de': '2020 habe ich ein stationäres Fahrrad, ein Oculus Go und einen VZFit Explorer gekauft, um die geplante aber aufgrund von Covid blockierte Reise nach Japan virtuell durchzuführen.',
                        'de-ch': '2020 hani mer es stationärs Velo, es Oculus Go u VZFit Explorer poschtet, für die planti aber wäge Covid verschobeni Reis nach Japan virtueu dürezfüehre.'
                    },
                    followup: {
                        'ja': 'この地図は、ルートと私の現在の進捗状況を示しています。',
                        'en': 'This map shows the route and my current progress.',
                        'de': 'Diese Karte zeigt die Route und meinen aktuellen Fortschritt.',
                        'de-ch': 'Uf dere Charte gseht me d\'Route u woni grad stecke.'

                    }
                }
            };
        },
        mounted() {
            fetch('data/data.json').then((response) => {
                return response.json();
            }).then(data => {
                this.translations = data.translations;
                this.items = data.rides;
                this.toggleContentButtonHint = this.getTranslation(this.contentOpen ? 'close' : 'open details');
                this.toggleContentButtonLabel = this.getTranslation(this.contentOpen ? 'X' : 'open details');
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
                    this.contentOpen = false;
                    this.toggleContentButtonHint = this.toggleContentButtonLabel = this.getTranslation('open details');
                }
                this.$emit('open-kml', { filename: filename, doZoom: doZoom });
            },
            toggleContent: function () {
                this.contentOpen = !this.contentOpen;
                this.toggleContentButtonHint = this.getTranslation(this.contentOpen ? 'close' : 'open details');
                this.toggleContentButtonLabel = this.getTranslation(this.contentOpen ? 'X' : 'open details');
                if (!this.contentOpen) {
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
            completedClass (ride) {
                const completed = parseFloat(ride.completed);
                return completed >= 100
                    ? 'ride-done'
                    : completed > 0
                        ? 'ride-in-progress'
                        : 'ride-open';
            },
            changeLanguage (language) {
                this.langOpen = false;
                this.language = language;
                this.toggleLangButtonHint = this.getTranslation(this.langOpen ? 'close' : 'choose language');
                this.toggleLangButtonLabel = this.getTranslation(this.langOpen ? 'X' : 'language');
                this.toggleContentButtonHint = this.getTranslation(this.contentOpen ? 'close' : 'open details');
                this.toggleContentButtonLabel = this.getTranslation(this.contentOpen ? 'X' : 'open details');
                this.$emit('change-language', this.language);
            }
        }
    }
</script>