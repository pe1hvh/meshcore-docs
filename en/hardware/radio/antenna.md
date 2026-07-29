# Antenna

*CONNECTOR · SWR · RF SWITCH · PRACTICAL CHOICE*

The antenna is the only part of a node that knows no firmware and still
determines most of your range. What the firmware does know about it is the
switch in between: one antenna has to both transmit and receive, and the
chip has to know how that changeover is wired. This chapter describes that
switch, the connector, and the relation between standing wave ratio and
reflected power.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `src/helpers/radiolib/CustomSX1262.h` and the RF flags in `variants/`.
> Connectors, SWR and antenna types do not come from the firmware; that is
> general radio engineering and is marked as such.

![Diagram of the RF path: from the chip through the RF switch to the
connector and the antenna, with DIO2 switching the transmit path and RXEN
switching the receive path](../../../images/en/antenna-1.svg)

## One antenna, two paths

Transmitting and receiving happen over the same antenna but not over the
same path: the transmit path runs through the power amplifier, the receive
path through the LNA. So there is a switch between chip and connector.
MeshCore knows two ways of driving it, and they are not mutually exclusive.

| Drive | Flag | Variant directories |
|---|---|---|
| DIO2 on the chip drives the switch | `SX126X_DIO2_AS_RF_SWITCH` | 60 of 79 |
| separate GPIO pins drive the switch | `SX126X_RXEN` · `SX126X_TXEN` | 24 of 79 |

Counted per variant directory across `variants/`, including both `-D` flags
in `platformio.ini` and `#define` lines in a header inside that directory;
commented-out lines do not count.

The first is the simpler one: the chip pulls DIO2 high as soon as it
transmits and low as soon as it listens. The firmware only has to pass the
flag on to RadioLib, which happens in `std_init()` — see
[The LoRa Transceiver](sx1262.md).

The second appears on boards with an external power amplifier or a separate
LNA, where one line is not enough. If one of the two pins is missing, the
wrapper fills it in with `RADIOLIB_NC`.

## A board that uses both

The T-Beam 1W combines them, and the comment in the variant says exactly
how:

`variants/lilygo_tbeam_1w/platformio.ini` r.22-28

```ini
  ; RF switch configuration:
  ;   DIO2 controls TX path (PA enable) via SX126X_DIO2_AS_RF_SWITCH
  ;   GPIO21 controls RX path (LNA enable) via SX126X_RXEN
  ; Truth table: DIO2=1,RXEN=0 → TX | DIO2=0,RXEN=1 → RX
  -D SX126X_DIO2_AS_RF_SWITCH=true
  -D SX126X_RXEN=21
  -D SX126X_DIO3_TCXO_VOLTAGE=3.0
```

DIO2 switches the transmit path, GPIO21 the receive path. `SX126X_TXEN` is
not set and therefore becomes `RADIOLIB_NC`. The same file also explains
what sits behind that switch:

`variants/lilygo_tbeam_1w/platformio.ini` r.33-34

```ini
  ; TX power: 22dBm to SX1262, PA module adds ~10dB for 32dBm total
  -D LORA_TX_POWER=22
```

The chip runs at 22 dBm, the external amplifier turns that into roughly
32 dBm. That is why `LORA_TX_POWER` can never be read on its own: it is the
power the chip delivers, not the power leaving the antenna. What you are
allowed to radiate is in
[Regulations & Duty Cycle](../../usage/regulations.md).

> [!WARNING]
> Transmitting without an antenna, or with an antenna for the wrong band,
> sends the power back into the power amplifier. At 22 dBm that is already
> unhealthy; on a board with an external amplifier it is fatal. Connect the
> antenna before you apply power.

## Connector and cable

Not from the firmware — general radio engineering.

| Connector | Where | Note |
|---|---|---|
| SMA | on most development boards | pin in the centre on the cable side |
| RP-SMA | much WiFi hardware | reversed pin; fits mechanically, does not work |
| IPEX/U.FL | on modules and compact nodes | fragile, meant for a pigtail |

SMA and RP-SMA screw onto each other without making contact in the centre.
That is the most common fault behind a node that transmits but reaches
nothing.

Cable is loss. At 868 MHz thin coax easily costs several dB per ten metres.
A node close to the antenna with a short cable beats a node indoors with a
long one. What a dB costs in distance is in [Link Budget](link-budget.md).

## SWR: what comes back

Not from the firmware — this is the standard conversion from standing wave
ratio to reflected power.

| SWR | Reflected | In practice |
|---|---|---|
| 1.0 : 1 | 0 % | theoretically perfect |
| 1.5 : 1 | 4 % | fine |
| 2.0 : 1 | 11 % | acceptable |
| 3.0 : 1 | 25 % | too high, needs matching |
| ∞ | 100 % | open or shorted |

The SX1262 has no SWR measurement on board and the firmware therefore reads
nothing about it. You notice a bad match only through disappointing range
and a power amplifier that runs hot.

## Three practical rules

1. **More gain is direction, not power.** An antenna with higher gain looks
   flatter and loses above and below. Why more gain can even work against
   you is in
   [Higher and stronger isn't always better](../../technical/dead-zone.md);
   the radiation pattern and the dead zone belong there and are not repeated
   here.
2. **A half-wave dipole is nearly always enough.** 2.15 dBi, no ground plane
   needed, and exactly the reference the regulations use.
3. **Height beats power.** One metre higher more often gains you more than
   one dB extra, because it lifts obstacles out of the first Fresnel zone.

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`src/helpers/radiolib/CustomSX1262.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/radiolib/CustomSX1262.h)
  — `setDio2AsRfSwitch()` and `setRfSwitchPins()`
- [`variants/lilygo_tbeam_1w/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/lilygo_tbeam_1w/platformio.ini)
  — the RF switch truth table and the external amplifier

Not from the firmware repo: connectors, SWR and antenna types. That is
general radio engineering; the SWR table is the standard conversion from
standing wave ratio to reflected power.

Related in this documentation:

- [The LoRa Transceiver](sx1262.md) — what sits on the other side of the
  switch
- [Link Budget](link-budget.md) — what gain and loss are worth in distance
- [Higher and stronger isn't always better](../../technical/dead-zone.md) —
  radiation pattern, antenna gain and coverage
- [Regulations & Duty Cycle](../../usage/regulations.md) — what you may
  radiate
- [Node Matrix](../../platform/node-matrix.md) — which board has which
  connector

Translated from Dutch by Anthropic Claude
