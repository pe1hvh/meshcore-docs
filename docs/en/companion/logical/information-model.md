# Information model

*CONTACT · CHANNEL · MESSAGE · ADVERT · PATH · WHAT LIVES WHERE*

The interface knows a handful of data kinds. Some exist on both sides and
have to stay in step, others exist in only one place and are therefore never
a synchronisation problem. This chapter sets out that three-way split.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `examples/companion_radio/MyMesh.cpp`, `src/helpers/ContactInfo.h`,
> `src/helpers/ChannelDetails.h` and `examples/companion_radio/NodePrefs.h`.

![Three columns: data living only on the node, data existing on both sides
and needing synchronisation, and data existing only in the app](../../../images/en/companion-information-model-1.svg)

## Contact

A contact is the stored description of another node: public key, name, type
and the last known path to it. How many fit differs per firmware variant —
see [Responsibilities](responsibilities.md).

What an app has to know:

- **The key is the identity, not the name.** Names are not unique and they
  change. `CMD_GET_CONTACT_BY_KEY` (30) looks up by key prefix.
- **The app can fetch only the contacts that changed.** `CMD_GET_CONTACTS`
  (4) optionally takes a timestamp, so only contacts changed since then come
  back. That is called incremental synchronisation. With hundreds of contacts
  over BLE it makes a noticeable difference.
- **Full is full.** When the table fills up, the node reports it with
  `PUSH_CODE_CONTACTS_FULL` (`0x90`). If automatic overwriting is enabled,
  the oldest non-favourite contact disappears and
  `PUSH_CODE_CONTACT_DELETED` (`0x8F`) follows. An app ignoring those two
  shows contacts that no longer exist.

Which kinds of contact get added automatically is configurable with a
bitmask: a single number whose individual bits each switch one option on or
off. The first bit below covers overwriting the oldest contact, the second
covers chat nodes, and so on:

`examples/companion_radio/MyMesh.cpp` r.142-146

```cpp
#define AUTO_ADD_OVERWRITE_OLDEST (1 << 0)  // 0x01 - overwrite oldest non-favourite when full
#define AUTO_ADD_CHAT             (1 << 1)  // 0x02 - auto-add Chat (Companion) (ADV_TYPE_CHAT)
#define AUTO_ADD_REPEATER         (1 << 2)  // 0x04 - auto-add Repeater (ADV_TYPE_REPEATER)
#define AUTO_ADD_ROOM_SERVER      (1 << 3)  // 0x08 - auto-add Room Server (ADV_TYPE_ROOM)
#define AUTO_ADD_SENSOR           (1 << 4)  // 0x10 - auto-add Sensor (ADV_TYPE_SENSOR)
```

## Channel

The node has a fixed number of channel slots. Each slot holds a channel name
and a shared key. The number of slots is fixed at compile time — 8 or 40 in
the companion builds — and the app reads it from the response to
`CMD_DEVICE_QUERY`.

Channels are read and written by index, not by name: `CMD_GET_CHANNEL` (31)
with an index, `CMD_SET_CHANNEL` (32) with index, name and key. An empty
slot is a valid answer.

The public group has a fixed key that lives in the firmware:

`examples/companion_radio/MyMesh.cpp` r.109

```cpp
#define PUBLIC_GROUP_PSK                "izOH6cXN6mrJ5e26oRXNcg=="
```

It is therefore not a secret and offers no confidentiality — it only makes
sure everyone decrypts the same way. See
[Channel Structure & PSK](../../technical/channel-structure.md).

What the node does **not** keep is which region scope belongs to which
channel. A scope is the area within which a message may circulate; MeshCore
calls such an area a region. That mapping exists only in the app, which sets
the scope before every transmission. When sending, the firmware picks the
temporary setting if there is one and otherwise the node's fixed default;
see
[Regions and Scopes](../../technical/regions-and-scopes.md).

## Message

A message exists on both sides, but not for equally long. On the node it sits
in the queue until the app fetches it; after that it is gone. The app can
keep it in its message history indefinitely.

There are three forms, and each has its own command:

| Form | Sending | Receiving |
|---|---|---|
| Direct message | `CMD_SEND_TXT_MSG` (2) | `RESP_CODE_CONTACT_MSG_RECV` (7) or `_V3` (16) |
| Channel message | `CMD_SEND_CHANNEL_TXT_MSG` (3) | `RESP_CODE_CHANNEL_MSG_RECV` (8) or `_V3` (17) |
| Datagram on a channel | `CMD_SEND_CHANNEL_DATA` (62) | `RESP_CODE_CHANNEL_DATA_RECV` (27) |

That third track is for apps exchanging structured data rather than text over
a channel. Such a separate packet of binary or otherwise structured data is
called a datagram. Room is tight:

`examples/companion_radio/MyMesh.cpp` r.101

```cpp
#define MAX_CHANNEL_DATA_LENGTH       (MAX_FRAME_SIZE - 9)
```

With `MAX_FRAME_SIZE` at 176 that leaves 167 bytes for the data itself. See
[The frame](../technical/frame-format.md).

## Advert and path

An advert is a node's self-announcement. The app sees two kinds of
notification for it: `PUSH_CODE_ADVERT` (`0x80`) for a known node and
`PUSH_CODE_NEW_ADVERT` (`0x8A`) for an unknown one. Only with the second is
the app faced with the choice of adding a contact.

A path is the route that turned out to work towards a contact. The node
tracks it and reports changes with `PUSH_CODE_PATH_UPDATED` (`0x81`). The
app can request it with `CMD_GET_ADVERT_PATH` (42) and clear it with
`CMD_RESET_PATH` (13). See [Route tracing](../../technical/route-tracing.md).

## The three-way split

| On the node only | On both sides | In the app only |
|---|---|---|
| private key | contact | message history |
| radio parameters | channel | channel → scope |
| PIN code | advert | own names and grouping |
| the message queue | path to a contact | read state |
| storage counters | clock | map data |

The left column never leaves the node, with one exception:
`CMD_EXPORT_PRIVATE_KEY` (23) takes the private key out, and
`CMD_IMPORT_PRIVATE_KEY` (24) puts one back. That is meant for migration to
a new device and is the most sensitive operation in the whole protocol.

The right column never enters the node. Only the middle column is a
synchronisation problem.

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.cpp)
  — `PUBLIC_GROUP_PSK`, `MAX_CHANNEL_DATA_LENGTH`, the auto-add bitmask
- [`src/helpers/ContactInfo.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ContactInfo.h)
  — the fields of a contact
- [`src/helpers/ChannelDetails.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ChannelDetails.h)
  — the fields of a channel slot

Related chapters:

- [Responsibilities](responsibilities.md) — why the split runs this way
- [Channel Structure & PSK](../../technical/channel-structure.md) — what a
  channel key does
- [Regions and Scopes](../../technical/regions-and-scopes.md) — the mapping
  the app maintains

Translated from Dutch by Anthropic Claude
