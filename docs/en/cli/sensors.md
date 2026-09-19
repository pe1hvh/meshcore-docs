# Sensors

*SETTINGS · GPIO · EXAMPLE HOOK*

Settings of the board's sensor manager, plus two commands that only the sensor
firmware knows and that are not in the official documentation.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `src/helpers/SensorManager.h`, `examples/simple_sensor/SensorMesh.cpp`,
> `examples/simple_sensor/main.cpp`, `src/MeshCore.h`, and the official
> `docs/cli_commands.md`. Line numbers refer to this commit and can be
> reproduced with [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `sensor list [start]` | | — | | `CommonCLI.cpp` r.328 |
| `sensor get <key>` / `sensor set <key> <value>` | | — | | `CommonCLI.cpp` r.309, r.317 |
| `io` / `io <hex>` / `io r<hex>` / `io s<hex>` / `io t<hex>` | `sensor only` | — | | `SensorMesh.cpp` r.427 |
| `magic` | `sensor only` | — | | `simple_sensor/main.cpp` r.35 |

## Commands

### sensor list

Shows the settings as `name=value`, after a line with the count. If not
everything fits in the reply, it ends with `... next:<n>`; pass that number as
`start`. If the board has none, the reply is `no custom var` (`SensorManager.h`
r.21).

**Example** *(board without settings)*:

```text
sensor list
  -> no custom var
```

### sensor get / sensor set

Reads or sets one setting. An unknown key gives `null` for `get` and
`can't find custom var` for `set`.

**Example** *(board without settings)*:

```text
sensor get gps
  -> null
```

### io

Reads or writes the board's GPIO outputs as a hex value. `io` reads; `io <hex>`
sets the value, `r` clears bits, `s` sets bits and `t` toggles bits. The reply
is always the value after the action. The comparison only looks at the first two
characters, so any command starting with `io` ends up here. A board that offers
no GPIO always gives `0` (`MeshCore.h` r.62–63).

**Example** *(board without GPIO)*:

```text
io s1
  -> 0
```

### magic

An example of a custom command: `simple_sensor/main.cpp` shows how a sensor
build can add commands through `handleCustomCommand()` (`SensorMesh.cpp` r.389).
It is in every build of this example firmware and does nothing else.

**Example:**

```text
magic
  -> **Magic now done**
```

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/SensorManager.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/SensorManager.h)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/main.cpp)
- [MeshCore firmware — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
