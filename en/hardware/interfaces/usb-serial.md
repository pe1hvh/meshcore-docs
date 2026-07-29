# USB Serial

*FRAME FORMAT · `>` AND `<` · 16-BIT LENGTH · 176 BYTES*

The serial link is the transport without a radio, without a PIN code and
without a network: a cable to a computer. It is also the transport whose
format is easiest to read, and that format is the same as with BLE and
WiFi. This chapter describes the frame byte by byte and the state machine
that pulls it out of the byte stream.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `src/helpers/ArduinoSerialInterface.cpp`,
> `src/helpers/ArduinoSerialInterface.h` and
> `src/helpers/BaseSerialInterface.h`.

![Frame layout of the serial link: start byte, length in two bytes least
significant first, followed by the payload, with the four states of the
receiving state machine](../../../images/en/usb-serial-1.svg)

## One interface, three implementations

Everything a companion app exchanges with a node passes through
`BaseSerialInterface`. It knows only two functions:

`src/helpers/BaseSerialInterface.h` r.16-20

```cpp
  virtual bool isConnected() const = 0;

  virtual bool isWriteBusy() const = 0;
  virtual size_t writeFrame(const uint8_t src[], size_t len) = 0;
  virtual size_t checkRecvFrame(uint8_t dest[]) = 0;
```

`ArduinoSerialInterface`, `SerialBLEInterface` and `SerialWifiInterface`
fill those in. Which one ends up in the firmware is a build choice; see
[WiFi as a Companion Link](wifi.md).

The frame size is the same for all three:

`src/helpers/BaseSerialInterface.h` r.5

```cpp
#define MAX_FRAME_SIZE  176   // +4 for transport codes (region scoping)
```

176 bytes, with the comment that four more are added for transport codes.
What those transport codes are is in
[Regions and Scopes](../../technical/regions-and-scopes.md).

## The frame the node sends

Three header bytes, then the payload:

`src/helpers/ArduinoSerialInterface.cpp` r.24-37

```cpp
size_t ArduinoSerialInterface::writeFrame(const uint8_t src[], size_t len) {
  if (len > MAX_FRAME_SIZE) {
    // frame is too big!
    return 0;
  }

  uint8_t hdr[3];
  hdr[0] = '>';
  hdr[1] = (len & 0xFF);  // LSB
  hdr[2] = (len >> 8);    // MSB

  _serial->write(hdr, 3);
  return _serial->write(src, len);
}
```

| Byte | Value | Meaning |
|---|---|---|
| 0 | `>` (`0x3E`) | node → computer |
| 1 | length low | LSB first |
| 2 | length high | MSB |
| 3… | payload | at most 176 bytes |

Direction sits in the start byte. The node sends with `>` and listens for
`<`: a frame going the other way therefore starts with a different
character. That is not encryption, but it makes it impossible to
accidentally read your own output as input.

A frame larger than 176 bytes is not truncated but not sent at all —
`writeFrame()` then returns zero.

## The state machine on the receiving side

Bytes arrive one at a time, so the receiver is a state machine with four
states:

```text
  IDLE        ── sees '<' ───▶  HDR_FOUND
  HDR_FOUND   ── length LSB ─▶  LEN1_FOUND
  LEN1_FOUND  ── length MSB ─▶  LEN2_FOUND   (or back to IDLE on length 0)
  LEN2_FOUND  ── payload ────▶  frame done, back to IDLE
```

Two details are worth noting:

`src/helpers/ArduinoSerialInterface.cpp` r.59-68

```cpp
      default:
        if (rx_len < MAX_FRAME_SIZE) {
          rx_buf[rx_len] = (uint8_t)c;   // rest of frame will be discarded if > MAX
        }
        rx_len++;
        if (rx_len >= _frame_len) {  // received a complete frame?
          if (_frame_len > MAX_FRAME_SIZE) _frame_len = MAX_FRAME_SIZE;    // truncate
          memcpy(dest, rx_buf, _frame_len);
          _state = RECV_STATE_IDLE;  // reset state, for next frame
          return _frame_len;
        }
```

An overlong frame *is* read in full but only kept up to 176 bytes; the rest
disappears. The counter keeps running so the state machine is at the right
point in the stream once the frame ends. And an announced length of zero
sends the machine straight back to `IDLE` — an empty frame does not exist.

## There is no connection detection

`src/helpers/ArduinoSerialInterface.cpp` r.16-18

```cpp
bool ArduinoSerialInterface::isConnected() const { 
  return true;   // no way of knowing, so assume yes
}
```

A serial port has no concept of a connection. The firmware therefore always
says yes. With BLE and WiFi it is different: there is a counterpart that
connects and drops away, and there the interface does track it. See
[BLE Architecture](ble-architecture.md).

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`src/helpers/ArduinoSerialInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ArduinoSerialInterface.cpp)
  — `writeFrame()`, `checkRecvFrame()` and the four states
- [`src/helpers/BaseSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/BaseSerialInterface.h)
  — the shared interface and `MAX_FRAME_SIZE`

Related in this documentation:

- [WiFi as a Companion Link](wifi.md) — the same frame over TCP
- [BLE Architecture](ble-architecture.md) — the same frame over BLE
- [Regions and Scopes](../../technical/regions-and-scopes.md) — the four
  transport code bytes the comment refers to
- [The Hardware of a Node](../introduction.md) — where this part sits

Translated from Dutch by Anthropic Claude
