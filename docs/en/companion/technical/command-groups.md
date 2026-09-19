# The command groups

*58 COMMANDS · NINE GROUPS · RESERVED NUMBERS · WHAT THE SPEC MISSES*

The firmware knows fifty-eight commands, spread over a number range from 1
to 65 with seven gaps in it. They live in a single `#define` block and are
handled by a single else-if chain. This chapter orders them by subject, so
you can see which ones a client needs and which are incidental.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — file
> `examples/companion_radio/MyMesh.cpp` r.6-64 for the numbers and the
> else-if chain below it for the handling. The grouping is this
> documentation's own and does not appear that way in the firmware;
> `tools/companion-opcodes.py` checks that every number falls into exactly
> one group.

## All 58 commands are handled by the firmware

Every `#define CMD_…` has a matching `cmd_frame[0] == …` in the handling: 58
out of 58. So there are no commands that have a number but do nothing. What
does exist is reserved numbers without a name:

| Unused | What the firmware says about it |
|---|---|
| 44 – 49 | `// NOTE: CMD range 44..49 parked, potentially for WiFi operations` |
| 53 | no comment |

A client must not use those numbers and should count on them acquiring
meaning in a later version.

## Session and device — 12 commands

Everything concerning the connection itself and the device.

| No | Command | Purpose |
|---|---|---|
| 1 | `CMD_APP_START` | the app announces itself with a name; the answer is `RESP_CODE_SELF_INFO` |
| 22 | `CMD_DEVICE_QUERY` | version negotiation and the limits of this device |
| 5 | `CMD_GET_DEVICE_TIME` | read the node's clock |
| 6 | `CMD_SET_DEVICE_TIME` | set the clock; required before anything with a timestamp |
| 19 | `CMD_REBOOT` | restart |
| 51 | `CMD_FACTORY_RESET` | wipe; literally demands the text `reset` as an argument |
| 37 | `CMD_SET_DEVICE_PIN` | change the BLE PIN code |
| 20 | `CMD_GET_BATT_AND_STORAGE` | battery voltage and storage usage |
| 56 | `CMD_GET_STATS` | counters; the second byte selects core, radio or packets |
| 43 | `CMD_GET_TUNING_PARAMS` | read the fine-tuning |
| 21 | `CMD_SET_TUNING_PARAMS` | set the fine-tuning (receive delay, AGC) |
| 38 | `CMD_SET_OTHER_PARAMS` | manual contact adding and the three telemetry modes |

## Identity and advert — 9 commands

| No | Command | Purpose |
|---|---|---|
| 7 | `CMD_SEND_SELF_ADVERT` | announce itself; the argument decides zero-hop or flood |
| 8 | `CMD_SET_ADVERT_NAME` | the name the node announces itself under |
| 14 | `CMD_SET_ADVERT_LATLON` | the position in the advert |
| 23 | `CMD_EXPORT_PRIVATE_KEY` | take the private key out |
| 24 | `CMD_IMPORT_PRIVATE_KEY` | put a private key back |
| 42 | `CMD_GET_ADVERT_PATH` | request the stored path to a node |
| 33 | `CMD_SIGN_START` | begin signing; the answer reports the maximum length |
| 34 | `CMD_SIGN_DATA` | supply a chunk of data |
| 35 | `CMD_SIGN_FINISH` | finish; the answer is the signature |

Two terms from the first row: **zero-hop** means directly, without other
nodes forwarding the message. **Flood** means every node suited to it
forwards the message, so that it spreads across the whole reachable network.

> [!WARNING]
> `CMD_EXPORT_PRIVATE_KEY` (23) gives away the node's identity. Whoever has
> the key *is* the node — signing messages, decrypting direct messages, all
> of it. A client offering this command should put it behind an explicit
> confirmation and never log the result.

## Contacts — 9 commands

| No | Command | Purpose |
|---|---|---|
| 4 | `CMD_GET_CONTACTS` | all contacts, optionally only those after a timestamp |
| 9 | `CMD_ADD_UPDATE_CONTACT` | add or change |
| 15 | `CMD_REMOVE_CONTACT` | remove |
| 16 | `CMD_SHARE_CONTACT` | share a contact over the mesh |
| 17 | `CMD_EXPORT_CONTACT` | request a contact as shareable text |
| 18 | `CMD_IMPORT_CONTACT` | read such text back in |
| 30 | `CMD_GET_CONTACT_BY_KEY` | look up one contact by key prefix |
| 58 | `CMD_SET_AUTOADD_CONFIG` | the bitmask for automatic adding |
| 59 | `CMD_GET_AUTOADD_CONFIG` | read that same mask |

## Channels — 2 commands

| No | Command | Purpose |
|---|---|---|
| 31 | `CMD_GET_CHANNEL` | read one slot, by index |
| 32 | `CMD_SET_CHANNEL` | write one slot: index, name, key |

There is no command to delete a channel. You empty a slot by overwriting it.

## Messages — 6 commands

| No | Command | Purpose |
|---|---|---|
| 2 | `CMD_SEND_TXT_MSG` | direct message to a contact |
| 3 | `CMD_SEND_CHANNEL_TXT_MSG` | message on a channel |
| 10 | `CMD_SYNC_NEXT_MESSAGE` | take the next message out of the queue |
| 62 | `CMD_SEND_CHANNEL_DATA` | datagram on a channel, at most 167 bytes |
| 25 | `CMD_SEND_RAW_DATA` | raw data to a contact |
| 65 | `CMD_SEND_RAW_PACKET` | inject a fully assembled packet |

That last command is the back door for tooling: the app builds the packet
itself and the node transmits it without adding anything.

## Connecting to other nodes — 8 commands

For repeaters, room servers and sensors that require a session.

| No | Command | Purpose |
|---|---|---|
| 26 | `CMD_SEND_LOGIN` | log in to a remote node |
| 29 | `CMD_LOGOUT` | end that session |
| 28 | `CMD_HAS_CONNECTION` | is there still a session with this key |
| 27 | `CMD_SEND_STATUS_REQ` | status request |
| 39 | `CMD_SEND_TELEMETRY_REQ` | request telemetry; the firmware itself calls this replaceable |
| 50 | `CMD_SEND_BINARY_REQ` | the successor, typed request |
| 55 | `CMD_SEND_CONTROL_DATA` | control data, zero-hop |
| 57 | `CMD_SEND_ANON_REQ` | request to a node that is not a contact |

Number 57 only works from `FIRMWARE_VER_CODE` 13 onwards; on older firmware
the node requires the recipient to be a known contact.

## Radio and path — 7 commands

| No | Command | Purpose |
|---|---|---|
| 11 | `CMD_SET_RADIO_PARAMS` | frequency, bandwidth, spreading, coding |
| 12 | `CMD_SET_RADIO_TX_POWER` | transmit power, capped at `MAX_LORA_TX_POWER` |
| 13 | `CMD_RESET_PATH` | clear the stored path to a contact |
| 36 | `CMD_SEND_TRACE_PATH` | trace a route |
| 52 | `CMD_SEND_PATH_DISCOVERY_REQ` | have a path discovered |
| 61 | `CMD_SET_PATH_HASH_MODE` | how the node compares paths: on the full route or on a shortened fingerprint of it (path hash); values 0 to 2 |
| 60 | `CMD_GET_ALLOWED_REPEAT_FREQ` | the frequency ranges in which repeating is allowed |

Number 60 is regulation in code: the node returns the ranges within which
`client repeat` is permitted. See
[Regulations & Duty Cycle](../../usage/regulations.md).

## Region and scope — 3 commands

| No | Command | Purpose |
|---|---|---|
| 54 | `CMD_SET_FLOOD_SCOPE_KEY` | temporary scope key, or force unscoped |
| 63 | `CMD_SET_DEFAULT_FLOOD_SCOPE` | the node's fixed default scope |
| 64 | `CMD_GET_DEFAULT_FLOOD_SCOPE` | read that default |

These three are the reason the app has to track which channel belongs to
which scope: the firmware does not store that mapping. See
[Regions and Scopes](../../technical/regions-and-scopes.md).

## Custom variables — 2 commands

| No | Command | Purpose |
|---|---|---|
| 40 | `CMD_GET_CUSTOM_VARS` | the settable variables as a comma-separated list |
| 41 | `CMD_SET_CUSTOM_VAR` | set one |

Meant for sensor variants that bring their own settings.

## What the official spec describes

Of these fifty-eight, seven appear by name in
`docs/companion_protocol.md`: `CMD_APP_START`, `CMD_DEVICE_QUERY`,
`CMD_GET_CHANNEL`, `CMD_SET_CHANNEL`, `CMD_SEND_CHANNEL_TXT_MSG`,
`CMD_SEND_CHANNEL_DATA` and `CMD_GET_BATT_AND_STORAGE`. Of the 46 response
and push codes, five appear.

That is not a reproach to the spec — it says itself that it is still in
development — but it is why anyone building a client needs the firmware and
cannot get by on the document alone.

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.cpp)
  — the numbers at r.6-64 and the handling below them
- [`docs/companion_protocol.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/docs/companion_protocol.md)
  — the official spec and what it does describe

Reproduction:

- `tools/companion-opcodes.py` — the numbers, the grouping and the coverage
  figures
- `tools/companion-opcodes-snapshot.json` — the result at commit `03b6ef4`

Related chapters:

- [The interaction model](../logical/interaction-model.md) — how a command
  gets its answer
- [The frame](frame-format.md) — what fits into the payload
- [Architecture of a client](client-architecture.md) — how to cast this into
  layers

Translated from Dutch by Anthropic Claude
