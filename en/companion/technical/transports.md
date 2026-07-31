# The three transports

*BLE · USB · TCP · QUEUES · ONE CLIENT · RECONNECTING*

The companion protocol runs over three connections, and the firmware does
not know the difference: above `BaseSerialInterface` there is only a frame.
For a client it is different. This chapter describes what each transport
imposes on the side building the app — not what the bytes look like, because
that is documented elsewhere.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
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

## One transport per firmware variant

Which of the three is in there is chosen at compile time and is not a
setting. The
branches in `main.cpp` are mutually exclusive: with `WIFI_SSID` it becomes
TCP, with `BLE_PIN_CODE` it becomes BLE, and otherwise serial. A node
flashed as a BLE companion has no TCP port, and vice versa.

For a client that means the transport is a property of the device someone
holds, not something the app can choose. A full client therefore supports
all three. `meshcore_py` does that with `ble_cx`, `serial_cx` and `tcp_cx`
behind one protocol interface; see
[Architecture of a client](client-architecture.md).

## BLE: the node sends at intervals

The BLE implementation does not write directly but queues frames and drains
that queue with a fixed minimum interval:

`src/helpers/esp32/SerialBLEInterface.cpp` r.183-192

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

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/main.cpp)
  — which interface belongs to which build flag
- [`src/helpers/esp32/SerialBLEInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/esp32/SerialBLEInterface.cpp)
  — `BLE_WRITE_MIN_INTERVAL` and the send queue
- [`src/helpers/esp32/SerialWifiInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/esp32/SerialWifiInterface.cpp)
  — displacing an existing client
- [`src/helpers/ArduinoSerialInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ArduinoSerialInterface.cpp)
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
