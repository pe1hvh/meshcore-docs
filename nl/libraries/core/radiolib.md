# RadioLib

*TRANSCEIVER · GODMODE · EXCLUDE · WRAPPER*

RadioLib is de laag tussen MeshCore en de radiochip. Zes verschillende
transceivers worden erdoor bediend, elk met een eigen wrapper in
`src/helpers/radiolib/`. MeshCore gebruikt de library niet zoals bedoeld: met
`RADIOLIB_GODMODE` worden de interne registers opengezet, en veertien
protocollen worden er bij het compileren uitgesloopt.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini` en de zestien bestanden in `src/helpers/radiolib/`.

## Wat het doet

RadioLib van Jan Gromeš is een Arduino-library voor draadloze modules. Hij
ondersteunt tientallen chips en een reeks protocollen — LoRa, FSK, maar ook
AX.25, APRS, morse, RTTY en SSTV — achter één interface. Voor elke
ondersteunde transceiver is er een klasse die de SPI-commando's, het
registermodel en de timing van die specifieke chip afhandelt. De
documentatie staat op [github.com/jgromes/RadioLib](https://github.com/jgromes/RadioLib)
en de API is uitgebreid gedocumenteerd in de wiki van die repo.

## Hoe MeshCore hem binnenhaalt

`platformio.ini` r.22

```text
  jgromes/RadioLib @ ^7.6.0
```

De regel staat in `[arduino_base]`, dus RadioLib zit in alle 507
build-targets. Het versiebereik is open naar boven binnen de 7.x-reeks.

Twee bouwvlaggen sturen hoe de library zich gedraagt:

`platformio.ini` r.27

```text
build_flags = -w -DNDEBUG -DRADIOLIB_STATIC_ONLY=1 -DRADIOLIB_GODMODE=1
```

`RADIOLIB_STATIC_ONLY` verbiedt dynamische allocatie in de library.
`RADIOLIB_GODMODE` maakt alle `private`- en `protected`-leden publiek. Dat
laatste is geen debugoptie die is blijven staan: MeshCore heeft hem nodig,
zoals hieronder blijkt.

Daarna worden veertien protocollen uitgeschakeld:

`platformio.ini` r.34-47

```text
  -D RADIOLIB_EXCLUDE_CC1101=1
  -D RADIOLIB_EXCLUDE_RF69=1
  -D RADIOLIB_EXCLUDE_SX1231=1
  -D RADIOLIB_EXCLUDE_SI443X=1
  -D RADIOLIB_EXCLUDE_RFM2X=1
  -D RADIOLIB_EXCLUDE_SX128X=1
  -D RADIOLIB_EXCLUDE_AFSK=1
  -D RADIOLIB_EXCLUDE_AX25=1
  -D RADIOLIB_EXCLUDE_HELLSCHREIBER=1
  -D RADIOLIB_EXCLUDE_MORSE=1
  -D RADIOLIB_EXCLUDE_APRS=1
  -D RADIOLIB_EXCLUDE_BELL=1
  -D RADIOLIB_EXCLUDE_RTTY=1
  -D RADIOLIB_EXCLUDE_SSTV=1
```

Zes daarvan sluiten chipfamilies uit die MeshCore niet gebruikt, acht sluiten
protocollen uit die de library bovenop de radio aanbiedt.

## Hoe MeshCore hem gebruikt

In `src/helpers/radiolib/` staan zestien bestanden. Zes daarvan zijn paren
van een `Custom*`-klasse en een `Custom*Wrapper`: LLCC68, LR1110, STM32WLx,
SX1262, SX1268 en SX1276. De `Custom*`-klasse erft van de RadioLib-klasse en
voegt toe wat MeshCore mist; de wrapper zet dat om naar de generieke
radio-interface van de mesh-laag.

`src/helpers/radiolib/CustomSTM32WLx.h` r.8-17

```cpp
class CustomSTM32WLx : public STM32WLx {
  public:
    CustomSTM32WLx(STM32WLx_Module *mod) : STM32WLx(mod) { }

    bool isReceiving() {
      uint16_t irq = getIrqFlags();
      bool detected = (irq & SX126X_IRQ_HEADER_VALID) || (irq & SX126X_IRQ_PREAMBLE_DETECTED);
      return detected;
    }
};
```

Waar GODMODE voor nodig is, laat `SX126xReset.h` zien. Om een SX126x-chip
opnieuw te kalibreren praat MeshCore rechtstreeks tegen de modulelaag van
RadioLib — `mod` en `hal` zijn in de library zelf niet publiek:

`src/helpers/radiolib/SX126xReset.h` r.13-19

```cpp
  radio->mod->SPIwriteStream(RADIOLIB_SX126X_CMD_CALIBRATE, &calData, 1, true, false);
  radio->mod->hal->delay(5);
  uint32_t start = millis();
  while (radio->mod->hal->digitalRead(radio->mod->getGpio())) {
    if (millis() - start > 50) break;
    radio->mod->hal->yield();
  }
```

De tekst `RadioLib` komt voor in 94 van de 590 bronbestanden van de repo —
verreweg het meest van alle libraries. Het leeuwendeel daarvan zijn
`variants/`-bestanden die een `RADIO_CLASS` kiezen.

![Van de MeshCore-wrapperklassen via RadioLib naar de transceiver: zes
Custom-wrapperparen bedienen LLCC68, LR1110, SX1262, SX1268 en SX1276 over de
SPI-bus, terwijl de STM32WLx als aparte tak op dezelfde chip zit als de
processor](../../../images/nl/radiolib-1.svg)

## Wat het voor een node betekent

De keuze van de radiochip is een compileerkeuze, geen instelling. Een
variant zet `RADIO_CLASS` op de juiste `Custom*`-klasse en daarmee ligt vast
welke transceiver de firmware kan aansturen. Wie een bord flasht met de
verkeerde variant, krijgt firmware die de radio niet vindt.

De uitgesloten protocollen zijn er niet: een MeshCore-node kan geen APRS of
morse verzenden, ook al kan de library dat in principe wel.

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/radiolib/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/src/helpers/radiolib)
- [`src/helpers/radiolib/SX126xReset.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/radiolib/SX126xReset.h)
- [`src/helpers/radiolib/CustomSTM32WLx.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/radiolib/CustomSTM32WLx.h)
- [jgromes/RadioLib](https://github.com/jgromes/RadioLib)
