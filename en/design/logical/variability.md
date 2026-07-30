# Variability

*THREE AXES · 508 BUILDS · WHY COUNTING ON NAMES GOES WRONG*

One codebase produces 508 different build targets. This chapter describes how
that works: along which axes MeshCore varies, which part of the theoretically
possible combinations actually exists, and why you cannot read the figures off
the names of the targets.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — the root `platformio.ini` and all
> 79 `variants/*/platformio.ini`. All figures come from
> `tools/design-overview.py`.

## Three axes

MeshCore varies along three independent axes. A build target is a point in that
space: one role, one platform family, one board.

![Three axes in a block diagram: role, platform family and board. Beside it a
separate column with the mixins that can be on or off independently of the
axes: radio, display, bridge, sensors and logging.](../../../images/en/variability-1.svg)

| Axis | Values | Fixed by |
|---|---|---|
| Role | 6 | Which application directory is compiled in |
| Platform family | 4 | Which platform macro is defined |
| Board | 79 variants | Which variant file defines the target |

Alongside those are mixins that stand apart from the axes: which radio chip,
which display type, whether there is a bridge, whether there are sensors, and
whether logging is on.

## The figures

```
ini files read               80   (1 root + 79 variants)
sections total              616
[env:...] sections          508
base sections               108
```

Of the 508 targets, 507 compile one application; the 508th is the test target
that runs on the development machine.

| Role | Targets | Variant directories |
|---|---|---|
| Companion radio | 174 | 76 |
| Repeater | 136 | 75 |
| KISS modem | 80 | 74 |
| Room server | 73 | 65 |
| Terminal chat | 26 | 24 |
| Sensor | 18 | 16 |

| Platform family | Targets |
|---|---|
| ESP32 | 270 |
| nRF52 | 199 |
| RP2040 | 22 |
| STM32 | 16 |

And the cross table, which shows that the axes are not fully independent:

| Role | ESP32 | nRF52 | RP2040 | STM32 |
|---|---|---|---|---|
| Companion radio | 91 | 75 | 4 | 4 |
| Repeater | 83 | 42 | 6 | 5 |
| KISS modem | 36 | 36 | 4 | 4 |
| Room server | 34 | 35 | 4 | 0 |
| Terminal chat | 17 | 5 | 4 | 0 |
| Sensor | 9 | 6 | 0 | 3 |

Three cells are zero. There is no room server and no terminal chat on STM32,
and no sensor on RP2040. That is not a technical impossibility but a choice:
nobody has needed that combination.

## The product space is not full

Six roles on seventy-nine boards would give 474 combinations. There are 507.
That is not a contradiction but the result of the mixins: the same role on the
same board exists several times, in variants with and without a bridge, with
different displays or with a different transport.

At the same time the space is not full. Far from every board carries all six
roles. The companion radio exists on 76 of the 79 boards, the sensor on 16.

| Mixin | Targets |
|---|---|
| GPS enabled | 323 |
| Display present | 309 |
| ESP-NOW bridge | 33 |
| RS232 bridge | 13 |
| Debug output on | 36 |
| Packet logging on | 10 |

## Class injection

The mixins work through one mechanism: the build system passes a class name
along as a macro, and the code uses that name as if it had always been there.
That is how a variant file chooses which radio and which display end up in the
binary, without the application knowing about it.

| Macro | Distinct values | Targets that set it |
|---|---|---|
| `RADIO_CLASS` | 5 | 501 |
| `WRAPPER_CLASS` | 5 | 501 |
| `DISPLAY_CLASS` | 11 | 309 |

The five radio values cover five chip families. A sixth implementation is
present in the source that no target selects; it is available for anyone who
needs it in a variant of their own.

Seven targets set no `RADIO_CLASS`. Five of those are ESP-NOW variants that use
no LoRa radio, and the sixth is the test target. The seventh is a bug; see
below.

## Why counting on names goes wrong

This is the most important warning in this chapter, and the reason a script
comes with it.

The name of an `[env:...]` section is free text. It says nothing about what is
compiled. Three ways in which the name lies:

**The name does not mention the role.** `Generic_ESPNOW_room_svr` compiles the
room server, but searching for `_room_server` will not find it. There are also
targets with `_repeatr` and `_Repeater` in the name.

**The name mentions a role that is not there.** Conversely, a name ending in
`_repeater` is no proof that the repeater is in it.

**The role is not in the section itself.** 28 of the 508 targets name no
application directory anywhere in their own text. They inherit it through
`extends` or through a text reference to another section. A search over the
file does not see them.

The correct method is: resolve the section completely — follow `extends` and
expand text references — and then look at which application directory the
source filter includes. `tools/design-overview.py` does exactly that:

```bash
python3 tools/design-overview.py /path/to/MeshCore --targets simple_room_server
```

As a check: that call yields 73 targets in 65 variant directories, the same
figure `tools/room-server-overview.py` arrives at by a different route.

## Two traps when counting

**Count sections, not lines.** A naive search for `examples/` counts lines and
overstates the companion radio by a factor of three, because that application
spreads its source filter over several lines.

**Ignore commented-out macros.** Search the text for `MESH_DEBUG` and you find
387. It is genuinely enabled in 36 targets; in the rest the line sits disabled
in the file as an example. The same holds for packet logging: 385 mentions, 10
actually on.

## Three variant files with other line endings

`variants/minewsemi_me25ls01`, `variants/nibble_screen_connect` and
`variants/wio_wm1110` use Windows line endings. Read the files line by line
without normalising and an invisible character remains at the end of every
value. The parent with that character and the parent without then count as two
different sections, and half the inheritance chain drops out. The script
normalises the line endings before doing anything else.

## One target that cannot compile

`Generic_E22_kiss_modem` extends the base section `Generic_E22` and thereby
also takes over the source filter that includes `variants/generic-e22/`. That
directory contains:

`variants/generic-e22/target.cpp` l.8-13

```cpp
  RADIO_CLASS radio = new Module(P_LORA_NSS, P_LORA_DIO_1, P_LORA_RESET, P_LORA_BUSY, spi);
```

But neither the target, nor the base section, nor any section above it defines
`RADIO_CLASS`. This target's siblings do — each picks between the SX1262 and
SX1268 version per target — but the KISS modem variant was skipped. That makes
it the only one of the 508 that does not translate.

## Sources

- [MeshCore `03b6ef4` — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [MeshCore `03b6ef4` — `variants/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/variants)
- [MeshCore `03b6ef4` — `variants/heltec_v3/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/heltec_v3/platformio.ini)
- [PlatformIO — Project Configuration File](https://docs.platformio.org/en/latest/projectconf/index.html)

Translated from Dutch by Anthropic Claude
