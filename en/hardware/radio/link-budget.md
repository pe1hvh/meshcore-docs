# Link Budget

*TRANSMIT POWER · PATH LOSS · SENSITIVITY · MARGIN*

A link works when more signal arrives at the receiving end than the chip
needs. Everything in between is adding and subtracting decibels. This
chapter sets up that sum, with firmware values where they exist and with
explicitly marked assumptions where they do not.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — the root
> `platformio.ini`, `src/helpers/radiolib/RadioLibWrappers.cpp` and the
> `LORA_TX_POWER` flags in `variants/`. Every figure on this page is
> recomputed by [`tools/link-budget.py`](../../../tools/link-budget.py).

![Bar chart of the link budget: transmit power plus antenna gain minus cable
loss minus path loss, down to the receiver sensitivity, with the remaining
margin](../../../images/en/link-budget-1.svg)

> [!WARNING]
> Two input values do **not** come from the firmware repo and are marked
> below with `°`: the noise figure of the receive chain and the required SNR
> per spreading factor. They are constants at the top of
> `tools/link-budget.py` and have not been verified against a datasheet.
> Every figure that follows from them carries the same uncertainty.

## What the firmware fixes

Three values live in the root `platformio.ini` and apply to every board that
does not override them:

| Flag | Value |
|---|---|
| `LORA_FREQ` | 869.618 MHz |
| `LORA_BW` | 62.5 kHz |
| `LORA_SF` | 8 |

> [!NOTE]
> `LORA_SF=8` is the compile-time default from `platformio.ini`, not the
> setting the Dutch network runs on. The radio parameters are overridden by the
> node configuration after flashing; the *Netherlands* preset sets **SF7** with
> CR5 — see [Getting Started](../../usage/getting-started.md). The sum further
> down this page uses the firmware default SF8 (−130.0 dBm). At SF7 the
> sensitivity is −127.5 dBm and the budget comes out 2.5 dB lower.

Transmit power is fixed per board. Counted across
`variants/*/platformio.ini`, active lines only:

| `LORA_TX_POWER` | Lines |
|---|---|
| 22 dBm | 93 |
| 20 dBm | 13 |
| 19 dBm | 1 |
| 10 dBm | 1 |
| 9 dBm | 4 |
| 8 dBm | 1 |
| 7 dBm | 2 |

That is 115 active lines across 76 variant directories. More lines than
directories, because a variant file can hold several `[env:…]` sections that
each set their own flag. The low values are not frugal boards but boards
with an external power amplifier: 7 dBm at the chip becomes well over 27 dBm
at the connector. See [Antenna](antenna.md).

## The noise floor

At the bottom of the sum sits the noise level. Thermal noise is −174 dBm per
hertz at room temperature; over 62.5 kHz that is −126.0 dBm. The noise
figure of the receive chain is added to that:

| Item | Value |
|---|---|
| thermal noise over 62.5 kHz | −126.0 dBm |
| noise figure receive chain `°` | 6.0 dB |
| **receiver noise floor** | **−120.0 dBm** |

> [!NOTE]
> That the computed floor lands exactly on the −120 dBm at which the
> firmware clamps its own measurement is a coincidence with this noise
> figure, not a proof. The noise figure is an assumption; change it to 5 or
> 7 dB and the equality is gone. The clamp itself *is* in the firmware — see
> [The LoRa Transceiver](sx1262.md).

## Sensitivity per spreading factor

LoRa receives below the noise floor. How far below depends on the spreading
factor:

| SF | Required SNR `°` | Sensitivity |
|---|---|---|
| 7 | −7.5 dB | −127.5 dBm |
| 8 | −10.0 dB | −130.0 dBm |
| 9 | −12.5 dB | −132.5 dBm |
| 10 | −15.0 dB | −135.0 dBm |
| 11 | −17.5 dB | −137.5 dBm |
| 12 | −20.0 dB | −140.0 dBm |

Each SF step buys 2.5 dB of sensitivity and costs a doubling of airtime.
What that airtime costs in duty cycle is in
[Regulations & Duty Cycle](../../usage/regulations.md).

## The sum

Take a node at 22 dBm, a half-wave dipole of 2.15 dBi on both ends and 1 dB
of cable loss:

```text
  transmit power chip        +22.00 dBm
  antenna gain TX             +2.15 dBi
  cable loss TX                −1.00 dB
  ------------------------------------
  e.i.r.p.                   +23.15 dBm

  antenna gain RX             +2.15 dBi
  cable loss RX                −1.00 dB
  sensitivity at SF8        −130.00 dBm
  ------------------------------------
  budget                     154.30 dB
```

That budget may be spent on path loss. In free space the path loss is
32.44 + 20·log(f in MHz) + 20·log(d in km):

| Distance | Free-space loss |
|---|---|
| 100 m | 71.2 dB |
| 1 km | 91.2 dB |
| 5 km | 105.2 dB |
| 10 km | 111.2 dB |
| 50 km | 125.2 dB |

A budget of 154 dB would reach more than a thousand kilometres in free
space. That number is correct and useless at the same time: free space does
not exist at ground level. The earth curves away, buildings and trees get in
the way, and the Fresnel zone touches the ground long before the budget runs
out. Free-space loss is an upper bound, not a prediction. Why practice falls
so far short is in
[Higher and stronger isn't always better](../../technical/dead-zone.md).

## What a dB is worth

More useful than an absolute distance is the ratio. Every 6 dB doubles the
distance in free space, every 6 dB less halves it:

| Change | Factor on distance |
|---|---|
| −6 dB | × 0.50 |
| −3 dB | × 0.71 |
| −1 dB | × 0.89 |
| +1 dB | × 1.12 |
| +3 dB | × 1.41 |
| +6 dB | × 2.00 |

That is where the practical value of this whole chapter sits. A bad
connector costing 3 dB takes almost 30 percent of your distance. One SF step
buys 2.5 dB and therefore a good 30 percent — but doubles the airtime. And
an antenna one metre higher often beats both, because it removes the
obstacle instead of trying to transmit through it.

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/platformio.ini)
  — `LORA_FREQ`, `LORA_BW` and `LORA_SF`
- [`src/helpers/radiolib/RadioLibWrappers.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/radiolib/RadioLibWrappers.cpp)
  — the measured noise floor and the −120 dBm lower bound
- [`variants/heltec_v3/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/heltec_v3/platformio.ini)
  — `LORA_TX_POWER=22`

In this repository:

- [`tools/link-budget.py`](../../../tools/link-budget.py) — recomputes every
  figure on this page

Not from the firmware repo: the noise figure of the receive chain and the
required SNR per spreading factor, both marked with `°`. The thermal noise
floor of −174 dBm/Hz is not a datasheet value but follows from *kT* at room
temperature.

Related in this documentation:

- [The LoRa Transceiver](sx1262.md) — where the transmit power is set
- [Antenna](antenna.md) — gain and loss at the RF port
- [Higher and stronger isn't always better](../../technical/dead-zone.md) —
  why free space is not practice
- [Regulations & Duty Cycle](../../usage/regulations.md) — how much of this
  budget you may actually use

Translated from Dutch by Anthropic Claude
