# The Display

*DISPLAYDRIVER · TWELVE CLASSES · UICOLOR · SCALING · CP437*

A node does not need a screen, and many nodes have none. If one is fitted,
the firmware never talks to it directly: everything runs through a single
abstract class with twelve implementations under it. This chapter describes
that abstraction, what happens when there is no screen, why accented
characters show up as blocks on an OLED, and why one of the twelve drivers
stretches the image while the other eleven do not.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.17.1, commit `d929643`, 14 August 2026 — files
> `src/helpers/ui/DisplayDriver.h`, `src/helpers/ui/NullDisplayDriver.h`,
> `src/helpers/ui/SSD1306Display.cpp`, `src/helpers/ui/NV3001BDisplay.h`,
> `src/helpers/ui/NV3001BDisplay.cpp`, `src/helpers/RefCountedDigitalPin.h`
> and the `DISPLAY_CLASS` flags in `variants/`.

## One class, twelve implementations

The firmware knows the notion *screen* only as `DisplayDriver`: an abstract
class with fourteen methods every driver has to implement, plus a handful of
helper methods falling back on those fourteen. Which driver is compiled in
sits in one build flag per board, `DISPLAY_CLASS`.

![The display abstraction: DisplayDriver with twelve implementations under
it, split across OLED on the I²C bus, TFT and e-paper on SPI, and an empty
implementation for boards without a screen](../../../images/en/display-1.svg)

Counted across `variants/`, 205 uncommented `-D DISPLAY_CLASS=` lines
spread over 65 files:

| Driver | Lines | What it is |
|---|---|---|
| `SSD1306Display` | 110 | the small OLED, on I²C |
| `NullDisplayDriver` | 26 | no screen |
| `ST7789LCDDisplay` | 14 | larger colour TFT |
| `ST7735Display` | 14 | small colour TFT, on SPI |
| `SH1106Display` | 13 | OLED with a slightly different controller |
| `E213Display` | 10 | e-paper 2.13 inch |
| `GxEPDDisplay` | 7 | generic e-paper |
| `E290Display` | 5 | e-paper 2.9 inch |
| `ST7789Display` | 3 | same controller, different driving |
| `U8g2Display` | 1 | generic monochrome driver |
| `SCIndicatorDisplay` | 1 | board-specific, inherits from `LGFXDisplay` |
| `NV3001BDisplay` | 1 | colour LCD that scales up the UI coordinates |

Repeat with:

```bash
grep -rh -- "-D DISPLAY_CLASS=" variants/ | grep -v "^\s*;" \
  | sed 's/.*DISPLAY_CLASS=//' | tr -d ' \r' | sort | uniq -c | sort -rn
```

Which specific board has which screen is in the
[Node Matrix](../../platform/node-matrix.md) and is not repeated here. How
the screen physically hangs off the SoC is in
[The I²C Bus](../interfaces/i2c.md) and [The SPI Bus](../interfaces/spi.md).

## No screen is also a screen

Twenty-six build targets set `DISPLAY_CLASS=NullDisplayDriver`. That is not a
missing flag but an explicit choice: a complete implementation that does
nothing.

`src/helpers/ui/NullDisplayDriver.h` r.5-14

```cpp
class NullDisplayDriver : public DisplayDriver {
public:
  NullDisplayDriver() : DisplayDriver(128, 64) { }
  bool begin() { return false; }   // not present

  bool isOn() override { return false; }
  void turnOn() override { }
  void turnOff() override { }
  void clear() override { }
  void startFrame(ColorVal bkg = UIColor::window_bkg) override { }
```

It reports a screen size of 128 by 64 pixels that does not exist, `begin()`
returns `false`, and every drawing method is empty. The code above it
therefore never has to check whether a screen is present — it simply draws
into nothing. That is cheaper than an `if (display != NULL)` everywhere.

## Colour is a role, not a value

Up to the previous pinned commit `DisplayDriver` had an enumeration of seven
colours with one line of comment under it: on a black-and-white screen
everything except `DARK` is simply "on". That enumeration is still there, but
commented out — see `src/helpers/ui/DisplayDriver.h` r.19. What took its place
turns it around. The colour is not what is fixed; the *role* it fills is:

`src/helpers/ui/DisplayDriver.h` r.8-12

```cpp
class UIColor {
public:
  // color definitions (by element _type_)
  static ColorVal window_bkg, title_bkg, title_txt, primary_txt, secondary_txt, warning_txt, popup_bkg, popup_txt, corp_blue;
};
```

Nine roles: window background, title background, title text, primary text,
secondary text, warning text, popup background, popup text and one corporate
blue. The UI code asks for `UIColor::warning_txt` and does not have to know
which value comes out.

This is not a colour scheme. A scheme is a fixed set of colours; this is a
list of roles *without* values, which **twelve screen drivers each fill in
separately**. Every driver puts the nine fields down in its own `.cpp`, with
the values its panel knows. Three of them side by side:

| Role | `SSD1306Display` | `E213Display` | `NV3001BDisplay` |
|---|---|---|---|
| `window_bkg` | `SSD1306_BLACK` | `WHITE` | `0xFFFF` — white |
| `title_bkg` | `SSD1306_BLACK` | `WHITE` | `0x001F` — blue |
| `title_txt` | `SSD1306_WHITE` | `BLACK` | `0xFFFF` — white |
| `primary_txt` | `SSD1306_WHITE` | `BLACK` | `0x0000` — black |
| `warning_txt` | `SSD1306_WHITE` | `BLACK` | `0xFD20` — orange |
| `popup_bkg` | `SSD1306_BLACK` | `WHITE` | `0x07FF` — cyan |

The other nine drivers do the same: `E290Display`, `GxEPDDisplay`,
`LGFXDisplay`, `NullDisplayDriver`, `SH1106Display`, `ST7735Display`,
`ST7789Display`, `ST7789LCDDisplay` and `U8g2Display`. Writing out all twelve
adds nothing to the point: the same UI code yields black-on-white on e-paper
and white-on-black on an OLED, without an `if` anywhere that asks what type of
screen is underneath. On a monochrome screen several roles land on the same
value — that is not a loss, that is exactly what the mechanism does.
`NullDisplayDriver` sets all nine to zero, because there is nothing to drive.

`UIColor` holds static fields only and not a single method. Where that kind of
class belongs in the firmware, and why, is in
[The class model](../../design/technical/class-model.md).

Something similar holds for e-paper. `isEink()` returns `false` by default and
is overridden only by the e-paper drivers
(`src/helpers/ui/DisplayDriver.h` r.25). The code above can use that to decide
to refresh less often — e-paper has no interest in ten redraws per second.

## Accents become blocks

The screen drivers work with fonts that only know ASCII. What comes in is
UTF-8. The abstraction resolves that by replacing everything outside the
printable ASCII range with a single block character:

`src/helpers/ui/DisplayDriver.h` r.55-68

```cpp
  virtual void translateUTF8ToBlocks(char* dest, const char* src, size_t dest_size) {
    size_t j = 0;
    for (size_t i = 0; src[i] != 0 && j < dest_size - 1; i++) {
      unsigned char c = (unsigned char)src[i];
      if (c >= 32 && c <= 126) {
        dest[j++] = c;  // ASCII printable
      } else if (c >= 0x80) {
        dest[j++] = '\xDB';  // CP437 full block █
        while (src[i+1] && (src[i+1] & 0xC0) == 0x80) 
          i++;  // skip UTF-8 continuation bytes
      }
    }
    dest[j] = 0;
  }
```

A message with `é` or `ü` shows a filled block on screen, not the letter
and not two strange characters: the continuation bytes of the UTF-8
character are skipped, so one character stays one character wide. For Dutch
users this is the most common way a node appears to work "wrong" while
doing exactly what it says.

## Text that does not fit

For text that is too wide there is a truncation method with a notable
trick: the driver does not itself know whether its font is fixed or
variable width, so it measures.

`src/helpers/ui/DisplayDriver.h` r.87-94

```cpp
    // use a simple heuristic: if 'i' and 'l' have different widths, it's variable-width
    int i_width = getTextWidth("i");
    int l_width = getTextWidth("l");
    if (i_width != l_width) {
      ellipsis = "... ";  // variable-width fonts: add space
    } else {
      ellipsis = "...";   // fixed-width fonts: no space
    }
```

If `i` and `l` differ in width the font is variable and a space follows the
dots. On an OLED with a fixed font that space is left out, because there
every character takes up space.

## The power rail is counted, not switched

On many boards the screen hangs off a switchable power rail — the same rail
the GPS or a sensor sometimes sits on. Switching it off while another part
still needs it switches that other part off too. The firmware solves that
with a counter:

`src/helpers/RefCountedDigitalPin.h` r.17-31

```cpp
  void claim() {
    _claims++;
    if (_claims > 0) {
      digitalWrite(_pin, _active);
    }
  }

  void release() {
    if (_claims == 0) return; // avoid negative _claims

    _claims--;
    if (_claims == 0) {
      digitalWrite(_pin, !_active);
    }
  }
```

Every part claims the rail when switching on and releases it when switching
off; only at zero does the voltage go away. The screen makes that claim in
its own `begin()` and when switching back on after a power cut
(`src/helpers/ui/SSD1306Display.cpp` r.22 and r.33-35).

## The NV3001B is the only one that scales

Eleven of the twelve drivers pass a UI coordinate straight through to the
panel. The twelfth does not. `NV3001BDisplay` stretches the image: the UI
draws in a small area and the driver spreads that across the whole screen.
That is the distinguishing property of this driver, not the difference in
dimensions as such.

The chip itself is a display controller sitting between the processor and an
LCD panel. It talks over SPI using the command set of the ST77xx family:
`CASET` and `RASET` mark out a rectangle, `RAMWR` fills it with colours and
`MADCTL` sets the rotation. The colour mode is set to `0x05` —
`NV3001B_COLMOD` in `src/helpers/ui/NV3001BDisplay.cpp` r.370 — so 16 bits per
pixel in RGB565. A colour screen, then, not an OLED matrix.

### Three pairs of dimensions, to be kept apart

| Pair | Value | What it is | Location |
|---|---|---|---|
| `NV3001B_PANEL_WIDTH` / `_HEIGHT` | 128 × 220 | the bare panel, portrait | `src/helpers/ui/NV3001BDisplay.h` r.16 and r.20 |
| `NV3001B_SCREEN_WIDTH` / `_HEIGHT` | 220 × 128 | the same panel, landscape in use | `src/helpers/ui/NV3001BDisplay.cpp` r.54 and r.58 |
| `NV3001B_LOGICAL_WIDTH` / `_HEIGHT` | 128 × 64 | the area the UI draws in | `src/helpers/ui/NV3001BDisplay.h` r.8 and r.12 |

The first and the second pair are the same panel, noted once portrait and once
landscape. Anyone laying them side by side without noticing that is comparing
two different axes.

The constructor passes only the logical pair to `DisplayDriver`
(`src/helpers/ui/NV3001BDisplay.h` r.47). `width()` and `height()` therefore
report 128 and 64 to the rest of the firmware; the physical size can be
requested separately through `physicalWidth()` and `physicalHeight()`
(`src/helpers/ui/NV3001BDisplay.h` r.51 and r.52).

### Two scale factors, and why they differ

The factors are derived from the screen pair and the logical pair:

`src/helpers/ui/NV3001BDisplay.cpp` r.61-67

```cpp
#ifndef DISPLAY_SCALE_X
  #define DISPLAY_SCALE_X ((float)NV3001B_SCREEN_WIDTH / NV3001B_LOGICAL_WIDTH)
#endif

#ifndef DISPLAY_SCALE_Y
  #define DISPLAY_SCALE_Y ((float)NV3001B_SCREEN_HEIGHT / NV3001B_LOGICAL_HEIGHT)
#endif
```

| Axis | Calculation | Factor |
|---|---|---|
| horizontal | 220 / 128 | ≈ 1.72 |
| vertical | 128 / 64 | 2 |

Every coordinate passes through those factors:

`src/helpers/ui/NV3001BDisplay.cpp` r.110-116

```cpp
static int scaleX(int x) {
  return (int)(x * DISPLAY_SCALE_X);
}

static int scaleY(int y) {
  return (int)(y * DISPLAY_SCALE_Y);
}
```

![The logical area of 128 by 64 units beside the screen of 220 by 128 pixels,
and beside that the same logical area stretched across the whole screen. The
horizontal stretch is about 1.72 times, the vertical exactly 2 times, so a
square in the UI comes out taller than it is
wide](../../../images/en/display-2.svg)

The vertical factor is exactly 2, the horizontal one is not. A logical pixel
therefore becomes roughly 1.7 pixels wide and 2 pixels tall, and because the
conversion truncates with `(int)`, straight lines do not all come out the same
width. The vertical stretch is the larger of the two: a square in the UI comes
out taller than it is wide on this screen. Text width is converted back
for the same reason: `getTextWidth()`
(`src/helpers/ui/NV3001BDisplay.cpp` r.542) divides its result by
`DISPLAY_SCALE_X` again on r.547, so the UI gets its answer back in logical
units.

The whole panel is written to. The method `fillPhysicalRect` sits at
`src/helpers/ui/NV3001BDisplay.cpp` r.380 and clamps to the screen dimensions
`NV3001B_SCREEN_WIDTH` and `NV3001B_SCREEN_HEIGHT`, on r.391 and r.392. And
`NV3001BDisplay::clear` fills from (0,0) to the full screen, at
`src/helpers/ui/NV3001BDisplay.cpp` r.464. So no strip is left over that would
stay unused.

### One board

The driver occurs on exactly one variant: `heltec_rc32`, an ESP32-S3 with an
SX1262 and a rotary knob. The choice sits in the build flag `DISPLAY_CLASS` in
`variants/heltec_rc32/platformio.ini` r.71, in the section
`[Heltec_RC32_with_display]` — the variants of the same board *without* a
screen do not set that flag.

## Sources

Firmware, commit `d929643` (v1.17.1, 14 August 2026):

- [`src/helpers/ui/DisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/DisplayDriver.h)
  — the abstraction, `UIColor` and the text helpers
- [`src/helpers/ui/NullDisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/NullDisplayDriver.h)
  — the empty implementation
- [`src/helpers/ui/SSD1306Display.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/SSD1306Display.cpp)
  — the most common screen
- [`src/helpers/ui/NV3001BDisplay.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/NV3001BDisplay.h)
  — the three pairs of dimensions and the constructor
- [`src/helpers/ui/NV3001BDisplay.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/NV3001BDisplay.cpp)
  — the colour mode, the scale factors and how they are applied
- [`variants/heltec_rc32/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/d929643/variants/heltec_rc32/platformio.ini)
  — the only board with an NV3001B
- [`src/helpers/RefCountedDigitalPin.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/RefCountedDigitalPin.h)
  — the shared power rail

Related in this documentation:

- [The I²C Bus](../interfaces/i2c.md) — where the OLED hangs
- [The SPI Bus](../interfaces/spi.md) — where TFT and e-paper hang
- [Display libraries](../../libraries/other/displays.md) — the external
  libraries behind these drivers
- [Node Matrix](../../platform/node-matrix.md) — which board has which
  screen

Translated from Dutch by Anthropic Claude
