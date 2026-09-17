# Logging

*RX LOG · START · STOP · ERASE · SHOW*

A node can write received packets to a file. On the repeater that is
`/packet_log` (`MyMesh.h` r.81). Four commands switch this on and off, erase the
file and show it.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `examples/simple_repeater/MyMesh.cpp`, `examples/simple_repeater/MyMesh.h`,
> and the official `docs/cli_commands.md`. Line numbers refer to this commit and
> can be reproduced with [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `log start` | | — | | `CommonCLI.cpp` r.458 |
| `log stop` | | — | | `CommonCLI.cpp` r.461 |
| `log erase` | | — | | `CommonCLI.cpp` r.464 |
| `log` | | — | yes | `CommonCLI.cpp` r.467 |

## Commands

### log start

Starts logging. The reply starts with three spaces.

**Example:**

```text
log start
  ->    logging on
```

**Netherlands:** no agreed setting.

### log stop

Stops logging.

**Example:**

```text
log stop
  ->    logging off
```

**Netherlands:** no agreed setting.

### log erase

Erases the log file.

**Example:**

```text
log erase
  ->    log erased
```

**Netherlands:** no agreed setting.

### log

Writes the log file to the serial console (`MyMesh.cpp` r.1042) and ends with
`EOF`.

**Example:**

```text
log
  ->    EOF
```

With an empty log file, `EOF` is all that appears.

**Netherlands:** no agreed setting.

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
