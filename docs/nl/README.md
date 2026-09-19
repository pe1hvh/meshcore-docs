# MeshCore documentatie

Off-grid mesh communicatie via LoRa radio.

Nieuw hier? De [Leeswijzer](reading-guide.md) zegt wat elke sectie van je
vraagt en waar je het beste begint.

## Gebruik

- [Wat is MeshCore?](usage/what-is-meshcore.md)
- [Ontstaan en Geschiedenis](usage/history.md)
- [Node Types](usage/node-types.md)
- [Aan de Slag](usage/getting-started.md)
- [Communicatie](usage/communication.md)
- [Privacy & Beveiliging](usage/privacy.md)
- [Praktische Toepassingen](usage/applications.md)
- [Hardware Overzicht](usage/hardware.md)
- [Off-Grid Client Repeat Mode](usage/off-grid.md)
- [Regelgeving & Duty Cycle](usage/regulations.md)

## Techniek

- [Het Lagenmodel van MeshCore](technical/layer-model.md)
- [Van Tekst naar Chirp](technical/text-to-chirp.md)
- [Chirp en DeChirp vereenvoudigd voorgesteld](technical/dechirp.md)
- [LoRa Modulatie](technical/lora-modulation.md)
- [MeshCore Pakketstructuur](technical/packet-structure.md)
- [Regio's en Scopes](technical/regions-and-scopes.md)
- [Regio's: bedoeling en praktijk](technical/regions-in-practice.md)
- [Direct Messages](technical/direct-messages.md)
- **Room Server** — `technical/roomserver/`
  - [Wat een Room Server is](technical/roomserver/introduction.md)
  - [Inloggen en de ACL](technical/roomserver/login-and-acl.md)
  - [Posts en synchronisatie](technical/roomserver/posts-and-sync.md)
  - [Requests en CLI](technical/roomserver/requests-and-cli.md)
  - [Grenzen en open einden](technical/roomserver/limits-and-todos.md)
- [Private & Public Key Encryptie](technical/key-encryption.md)
- [Channel Structure & PSK](technical/channel-structure.md)
- [Remote Bediening](technical/remote-control.md)
- [Route traceren](technical/route-tracing.md)
- [Repeater TX/RX flow](technical/repeater-flow.md)
- [SenseCap DFU](technical/sensecap-dfu.md)
- [Hoger en sterker is niet altijd beter](technical/dead-zone.md)

## Ontwerp (Node)

- [Ontwerp van MeshCore](design/introduction.md)
- **Logisch ontwerp** — `design/logical/`
  - [Rollen](design/logical/roles.md)
  - [Componenten](design/logical/components.md)
  - [Contracten](design/logical/interfaces.md)
  - [Informatiemodel](design/logical/information-model.md)
  - [Variabiliteit](design/logical/variability.md)
  - [Ontwerpbeslissingen](design/logical/decisions.md)
- **Technisch ontwerp** — `design/technical/`
  - [De broncodestructuur](design/technical/source-layout.md)
  - [Het klassenmodel](design/technical/class-model.md)
  - [Platformrealisatie](design/technical/platform-realisation.md)
  - [Radiorealisatie](design/technical/radio-realisation.md)
  - [Het buildsysteem](design/technical/build-system.md)
  - [Compile-time configuratie](design/technical/configuration.md)
  - [Traceerbaarheid](design/technical/traceability.md)

## Ontwerp (Companion)

- [De companion-interface](companion/introduction.md)
- **Logisch ontwerp** — `companion/logical/`
  - [Verantwoordelijkheden](companion/logical/responsibilities.md)
  - [Het interactiemodel](companion/logical/interaction-model.md)
  - [Informatiemodel](companion/logical/information-model.md)
- **Technisch ontwerp** — `companion/technical/`
  - [De drie transporten](companion/technical/transports.md)
  - [Het frame](companion/technical/frame-format.md)
  - [De commandogroepen](companion/technical/command-groups.md)
  - [Architectuur van een client](companion/technical/client-architecture.md)
  
## Platform

- [MeshCore Platforms](platform/platforms.md)
- [De vier platformfamilies](platform/platform-families.md)
- [Nodematrix](platform/node-matrix.md)

## Hardware

- [Hardware van een node](hardware/introduction.md)
- **Radio** — `hardware/radio/`
  - [De LoRa-transceiver](hardware/radio/sx1262.md)
  - [Antenne](hardware/radio/antenna.md)
  - [Linkbudget](hardware/radio/link-budget.md)
  - [Filters](hardware/radio/filters.md)
- **Interfaces** — `hardware/interfaces/`
  - [BLE Architectuur](hardware/interfaces/ble-architecture.md)
  - [WiFi als companion-verbinding](hardware/interfaces/wifi.md)
  - [USB-serieel](hardware/interfaces/usb-serial.md)
  - [De I²C-bus](hardware/interfaces/i2c.md)
  - [De SPI-bus](hardware/interfaces/spi.md)
- **Randapparatuur** — `hardware/peripherals/`
  - [Het scherm](hardware/peripherals/display.md)
  - [GPS](hardware/peripherals/gps.md)
  - [Knoppen en LED's](hardware/peripherals/buttons-and-leds.md)

## Libraries

- [Libraries in MeshCore](libraries/introduction.md)
- [Afhankelijkheden tussen libraries](libraries/dependencies.md)
- [Library Configuratie](libraries/library-configuration.md)
- **Kernlibraries** — `libraries/core/`
  - [RadioLib](libraries/core/radiolib.md)
  - [Crypto: rweather en ed25519](libraries/core/crypto.md)
  - [CayenneLPP](libraries/core/cayenne-lpp.md)
  - [RTClib](libraries/core/rtclib.md)
  - [Melopero RV3028](libraries/core/rv3028.md)
  - [CustomLFS](libraries/core/custom-lfs.md)
  - [Adafruit LittleFS voor STM32](libraries/core/littlefs-stm32.md)
  - [SubGhz](libraries/core/subghz.md)
  - [ESPAsyncWebServer](libraries/core/espasyncwebserver.md)
  - [AsyncElegantOTA](libraries/core/asyncelegantota.md)
  - [Wire en SPI](libraries/core/wire-spi.md)
- **Ondersteunende libraries** — `libraries/other/`
  - [Displaylibraries](libraries/other/displays.md)
  - [Sensorlibraries](libraries/other/sensors.md)
  - [GPS-libraries](libraries/other/gps.md)
  - [Voeding en energiemeting](libraries/other/power.md)
  - [Randapparatuur](libraries/other/peripherals.md)
  - [Hulplibraries](libraries/other/utilities.md)
  - [Testlibraries](libraries/other/testing.md)

## CLI-referentie

- [CLI-referentie](cli/introduction.md)
- [Bediening](cli/operational.md)
- [Buren](cli/neighbors.md)
- [Statistieken](cli/statistics.md)
- [Logging](cli/logging.md)
- [Informatie](cli/info.md)
- [Radio](cli/radio.md)
- [Systeem](cli/system.md)
- [Routing](cli/routing.md)
- [ACL](cli/acl.md)
- [Regio's](cli/regions.md)
- [GPS](cli/gps.md)
- [Sensoren](cli/sensors.md)
- [Bridge](cli/bridge.md)
- [Energiebeheer (nRF52)](cli/power-management.md)
- [Companion: CLI Rescue](cli/companion-rescue.md)
- [Na de gepinde commit](cli/after-pinned-commit.md)

## Naslag

- [Terminologie](reference/terminology.md)
- [Referenties & Bronnen](reference/references.md)
- [Links & Resources](reference/links.md)

## Project

- [Leeswijzer](reading-guide.md)
- [Over DOMCA](project/about-domca.md)
- [GitHub Repositories](project/github.md)
- [Forks & varianten](https://domca.nl/#analyse/forks-en-varianten) — analyse op domca.nl
