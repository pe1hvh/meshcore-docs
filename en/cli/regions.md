# Regions

*REGION TREE · FLOOD PERMISSIONS · HOME REGION · SCOPE · SAVING*

These commands build a node's region tree, decide which regions may forward
flood traffic and set the scope the node itself sends with. What regions and
scopes are is explained in
[Regions and Scopes](../technical/regions-and-scopes.md); the Dutch layout in
[Regions: intent and practice](../technical/regions-in-practice.md).

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `src/helpers/RegionMap.cpp`, `src/helpers/RegionMap.h`,
> `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, and the official
> `docs/cli_commands.md`. Line numbers refer to this commit and can be
> reproduced with [`tools/cli-commands.py`](../../tools/cli-commands.py).

> [!NOTE]
> Changes made with `put`, `def`, `allowf`, `denyf`, `home` and `remove` apply
> immediately but only reach the file system after `region save`. The sensor
> cannot save regions: `saveRegions()` is not implemented there (`CommonCLI.h`
> r.97–99), so its region settings are lost after a restart.

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `region` | | — | | `CommonCLI.cpp` r.1005–1007 |
| `region put <name> [parent_name]` | | — | | `CommonCLI.cpp` r.1078 |
| `region def <token> [<token> ...]` | | — | | `CommonCLI.cpp` r.991 |
| `region load` | `not sensor` | — | | `CommonCLI.cpp` r.1008 |
| `region save` | `not sensor` | — | | `CommonCLI.cpp` r.1010–1014 |
| `region allowf <name>` / `region denyf <name>` | | — | | `CommonCLI.cpp` r.1015, r.1023 |
| `region get <name>` | | — | | `CommonCLI.cpp` r.1031 |
| `region home` / `region home <name>` | | — | | `CommonCLI.cpp` r.1043, r.1051 |
| `region default` / `region default {<name>\|<null>}` | | — | | `CommonCLI.cpp` r.1054, r.1075 |
| `region remove <name>` | | — | | `CommonCLI.cpp` r.1091 |
| `region list <allowed\|denied>` | | — | | `CommonCLI.cpp` r.1102 |

## Commands

### region

Shows the tree, one region per line, indented per level. `F` means flood is
allowed, `^` marks the home region (`RegionMap.cpp` r.285–302). A `#` in front
of the name is left out.

**Example** *(after the basic configuration below)*:

```text
region
  -> * F
 eu F
  nl F
   nl-ov F
```

**Netherlands:** no agreed setting.

### region put

Creates a region under the given parent, or under `*` if none is given. A new
region is always allowed to flood. Other replies: `Err - unknown parent` and
`Err - unable to put`.

**Example:**

```text
region put nl-ov nl
  -> OK - (flood allowed)
```

**Netherlands:** the basic configuration from
[Getting Started](../usage/getting-started.md), here for Overijssel:

```text
region put eu
region put nl eu
region put nl-ov nl
region default nl-ov
region save
```

### region def

Builds a tree on one line. Each token becomes a child of the cursor, which
starts at `*`; `name|jump` creates `name` and then moves the cursor to `jump`.
The reply is the new tree, or an error such as `Err - unknown jump: <name>`
(`CommonCLI.cpp` r.969–978). Regions created before the error remain.

**Example:**

```text
region def eu nl nl-ov
  -> * F
 eu F
  nl F
   nl-ov F
```

**Netherlands:** no agreed setting.

### region load

Loads a tree line by line. The number of leading spaces sets the level (1–7), an
`F` after the name allows flooding; an empty line finishes
(`simple_repeater/MyMesh.cpp` r.1175–1207). The loaded tree replaces the whole
existing tree: `resetFrom()` starts empty (`RegionMap.h` r.52). A region that
already existed keeps its id and flood permission. On the sensor the command
does nothing. The firmware ignores extra arguments after `load`, as the official
documentation lists them.

**Example:**

```text
region load
 eu F
  nl F
   nl-ov F

  -> OK - loaded 3 regions
```

**Netherlands:** no agreed setting.

### region save

Writes the regions to the file system. The sensor replies `Err - save failed`.

**Example:**

```text
region save
  -> OK
```

**Netherlands:** no agreed setting.

### region allowf / region denyf

Allows or forbids flood traffic for a region. The name may be a prefix; `*` is
the region for packets without a scope. Unknown name: `Err - unknown region`.

**Example:**

```text
region denyf eu
  -> OK
```

**Netherlands:** `region denyf *` only as agreed in
[Getting Started](../usage/getting-started.md).

### region get

Shows one region: name, parent in parentheses and `F` if flood is allowed. The
reply starts with a space.

**Example:**

```text
region get nl-ov
  ->  nl-ov (nl) F
```

**Netherlands:** no agreed setting.

### region home

Shows or sets the home region. Without a home region the reply is ` home is *`.

**Example:**

```text
region home nl-ov
  ->  home is now nl-ov
```

**Netherlands:** no agreed setting.

### region default

Shows or sets the scope the node itself sends with. An unknown name is created;
the region gets flood permission and is saved immediately. `<null>` clears the
scope.

**Example:**

```text
region default nl-ov
  ->  default scope is now nl-ov
```

**Netherlands:** your own province, see
[Getting Started](../usage/getting-started.md).

### region remove

Removes a region. The name must match exactly. A region with children gives
`Err - not empty`, an unknown one `Err - not found`.

**Example:**

```text
region remove nl-ov
  -> OK
```

**Netherlands:** no agreed setting.

### region list

Names of the regions that may or may not forward flood traffic, separated by
commas; `-none-` if there are none. The official documentation calls this
command serial-only; the firmware does not check that.

**Example:**

```text
region list allowed
  -> *,eu,nl,nl-ov
```

**Netherlands:** no agreed setting.

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/RegionMap.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/RegionMap.cpp)
- [MeshCore firmware — `src/helpers/RegionMap.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/RegionMap.h)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
