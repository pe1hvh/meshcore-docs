# CHANGELOG

All notable changes to meshcore-docs are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added

- **Direct Messages** (`nl/techniek/direct-messages.md`,
  `en/technical/direct-messages.md`): nieuw techniekhoofdstuk dat de vier fasen
  van een DM beschrijft — eerste bericht als gescoopte flood, PATH-antwoord,
  geleerd pad, bevestiging — en de vraag beantwoordt waarom een direct
  gerouteerde DM geen transport code draagt. Die vraag werd tot nu toe alleen in
  één tabelregel van `regions-and-scopes.md` aangestipt, zonder onderbouwing.
  Het hoofdstuk benoemt ook de keerzijde: de padontdekking eromheen is wél
  gescoped, waardoor een regiofout DM's naar nieuwe contacten breekt.
- Beide hoofdstukken opgenomen in `nl/README.md` en `en/README.md` onder
  *Techniek* / *Technical*, direct na *Regio's: bedoeling en praktijk*.
- Drie diagrammen in `images/nl/` en `images/en/`:
  `direct-messages-1.svg` (de vier fasen), `direct-messages-2.svg` (hetzelfde
  pakket in beide routetypes, byte voor byte) en `direct-messages-3.svg` (de
  beslisboom van een repeater, die laat zien dat de regiotak alleen aan de
  floodkant hangt).
- `tools/dm-example.py`: reproduceert het DM-voorbeeld uit het nieuwe
  hoofdstuk — klaartekst, cijfertekst, transport code, beide framelengtes en de
  ACK — met dezelfde voorbeelddata als `tools/example-calculation.py`.
- Zeven termen toegevoegd aan `nl/naslag/terminology.md` en
  `en/reference/terminology.md`: *Dest hash / Src hash*, *Direct routing*,
  *Encrypt-then-MAC*, *First packet wins*, *out_path*, *PATH-pakket* en
  *Zero-hop*.
- **MeshCore Platforms** (`nl/techniek/platforms.md`,
  `en/technical/platforms.md`): nieuw techniekhoofdstuk over de vier
  platformfamilies waar MeshCore op bouwt — ESP32, nRF52840, RP2040 en
  STM32WL. Het beantwoordt de vraag waarom niet elke node hetzelfde kan:
  dezelfde firmware, maar per familie andere transporten, opslag, displays,
  updatemethoden en flashartefacten. De docs beschreven tot nu toe wel
  apparaten (`gebruik/hardware.md`), maar nergens de chip erachter.
- Het hoofdstuk gebruikt bewust de term *platform* en niet *microcontroller*.
  De firmware zelf spreekt van platforms (`ESP32_PLATFORM`, `NRF52_PLATFORM`,
  `RP2040_PLATFORM`, `STM32_PLATFORM`, `platformio.ini` r.63, 90, 104, 113),
  en drie van de vier chips zijn een SoC en geen kale microcontroller.
- Beide hoofdstukken opgenomen in `nl/README.md` en `en/README.md` onder
  *Techniek* / *Technical*, direct na *SenseCap DFU*.
- Drie diagrammen in `images/nl/` en `images/en/`: `platforms-1.svg` (de vier
  families naast elkaar, met per familie wat er wel en niet is),
  `platforms-2.svg` (losse SX1262 over SPI tegenover de SubGHz-radio op de
  STM32WL-die) en `platforms-3.svg` (beslisboom voor de platformkeuze).
- `tools/platform-overview.py`: genereert de drie tellingstabellen uit een
  kloon van `meshcore-dev/MeshCore` en een opgeslagen pagina van de web
  flasher, zodat het hoofdstuk narekenbaar blijft bij een volgende release.
  Het script controleert ook de aannames in de tekst, zoals dat
  `framework = arduino` precies één keer in de repo staat.
- Vijfentwintig termen toegevoegd aan `nl/naslag/terminology.md` en
  `en/reference/terminology.md`: *Arduino-core*, *bootloader*, *build flag*,
  *Cortex-M0+/M4/M4F*, *ESP-IDF*, *ESP-NOW*, *HAL*, *LittleFS*, *LPCOMP*,
  *Platform*, *Platformfamilie*, *PlatformIO environment*, *PSRAM*, *RISC-V*,
  *RP2040*, *SoC*, *SoftDevice*, *SPIFFS*, *ST-Link*, *STM32WLE5*,
  *SubGHz-radio*, *SYSTEMOFF*, *UF2*, *Variant* en *Xtensa*.
- Vier externe datasheets toegevoegd aan `nl/naslag/references.md` en
  `en/reference/references.md`: RP2040, ESP32-serie, nRF52840 en STM32WLE5.
  De RP2040-cijfers in het hoofdstuk komen daar vandaan en niet uit de
  firmware-repo; dat staat ook zo in een voetnoot bij de tabel.
- **De vier platformfamilies** (`nl/platform/platform-families.md`,
  `en/platform/platform-families.md`): nieuw hoofdstuk in de rubriek
  `platform/`, met de vier
  familiebeschrijvingen — ESP32, nRF52840, RP2040 en STM32WL — die tot nu toe
  in `platforms.md` stonden. Reden voor de splitsing: dat bestand diende twee
  verschillende leesdoelen. Wie *vergelijkt en kiest* heeft andere tekst nodig
  dan wie zich *per familie verdiept*, en die twee stonden door elkaar heen.
  Een opsplitsing per processor is overwogen en afgevallen: slechts 29 % van
  de tekst is aan één familie toe te wijzen, dus vier pagina's zouden
  grotendeels uit boilerplate bestaan en het bron-blok van twee naar tien
  plekken gaan. Het resultaat is twee volwaardige hoofdstukken van circa 1900
  en 1050 woorden, geen stubs.
- Beide taalversies opgenomen in `nl/README.md` en `en/README.md` onder een
  nieuw kopje *Platform*, tussen *Techniek* / *Technical* en *Naslag* /
  *Reference*. De twee hoofdstukken stonden eerst in de Techniek-lijst; nu de
  rubriek `platform/` bestaat, volgt de inhoudsopgave de mapstructuur.
  `README.md` en `CLAUDE.md` noemen `platform/` ook in hun
  structuuroverzicht — daar ontbrak de map nog.
- Vier kruisverwijzingen tussen de twee hoofdstukken: van *MeshCore Platforms*
  naar *De vier platformfamilies* onderaan de inleiding en aan het eind van
  *De vier families in één oogopslag*, en terug vanuit de inleiding en de
  STM32WL-sectie van het nieuwe hoofdstuk.

### Changed

- `nl/techniek/regions-and-scopes.md`, `en/technical/regions-and-scopes.md`: de
  tabelregel over directe routes verwijst nu door naar het nieuwe hoofdstuk voor
  de onderbouwing.
- `nl/gebruik/communication.md`, `en/usage/communication.md`: de sectie *Direct
  Messages* verwijst onderaan naar het techniekhoofdstuk. Het gebruikersverhaal
  blijft hier staan.
- `nl/techniek/key-encryption.md`, `en/technical/key-encryption.md`: de sectie
  *Routing en bevestiging* verwijst door naar het nieuwe hoofdstuk voor padleren
  en routering. ECDH blijft hier, zodat er geen tweede beschrijving ontstaat.
- `nl/gebruik/hardware.md`, `en/usage/hardware.md`: een NOTE-blok boven de
  vergelijkingstabel scheidt de twee onderwerpen. Deze pagina blijft over
  apparaten gaan; de chip erin en wat die bepaalt staat vanaf nu in
  *MeshCore Platforms*.
- `nl/naslag/terminology.md`, `en/reference/terminology.md`: de regel *DFU*
  beschreef alleen de Bluetooth-variant. DFU is breder — op STM32 gaat het via
  USB — en de regel is daarop verruimd.
- `CLAUDE.md`: de conventies zijn gelijkgetrokken met de repo. Slugs zijn
  Engels en zonder rubrieksprefix (het document schreef nog Nederlandse slugs
  voor), diagrammen staan per taal in `images/nl/` en `images/en/` onder
  dezelfde naam (het document beschreef een gedeelde map met `-en.svg`-
  varianten), en de bestandsnamen `terminology.md` en `references.md` zijn
  gecorrigeerd. Toegevoegd: commits pinnen in bronlinks in plaats van `main`,
  externe cijfers markeren, en de regel dat de repo wint als dit document de
  repo tegenspreekt.
- **MeshCore Platforms** is verplaatst van `nl/techniek/platforms.md` en
  `en/technical/platforms.md` naar `nl/platform/platforms.md` en
  `en/platform/platforms.md`. De twee platformhoofdstukken staan daarmee in
  hun eigen rubriek `platform/`, die in beide taalbomen dezelfde naam draagt.
  De slug `platforms` is ongewijzigd. Links vanuit `nl/README.md`,
  `en/README.md`, `nl/gebruik/hardware.md` en `en/usage/hardware.md` wijzen
  mee.
- `nl/platform/platforms.md`, `en/platform/platforms.md`: ingekort tot het
  vergelijkende deel. De vier familiesecties zijn woord voor woord verhuisd
  naar `platform-families.md`; wat blijft staan is *waarom het platform
  uitmaakt*, de vier families in één oogopslag, de vergelijking op zes assen,
  de rollentabel, de flasherlijst, hoe de firmware de verschillen opvangt en
  de keuzehulp. De subtitel is `*VERGELIJKEN · KIEZEN · WAT DE CHIP BEPAALT*`
  geworden, de inleiding belooft niet langer wat nu op de andere pagina staat.
  De voetnoot bij de RP2040-cijfers en de NOTE over de ontbrekende
  mA-getallen blijven hier, bij de tabellen waar ze bij horen.
- `images/nl/platforms-2.svg` en `images/en/platforms-2.svg` zijn hernoemd
  naar `platform-families-1.svg`. Het diagram hoort bij het nieuwe hoofdstuk,
  en de conventie is `images/<taal>/<slug>-<n>.svg`. De inhoud van de
  SVG-bestanden is niet gewijzigd, alleen de naam en de verwijzing.
- `nl/gebruik/hardware.md`, `en/usage/hardware.md`: het NOTE-blok boven de
  vergelijkingstabel verwijst nu naar beide hoofdstukken — naar *MeshCore
  Platforms* voor wat de chip bepaalt, en naar *De vier platformfamilies*
  voor wat er per familie in zit.
- Geen enkel cijfer is bij deze wijziging veranderd. Dit is een herindeling
  van bestaande, al geverifieerde tekst, geen herverificatie: de firmware-repo
  is niet opnieuw opgehaald en `tools/platform-overview.py` niet opnieuw
  gedraaid. Beide hoofdstukken pinnen dezelfde commit `03b6ef4` (28 juli 2026,
  v1.16.0) en vermelden dat de tellingen ook op `a3a1aa5` identiek zijn.
- `CLAUDE.md`: bestandsnamen zijn nu expliciet altijd Engels, kebab-case, ook
  in de Nederlandse boom en ook voor scripts en diagrammen. Dat stond er nog
  niet: de regel gold alleen voor hoofdstukslugs, en bij `tools/` stond zelfs
  het tegendeel — die naamconventie schreef Nederlands voor. De drie
  bestaande scripts en twee verweesde SVG's met een `techniek-`-prefix
  voldoen nog niet en staan als valkuil genoteerd; hernoemen raakt links in
  `README.md`, `CHANGELOG.md` en vier hoofdstukken en is een aparte opdracht.
  De regel gaat expliciet over bestanden, niet over mappen: mapnamen volgen
  de rubrieksmapping, die is aangevuld met `platform` ↔ `platform`.
- De drie scripts in `tools/` zijn hernoemd naar Engelse namen:
  `bereken-voorbeeld.py` → `example-calculation.py`, `dm-voorbeeld.py` →
  `dm-example.py` en `platform-overzicht.py` → `platform-overview.py`. De
  code zelf is niet gewijzigd; alleen twee zelfverwijzingen in commentaar en
  in de usage-regel zijn meegetrokken. Meeverhuisd zijn de verwijzingen in
  `README.md`, `CLAUDE.md`, `nl/techniek/direct-messages.md`,
  `en/technical/direct-messages.md`, de vier platformhoofdstukken en het
  bijschrift in `images/nl/direct-messages-2.svg` en
  `images/en/direct-messages-2.svg`, waar de scriptnaam in het diagram staat.

### Fixed

- `nl/gebruik/communication.md`, `en/usage/communication.md`: de waarschuwing
  *"Adverts worden NIET doorgestuurd door repeaters. Beide nodes moeten elkaar
  direct kunnen horen voor de key-uitwisseling"* was onjuist. Repeaters sturen
  flood-adverts wél door, tot de aparte hoplimiet `flood.max.advert` en met
  verlaagde prioriteit; alleen een *zero-hop* advert blijft bij de buren. De
  oude tekst stuurde lezers naar een verkeerd beeld van hoe contacten elkaar
  vinden.
- `nl/techniek/key-encryption.md`, `en/technical/key-encryption.md`: de ACK werd
  beschreven als *"een 4-byte SHA256-hash"*. Voor een gewone DM is de
  ACK-payload 6 bytes: 4 hash-bytes, 1 byte pogingnummer en 1 willekeurige byte,
  waarvan alleen de eerste 4 worden vergeleken.
- `nl/techniek/regions-and-scopes.md`, `en/technical/regions-and-scopes.md`,
  `nl/naslag/terminology.md`, `en/reference/terminology.md`: dode links naar
  `techniek-locode.md`, een bestand dat niet in de repo staat. De verwijzingen
  wijzen nu naar `regions-in-practice.md`, waar de naamgevingsafspraken staan.

---

## [2026-07-27] Removed
- Deleted unlinked files

## [2026-07-27] Major changes

### Added

- **Privacy & Beveiliging** (`nl/gebruik/privacy.md`, `en/usage/privacy.md`):
  eigen hoofdstuk, afgesplitst uit `regulations.md`. Behandelt wat er altijd
  zichtbaar is (beacons voor routing), wat in ISM-modus nooit zichtbaar is, en de
  vergelijkingstabel HAM- versus ISM-modus.
- **Praktische Toepassingen** (`nl/gebruik/applications.md`,
  `en/usage/applications.md`): eigen hoofdstuk, afgesplitst uit
  `what-is-meshcore.md`. Vier scenario's: familie-mesh, Morse-club, Amateur Radio
  Mesh en Remote Station.
- Beide hoofdstukken opgenomen in `nl/README.md` en `en/README.md` onder
  *Gebruik* / *Usage*, direct na *Communicatie* / *Communication*.
- **Regelgeving & Duty Cycle** (`nl/gebruik/regulations.md`, `en/usage/regulations.md`):
  nieuwe sectie *Duty cycle in een mesh — wat er anders is dan bij een solo-node*.
  Behandelt dat de duty cycle per zendend apparaat geldt en niet per netwerk, dat
  doorgegeven verkeer meetelt in het eigen uurbudget van de repeater, en dat één
  flood-bericht één transmissie kost bij élke repeater die het hoort. Met een
  time-on-air-budgettabel (SF7 / BW 62,5 kHz / CR 4/5) en een tabel gedragsregels
  die de mesh ontlasten.
- Waarschuwing dat de MeshCore firmware-default `set dutycycle` op **50 %** staat
  (en de verouderde `set af` op `1.0`, eveneens ~50 %), ruim boven zowel H4 (10 %)
  als H5 (0,1 %). Een vers geflashte repeater is niet conform tot `set dutycycle 10`
  is gezet. Gecontroleerd tegen `docs.meshcore.io/cli_commands` (firmware v1.15.0).
- Toelichting waarom de LBT+AFA-uitweg voor MeshCore in Nederland niet beschikbaar
  is: AFA vereist frequentie-agility, terwijl MeshCore op één vaste draaggolf draait.

### Changed

- **Beeldmateriaal per taal gescheiden** (`images/nl/`, `images/en/`): `images/`
  was één gedeelde map, waardoor de Engelse hoofdstukken op 19 van de 25 plekken
  een diagram met Nederlandse tekst toonden. Beide talen hebben nu een eigen map
  met identieke bestandsnamen, zodat beeld dezelfde spiegelregel volgt als de
  hoofdstukken: alleen de mapnaam verschilt. Alle 50 verwijzingen in `nl/` en
  `en/` zijn meeverhuisd; er is niets verwijderd.
- Het achtervoegsel `-en` is vervallen. De vijf `techniek-packets-1..5-en.svg`
  zijn via `git mv` in `images/en/` terechtgekomen en heten daar inmiddels
  `packet-structure-1..5.svg`. Dat achtervoegsel was een eenmalige oplossing voor
  één hoofdstukreeks en week af van de afspraak dat bestandsnamen in beide talen
  identiek zijn.
- **Bestandsnamen naar het Engels.** Hoofdstuk- en beeldbestanden droegen
  Nederlandse of half-Nederlandse namen (`dode-zone.md`, `techniek-packets-1.svg`)
  terwijl de Engelse mappen al `usage/`, `technical/` en `reference/` heetten. 22
  van de 30 slugs zijn hernoemd, 8 waren al Engels of neutraal. Het voorvoegsel
  `techniek-` is vervallen: het herhaalde de mapnaam. De 25 diagrammen volgen hun
  hoofdstuk, dus `techniek-packets-1.svg` → `packet-structure-1.svg`,
  `dode-zone-1.svg` → `dead-zone-1.svg`, `techniek-lagen-1.svg` →
  `layer-model-1.svg`. Alles via `git mv`, beide talen in dezelfde stap, omdat
  `DocsGenerator` een slug alleen oplevert als hij in `nl/` én `en/` bestaat.
- De onderliggende afspraak is nu expliciet: **wat gedeeld is tussen de talen staat
  in het Engels, wat bij één taal hoort staat in die taal.** Bestandsnamen zijn
  gedeeld en dus Engels; mapnamen horen bij één taal en blijven daarom `gebruik/`
  naast `usage/`.
- **Diagrammen in `images/en/` vertaald.** De vertaalronde is uitgevoerd: alle
  diagrammen met Nederlandse tekst staan nu in het Engels. 176 tekstnodes
  aangepast, goed voor 731 Nederlandse woorden. De overige tekstnodes in die
  bestanden waren al Engels — code-identifiers, registernamen, hexbytes, cijfers —
  en zijn ongemoeid gelaten. `node-types-1.svg` is taalneutraal en de vijf
  `packet-structure`-diagrammen waren al vertaald; die zes zijn niet aangeraakt.
- Uitsluitend de tekstinhoud binnen `<text>`-elementen is gewijzigd. Per bestand is
  geverifieerd dat attributen, coördinaten, CSS-variabelen, opmaak en bytevolgorde
  identiek zijn gebleven.
- Het voorbeeldbericht *"Op Woensdag a.s. Blauwvingerdagen"* in
  `packet-structure-5.svg` blijft onvertaald. Dat is de payload van het
  voorbeeldpakket, geen interface-tekst; in de Engelse documentpagina staat die
  regel ook onvertaald.
- README: structuurblok toont de nieuwe indeling, en de telling *50 diagrammen* is
  gecorrigeerd naar *25 diagrammen per taal*. De oude telling rekende 20 ongebruikte
  PNG-bestanden mee.
- Van die 20 PNG's zijn er 10 opnieuw gegenereerd uit de vertaalde SVG's, op exact
  hetzelfde formaat: `18-ble-architecture-1`, `20-channel-structure-psk-1..4`,
  `23-repeater-flow-1..2` en `24-dead-zone-1..3`. De render-parameters zijn
  gereconstrueerd door de Nederlandse SVG terug te renderen en met het origineel te
  vergelijken; bij de `20-*`-reeks is die reproductie pixelexact. De twee
  `23-repeater-flow`-PNG's bleken niet op viewBox-formaat gerenderd maar op 2770 px
  breed met 25 px witmarge, bij `-2` met de onderste witruimte weggeknipt.
- De pagina-indeling van de website wordt weer gevolgd: `privacy` en
  `applications` waren tijdens de HTML→markdown-migratie samengevoegd met
  `regulations` respectievelijk `what-is-meshcore`. Die samenvoeging is
  teruggedraaid; beide zijn nu weer losse hoofdstukken, net als op domca.nl.
  De tekst is ongewijzigd verplaatst — inclusief de eerder aangebrachte
  correcties op de encryptieregel en de vermogensrij.
- Koppen in de afgesplitste hoofdstukken van `####` terug naar `##`, en de
  paginatitel weer als H1 met de subtitelregel eronder, conform de overige
  hoofdstukken.
- Configuratieblok bijgewerkt van **SF8 naar SF7** en aangevuld met coding rate,
  conform de huidige Nederlandse netwerkparameters (BW 62,5 kHz / SF7 / CR 4/5).
- Vermogensrij in de ISM/HAM-tabel gecorrigeerd van `25 mW ERP (EU)` naar
  `500 mW e.r.p. (H4) of 25 mW e.r.p. (H5)`; de oude waarde sprak de H4-conclusie
  van de pagina tegen.
- Opmerking bij de Ebyte E22-900M30S aangevuld: terugregelen gebeurt via de PA-trap,
  omdat `set tx` (1–22 dBm) alleen de LoRa-chip aanstuurt.

### Fixed

- **Feitelijke fout:** de relatie tussen spreading factor en time-on-air stond
  omgekeerd ("lagere spreading factors waar pakketten langer in de lucht zijn").
  Een hógere SF geeft langere time-on-air. Beide taalversies.
- Conversie-artefacten uit de oorspronkelijke HTML→markdown-migratie hersteld:
  de duty-cycle-kaarten zijn nu een tabel, en het configuratieblok en de
  dBi/dBd-formules staan niet langer op één regel geplakt.
- **Telling van de te vertalen diagrammen gecorrigeerd van 18 naar 19.**
  `text-to-chirp-5.svg` (voorheen `techniek-chirp-5.svg`) stond eerder als
  taalneutraal aangemerkt, maar bevat de zesregelige samenvatting van de
  chirp-keten in het Nederlands (*Tekst → ASCII → Bits*, *Chirp doorloopt alle
  treden, wrappend bij de top*, enzovoort). Alleen `node-types-1.svg` is werkelijk
  taalneutraal: dat bevat vier rolbenamingen plus emoji. Het diagram is alsnog
  meegenomen in de vertaalronde.
- De opgave *357 tekstnodes* hoorde bij die 18 bestanden; met de twaalf nodes van
  `text-to-chirp-5.svg` erbij zijn het er 369. Daarvan bevatten er 176 Nederlandse
  tekst. De schatting *~1140 woorden* telde alle tekstnodes mee; het aantal
  daadwerkelijk vertaalde Nederlandse woorden is 731.
- **Dubbele beeldnamen in `images/en/` opgeruimd.** De map telde 47 SVG-bestanden
  voor 25 unieke diagrammen: 22 byte-identieke paren onder twee naamgevingsschema's,
  omdat de hernoeming naar Engelse slugs als kopie was uitgevoerd in plaats van als
  verplaatsing. Er is geen diagram verloren gegaan — de oude namen waren geen tweede
  afbeelding maar een onafgemaakte `git mv`. Het Engelse schema blijft; dat is wat
  de 50 verwijzingen in `nl/` en `en/` daadwerkelijk aanroepen. Beide mappen bevatten
  nu 25 SVG-bestanden met identieke namen.
- Interne link `../techniek/techniek-locode.md` in `terminology.md` verwijst naar een
  hoofdstuk dat niet bestaat, in beide taalversies. Nog niet hersteld; zie *Open punten*.

### Removed

- Sectie *De exacte specificaties* / *The exact specifications*. Elk datapunt
  daaruit stond al in de H-regeltabel erboven, in de openingszin van dezelfde
  sectie, of in *Wat is een duty cycle?*. Er gaat geen informatie verloren.

### Fixed (EN-versie)

- Ontbrekende sectiescheiding vóór *Which regime applies to your node?* hersteld,
  zodat de EN-versie dezelfde structuur heeft als de NL-versie.
- Dubbele vertaalvoetnoot verwijderd en de resterende Nederlandstalige `[!NOTE]`
  over de verwijderde rekenhulp vertaald.
- Dubbele vertaalvoetnoot in `en/usage/what-is-meshcore.md` verwijderd; die was bij
  het samenvoegen van `applications` blijven staan.

### Open punten

- **De 20 PNG-bestanden volgen het nieuwe naamschema niet.** Ze dragen nog het
  genummerde schema van vóór de mappenindeling (`18-ble-architecture-1`,
  `24-dead-zone-1`). Dat schema is wel Engels — het is zelfs de bron waaruit de
  huidige slugs zijn afgeleid — maar het nummerdeel verwijst naar een
  hoofdstukvolgorde die niet meer bestaat. Zolang geen enkel hoofdstuk ze aanroept
  is dat onschadelijk.
- Tien van de 20 PNG-bestanden bevatten nog Nederlandse tekst en hebben geen
  SVG-bron in de map: `05-group-communication-1` en `-2` (onderling byte-identiek),
  `08-practical-applications-1`, `12-text-to-chirp-1..4`, `14-lora-modulation-1`,
  `15-layer-model-1` en `16-remote-control-1`. Ze zijn in een andere huisstijl
  gemaakt dan de SVG-set en kunnen niet vertaald worden zonder ze na te bouwen.
  De inhoud overlapt grotendeels met de SVG-diagrammen die wél gebruikt worden.
  Er moet nog besloten worden wat ermee gebeurt; de git-historie bewaart ze hoe dan ook.
- Nog te beantwoorden: waarom zijn tien ongebruikte PNG's opnieuw gegenereerd?
  Als ze nergens worden aangeroepen, kost het onderhoud zonder dat een lezer ze ziet.
  Als ze elders wél gebruikt worden — buiten deze repo — dan klopt de aanmerking
  *ongebruikt* niet en hoort dat hier vastgelegd te worden.
- In `16-remote-control-1.png` ontbreken lettertekens: `[Phone]`, `[Radio]`,
  `[Rot]`, `[Rel]` en `[Rig]` staan als letterlijke placeholders in beeld en
  diverse emoji en vinkjes renderen als lege blokjes. Bestaand renderprobleem, geen
  vertaalkwestie.
- `terminology.md` linkt in beide talen naar `techniek-locode.md`, een hoofdstuk dat
  niet bestaat. Ofwel het hoofdstuk schrijven, ofwel de link weghalen.

### Voor beheerders van domca.nl

- **`DocsGenerator` is aangepast en meegeleverd.** Hij maakte één
  `MarkdownConverter` met een vaste `$imageDir` (`docsRoot/images`), buiten de
  taallus, en wist dus niet in welke taal hij bezig was. Er is nu één converter per
  taal, met `$this->docsRoot . '/images/' . $config['dir']`; `self::LANGUAGES`
  bevatte de mapnamen `nl` en `en` al. Het verzamelen van waarschuwingen loopt over
  alle converters.
- Toegevoegd: `controleerBeeldmappen()`, aangeroepen aan het begin van `run()`. Die
  meldt bestanden die wel in `images/nl` staan en niet in `images/en` of andersom.
  Hoofdstukken hadden die bescherming al; beeld niet, terwijl daar na de splitsing
  hetzelfde kan misgaan. Zichtbaar bij `--dry-run`, dus vóór het live gaat.
- **`MarkdownConverter` is nog niet nagekeken.** Herschrijft die alleen paden, dan is
  er niets te doen. Kopieert hij de bestanden naar de webroot, dan botsen
  `images/nl/layer-model-1.svg` en `images/en/layer-model-1.svg` op dezelfde
  doelnaam en moet ook de doelmap per taal gescheiden worden.
- **Oude fragmenten blijven op de webroot staan.** De generator kent geen opruimstap,
  dus na de hernoeming staan `content/<oude-slug>.html` en `.en.html` er nog. Dat is
  gunstig: `navigateTo()` haalt fragmenten rechtstreeks op, buiten het menu om, dus
  gedeelde links als `#dode-zone` blijven werken. Wel bevriezen ze op de inhoud van
  vóór de hernoeming. Weghalen kan, maar dan tonen die links *"Deze pagina is nog in
  ontwikkeling"*.
- Routing verloopt via `window.location.hash`, dus de slug staat achter een `#` en
  wordt nooit naar de server gestuurd. De hernoeming kost daarom geen zoekposities.
- `'live-intro'` in `HANDMATIGE_GROEPEN` valt buiten de hernoeming en buiten de
  menumarkers in `index.html`. Ongewijzigd, maar het blijft handwerk.
- **Losstaand probleem: de diagrammen volgen de themaschakelaar niet.** `router.js`
  zet het thema als `body.light` via `localStorage`, terwijl alle 30 SVG's
  `@media (prefers-color-scheme: dark)` gebruiken. Die twee zijn niet gekoppeld: de
  pagina volgt de 🌙☀️-knop, de diagrammen volgen de OS-instelling. Een lezer met een
  donker besturingssysteem krijgt donkere diagrammen op een lichte pagina. Raakt de
  vertaling niet, maar wel elk diagram.
