# MeshCore documentatie

Off-grid mesh communicatie via LoRa radio.

## Gebruik

- [Wat is MeshCore?](gebruik/what-is-meshcore.md)
- [Ontstaan en Geschiedenis](gebruik/history.md)
- [Node Types](gebruik/node-types.md)
- [Aan de Slag](gebruik/getting-started.md)
- [Communicatie](gebruik/communication.md)
- [Privacy & Beveiliging](gebruik/privacy.md)
- [Praktische Toepassingen](gebruik/applications.md)
- [Hardware Overzicht](gebruik/hardware.md)
- [Off-Grid Client Repeat Mode](gebruik/off-grid.md)
- [Regelgeving & Duty Cycle](gebruik/regulations.md)

## Techniek

- [Het Lagenmodel van MeshCore](techniek/layer-model.md)
- [Van Tekst naar Chirp](techniek/text-to-chirp.md)
- [Chirp en DeChirp vereenvoudigd voorgesteld](techniek/dechirp.md)
- [LoRa Modulatie](techniek/lora-modulation.md)
- [MeshCore Packet Structuur](techniek/packet-structure.md)
- [Regio's en Scopes](techniek/regions-and-scopes.md)
- [Regio's: bedoeling en praktijk](techniek/regions-in-practice.md)
- [Direct Messages](techniek/direct-messages.md)
- [Private & Public Key Encryptie](techniek/key-encryption.md)
- [Channel Structure & PSK](techniek/channel-structure.md)
- [BLE Architectuur](techniek/ble-architecture.md)
- [Remote Bediening](techniek/remote-control.md)
- [Route traceren](techniek/route-tracing.md)
- [Repeater TX/RX flow](techniek/repeater-flow.md)
- [SenseCap DFU](techniek/sensecap-dfu.md)
- [Hoger en sterker is niet altijd beter](techniek/dead-zone.md)

## Platform

- [MeshCore Platforms](platform/platforms.md)
- [De vier platformfamilies](platform/platform-families.md)
- [Nodematrix](platform/node-matrix.md)

## Libraries

- [Libraries in MeshCore](libraries/introduction.md)
- [Afhankelijkheden tussen libraries](libraries/dependencies.md)
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

## Naslag

- [Terminologie](naslag/terminology.md)
- [Referenties & Bronnen](naslag/references.md)
- [Links & Resources](naslag/links.md)

## Project

- [Over DOMCA](project/about-domca.md)
- [GitHub Repositories](project/github.md)
