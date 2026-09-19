# RTClib

*TIMESTAMP · DS3231 · PCF8563 · ADVERT*

Every packet MeshCore sends carries a timestamp, and every advert has one.
RTClib supplies the clock those timestamps come from — whether or not the node
has a real RTC chip on board.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini`, `src/helpers/AutoDiscoverRTCClock.cpp`,
> `src/helpers/RTC_RX8130CE.h` and the `examples/` directory.

## What it does

RTClib by Adafruit talks to real-time clock chips over I²C. It knows the
DS3231, DS1307 and PCF8563 among others, each with its own class, and supplies
the `DateTime` type for calculating with moments in time — to and from unix
time, with calendar conversion. The repository is at
[github.com/adafruit/RTClib](https://github.com/adafruit/RTClib).

## How MeshCore pulls it in

`platformio.ini` r.24

```text
  adafruit/RTClib @ ^2.1.3
```

In `[arduino_base]`, so in all 507 build targets. RTClib is additionally
declared separately in seven variant files.

## How MeshCore uses it

The RTClib classes come together in `AutoDiscoverRTCClock`, which scans the
I²C bus for a clock chip at start-up:

`src/helpers/AutoDiscoverRTCClock.cpp` r.6-16

```cpp
static RTC_DS3231 rtc_3231;
static bool ds3231_success = false;

static Melopero_RV3028 rtc_rv3028;
static bool rv3028_success = false;

static RTC_PCF8563 rtc_8563;
static bool rtc_8563_success = false;

static RTC_RX8130CE rtc_8130;
static bool rtc_8130_success = false;
```

Two of those four classes come from RTClib (`RTC_DS3231`, `RTC_PCF8563`), one
from another library (see [`rv3028.md`](rv3028.md)) and one from MeshCore
itself. The `DateTime` type from RTClib is also used by the GPS time
synchronisation in `src/helpers/sensors/MicroNMEALocationProvider.h` r.5.

The example sketches include the library directly:

`examples/simple_repeater/MyMesh.h` r.3-6

```cpp
#include <Arduino.h>
#include <Mesh.h>
#include <RTClib.h>
#include <target.h>
```

In total, eleven of the 590 source files name `RTClib`: six under `src/` and
five in `examples/` — the three `MyMesh.h` files of `simple_repeater`,
`simple_room_server` and `companion_radio`, plus `SensorMesh.h` of
`simple_sensor` and `main.cpp` of `simple_secure_chat`.

## What it means for a node

A node without an RTC chip works fine, but only keeps time while it is
powered. After a restart the counter starts again, unless the time is set from
outside — through the CLI, through a companion app or through GPS. A node
*with* one of the four supported clock chips remembers the time across a
restart, and that shows in the timestamps on received messages and in how
adverts play out.

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/AutoDiscoverRTCClock.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/AutoDiscoverRTCClock.cpp)
- [`examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [`src/helpers/sensors/MicroNMEALocationProvider.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/MicroNMEALocationProvider.h)
- [adafruit/RTClib](https://github.com/adafruit/RTClib)

Translated from Dutch by Anthropic Claude
