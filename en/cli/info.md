# Info

*VERSION · BOARD*

Two commands that tell which firmware runs on which board. The role and the
public key are under [System](system.md).

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `examples/simple_repeater/MyMesh.h`,
> `variants/sensecap_solar/SenseCapSolarBoard.h`, and the official
> `docs/cli_commands.md`. Line numbers refer to this commit and can be
> reproduced with [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `ver` | | — | | `CommonCLI.cpp` r.305 |
| `board` | | — | | `CommonCLI.cpp` r.307 |

## Commands

### ver

Firmware version and build date. Both come from `FIRMWARE_VERSION` and
`FIRMWARE_BUILD_DATE`; without a build flag these are `v1.16.0` and `6 Jun 2026`
(`simple_repeater/MyMesh.h` r.71–76).

**Example** *(fallback values)*:

```text
ver
  -> v1.16.0 (Build: 6 Jun 2026)
```

### board

The name the board reports for itself.

**Example** *(SenseCap Solar, `SenseCapSolarBoard.h` r.36–38)*:

```text
board
  -> Seeed SenseCap Solar
```

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore firmware — `variants/sensecap_solar/SenseCapSolarBoard.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/sensecap_solar/SenseCapSolarBoard.h)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
