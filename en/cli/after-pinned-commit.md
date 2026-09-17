# After the pinned commit

*MAIN · CAD · FEM GAIN · EXTRA SF · ETHERNET*

The rest of this section is pinned to `03b6ef4`. More commands were added to
`main` after that. They are listed here separately, so that anyone running newer
firmware does not miss them, without letting go of the pin.

> [!WARNING]
> **Not verified against the pin.** This page was checked against `main` at
> commit `0679dbe`, 24 August 2026 — files `src/helpers/CommonCLI.cpp`,
> `src/helpers/nrf52/EthernetCLI.h`, `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, and the official
> `docs/cli_commands.md` at that commit. `main` changes constantly; check this
> against the firmware you run. The list can be reproduced with
> [`tools/cli-commands.py`](../../tools/cli-commands.py) and a second checkout.

## Overview

| Command | Source at `0679dbe` | Condition | In official documentation |
|---|---|---|---|
| `get cad` / `set cad <on\|off>` | `CommonCLI.cpp` r.470, r.818 | — | yes |
| `get radio.fem.rxgain` / `set radio.fem.rxgain <on\|off>` | `CommonCLI.cpp` r.544, r.847 | board with controllable FEM | yes |
| `get radio.fem.txgain` / `set radio.fem.txgain <on\|off>` | `CommonCLI.cpp` r.566, r.853 | board with controllable FEM | yes |
| `get extra.sf` / `set extra.sf <sf>[,<sf>…]` | `CommonCLI.cpp` r.780, r.976 | `set`: `USE_LR2021` | no |
| `eth.status` | `nrf52/EthernetCLI.h` r.89 | `ETHERNET_ENABLED` | yes |

## Commands

### cad

Hardware Channel Activity Detection before transmitting. `on` switches it on,
any other value off. All three roles set the default to `off`
(`simple_repeater/MyMesh.cpp` r.909, `simple_room_server/MyMesh.cpp` r.667,
`SensorMesh.cpp` r.731). According to the official documentation it is
independent of `int.thresh`. This is not certified LBT; the duty cycle limit
still applies, see [Regulations & Duty Cycle](../usage/regulations.md).

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
`on`/`off` gives `Error: state must be on or off`. Default `on` in all three
roles (for example `simple_room_server/MyMesh.cpp` r.684).

**Example:**

```text
set radio.fem.rxgain on
  -> OK - LoRa FEM RX gain on
```

### radio.fem.txgain

The same for the FEM's transmit gain. Default `off`
(`simple_room_server/MyMesh.cpp` r.685). The official documentation names the
Station G3 as an example and warns that the selected level must comply with
local limits.

**Example:**

```text
get radio.fem.txgain
  -> Error: unsupported
```

### extra.sf

Not in the official documentation. `set` exists only in builds with `USE_LR2021`
and takes up to three extra spreading factors, separated by commas; the reply is
`OK - extra SFs set` or `Invalid extra SF config`. `get` shows the list or
`No extra SF configured`.

**Example:**

```text
get extra.sf
  -> No extra SF configured
```

### eth.status

Status of the Ethernet connection on nRF52 boards with Ethernet. The reply is
`ETH: not connected` or the IP address with the TCP port for the CLI, 23 by
default (`nrf52/EthernetCLI.h` r.21).

**Example:**

```text
eth.status
  -> ETH: not connected
```

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/0679dbe/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/nrf52/EthernetCLI.h`](https://github.com/meshcore-dev/MeshCore/blob/0679dbe/src/helpers/nrf52/EthernetCLI.h)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/0679dbe/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/0679dbe/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/0679dbe/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/0679dbe/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
