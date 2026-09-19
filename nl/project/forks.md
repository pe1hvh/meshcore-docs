# Forks & varianten

*AFSPLITSINGEN · REPEATERBELEID · COMPANION · MEETMETHODE*

Van `meshcore-dev/MeshCore` bestaan ruim duizend forks. Verreweg de meeste
bevatten geen eigen werk. Deze pagina beschrijft de twaalf afsplitsingen waarin
wel wordt doorontwikkeld: wat elke fork functioneel toevoegt, en hoe ver hij op
de peildatum van upstream af staat. Waar [GitHub Repositories](github.md)
catalogiseert wat er bestaat, beschrijft deze pagina wat de afsplitsingen anders
doen.

> [!NOTE]
> **Bron.** De cijfers op deze pagina zijn zelf gemeten, niet overgenomen uit
> README's of samenvattingen van derden. De forklijst is via de GitHub-API
> opgehaald en op sterren gesorteerd; daarvan zijn 300 forks bekeken van de
> circa 1300 die de API meldt — de niet-opgehaalde staart heeft per definitie
> nul sterren. Van elke uitgelichte fork is de actieve branch lokaal opgehaald
> en met `git merge-base` en `git rev-list` tegen upstream `dev` gezet. De
> functionele beschrijvingen komen uit de documentatie van de fork, en waar die
> ontbrak of onduidelijk was uit de broncode. Bij de meting is geen commit-hash
> van upstream `dev` vastgelegd; de vergelijking geldt voor de stand van
> 19 september 2026. Er is niets van deze firmware op hardware getest, dus deze
> pagina doet geen uitspraken over stabiliteit of praktijkprestaties en spreekt
> geen voorkeur uit voor een fork.

De meting is te herhalen met drie commando's, waarbij `up` de remote naar
`meshcore-dev/MeshCore` is:

```bash
git merge-base up/dev <fork-branch>          # gemeenschappelijk vertrekpunt
git rev-list --count <base>..<fork-branch>   # eigen commits
git rev-list --count <base>..up/dev          # achterstand
```

## Hoe het forklandschap eruitziet

Van de 300 bekeken forks:

| Kenmerk | Aantal |
|---|---|
| Nul sterren | 167 |
| Eigen beschrijving geschreven | 39 |
| Repository hernoemd | 49 |
| Meer dan een half jaar niet aangeraakt | 72 |

De ruwe conclusie uit die vier regels: ruim 80% van de bekeken forks bevat geen
eigen werk. Iemand forkt om één bord toe te voegen, één regel te wijzigen of de
code te bewaren. Het aantal van 1300 zegt daarmee weinig over het aantal
varianten dat er werkelijk toe doet.

## Stand per fork op de peildatum

**Peildatum: 19 september 2026.** Deze tabel is een momentopname en veroudert
dagelijks; de rest van de pagina niet. *Eigen* is het aantal commits dat de fork
vóórloopt op het gemeenschappelijke vertrekpunt met upstream `dev`, *achter* het
aantal dat upstream sindsdien heeft toegevoegd.

| Fork | Actieve branch | Eigen | Achter | Laatste commit |
| --- | --- | ---: | ---: | --- |
| jhuebert | `repeater-filter` | 46 | 4 | 17-09 |
| weebl2000 | `dev_plus` | 276 | 14 | 15-09 |
| l5yth (meshcore-linux) | `linux` | 16 | 56 | 30-08 |
| Dutch-MeshCore | `dmc-dev` | 39 | 29 | 14-09 |
| MichTronics (MeshCoreNG) | `main` | 265 | 122 | 10-09 |
| ksanislo (LVGL) | `main` | 294 | 122 | 15-08 |
| tek126 (mtbeacon) | `meshtastic-beacon` | 28 | 122 | 29-08 |
| MarekZegare4 (Solo) | `main` | 709 | 122 | 08-09 |
| jooray (BitChat) | `feature/bitchat-bridge` | 27 | 169 | 10-08 |
| Meshcore-Portugal (lusofw) | `main` | 122 | 481 | 01-07 |
| TogeriX-hub (FieldMesh) | `main` | 55 | 760 | 28-04 |
| mattzzw (Evo) | `meshcore-evo` | 27 | 1337 | 17-01 |

De kolom *achter* is het bruikbaarste getal van de tabel. Boven de honderd mis je
de recente correcties uit upstream; boven de vijfhonderd is de fork praktisch een
doodlopend spoor, ongeacht het aantal sterren.

## Wat de forks toevoegen

De volgorde hieronder loopt van veel naar weinig toegevoegde functionaliteit voor
een Nederlandse repeater, niet van nieuw naar oud.

### jhuebert — repeaterfilter op kanaalidentiteit

[jhuebert/MeshCore](https://github.com/jhuebert/MeshCore), branch
`repeater-filter`.

**Sterk punt: filterregels die op de werkelijke kanaalidentiteit matchen, bij een
fork die vrijwel gelijk loopt met upstream.**

Eén regel kan pakkettype, routetype (flood of direct), regio, hopbereik,
payloadlengte, bereik van de Signal-to-Noise Ratio (SNR), pad-hashgrootte en
kanaal combineren, met als actie doorlaten, laten vallen of alleen loggen. Eerste
match wint.

Kanaalfiltering kan op twee manieren. De grove manier is de 1-byte air hash — in
de code zelf aangemerkt als botsingsgevoelig. De hoofdweg is een kanaal
registreren met zijn werkelijke Pre-Shared Key (PSK): de repeater ontsleutelt het
groepsbericht en matcht op de echte kanaalidentiteit, en desgewenst ook op
afzendernaam of op de berichttekst via een eigen, compacte engine voor reguliere
expressies.

Verder:

- **Snelheidslimiet op flood-adverts per node**, met een venster tot dertig
  dagen.
- **Onder een instelbare accuspanning stopt de repeater met doorgeven**, maar
  blijft bereikbaar en blijft adverteren; herstelt automatisch, met debounce en
  hysterese. Bedoeld voor solar- en off-grid-locaties.
- **Beheer op afstand over de mesh** door een geauthenticeerde beheerder, naast
  de gewone seriële [CLI](../cli/introduction.md).
- **Wekelijkse automatische synchronisatie met upstream** via een
  geautomatiseerde workflow, plus twee releasekanalen: een dev-kanaal op
  `dev`-basis en een stabiel kanaal op upstream-releases.

Die automatische synchronisatie is achteraf gezien waardevoller dan het filter
zelf: het is de reden dat deze fork de kleinste achterstand van de twaalf heeft
terwijl de rest wegdrijft.

**Aandachtspunt.** Filteren op afzender of tekst vereist dat de PSK in de
repeater staat en dat de repeater meeleest. Voor een spammer op een publiek
kanaal is dat verdedigbaar; voor noodcommunicatie maakt het van een doorgeefluik
een instantie die op inhoud beslist. Een verkeerd gestelde reguliere expressie
laat een hulpvraag stil verdwijnen. Daarnaast draait die expressie per pakket op
door de afzender aangeleverde tekst — de code parst zichtbaar defensief, maar het
blijft een aanvalsoppervlak dat de andere forks niet hebben.

### Dutch-MeshCore — expliciete regels en een correcte duty cycle

[Dutch-MeshCore/MeshCore](https://github.com/Dutch-MeshCore/MeshCore), branch
`dmc-dev`. De branch `main` is hier een spiegel van upstream; het werk staat op
`dmc-dev`.

**Sterk punt: de automatische afleiding van de duty cycle, en een filter waarvan
je kunt zien wat het weggooit.**

**Duty cycle op `auto`.** Upstream heeft sinds v1.15 een instelbare limiet met
50% als standaard. Deze fork maakt `auto` de standaard: de limiet volgt de
subband waarop het knooppunt is afgestemd, en wordt opnieuw bepaald zodra
`set freq` of `set radio` die frequentie verandert.

| Subband (MHz) | Limiet |
|---|---|
| 863,0 – 865,0 | 0,1% |
| 865,0 – 868,0 | 1% |
| 868,0 – 868,6 | 1% |
| 868,7 – 869,2 | 0,1% |
| 869,4 – 869,65 | 10% |

Buiten 863–870 MHz betekent `auto` geen limiet. Dit is de belangrijkste wijziging
van de fork; de aanbeveling om hem naar upstream terug te brengen staat onderaan
deze pagina. De Nederlandse regels waar dit op aansluit staan in
[Regelgeving & Duty Cycle](../gebruik/regulations.md).

**Pakketfilter.** Standaard uit. Direct gerouteerd verkeer en prioriteitsverkeer
van bekende contacten uit de Access Control List (ACL) passeren altijd; alleen
floodverkeer wordt gefilterd. Vijf mechanismen:

- **Hopgrens per pakkettype**, voor elk van de twaalf types afzonderlijk.
- **Snelheidslimiet per type**, met optioneel een geleidelijke afknijping: tot
  een ondergrens alles doorlaten, daarboven een lineair dalende doorgeefkans, bij
  de harde grens dicht. Dat voorkomt dat een abrupte grens legitiem verkeer
  meesleurt op het moment dat een spammer de teller volgooit.
- **Kanaalblokkering**, maximaal zestien namen.
- **Minimale pad-hashlengte** — de documentatie waarschuwt er zelf bij dat een
  minimum van 2 vrijwel al het floodverkeer wegneemt, niet alleen het misbruik.
- **Controle op misvormde groepsberichten.**

Belangrijker dan de filters zelf: `filter stats <onderwerp>` meldt per reden
hoeveel er is weggegooid, zodat je kunt zien of een regel iets doet voordat je
hem scherper zet.

De kanaalblokkering heeft een beperking. Er wordt gematcht op één byte, afgeleid
uit de kanaalnaam. Daardoor deelt ruwweg één op de 256 andere kanalen die waarde
en wordt onbedoeld meegeblokkeerd. Kanalen met een eigen willekeurige PSK kunnen
niet worden opgegeven, want de hash is dan niet uit de naam te reconstrueren.
Alleen groepsteksten worden geraakt, en er is geen witte lijst — uitsluitend een
zwarte lijst.

**Regio's tijdelijk sluiten bij een hoge duty cycle.** Uit tenzij ingeschakeld.
Stijgt de eigen TX-duty-cycle boven de drempel (standaard 70%), dan sluit de
repeater regio's van buiten naar binnen af: eerst de wildcard, dan de breedste
benoemde regio's. De binnenste laag en de thuisregio blijven altijd open. Onder
drempel min hysterese (standaard 60%) gaan ze weer open van binnen naar buiten,
met een kleine willekeurige vertraging per stap zodat naburige repeaters niet in
lockstep herstellen. De regiohiërarchie waar dit op steunt staat in
[Regio's en Scopes](../techniek/regions-and-scopes.md).

Het sluiten is uitdrukkelijk tijdelijk: het wordt nooit naar de regioconfiguratie
geschreven, zodat een `region save` of een herstart midden in een piek geen
permanente blokkade kan achterlaten. Volgorde per pakket: eerst de regiostap, dan
het pakketfilter.

### MeshCoreNG (MichTronics) — meten en automatisch dempen

[MichTronics/MeshCoreNG](https://github.com/MichTronics/MeshCoreNG), branch
`main`.

**Sterk punt: het is de enige fork die het gedrag van een repeater in een druk
net meetbaar maakt.**

Expliciet ontwikkeld vanuit Nederland, met het argument dat een klein,
dichtbevolkt land met de duty-cycle-limieten van EU868 precies de plek is waar
problemen met een dicht mesh het eerst zichtbaar worden.

- **`get dense.stats`** toont ontvangen, doorgegeven en verworpen adverts,
  dubbele floodpakketten, geschatte RX/TX-airtime, aantal
  kanaal-bezet-detecties, en een dichtheids- en congestieniveau. Alleen in RAM;
  weg na herstart.
- **Minder adverts doorgeven naarmate het hopgetal oploopt** — een basisfactor
  (standaard 0,308) bepaalt hoe sterk dat gebeurt. 0 is niets doorgeven, 1 is
  alles zoals voorheen.
- **`flood.relay.prob` 0–255** — de kans waarmee floodverkeer wordt doorgegeven,
  bijvoorbeeld de helft.
- **Kanaal-bezet-detectie via Channel Activity Detection (CAD) in hardware**
  vóór het zenden.
- **Naburige repeaters uit fase houden** — bovenop de bestaande willekeurige
  `txdelay` een kleine, vaste offset afgeleid van de node-identiteit, stabiel
  over herstarts, zodat repeaters niet gelijktijdig beginnen te zenden.
- **Onderdrukking bij dubbel horen** — hoort een repeater vóór het aflopen van
  zijn eigen timer genoeg anderen hetzelfde pakket doorgeven, dan annuleert hij
  zijn eigen retransmissie.
- **Accubewaking bij opstart en tijdens bedrijf** — onder een ingestelde spanning
  gaat de node slapen en probeert later opnieuw, in plaats van radio, GPS en
  scherm aan te zetten en de accu verder leeg te trekken.
- **Nederlandse regio-opzoektabel** — 2484 plaatsen over twaalf provincies,
  gegenereerd uit de MeshWiki-lijst en als tabel in flash opgeslagen, met een
  `regiondb`-commando. Nadrukkelijk een opzoektabel náást de bewerkbare
  regiomap, niet erin. Zie
  [Regio's: bedoeling en praktijk](../techniek/regions-in-practice.md).

Een aangekondigde dynamische modus is aanwezig maar doet in deze versie nog
niets; de auteurs willen eerst gegevens uit echte netwerken verzamelen voordat de
firmware zelf beslissingen neemt.

### weebl2000 — de gehardde dev-tak

[weebl2000/meshcore](https://github.com/weebl2000/meshcore), branch `dev_plus`.

**Sterk punt: correctheid en veiligheid, bij de best bijgehouden fork van de
zware afsplitsingen.**

Geen nieuwe functies om over op te scheppen, wel de dingen die stilletjes
misgaan:

- Constante-tijdvergelijking bij de verificatie van de Message Authentication
  Code (MAC), in plaats van een gewone geheugenvergelijking.
- Grenscontroles gerepareerd bij het verwerken van PATH- en TRACE-payloads.
- Fouten rond het overlopen van de millisecondenteller opgelost; tijd overleeft
  nu een warme reset op nRF52.
- Watchdog toegevoegd, en beveiliging tegen defecte kristallen bij het opstarten.

Functioneel erbij: duty cycle afdwingen via een token bucket, dynamische
CAD-gevoeligheid, een codeersnelheid die zich aanpast aan de gemeten SNR bij
retransmissie, en een reeks nieuwe boards (RAK11200/13300, ThinkNode M4, T-Beam
Supreme S3).

Dit is de enige fork die de routeringskern zelf substantieel aanraakt.

### meshcore-linux (l5yth) — native op de Raspberry Pi

[l5yth/meshcore-linux](https://github.com/l5yth/meshcore-linux), branch `linux`.

**Sterk punt: geen microcontroller meer nodig, en klein genoeg om bij te
houden.**

Draait dezelfde firmwarecode native op een Raspberry Pi met een SX1262 aan de
SPI-bus, via een Arduino-API-laag voor Linux. Levert een `meshcored`-daemon op.
Getest op Pi Zero tot en met Pi 5. Met een klein aantal eigen commits is dit een
fork die zonder veel moeite actueel te houden is.

### Solo (MarekZegare4) — het knooppunt als zelfstandig apparaat

[MarekZegare4/MeshCore-Solo](https://github.com/MarekZegare4/MeshCore-Solo),
branch `main`.

**Sterk punt: volwaardig bruikbaar zonder telefoon.**

Berichten lezen en typen op het scherm; waypoints zetten en terugnavigeren;
kompas afgeleid uit de koers over de grond, dus zonder magnetometer; route-opname
met export naar een GPX-bestand; locaties delen en live positie uitzenden;
geofence met alarm bij aankomst of vertrek, met een zoemer die sneller piept
naarmate je dichterbij komt; klok met alarm, timer en stopwatch;
schermvergrendeling; sensorschermen; en toetsenbordindelingen voor tien talen.
Werkt met externe CardKB-toetsenbordjes.

### FieldMesh (TogeriX-hub) — buitengebruik

[TogeriX-hub/FieldMesh](https://github.com/TogeriX-hub/FieldMesh), branch `main`.

**Sterk punt: corrigeert de frequentie-instellingen van Client Repeat.**

De auteur stelt dat de upstream-standaarden voor Client Repeat onbruikbaar of
illegaal waren: 433 MHz een enkele illegale puntfrequentie, 869 MHz in een
subband met 0,1% duty cycle, en 915 MHz buiten de band in sommige regio's.
FieldMesh zet er legale waarden voor in de plaats en biedt een Off-Grid-modus met
één druk op de knop, op 869,4625 MHz, die de normale parameters bewaart zodat je
terug kunt. Wat Client Repeat zelf doet staat in
[Off-Grid Client Repeat Mode](../gebruik/off-grid.md).

Verder: automatische GPS-advert elke vijf minuten, standaard zero-hop zodat het
bredere net er niet onder lijdt; een aparte pagina met posities en afstanden van
favoriete contacten; berichtgeschiedenis op het apparaat; en een SOS-knop met
zoemer.

Deze fork staat ver achter op upstream — zie de tabel hierboven. De ideeën zijn
interessanter dan de code.

### lusofw (Meshcore-Portugal) — distributie, geen afsplitsing

[Meshcore-Portugal/lusofw](https://github.com/Meshcore-Portugal/lusofw), branch
`main`.

**Sterk punt: expliciet gepositioneerd als release- en testkanaal, niet als harde
afsplitsing.**

Standaard 433 MHz, brug standaard uit, tijdsynchronisatie op basis van
advertgegevens, duty cycle via een token bucket, een kansmechanisme dat de
doorgifte van adverts beperkt, en adverts alleen doorgeven in een
onderhoudsvenster tussen 02:00 en 07:00. Buren ouder dan 48 uur vallen
automatisch weg. Eigen regio `#portugal`, standaard op flood.

### mtbeacon (tek126) — zichtbaar op Meshtastic

[tek126/MeshCore-mtbeacon](https://github.com/tek126/MeshCore-mtbeacon), branch
`meshtastic-beacon`.

**Sterk punt: smal afgebakend en goed gedocumenteerd.**

Laat een MeshCore-repeater zich periodiek aankondigen op een
Meshtastic-netwerk, zodat Meshtastic-gebruikers een tekstregel zien verschijnen.
De README legt duidelijk uit waarom dat werk vergt: de twee gebruiken een ander
sync word (`0x12` tegen `0x2B`), andere bandbreedte en spreading factor, en
andere framing — de radio's horen elkaar simpelweg niet. Voor één pakket doet de
repeater zich dus voor als Meshtastic-zender.

### BitChat (jooray) — brug naar een ander protocol

[jooray/MeshCore-BitChat](https://github.com/jooray/MeshCore-BitChat), branch
`feature/bitchat-bridge`.

**Sterk punt: het idee.**

Een brugapparaat dat berichten doorgeeft tussen BitChat-gebruikers en MeshCore.
Omdat de bluetoothverbinding daarvoor bezet is, configureer je dat knooppunt via
USB-serieel.

**Aandachtspunt bij de kwaliteit.** Van de circa 45.000 toegevoegde regels is
ongeveer de helft per ongeluk meegecommitte build-logbestanden in een `tmp`-map.

### LVGL (ksanislo) — tweede grafische companion

[ksanislo/MeshCore-LVGL](https://github.com/ksanislo/MeshCore-LVGL), branch
`main`.

**Sterk punt: de release-infrastructuur eromheen.**

Geen nieuwe netwerkfuncties, wel een volledig tweede companion met grafische
interface. Interessanter is het omhulsel: Over-The-Air-updates (OTA) over wifi,
coredumps naar SD-kaart met de bijbehorende debugsymbolen bewaard zodat crashes
achteraf leesbaar zijn, en eigen, rechtenvrije meldingsgeluiden.

### Evo (mattzzw) — waarschuwing

[mattzzw/MeshCore-Evo](https://github.com/mattzzw/MeshCore-Evo), branch
`meshcore-evo`.

Een bekende naam in dit rijtje, maar de actieve branch heeft de grootste
achterstand van de twaalf en is al maanden niet aangeraakt — zie de tabel
hierboven. De reputatie loopt ver achter op de werkelijkheid. Opgenomen om die
reden, niet om de inhoud.

## Wat hieruit volgt

**De routeringskern is onomstreden.** Vrijwel alle toegevoegde functionaliteit
zit in drie hoeken: companion-interface, repeaterbeleid, en nieuwe boards of
platforms. Alleen weebl2000 raakt de kern substantieel aan, en dan nog vooral om
te repareren. Dat is in feite een compliment aan upstream — het protocol zelf is
niet waar men het oneens over is.

**Er wordt veel dubbel gebouwd.** Minstens vier onafhankelijke
companion-interfaces en twee onafhankelijk geschreven pakketfilters. Het verlies
in dit ecosysteem zit niet in het forken maar in het drie keer bouwen van
hetzelfde.

**Twee filosofieën bij hetzelfde probleem.** MeshCoreNG meet en dempt continu en
automatisch; Dutch-MeshCore laat de beheerder expliciete regels stellen en grijpt
alleen automatisch in bij een piek; jhuebert biedt de meest gedetailleerde regels
maar vraagt daarvoor inzage in de berichtinhoud. Voor noodcommunicatie pleit de
tweede aanpak het sterkst, omdat je achteraf moet kunnen uitleggen waarom een
pakket niet is doorgekomen.

**Afsplitsen vergt permanent samenvoegwerk.** Wie afsplitst, moet elke
upstream-wijziging zelf blijven samenvoegen. Van de twaalf besproken forks houden
er drie werkelijk gelijke tred, en de enige die dat structureel heeft opgelost —
jhuebert, met wekelijkse automatische synchronisatie — dankt dat aan
automatisering, niet aan discipline.

## Eén aanbeveling voor upstream

Van alles op deze pagina is er één wijziging die zonder discussie in de originele
repository thuishoort: de **automatische afleiding van de duty cycle uit de
frequentie** van Dutch-MeshCore.

De standaardfrequentie in de upstream-configuratie is 869,618 MHz, wat in de
subband met 10% duty cycle valt. De standaardinstelling is 50%, ofwel airtime
factor 1,0 — vijf keer de toegestane zendtijd. Dit is bovendien een SRD-band, dus
een zendmachtiging helpt hier niet; die geldt voor de amateurbanden. Upstream
zegt dat ook zelf bij de verouderde `af`-parameter: de gebruiker is
verantwoordelijk voor een waarde die bij zijn jurisdictie past. De Nederlandse
kant daarvan staat in
[Regelgeving & Duty Cycle](../gebruik/regulations.md), de commando's in
[Routing](../cli/routing.md).

Nuance die erbij hoort: het is een plafond, geen streefwaarde. Een normale
repeater komt niet in de buurt van 50%, dus in de dagelijkse praktijk gebeurt er
niets. Maar de instelling is stilzwijgend permissief op precies het moment dat
het druk wordt — en dat is het moment waarop hij bedoeld was om te werken.

De oplossing breekt niets aan het protocol, raakt geen enkele client en is puur
een correctheidskwestie.

## Bronnen

- [MeshCore firmware — `meshcore-dev/MeshCore`, branch `dev`](https://github.com/meshcore-dev/MeshCore/tree/dev)
  — het vergelijkingspunt voor alle getallen op deze pagina.
- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
  — `set dutycycle` en `set af`, commit `03b6ef4` (v1.16.0).
- De repositories van de twaalf forks: de link staat bij elke fork hierboven.
  Functionele beschrijvingen komen uit de documentatie en de broncode van die
  repositories, zoals opgehaald op 19 september 2026.
