# Architectuur van een client

*ZES LAGEN · HERVERBINDEN · ABONNEMENTEN · BESTAANDE CLIENTS*

Een werkende companion-client is geen dunne laag om een netwerkverbinding
(*socket*). Er zitten zes duidelijk gescheiden verantwoordelijkheden in, en
`meshcore_py` laat zien welke. Dit hoofdstuk beschrijft die indeling en zet
erbij welke clients er al zijn.

> [!NOTE]
> **Bron.** De laagindeling is afgeleid uit `meshcore_py` v2.3.8, commit
> `c487efb` — modules `ble_cx.py`, `serial_cx.py`, `tcp_cx.py`,
> `connection_manager.py`, `reader.py`, `events.py`, `commands/` en
> `meshcore.py`. De protocolfeiten waarnaar verwezen wordt komen uit
> `MeshCore` v1.16.0, commit `03b6ef4`.

![Zes lagen boven elkaar, van transport tot publieke API met cache, met per
laag de module uit meshcore_py die die rol vervult](../../../images/nl/companion-architecture-1.svg)

> [!WARNING]
> Dit hoofdstuk is normatief: het beschrijft een indeling die werkt, niet een
> voorgeschreven standaard. Er bestaat geen officiële referentiearchitectuur
> voor MeshCore-clients. Wijkt jouw client af en werkt hij, dan is dat geen
> fout.

De zes lagen, in één zin per laag:

| Laag | Wat die laag doet |
|---|---|
| Transport | legt de verbinding en verplaatst bytes; kent geen frames |
| Verbindingsbeheer | bewaakt de verbinding en meldt de app opnieuw aan na herverbinden |
| Framelezer | knipt de bytestroom in frames en zet elk frame om in een object met benoemde velden |
| Gebeurtenissen | verdeelt die objecten over alle onderdelen van de app die erop wachten |
| Commandolaag | verstuurt commando's en koppelt binnengekomen antwoorden aan het juiste verzoek |
| Publieke API met cache | de laag die de app zelf aanroept; houdt de actuele toestand bij |

## Laag 1 — Transport

Verbinden, bytes heen en weer, meer niet. Drie implementaties achter één
afspraak, precies zoals `BaseSerialInterface` dat aan de firmwarekant doet.
`meshcore_py` legt die afspraak vast als een `Protocol` met vier methoden en
documenteert het retourcontract expliciet:

`src/meshcore/connection_manager.py` r.13-23

```python
class ConnectionProtocol(Protocol):
    """Protocol defining the interface that connection classes must implement.

    Return contract for connect():
        - On success: return a truthy value (typically an address string)
          that identifies the connection. This value is included in the
          CONNECTED event payload as ``connection_info``.
        - On failure: return ``None`` (soft failure — triggers a retry in
          ``_attempt_reconnect``) **or** raise an exception (hard failure —
          also triggers a retry, logged as an error).
    """
```

Wat `connect()` teruggeeft, komt terecht in de gegevens van de
verbindingsgebeurtenis (`connection_info` in de `CONNECTED`-gebeurtenis). Het
onderscheid tussen zachte en harde fout is niet cosmetisch: een BLE-radio die
even niets vindt is iets anders dan een seriële poort die niet bestaat, maar
allebei moeten leiden tot een nieuwe poging.

## Laag 2 — Verbindingsbeheer

Herverbinden, tellen hoe vaak, en — dit is het punt dat clients het vaakst
missen — na elke geslaagde herverbinding opnieuw aanmelden. `ConnectionManager`
neemt daarvoor een `reconnect_callback` aan.

Dat is de laag waar het gedrag uit
[Het interactiemodel](../logisch/interaction-model.md) thuishoort:
`app_target_ver` op de node is na een verbreking weer nul, dus `CMD_APP_START`
en `CMD_DEVICE_QUERY` moeten opnieuw. Hangt die aanmelding aan het opstarten
van het programma in plaats van aan de verbinding, dan werkt de client de
eerste keer en levert hij daarna stilzwijgend verkeerd geparsede frames.

## Laag 3 — Framelezer

Bytes in, getypeerde gebeurtenis uit. Eén ingang die de eerste byte leest,
beslist of het een antwoord of een ongevraagde melding is, de gegevensvelden
uit de payload leest en er een object van maakt. In `meshcore_py` is dat
`reader.py` — met ruim duizend regels de grootste module van die
softwarebibliotheek, wat een bruikbare indicatie is van hoeveel werk deze
laag is.

Hier hoort ook de lengtecontrole: een veld dat pas vanaf een bepaalde
`FIRMWARE_VER_CODE` bestaat, mag alleen gelezen worden als het frame lang
genoeg is. Zie [Het frame](frame-format.md).

## Laag 4 — Gebeurtenissen

Abonnementen in plaats van losse terugroepfuncties (*callbacks*). De reden is
de aard van het protocol: ongevraagde meldingen komen binnen zonder dat er
iets om gevraagd heeft, en kunnen meerdere belanghebbenden hebben. Een
kaartweergave, een meldingenteller en een gesprekvenster willen alledrie iets
weten van hetzelfde binnengekomen bericht.

`meshcore_py` definieert daarvoor ruim vijftig gebeurtenistypen, waaronder
twee die niet uit het protocol komen maar uit laag 2: `CONNECTED` en
`DISCONNECTED`.

## Laag 5 — Commandolaag

Verzenden, wachten, en het antwoord aan het verzoek koppelen. Twee dingen
liggen hier vast:

- **Eén verzoek tegelijk.** `meshcore_py` zet een vergrendeling (*lock*) rond
  verzoeken die de mesh in gaan. Dat is geen voorzichtigheid maar noodzaak: de
  verzendwachtrij van de node is vier of twaalf frames groot en overloop is
  stil. Zie [De drie transporten](transports.md).
- **Een tijdslimiet per verzoek.** `CommandHandlerBase.DEFAULT_TIMEOUT` staat
  op 15 seconden. Verzoeken die de mesh in gaan mogen langer duren en krijgen
  hun grens uit het antwoord van de node zelf.

## Laag 6 — Publieke API met cache

De laag die een app daadwerkelijk gebruikt: in `meshcore_py` de gevel
(*facade*) waarachter de vijf lagen eronder schuilgaan. Houdt contacten,
`self_info` en de klok bij, en biedt de synchronisatielus als iets dat je
aanzet in plaats van iets dat je zelf schrijft. Die cache is meer dan een
snelheidsmaatregel: het is de actuele toestand waarop de app werkt, en hij
moet dus worden bijgewerkt zodra er een melding binnenkomt die hem raakt.
`meshcore_py` abonneert zich op `MESSAGES_WAITING` en start dan een lus die
`CMD_SYNC_NEXT_MESSAGE` herhaalt tot er geen berichten meer zijn — precies
het patroon uit
[Verantwoordelijkheden](../logisch/responsibilities.md).

## Waarom deze volgorde

| Laag | Verandert wanneer | Mag niets weten van |
|---|---|---|
| Transport | een nieuw verbindingstype erbij komt | opcodes |
| Verbindingsbeheer | het herverbindingsbeleid wijzigt | payloadindeling |
| Framelezer | de firmware een veld toevoegt | de gebruikersinterface |
| Gebeurtenissen | zelden | bytes |
| Commandolaag | er een commando bij komt | het transport |
| Publieke API | de app iets anders wil | framegrenzen |

De middelste kolom voorspelt waar het werk zit bij een firmware-update: bijna
altijd in laag 3 en 5, zelden daarbuiten.

## Welke clients er zijn

De officiële MeshCore Companion App is gesloten. Er is geen publieke
repository van de Android-, iOS- of webversie; de app is in Flutter gebouwd en
gratis te gebruiken.

| Client | Platform | Bron | Status |
|---|---|---|---|
| MeshCore Companion App | Android, iOS, web | gesloten | de officiële app |
| `meshcore_py` | Python | MIT | officieel, v2.3.8 |
| `meshcore.js` | JavaScript | MIT | officieel, v1.13.0 |
| `meshcore-cli` | Python | MIT | officieel, bovenop `meshcore_py` |
| `liamcottle/meshcore-web` | web | open | niet meer bijgewerkt, expliciet als referentie bedoeld |
| MeshCore Open | Flutter, meerdere platformen | MIT | door de gemeenschap |
| MeshCore One | iOS | open | door de gemeenschap |

De twee onderste zijn geen officiële projecten en staan hier omdat ze
werkende, leesbare implementaties zijn — niet als aanbeveling.

> [!NOTE]
> De firmware verwijst op twee plaatsen naar verschillende repositories voor
> dezelfde softwarebibliotheken. `README.md` r.70-71 noemt
> `liamcottle/meshcore.js` en `fdlamotte/meshcore-cli`;
> `docs/companion_protocol.md` r.16-17 noemt
> `meshcore-dev/meshcore.js` en `meshcore-dev/meshcore_py`. De projecten zijn
> naar de organisatie verhuisd en de README is niet meegegaan. Ga uit van de
> `meshcore-dev`-varianten.

## Bronnen

`meshcore_py` v2.3.8, commit `c487efb`:

- [`src/meshcore/connection_manager.py`](https://github.com/meshcore-dev/meshcore_py/blob/main/src/meshcore/connection_manager.py)
  — het verbindingscontract en het herverbinden
- [`src/meshcore/reader.py`](https://github.com/meshcore-dev/meshcore_py/blob/main/src/meshcore/reader.py)
  — frames naar gebeurtenissen
- [`src/meshcore/commands/base.py`](https://github.com/meshcore-dev/meshcore_py/blob/main/src/meshcore/commands/base.py)
  — tijdslimieten en het koppelen van antwoord aan verzoek
- [`src/meshcore/meshcore.py`](https://github.com/meshcore-dev/meshcore_py/blob/main/src/meshcore/meshcore.py)
  — de publieke API en de synchronisatielus

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`README.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/README.md)
  — de clientlijst met de afwijkende verwijzingen

Verwante hoofdstukken:

- [Het interactiemodel](../logisch/interaction-model.md) — waarom
  herverbinden opnieuw aanmelden is
- [De drie transporten](transports.md) — waarom één verzoek tegelijk
- [GitHub Repositories](../../project/github.md) — de repositories zelf
