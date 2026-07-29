# CayenneLPP

*TELEMETRY · WIRE FORMAT · PINNED EXACTLY · CHANNELS*

CayenneLPP determines how MeshCore puts sensor values on the wire. It is the
only library in `[arduino_base]` pinned to an exact version, and that is
understandable: the library does not encode data for internal use but the
format in which two nodes exchange telemetry.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini`, `src/helpers/SensorManager.h`,
> `src/helpers/sensors/EnvironmentSensorManager.cpp` and
> `examples/kiss_modem/KissModem.cpp`.

## What it does

Cayenne Low Power Payload is a compact binary format for sensor data,
originally devised for LoRaWAN. Every measurement consists of a channel
number, a type code and the value on a fixed scale — temperature in steps of
0.1 °C, air pressure in steps of 0.1 hPa, and so on. That way a complete
sensor reading fits in a few dozen bytes, without field names and without
separators. The implementation MeshCore uses is the one by Electronic Cats,
[github.com/ElectronicCats/CayenneLPP](https://github.com/ElectronicCats/CayenneLPP).

## How MeshCore pulls it in

`platformio.ini` r.26

```text
  electroniccats/CayenneLPP @ 1.6.1
```

No `^`, no `~`: exactly 1.6.1. The line sits in `[arduino_base]`, so all 507
build targets get it. Through its `library.json` CayenneLPP brings in
`bblanchon/ArduinoJson` — see [`../dependencies.md`](../dependencies.md).

The exact pin stands out because the other six lines in the same section *do*
have a range. No explanation for it appears anywhere in the repo. The
suspicion that it has to do with the wire format is an obvious one: change the
encoding and two nodes on different versions no longer understand each other.
That is a suspicion, not an established reason.

## How MeshCore uses it

CayenneLPP sits at the heart of the sensor abstraction. `SensorManager` passes
a `CayenneLPP` object to whoever reads sensors:

`src/helpers/SensorManager.h` r.3

```cpp
#include <CayenneLPP.h>
```

`src/helpers/SensorManager.h` r.19

```cpp
  virtual bool querySensors(uint8_t requester_permissions, CayenneLPP& telemetry) { return false; }
```

Every sensor driver writes straight into that object. The `query_*` functions
in `EnvironmentSensorManager.cpp` do nothing else:

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.246-251

```cpp
static void query_ahtx0(uint8_t ch, uint8_t, CayenneLPP& lpp) {
  sensors_event_t humidity, temp;
  AHTX0.getEvent(&humidity, &temp);
  lpp.addTemperature(ch, temp.temperature);
  lpp.addRelativeHumidity(ch, humidity.relative_humidity);
}
```

At the other end of the chain the buffer is read out and transmitted:

`examples/kiss_modem/KissModem.cpp` r.557-560

```cpp
  uint8_t permissions = data[0];
  CayenneLPP telemetry(255);
  if (_sensors.querySensors(permissions, telemetry)) {
    writeHardwareFrame(HW_RESP(HW_CMD_GET_SENSORS), telemetry.getBuffer(), telemetry.getSize());
```

The text `CayenneLPP` occurs in 24 of the 590 source files.

## What it means for a node

Everything a node sends as sensor data passes through this format. The channel
number a measurement appears under is assigned at start-up in the order
sensors are detected — channel 1 is reserved for the node itself
(`TELEM_CHANNEL_SELF`), the first sensor found gets channel 2. Two nodes with
different sensors therefore do not share a channel layout.

Because the library is pinned exactly, a build made today behaves here the
same as a build made last year. That does not hold for the libraries with a
`^` range.

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/SensorManager.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/SensorManager.h)
- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/EnvironmentSensorManager.cpp)
- [`examples/kiss_modem/KissModem.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/kiss_modem/KissModem.cpp)
- [ElectronicCats/CayenneLPP](https://github.com/ElectronicCats/CayenneLPP)

Translated from Dutch by Anthropic Claude
