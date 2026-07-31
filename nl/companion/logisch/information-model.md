# Informatiemodel

*CONTACT · KANAAL · BERICHT · AANKONDIGING · PAD · WAT WAAR BLIJFT*

Het koppelvlak kent een handvol gegevenssoorten. Sommige bestaan aan beide
kanten en moeten synchroon blijven, andere bestaan maar op één plek en zijn
daarom nooit een synchronisatieprobleem. Dit hoofdstuk zet die driedeling
uiteen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `examples/companion_radio/MyMesh.cpp`, `src/helpers/ContactInfo.h`,
> `src/helpers/ChannelDetails.h` en `examples/companion_radio/NodePrefs.h`.

![Drie kolommen: gegevens die alleen op de node worden bewaard, gegevens die
aan beide kanten bestaan en gesynchroniseerd moeten worden, en gegevens die
alleen in de app bestaan](../../../images/nl/companion-information-model-1.svg)

## Contact

Een contact is de opgeslagen beschrijving van een andere node: publieke
sleutel, naam, type en het laatst bekende pad ernaartoe. Hoeveel er passen
verschilt per firmwarevariant — zie
[Verantwoordelijkheden](responsibilities.md).

Wat een app moet weten:

- **De sleutel is de identiteit, niet de naam.** Namen zijn niet uniek en
  veranderen. `CMD_GET_CONTACT_BY_KEY` (30) zoekt op het eerste deel van de
  publieke sleutel (de sleutelprefix).
- **De app kan alleen gewijzigde contacten ophalen.** `CMD_GET_CONTACTS` (4)
  neemt optioneel een tijdstempel mee, zodat alleen contacten terugkomen die
  daarna zijn veranderd. Dat heet incrementeel synchroniseren. Bij honderd
  contacten over BLE scheelt het merkbaar.
- **Vol is vol.** Loopt de tabel vol, dan meldt de node dat met
  `PUSH_CODE_CONTACTS_FULL` (`0x90`). Is automatisch overschrijven
  ingeschakeld, dan verdwijnt het oudste niet-favoriete contact en komt er
  `PUSH_CODE_CONTACT_DELETED` (`0x8F`). Een app die die twee negeert, toont
  contacten die niet meer bestaan.

Welke soorten contacten automatisch worden toegevoegd, is instelbaar met een
bitmasker: één getal waarvan de afzonderlijke bits elk een eigen optie aan-
of uitzetten. De eerste bit staat hieronder voor het overschrijven van het
oudste contact, de tweede voor chatnodes, enzovoort:

`examples/companion_radio/MyMesh.cpp` r.142-146

```cpp
#define AUTO_ADD_OVERWRITE_OLDEST (1 << 0)  // 0x01 - overwrite oldest non-favourite when full
#define AUTO_ADD_CHAT             (1 << 1)  // 0x02 - auto-add Chat (Companion) (ADV_TYPE_CHAT)
#define AUTO_ADD_REPEATER         (1 << 2)  // 0x04 - auto-add Repeater (ADV_TYPE_REPEATER)
#define AUTO_ADD_ROOM_SERVER      (1 << 3)  // 0x08 - auto-add Room Server (ADV_TYPE_ROOM)
#define AUTO_ADD_SENSOR           (1 << 4)  // 0x10 - auto-add Sensor (ADV_TYPE_SENSOR)
```

## Kanaal

De node heeft een vast aantal kanaalplaatsen, in de firmware *slots*
genoemd. Elke plaats bevat een kanaalnaam en een gedeelde sleutel. Het
aantal plaatsen ligt vast bij het compileren — 8 of 40 in de
companion-varianten — en de app leest het uit het antwoord op
`CMD_DEVICE_QUERY`.

Kanalen worden per index gelezen en geschreven, niet per naam:
`CMD_GET_CHANNEL` (31) met een index, `CMD_SET_CHANNEL` (32) met index,
naam en sleutel. Een lege plaats is een geldig antwoord.

De publieke groep heeft een vaste sleutel die in de firmware staat:

`examples/companion_radio/MyMesh.cpp` r.109

```cpp
#define PUBLIC_GROUP_PSK                "izOH6cXN6mrJ5e26oRXNcg=="
```

Die is dus geen geheim en biedt geen vertrouwelijkheid — hij zorgt alleen
dat iedereen op dezelfde manier ontsleutelt. Zie
[Channel Structure & PSK](../../techniek/channel-structure.md).

Wat de node **niet** bewaart, is bij welk kanaal welk verspreidingsgebied
hoort. Een verspreidingsgebied (*scope*) is het gebied waarbinnen een bericht
mag rondgaan; MeshCore noemt zo'n gebied een regio. Die koppeling zit alleen
in de app, en de app stelt het gebied dus in vóór elke verzending. De
firmware kiest bij verzenden de tijdelijke instelling als die er is, en
anders de vaste standaard van de node; zie
[Regio's en Scopes](../../techniek/regions-and-scopes.md).

## Bericht

Een bericht bestaat aan beide kanten, maar niet even lang. Op de node staat
het in de wachtrij tot de app het ophaalt; daarna is het weg. De app kan het
blijvend in de berichtgeschiedenis bewaren.

Er zijn drie vormen, en ze hebben elk een eigen commando:

| Vorm | Verzenden | Ontvangen |
|---|---|---|
| Direct bericht | `CMD_SEND_TXT_MSG` (2) | `RESP_CODE_CONTACT_MSG_RECV` (7) of `_V3` (16) |
| Kanaalbericht | `CMD_SEND_CHANNEL_TXT_MSG` (3) | `RESP_CODE_CHANNEL_MSG_RECV` (8) of `_V3` (17) |
| Datagram op een kanaal | `CMD_SEND_CHANNEL_DATA` (62) | `RESP_CODE_CHANNEL_DATA_RECV` (27) |

Dat derde spoor is voor apps die geen tekst uitwisselen maar gestructureerde
gegevens over een kanaal sturen. Zo'n los pakket met binaire of anderszins
gestructureerde gegevens heet een datagram. De ruimte is krap:

`examples/companion_radio/MyMesh.cpp` r.101

```cpp
#define MAX_CHANNEL_DATA_LENGTH       (MAX_FRAME_SIZE - 9)
```

Met `MAX_FRAME_SIZE` op 176 blijft er 167 byte over voor de gegevens zelf.
Zie [Het frame](../technisch/frame-format.md).

## Aankondigingen en routes

Een aankondiging (*advert*) is het bericht waarmee een node zichzelf in het
netwerk bekendmaakt. De app ziet er twee soorten melding van:
`PUSH_CODE_ADVERT` (`0x80`) voor een bekende node en `PUSH_CODE_NEW_ADVERT`
(`0x8A`) voor een onbekende. Alleen bij de tweede staat de app voor de keuze
om een contact toe te voegen.

Een pad is de route die naar een contact bleek te werken. De node houdt het
bij en meldt wijzigingen met `PUSH_CODE_PATH_UPDATED` (`0x81`). De app kan
het opvragen met `CMD_GET_ADVERT_PATH` (42) en wissen met
`CMD_RESET_PATH` (13). Zie [Route traceren](../../techniek/route-tracing.md).

## De driedeling

| Alleen op de node | Aan beide kanten | Alleen in de app |
|---|---|---|
| privésleutel | contact | berichthistorie |
| radioparameters | kanaal | kanaal → verspreidingsgebied |
| pincode | aankondiging | eigen namen en groepering |
| de berichtenwachtrij | pad naar een contact | leesstatus |
| opslagtellers | klok | kaartgegevens |

De linkerkolom verlaat de node nooit, op één uitzondering na:
`CMD_EXPORT_PRIVATE_KEY` (23) haalt de privésleutel eruit, en
`CMD_IMPORT_PRIVATE_KEY` (24) zet er een terug. Dat is bedoeld voor
migratie naar een nieuw apparaat en is de gevoeligste bewerking in het hele
protocol.

De rechterkolom komt de node nooit binnen. Alleen de middelste kolom is een
synchronisatievraagstuk.

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.cpp)
  — `PUBLIC_GROUP_PSK`, `MAX_CHANNEL_DATA_LENGTH`, het auto-add-bitmasker
- [`src/helpers/ContactInfo.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ContactInfo.h)
  — de velden van een contact
- [`src/helpers/ChannelDetails.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ChannelDetails.h)
  — de velden van een kanaalslot

Verwante hoofdstukken:

- [Verantwoordelijkheden](responsibilities.md) — waarom de driedeling zo
  loopt
- [Channel Structure & PSK](../../techniek/channel-structure.md) — wat een
  kanaalsleutel doet
- [Regio's en Scopes](../../techniek/regions-and-scopes.md) — de koppeling
  die de app bijhoudt
