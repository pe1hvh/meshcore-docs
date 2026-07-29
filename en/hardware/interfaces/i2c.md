# The I²C Bus

*TWO WIRES · ADDRESSES 0x08–0x77 · SCAN BEFORE USE · WIRE AND WIRE1*

I²C is the bus for everything that does not need to be fast: the display,
the real-time clock, the sensors, sometimes the GPS. Two wires, one address
per device, and a firmware that does not know in advance what is out there.
This chapter describes how MeshCore scans the bus, why that happens before
any sensor library runs, and when a node uses a second bus.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `src/helpers/sensors/EnvironmentSensorManager.cpp`,
> `src/helpers/AutoDiscoverRTCClock.cpp` and the `PIN_BOARD_SDA` flags in
> `variants/`.

![Diagram of the I²C bus: SDA and SCL with pull-ups, the SoC as master and
display, clock and sensors as slaves, each with its own
address](../../../images/en/i2c-1.svg)

## Two wires, two pins

The bus has one data line (`SDA`) and one clock line (`SCL`). Which pins
those are is set by the variant:

`variants/lilygo_tbeam_1w/platformio.ini`

```ini
  ; I2C pins
  -D PIN_BOARD_SDA=8
  -D PIN_BOARD_SCL=9
```

53 of the 79 variant directories set `PIN_BOARD_SDA`; counted per directory
across `variants/`, commented-out lines excluded. The rest use the Arduino
board's default pins or have no I²C devices on board.

`Wire` is the name of that bus in the Arduino world. It is a framework
library and not a PlatformIO package — see
[Wire and SPI](../../libraries/core/wire-spi.md).

## Scanning before anything is addressed

The most striking thing about I²C handling in MeshCore is the order. The
firmware first probes the whole bus and only afterwards starts the libraries
of the devices that answered:

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.220-225

```cpp
static void scanI2CBus(TwoWire* wire, bool found[128]) {
  for (uint8_t addr = 0x08; addr < 0x78; addr++) {
    wire->beginTransmission(addr);
    found[addr] = (wire->endTransmission() == 0);
  }
}
```

Addresses `0x08` through `0x77`. Addresses outside that range are reserved
in the I²C standard and are not tried. A device that acknowledges
(`endTransmission()` returns zero) is noted; nothing else happens yet.

The comment above it says why that order matters:

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.215-218

```cpp
// Probes every valid address and records which ones ACK.
// This runs before any sensor library is touched, so a missing
// or misbehaving device cannot stall or crash the boot sequence.
```

A sensor library addressing a device that is not there can hang or crash. By
scanning first and initialising only the addresses that were found, a
missing or broken sensor cannot hold up the boot. Which sensors those are
and which libraries belong to them is in
[Sensor libraries](../../libraries/other/sensors.md).

## The clock does not scan, it tries four addresses

For the real-time clock it works differently. Four addresses are hard-coded
and each is tried separately:

`src/helpers/AutoDiscoverRTCClock.cpp` r.18-27

```cpp
#define DS3231_ADDRESS   0x68
#define RV3028_ADDRESS   0x52
#define PCF8563_ADDRESS  0x51
#define RX8130CE_ADDRESS 0x32

bool AutoDiscoverRTCClock::i2c_probe(TwoWire& wire, uint8_t addr) {
  wire.beginTransmission(addr);
  uint8_t error = wire.endTransmission();
  return (error == 0);
}
```

| Chip | Address |
|---|---|
| DS3231 | `0x68` |
| RV3028 | `0x52` |
| PCF8563 | `0x51` |
| RX8130CE | `0x32` |

The same technique — begin a transmission and see whether it is
acknowledged — but targeted instead of broad. There are only four supported
clocks, so a full scan would add nothing. The DS3231 probe can also be
disabled with `DISABLE_DS3231_PROBE`, because on some boards something else
sits at `0x68`.

## Two buses on some boards

Sensors do not have to sit on the same bus as the display:

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.6-8

```cpp
#define TELEM_WIRE &Wire1  // Use Wire1 as the I2C bus for Environment Sensors
// ...
#define TELEM_WIRE &Wire  // Use default I2C bus for Environment Sensors
```

`TELEM_WIRE` points at `Wire1` on boards that have a second bus and at
`Wire` otherwise. Every sensor library is handed that reference on
construction. A second bus is useful when the display keeps the first bus
busy, or when a sensor uses an address that is already taken.

> [!NOTE]
> An address collision cannot be solved in software on I²C. Two devices at
> the same address on the same bus both answer and the result is unusable.
> The second bus is then the only way out — or a sensor with a selectable
> address.

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/sensors/EnvironmentSensorManager.cpp)
  — `scanI2CBus()` and `TELEM_WIRE`
- [`src/helpers/AutoDiscoverRTCClock.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/AutoDiscoverRTCClock.cpp)
  — the four clock addresses and `i2c_probe()`
- [`variants/lilygo_tbeam_1w/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/lilygo_tbeam_1w/platformio.ini)
  — `PIN_BOARD_SDA` and `PIN_BOARD_SCL` of one board

Related in this documentation:

- [The SPI Bus](spi.md) — the fast bus next to it
- [Wire and SPI](../../libraries/core/wire-spi.md) — why these are framework
  libraries and not packages
- [The Display](../peripherals/display.md) — the most common I²C device
- [GPS](../peripherals/gps.md) — GPS over I²C instead of serial
- [Sensor libraries](../../libraries/other/sensors.md) — what gets
  initialised after the scan

Translated from Dutch by Anthropic Claude
