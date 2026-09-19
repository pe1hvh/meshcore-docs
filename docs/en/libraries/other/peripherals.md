# Peripherals

*BUZZER · LED · BUS EXPANDER · ACCELEROMETER*

Four libraries drive whatever else may hang off a MeshCore board: a buzzer, an
addressable LED, a bus expander that solves a shortage of pins, and an
accelerometer. They have little to do with one another, beyond none of them
being part of the measuring or the communication.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini`, `src/helpers/ui/buzzer.cpp`,
> `src/helpers/ui/GxEPDDisplay.cpp`, `variants/thinknode_m5/` and
> `variants/wio_wm1110/platformio.ini`.

## How MeshCore calls this group

All four sit behind an `#ifdef` on a pin constant from the variant file. If
the pin does not exist, the code does not exist:

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

RTTTL is the text format old Nokia phones stored their ringtones in: a name, a
few default settings and then the notes as text. The ordinary Arduino
implementations play such a melody using `delay()`, which stops the firmware
for seconds at a time. NonBlockingRTTTL does it with a state machine that
takes one step per pass through the main loop — so a MeshCore node can play a
melody and keep receiving packets at the same time.

MeshCore wraps it in `genericBuzzer` (`src/helpers/ui/buzzer.h` and `.cpp`),
which starts, interrupts and silences the melody. With seventeen variants this
is the most common library in this group after the display libraries.

## adafruit/Adafruit NeoPixel

NeoPixel is Adafruit's name for addressable LEDs of the WS2812 type and
relatives: one data line, and three or four bytes of colour per LED, with a
protocol accurate to the microsecond. The library handles that timing per
platform.

Declared in three variants, among them `lilygo_techo_card`,
`heltec_mesh_solar` and `nibble_screen_connect`. The library is additionally
brought in by three Adafruit sensor libraries as a dependency for their
example sketches; see [`../dependencies.md`](../dependencies.md).

## maxpromer/PCA9557-arduino

The PCA9557 is an I²C bus expander: one chip on the I²C bus supplies eight
extra inputs and outputs. On boards where the pins have run out, the reset and
select lines of an e-ink display may hang off it, for example.

MeshCore uses it on the ThinkNode M5. The expander is created in the variant
file and used by the display driver:

`src/helpers/ui/GxEPDDisplay.cpp` r.5-6

```cpp
  #include <PCA9557.h>
  extern PCA9557 expander;
```

`variants/thinknode_m5/ThinknodeM5Board.cpp` r.3

```cpp
PCA9557 expander (0x18, &Wire1);
```

Note that the expander hangs off `Wire1`, the board's second I²C bus. This is
the only library in the repo without a version specification in `lib_deps`:
the line reads just `maxpromer/PCA9557-arduino`, so PlatformIO takes whatever
is newest at that moment.

## adafruit/Adafruit LIS3DH

The LIS3DH is a three-axis accelerometer, usable to notice that a device has
been picked up or moved. The library is declared in one variant:

`variants/wio_wm1110/platformio.ini` r.36

```text
  adafruit/Adafruit LIS3DH @ ^1.2.4
```

No include of `Adafruit_LIS3DH` can be found in `src/`, `examples/`,
`variants/` or `arch/`. That observation is described in
[`../dependencies.md`](../dependencies.md); no conclusion is drawn from it
here.

## Overview

| Library | Version | Variants | Board |
|---|---|---|---|
| `end2endzone/NonBlockingRTTTL` | `^1.3.0` | 17 | all boards with `PIN_BUZZER` |
| `adafruit/Adafruit NeoPixel` | `^1.10.0` · `^1.12.3` | 3 | T-Echo Card, Heltec Mesh Solar, Nibble Screen Connect |
| `maxpromer/PCA9557-arduino` | none | 1 | ThinkNode M5 |
| `adafruit/Adafruit LIS3DH` | `^1.2.4` | 1 | Wio WM1110 |

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/ui/buzzer.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/buzzer.cpp)
- [`src/helpers/ui/GxEPDDisplay.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/GxEPDDisplay.cpp)
- [`variants/thinknode_m5/ThinknodeM5Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/thinknode_m5/ThinknodeM5Board.cpp)
- [`variants/wio_wm1110/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/wio_wm1110/platformio.ini)
- [end2endzone/NonBlockingRTTTL](https://github.com/end2endzone/NonBlockingRTTTL)
- [adafruit/Adafruit_NeoPixel](https://github.com/adafruit/Adafruit_NeoPixel)

Translated from Dutch by Anthropic Claude
