# Neighbors

*NEIGHBORS · REMOVAL · DISCOVERY*

A repeater keeps track of which other repeaters it hears directly. These three
commands show that list, remove entries from it and ask the neighbours to
report. Only the repeater has such a list.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `examples/simple_repeater/MyMesh.cpp`, `examples/simple_repeater/MyMesh.h`,
> `examples/simple_room_server/MyMesh.h`, `examples/simple_sensor/SensorMesh.h`,
> `src/Utils.cpp`, and the official `docs/cli_commands.md`. Line numbers refer
> to this commit and can be reproduced with
> [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `neighbors` | `repeater only` | — | | `CommonCLI.cpp` r.261 |
| `neighbor.remove <pubkey_prefix>` | `effect: repeater` | — | | `CommonCLI.cpp` r.263 |
| `discover.neighbors` | `repeater only` | — | | `simple_repeater/MyMesh.cpp` r.1251 |

## Commands

### neighbors

Each line is `<first 4 bytes of public key>:<seconds ago>:<SNR × 4>`, newest
first (`MyMesh.cpp` r.1084–1100). Divide the last value by 4 for the SNR in dB
(`MyMesh.h` r.68). The list stops once the reply reaches 134 characters
(`MyMesh.cpp` r.1088); without neighbours the reply is `-none-`. Room server and
sensor reply `not supported` (`simple_room_server/MyMesh.h` r.207,
`simple_sensor/SensorMesh.h` r.71). The official documentation calls the second
field a timestamp; the firmware gives the number of seconds ago.

**Example** *(example keys from `tools/dm-example.py`)*:

```text
neighbors
  -> E3A0313A:312:26
EA1F69C3:1840:-6
```

`E3A0313A` was heard 312 seconds ago at SNR 6.5 dB, `EA1F69C3` 1840 seconds ago
at −1.5 dB. Only the first line gets the `  -> ` prefix.

### neighbor.remove

Removes every neighbour whose public key starts with the given hex prefix
(`MyMesh.cpp` r.1112–1121). The prefix must have an even number of hex
characters, otherwise the reply is `ERR: bad pubkey` (`src/Utils.cpp` r.124). An
empty prefix — the command ends right after the space — removes all neighbours.
Room server and sensor reply `OK` but do nothing (`CommonCLI.h` r.83–85).

**Example:**

```text
neighbor.remove E3A0313A
  -> OK
```

### discover.neighbors

Sends a discovery request to direct neighbours. The command takes no options;
with extra text the reply is `Err - discover.neighbors has no options`.

**Example:**

```text
discover.neighbors
  -> OK - Discover sent
```

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.h)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.h)
- [MeshCore firmware — `src/Utils.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Utils.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
