# Channel Structure & PSK

*KANAALSTRUCTUUR · AES-128 · PSK · FLASH-OPSLAG · PROTOCOL-COMMANDO'S*

══════════════════════════════════════════════════════════════

## 1. Wat is een kanaal?

Een **kanaal** in MeshCore is een **gedeelde versleutelingssleutel voor over-the-air broadcast**. Alle nodes die dezelfde Pre-Shared Key (PSK) hebben geconfigureerd, kunnen berichten van dat kanaal ontsleutelen en er berichten op versturen. Er is geen server, geen berichtgeschiedenis en geen centrale "room" — een kanaal bestaat uit niets anders dan de berichten die op dezelfde wijze versleuteld zijn.

**Belangrijk:** het woord "kanaal" heeft hier *niets* te maken met een fysiek radiokanaal of frequentieband. Alle MeshCore-nodes zenden op **exact dezelfde frequentie**, met dezelfde bandbreedte en dezelfde LoRa-parameters. Er is slechts één gedeeld radiokanaal. Wat in MeshCore een "kanaal" heet, is uitsluitend een **logische scheiding op basis van de versleuteling**: berichten van verschillende kanalen reizen door dezelfde lucht, maar zijn alleen leesbaar voor nodes die de bijbehorende PSK kennen. Een repeater die de PSK niet heeft, forwardt het bericht gewoon door — hij kan het alleen niet ontsleutelen.

Dit onderscheidt een kanaal fundamenteel van een *Room Server*: een Room Server slaat berichten op zodat je ze later kunt ophalen. Een kanaal niet — een bericht dat over de lucht gaat, wordt ofwel ontvangen op het moment van uitzending, of is voor altijd verloren. Er is geen herhaalmechanisme, geen synchronisatie en geen servercomponent.

| Eigenschap | MeshCore kanaal | Room Server (ter vergelijking) |
|---|---|---|
| Berichtopslag | ❌ Geen — fire and forget | ✅ Ja — tot 32 ongelezen berichten |
| Server vereist | ❌ Nee — puur peer-to-peer | ✅ Ja — aparte room server node |
| Bericht missen | Ja — buiten bereik = bericht kwijt | Nee — ophalen zodra je verbinding hebt |
| Technisch model | Gedeelde AES-sleutel voor broadcast | Berichten-server met auth + sync |

> [!WARNING]
> **⚠ Let op** — Kanaalcommunicatie vereist dat het device de PSK kent. De GUI kan geen berichten op kanalen versturen of ontvangen waarvan het device de sleutel niet heeft. Dit is de fundamentele reden waarom de GUI niet meer kanalen kan *activeren* dan het device slots heeft.

══════════════════════════════════════════════════════════════

## 2. Drie typen kanalen

MeshCore kent **drie typen kanalen** die fundamenteel van elkaar verschillen in hoe de PSK tot stand komt en wie er toegang toe heeft. Het slotnummer bepaalt *niet* het type — dat bepaalt uitsluitend de oorsprong en distributiemethode van de PSK.

🌐 Type 1 — Public (Openbaar)

- **PSK:** hardcoded in firmware — `izOH6cXN6mrJ5e26oRXNcg==`
- **Sleuteloorsprong:** vaste bekende sleutel, identiek op elk MeshCore device
- **Toegang:** iedereen met een MeshCore device, zonder configuratie
- **Slot:** altijd slot 0 — automatisch aangemaakt bij opstart
- **Schrijfbescherming:** GUI mag nooit naar slot 0 schrijven
- **Gebruik:** ontdekking, open groepschat, testen

#️⃣ Type 2 — Hashtag (naam-afgeleide sleutel)

- **PSK:** afgeleid van de kanaalnaam via een deterministisch algoritme
- **Sleuteloorsprong:** `hash(naam)` — iedereen die de naam kent, kan de PSK reproduceren
- **Toegang:** iedereen die de kanaalnaam kent — geen expliciete sleuteluitwisseling nodig
- **Slot:** slots 1–N (configureerbaar)
- **Gebruik:** community-kanalen, open groepen met bekende naam

🔒 Type 3 — Private (willekeurige sleutel)

- **PSK:** willekeurig gegenereerde 16-byte sleutel
- **Sleuteluitwisseling:** out-of-band via QR-code export of handmatig invoeren
- **Toegang:** uitsluitend nodes waaraan de PSK expliciet is verstrekt
- **Slot:** slots 1–N (configureerbaar)
- **Gebruik:** besloten groepen, beveiliging, teamcommunicatie

> [!NOTE]
> **Sleuteloorsprong bepaalt het type** — Technisch zijn slots 1–N identiek. Het verschil tussen Hashtag en Private zit uitsluitend in hoe de PSK tot stand komt: afgeleid van de naam (Hashtag) of willekeurig gegenereerd (Private). Slot 0 is altijd Public door de hardcoded PSK in de firmware.

### Technische vergelijking

| Eigenschap | Public | Hashtag | Private |
|---|---|---|---|
| PSK-oorsprong | Hardcoded in firmware | Afgeleid van kanaalnaam | Willekeurig gegenereerd |
| Sleuteluitwisseling | Geen — ingebouwd | Naam kennen volstaat | QR-code of handmatig invoeren |
| channel.hash waarde | Altijd hetzelfde (deterministisch) | Deterministisch op naam | Afhankelijk van random PSK |
| Toegang zonder configuratie | Ja — direct op elk device | Ja — als naam bekend is | Nee — PSK moet worden geladen |
| Repeater-forwarding | Altijd forwarden op hash-match | Forwarden op hash-match | Forwarden op hash — PSK niet nodig |
| GUI schrijven | ❌ Verboden (slot 0) | ✅ Via CMD_SET_CHANNEL | ✅ Via CMD_SET_CHANNEL |
| Beveiliging berichten | Geen — PSK wereldwijd bekend | Laag — naam is de sleutel | Hoog — PSK alleen bij leden |

> [!NOTE]
> **Hash-byte en repeaters** — Repeaters forwarden op de `channel.hash`-byte zonder te ontsleutelen. Voor het Public channel kent elke node de hash. Voor private kanalen kennen repeaters de hash ook — maar kunnen de inhoud niet lezen zonder PSK. Repeaters hoeven de PSK niet te kennen om berichten door te sturen.

══════════════════════════════════════════════════════════════

## 3. Data-structuur: ChannelDetails

Op het device wordt elk kanaal opgeslagen in een `ChannelDetails`-struct met drie velden:

| Veld | Type | Grootte | Doel |
|---|---|---|---|
| `channel.secret` | `uint8_t[32]` | 32B | Pre-Shared Key — AES-128 gebruikt de eerste 16 bytes |
| `channel.hash` | `uint8_t[1]` | 1B | SHA-256(secret)[0] — runtime berekend, nooit opgeslagen. Snelle packet-matching. |
| `name` | `char[32]` | 32B | Weergavenaam, null-terminated UTF-8. Max 31 bruikbare tekens. |

### Bestandsformaat: /channels2

Kanalen worden persistent opgeslagen in `/channels2` op het device-filesystem (SPIFFS/LittleFS). Elk record is exact **68 bytes**:

0x00
4B
unused — gereserveerd voor toekomstige metadata
0x04
32B
name
— kanaalnaam, null-padded
0x24
32B
channel.secret
— Pre-Shared Key (AES-128, eerste 16 bytes)

4 + 32 + 32 = **68 bytes per record**. De `channel.hash` wordt bij elke opstart herberekend en nooit opgeslagen.

### Slot-array op het device

> [!NOTE]
> **channels[MAX_GROUP_CHANNELS]** — `MAX_GROUP_CHANNELS` is een compile-time build-flag (default: **8**, configureerbaar tot bijv. 40). Het device rapporteert de actuele waarde als `max_channels` (uint8) in de `RESP_CODE_DEVICE_INFO` response (byte 3, firmware ≥ v3). Slot 0 = altijd Public.

══════════════════════════════════════════════════════════════

## 4. Protocol-commando's

### CMD_GET_CHANNEL (0x1F) — kanaalinfo opvragen

0x1F
cmd
idx
slot 0–N

Response: `PACKET_CHANNEL_INFO (0x12)` — kanaalnaam (32B) + secret (16B).

### CMD_SET_CHANNEL (0x20) — kanaal schrijven (alleen private slots!)

0x20
cmd
idx
slot ≠ 0
naam · 32 bytes · null-padded
name
secret · 32 bytes
PSK

Frame-grootte: **66 bytes**. BLE vereist MTU ≥ 66 (request MTU = 512B). Na ontvangst herberekent het device `hash` en schrijft naar `/channels2`.

### CMD_SEND_CHANNEL_TXT_MSG (0x03) — bericht versturen

0x03
cmd
type
txt_type
idx
kanaal
timestamp · 4B little-endian Unix
ts
tekst · max 133 tekens UTF-8
payload
══════════════════════════════════════════════════════════════

## 5. Flowdiagrammen

### Flow 1 — Device opstarten & kanaalinitialisatie

![Diagram 1 bij techniek-channels](../../images/nl/techniek-channels-1.svg)

Figuur 1 — Device-opstartsequentie: laden van /channels2, hash-berekening, Public auto-add bij afwezigheid

### Flow 2 — Kanaal bericht verzenden (GUI → radio)

Het verzendpad bij public en private kanalen is identiek. Het verschil zit uitsluitend in de PSK.

![Diagram 2 bij techniek-channels](../../images/nl/techniek-channels-2.svg)

Figuur 2 — Verzendpad: GUI → AES-128 versleuteling → LoRa TX.

### Flow 3 — Kanaal bericht ontvangen (radio → GUI)

De hash-scan maakt het systeem efficiënt: het device vergelijkt één byte per slot vóórdat het de zwaardere AES-decrypt uitvoert.

![Diagram 3 bij techniek-channels](../../images/nl/techniek-channels-3.svg)

Figuur 3 — Ontvangstpad: LoRa RX → hash-scan → AES-128 decrypt → GUI.

### Flow 4 — Preset schrijven naar device-slot (CMD_SET_CHANNEL)

Alleen private slots (idx ≥ 1) mogen worden beschreven. De GUI is verantwoordelijk voor de slot 0-beveiliging.

![Diagram 4 bij techniek-channels](../../images/nl/techniek-channels-4.svg)

Figuur 4 — Preset schrijven: GUI → CMD_SET_CHANNEL → RAM + hash → /channels2 → bevestiging terug naar GUI

══════════════════════════════════════════════════════════════

## 6. Cryptografische details

### Versleuteling: AES-128

| Aspect | Detail |
|---|---|
| Algoritme | AES-128 (encryptThenMAC patroon) |
| Sleutellengte | 16 bytes — de eerste 16 bytes van `channel.secret[32]` |
| PSK-formaat (extern) | Base64-encoded, 16 bytes gedecodeerd. Voorbeeld Public: `izOH6cXN6mrJ5e26oRXNcg==` |
| Hash-byte | `SHA-256(secret)[0]` — packet-matching, niet voor security |
| Opslag op device | Flash als `secret[32]`; `hash` runtime herberekend bij opstart |
| Opslag op host (GUI) | Productie: OS-keychain. v1: JSON (bewust geaccepteerd risico) |

> [!WARNING]
> **⚠ Hash-botsingen** — De hash-byte is slechts 1 byte (256 waarden). Bij 8 actieve kanalen: ~3% kans op botsing. Het device probeert bij een botsing AES-decrypt op beide matching slots — de MAC-verificatie bepaalt welke correct is. Ontworpen gedrag, geen bug.

### Public / Hashtag / Private: cryptografisch verschil

| Eigenschap | Public | Hashtag | Private |
|---|---|---|---|
| PSK-oorsprong | Hardcoded in firmware — altijd gelijk | Deterministisch afgeleid van naam | Willekeurig — uniek per kanaal |
| channel.hash | Deterministisch, gelijk op alle nodes | Deterministisch op naam | Afhankelijk van de willekeurige PSK |
| Toegang zonder configuratie | Ja — direct beschikbaar op elk device | Ja — naam kennen is voldoende | Nee — PSK moet eerst worden geladen |
| AES-decrypt door derden | Ja — PSK wereldwijd bekend | Ja — als naam herleidbaar is | Alleen bij nodes met dezelfde PSK |
| Repeater-forwarding | Elke repeater herkent hash en forwardt | Forwarden op hash — PSK niet nodig | Forwarden op hash — PSK niet nodig |
| GUI schrijven | ❌ Verboden | ✅ Via CMD_SET_CHANNEL | ✅ Via CMD_SET_CHANNEL |

══════════════════════════════════════════════════════════════

## 7. Beperkingen samenvatting

| Beperking | Waarde | Wijzigbaar zonder firmware? |
|---|---|---|
| Max actieve kanalen | `MAX_GROUP_CHANNELS` (default 8) | Nee — compile-time build-flag |
| Max kanaalnaam | 31 bruikbare tekens + null-terminator | Nee — vaste struct-veldgrootte |
| Secret-formaat | 32 bytes intern, eerste 16 voor AES-128 | Nee — protocol-definitie |
| Slot 0 | Altijd Public (hardcoded PSK) — GUI schrijft hier nooit naar | Nee — firmware-initialisatie |
| BLE MTU voor CMD_SET_CHANNEL | ≥ 66 bytes (request MTU = 512) | GUI-verantwoordelijkheid |
| Firmware-versie voor max_channels | Firmware ≥ v3 vereist (RESP_CODE_DEVICE_INFO byte 3) | GUI moet firmware_ver checken |

Bronnen
meshcore-dev/MeshCore @ 9f1a3eaf — ChannelDetails.h
meshcore-dev/MeshCore @ 9f1a3eaf — DataStore.cpp
docs.meshcore.io — Companion Protocol
