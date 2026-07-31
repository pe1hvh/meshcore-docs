# DOMCA — MeshCore documentatie

**Dutch Open MeshCore Activity** · Off-grid mesh-communicatie via LoRa
Tweetalige documentatie: van je eerste node tot de bits op de radio.

[![Licentie: CC BY-SA 4.0](https://img.shields.io/badge/licentie-CC%20BY--SA%204.0-blue.svg)](LICENSE)
[![Talen](https://img.shields.io/badge/talen-NL%20%7C%20EN-informational.svg)](#)
[![Website](https://img.shields.io/badge/web-domca.nl-brightgreen.svg)](https://domca.nl)

### 📖 [Lees in het Nederlands →](nl/README.md)  ·  🇬🇧 [Read in English →](en/README.md)

---

## Nederlands

MeshCore laat goedkope LoRa-radiootjes een eigen netwerk vormen. Berichten
hoppen van node naar node tot ze aankomen — zonder internet, zonder zendmast,
zonder abonnement. **DOMCA** is een initiatief om die kennis toegankelijk te
maken voor de Nederlandse community.

Deze repository bevat de volledige documentatie: 70 hoofdstukken in het
Nederlands, dezelfde 70 in het Engels, met 52 diagrammen per taal. De
hoofdstuktelling is het aantal `.md`-bestanden per taalboom zonder de
`README.md`-indexen; de diagramtelling is het aantal SVG's waarnaar een
hoofdstuk verwijst, niet het aantal bestanden in `images/`.




### Beginnen/Leeswijzer

De hoofdstukken lopen sterk uiteen in benodigde voorkennis. Deze tabel zegt
per sectie welke voorkennis handig is, zodat je weet welk detailniveau je kunt
verwachten.

| Sectie | Wat je er vindt | Benodigde voorkennis |
|---|---|---|
| [Gebruik](nl/gebruik/) | Wat MeshCore is, een node aan de praat krijgen, hardware, regelgeving, privacy | Geen. Geen programmeerkennis vereist |
| [Techniek](nl/techniek/) | Protocol, pakketopbouw byte voor byte, encryptie, routing, repeaters, room server | Basisbegrip van netwerken en hexadecimale notatie helpt; programmeren niet nodig |
| [Platform](nl/platform/) | De vier platformfamilies en de keuze ertussen | Geen, afgezien van globale kennis van microcontrollers |
| [Hardware](nl/hardware/) | Radio, antenne, linkbudget, BLE, WiFi, USB, I²C, SPI, scherm, GPS, knoppen | Basiskennis elektronica aanbevolen; enkele hoofdstukken tonen C++ fragmenten |
| [Libraries](nl/libraries/) | De tweeënvijftig externe libraries die de firmware in gaan | Kennis van PlatformIO-buildconfiguraties aanbevolen |
| [Ontwerp → logisch](nl/ontwerp/logisch/) | Rollen, componenten, contracten, informatiemodel, variabiliteit, ontwerpbeslissingen | Basiskennis van klassen en interfaces aanbevolen; de tekst blijft weg bij broncode |
| [Ontwerp → technisch](nl/ontwerp/technisch/) | Broncodestructuur, klassenmodel, platform- en radiorealisatie, buildsysteem, macro's, traceerbaarheid | C++ klassen, overerving en PlatformIO-buildconfiguraties |
| [Naslag](nl/naslag/) | Terminologie, referenties, links | Geen. Bedoeld om in op te zoeken, niet om door te lezen |
| [Project](nl/project/) | Over DOMCA, opzet van de repository | Geen |

Kom je een term tegen die je niet kent, dan staat hij in
[Terminologie](nl/naslag/terminology.md).

Het volledige overzicht staat in **[nl/README.md](nl/README.md)**.

### Wat dit anders maakt

De gebruikershoofdstukken doen wat je verwacht. De techniekhoofdstukken gaan
een stap verder, en dat is bewust:

- **Byte voor byte.** Pakketten worden uitgeschreven met echte waarden, niet met
  `XX XX`. Je ziet waar de header ophoudt en de payload begint.
- **Geverifieerd tegen de broncode.** Technische claims vermelden de
  firmwareversie en commit waartegen ze zijn gecontroleerd, met verwijzing naar
  het betreffende bestand in `meshcore-dev/MeshCore`.
- **Narekenbaar.** De voorbeelden in [Regio's en Scopes](nl/techniek/regions-and-scopes.md)
  zijn met [`tools/example-calculation.py`](tools/example-calculation.py) te
  reproduceren. Klopt de tekst niet, dan zie je dat zelf.
- **Ook wat níet werkt.** Stub-implementaties, `TODO`'s in de firmware en
  onbeschreven commando's staan er gewoon in.

> [!WARNING]
> **Disclaimer.** Deze documentatie is samengesteld met hulp van AI-tools
> (ChatGPT, Claude, Perplexity). Die kunnen hallucineren — ze presenteren soms
> onjuiste informatie met grote stelligheid. Er wordt gecontroleerd tegen
> officiële bronnen en broncode, maar fouten zijn mogelijk. Raadpleeg bij
> twijfel de officiële MeshCore-documentatie. MeshCore is nog volop in
> ontwikkeling; informatie veroudert.

---

## English

MeshCore turns inexpensive LoRa radios into a network of their own. Messages hop
from node to node until they arrive — no internet, no cell towers, no
subscription. **DOMCA** (Dutch Open MeshCore Activity) exists to make that
knowledge accessible, and this repository holds the full documentation: 70
chapters in Dutch, the same 70 in English, with 52 diagrams per language. The
chapter count is the number of `.md` files per language tree excluding the
`README.md` indexes; the diagram count is the number of SVGs a chapter
references, not the number of files in `images/`.

### Getting started/How to read this


The chapters differ widely in the background they assume. This table states
per section what you need to bring, so you know what level of detail to expect.

| Section | What you find there | Assumed knowledge |
|---|---|---|
| [Usage](en/usage/) | What MeshCore is, getting a node running, hardware, regulations, privacy | None. No programming knowledge required |
| [Technical](en/technical/) | Protocol, packet layout byte by byte, encryption, routing, repeaters, room server | A basic grasp of networking and hexadecimal notation helps; programming is not needed |
| [Platform](en/platform/) | The four platform families and choosing between them | None beyond a general idea of microcontrollers |
| [Hardware](en/hardware/) | Radio, antenna, link budget, BLE, WiFi, USB, I²C, SPI, display, GPS, buttons | Basic electronics recommended; a few chapters show C++ fragments |
| [Libraries](en/libraries/) | The fifty-two external libraries that go into the firmware | Familiarity with PlatformIO build configurations recommended |
| [Design → logical](en/design/logical/) | Roles, components, contracts, information model, variability, design decisions | Basic knowledge of classes and interfaces recommended; the text stays away from source code |
| [Design → technical](en/design/technical/) | Source tree, class model, platform and radio realisation, build system, macros, traceability | C++  classes, inheritance and PlatformIO build configurations |
| [Reference](en/reference/) | Terminology, references, links | None. Meant for looking things up, not for reading through |
| [Project](en/project/) | About DOMCA, how the repository is organised | None |

If you hit a term you do not know, it is in
[Terminology](en/reference/terminology.md).

The full index is in **[en/README.md](en/README.md)**.

### What makes this different

The usage chapters do what you would expect. The technical chapters go a step
further, deliberately so:

- **Byte by byte.** Packets are written out with real values, not `XX XX`.
- **Verified against the source.** Technical claims name the firmware version and
  commit they were checked against, pointing at the relevant file in
  `meshcore-dev/MeshCore`.
- **Reproducible.** The examples in [Regions and Scopes](en/technical/regions-and-scopes.md)
  can be recomputed with [`tools/example-calculation.py`](tools/example-calculation.py).
- **Including what does not work.** Stub implementations, firmware `TODO`s and
  undocumented commands are described as such.

> [!WARNING]
> **Disclaimer.** This documentation was compiled with the help of AI tools
> (ChatGPT, Claude, Perplexity), which can hallucinate — sometimes presenting
> incorrect information with great confidence. Content is checked against
> official sources and source code, but errors are possible. When in doubt,
> consult the official MeshCore documentation. MeshCore is under active
> development; information ages.

---

## Structuur · Layout

```
├── nl/                 Nederlandse hoofdstukken
│   ├── gebruik/          gebruik, hardware, regelgeving
│   ├── techniek/         protocol, pakketten, encryptie, repeaters
│   │   └── roomserver/     inloggen, posts, synchronisatie, grenzen
│   ├── ontwerp/          hoe de firmware in elkaar zit
│   │   ├── logisch/        rollen, componenten, contracten, variabiliteit
│   │   └── technisch/      klassen, platformrealisatie, buildsysteem
│   ├── platform/         de vier platformfamilies en de keuze ertussen
│   ├── hardware/         waar een node uit bestaat
│   │   ├── radio/          transceiver, antenne, linkbudget
│   │   ├── interfaces/     BLE, WiFi, USB-serieel, I²C, SPI
│   │   └── peripherals/    scherm, GPS, knoppen en LED's
│   ├── libraries/        welke externe code de firmware in komt
│   │   ├── core/           kernlibraries, één hoofdstuk per library
│   │   └── other/          ondersteunende libraries, per functie gegroepeerd
│   ├── naslag/           terminologie, referenties, links
│   └── project/          over DOMCA, GitHub-overzicht
├── en/                 English chapters (same structure)
│   ├── usage/
│   ├── technical/
│   │   └── roomserver/
│   ├── design/
│   │   ├── logical/
│   │   └── technical/
│   ├── platform/
│   ├── hardware/
│   │   ├── radio/
│   │   ├── interfaces/
│   │   └── peripherals/
│   ├── libraries/
│   │   ├── core/
│   │   └── other/
│   ├── reference/
│   └── project/
├── images/
│   ├── nl/               diagrammen met Nederlandse tekst
│   └── en/               diagrammen met Engelse tekst
├── tools/              narekenscripts bij de techniekhoofdstukken
└── LICENSE             CC BY-SA 4.0
```

## Fouten en bijdragen · Errata and contributions

Fouten zijn welkom als issue, hoe klein ook. Bij technische correcties help je
het meest met een verwijzing naar het betreffende bestand in de
[MeshCore-broncode](https://github.com/meshcore-dev/MeshCore) — dan is het
verifieerbaar in plaats van aannemelijk.

*Corrections are welcome as issues, however small. For technical corrections, a
pointer to the relevant file in the MeshCore source is the most useful thing you
can add.*

## Licentie · Licence

[Creative Commons Attribution-ShareAlike 4.0 International](LICENSE) (CC BY-SA 4.0).
Delen en bewerken mag, ook commercieel, mits met naamsvermelding en onder
dezelfde licentie.

De licentie dekt de tekst, diagrammen en afbeeldingen in deze repository. De
MeshCore-firmware valt er niet onder — die wordt door de eigen auteurs onder
eigen voorwaarden verspreid. Code in `tools/` staat onder de MIT-licentie.

Copyright © 2025-2026 PE1HVH and contributors.

## Community

- [MeshCore](https://meshcore.io/) — officiële projectsite
- [MeshCore UK](https://meshcore.co.uk/) — flasher, hardware en community-hub
- [MeshCore Discord](https://discord.gg/ZVH2ujy9ex) — community server
- [LocalMesh NL](https://www.localmesh.nl/) — Nederlandse community
- [MeshCore op GitHub](https://github.com/meshcore-dev/MeshCore) — firmware

---

<div align="center">

**[domca.nl](https://domca.nl)** · [meshcore@pe1hvh.nl](mailto:meshcore@pe1hvh.nl)

73 de PE1HVH

</div>
