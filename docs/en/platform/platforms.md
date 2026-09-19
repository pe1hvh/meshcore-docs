# MeshCore Platforms

*COMPARING · CHOOSING · WHAT THE CHIP DECIDES*

MeshCore runs on four platform families. The same source code, the same
protocol, the same radio — and yet one node can do things another cannot.
This chapter shows why the platform matters, how the four compare, what
you can buy today and how to choose. What each family puts in the chip is
covered in [The Four Platform Families](platform-families.md).

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.17.1 (`FIRMWARE_BUILD_DATE "14 Aug 2026"`), commit
> `d929643`, 14 August 2026 — `platformio.ini`, `variants/*/platformio.ini`
> (87 directories, 584 build targets), `boards/*.json` (44 definitions),
> `examples/companion_radio/main.cpp`, `src/helpers/IdentityStore.h` and
> `src/Utils.cpp`. Every count was also run against the previous pin
> `03b6ef4`; the difference is listed in
> [Changes in v1.17.1](../project/release-v1-17-1.md). The device list comes
> from `config.json` in
> [meshcore-dev/flasher.meshcore.io](https://github.com/meshcore-dev/flasher.meshcore.io),
> commit `b84f889`, 9 September 2026. To reproduce:
> [`tools/platform-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/platform-overview.py).

## Why the platform matters

Take the sharpest example: a companion that talks to your phone over
Bluetooth. It exists as a build target on ESP32 and on nRF52840, and on
neither of the other two families. Not because the hardware cannot do it —
the Raspberry Pi Pico W has Bluetooth on board — but because the firmware
has no implementation for it. In `examples/companion_radio/main.cpp`
lines 55-66 the WiFi and BLE branches for RP2040 are commented out, and
every RP2040 variant sets `lib_ignore = BLE`.

Same protocol, same radio, different behaviour. The platform decides which
transports, storage, displays and update methods are available.

Note the wording. The firmware does not speak of microcontrollers but of
**platforms**: the four build targets are named `ESP32_PLATFORM`,
`NRF52_PLATFORM`, `RP2040_PLATFORM` and `STM32_PLATFORM`
(`platformio.ini` lines 63, 90, 104, 113). And three of the four are
strictly speaking not a microcontroller but a **SoC**: a chip with the
radio inside it. Only the RP2040 is a bare microcontroller.

So "MeshCore supports four microcontrollers" is a double simplification.
There are four platform bases in `platformio.ini`, covering at least seven
different SoCs and two processor architectures.

What exactly distinguishes a SoC from an MCU — and why every SoC contains an
MCU but not the other way round — is covered in
[The Hardware of a Node](../hardware/introduction.md).

## The four families at a glance

| Family | SoCs | Core | Clock | RAM | Flash for the app | Radio | Variants | Build targets |
|---|---|---|---|---|---|---|---|---|
| ESP32 | ESP32, S3, C3, C6 | Xtensa LX6/LX7 + RISC-V | 160–240 MHz | 320 KB, up to 8 MB with PSRAM | 4–16 MB | external, over SPI | 43 | 332 |
| nRF52 | nRF52840 | Cortex-M4F | 64 MHz | 230 KB | 792–796 KB | external, over SPI | 36 | 214 |
| RP2040 | RP2040 | 2× Cortex-M0+ | 133 MHz \* | 264 KB \* | 2 MB \* | external, over SPI | 4 | 22 |
| STM32WL | STM32WLE5CCU | Cortex-M4 | 48 MHz | 64 KB | 224 KB | on the die (SubGHz) | 4 | 16 |

> [!NOTE]
> **\* These three RP2040 figures are not in the MeshCore repo.** The four
> RP2040 boards use PlatformIO's built-in board definitions; there is no
> `boards/*.json` for them. The source for clock speed, RAM and flash is
> the [RP2040 Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)
> by Raspberry Pi Ltd. Every other figure in this table comes from
> `boards/*.json` and `variants/*/platformio.ini` in the firmware repo.

![Four columns side by side showing per platform family the SoC, core,
clock, memory and a plus or minus sign for BLE, WiFi, USB serial, display,
OTA and ESP-NOW; at the bottom the number of devices in the web
flasher.](../../images/en/platforms-1.svg)

What each family actually brings — the SoCs under the heading, the cores,
the power management and what the chip demands in memory and energy — is
worked out family by family in
[The Four Platform Families](platform-families.md).

## Comparison on six axes

| Axis | ESP32 | nRF52840 | RP2040 | STM32WL |
|---|---|---|---|---|
| Compute | highest, 160–240 MHz, S3 with vector instructions | 64 MHz with FPU | 133 MHz, two cores, no FPU | 48 MHz, the lowest |
| Memory | generous; PSRAM possible | ample for every role | ample for every role | tight: 64 KB RAM, 224 KB app flash |
| Connectivity | BLE, WiFi, ESP-NOW, USB | BLE and USB | USB only | USB only |
| Storage | SPIFFS on internal flash | `InternalFS` plus `EXTRAFS` | LittleFS | LittleFS port in `arch/stm32/` |
| Power | highest; no power management in the firmware | lowest; the only one actively supported, but on 5 of 19 boards | no power management in the firmware | frugal by nature; no power management in the firmware |
| Ease of flashing | web flasher over USB | drag a `.uf2`, or OTA over Bluetooth | drag a `.uf2` | `.hex` with ST-Link or DFU |

> [!NOTE]
> **No current figures.** This chapter contains no numbers in mA. They do
> not appear anywhere in the firmware repo, and datasheet figures say
> little about a node with a radio, display and GPS attached. For the one
> platform where the firmware really does something about it,
> `docs/nrf52_power_management.md` is the place to look.

## Which roles run on which platform

A hard count of the `[env:]` blocks in `variants/*/platformio.ini`. Each
number is a count of build targets, not of boards — one board usually
yields five to ten targets.

| Role | ESP32 | nRF52 | RP2040 | STM32WL |
|---|---|---|---|---|
| companion BLE | 46 | 42 | 0 | 0 |
| companion WiFi | 25 | 0 | 0 | 0 |
| companion USB | 41 | 37 | 4 | 4 |
| companion serial | 3 | 0 | 0 | 0 |
| companion Ethernet | 1 | 1 | 0 | 0 |
| repeater | 95 | 45 | 6 | 5 |
| room server | 42 | 38 | 4 | **0** |
| sensor | 14 | 6 | **0** | 3 |
| KISS modem | 43 | 40 | 4 | 4 |
| terminal chat | 22 | 5 | 4 | 0 |
| **total** | **332** | **214** | **22** | **16** |

Two gaps stand out. STM32WL has no room server at all, and RP2040 has no
sensor build. That is not a limitation of the chip but a choice in the
variants: nobody has created them.

The *companion Ethernet* row is new in v1.17.1 and holds two targets:
`RAK_4631_companion_radio_ethernet` and
`ThinkNode_M7_companion_radio_ethernet`. There is also one repeater and one
room server over Ethernet, counted in their own rows. What you can do with
it is described in [Ethernet](../cli/ethernet.md).

Of the 332 ESP32 targets, sixteen come from the three C6 variants: five
repeater, five companion BLE, three KISS modem, two room server and one
companion USB.

## What you can buy and flash today

The firmware builds for four families. The
[web flasher](https://flasher.meshcore.io) — the route most people take —
offers two. The flasher's `config.json` holds 66 entries for sixty-five
devices; the LilyGo T-Lora Pager appears twice, once per firmware project:

| Family | Devices in the flasher | Share | Variants in the repo |
|---|---|---|---|
| ESP32 | 35 | 54 % | 43 |
| nRF52840 | 29 | 45 % | 36 |
| RP2040 | 1, and not flashable through the web flasher | 2 % | 4 |
| STM32WL | 0 | 0 % | 4 |

Nine of those sixty-five devices cannot run MeshCore at all: the flasher
offers only Ripple firmware for them. Which ones is listed in
[Node matrix](node-matrix.md).

The single RP2040 device in the list, the Pico with a WaveShare SX1262
module, gets no platform icon but a generic glyph. The flasher's own
configuration gives the reason: `"type": "noflash"`. You get a link to the
`.uf2` file and copy it across yourself.

For STM32WL there is nothing at all. Anyone who wants such a node compiles
it themselves and flashes it with ST-Link or DFU. Within MeshCore,
STM32WL is not a consumer platform but a builder's platform.

Within ESP32 the S3 dominates: 28 of the 35 devices. Alongside it five with
the classic ESP32 (Heltec v2, LilyGo LoRa32 v2.1_1.6 and the three T-Beams)
and one with a C3 (Seeed Xiao C3); the sub-SoC of the T-Deck Pro v1.1 is
unknown. The previous pin named four classic ESP32s where there were five —
the T-Beam 1W was missing from that list. Of the C6, the sub-SoC
carrying the "experimental" label, not a single device appears in the
list.

> [!NOTE]
> **The flasher list is not a copy of `variants/`.** Seven ESP32-S3
> devices in the list — the LilyGo T-Deck Max, T-Deck Pro, T-Display Pro,
> T-Lora Pager, T-Watch S3 Plus, T-Watch Ultra and T5 E-Paper S3 Pro —
> have no variant in this repo. They run the closed-source Ripple GUI or
> MeshOS firmware. Conversely, the four STM32WL variants, three of the
> four RP2040 variants, all three C6 variants and generic targets such as
> `generic-e22` and `meshtiny` do not appear in the flasher.

## How MeshCore absorbs the differences

### One API, four cores

`framework = arduino` appears exactly once in the entire repo:
`platformio.ini` line 17, in `[arduino_base]`. All four platform bases
extend it, and none of the 87 variants overrides it.

Even so, these are four different Arduino cores: Arduino-ESP32 on ESP-IDF,
the Adafruit nRF52 core on the SoftDevice, the earlephilhower arduino-pico,
and STM32duino on the STM32 HAL. The same API, four implementations —
hence the `#ifdef` chains throughout the helper layer.

How sharp that can get is visible in
`examples/companion_radio/main.cpp` lines 5-6. There sits a hand-written
`_atoi()` with a note that the standard C function is broken on some
platforms.

A tidy example of the opposite movement is `src/helpers/IdentityStore.h`
lines 3-11, where one macro covers four cases:

```text
#if defined(ESP32) || defined(RP2040_PLATFORM)
  #define FILESYSTEM  fs::FS
#elif defined(NRF52_PLATFORM) || defined(STM32_PLATFORM)
  #define FILESYSTEM  Adafruit_LittleFS
#endif
```

Everything above that line — storing identities, keeping contacts — no
longer needs to know which platform it is running on.

### The core is not Arduino-dependent

The Arduino dependency lives in `src/helpers/` and `examples/`, not in the
protocol core. In `src/Utils.cpp` lines 5-7 the `#include <Arduino.h>`
sits behind `#ifdef ARDUINO`, and `src/MeshCore.h` lines 25 and 34 use
`ARDUINO` only to switch debug output on or off.

The proof is at the bottom of `platformio.ini`: `[env:native]`
(lines 158-168) builds against googletest, with `platform = native`, mocks
from `test/mocks/` and not a single line of Arduino. That is why a Zephyr
port of MeshCore can exist that speaks exactly the same protocol.

### Four flash artefacts

| Platform | Build script | Result | How it reaches the node |
|---|---|---|---|
| ESP32 | `merge-bin.py` | a single `.bin` | esptool or the web flasher |
| nRF52 | `create-uf2.py` | `.uf2` | drag onto the USB drive, or OTA over Bluetooth |
| RP2040 | `upload_protocol = picotool` | `.uf2` | drag onto the UF2 bootloader |
| STM32 | `arch/stm32/build_hex.py` | `.hex` via `objcopy -O ihex` | ST-Link or DFU |

That is also the explanation for the flasher table above. Only ESP32 and
nRF52 have an artefact a web page can write straight to the device.

## Choosing

![Decision tree starting with the question whether the node needs to talk
to a phone and arriving, via battery life and the need for WiFi, OTA or
ESP-NOW, at nRF52840, ESP32 or STM32WL.](../../images/en/platforms-3.svg)

In words:

- **Need to pair with a phone?** Then ESP32 or nRF52840; the other two
  have no BLE companion.
- **Running on a battery or solar panel?** nRF52840 — but first check
  whether your board is marked "Implemented" in the table in
  `docs/nrf52_power_management.md`.
- **Need WiFi, OTA or ESP-NOW?** ESP32 only.
- **A small, frugal repeater without a phone, and you build it yourself?**
  STM32WL. Count on 64 KB of RAM and on flashing with ST-Link or DFU.
- **RP2040** is the choice for someone who already has a Pico lying around
  and wants a repeater or USB companion. No BLE, no WiFi, no display.

Which specific board fits is covered in
[Hardware Overview](../usage/hardware.md).

## Sources

Firmware: [meshcore-dev/MeshCore](https://github.com/meshcore-dev/MeshCore),
tag `companion-v1.17.1`, commit `d929643`, 14 August 2026, v1.17.1.

Device list: `config.json` from
[meshcore-dev/flasher.meshcore.io](https://github.com/meshcore-dev/flasher.meshcore.io),
commit `b84f889`, 9 September 2026.

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/platformio.ini)
  — lines 16-53 `[arduino_base]` with `framework = arduino` on line 17;
  67-70 `[esp32_ota]`; 158-168 `[env:native]`
- [`variants/`](https://github.com/meshcore-dev/MeshCore/tree/d92964352441e53b93e8667b802e04f6e072b39e/variants)
  — 87 directories holding 584 `[env:]` blocks between them
- [`boards/`](https://github.com/meshcore-dev/MeshCore/tree/d92964352441e53b93e8667b802e04f6e072b39e/boards)
  — 44 board definitions with `mcu`, `f_cpu`, `maximum_ram_size` and
  `maximum_size`. The previous pin said 41; that was the number of files in
  the directory, four linker scripts included, not the number of `.json`
  definitions (37).
- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/companion_radio/main.cpp)
  — lines 5-6 the hand-written `_atoi()`
- [`src/helpers/IdentityStore.h`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/IdentityStore.h)
  — lines 3-11, the `FILESYSTEM` abstraction
- [`src/Utils.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/Utils.cpp)
  — lines 5-7, `#ifdef ARDUINO`
- `merge-bin.py`, `create-uf2.py` and `arch/stm32/build_hex.py` — the
  three build scripts that produce the flash artefacts

Device list: saved page of the
[MeshCore web flasher](https://flasher.meshcore.io), 27 July 2026,
sixty devices.

Not from the firmware repo:

- [RP2040 Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf),
  Raspberry Pi Ltd — clock speed, SRAM and flash of the RP2040

To recompute: [`tools/platform-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/platform-overview.py)
generates tables 1, 3 and 4 from a clone of the firmware repo and a saved
flasher page.

Translated from Dutch by Anthropic Claude
