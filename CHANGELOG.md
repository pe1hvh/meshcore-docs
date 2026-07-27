# CHANGELOG

All notable changes to meshcore-docs are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added

- **Privacy & Beveiliging** (`nl/gebruik/privacy.md`, `en/usage/privacy.md`):
  eigen hoofdstuk, afgesplitst uit `regelgeving.md`. Behandelt wat er altijd
  zichtbaar is (beacons voor routing), wat in ISM-modus nooit zichtbaar is, en de
  vergelijkingstabel HAM- versus ISM-modus.
- **Praktische Toepassingen** (`nl/gebruik/toepassingen.md`,
  `en/usage/toepassingen.md`): eigen hoofdstuk, afgesplitst uit
  `wat-is-meshcore.md`. Vier scenario's: familie-mesh, Morse-club, Amateur Radio
  Mesh en Remote Station.
- Beide hoofdstukken opgenomen in `nl/README.md` en `en/README.md` onder
  *Gebruik* / *Usage*, direct na *Communicatie* / *Communication*.
- **Regelgeving & Duty Cycle** (`nl/gebruik/regelgeving.md`, `en/usage/regelgeving.md`):
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

- De pagina-indeling van de website wordt weer gevolgd: `privacy` en
  `toepassingen` waren tijdens de HTML→markdown-migratie samengevoegd met
  `regelgeving` respectievelijk `wat-is-meshcore`. Die samenvoeging is
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

### Removed

- Sectie *De exacte specificaties* / *The exact specifications*. Elk datapunt
  daaruit stond al in de H-regeltabel erboven, in de openingszin van dezelfde
  sectie, of in *Wat is een duty cycle?*. Er gaat geen informatie verloren.

### Fixed (EN-versie)

- Ontbrekende sectiescheiding vóór *Which regime applies to your node?* hersteld,
  zodat de EN-versie dezelfde structuur heeft als de NL-versie.
- Dubbele vertaalvoetnoot verwijderd en de resterende Nederlandstalige `[!NOTE]`
  over de verwijderde rekenhulp vertaald.
- Dubbele vertaalvoetnoot in `en/usage/wat-is-meshcore.md` verwijderd; die was bij
  het samenvoegen van `toepassingen` blijven staan.
