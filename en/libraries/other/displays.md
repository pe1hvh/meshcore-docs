# Display libraries

*DISPLAY_CLASS · OLED · E-INK · TFT · ABSTRACTION*

MeshCore knows eleven values for `DISPLAY_CLASS`, from an OLED a couple of
centimetres across to an e-ink panel and a colour TFT. Almost none of that
shows in the firmware: all displays sit behind a single interface, and which
library actually gets compiled in is decided by one build flag per variant.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini`, the seventy-nine `variants/*/platformio.ini`,
> `src/helpers/ui/DisplayDriver.h`, `src/helpers/ui/SSD1306Display.h` and
> `examples/simple_repeater/main.cpp`.

## How MeshCore calls this group

The abstraction is called `DisplayDriver`. Every display driver inherits from
it and implements the same methods:

`src/helpers/ui/DisplayDriver.h` r.6-24

```cpp
class DisplayDriver {
  int _w, _h;
protected:
  DisplayDriver(int w, int h) { _w = w; _h = h; }
public:
  enum Color { DARK=0, LIGHT, RED, GREEN, BLUE, YELLOW, ORANGE }; // on b/w screen, colors will be !=0 synonym of light

  int width() const { return _w; }
  int height() const { return _h; }

  virtual bool isOn() = 0;
  virtual bool isEink() { return false; } // default to non-eink, override in eink drivers
  virtual void turnOn() = 0;
  virtual void turnOff() = 0;
  virtual void clear() = 0;
  virtual void startFrame(Color bkg = DARK) = 0;
```

Which implementation it becomes is stated by the variant with
`-D DISPLAY_CLASS=…`. The sketches know only that name:

`examples/simple_repeater/main.cpp` r.42-46

```cpp
#ifdef DISPLAY_CLASS
  if (display.begin()) {
    display.startFrame();
    display.setCursor(0, 0);
    display.print("Please wait...");
```

If `DISPLAY_CLASS` is not defined, all display code disappears from the build.
There is also a `NullDisplayDriver` for boards that run the UI task but have
no screen.

![The DISPLAY_CLASS abstraction in MeshCore: every variant picks a display
driver with a single build flag, all drivers inherit from the same
DisplayDriver interface, and behind that sit the individual display libraries
from Adafruit, GxEPD2, U8g2 and LovyanGFX](../../../images/en/displays-1.svg)

## Adafruit SSD1306

The SSD1306 is the controller of the small monochrome OLED panels of 128 × 64
or 128 × 32 pixels found on most MeshCore boards. Adafruit's library talks to
it over I²C or SPI and keeps a full framebuffer in RAM. With twenty-three
variants this is the most common display library in the repo, and
`SSD1306Display` is by far the most common `DISPLAY_CLASS`. The driver sets
`SSD1306_NO_SPLASH` before the include, so the Adafruit logo does not appear
at start-up.

## Adafruit SH110X

The SH1106 and SH1107 are OLED controllers that closely resemble the SSD1306
but have a slightly different memory layout — drive a panel with one of these
as an SSD1306 and the image comes out shifted by a few pixels. The library
supports both types. In seven variants: `lilygo_tbeam_1w`,
`lilygo_tbeam_supreme_SX1262`, `nano_g2_ultra`, `station_g2`,
`station_g3_esp32`, `thinknode_m2` and `wio-tracker-l1`, with `SH1106Display`
as the driver.

## zinggjm/GxEPD2

GxEPD2 is the standard e-ink library on Arduino: it knows dozens of panel
types, each with its own initialisation sequence and refresh behaviour, and
offers both full and partial refresh. Five variants use it — `lilygo_techo`,
`lilygo_techo_lite`, `mesh_pocket`, `thinknode_m1` and `thinknode_m5` —
through `GxEPDDisplay`. The sixth e-ink variant, `wio-tracker-l1-eink`,
fetches a fork: `https://github.com/SoulOfNoob/GxEPD2.git`, with no revision
after the URL.

## Adafruit GFX Library

GFX is not a display driver but the drawing layer underneath: lines,
rectangles, text, fonts and bitmaps, all in a framebuffer a driver then writes
to the screen. SSD1306, SH110X, ST7735/ST7789 and Adafruit EPD all four need
it and declare it in their own `depends=`. In eight variants it is
*additionally* declared explicitly in `lib_deps` — see
[`../dependencies.md`](../dependencies.md), where that is described as
deliberate version control across the chain.

## Adafruit BusIO

BusIO is Adafruit's shared bus access layer: one API for a register on an I²C
or SPI device, so the driver libraries do not have to concern themselves with
the bus. Nearly every Adafruit library brings it in through `depends=`. In
exactly one variant it is declared explicitly,
`sensecap_indicator-espnow`.

## Adafruit ST7735 and ST7789 Library

ST7735 and ST7789 are controllers for small colour TFT panels. The library
supports both and works on top of GFX. Six variants use it: `heltec_t096`,
`heltec_t1`, `heltec_tracker`, `heltec_tracker_v2`, `heltec_v4` and
`lilygo_tdeck`, with `ST7735Display`, `ST7789Display` or `ST7789LCDDisplay` as
the driver. This library drags in two libraries named nowhere else —
`Adafruit seesaw Library` and `SD` — because its examples need them.

## Adafruit EPD

Adafruit EPD is Adafruit's e-ink library, supporting their own panels and
breakouts. It is declared in one variant, `mesh_pocket`, pinned exactly to
4.6.1. No include of `Adafruit_EPD` can be found anywhere in the source; that
observation is described in [`../dependencies.md`](../dependencies.md).

## olikraus/U8g2

U8g2 is a monochrome graphics library supporting a large number of display
controllers, with a font system of its own and the option to work without a
full framebuffer — usable on boards with little RAM. One variant uses it,
`lilygo_techo_card`, through `U8g2Display`.

## lovyan03/LovyanGFX

LovyanGFX is a graphics library for colour displays that uses DMA on ESP32 and
is therefore fast on large panels. One variant uses it,
`sensecap_indicator-espnow`, through `LGFXDisplay`.

## heltec-eink-modules

For Heltec's e-ink modules, two different forks of the same library are
fetched, both as a zip of a full commit hash:

| Fork | Commit | Variants |
|---|---|---|
| `Quency-D/heltec-eink-modules` | `563dd41` | `heltec_e213`, `heltec_e290` |
| `todd-herbert/heltec-eink-modules` | `9207eb6` | `heltec_wireless_paper` |

The accompanying drivers are `E213Display` and `E290Display`; both include
`heltec-eink-modules.h` and use `CRC32` to decide whether the screen needs
refreshing at all — see [`utilities.md`](utilities.md).

## Overview

| Library | Version | Variants | Driver |
|---|---|---|---|
| `adafruit/Adafruit SSD1306` | `^2.5.13` | 23 | `SSD1306Display` |
| `adafruit/Adafruit SH110X` | `^2.1.13` · `~2.1.13` | 7 | `SH1106Display` |
| `adafruit/Adafruit GFX Library` | `^1.12.1` | 8 | drawing layer |
| `adafruit/Adafruit BusIO` | `^1.17.2` | 1 | bus access |
| `adafruit/Adafruit ST7735 and ST7789 Library` | `^1.11.0` | 6 | `ST7735Display`, `ST7789Display`, `ST7789LCDDisplay` |
| `adafruit/Adafruit EPD` | `4.6.1` | 1 | no include found |
| `zinggjm/GxEPD2` | `1.6.2` | 5 | `GxEPDDisplay` |
| `SoulOfNoob/GxEPD2` | no revision | 1 | `GxEPDDisplay` |
| `Quency-D/heltec-eink-modules` | `563dd41` | 2 | `E213Display`, `E290Display` |
| `todd-herbert/heltec-eink-modules` | `9207eb6` | 1 | `E290Display` |
| `olikraus/U8g2` | `^2.35.19` | 1 | `U8g2Display` |
| `lovyan03/LovyanGFX` | `^1.2.7` | 1 | `LGFXDisplay` |

## Sources

- [`src/helpers/ui/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/src/helpers/ui)
- [`src/helpers/ui/DisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/DisplayDriver.h)
- [`src/helpers/ui/SSD1306Display.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/SSD1306Display.h)
- [`examples/simple_repeater/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/main.cpp)
- [adafruit/Adafruit_SSD1306](https://github.com/adafruit/Adafruit_SSD1306)
- [ZinggJM/GxEPD2](https://github.com/ZinggJM/GxEPD2)
- [olikraus/U8g2_Arduino](https://github.com/olikraus/U8g2_Arduino)
- [lovyan03/LovyanGFX](https://github.com/lovyan03/LovyanGFX)

Translated from Dutch by Anthropic Claude
