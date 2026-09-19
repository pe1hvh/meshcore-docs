# Information model

*DATA OBJECTS · RELATIONS · WHAT IS VOLATILE AND WHAT REMAINS*

The components in this design exchange a limited number of data objects. This
chapter describes which those are, how they relate to one another, and — the
most underestimated question for a node running on a battery — what survives a
restart and what does not.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — `src/Packet.h`, `src/Identity.h`,
> `src/Mesh.h`, `src/helpers/ClientACL.h` and `src/helpers/ContactInfo.h`.

## The objects

![Seven data objects with their relations. Identity is central: contact, access
entry and the own node all point at it. Packet stands apart and carries a path;
channel stands loose from identity because group messages are not bound to a
sender.](../../../images/en/information-model-1.svg)

| Object | What it is | Survives a restart |
|---|---|---|
| Identity | A public key, and thereby a party whose signature can be checked | — |
| Own identity | This node's identity, with private key | Yes |
| Packet | The unit that goes over the air | No |
| Path | The sequence of nodes a packet travelled or must travel | Partly |
| Contact | A known counterparty with name, key and last known path | Yes |
| Channel | A group with a shared secret | Yes |
| Access entry | A known client with a permission level | Yes |
| Preferences | This node's settings | Yes |

## Identity is the hub

Almost everything hangs off the identity. The design makes a distinction there
that echoes everywhere: there is an identity of which you know only the public
key, and there is the own identity with the full key pair. The second is an
extension of the first, not something different.

That difference is the only thing separating signing from verifying. Every node
can verify any other node's signature; only the node itself can sign.

The short label by which a node is addressed in packets also follows from the
public key. That label is not a separate calculation but simply the start of
the key:

`src/Identity.h` l.18-25

```cpp
  int copyHashTo(uint8_t* dest) const { 
    memcpy(dest, pub_key, PATH_HASH_SIZE);    // hash is just prefix of pub_key
    return PATH_HASH_SIZE;
  }
  int copyHashTo(uint8_t* dest, uint8_t len) const { 
    memcpy(dest, pub_key, len);    // hash is just prefix of pub_key
    return len;
  }
```

That has a consequence the information model has to carry: the label is one
byte long. There are 256 possible values, and in a network of any size
collisions occur. The design deals with that explicitly by trying every
candidate on a collision rather than picking one.

## Packet and path

A packet carries its own route. There is no table in which a node looks up how
to reach somewhere; the path is in the packet or is built up along the way. See
[Packet Structure](../../technical/packet-structure.md) for the byte layout and
[Route tracing](../../technical/route-tracing.md) for the behaviour.

For the information model one thing matters: a path is a property of a
connection between two parties, not of the network. It is stored with the
contact or with the access entry, and it can go stale without anybody noticing
until a message fails to arrive.

## Volatile and persistent in one object

The access entry is the clearest example of an object containing both. Who is
in it, which permissions that party has and along which path it can be reached,
is kept. When that party was last heard from disappears on a restart.

`src/helpers/ClientACL.h` l.15-24

```cpp
struct ClientInfo {
  mesh::Identity id;
  uint8_t permissions;
  uint8_t out_path_len;
  uint8_t out_path[MAX_PATH_SIZE];
  uint8_t shared_secret[PUB_KEY_SIZE];
  uint32_t last_timestamp;   // by THEIR clock  (transient)
  uint32_t last_activity;    // by OUR clock    (transient)
```

The note `transient` in the source is the only place that distinction is
recorded. For anyone trying to explain a repeater's behaviour after a power
cut, it is the most important line in the file.

The shared secret is a third category: it is kept, but it is derived and thus
recomputable. It is there to save computation, not because it is
indispensable.

## Limits

The model has hard upper bounds, and they are not large. They are here because
they shape the design, not because they happen to be set that way.

| Limit | Default | Configurable per build |
|---|---|---|
| Known clients per node | 20 | Yes |
| Length of a path | 64 hops | No |
| Payload of a packet | 184 bytes | No |
| Contacts in a companion radio | varies per board | Yes |
| Channels in a companion radio | varies per board | Yes |

The first is the most keenly felt: a repeater knows twenty clients, and the
twenty-first does not fit. For a repeater running as a managed node that is
ample; for a repeater in a busy area it is not.

## What is not in the model

There is no object for a network, a neighbour or a connection. A node knows who
it knows and which path led there, but has no picture of the topology.
Repeaters do keep a neighbour count, but that is for statistics, not routing.

Nor is there an object for a message as a persistent item. Messages are
packets, and packets are volatile. The room server is the only role that
deviates and keeps messages; see
[Posts and synchronisation](../../technical/roomserver/posts-and-sync.md).

## Sources

- [MeshCore `03b6ef4` — `src/Identity.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Identity.h)
- [MeshCore `03b6ef4` — `src/Packet.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Packet.h)
- [MeshCore `03b6ef4` — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore `03b6ef4` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)

Translated from Dutch by Anthropic Claude
