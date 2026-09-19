# Platform realisation

*STORAGE · BOARD CLASSES · ASYMMETRY · FOUR FAMILIES*

Four platform families, one codebase. This chapter describes where those four
diverge and how the firmware absorbs it. The sharpest dividing line is not at
the radio or the display but at the file system, and the way that choice is
made says something about how support has grown.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — `src/helpers/IdentityStore.h`,
> `src/helpers/ESP32Board.h`, `src/helpers/NRF52Board.h`,
> `src/helpers/stm32/STM32Board.h` and the board classes in `variants/`.

## Storage is the dividing line

Which file system layer a build uses is chosen with a macro. The four families
fall into two camps.

`src/helpers/IdentityStore.h` r.3-11

```cpp
#if defined(ESP32) || defined(RP2040_PLATFORM)
  #include <FS.h>
  #define FILESYSTEM  fs::FS
#elif defined(NRF52_PLATFORM) || defined(STM32_PLATFORM)
  #include <Adafruit_LittleFS.h>
  #define FILESYSTEM  Adafruit_LittleFS

  using namespace Adafruit_LittleFS_Namespace;
#endif
```

ESP32 and RP2040 get `fs::FS`, the Arduino abstraction over a file system.
nRF52 and STM32 get `Adafruit_LittleFS`, a separate implementation with a
namespace of its own. No component from `IdentityStore` upwards notices any
difference between the two file systems: everything works with `FILESYSTEM`.

## The asymmetry in the test itself

Note how the four families are recognised in that fragment. Three of them by
their own `*_PLATFORM` macro, one not:

| Family | Recognised by | Whose macro is that |
|---|---|---|
| ESP32 | `ESP32` | Arduino-ESP32 core |
| RP2040 | `RP2040_PLATFORM` | MeshCore |
| nRF52 | `NRF52_PLATFORM` | MeshCore |
| STM32 | `STM32_PLATFORM` | MeshCore |

MeshCore does define an `ESP32_PLATFORM`, but it is read nowhere in the source
tree — not in `src/`, not in `examples/`, not in `variants/`. It exists and
does nothing, because ESP32 code uses the core macro `ESP32` that is there
anyway. See [Compile-time configuration](configuration.md).

That is not a fault: it works. But it does mean that anyone adding a fifth
family finds not one pattern to follow but two.

## Board classes per family

The board contract `mesh::MainBoard` (`src/MeshCore.h` r.45) lays down what
every board must be able to do: report battery voltage, restart, sleep, report
the startup reason. Three families implement that with a shared class the
variant classes inherit from. The fourth does not.

| Family | Shared board class | Descendants in `src/` | Targets |
|---|---|---|---|
| ESP32 | `ESP32Board` | `MeshadventurerBoard`, `TBeamBoard` | 270 |
| nRF52 | `NRF52Board` | `NRF52BoardDCDC` | 199 |
| STM32 | `STM32Board` | none | 16 |
| RP2040 | **none** | four separate ones in `variants/` | 22 |

![Four columns under the contract mesh::MainBoard. Three of them have a shared
board class as an intermediate layer with the variant classes underneath; the
fourth column, RP2040, connects four variant classes directly to the contract
with no intermediate layer.](../../../images/en/platform-realisation-1.svg)

The four RP2040 board classes — `RAK11310Board`, `PicoWBoard`,
`WaveshareBoard` and `XiaoRP2040Board` — inherit from `mesh::MainBoard`
directly and therefore each write out for themselves what the other families
get from their shared parent. At 22 targets that is manageable; it is the
reason no `RP2040Board` ever appeared.

## How much code each family shares

| File | Lines |
|---|---|
| `src/helpers/ESP32Board.h` | 186 |
| `src/helpers/ESP32Board.cpp` | 47 |
| `src/helpers/NRF52Board.h` | 78 |
| `src/helpers/NRF52Board.cpp` | 366 |
| `src/helpers/stm32/STM32Board.h` | 44 |

The ratio is the opposite of what you would expect. nRF52 carries fewer
targets than ESP32 but has almost eight times as much implementation code: 366
lines against 47. That sits in power management. The nRF52 boards switch
between a DC/DC converter and a linear regulator, read the battery through an
ADC with its own reference voltage, and manage sleep themselves. `ESP32Board`
leaves most of that to the Arduino core.

STM32 makes do with 44 lines in one header and has no `.cpp` at all. There are
16 targets, all on the same SoC family, with the same radio on them — there is
little to vary.

## What else a family shares

Besides the board class, ESP32, nRF52 and STM32 each have their own directory
under `src/helpers/`. What sits in it is not a platform difference but a
capability the other families lack:

| Directory | Classes | Why only there |
|---|---|---|
| `esp32/` | `ESPNOWRadio`, `SerialBLEInterface`, `SerialWifiInterface`, `TBeamBoard` | ESP32 has BLE, WiFi *and* ESP-NOW |
| `nrf52/` | `SerialBLEInterface` | nRF52 only has BLE |
| `stm32/` | `STM32Board` | STM32 has neither |

RP2040 has no directory. An RP2040 node talks to the phone app over USB
serial, not over BLE or WiFi.

## The clock as a counter-example

Not every abstraction splits per family. The clock contract `mesh::RTCClock`
(`src/MeshCore.h` r.80) is implemented in three ways, and those three cut
straight across the families:

| Implementation | Location | When |
|---|---|---|
| `ESP32RTCClock` | `src/helpers/ESP32Board.h` r.160 | ESP32 with an internal RTC |
| `AutoDiscoverRTCClock` | `src/helpers/AutoDiscoverRTCClock.h` r.7 | Board with an RTC chip on I²C |
| `VolatileRTCClock` | `src/helpers/ArduinoHelpers.h` r.6 | Board without an RTC |

`AutoDiscoverRTCClock` searches the I²C bus at startup for a known RTC chip
and falls back to a volatile clock if it finds nothing. That is a hardware
difference with nothing to do with the platform family: the same ESP32 family
contains boards with and without an RTC chip.

## Sources

- [MeshCore `03b6ef4` — `src/helpers/IdentityStore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/IdentityStore.h)
- [MeshCore `03b6ef4` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore `03b6ef4` — `src/helpers/ESP32Board.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ESP32Board.h)
- [MeshCore `03b6ef4` — `src/helpers/NRF52Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/NRF52Board.cpp)
- [MeshCore `03b6ef4` — `src/helpers/stm32/STM32Board.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/stm32/STM32Board.h)

Translated from Dutch by Anthropic Claude
