# GPS

*ON/OFF · TIME · LOCATION · ADVERT POLICY*

Commands for a GPS receiver on the node. They exist only if the build sets
`ENV_INCLUDE_GPS=1` (`CommonCLI.cpp` r.355–433); otherwise each of them gives
`Unknown command`.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, and the official
> `docs/cli_commands.md`. Line numbers refer to this commit and can be
> reproduced with [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `gps` | `build flag` | — | | `CommonCLI.cpp` r.415 |
| `gps on` / `gps off` | `build flag` | `off` | | `CommonCLI.cpp` r.356, r.364 |
| `gps sync` | `build flag` | — | | `CommonCLI.cpp` r.372 |
| `gps setloc` | `build flag` | — | | `CommonCLI.cpp` r.380 |
| `gps advert` / `gps advert <none\|share\|prefs>` | `build flag` | `prefs` | | `CommonCLI.cpp` r.385 |

## Commands

### gps

Shows the state: `off` if the receiver is off, otherwise
`on, <active|deactivated>, <fix|no fix>, <n> sats`. Without a receiver:
`Can't find GPS`.

**Example** *(board without a GPS receiver)*:

```text
gps
  -> Can't find GPS
```

### gps on / gps off

Switches the receiver on or off and saves that. Without a switchable receiver:
`gps toggle not found`. The official documentation writes this as `gps <state>`.

**Example:**

```text
gps on
  -> ok
```

### gps sync

Synchronises the clock with GPS time. Without a receiver:
`gps provider not found`.

**Example:**

```text
gps sync
  -> ok
```

### gps setloc

Copies the GPS position into `lat` and `lon` and saves it.

**Example:**

```text
gps setloc
  -> ok
```

### gps advert

Which location goes into adverts: none (`none`), the current GPS position
(`share`) or the stored `lat`/`lon` (`prefs`). Another value gives `error`.

**Example:**

```text
gps advert
  -> > prefs
gps advert none
  -> ok
```

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
