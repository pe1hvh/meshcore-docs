# Terugkoppeling

*MOMENTARYBUTTON · VIJF GEBEURTENISSEN · RTTTL · TRILLING · ZENDLAMPJE*

De eenvoudigste onderdelen van een node zijn ook de enige waarmee je hem
bedient en uitleest zonder telefoon. Eén knop, een lampje, soms een zoemer en
soms een trilmotor. Dit hoofdstuk beschrijft hoe de firmware vijf
verschillende gebeurtenissen uit één knop haalt, welke lampjes er zijn, welk
melodietje er bij het opstarten klinkt en langs welke twee wegen een node kan
trillen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.17.1, commit `d929643`, 14 augustus 2026 — bestanden
> `src/helpers/ui/MomentaryButton.h`, `src/helpers/ui/MomentaryButton.cpp`,
> `src/helpers/ui/buzzer.h`, `src/helpers/ui/GenericVibration.h`,
> `src/helpers/ui/DRV2605Vibration.h`, `src/helpers/ESP32Board.h`,
> de drie `UITask`-varianten onder `examples/companion_radio/` en de
> pinvlaggen in `variants/`.

> [!NOTE]
> De tekening bij dit hoofdstuk heet `buttons-and-leds-1.svg` en niet
> `feedback-1.svg`. Dat is geen vergissing. `IMAGES.md` bepaalt dat
> beeldbestanden nooit worden verplaatst of hernoemd, ook niet wanneer de slug
> van het hoofdstuk verandert; de bestandsnaam en de slug lopen daardoor
> uiteen.

## Vijf gebeurtenissen uit één knop

De meeste MeshCore-borden hebben precies één bedienbare knop.
Zevenenveertig variantbestanden zetten een `-D PIN_USER_BTN=`-regel, samen
vijftig regels — `rak4631` zet de vlag vier keer, in vier verschillende
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
| `P_LORA_TX_LED` | 49 | 45 | brandt tijdens zenden |
| `PIN_STATUS_LED` | 9 | 9 | statusindicatie |
| `PIN_LED` | 1 | 1 | algemeen lampje |

Te herhalen met `grep -rh -- "-D P_LORA_TX_LED=" variants/ | grep -v "^\s*;" | wc -l`
en hetzelfde patroon voor de andere twee.

Het zendlampje is het enige dat de bordklasse zelf initialiseert:

`src/helpers/ESP32Board.h` r.40-43

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

Achttien variantbestanden zetten een `-D PIN_BUZZER=`-regel, samen
zesentwintig regels. Wat er klinkt is geen toonreeks in de code maar een
RTTTL-string — het formaat
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

Een melding hoeft niet hoorbaar te zijn. Naast de zoemer kent de firmware een
trilmotor: dezelfde soort melding, langs een ander zintuig. Daarom staat deze
sectie hier, direct naast de RTTTL-melodieën.

Er zijn twee uitvoeringen, met hetzelfde doel en een heel verschillende
mechaniek:

| Klasse | Plek | Mechaniek | Hoort bij |
|---|---|---|---|
| `GenericVibration` | `src/helpers/ui/GenericVibration.h` r.21 | schakelt een pin aan en weer uit | `ui-new`, `ui-tiny` |
| `DRV2605Vibration` | `src/helpers/ui/DRV2605Vibration.h` r.22 | een aanstuurchip op I²C speelt een effect uit zijn eigen bibliotheek af | `ui-orig` |

Beide wachten `VIBRATION_TIMEOUT` — 5000 milliseconde — tussen twee
trillingen (`src/helpers/ui/GenericVibration.h` r.18). De eerste schakelt
alleen de pin `PIN_VIBRATION`; de tweede stuurt effectnummer 16 naar de chip,
"1000 ms alert" uit de effectbibliotheek van de DRV2605 — zie
`DRV2605_EFFECT` in `src/helpers/ui/DRV2605Vibration.h` r.19.

`DRV2605Vibration` kan twee dingen die `GenericVibration` niet kan. De
trilling tijdelijk onderdrukken met `quiet(bool)`, en die stand opvragen met
`isQuiet()` (`src/helpers/ui/DRV2605Vibration.h` r.29 en r.30). En een
trilling forceren voorbij de wachttijd, via de parameter `force` op
`trigger()` (r.25). Het eerste is geen sierstukje: `ui-orig` gebruikt het om
met driemaal drukken door de meldingsstanden te lopen — zoemer én trilling,
alleen zoemer, alleen trilling, stil.

### Welke van de twee erin zit, hangt aan de UI-variant

Dit is de kernvaststelling van deze sectie. Niet het bord kiest tussen de twee
klassen, maar de gekozen UI-variant. Elke variant kent er precies één:

| UI-variant | Klasse | Plek |
|---|---|---|
| `ui-orig` | `DRV2605Vibration` | `examples/companion_radio/ui-orig/UITask.h` r.18 |
| `ui-new` | `GenericVibration` | `examples/companion_radio/ui-new/UITask.h` r.19 |
| `ui-tiny` | `GenericVibration` | `examples/companion_radio/ui-tiny/UITask.h` r.22 |

Het bord bepaalt iets anders: óf er überhaupt een trilmotor is. Beide klassen
zitten volledig in een `#ifdef` — `GenericVibration` in `PIN_VIBRATION`,
`DRV2605Vibration` in `HAS_DRV2605`. Zonder die vlag blijft de klasse leeg en
compileert er niets van mee.

> [!NOTE]
> **Op de gepinde commit heeft één bord werkende trilling.**
> `meshtracker_x1` zet `HAS_DRV2605` aan
> (`variants/meshtracker_x1/platformio.ini` r.86) en neemt `ui-orig`. Bij
> `gat562_mesh_watch13` staat `GenericVibration.cpp` wel in het
> `build_src_filter`, maar de vlag `PIN_VIBRATION` staat uitgecommentarieerd
> (`variants/gat562_mesh_watch13/platformio.ini` r.77). Uitgecommentarieerd
> telt niet mee: dat bord trilt niet. Te herhalen met
> `tools/hardware-overview.py`, sectie 9b.

### Wanneer er getrild wordt, verschilt per variant

De twee varianten trillen niet op hetzelfde moment, en dat is geen detail.

`ui-orig` trilt alleen bij een nieuw bericht, in `UITask::newMsg`
(`examples/companion_radio/ui-orig/UITask.cpp` r.142) — ook wanneer de app
verbonden is.

`ui-new` en `ui-tiny` trillen in `UITask::notify`
(`examples/companion_radio/ui-new/UITask.cpp` r.622 en
`examples/companion_radio/ui-tiny/UITask.cpp` r.476), bij elke `UIEventType`
behalve `none`. Dat zijn er vijf: `contactMessage`, `channelMessage`,
`roomMessage`, `newContactMessage` en `ack`. Waar `ui-orig` één keer trilt,
trillen de andere twee dus ook bij een ontvangstbevestiging.

## Bronnen

Firmware, commit `d929643` (v1.17.1, 14 augustus 2026):

- [`src/helpers/ui/MomentaryButton.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/MomentaryButton.h)
  — de vijf gebeurtenissen en de constructors
- [`src/helpers/ui/MomentaryButton.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/MomentaryButton.cpp)
  — het klikvenster en de pinconfiguratie
- [`src/helpers/ui/buzzer.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/buzzer.h)
  — de melodieën en het openstaande punt
- [`src/helpers/ui/GenericVibration.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/GenericVibration.h)
  — de pingestuurde trilling en de wachttijd
- [`src/helpers/ui/DRV2605Vibration.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/DRV2605Vibration.h)
  — de I²C-aanstuurchip, het effectnummer en `quiet()`
- [`src/helpers/ESP32Board.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ESP32Board.h)
  — het zendlampje

Verwant in deze documentatie:

- [Het scherm](display.md) — de andere kant van de bediening
- [Randapparatuur](../../libraries/other/peripherals.md) — de libraries
  achter zoemer, NeoPixel en busexpander
- [Nodematrix](../../platform/node-matrix.md) — welk bord knoppen heeft
