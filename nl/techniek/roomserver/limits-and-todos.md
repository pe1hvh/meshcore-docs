# Grenzen en open einden

*WAT WEG IS · WAT VOL LOOPT · WAT ER LETTERLIJK ALS TODO IN STAAT*

Dit hoofdstuk verzamelt wat de room server níet doet. Niet als kritiek — de
firmware is klein en doet zijn werk — maar omdat een aantal van die grenzen
haaks staat op wat gebruikers verwachten, en omdat de auteurs een deel ervan
zelf hebben opgeschreven in de code. Acht `TODO`- en `REVISIT`-regels staan
in `MyMesh.cpp`; ze worden hieronder allemaal genoemd.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `examples/simple_room_server/MyMesh.h`,
> `examples/simple_room_server/MyMesh.cpp`, `src/helpers/ClientACL.h`,
> `src/helpers/ClientACL.cpp`, en de officiële `docs/faq.md`. De controle op
> variantoverrides komt uit
> [`tools/room-server-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/room-server-overview.py).

## Niets van de inhoud overleeft een herstart

De wachtrij is een array in het werkgeheugen. Er is geen enkele plek in
`MyMesh.cpp` waar posts naar het filesystem gaan; de enige bestanden die de
room server aanmaakt zijn de ACL en het optionele pakketlogboek. Een reset,
een lege accu of een `reboot`-commando wist alle 32 plaatsen.

Dat betekent ook dat het inhalen van een achterstand na een serverherstart
niet gebeurt. De clients weten nog waar ze gebleven waren en sturen hun
`sync_since` netjes mee, maar de server heeft niets meer om tegenover die
grens te zetten. Er komt geen foutmelding: alles is bij, want er is niets.

> [!WARNING]
> **Behandel een room server niet als archief.** Wie het gesprek wil bewaren,
> bewaart het op de client. De server is bedoeld om enkele uren tot dagen te
> overbruggen, niet om geschiedenis vast te houden.

## De wachtrij loopt over zonder waarschuwing

32 plaatsen, cyclisch. `next_post_idx` loopt rond en overschrijft de oudste
plaats, ongeacht of die post al bij iedereen is aangekomen. De naam
`MAX_UNSYNCED_POSTS` suggereert dat het om ónbevestigde posts gaat, maar er
wordt bij het toevoegen nergens gekeken of de plaats die wordt overschreven
al is afgeleverd.

Praktisch gevolg: een deelnemer die langer wegblijft dan 32 posts kan posts
overslaan zonder dat iemand dat merkt. Zijn `sync_since` springt bij de
volgende bevestiging gewoon naar de tijdstempel van de post die hij wél
kreeg; wat daartussen zat is nooit verstuurd en wordt nooit gemist.

Geen enkele variant zet `MAX_UNSYNCED_POSTS` of `MAX_CLIENTS` op een andere
waarde — de firmware is op alle 73 room-server-build-targets gelijk wat deze
twee grenzen betreft. Wie meer wil, compileert zelf.

## De clienttabel verdringt de stilste deelnemer

`MAX_CLIENTS` is 20. Loopt de tabel vol, dan gooit `putClient()` er iemand
uit om plaats te maken:

`src/helpers/ClientACL.cpp` r.97-113

```cpp
ClientInfo* ClientACL::putClient(const mesh::Identity& id, uint8_t init_perms) {
  uint32_t min_time = 0xFFFFFFFF;
  ClientInfo* oldest = &clients[MAX_CLIENTS - 1];
  for (int i = 0; i < num_clients; i++) {
    if (id.matches(clients[i].id)) return &clients[i];  // already known
    if (!clients[i].isAdmin() && clients[i].last_activity < min_time) {
      oldest = &clients[i];
      min_time = oldest->last_activity;
    }
  }

  ClientInfo* c;
  if (num_clients < MAX_CLIENTS) {
    c = &clients[num_clients++];
  } else {
    c = oldest;  // evict least active contact
  }
```

De langst inactieve niet-beheerder wordt overschreven. Dat is redelijk
gedrag, maar het is stil: de verdrongen deelnemer krijgt geen melding en
merkt het pas doordat de server hem niets meer stuurt. Hij komt er weer in
door opnieuw in te loggen — waarna hij op zijn beurt iemand anders verdringt.
Bij meer dan twintig actieve deelnemers gaat een room server dus rondzingen.

Eén randgeval verdient aandacht. `oldest` begint op de láátste plaats in de
tabel, en de lus vervangt die aanwijzer alleen door niet-beheerders. Zitten
alle twintig plaatsen vol met beheerders, dan blijft `oldest` op
`clients[19]` staan en wordt daar dus een **beheerder** overschreven. Dat is
niet uit te lokken door een buitenstaander — je moet eerst twintig
beheerderswachtwoorden hebben — maar het is wel het enige pad waarlangs een
beheerder uit de ACL verdwijnt zonder `setperm`.

## Na drie mislukte pogingen valt het stil

Een client waarvan drie duwpogingen op rij onbevestigd blijven, wordt
overgeslagen in de ronde. Er is geen herstelmechanisme aan de serverkant: de
teller gaat alleen terug naar nul wanneer de client zelf iets stuurt — een
post, een keep-alive of een request.

Voor een client die met keep-alives werkt is dat geen probleem. Voor een
client die dat niet doet en alleen luistert, wél: die valt na drie gemiste
duwpogingen permanent stil, ook als hij daarna weer prima bereikbaar is.

Daar hoort een tweede beperking bij, die de auteurs zelf hebben genoteerd:

`examples/simple_room_server/MyMesh.cpp` r.955

```cpp
        c->extra.room.pending_ack = 0; // reset  (TODO: keep prev expected_ack's in a list, incase they arrive LATER, after we retry)
```

Een ACK die ná de timeout binnenkomt wordt niet meer herkend. De server heeft
de verwachte waarde weggegooid en telt de poging als mislukt, terwijl het
bericht wél is aangekomen. Op trage paden met veel hops — waar de timeout
`4000 + 2000 × hops` milliseconden is — is dat een reëel scenario, en het
gevolg is dat dezelfde post nog eens wordt verstuurd.

## Keep-alives worden niet afgeknepen

`examples/simple_room_server/MyMesh.cpp` r.549-550

```cpp
        // TODO: Throttle KEEP_ALIVE requests!
        // if client sends too quickly, evict()
```

Er zit geen rem op. Een client die keep-alives in hoog tempo stuurt, wordt
elke keer beantwoord, en elk antwoord kost zendtijd op een band waar de duty
cycle telt. De bedoelde oplossing staat er letterlijk naast en is niet
gebouwd. Zie [Regelgeving & Duty Cycle](../../gebruik/regulations.md) voor
waarom dat meer dan een cosmetisch punt is.

Ook `onPeerPathRecv()` — de functie die een nieuw pad naar een client
opslaat — draagt een open einde: `// TODO: prevent replay attacks` op r.589.
Anders dan bij berichten en requests wordt de tijdstempel daar niet getoetst.

## Rollen en velden die niets doen

| Wat | Waar | Status |
|---|---|---|
| `PERM_ACL_READ_ONLY` (1) | `src/helpers/ClientACL.h` r.9 | gedefinieerd, door de room server nooit toegekend |
| byte 5 van het inlogantwoord | `MyMesh.cpp` r.372 | altijd 0, was het aanbevolen keep-alive-interval |
| `<titel>/<omschrijving>` in een post | `MyMesh.cpp` r.42 | als `TODO` genoteerd, niet geïmplementeerd |
| aantal wachtende posts in het inlogantwoord | `MyMesh.cpp` r.370 | als `TODO` genoteerd; zit nu in de keep-alive-ACK |

Het derde punt verklaart waarom posts in de praktijk ongestructureerd zijn.
De firmware kent geen onderwerp en geen indeling: een post is 151 tekens
platte tekst en verder niets. Afspraken daarover moet een room zelf maken.

## Doorsturen staat uit, en dat is met opzet

Een room server heeft `disable_fwd = 1` als standaard. Hij hoort dus wel al
het verkeer om zich heen, maar geeft niets door. Dat kan met `set repeat on`
worden aangezet, en de officiële FAQ raadt dat af: een room server met
doorsturen aan mist de volledige set repeaterfuncties en het beheer dat
daarbij hoort. De aanbeveling in de FAQ is om repeater en room server op
aparte apparaten te draaien.

Twee `REVISIT`-regels raken dit gebied. Op r.78 staat de vraag open met welke
padhash-grootte een post via flood moet worden verstuurd wanneer het pad naar
een client nog onbekend is; op r.719 of er een eigen regio voor de retourweg
in de transportcodes hoort. Beide gaan over routering en niet over de
roomfunctie zelf; zie [Regio's en Scopes](../regions-and-scopes.md) voor de
context.

## Wat dit betekent voor wie er een neerzet

- Reken op **enkele dagen** overbrugging, niet op geschiedenis.
- Houd de room onder de **twintig** actieve deelnemers, anders verdringen ze
  elkaar uit de tabel.
- Zet **beide wachtwoorden** om voordat de node de lucht in gaat.
- Laat de node **niet ook repeaten**; zet daar een tweede node voor neer.
- Verwacht geen **ledenlijst** en geen **moderatie**: er is één commando dat
  rechten zet, en verder niets.

## Bronnen

- [MeshCore firmware — `examples/simple_room_server/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore firmware — `src/helpers/ClientACL.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.cpp)
- [MeshCore firmware — `docs/faq.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/faq.md)
