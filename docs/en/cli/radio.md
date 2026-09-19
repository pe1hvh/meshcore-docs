# Radio

*FREQUENCY · BANDWIDTH · SF · CR · TRANSMIT POWER*

The node's radio parameters: frequency, bandwidth, spreading factor and coding
rate, the chip's transmit power and the receive gain. Changes to the radio
parameters take effect only after a restart; `tempradio` tries them out
temporarily.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.17.1, commit `d929643`, 14 August 2026 — files `src/helpers/CommonCLI.cpp`,
> `platformio.ini`, `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_room_server/MyMesh.cpp`, `examples/simple_sensor/SensorMesh.cpp`,
> `src/helpers/TxtDataHelpers.cpp`, and the official `docs/cli_commands.md`.
> Line numbers refer to this commit and can be reproduced with
> [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `get radio` / `set radio <freq>,<bw>,<sf>,<cr>` | | `869.618,62.5,8,5` | | `CommonCLI.cpp` r.588, r.859 |
| `get tx` / `set tx <dbm>` | | per board, fallback 20 | | `CommonCLI.cpp` r.708, r.898 |
| `tempradio <freq>,<bw>,<sf>,<cr>,<timeout_mins>` | | — | | `CommonCLI.cpp` r.241 |
| `get freq` / `set freq <frequency>` | | `869.618` | `set` only | `CommonCLI.cpp` r.713, r.900 |
| `get radio.rxgain` / `set radio.rxgain <on\|off>` | `effect: repeater, room server` | R/RS `on` ¹ · S `off` | | `CommonCLI.cpp` r.535, r.845 |
| `get cad` / `set cad <on\|off>` | | `off` | | `CommonCLI.cpp` r.470, r.818 |
| `get radio.fem.rxgain` / `set radio.fem.rxgain <on\|off>` | board with a controllable FEM | `on` | | `CommonCLI.cpp` r.544, r.847 |
| `get radio.fem.txgain` / `set radio.fem.txgain <on\|off>` | board with a controllable FEM | `off` | | `CommonCLI.cpp` r.566, r.853 |
| `get extra.sf` / `set extra.sf <sf>[,<sf>…]` | `build flag` (`set`) | — | | `CommonCLI.cpp` r.780, r.976 |

The default `869.618,62.5,8,5` comes from `platformio.ini` r.29–31 (frequency,
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
(`CommonCLI.cpp` r.116). An amplifier on the board comes on top of that.

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

Boosted receive gain. Up to v1.16.0 the command existed only in builds with
`USE_SX1262`, `USE_SX1268` or `USE_LR1110`; since v1.17.1 it is always compiled
in and a board that cannot do it replies `Error: unsupported`. Repeater and room
server apply the setting, at start-up and directly after `set`
(`simple_repeater/MyMesh.cpp` r.981, r.1080, `simple_room_server/MyMesh.cpp`
r.727). The sensor does nothing with it. The official documentation states `on`
as the default for all roles.

**Example:**

```text
set radio.rxgain on
  -> OK
get radio.rxgain
  -> > on
```

¹ For SX1262/SX1268 builds, unless `SX126X_RX_BOOSTED_GAIN` says otherwise
(`simple_repeater/MyMesh.cpp` r.927–933, `simple_room_server/MyMesh.cpp`
r.677–683). In LR1110 builds they do not set the value and it is `off`. Up to
v1.16.0 the room server did not set it either; v1.17.1 brings it in line with
the repeater.

### cad

Hardware Channel Activity Detection before transmitting. `on` enables it, any
other value disables it. All three roles set the default to `off`
(`simple_repeater/MyMesh.cpp` r.909, `simple_room_server/MyMesh.cpp` r.667,
`simple_sensor/SensorMesh.cpp` r.731). According to the official documentation
it runs independently of `int.thresh`. This is not certified LBT; the duty cycle
limit still applies, see [Regulations & Duty Cycle](../usage/regulations.md).

**Example:**

```text
set cad on
  -> OK
get cad
  -> > on
```

### radio.fem.rxgain

The LNA of an external front-end module (FEM), separate from `radio.rxgain`.
Without a controllable FEM the reply is `Error: unsupported`; a value other than
`on`/`off` gives `Error: state must be on or off`. The default is `on` for all
three roles (for example `simple_room_server/MyMesh.cpp` r.684).

**Example:**

```text
set radio.fem.rxgain on
  -> OK - LoRa FEM RX gain on
```

### radio.fem.txgain

The same for the FEM transmit gain. The default is `off`
(`simple_room_server/MyMesh.cpp` r.685). The official documentation gives the
Station G3 as an example and warns that the selected level must comply with
local limits.

**Example:**

```text
get radio.fem.txgain
  -> Error: unsupported
```

### extra.sf

Not in the official documentation. `set` exists only in builds with
`USE_LR2021` and takes up to three extra spreading factors, separated by commas;
the reply is `OK - extra SFs set` or `Invalid extra SF config`. `get` shows the
list or `No extra SF configured`.

**Example:**

```text
get extra.sf
  -> No extra SF configured
```

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/d929643/platformio.ini)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `src/helpers/TxtDataHelpers.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/TxtDataHelpers.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/d929643/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
