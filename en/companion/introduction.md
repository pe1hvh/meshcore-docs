# The companion interface

*APP · NODE · FRAMES · OPCODES · SOURCE HIERARCHY*

A companion node is a MeshCore radio operated through an app; it has no full
control panel of its own. Everything a person does with it — typing a
message, adding a contact, changing the transmit power — the app sends to the
node as one delimited block of data. Such a block is called a **frame**
throughout this documentation. This section describes that interface: which
agreements hold between app and node, and how you build a client on top of it
yourself.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `examples/companion_radio/MyMesh.cpp`,
> `examples/companion_radio/MyMesh.h` and the official
> `docs/companion_protocol.md`. In addition against `meshcore_py` v2.3.8
> (commit `c487efb`) and `meshcore.js` v1.13.0 (commit `bbe1f93`).

![The app talks to the companion node over BLE, USB or TCP; the node talks
to the mesh over LoRa. The app never reaches the mesh directly](../../images/en/companion-context-1.svg)

> [!WARNING]
> **This section describes the rules a client has to follow, but it is not an
> official specification.** It describes how to build your own companion
> client,
> derived from the firmware source at commit `03b6ef4` and checked against
> `meshcore_py` v2.3.8. There is no version guarantee: `FIRMWARE_VER_CODE`
> changes between releases, and the official `docs/companion_protocol.md`
> currently describes 7 of the 58 commands. Always check against the source
> that belongs to your firmware.

## The terms in one place

The rest of this section uses a handful of technical terms. They are
collected here so you do not have to look them up while reading.

| Term | What it means |
|---|---|
| companion node | a MeshCore radio operated through an app |
| client | the app or software that talks to the node |
| transport | the connection it talks over: BLE, USB serial or TCP |
| frame | one delimited block of data between app and node, at most 176 bytes here |
| opcode | the first byte of a frame: the number stating which command, response or unsolicited notification it holds |
| payload | the data content of the frame, everything after the opcode |
| unsolicited notification | a frame the node sends of its own accord, so not an answer to a question; its number is called a push code |
| advert | a message with which a node announces itself on the network |
| scope | the area within which a message may circulate |
| firmware variant | one specific compiled version of the firmware; limits such as the contact count differ per variant |

Fuller definitions are in [Terminology](../reference/terminology.md).

## Why this section exists

The official MeshCore Companion App is closed. There is no public
repository of the Android, iOS or web version, so no design can be read out
of it. What *is* public is the contract that app adheres to: the firmware
receiving the frames, and two official libraries implementing the other
side.

So this section does not describe the design of the official app, but the
protocol agreements every compatible app has to meet.

## The four sources and how complete they are

Not every source is equally complete. The ratio was measured with
`tools/companion-opcodes.py` and is reproducible:

| Source | Commands | Response and push codes |
|---|---|---|
| firmware `MyMesh.cpp` | 58/58 | 46/46 |
| `meshcore_py` v2.3.8 | 56/58 | 46/46 |
| `meshcore.js` v1.13.0 | 39/58 | not compared |
| `docs/companion_protocol.md` | 7/58 | 5/46 |

The firmware decides: it determines what happens. After the firmware,
`meshcore_py` is the most complete source — that library knows all 46
response and push codes and misses only two commands,
`CMD_SEND_CHANNEL_DATA` (62) and `CMD_SEND_RAW_PACKET` (65). `meshcore.js`
lags further behind.

The official spec is the weakest source, and says so itself: at the top of
the file it states that the document is still in development and may contain
inaccuracies. The header names "Companion Firmware v1.12.0+" and the last
change is dated 8 March 2026, while the firmware this section was written
against is v1.16.0. Where this section deviates from the spec, that is
noted.

## What is not here

This section does not repeat content from other sections. Where the subject
touches, there is a reference.

| Subject | Found in |
|---|---|
| Byte layout of the frame header on serial | [USB Serial](../hardware/interfaces/usb-serial.md) |
| BLE stack, GATT, NUS and pairing | [BLE Architecture](../hardware/interfaces/ble-architecture.md) |
| WiFi setup and credentials in the binary | [WiFi as a companion link](../hardware/interfaces/wifi.md) |
| What travels over the air | [The Layer Model](../technical/layer-model.md) |
| Structure of the firmware itself | [Design of MeshCore](../design/introduction.md) |
| Which boards can be a companion | [Node matrix](../platform/node-matrix.md) |

In short: `hardware/interfaces/` describes the wire and the bytes on it,
`companion/` describes what those bytes mean.

## Reading guide

The logical part describes *what* the interface is, without pointing at C++.
The technical part describes *how* you use it, with file names and line
numbers.

- **Logical design**
  - [Responsibilities](logical/responsibilities.md) — who keeps what
  - [The interaction model](logical/interaction-model.md) — request,
    response, push and version negotiation
  - [Information model](logical/information-model.md) — the data that moves
    back and forth
- **Technical design**
  - [The three transports](technical/transports.md) — what the protocol
    demands of a connection
  - [The frame](technical/frame-format.md) — what fits into the 176 bytes
  - [The command groups](technical/command-groups.md) — all 58 commands,
    ordered
  - [Architecture of a client](technical/client-architecture.md) — the
    layers a working client consists of

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.cpp)
  — the opcode table and all command handling
- [`examples/companion_radio/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.h)
  — `FIRMWARE_VER_CODE`, `MAX_CONTACTS`, `OFFLINE_QUEUE_SIZE`
- [`docs/companion_protocol.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/docs/companion_protocol.md)
  — the official spec, with its own caveat

Official libraries:

- [`meshcore-dev/meshcore_py`](https://github.com/meshcore-dev/meshcore_py)
  — Python, v2.3.8
- [`meshcore-dev/meshcore.js`](https://github.com/meshcore-dev/meshcore.js)
  — JavaScript, v1.13.0

Reproduction:

- `tools/companion-opcodes.py` — counts the opcodes and the coverage per
  source
- `tools/companion-opcodes-snapshot.json` — the result at commit `03b6ef4`

Related chapters:

- [USB Serial](../hardware/interfaces/usb-serial.md) — the frame byte by
  byte
- [GitHub Repositories](../project/github.md) — the official repositories
- [Terminology](../reference/terminology.md) — the terms used in this
  section

Translated from Dutch by Anthropic Claude
