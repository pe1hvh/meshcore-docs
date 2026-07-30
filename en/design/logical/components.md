# Components

*RESPONSIBILITIES · BOUNDARIES · WHO KNOWS WHAT*

MeshCore consists of a handful of components with sharply drawn
responsibilities. This chapter describes what each part does and — more
importantly — what it does not know. The boundaries between the components are
what makes the design portable: the same mesh logic runs on four platform
families without noticing.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — `src/MeshCore.h`,
> `src/Dispatcher.h`, `src/Mesh.h`, `src/Packet.h`, `src/Identity.h` and the
> abstractions under `src/helpers/`.

## The stack in one picture

![Three layers stacked. At the bottom the hardware abstractions radio, board,
clock and entropy; in the middle packet handling and mesh logic; at the top the
application. Beside the stack the supporting components for storage,
permissions, control and interfaces.](../../../images/en/components-1.svg)

## The core

### Packet handling

The lowest layer with logic of its own. Responsible for: listening for
incoming data, turning received bytes into a packet, queueing outbound packets
and transmitting them at the right moment. It guards the airtime budget while
doing so and keeps counters of what was sent and received.

What this layer does not know: what a packet is about. It knows no messages, no
contacts and no encryption. To it, a packet is a block of bytes with a priority
and a moment at which it may leave.

### Mesh logic

The layer above. Here a packet is interpreted for the first time: which type is
it, is it meant for this node, must it be passed on, and if so with how much
delay. This is also where the decision lives to drop a packet because it came
past before.

What this layer does not know: how the radio works, and what the application
will do with a message. It offers the application a set of hooks and fills in
nothing itself.

### Application

The role from [Roles](roles.md). This holds the behaviour that makes a repeater
a repeater and a room server a room server. The application decides what
happens to an incoming message, when something is sent, and what appears on the
screen.

## The hardware abstractions

Four components shield the rest of the firmware from the hardware. They are all
pure: they contain no mesh logic, only a translation to what the board can do.

| Component | Responsible for | Knows nothing of |
|---|---|---|
| Radio | Getting bytes into and out of the air, estimating airtime, reporting signal strength | Packets, addressing, encryption |
| Board | Battery voltage, temperature, restart, sleep, startup reason | Radio, network, application |
| Clock | The current time in UNIX seconds | What that time is used for |
| Entropy | Supplying random bytes | Where those bytes end up |

The separation between radio and board is sharper than you would expect. The
board does know there is a moment before and after transmitting — it gets a
signal so it can switch on an amplifier, for instance — but it does not know
what is being transmitted.

## The supporting components

### Packet pool

Packets are not requested from the system's memory manager but taken from a
pre-reserved pool. That is a deliberate choice; see
[Design decisions](decisions.md). The same component manages the inbound and
outbound queues, with a priority and a scheduled send moment per packet.

### Seen table

Keeps track of which packets have already come past. Without this component
every packet in a network with several repeaters would circulate forever.

### Identity

Manages this node's key pair and other parties' public keys. The component
distinguishes two kinds: an identity of which only the public key is known, and
the own identity with the complete key pair. Only the second can sign.

### Access list

The list of known clients of a repeater, room server or sensor, with a
permission level per client and the last known route to it. Four levels: guest,
read only, read and write, administrator.

### Storage

Keeping identity, preferences, contacts and access list across a restart. To
the rest of the firmware this is one component; that the underlying file system
differs per platform family is a technical matter.

### Control

The command line shared by repeater, room server and sensor. It translates text
into actions and returns the answers — whether over a serial connection or in
an encrypted packet from a remote administrator.

### Interface

The connection to a companion application. Four variants — BLE, USB serial,
WiFi and ESP-NOW — behind one agreement, so the companion radio does not know
which one it is.

### Display

Writing out text and images to a screen. Eleven different display types share
the same contract, including one that does nothing: nodes without a screen get
that one.

### Bridge

Passing packets over a medium other than the radio — a serial connection or
ESP-NOW — so two mesh segments can be tied together.

### Sensor management

Reading attached measurement hardware and packing the values into a
standardised format.

## What is not there

Two things you would expect in a network stack are deliberately absent.

There is no routing table in the classical sense. A node builds no map of the
network; paths travel with the packets themselves. See
[Route tracing](../../technical/route-tracing.md).

There is no scheduler or task model. Everything runs in one loop. Components
get a turn to do something, and a component that hangs holds up the rest. That
is an explicit choice and not a shortcoming; [Design decisions](decisions.md)
goes into it.

## Sources

- [MeshCore `03b6ef4` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore `03b6ef4` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Dispatcher.h)
- [MeshCore `03b6ef4` — `src/Mesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Mesh.h)
- [MeshCore `03b6ef4` — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)

Translated from Dutch by Anthropic Claude
