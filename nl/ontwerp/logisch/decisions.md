# Ontwerpbeslissingen

*KEUZES · CONSEQUENTIES · WAT ZE ONMOGELIJK MAKEN*

Elk ontwerp is een reeks keuzes, en elke keuze sluit iets uit. Dit hoofdstuk
beschrijft de zeven beslissingen die het karakter van MeshCore bepalen — niet
als verantwoording, maar als uitleg van wat je wel en niet kunt verwachten van
een node die op deze manier is gebouwd.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — `src/Dispatcher.h`,
> `src/MeshCore.h`, `src/helpers/StaticPoolPacketManager.h` en de root
> `platformio.ini`.

## 1. Configuratie bij het compileren, niet bij het opstarten

De rol, de radio, het scherm en de bruggen liggen vast in de binary. Er is
geen configuratiebestand dat bepaalt of een node repeater of room server is.

**Waarom.** Een nRF52 met 256 KB RAM kan niet alle zes de rollen en elf
displaydrivers tegelijk in het geheugen houden. Door bij het compileren te
kiezen, komt alleen de gekozen code in de binary terecht.

**Wat het kost.** Je kunt een node niet van rol laten wisselen zonder nieuwe
firmware te flashen. En het aantal buildtargets groeit met het product van de
assen — 508 stuks, die allemaal moeten blijven compileren.

## 2. Eén lus, geen takenmodel

Alles draait in één `loop()`. Er is geen scheduler, geen threads, geen
prioriteiten tussen taken.

**Waarom.** Het scheelt geheugen, het maakt het gedrag voorspelbaar, en het
werkt hetzelfde op vier platformfamilies waarvan er twee geen bruikbaar
takenmodel hebben.

**Wat het kost.** Elke component moet snel teruggeven. Een displaydriver die
een e-ink scherm ververst, houdt de radio tegen. Het ontwerp lost dat niet op;
het maakt het zichtbaar, doordat het schermcontract de applicatie laat vragen
of het om e-ink gaat.

## 3. Pakketten uit een vaste voorraad

Pakketten worden niet dynamisch aangevraagd maar uit een vooraf gereserveerde
pool gehaald.

**Waarom.** Op een microcontroller die maanden achtereen moet draaien kan
geheugenfragmentatie geleidelijk tot instabiliteit leiden. Een vaste pool kan
niet fragmenteren en het geheugengebruik is bij het opstarten bekend.

**Wat het kost.** De pool kan op. Als er meer pakketten tegelijk onderweg
zijn dan er plekken zijn, valt er een af. Dat is een ontwerpkeuze — liever een
voorspelbaar verlies dan een onvoorspelbare herstart.

## 4. Routering zit in het pakket, niet in de node

Een node houdt geen kaart van het netwerk bij. Paden reizen mee met de
pakketten.

**Waarom.** Een routeringstabel moet worden onderhouden, en dat kost verkeer.
In een netwerk waar zendtijd wettelijk begrensd is en de bandbreedte in
honderden bytes per seconde wordt gemeten, is elk onderhoudsbericht een bericht
dat niet doorkomt.

**Wat het kost.** Een node weet niet of een pad nog werkt tot hij het probeert.
Er is geen manier om te ontdekken dat een repeater is uitgevallen behalve door
te merken dat er niets terugkomt.

## 5. Alles achter een contract, ook wat maar één implementatie heeft

De gezien-tabel en de pakketpool hebben elk precies één implementatie, en toch
zit er een contract tussen.

**Waarom.** Het contract is geen voorbereiding op toekomstige implementaties
maar een grens. Het legt vast wat de mesh-logica van die component mag
verwachten, en dwingt af dat er niets doorheen lekt.

**Wat het kost.** Een laag indirectie die op deze schaal niets oplevert aan
flexibiliteit. Dat is de prijs die het ontwerp bewust betaalt.

## 6. Vier platformfamilies, drie gedeelde bordklassen

ESP32, nRF52 en STM32 hebben elk een gedeelde bordimplementatie in de kern.
RP2040 niet: elk van de vier RP2040-borden schrijft zijn eigen.

**Waarom.** Dit is geen ontwerpkeuze maar een gegroeide situatie. RP2040 kwam
later en met weinig varianten; er was nooit genoeg overlap om een gedeelde
basis te rechtvaardigen.

**Wat het kost.** Vier keer dezelfde code voor batterijmeting en herstart, op
vier plekken die apart onderhouden moeten worden. Wie een vijfde RP2040-bord
toevoegt, kopieert opnieuw.

Het is de duidelijkste plek waar het ontwerp niet consistent is doorgevoerd, en
het staat hier omdat het weglaten ervan het document mooier maar onjuist zou
maken.

## 7. Geen foutmodel

Contracten geven geen fouten terug. Een radio die niet reageert meldt dat niet;
hij levert eenvoudigweg geen pakketten. Een schrijfactie naar de opslag die
mislukt, mislukt stil.

**Waarom.** Foutafhandeling kost code en geheugen, en op een node zonder
gebruiker is er meestal niemand om de fout aan te melden.

**Wat het kost.** Diagnose op afstand is moeilijk. Een repeater die zijn radio
kwijt is, gedraagt zich als een repeater in een stil gebied. De statistieken
die een node bijhoudt — verzonden, ontvangen, zendtijdbudget — zijn daarom het
enige gereedschap dat er is.

## Wat deze keuzes samen opleveren

Zes van de zeven wijzen dezelfde kant op: voorspelbaar geheugengebruik en
weinig verkeer, ten koste van flexibiliteit tijdens het draaien. Dat is een
coherent ontwerp voor wat MeshCore wil zijn — een node die je ophangt en
vergeet.

De zevende, de asymmetrie bij RP2040, past daar niet in. Die is er gewoon.

## Bronnen

- [MeshCore `03b6ef4` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Dispatcher.h)
- [MeshCore `03b6ef4` — `src/helpers/StaticPoolPacketManager.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/StaticPoolPacketManager.h)
- [MeshCore `03b6ef4` — `src/helpers/ui/DisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/DisplayDriver.h)
- [MeshCore `03b6ef4` — `variants/rak11310/RAK11310Board.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/rak11310/RAK11310Board.h)
