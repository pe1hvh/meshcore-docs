# Companion: CLI Rescue

*EMERGENCY CONSOLE · BLE PIN · FILE SYSTEM*

The companion firmware does not use `CommonCLI`; its settings go through the
companion protocol, see [The companion interface](../companion/introduction.md).
It does have an emergency console on the serial port, with seven commands to set
the BLE PIN, inspect or erase the file system, and restart.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `examples/companion_radio/MyMesh.cpp`,
> `examples/companion_radio/ui-tiny/UITask.cpp`,
> `examples/companion_radio/ui-new/UITask.cpp`,
> `examples/companion_radio/ui-orig/UITask.cpp`, and the official
> `docs/cli_commands.md`. Line numbers refer to this commit and can be
> reproduced with [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Starting

Press the button long within 8 seconds after start-up (`ui-tiny/UITask.cpp`
r.766–767, `ui-new/UITask.cpp` r.866–867, `ui-orig/UITask.cpp` r.451–452). This
is therefore only possible on a board with a button and a UI. The console
reports `========= CLI Rescue =========` (`examples/companion_radio/MyMesh.cpp`
r.2006) and echoes every character typed. There is no `  -> ` in front of a
reply; replies usually start with two spaces. An unknown command gives
`  Error: unknown command`.

## Overview

| Command | Function | Source |
|---|---|---|
| `set pin <nnnnnn>` | Fix the BLE PIN | r.2028 |
| `rebuild` | Erase the file system and write identity, settings, contacts and channels back | r.2035 |
| `erase` | Erase the file system | r.2046 |
| `ls [path]` | List files | r.2053 |
| `cat <path>` | Show a file, in hex | r.2101 |
| `rm <path>` | Delete a file | r.2138 |
| `reboot` | Restart | r.2171 |

## Commands

### set pin

Sets a fixed six-digit BLE PIN. With `0` the firmware chooses: on a board with a
display and the default code 123456 a random code per session, otherwise
`BLE_PIN_CODE` (r.939–950). A setting other than `pin` gives
`  Error: unknown config: <name>`.

**Example:**

```text
set pin 123456
  > pin is now 123456
```

**Netherlands:** no agreed setting.

### rebuild

Formats the file system and then writes the identity, settings, contacts and
channels back from memory. If formatting fails: `  Error: erase failed`.

**Example:**

```text
rebuild
  > erase and rebuild done
```

**Netherlands:** no agreed setting.

### erase

Formats the file system without writing anything back.

**Example:**

```text
erase
  > erase done
```

> [!WARNING]
> After `erase` the companion's identity is gone. Use `rebuild` if you want to
> keep it.

**Netherlands:** no agreed setting.

### ls

Lists directories and files. A path starting with `UserData/` refers to the
normal file system, `ExtraFS/` to the second one. Each line starts with `[dir]`
or `[file]`; a file has its size after it.

**Example:**

```text
ls UserData/
Listing files in /
[dir]  UserData//<directory>
[file] UserData//<file> (<n> bytes)
```

**Netherlands:** no agreed setting.

### cat

Shows the contents of a file as hex. The path must start with `UserData/` or
`ExtraFS/`, otherwise
`Invalid path provided, must start with UserData/ or ExtraFS/`.

**Example:**

```text
cat notes.txt
Invalid path provided, must start with UserData/ or ExtraFS/
```

**Netherlands:** no agreed setting.

### rm

Deletes a file. An empty path or `/` gives `Invalid path provided`; a file that
cannot be removed gives `Failed to remove file`. The example uses the file from
the comment in the source code (r.2139).

**Example:**

```text
rm UserData/adv_blobs
File removed
```

**Netherlands:** no agreed setting.

### reboot

Restarts the companion. No reply.

**Example:**

```text
reboot
```

**Netherlands:** no agreed setting.

If you send a command from the companion app to a repeater, the repeater carries
it out. The other pages of this section apply to that.

## Sources

- [MeshCore firmware — `examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/MyMesh.cpp)
- [MeshCore firmware — `examples/companion_radio/ui-tiny/UITask.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/ui-tiny/UITask.cpp)
- [MeshCore firmware — `examples/companion_radio/ui-new/UITask.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/ui-new/UITask.cpp)
- [MeshCore firmware — `examples/companion_radio/ui-orig/UITask.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/ui-orig/UITask.cpp)

Translated from Dutch by Anthropic Claude
