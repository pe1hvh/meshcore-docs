# De SPI-bus

*VIER LIJNEN · NSS EN BUSY · DRIE PLATFORMS, DRIE MANIEREN · DIO1*

SPI is de bus waar de radio aan hangt, en dat maakt hem de belangrijkste
van de twee. Elk pakket dat een node verstuurt of ontvangt gaat over deze
vier draden. Dit hoofdstuk beschrijft welke pinnen dat zijn, welke extra
lijnen de SX1262 nodig heeft naast de bus zelf, en waarom de firmware voor
elk platform een andere manier gebruikt om die pinnen in te stellen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestand
> `src/helpers/radiolib/CustomSX1262.h` en de `P_LORA_`-vlaggen in
> `variants/`.

![Schema van de SPI-verbinding tussen SoC en radio: SCLK, MOSI, MISO en NSS
als bus, met BUSY, RESET en DIO1 als losse
stuurlijnen](../../../images/nl/spi-1.svg)

## Vier lijnen voor de bus, drie ernaast

SPI zelf is vier draden. De SX1262 heeft er nog drie nodig die geen deel van
de bus zijn:

| Vlag | Lijn | Rol |
|---|---|---|
| `P_LORA_SCLK` | `SCLK` | klok, door de SoC gestuurd |
| `P_LORA_MOSI` | `MOSI` | SoC → radio |
| `P_LORA_MISO` | `MISO` | radio → SoC |
| `P_LORA_NSS` | `NSS` | chipselect, actief laag |
| `P_LORA_BUSY` | — | radio is bezig, geen opdrachten sturen |
| `P_LORA_RESET` | — | harde reset van de chip |
| `P_LORA_DIO_1` | — | interrupt: pakket klaar of ontvangen |

De laatste drie zijn de reden dat een SX1262 niet zomaar op een willekeurige
SPI-bus te hangen is. `BUSY` moet gelezen kunnen worden vóór elke opdracht,
en `DIO1` moet op een pin zitten die een interrupt kan geven — anders moet
de firmware pollen en mist hij pakketten.

`variants/lilygo_tbeam_1w/platformio.ini` r.12-19

```ini
  -D RADIO_CLASS=CustomSX1262
  -D WRAPPER_CLASS=CustomSX1262Wrapper
  -D P_LORA_DIO_1=1
  -D P_LORA_NSS=15
  -D P_LORA_RESET=3
  -D P_LORA_BUSY=38
  -D P_LORA_SCLK=13
  -D P_LORA_MISO=12
  -D P_LORA_MOSI=11
```

Over alle variantmappen samen, uitgecommentarieerde regels niet meegeteld,
komt `P_LORA_DIO_1` het vaakst voor (241 regels) en `P_LORA_MOSI` het minst
(93). Dat verschil is geen inconsistentie: borden waar de radio in de SoC zit
of op een vaste SPI-bus hangt hoeven de drie busleidingen niet te benoemen,
maar hebben altijd een interruptpin nodig.

## Drie platforms, drie manieren

Hier zit de eigenaardigheid van dit hoofdstuk. Het instellen van de
SPI-pinnen gebeurt per platform anders, en dat verschil komt niet uit
MeshCore maar uit de Arduino-cores eronder:

`src/helpers/radiolib/CustomSX1262.h` r.30-44

```cpp
  #if defined(P_LORA_SCLK)
    #ifdef NRF52_PLATFORM
      if (spi) { spi->setPins(P_LORA_MISO, P_LORA_SCLK, P_LORA_MOSI); spi->begin(); }
    #elif defined(RP2040_PLATFORM)
      if (spi) {
        spi->setMISO(P_LORA_MISO);
        //spi->setCS(P_LORA_NSS); // Setting CS results in freeze
        spi->setSCK(P_LORA_SCLK);
        spi->setMOSI(P_LORA_MOSI);
        spi->begin();
      }
    #else
      if (spi) spi->begin(P_LORA_SCLK, P_LORA_MISO, P_LORA_MOSI);
    #endif
  #endif
```

| Platform | Manier |
|---|---|
| nRF52 | één `setPins()` met drie argumenten, daarna `begin()` |
| RP2040 | drie losse setters, daarna `begin()` |
| overige (ESP32) | `begin()` met de drie pinnen als argument |

Alledrie doen hetzelfde en geen van drieën is uitwisselbaar. De volgorde van
de argumenten verschilt bovendien: bij nRF52 is het MISO, SCLK, MOSI; bij
ESP32 is het SCLK, MISO, MOSI. Een pin die op de verkeerde plaats staat
levert geen foutmelding op maar een radio die niet reageert.

> [!NOTE]
> De uitgecommentarieerde regel bij RP2040 is geen restant maar een
> waarschuwing met een reden erbij: `setCS()` aanroepen laat het bord
> vastlopen. De chipselect wordt daar dus door RadioLib zelf gestuurd via
> `P_LORA_NSS`, niet door de SPI-klasse.

Het hele blok staat achter `#if defined(P_LORA_SCLK)`. Zet een variant die
vlag niet, dan gebeurt er niets en gebruikt de SPI-klasse de
standaardpinnen van het bord. Dat is het normale geval op borden waar de
radio aan de hardwarematige SPI-poort hangt.

## Wat er nog meer aan hangt

SPI is niet exclusief voor de radio. Op borden met een e-paperscherm of een
SD-kaart delen die dezelfde bus, elk met een eigen chipselect. Dat werkt
zolang precies één `NSS` tegelijk laag is. Welke borden een SPI-scherm
hebben staat in [Het scherm](../peripherals/display.md).

De radio is daarbij de veeleisendste gebruiker: hij wil op tijd bediend
worden als `DIO1` afgaat. Een langdurige schermverversing over dezelfde bus
kan leiden tot pakketverlies.

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`src/helpers/radiolib/CustomSX1262.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/radiolib/CustomSX1262.h)
  — de drie platformafhankelijke manieren om de SPI-pinnen te zetten
- [`variants/lilygo_tbeam_1w/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/lilygo_tbeam_1w/platformio.ini)
  — de `P_LORA_`-pinnen van één bord

Verwante hoofdstukken:

- [De LoRa-transceiver](../radio/sx1262.md) — wat er aan het andere eind van
  de bus zit
- [De I²C-bus](i2c.md) — de langzame bus ernaast
- [Wire en SPI](../../libraries/core/wire-spi.md) — waarom dit
  frameworklibraries zijn en geen pakketten
- [Het scherm](../peripherals/display.md) — de andere gebruiker van deze bus
- [De vier platformfamilies](../../platform/platform-families.md) — waar het
  platformverschil vandaan komt
