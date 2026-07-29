# Dependencies between libraries

*DEPENDS · TRANSITIVE · LDF · HIDDEN CODE*

A library you pull in may need libraries of its own. PlatformIO arranges that
without reporting it: code appears in the build that is named in no
`platformio.ini` at all. This chapter makes that layer visible — six libraries
that are declared nowhere and are compiled in regardless, and a handful of
dependencies requested not by a library's driver but by its example sketches.

> [!NOTE]
> **Source.** This page is the only one in the repo that does not rest solely
> on the MeshCore source code. The dependencies come from the
> `library.properties` and `library.json` files of the upstream repositories,
> fetched from `raw.githubusercontent.com` on 28 July 2026 with
> `tools/library-overview.py`. The declarations themselves were verified
> against `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 —
> `platformio.ini` and the seventy-nine `variants/*/platformio.ini`.

## How PlatformIO finds dependencies

Two mechanisms work side by side.

The first is the library's own metadata. An Arduino library has a
`library.properties` with a `depends=` line, a PlatformIO library a
`library.json` with a `"dependencies"` key. Whatever is there is fetched as if
it had been written in `lib_deps`.

The second is the Library Dependency Finder. The LDF scans the source for
`#include` lines and looks for matching libraries, even when nobody declared
them. In its default `chain` mode it looks at the files that are actually
compiled. The result is that a build can contain more than what you wrote
down, and that you see nothing of it as long as everything compiles.

## The six libraries declared nowhere

These six appear in none of the eighty `platformio.ini` files and still end up
in the build:

| Library | Arrives via | Scope |
|---|---|---|
| `bblanchon/ArduinoJson` | `electroniccats/CayenneLPP` | all 507 builds |
| `Adafruit Unified Sensor` | BME280, BMP280, BMP085, BME680, AHTX0, SHTC3, LIS3DH, SHT4x | sensor builds |
| `Sensirion Core` | `Sensirion I2C SHT4x` | sensor builds |
| `ESP32Async/AsyncTCP` | `ESPAsyncWebServer` | ESP32 with WiFi OTA |
| `Adafruit seesaw Library` | `Adafruit ST7735 and ST7789` | six TFT variants |
| `SD` | `Adafruit ST7735 and ST7789` | six TFT variants |

The first row is the most striking. `CayenneLPP` sits in `[arduino_base]` and
therefore applies to all 507 build targets; its `library.json` names
`bblanchon/ArduinoJson` as a dependency. That puts a JSON parser in *every*
MeshCore build, including that of a repeater that never sees any JSON.

`Adafruit Unified Sensor` is Adafruit's shared sensor abstraction; eight of
the fifteen sensor libraries in `[sensor_base]` ask for it. `SD` and
`Adafruit seesaw Library` arrive with the ST7735/ST7789 driver, including on
boards without a card reader.

## The full `depends=` table

Per declared library, whatever its own metadata states. Generated with
`tools/library-overview.py`; an empty cell means the library declares no
dependencies.

<!-- library-overview:start -->

*Generated with `tools/library-overview.py` against commit `03b6ef4`.*

| Library | Depends on | Source |
|---|---|---|
| `Adafruit AHTX0` | `Adafruit Unified Sensor`, `Adafruit BusIO`, `Adafruit SH110X` | `library.properties` |
| `Adafruit BME280 Library` | `Adafruit Unified Sensor`, `Adafruit BusIO` | `library.properties` |
| `Adafruit BME680 Library` | `Adafruit Unified Sensor`, `Adafruit GFX Library`, `Adafruit SSD1306`, `Adafruit BusIO` | `library.properties` |
| `Adafruit BMP085 Library` | `Adafruit Unified Sensor`, `Adafruit BusIO` | `library.properties` |
| `Adafruit BMP280 Library` | `Adafruit Unified Sensor`, `Adafruit BusIO` | `library.properties` |
| `Adafruit BusIO` | — | `library.properties` |
| `Adafruit EPD` | `Adafruit GFX Library` | `library.properties` |
| `Adafruit GFX Library` | `Adafruit BusIO` | `library.properties` |
| `Adafruit INA219` | `Adafruit NeoPixel`, `Adafruit GFX Library`, `Adafruit SSD1306`, `Adafruit BusIO` | `library.properties` |
| `Adafruit INA260 Library` | `Adafruit BusIO`, `Adafruit NeoPixel` | `library.properties` |
| `Adafruit INA3221 Library` | `Adafruit BusIO` | `library.properties` |
| `Adafruit LIS3DH` | `Adafruit Unified Sensor`, `Adafruit BusIO` | `library.properties` |
| `Adafruit MLX90614 Library` | `Adafruit BusIO` | `library.properties` |
| `Adafruit NeoPixel` | — | `library.properties` |
| `Adafruit SH110X` | `Adafruit GFX Library`, `Adafruit BusIO` | `library.properties` |
| `Adafruit SHT4x Library` | `Adafruit BusIO`, `Adafruit Unified Sensor`, `Adafruit SH110X`, `Adafruit SSD1306` | `library.properties` |
| `Adafruit SHTC3 Library` | `Adafruit BusIO`, `Adafruit Unified Sensor` | `library.properties` |
| `Adafruit SSD1306` | `Adafruit GFX Library` | `library.properties` |
| `Adafruit ST7735 and ST7789 Library` | `Adafruit GFX Library`, `Adafruit seesaw Library`, `SD` | `library.properties` |
| `Adafruit_VL53L0X` | `Adafruit SSD1306`, `Adafruit GFX Library` | `library.properties` |
| `Arduino_LPS22HB` | — | `library.properties` |
| `base64` | — | `library.properties` |
| `BME280` | — | `library.properties` |
| `BSEC` | `BME68x Sensor library` | `library.properties` |
| `CayenneLPP` | `bblanchon/ArduinoJson` | `library.json` |
| `CRC32` | — | `library.properties` |
| `Crypto` | — | `library.json` |
| `ESPAsyncWebServer` | `AsyncTCP`, `ESPAsyncTCP`, `Hash`, `RPAsyncTCP` | `library.json` |
| `googletest` | *not retrieved — no Arduino metadata; the registry package carries no library.json* | — |
| `GxEPD2` | `Adafruit GFX Library` | `library.properties` |
| `INA226` | — | `library.properties` |
| `LovyanGFX` | — | `library.properties` |
| `Melopero RV3028` | *not retrieved — repository not found under the expected name on GitHub* | — |
| `MicroNMEA` | — | `library.properties` |
| `NonBlockingRTTTL` | — | `library.properties` |
| `PCA9557-arduino` | — | `library.properties` |
| `RadioLib` | — | `library.properties` |
| `RTClib` | `Adafruit BusIO` | `library.properties` |
| `Sensirion I2C SHT4x` | `Sensirion Core` | `library.properties` |
| `SparkFun u-blox GNSS Arduino Library` | — | `library.properties` |
| `SPI` | *not retrieved — framework library, ships with the platform package* | — |
| `SubGhz` | *not retrieved — framework library, ships with framework-arduinoststm32* | — |
| `U8g2` | — | `library.properties` |
| `Wire` | *not retrieved — framework library, ships with the platform package* | — |
| `XPowersLib` | — | `library.properties` |

<!-- library-overview:end -->

![Dependency graph of the MeshCore libraries: declared libraries point to the
libraries they bring in themselves, with ArduinoJson, Adafruit Unified Sensor,
Sensirion Core, AsyncTCP, Adafruit seesaw and SD in a different colour because
they appear in no platformio.ini](../../images/en/dependencies-1.svg)

## Dependencies of example sketches

A `depends=` says nothing about *which* part of the library needs something.
For five Adafruit libraries the declaration applies to the `examples/`
directory, not to the driver:

| Library | Declares | Needed for |
|---|---|---|
| `Adafruit INA219` | NeoPixel, GFX, SSD1306, BusIO | example sketches |
| `Adafruit INA260` | BusIO, NeoPixel | example sketches |
| `Adafruit_VL53L0X` | SSD1306, GFX | example sketches |
| `Adafruit BME680` | Unified Sensor, GFX, SSD1306, BusIO | example sketches |
| `Adafruit AHTX0` | Unified Sensor, BusIO, SH110X | example sketches |

The consequence is concrete: switch on `[sensor_base]` and a current meter
pulls in two display libraries. The `-w` flag in `[arduino_base]` suppresses
all compiler warnings, so no signal about that ever appears:

`platformio.ini` r.27

```text
build_flags = -w -DNDEBUG -DRADIOLIB_STATIC_ONLY=1 -DRADIOLIB_GODMODE=1
```

## Manually pinned transitive dependencies

`adafruit/Adafruit GFX Library @ ^1.12.1` is declared explicitly in
`lib_deps` in eight variants, while `Adafruit SSD1306` already brings it in
through its own `depends=`. `adafruit/Adafruit BusIO @ ^1.17.2` is declared
explicitly in one:

`variants/sensecap_indicator-espnow/platformio.ini` r.31-33

```text
lib_deps=${esp32_base.lib_deps}
  adafruit/Adafruit BusIO @ ^1.17.2
  lovyan03/LovyanGFX @ ^1.2.7
```

That is not duplication. A transitive dependency has no version range of its
own in the build; declaring it anyway pins the version of a library you never
use directly.

## Not verified

The dependencies of `melopero/Melopero RV3028` could not be retrieved: the
`library.properties` was not found and the repository is not on GitHub under
the expected name. That row stays empty, with the reason stated.
`google/googletest` has no Arduino metadata; the registry package carries no
`library.json`. The three framework libraries `SPI`, `Wire` and `SubGhz` have
no upstream metadata by definition.

## Three declarations without a findable include

> [!NOTE]
> Three libraries are declared but no `#include` of their headers can be found
> anywhere in `src/`, `examples/`, `variants/` or `arch/`. They are
> `adafruit/Adafruit EPD @ 4.6.1`
> (`variants/mesh_pocket/platformio.ini` r.30) and
> `adafruit/Adafruit LIS3DH @ ^1.2.4` plus
> `adafruit/Adafruit SHT4x Library @ ^1.0.4`
> (`variants/wio_wm1110/platformio.ini` r.36-37). The search ran on the header
> names `Adafruit_EPD`, `Adafruit_LIS3DH` and `Adafruit_SHT4x` across all files
> with extension `.h`, `.hpp`, `.c`, `.cpp` and `.ino`. The SHT4x sensor is
> driven in the firmware by `SensirionI2cSht4x`
> (`src/helpers/sensors/EnvironmentSensorManager.cpp` r.90-91), not by the
> Adafruit library. This is an observation; no conclusion is drawn from it
> here.

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`variants/mesh_pocket/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/mesh_pocket/platformio.ini)
- [`variants/wio_wm1110/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/wio_wm1110/platformio.ini)
- [`variants/sensecap_indicator-espnow/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/sensecap_indicator-espnow/platformio.ini)
- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/EnvironmentSensorManager.cpp)
- [PlatformIO — Library Dependency Finder](https://docs.platformio.org/en/latest/librarymanager/ldf.html)

Translated from Dutch by Anthropic Claude
