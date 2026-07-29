# Requests en CLI

*STATUS · KEEP-ALIVE · TELEMETRIE · ACCESS LIST · BEHEER OVER DE RADIO*

Naast posten kan een ingelogde client de server ook iets vrágen. Vier
requesttypes, elk met een eigen drempel: sommige mag iedereen die is
ingelogd, één is voorbehouden aan de beheerder, en één levert een ander
antwoord op naar gelang je rechten. Daarbovenop kan een beheerder de hele
CLI over de radio bedienen — hetzelfde commandostel dat je via USB krijgt.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, `src/helpers/CommonCLI.cpp`,
> `src/helpers/ClientACL.cpp`, en de officiële `docs/cli_commands.md`,
> `docs/payloads.md` en `docs/faq.md`.

## Het overzicht

![Requesttypes van client naar room server, met per type wie het mag
gebruiken](../../../images/nl/room-server-requests-1.svg)

Een request gaat als `PAYLOAD_TYPE_REQ`: vier bytes tijdstempel, dan één byte
requesttype, dan eventuele parameters. Het antwoord is een
`PAYLOAD_TYPE_RESPONSE` waarin de server de tijdstempel van de vraag
terugkaatst, zodat de client vraag en antwoord aan elkaar kan knopen.

De nummering is niet exclusief voor de room server. `0x01`, `0x02` en `0x03`
komen ook voor bij de repeater, de sensor en de companion; `0x04`
(`REQ_TYPE_GET_AVG_MIN_MAX`) hoort alleen bij de sensor, en `0x06` en `0x07`
(buren en eigenaarinformatie) alleen bij de repeater. Een room server die
`0x06` binnenkrijgt, valt door naar het einde van `handleRequest()` en
antwoordt niet.

## 0x01 — status

Levert een blok van 52 bytes met de toestand van de node: accuspanning,
ruisvloer, laatste RSSI en SNR, aantallen verzonden en ontvangen pakketten
gesplitst naar flood en direct, totale zendtijd, uptime, duplicaten, en twee
tellers die alleen een room server heeft.

`examples/simple_room_server/MyMesh.cpp` r.24-39

```cpp
struct ServerStats {
  uint16_t batt_milli_volts;
  uint16_t curr_tx_queue_len;
  int16_t noise_floor;
  int16_t last_rssi;
  uint32_t n_packets_recv;
  uint32_t n_packets_sent;
  uint32_t total_air_time_secs;
  uint32_t total_up_time_secs;
  uint32_t n_sent_flood, n_sent_direct;
  uint32_t n_recv_flood, n_recv_direct;
  uint16_t err_events; // was 'n_full_events'
  int16_t last_snr;    // x 4
  uint16_t n_direct_dups, n_flood_dups;
  uint16_t n_posted, n_post_push;
};
```

`n_posted` telt hoeveel posts er ooit zijn geplaatst, `n_post_push` hoeveel
duwpogingen er zijn gedaan. Het verschil tussen die twee zegt iets over de
gezondheid van de room: bij twee actieve deelnemers hoort `n_post_push`
ongeveer gelijk te zijn aan `n_posted` (elke post gaat naar één ander), bij
tien deelnemers ongeveer negen keer zo hoog. Loopt hij nog veel verder op,
dan worden er posts herhaald omdat de bevestigingen niet aankomen.

`last_snr` staat vermenigvuldigd met 4 in het veld; de client moet delen om
de echte waarde te krijgen.

## 0x02 — keep-alive

Dit is het enige request dat de server **alleen direct** beantwoordt, dus
niet als het pad nog onbekend is. Een client stuurt hem periodiek om drie
dingen tegelijk te doen: laten weten dat hij er nog is, zijn `sync_since`
bijstellen, en horen hoeveel er voor hem klaarstaat.

Het antwoord is geen `RESPONSE` maar een ACK met één byte eraan geplakt:

`examples/simple_room_server/MyMesh.cpp` r.554-561

```cpp
          uint32_t ack_hash; // calc ACK to prove to sender that we got request
          mesh::Utils::sha256((uint8_t *)&ack_hash, 4, data, 9, client->id.pub_key, PUB_KEY_SIZE);

          auto reply = createAck(ack_hash);
          if (reply) {
            reply->payload[reply->payload_len++] = getUnsyncedCount(client); // NEW: add unsynced counter to end of ACK packet
            sendDirect(reply, client->out_path, client->out_path_len, SERVER_RESPONSE_DELAY);
          }
```

Die extra byte is de teller die vroeger in het inlogantwoord zat (zie
[Inloggen en de ACL](login-and-acl.md)). Hij telt de posts die nieuwer zijn
dan `sync_since` en niet van deze client zelf zijn — dus wat er nog voor hem
in de wachtrij staat.

De client mag in het request optioneel vier bytes meesturen met de tijdstempel
van de laatste post die hij heeft. Staat daar een waarde groter dan nul, dan
overschrijft de server zijn eigen `sync_since` voor deze client daarmee. Dat
is het herstelpad na een herstart van de server: de client vertelt waar hij
gebleven was.

> [!NOTE]
> **Die overschrijving kent geen controle.** De server neemt de waarde over
> zonder te toetsen of hij vooruit of achteruit gaat. Een client kan zijn
> teller dus ook terugzetten en posts opnieuw ontvangen — voor zover die nog
> in de wachtrij staan.

## 0x03 — telemetrie

Levert de meetwaarden van de node in CayenneLPP-formaat: minimaal de
accuspanning en, waar het bord dat ondersteunt, de temperatuur van de
processor. Externe sensoren komen erbij als ze aanwezig zijn.

De client stuurt een masker mee dat bepaalt welke kanalen hij wil zien. Voor
een gast wordt dat masker genegeerd en op `0x00` gezet: die krijgt alleen de
basiswaarden, ongeacht wat hij vraagt
(`examples/simple_room_server/MyMesh.cpp` r.170-172).

## 0x05 — access list

Alleen voor een beheerder, en het antwoord is smaller dan de naam doet
vermoeden.

`examples/simple_room_server/MyMesh.cpp` r.185-195

```cpp
  if (payload[0] == REQ_TYPE_GET_ACCESS_LIST && sender->isAdmin()) {
    uint8_t res1 = payload[1];   // reserved for future  (extra query params)
    uint8_t res2 = payload[2];
    if (res1 == 0 && res2 == 0) {
      uint8_t ofs = 4;
      for (int i = 0; i < acl.getNumClients() && ofs + 7 <= sizeof(reply_data) - 4; i++) {
        auto c = acl.getClientByIdx(i);
        if (!c->isAdmin()) continue;  // skip non-Admin entries
        memcpy(&reply_data[ofs], c->id.pub_key, 6); ofs += 6;  // just 6-byte pub_key prefix
        reply_data[ofs++] = c->permissions;
      }
    }
```

Per entry zeven bytes: zes bytes sleutelprefix en één permissiebyte. De regel
`if (!c->isAdmin()) continue;` zorgt ervoor dat er uitsluitend beheerders in
de lijst staan. Wie de deelnemers van zijn room wil zien, komt van een
koude kermis thuis: **die lijst bestaat niet**, ook niet voor de beheerder.
Een room server weet wel wie er is ingelogd — hij heeft hun sleutels en hun
tellers nodig — maar geeft die kennis nergens prijs.

> [!WARNING]
> **Deze documentatie beweerde eerder iets anders.** Het hoofdstuk
> [Communicatie](../../gebruik/communication.md) noemde tot deze revisie een
> ledenlijst als eigenschap van een room server. Dat klopte niet en is
> gecorrigeerd.

Een client die niet als beheerder is ingelogd krijgt op `0x05` geen
foutmelding maar helemaal geen antwoord: `handleRequest()` valt door naar
`return 0` en de aanroeper verstuurt dan niets.

## De CLI over de radio

Een beheerder kan elk CLI-commando naar de server sturen als tekstbericht met
vlaggen `TXT_TYPE_CLI_DATA` in plaats van `TXT_TYPE_PLAIN`. Het antwoord komt
terug als tekstbericht met dezelfde vlaggen.

`examples/simple_room_server/MyMesh.cpp` r.452-464

```cpp
      if (flags == TXT_TYPE_CLI_DATA) {
        if (client->isAdmin()) {
          if (is_retry) {
            temp[5] = 0; // no reply
          } else {
            handleCommand(sender_timestamp, (char *)&data[5], (char *)&temp[5]);
            temp[4] = (TXT_TYPE_CLI_DATA << 2); // attempt and flags,  (NOTE: legacy was: TXT_TYPE_PLAIN)
          }
          send_ack = false;
        } else {
          temp[5] = 0;      // no reply
          send_ack = false; // and no ACK...  user shoudn't be sending these
        }
```

Twee dingen vallen op. Er komt **nooit** een ACK op een CLI-commando, ook
niet voor een beheerder: het antwoord zelf is de bevestiging. En een
herhaalde poging wordt herkend en niet opnieuw uitgevoerd — dat voorkomt dat
een `reboot` twee keer wordt uitgevoerd omdat het antwoord onderweg
zoekraakte, maar het betekent ook dat je op een herhaling geen antwoord meer
krijgt.

Een niet-beheerder die een commando stuurt, krijgt niets terug. Geen
weigering, geen ACK.

### De room-specifieke commando's

De meeste commando's komen uit `CommonCLI` en zijn gelijk aan die van een
repeater. Vier zijn hier van belang:

| Commando | Wat het doet | Alleen serieel |
|---|---|---|
| `set guest.password <tekst>` | het deelnemerswachtwoord | nee |
| `set allow.read.only on\|off` | meelezen zonder geldig wachtwoord | nee |
| `setperm <pubkey-hex> <getal>` | rechten zetten op een publieke sleutel | nee |
| `get acl` | de ACL op de console dumpen | **ja** |

`setperm` is het enige beheer dat er is. Het neemt een publieke sleutel in
hex — een prefix mag, mits een even aantal tekens — en een getal met de
nieuwe rechten. Rechten `0` verwijdert het contact uit de tabel in plaats van
het met rol `GUEST` te bewaren (`src/helpers/ClientACL.cpp` r.123-128). Er is
geen apart commando om iemand toe te voegen: een deelnemer voegt zichzelf toe
door in te loggen.

`get acl` controleert expliciet op `sender_timestamp == 0`, wat alleen zo is
bij invoer via de seriële console. Over de radio bestaat dit commando niet;
het valt dan door naar de gewone CLI-afhandeling, die het niet kent.

### Beheer op afstand vanaf een client

Wat de firmware doet is hierboven beschreven: elke ingelogde beheerder kan
CLI-commando's sturen. Of jouw client dat ook aanbiedt, is een tweede. De
officiële FAQ meldt dat je op een T-Deck een registratiesleutel nodig hebt om
beheer over RF te ontgrendelen, en dat de Android- en iOS-app een wachttimer
voor beheer van repeaters en room servers kent die je kunt vrijkopen. Dat is
dus een beperking in de clientsoftware en niet in de room server.

> [!NOTE]
> **Ook dit stond eerder anders in deze documentatie.** Het hoofdstuk
> [Node Types](../../gebruik/node-types.md) sprak van een "Ultra-licentie".
> Die term komt in de firmware en in de officiële documentatie niet voor en
> is vervangen door wat de FAQ beschrijft.

## Bronnen

- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
- [MeshCore firmware — `docs/payloads.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/payloads.md)
- [MeshCore firmware — `docs/faq.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/faq.md)
