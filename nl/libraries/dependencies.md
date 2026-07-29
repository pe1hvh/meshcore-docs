# Afhankelijkheden tussen libraries

*DEPENDS · TRANSITIEF · LDF · VERBORGEN CODE*

Een library die je binnenhaalt kan zelf ook weer libraries nodig hebben.
PlatformIO regelt dat zonder erover te rapporteren: er verschijnt code in de
build die in geen enkele `platformio.ini` genoemd wordt. Dit hoofdstuk maakt
die laag zichtbaar — zes libraries die nergens gedeclareerd staan en toch
meegecompileerd worden, en een handvol afhankelijkheden die niet door de
driver maar door de voorbeeldschetsen van een library gevraagd worden.

> [!NOTE]
> **Bron.** Deze pagina is als enige in de repo niet uitsluitend op de
> MeshCore-broncode gebaseerd. De afhankelijkheden komen uit de
> `library.properties` en `library.json` van de upstream-repo's, opgehaald
> van `raw.githubusercontent.com` op 28 juli 2026 met
> `tools/library-overview.py`. De declaraties zelf zijn geverifieerd tegen
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — `platformio.ini` en
> de negenenzeventig `variants/*/platformio.ini`.

## Hoe PlatformIO afhankelijkheden vindt

Twee mechanismen werken naast elkaar.

Het eerste is de metadata van de library zelf. Een Arduino-library heeft een
`library.properties` met een regel `depends=`, een PlatformIO-library een
`library.json` met een sleutel `"dependencies"`. Wat daar staat, wordt
opgehaald alsof het in `lib_deps` had gestaan.

Het tweede is de Library Dependency Finder. De LDF scant de broncode op
`#include`-regels en zoekt daar libraries bij, ook als niemand ze heeft
gedeclareerd. In de standaardmodus `chain` kijkt hij daarbij in de bestanden
die daadwerkelijk gecompileerd worden. Het resultaat is dat een build meer
kan bevatten dan wat je opschreef, en dat je dat nergens terugziet zolang
alles compileert.

## De zes libraries die nergens gedeclareerd staan

Deze zes staan in geen enkele van de tachtig `platformio.ini`-bestanden en
komen toch in de build terecht:

| Library | Komt binnen via | Reikwijdte |
|---|---|---|
| `bblanchon/ArduinoJson` | `electroniccats/CayenneLPP` | alle 507 builds |
| `Adafruit Unified Sensor` | BME280, BMP280, BMP085, BME680, AHTX0, SHTC3, LIS3DH, SHT4x | sensorbuilds |
| `Sensirion Core` | `Sensirion I2C SHT4x` | sensorbuilds |
| `ESP32Async/AsyncTCP` | `ESPAsyncWebServer` | ESP32 met WiFi-OTA |
| `Adafruit seesaw Library` | `Adafruit ST7735 and ST7789` | zes TFT-varianten |
| `SD` | `Adafruit ST7735 and ST7789` | zes TFT-varianten |

De eerste rij is de opvallendste. `CayenneLPP` staat in `[arduino_base]` en
geldt dus voor alle 507 build-targets; zijn `library.json` noemt
`bblanchon/ArduinoJson` als afhankelijkheid. Daarmee zit er een JSON-parser
in élke MeshCore-build, ook in die van een repeater die nooit JSON ziet.

`Adafruit Unified Sensor` is de gedeelde sensorabstractie van Adafruit; acht
van de vijftien sensorlibraries in `[sensor_base]` vragen erom. `SD` en
`Adafruit seesaw Library` komen mee met de ST7735/ST7789-driver, ook op
borden zonder kaartlezer.

## De volledige `depends=`-tabel

Per gedeclareerde library wat zijn eigen metadata opgeeft. Gegenereerd met
`tools/library-overview.py`; een lege cel betekent dat de library geen
afhankelijkheden declareert.

<!-- library-overview:start -->

*Gegenereerd met `tools/library-overview.py` tegen commit `03b6ef4`.*

| Library | Hangt af van | Bron |
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
| `googletest` | *niet opgehaald — no Arduino metadata; the registry package carries no library.json* | — |
| `GxEPD2` | `Adafruit GFX Library` | `library.properties` |
| `INA226` | — | `library.properties` |
| `LovyanGFX` | — | `library.properties` |
| `Melopero RV3028` | *niet opgehaald — repository not found under the expected name on GitHub* | — |
| `MicroNMEA` | — | `library.properties` |
| `NonBlockingRTTTL` | — | `library.properties` |
| `PCA9557-arduino` | — | `library.properties` |
| `RadioLib` | — | `library.properties` |
| `RTClib` | `Adafruit BusIO` | `library.properties` |
| `Sensirion I2C SHT4x` | `Sensirion Core` | `library.properties` |
| `SparkFun u-blox GNSS Arduino Library` | — | `library.properties` |
| `SPI` | *niet opgehaald — framework library, ships with the platform package* | — |
| `SubGhz` | *niet opgehaald — framework library, ships with framework-arduinoststm32* | — |
| `U8g2` | — | `library.properties` |
| `Wire` | *niet opgehaald — framework library, ships with the platform package* | — |
| `XPowersLib` | — | `library.properties` |

<!-- library-overview:end -->

![Afhankelijkheidsgraaf van de MeshCore-libraries: gedeclareerde libraries
verwijzen naar de libraries die zij zelf meebrengen, met ArduinoJson,
Adafruit Unified Sensor, Sensirion Core, AsyncTCP, Adafruit seesaw en SD in
een afwijkende kleur omdat die in geen enkele platformio.ini
staan](../../images/nl/dependencies-1.svg)

## Afhankelijkheden van voorbeeldschetsen

Een `depends=` zegt niets over de vraag wélk deel van de library iets nodig
heeft. Bij vijf Adafruit-libraries slaat de opgave op de `examples/`-map, niet
op de driver:

| Library | Declareert | Nodig voor |
|---|---|---|
| `Adafruit INA219` | NeoPixel, GFX, SSD1306, BusIO | voorbeeldschetsen |
| `Adafruit INA260` | BusIO, NeoPixel | voorbeeldschetsen |
| `Adafruit_VL53L0X` | SSD1306, GFX | voorbeeldschetsen |
| `Adafruit BME680` | Unified Sensor, GFX, SSD1306, BusIO | voorbeeldschetsen |
| `Adafruit AHTX0` | Unified Sensor, BusIO, SH110X | voorbeeldschetsen |

Het gevolg is concreet: wie `[sensor_base]` aanzet, haalt via een stroommeter
twee displaylibraries binnen. De `-w`-vlag in `[arduino_base]` onderdrukt
alle compilerwaarschuwingen, dus daar verschijnt geen enkel signaal over:

`platformio.ini` r.27

```text
build_flags = -w -DNDEBUG -DRADIOLIB_STATIC_ONLY=1 -DRADIOLIB_GODMODE=1
```

## Handmatig vastgepinde transitieve afhankelijkheden

`adafruit/Adafruit GFX Library @ ^1.12.1` staat in acht varianten expliciet in
`lib_deps`, terwijl `Adafruit SSD1306` hem via zijn eigen `depends=` al
meebrengt. `adafruit/Adafruit BusIO @ ^1.17.2` staat in één variant expliciet:

`variants/sensecap_indicator-espnow/platformio.ini` r.31-33

```text
lib_deps=${esp32_base.lib_deps}
  adafruit/Adafruit BusIO @ ^1.17.2
  lovyan03/LovyanGFX @ ^1.2.7
```

Dat is geen dubbeling. Een transitieve afhankelijkheid heeft geen eigen
versiebereik in de build; door hem alsnog te declareren wordt de versie van
een library die je nooit rechtstreeks gebruikt, toch vastgelegd.

## Niet geverifieerd

De afhankelijkheden van `melopero/Melopero RV3028` konden niet worden
opgehaald: de `library.properties` was niet te vinden en de repo staat niet
onder de verwachte naam op GitHub. Die rij blijft leeg, met de reden erbij.
`google/googletest` heeft geen Arduino-metadata; het registrypakket bevat
geen `library.json`. De drie frameworklibraries `SPI`, `Wire` en `SubGhz`
hebben per definitie geen upstream-metadata.

## Drie declaraties zonder vindbare include

> [!NOTE]
> Drie libraries worden wel gedeclareerd, maar in `src/`, `examples/`,
> `variants/` en `arch/` is geen enkele `#include` van hun headers te
> vinden. Het gaat om `adafruit/Adafruit EPD @ 4.6.1`
> (`variants/mesh_pocket/platformio.ini` r.30) en
> `adafruit/Adafruit LIS3DH @ ^1.2.4` plus
> `adafruit/Adafruit SHT4x Library @ ^1.0.4`
> (`variants/wio_wm1110/platformio.ini` r.36-37). Gezocht is op de
> headernamen `Adafruit_EPD`, `Adafruit_LIS3DH` en `Adafruit_SHT4x` over
> alle bestanden met de extensie `.h`, `.hpp`, `.c`, `.cpp` en `.ino`. De
> SHT4x-sensor wordt in de firmware bediend door `SensirionI2cSht4x`
> (`src/helpers/sensors/EnvironmentSensorManager.cpp` r.90-91), niet door de
> Adafruit-library. Dit is een waarneming; er wordt hier geen conclusie aan
> verbonden.

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`variants/mesh_pocket/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/mesh_pocket/platformio.ini)
- [`variants/wio_wm1110/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/wio_wm1110/platformio.ini)
- [`variants/sensecap_indicator-espnow/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/sensecap_indicator-espnow/platformio.ini)
- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/EnvironmentSensorManager.cpp)
- [PlatformIO — Library Dependency Finder](https://docs.platformio.org/en/latest/librarymanager/ldf.html)
