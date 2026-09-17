# ACL

*PERMISSIONS · TABLE · READ-ONLY ACCESS*

The ACL is the table of known clients and their permissions. Two commands are
not in `CommonCLI` but in each role separately, with the same code. Logging in
itself is covered in
[Logging In and the ACL](../technical/roomserver/login-and-acl.md).

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, `src/helpers/ClientACL.cpp`,
> `src/helpers/ClientACL.h`, `src/helpers/CommonCLI.cpp`, and the official
> `docs/cli_commands.md`. Line numbers refer to this commit and can be
> reproduced with [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md). An empty cell means: works on repeater, room
server and sensor.

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `setperm <pubkey> <permissions>` | | — | | R r.1218 · RS r.904 · S r.394 |
| `get acl` | | — | yes | R r.1240 · RS r.926 · S r.416 |
| `get allow.read.only` / `set allow.read.only <on\|off>` | `effect: room server` | `off` | | `CommonCLI.cpp` r.511, r.783 |

## Commands

### setperm

Sets a client's permissions: 0 guest, 1 read-only, 2 read-write, 3 admin
(`ClientACL.h` r.7–11). Permission 0 removes the client; a key prefix is enough
for that. For 1–3 the full key of 64 hex characters is required (`ClientACL.cpp`
r.121–143). Without a permission value the reply is `Err - bad params`; the
official documentation says that omitting it removes the client.

**Example** *(example key from `tools/dm-example.py`)*:

```text
setperm E3A0313ACE439E364C44894F5151D53A35E7D70523B45A69794CCD30E484FCE7 3
  -> OK
setperm E3A0313A 0
  -> OK
```

Other replies: `Err - bad pubkey` for invalid hex and `Err - invalid params` if
the key is too short or unknown.

### get acl

Writes the table to the serial console: per client the permissions in hex and
the full public key. Guests are not listed. The command itself gives no reply,
so there is no `  -> `. It does not exist over the radio; see
[Requests and CLI](../technical/roomserver/requests-and-cli.md).

**Example:**

```text
get acl
ACL:
03 E3A0313ACE439E364C44894F5151D53A35E7D70523B45A69794CCD30E484FCE7
```

### allow.read.only

Only the room server uses this flag: with a wrong password the client still gets
guest rights (`simple_room_server/MyMesh.cpp` r.336).

**Example:**

```text
set allow.read.only on
  -> OK
get allow.read.only
  -> > on
```

## Sources

- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
