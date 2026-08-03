# Het scherm

*DISPLAYDRIVER · ELF KLASSEN · CP437 · VOEDING PER CLAIM*

Een node hoeft geen scherm te hebben, en veel nodes hebben er geen. Zit er
wel een, dan praat de firmware er nooit rechtstreeks mee: alles loopt via
één abstracte klasse waar elf implementaties onder hangen. Dit hoofdstuk
beschrijft die abstractie, wat er gebeurt als er geen scherm is, en waarom
je accenten op een OLED als blokjes ziet.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/ui/DisplayDriver.h`, `src/helpers/ui/NullDisplayDriver.h`,
> `src/helpers/ui/SSD1306Display.cpp`, `src/helpers/RefCountedDigitalPin.h`
> en de `DISPLAY_CLASS`-vlaggen in `variants/`.

## Eén klasse, elf implementaties

De firmware kent het begrip *scherm* alleen als `DisplayDriver`: een abstracte
klasse met veertien methodes die elke driver moet implementeren, plus een
handvol hulpmethodes die op die veertien teruggrijpen. Welke driver wordt
meegecompileerd staat in één buildvlag per bord, `DISPLAY_CLASS`.

![De schermabstractie: DisplayDriver met elf implementaties eronder,
verdeeld over OLED op de I²C-bus, TFT en e-paper op SPI, en een lege
implementatie voor borden zonder scherm](../../../images/nl/display-1.svg)

Geteld over `variants/`, 164 niet-uitgecommentarieerde `-D
DISPLAY_CLASS=`-regels verdeeld over 57 bestanden:

| Driver | Regels | Wat het is |
|---|---|---|
| `SSD1306Display` | 88 | het kleine OLED, op I²C |
| `NullDisplayDriver` | 15 | geen scherm |
| `ST7735Display` | 14 | kleine kleuren-TFT, op SPI |
| `SH1106Display` | 13 | OLED met net andere controller |
| `E213Display` | 10 | e-paper 2,13 inch |
| `ST7789LCDDisplay` | 8 | grotere kleuren-TFT |
| `GxEPDDisplay` | 7 | generieke e-paper |
| `E290Display` | 5 | e-paper 2,9 inch |
| `ST7789Display` | 2 | dezelfde controller, andere aansturing |
| `U8g2Display` | 1 | generieke monochroomdriver |
| `SCIndicatorDisplay` | 1 | bordspecifiek |

Te herhalen met:

```bash
grep -rh -- "-D DISPLAY_CLASS=" variants/ | grep -v "^\s*;" \
  | sed 's/.*DISPLAY_CLASS=//' | tr -d ' \r' | sort | uniq -c | sort -rn
```

Welk concreet bord welk scherm heeft staat in
[Nodematrix](../../platform/node-matrix.md) en wordt hier niet herhaald.
Hoe het scherm fysiek aan de SoC hangt staat in [De I²C-bus](../interfaces/i2c.md)
en [De SPI-bus](../interfaces/spi.md).

## Geen scherm is ook een scherm

Vijftien buildtargets zetten `DISPLAY_CLASS=NullDisplayDriver`. Dat is geen
ontbrekende vlag maar een expliciete keuze: een volledige implementatie die
niets doet.

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

Het meldt een schermformaat van 128 bij 64 pixels dat er niet is, `begin()`
geeft `false` terug, en alle tekenmethodes zijn leeg. De code erboven hoeft
daardoor nergens te controleren of er een scherm is — hij tekent gewoon in
het niets. Dat is goedkoper dan overal een `if (display != NULL)`.

## Kleur op een zwart-wit scherm

`DisplayDriver` heeft een kleurenopsomming van zeven waarden en lost het
verschil tussen schermtypes op met één regel commentaar:

`src/helpers/ui/DisplayDriver.h` r.11

```cpp
  enum Color { DARK=0, LIGHT, RED, GREEN, BLUE, YELLOW, ORANGE }; // on b/w screen, colors will be !=0 synonym of light
```

Op een monochroom scherm is elke kleur behalve `DARK` dus gewoon "aan". De
schermcode hoeft niet te weten wat eronder hangt.

Iets soortgelijks geldt voor e-paper. `isEink()` geeft standaard `false` en
wordt alleen door de e-paperdrivers overschreven
(`src/helpers/ui/DisplayDriver.h` r.17). De code erboven kan daarmee
besluiten om minder vaak te verversen — e-paper heeft geen zin in
tien beeldopbouwen per seconde.

## Accenten worden blokjes

De schermdrivers werken met fonts die alleen ASCII kennen. Wat er
binnenkomt is UTF-8. De abstractie lost dat op door alles buiten het
printbare ASCII-bereik te vervangen door één blokteken:

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

Een berichtje met `é` of `ü` toont op het scherm een gevuld blok, niet de
letter en niet twee vreemde tekens: de vervolgbytes van het UTF-8-teken
worden overgeslagen, dus één teken blijft één teken breed. Voor Nederlandse
gebruikers is dat de gewoonste manier waarop een node "verkeerd" lijkt te
werken terwijl hij precies doet wat er staat.

## Tekst die niet past

Voor tekst die te breed is zit er een afkapmethode in met een opmerkelijke
truc: de driver weet zelf niet of zijn font vaste of variabele breedte
heeft, dus meet hij het.

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

Verschillen `i` en `l` in breedte, dan is het font variabel en komt er een
spatie achter de puntjes. Op een OLED met een vast lettertype blijft die
spatie weg, omdat elk teken ruimte inneemt.

## De voeding wordt geteld, niet geschakeld

Op veel borden hangt het scherm aan een schakelbare voedingsrail — dezelfde
rail waar soms ook de GPS of een sensor aan zit. Wie hem uitzet terwijl een
ander onderdeel hem nog nodig heeft, zet dat andere onderdeel ook uit. De
firmware lost dat op met een teller:

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

Elk onderdeel claimt de rail bij het aanzetten en geeft hem vrij bij het
uitzetten; pas bij nul gaat de spanning eraf. Het scherm doet die claim in
zijn eigen `begin()` en bij het weer aanzetten na een stroomonderbreking
(`src/helpers/ui/SSD1306Display.cpp` r.11 en r.23-24).

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`src/helpers/ui/DisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/DisplayDriver.h)
  — de abstractie, de kleurenopsomming en de teksthulpmethodes
- [`src/helpers/ui/NullDisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/NullDisplayDriver.h)
  — de lege implementatie
- [`src/helpers/ui/SSD1306Display.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/SSD1306Display.cpp)
  — het meest voorkomende scherm
- [`src/helpers/RefCountedDigitalPin.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/RefCountedDigitalPin.h)
  — de gedeelde voedingsrail

Verwant in deze documentatie:

- [De I²C-bus](../interfaces/i2c.md) — waar het OLED aan hangt
- [De SPI-bus](../interfaces/spi.md) — waar TFT en e-paper aan hangen
- [Displaylibraries](../../libraries/other/displays.md) — de externe
  libraries achter deze drivers
- [Nodematrix](../../platform/node-matrix.md) — welk bord welk scherm heeft
