# GPS libraries

*NMEA · UBX · LOCATIONPROVIDER · TIME SYNCHRONISATION*

For positioning, MeshCore uses two libraries that serve the same purpose but
have nothing in common. One parses lines of text that virtually every GPS
receiver emits; the other speaks a binary protocol with one specific
manufacturer.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini`, `src/helpers/sensors/MicroNMEALocationProvider.h` and
> `src/helpers/sensors/EnvironmentSensorManager.cpp`.

## How MeshCore calls this group

Both libraries sit behind the same abstraction, `LocationProvider`. The
`SensorManager` supplies one on request:

`src/helpers/SensorManager.h` r.25

```cpp
  virtual LocationProvider* getLocationProvider() { return NULL; }
```

Whoever wants a position — for the location in an advert, for telemetry or for
setting the clock — asks the provider for it and does not have to know which
receiver sits underneath.

## stevemarple/MicroNMEA

NMEA 0183 is the protocol virtually every GPS receiver emits over a serial
line: lines of text starting with `$GP` or `$GN`, carrying position, time,
speed and the number of visible satellites, closed off with a checksum.
MicroNMEA parses those lines character by character, without allocating
buffers and without dynamic memory — written for microcontrollers where that
matters.

MeshCore uses it in `MicroNMEALocationProvider`:

`src/helpers/sensors/MicroNMEALocationProvider.h` r.3-6

```cpp
#include "LocationProvider.h"
#include <MicroNMEA.h>
#include <RTClib.h>
#include <helpers/RefCountedDigitalPin.h>
```

That `RTClib.h` sits beside it is no accident: the time from the NMEA lines is
used to set the node's clock.

With twenty variants, MicroNMEA is the most common sensor library in the repo.
It is also in `[sensor_base]`, behind the `ENV_INCLUDE_GPS` flag.

## sparkfun/SparkFun u-blox GNSS Arduino Library

Besides NMEA, u-blox receivers speak UBX, their own binary protocol. That is
more compact, supplies more fields and allows the receiver to be configured —
measurement rate, power management, which satellite systems are used. It also
works over I²C, where NMEA usually runs over a serial port.

MeshCore uses that for the RAK12500, a u-blox module on the I²C bus:

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.171-175

```cpp
#ifndef TELEM_RAK12500_ADDRESS
#define TELEM_RAK12500_ADDRESS   0x42     //RAK12500 Ublox GPS via i2c
#endif
#include <SparkFun_u-blox_GNSS_Arduino_Library.h>
static SFE_UBLOX_GNSS ublox_GNSS;
```

Below that sits `RAK12500LocationProvider`, which implements the same
`LocationProvider` interface as the NMEA version. Six variants declare the
library, all of them RAK boards or derived from them.

## Overview

| Library | Version | Variants | Protocol | Bus |
|---|---|---|---|---|
| `stevemarple/MicroNMEA` | `^2.0.6` · `~2.0.6` | 20 | NMEA 0183 | serial |
| `sparkfun/SparkFun u-blox GNSS Arduino Library` | `^2.2.27` | 6 | UBX | I²C |

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/sensors/MicroNMEALocationProvider.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/MicroNMEALocationProvider.h)
- [`src/helpers/sensors/LocationProvider.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/LocationProvider.h)
- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/EnvironmentSensorManager.cpp)
- [stevemarple/MicroNMEA](https://github.com/stevemarple/MicroNMEA)
- [sparkfun/SparkFun_u-blox_GNSS_Arduino_Library](https://github.com/sparkfun/SparkFun_u-blox_GNSS_Arduino_Library)

Translated from Dutch by Anthropic Claude
