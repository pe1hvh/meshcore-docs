# Library Configuratie

*OPT-OUT · OPT-IN · TYPEINJECTIE · LIB_DEPS*

Een library die in `lib_deps` staat, is nog niet af. Wat er van hem in de
firmware terechtkomt en hoe hij zich gedraagt, hangt af van macro's die de
compiler meekrijgt. Er is geen standaard voor hoe die macro's werken: de ene
library gaat ervan uit dat je alles wilt en laat je weglaten, de andere gaat
ervan uit dat je niets wilt en laat je toevoegen, en de meeste hebben helemaal
geen schakelaars. Dit hoofdstuk zet die conventies naast elkaar, want zonder
dat overzicht is een regel als `-D RADIOLIB_EXCLUDE_MORSE=1` niet te lezen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — `platformio.ini`, de
> negenenzeventig `variants/*/platformio.ini`,
> `src/helpers/sensors/EnvironmentSensorManager.cpp`,
> `src/helpers/BaseChatMesh.h` en `examples/simple_repeater/main.cpp`.
> Daarnaast tegen de librarysources zelf: RadioLib 7.6.0, de twee
> littlefs-kopieën in de bouwboom, Adafruit SSD1306, Adafruit RTClib,
> `rweather/Crypto`, ESPAsyncWebServer en CustomLFS 0.2.2.

## Zeventien vlaggen

Van alle macro's die MeshCore aan de compiler meegeeft, is een klein deel
gericht op een library. De rest is MeshCore's eigen configuratie of een
instelling voor een Arduino-core. De getallen staan onderaan in de
[inventaris](#inventaris); de kern ervan is dit: **zeventien** actieve
macro's raken een library, en **alle zeventien** staan in de root-
`platformio.ini`. De negenenzeventig variantbestanden zetten er samen nul.

Zestien van die zeventien zijn voor RadioLib, één voor littlefs.
Libraryconfiguratie in MeshCore is dus bijna volledig gecentraliseerd en
bijna volledig één library.

## Uitsluiten: de standaardtoestand is alles

RadioLib kent geen macro om een driver *aan* te zetten. De overkoepelende
header bevat een onvoorwaardelijke `#include` voor elke moduledriver en elk
protocol:

`RadioLib.h` r.76-124 (v7.6.0)

```text
#include "modules/CC1101/CC1101.h"
#include "modules/LLCC68/LLCC68.h"
...
#include "protocols/Morse/Morse.h"
#include "protocols/SSTV/SSTV.h"
```

De schakelaar zit een niveau lager, in de headers zelf, en is negatief
geformuleerd:

`Morse.h` r.1

```text
#if !defined(_RADIOLIB_MORSE_H) && !RADIOLIB_EXCLUDE_MORSE
```

Een niet-gedefinieerde macro evalueert in de preprocessor als `0`. Zonder
vlaggen is `!RADIOLIB_EXCLUDE_MORSE` dus waar en wordt de klasse
meegecompileerd. In `BuildOpt.h` staat de lijst uitsluitmacro's daarom
uitgecommentarieerd geleverd (r.182-204): insluiten is de standaardtoestand,
uitsluiten is de handeling.

De library noemt zelf twee redenen om uit te sluiten — naambotsingen met het
platform voorkomen, en de bouwtijd bekorten (`BuildOpt.h` r.177-178). Voor
MeshCore komt de flashruimte erbij: een build die op een nRF52840 moet
passen, kan geen drivers meenemen voor radio's die het bord niet heeft.

Twee dingen om te weten bij het lezen van die lijst. Ten eerste zijn de
uitsluitingen eenzijdig afhankelijk: `SX1231` erft van `RF69` en `RFM2X` van
`SI443X`, dus wie de basisklasse uitsluit verliest de afgeleide automatisch —
andersom niet (`BuildOpt.h` r.179-181). Ten tweede is de lijst in `BuildOpt.h`
niet volledig: er staan drieëntwintig macro's, terwijl de bronbestanden er
vijfentwintig gebruiken. `RADIOLIB_EXCLUDE_ADSB` en
`RADIOLIB_EXCLUDE_LR2021` (`LR2021.h` r.6) zijn ongedocumenteerd.

Dit mechaniek is niet uniek voor RadioLib. Twee andere libraries in de
bouwboom werken precies zo:

| Library | Macro | Standaard zonder macro | Zet MeshCore hem? |
|---|---|---|---|
| RadioLib 7.6.0 | `RADIOLIB_EXCLUDE_*` | alles ingesloten | veertien |
| littlefs | `LFS_NO_ASSERT` | asserts actief | ja, op nRF52 |
| Adafruit SSD1306 | `SSD1306_NO_SPLASH` | splashbitmap meegecompileerd | nee |

`arch/stm32/Adafruit_LittleFS_stm32/src/littlefs/lfs_util.h` r.77-81

```text
#ifndef LFS_NO_ASSERT
#define LFS_ASSERT(test) assert(test)
#else
#define LFS_ASSERT(test)
#endif
```

En Adafruit levert de zijne net als RadioLib uitgecommentarieerd mee:

`Adafruit_SSD1306.h` r.36

```text
// #define SSD1306_NO_SPLASH
```

Bij littlefs heeft dat mechaniek een gevolg dat de moeite waard is. Littlefs
staat in geen enkele `lib_deps`-regel — hij komt mee in andere pakketten, en
er zijn er twee. Op nRF52 die in het gevorkte Adafruit-framework, op STM32 die
in de repo zelf (`arch/stm32/Adafruit_LittleFS_stm32/src/littlefs/`). De vlag
`-D LFS_NO_ASSERT=1` staat in `[nrf52_base]` (`platformio.ini` r.91) en niet
in `[stm32_base]`. Dezelfde library, twee builds, tegengestelde toestand:
nRF52-firmware compileert littlefs zonder asserts, STM32-firmware met.
CustomLFS bevat zelf geen littlefs; het is een wrapper om
`Adafruit_LittleFS` (`CustomLFS.h` r.30) — zie
[`core/custom-lfs.md`](core/custom-lfs.md).

## Insluiten: hetzelfde probleem, omgekeerde conventie

De andere helft van RadioLibs configuratie werkt wél opt-in. `RADIOLIB_GODMODE`
en `RADIOLIB_STATIC_ONLY` staan standaard uit en voegen gedrag toe zodra je ze
definieert; zie [`core/radiolib.md`](core/radiolib.md) voor wat MeshCore
daarmee doet.

MeshCore gebruikt voor zijn eigen code consequent opt-in. De sensordrivers
zitten allemaal achter een eigen vlag:

`platformio.ini` r.123-137

```text
[sensor_base]
build_flags =
  -D ENV_INCLUDE_GPS=1
  -D ENV_INCLUDE_AHTX0=1
  -D ENV_INCLUDE_BME280=1
  ...
```

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.63

```text
#if ENV_INCLUDE_BME280
```

Zonder vlag geen driver. Dat is het spiegelbeeld van RadioLib, in dezelfde
firmware, voor hetzelfde doel — flash sparen. Wie alleen `radiolib.md` leest,
zou denken dat uitsluiten de norm is; wie alleen
[`other/sensors.md`](other/sensors.md) leest, denkt het tegendeel. Beide
conventies bestaan naast elkaar en de keuze ligt bij de auteur van de code,
niet bij MeshCore.

## Overriden: een getal met een standaardwaarde

Een derde vorm schakelt niets aan of uit maar verzet een waarde. Het patroon
is `#ifndef` met een standaard eronder, zodat een `-D` van buitenaf voorgaat.
ESPAsyncWebServer doet dit (`ESPAsyncWebServer.h` r.72), MeshCore ook:

`src/helpers/BaseChatMesh.h` r.36-38

```text
#ifndef MAX_CONTACTS
  #define MAX_CONTACTS  32
#endif
```

Deze macro's zijn niet te herkennen aan hun naam en niet te vinden door in
`platformio.ini` te zoeken: als niemand ze overschrijft, staan ze nergens in
de build en gelden ze toch. Ze zijn alleen te inventariseren door de
librarysource te lezen.

## Typeinjectie: een macro die een klassenaam draagt

De vierde vorm draagt geen `1` maar een type. `RADIO_CLASS`, `WRAPPER_CLASS`,
`DISPLAY_CLASS` en `EINK_DISPLAY_MODEL` bevatten de naam van de klasse die de
firmware moet instantiëren:

`variants/heltec_v3/platformio.ini` r.18

```text
  -D RADIO_CLASS=CustomSX1262
```

Aanwezigheid en identiteit zitten in één macro, en de firmware gebruikt beide
eigenschappen:

`examples/simple_repeater/main.cpp` r.6-8

```text
#ifdef DISPLAY_CLASS
  #include "UITask.h"
  static UITask ui_task(display);
```

`#ifdef` vraagt of er een scherm is; de waarde bepaalt welk. Dit is
MeshCore's eigen mechaniek, geen library-conventie, maar het bepaalt wél welke
displaylibrary in de build terechtkomt — zie
[`other/displays.md`](other/displays.md).

## Libraries zonder schakelaars

De meeste libraries in MeshCore hebben helemaal geen configuratiemacro's. In
`Crypto.h` van `rweather/Crypto` staat één `#ifndef`, en dat is de
include-guard. In `RTClib.h` staan acht chipklassen achter, ook, één
include-guard. Wat je krijgt, bepaal je door te includeren en te
instantiëren.

Bij zulke libraries verhuist het uitsluiten naar het niveau van de
afhankelijkheden. `adafruit/Adafruit SSD1306` staat in achtentwintig van de
negenenzeventig varianten; de andere eenenvijftig builds bevatten de library
niet omdat hij daar niet gedeclareerd is. Geen macro nodig — zie
[`dependencies.md`](dependencies.md) en
[`introduction.md`](introduction.md) voor hoe die declaraties werken.

Dat maakt `lib_deps` het krachtigste exclusiemechaniek van de vier, met één
beperking: het werkt per `[env:…]`-sectie. Vlaggen in `[arduino_base]` gelden
voor alle 507 build-targets, dus een driver die één bord nodig heeft, moet
voor alle borden blijven staan. Daarom sluit MeshCore veertien van de
vijfentwintig RadioLib-macro's uit en niet meer: de rest hoort bij chips die
ergens in de reeks wél gebruikt worden.

## Vorken

Blijft er niets over, dan verandert MeshCore de library zelf. Dat gebeurt op
vier manieren: een kopie in de repo (`lib/ed25519`, `lib/nrf52`,
`arch/esp32/AsyncElegantOTA`, `arch/stm32/Adafruit_LittleFS_stm32`), een
gevorkt framework (`platformio.ini` r.87, met de reden in het commentaar
erboven), een gevorkte library uit een andere repo
(`variants/lilygo_techo_lite/platformio.ini` r.42) en een vastgepinde
archiefdownload. Configuratie door de code te veranderen, met als prijs dat
een upstream-update niet meer automatisch binnenkomt.

## Waar de macro's binnenkomen

RadioLib biedt twee kanalen aan: `-D`-vlaggen, en een meegeleverd
configuratiebestand dat je zelf mag vullen.

`BuildOptUser.h` r.4-6

```text
// this file can be used to define any user build options
// most commonly, RADIOLIB_EXCLUDE_* macros
// or enabling debug output
```

Dat bestand wordt vanuit `TypeDef.h` r.5 geïncludeerd. MeshCore gebruikt het
niet, en dat is consistent: PlatformIO beheert de map waarin de library staat
en haalt hem bij een versiewissel opnieuw op, waarmee een handmatige
wijziging in `BuildOptUser.h` verdwijnt. Een `-D` in `platformio.ini` staat
in de repo en overleeft dat.

## Inventaris

De tabel bevat elke actieve macro in de tachtig `platformio.ini`-bestanden die
door een third-party library wordt geconsumeerd. Het eigenaarschap volgt niet
uit de naam, dus het komt uit een tabel in het script waarin per namespace is
vastgelegd welk bronbestand de macro leest; die verwijzingen zijn met de hand
tegen de librarysource gecontroleerd. Uitgecommentarieerde regels tellen niet
mee: een `; -D RADIOLIB_DEBUG_SPI=1` zit in geen enkele build.

<!-- config-flags:start -->

*Gegenereerd met `tools/config-flags.py` tegen commit `03b6ef4`.*

| Macro | Library | Mechaniek | Sectie | Waar |
|---|---|---|---|---|
| `LFS_NO_ASSERT` | `littlefs (via Adafruit_LittleFS)` | uitsluiten | `[nrf52_base]` | root |
| `RADIOLIB_EXCLUDE_AFSK` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_APRS` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_AX25` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_BELL` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_CC1101` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_HELLSCHREIBER` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_MORSE` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_RF69` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_RFM2X` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_RTTY` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_SI443X` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_SSTV` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_SX1231` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_SX128X` | `jgromes/RadioLib` | uitsluiten | `[arduino_base]` | root |
| `RADIOLIB_GODMODE` | `jgromes/RadioLib` | insluiten | `[arduino_base]` | root |
| `RADIOLIB_STATIC_ONLY` | `jgromes/RadioLib` | insluiten | `[arduino_base]` | root |

Van de 277 unieke `-D`-macro's in de tachtig `platformio.ini`-bestanden zijn er 17 op een library gericht, 6 op een Arduino-core of platform, en 254 op MeshCore's eigen code.

Uitgecommentarieerd, dus in geen enkele build actief: `RADIOLIB_DEBUG_BASIC`, `RADIOLIB_DEBUG_SPI`.

<!-- config-flags:end -->

De tabel dekt alleen wat in `platformio.ini` staat. Overridemacro's die
nergens overschreven worden en libraries zonder schakelaars komen er niet in
voor; die zijn per definitie onzichtbaar in de buildconfiguratie.

![Vier mechanieken naast elkaar: uitsluiten begint bij alles en haalt weg,
insluiten begint bij niets en voegt toe, overriden verzet een standaardwaarde
en typeinjectie draagt een klassenaam; onderaan lib_deps als exclusie op
projectniveau](../../images/nl/library-configuration-1.svg)

## Wat het voor een node betekent

Wat een node kan, staat vast op het moment dat de firmware gebouwd wordt. Er
is geen instelling die een uitgesloten protocol terugbrengt of een niet
gedeclareerde library alsnog laadt. Wie iets mist, bouwt zelf — en moet dan
weten welk van de vier mechanieken bij de betrokken library hoort, want
`-D IETS_ENABLE=1` toevoegen werkt niet als de library `IETS_EXCLUDE`
verwacht.

De zeventien vlaggen in dit hoofdstuk zijn het deel van de 277 `-D`-macro's
dat bij een library uitkomt. De andere 260 — zes voor een Arduino-core en 254
voor MeshCore zelf — staan in
[Compile-time configuratie](../ontwerp/technisch/configuration.md), samen met
de bevinding dat 53 daarvan nergens worden gelezen.

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/EnvironmentSensorManager.cpp)
- [`src/helpers/BaseChatMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/BaseChatMesh.h)
- [`examples/simple_repeater/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/main.cpp)
- [`RadioLib 7.6.0 — BuildOpt.h`](https://github.com/jgromes/RadioLib/blob/7.6.0/src/BuildOpt.h)
- [`RadioLib 7.6.0 — BuildOptUser.h`](https://github.com/jgromes/RadioLib/blob/7.6.0/src/BuildOptUser.h)
- [`Adafruit_SSD1306.h`](https://github.com/adafruit/Adafruit_SSD1306/blob/master/Adafruit_SSD1306.h)
- [`arch/stm32/Adafruit_LittleFS_stm32/src/littlefs/lfs_util.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/arch/stm32/Adafruit_LittleFS_stm32/src/littlefs/lfs_util.h)
- [`Adafruit_nRF52_Arduino — Adafruit_LittleFS/src/littlefs/lfs_util.h`](https://github.com/meshcore-dev/Adafruit_nRF52_Arduino/blob/d541301/libraries/Adafruit_LittleFS/src/littlefs/lfs_util.h)
- [`oltaco/CustomLFS`](https://github.com/oltaco/CustomLFS)
