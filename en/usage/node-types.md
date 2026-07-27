# Node Types

*FIRMWARE PROFILES · ROLES IN THE MESH*

MeshCore distinguishes different node types based on their function in the network. These types are determined by the **firmware profile** you flash onto your hardware.

## Node Types Overview

- **Companion Radio** — The most commonly used type for end users. Acts as a radio interface for a smartphone via Bluetooth (BLE), USB, or WiFi. The MeshCore Companion App controls the node.
- **Repeater** — Primary task: forwarding messages to extend network range. Typically placed at strategic locations with a good antenna position such as rooftops or hilltops.
- **Room Server** — Manages one or more Rooms with store-and-forward functionality. Stores messages for offline recipients. Requires an Ultra licence for remote management.
- **Standalone Device** — Hardware such as the T-Deck Plus can operate completely independently. With a built-in screen and keyboard you can type and read messages directly — no smartphone needed.
- **Telemetry Node** — Specifically for sending sensor data: temperature, humidity, battery voltage. Expandable via GPIO, I²C, or SPI interfaces.

## Typical network

In practice, a network consists of a combination of these node types. A typical family network:

> [!NOTE]
> **Example:** 2–4 Companion Radios for family members, 1 Repeater at a high point for better coverage, and 1 Room Server at home for store-and-forward.

![Diagram 1 bij node-types](../../images/node-types-1.svg)

Translated from Dutch by Anthropic Claude
