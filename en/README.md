# MeshCore documentation

Off-grid mesh communication over LoRa radio.

New here? [How to read this](reading-guide.md) states what each section
assumes and where to start.

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
- **Room Server** — `technical/roomserver/`
  - [What a Room Server Is](technical/roomserver/introduction.md)
  - [Logging In and the ACL](technical/roomserver/login-and-acl.md)
  - [Posts and Synchronisation](technical/roomserver/posts-and-sync.md)
  - [Requests and CLI](technical/roomserver/requests-and-cli.md)
  - [Limits and Loose Ends](technical/roomserver/limits-and-todos.md)
- [Private & Public Key Encryption](technical/key-encryption.md)
- [Channel Structure & PSK](technical/channel-structure.md)
- [Remote Control](technical/remote-control.md)
- [Route Tracing](technical/route-tracing.md)
- [Repeater TX/RX flow](technical/repeater-flow.md)
- [SenseCap DFU](technical/sensecap-dfu.md)
- [Higher and stronger isn't always better](technical/dead-zone.md)

## Design (Node)

- [Designing MeshCore](design/introduction.md)
- **Logical design** — `design/logical/`
  - [Roles](design/logical/roles.md)
  - [Components](design/logical/components.md)
  - [Contracts](design/logical/interfaces.md)
  - [Information model](design/logical/information-model.md)
  - [Variability](design/logical/variability.md)
  - [Design decisions](design/logical/decisions.md)
- **Technical design** — `design/technical/`
  - [The source tree](design/technical/source-layout.md)
  - [The class model](design/technical/class-model.md)
  - [Platform realisation](design/technical/platform-realisation.md)
  - [Radio realisation](design/technical/radio-realisation.md)
  - [The build system](design/technical/build-system.md)
  - [Compile-time configuration](design/technical/configuration.md)
  - [Traceability](design/technical/traceability.md)
  
## Design (Companion)

- [The companion interface](companion/introduction.md)
- **Logical design** — `companion/logical/`
  - [Responsibilities](companion/logical/responsibilities.md)
  - [The interaction model](companion/logical/interaction-model.md)
  - [Information model](companion/logical/information-model.md)
- **Technical design** — `companion/technical/`
  - [The three transports](companion/technical/transports.md)
  - [The frame](companion/technical/frame-format.md)
  - [The command groups](companion/technical/command-groups.md)
  - [Architecture of a client](companion/technical/client-architecture.md)

## Platform

- [MeshCore Platforms](platform/platforms.md)
- [The Four Platform Families](platform/platform-families.md)
- [Node Matrix](platform/node-matrix.md)

## Hardware

- [The Hardware of a Node](hardware/introduction.md)
- **Radio** — `hardware/radio/`
  - [The LoRa Transceiver](hardware/radio/sx1262.md)
  - [Antenna](hardware/radio/antenna.md)
  - [Link Budget](hardware/radio/link-budget.md)
- **Interfaces** — `hardware/interfaces/`
  - [BLE Architecture](hardware/interfaces/ble-architecture.md)
  - [WiFi as a Companion Connection](hardware/interfaces/wifi.md)
  - [USB Serial](hardware/interfaces/usb-serial.md)
  - [The I²C Bus](hardware/interfaces/i2c.md)
  - [The SPI Bus](hardware/interfaces/spi.md)
- **Peripherals** — `hardware/peripherals/`
  - [The Display](hardware/peripherals/display.md)
  - [GPS](hardware/peripherals/gps.md)
  - [Buttons and LEDs](hardware/peripherals/buttons-and-leds.md)

## Libraries

- [Libraries in MeshCore](libraries/introduction.md)
- [Dependencies between libraries](libraries/dependencies.md)
- [Library Configuration](libraries/library-configuration.md)
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

- [How to read this](reading-guide.md)
- [About DOMCA](project/about-domca.md)
- [GitHub Repositories](project/github.md)
