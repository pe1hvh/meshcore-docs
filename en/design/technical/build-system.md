# The build system

*INI FILES · BASE SECTIONS · INHERITANCE · SOURCE FILTER*

One codebase yields 508 firmware images. This chapter describes the machinery
that does it: eighty `platformio.ini` files, 108 base sections and two
different inheritance mechanisms that both have to be followed. Follow only
one and you miss 28 build targets without anything breaking.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — the root `platformio.ini` and all
> 79 `variants/*/platformio.ini`.

## The numbers

| What | Count |
|---|---|
| `platformio.ini` files | 80 (1 root + 79 variants) |
| Sections in total | 616 |
| `[env:...]` sections (build targets) | 508 |
| Base sections | 108 |
| Targets that get their application only through inheritance | 28 |

A base section is a section without the `env:` prefix. PlatformIO does not
build it, but other sections can inherit from it through `extends`. The 108
base sections therefore carry the shared settings of the 508 targets.

![A pyramid. At the bottom arduino_base with 507 targets under it; above that
the four family base sections esp32_base, nrf52_base, rp2040_base and
stm32_base; above those the board-specific base sections; at the top the
individual env sections.](../../../images/en/build-system-1.svg)

## Two inheritance mechanisms

PlatformIO has two, and they work differently.

**`extends`** takes over every option from the named section. A section with
`extends = esp32_base` gets every option in it, unless it overrides one
itself.

**`${section.option}`** splices text. That is not inheritance but text
substitution: in place of the reference, the value of that one option appears
literally.

A section can use both, and many do. Follow only `extends` and you miss the
options arriving through `${...}`; follow only `${...}` and you miss
everything inherited through `extends`. In MeshCore `03b6ef4`, following just
one of the two costs 28 build targets: those get their `build_src_filter` —
and therefore their application — from a shared base section that is not an
`[env:...]` itself.

## How many targets come from which base section

| Base section | Targets inheriting from it |
|---|---|
| `arduino_base` | 507 |
| `esp32_base` | 270 |
| `nrf52_base` | 199 |
| `rp2040_base` | 22 |
| `esp32c6_base` | 16 |
| `stm32_base` | 16 |
| `nibble_screen_connect_base` | 8 |
| `Heltec_E213_base` | 6 |
| `Heltec_E290_base` | 6 |
| `Heltec_T190_base` | 6 |
| `Heltec_tracker_base` | 6 |
| `Heltec_Wireless_Paper_base` | 6 |

`arduino_base` sits under everything: 507 of the 508 targets inherit from it.
The only exception is `[env:native]`, the section that runs the tests on a PC.

The four family base sections beneath it — 270 + 199 + 22 + 16 — add up to
507. Every target belongs to exactly one platform family.

`esp32c6_base` is not a fifth family. That section itself inherits from
`esp32_base` and therefore sits inside the ESP32 family; the 16 targets under
it are counted in the 270 as well. The ESP32-C6 is a RISC-V chip rather than
an Xtensa, which calls for a few different compiler options, but for the
firmware it is the same family.

## The name of a section proves nothing

This is the most important pitfall in this chapter, and it applies to every
count over the build matrix.

Which application a target compiles is in `build_src_filter` — the option that
determines which source files come along. Not in the name of the section. A
section called `Generic_ESPNOW_room_svr` compiles the room server without
`room_server` appearing in the name; conversely, a name ending in
`_room_server` proves nothing.

Counting on the name gives 70 room server targets in 66 directories. Counting
on the resolved source filter gives 73 in 65. That difference of three targets
and one directory comes entirely from the two inheritance mechanisms above.

| Role | Targets |
|---|---|
| Companion radio | 174 |
| Repeater | 136 |
| KISS modem | 80 |
| Room server | 73 |
| Terminal chat | 26 |
| Sensor | 18 |

Together 507, plus `[env:native]` without an application. What each role does
is in [Roles](../logical/roles.md).

## Admixture

On top of the combination of board and role come the separate switches. They
are on or off independently of one another, and explain why there are more
targets than boards times roles:

| Switch | Targets |
|---|---|
| `ENV_INCLUDE_GPS` | 323 |
| `DISPLAY_CLASS` | 309 |
| `MESH_DEBUG` | 36 |
| `WITH_ESPNOW_BRIDGE` | 33 |
| `WITH_RS232_BRIDGE` | 13 |
| `MESH_PACKET_LOGGING` | 10 |

`MESH_DEBUG` deserves a warning. The macro appears 387 times across the eighty
ini files, but is genuinely on in only 36 targets. The rest sit commented out
behind a `;`. Anyone searching on text rather than on active lines overstates
debugging by a factor of ten. `MESH_PACKET_LOGGING` behaves the same way: 385
mentions, 10 targets.

## Three files with CRLF

`variants/minewsemi_me25ls01/`, `variants/nibble_screen_connect/` and
`variants/wio_wm1110/` use Windows line endings. Without normalisation
`esp32_base\r` and `esp32_base` read as two different parents, and those
targets fall outside every count.

`tools/design-overview.py` therefore strips the line endings before it does
anything else.

## What does not compile

`Generic_E22_kiss_modem` does not compile. The section exists and PlatformIO
recognises it, but the combination of options produces a build error. The
target sits in the counts because it is an `[env:...]` section; anyone
expecting a firmware image will not get one.

`platformio.local.ini` is listed in the root's `extra_configs` but is not in
the repo. That is deliberate: it is the place for local settings you do not
commit. PlatformIO skips a missing file in `extra_configs` without
complaining.

`FIRMWARE_BUILD_DATE` reads `"6 Jun 2026"` in four of the six applications,
while this commit is from 28 July. The value is set by hand, is rarely
updated, and is therefore no reliable indication of when a build was made.

## Recomputing

```bash
python3 tools/design-overview.py /path/to/MeshCore
python3 tools/design-overview.py /path/to/MeshCore --targets simple_room_server
```

The script resolves both `extends` and `${section.option}`, strips CRLF, and
skips commented-out lines. Its room server count (73 targets in 65
directories) matches `tools/room-server-overview.py`, which arrives at the same
number by a different route — that cross-check is the proof the resolver is
right.

## Sources

- [MeshCore `03b6ef4` — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [MeshCore `03b6ef4` — `variants/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/variants)
- [MeshCore `03b6ef4` — `variants/heltec_v3/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/heltec_v3/platformio.ini)
- [PlatformIO — Section extension](https://docs.platformio.org/en/latest/projectconf/section_env.html)

Translated from Dutch by Anthropic Claude
