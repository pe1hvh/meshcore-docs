# Inloggen en de ACL

*ANON_REQ · DRIE WACHTWOORDPADEN · PERMISSIES · WAT EEN HERSTART OVERLEEFT*

Een room server accepteert niets van een onbekende. Voordat een client mag
posten of iets mag opvragen, moet hij zich melden met een wachtwoord — en het
wachtwoord dat hij invult bepaalt niet of hij binnenkomt, maar *als wat*. Dit
hoofdstuk volgt dat inlogpakket van de eerste byte tot de rechten die de
server eraan hangt, en laat zien welk deel van dat lidmaatschap een herstart
niet overleeft.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `examples/simple_room_server/MyMesh.cpp`, `src/helpers/ClientACL.h`,
> `src/helpers/ClientACL.cpp`, `src/helpers/BaseChatMesh.cpp`,
> `src/helpers/CommonCLI.cpp`, en de officiële `docs/payloads.md` en
> `docs/cli_commands.md`. De tellingen over `ROOM_PASSWORD` komen uit
> [`tools/room-server-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/room-server-overview.py).

## Het inlogpakket

Inloggen gebeurt met `PAYLOAD_TYPE_ANON_REQ`: een datagram waarin de afzender
zijn volledige publieke sleutel meestuurt, omdat de server hem nog niet kent.
De klaartekst binnen dat pakket is voor een room server anders dan voor een
repeater of sensor — er zit een veld extra in.

| Veld | Grootte | Waarde in het voorbeeld |
|---|---|---|
| tijdstempel | 4 | `C0 3C 6B 6A` (1785412800) |
| `sync_since` | 4 | `00 00 00 00` (eerste keer inloggen) |
| wachtwoord | rest | `68 65 6C 6C 6F` (`hello`) |

Het tweede veld is het interessante. `sync_since` is de tijdstempel van de
laatste post die deze client al heeft; de server gebruikt hem als startpunt
en stuurt alleen wat daarna is gepost. Bij een repeater of sensor ontbreekt
dat veld en begint het wachtwoord direct na de tijdstempel.

`src/helpers/BaseChatMesh.cpp` r.565-572

```cpp
    uint32_t now = getRTCClock()->getCurrentTimeUnique();
    memcpy(temp, &now, 4);   // mostly an extra blob to help make packet_hash unique
    if (recipient.type == ADV_TYPE_ROOM) {
      memcpy(&temp[4], &recipient.sync_since, 4);
      int len = strlen(password); if (len > 15) len = 15;  // max 15 chars currently
      memcpy(&temp[8], password, len);
      tlen = 8 + len;
    } else {
```

Een wachtwoord is dus maximaal 15 tekens. De client kapt langere invoer af
zonder er iets over te zeggen; wie een langer wachtwoord instelt op de server
kan er daarna niet meer op inloggen.

## De drie paden

De server loopt vier tests af, in vaste volgorde. De eerste is een
kortsluiting voor wie al bekend is; de andere drie bepalen de rechten van een
nieuwe client.

![Beslisboom van het inloggen: leeg wachtwoord met bekende publieke sleutel,
adminwachtwoord, gastwachtwoord, read-only-vlag, en anders geen
antwoord](../../../images/nl/room-server-login-1.svg)

`examples/simple_room_server/MyMesh.cpp` r.329-342

```cpp
    if (client == NULL) {
      uint8_t perm;
      if (strcmp((char *)&data[8], _prefs.password) == 0) { // check for valid admin password
        perm = PERM_ACL_ADMIN;
      } else {
        if (strcmp((char *)&data[8], _prefs.guest_password) == 0) {   // check the room/public password
          perm = PERM_ACL_READ_WRITE;
        } else if (_prefs.allow_read_only) {
          perm = PERM_ACL_GUEST;
        } else {
          MESH_DEBUG_PRINTLN("Incorrect room password");
          return; // no response. Client will timeout
        }
      }
```

Die laatste `return` is het opvallendste gedrag in dit hoofdstuk: bij een
verkeerd wachtwoord stuurt de server **niets** terug. Geen foutmelding, geen
weigering, geen enkel pakket. De client blijft wachten tot zijn eigen timeout
afloopt en meldt dan dat de server niet reageert. Voor de gebruiker is een
tikfout in het wachtwoord dus niet te onderscheiden van een server die buiten
bereik is.

> [!NOTE]
> **Dat is een bewuste keuze en geen bug.** Een server die "verkeerd
> wachtwoord" zou antwoorden, bevestigt aan iedereen die het probeert dat er
> een room server op die sleutel luistert, en maakt het uitproberen van
> wachtwoorden goedkoop. Stilte dwingt een aanvaller tot een volledige
> timeout per poging.

## Wat de wachtwoorden zijn

| Instelling | CLI | Build-vlag | Standaard |
|---|---|---|---|
| beheerder | `set password` | `ADMIN_PASSWORD` | `password` |
| deelnemer | `set guest.password` | `ROOM_PASSWORD` | leeg in de code, `hello` in de varianten |
| meeleesrecht zonder wachtwoord | `set allow.read.only` | — | `off` |

De standaardwaarde van het deelnemerswachtwoord verdient toelichting, omdat
de firmware en de varianten iets anders zeggen. In `CommonCLI.h` is
`guest_password` een leeg veld; de varianten zetten hem via een build-vlag.
Van de 79 variantmappen zetten er 59 regels `ROOM_PASSWORD` op `hello`, en in
één variant (`gat562_mesh_watch13`) staat die regel uitgecommentarieerd. Een
room server die je van de flasher haalt, heeft dus vrijwel zeker `hello` als
deelnemerswachtwoord en `password` als beheerderswachtwoord.

> [!WARNING]
> **Beide standaardwachtwoorden staan publiek in de broncode.** Zolang je ze
> niet verandert, kan iedereen die het weet meelezen én posten, en met
> `password` ook je node herconfigureren en je zendvermogen aanpassen. Zet ze
> om vóór de node de lucht in gaat.

## De permissies

`src/helpers/ClientACL.h` r.7-11

```cpp
#define PERM_ACL_ROLE_MASK     3   // lower 2 bits
#define PERM_ACL_GUEST         0
#define PERM_ACL_READ_ONLY     1
#define PERM_ACL_READ_WRITE    2
#define PERM_ACL_ADMIN         3
```

| Waarde | Rol | Mag posten | Mag CLI | Mag access list |
|---|---|---|---|---|
| 0 | `GUEST` | nee | nee | nee |
| 1 | `READ_ONLY` | — | — | — |
| *2* | *`READ_WRITE`* | *ja* | *nee* | *nee* |
| 3 | `ADMIN` | ja | ja | ja |

De rij met waarde 1 is leeg omdat de room server die rol nergens toekent. Het
meeleesrecht dat `allow.read.only` inschakelt levert `PERM_ACL_GUEST` op —
waarde 0, niet 1. `PERM_ACL_READ_ONLY` wordt in de hele firmware maar op één
plek gebruikt, in `examples/simple_sensor/SensorMesh.cpp` r.189, en dan nog
als ondergrens in een vergelijking. Voor een room server is de rol dus een
gereserveerd nummer zonder gedrag.

Alleen de onderste twee bits van `permissions` zijn de rol; de bovenste zes
zijn vrij en worden bij een sensor gebruikt als masker voor welke meetwaarden
een client mag zien.

## Het antwoord op een geslaagde login

Dertien bytes, en drie ervan dragen sporen van een oudere protocolversie.

`examples/simple_room_server/MyMesh.cpp` r.368-377

```cpp
    uint32_t now = getRTCClock()->getCurrentTimeUnique();
    memcpy(reply_data, &now, 4); // response packets always prefixed with timestamp
    // TODO: maybe reply with count of messages waiting to be synced for THIS client?
    reply_data[4] = RESP_SERVER_LOGIN_OK;
    reply_data[5] = 0; // Legacy: was recommended keep-alive interval (secs / 16)
    reply_data[6] = (client->isAdmin() ? 1 : (client->permissions == 0 ? 2 : 0));
    // LEGACY: reply_data[7] = getUnsyncedCount(client);
    reply_data[7] = client->permissions; // NEW
    getRNG()->random(&reply_data[8], 4);   // random blob to help packet-hash uniqueness
    reply_data[12] = FIRMWARE_VER_LEVEL;  // New field
```

| Byte | Inhoud |
|---|---|
| 0-3 | tijdstempel van de server |
| 4 | `RESP_SERVER_LOGIN_OK` (0) |
| 5 | altijd 0 — was het aanbevolen keep-alive-interval |
| 6 | 1 voor een beheerder, 2 voor een gast, 0 voor de rest |
| 7 | de permissiebyte — was het aantal wachtende posts |
| 8-11 | vier willekeurige bytes, zodat de pakkethash uniek is |
| 12 | `FIRMWARE_VER_LEVEL` (1) |

Byte 7 is het punt om op te letten bij versieverschillen. Tot deze wijziging
stond daar het aantal posts dat nog voor deze client klaarstond; nu staan er
de rechten. Een oudere client leest dat getal nog steeds als een teller en
denkt dus dat er drie berichten klaarstaan wanneer hij als `ADMIN` inlogt.
Waar die teller nu wél te vinden is, staat in
[Requests en CLI](requests-and-cli.md).

## Wat een herstart overleeft

De ACL staat op het filesystem, maar niet in zijn geheel. Bij het opslaan
gaat er een filter overheen:

`examples/simple_room_server/MyMesh.cpp` r.942-944

```cpp
bool MyMesh::saveFilter(ClientInfo* client) {
  return client->isAdmin();    // only save Admins
}
```

Alleen beheerders worden weggeschreven. Een deelnemer met `READ_WRITE`
bestaat na een herstart niet meer voor de server — inclusief zijn
`sync_since`, zijn bekende pad en zijn gedeelde geheim. Hij moet opnieuw
inloggen, en omdat zijn client zijn eigen `sync_since` wél heeft bewaard,
stuurt die de juiste waarde mee en gaat de synchronisatie daarna gewoon
verder. Wat verdwenen is, zijn de posts zelf; zie
[Posts en synchronisatie](posts-and-sync.md).

`ClientACL::applyPermissions()` weigert bovendien een gastrol op te slaan
(`src/helpers/ClientACL.cpp` r.123), zodat een `setperm … 0` een contact
effectief uit het bestand haalt in plaats van hem met rechten 0 te bewaren.

De tabel heeft standaard 20 plaatsen (`MAX_CLIENTS` in
`src/helpers/ClientACL.h` r.37) en geen enkele variant zet die waarde anders.
Er is geen mechanisme dat oude clients opruimt om plaats te maken; wat er
gebeurt als de tabel vol zit, staat in
[Grenzen en open einden](limits-and-todos.md).

## Bescherming tegen herhaling

Elke client heeft een `last_timestamp`: de hoogste tijdstempel die de server
ooit van hem zag. Een inlogpakket met een tijdstempel dat daar niet boven
ligt wordt weggegooid met de melding `possible replay attack!`
(`examples/simple_room_server/MyMesh.cpp` r.345-347). Wie een opgenomen
inlogpakket opnieuw uitzendt, komt daar dus niet mee binnen.

De keerzijde is dat de klok van de client ertoe doet. Een client met een klok
die ver vooruit loopt zet `last_timestamp` op een waarde in de toekomst;
daarna wordt alles wat hij met de goede tijd stuurt geweigerd tot de echte
tijd die waarde heeft ingehaald. De officiële FAQ noemt precies dit als
oorzaak wanneer een node "vele dagen geleden voor het laatst gezien" lijkt.

## Bronnen

- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore firmware — `src/helpers/ClientACL.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.cpp)
- [MeshCore firmware — `src/helpers/BaseChatMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/BaseChatMesh.cpp)
- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `docs/payloads.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/payloads.md)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
