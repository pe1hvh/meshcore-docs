# The Display

*DISPLAYDRIVER · ELEVEN CLASSES · CP437 · POWER BY CLAIM*

A node does not need a screen, and many nodes have none. If one is fitted,
the firmware never talks to it directly: everything runs through a single
abstract class with eleven implementations under it. This chapter describes
that abstraction, what happens when there is no screen, and why accented
characters show up as blocks on an OLED.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `src/helpers/ui/DisplayDriver.h`, `src/helpers/ui/NullDisplayDriver.h`,
> `src/helpers/ui/SSD1306Display.cpp`, `src/helpers/RefCountedDigitalPin.h`
> and the `DISPLAY_CLASS` flags in `variants/`.

## One class, eleven fillings

The firmware knows the notion *screen* only as `DisplayDriver`: an abstract
class with fourteen methods every driver has to fill in, plus a handful of
helper methods falling back on those fourteen. Which driver is compiled in
sits in one build flag per board, `DISPLAY_CLASS`.

![The display abstraction: DisplayDriver with eleven implementations under
it, split across OLED on the I²C bus, TFT and e-paper on SPI, and an empty
implementation for boards without a screen](../../../images/en/display-1.svg)

Counted across `variants/`, 164 uncommented `-D DISPLAY_CLASS=` lines
spread over 57 files:

| Driver | Lines | What it is |
|---|---|---|
| `SSD1306Display` | 88 | the small OLED, on I²C |
| `NullDisplayDriver` | 15 | no screen |
| `ST7735Display` | 14 | small colour TFT, on SPI |
| `SH1106Display` | 13 | OLED with a slightly different controller |
| `E213Display` | 10 | e-paper 2.13 inch |
| `ST7789LCDDisplay` | 8 | larger colour TFT |
| `GxEPDDisplay` | 7 | generic e-paper |
| `E290Display` | 5 | e-paper 2.9 inch |
| `ST7789Display` | 2 | same controller, different driving |
| `U8g2Display` | 1 | generic monochrome driver |
| `SCIndicatorDisplay` | 1 | board-specific |

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

Fifteen build targets set `DISPLAY_CLASS=NullDisplayDriver`. That is not a
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
  void startFrame(Color bkg = DARK) override { }
```

It reports a screen size of 128 by 64 pixels that does not exist, `begin()`
returns `false`, and every drawing method is empty. The code above it
therefore never has to check whether a screen is present — it simply draws
into nothing. That is cheaper than an `if (display != NULL)` everywhere.

## Colour on a black-and-white screen

`DisplayDriver` has a colour enumeration of seven values and settles the
difference between screen types with one line of comment:

`src/helpers/ui/DisplayDriver.h` r.11

```cpp
  enum Color { DARK=0, LIGHT, RED, GREEN, BLUE, YELLOW, ORANGE }; // on b/w screen, colors will be !=0 synonym of light
```

On a monochrome screen every colour except `DARK` is simply "on". The
screen code does not have to know what is underneath.

Something similar holds for e-paper. `isEink()` returns `false` by default
and is overridden only by the e-paper drivers
(`src/helpers/ui/DisplayDriver.h` r.17). The code above can use that to
decide to refresh less often — e-paper has no interest in ten redraws per
second.

## Accents become blocks

The screen drivers work with fonts that only know ASCII. What comes in is
UTF-8. The abstraction resolves that by replacing everything outside the
printable ASCII range with a single block character:

`src/helpers/ui/DisplayDriver.h` r.47-60

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

`src/helpers/ui/DisplayDriver.h` r.79-86

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
every character is precious.

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
(`src/helpers/ui/SSD1306Display.cpp` r.11 and r.23-24).

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`src/helpers/ui/DisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/DisplayDriver.h)
  — the abstraction, the colour enumeration and the text helpers
- [`src/helpers/ui/NullDisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/NullDisplayDriver.h)
  — the empty implementation
- [`src/helpers/ui/SSD1306Display.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/SSD1306Display.cpp)
  — the most common screen
- [`src/helpers/RefCountedDigitalPin.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/RefCountedDigitalPin.h)
  — the shared power rail

Related in this documentation:

- [The I²C Bus](../interfaces/i2c.md) — where the OLED hangs
- [The SPI Bus](../interfaces/spi.md) — where TFT and e-paper hang
- [Display libraries](../../libraries/other/displays.md) — the external
  libraries behind these drivers
- [Node Matrix](../../platform/node-matrix.md) — which board has which
  screen

Translated from Dutch by Anthropic Claude
