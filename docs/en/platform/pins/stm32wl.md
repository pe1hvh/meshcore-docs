# Pin assignments — STM32WL

*4 VARIANTS · SIGNAL NAME · GPIO · SOURCE LINE*

Which pin of the STM32WL connects to what, per variant in the firmware repo.
This is a reference page for anyone who builds, measures or wants to
understand a board — which device you can buy is in
[Node matrix](../node-matrix.md), and what sits inside the chip per family is
in [The four platform families](../platform-families.md).

> [!NOTE]
> **Source.** MeshCore v1.17.1, commit
> [`d929643`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e), 14 August 2026 — `variants/*/platformio.ini` and the
> headers in the same directory. Reproduce with
> [`tools/variant-pins.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/variant-pins.py):
>
> ```bash
> python3 tools/variant-pins.py --repo ../MeshCore \
>     --familie STM32WL --markdown --taal en --kopniveau 3
> ```
>
> Commented-out lines do not count. A `#define` inside `#if 0` does: the
> script cannot tell the difference.

## How to read these tables

Per variant the signals are grouped: LoRa radio, I2C, SPI, display, GPS,
buttons and LED, power and battery, and whatever falls outside that. Each
line names the file and line number where the definition sits, so you can
check it yourself.

The value is sometimes not a number but another name — `P_LORA_NSS` then
points at `LORA_CS`, which sits a few lines up with the real number. The
first occurrence wins: if a name appears twice, the second is an alias.

Constants that look like a pin but are not do not appear in the table.
`LORA_TX_POWER`, `SX126X_DIO3_TCXO_VOLTAGE` and `BLE_PIN_CODE` are radio and
firmware settings; the script reports them separately.

The four STM32WL variants have the shortest tables of any family: 15 signals
from the `build_flags` and 2 from a header. The radio sits on the die, so
there is no SPI link to a separate transceiver eating pins.

## The variants

### `rak3x72`

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `A0` | `target.h` l.11 |


### `tiny_relay`

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `A0` | `target.h` l.11 |


### `wio-e5-dev`

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_SERIAL_RX` | `PB7` | `platformio.ini` l.12 |
| `PIN_SERIAL_TX` | `PB6` | `platformio.ini` l.13 |


### `wio-e5-mini`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_TX_LED` | `LED_RED` | `platformio.ini` l.12 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `USER_BTN` | `platformio.ini` l.13 |

## Sources

- [`variants/`](https://github.com/meshcore-dev/MeshCore/tree/d92964352441e53b93e8667b802e04f6e072b39e/variants)
  — 4 directories of this family, each with a `platformio.ini` and the
  headers beside it
- [`tools/variant-pins.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/variant-pins.py) — the script that builds
  these tables

Related in this documentation:

- [Node matrix](../node-matrix.md) — which devices you can buy
- [MeshCore Platforms](../platforms.md) — why the platform matters
- [The four platform families](../platform-families.md) — what sits inside
  the chip per family
