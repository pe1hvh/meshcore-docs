# Compile-time configuration

*330 MACROS · THREE OWNERS · 55 UNREAD · MEASURING METHOD*

The eighty-eight `platformio.ini` files together define 330 unique `-D`
macros. This chapter sorts them by owner — library, Arduino core or MeshCore
itself — and then goes into the most important finding: of the 307 MeshCore
macros, 60 are defined and read nowhere.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.17.1, commit `d929643`, 14 August 2026 — the root `platformio.ini`, all
> 87 `variants/*/platformio.ini` and the complete source tree under `src/`,
> `examples/` and `variants/`.

## Three owners

A macro belongs to whoever reads it, not to whoever defines it. All 330 are
set in MeshCore's own ini files, but they end up with three different parties.

| Group | Macros | Read by |
|---|---|---|
| 1 — library | 17 | An external library |
| 2 — framework | 11 | An Arduino core |
| 3 — MeshCore | 302 | MeshCore's own source files |

![Three stacks. On the left seventeen macros with an arrow to a block of
external libraries, in the middle eleven with an arrow to a block of Arduino
cores, on the right three hundred and two with an arrow to the MeshCore
source tree. From that third stack a portion of fifty-five runs to an empty
field with no reader.](../../../images/en/configuration-1.svg)

Group 1 is written out in
[Library configuration](../../libraries/library-configuration.md), where it
belongs: those macros say something about the libraries, not about MeshCore.

Sixteen macros occur only on commented-out `-D` lines and are therefore
active in no build. They are not counted in the 330:

`ARDUHAL_LOG_LEVEL`, `BRIDGE_DEBUG`, `DEBUG_RP2040_CORE`,
`DEBUG_RP2040_PORT`, `DEBUG_RP2040_SPI`, `DEBUG_RP2040_WIRE`,
`ESPNOW_DEBUG_LOGGING`, `FORMAT_FS`, `GPS_NMEA_DEBUG`,
`HW_SPI1_DEVICE`, `MESH_PACKET_LOGGING`, `PICOW`,
`PIN_VIBRATION`, `RADIOLIB_DEBUG_BASIC`, `RADIOLIB_DEBUG_SPI`
and `STM32WL_TCXO_VOLTAGE`.

On `03b6ef4` there were fourteen; `GPS_NMEA_DEBUG` and `MESH_PACKET_LOGGING`
were added in v1.17.1. The list can be reproduced with
`tools/config-flags.py --commented`.

> [!NOTE]
> **Departure from the previous edition.** This said there were two:
> `RADIOLIB_DEBUG_BASIC` and `RADIOLIB_DEBUG_SPI`. That held only for the
> library macros of group 1, not for the whole.

## Group 2 — framework (11)

| Macro | Consumer |
|---|---|
| `ARDUINO_LOOP_STACK_SIZE` | Arduino-ESP32 core |
| `ARDUINO_RAKWIRELESS_RAK11300` | arduino-pico core |
| `ARDUINO_USB_CDC_ON_BOOT` | Arduino-ESP32 core |
| `ARDUINO_USB_MODE` | Arduino-ESP32 core |
| `ARDUINO_heltec_wifi_lora_32_V3` | Arduino-ESP32 core |
| `BOARD_HAS_PSRAM` | Arduino-ESP32 core |
| `CORE_DEBUG_LEVEL` | Arduino-ESP32 core |
| `ENABLE_HWSERIAL2` | Arduino-ESP32 core |
| `NDEBUG` | C standard library |
| `PIN_SERIAL_RX` | Adafruit nRF52 core |
| `PIN_SERIAL_TX` | Adafruit nRF52 core |

Eight of the eleven are ESP32 macros. That is no accident: the Arduino-ESP32
core lets more be set through build flags than the other three cores do,
particularly around USB and the serial-over-USB behaviour at startup.

> [!NOTE]
> **Departure from the previous edition.** This group held six macros. The
> last five — `BOARD_HAS_PSRAM`, `ENABLE_HWSERIAL2`, `NDEBUG`,
> `PIN_SERIAL_RX` and `PIN_SERIAL_TX` — sat in group 3 while a core or the
> standard library reads them. They have no recognisable name prefix, so the
> ownership table `NAMESPACES` in `tools/config-flags.py` did not catch them.
> They are now separate entries in it. Group 3 thereby falls from 307 to 302
> and the number of unread macros from 60 to 55.

## Group 3 — MeshCore (302)

Of the 307 MeshCore macros, **247** are read somewhere in the source tree and
**60** nowhere.

The 247 by the place where they first occur:

| Where | Macros |
|---|---|
| `variants/` | 63 |
| `src/helpers/ui/` | 47 |
| `src/helpers/` (core) | 38 |
| `examples/` | 36 |
| `src/helpers/sensors/` | 27 |
| `src/helpers/esp32,nrf52,stm32/` | 21 |
| `src/helpers/radiolib/` | 11 |
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
| `WITH_RS232_BRIDGE` | `src/helpers/CommonCLI.cpp` r.737 |
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

## The 55 that are read nowhere

Eighteen percent of the MeshCore macros are defined and never tested. They
fall into three groups.

### Board markers (42)

`EBYTE_EORA_S3`, `GENERIC_E22`, `HELTEC_HT_CT62`, `HELTEC_LORA_V2`,
`HELTEC_LORA_V4`, `HELTEC_MESH_POCKET`, `HELTEC_RC32`, `HELTEC_T1`,
`HELTEC_T114`, `HELTEC_TOWER_V2`, `HELTEC_V4_R8`, `HELTEC_WIRELESS_PAPER`,
`KEEPTEEN_LT1`, `LILYGO_T3S3`, `LILYGO_TETH_ELITE`, `LILYGO_TLORA`,
`LILYGO_T_ETH_ELITE_ESP32S3`, `MESHADVENTURER`, `MESHNOLOGY_W12`, `MESHTINY`,
`MESH_TRACKER_X1`, `NIBBLE_SCREEN_CONNECT`, `NIBBLE_ZERO_CONNECT`, `PROMICRO`,
`RAK_11310`, `RAK_3112`, `RAK_3401`, `RAK_3X72`, `SEEED_XIAO_S3`,
`STATION_G2`, `STATION_G3_ESP32`, `T1000_E`, `TBEAM_1W`, `THINKNODE_M2`,
`THINKNODE_M3`, `THINKNODE_M5`, `THINKNODE_M7`, `Vision_Master_E213`,
`Vision_Master_E290`, `WIO_TRACKER_L1`, `WIRELESS_PAPER`, `me25ls01`.

Every variant file defines its own name as a macro. Nothing tests for it,
because the variant already gets its own `-I` path and therefore sees its own
headers. They are documentation in the shape of a macro: you read in the
`platformio.ini` which board it is, and the compiler does nothing with it.

### Platform marker (1)

`ESP32_PLATFORM`. The other three platform macros — `NRF52_PLATFORM`,
`RP2040_PLATFORM`, `STM32_PLATFORM` — *are* read; this one is not, because
ESP32 code uses the core macro `ESP32` that is there anyway. See
[Platform realisation](platform-realisation.md).

### Other (12)

`DISABLE_DIAGNOSTIC_OUTPUT`, `DISPLAY_LINES`, `HAS_NEOPIXEL`, `HAS_TOUCH`,
`IO_EXPANDER_IRQ`, `LINE_LENGTH`, `NEOPIXEL_COUNT`, `NEOPIXEL_DATA`,
`NEOPIXEL_TYPE`, `PIN_RESET`, `UI_GPS_PAGE`,
`WITH_ESPNOW_BRIDGE_SECRET`.

> [!NOTE]
> Up to and including `03b6ef4` this list held seventeen macros, among them
> five that do have a reader. Those five are now in group 2; see the note
> there. `tools/config-flags.py --misfiled` shows which they were.

These twelve, among them `HAS_NEOPIXEL`, `NEOPIXEL_COUNT` and
`UI_GPS_PAGE`, point at functionality that does not exist in this commit. The
build flags are there, the code reacting to them is not — or no longer.

## What this means

A macro that is read nowhere is not dangerous, but it is misleading. Anyone
seeing `HAS_TOUCH` in a `platformio.ini` may assume something happens with
touch input. It does not.

For anyone adding a board that matters in practice: copying the board marker
has no effect, and switching on `UI_GPS_PAGE` yields no GPS page. What *does*
work is visible in the 247 macros that do have a reader.

## Recomputing

```bash
python3 tools/config-flags.py /path/to/MeshCore
python3 tools/config-flags.py /path/to/MeshCore --owners
python3 tools/config-flags.py /path/to/MeshCore --consumption
python3 tools/config-flags.py /path/to/MeshCore --commented
python3 tools/config-flags.py /path/to/MeshCore --misfiled
```

`--owners` writes groups 2 and 3 as a markdown table; `--consumption` gives
per MeshCore macro the first file and line number where it occurs, with an
explicit category *read nowhere*. `--commented` lists the macros that occur
only on commented-out lines, `--misfiled` the five that sat in the wrong group
up to and including v1.16.0. The script skips lines behind a `;`, so that
commented-out macros do not inflate the configuration surface.

## Sources

- [MeshCore `d929643` — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/d929643/platformio.ini)
- [MeshCore `d929643` — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/CommonCLI.cpp)
- [MeshCore `d929643` — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/examples/simple_repeater/MyMesh.cpp)
- [MeshCore `d929643` — `src/helpers/IdentityStore.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/IdentityStore.h)

Translated from Dutch by Anthropic Claude
