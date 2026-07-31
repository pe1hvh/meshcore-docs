# Het interactiemodel

*VRAAG · ANTWOORD · PUSH · TWEE VERSIEASSEN · HERVERBINDEN*

Er lopen twee soorten verkeer over dezelfde verbinding: antwoorden die de
app heeft opgevraagd, en meldingen die de node uit zichzelf stuurt. Dat
onderscheid bepaalt de vorm van elke client. Daarnaast onderhandelen app en
node bij het verbinden over wat ze van elkaar begrijpen — over twee
onafhankelijke versienummers.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `examples/companion_radio/MyMesh.cpp` en
> `examples/companion_radio/MyMesh.h`. De volgorde van de openingsstappen is
> vergeleken met `docs/companion_protocol.md` en met `meshcore_py` v2.3.8.

![Verloop van een verbinding: app start, apparaatvraag, tijd zetten,
contacten en kanalen ophalen, en daarna een lus die berichten ophaalt zolang
de node meldt dat er iets klaarstaat](../../../images/nl/companion-interaction-1.svg)

## Drie soorten frames

Een frame is één afgebakend gegevensblok dat tussen de app en de node wordt
verstuurd. Het is iets anders dan een LoRa-pakket: dat gaat over de lucht,
een frame gaat over de kabel of de radioverbinding tussen app en node. De
eerste byte van elk frame geeft aan wat voor frame het is. De gebruikte
nummerreeksen overlappen niet:

| Soort | Bereik | Richting | Aantal |
|---|---|---|---|
| Commando | 1 – 65 | app → node | 58 |
| Antwoord | 0 – 28 | node → app, op verzoek | 29 |
| Push | `0x80` – `0x90` | node → app, ongevraagd | 17 |

Antwoorden en pushcodes delen dezelfde byte maar botsen niet: pushcodes
beginnen op `0x80`, ver boven de hoogste antwoordcode. Een client kan daarom
op één plek beslissen of een binnengekomen frame hoort bij een openstaand
verzoek — een commando waarop de app nog een antwoord verwacht — of niet.

## Vraag en antwoord

Eén commando levert nul, één of veel frames op. `CMD_GET_CONTACTS` is het
duidelijkste voorbeeld: `RESP_CODE_CONTACTS_START`, dan een reeks
`RESP_CODE_CONTACT`, dan `RESP_CODE_END_OF_CONTACTS`. Een client die na het
eerste antwoord ophoudt met luisteren, mist de rest.

Sommige commando's leveren alleen `RESP_CODE_OK` of `RESP_CODE_ERR` op. De
foutcode zit in de tweede byte:

`examples/companion_radio/MyMesh.cpp` r.130-135

```cpp
#define ERR_CODE_UNSUPPORTED_CMD        1
#define ERR_CODE_NOT_FOUND              2
#define ERR_CODE_TABLE_FULL             3
#define ERR_CODE_BAD_STATE              4
#define ERR_CODE_FILE_IO_ERROR          5
#define ERR_CODE_ILLEGAL_ARG            6
```

`ERR_CODE_UNSUPPORTED_CMD` is de code die een client tegenkomt wanneer hij
een commando gebruikt dat deze firmware nog niet kent. Dat is de praktische
manier om te ontdekken wat een node kan: proberen, en op deze fout letten.

## Push: de node vraagt om aandacht

Een ongevraagde melding — in de firmware een pushbericht, herkenbaar aan zijn
pushcode — is een frame dat de node uit zichzelf stuurt, zonder dat de app
erom heeft gevraagd. Binnengekomen berichten stuurt de node namelijk niet uit
zichzelf. Hij meldt alleen dát er iets klaarstaat, met
`PUSH_CODE_MSG_WAITING` (`0x83`). De app haalt
het vervolgens op met `CMD_SYNC_NEXT_MESSAGE`, net zo lang tot
`RESP_CODE_NO_MORE_MESSAGES` komt.

Die omkering is bewust. De node hoeft niet bij te houden wat de app al
gezien heeft; de app bepaalt zelf wanneer hij leegt. De prijs is dat een
client die de melding negeert, de wachtrij laat vollopen — zie
[Verantwoordelijkheden](responsibilities.md).

De overige zestien pushcodes werken hetzelfde: ze melden een gebeurtenis
(`PUSH_CODE_ADVERT`, `PUSH_CODE_SEND_CONFIRMED`, `PUSH_CODE_CONTACTS_FULL`)
en zijn nooit een antwoord op een openstaand verzoek.

## Twee versieassen

Bij het verbinden wisselen app en node twee getallen uit die niets met
elkaar te maken hebben. Er is daarnaast nog een derde versienummer in omloop,
dat voor het protocol geen betekenis heeft:

| Nummer | Van wie | Wat het zegt |
|---|---|---|
| `app_target_ver` | de app | welke protocolversie de app begrijpt |
| `FIRMWARE_VER_CODE` | de node | welke protocolversie de firmware aankan |
| firmwareversie, bijvoorbeeld `v1.16.0` | de node | het versienummer dat mensen zien; staat los van het protocol |

**De app zegt wat hij begrijpt.** Byte 1 van `CMD_DEVICE_QUERY` is
`app_target_ver`. De firmware bewaart dat en past aan wat hij stuurt:

`examples/companion_radio/MyMesh.cpp` r.1009-1016

```cpp
  if (cmd_frame[0] == CMD_DEVICE_QUERY && len >= 2) { // sent when app establishes connection
    app_target_ver = cmd_frame[1];                    // which version of protocol does app understand

    int i = 0;
    out_frame[i++] = RESP_CODE_DEVICE_INFO;
    out_frame[i++] = FIRMWARE_VER_CODE;
    out_frame[i++] = MAX_CONTACTS / 2;   // v3+
    out_frame[i++] = MAX_GROUP_CHANNELS; // v3+
```

Bij `app_target_ver >= 3` stuurt de firmware ontvangen berichten in een
ander formaat: `RESP_CODE_CONTACT_MSG_RECV_V3` (16) in plaats van
`RESP_CODE_CONTACT_MSG_RECV` (7). Een client die 3 opgeeft maar het oude
formaat verwacht, leest onzin.

**De node zegt wat hij kan.** Dat is `FIRMWARE_VER_CODE`, een enkel getal
dat losstaat van het versienummer dat mensen zien:

`examples/companion_radio/MyMesh.h` r.7-8

```cpp
/*------------ Frame Protocol --------------*/
#define FIRMWARE_VER_CODE 13
```

Op commit `03b6ef4` staat dat op 13, bij firmware `v1.16.0`. Aan dat getal
hangen velden en gedrag: `client_repeat` in het apparaatantwoord vanaf 9,
`path_hash_mode` vanaf 10, en verzoeken aan nodes die geen contact zijn
vanaf 13. Een client die die velden onvoorwaardelijk leest, loopt op oudere
firmware uit het frame.

De twee assen zijn onafhankelijk: een nieuwe app op oude firmware en een
oude app op nieuwe firmware zijn allebei normale situaties.

## Herverbinden is opnieuw beginnen

`app_target_ver` staat in het geheugen van de node, niet op schijf, en
begint op nul:

`examples/companion_radio/MyMesh.cpp` r.861

```cpp
  app_target_ver = 0;
```

Valt de verbinding weg, dan is de onderhandeling vergeten. Na elke
herverbinding moet de opening dus opnieuw: de app meldt zich aan met
`CMD_APP_START`, vraagt met `CMD_DEVICE_QUERY` de apparaatgegevens op en
spreekt daarbij de protocolversie af, en werkt daarna pas zijn eigen
gegevens bij. Een client die na herverbinden meteen berichten ophaalt zonder
die twee commando's, krijgt stilzwijgend het oudste formaat. Dat is geen
foutmelding — het is een frame dat er plausibel uitziet en verkeerd wordt
gelezen.

`meshcore_py` lost dat op door de aanmelding aan de herverbinding te hangen
in plaats van aan het opstarten van het programma; zie
[Architectuur van een client](../technisch/client-architecture.md).

## De openingsvolgorde

De officiële spec beschrijft deze volgorde, en `meshcore_py` volgt hem:

1. `CMD_APP_START` — de app meldt zich met een naam; de node antwoordt met
   `RESP_CODE_SELF_INFO`: eigen sleutel, zendvermogen, positie,
   radioparameters
2. `CMD_DEVICE_QUERY` — versieonderhandeling en de grenzen van dit apparaat
3. `CMD_SET_DEVICE_TIME` — de node heeft geen eigen tijdsbron die
   betrouwbaar doorloopt
4. `CMD_GET_CONTACTS` — eventueel met een tijdstempel, zodat alleen
   gewijzigde contacten terugkomen
5. `CMD_GET_CHANNEL` — één keer per slot, tot het aantal dat stap 2 meldde
6. `CMD_SYNC_NEXT_MESSAGE` — tot `RESP_CODE_NO_MORE_MESSAGES`

Stap 3 is geen formaliteit. Zonder gezette klok krijgen verzonden berichten
een tijdstempel die nergens op slaat, en dat is aan de ontvangende kant niet
te herstellen.

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.cpp)
  — foutcodes, `CMD_DEVICE_QUERY`, `app_target_ver`
- [`examples/companion_radio/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.h)
  — `FIRMWARE_VER_CODE`
- [`docs/companion_protocol.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/docs/companion_protocol.md)
  — de officiële beschrijving van de openingsvolgorde

Verwante hoofdstukken:

- [Verantwoordelijkheden](responsibilities.md) — waarom de wachtrij leeg
  moet
- [De commandogroepen](../technisch/command-groups.md) — alle 58 commando's
- [Architectuur van een client](../technisch/client-architecture.md) — waar
  de herverbinding thuishoort
