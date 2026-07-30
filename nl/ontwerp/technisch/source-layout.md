# De bronboom

*SRC · HELPERS · EXAMPLES · VARIANTS · SCHEEFHEID*

De MeshCore-bronboom valt in vier stukken uiteen: een kern van elf bestanden,
een verzameling hulpklassen, zes applicaties en negenenzeventig
variantmappen. Dit hoofdstuk beschrijft wat waar staat en hoeveel het is. De
interessantste bevinding zit niet in de aantallen zelf maar in hun
scheefheid: de ene platformfamilie heeft acht gedeelde bestanden, de andere
geen enkel.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — de volledige bronboom onder
> `src/`, `examples/` en `variants/`.

## De vier stukken

![Vier blokken naast elkaar. Links de kern src met elf bestanden, daarnaast
src/helpers met achtendertig losse bestanden en zeven onderliggende mappen,
vervolgens examples met zes applicaties, en rechts variants met
negenenzeventig mappen. Pijlen lopen van rechts naar links: elke variant kiest
uit helpers, elke applicatie gebruikt de kern.](../../../images/nl/source-layout-1.svg)

| Locatie | Inhoud |
|---|---|
| `src/` | 5 headerparen plus `MeshCore.h`; 14 klassen; 2332 regels |
| `src/helpers/` | 38 losse bestanden, 33 klassen |
| `src/helpers/bridges/` | 3 klassen — `BridgeBase`, `ESPNowBridge`, `RS232Bridge` |
| `src/helpers/esp32/` | 4 klassen — ESP-NOW-radio, BLE, WiFi, T-Beam-bord |
| `src/helpers/nrf52/` | 1 klasse — alleen `SerialBLEInterface` |
| `src/helpers/stm32/` | 1 klasse — alleen `STM32Board` |
| `src/helpers/radiolib/` | 14 klassen, 16 bestanden |
| `src/helpers/sensors/` | 6 klassen |
| `src/helpers/ui/` | 18 klassendeclaraties, deels gevendorde code |
| `examples/` | 6 applicaties, 25 klassen |
| `variants/` | 79 directory's, 77 klassen |

De 119 klassen in `src/` en `examples/` samen vormen de gedeelde boom: code
die in elke build kan meedoen. De 77 in `variants/` horen bij precies één
bord. Samen 196. Hoe die 196 zijn ingedeeld staat in
[Het klassenmodel](class-model.md).

> [!NOTE]
> **Telmethode.** Geteld is elke regel van de vorm `class Naam { …` of
> `class Naam : basis { …`, waarbij de accolade op dezelfde regel staat.
> `struct`-declaraties tellen niet mee: dat zijn gegevensrecords, geen
> onderdelen van het ontwerp. Een voorwaartse declaratie zonder body telt
> evenmin. Het script `tools/design-overview.py --classes` reproduceert de
> tabel hierboven.

## De kern

`src/` bevat vijf paren van een header en een implementatiebestand —
`Dispatcher`, `Identity`, `Mesh`, `Packet`, `Utils` — plus `MeshCore.h`, dat
geen eigen `.cpp` heeft. In dat ene extra bestand staan de twee contracten
die de hardware afdekken: `MainBoard` op regel 45 en `RTCClock` op regel 80.

Elf bestanden, 2332 regels. Dat is de hele gedeelde kern van een firmware die
in 508 varianten wordt gebouwd. Alles wat groter is, staat eronder in
`helpers/`, of ernaast in `variants/`.

## Helpers, en waarom er zeven ondermappen zijn

De 38 bestanden direct onder `src/helpers/` zijn de onderdelen die niet
platformgebonden zijn: de rechtenlijst, de opslag, de bediening, de
regiotabel, de pakketvoorraad. De zeven ondermappen zijn dat wel, of ze horen
bij één onderwerp:

| Map | Waarom apart |
|---|---|
| `bridges/` | Onderwerp: koppeling tussen twee netwerken |
| `radiolib/` | Onderwerp: alles wat RadioLib aanpast of inpakt |
| `sensors/` | Onderwerp: meetwaarden en locatie |
| `ui/` | Onderwerp: schermen en knoppen |
| `esp32/` | Platform: code die alleen op ESP32 compileert |
| `nrf52/` | Platform: idem voor nRF52 |
| `stm32/` | Platform: idem voor STM32 |

## De scheefheid tussen de platformmappen

Dit is het punt van dit hoofdstuk. De drie platformmappen zijn extreem
ongelijk gevuld, en er is een vierde familie die er helemaal geen heeft.

| Familie | Platformmap | Klassen daarin | Buildtargets |
|---|---|---|---|
| ESP32 | `src/helpers/esp32/` | 4 | 270 |
| nRF52 | `src/helpers/nrf52/` | 1 | 199 |
| STM32 | `src/helpers/stm32/` | 1 | 16 |
| RP2040 | geen | — | 22 |

De verleiding is om dit te lezen als een maat voor ondersteuning: ESP32 goed
ondersteund, RP2040 stiefmoederlijk. Dat klopt niet. nRF52 draagt 199
buildtargets met één gedeelde klasse in zijn platformmap, en die targets
werken. Wat de tabel meet is hoeveel er te delen viel.

ESP32 heeft vier klassen in zijn platformmap omdat ESP32-chips iets kunnen
wat de andere niet kunnen: BLE én WiFi én ESP-NOW, elk met een eigen
koppelvlakklasse. Dat zijn onderwerpen, geen platformverschillen. nRF52 heeft
alleen BLE en dus alleen `SerialBLEInterface`. RP2040 heeft geen van drieën en
houdt niets over om te delen; zijn vier bordklassen staan los in `variants/`.
Zie [Platformrealisatie](platform-realisation.md).

## Gevendorde code in `src/helpers/ui/`

Achttien klassendeclaraties in `ui/` is meer dan het aantal schermdrivers, en
dat komt doordat niet alles in die map van MeshCore is. `OLEDDisplay.h`
bevat code van ThingPulse, letterlijk overgenomen in plaats van als library
opgenomen.

Dat is aan twee dingen te zien. Ten eerste staat `OLEDDisplay` twee keer in
hetzelfde bestand, op regel 159 en regel 161, achter een `#if`: de ene versie
erft van `Print`, de andere van `Stream`. Ten tweede staat op regel 50 een
declaratie van `String` — een vooruitverwijzing die alleen zin heeft binnen de
oorspronkelijke codebase.

> [!NOTE]
> Beide zijn geen MeshCore-ontwerp. Ze staan in de telling omdat ze
> declaraties in de bronboom zijn, maar wie het klassenmodel leest moet weten
> dat drie van de achttien uit overgenomen code komen. Waar MeshCore
> libraries wél als library opneemt, staat in
> [Libraries in MeshCore](../../libraries/introduction.md).

## `examples/` is geen voorbeeldmap

De naam is misleidend. `examples/` bevat de zes applicaties die MeshCore kan
zijn — companion radio, repeater, room server, sensor, terminal chat en
KISS-modem — en elke build compileert er precies één van. Het zijn geen
demonstraties naast het product; ze zíjn het product.

Vijfentwintig klassen, waarvan een groot deel schermtaken (`UITask` komt zes
keer voor, in zes applicaties) en vijf keer een klasse die letterlijk `MyMesh`
heet. Welke rol elke applicatie vervult staat in
[Rollen](../logisch/roles.md).

## `variants/`: 79 mappen, 77 klassen

Elke map onder `variants/` beschrijft één bord: welke pinnen waar zitten,
welke radiochip erop zit, welk scherm eraan hangt. Twee mappen bevatten geen
klasse — die leveren alleen een `platformio.ini` en een `target.h`.

De 77 klassen daarin zijn opvallend eenvormig: 65 bordklassen, 7
sensorbeheerders, 3 schermen en 2 toevalsbronnen. Ze vullen alle een contract
in dat in de gedeelde boom is vastgelegd. Dat maakt ze samen goed voor 39 %
van alle klassen in de firmware, terwijl er nauwelijks ontwerp in zit — het is
bijna allemaal pinbezetting.

## Bronnen

- [MeshCore `03b6ef4` — `src/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/src)
- [MeshCore `03b6ef4` — `src/helpers/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/src/helpers)
- [MeshCore `03b6ef4` — `src/helpers/ui/OLEDDisplay.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/OLEDDisplay.h)
- [MeshCore `03b6ef4` — `examples/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/examples)
- [MeshCore `03b6ef4` — `variants/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/variants)
