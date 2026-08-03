# The SPI Bus

*FOUR LINES · NSS AND BUSY · THREE PLATFORMS, THREE WAYS · DIO1*

SPI is the bus the radio hangs off, which makes it the more important of the
two. Every packet a node sends or receives travels over these four wires.
This chapter describes which pins those are, which extra lines the SX1262
needs beside the bus itself, and why the firmware uses a different method
per platform to set those pins.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — file
> `src/helpers/radiolib/CustomSX1262.h` and the `P_LORA_` flags in
> `variants/`.

![Diagram of the SPI link between SoC and radio: SCLK, MOSI, MISO and NSS as
the bus, with BUSY, RESET and DIO1 as separate control
lines](../../../images/en/spi-1.svg)

## Four lines for the bus, three beside it

SPI itself is four wires. The SX1262 needs three more that are not part of
the bus:

| Flag | Line | Role |
|---|---|---|
| `P_LORA_SCLK` | `SCLK` | clock, driven by the SoC |
| `P_LORA_MOSI` | `MOSI` | SoC → radio |
| `P_LORA_MISO` | `MISO` | radio → SoC |
| `P_LORA_NSS` | `NSS` | chip select, active low |
| `P_LORA_BUSY` | — | radio is busy, do not send commands |
| `P_LORA_RESET` | — | hard reset of the chip |
| `P_LORA_DIO_1` | — | interrupt: packet done or received |

The last three are why an SX1262 cannot simply be hung off an arbitrary SPI
bus. `BUSY` has to be readable before every command, and `DIO1` has to sit
on a pin that can raise an interrupt — otherwise the firmware has to poll
and misses packets.

`variants/lilygo_tbeam_1w/platformio.ini` r.12-19

```ini
  -D RADIO_CLASS=CustomSX1262
  -D WRAPPER_CLASS=CustomSX1262Wrapper
  -D P_LORA_DIO_1=1
  -D P_LORA_NSS=15
  -D P_LORA_RESET=3
  -D P_LORA_BUSY=38
  -D P_LORA_SCLK=13
  -D P_LORA_MISO=12
  -D P_LORA_MOSI=11
```

Across all variant directories together, commented-out lines excluded,
`P_LORA_DIO_1` occurs most often (241 lines) and `P_LORA_MOSI` least (93).
That difference is not an inconsistency: boards where the radio sits inside
the SoC or hangs off a fixed SPI bus do not need to name the three bus
lines, but always need an interrupt pin.

## Three platforms, three ways

Here is the oddity of this chapter. Setting the SPI pins happens differently
per platform, and that difference comes not from MeshCore but from the
Arduino cores underneath:

`src/helpers/radiolib/CustomSX1262.h` r.30-44

```cpp
  #if defined(P_LORA_SCLK)
    #ifdef NRF52_PLATFORM
      if (spi) { spi->setPins(P_LORA_MISO, P_LORA_SCLK, P_LORA_MOSI); spi->begin(); }
    #elif defined(RP2040_PLATFORM)
      if (spi) {
        spi->setMISO(P_LORA_MISO);
        //spi->setCS(P_LORA_NSS); // Setting CS results in freeze
        spi->setSCK(P_LORA_SCLK);
        spi->setMOSI(P_LORA_MOSI);
        spi->begin();
      }
    #else
      if (spi) spi->begin(P_LORA_SCLK, P_LORA_MISO, P_LORA_MOSI);
    #endif
  #endif
```

| Platform | Method |
|---|---|
| nRF52 | one `setPins()` with three arguments, then `begin()` |
| RP2040 | three separate setters, then `begin()` |
| others (ESP32) | `begin()` with the three pins as arguments |

All three do the same thing and none of the three is interchangeable. The
argument order differs as well: on nRF52 it is MISO, SCLK, MOSI; on ESP32 it
is SCLK, MISO, MOSI. A pin in the wrong position produces no error message
but a radio that does not respond.

> [!NOTE]
> The commented-out line under RP2040 is not a leftover but a warning with a
> reason attached: calling `setCS()` freezes the board. Chip select is
> therefore driven by RadioLib itself through `P_LORA_NSS`, not by the SPI
> class.

The whole block sits behind `#if defined(P_LORA_SCLK)`. If a variant does
not set that flag, nothing happens and the SPI class uses the board's
default pins. That is the normal case on boards where the radio hangs off
the hardware SPI port.

## What else hangs off it

SPI is not exclusive to the radio. On boards with an e-paper display or an
SD card, those share the same bus, each with its own chip select. That works
as long as exactly one `NSS` is low at a time. Which boards have an SPI
display is in [The Display](../peripherals/display.md).

The radio is the most demanding user here: it wants to be served in time
when `DIO1` fires. A long display refresh over the same bus can result
in packet loss.

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`src/helpers/radiolib/CustomSX1262.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/radiolib/CustomSX1262.h)
  — the three platform-dependent ways of setting the SPI pins
- [`variants/lilygo_tbeam_1w/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/lilygo_tbeam_1w/platformio.ini)
  — the `P_LORA_` pins of one board

Related in this documentation:

- [The LoRa Transceiver](../radio/sx1262.md) — what sits at the other end of
  the bus
- [The I²C Bus](i2c.md) — the slow bus next to it
- [Wire and SPI](../../libraries/core/wire-spi.md) — why these are framework
  libraries and not packages
- [The Display](../peripherals/display.md) — the other user of this bus
- [The Four Platform Families](../../platform/platform-families.md) — where
  the platform difference comes from

Translated from Dutch by Anthropic Claude
