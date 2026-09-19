# Libraries in MeshCore

*LIB_DEPS · INHERITANCE · VERSIONING · INVENTORY*

MeshCore is not a self-contained program. The firmware leans on fifty-two
external libraries, which enter the build along four different routes, plus a
handful of code that bypasses the dependency mechanism altogether. This
chapter shows which they are, where they come from, and why a build made
today does not produce the same bytes as a build made six months ago.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini`, the seventy-nine `variants/*/platformio.ini`, `lib/`,
> `arch/` and `src/helpers/sensors/`.

## What a `lib_dep` is

PlatformIO describes a project in `platformio.ini`. Under the key `lib_deps`,
each section states which libraries it needs. When building, PlatformIO
fetches those — from its own registry, from a URL or from a path on disk —
unpacks them into `.pio/libdeps/<environment>/` and puts them on the
compiler's include path.

MeshCore has eighty of those files: the `platformio.ini` in the project root
plus seventy-nine in `variants/`. The root pulls them all in through
`extra_configs`:

`platformio.ini` r.11-14

```text
[platformio]
extra_configs =
  variants/*/platformio.ini
  platformio.local.ini
```

Together those eighty files declare fifty-two unique libraries. The root
names twenty-eight of them; the rest come from the variants.

## The four routes in

**Registry with a version range.** The ordinary form. The name consists of an
author prefix and a library name, followed by a range with `^` or `~`.

`platformio.ini` r.22

```text
  jgromes/RadioLib @ ^7.6.0
```

**Registry, pinned exactly.** Without `^` or `~`, exactly one version is
named. Across the whole repo this happens for four libraries.

`platformio.ini` r.26

```text
  electroniccats/CayenneLPP @ 1.6.1
```

**Git tag or zip with a commit hash.** PlatformIO accepts a URL. After `#`
comes a tag or commit; whatever is there determines what you get.

`platformio.ini` r.95

```text
  https://github.com/oltaco/CustomLFS#0.2.2
```

`variants/` holds four more URL declarations. Three of them fetch a zip of a
full commit hash: `NMIoT/meshsolar` and the two forks of
`heltec-eink-modules`, from `Quency-D` and from `todd-herbert`. The fourth,
`SoulOfNoob/GxEPD2`, is a `.git` URL with no revision behind it and is
therefore not fixed.

**Local path.** Code that lives in the MeshCore repo itself, pointed at with
`file://`. There is no upstream to fetch from and no version number to raise.

`platformio.ini` r.70

```text
  file://arch/esp32/AsyncElegantOTA
```

`platformio.ini` r.119

```text
  file://arch/stm32/Adafruit_LittleFS_stm32
```

## What arrives outside `lib_deps`

Not all external code goes through `lib_deps`. PlatformIO compiles everything
in the `lib/` directory automatically. MeshCore uses that for two things:

- `lib/ed25519` — a C implementation of Ed25519, vendored into the repo. See
  [`core/crypto.md`](core/crypto.md), where it sits alongside the Ed25519 from
  `rweather/Crypto`.
- `lib/nrf52` — headers and the SoftDevice API `s140_nrf52_7.3.0_API` for the
  nRF52 platform.

On top of that, a complete sensor driver simply sits in the source tree:
`src/helpers/sensors/RAK12035_SoilMoisture.h` and `.cpp`. It appears in no
`lib_deps` line at all. See [`other/sensors.md`](other/sensors.md).

## Framework libraries

Two lines in `[arduino_base]` have no author prefix and no version:

`platformio.ini` r.20-21

```text
  SPI
  Wire
```

Those are not registry packages but framework libraries: they ship with the
platform's own framework package. On ESP32 they come from Arduino-ESP32, on
nRF52 from the Adafruit nRF52 core, on RP2040 from arduino-pico and on STM32
from STM32duino. The name is the same, the implementation is not. The same
holds for `SubGhz` on r.120. See [`core/wire-spi.md`](core/wire-spi.md) and
[`core/subghz.md`](core/subghz.md).

## Inheritance

`[arduino_base]` contains seven `lib_deps` lines. Every variant inherits from
it, directly or through a platform section, so those seven apply to all 507
build targets in the repo. The eighth target, `[env:native]`, is not an
Arduino build and inherits nothing.

The platform sections handle that in two different ways:

`platformio.ini` r.57-58

```text
[esp32_base]
extends = arduino_base
```

`platformio.ini` r.93-95

```text
lib_deps =
  ${arduino_base.lib_deps}
  https://github.com/oltaco/CustomLFS#0.2.2
```

`[esp32_base]` defines no `lib_deps` of its own and therefore keeps what
`extends` gives it. `[nrf52_base]` (r.93) and `[stm32_base]` (r.118) do have
their own `lib_deps`, and that key replaces the inherited one rather than
adding to it. That is why those two have to repeat `${arduino_base.lib_deps}`
explicitly: without that line, RadioLib, Crypto, RTClib, RV3028 and CayenneLPP
would disappear from the nRF52 and STM32 platforms.

Such `${section.lib_deps}` references occur 572 times across the eighty files.
`tools/library-overview.py` deliberately does not resolve them, because that
would hide which variant inherits from which base.

## What `^` means

`^7.6.0` means: at least 7.6.0, but below 8.0.0. `~2.0.6` is narrower — at
least 2.0.6, below 2.1.0. `1.6.1` without a sign is exactly that version.

The consequence is that most libraries in this list are not fixed. Anyone
building today with `jgromes/RadioLib @ ^7.6.0` gets the newest 7.x in the
registry at that moment; anyone who did so six months ago got a different one.
The firmware is reproducible in behaviour, not in bytes. Only the four
exactly pinned libraries, the tagged git URL and the two local paths yield
the same result over time.

## Inventory

All fifty-two libraries, with the route they arrive by, in how many of the
eighty `platformio.ini` files they are declared, and the chapter that covers
them. A `·` after the name means: declared in the root as well.

The second table counts in how many firmware source files a library is
actually named. The count runs over the 590 files with extension `.h`, `.hpp`,
`.c`, `.cpp` or `.ino` under `src/`, `examples/`, `test/`, `arch/`, `lib/` and
`variants/`; the *Token* column gives the search pattern, so the figure can be
recomputed.

<!-- library-overview:start -->

*Generated with `tools/library-overview.py` against commit `03b6ef4`.*

| Library | Version | Route | `.ini` | Kind | Chapter |
|---|---|---|---|---|---|
| `adafruit/Adafruit AHTX0` **·** | `^2.0.5` | registry, range | 3 | supporting | `other/sensors.md` |
| `adafruit/Adafruit BME280 Library` **·** | `^2.3.0` | registry, range | 6 | supporting | `other/sensors.md` |
| `adafruit/Adafruit BME680 Library` **·** | `^2.0.4` | registry, range | 1 | supporting | `other/sensors.md` |
| `adafruit/Adafruit BMP085 Library` **·** | `^1.2.4` | registry, range | 1 | supporting | `other/sensors.md` |
| `adafruit/Adafruit BMP280 Library` **·** | `^2.6.8` | registry, range | 2 | supporting | `other/sensors.md` |
| `adafruit/Adafruit BusIO` | `^1.17.2` | registry, range | 1 | supporting | `other/displays.md` |
| `adafruit/Adafruit EPD` | `4.6.1` | registry, pinned | 1 | supporting | `other/displays.md` |
| `adafruit/Adafruit GFX Library` | `^1.12.1` | registry, range | 8 | supporting | `other/displays.md` |
| `adafruit/Adafruit INA219` **·** | `^1.2.3` | registry, range | 3 | supporting | `other/power.md` |
| `adafruit/Adafruit INA260 Library` **·** | `^1.5.3` | registry, range | 1 | supporting | `other/power.md` |
| `adafruit/Adafruit INA3221 Library` **·** | `^1.0.1` | registry, range | 3 | supporting | `other/power.md` |
| `adafruit/Adafruit LIS3DH` | `^1.2.4` | registry, range | 1 | supporting | `other/peripherals.md` |
| `adafruit/Adafruit MLX90614 Library` **·** | `^2.1.5` | registry, range | 1 | supporting | `other/sensors.md` |
| `adafruit/Adafruit NeoPixel` | `^1.10.0` · `^1.12.3` | registry, range | 3 | supporting | `other/peripherals.md` |
| `adafruit/Adafruit SH110X` | `^2.1.13` · `~2.1.13` | registry, range | 7 | supporting | `other/displays.md` |
| `adafruit/Adafruit SHT4x Library` | `^1.0.4` | registry, range | 1 | supporting | `other/sensors.md` |
| `adafruit/Adafruit SHTC3 Library` **·** | `^1.0.1` | registry, range | 1 | supporting | `other/sensors.md` |
| `adafruit/Adafruit SSD1306` | `^2.5.13` | registry, range | 23 | supporting | `other/displays.md` |
| `adafruit/Adafruit ST7735 and ST7789 Library` | `^1.11.0` | registry, range | 6 | supporting | `other/displays.md` |
| `file://arch/stm32/Adafruit_LittleFS_stm32` **·** | — | local path | 1 | core | `core/littlefs-stm32.md` |
| `adafruit/Adafruit_VL53L0X` **·** | `^1.2.4` | registry, range | 1 | supporting | `other/sensors.md` |
| `arduino-libraries/Arduino_LPS22HB` **·** | `^1.0.2` | registry, range | 1 | supporting | `other/sensors.md` |
| `file://arch/esp32/AsyncElegantOTA` **·** | — | local path | 1 | core | `core/asyncelegantota.md` |
| `densaugeo/base64` | `~1.4.0` | registry, range | 76 | supporting | `other/utilities.md` |
| `finitespace/BME280` | `^3.0.0` | registry, range | 1 | supporting | `other/sensors.md` |
| `boschsensortec/BSEC Software Library` | `^1.8.1492` | registry, range | 2 | supporting | `other/sensors.md` |
| `electroniccats/CayenneLPP` **·** | `1.6.1` | registry, pinned | 1 | core | `core/cayenne-lpp.md` |
| `bakercp/CRC32` | `^2.0.0` | registry, range | 15 | supporting | `other/utilities.md` |
| `rweather/Crypto` **·** | `^0.4.0` | registry, range | 3 | core | `core/crypto.md` |
| `oltaco/CustomLFS` **·** | `0.2.2` | git/zip URL | 1 | core | `core/custom-lfs.md` |
| `ESP32Async/ESPAsyncWebServer` **·** | `3.10.3` | registry, pinned | 1 | core | `core/espasyncwebserver.md` |
| `google/googletest` **·** | `1.17.0` | registry, pinned | 1 | supporting | `other/testing.md` |
| `zinggjm/GxEPD2` | `1.6.2` | registry, pinned | 5 | supporting | `other/displays.md` |
| `SoulOfNoob/GxEPD2` | — | git/zip URL | 1 | supporting | `other/displays.md` |
| `Quency-D/heltec-eink-modules` | `563dd41` | git/zip URL | 2 | supporting | `other/displays.md` |
| `todd-herbert/heltec-eink-modules` | `9207eb6` | git/zip URL | 1 | supporting | `other/displays.md` |
| `robtillaart/INA226` **·** | `^0.6.4` | registry, range | 1 | supporting | `other/power.md` |
| `lovyan03/LovyanGFX` | `^1.2.7` | registry, range | 1 | supporting | `other/displays.md` |
| `melopero/Melopero RV3028` **·** | `^1.1.0` | registry, range | 1 | core | `core/rv3028.md` |
| `NMIoT/meshsolar` | `dfc5330` | git/zip URL | 1 | supporting | `other/power.md` |
| `stevemarple/MicroNMEA` **·** | `^2.0.6` · `~2.0.6` | registry, range | 20 | supporting | `other/gps.md` |
| `end2endzone/NonBlockingRTTTL` | `^1.3.0` | registry, range | 17 | supporting | `other/peripherals.md` |
| `maxpromer/PCA9557-arduino` | — | registry, no version | 1 | supporting | `other/peripherals.md` |
| `jgromes/RadioLib` **·** | `^7.6.0` | registry, range | 1 | core | `core/radiolib.md` |
| `adafruit/RTClib` **·** | `^2.1.3` | registry, range | 7 | core | `core/rtclib.md` |
| `sensirion/Sensirion I2C SHT4x` **·** | `^1.1.2` | registry, range | 1 | supporting | `other/sensors.md` |
| `sparkfun/SparkFun u-blox GNSS Arduino Library` | `^2.2.27` | registry, range | 6 | supporting | `other/gps.md` |
| `SPI` **·** | — | framework package | 1 | core | `core/wire-spi.md` |
| `SubGhz` **·** | — | framework package | 1 | core | `core/subghz.md` |
| `olikraus/U8g2` | `^2.35.19` | registry, range | 1 | supporting | `other/displays.md` |
| `Wire` **·** | — | framework package | 1 | core | `core/wire-spi.md` |
| `lewisxhe/XPowersLib` | `^0.2.7` | registry, range | 3 | supporting | `other/power.md` |

| Library | Token | Source files |
|---|---|---|
| `RadioLib` | `RadioLib` | 94 |
| `Wire` | `\bWire\b` | 149 |
| `SPI` | `\bSPI\b` | 83 |
| `RTClib` | `RTClib` | 11 |
| `Melopero RV3028` | `RV3028` | 1 |
| `CayenneLPP` | `CayenneLPP` | 24 |
| `Crypto (rweather)` | `<AES\.h>|<SHA256\.h>|<Ed25519\.h>` | 5 |
| `ed25519 (vendored)` | `ed25519_|ed_25519\.h` | 8 |
| `CustomLFS` | `CustomLFS` | 2 |
| `SubGhz` | `SubGhz|STM32WL` | 11 |
| `ESPAsyncWebServer` | `ESPAsyncWebServer|AsyncWebServer` | 3 |
| `AsyncElegantOTA` | `AsyncElegantOTA` | 3 |
| `MicroNMEA` | `MicroNMEA` | 46 |
| `SparkFun u-blox GNSS` | `SFE_UBLOX|u-blox_GNSS` | 1 |
| `base64` | `base64\.hpp|decode_base64|encode_base64` | 1 |
| `CRC32` | `<CRC32\.h>` | 3 |
| `NonBlockingRTTTL` | `rtttl::|NonBlockingRtttl` | 2 |
| `XPowersLib` | `XPowers` | 2 |
| `PCA9557-arduino` | `PCA9557` | 4 |
| `googletest` | `gtest/gtest\.h` | 1 |

<!-- library-overview:end -->

![Four routes by which libraries enter the MeshCore build: the PlatformIO
registry with a version range, the registry with a pinned version, a git or
zip URL with a tag or commit, and a local path inside the repo; alongside them
the lib/ directory that is compiled in automatically and the per-platform
framework packages, all converging on a single
build](../../images/en/introduction-1.svg)

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`variants/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/variants)
- [`lib/ed25519`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/lib/ed25519)
- [`lib/nrf52`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/lib/nrf52)
- [`src/helpers/sensors/RAK12035_SoilMoisture.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/RAK12035_SoilMoisture.h)
- [PlatformIO — Library Dependencies](https://docs.platformio.org/en/latest/projectconf/sections/env/options/library/lib_deps.html)

Translated from Dutch by Anthropic Claude
