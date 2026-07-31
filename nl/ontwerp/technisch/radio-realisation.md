# Radiorealisatie

*KOPPELPUNT · CHIPDRIVER · WRAPPER · ESP-NOW*

De radio is de enige hardware-abstractie waar de kern zelf de implementatie
niet kiest. Dit hoofdstuk laat zien waar die keuze wél wordt gemaakt — in de
variant, niet in de kern — en waarom er per radiochip twee klassen bestaan in
plaats van één. Dat laatste is geen dubbeling maar een taakverdeling.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — `src/Dispatcher.h`,
> `src/helpers/radiolib/`, `src/helpers/esp32/ESPNOWRadio.h` en de
> `target.h`-bestanden in `variants/`.

## Het contract

`mesh::Radio` staat in `src/Dispatcher.h` op regel 22. Het legt vast dat er
iets moet zijn dat bytes verstuurt en ontvangt, de zendtijd van een pakket kan
schatten en de signaalsterkte van het laatste ontvangen pakket kan melden. Wat
er onder hangt weet het niet.

De pakketafhandeling houdt een `Radio*` vast. Verder komt de abstractie niet:
nergens in `src/` of `examples/` staat een regel die bepaalt wélke radio dat
is.

## Het koppelpunt ligt in de variant

`RADIO_CLASS` en `WRAPPER_CLASS` zijn de twee macro's die de radiokeuze
dragen. In de gedeelde broncode worden ze **nergens gelezen**. De enige
treffers zijn vier commentaarregels in `src/helpers/esp32/TBeamBoard.cpp`:
`RADIO_CLASS` op r.313 en r.334, `WRAPPER_CLASS` op r.314 en r.335.
Uitgecommentarieerde code, geen werkende.

De macro's worden geconsumeerd in `variants/*/target.h` en
`variants/*/target.cpp`:

`variants/heltec_v3/target.h` r.16-24

```cpp
extern HeltecV3Board board;
extern WRAPPER_CLASS radio_driver;
extern AutoDiscoverRTCClock rtc_clock;
extern EnvironmentSensorManager sensors;

#ifdef DISPLAY_CLASS
  extern DISPLAY_CLASS display;
  extern MomentaryButton user_btn;
#endif
```

De applicatie includeert `target.h` en gebruikt `radio_driver` als globale
variabele. Het koppelpunt ligt dus in de variant, niet in de kern — precies
omgekeerd aan wat je bij een abstractielaag zou verwachten. Normaal krijgt de
kern een implementatie aangereikt; hier definieert de rand een globale
variabele waarvan de kern aanneemt dat hij bestaat.

![Van links naar rechts: platformio.ini definieert RADIO_CLASS en
WRAPPER_CLASS als buildvlag; target.h in de variantmap gebruikt WRAPPER_CLASS
om de globale variabele radio_driver te declareren; de applicatie in examples
includeert target.h en geeft radio_driver door aan de pakketafhandeling, die
alleen een mesh::Radio-verwijzing
ziet.](../../../images/nl/radio-realisation-1.svg)

Dat verklaart waarom de radio niet in de driedeling van
[het klassenmodel](class-model.md) past zoals de andere abstracties. Bij het
bord kiest de variant een klasse die van een gedeelde ouder erft; bij de radio
kiest de variant een klasse én de naam waaronder de kern hem terugvindt.

## Chipdriver en MeshCore-wrapper

Per radiochip bestaan er twee klassen, en dat is opzet.

| Chip | Aangepaste driver | Implementatie | Targets |
|---|---|---|---|
| SX1262 | `CustomSX1262` | `CustomSX1262Wrapper` | 424 |
| SX1276 | `CustomSX1276` | `CustomSX1276Wrapper` | 29 |
| LR1110 | `CustomLR1110` | `CustomLR1110Wrapper` | 20 |
| STM32WLx | `CustomSTM32WLx` | `CustomSTM32WLxWrapper` | 16 |
| SX1268 | `CustomSX1268` | `CustomSX1268Wrapper` | 12 |
| LLCC68 | `CustomLLCC68` | `CustomLLCC68Wrapper` | **0** |

De linkerkolom erft van RadioLib. `CustomSX1262` is een `SX1262` van RadioLib
met aanpassingen; hij weet niets van MeshCore en vult geen MeshCore-contract
in. Daarom staat hij in groep 3 van het klassenmodel, bij de zelfstandige
klassen.

De rechterkolom erft van `RadioLibWrapper`, die op zijn beurt `mesh::Radio`
implementeert. Dat is de klasse die het contract draagt. De scheiding houdt de
RadioLib-aanpassingen los van de MeshCore-afspraak: wie de chipdriver moet
bijsturen raakt de linkerkolom aan, wie iets aan de mesh-kant verandert de
rechter.

![Twee kolommen. Links de RadioLib-stamboom: PhysicalLayer met daaronder de
zes chipklassen en daaronder de zes Custom-drivers. Rechts de MeshCore-kant:
mesh::Radio met daaronder RadioLibWrapper en daaronder de zes Wrapper-klassen.
Een horizontale pijl loopt van elke Custom-driver naar de bijbehorende
Wrapper, die hem als PhysicalLayer-verwijzing
vasthoudt.](../../../images/nl/radio-realisation-2.svg)

## LLCC68 bestaat en wordt niet gebruikt

`CustomLLCC68` en `CustomLLCC68Wrapper` bestaan volledig — header, klasse,
alles wat de andere vijf paren ook hebben — en worden door **geen enkel**
buildtarget gekozen. Van de 508 targets stelt geen enkele `RADIO_CLASS` in op
`CustomLLCC68`.

Dat is geen dode code in de zin van onbereikbare code; het is werkende code
zonder afnemer. De LLCC68 is een goedkopere variant van de SX1262 met een
beperkter frequentiebereik, en er is kennelijk ooit een bord voorzien dat er
niet gekomen is. Wie er een toevoegt, hoeft alleen `RADIO_CLASS` en
`WRAPPER_CLASS` in zijn `platformio.ini` te zetten.

Zeven van de 508 targets stellen helemaal geen radioklasse in. Dat zijn de
targets die geen LoRa gebruiken, plus `[env:native]` voor de tests.

## `RadioLibWrapper` zelf

`src/helpers/radiolib/RadioLibWrappers.h` r.6. Erft van `mesh::Radio` en houdt
twee verwijzingen vast: een `PhysicalLayer*` naar de RadioLib-driver, en een
`mesh::MainBoard*` naar het bord.

Die tweede is het vermelden waard. Een radiowrapper die het bord kent, klinkt
als een laagschending, maar er is een reden: op veel borden moet er vóór het
zenden iets geschakeld worden — een antenneschakelaar, een
zend-ontvangstschakelaar, een LED — en na afloop weer terug. Het bord krijgt
daarom een seintje voor en na elke uitzending.

In hetzelfde bestand staat op regel 74 `RadioNoiseListener`, die `mesh::RNG`
implementeert: de ruis van de radio-ontvanger als bron van willekeur. Dat is
de reden dat de entropiebron in het logisch ontwerp een eigen component is en
niet een detail van de radio.

## Buiten het schema: ESP-NOW

`ESPNOWRadio` (`src/helpers/esp32/ESPNOWRadio.h` r.5) vult `mesh::Radio`
rechtstreeks in, zonder RadioLib en zonder wrapper. Hij gebruikt geen LoRa
maar ESP-NOW, het 2,4 GHz-protocol van Espressif.

Dat het contract dat toelaat, is het beste bewijs dat de abstractie deugt: de
pakketafhandeling merkt niet dat er onder zijn `Radio*` geen LoRa-chip maar een
WiFi-radio zit. Bereik en gedrag verschillen volledig, het contract niet.

Verwar `ESPNOWRadio` niet met `ESPNowBridge` (`src/helpers/bridges/`). De
eerste is een radio waarover het mesh-protocol loopt; de tweede is een brug
die twee netwerken koppelt.

## Narekenen

De targetaantallen in dit hoofdstuk komen uit `tools/design-overview.py`:

```bash
python3 tools/design-overview.py /pad/naar/MeshCore
```

Het script leest per `[env:...]`-sectie de opgeloste waarde van `RADIO_CLASS`
en `WRAPPER_CLASS`, met `extends` en `${sectie.optie}` uitgewerkt. Tellen op de
naam van een sectie geeft een ander antwoord; waarom dat fout is, staat in
[Variabiliteit](../logisch/variability.md).

## Bronnen

- [MeshCore `03b6ef4` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Dispatcher.h)
- [MeshCore `03b6ef4` — `src/helpers/radiolib/RadioLibWrappers.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/radiolib/RadioLibWrappers.h)
- [MeshCore `03b6ef4` — `src/helpers/esp32/ESPNOWRadio.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/esp32/ESPNOWRadio.h)
- [MeshCore `03b6ef4` — `src/helpers/esp32/TBeamBoard.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/esp32/TBeamBoard.cpp)
- [MeshCore `03b6ef4` — `variants/heltec_v3/target.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/heltec_v3/target.h)
