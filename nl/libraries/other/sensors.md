# Sensorlibraries

*SENSOR_BASE · ENV_INCLUDE · QUERY_ · LPP*

Zeventien sensorlibraries zitten in de firmware, en ze worden allemaal op
dezelfde manier aangeroepen: een `init_`-functie, een `query_`-functie en een
regel in één tabel. Wat er in een build zit, bepaalt een reeks
`ENV_INCLUDE_*`-vlaggen: zonder vlag geen driver. Dat is precies het
omgekeerde van hoe RadioLib zijn protocollen behandelt — zie
[`../library-configuration.md`](../library-configuration.md). Eén sensordriver
hoort er wel bij maar staat in geen enkele `lib_deps`-regel.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini` r.122-154, `src/helpers/sensors/EnvironmentSensorManager.cpp`
> en `src/helpers/sensors/RAK12035_SoilMoisture.h`.

## Hoe MeshCore deze groep aanroept

Alle omgevingssensoren zitten in één bestand,
`EnvironmentSensorManager.cpp`, elk achter een eigen `#if ENV_INCLUDE_*`.
Per sensor staan er twee functies: één om hem te initialiseren, één om hem
uit te lezen. Die laatste schrijft rechtstreeks in een `CayenneLPP`-buffer:

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

Die twee functies worden samen met het I²C-adres in één tabel gezet:

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

Bij het opstarten loopt MeshCore die tabel af, probeert elk adres op de
I²C-bus en kent aan elke gevonden sensor een LPP-kanaal toe, in de volgorde
van de tabel. Toevoegen van een sensor is dus: een library declareren, een
`ENV_INCLUDE_`-vlag, twee functies en één regel in de tabel.

![Van bouwvlag naar telemetriepakket: de ENV_INCLUDE-vlaggen bepalen welke
sensorcode meegecompileerd wordt, de sensortabel koppelt elk I²C-adres aan
een init- en een query-functie, en die query-functies schrijven hun waarden
in één CayenneLPP-buffer die als telemetriepakket de mesh in
gaat](../../../images/nl/sensors-1.svg)

## De vijftien uit `[sensor_base]`

De sectie `[sensor_base]` (`platformio.ini` r.122-154) zet vijftien vlaggen
en declareert vijftien libraries. Wie de sectie aanroept, krijgt ze alle
vijftien.

`platformio.ini` r.139-144

```text
lib_deps =
  adafruit/Adafruit INA3221 Library @ ^1.0.1
  adafruit/Adafruit INA219 @ ^1.2.3
  robtillaart/INA226 @ ^0.6.4
  adafruit/Adafruit INA260 Library @ ^1.5.3
  adafruit/Adafruit AHTX0 @ ^2.0.5
```

**`Adafruit AHTX0`** bedient de AHT10 en AHT20, goedkope temperatuur- en
luchtvochtigheidssensoren met een vast I²C-adres. Levert temperatuur en
relatieve vochtigheid.

**`Adafruit BME280 Library`** bedient de Bosch BME280: temperatuur,
luchtvochtigheid en luchtdruk in één behuizing. In de repo is dit de meest
voorkomende omgevingssensor buiten `[sensor_base]` om; zeven varianten
noemen een BME280-library.

**`Adafruit BMP280 Library`** is de variant zonder vochtigheidsmeting —
temperatuur en luchtdruk.

**`Adafruit BMP085 Library`** bedient de oudere BMP085 en BMP180.

**`Adafruit BME680 Library`** bedient de BME680, die naast temperatuur,
vochtigheid en druk ook een gasweerstand meet. Zijn `depends=` vraagt om GFX
en SSD1306 voor de voorbeeldschetsen.

**`Adafruit SHTC3 Library`** bedient de Sensirion SHTC3, een compacte
temperatuur- en vochtigheidssensor met laag verbruik.

**`Sensirion I2C SHT4x`** bedient de SHT4x-reeks van Sensirion. Dit is de
library die de SHT4x-sensoren in de firmware daadwerkelijk aanstuurt, via
`SensirionI2cSht4x` (`EnvironmentSensorManager.cpp` r.90-91). Hij brengt
`Sensirion Core` mee, die nergens gedeclareerd staat.

**`Arduino_LPS22HB`** bedient de ST LPS22HB-luchtdruksensor, zoals die op de
Arduino Nano 33 BLE Sense zit.

**`Adafruit MLX90614 Library`** bedient een infrarood-thermometer die de
temperatuur van een oppervlak op afstand meet, naast zijn eigen
omgevingstemperatuur. Vandaar het `sub_ch`-argument in de `query_`-functie:
twee waarden uit één sensor.

**`Adafruit_VL53L0X`** bedient een time-of-flight-afstandssensor, die met
een laserpuls de afstand tot een object meet.

**`Adafruit INA219`**, **`Adafruit INA260 Library`**,
**`Adafruit INA3221 Library`** en **`robtillaart/INA226`** meten stroom en
spanning; die vier worden behandeld in [`power.md`](power.md).

**`stevemarple/MicroNMEA`** hoort ook in deze sectie thuis maar is een
GPS-library; zie [`gps.md`](gps.md).

## finitespace/BME280

Een tweede BME280-library, buiten `[sensor_base]` om, in één variant
gedeclareerd. Anders dan de Adafruit-versie gebruikt hij geen
`Adafruit Unified Sensor` en levert hij zijn waarden zonder die abstractie.

## boschsensortec/BSEC Software Library

BSEC is de gesloten softwarelaag van Bosch bovenop de BME680. Waar de
gewone library een gasweerstand in ohm oplevert, rekent BSEC dat om naar een
luchtkwaliteitsindex, met een kalibratie die over dagen loopt. In twee
varianten gedeclareerd, `lilygo_tbeam_SX1276` en `rak4631`, achter de vlag
`ENV_INCLUDE_BME680_BSEC` met een eigen `query_bme680_bsec`-functie.

## RAK12035_SoilMoisture — meegeleverd

De bodemvochtsensor RAK12035 heeft geen `lib_deps`-regel. Zijn driver staat
gewoon in de broncode, als `src/helpers/sensors/RAK12035_SoilMoisture.h` en
`.cpp`, en volgt verder exact hetzelfde patroon als de andere: een
`ENV_INCLUDE_RAK12035`-vlag, een `init_`- en een `query_rak12035`-functie en
een regel in de sensortabel. Wie de sensorlijst opmaakt uit de
`platformio.ini`-bestanden, mist deze.

## Overzicht

| Library | Versie | Varianten | Vlag |
|---|---|---|---|
| `adafruit/Adafruit AHTX0` | `^2.0.5` | 3 | `ENV_INCLUDE_AHTX0` |
| `adafruit/Adafruit BME280 Library` | `^2.3.0` | 6 | `ENV_INCLUDE_BME280` |
| `adafruit/Adafruit BMP280 Library` | `^2.6.8` | 2 | `ENV_INCLUDE_BMP280` |
| `adafruit/Adafruit BMP085 Library` | `^1.2.4` | 1 | `ENV_INCLUDE_BMP085` |
| `adafruit/Adafruit BME680 Library` | `^2.0.4` | 1 | `ENV_INCLUDE_BME680` |
| `adafruit/Adafruit SHTC3 Library` | `^1.0.1` | 1 | `ENV_INCLUDE_SHTC3` |
| `sensirion/Sensirion I2C SHT4x` | `^1.1.2` | 1 | `ENV_INCLUDE_SHT4X` |
| `adafruit/Adafruit SHT4x Library` | `^1.0.4` | 1 | geen include gevonden |
| `arduino-libraries/Arduino_LPS22HB` | `^1.0.2` | 1 | `ENV_INCLUDE_LPS22HB` |
| `adafruit/Adafruit MLX90614 Library` | `^2.1.5` | 1 | `ENV_INCLUDE_MLX90614` |
| `adafruit/Adafruit_VL53L0X` | `^1.2.4` | 1 | `ENV_INCLUDE_VL53L0X` |
| `finitespace/BME280` | `^3.0.0` | 1 | — |
| `boschsensortec/BSEC Software Library` | `^1.8.1492` | 2 | `ENV_INCLUDE_BME680_BSEC` |
| *`RAK12035_SoilMoisture`* | *meegeleverd* | *—* | `ENV_INCLUDE_RAK12035` |

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/EnvironmentSensorManager.cpp)
- [`src/helpers/sensors/RAK12035_SoilMoisture.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/RAK12035_SoilMoisture.h)
- [`src/helpers/SensorManager.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/SensorManager.h)
- [Sensirion/arduino-i2c-sht4x](https://github.com/Sensirion/arduino-i2c-sht4x)
- [boschsensortec/Bosch-BSEC2-Library](https://github.com/boschsensortec/Bosch-BSEC2-Library)
