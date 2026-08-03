# Hardware van een node

*BLOKSCHEMA · RADIO · INTERFACES · RANDAPPARATUUR*

Een MeshCore-node is een MCU met een radio ernaast en een handvol
onderdelen eromheen. Deze sectie beschrijft die onderdelen stuk voor stuk:
wat het is, hoe het aan de MCU hangt, en wat de firmware ermee doet.
Dit hoofdstuk zet het blokschema neer en legt uit waar de grens ligt tussen
de drie groepen waarin de rest van de sectie is ingedeeld.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `variants/heltec_v3/platformio.ini`, `variants/heltec_v3/target.h`,
> `src/helpers/BaseSerialInterface.h`, `src/helpers/ui/DisplayDriver.h` en
> `src/helpers/SensorManager.h`.

## Wat er in een node zit

![Blokschema van een MeshCore-node: antenne en LoRa-transceiver links, de
MCU in het midden, BLE, WiFi en USB-serieel naar boven richting de
companion-app, en display, GPS en knoppen onderaan aan de bussen van de
MCU](../../images/nl/node-blockdiagram-1.svg)

Links staat de RF-kant: een antenne op een transceiver, die via SPI aan de
MCU hangt. In het midden de MCU — het enige onderdeel dat in elke node
zit, en het onderdeel dat bepaalt wat de rest kan zijn. Naar boven de
verbindingen met de buitenwereld, waarlangs een telefoon of terminal de
node bedient. Naar beneden alles wat aan de bussen van de MCU hangt en
optioneel is: een node werkt zonder scherm, zonder GPS en zonder knoppen.

De transceiver is niet optioneel. Zonder radio is er geen node, alleen een
bordje met een processor.

## MCU of SoC

Het middelste blok heet in deze sectie de **MCU**: de chip waarop de
firmware draait, met processor, geheugen, flash en de bussen waaraan de
rest hangt. Dat is de term die de rest van de documentatie ook gebruikt —
`node-matrix.md` zet de zestig boards eronder in één kolom.

Op drie van de vier platformfamilies zit die MCU niet als losse chip op het
bord, maar als onderdeel van een **SoC**: een chip die er geheugen, en
meestal ook een radio, omheen pakt. Het verschil in één regel:

| Term | Wat het aanduidt |
|---|---|
| MCU | De rekenende chip: processor, geheugen, flash, bussen |
| SoC | Een chip die een MCU en meer eromheen in één behuizing combineert |

Elke SoC bevat dus een MCU; niet elke MCU zit in een SoC.

| Familie | Chip | SoC? | Wat er extra in zit |
|---|---|---|---|
| ESP32 | ESP32, ESP32-S3, ESP32-C3, ESP32-C6 | ja | WiFi en BLE |
| nRF52 | nRF52840 | ja | BLE |
| STM32 | STM32WLE5 | ja | De LoRa-radio zelf |
| RP2040 | RP2040 | nee | Kale MCU; alles zit ernaast |

De RP2040 is de enige kale microcontroller in de reeks, en dat verklaart
waarom een RP2040-node geen BLE en geen WiFi heeft: die zitten nergens in.
Zie [MeshCore Platforms](../platform/platforms.md).

De LoRa-transceiver staat hier los van. Ook op een SoC is dat vrijwel
altijd een aparte chip — de SX1262 of SX1276 naast de MCU. De STM32WLE5 is
de uitzondering: daar zit de LoRa-radio wél op dezelfde chip.

## Hoe de firmware de blokken benoemt

De blokken uit het schema zijn geen abstractie achteraf: ze staan letterlijk
in de firmware, als buildvlaggen per bord. Elk ondersteund bord heeft een
eigen map onder `variants/` met een `platformio.ini` die de pinnen
vastlegt. Voor de Heltec WiFi LoRa 32 V3 ziet dat er zo uit:

`variants/heltec_v3/platformio.ini` r.10-24

```ini
  -D P_LORA_DIO_1=14
  -D P_LORA_NSS=8
  -D P_LORA_RESET=RADIOLIB_NC
  -D P_LORA_BUSY=13
  -D P_LORA_SCLK=9
  -D P_LORA_MISO=11
  -D P_LORA_MOSI=10
  -D USE_SX1262
  -D RADIO_CLASS=CustomSX1262
  -D WRAPPER_CLASS=CustomSX1262Wrapper
  -D LORA_TX_POWER=22
  -D P_LORA_TX_LED=35
  -D PIN_BOARD_SDA=17
  -D PIN_BOARD_SCL=18
  -D PIN_USER_BTN=0
```

Daar staat het blokschema in vijftien regels: `SCLK`, `MISO`, `MOSI` en
`NSS` zijn de SPI-bus naar de radio, `BUSY` en `DIO_1` de twee lijnen
waarmee de radio terugpraat, `SDA` en `SCL` de I²C-bus waar het scherm aan
hangt, en `USER_BTN` de enige knop van dit bord. Een bord zonder scherm
mist de `PIN_BOARD_*`-regels eenvoudigweg.

In de C++-kant komt elk blok terug als een abstracte klasse met een
implementatie per chip:

| Blok | Abstractie in de firmware | Waar |
|---|---|---|
| Radio | `RADIO_CLASS` / `WRAPPER_CLASS`, per chip ingevuld | `src/helpers/radiolib/` |
| Verbinding naar buiten | `BaseSerialInterface` | `src/helpers/BaseSerialInterface.h` |
| Scherm | `DisplayDriver` | `src/helpers/ui/DisplayDriver.h` |
| Sensoren en GPS | `SensorManager` | `src/helpers/SensorManager.h` |
| Knop | `MomentaryButton` | `src/helpers/ui/MomentaryButton.h` |

Dat `BaseSerialInterface` één abstractie is voor BLE, WiFi én USB is geen
detail: voor de firmware zijn dat drie implementaties van hetzelfde begrip —
een verbinding waarover frames naar een companion gaan.

## De drie subsecties

De sectie is verdeeld naar wat een onderdeel dóét, niet naar waar het op
het bord ligt:

| Subsectie | Wat erin hoort | Criterium |
|---|---|---|
| `radio/` | transceiver, antenne, linkbudget | alles tussen de firmware en de ether |
| `interfaces/` | BLE, WiFi, USB-serieel, I²C, SPI | een verbinding waarlangs data gaat, niet het apparaat aan het eind |
| `peripherals/` | display, GPS, knoppen en LED's | het apparaat aan het eind van zo'n verbinding |

Het onderscheid tussen de laatste twee vraagt af en toe om uitleg. SPI staat
onder `interfaces/`, de SX1262 die eraan hangt onder `radio/`, en het OLED
dat aan I²C hangt onder `peripherals/`. De bus en wat eraan hangt zijn twee
onderwerpen.

> [!NOTE]
> **Het woord randapparatuur.** Dat woord is in deze documentatie op drie
> plaatsen in gebruik en betekent niet overal hetzelfde. Tabel 3 van
> [Nodematrix](../platform/node-matrix.md) groepeert er display, GPS, WiFi,
> BLE en USB onder — dus inclusief de verbindingen. Het hoofdstuk
> [Randapparatuur](../libraries/other/peripherals.md) gaat over
> libraries voor buzzers, LED's en busexpanders. Hier is het alleen de
> naam van de derde groep hierboven, waar de verbindingen juist níet onder
> vallen. De LoRa-radio valt nergens onder die noemer: die is de reden dat
> een node bestaat, niet iets wat eraan hangt.

## Wat elders staat

Deze sectie beschrijft de onderdelen zelf. Welk bord welk onderdeel heeft,
staat ergens anders, en die tellingen worden hier niet herhaald:

- [MeshCore Platforms](../platform/platforms.md) — waarom de chip bepaalt
  wat het apparaat kan.
- [De vier platformfamilies](../platform/platform-families.md) — wat er per
  familie in de chip zit, en waar BLE of WiFi ontbreekt.
- [Nodematrix](../platform/node-matrix.md) — elk bord met zijn radio,
  scherm, GPS en koppeling naast elkaar.
- [Hardware Overzicht](../gebruik/hardware.md) — vier apparaten uitgebreid
  besproken, met prijzen.
- [Regelgeving & Duty Cycle](../gebruik/regulations.md) — wat je op 868 MHz
  werkelijk mag uitzenden. Duty cycle blijft daar; de radiohoofdstukken
  verwijzen ernaar.
- [Het Lagenmodel van MeshCore](../techniek/layer-model.md) — waar de
  hardware ophoudt en het protocol begint.

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`variants/heltec_v3/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/heltec_v3/platformio.ini)
  — pindefinities van het voorbeeldbord
- [`variants/heltec_v3/target.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/heltec_v3/target.h)
  — welke blokken dat bord instantieert
- [`src/helpers/BaseSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/BaseSerialInterface.h)
  — de gedeelde abstractie voor BLE, WiFi en USB-serieel
- [`src/helpers/ui/DisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/DisplayDriver.h)
  — de abstractie waar alle schermtypes onder vallen
- [`src/helpers/SensorManager.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/SensorManager.h)
  — sensoren en locatiebronnen
