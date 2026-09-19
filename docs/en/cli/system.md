# System

*NAME · LOCATION · KEYS · PASSWORDS · ROLE*

Settings that describe the node itself: name, location, owner, key pair and
passwords, plus the battery correction and the repeater's power saving.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files `src/helpers/CommonCLI.cpp`,
> `src/helpers/CommonCLI.h`, `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_repeater/main.cpp`, `examples/simple_repeater/MyMesh.h`,
> `examples/simple_room_server/MyMesh.h`, `examples/simple_sensor/SensorMesh.h`,
> `src/MeshCore.h`, and the official `docs/cli_commands.md`. Line numbers refer
> to this commit and can be reproduced with
> [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `get name` / `set name <name>` | | R `repeater` · RS `Test BBS` · S `sensor` ¹ | | `CommonCLI.cpp` r.552, r.796 |
| `get lat` / `set lat <degrees>` / `get lon` / `set lon <degrees>` | | `0.0` | | `CommonCLI.cpp` r.589, r.593, r.800, r.802 |
| `get prv.key` / `set prv.key <private_key>` | | — | `get` only | `CommonCLI.cpp` r.539, r.791 |
| `password <new_password>` | | `password` | | `CommonCLI.cpp` r.289 |
| `get guest.password` / `set guest.password <password>` | `effect: repeater, room server` | RS `ROOM_PASSWORD` ¹, otherwise empty | | `CommonCLI.cpp` r.535, r.789 |
| `get owner.info` / `set owner.info <text>` | `effect: repeater` | `empty` | | `CommonCLI.cpp` r.651, r.825 |
| `get adc.multiplier` / `set adc.multiplier <value>` | | `0.0` (board value) | | `CommonCLI.cpp` r.749, r.895 |
| `get public.key` | | — | | `CommonCLI.cpp` r.851 |
| `get role` | | — | | `CommonCLI.cpp` r.854 |
| `powersaving` / `powersaving on` / `powersaving off` | `effect: repeater` | `off` | | `CommonCLI.cpp` r.434–458 |

## Commands

### name

The name in the adverts. The field is 32 bytes (`CommonCLI.h` r.24). The
characters `[ ] \ : , ? *` are not allowed; the reply is then
`Error, bad chars`.

**Example:**

```text
set name PE1HVH Repeater
  -> OK
get name
  -> > PE1HVH Repeater
```

¹ Fallback values of `ADVERT_NAME`; most builds set a name of their own.

### lat / lon

Latitude and longitude in decimal degrees, without a range check. `get` uses the
same float formatting as `get radio`. The location is included in adverts,
depending on `gps advert`.

**Example:**

```text
set lat 52.5168
  -> OK
get lat
  -> > 52.5167999
set lon 6.083
  -> OK
get lon
  -> > 6.0830001
```

### prv.key

The node's key pair. `set` expects the private key as 128 hex characters
(`PRV_KEY_SIZE` 64, `MeshCore.h` r.9), validates it and replies with the new
public key; the change takes effect after a restart. `get` works on the serial
console only. The official documentation speaks of 64 hex characters.

**Example:**

```text
set prv.key 00
  -> Error, bad key
```

With a valid key the reply is `OK, reboot to apply! New pubkey: ` followed by 64
hex characters.

### password

The admin password, at most 15 characters (`CommonCLI.h` r.26). The reply
repeats the new password.

**Example:**

```text
password Zwolle2026
  -> password now: Zwolle2026
```

> [!WARNING]
> The default `password` is known to everyone. As long as it is in place, any
> client with that password can manage the node.

### guest.password

The password for ordinary participants, at most 15 characters (`CommonCLI.h`
r.34). Repeater and room server use it at login (`simple_repeater/MyMesh.cpp`
r.104, `simple_room_server/MyMesh.cpp` r.334). See
[Logging In and the ACL](../technical/roomserver/login-and-acl.md).

**Example:**

```text
set guest.password zwolle
  -> OK
get guest.password
  -> > zwolle
```

¹ Only if the build sets `ROOM_PASSWORD` (`simple_room_server/MyMesh.cpp`
r.653–655). The official documentation states empty as the default.

### owner.info

Free text about the owner, at most 119 characters (`CommonCLI.h` r.62). A `|` is
stored as a line break and shown as `|` again by `get`. Only the repeater does
anything with it (`simple_repeater/MyMesh.cpp` r.179, r.376).

**Example:**

```text
set owner.info PE1HVH|Zwolle
  -> OK
get owner.info
  -> > PE1HVH|Zwolle
```

### adc.multiplier

Correction factor for the battery reading. `0` restores the board's own value.
If the board does not support it, the reply is
`Error: unsupported by this board`; `get` gives the same reply when the board
has no factor.

**Example:**

```text
set adc.multiplier 1.05
  -> OK - multiplier set to 1.050
set adc.multiplier 0
  -> OK - using default board multiplier
```

### public.key

The node's public key as 64 hex characters.

**Example** *(example key from `tools/dm-example.py`)*:

```text
get public.key
  -> > EA1F69C38A415ABDD55590ECC796DE3D04FE6D80FAEE006A37021432804CBDCC
```

### role

The role the firmware was built for: `repeater`, `room_server` or `sensor`
(`FIRMWARE_ROLE` in the three role files).

**Example:**

```text
get role
  -> > repeater
```

### powersaving

Lets the repeater sleep when there is nothing to do. Only the repeater's main
loop reads the flag (`simple_repeater/main.cpp` r.155). The reply to
`powersaving on` depends on the platform: on nRF52 `on - Immediate effect`, on
ESP32 `on - After 2 minutes`, in a build with a bridge `Bridge not supported`
and elsewhere `Board not supported`. Without an argument the command shows `on`
or `off`.

**Example** *(nRF52, such as the SenseCap Solar)*:

```text
powersaving on
  -> on - Immediate effect
powersaving
  -> on
```

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/CommonCLI.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.h)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_repeater/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/main.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.h)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.h)
- [MeshCore firmware — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
