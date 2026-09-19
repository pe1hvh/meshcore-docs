# The MeshCore Layer Model

*4 LAYERS · RF TO LEGAL*

MeshCore is built from four strictly separated layers, each with a specific function.

## The four layers

![Diagram 1 bij techniek-lagen](../../images/en/layer-model-1.svg)

## Layer 1: RF Hardware

Microcontroller (ESP32/nRF52), LoRa chip (SX1262), antenna, and power supply. This is the physical foundation of every node.

## Layer 2: LoRa PHY

The modem layer translates bits into radio signals via Chirp Spread Spectrum. Bandwidth (BW), Spreading Factor (SF), and Coding Rate (CR) determine the balance between range and speed.

## Layer 3: Firmware and Network Stack

MeshCore firmware handles routing, message processing, and network management. Every node has its own identity in the form of an Ed25519 keypair; in packets and paths that node is identified by the **first byte of its public key** (see [MeshCore Packet Structure](packet-structure.md)). Nodes can learn routes to other nodes: **intelligent routing** instead of flooding ensures efficient network traffic.

## Layer 4: Legal mode

Determines whether the device runs in HAM mode (70 cm band, no encryption, callsign required) or ISM mode (868 MHz, encryption, anonymous possible).

## Link Budget — Why LoRa reaches so far

Link budget is the total signal loss a connection can sustain. LoRa achieves **150+ dB link budget**, enabling:

- Long distances with low power
- Connections below the noise floor that can still be decoded
- Meshes with few nodes that can already scale regionally (via hops)

Translated from Dutch by Anthropic Claude
