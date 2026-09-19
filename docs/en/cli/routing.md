# Routing

*FORWARDING · DELAY · DUTY CYCLE · ADVERTS · HOP LIMITS*

How a node passes traffic on: whether it forwards, how long it waits, how much
airtime it may use, how often it announces itself and how far flood packets may
travel. Most of the Dutch agreements are here; they come from
[Regulations & Duty Cycle](../usage/regulations.md).

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `examples/simple_repeater/MyMesh.cpp`, `examples/simple_repeater/MyMesh.h`,
> `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_room_server/MyMesh.h`,
> `examples/simple_sensor/SensorMesh.cpp`, and the official
> `docs/cli_commands.md`. Line numbers refer to this commit and can be
> reproduced with [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

> [!WARNING]
> The firmware default for `dutycycle` is 50 %. That is far above the 10 % that
> applies in the Netherlands. A freshly flashed node is therefore not compliant
> until you give `set dutycycle 10`. See
> [Regulations & Duty Cycle](../usage/regulations.md). The Dutch-MeshCore fork
> solves this with `set dutycycle auto`, which derives the limit from the
> sub-band — see [Forks & variants](https://domca.nl/#analysis/forks-and-variants).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `get repeat` / `set repeat <on\|off>` | | R `on` · RS `off` · S `off` | | `CommonCLI.cpp` r.560, r.798 |
| `get path.hash.mode` / `set path.hash.mode <0\|1\|2>` | | `0` | | `CommonCLI.cpp` r.661, r.835 |
| `get loop.detect` / `set loop.detect <off\|minimal\|moderate\|strict>` | `effect: repeater` | `off` | | `CommonCLI.cpp` r.671, r.837 |
| `get txdelay` / `set txdelay <0-2>` | | `0.5` | | `CommonCLI.cpp` r.606, r.815 |
| `get direct.txdelay` / `set direct.txdelay <0-2>` | | R `0.3` · RS/S `0.2` | | `CommonCLI.cpp` r.642, r.823 |
| `get rxdelay` / `set rxdelay <0-20>` | | `0.0` | | `CommonCLI.cpp` r.597, r.813 |
| `get dutycycle` / `set dutycycle <1-100>` | | `50` | | `CommonCLI.cpp` r.483, r.770 |
| `get af` / `set af <value>` | | `1.0` | | `CommonCLI.cpp` r.495, r.775 |
| `get int.thresh` / `set int.thresh <value>` | | `0` | | `CommonCLI.cpp` r.499, r.777 |
| `get agc.reset.interval` / `set agc.reset.interval <seconds>` | | `0` | | `CommonCLI.cpp` r.503, r.779 |
| `get multi.acks` / `set multi.acks <0\|1>` | `effect: repeater, room server` | `0` | | `CommonCLI.cpp` r.507, r.781 |
| `get flood.advert.interval` / `set flood.advert.interval <hours>` | | R/RS `47` · S `0` | | `CommonCLI.cpp` r.515, r.785 |
| `get advert.interval` / `set advert.interval <minutes>` | | `2`, `0` after the first saved change ¹ | | `CommonCLI.cpp` r.525, r.787 |
| `get flood.max` / `set flood.max <0-64>` | | `64` | | `CommonCLI.cpp` r.633, r.821 |
| `get flood.max.unscoped` / `set flood.max.unscoped <0-64>` | `effect: repeater, room server` | R/RS `64` · S `0` ¹ | | `CommonCLI.cpp` r.615, r.819 |
| `get flood.max.advert` / `set flood.max.advert <0-64>` | `effect: repeater, room server` | R/RS `8` · S `0` ¹ | | `CommonCLI.cpp` r.624, r.817 |

## Commands

### repeat

Whether the node forwards packets. Only the value `off` switches it off; any
other value switches it on. Room server and sensor are off by default
(`simple_room_server/MyMesh.cpp` r.646, `SensorMesh.cpp` r.726). The official
documentation states `on` for all roles.

**Example:**

```text
set repeat off
  -> OK - repeat is now OFF
get repeat
  -> > off
```

**Netherlands:** `on` on a repeater. Switching it off means no relaying.

### path.hash.mode

The size of the hash the node uses for itself in the path of its own adverts: 0
= 1 byte, 1 = 2 bytes, 2 = 3 bytes. Other values give
`Error, must be 0,1, or 2`.

**Example:**

```text
set path.hash.mode 1
  -> OK
get path.hash.mode
  -> > 1
```

### loop.detect

Drops flood packets in which the node's own hash already appears too often in
the path. Only the repeater uses it (`MyMesh.cpp` r.440–444); room server and
sensor store the value but do nothing with it. Another value gives
`Error, must be: off, minimal, moderate, or strict`.

**Example:**

```text
set loop.detect minimal
  -> OK
get loop.detect
  -> > minimal
```

**Netherlands:** `set loop.detect minimal`.

### txdelay

Factor for the random wait window before a flood packet is forwarded. Outside
0–2: `Error, must be 0-2`.

**Example:**

```text
get txdelay
  -> > 0.5
```

**Netherlands:** leave at the default.

### direct.txdelay

The same for direct traffic. The repeater is at 0.3 (`MyMesh.cpp` r.880); the
official documentation states 0.2. Because of the float formatting, `get` shows
`0.1999999` on room server and sensor.

**Example** *(room server)*:

```text
get direct.txdelay
  -> > 0.1999999
```

**Netherlands:** leave at the default.

### rxdelay

Base for a delay when processing weakly received flood packets; 0 switches it
off. Outside 0–20: `Error, must be 0-20`.

**Example:**

```text
get rxdelay
  -> > 0.0
```

### dutycycle

Maximum share of airtime. The firmware converts it to the airtime factor:
`af = 100 / dutycycle − 1`. Outside 1–100: `ERROR: dutycycle must be 1-100`.

**Example:**

```text
get dutycycle
  -> > 50.0%
set dutycycle 10
  -> OK - 10.0%
```

**Netherlands:** `set dutycycle 10`.

### af

The airtime factor itself, deprecated since v1.15.0. `set af` checks no limits;
at the next start the firmware constrains the value to 0–9 (`CommonCLI.cpp`
r.100). The duty cycle is roughly `100 / (af + 1)` percent.

**Example:**

```text
set af 9
  -> OK
get af
  -> > 9.0
```

**Netherlands:** `set af 9` on firmware older than v1.15.0.

### int.thresh

Threshold for local interference; 0 disables the check. The command does not
check the value.

**Example:**

```text
get int.thresh
  -> > 0
```

### agc.reset.interval

Interval in seconds at which the receiver's AGC is reset; 0 switches it off. The
value is rounded down to a multiple of 4.

**Example:**

```text
set agc.reset.interval 17
  -> OK - interval rounded to 16
```

### multi.acks

Multiple ACKs per message. `set` does not check the value; at the next start the
firmware constrains it to 0–1 (`CommonCLI.cpp` r.106). The sensor does not use
the setting.

**Example:**

```text
set multi.acks 1
  -> OK
```

### flood.advert.interval

How often the node sends a flood advert, in hours: 3–168, or 0 for off.
Otherwise `Error: interval range is 3-168 hours`. The official documentation
states 12 as the repeater default; the firmware sets 47 (`MyMesh.cpp` r.891).

**Example:**

```text
set flood.advert.interval 49
  -> OK
```

**Netherlands:** `set flood.advert.interval 49`.

### advert.interval

How often the node sends a zero-hop advert, in minutes: 60–240, or 0 for off.
Otherwise `Error: interval range is 60-240 minutes`. The value is stored halved,
so odd values are rounded down.

**Example:**

```text
set advert.interval 240
  -> OK
get advert.interval
  -> > 240
```

¹ A new installation sends every 2 minutes. At the first change that is saved,
the firmware sets this to 0, because it is below 60 minutes (`CommonCLI.cpp`
r.196–198). The official documentation states 0.

**Netherlands:** `set advert.interval 240`.

### flood.max

Maximum number of hops for any flood packet. Above 64: `Error, max 64`.

**Example:**

```text
get flood.max
  -> > 64
```

### flood.max.unscoped

The same for flood packets without a scope (`MyMesh.cpp` r.433). The official
documentation describes a value `0xFF` that follows `flood.max`; that logic is
not in this commit. See
[Regions and Scopes](../technical/regions-and-scopes.md).

**Example:**

```text
set flood.max.unscoped 3
  -> OK
```

¹ The sensor neither sets nor uses this value; `get` shows `0` there.

**Netherlands:** for example `set flood.max.unscoped 3`, see
[Getting Started](../usage/getting-started.md).

### flood.max.advert

The same for adverts (`MyMesh.cpp` r.434).

**Example:**

```text
get flood.max.advert
  -> > 8
```

¹ See `flood.max.unscoped`.

**Netherlands:** `8`, the default.

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.h)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
