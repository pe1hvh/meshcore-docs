# ESPAsyncWebServer

*OTA · WIFI · ADMIN_PASSWORD · ASYNCTCP*

Een ESP32-repeater of room server kan zijn firmware over WiFi bijwerken. De
webserver die daarvoor nodig is, komt uit ESPAsyncWebServer. De library zit
niet in de basis maar in een eigen sectie, die zesendertig varianten
aanroepen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, de negenenzeventig `variants/*/platformio.ini` en
> `src/helpers/ESP32Board.cpp`.

## Wat het doet

ESPAsyncWebServer is een HTTP-server voor ESP32 en ESP8266 die niet per
verbinding een taak opzet, maar met callbacks werkt op een asynchrone
TCP-laag. Een route registreer je met een methode en een pad, en de
bijbehorende lambda wordt aangeroepen zodra er een verzoek binnenkomt. De
onderhouden fork die MeshCore gebruikt staat op
[github.com/ESP32Async/ESPAsyncWebServer](https://github.com/ESP32Async/ESPAsyncWebServer).

## Hoe MeshCore hem binnenhaalt

`platformio.ini` r.67-70

```text
[esp32_ota]
lib_deps =
  ESP32Async/ESPAsyncWebServer @ 3.10.3
  file://arch/esp32/AsyncElegantOTA
```

Een eigen sectie, exact vastgepind op 3.10.3, met de OTA-library ernaast.
Zesendertig varianten verwijzen naar `[esp32_ota]`; de rest van de repo
krijgt deze twee libraries niet.

Via zijn `library.json` brengt ESPAsyncWebServer `AsyncTCP` mee, die nergens
in een `platformio.ini` staat — zie [`../dependencies.md`](../dependencies.md).

## Hoe MeshCore hem gebruikt

De hele webserver zit achter één voorwaarde:

`src/helpers/ESP32Board.cpp` r.5-9

```cpp
#if defined(ADMIN_PASSWORD) && !defined(DISABLE_WIFI_OTA)   // Repeater or Room Server only
#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <AsyncElegantOTA.h>
```

Zonder `ADMIN_PASSWORD` bestaat deze code niet in de build. Wordt hij wel
gecompileerd, dan zet `startOTAUpdate()` een server op poort 80 neer met twee
routes:

`src/helpers/ESP32Board.cpp` r.25-32

```cpp
  AsyncWebServer* server = new AsyncWebServer(80);

  server->on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(200, "text/html", home_buf);
  });
  server->on("/log", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(SPIFFS, "/packet_log", "text/plain");
  });
```

De eerste route toont een korte begroeting met het ID van de node. De tweede
serveert het pakketlogboek rechtstreeks uit SPIFFS.

## Wat het voor een node betekent

Een repeater met een adminwachtwoord kan op afstand een OTA-sessie starten en
biedt dan tijdelijk twee webpagina's aan. Het pakketlogboek is via `/log`
zonder verdere authenticatie te lezen zolang die sessie loopt.

De server draait alleen tijdens een OTA-sessie; hij wordt bij het starten
daarvan aangemaakt. Het vervolg — het accesspoint, de uploadpagina en het
herstarten — staat in [`asyncelegantota.md`](asyncelegantota.md).

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/ESP32Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ESP32Board.cpp)
- [ESP32Async/ESPAsyncWebServer](https://github.com/ESP32Async/ESPAsyncWebServer)
