# Statistics

*CORE · RADIO · PACKETS · RESET*

Three commands return counters and measurements as a JSON object, one resets the
counters. All three roles use the same formatting from
`src/helpers/StatsFormatHelper.h`. The three read commands only work on the
serial console.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `src/helpers/StatsFormatHelper.h`, `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, and the official
> `docs/cli_commands.md`. Line numbers refer to this commit and can be
> reproduced with [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `clear stats` | | — | | `CommonCLI.cpp` r.295 |
| `stats-core` | | — | yes | `CommonCLI.cpp` r.474 |
| `stats-radio` | | — | yes | `CommonCLI.cpp` r.472 |
| `stats-packets` | | — | yes | `CommonCLI.cpp` r.470 |

## Commands

### clear stats

Resets the node's counters.

**Example:**

```text
clear stats
  -> (OK - stats reset)
```

### stats-core

Battery voltage in mV, uptime in seconds, error flags and the length of the
transmit queue (`StatsFormatHelper.h` r.12–13).

**Example** *(format; values depend on the node)*:

```text
stats-core
  -> {"battery_mv":<mV>,"uptime_secs":<s>,"errors":<n>,"queue_len":<n>}
```

### stats-radio

Noise floor, RSSI and SNR of the last packet, and transmit and receive airtime
in seconds (`StatsFormatHelper.h` r.27–28). The SNR has two decimals.

**Example** *(format)*:

```text
stats-radio
  -> {"noise_floor":<dBm>,"last_rssi":<dBm>,"last_snr":<dB>,"tx_air_secs":<s>,"rx_air_secs":<s>}
```

### stats-packets

Packet counters: received, sent, flood and direct per direction, and receive
errors (`StatsFormatHelper.h` r.44–45).

**Example** *(format)*:

```text
stats-packets
  -> {"recv":<n>,"sent":<n>,"flood_tx":<n>,"direct_tx":<n>,"flood_rx":<n>,"direct_rx":<n>,"recv_errors":<n>}
```

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/StatsFormatHelper.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/StatsFormatHelper.h)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
