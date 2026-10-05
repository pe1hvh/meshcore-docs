# WiFi as a Companion Link

*ALONGSIDE OTHER TRANSPORTS · TCP 5000 · CREDENTIALS IN THE BINARY · ESP32 ONLY*

In MeshCore, WiFi is not a network layer but one of the ways a companion app
talks to a node. Since v1.17.1 it no longer replaces the BLE link or the
serial cable but sits alongside them: which transports are included is a
build choice, and a build can include several. This chapter describes how
that choice is made, what travels over TCP, and why your network credentials
end up inside the firmware.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.17.1, commit `d929643`, 14 August 2026 — files
> `examples/companion_radio/main.cpp`,
> `src/helpers/esp32/SerialWifiInterface.cpp`,
> `src/helpers/BaseSerialInterface.h`, `src/helpers/MultiSerialInterface.h`
> and the `WIFI_SSID` flags in `variants/`. The counts can be reproduced
> with
> [`tools/hardware-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/hardware-overview.py)
> using `--pin d929643`.

![Block diagram of the companion link: MultiSerialInterface at the top,
with below it five transports that are each added by a build flag of their
own — WiFi over TCP, BLE, USB, a serial port on pins and Ethernet; the WiFi
row is highlighted](../../../images/en/wifi-1.svg)

## Every flag adds a transport

The companion firmware selects its transports with preprocessor directives,
not with a setting. For WiFi:

`examples/companion_radio/main.cpp` r.34-46

```cpp
// include wifi interface
#ifdef WIFI_SSID
  #ifndef TCP_PORT
    #define TCP_PORT 5000
  #endif
  #ifdef ESP32
    // include esp32 wifi interface
    #include <helpers/esp32/SerialWifiInterface.h>
    SerialWifiInterface wifi_interface;
  #else
    #error "SerialWifiInterface is not defined for this platform"
  #endif
#endif
```

In v1.16.0 this was an `#elif` chain: if `WIFI_SSID` was defined, BLE and the
serial variant never made it into the binary. In v1.17.1 each transport has
its own `#if`. At start-up the firmware registers WiFi with
`interface_manager`, a `MultiSerialInterface`:

`examples/companion_radio/main.cpp` r.208-210

```cpp
  WiFi.begin(WIFI_SSID, WIFI_PWD);
  wifi_interface.begin(TCP_PORT);
  interface_manager.addInterface(InterfaceType::WiFi, &wifi_interface);
```

A node can therefore talk to an app over BLE and over WiFi at the same time,
if the build sets both flags. Switching without reflashing is still not
possible: what is not compiled in is not there. How `MultiSerialInterface`
serves the transports together, and what limit there is on their number, is
in [USB Serial](usb-serial.md).

> [!NOTE]
> That explains why nodes with the same chip behave differently: which
> transport they speak is a property of the firmware on them, not of the
> board. Which boards offer which connection options is in
> [Node Matrix](../../platform/node-matrix.md).

## ESP32 only

On any other platform a build with `WIFI_SSID` stops with an error
(`examples/companion_radio/main.cpp` r.43-45). That shows up in the variant
files:

| `WIFI_SSID` | Count |
|---|---|
| active | 25 lines in 21 variant directories |
| commented out | 4 lines, all four RP2040 |

Counted across `variants/*/platformio.ini`; lines starting with `;` are
commented out and do not count as a build flag. More lines than directories,
because a variant file can hold several `[env:…]` sections.

The four commented-out lines are in `rak11310`, `rpi_picow`,
`waveshare_rp2040_lora` and `xiao_rp2040`. In v1.16.0 `main.cpp` still held
a commented-out RP2040 branch that referred to a `SerialWifiInterface` for
RP2040. That branch is gone in v1.17.1, and no such class exists in the
firmware. Enabling one of the four lines produces the error.

## What travels over the link

`SerialWifiInterface` opens a TCP server. The port is `TCP_PORT`, and if the
variant does not set it, it is 5000.

`src/helpers/esp32/SerialWifiInterface.cpp` r.4-7

```cpp
void SerialWifiInterface::begin(int port) {
  // wifi setup is handled outside of this class, only starts the server
  server.begin(port);
}
```

The class does nothing to the network itself — connecting happens outside
the class, in `main.cpp`. Since v1.17.1 that is also where the node is kept
from sleeping while WiFi is active (r.195), and where it reconnects every ten
seconds after the connection drops (r.198-206 and r.265-273). What travels
over the link is the same as with BLE and serial: frames of at most 176
bytes, behind the same interface.

`src/helpers/BaseSerialInterface.h` r.5

```cpp
#define MAX_FRAME_SIZE  176   // +4 for transport codes (region scoping)
```

Over TCP every frame gets the same header as over the cable, `>` or `<` and
two length bytes (`src/helpers/esp32/SerialWifiInterface.cpp` r.91-94); a
frame that does not start with `<` is skipped by the node (r.143-144). All
transports implement `BaseSerialInterface` with `writeFrame()` and
`checkRecvFrame()`, and the rest of the firmware only sees
`MultiSerialInterface`, not which transport sits underneath. What those
frames look like byte by byte is in [USB Serial](usb-serial.md).

## The credentials live in the binary

`WIFI_SSID` and `WIFI_PWD` are build flags. They are substituted into the
code at compile time:

`examples/companion_radio/main.cpp` r.208-209

```cpp
  WiFi.begin(WIFI_SSID, WIFI_PWD);
  wifi_interface.begin(TCP_PORT);
```

> [!WARNING]
> The name and password of your WiFi network end up as readable text inside
> the firmware image. Whoever has the binary — or reads out the node — has
> your network password. Do not share self-built WiFi firmware, and do not
> put a node with WiFi firmware on a network you cannot afford to lose. A
> guest network or a separate VLAN is exactly what this situation calls for.

This is a different trade-off from BLE, where a PIN code sits in the
firmware but no network secret. See [BLE Architecture](ble-architecture.md).

## Sources

Firmware, commit `d929643` (v1.17.1, 14 August 2026):

- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/companion_radio/main.cpp)
  — the `#if` per transport, the registration with `interface_manager`,
  `WiFi.begin()` and the reconnecting
- [`src/helpers/esp32/SerialWifiInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/esp32/SerialWifiInterface.cpp)
  — the TCP server, the header and the send queue
- [`src/helpers/BaseSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/BaseSerialInterface.h)
  — the shared interface and `MAX_FRAME_SIZE`
- [`src/helpers/MultiSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/MultiSerialInterface.h)
  — the class that serves all transports together

Related in this documentation:

- [BLE Architecture](ble-architecture.md) — the transport that since v1.17.1
  can sit alongside WiFi in one build
- [USB Serial](usb-serial.md) — the same frame over a cable, and
  `MultiSerialInterface`
- [The Hardware of a Node](../introduction.md) — where this part sits
- [Node Matrix](../../platform/node-matrix.md) — which board has WiFi on
  board
- [The Four Platform Families](../../platform/platform-families.md) — which
  families know WiFi

Translated from Dutch by Anthropic Claude
