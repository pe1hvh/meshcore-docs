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

Deze repository bevat de volledige documentatie: 30 hoofdstukken in het
Nederlands, dezelfde 30 in het Engels, met 50 diagrammen.

### Beginnen

| Ik wil… | Begin hier |
|---|---|
| weten waar dit over gaat | [Wat is MeshCore?](nl/gebruik/wat-is-meshcore.md) |
| een node aan de praat krijgen | [Aan de Slag](nl/gebruik/aan-de-slag.md) · [Hardware](nl/gebruik/hardware.md) |
| weten wat mag binnen de regels | [Regelgeving & Duty Cycle](nl/gebruik/regelgeving.md) |
| begrijpen hoe het écht werkt | [Het Lagenmodel](nl/techniek/techniek-lagen.md) → [Packet Structuur](nl/techniek/techniek-packets.md) |
| een repeater goed instellen | [Regio's en Scopes](nl/techniek/techniek-scope.md) · [Repeater TX/RX flow](nl/techniek/repeater-flow.md) |
| weten waarom regio's zijn zoals ze zijn | [Regio's: bedoeling en praktijk](nl/techniek/techniek-regios-praktijk.md) |
| een term opzoeken | [Terminologie](nl/naslag/terminologie.md) |

Het volledige overzicht staat in **[nl/README.md](nl/README.md)**.

### Wat dit anders maakt

De gebruikershoofdstukken doen wat je verwacht. De techniekhoofdstukken gaan
een stap verder, en dat is bewust:

- **Byte voor byte.** Pakketten worden uitgeschreven met echte waarden, niet met
  `XX XX`. Je ziet waar de header ophoudt en de payload begint.
- **Geverifieerd tegen de broncode.** Technische claims vermelden de
  firmwareversie en commit waartegen ze zijn gecontroleerd, met verwijzing naar
  het betreffende bestand in `meshcore-dev/MeshCore`.
- **Narekenbaar.** De voorbeelden in [Regio's en Scopes](nl/techniek/techniek-scope.md)
  zijn met [`tools/bereken-voorbeeld.py`](tools/bereken-voorbeeld.py) te
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
knowledge accessible, and this repository holds the full documentation: 30
chapters in Dutch, the same 30 in English, with 50 diagrams.

### Getting started

| I want to… | Start here |
|---|---|
| know what this is about | [What is MeshCore?](en/usage/wat-is-meshcore.md) |
| get a node running | [Getting Started](en/usage/aan-de-slag.md) · [Hardware](en/usage/hardware.md) |
| stay within the rules | [Regulations & Duty Cycle](en/usage/regelgeving.md) |
| understand how it really works | [The Layer Model](en/technical/techniek-lagen.md) → [Packet Structure](en/technical/techniek-packets.md) |
| configure a repeater properly | [Regions and Scopes](en/technical/techniek-scope.md) · [Repeater TX/RX flow](en/technical/repeater-flow.md) |
| know why regions are the way they are | [Regions: intent and practice](en/technical/techniek-regios-praktijk.md) |
| look up a term | [Terminology](en/reference/terminologie.md) |

The full index is in **[en/README.md](en/README.md)**.

### What makes this different

The usage chapters do what you would expect. The technical chapters go a step
further, deliberately so:

- **Byte by byte.** Packets are written out with real values, not `XX XX`.
- **Verified against the source.** Technical claims name the firmware version and
  commit they were checked against, pointing at the relevant file in
  `meshcore-dev/MeshCore`.
- **Reproducible.** The examples in [Regions and Scopes](en/technical/techniek-scope.md)
  can be recomputed with [`tools/bereken-voorbeeld.py`](tools/bereken-voorbeeld.py).
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
│   ├── naslag/           terminologie, referenties, links
│   └── project/          over DOMCA, GitHub-overzicht
├── en/                 English chapters (same structure)
│   ├── usage/ 
│   ├── technical/
│   ├── reference/
│   └── project/
├── images/             diagrammen (SVG) en foto's
├── tools/              narekenscripts bij de techniekhoofdstukken
└── LICENSE             CC BY-SA 4.0
```

`RECONCILIATIE.md` en `OPENSTAAND.md` zijn werkbestanden van de redactie, geen
hoofdstukken — ze houden bij wat er nog samengevoegd of aangevuld moet worden.

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
