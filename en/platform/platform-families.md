# The Four Platform Families

*ESP32 · NRF52840 · RP2040 · STM32WL*

Four families, one firmware. ESP32, nRF52840, RP2040 and STM32WL share the
same source code, but each chip brings its own cores, memory, transports
and limits. This chapter walks through them one by one: what the chip
brings and what it costs. The comparison, the device list and the decision
guide are in [MeshCore Platforms](platforms.md).

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0 (`FIRMWARE_BUILD_DATE "6 Jun 2026"`), commit
> `03b6ef4`, 28 July 2026 — `platformio.ini`, `variants/*/platformio.ini`
> (79 directories, 507 build targets), `boards/*.json` (41 definitions),
> `examples/companion_radio/main.cpp` and
> `docs/nrf52_power_management.md`. Every count in this chapter was also
> checked against commit `a3a1aa5` (19 July 2026) and is identical there.
> To reproduce: [`tools/platform-overview.py`](../../tools/platform-overview.py).

## ESP32 — the versatile workhorse

### Four SoCs under one heading

`[esp32_base]` (`platformio.ini` lines 57-65) covers four different chips.
The 37 variants divide up roughly like this: about 24 use an ESP32-S3, six
the classic ESP32, four a C3 and three a C6. Those are also two different
processor architectures: Xtensa LX6 in the classic ESP32, Xtensa LX7 in
the S3, and RISC-V in the C3 and C6.

The C6 is an edge case. `[esp32c6_base]` (lines 72-76) extends
`esp32_base` but pulls its platform from a different URL — pioarduino with
Arduino-ESP32 3.x. Above it, the repo itself notes that this is
experimental and may be less stable than the other platforms (line 73).
Three variants, sixteen build targets, and — see the table further down —
not a single ready-made device in the web flasher.

### What you get for it

ESP32 is the only family with WiFi (17 build targets), the only one with
OTA (36 variants load `[esp32_ota]`, lines 67-70) and the only one with
ESP-NOW (`src/helpers/esp32/ESPNOWRadio.cpp`, 32 variants). On top of that
4 to 16 MB of flash, PSRAM on the more expensive boards, and the second
best display support after nRF52.

`src/helpers/esp32/` is accordingly the fattest helper directory of the
four: BLE, WiFi, ESP-NOW, board classes. For comparison:
`src/helpers/nrf52/` contains only a BLE interface, and
`src/helpers/rp2040/` does not exist.

### What it costs

The highest clock speed of the four — 240 MHz — and the highest power
draw. For ESP32 the firmware has no built-in power management like nRF52
does. There is an `ESP32_CPU_FREQ` build flag in `platformio.ini`
(line 64), but it is commented out; lowering the clock is up to you.

## nRF52840 — the frugal one

### A fork of the Adafruit core

`[nrf52_base]` (lines 80-95) does not use a stock Arduino core but a fork
of its own:

```text
platform_packages =
  framework-arduinoadafruitnrf52 @
    https://github.com/meshcore-dev/Adafruit_nRF52_Arduino#d541301
```

The reason is in the comment next to it: a patch to the BLE stack that
prevents firmware lockups during rapid connect and disconnect cycles
(PR #1177 and #1295).

Two of the 34 nRF52 variants are exceptions:
`variants/heltec_mesh_solar/platformio.ini` line 4 and
`variants/mesh_pocket/platformio.ini` line 4 set
`platform_packages = framework-arduinoadafruitnrf52` without a URL, so the
plain Adafruit core, plus an older SoftDevice linker script
(`nrf52840_s140_v6.ld`). Anyone seeing BLE trouble there now knows where
to look.

Beyond that: 64 MHz, 230 KB of RAM, 792 to 796 KB of flash for the
application, and two filesystems — `InternalFS` plus an extra volume
compiled in through `EXTRAFS=1`.

### Power management: what exists and where it is missing

`docs/nrf52_power_management.md` (217 lines) describes what is possible:
waking on LPCOMP or VBUS, `SYSTEMOFF`, and recording the reason for a
shutdown. This is the only platform where the firmware genuinely does
something about power.

But read the *Supported Boards* table (lines 38-57) alongside it: of the
nineteen boards listed, **five** are marked "Implemented" — XIAO
nRF52840, RAK4631, Heltec T114, GAT562 Mesh Watch13 and SenseCAP Solar.
The other fourteen are marked "No", including popular choices such as the
T-Echo, T1000-E, Nano G2 Ultra, ProMicro, Mesh Pocket and the ThinkNode
M1/M3/M6.

"nRF52 is the frugal family" holds at chip level. Whether your particular
board actually benefits is in that table.

### The most BLE targets of all

Forty of the 199 nRF52 build targets are a BLE companion. That is two more
than the entire ESP32 family, which has three times as many targets.

## RP2040 — the simple one

### USB serial only

Four variants, 22 build targets, not one with BLE or WiFi. The branches
are there, but commented out (`examples/companion_radio/main.cpp` lines
55-66), and all four variants set `lib_ignore = BLE`. That includes the
Pico W, which does have the hardware for it.

What remains: repeater, room server, KISS modem, terminal chat and a
companion over USB. Not a single variant has a display, and there is no
`src/helpers/rp2040/` directory.

The four boards use PlatformIO's built-in definitions rather than their
own `boards/*.json`. That is why the RP2040 figures in table 1 carry an
asterisk.

## STM32WL — the integrated one

### The radio is on the die

All four STM32WL variants set `SPI_INTERFACES_COUNT=0` and
`RADIO_CLASS=CustomSTM32WLx`, and `[stm32_base]` loads the SubGhz library
from the STM32duino core (`platformio.ini` lines 115, 120). There is no
separate SX126x and no SPI bus to the radio: the LoRa transceiver sits on
the same die as the processor.

![Two block diagrams side by side. On the left an MCU with six SPI lines
running to a separate SX1262 radio chip. On the right a single STM32WLE5
block with the SubGHz radio inside it and no SPI
connection.](../../images/en/platform-families-1.svg)

### 64 KB of RAM and 224 KB of flash

From `boards/rak3172.json` and `boards/tiny_relay.json`: `stm32wle5ccu`,
48 MHz, 65536 bytes of RAM and 262144 bytes of flash. Not all of that
flash is left for the application. All four variants set:

```text
board_upload.maximum_size = 229376 ; 32kb for FS
```

So 224 KB for the app and 32 KB for the filesystem. That is three times
less RAM than nRF52 and twenty times less flash than a generously
specified ESP32. It bears directly on settings such as `MAX_CONTACTS` and
`MAX_NEIGHBOURS`, which are set per build target.

One of the four variants has a display (`wio-e5-mini`). A companion is
available over USB only.

How these four compare on compute, memory, connectivity, storage, power
and ease of flashing — and which platform suits which role — is covered in
[MeshCore Platforms](platforms.md).

## Sources

Firmware: [meshcore-dev/MeshCore](https://github.com/meshcore-dev/MeshCore),
branch `main`, commit `03b6ef4`, 28 July 2026, v1.16.0.

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/platformio.ini)
  — lines 57-65 `[esp32_base]`; 72-76 `[esp32c6_base]` with the
  "experimental" comment on line 73; 80-95 `[nrf52_base]` with the
  Adafruit fork; 98-104 `[rp2040_base]`; 108-120 `[stm32_base]` with the
  SubGhz library on lines 115 and 120
- [`variants/heltec_mesh_solar/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/heltec_mesh_solar/platformio.ini)
  line 4 and
  [`variants/mesh_pocket/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/mesh_pocket/platformio.ini)
  line 4 — the core override without a URL
- [`variants/rak3x72/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/rak3x72/platformio.ini)
  line 4 and
  [`variants/tiny_relay/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/tiny_relay/platformio.ini)
  line 4 — `board_upload.maximum_size`
- [`boards/rak3172.json`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/boards/rak3172.json),
  [`boards/tiny_relay.json`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/boards/tiny_relay.json)
  and
  [`boards/rak4631.json`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/boards/rak4631.json)
  — `mcu`, `f_cpu`, `maximum_ram_size` and `maximum_size`
- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/main.cpp)
  — lines 15-35 the filesystem per platform; 37-85 the transport layer per
  platform; 55-66 the commented-out WiFi and BLE branches for RP2040
- [`docs/nrf52_power_management.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/docs/nrf52_power_management.md)
  — 217 lines, with the *Supported Boards* table on lines 38-57

Not from the firmware repo:

- [RP2040 Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf),
  Raspberry Pi Ltd — clock speed, SRAM and flash of the RP2040
- Espressif datasheets — the specifications per ESP32 sub-SoC

Translated from Dutch by Anthropic Claude
