# GitHub Repositories

*DEVELOPERS · LIBRARIES · TOOLS · COMMUNITY PROJECTS*

Overview of MeshCore-related GitHub repositories for developers. From official libraries and CLI tools to community projects and GUI clients.

## Official Repositories (meshcore-dev)

| Repository | Language | Description |
|---|---|---|
| [MeshCore](https://github.com/meshcore-dev/MeshCore) | C++ | The core library: lightweight, portable C++ library for multi-hop packet routing on embedded LoRa devices. Includes sample applications such as Companion Radio, Repeater, Room Server, and Secure Chat. |
| [meshcore_py](https://github.com/meshcore-dev/meshcore_py) | Python | Official Python bindings for MeshCore. Provides programmatic access to MeshCore nodes via BLE, serial, or TCP for building custom applications and automation. |
| [meshcore-cli](https://github.com/meshcore-dev/meshcore-cli) | Python | Command line interface for MeshCore nodes. Connects via BLE, TCP, or serial and offers an interactive shell for messages, contact management, remote node management, and scripting. |
| [meshcore.js](https://github.com/meshcore-dev/meshcore.js) | JavaScript | JavaScript/TypeScript library for decoding MeshCore mesh packets with full cryptographic support. Foundation for web-based MeshCore clients. |
| [meshcore-ha](https://github.com/meshcore-dev/meshcore-ha) | Python | Home Assistant integration for monitoring and controlling MeshCore radio networks. Brings mesh data to your home automation dashboard. |

## Desktop & Terminal Clients

| Repository | Language | Description |
|---|---|---|
| [meshcore-gui (PE1HVH)](https://github.com/pe1hvh/meshcore-gui) | Python | MeshCore LAN server with web-based GUI. Runs as a background service on a Raspberry Pi or desktop and offers bot functionality, observer mode for network monitoring, and a large message archive. Intended as an always-on server in your own LAN. |
| [MeshTUI](https://github.com/ekollof/meshtui) | Python | Terminal UI (TUI) for MeshCore nodes built with Textual. Two-panel layout with tabs for chat, settings, node management, and logs. Supports BLE, TCP, and serial with optional TCP proxy. |

## Mobile Clients

| Repository | Language | Description |
|---|---|---|
| [meshcore-open](https://github.com/zjs81/meshcore-open) | Flutter/Dart | Open-source Flutter client for MeshCore. Fully featured mobile app with contacts, chat, channels, network map, settings, and repeater management. Supports background BLE and offline maps. |

## Firmware Variants & Bridges

| Repository | Language | Description |
|---|---|---|
| [dabeani/meshcore](https://github.com/dabeani/meshcore) | C++ | MeshCore firmware fork with improved companion UI for embedded devices. Touch-first interface with tabs for contacts, channels, map, and management. Extra support for T-Deck Plus and SenseCap Indicator. |
| [Akita-Zmodem-MeshCore](https://github.com/AkitaEngineering/Akita-Zmodem-MeshCore) | Python | File transfer over MeshCore networks using the Zmodem protocol. Designed for low bandwidth and high latency. Supports files and folders via asyncio. |
| [pe1hvh/meshcore-bridge](https://github.com/pe1hvh/meshcore-bridge) | Python | MeshCore bridge implementation by PE1HVH. Connects a MeshCore node via BLE or serial to other systems and services. |

## Web Tools & Maps

| Repository | Language | Description |
|---|---|---|
| [flasher.meshcore.dev](https://github.com/meshcore-dev/flasher.meshcore.dev) | JavaScript | Source code for the official MeshCore Web Flasher. Enables firmware flashing directly from the browser via the WebSerial API. |
| [map.meshcore.dev](https://github.com/meshcore-dev/map.meshcore.dev) | JavaScript | Source code for the official MeshCore network map. Displays live positions of active nodes, repeaters, and room servers. |

Translated from Dutch by Anthropic Claude
