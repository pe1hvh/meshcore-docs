# Rollen

*ZES APPLICATIES · ÉÉN PER BUILD · WAT EEN ROL WEL EN NIET DOET*

MeshCore is geen enkele applicatie maar zes. Welke van de zes een node is,
wordt bij het compileren vastgelegd en kan daarna niet meer veranderen. Een
repeater kan niet in een room server veranderen door een instelling om te
zetten; het is andere firmware. Dit hoofdstuk beschrijft de zes rollen als
logische actoren: wat elk van hen doet, wat het uitdrukkelijk niet doet, en
hoe ze zich tot elkaar verhouden.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — de zes directory's onder
> `examples/` en de 508 `[env:...]`-secties in `platformio.ini` plus de 79
> variantbestanden. Aantallen uit `tools/design-overview.py`.

## Eén rol per build

Van de 508 buildtargets compileren er 507 precies één applicatie. Het 508e is
`env:native`, het testtarget dat op de ontwikkelmachine draait en helemaal
geen applicatie bouwt. Er is geen enkel target dat er twee combineert.

Dat is een harde eigenschap van het ontwerp en niet een toevalligheid van de
huidige configuratie: de applicaties hebben elk hun eigen `main.cpp` en hun
eigen `setup()` en `loop()`. Twee van die bestanden in één binary levert een
dubbele symbooldefinitie op.

| Rol | Directory | Targets | Variantdirectory's |
|---|---|---|---|
| Companion radio | `examples/companion_radio` | 174 | 76 |
| Repeater | `examples/simple_repeater` | 136 | 75 |
| KISS-modem | `examples/kiss_modem` | 80 | 74 |
| Room server | `examples/simple_room_server` | 73 | 65 |
| Terminal chat | `examples/simple_secure_chat` | 26 | 24 |
| Sensor | `examples/simple_sensor` | 18 | 16 |

De tweede kolom telt buildtargets, de derde het aantal hardwarevarianten
waarvoor die rol beschikbaar is. Het verschil zit in bridge- en
displayvarianten van dezelfde rol op dezelfde hardware.

![Zes rollen naast elkaar, elk met de laag waar hij op rust: alle zes gebruiken
dezelfde mesh-kern, maar drie ervan zijn autonome netwerkdiensten en drie
dienen een gebruiker of een aangesloten machine.](../../../images/nl/roles-1.svg)

## De zes rollen

### Companion radio

De grootste rol, en de enige die niet zelfstandig bruikbaar is. Een companion
radio is een radiomodem met een sleutelbos: hij houdt de identiteit, de
contactenlijst en de kanalen bij, maar hij heeft geen eigen
gebruikersinterface voor het lezen en schrijven van berichten. Dat doet een
telefoon- of desktopapplicatie die via BLE, USB-serieel, WiFi of ESP-NOW is
aangesloten.

Wat de rol wél doet: identiteit beheren, contacten bijhouden, paden onthouden,
berichten in de wachtrij zetten wanneer de begeleidende app niet verbonden is.
Wat hij niet doet: pakketten van anderen doorgeven. Een companion radio is
geen repeater, tenzij hij expliciet in client-repeatmodus wordt gezet.

### Repeater

Een autonome netwerkdienst zonder gebruiker. Een repeater ontvangt pakketten,
beslist of hij ze doorgeeft, en zendt ze opnieuw uit. Hij houdt bij wat hij al
gezien heeft zodat hetzelfde pakket niet twee keer de lucht in gaat, en hij
bewaakt zijn eigen zendtijdbudget.

Daarnaast is een repeater beheerbaar op afstand: hij houdt een lijst van
bekende clients bij met per client een rechtenniveau, en accepteert commando's
van wie daar admin-rechten heeft. Wat hij niet doet: berichten opslaan voor
later. Wie niet luistert op het moment dat de repeater uitzendt, mist het.

### Room server

Een repeater die wél opslaat. De room server houdt berichten vast en levert ze
na aan clients die zich later melden — het model van een prikbord. Daarvoor
heeft hij per client een synchronisatiepunt nodig: sinds welk moment moet er
worden nagestuurd.

Een room server is niet een repeater plus opslag; het is een aparte applicatie
met een eigen rechtenmodel. Zie [Room Server](../../techniek/roomserver/introduction.md)
voor het gedrag.

### Sensor

Een node die meetwaarden verzamelt en op verzoek of periodiek uitstuurt. De
rol houdt een tijdreeks in het geheugen en verpakt metingen in een
gestandaardiseerd formaat. Hij deelt het rechtenmodel met de repeater en de
room server.

### Terminal chat

De eenvoudigste rol, en de enige die een mens rechtstreeks bedient zonder
tussenliggende app: een chatclient over de seriële verbinding. Bedoeld om te
demonstreren en te testen, niet om dagelijks te gebruiken. Het is de enige rol
die uit één bestand bestaat.

### KISS-modem

Geen MeshCore-applicatie in de gebruikelijke zin. Een KISS-modem geeft rauwe
frames door tussen de radio en een aangesloten computer, volgens een protocol
dat uit de packetradio komt. De node neemt geen enkele beslissing over
routering of versleuteling; dat laat hij aan de software aan de andere kant.

Dat maakt het KISS-modem de enige rol die de mesh-logica grotendeels omzeilt,
en meteen de reden dat hij op bijna alle hardware beschikbaar is: er is weinig
nodig om hem te draaien.

## Welke rollen samen voorkomen

Een werkend netwerk heeft minstens twee rollen nodig. Companion radio's praten
met elkaar, maar zonder repeaters komen ze niet verder dan elkaars directe
bereik. Repeaters onderling vormen de netwerkinfrastructuur waarover andere
nodes hun berichten doorgeven; room servers hangen daaraan als dienst.

| Combinatie | Zinvol |
|---|---|
| Companion radio + repeater | De standaardopstelling |
| Repeater + repeater | Bereik uitbreiden |
| Companion radio + room server | Prikbord zonder tussenliggende repeater, alleen binnen bereik |
| Sensor + repeater | Meetpunt dat via het net wordt uitgelezen |
| KISS-modem alleen | Experiment of gateway naar andere software |

## Bronnen

- [MeshCore `03b6ef4` — `examples/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/examples)
- [MeshCore `03b6ef4` — `examples/companion_radio/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/MyMesh.h)
- [MeshCore `03b6ef4` — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore `03b6ef4` — `examples/kiss_modem/KissModem.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/kiss_modem/KissModem.h)
