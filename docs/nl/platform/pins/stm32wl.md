# Pinbezetting — STM32WL

*4 VARIANTEN · SIGNAALNAAM · GPIO · BRONREGEL*

Welke pin van de STM32WL waar aan vastzit, per variant in de firmware-repo.
Dit is een naslagpagina voor wie zelf bouwt, meet of een bord doorgrondt —
welk apparaat je kunt kopen staat in [Nodematrix](../node-matrix.md), en wat
er per familie in de chip zit in
[De vier platformfamilies](../platform-families.md).

> [!NOTE]
> **Bron.** MeshCore v1.17.1, commit
> [`d929643`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e), 14 augustus 2026 — `variants/*/platformio.ini` en de
> headers in dezelfde map. Reproduceren kan met
> [`tools/variant-pins.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/variant-pins.py):
>
> ```bash
> python3 tools/variant-pins.py --repo ../MeshCore \
>     --familie STM32WL --markdown --kopniveau 3
> ```
>
> Uitgecommentarieerde regels tellen niet mee. Een `#define` binnen `#if 0`
> wel: dat onderscheid maakt het script niet.

## Hoe je deze tabellen leest

Per variant staan de signalen gegroepeerd: LoRa-radio, I2C, SPI, display,
GPS, knoppen en LED, voeding en accu, en wat daarbuiten valt. Elke regel
noemt het bestand en het regelnummer waar de definitie staat, zodat je hem
zelf kunt nakijken.

De waarde is soms geen getal maar een andere naam — `P_LORA_NSS` wijst dan
naar `LORA_CS`, en die staat een paar regels hoger met het echte nummer. De
eerste vindplaats wint: staat een naam twee keer, dan is de tweede een alias.

Constanten die op een pin lijken maar het niet zijn, staan niet in de tabel.
`LORA_TX_POWER`, `SX126X_DIO3_TCXO_VOLTAGE` en `BLE_PIN_CODE` zijn
radio- en firmware-instellingen; het script meldt ze apart.

De vier STM32WL-varianten hebben de kortste tabellen van alle families: 15
signalen uit de `build_flags` en 2 uit een header. De radio zit op de die,
dus er is geen SPI-koppeling naar een losse transceiver die pinnen kost.

## De varianten

### `rak3x72`

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `A0` | `target.h` r.11 |


### `tiny_relay`

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `A0` | `target.h` r.11 |


### `wio-e5-dev`

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_SERIAL_RX` | `PB7` | `platformio.ini` r.12 |
| `PIN_SERIAL_TX` | `PB6` | `platformio.ini` r.13 |


### `wio-e5-mini`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_TX_LED` | `LED_RED` | `platformio.ini` r.12 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `USER_BTN` | `platformio.ini` r.13 |

## Bronnen

- [`variants/`](https://github.com/meshcore-dev/MeshCore/tree/d92964352441e53b93e8667b802e04f6e072b39e/variants)
  — 4 mappen van deze familie, elk met `platformio.ini` en de headers
  ernaast
- [`tools/variant-pins.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/variant-pins.py) — het script dat deze
  tabellen maakt

Verwant in deze documentatie:

- [Nodematrix](../node-matrix.md) — welke apparaten er te koop zijn
- [MeshCore Platforms](../platforms.md) — waarom het platform uitmaakt
- [De vier platformfamilies](../platform-families.md) — wat er per familie in
  de chip zit
