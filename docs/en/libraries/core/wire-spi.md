# Wire and SPI

*FRAMEWORK LIBRARY · I²C · BUS INSTANCE · FOUR IMPLEMENTATIONS*

`Wire` and `SPI` are the two buses that nearly everything in a MeshCore node
hangs off. They sit at the top of `[arduino_base]`, without an author prefix
and without a version number, because they do not come from the registry but
from the platform's framework package.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini`, `src/helpers/ESP32Board.h`,
> `src/helpers/ui/ST7789LCDDisplay.cpp` and `src/helpers/ui/GxEPDDisplay.cpp`.

## What it does

`Wire` is the Arduino API for I²C: a two-wire bus that can carry dozens of
devices, each with its own address. `SPI` is the API for the bus of the same
name: faster, with four wires, and with a separate select line per device.

Neither is a library in the ordinary sense. They belong to the platform's
Arduino core, so there is one of each per platform: Arduino-ESP32 on ESP32,
the Adafruit nRF52 core on nRF52, arduino-pico on RP2040 and STM32duino on
STM32. The API is the same, the behaviour underneath is not — in the number of
available bus instances, in the free choice of pins and in the timing.

## How MeshCore pulls it in

`platformio.ini` r.19-21

```text
lib_deps =
  SPI
  Wire
```

Two lines in `[arduino_base]`, without a prefix and without an `@` version.
They apply to all 507 build targets. For the STM32WL a third framework library
joins them, `SubGhz` — see [`subghz.md`](subghz.md).

## How MeshCore uses it

**SPI carries the radio.** On every platform except STM32WL the transceiver
sits on the SPI bus; the variant files define `P_LORA_MISO`, `P_LORA_MOSI`,
`P_LORA_SCLK` and `P_LORA_NSS` for it. RadioLib does the rest — see
[`radiolib.md`](radiolib.md).

Larger displays do not always share that bus. Where it clashes, a second bus
instance is created:

`src/helpers/ui/GxEPDDisplay.cpp` r.13-15

```cpp
#ifdef ESP32
  SPIClass SPI1 = SPIClass(FSPI);
#endif
```

And for a TFT display on some boards the bus is started with explicit pins:

`src/helpers/ui/ST7789LCDDisplay.cpp` r.31-34

```cpp
    // Im not sure if this is just a t-deck problem or not, if your display is slow try this.
    #if defined(LILYGO_TDECK) || defined(HELTEC_LORA_V4_TFT)
      displaySPI.begin(PIN_TFT_SCL, -1, PIN_TFT_SDA, PIN_TFT_CS);
    #endif
```

**Wire carries the rest.** Sensors, clock chips, current meters, bus expanders
and the smaller OLED displays all sit on I²C. The board decides on which pins:

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

That the pins can be passed in here is an ESP32 property: on that platform the
I²C controller can be mapped freely onto pins. On the other platforms they are
fixed.

The text `Wire` occurs in 149 of the 590 source files, `SPI` in 83.

## What it means for a node

Nearly every problem with a sensor that is not found, or a display that stays
black, comes back to one of these two buses: wrong pins in the variant file,
two devices on the same I²C address, or a display pushing the radio off the
SPI bus.

The STM32WL is the exception as far as the radio is concerned: there is no
external SPI connection to the transceiver there, because it sits on the same
chip. It does use Wire, for whatever else hangs off the board.

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/ESP32Board.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ESP32Board.h)
- [`src/helpers/ui/GxEPDDisplay.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/GxEPDDisplay.cpp)
- [`src/helpers/ui/ST7789LCDDisplay.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/ST7789LCDDisplay.cpp)
- [Arduino — Wire](https://docs.arduino.cc/language-reference/en/functions/communication/wire/)
- [Arduino — SPI](https://docs.arduino.cc/language-reference/en/functions/communication/SPI/)

Translated from Dutch by Anthropic Claude
