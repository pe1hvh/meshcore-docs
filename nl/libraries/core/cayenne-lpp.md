# CayenneLPP

*TELEMETRIE · DRAADFORMAAT · EXACT VASTGEPIND · KANALEN*

CayenneLPP bepaalt hoe MeshCore sensorwaarden op de draad zet. Het is de
enige library in `[arduino_base]` die op een exacte versie is vastgepind, en
dat is te begrijpen: de library codeert geen data voor intern gebruik maar
het formaat waarin twee nodes telemetrie uitwisselen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, `src/helpers/SensorManager.h`,
> `src/helpers/sensors/EnvironmentSensorManager.cpp` en
> `examples/kiss_modem/KissModem.cpp`.

## Wat het doet

Cayenne Low Power Payload is een compact binair formaat voor sensordata,
oorspronkelijk bedacht voor LoRaWAN. Elke meting bestaat uit een kanaalnummer,
een typecode en de waarde in een vaste schaal — temperatuur in stapjes van
0,1 °C, luchtdruk in stapjes van 0,1 hPa, enzovoort. Daardoor past een
volledige sensoruitlezing in enkele tientallen bytes, zonder veldnamen en
zonder scheidingstekens. De implementatie die MeshCore gebruikt is die van
Electronic Cats,
[github.com/ElectronicCats/CayenneLPP](https://github.com/ElectronicCats/CayenneLPP).

## Hoe MeshCore hem binnenhaalt

`platformio.ini` r.26

```text
  electroniccats/CayenneLPP @ 1.6.1
```

Geen `^`, geen `~`: precies 1.6.1. De regel staat in `[arduino_base]`, dus
alle 507 build-targets krijgen hem. Via zijn `library.json` sleept
CayenneLPP `bblanchon/ArduinoJson` mee — zie
[`../dependencies.md`](../dependencies.md).

Het exacte pin is opvallend omdat de andere zes regels in dezelfde sectie
wél een bereik hebben. Een verklaring staat nergens in de repo. Het
vermóéden ligt voor de hand dat het met het draadformaat te maken heeft:
verandert de codering, dan verstaan twee nodes met verschillende versies
elkaar niet meer. Dat is een vermoeden, geen vastgestelde reden.

## Hoe MeshCore hem gebruikt

CayenneLPP zit in de kern van de sensorabstractie. `SensorManager` geeft een
`CayenneLPP`-object door aan wie sensoren uitleest:

`src/helpers/SensorManager.h` r.3

```cpp
#include <CayenneLPP.h>
```

`src/helpers/SensorManager.h` r.19

```cpp
  virtual bool querySensors(uint8_t requester_permissions, CayenneLPP& telemetry) { return false; }
```

Elke sensordriver schrijft rechtstreeks in dat object. De
`query_*`-functies in `EnvironmentSensorManager.cpp` doen niets anders:

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.246-251

```cpp
static void query_ahtx0(uint8_t ch, uint8_t, CayenneLPP& lpp) {
  sensors_event_t humidity, temp;
  AHTX0.getEvent(&humidity, &temp);
  lpp.addTemperature(ch, temp.temperature);
  lpp.addRelativeHumidity(ch, humidity.relative_humidity);
}
```

Aan de andere kant van de keten wordt de buffer uitgelezen en verstuurd:

`examples/kiss_modem/KissModem.cpp` r.557-560

```cpp
  uint8_t permissions = data[0];
  CayenneLPP telemetry(255);
  if (_sensors.querySensors(permissions, telemetry)) {
    writeHardwareFrame(HW_RESP(HW_CMD_GET_SENSORS), telemetry.getBuffer(), telemetry.getSize());
```

De tekst `CayenneLPP` komt voor in 24 van de 590 bronbestanden.

## Wat het voor een node betekent

Alles wat een node aan sensordata verstuurt, gaat door dit formaat heen. Het
kanaalnummer waaronder een meting verschijnt, wordt bij het opstarten
toegekend in de volgorde waarin sensoren gedetecteerd worden — kanaal 1 is
gereserveerd voor de node zelf (`TELEM_CHANNEL_SELF`), de eerste gevonden
sensor krijgt kanaal 2. Twee nodes met verschillende sensoren hebben dus
niet dezelfde kanaalindeling.

Omdat de library exact vastgepind is, levert een build van vandaag hier
hetzelfde gedrag als een build van vorig jaar. Dat geldt niet voor de
libraries met een `^`-bereik.

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/SensorManager.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/SensorManager.h)
- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/EnvironmentSensorManager.cpp)
- [`examples/kiss_modem/KissModem.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/kiss_modem/KissModem.cpp)
- [ElectronicCats/CayenneLPP](https://github.com/ElectronicCats/CayenneLPP)
