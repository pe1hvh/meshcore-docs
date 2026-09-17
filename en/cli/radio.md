# Radio

*FREQUENCY · BANDWIDTH · SF · CR · TRANSMIT POWER*

The node's radio parameters: frequency, bandwidth, spreading factor and coding
rate, the chip's transmit power and the receive gain. Changes to the radio
parameters take effect only after a restart; `tempradio` tries them out
temporarily.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `platformio.ini`, `examples/simple_repeater/MyMesh.cpp`,
> `src/helpers/TxtDataHelpers.cpp`, and the official `docs/cli_commands.md`.
> Line numbers refer to this commit and can be reproduced with
> [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `get radio` / `set radio <freq>,<bw>,<sf>,<cr>` | | `869.618,62.5,8,5` | | `CommonCLI.cpp` r.571, r.808 |
| `get tx` / `set tx <dbm>` | | per board, fallback 20 | | `CommonCLI.cpp` r.691, r.847 |
| `tempradio <freq>,<bw>,<sf>,<cr>,<timeout_mins>` | | — | | `CommonCLI.cpp` r.274 |
| `get freq` / `set freq <frequency>` | | `869.618` | `set` only | `CommonCLI.cpp` r.696, r.849 |
| `get radio.rxgain` / `set radio.rxgain <on\|off>` | `build flag` · `effect: repeater` | R `on` ¹ · RS/S `off` | | `CommonCLI.cpp` r.565, r.805 |

The default `869.618,62.5,8,5` comes from `platformio.ini` r.28–30 (frequency,
bandwidth, SF) and the fallback `LORA_CR 5`; no variant overrides them. The
official documentation states `869.525,250,11,5`. An unmodified build is
therefore on **SF8**, while the Dutch network uses SF7.

## Commands

### radio

Frequency in MHz (150–2500), bandwidth in kHz (7–500), SF (5–12) and CR (5–8).
Outside those limits the reply is `Error, invalid radio params`. `get radio`
shows the frequency with the firmware's float formatting, hence `869.6179809`
(`TxtDataHelpers.cpp` r.52–130).

**Example:**

```text
get radio
  -> > 869.6179809,62.5,8,5
set radio 869.618,62.5,7,5
  -> OK - reboot to apply
```

**Netherlands:** `set radio 869.618,62.5,7,5`, see
[Getting Started](../usage/getting-started.md). The network moved to SF7 in May
2026; a node on SF8 does not hear the rest.

### tx

Transmit power of the LoRa chip in dBm. It takes effect immediately. `set tx`
checks no limits; at the next start the firmware constrains the value to −9…30
(`CommonCLI.cpp` r.105). An amplifier on the board comes on top of that.

**Example:**

```text
set tx 20
  -> OK
get tx
  -> > 20
```

**Netherlands:** see [Regulations & Duty Cycle](../usage/regulations.md) for the
difference between transmit power and radiated power (ERP).

### tempradio

Sets the radio parameters temporarily, for the given number of minutes. Nothing
is saved. The limits are 150–2500 MHz, 7–500 kHz, SF 5–12, CR 5–8 and a time
greater than 0; otherwise `Error, invalid params`. The official documentation
states 300–2500 MHz and 7.8–500 kHz.

**Example:**

```text
tempradio 869.618,62.5,7,5,30
  -> OK - temp params for 30 mins
```

### freq

The frequency only. `set freq` works on the serial console only and takes effect
after a restart.

**Example:**

```text
set freq 869.618
  -> OK - reboot to apply
get freq
  -> > 869.6179809
```

**Netherlands:** 869.618 MHz, see
[Getting Started](../usage/getting-started.md). That is also the build default.

### radio.rxgain

Boosted receive gain. Exists only in builds with `USE_SX1262`, `USE_SX1268` or
`USE_LR1110`. Only the repeater applies the setting, at start-up and directly
after `set` (`MyMesh.cpp` r.965, r.1063). The official documentation states `on`
as the default for all roles.

**Example:**

```text
set radio.rxgain on
  -> OK
get radio.rxgain
  -> > on
```

¹ For SX1262/SX1268 builds, unless `SX126X_RX_BOOSTED_GAIN` says otherwise
(`MyMesh.cpp` r.913–919). In LR1110 builds the repeater does not set the value
and it is `off`.

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `src/helpers/TxtDataHelpers.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/TxtDataHelpers.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
