# GitHub Repositories

*ONTWIKKELAARS · LIBRARIES · TOOLS · COMMUNITY PROJECTEN*

Overzicht van MeshCore gerelateerde GitHub repositories voor ontwikkelaars. Van officiële libraries en CLI-tools tot community-projecten en GUI-clients.

## Officiële Repositories (meshcore-dev)

| Repository | Taal | Beschrijving |
|---|---|---|
| [MeshCore](https://github.com/meshcore-dev/MeshCore) | C++ | De kern-library: lightweight, portable C++ library voor multi-hop packet routing op embedded LoRa-apparaten. Bevat voorbeeldapplicaties zoals Companion Radio, Repeater, Room Server en Secure Chat. |
| [meshcore_py](https://github.com/meshcore-dev/meshcore_py) | Python | Officiële Python bindings voor MeshCore. Biedt programmatische toegang tot MeshCore nodes via BLE, serieel of TCP voor het bouwen van eigen applicaties en automatisering. |
| [meshcore-cli](https://github.com/meshcore-dev/meshcore-cli) | Python | Command line interface voor MeshCore nodes. Verbindt via BLE, TCP of serieel en biedt interactieve shell voor berichten, contactbeheer, remote node management en scripting. |
| [meshcore.js](https://github.com/meshcore-dev/meshcore.js) | JavaScript | Officiële JavaScript-library voor het companion-protocol. Verbindt via Web Bluetooth, Web Serial, seriële poort of TCP met een node en spreekt de commando's en antwoorden van de companion-firmware. Basis voor web-gebaseerde MeshCore clients. |
| [meshcore-ha](https://github.com/meshcore-dev/meshcore-ha) | Python | Home Assistant integratie voor het monitoren en besturen van MeshCore radio-netwerken. Brengt mesh-data naar je domotica-dashboard. |

> [!NOTE]
> De MeshCore-firmware verwijst op twee plaatsen naar verschillende
> repositories voor dezelfde libraries. `README.md` r.70-71 noemt
> `liamcottle/meshcore.js` en `fdlamotte/meshcore-cli`;
> `docs/companion_protocol.md` r.16-17 noemt `meshcore-dev/meshcore.js` en
> `meshcore-dev/meshcore_py`. De projecten zijn naar de organisatie verhuisd
> en de README is niet meegegaan. De tabel hierboven volgt de
> `meshcore-dev`-varianten. Zie
> [Architectuur van een client](../companion/technisch/client-architecture.md).

## Desktop & Terminal Clients

| Repository | Taal | Beschrijving |
|---|---|---|
| [meshcore-gui (PE1HVH)](https://github.com/pe1hvh/meshcore-gui) | Python | MeshCore LAN-server met web-based GUI. Draait als achtergrondservice op een Raspberry Pi of desktop en biedt bot-functionaliteit, observer-modus voor netwerkmonitoring en een groot berichtenarchief. Bedoeld als always-on server in je eigen LAN. |
| [MeshTUI](https://github.com/ekollof/meshtui) | Python | Terminal UI (TUI) voor MeshCore nodes gebouwd met Textual. Twee-panel layout met tabs voor chat, instellingen, node management en logs. Ondersteunt BLE, TCP en serieel met optionele TCP proxy. |

## Mobiele Clients

| Repository | Taal | Beschrijving |
|---|---|---|
| [meshcore-open](https://github.com/zjs81/meshcore-open) | Flutter/Dart | Open-source Flutter client voor MeshCore. Volledig uitgeruste mobiele app met contacten, chat, kanalen, netwerkkaart, instellingen en repeater-beheer. Ondersteunt achtergrond-BLE en offline kaarten. |

## Firmware Varianten & Bridges

| Repository | Taal | Beschrijving |
|---|---|---|
| [dabeani/meshcore](https://github.com/dabeani/meshcore) | C++ | MeshCore firmware fork met verbeterde companion UI voor embedded apparaten. Touch-first interface met tabs voor contacten, kanalen, kaart en beheer. Extra ondersteuning voor T-Deck Plus en SenseCap Indicator. |
| [Akita-Zmodem-MeshCore](https://github.com/AkitaEngineering/Akita-Zmodem-MeshCore) | Python | Bestandsoverdracht via MeshCore netwerken met het Zmodem-protocol. Ontworpen voor lage bandbreedte en hoge latency. Ondersteunt bestanden en mappen via asyncio. |
| [pe1hvh/meshcore-bridge](https://github.com/pe1hvh/meshcore-bridge) | Python | MeshCore bridge implementatie door PE1HVH. Koppelt een MeshCore node via BLE of serieel aan andere systemen en diensten. |

## Web Tools & Kaarten

| Repository | Taal | Beschrijving |
|---|---|---|
| [flasher.meshcore.dev](https://github.com/meshcore-dev/flasher.meshcore.dev) | JavaScript | Broncode van de officiële MeshCore Web Flasher. Maakt firmware flashen mogelijk direct vanuit de browser via WebSerial API. |
| [map.meshcore.dev](https://github.com/meshcore-dev/map.meshcore.dev) | JavaScript | Broncode van de officiële MeshCore netwerkkaart. Toont live posities van actieve nodes, repeaters en room servers. |
