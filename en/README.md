# MeshCore documentation

Off-grid mesh communication over LoRa radio.

## Usage

- [What is MeshCore?](usage/what-is-meshcore.md)
- [Origin and History](usage/history.md)
- [Node Types](usage/node-types.md)
- [Getting Started](usage/getting-started.md)
- [Communication](usage/communication.md)
- [Privacy & Security](usage/privacy.md)
- [Practical Applications](usage/applications.md)
- [Hardware Overview](usage/hardware.md)
- [Off-Grid Client Repeat Mode](usage/off-grid.md)
- [Regulations & Duty Cycle](usage/regulations.md)

## Technical

- [The MeshCore Layer Model](technical/layer-model.md)
- [From Text to Chirp](technical/text-to-chirp.md)
- [Chirp and DeChirp Simplified](technical/dechirp.md)
- [LoRa Modulation](technical/lora-modulation.md)
- [MeshCore Packet Structure](technical/packet-structure.md)
- [Regions and Scopes](technical/regions-and-scopes.md)
- [Regions: intent and practice](technical/regions-in-practice.md)
- [Direct Messages](technical/direct-messages.md)
- [Private & Public Key Encryption](technical/key-encryption.md)
- [Channel Structure & PSK](technical/channel-structure.md)
- [BLE Architecture](technical/ble-architecture.md)
- [Remote Control](technical/remote-control.md)
- [Route Tracing](technical/route-tracing.md)
- [Repeater TX/RX flow](technical/repeater-flow.md)
- [SenseCap DFU](technical/sensecap-dfu.md)
- [Higher and stronger isn't always better](technical/dead-zone.md)

## Platform

- [MeshCore Platforms](platform/platforms.md)
- [The Four Platform Families](platform/platform-families.md)
- [Node Matrix](platform/node-matrix.md)

## Libraries

- [Libraries in MeshCore](libraries/introduction.md)
- [Dependencies between libraries](libraries/dependencies.md)
- **Core libraries** — `libraries/core/`
  - [RadioLib](libraries/core/radiolib.md)
  - [Crypto: rweather and ed25519](libraries/core/crypto.md)
  - [CayenneLPP](libraries/core/cayenne-lpp.md)
  - [RTClib](libraries/core/rtclib.md)
  - [Melopero RV3028](libraries/core/rv3028.md)
  - [CustomLFS](libraries/core/custom-lfs.md)
  - [Adafruit LittleFS for STM32](libraries/core/littlefs-stm32.md)
  - [SubGhz](libraries/core/subghz.md)
  - [ESPAsyncWebServer](libraries/core/espasyncwebserver.md)
  - [AsyncElegantOTA](libraries/core/asyncelegantota.md)
  - [Wire and SPI](libraries/core/wire-spi.md)
- **Supporting libraries** — `libraries/other/`
  - [Display libraries](libraries/other/displays.md)
  - [Sensor libraries](libraries/other/sensors.md)
  - [GPS libraries](libraries/other/gps.md)
  - [Power and energy measurement](libraries/other/power.md)
  - [Peripherals](libraries/other/peripherals.md)
  - [Utility libraries](libraries/other/utilities.md)
  - [Test libraries](libraries/other/testing.md)

## Reference

- [Terminology](reference/terminology.md)
- [References & Sources](reference/references.md)
- [Links & Resources](reference/links.md)

## Project

- [About DOMCA](project/about-domca.md)
- [GitHub Repositories](project/github.md)
