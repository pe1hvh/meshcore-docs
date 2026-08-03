# The Hardware of a Node

*BLOCK DIAGRAM · RADIO · INTERFACES · PERIPHERALS*

A MeshCore node is an MCU with a radio beside it and a handful of
parts around it. This section describes those parts one by one: what each
is, how it attaches to the MCU, and what the firmware does with
it. This chapter sets out the block diagram and explains where the
boundary lies between the three groups the rest of the section is split
into.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `variants/heltec_v3/platformio.ini`, `variants/heltec_v3/target.h`,
> `src/helpers/BaseSerialInterface.h`, `src/helpers/ui/DisplayDriver.h` and
> `src/helpers/SensorManager.h`.

## What is inside a node

![Block diagram of a MeshCore node: antenna and LoRa transceiver on the
left, the MCU in the middle, BLE, WiFi and USB serial above it towards the
companion app, and display, GPS and buttons below on the buses of the
MCU](../../images/en/node-blockdiagram-1.svg)

On the left is the RF side: an antenna on a transceiver, which hangs off
the MCU over SPI. In the middle sits the MCU — the only part present in
every node, and the part that determines what the rest can be. Above it the
connections to the outside world, along which a phone or a terminal
operates the node. Below it everything that hangs on the buses of the MCU
and is optional: a node works without a screen, without GPS and without
buttons.

The transceiver is not optional. Without a radio there is no node, just a
board with a processor on it.

## MCU or SoC

The middle block is called the **MCU** throughout this section: the chip the
firmware runs on, with processor, memory, flash and the buses the rest hangs
off. That is the term the rest of the documentation uses too —
`node-matrix.md` puts the sixty boards under it in a single column.

On three of the four platform families that MCU is not a separate chip on
the board but part of a **SoC**: a chip that wraps memory, and usually a
radio, around it. The difference in one line:

| Term | What it names |
|---|---|
| MCU | The computing chip: processor, memory, flash, buses |
| SoC | A chip combining an MCU and more around it in one package |

Every SoC therefore contains an MCU; not every MCU sits in a SoC.

| Family | Chip | SoC? | What else is in it |
|---|---|---|---|
| ESP32 | ESP32, ESP32-S3, ESP32-C3, ESP32-C6 | yes | WiFi and BLE |
| nRF52 | nRF52840 | yes | BLE |
| STM32 | STM32WLE5 | yes | The LoRa radio itself |
| RP2040 | RP2040 | no | Bare MCU; everything sits beside it |

The RP2040 is the only bare microcontroller in the set, and that explains why
an RP2040 node has no BLE and no WiFi: they are in nothing. See
[MeshCore Platforms](../platform/platforms.md).

The LoRa transceiver stands apart from this. Even on a SoC it is nearly
always a separate chip — the SX1262 or SX1276 beside the MCU. The STM32WLE5
is the exception: there the LoRa radio does sit on the same chip.

## How the firmware names the blocks

The blocks in the diagram are not an abstraction added afterwards: they are
in the firmware literally, as build flags per board. Every supported board
has its own directory under `variants/` with a `platformio.ini` that fixes
the pins. For the Heltec WiFi LoRa 32 V3 it looks like this:

`variants/heltec_v3/platformio.ini` r.10-24

```ini
  -D P_LORA_DIO_1=14
  -D P_LORA_NSS=8
  -D P_LORA_RESET=RADIOLIB_NC
  -D P_LORA_BUSY=13
  -D P_LORA_SCLK=9
  -D P_LORA_MISO=11
  -D P_LORA_MOSI=10
  -D USE_SX1262
  -D RADIO_CLASS=CustomSX1262
  -D WRAPPER_CLASS=CustomSX1262Wrapper
  -D LORA_TX_POWER=22
  -D P_LORA_TX_LED=35
  -D PIN_BOARD_SDA=17
  -D PIN_BOARD_SCL=18
  -D PIN_USER_BTN=0
```

That is the block diagram in fifteen lines: `SCLK`, `MISO`, `MOSI` and
`NSS` are the SPI bus to the radio, `BUSY` and `DIO_1` the two lines the
radio answers back on, `SDA` and `SCL` the I²C bus the display hangs on,
and `USER_BTN` the only button on this board. A board without a screen
simply lacks the `PIN_BOARD_*` lines.

On the C++ side every block returns as an abstract class with one
implementation per chip:

| Block | Abstraction in the firmware | Where |
|---|---|---|
| Radio | `RADIO_CLASS` / `WRAPPER_CLASS`, filled in per chip | `src/helpers/radiolib/` |
| Connection to the outside | `BaseSerialInterface` | `src/helpers/BaseSerialInterface.h` |
| Screen | `DisplayDriver` | `src/helpers/ui/DisplayDriver.h` |
| Sensors and GPS | `SensorManager` | `src/helpers/SensorManager.h` |
| Button | `MomentaryButton` | `src/helpers/ui/MomentaryButton.h` |

That `BaseSerialInterface` is a single abstraction for BLE, WiFi *and* USB
is not a detail: to the firmware these are three implementations of the same
notion — a connection carrying frames to a companion.

## The three subsections

The section is divided by what a part *does*, not by where it sits on the
board:

| Subsection | What belongs there | Criterion |
|---|---|---|
| `radio/` | transceiver, antenna, link budget | everything between the firmware and the air |
| `interfaces/` | BLE, WiFi, USB serial, I²C, SPI | a connection data travels along, not the device at the far end |
| `peripherals/` | display, GPS, buttons and LEDs | the device at the far end of such a connection |

The distinction between the last two occasionally needs explaining. SPI is under
`interfaces/`, the SX1262 hanging off it is under `radio/`, and the OLED
hanging off I²C is under `peripherals/`. The bus and the thing on it are
two separate topics.

> [!NOTE]
> **The word peripherals.** The word is used in three places in this
> documentation and does not mean the same thing everywhere. Table 3 of
> the [Node Matrix](../platform/node-matrix.md) groups display, GPS, WiFi,
> BLE and USB under it — connections included. The chapter
> [Peripherals](../libraries/other/peripherals.md) is about libraries for
> buzzers, LEDs and bus expanders. Here it is only the name of the third
> group above, which specifically excludes the connections. The LoRa radio
> falls under that heading nowhere: it is the reason a node exists, not
> something attached to it.

## What is documented elsewhere

This section describes the parts themselves. Which board has which part is
documented elsewhere, and those counts are not repeated here:

- [MeshCore Platforms](../platform/platforms.md) — why the chip determines
  what the device can do.
- [The Four Platform Families](../platform/platform-families.md) — what
  each family puts inside the chip, and where BLE or WiFi is missing.
- [Node Matrix](../platform/node-matrix.md) — every board with its radio,
  screen, GPS and link options side by side.
- [Hardware Overview](../usage/hardware.md) — four devices discussed at
  length, with prices.
- [Regulations & Duty Cycle](../usage/regulations.md) — what you may
  actually transmit on 868 MHz. Duty cycle stays there; the radio chapters
  refer to it.
- [The Layer Model of MeshCore](../technical/layer-model.md) — where the
  hardware ends and the protocol begins.

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`variants/heltec_v3/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/heltec_v3/platformio.ini)
  — pin definitions of the example board
- [`variants/heltec_v3/target.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/heltec_v3/target.h)
  — which blocks that board instantiates
- [`src/helpers/BaseSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/BaseSerialInterface.h)
  — the shared abstraction for BLE, WiFi and USB serial
- [`src/helpers/ui/DisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/DisplayDriver.h)
  — the abstraction covering all screen types
- [`src/helpers/SensorManager.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/SensorManager.h)
  — sensors and location providers

Translated from Dutch by Anthropic Claude
