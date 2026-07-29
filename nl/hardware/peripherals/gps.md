# GPS

*LOCATIONPROVIDER · NMEA · ENABLE-PIN · TIJDSYNCHRONISATIE*

Een GPS-ontvanger doet in een MeshCore-node twee dingen: hij geeft een
positie, en hij zet de klok gelijk. Het eerste is optioneel, het tweede is
op borden zonder RTC het enige wat de node aan echte tijd heeft. Dit
hoofdstuk beschrijft hoe de firmware de ontvanger uitleest, aan- en uitzet,
en wat er gebeurt als er geen fix is.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/sensors/LocationProvider.h`,
> `src/helpers/sensors/MicroNMEALocationProvider.h`,
> `src/helpers/sensors/EnvironmentSensorManager.cpp` en de
> `PIN_GPS_*`-vlaggen in `variants/`.

## Eén interface, twee soorten ontvanger

De firmware kent locatie alleen als `LocationProvider`: veertien methodes
die zeggen waar je bent, hoe laat het is en of dat te vertrouwen is.

`src/helpers/sensors/LocationProvider.h` r.6-25

```cpp
class LocationProvider {
protected:
    bool _time_sync_needed = true;

public:
    virtual void syncTime() { _time_sync_needed = true; }
    virtual bool waitingTimeSync() { return _time_sync_needed; }
    virtual long getLatitude() = 0;
    virtual long getLongitude() = 0;
    virtual long getAltitude() = 0;
    virtual long satellitesCount() = 0;
    virtual bool isValid() = 0;
    virtual long getTimestamp() = 0;
    virtual void sendSentence(const char * sentence);
    virtual void reset() = 0;
    virtual void begin() = 0;
    virtual void stop() = 0;
    virtual void loop() = 0;
    virtual bool isEnabled() = 0;
```

Twee dingen vallen daarin op. `isValid()` staat los van `isEnabled()`: een
ingeschakelde ontvanger zonder fix is iets anders dan een uitgeschakelde.
En `_time_sync_needed` staat standaard op `true` — de node gaat ervan uit
dat zijn klok fout is tot de GPS het tegendeel bewijst.

Er zijn twee wegen naar zo'n provider:

| Route | Klasse | Aansluiting |
|---|---|---|
| serieel | `MicroNMEALocationProvider` | UART, `PIN_GPS_RX` / `PIN_GPS_TX` |
| I²C | via de sensortabel, RAK12500 op `0x42` | zie [De I²C-bus](../interfaces/i2c.md) |

De seriële route is de gewone. Achttien variantbestanden zetten een
`-D PIN_GPS_RX=`-regel; te herhalen met
`grep -rl -- "-D PIN_GPS_RX=" variants/ | wc -l`.

![Het pad van de GPS naar de firmware: de ontvanger op een UART, NMEA-zinnen
in een buffer van honderd bytes, de parser die er positie en tijd uit haalt,
en de enable-pin die de hele module uit kan zetten](../../../images/nl/gps-1.svg)

## NMEA in een buffer van honderd bytes

De seriële provider leest de ontvanger uit met de library MicroNMEA en
geeft die een vaste buffer mee:

`src/helpers/sensors/MicroNMEALocationProvider.h` r.36-40

```cpp
class MicroNMEALocationProvider : public LocationProvider {
    char _nmeaBuffer[100];
    MicroNMEA nmea;
    mesh::RTCClock* _clock;
    Stream* _gps_serial;
```

Honderd bytes is één NMEA-zin. De provider krijgt een `Stream` — dezelfde
abstractie die ook voor de companion-verbinding wordt gebruikt — en een
klok, want zodra er een geldige tijd binnenkomt zet hij die door. Op de
Heltec V3 wordt die `Stream` letterlijk `Serial1`:

`variants/heltec_v3/target.cpp` r.18-21

```cpp
#if ENV_INCLUDE_GPS
  #include <helpers/sensors/MicroNMEALocationProvider.h>
  MicroNMEALocationProvider nmea = MicroNMEALocationProvider(Serial1, &rtc_clock);
  EnvironmentSensorManager sensors = EnvironmentSensorManager(nmea);
```

Zonder `ENV_INCLUDE_GPS` komt er een sensormanager zonder locatiebron en
verdwijnt de hele GPS-code uit de build.

## De enable-pin en zijn vier lagen

Een GPS-ontvanger die staat te zoeken kost meer stroom dan de rest van de
node bij elkaar. Daarom kan hij uit. Welke pin dat doet wordt in vier
stappen bepaald:

`src/helpers/sensors/MicroNMEALocationProvider.h` r.8-18

```cpp
#ifndef GPS_EN
    #ifdef PIN_GPS_EN
        #define GPS_EN PIN_GPS_EN
    #else
        #define GPS_EN (-1)
    #endif
#endif

#ifndef PIN_GPS_EN_ACTIVE
    #define PIN_GPS_EN_ACTIVE HIGH
#endif
```

Staat `GPS_EN` al ergens gezet, dan wint die. Anders `PIN_GPS_EN` uit het
variantbestand. Staat ook die er niet, dan wordt het `-1` en is de
ontvanger niet uit te zetten. Dezelfde cascade staat er nog eens voor de
resetlijn, met `LOW` als standaard actief niveau in plaats van `HIGH`.

Die drie lagen bestaan omdat sommige borden hun pinnen in een `variant.h`
zetten en andere in `platformio.ini`. Wie een bord toevoegt en `-1` krijgt,
merkt dat niet aan een foutmelding maar aan de batterijduur.

Op de RAK4631 loopt het weer anders: daar deelt de GPS de
voedingsschakelaar `WB_IO2` met andere modules, en wordt met
`gpsIsAwake(WB_IO2)` gekeken of hij al aanstaat
(`src/helpers/sensors/EnvironmentSensorManager.cpp` r.788). Hoe zo'n
gedeelde rail wordt geteld staat in [Het scherm](display.md).

## Tijd is het tweede product

`waitingTimeSync()` en `syncTime()` zitten niet voor niets in de interface.
Een node zonder RTC weet na een herstart niet hoe laat het is, en tijd is
in MeshCore geen sierstukje: berichten dragen een tijdstempel en
sleuteluitwisseling leunt erop. De GPS is op zulke borden de enige bron.

Zit er wél een RTC, dan wordt die apart gezocht op de I²C-bus — vier
adressen, zie [De I²C-bus](../interfaces/i2c.md). De GPS is dan de
correctie, niet de bron.

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`src/helpers/sensors/LocationProvider.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/sensors/LocationProvider.h)
  — de interface
- [`src/helpers/sensors/MicroNMEALocationProvider.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/sensors/MicroNMEALocationProvider.h)
  — de seriële implementatie en de pincascade
- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/sensors/EnvironmentSensorManager.cpp)
  — de I²C-route en de voedingsschakelaar
- [`variants/heltec_v3/target.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/heltec_v3/target.cpp)
  — hoe één bord de provider aanmaakt

Verwant in deze documentatie:

- [De I²C-bus](../interfaces/i2c.md) — de GPS over I²C, en de klok
- [Het scherm](display.md) — de gedeelde voedingsrail
- [GPS-libraries](../../libraries/other/gps.md) — MicroNMEA en de
  u-blox-library
- [Nodematrix](../../platform/node-matrix.md) — welk bord GPS heeft
