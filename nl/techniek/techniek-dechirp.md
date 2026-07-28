# Chirp en DeChirp vereenvoudigd voorgesteld

## Inleiding

Deze analyse hoort bij een poging om beter te begrijpen waarom LoRa zo goed werkt. Het doel is om op een eenvoudige manier duidelijk te maken wat er **wordt verzonden**, wat er **door de ontvanger wordt ontvangen**, wat het **dechirp-proces** daarmee doet en hoe de **FFT** daar uiteindelijk het symbool uit haalt.

Om het duidelijk te houden, wordt een sterk vereenvoudigd voorbeeld gebruikt: een "bandbreedte" van **10 frequentiestappen** (0–9), waarbij elk sample 1 seconde duurt. In de praktijk zijn de tijden veel korter (milliseconden) en het aantal samples per symbool veel groter (128–4096), maar het principe blijft hetzelfde.

## Het probleem met de simpele tabel

Bij mijn eerste poging om LoRa dechirp met een eenvoudige som-tabel te laten zien, gaat het mis zodra er een **wrap** in de frequentie optreedt. Eerst het geval zonder verschuiving.

### Symbool 0 (geen verschuiving) — Werkt

Hier zie je links het **verzonden signaal**: de TX up-chirp.<br>Daarnaast staat de **referentie in de ontvanger**: de RX down-chirp die lokaal in de ontvanger wordt gebruikt om het binnengekomen signaal mee te vergelijken.<br>In dit eenvoudige voorbeeld lopen die netjes tegenover elkaar, waardoor de som constant blijft.

| TX (up) | RX (down) | Som |
|---|---|---|
| 0 | 10 | 10 |
| 1 | 9 | 10 |
| 2 | 8 | 10 |
| 3 | 7 | 10 |
| 4 | 6 | 10 |
| 5 | 5 | 10 |
| 6 | 4 | 10 |
| 7 | 3 | 10 |
| 8 | 2 | 10 |
| 9 | 1 | 10 |

✓ Constante som = 10. Hier werkt het idee "constante som = goed".

### Symbool 3 (verschoven) — Faalt na wrap

Daarna dezelfde tabel voor de verschoven versie (symbool 3).<br>Daarbij is het **verzonden chirp-signaal** niet bij 0 gestart, maar bij 3.<br>De ontvanger gebruikt nog steeds dezelfde **lokale down-chirp referentie** om het ontvangen signaal mee te vergelijken:

| TX (start=3) | RX (down) | Som − 10 | Status |
|---|---|---|---|
| 3 | 10 | 3 | ✓ |
| 4 | 9 | 3 | ✓ |
| 5 | 8 | 3 | ✓ |
| 6 | 7 | 3 | ✓ |
| 7 | 6 | 3 | ✓ |
| 8 | 5 | 3 | ✓ |
| 9 | 4 | 3 | ✓ |
| 0 (wrap) | 3 | −7 | ✗ FOUT |
| 1 | 2 | −7 | ✗ FOUT |
| 2 | 1 | −7 | ✗ FOUT |

Na de wrap klopt de berekening niet meer in deze simpele benadering.

## Waarom wrapping noodzakelijk is

De frequentieband is fysiek begrensd. In dit voorbeeld gebruiken we 10 stappen (0–9), in de praktijk bijvoorbeeld 64 kHz bandbreedte met een vaste kanaalbreedte.

De frequentie mag niet buiten de band omdat:

- Het buiten het toegewezen spectrum zou vallen (illegaal)
- Het andere diensten zou verstoren
- De ontvanger het signaal dan niet kan volgen

Daarom loopt de tijd/positie netjes door (0–9), maar springt de **verzonden of ontvangen momentane frequentie** terug naar 0 wanneer die voorbij 9 zou gaan: dat is de **wrap**.<br>Belangrijk daarbij is dat alleen de zichtbare frequentie binnen de band terugklapt; de onderliggende fase-ontwikkeling van het signaal loopt wiskundig gewoon door.

> [!WARNING]
> **Belangrijk:** de wrap is een praktische beperking van de frequentieband, niet een echte "reset" van de onderliggende fase-ontwikkeling van het signaal.

## De correcte interpretatie

De oplossing is om niet naar de som te kijken, maar naar het **verschil** tussen:<br>- de frequentie van het **ontvangen/verzonden LoRa-signaal** op dat moment, en<br>- de **lokale referentiechirp in de ontvanger**.<br><br>Daarbij moet de TX-frequentie na de wrap wiskundig worden gezien als doorlopend. Dan blijft het verschil constant.

| Positie | TX freq | TX (wiskundig) | RX ref | Verschil |
|---|---|---|---|---|
| 0 | 3 | 3 | 0 | 3 |
| 1 | 4 | 4 | 1 | 3 |
| 2 | 5 | 5 | 2 | 3 |
| 3 | 6 | 6 | 3 | 3 |
| 4 | 7 | 7 | 4 | 3 |
| 5 | 8 | 8 | 5 | 3 |
| 6 | 9 | 9 | 6 | 3 |
| 7 | 0 (wrap) | 10 | 7 | 3 |
| 8 | 1 | 11 | 8 | 3 |
| 9 | 2 | 12 | 9 | 3 |

**Het verschil blijft constant = 3, ongeacht de wrap!**

Door de TX-frequentie wiskundig "door te tellen" (10, 11, 12, …) zie je dat het verschil met de RX-referentie overal 3 blijft, ook na de wrap.<br>Met andere woorden: de ontvanger ziet na de dechirp-bewerking steeds hetzelfde frequentieverschil terug. Dat constante verschil is precies wat de FFT als piek terugvindt.

> [!NOTE]
> **Let op:** dit is een vereenvoudigde voorstelling die bedoeld is om het werkingsprincipe van de dechirp- en FFT-piekdetectie intuïtief te maken; de daadwerkelijke LoRa-implementatie gebruikt een complexere, maar wiskundig equivalente beschrijving.

## FFT piekdetectie — Grafische voorstelling

De FFT kijkt naar het resultaat **nadat het ontvangen signaal met de lokale referentiechirp is gedechirpt**.<br>Zij telt dan in feite hoe vaak elk mogelijk frequentieverschil voorkomt; elk verschil komt in een eigen **bin** terecht.<br>Voor symbool 3 leveren alle 10 samples hetzelfde verschil 3 op, dus stapelt alle energie zich in bin 3.

Een bin is letterlijk een "bakje" waarin de energie voor dat specifieke frequentieverschil wordt opgeteld.

### Ideaal signaal (geen verlies)

Alle 10 samples dragen bij aan bin 3. Bin 3 krijgt daardoor een piekhoogte van 10, de andere bins blijven laag.

FFT Bar Chart: Ideal signal

![Diagram 1 bij techniek-dechirp](../../images/nl/techniek-dechirp-1.svg)

### Met 30% sample verlies

Zelfs met 3 gemiste samples blijft de piek bij bin 3 dominant. Het symbool wordt correct gedetecteerd.

FFT Bar Chart: 30% loss

![Diagram 2 bij techniek-dechirp](../../images/nl/techniek-dechirp-2.svg)

### Met ruis/interferentie

Ruis en fouten landen in willekeurige bins. Ze zijn verspreid en kunnen de signaalpiek niet overstijgen.

FFT Bar Chart: With noise

![Diagram 3 bij techniek-dechirp](../../images/nl/techniek-dechirp-3.svg)

## Het kernprincipe

| SIGNAAL | RUIS |
|---|---|
| Alle samples → dezelfde bin | Fouten → willekeurige bins |
| = GECONCENTREERDE ENERGIE | = VERSPREIDE ENERGIE |

Daarom kan incidentele vervuiling, ruis of sampleverlies de echte signaalpiek meestal niet overstijgen:<br>het **juiste ontvangen symbool** concentreert zich na dechirp in één bin, terwijl fouten en ruis juist over meerdere bins verspreid raken.

## Hoeveel samples kun je missen?

De fouttolerantie hangt af van de Spreading Factor:

| Spreading Factor | Samples per symbool | ~30% verlies tolereerbaar |
|---|---|---|
| SF7 | 128 | ~38 samples |
| SF10 | 1024 | ~307 samples |
| SF12 | 4096 | ~1229 samples |

Daarnaast voegt de **Coding Rate (CR)** nog extra foutcorrectie toe:

| Coding Rate | Overhead | Fouttolerantie |
|---|---|---|
| CR 4/5 | 25% | Basis |
| CR 4/6 | 50% | Matig |
| CR 4/7 | 75% | Goed |
| CR 4/8 | 100% | Maximaal |

## Processing gain — De kracht van LoRa

De "magie" van LoRa zit in de **processing gain**: door het signaal te spreiden over vele samples, kun je signalen detecteren die onder de ruisvloer liggen.

In ons voorbeeld met 10 samples:

- Signaalenergie concentreert in **1 bin**
- Ruis verdeelt over **10 bins**
- Processing gain ≈ 10× (10 dB)

Bij SF12 met 4096 samples: processing gain ≈ **4096× (36 dB)!**

Dit verklaart waarom LoRa verbindingen kan maken die met conventionele radio onmogelijk zouden zijn.

## Conclusie

De oorspronkelijke tabel-aanpak mislukte omdat:

- Er met een **som** werd gewerkt in plaats van met een **verschil**
- De wrap werd gezien als een echte reset, in plaats van een praktische beperking van de frequentieband
- Er werd te veel gekeken naar losse, momentane frequenties, terwijl de ontvanger in werkelijkheid het **ontvangen signaal** vergelijkt met een **lokale referentiechirp**, waarna het relevante verschil via de FFT zichtbaar wordt als een piek

De FFT ziet het constante verschil als een duidelijke piek:

- Alle juiste samples stapelen zich in **dezelfde bin** (signaal)
- Ruis en fouten worden **uitgesmeerd** over andere bins
- De piek van het signaal blijft daardoor **dominant**, zelfs bij aanzienlijk sample-verlies

In MeshCore wordt de FFT zo gebruikt als beslisser: na het vergelijken van het **ontvangen signaal** met de **lokale referentie in de ontvanger** is de bin met de grootste energie het gedecodeerde symbool. Daardoor blijft de implementatie relatief eenvoudig, goed schaalbaar en robuust tegen fouten.


