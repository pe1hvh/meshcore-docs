# AsyncElegantOTA

*VENDORED · ACCESS POINT · UPLOAD PAGE · NO UPSTREAM*

The upload page through which an ESP32 node receives new firmware comes from
AsyncElegantOTA. That library is not in the registry but sits as a copy inside
the MeshCore repo, and therefore has no version range and no update path.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini`, `arch/esp32/AsyncElegantOTA/library.properties` and
> `src/helpers/ESP32Board.cpp`.

## What it does

AsyncElegantOTA puts an upload page on top of an asynchronous web server. You
open it in a browser, pick a firmware file, and the library writes that to the
OTA partition and restarts the board. The built-in page has a progress bar and
an error message if the file does not fit.

The `library.properties` in `arch/esp32/AsyncElegantOTA/` names version 2.2.8
and Ayush Sharma as author, with
`https://github.com/ayushsharma82/AsyncElegantOTA` as its origin.

## How MeshCore pulls it in

`platformio.ini` r.70

```text
  file://arch/esp32/AsyncElegantOTA
```

A local path in the `[esp32_ota]` section. The consequence is that there is no
version range and that PlatformIO never fetches anything: the code in
`arch/esp32/AsyncElegantOTA/` is the code you get. A newer upstream version
only lands here if someone updates the directory.

## How MeshCore uses it

The library is included in the same block as the web server:

`src/helpers/ESP32Board.cpp` r.9

```cpp
#include <AsyncElegantOTA.h>
```

The OTA session opens with an access point and by blocking sleep:

`src/helpers/ESP32Board.cpp` r.13-18

```cpp
bool ESP32Board::startOTAUpdate(const char* id, char reply[]) {
  inhibit_sleep = true;   // prevent sleep during OTA
  WiFi.softAP("MeshCore-OTA", NULL);

  sprintf(reply, "Started: http://%s/update", WiFi.softAPIP().toString().c_str());
  MESH_DEBUG_PRINTLN("startOTAUpdate: %s", reply);
```

After that the web server is created, AsyncElegantOTA is given the node's ID
and it attaches itself to that server:

`src/helpers/ESP32Board.cpp` r.34-36

```cpp
  AsyncElegantOTA.setID(id_buf);
  AsyncElegantOTA.begin(server);    // Start ElegantOTA
  server->begin();
```

## What it means for a node

The full route as a user sees it: an OTA session is started on the node, after
which the node broadcasts an open WiFi network called `MeshCore-OTA`. The node
replies with the address of the upload page, in the form `http://<ip>/update`.
Whoever joins that network and opens that page can upload a firmware file;
afterwards the board restarts with the new firmware.

The access point has no password — `WiFi.softAP("MeshCore-OTA", NULL)`. What
protects the session is that it can only be started by someone who knows the
node's admin password, and that it does not stay running. For as long as it
does run, anyone within radio range of the access point can reach it.

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`arch/esp32/AsyncElegantOTA/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/arch/esp32/AsyncElegantOTA)
- [`src/helpers/ESP32Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ESP32Board.cpp)
- [ayushsharma82/AsyncElegantOTA](https://github.com/ayushsharma82/AsyncElegantOTA)

Translated from Dutch by Anthropic Claude
