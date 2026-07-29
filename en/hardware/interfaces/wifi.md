# WiFi as a Companion Link

*ONE TRANSPORT AT A TIME · TCP 5000 · CREDENTIALS IN THE BINARY · ESP32 ONLY*

In MeshCore, WiFi is not a network layer but one of the ways a companion app
talks to a node. It replaces the BLE link or the serial cable — not as a
setting but as a build choice. This chapter describes how that choice is
made, what travels over TCP, and why your network credentials end up inside
the firmware.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `examples/companion_radio/main.cpp`,
> `src/helpers/esp32/SerialWifiInterface.cpp`,
> `src/helpers/BaseSerialInterface.h` and the `WIFI_SSID` flags in
> `variants/`.

![Block diagram of the companion link: one of three transports is compiled
in — WiFi over TCP, BLE, or serial — all behind the same
BaseSerialInterface](../../../images/en/wifi-1.svg)

## Three transports, one gets compiled

The companion firmware picks its transport with preprocessor directives, not
with a setting:

`examples/companion_radio/main.cpp` r.37-54

```cpp
#ifdef ESP32
  #ifdef WIFI_SSID
    #include <helpers/esp32/SerialWifiInterface.h>
    SerialWifiInterface serial_interface;
    #ifndef TCP_PORT
      #define TCP_PORT 5000
    #endif
  #elif defined(BLE_PIN_CODE)
    #include <helpers/esp32/SerialBLEInterface.h>
    SerialBLEInterface serial_interface;
  #elif defined(SERIAL_RX)
    #include <helpers/ArduinoSerialInterface.h>
    ArduinoSerialInterface serial_interface;
    HardwareSerial companion_serial(1);
  #else
    #include <helpers/ArduinoSerialInterface.h>
    ArduinoSerialInterface serial_interface;
  #endif
```

This is the most load-bearing line of the whole interfaces section. It is an
`#elif` chain: if `WIFI_SSID` is defined, WiFi is compiled in and BLE and
the serial variant never make it into the binary. A node therefore cannot
talk to an app over BLE and over WiFi at the same time, and you cannot
switch between them without reflashing.

> [!NOTE]
> That explains why nodes with the same chip behave differently: which
> transport they speak is a property of the firmware on them, not of the
> board. Which boards offer which connection options is in
> [Node Matrix](../../platform/node-matrix.md).

## ESP32 only

The chain above sits inside `#ifdef ESP32`. On RP2040 the same construct is
present in the file but entirely commented out. That shows up in the variant
files:

| `WIFI_SSID` | Count |
|---|---|
| active | 17 lines in 15 variant directories |
| commented out | 4 lines, all four RP2040 |

Counted across `variants/*/platformio.ini`; lines starting with `;` are
commented out and do not count as a build flag. More lines than directories,
because a variant file can hold several `[env:…]` sections.

The four commented-out lines are in `rak11310`, `rpi_picow`,
`waveshare_rp2040_lora` and `xiao_rp2040`. So it is not an oversight but work
lying ready: the code exists, the flags exist, but the RP2040 branch is not
in use.

## What travels over the link

`SerialWifiInterface` opens a TCP server. The port is `TCP_PORT`, and if the
variant does not set it, 5000.

`src/helpers/esp32/SerialWifiInterface.cpp` r.4-7

```cpp
void SerialWifiInterface::begin(int port) {
  // wifi setup is handled outside of this class, only starts the server
  server.begin(port);
}
```

The class does nothing about the network itself — connecting happens outside
the class, in `main.cpp`. What travels over the link is the same as with BLE
and serial: frames of at most 176 bytes, behind the same interface.

`src/helpers/BaseSerialInterface.h` r.5

```cpp
#define MAX_FRAME_SIZE  176   // +4 for transport codes (region scoping)
```

That is why the three transports are interchangeable: all three implement
`BaseSerialInterface` with `writeFrame()` and `checkRecvFrame()`, and the
rest of the firmware does not know which transport sits underneath. What
those frames look like byte by byte is in [USB Serial](usb-serial.md).

## The credentials live in the binary

`WIFI_SSID` and `WIFI_PWD` are build flags. They are substituted into the
code at compile time:

`examples/companion_radio/main.cpp` r.216-217

```cpp
  WiFi.begin(WIFI_SSID, WIFI_PWD);
  serial_interface.begin(TCP_PORT);
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

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/main.cpp)
  — the `#elif` chain that picks the transport, and `WiFi.begin()`
- [`src/helpers/esp32/SerialWifiInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/esp32/SerialWifiInterface.cpp)
  — the TCP server and the send queue
- [`src/helpers/BaseSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/BaseSerialInterface.h)
  — the shared interface and `MAX_FRAME_SIZE`

Related in this documentation:

- [BLE Architecture](ble-architecture.md) — the transport WiFi replaces
- [USB Serial](usb-serial.md) — the same frame over a cable
- [The Hardware of a Node](../introduction.md) — where this part sits
- [Node Matrix](../../platform/node-matrix.md) — which board has WiFi on
  board
- [The Four Platform Families](../../platform/platform-families.md) — which
  families know WiFi

Translated from Dutch by Anthropic Claude
