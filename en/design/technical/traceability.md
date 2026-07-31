# Traceability

*LOGICAL TO TECHNICAL · FILE AND LINE · EMPTY ROWS*

The logical design describes seventeen components. This chapter points each of
those seventeen out in the source tree, with file and line number. It closes
with the two things the logical design explicitly does *not* have — and which
therefore have no realisation either.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — every line number in the matrix
> was checked in the file named.

## What this matrix is for

Linking every logical element to the source code makes the design checkable
and verifiable. This table records that link: anyone doubting whether the mesh
logic really knows nothing of the radio can open `src/Mesh.h` r.26 and look.

The matrix runs one way. From logical component to realisation, not the other
way round — not every class in the source tree belongs to a logical component.
The 55 standalone classes from [the class model](class-model.md) are largely
utilities without a counterpart in the logical design.

## The matrix

| Logical component | Realisation |
|---|---|
| Packet handling | `Dispatcher`, `src/Dispatcher.h` r.116 |
| Mesh logic | `Mesh`, `src/Mesh.h` r.26 |
| Application | `MyMesh` / `SensorMesh` / `KissModem` in `examples/` |
| Radio | `mesh::Radio`, `src/Dispatcher.h` r.22 |
| Board | `mesh::MainBoard`, `src/MeshCore.h` r.45 |
| Clock | `mesh::RTCClock`, `src/MeshCore.h` r.80 |
| Entropy | `mesh::RNG`, `src/Utils.h` r.9 |
| Packet pool | `mesh::PacketManager`, `src/Dispatcher.h` r.85; implementation `StaticPoolPacketManager`, `src/helpers/StaticPoolPacketManager.h` r.21 |
| Seen table | `mesh::MeshTables`, `src/Mesh.h` r.16; implementation `SimpleMeshTables`, `src/helpers/SimpleMeshTables.h` r.11 |
| Identity | `mesh::Identity`, `src/Identity.h` r.11; `LocalIdentity` r.54 |
| Access list | `ClientACL`, `src/helpers/ClientACL.h` r.40; `ClientInfo` r.15 |
| Storage | `IdentityStore`, `src/helpers/IdentityStore.h` r.14 |
| Control | `CommonCLI`, `src/helpers/CommonCLI.h` r.117; contract `CommonCLICallbacks` r.68 |
| Interface | `BaseSerialInterface`, `src/helpers/BaseSerialInterface.h` r.7 |
| Display | `DisplayDriver`, `src/helpers/ui/DisplayDriver.h` r.6 |
| Bridge | `AbstractBridge`, `src/helpers/AbstractBridge.h` r.5; `BridgeBase` r.21 in `bridges/BridgeBase.h` |
| Sensor management | `SensorManager`, `src/helpers/SensorManager.h` r.12 |
| Routing table | *none — paths travel with the packet* |
| Task model | *none — everything runs in one loop* |

## What the matrix shows

Three things stand out.

**The core is small.** Seven of the seventeen components point at a file in
`src/`, and those seven files are 2332 lines together. The other ten sit in
`src/helpers/` or in `examples/`.

**Seven components are a contract, not a class.** Radio, board, clock,
entropy, interface, display and sensor management point at an interface class
class. What hangs underneath in a concrete build depends on the build target —
see [Platform realisation](platform-realisation.md) and
[Radio realisation](radio-realisation.md).

**Two components have no class at all.** The application points at three
different classes across six directories, because exactly one application
compiles per build. Those are `MyMesh` (five times, in five different files),
`SensorMesh` and `KissModem`.

## The two empty rows

At the bottom of the matrix are two rows without a realisation. They are there
deliberately, and they belong in the table: a matrix with the empty rows left
out suggests that everything has been realised.

**Routing table.** MeshCore builds no map of the network. A node does not know
which neighbours exist or by which route a destination can be reached; the
path travels with the packet. There is therefore no class maintaining it, and
no file where one should sit. See
[Route tracing](../../technical/route-tracing.md) for how it does work.

**Task model.** There is no scheduler and no task model. Everything runs in
one loop, and components get a turn to do something. A component that hangs
holds up the rest. The absence is a choice and not a shortcoming;
[Design decisions](../logical/decisions.md) goes into what that choice costs.

> [!NOTE]
> Both are described in [Components](../logical/components.md) under *What is
> not there*. They appear here as an empty row because the matrix would
> otherwise give the impression that the logical design consists solely of
> realised parts.

## Sources

- [MeshCore `03b6ef4` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Dispatcher.h)
- [MeshCore `03b6ef4` — `src/Mesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Mesh.h)
- [MeshCore `03b6ef4` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore `03b6ef4` — `src/Identity.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Identity.h)
- [MeshCore `03b6ef4` — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore `03b6ef4` — `src/helpers/CommonCLI.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.h)

Translated from Dutch by Anthropic Claude
