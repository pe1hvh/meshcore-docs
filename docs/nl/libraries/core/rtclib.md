# RTClib

*TIJDSTEMPEL · DS3231 · PCF8563 · ADVERT*

Elk pakket dat MeshCore verstuurt draagt een tijdstempel, en elke advert
heeft er een. RTClib levert de klok waar die tijdstempels vandaan komen — of
de node nu een echte RTC-chip aan boord heeft of niet.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, `src/helpers/AutoDiscoverRTCClock.cpp`,
> `src/helpers/RTC_RX8130CE.h` en de `examples/`-map.

## Wat het doet

RTClib van Adafruit praat met real-time clock-chips over I²C. De library
kent onder meer de DS3231, DS1307 en PCF8563, elk met een eigen klasse, en
levert daarnaast het type `DateTime` voor het rekenen met tijdstippen — van
en naar unix-tijd, met kalenderconversie. De repo staat op
[github.com/adafruit/RTClib](https://github.com/adafruit/RTClib).

## Hoe MeshCore hem binnenhaalt

`platformio.ini` r.24

```text
  adafruit/RTClib @ ^2.1.3
```

In `[arduino_base]`, dus in alle 507 build-targets. Daarnaast staat RTClib
nog in zeven variantbestanden apart gedeclareerd.

## Hoe MeshCore hem gebruikt

De klassen van RTClib komen samen in `AutoDiscoverRTCClock`, dat bij het
opstarten de I²C-bus afzoekt naar een klokchip:

`src/helpers/AutoDiscoverRTCClock.cpp` r.6-16

```cpp
static RTC_DS3231 rtc_3231;
static bool ds3231_success = false;

static Melopero_RV3028 rtc_rv3028;
static bool rv3028_success = false;

static RTC_PCF8563 rtc_8563;
static bool rtc_8563_success = false;

static RTC_RX8130CE rtc_8130;
static bool rtc_8130_success = false;
```

Twee van die vier klassen komen uit RTClib (`RTC_DS3231`, `RTC_PCF8563`),
één uit een andere library (zie [`rv3028.md`](rv3028.md)) en één uit
MeshCore zelf. Het type `DateTime` uit RTClib wordt daarnaast gebruikt door
de GPS-tijdsynchronisatie in
`src/helpers/sensors/MicroNMEALocationProvider.h` r.5.

De voorbeeldschetsen includeren de library rechtstreeks:

`examples/simple_repeater/MyMesh.h` r.3-6

```cpp
#include <Arduino.h>
#include <Mesh.h>
#include <RTClib.h>
#include <target.h>
```

In totaal noemen elf van de 590 bronbestanden `RTClib`: zes onder `src/` en
vijf in `examples/` — de drie `MyMesh.h`-bestanden van `simple_repeater`,
`simple_room_server` en `companion_radio`, plus `SensorMesh.h` van
`simple_sensor` en `main.cpp` van `simple_secure_chat`.

## Wat het voor een node betekent

Een node zonder RTC-chip werkt gewoon, maar houdt de tijd alleen bij zolang
hij aan staat. Na een herstart begint de teller opnieuw, tenzij de tijd van
buiten wordt gezet — via de CLI, via een companion-app of via GPS. Een node
mét een van de vier ondersteunde klokchips onthoudt de tijd over een
herstart heen, en dat is te merken aan de tijdstempels op ontvangen
berichten en aan het verloop van adverts.

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/AutoDiscoverRTCClock.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/AutoDiscoverRTCClock.cpp)
- [`examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [`src/helpers/sensors/MicroNMEALocationProvider.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/MicroNMEALocationProvider.h)
- [adafruit/RTClib](https://github.com/adafruit/RTClib)
