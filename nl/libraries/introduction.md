# Libraries in MeshCore

*LIB_DEPS · OVERERVING · VERSIEBEHEER · INVENTARIS*

MeshCore is geen op zichzelf staand programma. De firmware leunt op
tweeënvijftig externe libraries, die langs vier verschillende routes de
build in komen, plus een handvol code die helemaal buiten het
afhankelijkhedenmechanisme om wordt meegecompileerd. Dit hoofdstuk laat
zien welke dat zijn, waar ze vandaan komen en waarom een build van vandaag
niet dezelfde bytes oplevert als een build van een half jaar geleden.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, de negenenzeventig `variants/*/platformio.ini`,
> `lib/`, `arch/` en `src/helpers/sensors/`.

## Wat een `lib_dep` is

PlatformIO beschrijft een project in `platformio.ini`. Onder de sleutel
`lib_deps` staat per sectie welke libraries die sectie nodig heeft. Bij het
bouwen haalt PlatformIO die op — uit zijn eigen registry, van een URL of van
een pad op schijf — pakt ze uit in `.pio/libdeps/<omgeving>/` en zet ze op
het includepad van de compiler.

MeshCore heeft tachtig van die bestanden: de `platformio.ini` in de
projectroot plus negenenzeventig in `variants/`. De root laadt ze allemaal
in via `extra_configs`:

`platformio.ini` r.11-14

```text
[platformio]
extra_configs =
  variants/*/platformio.ini
  platformio.local.ini
```

Samen declareren die tachtig bestanden tweeënvijftig unieke libraries. De
root noemt er achtentwintig; de rest komt uit de varianten.

## De vier binnenhaalroutes

**Registry met een versiebereik.** De gewone vorm. De naam bestaat uit een
auteursprefix en een librarynaam, gevolgd door een bereik met `^` of `~`.

`platformio.ini` r.22

```text
  jgromes/RadioLib @ ^7.6.0
```

**Registry, exact vastgepind.** Zonder `^` of `~` staat er precies één
versie. In de hele repo gebeurt dat bij vier libraries.

`platformio.ini` r.26

```text
  electroniccats/CayenneLPP @ 1.6.1
```

**Git-tag of zip met een commit-hash.** PlatformIO accepteert een URL. Achter
`#` staat een tag of commit; wat daar staat, bepaalt wat je krijgt.

`platformio.ini` r.95

```text
  https://github.com/oltaco/CustomLFS#0.2.2
```

In `variants/` staan daarnaast vier URL-declaraties. Drie daarvan halen een
zip van een volledige commit-hash binnen: `NMIoT/meshsolar` en de twee forks
van `heltec-eink-modules`, van `Quency-D` en van `todd-herbert`. De vierde,
`SoulOfNoob/GxEPD2`, is een `.git`-URL zonder revisie erachter en ligt dus
niet vast.

**Lokaal pad.** Code die in de MeshCore-repo zelf staat, aangewezen met
`file://`. Er is geen upstream om vanaf te halen en geen versienummer om te
verhogen.

`platformio.ini` r.70

```text
  file://arch/esp32/AsyncElegantOTA
```

`platformio.ini` r.119

```text
  file://arch/stm32/Adafruit_LittleFS_stm32
```

## Wat er buiten `lib_deps` om binnenkomt

Niet alle externe code loopt via `lib_deps`. PlatformIO compileert alles in
de map `lib/` automatisch mee. MeshCore gebruikt dat voor twee dingen:

- `lib/ed25519` — een C-implementatie van Ed25519, meegeleverd in de repo.
  Zie [`core/crypto.md`](core/crypto.md), waar hij naast de
  Ed25519 van `rweather/Crypto` staat.
- `lib/nrf52` — headers en de SoftDevice-API `s140_nrf52_7.3.0_API` voor
  het nRF52-platform.

Daarnaast staat er een complete sensordriver gewoon in de broncode:
`src/helpers/sensors/RAK12035_SoilMoisture.h` en `.cpp`. Die komt in geen
enkele `lib_deps`-regel voor. Zie [`other/sensors.md`](other/sensors.md).

## Frameworklibraries

Twee regels in `[arduino_base]` hebben geen auteursprefix en geen versie:

`platformio.ini` r.20-21

```text
  SPI
  Wire
```

Dat zijn geen registrypakketten maar frameworklibraries: ze zitten in het
frameworkpakket van het platform zelf. Op ESP32 komen ze uit Arduino-ESP32,
op nRF52 uit de Adafruit nRF52-core, op RP2040 uit arduino-pico en op STM32
uit STM32duino. De naam is hetzelfde, de implementatie niet. Hetzelfde geldt
voor `SubGhz` op r.120. Zie [`core/wire-spi.md`](core/wire-spi.md) en
[`core/subghz.md`](core/subghz.md).

## Overerving

`[arduino_base]` bevat zeven `lib_deps`-regels. Elke variant erft daarvan,
direct of via een platformsectie, en daarmee gelden die zeven voor alle 507
build-targets in de repo. Het achtste target, `[env:native]`, is geen
Arduino-build en erft niets.

De platformsecties gaan daar op twee manieren mee om:

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

`[esp32_base]` definieert zelf helemaal geen `lib_deps` en houdt dus wat
`extends` hem geeft. `[nrf52_base]` (r.93) en `[stm32_base]` (r.118) hebben
wél een eigen `lib_deps`, en die vervangt de geërfde sleutel in plaats van
hem aan te vullen. Daarom moeten die twee `${arduino_base.lib_deps}`
expliciet herhalen: zonder die regel zouden RadioLib, Crypto, RTClib,
RV3028 en CayenneLPP van het nRF52- en STM32-platform verdwijnen.

Zulke `${sectie.lib_deps}`-verwijzingen komen 572 keer voor in de tachtig
bestanden. `tools/library-overview.py` lost ze bewust niet op, want dan zou
niet meer zichtbaar zijn welke variant van welke basis erft.

## Wat `^` betekent

`^7.6.0` staat voor: minimaal 7.6.0, maar onder 8.0.0. `~2.0.6` is nauwer —
minimaal 2.0.6, onder 2.1.0. `1.6.1` zonder teken is precies die versie.

Het gevolg is dat de meeste libraries in deze lijst niet vastliggen. Wie
vandaag bouwt met `jgromes/RadioLib @ ^7.6.0` krijgt de nieuwste 7.x die op
dat moment in de registry staat; wie dat een half jaar geleden deed kreeg
een andere. De firmware is reproduceerbaar in gedrag, niet in bytes. Alleen
de vier exact vastgepinde libraries, de tagged git-URL en de twee lokale
paden leveren over de tijd hetzelfde resultaat.

## Inventaris

Alle tweeënvijftig libraries, met de route waarlangs ze binnenkomen, in
hoeveel van de tachtig `platformio.ini`-bestanden ze gedeclareerd staan, en
het hoofdstuk waar ze behandeld worden. Een `·` achter de naam betekent: ook
in de root gedeclareerd.

De tweede tabel telt in hoeveel firmwarebronbestanden een library
daadwerkelijk genoemd wordt. Geteld wordt over de 590 bestanden met de
extensie `.h`, `.hpp`, `.c`, `.cpp` of `.ino` onder `src/`, `examples/`,
`test/`, `arch/`, `lib/` en `variants/`; de kolom *Token* geeft het
zoekpatroon, zodat het cijfer na te rekenen is.

<!-- library-overview:start -->

*Gegenereerd met `tools/library-overview.py` tegen commit `03b6ef4`.*

| Library | Versie | Route | `.ini` | Soort | Hoofdstuk |
|---|---|---|---|---|---|
| `adafruit/Adafruit AHTX0` **·** | `^2.0.5` | registry, range | 3 | ondersteunend | `other/sensors.md` |
| `adafruit/Adafruit BME280 Library` **·** | `^2.3.0` | registry, range | 6 | ondersteunend | `other/sensors.md` |
| `adafruit/Adafruit BME680 Library` **·** | `^2.0.4` | registry, range | 1 | ondersteunend | `other/sensors.md` |
| `adafruit/Adafruit BMP085 Library` **·** | `^1.2.4` | registry, range | 1 | ondersteunend | `other/sensors.md` |
| `adafruit/Adafruit BMP280 Library` **·** | `^2.6.8` | registry, range | 2 | ondersteunend | `other/sensors.md` |
| `adafruit/Adafruit BusIO` | `^1.17.2` | registry, range | 1 | ondersteunend | `other/displays.md` |
| `adafruit/Adafruit EPD` | `4.6.1` | registry, pinned | 1 | ondersteunend | `other/displays.md` |
| `adafruit/Adafruit GFX Library` | `^1.12.1` | registry, range | 8 | ondersteunend | `other/displays.md` |
| `adafruit/Adafruit INA219` **·** | `^1.2.3` | registry, range | 3 | ondersteunend | `other/power.md` |
| `adafruit/Adafruit INA260 Library` **·** | `^1.5.3` | registry, range | 1 | ondersteunend | `other/power.md` |
| `adafruit/Adafruit INA3221 Library` **·** | `^1.0.1` | registry, range | 3 | ondersteunend | `other/power.md` |
| `adafruit/Adafruit LIS3DH` | `^1.2.4` | registry, range | 1 | ondersteunend | `other/peripherals.md` |
| `adafruit/Adafruit MLX90614 Library` **·** | `^2.1.5` | registry, range | 1 | ondersteunend | `other/sensors.md` |
| `adafruit/Adafruit NeoPixel` | `^1.10.0` · `^1.12.3` | registry, range | 3 | ondersteunend | `other/peripherals.md` |
| `adafruit/Adafruit SH110X` | `^2.1.13` · `~2.1.13` | registry, range | 7 | ondersteunend | `other/displays.md` |
| `adafruit/Adafruit SHT4x Library` | `^1.0.4` | registry, range | 1 | ondersteunend | `other/sensors.md` |
| `adafruit/Adafruit SHTC3 Library` **·** | `^1.0.1` | registry, range | 1 | ondersteunend | `other/sensors.md` |
| `adafruit/Adafruit SSD1306` | `^2.5.13` | registry, range | 23 | ondersteunend | `other/displays.md` |
| `adafruit/Adafruit ST7735 and ST7789 Library` | `^1.11.0` | registry, range | 6 | ondersteunend | `other/displays.md` |
| `file://arch/stm32/Adafruit_LittleFS_stm32` **·** | — | local path | 1 | kern | `core/littlefs-stm32.md` |
| `adafruit/Adafruit_VL53L0X` **·** | `^1.2.4` | registry, range | 1 | ondersteunend | `other/sensors.md` |
| `arduino-libraries/Arduino_LPS22HB` **·** | `^1.0.2` | registry, range | 1 | ondersteunend | `other/sensors.md` |
| `file://arch/esp32/AsyncElegantOTA` **·** | — | local path | 1 | kern | `core/asyncelegantota.md` |
| `densaugeo/base64` | `~1.4.0` | registry, range | 76 | ondersteunend | `other/utilities.md` |
| `finitespace/BME280` | `^3.0.0` | registry, range | 1 | ondersteunend | `other/sensors.md` |
| `boschsensortec/BSEC Software Library` | `^1.8.1492` | registry, range | 2 | ondersteunend | `other/sensors.md` |
| `electroniccats/CayenneLPP` **·** | `1.6.1` | registry, pinned | 1 | kern | `core/cayenne-lpp.md` |
| `bakercp/CRC32` | `^2.0.0` | registry, range | 15 | ondersteunend | `other/utilities.md` |
| `rweather/Crypto` **·** | `^0.4.0` | registry, range | 3 | kern | `core/crypto.md` |
| `oltaco/CustomLFS` **·** | `0.2.2` | git/zip URL | 1 | kern | `core/custom-lfs.md` |
| `ESP32Async/ESPAsyncWebServer` **·** | `3.10.3` | registry, pinned | 1 | kern | `core/espasyncwebserver.md` |
| `google/googletest` **·** | `1.17.0` | registry, pinned | 1 | ondersteunend | `other/testing.md` |
| `zinggjm/GxEPD2` | `1.6.2` | registry, pinned | 5 | ondersteunend | `other/displays.md` |
| `SoulOfNoob/GxEPD2` | — | git/zip URL | 1 | ondersteunend | `other/displays.md` |
| `Quency-D/heltec-eink-modules` | `563dd41` | git/zip URL | 2 | ondersteunend | `other/displays.md` |
| `todd-herbert/heltec-eink-modules` | `9207eb6` | git/zip URL | 1 | ondersteunend | `other/displays.md` |
| `robtillaart/INA226` **·** | `^0.6.4` | registry, range | 1 | ondersteunend | `other/power.md` |
| `lovyan03/LovyanGFX` | `^1.2.7` | registry, range | 1 | ondersteunend | `other/displays.md` |
| `melopero/Melopero RV3028` **·** | `^1.1.0` | registry, range | 1 | kern | `core/rv3028.md` |
| `NMIoT/meshsolar` | `dfc5330` | git/zip URL | 1 | ondersteunend | `other/power.md` |
| `stevemarple/MicroNMEA` **·** | `^2.0.6` · `~2.0.6` | registry, range | 20 | ondersteunend | `other/gps.md` |
| `end2endzone/NonBlockingRTTTL` | `^1.3.0` | registry, range | 17 | ondersteunend | `other/peripherals.md` |
| `maxpromer/PCA9557-arduino` | — | registry, no version | 1 | ondersteunend | `other/peripherals.md` |
| `jgromes/RadioLib` **·** | `^7.6.0` | registry, range | 1 | kern | `core/radiolib.md` |
| `adafruit/RTClib` **·** | `^2.1.3` | registry, range | 7 | kern | `core/rtclib.md` |
| `sensirion/Sensirion I2C SHT4x` **·** | `^1.1.2` | registry, range | 1 | ondersteunend | `other/sensors.md` |
| `sparkfun/SparkFun u-blox GNSS Arduino Library` | `^2.2.27` | registry, range | 6 | ondersteunend | `other/gps.md` |
| `SPI` **·** | — | framework package | 1 | kern | `core/wire-spi.md` |
| `SubGhz` **·** | — | framework package | 1 | kern | `core/subghz.md` |
| `olikraus/U8g2` | `^2.35.19` | registry, range | 1 | ondersteunend | `other/displays.md` |
| `Wire` **·** | — | framework package | 1 | kern | `core/wire-spi.md` |
| `lewisxhe/XPowersLib` | `^0.2.7` | registry, range | 3 | ondersteunend | `other/power.md` |

| Library | Token | Bronbestanden |
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

![Vier routes waarlangs libraries de MeshCore-build binnenkomen: de
PlatformIO-registry met een versiebereik, de registry met een vastgepinde
versie, een git- of zip-URL met tag of commit, en een lokaal pad in de repo;
daarnaast de map lib/ die automatisch meegecompileerd wordt en de
frameworkpakketten per platform, alles uitkomend op één
build](../../images/nl/introduction-1.svg)

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`variants/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/variants)
- [`lib/ed25519`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/lib/ed25519)
- [`lib/nrf52`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/lib/nrf52)
- [`src/helpers/sensors/RAK12035_SoilMoisture.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/RAK12035_SoilMoisture.h)
- [PlatformIO — Library Dependencies](https://docs.platformio.org/en/latest/projectconf/sections/env/options/library/lib_deps.html)
