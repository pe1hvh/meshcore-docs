# Bridge

*RS232 · ESP-NOW · DELAY · SOURCE*

A bridge passes packets over a second path next to LoRa: RS232 or ESP-NOW.
Except for `get bridge.type`, these commands exist only in a build with
`WITH_RS232_BRIDGE` or `WITH_ESPNOW_BRIDGE`, and only the repeater derives
`WITH_BRIDGE` from that (`simple_repeater/MyMesh.h` r.16–24).

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `examples/simple_repeater/MyMesh.h`, `examples/simple_repeater/MyMesh.cpp`,
> and the official `docs/cli_commands.md`. Line numbers refer to this commit and
> can be reproduced with [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `get bridge.type` | | — | | `CommonCLI.cpp` r.856 |
| `get bridge.enabled` / `set bridge.enabled <on\|off>` | `repeater only` · `build flag` | `on` | | `CommonCLI.cpp` r.701, r.867 |
| `get bridge.delay` / `set bridge.delay <ms>` | `repeater only` · `build flag` | `500` | | `CommonCLI.cpp` r.706, r.869 |
| `get bridge.source` / `set bridge.source <rx\|tx>` | `repeater only` · `build flag` | `logTx` | | `CommonCLI.cpp` r.715, r.871 |
| `get bridge.baud` / `set bridge.baud <rate>` | `repeater only` · `build flag` | `115200` | | `CommonCLI.cpp` r.721, r.875 |
| `get bridge.channel` / `set bridge.channel <1-14>` | `repeater only` · `build flag` | `1` | | `CommonCLI.cpp` r.733, r.879 |
| `get bridge.secret` / `set bridge.secret <secret>` | `repeater only` · `build flag` | `LVSITANOS` | | `CommonCLI.cpp` r.743, r.881 |

## Commands

### bridge.type

Which type of bridge is in the build: `rs232`, `espnow` or `none`.

**Example:**

```text
get bridge.type
  -> > none
```

**Netherlands:** no agreed setting.

### bridge.enabled

Switches the bridge on or off, immediately. The firmware sets the default to
`on` (`MyMesh.cpp` r.898); the official documentation states `off`.

**Example:**

```text
get bridge.enabled
  -> > on
set bridge.enabled off
  -> OK
```

**Netherlands:** no agreed setting.

### bridge.delay

Delay in milliseconds for packets through the bridge, 0–10000. Otherwise
`Error: delay must be between 0-10000 ms`.

**Example:**

```text
set bridge.delay 1000
  -> OK
```

**Netherlands:** no agreed setting.

### bridge.source

Whether the bridge passes on received (`logRx`) or transmitted (`logTx`)
packets. `set` only checks whether the value starts with `rx`; everything else
becomes `logTx`. The official documentation gives `logRx` and `logTx` as values,
so `set bridge.source logRx` sets **logTx**.

**Example:**

```text
set bridge.source rx
  -> OK
get bridge.source
  -> > logRx
```

**Netherlands:** no agreed setting.

### bridge.baud

RS232 only. Speed from 9600 to 115200 (`BRIDGE_MAX_BAUD`, `CommonCLI.cpp` r.9);
the bridge restarts immediately.

**Example:**

```text
set bridge.baud 57600
  -> OK
```

**Netherlands:** no agreed setting.

### bridge.channel

ESP-NOW only. WiFi channel 1–14; otherwise
`Error: channel must be between 1-14`.

**Example:**

```text
set bridge.channel 6
  -> OK
```

**Netherlands:** no agreed setting.

### bridge.secret

ESP-NOW only. Key for the XOR encryption of bridge packets, at most 15
characters (`CommonCLI.h` r.53). The firmware sets `LVSITANOS` (`MyMesh.cpp`
r.904); the official documentation says the default differs per board.

**Example:**

```text
get bridge.secret
  -> > LVSITANOS
```

**Netherlands:** no agreed setting.

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
