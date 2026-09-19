# Knoppen en LED's

*MOMENTARYBUTTON · VIJF GEBEURTENISSEN · RTTTL · ZENDLAMPJE*

De eenvoudigste onderdelen van een node zijn ook de enige waarmee je hem
bedient zonder telefoon. Eén knop, een lampje en soms een zoemer. Dit
hoofdstuk beschrijft hoe de firmware vijf verschillende gebeurtenissen uit
één knop haalt, welke lampjes er zijn, en welk melodietje er bij het
opstarten klinkt.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/ui/MomentaryButton.h`, `src/helpers/ui/MomentaryButton.cpp`,
> `src/helpers/ui/buzzer.h`, `src/helpers/ESP32Board.h` en de pinvlaggen in
> `variants/`.

## Vijf gebeurtenissen uit één knop

De meeste MeshCore-borden hebben precies één bedienbare knop.
Tweeënveertig variantbestanden zetten een `-D PIN_USER_BTN=`-regel, samen
vierenveertig regels — `rak4631` zet de vlag drie keer, in drie verschillende
`[env:…]`-secties. Te herhalen met `tools/hardware-overview.py`. Uit die ene
knop haalt de firmware vijf verschillende gebeurtenissen:

`src/helpers/ui/MomentaryButton.h` r.5-9

```cpp
#define BUTTON_EVENT_NONE        0
#define BUTTON_EVENT_CLICK       1
#define BUTTON_EVENT_LONG_PRESS  2
#define BUTTON_EVENT_DOUBLE_CLICK 3
#define BUTTON_EVENT_TRIPLE_CLICK 4
```

![Hoe uit één knop vijf gebeurtenissen komen: kort indrukken, tweemaal en
driemaal binnen 280 milliseconden, en langer indrukken dan de ingestelde
drempel](../../../images/nl/buttons-and-leds-1.svg)

Het onderscheid zit in twee tijden. De lange druk heeft een drempel die
per bord wordt meegegeven; op de Heltec V3 is dat 1000 milliseconde
(`variants/heltec_v3/target.cpp` r.28). Het venster voor dubbel- en
drievoudig klikken staat vast in de code:

`src/helpers/ui/MomentaryButton.cpp` r.3

```cpp
#define MULTI_CLICK_WINDOW_MS  280
```

Volgt er binnen 280 milliseconde nog een klik, dan wordt het een dubbele of
drievoudige. Dat betekent ook dat een gewone klik pas *na* dat venster
gemeld kan worden — de firmware moet immers afwachten of er nog een volgt.
Wie meerdere klikken niet nodig heeft kan dat venster op nul zetten met de
constructorparameter `multiclick`, en dan meldt de knop meteen.

## De knop kent vier bedradingen

Niet elk bord trekt zijn knop dezelfde kant op. De constructor vangt dat op
met twee vlaggen, en er is een tweede constructor voor knoppen die aan een
analoge ingang hangen in plaats van aan een digitale.

`src/helpers/ui/MomentaryButton.cpp` r.35-39

```cpp
void MomentaryButton::begin() {
  if (_pin >= 0 && _threshold == 0) {
    pinMode(_pin, _pull ? (_reverse ? INPUT_PULLUP : INPUT_PULLDOWN) : INPUT);
  }
}
```

| Parameter | Betekenis |
|---|---|
| `reverse` | ingedrukt is laag in plaats van hoog |
| `pulldownup` | de interne weerstand aanzetten; richting volgt uit `reverse` |
| `analog_threshold` | knop op een analoge ingang; boven deze waarde geldt hij als ingedrukt |

Bij de analoge variant wordt `pinMode()` overgeslagen — vandaar de
voorwaarde `_threshold == 0`. Een pin van `-1` betekent geen knop, en ook
dan doet `begin()` niets.

## Lampjes

Er zijn drie soorten lampjes in de firmware, en ze doen alle drie iets
anders. Geteld over niet-uitgecommentarieerde `-D`-regels in `variants/`:

| Vlag | Regels | Bestanden | Wat het doet |
|---|---|---|---|
| `P_LORA_TX_LED` | 45 | 44 | brandt tijdens zenden |
| `PIN_STATUS_LED` | 6 | 6 | statusindicatie |
| `PIN_LED` | 1 | 1 | algemeen lampje |

Te herhalen met `grep -rh -- "-D P_LORA_TX_LED=" variants/ | grep -v "^\s*;" | wc -l`
en hetzelfde patroon voor de andere twee.

Het zendlampje is het enige dat de bordklasse zelf initialiseert:

`src/helpers/ESP32Board.h` r.39-42

```cpp
  #ifdef P_LORA_TX_LED
    pinMode(P_LORA_TX_LED, OUTPUT);
    digitalWrite(P_LORA_TX_LED, LOW);
  #endif
```

Dat het lampje bij het zenden brandt is geen sierstukje: het is de enige
manier om aan een node zonder scherm te zien dat hij werkelijk uitzendt.

Op drie borden zit in plaats daarvan een adresseerbare RGB-LED
(`heltec_mesh_solar`, `nibble_screen_connect` en `lilygo_techo_card`, via
de Adafruit NeoPixel-library). Die valt buiten de vlaggen hierboven; wat de
library doet staat in
[Randapparatuur](../../libraries/other/peripherals.md).

## De zoemer speelt ringtones uit 1999

Veertien variantbestanden zetten een `-D PIN_BUZZER=`-regel. Wat er
klinkt is geen toonreeks in de code maar een RTTTL-string — het formaat
waarmee Nokia-telefoons ooit hun beltonen opsloegen:

`src/helpers/ui/buzzer.h` r.33-34

```cpp
        const char *startup_song = "Startup:d=4,o=5,b=160:16c6,16e6,8g6";
        const char *shutdown_song = "Shutdown:d=4,o=5,b=100:8g5,16e5,16c5";
```

Het startdeuntje is een stijgende c-e-g in het zesde octaaf op tempo 160;
het afsluitdeuntje is dezelfde drieklank omgekeerd en langzamer. De klasse
eromheen is dun en zegt dat zelf ook:

`src/helpers/ui/buzzer.h` r.6-17

```cpp
/* class abstracts underlying RTTTL library 

    Just a simple implementation to start.  At the moment use same
    melody for message and discovery
    Suggest enum type for different sounds
    - on message
    - on discovery

    TODO
    - make message ring tone configurable

*/
```

Bericht en ontdekking krijgen dus hetzelfde geluid, en instelbaar is het
niet. Dat staat er letterlijk als openstaand punt.

Afspelen gebeurt niet-blokkerend: `loop()` duwt de melodie stukje bij
beetje verder, zodat de node ondertussen gewoon pakketten kan afhandelen.
Er is één uitzetschakelaar, `quiet()`.

## Trillen

Voor borden met een trilmotor bestaat `GenericVibration`
(`src/helpers/ui/GenericVibration.h`). Geen enkel variantbestand zet op dit
moment een `-D PIN_VIBRATION=`-regel in zijn buildvlaggen; de
ondersteuning is er, het gebruik nog niet.

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`src/helpers/ui/MomentaryButton.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/MomentaryButton.h)
  — de vijf gebeurtenissen en de constructors
- [`src/helpers/ui/MomentaryButton.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/MomentaryButton.cpp)
  — het klikvenster en de pinconfiguratie
- [`src/helpers/ui/buzzer.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/buzzer.h)
  — de melodieën en het openstaande punt
- [`src/helpers/ESP32Board.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ESP32Board.h)
  — het zendlampje

Verwant in deze documentatie:

- [Het scherm](display.md) — de andere kant van de bediening
- [Randapparatuur](../../libraries/other/peripherals.md) — de libraries
  achter zoemer, NeoPixel en busexpander
- [Nodematrix](../../platform/node-matrix.md) — welk bord knoppen heeft
