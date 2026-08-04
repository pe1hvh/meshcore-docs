# Filters

*DESENSITISATIE · FILTERTYPEN · PLAATSING · WANNEER HET LOONT*

Een node die naast een zendmast staat kan volstrekt gezond zijn en toch
vrijwel niets horen. De chip is heel, de antenne is goed afgeregeld, de
firmware klopt — en de ontvanger is doof, omdat er zoveel vermogen op de
ingang staat dat hij zijn eigen band niet meer schoon kan verwerken. Dit
hoofdstuk beschrijft hoe dat werkt, welke filters er bestaan, wat ze wel
en niet doen, en hoe je vooraf uitrekent of een filter in jouw geval winst
oplevert of juist verlies.

> [!NOTE]
> **Bron.** Vrijwel niets op deze pagina komt uit de MeshCore-firmware. Uit
> de firmware komen alleen de radioparameters en de ondergrens van de
> gemeten ruisvloer: `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026,
> bestand `src/helpers/radiolib/RadioLibWrappers.cpp`. De mastgegevens
> komen uit het openbare Antenneregister. Al het overige is algemene
> radiotechniek, en de niveauschattingen zijn berekeningen met expliciete
> aannames — geen metingen. Elk cijfer is herrekenbaar met
> [`tools/filter-planning.py`](../../../tools/filter-planning.py).

## Waarom een ontvanger doof wordt

De gevoeligheid van een LoRa-ontvanger is de ruisvloer plus de SNR die de
gekozen spreidingsfactor nodig heeft. Zie [Linkbudget](link-budget.md) voor
die som. Wat daar als een vast getal staat, is het in de praktijk niet: de
ruisvloer is geen eigenschap van de chip maar van de chip *op die plek*.

Zet dezelfde node naast een opstelpunt van een mobiele operator en de vloer
loopt op. Niet omdat er iets op 869 MHz zendt, maar omdat de versterker en
de menger in de ontvangketen al het vermogen te verwerken krijgen dat de
antenne binnenhaalt — over het hele spectrum, niet alleen in de 62,5 kHz
waar je in geïnteresseerd bent. Die verhoging heet **desensitisatie**.

Hoeveel vermogen dat is, laat zich schatten. Een opstelpunt in Zwolle met
antennes op 30,4 m draagt volgens het Antenneregister acht banden, van 773
tot 3700 MHz, met vermogens tot 48,2 dBW. Bij een schuine afstand van 40 m
en 25 dB onderdrukking onder de hoofdbundel komt dat neer op:

| Band | MHz | dBW | Aan de ingang |
|---|---|---|---|
| 5G n28 | 773 | 34,0 | −23,3 dBm |
| 4G B20 | 816 | 34,5 | −23,2 dBm |
| 2G/4G 900 | 940 | 34,9 | −24,1 dBm |
| L-band SDL | 1474,5 | 36,4 | −26,5 dBm |
| 4G B3 | 1815 | 39,2 | −25,5 dBm |
| 5G n1 | 2160 | 40,5 | −25,7 dBm |
| 4G/5G 2600 | 2660 | 35,9 | −32,1 dBm |
| 5G n78 | 3700 | 48,2 | −22,7 dBm |
| **composiet** | | | **−15,6 dBm** |

Dat is één sector; drie sectoren samen liggen enkele dB hoger. De afstand
en de patroononderdrukking zijn aannames en geen metingen — verander de
onderdrukking in 15 of 35 dB en de hele tabel schuift 10 dB mee. Wat de
tabel wél laat zien is de orde van grootte: enkele tientallen dB boven het
niveau waarop een ontvangeringang zonder voorselectie nog netjes lineair
blijft.

![Frequentiekaart van de zenders op een GSM-mast ten opzichte van 869,618
MHz, met de tweede-orde verschilproducten die op de SRD-band
landen](../../../images/nl/filters-1.svg)

*Balkhoogte is evenredig met het geregistreerde vermogen. Geen enkele
draaggolf ligt dicht bij 869,618 MHz — de dichtstbijzijnde staat 54 MHz
weg. Het probleem zit niet in nabijheid maar in totaal vermogen.*

## Vier manieren waarop het misgaat

**Blokkering.** De versterking van de ontvangketen regelt op het totale
vermogen op de ingang, niet op wat er in je kanaal zit. Sterke signalen ver
buiten je band drukken de versterking omlaag en tillen de effectieve
ruisvloer op. Dit is de meest voorkomende oorzaak en de enige waar een
filter altijd tegen helpt. ETSI kent hier een eis voor: EN 300 220-1
beschrijft blokkering en verdeelt ontvangers in categorieën, waarbij
categorie 1 de hoogste eisen stelt en categorie 3 de laagste.

**Tweede-orde intermodulatie.** Zodra de ingang niet meer lineair is, gaan
sterke signalen met elkaar mengen. Het verschil van twee zenders kan precies
in je band vallen. Voor dit opstelpunt geldt:

| Paar | Blokbreedte ±10 MHz | Nominale banddownlink |
|---|---|---|
| 1815 − 940 | 855–895 MHz — **raak** | 845–955 MHz — **raak** |
| 2660 − 1815 | 825–865 MHz — mis | 740–885 MHz — **raak** |

Het verschil tussen de 1800- en de 900-band landt onder elke redelijke
aanname op 869,618 MHz. Het verschil tussen 2600 en 1800 hangt af van de
werkelijke kanaalbreedtes: het register geeft voor 4G en 5G alleen een
middenfrequentie, geen bandbreedte. Neem je de blokken smal, dan mis je net;
neem je de nominale banden, dan raak je. Dat product is dus een kandidaat,
geen zekerheid.

> [!NOTE]
> **De norm laat dit bewust open.** EN 300 220-2 stelt geen eis aan
> intermodulatie, om het testen eenvoudig te houden; de redenering is dat de
> blokkeringseis het vermogen om sterke buiten-band signalen te verwerken al
> afdekt. De norm voegt daar zelf aan toe dat fabrikanten het risico op
> intermodulatie moeten beoordelen bij opstelling naast krachtige zenders.
> Precies de situatie die dit hoofdstuk beschrijft.

**Zenderruis.** Elke zender produceert breedbandige ruis buiten zijn eigen
kanaal. Basisstations zijn daar goed op gefilterd, dus dit is de minst
waarschijnlijke van de vier — maar bij honderden kilowatts opgeteld
uitgestraald vermogen is de bijdrage niet per definitie nul.

**Passieve intermodulatie.** Sterke velden die op corroderende metaal-op-
metaalovergangen vallen — bouten, hekwerk, regenpijp, beugelwerk —
produceren daar mengproducten die vervolgens opnieuw uitgestraald worden.
In de vakliteratuur heet dit het roestige-boutverschijnsel, en het is een
erkende oorzaak van ontvangerverstoring op zendmasten. Dit is de vervelende
variant: het product ontstaat *buiten* je node en zit al op 869 MHz voordat
enig filter eraan te pas komt.

## Wat een filter is

Een filter laat een band door en dempt de rest. Vier getallen beschrijven
hem volledig.

![Doorlaatkarakteristiek van een bandfilter met invoegverlies, onderdrukking
en een spurious doorlaat bij drie keer de
middenfrequentie](../../../images/nl/filters-2.svg)

*Schematisch. Het invoegverlies is overdreven getekend om het zichtbaar te
maken; in werkelijkheid is het een paar dB tegenover tientallen dB
onderdrukking.*

**Doorlaatband** — waar het signaal doorheen mag. Voor MeshCore in Europa is
dat de SRD-band 863–870 MHz. Smaller ontwerpen levert scherpere flanken,
maar maakt je gevoelig voor afstemming en temperatuur.

**Invoegverlies** — wat je in de doorlaatband kwijtraakt. Dit veroorzaakt
rechtstreeks verlies aan gevoeligheid en zendvermogen, dus het telt dubbel.

**Onderdrukking** — wat er buiten de band wegvalt. Het getal alleen zegt
niets; je moet weten *over welk frequentiebereik* het geldt. Een filter dat
40 dB haalt tot 2 GHz en daarboven openstaat is voor een opstelling naast
een 3700 MHz-zender niet bruikbaar.

**Vermogensgrens** — hoeveel het filter aan zendvermogen verdraagt. De
SX1262 levert maximaal 22 dBm; een filter dat tot +20 dBm is gespecificeerd
dwingt je het zendvermogen te begrenzen.

## De resonator

Vier van de vijf typen in de volgende paragraaf zijn opgebouwd uit hetzelfde
onderdeel. Wie dat kent, ziet meteen waarom ze in Q, invoegverlies en volume
zo uiteenlopen — en waarom ze allemaal dezelfde valkuil delen.

![Doorsnede van een kwartgolfresonator: een binnengeleider in een afgesloten
metalen kast, onderaan kortgesloten tegen de wand, met een afstemschroef boven
het vrije uiteinde en twee koppellussen](../../../images/nl/filters-4.svg)

*De binnengeleider staat onderaan in verbinding met de wand en eindigt bovenin
vrij. De koppellussen halen het signaal erin en eruit.*

Een kwartgolfresonator is een stuk geleider in een afgesloten metalen kast,
aan de ene kant kortgesloten tegen de wand en aan de andere kant vrij. Bij de
frequentie waarop die geleider precies een kwart golflengte lang is,
transformeert de kortsluiting aan de voet zich naar een open einde aan de top:
daar is de spanning maximaal en de stroom nul. Dat is resonantie, en anders
dan bij een spoel met een condensator ligt hij vast in de mechanische
afmetingen — niet in componenten met een tolerantie en een
temperatuurcoëfficiënt.

### Hoe lang

Een kwart golflengte op 869,618 MHz is 86,2 mm. In de praktijk wordt de
geleider korter gemaakt en het verschil aangevuld met capaciteit boven het
vrije uiteinde: de afstemschroef, of een schijfje. Dat heeft drie gevolgen.
Het filter wordt compacter, het is af te regelen zonder eraan te zagen, en de
eerstvolgende resonantie schuift omhoog. Dat laatste is geen bijzaak — het is
precies de knop waarmee je de spurious doorlaat verderop uit de weg zet.

### Waar de Q vandaan komt

De verliezen zitten vrijwel volledig in de weerstand van het metaaloppervlak
waarlangs de stroom loopt. Bij hetzelfde opgeslagen veld betekent meer
oppervlak minder verlies, en daarom groeit de Q mee met de afmetingen. Een
geleider van anderhalve centimeter in een kast van acht haalt een veelvoud van
dezelfde kring, opgerold in een blikje van twee. De rangschikking in de tabel
hieronder is dus geen toeval maar meetkunde: van klein en slap naar groot en
scherp.

### Van resonator naar filter

Eén kring is nog geen filter. Het signaal gaat erin en eruit via een lus, een
aftakking op de geleider of een korte kabel. Hoe vaster die koppeling, hoe
breder de doorlaat en hoe minder steil de flanken. Meer kringen achter elkaar
maken de flanken steiler en voegen per kring invoegverlies toe.

Waar die kringen zitten en hoe ze zijn kortgesloten bepaalt de naam. Opgerold
in een blikje heet het helical. Als staven naast elkaar in één doos, om en om
aan de andere kant kortgesloten, heet het interdigitaal; allemaal aan dezelfde
kant met capaciteit aan de top heet het combline. Elke kring in een eigen
kast, gekoppeld met lussen of kabeltjes: cavity filter.

## De filtertypen

| Type | Q per kring | Invoegverlies | Vermogen | Volume |
|---|---|---|---|---|
| LC / keramisch | 50–150 | 1,5–3 dB | watts | zeer klein |
| SAW | veelpolig, zie tekst | 1,5–3 dB | vaak +10 tot +20 dBm | zeer klein |
| Helical | 200–600 | 1–2 dB | watts | blikje |
| Interdigitaal / combline | 800–2000 | 0,5–1,5 dB | tientallen watts | doos |
| Cavity filter | 2000–5000 | 0,3–1 dB | honderden watts | groot en zwaar |

De getallen zijn indicatief en geven de ordegrootte en de onderlinge
verhouding weer; de werkelijke waarden staan in het datasheet van een
specifiek onderdeel.

**LC en keramisch.** Spoelen en condensatoren, of een keramisch blokje met
hetzelfde effect. Goedkoop, klein, ruim voldoende vermogen. De flanken zijn
slap: op 70 MHz afstand haal je vaak niet meer dan 15 tot 25 dB. Genoeg
tegen de banden boven 1,5 GHz, matig tegen de 900-band.

**SAW.** Een akoestische golf over een piëzo-kristal. De steilheid komt niet
van hoge Q per kring maar van veel polen tegelijk, dus de kolom Q is er niet
van toepassing. Steilste flanken in de kleinste behuizing, en daarmee de
beste keuze tegen de 900-band. Twee aandachtspunten: het vermogen is vaak
beperkt tot rond +10 à +20 dBm, en de demping ver boven de doorlaatband is
niet altijd gespecificeerd. Controleer de karakteristiek tot voorbij de
hoogste band in je omgeving.

**Helical.** Een spoel in een afgeschermd blikje — feitelijk een opgerolde
kwartgolfresonator. Aanzienlijk hogere Q dan LC, ruim vermogen, goed
zelfbouwbaar en met een NanoVNA af te regelen. De praktische middenweg.

**Interdigitaal en combline.** Meerdere kwartgolfstaven in één rechthoekige
doos. Bij interdigitaal zijn de staven om en om aan de andere kant
kortgesloten, bij combline allemaal aan dezelfde kant met capacitieve
topbelasting. Hoge Q, laag invoegverlies, en de meest bevredigende
zelfbouwvorm op 868 MHz.

**Cavity filter.** Eén kwartgolfresonator per metalen kast, gekoppeld met lussen
of korte kabels. De hoogste Q en het laagste verlies, en daarom de standaard
in repeaterduplexers waar 40 dB onderdrukking op 600 kHz afstand nodig is.
Voor een node naast een mast is dat overkill: je dichtstbijzijnde stoorbron
staat 54 MHz weg, niet 600 kHz. Dat vraagt volume en gewicht voor een
eigenschap die je niet gebruikt.

## Doorlaat of sper

Een **banddoorlaatfilter** laat je eigen band door en dempt al het overige.
Dit is bijna altijd de juiste keuze, omdat het tegen alle stoorbronnen
tegelijk werkt — ook tegen bronnen die je nog niet kent.

Een **bandsperfilter** of notch doet het omgekeerde: het dempt één smalle
band en laat de rest ongemoeid. Dat is alleen zinnig als er precies één
dominante stoorder is, die dicht bij je eigen frequentie ligt en die je
kent. Naast een multibandmast is dat vrijwel nooit het geval.

Een **laagdoorlaatfilter** kan als aanvulling zinnig zijn: in cascade achter
een resonatorfilter snijdt het alles boven ongeveer 1 GHz weg, inclusief de
spurious doorlaat die hierna aan bod komt.

## Twee valkuilen

**De spurious doorlaat.** Een kwartgolfresonator resoneert niet alleen op
zijn ontwerpfrequentie maar ook op drie, vijf en zeven keer die frequentie.
Voor 869,618 MHz is dat 2608,9 MHz — en op dit opstelpunt staat 51 MHz
daarvandaan een 2600-zender. Een zuiver kwartgolf-ontwerp zou die band dus
grotendeels doorlaten en daarmee een deel van zijn eigen nut ondergraven.
Capacitieve topbelasting, zoals bij combline, schuift die tweede resonantie
naar boven; een laagdoorlaat in cascade lost het ook op. Een SAW-filter kent
dit verschijnsel niet, maar heeft weer zijn eigen zwakke plekken hoog in het
spectrum. Er is geen type zonder aandachtspunt — er is alleen het
aandachtspunt dat je hebt nagekeken.

**Temperatuurdrift.** Een resonator van aluminium zet ongeveer 23 ppm per
kelvin uit. Van −10 tot +50 °C is dat zestig kelvin, dus circa 1400 ppm,
oftewel een verschuiving in de orde van 1,2 MHz op 869 MHz. Ontwerp een
buitenfilter daarom niet smaller dan de hele SRD-band van ruwweg 7 MHz. Dan
is de drift irrelevant en is het afregelen ook een stuk vergevingsgezinder.

## Waar het filter komt

Het filter hoort zo dicht mogelijk bij de antenne, vóór het eerste actieve
onderdeel. Dan zijn er twee routes.

![Twee manieren om een filter in het antennepad te plaatsen: in het gedeelde
zend- en ontvangstpad, of met een extra schakelaar alleen in het
ontvangstpad](../../../images/nl/filters-3.svg)

*In het gedeelde pad passeert ook het zendvermogen het filter. Met een extra
schakelaar blijft het zendpad ongefilterd en op vol vermogen.*

**In het gedeelde pad.** De eenvoudigste opstelling: één filter tussen
antenne en node. Zenden en ontvangen gaan er allebei doorheen. Het
invoegverlies telt twee keer mee en je moet het zendvermogen onder de
vermogensgrens van het filter houden.

**Alleen in het ontvangstpad.** De SX1262 stuurt zijn zend-ontvangst-
schakelaar aan via DIO2 — zie [Antenne](antenna.md). Met een extra externe
schakelaar splits je de paden en zet je het filter alleen in de RX-tak. Het
zendpad houdt vol vermogen en ziet alleen het verlies van de schakelaar. De
keerzijde is een extra onderdeel, een aansturing, en het feit dat je in de
print moet.

## Wanneer een filter loont

Een filter verbetert niet alles tegelijk. Het maakt de ontvangstkant beter
en de zendkant slechter, en of dat per saldo wint hangt af van hoeveel desense
je werkelijk hebt. Met een invoegverlies van 2 dB en een filter dat
begrenzing tot 20 dBm afdwingt, wordt de som:

- zendverlies: 2 dB begrenzing plus 2 dB invoegverlies is 4 dB, altijd
- ontvangstwinst: de desense min 2 dB invoegverlies

| Desense | Ontvangstwinst | Zendverlies | Netto |
|---|---|---|---|
| 4 dB | 2 dB | 4 dB | verlies |
| 6 dB | 4 dB | 4 dB | gelijk |
| 10 dB | 8 dB | 4 dB | winst |
| 20 dB | 18 dB | 4 dB | winst |
| 27 dB | 25 dB | 4 dB | winst |

Onder ongeveer 6 dB desense verslechtert een filter je situatie. Daarboven
wint het, en vanaf een dB of tien is de uitkomst niet meer twijfelachtig.

Er zit één asymmetrie in die de tabel niet laat zien en die in het voordeel
van het filter werkt. Een link is zo goed als zijn slechtste richting. Staat
alleen jouw node in het sterke veld, dan is jouw ontvangst de knellende
richting en de zendkant niet. Winst boeken op de knellende richting weegt
dan zwaarder dan evenveel verlies op de andere.

## Meten

Zonder nulmeting weet je achteraf niet wat een ingreep heeft opgeleverd.

**Lees de ruisvloer af** voordat je iets verandert. Thermische ruis over
62,5 kHz is −126,0 dBm; met het ruisgetal van de ontvangketen erbij verwacht
je een vloer rond −120 dBm. Zie [Linkbudget](link-budget.md).

**Vergelijk met een tweede node** op een rustige plek, liefst met dezelfde
hardware. Dat is de enige echte referentie die je hebt.

**Wissel de nodes van plek** als het verschil groot is. Volgt de hoge vloer
de locatie, dan is het de omgeving. Volgt hij de kast, dan is het de
hardware en levert een filter je niets op.

**Sluit een dummy load aan** in plaats van de antenne. Zakt de vloer dan
fors, dan komt de energie via de antenne binnen. Blijft hij hoog, dan straalt
het in via kast, voedingskabel of USB.

**Log een etmaal.** Blokkering door de altijd aanwezige draaggolven van een
basisstation ligt vrijwel vlak. Intermodulatie beweegt mee met het
mobiele verkeer en zwabbert tussen nacht en avondspits. Dat onderscheid
bepaalt of een filter gaat helpen.

> [!WARNING]
> **De firmware kapt af op −120 dBm.** MeshCore middelt 64 monsters en klemt
> de uitkomst op een ondergrens van −120 dBm; lager rapporteert hij niet,
> ook niet als de omgeving stiller is. Zie
> [De LoRa-transceiver](sx1262.md). Voor een node met een vloer van −90 dBm
> is de maximaal aantoonbare verbetering dus 30 dB. Wie al rond −118 zit,
> kan met deze meting geen verbetering meer aantonen — en heeft er ook geen
> nodig.

## Praktijkgeval

Twee repeaters in Zwolle, dezelfde firmware en dezelfde instellingen. De
ene staat direct onder het opstelpunt dat hierboven in de tabel staat, met
een 6 dBi collineair, en rapporteert een ruisvloer van −90 dBm. De andere
staat 30 meter lager, met een 3 dBi antenne, en rapporteert −117 dBm.

Verschil: 27 dB. Daarvan is hooguit 3 dB toe te schrijven aan het verschil
in antennewinst, en dan alleen voor stoorbronnen in de 868-band; buiten die
band zegt de winstopgave van een 868-antenne niets. Het overige is
omgeving.

Wat dat betekent voor de hoge node: alles wat zwakker binnenkomt dan
ongeveer 27 dB boven zijn normale drempel gaat verloren. Vertaald naar
afstand, met een propagatie-exponent tussen 2 en 3,5, hoort hij op ruwweg
een zesde tot een twintigste van de afstand die hij zou moeten halen.

Er zit een tweede aanwijzing in dezelfde opstelling die makkelijk over het
hoofd wordt gezien: de BLE-verbinding van de hoge node werkt alleen als de
telefoon er vlak tegenaan gehouden wordt. Dat is een andere radio, een
andere band en een ander antennepad, met hetzelfde symptoom. Twee
onafhankelijke ontvangers met dezelfde klacht wijzen naar de omgeving, niet
naar een defect. Een 868-filter lost dat tweede symptoom overigens niet op —
zie hieronder.

## Wat een filter niet oplost

**Signalen in je eigen band.** Passieve intermodulatie die op 869 MHz
ontstaat zit al in de doorlaatband voordat het filter eraan te pas komt.
Blijft de vloer na inbouw hoog én blijft hij het verkeerspatroon volgen, dan
is dit de oorzaak en helpt alleen geometrie: verder weg, lager, of een
opstelling die niet op dezelfde staalconstructie zit.

**Andere banden.** Een 868-filter zit in het LoRa-pad. BLE en WiFi hebben
hun eigen antenne, meestal op de print, en profiteren er niet van. Zie
[BLE Architectuur](../interfaces/ble-architecture.md).

**Instraling buiten het antennepad.** Velden die via de voedingskabel, de
USB-kabel of de behuizing binnenkomen, gaan om het filter heen. Ferrieten en
een mantelstroomsmoorspoel horen bij dezelfde ingreep.

**Een slechte opstelling.** Een filter levert je in het gunstigste geval
twintig, dertig dB op. Dertig meter lager gaan leverde in het geval
hierboven zevenentwintig dB op, zonder invoegverlies en zonder begrenzing
van het zendvermogen. Filteren is de oplossing als je niet kunt verplaatsen, niet
het alternatief voor nadenken over de plek.

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`src/helpers/radiolib/RadioLibWrappers.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/radiolib/RadioLibWrappers.cpp)
  — de gemeten ruisvloer, 64 monsters, en de ondergrens van −120 dBm
- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/platformio.ini)
  — `LORA_FREQ`, `LORA_BW` en het maximale zendvermogen

In deze repository:

- [`tools/filter-planning.py`](../../../tools/filter-planning.py) — rekent
  elk cijfer op deze pagina opnieuw uit en toont de gevoeligheid voor de
  aannames

Buiten de firmware:

1. [ETSI EN 300 220-1 V3.1.1](https://www.etsi.org/deliver/etsi_en/300200_300299/30022001/03.01.01_60/en_30022001v030101p.pdf)
   — ontvangercategorieën en de beschrijving van blokkering
2. [ETSI EN 300 220-2 V3.1.1](https://www.etsi.org/deliver/etsi_en/300200_300299/30022002/03.01.01_60/en_30022002v030101p.pdf)
   — blokkeringsgrenzen, en de toelichting waarom intermodulatie bewust niet
   genormeerd is
3. [Analog Devices — Passive Intermodulation Effects in Base Stations](https://www.analog.com/en/resources/analog-dialogue/articles/passive-intermodulation-effects-in-base-stations-understanding-the-challenges-and-solutions.html)
   — het roestige-boutverschijnsel en ontvangerverstoring door PIM
4. [Antenneregister](https://antenneregister.nl/) — de vermogens, hoogten en
   straalrichtingen van het opstelpunt
5. [ETSI TR 102 649-2](https://www.etsi.org/deliver/etsi_tr/102600_102699/10264902/01.03.01_60/tr_10264902v010301p.pdf)
   — subbandoverzicht 868–870 MHz
6. [Semtech SX1262](https://www.semtech.com/products/wireless-rf/lora-connect/sx1262)
   — het zendvermogen van de chip

Niet uit een bron: de schuine afstand van 40 m, de patroononderdrukking van
25 dB, de blokbreedtes rond de geregistreerde middenfrequenties, en de
indicatieve Q-waarden en invoegverliezen per filtertype. Alle vier staan als
zodanig in de tekst en in het script.

Verwante hoofdstukken:

- [Antenne](antenna.md) — de RF-schakelaar en de connector waar het filter
  tussen komt
- [Linkbudget](link-budget.md) — waar de ruisvloer in de som terechtkomt
- [De LoRa-transceiver](sx1262.md) — hoe de firmware zijn ruisvloer meet en
  afkapt
- [Hoger en sterker is niet altijd beter](../../techniek/dead-zone.md) —
  waarom de opstelling zwaarder weegt dan het onderdeel
- [Regelgeving & Duty Cycle](../../gebruik/regulations.md) — wat je mag
  uitstralen na aftrek van het invoegverlies
