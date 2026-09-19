# The transports

*BLE · USB · TCP · ETHERNET · QUEUES · ONE CLIENT · RECONNECTING*

The companion protocol runs over five kinds of connection, and the firmware
does not know the difference: above `BaseSerialInterface` there is only a frame.
For a client it is different. This chapter describes what each transport
imposes on the side building the app — not what the bytes look like, because
that is documented elsewhere.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.17.1, commit `d929643`, 14 August 2026 — files
> `examples/companion_radio/main.cpp`,
> `src/helpers/esp32/SerialBLEInterface.cpp`,
> `src/helpers/esp32/SerialBLEInterface.h`,
> `src/helpers/nrf52/SerialBLEInterface.h`,
> `src/helpers/esp32/SerialWifiInterface.cpp` and
> `src/helpers/ArduinoSerialInterface.cpp`.

![Above a shared interface lives one frame format; below it three
implementations, each with its own demands on the client](../../../images/en/companion-transports-1.svg)

> [!NOTE]
> The byte layout of the frame header, the four receive states and the BLE
> stack with GATT and NUS are not here but in
> [USB Serial](../../hardware/interfaces/usb-serial.md),
> [WiFi as a companion link](../../hardware/interfaces/wifi.md) and
> [BLE Architecture](../../hardware/interfaces/ble-architecture.md). This
> chapter is about the consequences of those for a client.

## More than one transport at a time

Up to and including v1.16.0 a build held exactly one transport and the
branches in `main.cpp` were mutually exclusive. Since v1.17.1 that is no
longer so. `MultiSerialInterface` is itself a `BaseSerialInterface` that holds
a set of other interfaces underneath and serves them all at once; `main.cpp`
registers them one by one and then hands the set to the mesh as a single
interface:

`examples/companion_radio/main.cpp` r.188-191

```cpp
#if defined(BLE_PIN_CODE)
  bluetooth_interface.begin(BLE_NAME_PREFIX, the_mesh.getNodePrefs()->node_name, the_mesh.getBLEPin());
  interface_manager.addInterface(InterfaceType::Bluetooth, &bluetooth_interface);
#endif
```

The blocks after it have the same shape and are independent: `WIFI_SSID` adds
WiFi, `ENABLE_USB_INTERFACE` the USB console, `ETHERNET_ENABLED` ethernet and
`SERIAL_RX` a second hardware serial port. They are no longer `else` branches,
so a build can have several. Which transports are in there is still decided at
compile time and is not a setting.

Five kinds, then. `InterfaceType` knows `Bluetooth`, `USB`, `WiFi`,
`Ethernet` and `HardwareSerial`
(`src/helpers/MultiSerialInterface.h` r.10-17).

> [!WARNING]
> **Five kinds, four slots.** `MAX_INTERFACES` defaults to four, with the
> comment `ble, usb, wifi, ethernet`
> (`src/helpers/MultiSerialInterface.h` r.5-8). `addInterface()` looks for the
> first free slot and returns `false` when there is none; in `main.cpp` that
> outcome is nowhere checked. A build that sets all five `#define`s therefore
> loses the last one silently. Among the shipped variants that combination
> does not occur — the two ethernet targets, `thinknode_m7` and `rak4631`, set
> no `SERIAL_RX` — but anyone building a variant of their own runs into a
> limit that gives no error.

For a client that means the transport is a property of the device someone
holds, not something the app can choose — but a device can now offer more than
one. A full client therefore supports BLE, serial and TCP. `meshcore_py` does
that with `ble_cx`, `serial_cx` and `tcp_cx` behind one protocol interface;
see [Architecture of a client](client-architecture.md).

> [!NOTE]
> `isConnected()` on `MultiSerialInterface` returns `true` as soon as one of
> the underlying interfaces is connected, and `writeFrame()` writes to every
> connected interface. Two clients attached at the same time on different
> transports therefore see each other's replies. The protocol still assumes
> one client at a time; see *What a client must assume per transport*.

## BLE: the node sends at intervals

The BLE implementation does not write directly but queues frames and drains
that queue with a fixed minimum interval:

`src/helpers/esp32/SerialBLEInterface.cpp` r.189-198

```cpp
#define  BLE_WRITE_MIN_INTERVAL   60

bool SerialBLEInterface::isWriteBusy() const {
  return millis() < _last_write + BLE_WRITE_MIN_INTERVAL;   // still too soon to start another write?
}

size_t SerialBLEInterface::checkRecvFrame(uint8_t dest[]) {
  if (send_queue_len > 0   // first, check send queue
    && millis() >= _last_write + BLE_WRITE_MIN_INTERVAL    // space the writes apart
  ) {
```

So there are at least sixty milliseconds between two notifications. That lets
the node send at most roughly sixteen notifications per second in theory.
When fetching three hundred and fifty contacts that is noticeable, and it is
the reason `CMD_GET_CONTACTS` accepts a timestamp so only changes come
back.

The send queue is small and differs per platform:

| Platform | `FRAME_QUEUE_SIZE` | File |
|---|---|---|
| ESP32, BLE | 4 | `src/helpers/esp32/SerialBLEInterface.h` r.26 |
| ESP32, WiFi | 4 | `src/helpers/esp32/SerialWifiInterface.h` r.27 |
| nRF52, BLE | 12 | `src/helpers/nrf52/SerialBLEInterface.h` r.24 |

If that queue fills up, `writeFrame()` returns zero and the frame is gone —
no error reaches the app. A client sending many commands in quick succession
without waiting for answers can therefore miss responses unnoticed. Waiting
for the response before sending the next command is not politeness but a
requirement.

## TCP: one client at a time

The WiFi implementation accepts a new connection by throwing out the
existing one:

`src/helpers/esp32/SerialWifiInterface.cpp` r.57-68

```cpp
  auto newClient = server.available();
  if (newClient) {

    // disconnect existing client
    deviceConnected = false;
    client.stop();

    // switch active connection to new client
    client = newClient;

    // forget received frame header
    resetReceivedFrameHeader();
```

Two apps on the same node over TCP is therefore not shared access: the new
connection drops the existing one without any protocol notification. The
displaced client only notices that its socket is closed. With BLE the same
holds by a different route: one GATT connection per radio, GATT being the
Bluetooth Low Energy layer these frames travel over. See
[BLE Architecture](../../hardware/interfaces/ble-architecture.md).

That is the technical underpinning of what
[Responsibilities](../logical/responsibilities.md) already noted: whoever
synchronises first empties the queue, and the second app never sees those
messages.

## Serial: the firmware cannot detect an unplugged cable

The serial implementation cannot know whether anything is at the other end
and therefore always answers affirmatively to `isConnected()`. For a client
that means no event arrives when the cable is pulled. The only detection
left is a response that fails to arrive within a time limit.

## What a client must assume per transport

On serial and TCP a continuous run of bytes arrives — a byte stream — with no
marker where one frame ends and the next begins. The client determines that
boundary itself from the header described in
[USB Serial](../../hardware/interfaces/usb-serial.md). On BLE, GATT delivers
each notification as a self-contained block.

| | BLE | USB serial | TCP |
|---|---|---|---|
| Frame boundary | given by GATT | extract from the byte stream | extract from the byte stream |
| Connection drops | noticeable | not noticeable | noticeable |
| Multiple clients | no | no | no, the new one displaces |
| Pace | at least 60 ms per frame | as fast as the port | as fast as the network |
| Reconnection needed | yes, regularly | rarely | on a network change |

The bottom row matters most. After every reconnection `app_target_ver` on
the node is zero again and the opening has to be redone: first
`CMD_APP_START`, then `CMD_DEVICE_QUERY`. See
[The interaction model](../logical/interaction-model.md).

## Sources

Firmware, commit `d929643` (v1.17.1, 14 August 2026):

- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/companion_radio/main.cpp)
  — which interface belongs to which build flag
- [`src/helpers/esp32/SerialBLEInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/esp32/SerialBLEInterface.cpp)
  — `BLE_WRITE_MIN_INTERVAL` and the send queue
- [`src/helpers/esp32/SerialWifiInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/esp32/SerialWifiInterface.cpp)
  — displacing an existing client
- [`src/helpers/ArduinoSerialInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/ArduinoSerialInterface.cpp)
  — `isConnected()`, which always answers affirmatively

Related chapters:

- [USB Serial](../../hardware/interfaces/usb-serial.md) — the frame byte by
  byte
- [BLE Architecture](../../hardware/interfaces/ble-architecture.md) — GATT,
  NUS and pairing
- [WiFi as a companion link](../../hardware/interfaces/wifi.md) — the setup
  of the TCP variant
- [The frame](frame-format.md) — what fits into the 176 bytes

Translated from Dutch by Anthropic Claude
