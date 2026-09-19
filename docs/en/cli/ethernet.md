# Ethernet

*ETH.STATUS · RAK13800 · CH390 · TCP PORT*

Some boards can be attached to a wired network alongside LoRa. On those builds
there is one extra command, `eth.status`, and the node listens on a TCP port.
This page describes what the firmware does there and which builds are involved.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.17.1, commit `d929643`, 14 August 2026 — files
> `src/helpers/nrf52/EthernetCLI.h`, `src/helpers/ethernet/EthernetInterface.h`,
> `src/helpers/ethernet/SerialEthernetInterface.h`,
> `src/helpers/ethernet/ch390/CH390EthernetInterface.h`,
> `variants/rak4631/platformio.ini`, `variants/thinknode_m7/platformio.ini`, and
> the official `docs/cli_commands.md`. Line numbers refer to this commit.

## Overview

The markers in the **Role** column are explained in the
[CLI reference](introduction.md).

| Command | Role | Default | Serial only | Source |
|---|---|---|---|---|
| `eth.status` | `build flag` `ETHERNET_ENABLED` · not companion | — | | `nrf52/EthernetCLI.h` r.89 |

`eth.status` is not in `CommonCLI.cpp` but in `nrf52/EthernetCLI.h`. The script
[`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py)
therefore counts `eth.status` as a command that is in the official
documentation and not in the files the script scans.

## Commands

### eth.status

Status of the Ethernet connection. If the interface is not active the reply is
`ETH: not connected`; otherwise the IP address obtained over DHCP with the TCP
port of the CLI (`nrf52/EthernetCLI.h` r.89–100). The port defaults to 23 and
can be changed with the build option `ETHERNET_TCP_PORT` (r.20–22). After a
failed start the firmware retries every 30 seconds
(`ETHERNET_RETRY_INTERVAL_MS`, r.28).

**Example:**

```text
eth.status
  -> ETH: not connected
```

With a connection the reply looks like this:

```text
eth.status
  -> ETH: 192.168.2.234:23
```

## Which builds

The Ethernet code is only compiled in with the build option
`ETHERNET_ENABLED`. It did not exist in `03b6ef4`; it was added in v1.17.0.

| Build | Hardware | What listens |
|---|---|---|
| `RAK_4631_repeater_ethernet` | RAK4631 with RAK13800 (W5100S) | CLI on TCP 23 |
| `RAK_4631_room_server_ethernet` | RAK4631 with RAK13800 (W5100S) | CLI on TCP 23 |
| `RAK_4631_companion_radio_ethernet` | RAK4631 with RAK13800 (W5100S) | companion protocol on TCP 5000 |
| `ThinkNode_M7_companion_radio_ethernet` | ThinkNode M7 with CH390 | companion protocol on TCP 5000 |

The companion has no command line; over Ethernet it speaks the same binary
protocol as over BLE and USB, on port 5000
(`ethernet/SerialEthernetInterface.h` r.5–6). See
[The companion interface](../companion/introduction.md) and
[Transport layers](../companion/technical/transports.md). For emergencies there
is [Companion: CLI Rescue](companion-rescue.md).

> [!WARNING]
> The CLI on TCP 23 has no encryption and no separate access control: anyone
> who can reach the IP address gets the same command line as over the serial
> console. Do not put such a node on a network that reaches beyond your own LAN
> without shielding it, and in any case change the default password, see
> [System](system.md).

## Sources

- [MeshCore firmware — `src/helpers/nrf52/EthernetCLI.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/nrf52/EthernetCLI.h)
- [MeshCore firmware — `src/helpers/ethernet/EthernetInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ethernet/EthernetInterface.h)
- [MeshCore firmware — `src/helpers/ethernet/SerialEthernetInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ethernet/SerialEthernetInterface.h)
- [MeshCore firmware — `src/helpers/ethernet/ch390/CH390EthernetInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ethernet/ch390/CH390EthernetInterface.h)
- [MeshCore firmware — `variants/rak4631/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/d929643/variants/rak4631/platformio.ini)
- [MeshCore firmware — `variants/thinknode_m7/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/d929643/variants/thinknode_m7/platformio.ini)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/d929643/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
