# Het frame

*OPCODE · PAYLOAD · 176 BYTES · GEEN FRAGMENTATIE · WAT NIET PAST*

Elk frame begint met één byte die aangeeft wat voor frame het is. De overige
bytes vormen de gegevensinhoud (*payload*). Binnen het frame staat geen extra
kop met een eigen lengteveld, en het protocol kan één bericht niet over
meerdere frames verdelen. Dat maakt het protocol eenvoudig te implementeren
en legt tegelijk een harde grens op aan wat er in één keer overheen kan.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/BaseSerialInterface.h` en
> `examples/companion_radio/MyMesh.cpp`. De byte-indeling van de
> transportheader staat in
> [USB-serieel](../../hardware/interfaces/usb-serial.md) en wordt hier niet
> herhaald.

## Opcode en payload

De opbouw is overal gelijk:

```text
[opcode: 1 byte][payload: 0 tot 175 bytes]
```

De eerste byte bepaalt hoe de rest gelezen wordt. Commando's lopen van 1
tot 65, antwoorden van 0 tot 28 en pushcodes van `0x80` tot `0x90`. Omdat
commando's alleen naar de node gaan en antwoorden en pushcodes alleen
terugkomen, botsen die bereiken nergens in de praktijk.

Binnen de payload gelden drie afspraken:

- **Bij getallen van meerdere bytes wordt de minst belangrijke byte eerst
  verstuurd** (*little-endian*). De uitzondering is CayenneLPP in
  telemetriegegevens, waar juist de belangrijkste byte vooropgaat
  (*big-endian*); zie [CayenneLPP](../../libraries/core/cayenne-lpp.md).
- **Tekst is UTF-8** en niet per se afgesloten met een nulbyte — de
  framelengte is de grens.
- **Er is geen uitlijning of opvulling.** Er staan geen ongebruikte
  tussenbytes tussen de velden: ze staan tegen elkaar aan, en
  een veld dat pas vanaf een bepaalde protocolversie bestaat, staat achteraan
  zodat oudere clients gewoon eerder ophouden met lezen.

Dat laatste is de reden dat de firmware zijn antwoorden opbouwt met een
oplopende teller en aan het eind precies zoveel bytes wegschrijft als hij
gevuld heeft, in plaats van een vaste structuur te versturen.

## De grens van 176 bytes

Er is één framegrootte voor alle transporten:

`src/helpers/BaseSerialInterface.h` r.5

```cpp
#define MAX_FRAME_SIZE  176   // +4 for transport codes (region scoping)
```

Het commentaar verwijst naar de vier bytes die een pakket extra kan dragen
om het tot een verspreidingsgebied te beperken (*region scoping*); zie
[Regio's en Scopes](../../techniek/regions-and-scopes.md).

Voor een client zijn er twee gevolgen. Bij verzenden moet je zelf
controleren of het past — de firmware weigert wat te groot is, maar pas
nadat het al is verstuurd. Bij ontvangen moet je erop rekenen dat een
frame nooit langer is dan 176 bytes, en dat een langer frame door de
firmware wordt afgekapt in plaats van geweigerd.

## Wat er overblijft voor gegevens

De opcode kost één byte, en de meeste commando's hebben nog een adres, een
index of een tijdstempel nodig. Voor datagrammen op een kanaal — losse
pakketten met gestructureerde gegevens in plaats van tekst — is die overhead
vastgelegd:

`examples/companion_radio/MyMesh.cpp` r.101

```cpp
#define MAX_CHANNEL_DATA_LENGTH       (MAX_FRAME_SIZE - 9)
```

Negen bytes overhead, dus 167 bytes gegevens. Wie meer aanbiedt, krijgt een
fout terug:

`examples/companion_radio/MyMesh.cpp` r.1169-1171

```cpp
    } else if (payload_len > MAX_CHANNEL_DATA_LENGTH) {
      MESH_DEBUG_PRINTLN("CMD_SEND_CHANNEL_DATA payload too long: %d > %d", payload_len, MAX_CHANNEL_DATA_LENGTH);
      writeErrFrame(ERR_CODE_ILLEGAL_ARG);
```

Voor tekstberichten geldt hetzelfde principe met een andere overhead. De
praktische ondergrens om te onthouden: reken op ongeveer 150 bytes bruikbare
tekst per bericht, en bedenk dat een LoRa-pakket daarna nóg een keer wordt
opgedeeld door wat er over de lucht past — zie
[MeshCore Pakketstructuur](../../techniek/packet-structure.md).

## Er is geen fragmentatie

Het protocol kan één groot logisch bericht niet automatisch over meerdere
frames verdelen. Zo'n verdeling heet fragmentatie. Waar ze toch nodig is, is
het per geval opgelost:

| Geval | Oplossing |
|---|---|
| Veel contacten ophalen | een reeks losse frames: `RESP_CODE_CONTACTS_START`, dan `RESP_CODE_CONTACT` per stuk, dan `RESP_CODE_END_OF_CONTACTS` |
| Berichten ophalen | één frame per bericht, herhaald tot `RESP_CODE_NO_MORE_MESSAGES` |
| Iets ondertekenen | een eigen deelprotocol van drie commando's: `CMD_SIGN_START` (33), `CMD_SIGN_DATA` (34), `CMD_SIGN_FINISH` (35) |

Dat derde geval is het enige waar de app zelf moet opdelen. De node meldt
bij `CMD_SIGN_START` hoeveel hij aankan:

`examples/companion_radio/MyMesh.cpp` r.1712-1717

```cpp
  } else if (cmd_frame[0] == CMD_SIGN_START) {
    out_frame[0] = RESP_CODE_SIGN_START;
    out_frame[1] = 0; // reserved
    uint32_t len = MAX_SIGN_DATA_LEN;
    memcpy(&out_frame[2], &len, 4);
    _serial->writeFrame(out_frame, 6);
```

`MAX_SIGN_DATA_LEN` is 8 KiB (`MyMesh.cpp` r.137). De app stuurt dat in
brokken van maximaal 175 bytes met `CMD_SIGN_DATA` en sluit af met
`CMD_SIGN_FINISH`.

## Wat een client moet controleren

| Bij verzenden | Bij ontvangen |
|---|---|
| past het commando binnen 176 bytes | is het frame lang genoeg voor de velden die je leest |
| ken je de lengtegrens van dít commando | is de eerste byte een antwoord of een push |
| is de klok gezet (voor alles met een tijdstempel) | hoort dit antwoord bij mijn openstaande verzoek |
| is er nog een verzoek open | is het veld dat je leest wel aanwezig in deze protocolversie |

De rechterkolom onderaan is de meest gemaakte fout. Velden die in een latere
`FIRMWARE_VER_CODE` zijn toegevoegd staan achteraan, en een oudere node
stuurt een korter frame. Wie de lengte niet controleert, kan bytes buiten het
ontvangen frame als geldige velden interpreteren of een leesfout
veroorzaken. Zie [Het interactiemodel](../logisch/interaction-model.md).

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`src/helpers/BaseSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/BaseSerialInterface.h)
  — `MAX_FRAME_SIZE`
- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.cpp)
  — `MAX_CHANNEL_DATA_LENGTH`, `MAX_SIGN_DATA_LEN`, de lengtecontroles

Verwante hoofdstukken:

- [USB-serieel](../../hardware/interfaces/usb-serial.md) — de header rond
  het frame
- [De drie transporten](transports.md) — wat elk transport oplegt
- [MeshCore Pakketstructuur](../../techniek/packet-structure.md) — wat er
  daarna over de lucht gaat
- [De commandogroepen](command-groups.md) — welk commando welke payload
  verwacht
