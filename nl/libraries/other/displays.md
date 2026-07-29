# Displaylibraries

*DISPLAY_CLASS · OLED · E-INK · TFT · ABSTRACTIE*

MeshCore kent elf waarden voor `DISPLAY_CLASS`, van een OLED van een paar
centimeter tot een e-inkpaneel en een kleuren-TFT. In de firmware is
daar bijna niets van te merken: alle schermen zitten achter één interface, en
welke library daadwerkelijk meegecompileerd wordt, bepaalt één bouwvlag per
variant.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, de negenenzeventig `variants/*/platformio.ini`,
> `src/helpers/ui/DisplayDriver.h`, `src/helpers/ui/SSD1306Display.h` en
> `examples/simple_repeater/main.cpp`.

## Hoe MeshCore deze groep aanroept

De abstractie heet `DisplayDriver`. Elke schermdriver erft ervan en
implementeert dezelfde methodes:

`src/helpers/ui/DisplayDriver.h` r.6-21

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

Welke implementatie het wordt, zegt de variant met `-D DISPLAY_CLASS=…`. De
schetsen kennen alleen die naam:

`examples/simple_repeater/main.cpp` r.42-46

```cpp
#ifdef DISPLAY_CLASS
  if (display.begin()) {
    display.startFrame();
    display.setCursor(0, 0);
    display.print("Please wait...");
```

Is `DISPLAY_CLASS` niet gedefinieerd, dan verdwijnt alle schermcode uit de
build. Er is daarnaast een `NullDisplayDriver` voor borden die wel de
UI-taak draaien maar geen scherm hebben.

![De DISPLAY_CLASS-abstractie in MeshCore: elke variant kiest met één
bouwvlag een schermdriver, alle drivers erven van dezelfde
DisplayDriver-interface, en daarachter zitten de losse displaylibraries van
Adafruit, GxEPD2, U8g2 en LovyanGFX](../../../images/nl/displays-1.svg)

## Adafruit SSD1306

De SSD1306 is de controller van de kleine monochrome OLED-schermpjes van
128 × 64 of 128 × 32 pixels die op de meeste MeshCore-borden zitten. De
library van Adafruit praat er over I²C of SPI mee en houdt een volledige
framebuffer in RAM aan. Met drieëntwintig varianten is dit de meest
voorkomende displaylibrary in de repo, en `SSD1306Display` is de
`DISPLAY_CLASS` van verreweg de meeste borden. De driver zet
`SSD1306_NO_SPLASH` vóór de include, zodat het Adafruit-logo bij het
opstarten niet verschijnt.

## Adafruit SH110X

De SH1106 en SH1107 zijn OLED-controllers die sterk op de SSD1306 lijken maar
een iets andere geheugenindeling hebben — een scherm met deze controller
aansturen als SSD1306 levert een beeld dat een paar pixels verschoven is. De
library ondersteunt beide typen. In zeven varianten: `lilygo_tbeam_1w`,
`lilygo_tbeam_supreme_SX1262`, `nano_g2_ultra`, `station_g2`,
`station_g3_esp32`, `thinknode_m2` en `wio-tracker-l1`, met `SH1106Display`
als driver.

## zinggjm/GxEPD2

GxEPD2 is de standaardlibrary voor e-inkpanelen op Arduino: hij kent
tientallen paneeltypes, elk met hun eigen initialisatiereeks en
verversingsgedrag, en biedt zowel volledige als gedeeltelijke verversing.
Vijf varianten gebruiken hem — `lilygo_techo`, `lilygo_techo_lite`,
`mesh_pocket`, `thinknode_m1` en `thinknode_m5` — via `GxEPDDisplay`. De
zesde e-inkvariant, `wio-tracker-l1-eink`, haalt een fork op:
`https://github.com/SoulOfNoob/GxEPD2.git`, zonder revisie achter de URL.

## Adafruit GFX Library

GFX is geen schermdriver maar de tekenlaag eronder: lijnen, rechthoeken,
tekst, lettertypen en bitmaps, allemaal in een framebuffer die een driver
daarna naar het scherm schrijft. SSD1306, SH110X, ST7735/ST7789 en Adafruit
EPD hebben hem alle vier nodig en declareren hem in hun eigen `depends=`.
In acht varianten staat hij dáárnaast nog eens expliciet in `lib_deps` —
zie [`../dependencies.md`](../dependencies.md), waar dat als bewust
versiebeheer over de keten heen beschreven staat.

## Adafruit BusIO

BusIO is de gedeelde bustoegangslaag van Adafruit: één API voor een register
op een I²C- of SPI-apparaat, zodat de driverlibraries zich niet met de bus
hoeven te bemoeien. Vrijwel elke Adafruit-library brengt hem via `depends=`
mee. In precies één variant staat hij expliciet gedeclareerd,
`sensecap_indicator-espnow`.

## Adafruit ST7735 and ST7789 Library

ST7735 en ST7789 zijn controllers voor kleine kleuren-TFT-schermen. De
library ondersteunt beide en werkt bovenop GFX. Zes varianten gebruiken hem:
`heltec_t096`, `heltec_t1`, `heltec_tracker`, `heltec_tracker_v2`,
`heltec_v4` en `lilygo_tdeck`, met `ST7735Display`, `ST7789Display` of
`ST7789LCDDisplay` als driver. Deze library sleept twee libraries mee die
verder nergens genoemd worden — `Adafruit seesaw Library` en `SD` — omdat
zijn voorbeelden die nodig hebben.

## Adafruit EPD

Adafruit EPD is de e-inklibrary van Adafruit, met ondersteuning voor hun
eigen panelen en breakouts. Hij staat in één variant gedeclareerd,
`mesh_pocket`, exact vastgepind op 4.6.1. In de broncode is geen enkele
include van `Adafruit_EPD` te vinden; die waarneming staat beschreven in
[`../dependencies.md`](../dependencies.md).

## olikraus/U8g2

U8g2 is een monochrome grafische library die een groot aantal
displaycontrollers ondersteunt, met een eigen lettertypesysteem en de
mogelijkheid om zonder volledige framebuffer te werken — bruikbaar op borden
met weinig RAM. Eén variant gebruikt hem, `lilygo_techo_card`, via
`U8g2Display`.

## lovyan03/LovyanGFX

LovyanGFX is een grafische library voor kleurenschermen die op ESP32 gebruik
maakt van DMA en daardoor snel is bij grote schermen. Eén variant gebruikt
hem, `sensecap_indicator-espnow`, via `LGFXDisplay`.

## heltec-eink-modules

Voor de e-inkmodules van Heltec worden twee verschillende forks van dezelfde
library opgehaald, allebei als zip van een volledige commit-hash:

| Fork | Commit | Varianten |
|---|---|---|
| `Quency-D/heltec-eink-modules` | `563dd41` | `heltec_e213`, `heltec_e290` |
| `todd-herbert/heltec-eink-modules` | `9207eb6` | `heltec_wireless_paper` |

De bijbehorende drivers zijn `E213Display` en `E290Display`. Beide gebruiken
`CRC32` om te bepalen of het scherm überhaupt ververst hoeft te worden — zie
[`utilities.md`](utilities.md).

## Overzicht

| Library | Versie | Varianten | Driver |
|---|---|---|---|
| `adafruit/Adafruit SSD1306` | `^2.5.13` | 23 | `SSD1306Display` |
| `adafruit/Adafruit SH110X` | `^2.1.13` · `~2.1.13` | 7 | `SH1106Display` |
| `adafruit/Adafruit GFX Library` | `^1.12.1` | 8 | tekenlaag |
| `adafruit/Adafruit BusIO` | `^1.17.2` | 1 | bustoegang |
| `adafruit/Adafruit ST7735 and ST7789 Library` | `^1.11.0` | 6 | `ST7735Display`, `ST7789Display`, `ST7789LCDDisplay` |
| `adafruit/Adafruit EPD` | `4.6.1` | 1 | geen include gevonden |
| `zinggjm/GxEPD2` | `1.6.2` | 5 | `GxEPDDisplay` |
| `SoulOfNoob/GxEPD2` | geen revisie | 1 | `GxEPDDisplay` |
| `Quency-D/heltec-eink-modules` | `563dd41` | 2 | `E213Display`, `E290Display` |
| `todd-herbert/heltec-eink-modules` | `9207eb6` | 1 | `E290Display` |
| `olikraus/U8g2` | `^2.35.19` | 1 | `U8g2Display` |
| `lovyan03/LovyanGFX` | `^1.2.7` | 1 | `LGFXDisplay` |

## Bronnen

- [`src/helpers/ui/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/src/helpers/ui)
- [`src/helpers/ui/DisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/DisplayDriver.h)
- [`src/helpers/ui/SSD1306Display.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/SSD1306Display.h)
- [`examples/simple_repeater/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/main.cpp)
- [adafruit/Adafruit_SSD1306](https://github.com/adafruit/Adafruit_SSD1306)
- [ZinggJM/GxEPD2](https://github.com/ZinggJM/GxEPD2)
- [olikraus/U8g2_Arduino](https://github.com/olikraus/U8g2_Arduino)
- [lovyan03/LovyanGFX](https://github.com/lovyan03/LovyanGFX)
