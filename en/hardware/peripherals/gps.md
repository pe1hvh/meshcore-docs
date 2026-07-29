# GPS

*LOCATIONPROVIDER · NMEA · ENABLE PIN · TIME SYNC*

A GPS receiver does two things in a MeshCore node: it gives a position, and
it sets the clock. The first is optional, the second is on boards without
an RTC the only real time the node has. This chapter describes how the
firmware reads the receiver, switches it on and off, and what happens when
there is no fix.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `src/helpers/sensors/LocationProvider.h`,
> `src/helpers/sensors/MicroNMEALocationProvider.h`,
> `src/helpers/sensors/EnvironmentSensorManager.cpp` and the `PIN_GPS_*`
> flags in `variants/`.

## One interface, two kinds of receiver

The firmware knows location only as `LocationProvider`: fourteen methods
saying where you are, what time it is and whether that is to be trusted.

`src/helpers/sensors/LocationProvider.h` r.6-25

```cpp
class LocationProvider {
protected:
    bool _time_sync_needed = true;

public:
    virtual void syncTime() { _time_sync_needed = true; }
    virtual bool waitingTimeSync() { return _time_sync_needed; }
    virtual long getLatitude() = 0;
    virtual long getLongitude() = 0;
    virtual long getAltitude() = 0;
    virtual long satellitesCount() = 0;
    virtual bool isValid() = 0;
    virtual long getTimestamp() = 0;
    virtual void sendSentence(const char * sentence);
    virtual void reset() = 0;
    virtual void begin() = 0;
    virtual void stop() = 0;
    virtual void loop() = 0;
    virtual bool isEnabled() = 0;
```

Two things stand out in that. `isValid()` is separate from `isEnabled()`: an
enabled receiver without a fix is not the same as a disabled one. And
`_time_sync_needed` starts at `true` — the node assumes its clock is wrong
until the GPS proves otherwise.

There are two routes to such a provider:

| Route | Class | Connection |
|---|---|---|
| serial | `MicroNMEALocationProvider` | UART, `PIN_GPS_RX` / `PIN_GPS_TX` |
| I²C | through the sensor table, RAK12500 at `0x42` | see [The I²C Bus](../interfaces/i2c.md) |

The serial route is the ordinary one. Eighteen variant files set a
`-D PIN_GPS_RX=` line; repeat with
`grep -rl -- "-D PIN_GPS_RX=" variants/ | wc -l`.

![The path from the GPS to the firmware: the receiver on a UART, NMEA
sentences in a hundred-byte buffer, the parser extracting position and time
from them, and the enable pin that can switch the whole module
off](../../../images/en/gps-1.svg)

## NMEA in a hundred-byte buffer

The serial provider reads the receiver using the MicroNMEA library and
hands it a fixed buffer:

`src/helpers/sensors/MicroNMEALocationProvider.h` r.36-40

```cpp
class MicroNMEALocationProvider : public LocationProvider {
    char _nmeaBuffer[100];
    MicroNMEA nmea;
    mesh::RTCClock* _clock;
    Stream* _gps_serial;
```

A hundred bytes is one NMEA sentence. The provider gets a `Stream` — the
same abstraction used for the companion connection — and a clock, because
as soon as a valid time arrives it passes it on. On the Heltec V3 that
`Stream` is literally `Serial1`:

`variants/heltec_v3/target.cpp` r.18-21

```cpp
#if ENV_INCLUDE_GPS
  #include <helpers/sensors/MicroNMEALocationProvider.h>
  MicroNMEALocationProvider nmea = MicroNMEALocationProvider(Serial1, &rtc_clock);
  EnvironmentSensorManager sensors = EnvironmentSensorManager(nmea);
```

Without `ENV_INCLUDE_GPS` a sensor manager without a location source is
created and the entire GPS code disappears from the build.

## The enable pin and its four layers

A GPS receiver searching for satellites costs more current than the rest of
the node put together. That is why it can be switched off. Which pin does
that is determined in four steps:

`src/helpers/sensors/MicroNMEALocationProvider.h` r.8-18

```cpp
#ifndef GPS_EN
    #ifdef PIN_GPS_EN
        #define GPS_EN PIN_GPS_EN
    #else
        #define GPS_EN (-1)
    #endif
#endif

#ifndef PIN_GPS_EN_ACTIVE
    #define PIN_GPS_EN_ACTIVE HIGH
#endif
```

If `GPS_EN` is already set somewhere, that wins. Otherwise `PIN_GPS_EN`
from the variant file. If that is missing too it becomes `-1` and the
receiver cannot be switched off. The same cascade appears again for the
reset line, with `LOW` as the default active level instead of `HIGH`.

Those layers exist because some boards put their pins in a `variant.h` and
others in `platformio.ini`. Anyone adding a board and ending up with `-1`
notices it not in an error message but in the battery life.

On the RAK4631 it works differently again: there the GPS shares the power
switch `WB_IO2` with other modules, and `gpsIsAwake(WB_IO2)` checks whether
it is already on (`src/helpers/sensors/EnvironmentSensorManager.cpp`
r.788). How such a shared rail is counted is in [The Display](display.md).

## Time is the second product

`waitingTimeSync()` and `syncTime()` are in the interface for a reason. A
node without an RTC does not know the time after a restart, and time is not
decoration in MeshCore: messages carry a timestamp and key exchange leans
on it. On such boards the GPS is the only source.

If an RTC *is* fitted, it is searched for separately on the I²C bus — four
addresses, see [The I²C Bus](../interfaces/i2c.md). The GPS is then the
correction, not the source.

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`src/helpers/sensors/LocationProvider.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/sensors/LocationProvider.h)
  — the interface
- [`src/helpers/sensors/MicroNMEALocationProvider.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/sensors/MicroNMEALocationProvider.h)
  — the serial implementation and the pin cascade
- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/sensors/EnvironmentSensorManager.cpp)
  — the I²C route and the power switch
- [`variants/heltec_v3/target.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/heltec_v3/target.cpp)
  — how one board creates the provider

Related in this documentation:

- [The I²C Bus](../interfaces/i2c.md) — GPS over I²C, and the clock
- [The Display](display.md) — the shared power rail
- [GPS libraries](../../libraries/other/gps.md) — MicroNMEA and the u-blox
  library
- [Node Matrix](../../platform/node-matrix.md) — which board has GPS

Translated from Dutch by Anthropic Claude
