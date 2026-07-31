# De companion-interface

*APP · NODE · FRAMES · OPCODES · BRONHIËRARCHIE*

Een companion-node is een MeshCore-radio die via een app wordt bediend; hij
heeft zelf geen volledig bedieningspaneel. Alles wat een mens ermee doet —
een bericht typen, een contact toevoegen, het zendvermogen wijzigen — stuurt
de app als één afgebakend gegevensblok naar de node. Zo'n gegevensblok heet
in deze documentatie een **frame**. Deze sectie beschrijft dat koppelvlak:
welke afspraken er gelden tussen app en node, en hoe je er zelf een client
op bouwt.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `examples/companion_radio/MyMesh.cpp`,
> `examples/companion_radio/MyMesh.h` en de officiële
> `docs/companion_protocol.md`. Daarnaast tegen `meshcore_py` v2.3.8
> (commit `c487efb`) en `meshcore.js` v1.13.0 (commit `bbe1f93`).

![De app praat met de companion-node over BLE, USB of TCP; de node praat met
de mesh over LoRa. De app bereikt de mesh nooit rechtstreeks](../../images/nl/companion-context-1.svg)

> [!WARNING]
> **Deze sectie beschrijft de regels waaraan een client zich moet houden,
> maar is geen officiële specificatie.** Ze beschrijft hoe je een eigen
> companion-client bouwt, afgeleid uit de
> firmwarebron op commit `03b6ef4` en gecontroleerd tegen `meshcore_py`
> v2.3.8. Er is geen versiegarantie: `FIRMWARE_VER_CODE` verandert tussen
> releases, en de officiële `docs/companion_protocol.md` beschrijft op dit
> moment 7 van de 58 commando's. Controleer altijd tegen de bron die bij
> jouw firmware hoort.

## De begrippen op één plek

De rest van deze sectie gebruikt een handvol vaktermen. Ze staan hier bij
elkaar, zodat je ze tijdens het lezen niet hoeft op te zoeken.

| Term | Wat het betekent |
|---|---|
| companion-node | een MeshCore-radio die via een app wordt bediend |
| client | de app of software die met de node communiceert |
| transport | de verbinding waarover dat gaat: BLE, USB-serieel of TCP |
| frame | één afgebakend gegevensblok tussen app en node, hier hoogstens 176 bytes |
| opcode | de eerste byte van een frame: het nummer dat aangeeft welk commando, antwoord of ongevraagde melding erin staat |
| payload | de gegevensinhoud van het frame, alles achter de opcode |
| ongevraagde melding | een frame dat de node uit zichzelf stuurt en dat dus geen antwoord is op een vraag; het nummer ervan heet een pushcode |
| aankondiging (*advert*) | een bericht waarmee een node zichzelf in het netwerk bekendmaakt |
| verspreidingsgebied (*scope*) | het gebied waarbinnen een bericht mag rondgaan |
| firmwarevariant | een specifiek gecompileerde versie van de firmware; grenzen zoals het aantal contacten verschillen per variant |

In lopende tekst staat de Nederlandse term. De Engelse broncodeterm staat er
bij het eerste gebruik tussen haakjes bij, zodat je die in de firmware en in
de officiële softwarebibliotheken kunt terugvinden. Namen van commando's en
constanten blijven onvertaald: `CMD_SEND_SELF_ADVERT` heet ook hier
`CMD_SEND_SELF_ADVERT`. Uitgebreidere definities staan in
[Terminologie](../naslag/terminology.md).

## Waarom deze sectie bestaat

De officiële MeshCore Companion App is gesloten. Er is geen publieke
repository van de Android-, iOS- of webversie, dus er valt geen ontwerp uit
af te lezen. Wat wél openbaar is, is het contract waaraan die app zich
houdt: de firmware die de frames ontvangt, en twee officiële
softwarebibliotheken die de andere kant implementeren.

Deze sectie beschrijft dus niet het ontwerp van de officiële app, maar de
protocolafspraken waaraan iedere compatibele app moet voldoen.

## De vier bronnen en hoe volledig ze zijn

Niet elke bron is even compleet. De verhouding is met
`tools/companion-opcodes.py` gemeten en reproduceerbaar:

| Bron | Commando's | Antwoord- en pushcodes |
|---|---|---|
| firmware `MyMesh.cpp` | 58/58 | 46/46 |
| `meshcore_py` v2.3.8 | 56/58 | 46/46 |
| `meshcore.js` v1.13.0 | 39/58 | niet vergeleken |
| `docs/companion_protocol.md` | 7/58 | 5/46 |

De firmware geeft de doorslag: die bepaalt wat er gebeurt. Na de firmware is
`meshcore_py` de meest volledige bron — die softwarebibliotheek kent alle 46
antwoord- en pushcodes en mist maar twee commando's,
`CMD_SEND_CHANNEL_DATA` (62) en `CMD_SEND_RAW_PACKET` (65). `meshcore.js`
loopt verder achter.

De officiële specificatie is de minst volledige bron, en zegt dat zelf ook:
bovenaan het bestand staat dat het document nog in ontwikkeling is en
onnauwkeurigheden kan bevatten. De kop noemt "Companion Firmware v1.12.0+"
en de laatste wijziging is van 8 maart 2026, terwijl de firmware waartegen
deze sectie geschreven is v1.16.0 is. Waar deze sectie afwijkt van de
specificatie, staat dat erbij.

## Wat hier niet staat

Deze sectie herhaalt geen inhoud uit andere secties. Waar het onderwerp
raakt, staat een verwijzing.

| Onderwerp | Staat in |
|---|---|
| Byte-indeling van de frameheader op serieel | [USB-serieel](../hardware/interfaces/usb-serial.md) |
| BLE-stack, GATT, NUS en pairing | [BLE Architectuur](../hardware/interfaces/ble-architecture.md) |
| WiFi-opzet en inloggegevens in het firmwarebestand | [WiFi als companion-verbinding](../hardware/interfaces/wifi.md) |
| Wat er over de lucht gaat | [Het Lagenmodel](../techniek/layer-model.md) |
| Structuur van de firmware zelf | [Ontwerp van MeshCore](../ontwerp/introduction.md) |
| Welke boards een companion kunnen zijn | [Nodematrix](../platform/node-matrix.md) |

Kort gezegd: `hardware/interfaces/` beschrijft de draad en de bytes erop,
`companion/` beschrijft wat die bytes betekenen.

## Leeswijzer

Het logisch deel beschrijft *wat* het koppelvlak is, zonder naar C++ te
wijzen. Het technisch deel beschrijft *hoe* je het gebruikt, met
bestandsnamen en regelnummers.

- **Logisch ontwerp**
  - [Verantwoordelijkheden](logisch/responsibilities.md) — wie bewaart wat
  - [Het interactiemodel](logisch/interaction-model.md) — vraag, antwoord,
    push en versieonderhandeling
  - [Informatiemodel](logisch/information-model.md) — de gegevens die heen
    en weer gaan
- **Technisch ontwerp**
  - [De drie transporten](technisch/transports.md) — wat het protocol van
    een verbinding eist
  - [Het frame](technisch/frame-format.md) — wat er in de 176 bytes past
  - [De commandogroepen](technisch/command-groups.md) — alle 58 commando's,
    geordend
  - [Architectuur van een client](technisch/client-architecture.md) — de
    lagen waaruit een werkende client bestaat

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.cpp)
  — de opcodetabel en alle commandoafhandeling
- [`examples/companion_radio/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.h)
  — `FIRMWARE_VER_CODE`, `MAX_CONTACTS`, `OFFLINE_QUEUE_SIZE`
- [`docs/companion_protocol.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/docs/companion_protocol.md)
  — de officiële specificatie, met eigen voorbehoud

Officiële softwarebibliotheken:

- [`meshcore-dev/meshcore_py`](https://github.com/meshcore-dev/meshcore_py)
  — Python, v2.3.8
- [`meshcore-dev/meshcore.js`](https://github.com/meshcore-dev/meshcore.js)
  — JavaScript, v1.13.0

Reproductie:

- `tools/companion-opcodes.py` — telt de opcodes en de dekking per bron
- `tools/companion-opcodes-snapshot.json` — de uitkomst op commit `03b6ef4`

Verwante hoofdstukken:

- [USB-serieel](../hardware/interfaces/usb-serial.md) — het frame byte voor
  byte
- [GitHub Repositories](../project/github.md) — de officiële repositories
- [Terminologie](../naslag/terminology.md) — de begrippen uit deze sectie
