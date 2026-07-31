# Verantwoordelijkheden

*NODE · APP · OPSLAG · WACHTRIJ · WAT VERLOREN GAAT*

De node en de app bewaren allebei iets, en het is geen willekeurige
verdeling. De node houdt wat hij nodig heeft om zonder telefoon te blijven
werken; de app houdt alles wat groeit. Wie die grens verkeerd trekt, bouwt
een client die berichten kwijtraakt.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `examples/companion_radio/MyMesh.h`,
> `examples/companion_radio/MyMesh.cpp` en
> `examples/companion_radio/DataStore.h`. De verdeling van de grenswaarden
> over de compilatiedoelen komt uit `tools/companion-opcodes.py`.

![De node bewaart identiteit, voorkeuren, contacten, kanaalplaatsen en een
berichtenwachtrij; de app bewaart de volledige historie en de koppeling
tussen kanaal en verspreidingsgebied](../../../images/nl/companion-responsibilities-1.svg)

## Wat de node bewaart

`DataStore` is de enige plek waar de firmware naar het bestandssysteem
schrijft. De klasse noemt precies vijf soorten gegevens:

`examples/companion_radio/DataStore.h` r.34-40

```cpp
  bool loadMainIdentity(mesh::LocalIdentity &identity);
  bool saveMainIdentity(const mesh::LocalIdentity &identity);
  void loadPrefs(NodePrefs& prefs, double& node_lat, double& node_lon);
  void savePrefs(const NodePrefs& prefs, double node_lat, double node_lon);
  void loadContacts(DataStoreHost* host);
  void saveContacts(DataStoreHost* host, bool (*filter)(const ContactInfo& c) = NULL);
  void loadChannels(DataStoreHost* host);
```

Identiteit, voorkeuren, contacten en kanalen. Meer niet — er is geen
`loadMessages()`, en dat is geen omissie maar het ontwerp.

## De maximale aantallen verschillen per firmwarevariant

De omvang ligt vast bij het compileren. Het zijn dus wel degelijk constanten,
maar hun waarde verschilt per firmwarevariant: de waarde in de header is
meestal **niet** de waarde die op het apparaat draait. `MyMesh.h` zet ze
achter `#ifndef`, zodat een compilatieoptie (*build flag*) ze overschrijft:

`examples/companion_radio/MyMesh.h` r.58-64

```cpp
#ifndef MAX_CONTACTS
#define MAX_CONTACTS 100
#endif

#ifndef OFFLINE_QUEUE_SIZE
#define OFFLINE_QUEUE_SIZE 16
#endif
```

Over de 174 compilatiedoelen (*build targets*) die
`examples/companion_radio` compileren, ziet de werkelijke verdeling er zo
uit:

| Constante | In de header | In de compilatiedoelen |
|---|---|---|
| `MAX_CONTACTS` | 100 | 350 (151×), 160 (12×), 100 (8×), 300 (3×) |
| `OFFLINE_QUEUE_SIZE` | 16 | 256 (113×), 128 (10×), niet gezet en dus 16 (51×) |
| `MAX_GROUP_CHANNELS` | staat er niet | 40 (154×), 8 (20×) |

Voor een app betekent dat één ding: **lees de grenzen uit het antwoord op
`CMD_DEVICE_QUERY` en neem ze nooit uit de broncode over.** Zie
[Het interactiemodel](interaction-model.md).

> [!WARNING]
> **Het aantal contacten staat gehalveerd in het frame.** De firmware
> verstuurt `MAX_CONTACTS / 2`, niet de waarde zelf. Een node met ruimte voor
> 350 contacten zet dus 175 in het antwoord op `CMD_DEVICE_QUERY`, en de app
> moet dat getal verdubbelen: 175 × 2 = 350. Een app die het frame
> letterlijk overneemt, denkt dat er half zoveel contacten in passen als er
> werkelijk passen.

## Wat de app bewaart

Alles wat groeit, en alles wat de firmware niet nodig heeft om te
functioneren:

- de volledige berichthistorie, per contact en per kanaal
- bij welk kanaal welk verspreidingsgebied (*scope*) hoort — de firmware
  kent die koppeling niet en verwacht dat de app het juiste gebied instelt
  vóór het verzenden; zie
  [Regio's en Scopes](../../techniek/regions-and-scopes.md)
- eigen namen, groepering, favorieten en leesstatus
- welke berichten al opgehaald waren toen de verbinding wegviel

## De wachtrij is een doorgeefbuffer

Een doorgeefbuffer is tijdelijke opslag: wat erin staat blijft er alleen tot
het is opgehaald, en verdwijnt daarna. `offline_queue` is de enige plek waar
de node een binnengekomen bericht bewaart tot de app het ophaalt. Loopt hij
vol, dan gooit de firmware het oudste **kanaalbericht** weg om ruimte te
maken:

`examples/companion_radio/MyMesh.cpp` r.219-232

```cpp
void MyMesh::addToOfflineQueue(const uint8_t frame[], int len) {
  if (offline_queue_len >= OFFLINE_QUEUE_SIZE) {
    MESH_DEBUG_PRINTLN("WARN: offline_queue is full!");
    int pos = 0;
    while (pos < offline_queue_len) {
      if (offline_queue[pos].isChannelMsg()) {
        for (int i = pos; i < offline_queue_len - 1; i++) { // delete oldest channel msg from queue
          offline_queue[i] = offline_queue[i + 1];
        }
        MESH_DEBUG_PRINTLN("INFO: removed oldest channel message from queue.");
        offline_queue[offline_queue_len - 1].len = len;
        memcpy(offline_queue[offline_queue_len - 1].buf, frame, len);
        return;
      }
```

Staan er alleen directe berichten in, dan loopt de lus af zonder iets te
verwijderen, meldt de firmware `no channel messages to remove from queue`,
en keert de functie terug zónder het nieuwe bericht op te slaan. Het is dus
niet zo dat het oudste bericht altijd wijkt: **directe berichten worden
nooit weggegooid, maar een nieuw bericht gaat verloren zodra de wachtrij
vol staat met directe berichten.**

Voor een client betekent dat één regel: haal de wachtrij leeg zodra het
kan, en verlaat je niet op de node als opslag.

## Gevolgen voor het ontwerp van een app

| Aanname | Klopt niet, omdat |
|---|---|
| "De node bewaart mijn gesprekken" | er is geen berichtenopslag, alleen een wachtrij |
| "Ik kan de app opnieuw installeren en alles terughalen" | de historie stond alleen in de app |
| "Twee apps op dezelfde node zien hetzelfde" | wie het eerst synchroniseert, leegt de wachtrij |
| "40 kanalen kan altijd" | het zijn er 8 of 40, afhankelijk van de firmwarevariant |
| "De node weet bij welk verspreidingsgebied mijn kanaal hoort" | die koppeling zit alleen in de app |

Dat voorlaatste punt is de reden dat twee gelijktijdige clients op één node
elkaar in de weg zitten. Zie
[De drie transporten](../technisch/transports.md) voor wat de transporten
daar wel en niet tegen doen.

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`examples/companion_radio/DataStore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/DataStore.h)
  — wat er naar het bestandssysteem gaat
- [`examples/companion_radio/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.h)
  — `MAX_CONTACTS` en `OFFLINE_QUEUE_SIZE`, allebei achter `#ifndef`
- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.cpp)
  — `addToOfflineQueue()` en `getFromOfflineQueue()`

Reproductie:

- `tools/companion-opcodes.py` — telt de compilatiedoelen voor de companion
  en de verdeling van `MAX_CONTACTS`, `OFFLINE_QUEUE_SIZE` en
  `MAX_GROUP_CHANNELS` daarover

**Meetmethode.** Het script telt een `[env:…]` als companion wanneer
`build_src_filter` `../examples/companion_radio` bevat, met `extends` en
`${sectie.optie}` opgelost. Het aantal van 174 komt overeen met
`tools/design-overview.py`, dat op dezelfde manier telt.

Verwante hoofdstukken:

- [Het interactiemodel](interaction-model.md) — hoe de wachtrij geleegd
  wordt
- [Informatiemodel](information-model.md) — welke gegevens er precies zijn
- [Regio's en Scopes](../../techniek/regions-and-scopes.md) — de koppeling
  die de app moet bijhouden
