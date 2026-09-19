# Changes in v1.17.1

*RELEASE · DIFF · PIN · STATE OF THE DOCUMENTATION*

MeshCore v1.17.1 was released on 14 August 2026. This page lists what changes
relative to the commit this documentation was pinned to until now, which
chapters have already been re-verified and which have not. What is stated here
was derived from the source code itself; the official release notes were used as
an index, not as evidence.

> [!NOTE]
> **Mind the wording around `UIColor`.** The official release table calls this
> "a new colour scheme on the companion UI". That does not cover it: a scheme
> is a fixed set of colours, whereas `UIColor` is a list of nine roles
> *without* values which every screen driver fills in separately. This
> documentation therefore does not use the term colour scheme for it.

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
| Configuration in JSON, in `/prefs.json` | `src/helpers/ConfigSerializer.{h,cpp}` new; `src/helpers/CommonCLI.cpp` r.30–47 | [CLI reference](../cli/introduction.md) |
| `cad` — hardware CAD before transmitting, through `get`/`set` | `src/helpers/CommonCLI.cpp` r.470, r.818 | [Radio](../cli/radio.md) |
| `radio.fem.rxgain` and `radio.fem.txgain`, settable and readable | `src/helpers/CommonCLI.cpp` r.544, r.566, r.847, r.853 | [Radio](../cli/radio.md) |
| `extra.sf`, readable in every build but settable only in LR2021 builds | writing sits behind `USE_LR2021` at `src/helpers/CommonCLI.cpp` r.779, with the setter at r.780 and the getter at r.976 | [Radio](../cli/radio.md) |
| `radio.rxgain` no longer behind a build option; the room server now applies it too | `src/helpers/CommonCLI.cpp` r.535; `examples/simple_room_server/MyMesh.cpp` r.727 | [Radio](../cli/radio.md) |
| `eth.status` and Ethernet support (RAK13800, CH390, serial) | `src/helpers/ethernet/`, `nrf52/EthernetCLI.h` new | [Ethernet](../cli/ethernet.md) |
| Advert name truncated at a UTF-8 code point boundary | `src/helpers/AdvertDataHelpers.cpp` r.21, `UTF8Helpers.h` new | [System](../cli/system.md) |
| `room.post` — a room server posts a message itself | `examples/simple_room_server/MyMesh.cpp` r.977 | [Requests and CLI](../technical/roomserver/requests-and-cli.md) |
| LR2021 radio | `src/helpers/radiolib/CustomLR2021.h` new | [The LR2021](../hardware/radio/lr2021.md) |
| Up to four serial interfaces side by side on the companion | `src/helpers/MultiSerialInterface.h` new | [The three transports](../companion/technical/transports.md) |
| Hardware crypto (CC310) on nRF52, for every nRF52 build | `nRFCrypto` in four files, nowhere in `03b6ef4` | [Private & Public Key Encryption](../technical/key-encryption.md) |
| Colour as a role on the companion UI: nine roles every screen driver fills in itself | `UIColor` in 32 files, nowhere in `03b6ef4` | [The Display](../hardware/peripherals/display.md) |
| Routing policy in a file of its own: three hop limits, four reply routes, three reply scopes | `src/helpers/RoutingPolicy.h` new, 68 lines; included by `examples/simple_repeater/MyMesh.h` r.37 and `examples/simple_room_server/MyMesh.h` r.24 | [Regions and Scopes](../technical/regions-and-scopes.md) |
| Screen driver NV3001B, the only one that scales up the UI coordinates | `src/helpers/ui/NV3001BDisplay.{h,cpp}` new; `variants/heltec_rc32/` | [The Display](../hardware/peripherals/display.md) |
| Vibration through a DRV2605 driver chip, beside the existing pin control | `src/helpers/ui/DRV2605Vibration.h` new; `GenericVibration.h` already existed | [Feedback](../hardware/peripherals/feedback.md) |
| Nine new variants: `heltec_tower_v2`, `heltec_rc32`, `heltec_v4_r8`, `meshnology_w12`, `meshtracker_x1`, `nibble_zero_connect`, `station_g3_esp32`, `thinknode_m7`, `thinknode_m9` | new directories under `variants/` | partly: five are in [Node Matrix](../platform/node-matrix.md), `heltec_rc32` in [ESP32](../platform/pins/esp32.md) and [The Display](../hardware/peripherals/display.md); `heltec_v4_r8`, `meshnology_w12` and `nibble_zero_connect` not yet |

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

Within this documentation the page *After the pinned commit* was taken out of
the table of contents. It described the commands that existed only on `main` —
`cad`, `radio.fem.rxgain`, `radio.fem.txgain`, `extra.sf` and `eth.status`.
All five belong to v1.17.1 and are now on [Radio](../cli/radio.md) and
[Ethernet](../cli/ethernet.md). The file `cli/after-pinned-commit.md` is still
present in both language trees, with no reference from a README and no place
in the menu; removing it awaits an explicit instruction.

## What is still on the old pin

> [!WARNING]
> The documentation currently carries **two pins**. Only the chapters in the
> table below were verified against `d929643`. All other chapters still name
> `03b6ef4` in their own `Source.` block and have not been re-checked. Go by
> the source block at the top of each chapter, not by this page.

Twenty-three chapters per language name `d929643` in their source block.
Reproducible with `grep -rl d929643 docs/en --include='*.md'`.

| Section | Chapters on `d929643` |
|---|---|
| CLI reference | [CLI reference](../cli/introduction.md), [Radio](../cli/radio.md), [System](../cli/system.md), [Ethernet](../cli/ethernet.md) |
| Technical | [Private & Public Key Encryption](../technical/key-encryption.md)°, [Regions and Scopes](../technical/regions-and-scopes.md)°, [Requests and CLI](../technical/roomserver/requests-and-cli.md) |
| Hardware | [The LoRa Transceiver](../hardware/radio/sx1262.md), [The LR2021](../hardware/radio/lr2021.md), [The Display](../hardware/peripherals/display.md), [Feedback](../hardware/peripherals/feedback.md) |
| Platform | [MeshCore Platforms](../platform/platforms.md), [The Four Platform Families](../platform/platform-families.md), [Node Matrix](../platform/node-matrix.md) and the four pin layouts |
| Node design | [The class model](../design/technical/class-model.md), [Compile-time configuration](../design/technical/configuration.md), [Platform realisation](../design/technical/platform-realisation.md)° |
| Companion design | [The three transports](../companion/technical/transports.md) |
| Project | this page |

° Partly: the source block of that chapter says which sections were verified
against `d929643` and which text is still on the old pin.

Not yet re-verified, measured with
[`tools/diff-impact.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/diff-impact.py):
87 of the 119 chapters per language name at least one file in their source block
that changed between `03b6ef4` and `d929643`. Nineteen of those are in the table
above; the remaining 68 are still on the old pin. A changed source file is not
proof that the text is wrong, but it is the list that has to be worked through.
The main concentrations are now [Direct
Messages](../technical/direct-messages.md), the remaining `cli/` chapters and
the `companion/` section.

## Sources

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/ConfigSerializer.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ConfigSerializer.cpp)
- [MeshCore firmware — `src/helpers/AdvertDataHelpers.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/AdvertDataHelpers.cpp)
- [MeshCore firmware — `src/helpers/MultiSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/MultiSerialInterface.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/examples/simple_room_server/MyMesh.cpp)
- [MeshCore release notes v1.17.1](https://blog.meshcore.io/2026/08/14/release-1-17-1)
- [MeshCore release notes v1.17.0](https://blog.meshcore.io/2026/08/09/release-1-17-0)

Translated from Dutch by Anthropic Claude
