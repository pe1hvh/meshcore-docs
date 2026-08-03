# Posts en synchronisatie

*CYCLISCHE WACHTRIJ · SIGNED PLAIN · ACK-HASH · SYNC_SINCE*

Een room server duwt, hij levert niet uit op verzoek. Hij houdt per client
één tijdstempel bij — hoe ver die client is — en werkt zijn deelnemers in een
vaste ronde af, één post per beurt, telkens wachtend op een
ontvangstbevestiging voordat de volgende mag. Dit hoofdstuk volgt een bericht
van het moment dat het binnenkomt tot het moment dat de teller van de
ontvanger opschuift, en rekent de bytes op de radio uit.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `examples/simple_room_server/MyMesh.h`,
> `examples/simple_room_server/MyMesh.cpp`, `src/Utils.cpp`,
> `src/helpers/TxtDataHelpers.h`, `src/helpers/BaseChatMesh.cpp`,
> `src/helpers/ClientACL.h`. Het uitgewerkte voorbeeld is te reproduceren met
> [`tools/room-server-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/room-server-overview.py).

## Van bericht naar post

Wat een client verstuurt is een gewoon tekstbericht: `PAYLOAD_TYPE_TXT_MSG`
met vlaggen `TXT_TYPE_PLAIN`, precies zoals een direct message. De server
kijkt naar de rechten van de afzender en beslist wat ermee gebeurt.

| Rol van de afzender | Wat de server doet |
|---|---|
| `GUEST` (0) | niets — geen post, geen antwoord, en ook geen ACK |
| `READ_WRITE` (2) | post toevoegen en een ACK sturen |
| `ADMIN` (3) | post toevoegen en een ACK sturen |

Ook hier is stilte het antwoord op een weigering. Een gast die post ziet zijn
bericht als niet-afgeleverd blijven staan, zonder uitleg.

`examples/simple_room_server/MyMesh.cpp` r.41-50

```cpp
void MyMesh::addPost(ClientInfo *client, const char *postData) {
  // TODO: suggested postData format: <title>/<descrption>
  posts[next_post_idx].author = client->id; // add to cyclic queue
  StrHelper::strncpy(posts[next_post_idx].text, postData, MAX_POST_TEXT_LEN);

  posts[next_post_idx].post_timestamp = getRTCClock()->getCurrentTimeUnique();
  next_post_idx = (next_post_idx + 1) % MAX_UNSYNCED_POSTS;

  next_push = futureMillis(PUSH_NOTIFY_DELAY_MILLIS);
  _num_posted++; // stats
}
```

Drie dingen om vast te houden. De post krijgt een tijdstempel van **de klok
van de server**, niet die van de afzender — dat maakt de volgorde tussen
posts betrouwbaar ook als clients hun tijd verkeerd hebben staan. De tekst
wordt afgekapt op `MAX_POST_TEXT_LEN`, dat is `(160-9)` en dus 151 tekens. En
`next_post_idx` loopt rond: post 33 overschrijft post 1, of die inmiddels
bij iedereen is aangekomen of niet.

`getCurrentTimeUnique()` garandeert bovendien dat twee posts binnen dezelfde
seconde toch verschillende tijdstempels krijgen. Dat is nodig omdat de
tijdstempel dienstdoet als volgnummer.

## De wachtrij

32 plaatsen (`MAX_UNSYNCED_POSTS`), een array in het werkgeheugen, en verder
niets. Er wordt nergens naar het filesystem geschreven: de enige bestanden
die een room server aanraakt zijn de ACL en het optionele pakketlogboek.

![Cyclische wachtrij met 32 plaatsen, per client een sync_since-tijdstempel,
en de lus duwen–ACK–tijdstempel opschuiven](../../../images/nl/room-server-sync-1.svg)

Per client staat er één tijdstempel tegenover die wachtrij: `sync_since`.
Alles met een hogere tijdstempel is nieuw voor hem, alles daaronder heeft hij
al gehad. Er is dus geen lijst van "wie heeft wat", alleen een grens per
client — 4 bytes per deelnemer in plaats van een matrix van 32 × 20 bits.

De selectie van de volgende post gebeurt met drie voorwaarden tegelijk:

`examples/simple_room_server/MyMesh.cpp` r.966-976

```cpp
      for (int k = 0, idx = next_post_idx; k < MAX_UNSYNCED_POSTS; k++) {
        auto p = &posts[idx];
        if (now >= p->post_timestamp + POST_SYNC_DELAY_SECS &&
            p->post_timestamp > client->extra.room.sync_since // is new post for this Client?
            && !p->author.matches(client->id)) {   // don't push posts to the author
          // push this post to Client, then wait for ACK
          pushPostToClient(client, *p);
          did_push = true;
          MESH_DEBUG_PRINTLN("loop - pushed to client %02X: %s", (uint32_t)client->id.pub_key[0], p->text);
          break;
        }
```

De lus begint bij `next_post_idx` en niet bij 0, dus bij de oudste plaats in
de ring — de posts komen in de volgorde waarin ze zijn geplaatst. De drie
voorwaarden zijn: de post is minstens 6 seconden oud
(`POST_SYNC_DELAY_SECS`), de post is nieuw voor deze client, en **de auteur
krijgt zijn eigen post niet terug**.

Waaróm die zes seconden er zijn, zegt de firmware niet — er staat geen
commentaar bij de constante. Het effect is dat de server niet begint te duwen
terwijl de ACK naar de plaatser nog onderweg is, maar dat is een
interpretatie en geen vastgelegde bedoeling.

Dat laatste heeft een gevolg dat in de praktijk verwarring geeft: je ziet je
eigen bijdrage niet terugkomen van de server. Je client toont hem omdat hij
hem zelf heeft verstuurd, niet omdat de room hem heeft bevestigd. Verdwijnt
je post ergens onderweg, dan merk je dat alleen aan het uitblijven van de
ACK.

## Het pakket dat de server stuurt

`examples/simple_room_server/MyMesh.cpp` r.53-68

```cpp
void MyMesh::pushPostToClient(ClientInfo *client, PostInfo &post) {
  int len = 0;
  memcpy(&reply_data[len], &post.post_timestamp, 4);
  len += 4; // this is a PAST timestamp... but should be accepted by client

  uint8_t attempt;
  getRNG()->random(&attempt, 1); // need this for re-tries, so packet hash (and ACK) will be different
  reply_data[len++] = (TXT_TYPE_SIGNED_PLAIN << 2) | (attempt & 3); // 'signed' plain text

  // encode prefix of post.author.pub_key
  memcpy(&reply_data[len], post.author.pub_key, 4);
  len += 4; // just first 4 bytes

  int text_len = strlen(post.text);
  memcpy(&reply_data[len], post.text, text_len);
  len += text_len;
```

De klaartekst is dus vier velden:

| Veld | Grootte | Betekenis |
|---|---|---|
| `post_timestamp` | 4 | tijdstempel van de post, LSB eerst — een tijdstip in het verleden |
| vlaggen | 1 | `TXT_TYPE_SIGNED_PLAIN` (2) in de bovenste zes bits, pogingnummer in de onderste twee |
| auteursprefix | 4 | de eerste vier bytes van de publieke sleutel van wie de post plaatste |
| tekst | rest | maximaal 151 tekens |

Het auteursveld is waarom dit type "signed plain" heet. Bij een gewoon direct
bericht weet je wie de afzender is omdat het pakket van hem komt; hier komt
het pakket van de server, en zonder dit veld zou elke post er hetzelfde
uitzien. Vier bytes is genoeg om de auteur in je contactenlijst op te zoeken,
en te weinig om als bewijs te dienen: het is een aanwijzing, geen
handtekening. Wie de server beheert, kan er zetten wat hij wil.

De onderste twee bits van de vlaggenbyte zijn puur toeval — `getRNG()` vult
ze. Ze staan er omdat een herhaalde poging anders byte voor byte gelijk zou
zijn aan de vorige, dezelfde pakkethash zou krijgen en door het netwerk als
duplicaat zou worden weggegooid.

## De verwachte ACK

De server berekent vooraf welke bevestiging hij terug wil zien:

`examples/simple_room_server/MyMesh.cpp` r.70-72

```cpp
  // calc expected ACK reply
  mesh::Utils::sha256((uint8_t *)&client->extra.room.pending_ack, 4, reply_data, len, client->id.pub_key, PUB_KEY_SIZE);
  client->extra.room.push_post_timestamp = post.post_timestamp;
```

Dat is SHA-256 over de klaartekst gevolgd door de publieke sleutel van de
ontvanger, afgekapt op vier bytes (`src/Utils.cpp` r.23-28). De client
berekent bij ontvangst hetzelfde en stuurt de uitkomst terug. Er wordt dus
niets opgezocht en niets meegestuurd: beide kanten reproduceren dezelfde
waarde uit gegevens die ze allebei al hebben. Dezelfde constructie als bij de
transportcodes in [Regio's en Scopes](../regions-and-scopes.md).

### Uitgewerkt

Met de projectvoorbeelden: `PE1RDP` post
`"Op Woensdag a.s. Blauwvingerdagen"` om `1785412800`, en de server duwt hem
naar `PE1HVH`.

```text
post_timestamp   1785412800        C0 3C 6B 6A
vlaggen          (2 << 2) | 0      08
auteursprefix    PE1RDP            E3 A0 31 3A
tekst            33 tekens         4F 70 20 57 6F 65 6E 73 64 61 67 …

klaartekst (42 bytes)
C0 3C 6B 6A 08 E3 A0 31 3A 4F 70 20 57 6F 65 6E 73 64 61 67 20 61 2E 73 2E
20 42 6C 61 75 77 76 69 6E 67 65 72 64 61 67 65 6E

verwachte ACK    88 C5 39 94   ->  0x9439C588
```

> [!NOTE]
> **De publieke sleutels zijn voorbeeldwaarden.** Ze komen uit dezelfde
> afspraak als in `tools/dm-example.py`: `sha256("voorbeeld public key
> PE1HVH")`. Een echte sleutel komt van het apparaat en is niet uit publieke
> gegevens te reproduceren. Alles daarna — de opbouw van de klaartekst en de
> ACK-berekening — is exact het firmwarepad.

Van de 151 beschikbare tekens gebruikt dit voorbeeld er 33. De payload van 42
bytes gaat daarna nog door de versleuteling en krijgt de gewone
pakketheaders; hoe dat eruitziet staat in
[Pakketstructuur](../packet-structure.md).

## De teller schuift pas op bij de ACK

`examples/simple_room_server/MyMesh.cpp` r.104-115

```cpp
bool MyMesh::processAck(const uint8_t *data) {
  for (int i = 0; i < acl.getNumClients(); i++) {
    auto client = acl.getClientByIdx(i);
    if (client->extra.room.pending_ack && memcmp(data, &client->extra.room.pending_ack, 4) == 0) { // got an ACK from Client!
      client->extra.room.pending_ack = 0; // clear this, so next push can happen
      client->extra.room.push_failures = 0;
      client->extra.room.sync_since = client->extra.room.push_post_timestamp; // advance Client's SINCE timestamp, to sync next post
      return true;
    }
  }
  return false;
}
```

Dit is de kern van de betrouwbaarheid. `sync_since` gaat alleen omhoog
wanneer de bevestiging binnen is. Gaat de post onderweg verloren, dan blijft
de teller staan en wordt dezelfde post opnieuw aangeboden. De server hoeft
daarvoor niets extra's bij te houden: de teller *is* de administratie.

Merk op dat de zoektocht over álle clients loopt en op de vier bytes matcht.
Twee clients die toevallig dezelfde verwachte ACK hebben, zouden elkaars
bevestiging kunnen opeisen. Omdat de publieke sleutel van de client in de
hash zit, is dat alleen mogelijk bij een echte hashbotsing op 32 bits.

## Timing

| Constante | Waarde | Wat het regelt |
|---|---|---|
| `PUSH_NOTIFY_DELAY_MILLIS` | 2000 ms | wachten na een nieuwe post voordat de ronde weer loopt |
| `POST_SYNC_DELAY_SECS` | 6 s | minimumleeftijd van een post voordat hij geduwd wordt |
| `SYNC_PUSH_INTERVAL` | 1200 ms | tussen twee geduwde posts |
| `SYNC_PUSH_INTERVAL / 8` | 150 ms | naar de volgende client als er niets te duwen was |
| `PUSH_ACK_TIMEOUT_FLOOD` | 12000 ms | wachttijd op een ACK als het pad onbekend is |
| `PUSH_TIMEOUT_BASE` | 4000 ms | basiswachttijd bij een bekend pad |
| `PUSH_ACK_TIMEOUT_FACTOR` | 2000 ms | daar bovenop, per hop in het pad |

De ronde is round robin: per doorgang van de hoofdlus komt één client aan de
beurt, en alleen die client. Een deelnemer met veel achterstand houdt de
anderen dus niet op, maar loopt zelf ook niet snel bij — bij twintig actieve
deelnemers zit er in het ongunstigste geval zo'n 24 seconden tussen twee van
jouw beurten; zijn de meesten bij, dan zakt dat naar enkele seconden omdat
een lege beurt maar 150 ms duurt.

Overgeslagen worden clients die nog op een ACK wachten, clients die nooit
actief zijn geweest, en clients met drie mislukte pogingen op rij. Die laatste
drempel is hard: na `push_failures == 3` krijgt een client niets meer, en de
enige manier om dat te herstellen is dat hij zelf iets stuurt. Elk bericht,
elke keep-alive en elk request zet de teller terug op nul.

## Wat een client ermee doet

Aan de andere kant houdt `BaseChatMesh` dezelfde teller bij, maar dan
voorzichtiger:

`src/helpers/BaseChatMesh.cpp` r.253-258

```cpp
    } else if (flags == TXT_TYPE_SIGNED_PLAIN) {
      if (timestamp > from.sync_since) {  // make sure 'sync_since' is up-to-date
        from.sync_since = timestamp;
      }
      from.lastmod = getRTCClock()->getCurrentTime(); // update last heard time
      onSignedMessageRecv(from, packet, timestamp, &data[5], (const char *) &data[9]);  // let UI know
```

De client schuift zijn eigen `sync_since` op zodra hij de post heeft
verwerkt, en stuurt die waarde mee bij de volgende login en bij elke
keep-alive. Daardoor kan de synchronisatie doorlopen nadat de server de
client is kwijtgeraakt — bijvoorbeeld na een herstart, waarbij alleen
beheerders bewaard blijven (zie
[Inloggen en de ACL](login-and-acl.md)). De client vertelt de server dan
opnieuw waar hij gebleven was.

Wat níet doorloopt zijn de posts zelf. Die stonden in RAM en zijn na de
herstart weg; de teller wijst dan naar een grens in een lege wachtrij.

## Bronnen

- [MeshCore firmware — `examples/simple_room_server/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `src/Utils.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Utils.cpp)
- [MeshCore firmware — `src/helpers/TxtDataHelpers.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/TxtDataHelpers.h)
- [MeshCore firmware — `src/helpers/BaseChatMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/BaseChatMesh.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore firmware — `docs/payloads.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/payloads.md)
