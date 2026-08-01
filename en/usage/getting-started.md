# Getting Started

*FIRST INSTALLATION · ONLINE IN 3 STEPS*

## Requirements

- MeshCore-compatible hardware (e.g. Heltec V3, T-Deck Plus, T1000-E)
- Antenna for **868 MHz** (EU frequency)
- Android or iOS phone with the MeshCore Companion App
- USB cable for initial configuration

## Step 1 — Flash firmware

Go to [flasher.meshcore.co.uk](https://flasher.meshcore.co.uk) in Chrome or Edge. Select your device, choose **'Companion Radio BLE'** firmware, and click Flash.

> [!WARNING]
> **Note:** The Web Flasher only works in Chromium-based browsers (Chrome, Edge). Firefox and Safari are not supported due to Web Serial API limitations.

## Step 2 — Connect to the app

Launch the **MeshCore Companion App**, choose Scan, select your node, and tap Connect. The app is available for both Android and iOS via the official app stores.

## Step 3 — Configure

In the app, select the **Netherlands** preset. This automatically sets the following parameters:

| Parameter | Value | Notes |
|---|---|---|
| Preset | Netherlands | Dutch network setting |
| Frequency | 869.618 MHz | EU ISM band (H4/H5, see *Regulations*) |
| Bandwidth | 62.5 kHz | Narrow — lower noise floor, better SNR |
| Spreading Factor | SF7 | Short time-on-air, fewer collisions |
| Coding Rate | 4/5 (CR5) | Default error correction |
| Power | 14 dBm | EU limit (25 mW ERP) |
| Encryption | On (default) | AES-128 |

> [!NOTE]
> **No Netherlands preset in your app?** Choose **Custom** and set the four
> values by hand: 869.618 MHz, BW 62.5 kHz, SF7, CR5.
>
> Older guides still mention **EU/UK (Narrow)** with **SF8 / CR8**. The Dutch
> network moved to SF7 / CR5 in May 2026 to shorten time-on-air and reduce
> collisions; frequency and bandwidth stayed the same. A node left on SF8 no
> longer hears the rest of the mesh.


## Step 4 - Region settings


Since firmware 1.10, MeshCore has regions and scopes to avoid unnecessary airtime: a message meant for your own neighborhood does not need to be forwarded across the whole of the Netherlands. Repeaters are assigned one or more regions (“which stamps do I let through”), and every message gets a scope (“which stamp do I put on it”). A repeater only forwards a message if the scope matches one of its configured regions.

The layout follows the ISO 3166-2:NL province codes, with a national layer on top:

| Level | Example | Significance |
|-----------|--------------------------|---------------------------------------|
| Country   | nl                       | Whole of the Netherlands              |
| Province  | nl-ov, nl-ge, nl-ut, ... | Own province (12x)                    |
| Local     | nl-ov-zwolle             | Community agreement, not standardized |

**Basic configuration on a repeater:**

```text
region put eu
region put nl eu
region put <your-province> nl
region default <your-province>
region save
```

The second argument to `region put` is the parent. Leave it out and the region
hangs under the wildcard `*`, giving you a flat list rather than a tree.

> [!WARNING]
> **Regions do not inherit.** A repeater compares a packet's scope against every
> region it knows itself, regardless of the hierarchy. So a repeater that knows
> only `nl` will **not** forward a message scoped to `nl-ov`. If you want to
> carry both national and provincial traffic, configure both regions on the
> repeater. The tree structure exists for readability and for `region remove`,
> not for forwarding.

*Note: the command “region denyf \*” (strict region filtering, rejecting everything outside your regions) was scheduled for phase 8 of the national rollout on 18 July 2026. Using it prematurely will cause your repeater to drop messages from nodes that have not yet configured their region; check the current state of the rollout before enabling it.*

A gentler intermediate step is `set flood.max.unscoped 3`. Unscoped traffic keeps
working locally but no longer travels across the whole country — without cutting
off nodes that have no region configured at all.

In the Companion App you set a scope per channel (for example national, provincial or local); the community agrees on local codes among themselves. The app sends the 16-byte key to the node rather than the name, and sets it per transmission. What goes over the air is a 16-bit code computed from that key and the message content — see [MeshCore Packet Structure](../technical/packet-structure.md). For the current configuration and tools:

- Setting region codes (step-by-step configurator): mesh-up.nl/tools/regiocodes-instellen
- Dashboard configurator: dashboard-elburg.f3dp.nl (tab “region-configurator”)
- Full list of region codes: meshwiki.nl/wiki/Lijst_van_regio%27s


## What's next?

After configuration your node is active on the mesh. You can send messages via the **#public** channel, discover other nodes via the map, and send Direct Messages to nodes you have seen. Read more about communication in the *Communication* section.

Translated from Dutch by Anthropic Claude
