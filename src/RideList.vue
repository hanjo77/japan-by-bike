<template>
    <div class="lang-container">
        <a class="toggle-button lang-button" v-bind:title="toggleLangButtonHint" v-on:click="toggleLangSelect()">{{ toggleLangButtonLabel }}</a>
        <div class="overlay lang-selection" v-if="langOpen">
            <h2>{{ getTranslation('choose language') }}</h2>
            <ul>
                <li v-for="lang in languages" :value="lang.key" :key="lang.key" :class="lang.key === language ? 'selected' : null">
                    <a v-on:click="changeLanguage(lang.key)">{{ lang.name }}</a>
                </li>
            </ul>
        </div>
    </div>
    <a class="toggle-button detail-button" v-bind:title="toggleContentButtonHint" v-on:click="toggleContent()">{{ toggleContentButtonLabel }}</a>
    <div class="overlay overlay-container" v-if="contentOpen">
        <fieldset class="toggle-overlay">
            <input type="checkbox" name="toggleOverlay" id="overlayVisible" v-model="overlayVisible" />
            <label for="overlayVisible">{{ getTranslation('show towns') }}</label>
            <a v-on:click="resetMap()" :title="getTranslation('reset map')">
                {{ getTranslation('reset map') }}
            </a>
        </fieldset>
        <div class="overlay-content">
            <p v-html="addLinks(texts.intro[language])"></p>
            <p v-html="addLinks(texts.followup[language])"></p>
            <table>
                <tr>
                    <th>{{ getTranslation('current location') }}</th>
                    <td>
                        <a v-on:click="openCurrentMarker()" :title="getTranslation('show on map')">
                            {{ locationName }}
                        </a>
                    </td>
                </tr>
                <tr>
                    <th>{{ getTranslation('total distance') }}</th>
                    <td>{{ totalDistance + texts.km[language]}}</td>
                </tr>
                <tr>
                    <th>{{ getTranslation('done distance') }}</th>
                    <td>{{ doneDistance + texts.km[language] + texts.percent[language].replace('VALUE', getPercentDone()) }}</td>
                </tr>
            </table>
            <ol id="ridelist" :class="`ridelist-${language}`">
                <li v-for="item in items" :key="item.filename" :class="completedClass(item)">
                    <a :title="getTranslation('show on map')"
                        v-on:click="openMap(item.filename, true)"
                        v-on:mouseenter="openMap(item.filename, false)"
                    >
                        {{ translateTitle(item.title) }}
                    </a>{{ texts.km_bracket[language].replace('VALUE', item.distance) }}
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
                totalDistance: 0,
                doneDistance: 0,
                toggleContentButtonHint: 'open details',
                toggleContentButtonLabel: 'open details',
                toggleLangButtonHint: 'choose language',
                toggleLangButtonLabel: 'language',
                overlayVisible: false,
                translations: [],
                language: this.getDefaultLanguage(),
                locationName: '',
                currentCoords: [],
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
                        'ja': '2020、私はエアロバイク、Oculus Quest、VZFit Explorerを購入して、COVIDのためにブロックされた今年の意図された日本旅行を事実上実行しました。',
                        'en': 'In 2020, I have bought a stationary bike, an Oculus Quest and VZFit Explorer to virtually go on my intended trip to Japan that was blocked by COVID.',
                        'de': '2020 habe ich ein stationäres Fahrrad, ein Oculus Quest und VZFit Explorer gekauft, um die geplante aber aufgrund von COVID blockierte Reise nach Japan virtuell durchzuführen.',
                        'de-ch': 'Im 2020 hani mer es stationärs Velo, es Oculus Quest u VZFit Explorer poschtet, für die planti aber wäge COVID verschobeni Reis nach Japan virtueu dürezfüehre.'
                    },
                    followup: {
                        'ja': 'この地図は、ルートと私の現在の進捗状況を示しています。',
                        'en': 'This map shows the route and my current progress.',
                        'de': 'Diese Karte zeigt die Route und meinen aktuellen Fortschritt.',
                        'de-ch': 'Uf dere Charte gseht me d\'Route u woni grad stecke.'
                    },
                    km: {
                        'ja': 'キロ',
                        'en': ' km',
                        'de': ' km',
                        'de-ch': ' km'
                    },
                    km_bracket: {
                        'ja': '（VALUEキロ）',
                        'en': ' (VALUE km)',
                        'de': ' (VALUE km)',
                        'de-ch': ' (VALUE km)'
                    },
                    percent: {
                        'ja': '（VALUE％）',
                        'en': ' (VALUE %)',
                        'de': ' (VALUE %)',
                        'de-ch': ' (VALUE %)'
                    }
                },
                links: {
                    'Oculus Quest': 'https://www.oculus.com/quest/',
                    'VZFit Explorer': 'https://www.virzoom.com/'
                }
            };
        },
        mounted() {
            fetch('data/data.json').then((response) => {
                return response.json();
            }).then(data => {
                this.translations = data.translations;
                this.items = data.rides;
                this.getCurrentCoords();
                this.changeLanguage(this.language);
                this.totalDistance = this.getTotalDistance();
                this.doneDistance = this.getDoneDistance();
                this.toggleContentButtonHint = this.getTranslation(this.contentOpen ? 'close' : 'open details');
                this.toggleContentButtonLabel = this.getTranslation(this.contentOpen ? 'X' : 'open details');
                this.toggleLangButtonHint = this.getTranslation(this.langOpen ? 'close' : 'choose language');
                this.toggleLangButtonLabel = this.getTranslation(this.langOpen ? 'X' : 'language');
            })
        },
        emits: ['open-kml', 'open-location', 'toggle-overlay', 'change-language'],
        watch: {
            overlayVisible: function(newVal) {
                this.$emit('toggle-overlay', newVal);
            }
        },
        methods: {
            addLinks: function (text) {
                Object.keys(this.links).forEach(key => text = text.replace(
                    key,
                    `<a href="${this.links[key]}" target="_blank" title="${this.getTranslation('new window')}">${key}</a>`
                ));
                return text;
            },
            getDefaultLanguage: function () {
                let lang = window.navigator.language.toLowerCase();
                const langs = ['ja', 'en', 'de', 'de-ch'];
                if (langs.indexOf(lang) > -1) {
                    return lang;
                } else if (langs.indexOf(lang.split('-')[0]) > -1) {
                    return lang.split('-')[0];
                }
                return 'en';
            },
            resetMap: function () {
                this.$emit('open-kml', null);
            },
            openMap: function (filename, doZoom) {
                if (!doZoom) {
                    this.resetMap();
                }
                if (this.isMobile) {
                    doZoom = true;
                    this.contentOpen = false;
                    this.toggleContentButtonHint = this.toggleContentButtonLabel = this.getTranslation('open details');
                }
                this.$emit('open-kml', { filename: filename, doZoom: doZoom });
            },
            openCurrentMarker: function () {
                if (this.isMobile) {
                    this.contentOpen = false;
                    this.toggleContentButtonHint = this.toggleContentButtonLabel = this.getTranslation('open details');
                }
                this.$emit('open-location', { location: this.currentCoords });
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
            getTotalDistance () {
                let distance = 0;
                this.items?.forEach(item => distance += parseInt(item.distance, 10));
                return distance;
            },
            getDoneDistance () {
                let distance = 0;
                this.items?.forEach(item => distance += ((item.distance * item.completed) / 100));
                return Math.round(distance);
            },
            getPercentDone () {
                return Math.round((this.doneDistance * 100) / this.totalDistance);
            },
            getCurrentCoords () {
                let lastCompleted = undefined;
                this.items.forEach(item => {
                    const completed = parseInt(item.completed, 10);
                    if (completed > 0) {
                        lastCompleted = item;
                    }
                });
                if (lastCompleted) {
                    const completed = parseInt(lastCompleted.completed, 10);
                    fetch('data/' + lastCompleted.filename)
                        .then(response => response.text())
                        .then(kmlData => {
                            const coordData = new DOMParser()
                                .parseFromString(kmlData, "text/xml")
                                .querySelector('coordinates')?.innerHTML
                                .split(new RegExp('[,\\s]', 'g'))
                                .filter(elem => !!elem)
                                .map(elem => parseFloat(elem));

                            const coords = [];

                            for (let i = 0; i < coordData?.length; i += 3) {
                                coords.push([coordData[i], coordData[i + 1]]);
                            }

                            if (completed < 100) {
                                const completedIndex = Math.floor(completed * coords.length / 100);
                                
                                if (coords[completedIndex]) {
                                    this.currentCoords = coords[completedIndex];
                                    this.getLocationName();
                                }
                            } else {
                                this.currentCoords = coords[coords.length - 1];
                                this.getLocationName();
                            }
                        });
                }
            },
            getLocationName () {
                if (this.language && this.currentCoords.length === 2) {
                    fetch('https://nominatim.openstreetmap.org/reverse?format=json'
                        + '&accept-language=' + this.language.split('-')[0]
                        + '&lon=' + this.currentCoords[0]
                        + '&lat=' + this.currentCoords[1]
                    )
                        .then((response) => response.json())
                        .then(function(json) {
                            this.locationName = json.display_name;
                        }.bind(this));
                }
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
                this.getLocationName();
                this.toggleLangButtonHint = this.getTranslation(this.langOpen ? 'close' : 'choose language');
                this.toggleLangButtonLabel = this.getTranslation(this.langOpen ? 'X' : 'language');
                this.toggleContentButtonHint = this.getTranslation(this.contentOpen ? 'close' : 'open details');
                this.toggleContentButtonLabel = this.getTranslation(this.contentOpen ? 'X' : 'open details');
                this.$emit('change-language', this.language);
            }
        }
    }
</script>