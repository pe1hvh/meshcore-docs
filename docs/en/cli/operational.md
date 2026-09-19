# Operational

*RESTART · CLOCK · ADVERTS · OTA · ERASE*

Commands that make the node *do* something rather than change a setting:
restart, power off, set the clock, send an advert, start a firmware update and
erase the file system. None of these commands has a default value.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `src/MeshCore.h`, `src/helpers/ESP32Board.cpp`, `src/helpers/NRF52Board.cpp`,
> and the official `docs/cli_commands.md`. Line numbers refer to this commit and
> can be reproduced with [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `reboot` | | — | | `CommonCLI.cpp` r.218 |
| `poweroff` / `shutdown` | | — | | `CommonCLI.cpp` r.216 |
| `clkreboot` | | — | | `CommonCLI.cpp` r.220 |
| `clock` | | — | | `CommonCLI.cpp` r.246 |
| `clock sync` | | — | | `CommonCLI.cpp` r.232 |
| `time <epoch_seconds>` | | — | | `CommonCLI.cpp` r.250 |
| `advert` | | — | | `CommonCLI.cpp` r.228 |
| `advert.zerohop` | | — | | `CommonCLI.cpp` r.224 |
| `start ota` | | — | | `CommonCLI.cpp` r.242 |
| `erase` | | — | yes | `CommonCLI.cpp` r.302 |

## Commands

### reboot

Restarts the node immediately. There is no reply, because `_board->reboot()`
does not return.

**Example:**

```text
reboot
```

### poweroff / shutdown

Powers the node off. Both names do the same. Again there is no reply.

**Example:**

```text
poweroff
```

### clkreboot

Sets the clock to `1715770351` (15 May 2024, 10:52:31 UTC) and restarts. This is
the way out when the clock is in the future: `time` and `clock sync` refuse a
time earlier than the current one. No reply.

**Example:**

```text
clkreboot
```

### clock

Shows the current time in UTC, in the form `hh:mm - d/m/yyyy UTC`.

**Example** *(clock at `1785412800`)*:

```text
clock
  -> 12:00 - 30/7/2026 UTC
```

### clock sync

Sets the clock to the sender's time plus one second, but only if that is later
than the node's own clock. On the serial console the sender time is always `0`,
so there the command always fails. It only works remotely, from an app.

**Example:**

```text
clock sync
  -> ERR: clock cannot go backwards
```

Remotely, with sender time `1785412800` and a clock that runs behind, the reply
is `OK - clock set: 12:00 - 30/7/2026 UTC`.

### time

Sets the clock to a Unix time, but only forwards. A time that is not later than
the current one gives `(ERR: clock cannot go backwards)` — with parentheses,
unlike `clock sync`.

**Example:**

```text
time 1785412800
  -> OK - clock set: 12:00 - 30/7/2026 UTC
```

### advert

Sends a flood advert, 1500 ms after the reply so that the reply goes out first.
The comparison only looks at the first six characters; `advert.zerohop` is
therefore caught earlier.

**Example:**

```text
advert
  -> OK - Advert sent
```

### advert.zerohop

Sends a zero-hop advert, for direct neighbours only, also after 1500 ms.

**Example:**

```text
advert.zerohop
  -> OK - zerohop advert sent
```

### start ota

Starts an over-the-air firmware update. What happens depends on the board. On
ESP32 a repeater or room server starts a WiFi access point `MeshCore-OTA` and
replies `Started: http://<address>/update` (`ESP32Board.cpp` r.13–16), unless
the build sets `DISABLE_WIFI_OTA`. On nRF52 BLE DFU starts and the reply is
`OK - mac: ` followed by the BLE address (`NRF52Board.cpp` r.319–362). Other
boards do not support it (`MeshCore.h` r.66) and reply `Error`.

**Example** *(board without OTA)*:

```text
start ota
  -> Error
```

### erase

Formats the file system. Serial console only.

**Example:**

```text
erase
  -> File system erase: OK
```

> [!WARNING]
> This erases everything the node has stored, including settings, regions and
> the ACL. There is no confirmation.

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore firmware — `src/helpers/ESP32Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ESP32Board.cpp)
- [MeshCore firmware — `src/helpers/NRF52Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/NRF52Board.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
