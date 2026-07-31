# DOMCA — MeshCore documentatie

**Dutch Open MeshCore Activity** · Off-grid mesh-communicatie via LoRa
Tweetalige documentatie: van je eerste node tot de bits op de radio.

[![Licentie: CC BY-SA 4.0](https://img.shields.io/badge/licentie-CC%20BY--SA%204.0-blue.svg)](LICENSE)
[![Talen](https://img.shields.io/badge/talen-NL%20%7C%20EN-informational.svg)](#)
[![Website](https://img.shields.io/badge/web-domca.nl-brightgreen.svg)](https://domca.nl)

### 📖 [Lees in het Nederlands →](nl/README.md)  ·  🇬🇧 [Read in English →](en/README.md)

---

## Waar te beginnen · Where to start

**Nederlands** — MeshCore laat goedkope LoRa-radiootjes een eigen netwerk
vormen: berichten hoppen van node naar node tot ze aankomen, zonder internet
en zonder zendmast. Begin bij de [Leeswijzer](nl/reading-guide.md) — die zegt
wat elke sectie van je vraagt — of ga rechtstreeks naar de
[inhoudsopgave](nl/README.md).

**English** — MeshCore turns inexpensive LoRa radios into a network of their
own: messages hop from node to node until they arrive, with no internet and
no cell towers. Start with [How to read this](en/reading-guide.md), which
states what each section assumes, or go straight to the
[index](en/README.md).

> [!WARNING]
> **Disclaimer.** Deze documentatie is samengesteld met hulp van AI-tools
> (ChatGPT, Claude, Perplexity). Die kunnen hallucineren — ze presenteren soms
> onjuiste informatie met grote stelligheid. Er wordt gecontroleerd tegen
> officiële bronnen en broncode, maar fouten zijn mogelijk. Raadpleeg bij
> twijfel de officiële MeshCore-documentatie. MeshCore is nog volop in
> ontwikkeling; informatie veroudert.
>
> *This documentation was compiled with the help of AI tools (ChatGPT, Claude,
> Perplexity), which can hallucinate — sometimes presenting incorrect
> information with great confidence. Content is checked against official
> sources and source code, but errors are possible. When in doubt, consult the
> official MeshCore documentation. MeshCore is under active development;
> information ages.*

---

## Structuur · Layout

```
├── nl/                 Nederlandse hoofdstukken
│   ├── README.md         inhoudsopgave
│   ├── reading-guide.md  leeswijzer: secties en benodigde voorkennis
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
│   ├── companion/        het koppelvlak tussen app en node
│   │   ├── logisch/        verantwoordelijkheden, interactie, gegevens
│   │   └── technisch/      transporten, frames, commando's, clientlagen
│   ├── libraries/        welke externe code de firmware in komt
│   │   ├── core/           kernlibraries, één hoofdstuk per library
│   │   └── other/          ondersteunende libraries, per functie gegroepeerd
│   ├── naslag/           terminologie, referenties, links
│   └── project/          over DOMCA, GitHub-overzicht
├── en/                 English chapters (same structure)
│   ├── README.md
│   ├── reading-guide.md
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
│   ├── companion/
│   │   ├── logical/
│   │   └── technical/
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
