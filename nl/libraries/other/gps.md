# GPS-libraries

*NMEA · UBX · LOCATIONPROVIDER · TIJDSYNCHRONISATIE*

Voor plaatsbepaling gebruikt MeshCore twee libraries die hetzelfde doel
dienen maar niets met elkaar gemeen hebben. De ene ontleedt tekstregels die
vrijwel elke GPS-ontvanger uitspuugt; de andere praat een binair protocol met
één specifieke fabrikant.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, `src/helpers/sensors/MicroNMEALocationProvider.h` en
> `src/helpers/sensors/EnvironmentSensorManager.cpp`.

## Hoe MeshCore deze groep aanroept

Beide libraries zitten achter dezelfde abstractie, `LocationProvider`. De
`SensorManager` levert er een op aanvraag:

`src/helpers/SensorManager.h` r.25

```cpp
  virtual LocationProvider* getLocationProvider() { return NULL; }
```

Wie een positie wil — voor de locatie in een advert, voor telemetrie of voor
het zetten van de klok — vraagt die op bij de provider en hoeft niet te weten
welke ontvanger eronder zit.

## stevemarple/MicroNMEA

NMEA 0183 is het protocol dat vrijwel elke GPS-ontvanger over een seriële
lijn uitzendt: regels tekst die met `$GP` of `$GN` beginnen, met daarin
positie, tijd, snelheid en het aantal zichtbare satellieten, afgesloten met
een controlegetal. MicroNMEA ontleedt die regels teken voor teken, zonder
buffers aan te maken en zonder dynamisch geheugen — geschreven voor
microcontrollers waar dat uitmaakt.

MeshCore gebruikt hem in `MicroNMEALocationProvider`:

`src/helpers/sensors/MicroNMEALocationProvider.h` r.3-6

```cpp
#include "LocationProvider.h"
#include <MicroNMEA.h>
#include <RTClib.h>
#include <helpers/RefCountedDigitalPin.h>
```

Dat `RTClib.h` ernaast staat, is geen toeval: de tijd uit de NMEA-regels
wordt gebruikt om de klok van de node gelijk te zetten.

Met twintig varianten is MicroNMEA de meest voorkomende sensorlibrary in de
repo. Hij staat ook in `[sensor_base]`, achter de vlag `ENV_INCLUDE_GPS`.

## sparkfun/SparkFun u-blox GNSS Arduino Library

u-blox-ontvangers spreken naast NMEA ook UBX, hun eigen binaire protocol.
Dat is compacter, levert meer velden en laat toe de ontvanger te
configureren — meetfrequentie, energiebeheer, welke satellietsystemen
gebruikt worden. Bovendien werkt het over I²C, waar NMEA meestal over een
seriële poort gaat.

MeshCore gebruikt dat voor de RAK12500, een u-blox-module aan de I²C-bus:

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.171-175

```cpp
#ifndef TELEM_RAK12500_ADDRESS
#define TELEM_RAK12500_ADDRESS   0x42     //RAK12500 Ublox GPS via i2c
#endif
#include <SparkFun_u-blox_GNSS_Arduino_Library.h>
static SFE_UBLOX_GNSS ublox_GNSS;
```

Daaronder staat `RAK12500LocationProvider`, die dezelfde
`LocationProvider`-interface implementeert als de NMEA-versie. Zes varianten
declareren de library, allemaal RAK-borden of daarvan afgeleid.

## Overzicht

| Library | Versie | Varianten | Protocol | Bus |
|---|---|---|---|---|
| `stevemarple/MicroNMEA` | `^2.0.6` · `~2.0.6` | 20 | NMEA 0183 | serieel |
| `sparkfun/SparkFun u-blox GNSS Arduino Library` | `^2.2.27` | 6 | UBX | I²C |

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/sensors/MicroNMEALocationProvider.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/MicroNMEALocationProvider.h)
- [`src/helpers/sensors/LocationProvider.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/LocationProvider.h)
- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/EnvironmentSensorManager.cpp)
- [stevemarple/MicroNMEA](https://github.com/stevemarple/MicroNMEA)
- [sparkfun/SparkFun_u-blox_GNSS_Arduino_Library](https://github.com/sparkfun/SparkFun_u-blox_GNSS_Arduino_Library)
