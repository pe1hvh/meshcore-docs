# Sensor libraries

*SENSOR_BASE · ENV_INCLUDE · QUERY_ · LPP*

Seventeen sensor libraries sit in the firmware, and they are all called the
same way: an `init_` function, a `query_` function and a row in one table.
What ends up in a build is decided by a series of `ENV_INCLUDE_*` flags. One
sensor driver belongs to the group but appears in no `lib_deps` line at all.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini` r.122-154,
> `src/helpers/sensors/EnvironmentSensorManager.cpp` and
> `src/helpers/sensors/RAK12035_SoilMoisture.h`.

## How MeshCore calls this group

All environment sensors sit in one file,
`EnvironmentSensorManager.cpp`, each behind its own `#if ENV_INCLUDE_*`. Per
sensor there are two functions: one to initialise it, one to read it. The
latter writes straight into a `CayenneLPP` buffer:

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.242-252

```cpp
#if ENV_INCLUDE_AHTX0
static uint8_t init_ahtx0(TwoWire* wire, uint8_t addr) {
  return AHTX0.begin(wire, 0, addr) ? 1 : 0;
}
static void query_ahtx0(uint8_t ch, uint8_t, CayenneLPP& lpp) {
  sensors_event_t humidity, temp;
  AHTX0.getEvent(&humidity, &temp);
  lpp.addTemperature(ch, temp.temperature);
  lpp.addRelativeHumidity(ch, humidity.relative_humidity);
}
#endif
```

Those two functions are put in one table together with the I²C address:

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.547-557

```cpp
struct SensorDef {
  uint8_t     address;
  const char* name;
  uint8_t   (*init)(TwoWire* wire, uint8_t address);
  void      (*query)(uint8_t channel, uint8_t sub_channel, CayenneLPP& telemetry);
};

static const SensorDef SENSOR_TABLE[] = {
#if ENV_INCLUDE_AHTX0
  { TELEM_AHTX_ADDRESS,    "AHT10/AHT20", init_ahtx0,    query_ahtx0    },
#endif
```

At start-up MeshCore walks that table, tries each address on the I²C bus and
assigns an LPP channel to every sensor found, in table order. Adding a sensor
therefore means: declare a library, an `ENV_INCLUDE_` flag, two functions and
one row in the table.

![From build flag to telemetry packet: the ENV_INCLUDE flags decide which
sensor code is compiled in, the sensor table maps each I²C address to an init
and a query function, and those query functions write their values into a
single CayenneLPP buffer that goes out into the mesh as a telemetry
packet](../../../images/en/sensors-1.svg)

## The fifteen from `[sensor_base]`

The `[sensor_base]` section (`platformio.ini` r.122-154) sets fifteen flags
and declares fifteen libraries. Call the section and you get all fifteen.

`platformio.ini` r.139-144

```text
lib_deps =
  adafruit/Adafruit INA3221 Library @ ^1.0.1
  adafruit/Adafruit INA219 @ ^1.2.3
  robtillaart/INA226 @ ^0.6.4
  adafruit/Adafruit INA260 Library @ ^1.5.3
  adafruit/Adafruit AHTX0 @ ^2.0.5
```

**`Adafruit AHTX0`** drives the AHT10 and AHT20, cheap temperature and
humidity sensors with a fixed I²C address. Supplies temperature and relative
humidity.

**`Adafruit BME280 Library`** drives the Bosch BME280: temperature, humidity
and air pressure in one package. In the repo this is the most common
environment sensor outside `[sensor_base]`; seven variants name a BME280
library.

**`Adafruit BMP280 Library`** is the variant without humidity measurement —
temperature and pressure.

**`Adafruit BMP085 Library`** drives the older BMP085 and BMP180.

**`Adafruit BME680 Library`** drives the BME680, which measures a gas
resistance alongside temperature, humidity and pressure. Its `depends=` asks
for GFX and SSD1306 for the example sketches.

**`Adafruit SHTC3 Library`** drives the Sensirion SHTC3, a compact,
low-power temperature and humidity sensor.

**`Sensirion I2C SHT4x`** drives the SHT4x range from Sensirion. This is the
library that actually drives the SHT4x sensors in the firmware, through
`SensirionI2cSht4x` (`EnvironmentSensorManager.cpp` r.90-91). It brings in
`Sensirion Core`, which is declared nowhere.

**`Arduino_LPS22HB`** drives the ST LPS22HB pressure sensor, as found on the
Arduino Nano 33 BLE Sense.

**`Adafruit MLX90614 Library`** drives an infrared thermometer that measures
the temperature of a surface at a distance, alongside its own ambient
temperature. Hence the `sub_ch` argument in the `query_` function: two values
from one sensor.

**`Adafruit_VL53L0X`** drives a time-of-flight distance sensor, which measures
the distance to an object with a laser pulse.

**`Adafruit INA219`**, **`Adafruit INA260 Library`**,
**`Adafruit INA3221 Library`** and **`robtillaart/INA226`** measure current
and voltage; those four are covered in [`power.md`](power.md).

**`stevemarple/MicroNMEA`** also belongs to this section but is a GPS library;
see [`gps.md`](gps.md).

## finitespace/BME280

A second BME280 library, outside `[sensor_base]`, declared in one variant.
Unlike the Adafruit version it does not use `Adafruit Unified Sensor` and
supplies its values without that abstraction.

## boschsensortec/BSEC Software Library

BSEC is Bosch's closed software layer on top of the BME680. Where the ordinary
library yields a gas resistance in ohms, BSEC converts that into an air
quality index, with a calibration that runs over days. Declared in two
variants, `lilygo_tbeam_SX1276` and `rak4631`, behind the
`ENV_INCLUDE_BME680_BSEC` flag with a `query_bme680_bsec` function of its own.

## RAK12035_SoilMoisture — vendored

The RAK12035 soil moisture sensor has no `lib_deps` line. Its driver simply
sits in the source, as `src/helpers/sensors/RAK12035_SoilMoisture.h` and
`.cpp`, and otherwise follows exactly the same pattern as the others: an
`ENV_INCLUDE_RAK12035` flag, an `init_` and a `query_rak12035` function and a
row in the sensor table. Anyone compiling a sensor list from the
`platformio.ini` files misses this one.

## Overview

| Library | Version | Variants | Flag |
|---|---|---|---|
| `adafruit/Adafruit AHTX0` | `^2.0.5` | 3 | `ENV_INCLUDE_AHTX0` |
| `adafruit/Adafruit BME280 Library` | `^2.3.0` | 6 | `ENV_INCLUDE_BME280` |
| `adafruit/Adafruit BMP280 Library` | `^2.6.8` | 2 | `ENV_INCLUDE_BMP280` |
| `adafruit/Adafruit BMP085 Library` | `^1.2.4` | 1 | `ENV_INCLUDE_BMP085` |
| `adafruit/Adafruit BME680 Library` | `^2.0.4` | 1 | `ENV_INCLUDE_BME680` |
| `adafruit/Adafruit SHTC3 Library` | `^1.0.1` | 1 | `ENV_INCLUDE_SHTC3` |
| `sensirion/Sensirion I2C SHT4x` | `^1.1.2` | 1 | `ENV_INCLUDE_SHT4X` |
| `adafruit/Adafruit SHT4x Library` | `^1.0.4` | 1 | no include found |
| `arduino-libraries/Arduino_LPS22HB` | `^1.0.2` | 1 | `ENV_INCLUDE_LPS22HB` |
| `adafruit/Adafruit MLX90614 Library` | `^2.1.5` | 1 | `ENV_INCLUDE_MLX90614` |
| `adafruit/Adafruit_VL53L0X` | `^1.2.4` | 1 | `ENV_INCLUDE_VL53L0X` |
| `finitespace/BME280` | `^3.0.0` | 1 | — |
| `boschsensortec/BSEC Software Library` | `^1.8.1492` | 2 | `ENV_INCLUDE_BME680_BSEC` |
| *`RAK12035_SoilMoisture`* | *vendored* | *—* | `ENV_INCLUDE_RAK12035` |

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/EnvironmentSensorManager.cpp)
- [`src/helpers/sensors/RAK12035_SoilMoisture.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/RAK12035_SoilMoisture.h)
- [`src/helpers/SensorManager.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/SensorManager.h)
- [Sensirion/arduino-i2c-sht4x](https://github.com/Sensirion/arduino-i2c-sht4x)
- [boschsensortec/Bosch-BSEC2-Library](https://github.com/boschsensortec/Bosch-BSEC2-Library)

Translated from Dutch by Anthropic Claude
