# Compile-time configuration

*277 MACROS · THREE OWNERS · 53 UNREAD · MEASURING METHOD*

The eighty `platformio.ini` files together define 277 unique `-D` macros. This
chapter sorts them by owner — library, Arduino core or MeshCore itself — and
then goes into the most important finding: of the 254 MeshCore macros, 53 are
defined and read nowhere.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — the root `platformio.ini`, all 79
> `variants/*/platformio.ini` and the complete source tree under `src/`,
> `examples/` and `variants/`.

## Three owners

A macro belongs to whoever reads it, not to whoever defines it. All 277 are
set in MeshCore's own ini files, but they end up with three different parties.

| Group | Macros | Read by |
|---|---|---|
| 1 — library | 17 | An external library |
| 2 — framework | 6 | An Arduino core |
| 3 — MeshCore | 254 | MeshCore's own source files |

![Three stacks. On the left seventeen macros with an arrow to a block of
external libraries, in the middle six with an arrow to a block of Arduino
cores, on the right two hundred and fifty-four with an arrow to the MeshCore
source tree. From that third stack a portion of fifty-three runs to an empty
field with no reader.](../../../images/en/configuration-1.svg)

Group 1 is written out in
[Library configuration](../../libraries/library-configuration.md), where it
belongs: those macros say something about the libraries, not about MeshCore.

Two macros sit commented out and are therefore active in no build:
`RADIOLIB_DEBUG_BASIC` and `RADIOLIB_DEBUG_SPI`. They are not counted in the
277.

## Group 2 — framework (6)

| Macro | Consumer |
|---|---|
| `ARDUINO_LOOP_STACK_SIZE` | Arduino-ESP32 core |
| `ARDUINO_RAKWIRELESS_RAK11300` | arduino-pico core |
| `ARDUINO_USB_CDC_ON_BOOT` | Arduino-ESP32 core |
| `ARDUINO_USB_MODE` | Arduino-ESP32 core |
| `ARDUINO_heltec_wifi_lora_32_V3` | Arduino-ESP32 core |
| `CORE_DEBUG_LEVEL` | Arduino-ESP32 core |

Five of the six are ESP32 macros. That is no accident: the Arduino-ESP32 core
lets more be set through build flags than the other three cores do,
particularly around USB and the serial-over-USB behaviour at startup.

## Group 3 — MeshCore (254)

Of the 254 MeshCore macros, **201** are read somewhere in the source tree and
**53** nowhere.

The 201 by the place where they first occur:

| Where | Macros |
|---|---|
| `variants/` | 48 |
| `src/helpers/ui/` | 35 |
| `examples/` | 29 |
| `src/helpers/` (core) | 28 |
| `src/helpers/sensors/` | 28 |
| `src/helpers/esp32,nrf52,stm32/` | 21 |
| `src/helpers/radiolib/` | 8 |
| `src/` | 2 |
| `src/helpers/bridges/` | 2 |

Two macros in `src/` — that is the entire core. Everything steerable with a
build flag sits in the layers around it. The core itself is not configurable
and compiles the same way in every build.

A few examples of places where such a macro is read. These are representative
reading places, not necessarily the first occurrence that the table above
counts:

| Macro | Read in |
|---|---|
| `ADVERT_NAME` | `examples/simple_repeater/MyMesh.cpp` r.22 |
| `MAX_NEIGHBOURS` | `examples/simple_repeater/MyMesh.cpp` r.64 |
| `DISPLAY_CLASS` | `examples/simple_repeater/main.cpp` r.6 |
| `WITH_RS232_BRIDGE` | `src/helpers/CommonCLI.cpp` r.720 |
| `P_LORA_NSS` | `src/helpers/MeshadventurerBoard.h` r.7 |

> [!NOTE]
> **Measuring method.** The distribution table counts per macro the **first
> occurrence** of the name in the source tree, traversed in the order `src/` →
> `examples/` → `variants/` and alphabetically within each directory. That
> order belongs with the figure: a different traversal order shifts the table
> by up to 22 macros.
>
> First occurrence is not the same as first *read*. `P_LORA_NSS` in
> `MeshadventurerBoard.h` r.7 is a `#define`, so a redefinition and not a
> test. The macros in the example table above were picked because they are
> illustrative, not because they are the first occurrence.

## The 53 that are read nowhere

Twenty-one percent of the MeshCore macros are defined and never tested. They
fall into three groups.

### Board markers (35)

`EBYTE_EORA_S3`, `GENERIC_E22`, `HELTEC_HT_CT62`, `HELTEC_LORA_V2`,
`HELTEC_LORA_V3`, `HELTEC_LORA_V4`, `HELTEC_MESH_POCKET`, `HELTEC_T114`,
`HELTEC_WIRELESS_PAPER`, `KEEPTEEN_LT1`, `LILYGO_T3S3`, `LILYGO_TETH_ELITE`,
`LILYGO_TLORA`, `LILYGO_T_ETH_ELITE_ESP32S3`, `MESHADVENTURER`, `MESHTINY`,
`NIBBLE_SCREEN_CONNECT`, `PROMICRO`, `RAK_11310`, `RAK_3112`, `RAK_3401`,
`RAK_3X72`, `SEEED_XIAO_S3`, `STATION_G2`, `STATION_G3_ESP32`, `T1000_E`,
`TBEAM_1W`, `THINKNODE_M2`, `THINKNODE_M3`, `THINKNODE_M5`,
`Vision_Master_E213`, `Vision_Master_E290`, `WIO_TRACKER_L1`,
`WIRELESS_PAPER`, `me25ls01`.

Every variant file defines its own name as a macro. Nothing tests for it,
because the variant already gets its own `-I` path and therefore sees its own
headers. They are documentation in the shape of a macro: you read in the
`platformio.ini` which board it is, and the compiler does nothing with it.

### Platform marker (1)

`ESP32_PLATFORM`. The other three platform macros — `NRF52_PLATFORM`,
`RP2040_PLATFORM`, `STM32_PLATFORM` — *are* read; this one is not, because
ESP32 code uses the core macro `ESP32` that is there anyway. See
[Platform realisation](platform-realisation.md).

### Other (17)

`BOARD_HAS_PSRAM`, `DISABLE_DIAGNOSTIC_OUTPUT`, `DISPLAY_LINES`,
`ENABLE_HWSERIAL2`, `HAS_NEOPIXEL`, `HAS_TOUCH`, `IO_EXPANDER_IRQ`,
`LINE_LENGTH`, `NDEBUG`, `NEOPIXEL_COUNT`, `NEOPIXEL_DATA`, `NEOPIXEL_TYPE`,
`PIN_SERIAL_RX`, `PIN_SERIAL_TX`, `P_LORA_TX_LED_ON`, `UI_GPS_PAGE`,
`WITH_ESPNOW_BRIDGE_SECRET`.

> [!IMPORTANT]
> These seventeen are not all dead. `NDEBUG` is standard C and is read by the
> standard library; `BOARD_HAS_PSRAM`, `PIN_SERIAL_RX`, `PIN_SERIAL_TX` and
> `ENABLE_HWSERIAL2` are read by an Arduino core. Those five therefore belong
> in group 2 and not in group 3. The ownership table `NAMESPACES` in
> `tools/config-flags.py` classifies them wrongly, because it works on name
> prefix and these five have no recognisable prefix. The script can show them
> separately as of this delivery, but the classification has not been silently
> corrected: that calls for a separate decision.

The remaining twelve, among them `HAS_NEOPIXEL`, `NEOPIXEL_COUNT` and
`UI_GPS_PAGE`, point at functionality that does not exist in this commit. The
build flags are there, the code reacting to them is not — or no longer.

## What this means

A macro that is read nowhere is not dangerous, but it is misleading. Anyone
seeing `HAS_TOUCH` in a `platformio.ini` may assume something happens with
touch input. It does not.

For anyone adding a board that matters in practice: copying the board marker
has no effect, and switching on `UI_GPS_PAGE` yields no GPS page. What *does*
work is visible in the 201 macros that do have a reader.

## Recomputing

```bash
python3 tools/config-flags.py /path/to/MeshCore
python3 tools/config-flags.py /path/to/MeshCore --owners
python3 tools/config-flags.py /path/to/MeshCore --consumption
```

`--owners` writes groups 2 and 3 as a markdown table; `--consumption` gives
per MeshCore macro the first file and line number where it occurs, with an
explicit category *read nowhere*. The script skips lines behind a `;`, so that
commented-out macros do not inflate the configuration surface.

## Sources

- [MeshCore `03b6ef4` — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [MeshCore `03b6ef4` — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore `03b6ef4` — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore `03b6ef4` — `src/helpers/IdentityStore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/IdentityStore.h)

Translated from Dutch by Anthropic Claude
