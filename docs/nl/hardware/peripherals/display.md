# Het scherm

*DISPLAYDRIVER · TWAALF KLASSEN · UICOLOR · SCHALING · CP437*

Een node hoeft geen scherm te hebben, en veel nodes hebben er geen. Zit er
wel een, dan praat de firmware er nooit rechtstreeks mee: alles loopt via
één abstracte klasse waar twaalf implementaties onder hangen. Dit hoofdstuk
beschrijft die abstractie, wat er gebeurt als er geen scherm is, waarom je
accenten op een OLED als blokjes ziet, en waarom één van de twaalf drivers
het beeld oprekt terwijl de elf andere dat niet doen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.17.1, commit `d929643`, 14 augustus 2026 — bestanden
> `src/helpers/ui/DisplayDriver.h`, `src/helpers/ui/NullDisplayDriver.h`,
> `src/helpers/ui/SSD1306Display.cpp`, `src/helpers/ui/NV3001BDisplay.h`,
> `src/helpers/ui/NV3001BDisplay.cpp`, `src/helpers/RefCountedDigitalPin.h`
> en de `DISPLAY_CLASS`-vlaggen in `variants/`.

## Eén klasse, twaalf implementaties

De firmware kent het begrip *scherm* alleen als `DisplayDriver`: een abstracte
klasse met veertien methodes die elke driver moet implementeren, plus een
handvol hulpmethodes die op die veertien teruggrijpen. Welke driver wordt
meegecompileerd staat in één buildvlag per bord, `DISPLAY_CLASS`.

![De schermabstractie: DisplayDriver met twaalf implementaties eronder,
verdeeld over OLED op de I²C-bus, TFT en e-paper op SPI, en een lege
implementatie voor borden zonder scherm](../../../images/nl/display-1.svg)

Geteld over `variants/`, 205 niet-uitgecommentarieerde `-D
DISPLAY_CLASS=`-regels verdeeld over 65 bestanden:

| Driver | Regels | Wat het is |
|---|---|---|
| `SSD1306Display` | 110 | het kleine OLED, op I²C |
| `NullDisplayDriver` | 26 | geen scherm |
| `ST7789LCDDisplay` | 14 | grotere kleuren-TFT |
| `ST7735Display` | 14 | kleine kleuren-TFT, op SPI |
| `SH1106Display` | 13 | OLED met net andere controller |
| `E213Display` | 10 | e-paper 2,13 inch |
| `GxEPDDisplay` | 7 | generieke e-paper |
| `E290Display` | 5 | e-paper 2,9 inch |
| `ST7789Display` | 3 | dezelfde controller, andere aansturing |
| `U8g2Display` | 1 | generieke monochroomdriver |
| `SCIndicatorDisplay` | 1 | bordspecifiek, erft van `LGFXDisplay` |
| `NV3001BDisplay` | 1 | kleuren-LCD dat de UI-coördinaten opschaalt |

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

Zesentwintig buildtargets zetten `DISPLAY_CLASS=NullDisplayDriver`. Dat is geen
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
  void startFrame(ColorVal bkg = UIColor::window_bkg) override { }
```

Het meldt een schermformaat van 128 bij 64 pixels dat er niet is, `begin()`
geeft `false` terug, en alle tekenmethodes zijn leeg. De code erboven hoeft
daardoor nergens te controleren of er een scherm is — hij tekent gewoon in
het niets. Dat is goedkoper dan overal een `if (display != NULL)`.

## Kleur is een rol, geen waarde

Tot de vorige gepinde commit had `DisplayDriver` een opsomming van zeven
kleuren, met één regel commentaar eronder: op een zwart-wit scherm is alles
behalve `DARK` gewoon "aan". Die opsomming staat er nog, maar
uitgecommentarieerd — zie `src/helpers/ui/DisplayDriver.h` r.19. Wat ervoor
in de plaats kwam draait het om. Niet de kleur ligt vast, maar de *rol* die
hij vervult:

`src/helpers/ui/DisplayDriver.h` r.8-12

```cpp
class UIColor {
public:
  // color definitions (by element _type_)
  static ColorVal window_bkg, title_bkg, title_txt, primary_txt, secondary_txt, warning_txt, popup_bkg, popup_txt, corp_blue;
};
```

Negen rollen: vensterachtergrond, titelachtergrond, titeltekst, primaire
tekst, secundaire tekst, waarschuwingstekst, popupachtergrond, popuptekst en
één huisblauw. De UI-code vraagt om `UIColor::warning_txt` en hoeft niet te
weten welke waarde daaruit komt.

Dit is geen kleurenschema. Een schema is een vastgelegde verzameling kleuren;
dit is een lijst rollen zónder waarden, die **twaalf schermdrivers elk apart
invullen**. Elke driver zet de negen velden neer in zijn eigen `.cpp`, met de
waarden die zijn paneel kent. Drie ervan naast elkaar:

| Rol | `SSD1306Display` | `E213Display` | `NV3001BDisplay` |
|---|---|---|---|
| `window_bkg` | `SSD1306_BLACK` | `WHITE` | `0xFFFF` — wit |
| `title_bkg` | `SSD1306_BLACK` | `WHITE` | `0x001F` — blauw |
| `title_txt` | `SSD1306_WHITE` | `BLACK` | `0xFFFF` — wit |
| `primary_txt` | `SSD1306_WHITE` | `BLACK` | `0x0000` — zwart |
| `warning_txt` | `SSD1306_WHITE` | `BLACK` | `0xFD20` — oranje |
| `popup_bkg` | `SSD1306_BLACK` | `WHITE` | `0x07FF` — cyaan |

De andere negen drivers doen hetzelfde: `E290Display`, `GxEPDDisplay`,
`LGFXDisplay`, `NullDisplayDriver`, `SH1106Display`, `ST7735Display`,
`ST7789Display`, `ST7789LCDDisplay` en `U8g2Display`. Alle twaalf uitschrijven
voegt niets toe aan het punt: dezelfde UI-code levert zwart-op-wit op e-paper
en wit-op-zwart op een OLED, zonder dat er ergens een `if` staat die het
schermtype opvraagt. Op een monochroom scherm vallen meerdere rollen op
dezelfde waarde samen — dat is geen verlies, dat is precies wat het mechanisme
doet. `NullDisplayDriver` zet ze alle negen op nul, want er is niets om aan te
sturen.

`UIColor` bevat uitsluitend statische velden en geen enkele methode. Waar dat
soort klassen in de firmware thuishoort en waarom, staat in
[Het klassenmodel](../../design/technical/class-model.md).

Iets soortgelijks geldt voor e-paper. `isEink()` geeft standaard `false` en
wordt alleen door de e-paperdrivers overschreven
(`src/helpers/ui/DisplayDriver.h` r.25). De code erboven kan daarmee besluiten
om minder vaak te verversen — e-paper heeft geen zin in tien beeldopbouwen per
seconde.

## Accenten worden blokjes

De schermdrivers werken met fonts die alleen ASCII kennen. Wat er
binnenkomt is UTF-8. De abstractie lost dat op door alles buiten het
printbare ASCII-bereik te vervangen door één blokteken:

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

Een berichtje met `é` of `ü` toont op het scherm een gevuld blok, niet de
letter en niet twee vreemde tekens: de vervolgbytes van het UTF-8-teken
worden overgeslagen, dus één teken blijft één teken breed. Voor Nederlandse
gebruikers is dat de gewoonste manier waarop een node "verkeerd" lijkt te
werken terwijl hij precies doet wat er staat.

## Tekst die niet past

Voor tekst die te breed is zit er een afkapmethode in met een opmerkelijke
truc: de driver weet zelf niet of zijn font vaste of variabele breedte
heeft, dus meet hij het.

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
(`src/helpers/ui/SSD1306Display.cpp` r.22 en r.33-35).

## De NV3001B is de enige die schaalt

Elf van de twaalf drivers geven een UI-coördinaat één op één aan het paneel
door. De twaalfde niet. `NV3001BDisplay` rekt het beeld op: de UI tekent in
een klein vlak en de driver spreidt dat uit over het hele scherm. Dat is het
onderscheidende kenmerk van deze driver, niet het maatverschil op zich.

De chip zelf is een schermcontroller tussen de processor en een LCD-paneel.
Hij praat over SPI met het commandostel uit de ST77xx-familie: `CASET` en
`RASET` bakenen een rechthoek af, `RAMWR` vult die met kleuren en `MADCTL`
zet de rotatie. De kleurmodus staat op `0x05` — `NV3001B_COLMOD` in
`src/helpers/ui/NV3001BDisplay.cpp` r.370 — dus 16 bits per pixel in RGB565.
Een kleurenscherm dus, geen OLED-matrix.

### Drie paren maten, uit elkaar te houden

| Paar | Waarde | Wat het is | Plek |
|---|---|---|---|
| `NV3001B_PANEL_WIDTH` / `_HEIGHT` | 128 × 220 | het kale paneel, staand | `src/helpers/ui/NV3001BDisplay.h` r.16 en r.20 |
| `NV3001B_SCREEN_WIDTH` / `_HEIGHT` | 220 × 128 | hetzelfde paneel, liggend in gebruik | `src/helpers/ui/NV3001BDisplay.cpp` r.54 en r.58 |
| `NV3001B_LOGICAL_WIDTH` / `_HEIGHT` | 128 × 64 | het vlak waarin de UI tekent | `src/helpers/ui/NV3001BDisplay.h` r.8 en r.12 |

Het eerste en het tweede paar zijn hetzelfde paneel, één keer staand en één
keer liggend genoteerd. Wie ze naast elkaar legt zonder daarop te letten,
vergelijkt twee verschillende assen.

De constructor geeft alleen het logische paar door aan `DisplayDriver`
(`src/helpers/ui/NV3001BDisplay.h` r.47). `width()` en `height()` melden
daarom 128 en 64 aan de rest van de firmware; de fysieke maat is apart op te
vragen via `physicalWidth()` en `physicalHeight()`
(`src/helpers/ui/NV3001BDisplay.h` r.51 en r.52).

### Twee schaalfactoren, en waarom ze verschillen

De factoren worden afgeleid uit het scherm- en het logische paar:

`src/helpers/ui/NV3001BDisplay.cpp` r.61-67

```cpp
#ifndef DISPLAY_SCALE_X
  #define DISPLAY_SCALE_X ((float)NV3001B_SCREEN_WIDTH / NV3001B_LOGICAL_WIDTH)
#endif

#ifndef DISPLAY_SCALE_Y
  #define DISPLAY_SCALE_Y ((float)NV3001B_SCREEN_HEIGHT / NV3001B_LOGICAL_HEIGHT)
#endif
```

| As | Berekening | Factor |
|---|---|---|
| horizontaal | 220 / 128 | ≈ 1,72 |
| verticaal | 128 / 64 | 2 |

Elke coördinaat gaat door die factoren heen:

`src/helpers/ui/NV3001BDisplay.cpp` r.110-116

```cpp
static int scaleX(int x) {
  return (int)(x * DISPLAY_SCALE_X);
}

static int scaleY(int y) {
  return (int)(y * DISPLAY_SCALE_Y);
}
```

![Het logische vlak van 128 bij 64 eenheden naast het scherm van 220 bij 128
pixels, en daarnaast hetzelfde logische vlak uitgerekt over het hele scherm.
De horizontale rek is ongeveer 1,72 keer, de verticale precies 2 keer, zodat
een vierkant in de UI op het scherm hoger dan breed
uitvalt](../../../images/nl/display-2.svg)

De verticale factor is precies 2, de horizontale niet. Een logische pixel
wordt dus ongeveer 1,7 pixel breed en 2 pixels hoog, en omdat de omrekening
met `(int)` naar beneden afkapt, vallen rechte lijnen niet allemaal even breed
uit. De verticale rek is de grootste van de twee: een vierkant in de UI komt
op dit scherm hoger dan breed uit. Tekstbreedte wordt
om dezelfde reden teruggerekend: `getTextWidth()`
(`src/helpers/ui/NV3001BDisplay.cpp` r.542) deelt de uitkomst weer door
`DISPLAY_SCALE_X` op r.547, zodat de UI zijn antwoord in logische eenheden
terugkrijgt.

Het hele paneel wordt beschreven. De methode `fillPhysicalRect` staat op
`src/helpers/ui/NV3001BDisplay.cpp` r.380 en klemt op de schermmaten
`NV3001B_SCREEN_WIDTH` en `NV3001B_SCREEN_HEIGHT`, op r.391 en r.392. En
`NV3001BDisplay::clear` vult van (0,0) tot het volledige scherm, op
`src/helpers/ui/NV3001BDisplay.cpp` r.464. Er blijft dus geen strook over die
ongebruikt zou blijven.

### Eén bord

De driver komt op precies één variant voor: `heltec_rc32`, een ESP32-S3 met
een SX1262 en een draaiknop. De keuze staat in de buildvlag
`DISPLAY_CLASS` in `variants/heltec_rc32/platformio.ini` r.71, in de sectie
`[Heltec_RC32_with_display]` — de varianten zónder scherm van hetzelfde bord
zetten die vlag niet.

## Bronnen

Firmware, commit `d929643` (v1.17.1, 14 augustus 2026):

- [`src/helpers/ui/DisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/DisplayDriver.h)
  — de abstractie, `UIColor` en de teksthulpmethodes
- [`src/helpers/ui/NullDisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/NullDisplayDriver.h)
  — de lege implementatie
- [`src/helpers/ui/SSD1306Display.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/SSD1306Display.cpp)
  — het meest voorkomende scherm
- [`src/helpers/ui/NV3001BDisplay.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/NV3001BDisplay.h)
  — de drie paren maten en de constructor
- [`src/helpers/ui/NV3001BDisplay.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/NV3001BDisplay.cpp)
  — de kleurmodus, de schaalfactoren en hun toepassing
- [`variants/heltec_rc32/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/d929643/variants/heltec_rc32/platformio.ini)
  — het enige bord met een NV3001B
- [`src/helpers/RefCountedDigitalPin.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/RefCountedDigitalPin.h)
  — de gedeelde voedingsrail

Verwant in deze documentatie:

- [De I²C-bus](../interfaces/i2c.md) — waar het OLED aan hangt
- [De SPI-bus](../interfaces/spi.md) — waar TFT en e-paper aan hangen
- [Displaylibraries](../../libraries/other/displays.md) — de externe
  libraries achter deze drivers
- [Nodematrix](../../platform/node-matrix.md) — welk bord welk scherm heeft
