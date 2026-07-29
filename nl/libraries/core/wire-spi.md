# Wire en SPI

*FRAMEWORKLIBRARY · I²C · BUSINSTANTIE · VIER IMPLEMENTATIES*

`Wire` en `SPI` zijn de twee bussen waar in een MeshCore-node vrijwel alles
aan hangt. Ze staan bovenaan in `[arduino_base]`, zonder auteursprefix en
zonder versienummer, want ze komen niet uit de registry maar uit het
frameworkpakket van het platform.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, `src/helpers/ESP32Board.h`,
> `src/helpers/ui/ST7789LCDDisplay.cpp` en `src/helpers/ui/GxEPDDisplay.cpp`.

## Wat het doet

`Wire` is de Arduino-API voor I²C: een bus met twee draden waar tientallen
apparaten met elk een eigen adres aan kunnen hangen. `SPI` is de API voor de
gelijknamige bus: sneller, met vier draden, en met per apparaat een eigen
selectielijn.

Geen van beide is een library in de gewone zin. Ze horen bij de Arduino-core
van het platform, en er is er dus één per platform: Arduino-ESP32 op ESP32,
de Adafruit nRF52-core op nRF52, arduino-pico op RP2040 en STM32duino op
STM32. De API is gelijk, het gedrag eronder verschilt — bij het aantal
beschikbare businstanties, bij de vrije keuze van pennen en bij de timing.

## Hoe MeshCore hem binnenhaalt

`platformio.ini` r.19-21

```text
lib_deps =
  SPI
  Wire
```

Twee regels in `[arduino_base]`, zonder prefix en zonder `@`-versie. Ze
gelden voor alle 507 build-targets. Voor de STM32WL komt er nog een derde
frameworklibrary bij, `SubGhz` — zie [`subghz.md`](subghz.md).

## Hoe MeshCore hem gebruikt

**SPI draagt de radio.** Op elk platform behalve STM32WL zit de transceiver
aan de SPI-bus; de variantbestanden definiëren daarvoor `P_LORA_MISO`,
`P_LORA_MOSI`, `P_LORA_SCLK` en `P_LORA_NSS`. RadioLib doet de rest — zie
[`radiolib.md`](radiolib.md).

Grotere schermen delen die bus niet altijd. Waar dat botst, wordt er een
tweede businstantie aangemaakt:

`src/helpers/ui/GxEPDDisplay.cpp` r.13-15

```cpp
#ifdef ESP32
  SPIClass SPI1 = SPIClass(FSPI);
#endif
```

En bij een TFT-scherm op sommige borden wordt de bus met expliciete pennen
opgestart:

`src/helpers/ui/ST7789LCDDisplay.cpp` r.31-34

```cpp
    // Im not sure if this is just a t-deck problem or not, if your display is slow try this.
    #if defined(LILYGO_TDECK) || defined(HELTEC_LORA_V4_TFT)
      displaySPI.begin(PIN_TFT_SCL, -1, PIN_TFT_SDA, PIN_TFT_CS);
    #endif
```

**Wire draagt de rest.** Sensoren, klokchips, stroommeters, busexpanders en
de kleinere OLED-schermen zitten allemaal op I²C. Het bord bepaalt op welke
pennen:

`src/helpers/ESP32Board.h` r.44-50

```cpp
  #if defined(PIN_BOARD_SDA) && defined(PIN_BOARD_SCL)
   #if PIN_BOARD_SDA >= 0 && PIN_BOARD_SCL >= 0
    Wire.begin(PIN_BOARD_SDA, PIN_BOARD_SCL);
   #endif
  #else
    Wire.begin();
  #endif    
```

Dat de pennen hier meegegeven kunnen worden, is een ESP32-eigenschap: op dat
platform is de I²C-controller vrij op pennen te leggen. Op de andere
platformen liggen ze vast.

De tekst `Wire` komt voor in 149 van de 590 bronbestanden, `SPI` in 83.

## Wat het voor een node betekent

Vrijwel elk probleem met een sensor die niet gevonden wordt, of een scherm
dat zwart blijft, komt op een van deze twee bussen uit: verkeerde pennen in
het variantbestand, twee apparaten op hetzelfde I²C-adres, of een scherm dat
de radio van de SPI-bus duwt.

De STM32WL is de uitzondering waar het de radio betreft: daar is geen externe
SPI-verbinding naar de transceiver, omdat die op dezelfde chip zit. Wire
gebruikt hij wel, voor wat er verder aan het bord hangt.

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/ESP32Board.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ESP32Board.h)
- [`src/helpers/ui/GxEPDDisplay.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/GxEPDDisplay.cpp)
- [`src/helpers/ui/ST7789LCDDisplay.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/ST7789LCDDisplay.cpp)
- [Arduino — Wire](https://docs.arduino.cc/language-reference/en/functions/communication/wire/)
- [Arduino — SPI](https://docs.arduino.cc/language-reference/en/functions/communication/SPI/)
