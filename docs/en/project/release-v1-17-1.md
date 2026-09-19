# Changes in v1.17.1

*RELEASE · DIFF · PIN · STATE OF THE DOCUMENTATION*

MeshCore v1.17.1 was released on 14 August 2026. This page lists what changes
relative to the commit this documentation was pinned to until now, which
chapters have already been re-verified and which have not. What is stated here
was derived from the source code itself; the official release notes were used as
an index, not as evidence.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.17.1, commit `d929643`, 14 August 2026, compared with the previous pin
> `03b6ef4` of 28 July 2026. The comparison can be reproduced with
> [`tools/diff-impact.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/diff-impact.py)
> and two checkouts. The official announcements are on
> [blog.meshcore.io](https://blog.meshcore.io/2026/08/14/release-1-17-1).

## What is pinned

The tags `companion-v1.17.1`, `repeater-v1.17.1` and `room-server-v1.17.1` all
point to the same commit, `d929643`. In that commit `FIRMWARE_VERSION` is
`v1.17.1`.

The previous pin `03b6ef4` was not a release but a snapshot of `main` from 28
July 2026, in which `FIRMWARE_VERSION` still read `v1.16.0`. The tag
`companion-v1.16.0` points to an older commit, `07a3ca9` of 6 June 2026. What
this documentation called "v1.16.0" until now therefore sat between releases
v1.16.0 and v1.17.0. Part of what the v1.17.0 release notes list was already in
the pinned text as a result.

## What is new

The comparison `03b6ef4` → `d929643` covers 366 files, with 12,026 lines added
and 1,783 removed. By topic, with the evidence in the source:

| Topic | Evidence | Chapter |
|---|---|---|
| Configuration in JSON, in `/prefs.json` | `src/helpers/ConfigSerializer.{h,cpp}` new; `CommonCLI.cpp` r.30–47 | [CLI reference](../cli/introduction.md) |
| `get`/`set cad` — hardware CAD before transmitting | `CommonCLI.cpp` r.470, r.818 | [Radio](../cli/radio.md) |
| `get`/`set radio.fem.rxgain` and `radio.fem.txgain` | `CommonCLI.cpp` r.544, r.566, r.847, r.853 | [Radio](../cli/radio.md) |
| `get`/`set extra.sf`, `set` only in `USE_LR2021` builds | `CommonCLI.cpp` r.780, r.976 | [Radio](../cli/radio.md) |
| `radio.rxgain` no longer behind a build option; the room server now applies it too | `CommonCLI.cpp` r.535; `simple_room_server/MyMesh.cpp` r.727 | [Radio](../cli/radio.md) |
| `eth.status` and Ethernet support (RAK13800, CH390, serial) | `src/helpers/ethernet/`, `nrf52/EthernetCLI.h` new | [Ethernet](../cli/ethernet.md) |
| Advert name truncated at a UTF-8 code point boundary | `AdvertDataHelpers.cpp` r.21, `UTF8Helpers.h` new | [System](../cli/system.md) |
| `room.post` — a room server posts a message itself | `simple_room_server/MyMesh.cpp` r.977 | not yet covered |
| LR2021 radio | `src/helpers/radiolib/CustomLR2021.h` new | not yet covered |
| Up to four serial interfaces side by side on the companion | `src/helpers/MultiSerialInterface.h` new | not yet covered |
| Hardware crypto (CC310) on nRF52 | `nRFCrypto` in four files, nowhere in `03b6ef4` | not yet covered |
| New colour scheme on the companion UI | `UIColor` in 32 files, nowhere in `03b6ef4` | not yet covered |
| Nine new variants: `heltec_tower_v2`, `heltec_rc32`, `heltec_v4_r8`, `meshnology_w12`, `meshtracker_x1`, `nibble_zero_connect`, `station_g3_esp32`, `thinknode_m7`, `thinknode_m9` | new directories under `variants/` | not yet covered |

Two items from the v1.17.0 release notes were already in the previous pin and
are therefore not a change for this documentation: `get pwrmgt.bootreason` and
the ST7735 display driver.

## What was dropped

Nothing in the command line. Between the two commits the firmware has 40
commands in `CommonCLI.cpp`, the same 40 in both cases. The number of settings
under `get`/`set` goes from 80 to 88; all 80 old ones still exist.

The comparison removes three files, none of them a function of a node:

| File | What happened to it |
|---|---|
| `.vscode/extensions.json` | development file, not firmware |
| `variants/minewsemi_me25ls01/NullDisplayDriver.h` | moved to the shared `src/helpers/ui/NullDisplayDriver.cpp` |
| `variants/wio-e5-mini/NullDisplayDriver.h` | the same |

Within this documentation something was dropped: the page *After the pinned
commit*. It described the commands that existed only on `main` — `cad`,
`radio.fem.rxgain`, `radio.fem.txgain`, `extra.sf` and `eth.status`. All five
belong to v1.17.1 and are now on [Radio](../cli/radio.md) and
[Ethernet](../cli/ethernet.md).

## What is still on the old pin

> [!WARNING]
> The documentation currently carries **two pins**. Only the chapters in the
> table below were verified against `d929643`. All other chapters still name
> `03b6ef4` in their own `Source.` block and have not been re-checked. Go by
> the source block at the top of each chapter, not by this page.

Verified against v1.17.1:

| Chapter | What was updated |
|---|---|
| [CLI reference](../cli/introduction.md) | line numbers, JSON configuration, defaults, deviation table |
| [Radio](../cli/radio.md) | four new commands, `radio.rxgain` corrected |
| [System](../cli/system.md) | line numbers, name length and UTF-8 truncation |
| [Ethernet](../cli/ethernet.md) | new chapter |

Not yet re-verified, measured with
[`tools/diff-impact.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/diff-impact.py):
83 of the 114 chapters per language name at least one file in their source block
that changed between `03b6ef4` and `d929643`. Five of those are the chapters
listed above plus this page; the remaining 78 are still on the old pin. A
changed source file is not proof that the text is wrong, but it is the list that
has to be worked through. The main concentrations are
`design/technical/class-model.md`, the `platform/` section and the `companion/`
section.

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/ConfigSerializer.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ConfigSerializer.cpp)
- [MeshCore firmware — `src/helpers/AdvertDataHelpers.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/AdvertDataHelpers.cpp)
- [MeshCore firmware — `src/helpers/MultiSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/MultiSerialInterface.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/examples/simple_room_server/MyMesh.cpp)
- [MeshCore release notes v1.17.1](https://blog.meshcore.io/2026/08/14/release-1-17-1)
- [MeshCore release notes v1.17.0](https://blog.meshcore.io/2026/08/09/release-1-17-0)

Translated from Dutch by Anthropic Claude
