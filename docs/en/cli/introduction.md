# CLI reference

*COMMAND LINE · ROLES · DEFAULTS · DISCREPANCIES*

Repeaters, room servers and sensors have a command line, on the serial console
or remotely from an app. This section describes every command the firmware
knows, by category: which role it works for, the default value, an example and,
where one is agreed, the Dutch setting. The companion has no such command line,
only an emergency console.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `src/helpers/CommonCLI.h`, `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_repeater/main.cpp`, `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, `examples/simple_sensor/main.cpp`,
> `platformio.ini`, and the official `docs/cli_commands.md`. Line numbers refer
> to this commit and can be reproduced with
> [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

## Where the commands come from

Repeater, room server and sensor use the same command handling:
`src/helpers/CommonCLI.cpp`. Before that, each role handles a few commands in
its own `handleCommand()`: `setperm` and `get acl` in all three,
`discover.neighbors` in the repeater, and `io` and `magic` in the sensor.
`CommonCLI` never looks at the role. Differences between roles arise in two
other places: callbacks that each role fills in differently, and settings that
only some roles read.

The companion does not use `CommonCLI`. Its settings go through the companion
protocol, see [The companion interface](../companion/introduction.md). There is
an emergency console: [Companion: CLI Rescue](companion-rescue.md).

## How to give a command

On the serial console you type the command and press Enter. The repeater puts
`  -> ` in front of each reply (`simple_repeater/main.cpp` r.127); a reply is at
most 159 characters (r.124). When a reply spans several lines, only the first
line gets that prefix.

Remotely, an admin sends the same command from an app, see
[Remote Control](../technical/remote-control.md) and
[Requests and CLI](../technical/roomserver/requests-and-cli.md). The sender time
is then not `0`, and so the commands in the **Serial only** column do not work.
A command may start with a three-character prefix such as `01|`; the node puts
it back in front of the reply (repeater r.1211, room server r.897, sensor
r.382).

## Markers

Each category page starts with an overview table. The **Role** column is empty
when the command works the same on repeater, room server and sensor. Otherwise
it holds one of these markers:

| Marker | Meaning |
|---|---|
| `<role> only` | Only that role carries out the command; the other roles do not know it or reply `not supported` |
| `not <role>` | That role accepts the command, but it does not work there |
| `effect: <role>` | Every role accepts and stores the setting, but only the named role uses it |
| `build flag` | The command exists only in a build with a specific option; the page names which |

Whether a role uses a setting was established by searching where the role reads
the setting outside its constructor. In the **Default** column R stands for
repeater, RS for room server and S for sensor. The **Serial only** column is
filled when the firmware checks that the command comes from the serial console.

## The categories

- [Operational](operational.md) — restart, clock, adverts, OTA, erase
- [Neighbors](neighbors.md) — the repeater's neighbour list
- [Statistics](statistics.md) — counters and measurements
- [Logging](logging.md) — the receive log
- [Info](info.md) — firmware version and board
- [Radio](radio.md) — frequency, SF, transmit power
- [System](system.md) — name, location, keys, passwords
- [Routing](routing.md) — forwarding, duty cycle, adverts, hop limits
- [ACL](acl.md) — client permissions
- [Regions](regions.md) — region tree and scope
- [GPS](gps.md) — GPS receiver
- [Sensors](sensors.md) — sensor settings, GPIO
- [Bridge](bridge.md) — RS232 and ESP-NOW bridge
- [Power management (nRF52)](power-management.md) — nRF52 power and bootloader
- [Companion: CLI Rescue](companion-rescue.md) — the companion's emergency console
- [After the pinned commit](after-pinned-commit.md) — commands that exist only on `main`

## Defaults per role

The firmware sets these values in each role's constructor
(`simple_repeater/MyMesh.cpp` r.876–925, `simple_room_server/MyMesh.cpp`
r.632–669, `simple_sensor/SensorMesh.cpp` r.710–736). They apply to a freshly
flashed node; if the node already has a settings file, `loadPrefs()` overrides
them (`CommonCLI.cpp` r.40–130). A ⚠ means the official documentation states
something else.

| Setting | Repeater | Room server | Sensor |
|---|---|---|---|
| `radio` ⚠ | `869.618,62.5,8,5` | same | same |
| `tx` | per board, fallback `20` | per board, fallback `20` | per board, fallback `20` |
| `radio.rxgain` ⚠ | `on` (SX1262/SX1268) | `off` | `off` |
| `name` | `repeater` | `Test BBS` | `sensor` |
| `lat` / `lon` | `0.0` | `0.0` | `0.0` |
| `password` | `password` | `password` | `password` |
| `guest.password` ⚠ | empty | `ROOM_PASSWORD` or empty | empty |
| `owner.info` | empty | empty | empty |
| `adc.multiplier` | `0.0` | `0.0` | `0.0` |
| `powersaving` | `off` | `off` | `off` |
| `repeat` ⚠ | `on` | `off` | `off` |
| `path.hash.mode` | `0` | `0` | `0` |
| `loop.detect` | `off` | `off` | `off` |
| `txdelay` | `0.5` | `0.5` | `0.5` |
| `direct.txdelay` ⚠ | `0.3` | `0.2` | `0.2` |
| `rxdelay` | `0.0` | `0.0` | `0.0` |
| `dutycycle` / `af` | `50` / `1.0` | `50` / `1.0` | `50` / `1.0` |
| `int.thresh` | `0` | `0` | `0` |
| `agc.reset.interval` | `0` | `0` | `0` |
| `multi.acks` | `0` | `0` | `0` |
| `flood.advert.interval` ⚠ | `47` | `47` | `0` |
| `advert.interval` ⚠ | `2` → `0` | `2` → `0` | `2` → `0` |
| `flood.max` | `64` | `64` | `64` |
| `flood.max.unscoped` ⚠ | `64` | `64` | `0` |
| `flood.max.advert` | `8` | `8` | `0` |
| `allow.read.only` | `off` | `off` | `off` |
| `gps` / `gps advert` | `off` / `prefs` | `off` / `prefs` | `off` / `prefs` |
| `bridge.enabled` ⚠ | `on` | — | — |
| `bridge.delay` / `bridge.source` | `500` / `logTx` | — | — |
| `bridge.baud` / `bridge.channel` | `115200` / `1` | — | — |
| `bridge.secret` ⚠ | `LVSITANOS` | — | — |

`advert.interval` is 2 minutes until the first saved change and 0 after that;
see [Routing](routing.md). The name is the fallback value of `ADVERT_NAME`; most
builds set a name of their own.

## Discrepancies with the official documentation

This reference follows the firmware. Where `docs/cli_commands.md` at the same
commit says something else, this is noted at the command. The overview:

| Topic | Official documentation | Firmware at `03b6ef4` | Page |
|---|---|---|---|
| default `radio` | `869.525,250,11,5` | `869.618,62.5,8,5` | [Radio](radio.md) |
| default `radio.rxgain` | `on` | `on` only on the repeater in SX1262/SX1268 builds | [Radio](radio.md) |
| limits `tempradio` | 300–2500 MHz, 7.8–500 kHz | 150–2500 MHz, 7–500 kHz | [Radio](radio.md) |
| `neighbors`, second field | timestamp | seconds ago | [Neighbors](neighbors.md) |
| `set prv.key` | 64 hex characters | 128 hex characters | [System](system.md) |
| default `guest.password` | empty | `ROOM_PASSWORD` on the room server, if that flag is set | [System](system.md) |
| default `repeat` | `on` | `off` on room server and sensor | [Routing](routing.md) |
| default `direct.txdelay` | `0.2` | `0.3` on the repeater | [Routing](routing.md) |
| default `flood.advert.interval` | `12` (repeater) | `47` | [Routing](routing.md) |
| default `advert.interval` | `0` | `2`, `0` after the first saved change | [Routing](routing.md) |
| `flood.max.unscoped` | `0xFF` follows `flood.max` | no `0xFF` logic | [Routing](routing.md) |
| `setperm` without permissions | removes the client | `Err - bad params`; removal uses `0` | [ACL](acl.md) |
| `region list` | serial only | also remote | [Regions](regions.md) |
| `region load <name> [flag]` | arguments | arguments are ignored | [Regions](regions.md) |
| default `bridge.enabled` | `off` | `on` | [Bridge](bridge.md) |
| values `bridge.source` | `logRx`, `logTx` | only a value starting with `rx` sets `logRx` | [Bridge](bridge.md) |
| default `bridge.secret` | per board | `LVSITANOS` | [Bridge](bridge.md) |
| `bootloader.ver`, `pwrmgt.*` | under *Bridge* | nRF52 platform | [Power management](power-management.md) |
| `io`, `magic` | missing | sensor commands | [Sensors](sensors.md) |

## Dutch settings at a glance

The agreements come from [Regulations & Duty Cycle](../usage/regulations.md) and
[Getting Started](../usage/getting-started.md). Each command's category page
repeats the setting.

| Command | Dutch setting | Page |
|---|---|---|
| `set radio` | `869.618,62.5,7,5` | [Radio](radio.md) |
| `set dutycycle` | `10` | [Routing](routing.md) |
| `set af` | `9` (firmware older than v1.15.0) | [Routing](routing.md) |
| `set loop.detect` | `minimal` | [Routing](routing.md) |
| `set flood.advert.interval` | `49` | [Routing](routing.md) |
| `set advert.interval` | `240` | [Routing](routing.md) |
| `set flood.max.advert` | `8` | [Routing](routing.md) |
| `set flood.max.unscoped` | for example `3` | [Routing](routing.md) |
| `set txdelay` / `set direct.txdelay` | default | [Routing](routing.md) |
| `set repeat` | `on` on a repeater | [Routing](routing.md) |
| `region put` / `region default` | `eu` → `nl` → province | [Regions](regions.md) |

## Newer firmware

Commands added after `03b6ef4` are listed separately, marked as not verified
against the pin: [After the pinned commit](after-pinned-commit.md).

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/CommonCLI.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.h)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_repeater/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/main.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/main.cpp)
- [MeshCore firmware — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
