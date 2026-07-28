# Regio's: bedoeling en praktijk

*ONTWERPINTENTIE VERSUS NEDERLANDSE PRAKTIJK *

Het oorspronkelijke regiomechanisme van MeshCore kent door zijn ontwerp de 
volgende eigenschappen;
1. het vermijdt een centrale registratie, 
2. maakt van scopes een code die niet te reproduceren (onvervalsbaar) is en
3. zorgt dat er geen permanent herkenbare vingerafdruk over de lucht gaat 
en dat alles binnen twee bytes.

Door de invoering van Regio-codes zoals de Nederlandse communitie dit heeft gedaan
zijn alle drie eigenschappen teniet gedaan.

** De minst slechtse keuze ** Er word echter een reëel probleem mee opgelost, en 
de meeste alternatieven zijn slechter. 

Dit hoofdstuk zet naast elkaar wat de intentie van het ontwerp was, wat men ervan 
gemaakt heeft en wat je inleverd.

Voor het mechanisme zelf — waar de bytes staan en hoe een repeater beslist — zie
[Regio's en Scopes](regions-and-scopes.md). Voor de conventie zelf zie
[MeshWiki — Regio en scope](https://www.meshwiki.nl/wiki/Regio_en_scope). 
Dit hoofdstuk gaat over de spanning tussen die twee.

> [!NOTE]
> **Bron.** Geverifieerd tegen `MeshCore` v1.16.0 —
> `src/helpers/RegionMap.cpp`, `src/helpers/RegionMap.h`,
> `src/helpers/TransportKeyStore.cpp`. Cijfers over gemeentelijke indeling van
> het CBS (peildatum 1 januari 2026), releasecadans van UN/LOCODE van UNECE.

## Intentie van het ontwerp

De scope in een pakket is geen regionummer maar een HMAC over de payload, gezet
met de regiosleutel. Dat kost rekenwerk bij elke hop. Daar staat het volgende
tegenover.

**Geen registratie nodig.** De sleutel volgt uit de naam. Twee mensen die
onafhankelijk `#hiking` aanmaken zitten in dezelfde regio, zonder dat iemand
nummers uitdeelt. Voor een netwerk dat expliciet zonder infrastructuur wil
werken is dat geen detail maar het uitgangspunt.

**Geen permanente botsingen.** Was de code een vaste hash van de naam, dan zou
16 bits binnen een paar honderd regio's structureel gaan botsen:

| Regio's wereldwijd | Kans op minstens één blijvend botsend paar |
|---|---|
| 100 | 7,3 % |
| 200 | 26,2 % |
| 342 | 58,9 % |
| 500 | 85,1 % |

Zo'n botsing is onherstelbaar: twee regio's forwarden dan voor altijd elkaars
verkeer, en de enige uitweg is hernoemen op elke node die de regio kent. Het
HMAC-ontwerp zet die systematische, permanente aliasing om in een onafhankelijke
toevalligheid van 1 op 65536 per pakket. Vergelijkbare foutkans, geen blijvende
structuur. Dat is een hele elegante eigenschap van dit mechanisme.

**Onvervalsbaar en onvolgbaar.** Bij een vast nummer schrijft iedereen dat getal
in zijn pakket en laat het hele land het flooden. En een vast nummer is een
identifier: wie meeluistert kan in kaart brengen welke code bij welke plaats hoort, 
en daarna alle verkeer uit die regio volgen. De HMAC verhindert allebei — mits de
sleutel niet raadbaar is.

Die laatste voorwaarde is waar het misgaat.

## Wat de firmware niet weet

De firmware heeft geen enkel begrip van UN/LOCODE. De sleutel komt uitsluitend
uit de naamstring:

```cpp
int RegionMap::getTransportKeysFor(const RegionEntry& src, TransportKey dest[], int max_num) {
  if (src.name[0] == '$') { ... }          // keystore-regio
  else if (src.name[0] == '#') {           // #hiking
    _store->getAutoKeyFor(src.id, src.name, dest[0]);
  } else {                                  // hiking -> wordt #hiking
    tmp[0] = '#'; strcpy(&tmp[1], src.name);
    _store->getAutoKeyFor(src.id, tmp, dest[0]);
  }
}
```

`src.parent` wordt niet aangeraakt. Geen landcode, geen niveaus, geen validatie.
`#hiking` is een volwaardige regionaam met dezelfde 30 tekens speelruimte als
`#nl-ov-zwo`.

En het beste tegenargument houdt ook geen stand. Je zou kunnen zeggen dat de
gestructureerde naam de hiërarchie draagt — maar de hiërarchie zit in een
parent-pointer die je met `region put <naam> <ouder>` zet, niet in de naam. In
`findMatch()` speelt de ouder geen enkele rol; er wordt per regio los getoetst op
`region->flags`. De boom bepaalt hoe het `region`-commando de lijst toont.
Voor het doorsturen van een pakket doet de `<ouder>` niets.

> [!Belangrijk]
> Je kunt je regio's `#nederland` → `#overijssel` → `#zwolle` noemen, of
> `#hiking`, en er verandert geen enkele byte in het gedrag. De streepjes in
> `nl-ov-zwo` zijn puur conventie.

## Wat men er van gemaakt heeft

In Nederland is die conventie een de-factostandaard geworden, met tools die je
dwingen regio's via UN/LOCODE in te stellen. Daarmee is precies datgene
ingebouwd wat het oorspronkelijke ontwerp vermeed: een centrale registratie. 
Alleen wordt hij nu met de hand bijgehouden in een tabel in plaats van door 
een server.

Dat op zichzelf is nog te verdedigen. Het probleem is wat het met de
sleutelruimte doet.

De sleutel van een `#`-regio is `SHA-256(naam)`. De robustheid van het hele
schema hangt dus af van hoe moeilijk die naam te raden is. Deze eigenschap 
is teniet gedaan; het zijn de 342 Nederlandse gemeenten, aangevuld met twaalf 
provincies en een landcode.

Een luisteraar die de conventie kent, rekent per opgevangen pakket een paar
honderd HMAC's door — triviaal op een laptop — en heeft daarmee exact de kaart
die het ontwerp wilde voorkomen. Welke regio's bestaan, waar en welk verkeer bij 
welke plaats hoort.

**De uitkomst is dus dat je het rekenwerk van een cryptografisch schema betaalt
en de beveiliging van een leesbaar label krijgt.**

Bij vrije namen ligt dat wezenlijk anders. Van `#hiking`, `#wandelclub-teun` of
`#kerstmarkt-deventer` bestaat geen lijst en blijft de regio code onzichtbaar.

## Waar de conventie vandaan komt

De afspraak voor regio's en scopes staat op
[MeshWiki — Regio en scope](https://www.meshwiki.nl/wiki/Regio_en_scope), met de
volledige codelijst op [Lijst van regio's](https://www.meshwiki.nl/wiki/Lijst_van_regio%27s)
en een parallelle indeling op
[LocalMesh.nl](https://www.localmesh.nl/meshcore-regio-indeling/). De opbouw is
vier lagen diep:

| Laag | Standaard | Voorbeeld |
|---|---|---|
| Land | ISO 3166-1 | `nl` |
| Provincie | ISO 3166-2:NL | `nl-nb` |
| Stad | UN/LOCODE | `nl-nb-ein` (Eindhoven stad) |
| Streek | *geen standaard — een verzonnen protocol* | `nl-ehv` (regio Eindhoven) |

Die laatste rij is veelzeggend. `nl-ehv` staat in geen enkele standaard. Hetzelfde
geldt voor de ondubbelzinneg die nodig was bij provincies met een gelijknamige
hoofdstad, waar `nl-ut`, `nl-utc` en `nl-ut-utc` naast elkaar zijn gezet.

**Er wordt dus geen standaard gevolgd; er wordt een register beheerd** — met eigen
codes, eigen uitzonderingsregels en een gepubliceerde lijst. Precies datgene wat niet de 
bedoeling was van het oorspronkelijke ontwerp.

> [!NOTE]
> De wiki opent met de zin dat MeshCore een hiërarchisch systeem voor regio's
> gebruikt dat op internationale standaarden is gebaseerd. Dat leest als een
> eigenschap van MeshCore, en dat is het niet. De firmware kent geen ISO 3166 en
> geen UN/LOCODE; ze kent alleen een naamstring waar een sleutel uit volgt. De
> hiërarchie in de wiki-voorbeelden ontstaat door `region put <naam> <ouder>` —
> een parent-pointer die bij het matchen van een pakket geen rol speelt.

De Wiki is verder goed opgezet: de configuratievoorbeelden per repeater kloppen, de
waarschuwing dat je na het instellen van regio's moet rebooten is terecht, en het
advies om de wildcard `*` voorlopig aan te houden is precies goed. De kritiek in
dit hoofdstuk gaat niet over die praktijk maar over wat de naamkeuze doet met de
eigenschappen van het onderliggende mechanisme — iets wat nergens ter sprake komt,
omdat niemand een reden had om te vermoeden dat de naam er cryptografisch toe doet.

## Het gevolg

Je levert iets in — de vrijheid om het naar eigen inzicht te doen — en krijgt er 
terugvindbaarheid voor.

Bij een noodnet in een DARES achtige situatie is vindbaarheid geen bijzaak. 
Iemand die met een verse node in Overijssel aankomt moet kunnen weten welke regio 
hij instelt zonder eerst een Discord-server of een Wiki te zoeken etc. 
Een voorspelbare naam is dan functioneel, geen lek. Voor NoodNet Overijssel is 
de keuze goed verdedigbaar.

Wat ontbreekt is dat hij ergens als keuze wordt benoemd. Een besloten
wandelgroep heeft niets aan vindbaarheid, en levert nu gratis het enige in wat
de crypto hem te bieden had. Die groep hoort te weten dat `#wandelclub-teun`
bestaat en beter bij haar past.

## De conventie als noodoplossing

Het lijkt een kwestie van ordelijkheid, maar de conventie lost een wezenlijk 
probleem op: het MeshCore-protocol biedt (nog steeds) geen enkele manier om 
regio's te ontdekken. Nodes kunnen elkaar niet vragen op welke regio's ze actief 
zijn; die vraag bestaat niet in het protocol. 

Daardoor blijft er één werkende methode over: pakketten uit de ether opvangen, 
kandidaatnamen doorrekenen en kijken welke naam de waargenomen code oplevert. 
Dat lukt alleen doordat de vaste naamvorm het aantal kandidaten eindig houdt.

De conventie ís dus het ontdekmechanisme. Ze bestaat niet omdat iemand orde 
wilde scheppen, maar omdat het protocol hier iets laat liggen en dit het enige 
beschikbare middel was. Dat je regionaam daardoor te achterhalen is, is geen 
slordigheid maar een bewuste keus.

## Wat het kost

**Een stille faalmodus.** Stel je een regio in die geen repeater in je bereik
draagt, dan levert `findMatch()` `NULL`, blijft `recv_pkt_region` leeg, geeft
`allowPacketForward()` `false`, en verdwijnt het pakket. Geen foutmelding, geen
ack, niets — flood-verkeer kent geen terugkoppeling van repeaters. Je bent dan
*slechter af dan zonder scope*: ongescoopt verkeer wordt onder de wildcard nog
doorgestuurd, alleen met een lagere hoplimiet. Een verkeerd ingestelde scope
levert geruisloos nul bereik op.

**Een register dat UN/LOCODE niet kan leveren.** De naamlijst is stabiel: het
aantal Nederlandse gemeenten staat sinds 2023 op 342, en UN/LOCODE kent
cut-offdata van 31 maart en 30 september. Dat is het makkelijke deel. Wat
werkelijk bijgehouden en gecommuniceerd moet worden is de *levende toestand*:
welke repeater draagt welke regio, op welk niveau werken mensen feitelijk, welke
niet-LOCODE-regio's zijn in omloop. Die verandert telkens wanneer iemand aan een
node zit — en volgt uit geen enkele externe standaard.

**Rekenwerk.** Tot 32 regio's × 4 sleutels = 128 HMAC-SHA256-berekeningen over
50–190 bytes per flood-pakket, op een nRF52 of ESP32, vóór er iets besloten is.

**Een hardnekkig verkeerd mentaal model.** De term "regiocode", documentatie(Wiki)
die een opzoektabel suggereert, en tools die een registratie afdwingen wijzen alle
drie dezelfde kant op: dat regiocodes worden *uitgegeven*. 
De broncode laat duidelijk zien dat dit niet zo is.

## Wat de broncode ons verteld

De broncode is de enige plek waar de oorspronkelijke opzet opzet terug te vinden
is, en wie hem decodeert ziet iets anders dan wat er in de praktijk gebeurt.

Het schema is ontworpen voor `$`-regio's, met een sleutel uit de keystore die
niet uit de naam volgt. Daar zijn onvervalsbaarheid en onvolgbaarheid echt. Alleen:
`TransportKeyStore` is in v1.16.0 een stub. `saveKeysFor()` bevat
`// TODO: update hardware keystore` en geeft `false` terug; `loadKeysFor()` heeft
alleen een RAM-cache met `// TODO: retrieve from difficult-to-copy keystore`.
Dezelfde signalen staan er overal: `transport_code_2` gereserveerd voor de
thuisregio, `REGION_DENY_DIRECT` met `// reserved for future`, nieuwe regio's die
standaard op *deny* staan.

**Deze code had niet zo ingewikkeld hoeven te zijn op de wijze zoals in Nederland 
de regio code is geimplementeerd. ** Wat vandaag werkt is uitsluitend het type 
waarbij de sleutel uit een raadbare naam volgt.

En daar lopen de twee uit elkaar. De broncode gaat uit van namen die niemand kan
raden. De praktijk gebruikt namen die iedereen kan opzoeken. Beide zijn intern
consistent; samen zijn ze het niet.

## Een opzoektabel had volstaan

Al met al kun je concluderen dat een opzoektabel had volstaan. Simpelere code
en minder CPU gebruik.

Zodra er een beheerde, gepubliceerde lijst bestaat, wijs je codes gewoon *toe* en
deel je er nooit een dubbel uit. Het botsingsprobleem verdwijnt per definitie. En
die lijst bestaat: dat is precies wat MeshWiki en LocalMesh bijhouden.

Daarmee valt het belangrijkste argument voor het HMAC-schema weg, juist in het
scenario waarin Nederland het gebruikt:

| | HMAC over de payload (nu) | Toegewezen code uit het register |
|---|---|---|
| Registratie nodig | nee — maar er is er tóch een | ja — en die is er al |
| Botsingen | 1 op 65536 per pakket, willekeurig | nul, je wijst ze toe |
| Rekenwerk per pakket | tot 128× HMAC-SHA256 | één vergelijking |
| Capture te labelen | nee | ja |
| Vervalsbaar | in theorie nee, met raadbare naam ja | ja |
| Volgbaar door meeluisteraar | ja, namen zijn opsombaar | ja |
| Stille faalmodus | ja | ja |

Overal is de uitkomst gelijk of slechter, behalve op rekenwerk en
debugbaarheid — en daar wint de tabel.

Er is geen tabel in de firmware vereist: de codes worden nu óók met de hand ingetypt, 
uit dezelfde gepubliceerde lijst. `region put nl-nb` zou net zo goed `region put nl-nb 0x0042` 
hebben kunnen zijn, met het nummer uit de wiki. Even veel werk voor de operator, 
geen firmware-update nodig, en geen van de kosten.

> [!Belangrijk]
> **Zoals Nederland regio's gebruikt, doet het HMAC-schema niets wat een simpele
> opzoektabel niet ook had gedaan.** Het rekenwerk wordt betaald, het register
> wordt bijgehouden, de namen zijn opsombaar, de codes zijn terug te rekenen.
> Wat overblijft is de complexiteit.
>
> Dat is geen argument om het protocol te veranderen — het schema is niet voor
> deze werkwijze bedoeld. Het is een argument om te weten wat je kiest: wie de
> gepubliceerde lijst gebruikt, gebruikt in feite een opzoektabel, en zou daar
> ook de verwachtingen van een opzoektabel bij moeten hebben.

## Wat het zou oplossen

Eén protocolfunctie: een repeater die zijn regio's aankondigt. Dan is er geen
centrale tabel nodig, kunnen namen vrij en onraadbaar zijn, verdwijnt de stille
faalmodus, en houdt het HMAC-schema de eigenschappen waarvoor het is gebouwd.

Zolang die er niet is, is er geen goede uitweg — alleen een keuze:

| | Vindbaar | Onvolgbaar |
|---|---|---|
| `#nl-ov-zwo` (conventie) | ✔ vreemden vinden je zonder te vragen | ✘ opsombare lijst, code triviaal terug te rekenen |
| `#wandelclub-teun` (vrij) | ✘ moet buiten het mesh om gedeeld worden | ✔ geen kandidatenlijst |
| `$besloten` (keystore) | ✘ sleutel buiten het mesh om gedeeld | ✔ echt — maar werkt nog niet in v1.16.0 |

## Praktisch

- **Noodnet, openbare infrastructuur, repeaters.** Gebruik de LOCODE-conventie.
  Vindbaarheid weegt hier zwaarder, en dat is een verdedigbare keuze.
- **Besloten groep.** Gebruik een vrije naam en deel hem buiten het mesh om. Je
  levert niets in wat je nodig had, en je haalt terug wat de conventie weggeeft.
- **Verwacht geen vertrouwelijkheid van een scope.** Die rol speelt de kanaal-PSK,
  en die alleen. Een regio bespaart airtime; meer niet.
- **Controleer of je scope ergens landt.** Er komt geen foutmelding. Test met een
  bekende repeater voordat je aanneemt dat het werkt.

## Bronnen

- [MeshCore firmware — `src/helpers/RegionMap.cpp`](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/RegionMap.cpp)
- [MeshCore firmware — `src/helpers/TransportKeyStore.cpp`](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/TransportKeyStore.cpp)
- [CBS — gemeentelijke indeling op 1 januari 2026](https://www.cbs.nl/nl-nl/onze-diensten/methoden/classificaties/overig/gemeentelijke-indelingen-per-jaar/indeling-per-jaar/gemeentelijke-indeling-op-1-januari-2026)
- [UNECE — UN/LOCODE](https://unece.org/trade/uncefact/unlocode)
- [MeshWiki — Regio en scope](https://www.meshwiki.nl/wiki/Regio_en_scope) — de conventie
- [MeshWiki — Lijst van regio's](https://www.meshwiki.nl/wiki/Lijst_van_regio%27s) — de codelijst
- [LocalMesh.nl — MeshCore regio-indeling](https://www.localmesh.nl/meshcore-regio-indeling/)
- [Regio's en Scopes](regions-and-scopes.md) — het mechanisme zelf
