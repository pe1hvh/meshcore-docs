# De I²C-bus

*TWEE DRADEN · ADRESSEN 0x08–0x77 · SCANNEN VOOR GEBRUIKEN · WIRE EN WIRE1*

I²C is de bus waar alles aan hangt wat niet snel hoeft: het scherm, de
realtimeklok, de sensoren, soms de GPS. Twee draden, een adres per apparaat,
en een firmware die niet vooraf weet wat er zit. Dit hoofdstuk beschrijft
hoe MeshCore de bus afzoekt, waarom dat vóór elke sensorlibrary gebeurt, en
wanneer een node een tweede bus gebruikt.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/sensors/EnvironmentSensorManager.cpp`,
> `src/helpers/AutoDiscoverRTCClock.cpp` en de `PIN_BOARD_SDA`-vlaggen in
> `variants/`.

![Schema van de I²C-bus: SDA en SCL met pull-ups, de SoC als master en
scherm, klok en sensoren als slaves, elk met een eigen
adres](../../../images/nl/i2c-1.svg)

## Twee draden, twee pinnen

De bus heeft één datalijn (`SDA`) en één kloklijn (`SCL`). Welke pinnen dat
zijn legt de variant vast:

`variants/lilygo_tbeam_1w/platformio.ini`

```ini
  ; I2C pins
  -D PIN_BOARD_SDA=8
  -D PIN_BOARD_SCL=9
```

53 van de 79 variantmappen zetten `PIN_BOARD_SDA`; geteld per map over
`variants/`, uitgecommentarieerde regels niet meegerekend. De rest gebruikt
de standaardpinnen van het Arduino-board of heeft geen I²C-apparaten aan
boord.

`Wire` is de naam van die bus in de Arduino-wereld. Dat is een
frameworklibrary en geen PlatformIO-pakket — zie
[Wire en SPI](../../libraries/core/wire-spi.md).

## Scannen voordat er iets wordt aangesproken

Het opvallendste aan de I²C-afhandeling in MeshCore is de volgorde. De
firmware zoekt eerst de hele bus af en start pas dáárna de libraries van de
apparaten die geantwoord hebben:

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.220-225

```cpp
static void scanI2CBus(TwoWire* wire, bool found[128]) {
  for (uint8_t addr = 0x08; addr < 0x78; addr++) {
    wire->beginTransmission(addr);
    found[addr] = (wire->endTransmission() == 0);
  }
}
```

Adressen `0x08` tot en met `0x77`. De adressen daarbuiten zijn in de
I²C-standaard gereserveerd en worden niet geprobeerd. Een apparaat dat
bevestigt (`endTransmission()` geeft nul) wordt genoteerd; verder gebeurt er
nog niets.

Het commentaar erboven zegt waarom die volgorde ertoe doet:

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.215-218

```cpp
// Probes every valid address and records which ones ACK.
// This runs before any sensor library is touched, so a missing
// or misbehaving device cannot stall or crash the boot sequence.
```

Een sensorlibrary die een apparaat aanspreekt dat er niet is, kan blijven
wachten of vastlopen. Door eerst te scannen en daarna alleen de gevonden
adressen te initialiseren kan een ontbrekende of kapotte sensor het opstarten
niet ophouden. Welke sensoren dat zijn en welke libraries erbij horen staat
in [Sensorlibraries](../../libraries/other/sensors.md).

## De klok scant niet, die probeert vier adressen

Voor de realtimeklok gaat het anders. Daar staan vier adressen hard in de
code en wordt elk apart geprobeerd:

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

| Chip | Adres |
|---|---|
| DS3231 | `0x68` |
| RV3028 | `0x52` |
| PCF8563 | `0x51` |
| RX8130CE | `0x32` |

Dezelfde techniek — een transmissie beginnen en kijken of er bevestigd wordt
— maar gericht in plaats van breed. Er zijn maar vier ondersteunde klokken,
dus een volledige scan zou niets extra's opleveren. De DS3231-test is
bovendien uit te zetten met `DISABLE_DS3231_PROBE`, omdat sommige borden op
`0x68` iets anders hebben zitten.

## Twee bussen op sommige borden

Sensoren hoeven niet op dezelfde bus te zitten als het scherm:

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.6-8

```cpp
#define TELEM_WIRE &Wire1  // Use Wire1 as the I2C bus for Environment Sensors
// ...
#define TELEM_WIRE &Wire  // Use default I2C bus for Environment Sensors
```

`TELEM_WIRE` verwijst naar `Wire1` op borden die een tweede bus hebben, en
anders naar `Wire`. Elke sensorlibrary krijgt die verwijzing mee bij het
aanmaken. Een tweede bus is nuttig als het scherm de eerste bus druk bezet
houdt, of als een sensor een adres gebruikt dat al bezet is.

> [!NOTE]
> Een adresbotsing is op I²C niet op te lossen in software. Twee apparaten
> op hetzelfde adres op dezelfde bus antwoorden allebei en het resultaat is
> onbruikbaar. De tweede bus is dan de enige uitweg — of een sensor met een
> instelbaar adres.

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/sensors/EnvironmentSensorManager.cpp)
  — `scanI2CBus()` en `TELEM_WIRE`
- [`src/helpers/AutoDiscoverRTCClock.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/AutoDiscoverRTCClock.cpp)
  — de vier klokadressen en `i2c_probe()`
- [`variants/lilygo_tbeam_1w/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/lilygo_tbeam_1w/platformio.ini)
  — `PIN_BOARD_SDA` en `PIN_BOARD_SCL` van één bord

Verwante hoofdstukken:

- [De SPI-bus](spi.md) — de snelle bus ernaast
- [Wire en SPI](../../libraries/core/wire-spi.md) — waarom dit
  frameworklibraries zijn en geen pakketten
- [Het scherm](../peripherals/display.md) — het meest voorkomende
  I²C-apparaat
- [GPS](../peripherals/gps.md) — GPS over I²C in plaats van serieel
- [Sensorlibraries](../../libraries/other/sensors.md) — wat er na de scan
  wordt geïnitialiseerd
