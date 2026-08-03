# Regelgeving & Duty Cycle

*VERGUNNINGVRIJ ZENDEN · EU/NL · 868 MHz · H-REGELS · ERP*

══════════════════════════════════════════════════════════════

Voor LoRa-apparatuur in de 868 MHz-band heb je in Nederland geen zendmachtiging nodig en ook geen meldingsplicht — mits je binnen de voorschriften blijft. Drie lagen regelgeving bepalen wat mag: een EU-apparatuurrichtlijn, een EU-spectrumbeschikking, en de Nederlandse regeling die dat nationaal vertaalt.

══════════════════════════════════════════════════════════════

## De regelgevingsstapel

De complete keten, van wettelijke grondslag tot concrete band-regels:

| Niveau | Document | Wat regelt het? |
|---|---|---|
| NL — wet | Telecommunicatiewet, art. 3.9 | Wettelijke basis voor vergunningvrij gebruik |
| NL — besluit | Frequentiebesluit 2013 | Delegeert welke categorieën vergunningvrij zijn |
| NL — regeling | Regeling frequentieruimte zonder vergunning en zonder meldingsplicht 2015, **Bijlage 11 Subcategorie 1** | De concrete H-regels (H1–H7) voor niet-specifieke korteafstandsapparatuur, inclusief LoRa |
| NL — besluit | Besluit radioapparaten 2016 | Nederlandse implementatie van de EU-apparatuurrichtlijn |
| EU — richtlijn | **Richtlijn 2014/53/EU (RED)** | Eisen aan de apparatuur zelf (CE-markering, essentiële eisen). Vervangt de oude R&TTE-richtlijn 1999/5/EG. |
| EU — beschikking | Beschikking 2006/771/EG (geconsolideerd) | EU-brede harmonisatie van SRD-frequentiebanden |
| EU — wijziging | Uitvoeringsbesluit (EU) 2025/105 | Laatste update van 2006/771/EG (januari 2025) |
| CEPT | ERC Recommendation 70-03 | CEPT-aanbeveling waar de EU-beschikking op is gebaseerd |
| ETSI | EN 300 220-1 & EN 300 220-2 | Geharmoniseerde meetnormen onder RED |

> [!NOTE]
> **Let op — verouderde verwijzing in de regelingtekst**
> In de opmerkingenkolom van Bijlage 11 wordt nog verwezen naar *"richtlijn nr. 1999/5/EG"* (R&TTE). Die richtlijn is per **13 juni 2016 ingetrokken** en vervangen door Richtlijn 2014/53/EU (RED). De regelingtekst is op dit punt nog niet bijgewerkt, maar de verwijzing moet gelezen worden als "de opvolger daarvan", dus RED. Voor nieuwe apparatuur geldt enkel RED.

══════════════════════════════════════════════════════════════

## Bijlage 11 Subcategorie 1 — de H-regels voor 868 MHz

De relevante rijen uit de Nederlandse regeling voor MeshCore en vergelijkbare LoRa-apparatuur. De kolom dBm is informatief toegevoegd. De kolom **CEPT 70-03** toont de Europese equivalent-identifier uit ERC Recommendation 70-03, Annex 1 (non-specific SRD).

| NL rij | CEPT 70-03 | Frequentieband | Max. vermogen | In dBm | Duty cycle | Alternatief | Opmerking |
|---|---|---|---|---|---|---|---|
| H3 | h1.5 | 868,000–868,600 MHz | 25 mW e.r.p. | +14 dBm | < 1 % | LBT+AFA | Typisch LoRaWAN EU868 uplink |
| H4 | h1.7 | 869,400–869,650 MHz | **500 mW e.r.p.** | **+27 dBm** | **< 10 %** | LBT+AFA | High-power regime — DC-bewaking of LBT+AFA vereist |
| H5 | — | 869,400–869,650 MHz | **25 mW e.r.p.** | **+14 dBm** | **< 0,1 %** | LBT+AFA | Geen CEPT-rij; NL-variant binnen h1.7-band |
| H6 | h1.8 | 869,700–870,000 MHz | 5 mW e.r.p. | +7 dBm | geen | — | Geen DC-beperking |
| H7 | h1.9 | 869,700–870,000 MHz | 25 mW e.r.p. | +14 dBm | < 1 % | LBT+AFA | Hoger vermogen, wel DC-beperking |

MeshCore in Nederland draait typisch op **869,618 MHz** — binnen de H4/H5-band (= CEPT h1.7). De keuze tussen H4 en H5 hangt af van hoe je apparaat is gecertificeerd.

══════════════════════════════════════════════════════════════

## H4 versus H5 — MeshCore kiest voor H4

H4 en H5 zijn twee regelprofielen voor non-specific SRD (telemetrie, data, alarmering) in de Nederlandse SRD-regeling en CEPT-richtlijnen. Ze dekken exact dezelfde frequentieband van 869,400–869,650 MHz, maar bieden verschillende limieten. H4 biedt ruimere limieten dan H5, wat het de standaardkeuze maakt voor MeshCore-netwerken.

> [!NOTE]
> **⚠ Terminologie — H4/H5 zijn Nederlandse tabelcodes, geen ETSI-klassen**
> "H4" en "H5" zijn rijlabels in Bijlage 11, Subcategorie 1 van BWBR0036378 — puur Nederlandse regelgevingscodes. ETSI EN 300 220-1 kent alleen *receiver categories* 1, 1.5, 2 en 3 (ontvangst-prestatie), en CEPT ERC 70-03 gebruikt kleine-letter-codes als `h1.7` voor dezelfde subband. Er is dus geen "ETSI H4-klasse". Wel geldt: apparatuur voor regime H4 of H5 moet onder RED 2014/53/EU via diezelfde ETSI EN 300 220 worden gecertificeerd, maar dan toegepast op de bij het regime horende parameters.

H4 geeft 20× meer zendvermogen en een 100× ruimere duty cycle dan H5, wat het geschikter maakt voor mesh-communicatie waarin repeaters regelmatig relaisverkeer moeten doorgeven.

### MeshCore-community gebruikt H4 als standaard

De Nederlandse MeshCore-community werkt binnen het H4-profiel. In het VERON-nieuwsartikel "MeshCore, de opvolger van Meshtastic" (22 december 2025, door Arno PE1RDP) staat letterlijk: *"Zo is het maximale RF vermogen 500mW ERP en de duty cycle 10%."* Dit zijn exact de H4-limieten.

De praktijkconfiguratie die op meerdere Nederlandse MeshCore-bronnen als standaard wordt genoemd:

```text
Preset:      Netherlands
Frequentie:  869,618 MHz
Bandbreedte: 62,5 kHz
Spreading:   SF7
Coding rate: 4/5
Max. TX:     ≤500 mW e.r.p. (+27 dBm)
Duty cycle:  ≤10 %
```

Deze configuratie valt binnen de H4-parameters uit Bijlage 11 en is interoperabel met andere Nederlandse MeshCore-nodes.

### Waarom niet H5?

Het H5-profiel (25 mW / 0,1 %) is in theorie ook toegestaan op dezelfde frequentieband, maar voor een mesh-netwerk met routering en doorgifte is 25 mW beperkt in bereik en 3,6 seconden zendtijd per uur beperkt in luchttijd. Voor single-purpose-toepassingen (een sensor die af en toe een kort berichtje stuurt) is H5 passend; voor een actief mesh-relayknooppunt minder praktisch.

### Bron

| Bron | Bevestiging |
|---|---|
| [VERON — MeshCore, de opvolger van Meshtastic](https://veron.nl/nieuws/meshcore-de-opvolger-van-meshtastic/) (Arno PE1RDP, 22-12-2025) | 500 mW ERP, 10 % duty cycle; EU/UK Narrow preset, 62,5 kHz bandbreedte |

══════════════════════════════════════════════════════════════

## Wat is een duty cycle?

Een **duty cycle** is het maximale deel van een aaneengesloten uur (T<sub>obs</sub> = 1 h) dat je zender mag uitzenden binnen de betreffende band. De regel bestaat om te voorkomen dat één zender een vergunningvrije band "dichttrekt" — iedereen moet eerlijk delen.

| Duty cycle | Zendtijd per uur | Regime |
|---|---|---|
| 0,1 % | 3,6 seconden | H5 |
| 1 % | 36 seconden | H3 / H7 |
| 10 % | 6 minuten | H4 |
| 100 % | onbeperkt | H6 (geen DC-beperking) |

### Alternatief: LBT+AFA (polite spectrum access)

**Listen Before Talk + Adaptive Frequency Agility** is een "beleefd" protocol: je node luistert eerst of de frequentie vrij is voor uitzending (LBT), en springt tussen kanalen (AFA) om niemand lang te blokkeren. Apparatuur die dit correct implementeert mag in veel gevallen de duty-cycle-limiet overschrijden, mits aantoonbaar "beleefd" volgens ETSI EN 300 220.

### Praktijk voor MeshCore-nodes

Een typisch MeshCore-pakket duurt 150–400 ms. In H4 (10%) mag je node max 6 minuten per uur zenden — ruim voldoende voor een gemiddelde node. Een repeater die veel verkeer relayt moet wel opletten: bij piekverkeer kun je het DC-budget sneller opmaken dan je denkt, zeker op hógere spreading factors waar pakketten langer in de lucht zijn.

### Duty cycle in een mesh — wat er anders is dan bij een solo-node

De H-regels beschrijven een enkel zendend apparaat. CEPT definieert de duty cycle als Σ(T<sub>on</sub>)/T<sub>obs</sub>, waarbij T<sub>on</sub> de zendtijd is van **één zendend apparaat** en T<sub>obs</sub> één aaneengesloten uur. Voor een mesh-netwerk volgen daar drie dingen uit:

**1. Er is geen netwerkbudget.** De regelgeving kent geen gezamenlijke limiet voor een mesh. Elke node wordt afzonderlijk beoordeeld. Twintig repeaters die elk op 9 % zitten, overtreden formeel niets — ook al is de band lokaal zwaar belast.

**2. Doorgegeven verkeer telt mee in je eigen budget.** Een pakket dat je repeater van een ander doorgeeft, is juridisch jouw transmissie. Waar een solo-sensor zijn duty cycle vooraf kan uitrekenen, is die van een repeater een functie van het verkeersaanbod van derden — precies op het moment dat het netwerk druk is, loopt je budget het snelst vol.

**3. Eén bericht vereist N transmissies.** MeshCore-clients repeaten niet; alleen repeaters en room servers met `repeat on`. Eén flood-bericht wordt daardoor één keer uitgezonden door élke repeater die het hoort. De belasting van de mesh schaalt met het aantal repeaters, niet met het aantal afzenders.

#### Hoeveel pakketten past er in 6 minuten?

Indicatief, berekend met de standaard LoRa time-on-air-formule voor SF7 / BW 62,5 kHz / CR 4/5 (de huidige NL-parameters):

| Payload | Time-on-air | H4 — 6 min/uur | H5 — 3,6 s/uur |
|---|---|---|---|
| 20 bytes | ~170 ms | ~2.100 transmissies/uur | ~21 transmissies/uur |
| 50 bytes | ~320 ms | ~1.130 transmissies/uur | ~11 transmissies/uur |
| 80 bytes | ~485 ms | ~740 transmissies/uur | ~7 transmissies/uur |

Onder H4 is er dus ruimte zat voor een normale repeater. Onder H5 zou dezelfde repeater op ongeveer tien doorgiftes per uur uitkomen — voor een relaisknooppunt in de praktijk onbruikbaar. Dat is de werkelijke reden waarom mesh-repeaters het H4-regime nodig hebben.

> [!WARNING]
> **⚠ De firmware-default voldoet niet aan de Nederlandse limiet**
> MeshCore's `set dutycycle` staat standaard op **50 %**, en de verouderde `set af` op `1.0` (eveneens ~50 %). Beide liggen ver boven zowel H4 (10 %) als H5 (0,1 %). Een vers geflashte repeater is dus **niet conform** tot je dit expliciet aanpast: `set dutycycle 10` (firmware v1.15.0 en nieuwer).

#### LBT+AFA is voor MeshCore geen alternatief

De regelgeving biedt LBT+AFA als uitweg uit de duty-cycle-limiet, maar AFA staat voor *Adaptive Frequency Agility* — springen tussen kanalen. MeshCore draait in Nederland op één vaste draaggolf, dus die voorwaarde wordt niet gehaald. De `txdelay`- en `rxdelay`-mechanismen zijn collision-avoidance, geen gecertificeerde LBT volgens ETSI EN 300 220. Voor NL-nodes geldt daarom in de praktijk uitsluitend de duty-cycle-route.

#### Gedragsregels die de mesh ontlasten

Deze instellingen zijn géén vervanging van RED-certificering, maar wel de praktische manier om binnen het H4-budget te blijven en de band leefbaar te houden.

| Instelling | Firmware-default | NL-advies | Waarom |
|---|---|---|---|
| `set dutycycle {1-100}` | 50 % | `10` | Harde limiter tegen het H4-plafond (v1.15.0+) |
| `set af {0-9}` *(verouderd)* | `1.0` (~50 %) | `9` (~10 %) | Zelfde doel op firmware ouder dan v1.15.0 |
| `set loop.detect` | `off` | `minimal` | Voorkomt packet storms door een node met afwijkende firmware (v1.14.0+) |
| `set flood.advert.interval {uren}` | 12 | `49` | Minder achtergrondverkeer; adverts zijn flood-pakketten |
| `set advert.interval {minuten}` | 0 | `240` | Voor zero-hop adverts is geen relay-capaciteit nodig |
| `set flood.max.advert` | 8 | 8 | Begrenst hoe ver een advert vloeit |
| `set flood.max.unscoped` | 64 | bijv. `3` | Houdt regioloze floods lokaal |
| `region` (scoping) | — | NL-regio's | Beperkt floods tot de eigen regio |
| `set txdelay` / `direct.txdelay` | `0.5` / `0.2` | default | Willekeurig venster tegen gelijktijdige retransmissies |
| `set repeat` | `on` | `on` | Uitzetten betekent geen relay |

Een repeater hoort bovendien zo min mogelijk *eigen* verkeer te genereren: gebruik zo mogelijk een apart apparaat als je eigen node.

> [!WARNING]
> **⚠ Wie controleert dit?**
> De **Rijksinspectie Digitale Infrastructuur (RDI)**, opvolger van Agentschap Telecom per 1 januari 2023. In de praktijk is handhaving op hobbyist-LoRa zeldzaam, maar bij aanhoudende klachten over storing kan RDI meetapparatuur inzetten en boetes opleggen.

══════════════════════════════════════════════════════════════

## TX ≠ ERP — wat telt mee?

De regelgeving spreekt over **e.r.p.** (Effective Radiated Power) — het totaal uitgestraald vermogen in de richting van maximale antennewinst, referentie halvegolf-dipool. Dat is *niet* hetzelfde als het vermogen dat je LoRa-chip uitstuurt. De formule:

```text
ERP (dBm) = TX-vermogen (dBm) + antennewinst (dBd) − kabel-/connectorverlies (dB)
```

### dBi versus dBd — let op de referentie

Antennes staan meestal in **dBi** op de datasheet (gain t.o.v. isotroop), maar de regelgeving gebruikt **dBd** (gain t.o.v. halvegolf-dipool). De conversie is een constante:

```text
dBi = dBd + 2,15
dBd = dBi − 2,15
```

Dus: een "3 dBi-antenne" op de verpakking heeft maar 0,85 dBd winst — 2,15 dB minder dan je op het eerste gezicht denkt. Voor 2,4 GHz en hoger gebruikt de regelgeving juist e.i.r.p. (dBi-referentie); vergis je daar niet in.

### Praktijktabel SX1262 op +22 dBm

Een standaard SX1262-node op +22 dBm TX-vermogen met 0,2 dB kabelverlies, per antennetype:

| Antenne | Gain (dBi) | Gain (dBd) | ERP (dBm) | ERP (mW) | Status |
|---|---|---|---|---|---|
| Korte rubberduck | 0 | −2,15 | 19,65 | 92 | Binnen H4 ✓ |
| ¼-golf whip | 2 | −0,15 | 21,65 | 146 | Binnen H4 ✓ |
| Dipool | 2,15 | 0 | 21,80 | 151 | Binnen H4 ✓ |
| Collineair 3 dBi | 3 | 0,85 | 22,65 | 184 | Binnen H4 ✓ |
| Collineair 5 dBi | 5 | 2,85 | 24,65 | 292 | Binnen H4 ✓ |
| **Collineair 8 dBi** | 8 | 5,85 | 27,65 | **582** | **⚠ Boven H4** |
| Yagi 10 dBi | 10 | 7,85 | 29,65 | 923 | ⚠ Ver boven H4 |

Opvallend: op +22 dBm zit je al bóven de H5-grens van 25 mW, ongeacht antenne. Strikt juridisch val je dan onder het H4-regime (met 10% DC-plicht én volledige ETSI EN 300 220-compliance tegen de H4-parameters). Bij een 8 dBi-collineair overschrijd je zelfs de H4-bovengrens van 500 mW. Oplossing: TX-vermogen terugschroeven naar +14 dBm (25 mW) om netjes onder H5 te blijven, of antennewinst matigen.

══════════════════════════════════════════════════════════════

## Welk regime geldt voor jouw node?

Per LoRa-chip en module-combinatie:

| Chip / module | Max. TX | In mW | Regime (met standaard dipool-antenne, ~0 dBd) |
|---|---|---|---|
| SX1276 RFO-pin | +14 dBm | 25 mW | Precies op H5-grens ✓ |
| SX1276 PA_BOOST-pin | +20 dBm | 100 mW | Boven H5, onder H4 — valt onder H4-regime |
| SX1262 (standaard) | +22 dBm | 158 mW | Boven H5, onder H4 — valt onder H4-regime |
| LR1121 | +22 dBm | 158 mW | Idem SX1262 |
| Ebyte E22-900M30S (PA) | +30 dBm | 1000 mW | Boven H4-grens — PA-trap terugregelen; `set tx` (1–22 dBm) stuurt alleen de LoRa-chip |

> [!NOTE]
> **De SX1262 grijze zone**
> Vrijwel alle hobbyist-MeshCore-boards (Heltec V3, RAK4631, LilyGO T-Deck) gebruiken de SX1262 op +22 dBm. Dat ligt formeel boven het H5-plafond van 25 mW, dus het apparaat zou aan het zwaardere H4-regime moeten voldoen — met ETSI EN 300 220-compliance tegen de H4-parameters (500 mW / <10% DC) én actieve duty-cycle-bewaking of polite spectrum access. In de praktijk voldoet de meeste hobbyist-hardware daar niet formeel aan.
> Wil je strikt binnen de regels blijven? Stel je TX-vermogen in op **+14 dBm** (25 mW) — dan val je netjes onder het H5-regime en hoeft je apparaat alleen tegen de H5-parameters gecertificeerd te zijn. Je geeft ~8 dB signaalsterkte op, maar dat haal je ruimschoots terug met een degelijke antenne.

══════════════════════════════════════════════════════════════
> [!WARNING]
> **⚠ Disclaimer**
> Deze pagina is informatief en **geen juridisch advies**. Regelgeving wordt periodiek bijgewerkt. Raadpleeg bij twijfel altijd de officiële bronnen hieronder, of neem contact op met de Rijksinspectie Digitale Infrastructuur (RDI).

══════════════════════════════════════════════════════════════

## Bronnen

Alle regelgeving en normen waarop deze pagina is gebaseerd, klikbaar en gegroepeerd per niveau.

### Nederlandse wetgeving

| Document | Rol |
|---|---|
| [Telecommunicatiewet, art. 3.9 (BWBR0009950)](https://wetten.overheid.nl/BWBR0009950) | Wettelijke basis voor vergunningvrij gebruik |
| [Frequentiebesluit 2013 (BWBR0032895)](https://wetten.overheid.nl/BWBR0032895) | Delegatie vergunningvrije categorieën |
| [Regeling frequentieruimte zonder vergunning en zonder meldingsplicht 2015, Bijlage 11 (BWBR0036378)](https://wetten.overheid.nl/BWBR0036378/2025-07-01/0) | Concrete H-regels (H1–H7) — bron van H4 en H5 |
| [Besluit radioapparaten 2016 (BWBR0038910)](https://wetten.overheid.nl/BWBR0038910) | NL-implementatie van RED 2014/53/EU |
| [Rijksinspectie Digitale Infrastructuur (RDI)](https://www.rdi.nl) | Handhavende instantie (voorheen Agentschap Telecom) |

### EU-wetgeving

| Document | Rol |
|---|---|
| [Richtlijn 2014/53/EU (RED — Radio Equipment Directive)](https://eur-lex.europa.eu/eli/dir/2014/53/oj) | Apparatuur-eisen; vervangt 1999/5/EG |
| [Beschikking 2006/771/EG (SRD-basisbeschikking, geconsolideerd)](https://eur-lex.europa.eu/eli/dec/2006/771/oj) | EU-brede spectrum-harmonisatie |
| [Uitvoeringsbesluit (EU) 2025/105](https://eur-lex.europa.eu/eli/dec_impl/2025/105/oj) | Laatste SRD-update (januari 2025) |
| [Uitvoeringsbesluit (EU) 2022/180](https://eur-lex.europa.eu/eli/dec_impl/2022/180/oj) | Voorgaande SRD-update (februari 2022) |

### CEPT / ETSI normen

| Document | Rol |
|---|---|
| [CEPT ERC Recommendation 70-03 (editie maart 2024)](https://docdb.cept.org/download/4635) | CEPT-aanbeveling (bron van de EU-beschikking); Annex 1 bevat de non-specific SRD-banden met identifiers h1.5, h1.6, **h1.7**, h1.8, h1.9 |
| [ETSI EN 300 220-1 V3.1.1 (PDF)](https://www.etsi.org/deliver/etsi_en/300200_300299/30022001/03.01.01_60/en_30022001v030101p.pdf) | Meetmethoden SRD 25–1000 MHz; definitie e.r.p. en bron voor rekenhulp-formule |
| [ETSI EN 300 220-2 V3.3.1 (maart 2025, PDF)](https://www.etsi.org/deliver/etsi_en/300200_300299/30022002/03.03.01_60/en_30022002v030301p.pdf) | Geharmoniseerde norm onder RED — band/vermogen-tabellen |

### Historisch

| Document | Status |
|---|---|
| [Richtlijn 1999/5/EG (R&TTE)](https://eur-lex.europa.eu/eli/dir/1999/5/oj) | Ingetrokken per 13-06-2016, vervangen door RED 2014/53/EU. Nog wel genoemd in de opmerkingen van Bijlage 11. |

> [!NOTE]
> Deze pagina bevatte een interactieve rekenhulp (zendvermogen/EIRP). Die kan markdown niet uitvoeren; de formule staat er nu uitgeschreven.
