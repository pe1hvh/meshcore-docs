# Randapparatuur

*BUZZER · LED · BUSEXPANDER · VERSNELLINGSMETER*

Vier libraries bedienen wat er verder nog aan een MeshCore-bord kan hangen:
een zoemer, een adresseerbare LED, een busexpander die tekort aan pennen
oplost, en een versnellingsmeter. Ze hebben weinig met elkaar te maken,
behalve dat ze geen van alle in de meting of de communicatie zitten.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, `src/helpers/ui/buzzer.cpp`,
> `src/helpers/ui/GxEPDDisplay.cpp`, `variants/thinknode_m5/` en
> `variants/wio_wm1110/platformio.ini`.

## Hoe MeshCore deze groep aanroept

Alle vier zitten achter een `#ifdef` op een penconstante uit het
variantbestand. Bestaat de pen niet, dan bestaat de code niet:

`src/helpers/ui/buzzer.cpp` r.1-16

```cpp
#include "Arduino.h"
#ifdef PIN_BUZZER
#include "buzzer.h"

void genericBuzzer::begin() {
//    Serial.print("DBG: Setting up buzzer on pin ");
//    Serial.println(PIN_BUZZER);
    #ifdef PIN_BUZZER_EN
      pinMode(PIN_BUZZER_EN, OUTPUT);
      digitalWrite(PIN_BUZZER_EN, HIGH);
    #endif

    quiet(false);
    pinMode(PIN_BUZZER, OUTPUT);
    digitalWrite(PIN_BUZZER, LOW); // need to pull low by default to avoid extreme power draw
}
```

## end2endzone/NonBlockingRTTTL

RTTTL is het tekstformaat waarin oude Nokia-telefoons hun beltonen bewaarden:
een naam, een paar standaardinstellingen en dan de noten als tekst. De
gewone Arduino-implementaties spelen zo'n melodie af met `delay()`, wat de
firmware seconden stilzet. NonBlockingRTTTL doet het met een toestandsmachine
die bij elke doorloop van de hoofdlus één stap zet — een MeshCore-node kan
dus een melodie spelen en tegelijk pakketten blijven ontvangen.

MeshCore verpakt hem in `genericBuzzer` (`src/helpers/ui/buzzer.h` en
`.cpp`), die de melodie start, onderbreekt en stilzet. Met zeventien
varianten is dit na de displaylibraries de meest voorkomende library in deze
groep.

## adafruit/Adafruit NeoPixel

NeoPixel is de Adafruit-naam voor adresseerbare LED's van het type WS2812 en
verwant: één datalijn, en per LED drie of vier bytes kleur, met een
protocol dat op de microseconde nauw luistert. De library regelt die timing
per platform.

In drie varianten gedeclareerd, waaronder `lilygo_techo_card`,
`heltec_mesh_solar` en `nibble_screen_connect`. De library wordt daarnaast
door drie Adafruit-sensorlibraries als afhankelijkheid meegebracht voor hun
voorbeeldschetsen; zie [`../dependencies.md`](../dependencies.md).

## maxpromer/PCA9557-arduino

De PCA9557 is een I²C-busexpander: één chip aan de I²C-bus levert acht extra
in- en uitgangen. Op borden waar de pennen op zijn, hangen daar bijvoorbeeld
de reset- en selectielijnen van een e-inkscherm aan.

MeshCore gebruikt hem op de ThinkNode M5. De expander wordt in het
variantbestand aangemaakt en door de schermdriver gebruikt:

`src/helpers/ui/GxEPDDisplay.cpp` r.5-6

```cpp
  #include <PCA9557.h>
  extern PCA9557 expander;
```

`variants/thinknode_m5/ThinknodeM5Board.cpp` r.3

```cpp
PCA9557 expander (0x18, &Wire1);
```

Merk op dat de expander aan `Wire1` hangt, de tweede I²C-bus van het bord.
De library staat als enige in de repo zonder versieaanduiding in `lib_deps`:
er staat alleen `maxpromer/PCA9557-arduino`, dus PlatformIO pakt wat er op
dat moment de nieuwste is.

## adafruit/Adafruit LIS3DH

De LIS3DH is een versnellingsmeter met drie assen, bruikbaar om te merken dat
een apparaat opgepakt of bewogen wordt. De library wordt in één variant
gedeclareerd:

`variants/wio_wm1110/platformio.ini` r.36

```text
  adafruit/Adafruit LIS3DH @ ^1.2.4
```

In `src/`, `examples/`, `variants/` en `arch/` is geen enkele include van
`Adafruit_LIS3DH` te vinden. Die waarneming staat beschreven in
[`../dependencies.md`](../dependencies.md); er wordt hier geen conclusie aan
verbonden.

## Overzicht

| Library | Versie | Varianten | Bord |
|---|---|---|---|
| `end2endzone/NonBlockingRTTTL` | `^1.3.0` | 17 | alle borden met `PIN_BUZZER` |
| `adafruit/Adafruit NeoPixel` | `^1.10.0` · `^1.12.3` | 3 | T-Echo Card, Heltec Mesh Solar, Nibble Screen Connect |
| `maxpromer/PCA9557-arduino` | geen | 1 | ThinkNode M5 |
| `adafruit/Adafruit LIS3DH` | `^1.2.4` | 1 | Wio WM1110 |

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/ui/buzzer.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/buzzer.cpp)
- [`src/helpers/ui/GxEPDDisplay.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/GxEPDDisplay.cpp)
- [`variants/thinknode_m5/ThinknodeM5Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/thinknode_m5/ThinknodeM5Board.cpp)
- [`variants/wio_wm1110/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/wio_wm1110/platformio.ini)
- [end2endzone/NonBlockingRTTTL](https://github.com/end2endzone/NonBlockingRTTTL)
- [adafruit/Adafruit_NeoPixel](https://github.com/adafruit/Adafruit_NeoPixel)
