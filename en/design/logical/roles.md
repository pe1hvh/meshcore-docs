# Roles

*SIX APPLICATIONS · ONE PER BUILD · WHAT A ROLE DOES AND DOES NOT DO*

MeshCore is not one application but six. Which of the six a node is, is fixed
at compile time and cannot change afterwards. A repeater cannot become a room
server by flipping a setting; it is different firmware. This chapter describes
the six roles as logical actors: what each of them does, what it explicitly
does not do, and how they relate to one another.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — the six directories under
> `examples/` and the 508 `[env:...]` sections in `platformio.ini` plus the 79
> variant files. Figures from `tools/design-overview.py`.

## One role per build

Of the 508 build targets, 507 compile exactly one application. The 508th is
`env:native`, the test target that runs on the development machine and builds
no application at all. Not a single target combines two.

That is a hard property of the design and not an accident of the current
configuration: the applications each have their own `main.cpp` with their own
`setup()` and `loop()`. Two of those files in one binary give a duplicate
symbol definition.

| Role | Directory | Targets | Variant directories |
|---|---|---|---|
| Companion radio | `examples/companion_radio` | 174 | 76 |
| Repeater | `examples/simple_repeater` | 136 | 75 |
| KISS modem | `examples/kiss_modem` | 80 | 74 |
| Room server | `examples/simple_room_server` | 73 | 65 |
| Terminal chat | `examples/simple_secure_chat` | 26 | 24 |
| Sensor | `examples/simple_sensor` | 18 | 16 |

The second column counts build targets, the third the number of hardware
variants for which that role is available. The difference is bridge and display
variants of the same role on the same hardware.

![Six roles side by side, each with the layer it rests on: all six use the same
mesh core, but three of them are autonomous network services and three serve a
user or an attached machine.](../../../images/en/roles-1.svg)

## The six roles

### Companion radio

The largest role, and the only one not usable on its own. A companion radio is
a radio modem with a keyring: it holds the identity, the contact list and the
channels, but it has no user interface of its own for reading and writing
messages. A phone or desktop application connected over BLE, USB serial, WiFi
or ESP-NOW does that.

What the role does do: manage the identity, keep contacts, remember paths,
queue messages while the companion app is disconnected. What it does not do:
forward other people's packets. A companion radio is not a repeater, unless it
is explicitly put in client repeat mode.

### Repeater

An autonomous network service without a user. A repeater receives packets,
decides whether to pass them on, and transmits them again. It keeps track of
what it has already seen so the same packet does not go out twice, and it
guards its own airtime budget.

A repeater is also remotely manageable: it keeps a list of known clients with a
permission level per client, and accepts commands from whoever holds admin
rights there. What it does not do: store messages for later. Whoever is not
listening at the moment the repeater transmits, misses it.

### Room server

A repeater that does store. The room server holds messages and delivers them to
clients that turn up later — the bulletin board model. For that it needs a
synchronisation point per client: from which moment onwards should it catch up.

A room server is not a repeater plus storage; it is a separate application with
its own permission model. See [Room Server](../../technical/roomserver/introduction.md)
for the behaviour.

### Sensor

A node that collects measurements and sends them out on request or
periodically. The role keeps a time series in memory and packs measurements in
a standardised format. It shares its permission model with the repeater and the
room server.

### Terminal chat

The simplest role, and the only one a human operates directly without an app in
between: a chat client over the serial connection. Meant to demonstrate and
test, not for daily use. It is the only role that consists of a single file.

### KISS modem

Not a MeshCore application in the usual sense. A KISS modem passes raw frames
between the radio and an attached computer, following a protocol that comes
from packet radio. The node makes no decision at all about routing or
encryption; it leaves that to the software on the other side.

That makes the KISS modem the only role that largely bypasses the mesh logic,
and immediately explains why it is available on almost all hardware: little is
needed to run it.

## Which roles occur together

A working network needs at least two roles. Companion radios talk to each
other, but without repeaters they get no further than each other's direct
range. Repeaters among themselves form the fabric; room servers hang off it as
a service.

| Combination | Sensible |
|---|---|
| Companion radio + repeater | The standard setup |
| Repeater + repeater | Extending range |
| Companion radio + room server | Bulletin board without an intermediate repeater, within range only |
| Sensor + repeater | Measurement point read out over the network |
| KISS modem alone | Experiment or gateway to other software |

## Sources

- [MeshCore `03b6ef4` — `examples/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/examples)
- [MeshCore `03b6ef4` — `examples/companion_radio/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/MyMesh.h)
- [MeshCore `03b6ef4` — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore `03b6ef4` — `examples/kiss_modem/KissModem.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/kiss_modem/KissModem.h)

Translated from Dutch by Anthropic Claude
