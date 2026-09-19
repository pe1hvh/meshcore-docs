# Power management (nRF52)

*BOOTLOADER · POWER SOURCE · BOOT REASON · BOOT VOLTAGE*

Five read commands for nRF52 boards. The official documentation lists them under
*Bridge*, but in the firmware they depend on the platform: `NRF52_PLATFORM` and
`NRF52_POWER_MANAGEMENT` (`CommonCLI.cpp` r.884–928).

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `src/helpers/NRF52Board.cpp`, `variants/sensecap_solar/platformio.ini`, and
> the official `docs/cli_commands.md`. Line numbers refer to this commit and can
> be reproduced with [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `get bootloader.ver` | `build flag` | — | | `CommonCLI.cpp` r.884 |
| `get pwrmgt.support` | `build flag` | — | | `CommonCLI.cpp` r.903 |
| `get pwrmgt.source` | `build flag` | — | | `CommonCLI.cpp` r.909 |
| `get pwrmgt.bootreason` | `build flag` | — | | `CommonCLI.cpp` r.915 |
| `get pwrmgt.bootmv` | `build flag` | — | | `CommonCLI.cpp` r.923 |

## Commands

### bootloader.ver

Bootloader version, or `> unknown`. On other platforms: `ERROR: unsupported`.

**Example** *(ESP32)*:

```text
get bootloader.ver
  -> ERROR: unsupported
```

### pwrmgt.support

`> supported` if the build sets `NRF52_POWER_MANAGEMENT`, such as the SenseCap
Solar (`variants/sensecap_solar/platformio.ini` r.13), otherwise
`> unsupported`.

**Example** *(SenseCap Solar)*:

```text
get pwrmgt.support
  -> > supported
```

### pwrmgt.source

`> external` or `> battery`. Without power management:
`ERROR: Power management not supported`.

**Example:**

```text
get pwrmgt.source
  -> > battery
```

### pwrmgt.bootreason

Reason for the last reset and the last shutdown, as text (`NRF52Board.cpp` r.69
onwards).

**Example** *(board without power management)*:

```text
get pwrmgt.bootreason
  -> ERROR: Power management not supported
```

With power management the form is `> Reset: <reason>; Shutdown: <reason>`, for
example with reset reason `Reset Pin`.

### pwrmgt.bootmv

Voltage at start-up, as `> <n> mV`.

**Example** *(board without power management)*:

```text
get pwrmgt.bootmv
  -> ERROR: Power management not supported
```

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/NRF52Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/NRF52Board.cpp)
- [MeshCore firmware — `variants/sensecap_solar/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/sensecap_solar/platformio.ini)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
