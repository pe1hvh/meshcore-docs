# Radio realisation

*INJECTION POINT · DOUBLE PAIR · WRAPPER · ESP-NOW*

The radio is the only hardware abstraction where the core does not pick the
filler itself. This chapter shows where that choice *is* made — in the
variant, not in the core — and why there are two classes per radio chip
instead of one. That last part is not duplication but a division of labour.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — `src/Dispatcher.h`,
> `src/helpers/radiolib/`, `src/helpers/esp32/ESPNOWRadio.h` and the
> `target.h` files in `variants/`.

## The contract

`mesh::Radio` sits in `src/Dispatcher.h` on line 22. It lays down that there
must be something that sends and receives bytes, can estimate the airtime of a
packet and can report the signal strength of the last packet received. What
hangs underneath it does not know.

Packet handling holds a `Radio*`. The abstraction goes no further: nowhere in
`src/` or `examples/` is there a line that determines *which* radio that is.

## The injection point sits in the variant

`RADIO_CLASS` and `WRAPPER_CLASS` are the two macros that carry the radio
choice. In the shared tree they are read **nowhere**. The only hits are four
comment lines in `src/helpers/esp32/TBeamBoard.cpp`: `RADIO_CLASS` on r.313 and
r.334, `WRAPPER_CLASS` on r.314 and r.335. Commented-out code, not working
code.

The macros are consumed in `variants/*/target.h` and `variants/*/target.cpp`:

`variants/heltec_v3/target.h` r.16-24

```cpp
extern HeltecV3Board board;
extern WRAPPER_CLASS radio_driver;
extern AutoDiscoverRTCClock rtc_clock;
extern EnvironmentSensorManager sensors;

#ifdef DISPLAY_CLASS
  extern DISPLAY_CLASS display;
  extern MomentaryButton user_btn;
#endif
```

The application includes `target.h` and uses `radio_driver` as a global
variable. The injection point therefore sits in the variant, not in the core —
exactly the reverse of what you would expect from an abstraction layer.
Normally the core is handed a filler; here the edge defines a global variable
the core assumes exists.

![From left to right: platformio.ini defines RADIO_CLASS and WRAPPER_CLASS as
build flags; target.h in the variant directory uses WRAPPER_CLASS to declare
the global variable radio_driver; the application in examples includes
target.h and passes radio_driver to packet handling, which only sees a
mesh::Radio reference.](../../../images/en/radio-realisation-1.svg)

That explains why the radio does not fit the three-way split of
[the class model](class-model.md) the way the other abstractions do. With the
board, the variant picks a class that inherits from a shared parent; with the
radio, the variant picks a class *and* the name under which the core finds it.

## The double pair

There are two classes per radio chip, and that is deliberate.

| Chip | Adapted driver | Contract filler | Targets |
|---|---|---|---|
| SX1262 | `CustomSX1262` | `CustomSX1262Wrapper` | 424 |
| SX1276 | `CustomSX1276` | `CustomSX1276Wrapper` | 29 |
| LR1110 | `CustomLR1110` | `CustomLR1110Wrapper` | 20 |
| STM32WLx | `CustomSTM32WLx` | `CustomSTM32WLxWrapper` | 16 |
| SX1268 | `CustomSX1268` | `CustomSX1268Wrapper` | 12 |
| LLCC68 | `CustomLLCC68` | `CustomLLCC68Wrapper` | **0** |

The left column inherits from RadioLib. `CustomSX1262` is a RadioLib `SX1262`
with adjustments; it knows nothing of MeshCore and fills no MeshCore contract.
That is why it sits in group 3 of the class model, among the standalone
classes.

The right column inherits from `RadioLibWrapper`, which in turn fills
`mesh::Radio`. That is the class carrying the contract. The separation keeps
the RadioLib adjustments apart from the MeshCore agreement: whoever has to
adjust the chip driver touches the left column, whoever changes something on
the mesh side the right one.

![Two columns. On the left the RadioLib family tree: PhysicalLayer with the
six chip classes below it and the six Custom drivers below those. On the right
the MeshCore side: mesh::Radio with RadioLibWrapper below it and the six
Wrapper classes below that. A horizontal arrow runs from each Custom driver to
the matching Wrapper, which holds it as a PhysicalLayer
reference.](../../../images/en/radio-realisation-2.svg)

## LLCC68 exists and is not used

`CustomLLCC68` and `CustomLLCC68Wrapper` exist in full — header, class,
everything the other five pairs have too — and are chosen by **no** build
target. Of the 508 targets, not one sets `RADIO_CLASS` to `CustomLLCC68`.

That is not dead code in the sense of unreachable code; it is working code
without a consumer. The LLCC68 is a cheaper variant of the SX1262 with a
narrower frequency range, and a board was evidently once foreseen that never
arrived. Anyone adding one only needs to set `RADIO_CLASS` and
`WRAPPER_CLASS` in their `platformio.ini`.

Seven of the 508 targets set no radio class at all. Those are the targets that
do not use LoRa, plus `[env:native]` for the tests.

## `RadioLibWrapper` itself

`src/helpers/radiolib/RadioLibWrappers.h` r.6. Inherits from `mesh::Radio` and
holds two references: a `PhysicalLayer*` to the RadioLib driver, and a
`mesh::MainBoard*` to the board.

The second is worth mentioning. A radio wrapper that knows the board sounds
like a layering violation, but there is a reason: on many boards something has
to be switched before transmitting — an antenna switch, a transmit-receive
switch, an LED — and switched back afterwards. The board therefore gets a
signal before and after every transmission.

In the same file, line 74 holds `RadioNoiseListener`, which fills `mesh::RNG`:
the noise of the radio receiver as a source of randomness. That is the reason
entropy is a component of its own in the logical design and not a detail of
the radio.

## Outside the scheme: ESP-NOW

`ESPNOWRadio` (`src/helpers/esp32/ESPNOWRadio.h` r.5) fills `mesh::Radio`
directly, without RadioLib and without a wrapper. It uses no LoRa but ESP-NOW,
Espressif's 2.4 GHz protocol.

That the contract permits this is the best evidence the abstraction is sound:
packet handling does not notice that underneath its `Radio*` there is not a
LoRa chip but a WiFi radio. Range and behaviour differ completely, the
contract does not.

Do not confuse `ESPNOWRadio` with `ESPNowBridge` (`src/helpers/bridges/`). The
first is a radio the mesh protocol runs over; the second is a bridge that
couples two networks.

## Recomputing

The target counts in this chapter come from `tools/design-overview.py`:

```bash
python3 tools/design-overview.py /path/to/MeshCore
```

The script reads the resolved value of `RADIO_CLASS` and `WRAPPER_CLASS` per
`[env:...]` section, with `extends` and `${section.option}` worked out.
Counting on the name of a section gives a different answer; why that is wrong
is in [Variability](../logical/variability.md).

## Sources

- [MeshCore `03b6ef4` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Dispatcher.h)
- [MeshCore `03b6ef4` — `src/helpers/radiolib/RadioLibWrappers.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/radiolib/RadioLibWrappers.h)
- [MeshCore `03b6ef4` — `src/helpers/esp32/ESPNOWRadio.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/esp32/ESPNOWRadio.h)
- [MeshCore `03b6ef4` — `src/helpers/esp32/TBeamBoard.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/esp32/TBeamBoard.cpp)
- [MeshCore `03b6ef4` — `variants/heltec_v3/target.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/heltec_v3/target.h)

Translated from Dutch by Anthropic Claude
