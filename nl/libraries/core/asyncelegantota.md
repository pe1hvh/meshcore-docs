# AsyncElegantOTA

*GEVENDORD · ACCESSPOINT · UPLOADPAGINA · GEEN UPSTREAM*

De uploadpagina waarmee een ESP32-node nieuwe firmware binnenkrijgt, komt uit
AsyncElegantOTA. Die library staat niet in de registry maar als kopie in de
MeshCore-repo zelf, en heeft daarmee geen versiebereik en geen updatepad.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, `arch/esp32/AsyncElegantOTA/library.properties` en
> `src/helpers/ESP32Board.cpp`.

## Wat het doet

AsyncElegantOTA zet bovenop een asynchrone webserver een uploadpagina neer.
Je opent hem in een browser, kiest een firmwarebestand, en de library schrijft
dat naar de OTA-partitie en herstart het bord. De ingebouwde pagina bevat een
voortgangsbalk en een foutmelding als het bestand niet past.

De `library.properties` in `arch/esp32/AsyncElegantOTA/` noemt versie 2.2.8
en Ayush Sharma als auteur, met
`https://github.com/ayushsharma82/AsyncElegantOTA` als herkomst.

## Hoe MeshCore hem binnenhaalt

`platformio.ini` r.70

```text
  file://arch/esp32/AsyncElegantOTA
```

Een lokaal pad in de sectie `[esp32_ota]`. Het gevolg is dat er geen
versiebereik is en dat PlatformIO nooit iets ophaalt: de code die in
`arch/esp32/AsyncElegantOTA/` staat, is de code die je krijgt. Een nieuwere
upstream-versie komt hier alleen terecht als iemand de map bijwerkt.

## Hoe MeshCore hem gebruikt

De library wordt geïncludeerd in dezelfde blok als de webserver:

`src/helpers/ESP32Board.cpp` r.9

```cpp
#include <AsyncElegantOTA.h>
```

De OTA-sessie begint met een accesspoint en het blokkeren van de slaapstand:

`src/helpers/ESP32Board.cpp` r.13-18

```cpp
bool ESP32Board::startOTAUpdate(const char* id, char reply[]) {
  inhibit_sleep = true;   // prevent sleep during OTA
  WiFi.softAP("MeshCore-OTA", NULL);

  sprintf(reply, "Started: http://%s/update", WiFi.softAPIP().toString().c_str());
  MESH_DEBUG_PRINTLN("startOTAUpdate: %s", reply);
```

Daarna wordt de webserver aangemaakt, krijgt AsyncElegantOTA het ID van de
node mee en hangt hij zichzelf aan die server:

`src/helpers/ESP32Board.cpp` r.34-36

```cpp
  AsyncElegantOTA.setID(id_buf);
  AsyncElegantOTA.begin(server);    // Start ElegantOTA
  server->begin();
```

## Wat het voor een node betekent

De volledige route zoals een gebruiker die ziet: op de node wordt een
OTA-sessie gestart, waarna de node een open WiFi-netwerk `MeshCore-OTA`
uitzendt. De node antwoordt met het adres van de uploadpagina, in de vorm
`http://<ip>/update`. Wie verbinding maakt met dat netwerk en die pagina
opent, kan een firmwarebestand uploaden; na afloop herstart het bord met de
nieuwe firmware.

Het accesspoint heeft geen wachtwoord — `WiFi.softAP("MeshCore-OTA", NULL)`.
Wat de sessie beschermt, is dat hij alleen gestart kan worden door iemand die
het adminwachtwoord van de node kent, en dat hij niet blijft draaien. Zolang
hij loopt, kan iedereen binnen radiobereik van het accesspoint erbij.

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`arch/esp32/AsyncElegantOTA/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/arch/esp32/AsyncElegantOTA)
- [`src/helpers/ESP32Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ESP32Board.cpp)
- [ayushsharma82/AsyncElegantOTA](https://github.com/ayushsharma82/AsyncElegantOTA)
