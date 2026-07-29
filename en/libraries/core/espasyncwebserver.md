# ESPAsyncWebServer

*OTA · WIFI · ADMIN_PASSWORD · ASYNCTCP*

An ESP32 repeater or room server can update its firmware over WiFi. The web
server needed for that comes from ESPAsyncWebServer. The library is not in the
base but in a section of its own, which thirty-six variants call in.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini`, the seventy-nine `variants/*/platformio.ini` and
> `src/helpers/ESP32Board.cpp`.

## What it does

ESPAsyncWebServer is an HTTP server for ESP32 and ESP8266 that does not spin
up a task per connection but works with callbacks on an asynchronous TCP
layer. You register a route with a method and a path, and the accompanying
lambda is called as soon as a request comes in. The maintained fork MeshCore
uses is at
[github.com/ESP32Async/ESPAsyncWebServer](https://github.com/ESP32Async/ESPAsyncWebServer).

## How MeshCore pulls it in

`platformio.ini` r.67-70

```text
[esp32_ota]
lib_deps =
  ESP32Async/ESPAsyncWebServer @ 3.10.3
  file://arch/esp32/AsyncElegantOTA
```

A section of its own, pinned exactly to 3.10.3, with the OTA library beside
it. Thirty-six variants refer to `[esp32_ota]`; the rest of the repo does not
get these two libraries.

Through its `library.json`, ESPAsyncWebServer brings in `AsyncTCP`, which
appears in no `platformio.ini` — see
[`../dependencies.md`](../dependencies.md).

## How MeshCore uses it

The entire web server sits behind one condition:

`src/helpers/ESP32Board.cpp` r.5-9

```cpp
#if defined(ADMIN_PASSWORD) && !defined(DISABLE_WIFI_OTA)   // Repeater or Room Server only
#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <AsyncElegantOTA.h>
```

Without `ADMIN_PASSWORD` this code does not exist in the build. When it is
compiled in, `startOTAUpdate()` puts a server on port 80 with two routes:

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

The first route shows a short greeting with the node's ID. The second serves
the packet log straight from SPIFFS.

## What it means for a node

A repeater with an admin password can start an OTA session remotely and then
offers two web pages. The packet log is readable through `/log` without
further authentication for as long as that session runs.

The server runs only during an OTA session; it is created when one starts. The
rest — the access point, the upload page and the restart — is described in
[`asyncelegantota.md`](asyncelegantota.md).

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/ESP32Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ESP32Board.cpp)
- [ESP32Async/ESPAsyncWebServer](https://github.com/ESP32Async/ESPAsyncWebServer)

Translated from Dutch by Anthropic Claude
