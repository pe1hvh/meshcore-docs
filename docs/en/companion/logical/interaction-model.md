# The interaction model

*REQUEST · RESPONSE · PUSH · TWO VERSION AXES · RECONNECTING*

Two kinds of traffic run over the same connection: responses the app asked
for, and notifications the node sends on its own. That distinction shapes
every client. On top of that, app and node negotiate what they understand of
each other when connecting — across two independent version numbers.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `examples/companion_radio/MyMesh.cpp` and
> `examples/companion_radio/MyMesh.h`. The order of the opening steps was
> compared with `docs/companion_protocol.md` and with `meshcore_py` v2.3.8.

![Course of a connection: app start, device query, setting the time,
fetching contacts and channels, and then a loop that fetches messages as
long as the node reports something is waiting](../../../images/en/companion-interaction-1.svg)

## Three kinds of frame

A frame is one delimited block of data sent between the app and the node. It
is not the same thing as a LoRa packet: that travels over the air, while a
frame travels over the cable or the radio link between app and node. The
first byte of every frame states what kind of frame it is. The number ranges
used do not overlap:

| Kind | Range | Direction | Count |
|---|---|---|---|
| Command | 1 – 65 | app → node | 58 |
| Response | 0 – 28 | node → app, on request | 29 |
| Push | `0x80` – `0x90` | node → app, unsolicited | 17 |

Responses and push codes share the same byte but do not collide: push codes
start at `0x80`, far above the highest response code. A client can therefore
decide in one place whether an incoming frame belongs to an outstanding
request — a command the app is still awaiting an answer to — or not.

## Request and response

One command yields zero, one or many frames. `CMD_GET_CONTACTS` is the
clearest example: `RESP_CODE_CONTACTS_START`, then a series of
`RESP_CODE_CONTACT`, then `RESP_CODE_END_OF_CONTACTS`. A client that stops
listening after the first response misses the rest.

Some commands only yield `RESP_CODE_OK` or `RESP_CODE_ERR`. The error code
sits in the second byte:

`examples/companion_radio/MyMesh.cpp` r.130-135

```cpp
#define ERR_CODE_UNSUPPORTED_CMD        1
#define ERR_CODE_NOT_FOUND              2
#define ERR_CODE_TABLE_FULL             3
#define ERR_CODE_BAD_STATE              4
#define ERR_CODE_FILE_IO_ERROR          5
#define ERR_CODE_ILLEGAL_ARG            6
```

`ERR_CODE_UNSUPPORTED_CMD` is the code a client meets when it uses a command
this firmware does not know yet. That is the practical way to discover what
a node can do: try, and watch for this error.

## Push: the node asks for attention

An unsolicited notification — in the firmware a push message, recognisable by
its push code — is a frame the node sends of its own accord, without the app
having asked for it. The node does not send incoming messages on its own. It
only reports *that* something is waiting, with `PUSH_CODE_MSG_WAITING`
(`0x83`). The app then fetches it with `CMD_SYNC_NEXT_MESSAGE`, repeatedly,
until `RESP_CODE_NO_MORE_MESSAGES` arrives.

That inversion is deliberate. The node does not have to track what the app
has already seen; the app decides when it drains. The price is that a client
ignoring the notification lets the queue fill up — see
[Responsibilities](responsibilities.md).

The other sixteen push codes work the same way: they report an event
(`PUSH_CODE_ADVERT`, `PUSH_CODE_SEND_CONFIRMED`, `PUSH_CODE_CONTACTS_FULL`)
and are never an answer to an outstanding request.

## Two version axes

When connecting, app and node exchange two numbers that have nothing to do
with each other. A third version number is also in circulation, which carries
no meaning for the protocol:

| Number | Whose | What it states |
|---|---|---|
| `app_target_ver` | the app | which protocol version the app understands |
| `FIRMWARE_VER_CODE` | the node | which protocol version the firmware handles |
| firmware version, for example `v1.16.0` | the node | the version number people see; unrelated to the protocol |

**The app states what it understands.** Byte 1 of `CMD_DEVICE_QUERY` is
`app_target_ver`. The firmware stores it and adapts what it sends:

`examples/companion_radio/MyMesh.cpp` r.1009-1016

```cpp
  if (cmd_frame[0] == CMD_DEVICE_QUERY && len >= 2) { // sent when app establishes connection
    app_target_ver = cmd_frame[1];                    // which version of protocol does app understand

    int i = 0;
    out_frame[i++] = RESP_CODE_DEVICE_INFO;
    out_frame[i++] = FIRMWARE_VER_CODE;
    out_frame[i++] = MAX_CONTACTS / 2;   // v3+
    out_frame[i++] = MAX_GROUP_CHANNELS; // v3+
```

At `app_target_ver >= 3` the firmware sends received messages in a different
format: `RESP_CODE_CONTACT_MSG_RECV_V3` (16) instead of
`RESP_CODE_CONTACT_MSG_RECV` (7). A client that declares 3 but expects the
old format reads nonsense.

**The node states what it can do.** That is `FIRMWARE_VER_CODE`, a single
number independent of the version number people see:

`examples/companion_radio/MyMesh.h` r.7-8

```cpp
/*------------ Frame Protocol --------------*/
#define FIRMWARE_VER_CODE 13
```

At commit `03b6ef4` it stands at 13, with firmware `v1.16.0`. Fields and
behaviour hang off that number: `client_repeat` in the device response from
9 onwards, `path_hash_mode` from 10, and requests to nodes that are not a
contact from 13. A client reading those fields unconditionally runs off the
end of the frame on older firmware.

The two axes are independent: a new app on old firmware and an old app on
new firmware are both normal situations.

## Reconnecting means starting over

`app_target_ver` lives in the node's memory, not on disk, and starts at
zero:

`examples/companion_radio/MyMesh.cpp` r.861

```cpp
  app_target_ver = 0;
```

If the connection drops, the negotiation is forgotten. After every
reconnection the opening therefore has to be done again: the app announces
itself with `CMD_APP_START`, requests the device details with
`CMD_DEVICE_QUERY` and settles the protocol version in the process, and only
then brings its own state up to date. A client that fetches messages straight
after reconnecting, without those two commands, silently gets the oldest
format. That is not an error message — it is a frame that looks plausible and
is read wrongly.

`meshcore_py` solves this by hanging the announcement off the reconnection
rather than off program start-up; see
[Architecture of a client](../technical/client-architecture.md).

## The opening sequence

The official spec describes this order, and `meshcore_py` follows it:

1. `CMD_APP_START` — the app announces itself with a name; the node answers
   with `RESP_CODE_SELF_INFO`: own key, transmit power, position, radio
   parameters
2. `CMD_DEVICE_QUERY` — version negotiation and the limits of this device
3. `CMD_SET_DEVICE_TIME` — the node has no reliable time source of its own
4. `CMD_GET_CONTACTS` — optionally with a timestamp, so only changed
   contacts come back
5. `CMD_GET_CHANNEL` — once per slot, up to the number reported in step 2
6. `CMD_SYNC_NEXT_MESSAGE` — until `RESP_CODE_NO_MORE_MESSAGES`

Step 3 is not a formality. Without a set clock, sent messages carry a
timestamp that means nothing, and that cannot be repaired at the receiving
end.

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.cpp)
  — error codes, `CMD_DEVICE_QUERY`, `app_target_ver`
- [`examples/companion_radio/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.h)
  — `FIRMWARE_VER_CODE`
- [`docs/companion_protocol.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/docs/companion_protocol.md)
  — the official description of the opening sequence

Related chapters:

- [Responsibilities](responsibilities.md) — why the queue has to be drained
- [The command groups](../technical/command-groups.md) — all 58 commands
- [Architecture of a client](../technical/client-architecture.md) — where
  the reconnection belongs

Translated from Dutch by Anthropic Claude
