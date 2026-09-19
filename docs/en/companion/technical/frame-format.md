# The frame

*OPCODE · PAYLOAD · 176 BYTES · NO FRAGMENTATION · WHAT DOES NOT FIT*

Every frame starts with one byte that indicates what kind of frame it is. The
remaining bytes form the data content (*payload*). Inside the frame there is
no extra header with a length field of its own, and the protocol cannot
spread one message across several frames. That makes the protocol easy to
implement and at the same time imposes a hard limit on what can cross in one
go.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `src/helpers/BaseSerialInterface.h` and
> `examples/companion_radio/MyMesh.cpp`. The byte layout of the transport
> header is in [USB Serial](../../hardware/interfaces/usb-serial.md) and is
> not repeated here.

## Opcode and payload

The structure is the same everywhere:

```text
[opcode: 1 byte][payload: 0 to 175 bytes]
```

The first byte determines how the rest is read. Commands run from 1 to 65,
responses from 0 to 28 and push codes from `0x80` to `0x90`. Because
commands only travel to the node and responses and push codes only come
back, those ranges never collide in practice.

Within the payload three conventions hold:

- **In multi-byte integers the least significant byte is sent first**
  (*little-endian*). The exception is CayenneLPP in telemetry data, where the
  most significant byte comes first instead (*big-endian*); see
  [CayenneLPP](../../libraries/core/cayenne-lpp.md).
- **Text is UTF-8** and not necessarily terminated with a null byte — the
  frame length is the boundary.
- **There is no alignment or padding.** There are no unused filler bytes
  between the fields: they sit against each other, and a
  field that only exists from a certain protocol version onwards sits at the
  end so older clients simply stop reading earlier.

That last point is why the firmware builds its responses with an increasing
counter and writes out exactly as many bytes as it filled, rather than
sending a fixed structure.

## The limit of 176 bytes

There is one frame size for all transports:

`src/helpers/BaseSerialInterface.h` r.5

```cpp
#define MAX_FRAME_SIZE  176   // +4 for transport codes (region scoping)
```

The comment refers to the four bytes a packet can carry extra for region
scoping; see [Regions and Scopes](../../technical/regions-and-scopes.md).

For a client there are two consequences. When sending you have to check
yourself whether it fits — the firmware refuses what is too large, but only
after it has already been sent. When receiving you must count on a
frame never being longer than 176 bytes, and on a longer frame being
truncated by the firmware rather than refused.

## What is left for data

The opcode takes up one byte, and most commands still need an address, an
index or a timestamp. For datagrams on a channel — separate packets of structured
data rather than text — that overhead is fixed:

`examples/companion_radio/MyMesh.cpp` r.101

```cpp
#define MAX_CHANNEL_DATA_LENGTH       (MAX_FRAME_SIZE - 9)
```

Nine bytes of overhead, so 167 bytes of data. Offer more and you get an
error back:

`examples/companion_radio/MyMesh.cpp` r.1169-1171

```cpp
    } else if (payload_len > MAX_CHANNEL_DATA_LENGTH) {
      MESH_DEBUG_PRINTLN("CMD_SEND_CHANNEL_DATA payload too long: %d > %d", payload_len, MAX_CHANNEL_DATA_LENGTH);
      writeErrFrame(ERR_CODE_ILLEGAL_ARG);
```

For text messages the same principle holds with different overhead. The
practical lower bound to remember: count on roughly 150 bytes of usable text
per message, and bear in mind that a LoRa packet is then divided again by
what fits over the air — see
[MeshCore Packet Structure](../../technical/packet-structure.md).

## There is no fragmentation

The protocol cannot automatically spread one large logical message across
several frames. Such a split is called fragmentation. Where it is needed
anyway, it has been solved case by case:

| Case | Solution |
|---|---|
| Fetching many contacts | a series of separate frames: `RESP_CODE_CONTACTS_START`, then `RESP_CODE_CONTACT` per item, then `RESP_CODE_END_OF_CONTACTS` |
| Fetching messages | one frame per message, repeated until `RESP_CODE_NO_MORE_MESSAGES` |
| Signing something | a sub-protocol of its own with three commands: `CMD_SIGN_START` (33), `CMD_SIGN_DATA` (34), `CMD_SIGN_FINISH` (35) |

That third case is the only one where the app has to split things itself.
The node reports at `CMD_SIGN_START` how much it can take:

`examples/companion_radio/MyMesh.cpp` r.1712-1717

```cpp
  } else if (cmd_frame[0] == CMD_SIGN_START) {
    out_frame[0] = RESP_CODE_SIGN_START;
    out_frame[1] = 0; // reserved
    uint32_t len = MAX_SIGN_DATA_LEN;
    memcpy(&out_frame[2], &len, 4);
    _serial->writeFrame(out_frame, 6);
```

`MAX_SIGN_DATA_LEN` is 8 KiB (`MyMesh.cpp` r.137). The app sends that in
chunks of at most 175 bytes with `CMD_SIGN_DATA` and closes with
`CMD_SIGN_FINISH`.

## What a client must check

| When sending | When receiving |
|---|---|
| does the command fit within 176 bytes | is the frame long enough for the fields you read |
| do you know the length limit of *this* command | is the first byte a response or a push |
| is the clock set (for anything with a timestamp) | does this response belong to my outstanding request |
| is another request still open | is the field you read present in this protocol version |

The bottom right is the most common mistake. Fields added in a later
`FIRMWARE_VER_CODE` sit at the end, and an older node sends a shorter frame.
Whoever does not check the length may interpret bytes outside the received
frame as valid fields, or trigger a read error. See
[The interaction model](../logical/interaction-model.md).

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`src/helpers/BaseSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/BaseSerialInterface.h)
  — `MAX_FRAME_SIZE`
- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.cpp)
  — `MAX_CHANNEL_DATA_LENGTH`, `MAX_SIGN_DATA_LEN`, the length checks

Related chapters:

- [USB Serial](../../hardware/interfaces/usb-serial.md) — the header around
  the frame
- [The three transports](transports.md) — what each transport imposes
- [MeshCore Packet Structure](../../technical/packet-structure.md) — what
  goes over the air afterwards
- [The command groups](command-groups.md) — which command expects which
  payload

Translated from Dutch by Anthropic Claude
