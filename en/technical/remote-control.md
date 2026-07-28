# Remote Control

*COMMAND & CONTROL · GPIO · OFF-GRID*

MeshCore is not just a chat system. It can be used as a fully off-grid, encrypted **command-and-control network**.

## Every node is more than a radio

Every MeshCore node simultaneously acts as:

- **A LoRa radio** — for wireless communication
- **A router** — for mesh network functions
- **A computer (ESP32)** — with processing power
- **I/O interfaces** — UART, GPIO, I2C, SPI, USB

## What can you connect?

- **Relays** — Switchable power for remote devices.
- **Arduino / Raspberry Pi** — More complex tasks via UART or I2C control.
- **Transceivers** — Control via CAT interface for remote radio.
- **Sensors** — Temperature, humidity, air pressure monitoring.
- **Motors and rotators** — Controlling antenna direction remotely.
- **Power switches** — Remote on/off for devices and installations.

## How does it work?

> [!WARNING]
> **What the protocol does and does not offer.** In firmware v1.16.0 there is no
> service layer with calls like `gpio.toggle`, `uart.send`, or `i2c.read`, and no
> COMMAND packet type. What does exist:
>
> - **CLI over the mesh** — an encrypted text message with `txt_type` = CLI command (see [MeshCore Packet Structure](packet-structure.md)). A logged-in admin can send any CLI command to a remote node this way.
> - **Requests** — `REQ` with sub-types for status, telemetry, neighbour table, and access list.
> - **Sensors** — `sensor get` / `sensor set`, and telemetry in Cayenne LPP, provided sensor support is compiled in.
> - **Custom extensions** — `PAYLOAD_TYPE_RAW_CUSTOM` (`0x0F`) permits free-form bytes with your own encryption, and the firmware is structured so you can add your own handling.
>
> The applications below are therefore achievable, but they require custom
> firmware or an attached microcontroller that acts on the CLI or a custom
> payload. They cannot be configured out of the stock firmware.

## Example: Rooftop Remote Station

> [!NOTE]
> Node on the roof with GPIO connections to an antenna rotator and transceiver. Node inside connected via BLE to phone. Command: **Phone → BLE → indoor node → mesh → rooftop node → GPIO → rotor turns**. No WiFi, no internet, no cloud.

## Why is this so powerful?

- Cannot be jammed with a single transmitter (frequency hopping, mesh routing)
- No central point that can fail
- No cloud or internet required
- Fully encrypted (AES)
- Tens of kilometres range via mesh hops

Translated from Dutch by Anthropic Claude
