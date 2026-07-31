# Designing MeshCore

*LOGICAL DESIGN · TECHNICAL DESIGN · SCOPE · READING GUIDE*

This section describes how MeshCore is put together. Not what goes over the
air — that is [Technical](../technical/layer-model.md) — but how the firmware
is divided up, which parts carry which responsibility, and how one codebase
produces 508 different builds. The section falls into a logical and a
technical design.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — the complete source tree, the root
> `platformio.ini` and all 79 `variants/*/platformio.ini`.

## Two layers

A logical design describes *what* a system is. Which parts exist, what each
part is responsible for, which agreements hold between those parts, and which
data travels between them. It does so without pointing at the implementation.
You can read it without knowing C++ and without knowing that a `Dispatcher.cpp`
exists.

A technical design describes *how* that is realised. Which class implements
which role, which files belong together, how the four platform families
implement the same abstraction in four ways, and how the build system
assembles the right combination. That is where file names and line numbers
live.

The split is not cosmetic. MeshCore's logical design is remarkably stable: the
roles, the layers and the contracts between those layers have been settled for
a long time. The technical design underneath does move — platforms are added,
drivers change, build targets appear and disappear between two commits. Read
the two as one and you end up with a document that is out of date every month.

![The logical design describes roles, components, contracts and data; the
technical design describes classes, platform realisation and the build system.
Arrows run from logical to technical: every logical part has a technical
counterpart.](../../images/en/design-layers-1.svg)

## What is not here

This section does not repeat content from other sections. Where the subject
touches, there is a reference.

| Subject | Lives in |
|---|---|
| Protocol layers and behaviour over the air | [The Layer Model](../technical/layer-model.md) |
| Byte layout of packets | [Packet Structure](../technical/packet-structure.md) |
| Choosing between the four platform families | [The four platform families](../platform/platform-families.md) |
| Physical buses and connections | [Hardware of a node](../hardware/introduction.md) |
| External libraries and their configuration | [Libraries in MeshCore](../libraries/introduction.md) |

In short: `technical/` describes the protocol, `hardware/` the physical node,
`libraries/` third-party code, and `design/` the structure of MeshCore's own
code.

## Reading guide

**Logical design**

- [Roles](logical/roles.md) — the six applications MeshCore can be
- [Components](logical/components.md) — what exists and what it covers
- [Contracts](logical/interfaces.md) — the agreements between components
- [Information model](logical/information-model.md) — the data and its relations
- [Variability](logical/variability.md) — how one codebase becomes 508 builds
- [Design decisions](logical/decisions.md) — the choices and what they cost

**Technical design**

- [The source tree](technical/source-layout.md) — what sits where, and the
  asymmetry
- [The class model](technical/class-model.md) — contract, implementation,
  standalone
- [Platform realisation](technical/platform-realisation.md) — four families,
  one abstraction
- [Radio realisation](technical/radio-realisation.md) — where the radio choice
  falls
- [The build system](technical/build-system.md) — how 508 targets come about
- [Compile-time configuration](technical/configuration.md) — 277 macros and
  their owner
- [Traceability](technical/traceability.md) — logical part to file and line

## Recomputing

Every figure in this section comes from `tools/design-overview.py`. That script
reads a MeshCore checkout and resolves, per build target, which application is
compiled, which platform family the target belongs to and which parts are
switched on:

```bash
python3 tools/design-overview.py /path/to/MeshCore
```

The script never counts on the name of an `[env:...]` section. Why that is a
trap is explained in [Variability](logical/variability.md).

## Sources

- [MeshCore `03b6ef4` — `src/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/src)
- [MeshCore `03b6ef4` — `examples/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/examples)
- [MeshCore `03b6ef4` — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)

Translated from Dutch by Anthropic Claude
