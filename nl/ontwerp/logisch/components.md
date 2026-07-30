# Componenten

*VERANTWOORDELIJKHEDEN · GRENZEN · WIE WEET WAT*

MeshCore bestaat uit een handvol componenten met scherp afgebakende
verantwoordelijkheden. Dit hoofdstuk beschrijft wat elk onderdeel doet en —
belangrijker — wat het níét weet. De grenzen tussen de componenten zijn wat
het ontwerp draagbaar maakt: dezelfde mesh-logica draait op vier
platformfamilies zonder er iets van te merken.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — `src/MeshCore.h`,
> `src/Dispatcher.h`, `src/Mesh.h`, `src/Packet.h`, `src/Identity.h` en de
> abstracties onder `src/helpers/`.

## De stapel in één beeld

![Drie lagen boven elkaar. Onderaan de hardware-abstracties radio, bord, klok
en toevalsbron; in het midden de pakketafhandeling en de mesh-logica; bovenaan
de applicatie. Naast de stapel staan de ondersteunende componenten voor opslag,
rechten, bediening en koppelvlakken.](../../../images/nl/components-1.svg)

## De kern

### Pakketafhandeling

De onderste laag met eigen logica. Verantwoordelijk voor: luisteren of er iets
binnenkomt, binnengekomen bytes tot een pakket maken, uitgaande pakketten in
een wachtrij zetten en op het juiste moment uitzenden. Hij bewaakt daarbij het
zendtijdbudget en houdt tellers bij van wat er verzonden en ontvangen is.

Wat deze laag níét weet: waar een pakket over gaat. Hij kent geen berichten,
geen contacten en geen versleuteling. Voor hem is een pakket een blok bytes met
een prioriteit en een moment waarop het weg mag.

### Mesh-logica

De laag erboven. Hier wordt een pakket voor het eerst geïnterpreteerd: welk
type is het, is het voor deze node bestemd, moet het worden doorgegeven, en zo
ja met hoeveel vertraging. Hier zit ook de beslissing om een pakket te laten
vallen omdat het al eerder langskwam.

Wat deze laag níét weet: hoe de radio werkt, en wat de applicatie met een
bericht gaat doen. Hij biedt de applicatie een reeks aanknopingspunten aan en
vult zelf niets in.

### Applicatie

De rol uit [Rollen](roles.md). Hier staat het gedrag dat een repeater een
repeater maakt en een room server een room server. De applicatie bepaalt wat er
met een binnengekomen bericht gebeurt, wanneer er zelf iets wordt verstuurd, en
wat er op het scherm komt.

## De hardware-abstracties

Vier componenten schermen de rest van de firmware af van de hardware. Ze zijn
allemaal zuiver: ze bevatten geen mesh-logica, alleen een vertaling naar wat
het bord kan.

| Component | Verantwoordelijk voor | Weet niets van |
|---|---|---|
| Radio | Bytes de lucht in en uit krijgen, zendtijd schatten, signaalsterkte melden | Pakketten, adressering, versleuteling |
| Bord | Batterijspanning, temperatuur, herstart, slaapstand, opstartreden | Radio, netwerk, applicatie |
| Klok | De huidige tijd in UNIX-seconden | Waar die tijd voor gebruikt wordt |
| Toevalsbron | Willekeurige bytes leveren | Waar die bytes in terechtkomen |

De scheiding tussen radio en bord is scherper dan je zou verwachten. Het bord
weet wél dat er een moment vóór en na het zenden is — het krijgt een seintje
zodat het bijvoorbeeld een versterker kan inschakelen — maar het weet niet wat
er verzonden wordt.

## De ondersteunende componenten

### Pakketvoorraad

Pakketten worden niet aangevraagd bij het geheugenbeheer van het systeem maar
uit een vooraf gereserveerde voorraad gehaald. Dat is een bewuste keuze; zie
[Ontwerpbeslissingen](decisions.md). Dezelfde component beheert ook de
wachtrijen naar binnen en naar buiten, met prioriteit en een gepland
verzendmoment per pakket.

### Gezien-tabel

Houdt bij welke pakketten al langs zijn geweest. Zonder deze component zou elk
pakket in een netwerk met meerdere repeaters oneindig blijven rondgaan.

### Identiteit

Beheert het sleutelpaar van deze node en de publieke sleutels van anderen. De
component onderscheidt twee soorten: een identiteit waarvan alleen de publieke
sleutel bekend is, en de eigen identiteit met het volledige sleutelpaar. Alleen
de tweede kan ondertekenen.

### Rechtenlijst

De lijst van bekende clients van een repeater, room server of sensor, met per
client een rechtenniveau en de laatst bekende route ernaartoe. Vier niveaus:
gast, alleen lezen, lezen en schrijven, beheerder.

### Opslag

Het bewaren van identiteit, voorkeuren, contacten en rechtenlijst over een
herstart heen. Voor de rest van de firmware is dit één component; dat het
onderliggende bestandssysteem per platformfamilie verschilt, is een technische
kwestie.

### Bediening

De commandoregel die repeater, room server en sensor delen. Hij vertaalt tekst
naar acties en levert de antwoorden terug — of dat nu over een seriële
verbinding gaat of in een versleuteld pakket van een beheerder op afstand.

### Koppelvlak

De verbinding met een begeleidende applicatie. Vier varianten — BLE,
USB-serieel, WiFi en ESP-NOW — achter één afspraak, zodat de companion radio
niet weet welke het is.

### Scherm

Het uitschrijven van tekst en beelden naar een display. Elf verschillende
displaytypen delen hetzelfde contract, waaronder er één die niets doet: nodes
zonder scherm krijgen die.

### Brug

Het doorgeven van pakketten over een ander medium dan de radio — een seriële
verbinding of ESP-NOW — zodat twee mesh-segmenten aan elkaar geknoopt kunnen
worden.

### Sensorbeheer

Het uitlezen van aangesloten meetapparatuur en het verpakken van de waarden in
een gestandaardiseerd formaat.

## Wat er niet is

Twee dingen die je in een netwerkstack zou verwachten, ontbreken met opzet.

Er is geen routeringstabel in de klassieke zin. Een node bouwt geen kaart van
het netwerk op; paden komen mee met de pakketten zelf. Zie
[Route traceren](../../techniek/route-tracing.md).

Er is geen scheduler of takenmodel. Alles draait in één lus. Componenten
krijgen om beurten de kans iets te doen, en een component die te lang blijft
hangen houdt de rest op. Dat is een expliciete keuze en geen tekortkoming;
[Ontwerpbeslissingen](decisions.md) gaat erop in.

## Bronnen

- [MeshCore `03b6ef4` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore `03b6ef4` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Dispatcher.h)
- [MeshCore `03b6ef4` — `src/Mesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Mesh.h)
- [MeshCore `03b6ef4` — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
