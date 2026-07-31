# Informatiemodel

*GEGEVENSOBJECTEN · RELATIES · WAT VLUCHTIG IS EN WAT BLIJFT*

De componenten uit dit ontwerp wisselen een beperkt aantal gegevensobjecten
uit. Dit hoofdstuk beschrijft welke dat zijn, hoe ze zich tot elkaar
verhouden, en — de meest onderschatte vraag bij een node die op een batterij
draait — wat een herstart overleeft en wat niet.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — `src/Packet.h`, `src/Identity.h`,
> `src/Mesh.h`, `src/helpers/ClientACL.h` en `src/helpers/ContactInfo.h`.

## De objecten

![Zeven gegevensobjecten met hun relaties. Identiteit staat centraal: contact,
rechtenregel en de eigen node verwijzen er alle naar. Pakket staat apart en
draagt een pad; kanaal staat los van identiteit omdat groepsberichten niet aan
een afzender worden gebonden.](../../../images/nl/information-model-1.svg)

| Object | Wat het is | Blijft na herstart |
|---|---|---|
| Identiteit | Een publieke sleutel, en daarmee een partij wiens handtekening te controleren is | — |
| Eigen identiteit | De identiteit van deze node, met privésleutel | Ja |
| Pakket | De eenheid die over de lucht gaat | Nee |
| Pad | De reeks nodes waarlangs een pakket liep of moet lopen | Deels |
| Contact | Een bekende tegenpartij met naam, sleutel en laatst bekende pad | Ja |
| Kanaal | Een groep met een gedeeld geheim | Ja |
| Rechtenregel | Een bekende client met een rechtenniveau | Ja |
| Voorkeuren | De instellingen van deze node | Ja |

## Identiteit is de spil

Bijna alles hangt aan de identiteit. Het ontwerp maakt daarbij een onderscheid
dat overal doorwerkt: er is een identiteit waarvan je alleen de publieke
sleutel kent, en er is de eigen identiteit met het volledige sleutelpaar. Het
tweede is een uitbreiding van het eerste, niet iets anders.

Dat verschil is het enige wat ondertekenen scheidt van controleren. Elke node
kan een handtekening van elke andere node controleren; alleen de node zelf kan
ondertekenen.

Uit de publieke sleutel volgt ook de korte aanduiding waarmee een node in
pakketten wordt aangeduid. Die aanduiding is geen aparte berekening maar
simpelweg het begin van de sleutel:

`src/Identity.h` r.18-25

```cpp
  int copyHashTo(uint8_t* dest) const { 
    memcpy(dest, pub_key, PATH_HASH_SIZE);    // hash is just prefix of pub_key
    return PATH_HASH_SIZE;
  }
  int copyHashTo(uint8_t* dest, uint8_t len) const { 
    memcpy(dest, pub_key, len);    // hash is just prefix of pub_key
    return len;
  }
```

Dat heeft een gevolg dat je in het informatiemodel moet meenemen: de
aanduiding is één byte lang. Er zijn 256 mogelijke waarden, en in een netwerk
van enige omvang komen botsingen voor. Het ontwerp gaat daar expliciet mee om
door bij een botsing alle kandidaten te proberen in plaats van er één te
kiezen.

## Pakket en pad

Een pakket draagt zijn eigen route mee. Er is geen tabel waarin een node
opzoekt hoe hij ergens komt; het pad zit in het pakket of wordt gaandeweg
opgebouwd. Zie [Pakketstructuur](../../techniek/packet-structure.md) voor de
byte-indeling en [Route traceren](../../techniek/route-tracing.md) voor het
gedrag.

Voor het informatiemodel is één ding van belang: een pad is een eigenschap van
een verbinding tussen twee partijen, niet van het netwerk. Het wordt opgeslagen
bij het contact of bij de rechtenregel, en het kan verouderen zonder dat iemand
dat merkt tot een bericht niet aankomt.

## Vluchtig en blijvend in één object

De rechtenregel is het duidelijkste voorbeeld van een object dat beide bevat.
Wie erin staat, welke rechten die partij heeft en langs welk pad die te
bereiken is, blijft bewaard. Wanneer die partij voor het laatst iets van zich
liet horen, verdwijnt bij een herstart.

`src/helpers/ClientACL.h` r.15-24

```cpp
struct ClientInfo {
  mesh::Identity id;
  uint8_t permissions;
  uint8_t out_path_len;
  uint8_t out_path[MAX_PATH_SIZE];
  uint8_t shared_secret[PUB_KEY_SIZE];
  uint32_t last_timestamp;   // by THEIR clock  (transient)
  uint32_t last_activity;    // by OUR clock    (transient)
```

De aantekening `transient` in de broncode is de enige plek waar dat
onderscheid is vastgelegd. Voor wie het gedrag van een repeater na een
stroomstoring probeert te verklaren, is het de belangrijkste regel in het
bestand.

Het gedeelde geheim is een derde categorie: het wordt wel bewaard, maar het is
afgeleid en dus opnieuw te berekenen. Het staat er om rekentijd te sparen, niet
omdat het onmisbaar is.

## Grenzen

Het model heeft harde bovengrenzen, en die zijn niet groot. Ze staan hier
omdat ze het ontwerp bepalen, niet omdat ze toevallig zo zijn ingesteld.

| Grens | Standaardwaarde | Instelbaar per build |
|---|---|---|
| Bekende clients per node | 20 | Ja |
| Lengte van een pad | 64 stappen | Nee |
| Payload van een pakket | 184 bytes | Nee |
| Contacten in een companion radio | wisselt per bord | Ja |
| Kanalen in een companion radio | wisselt per bord | Ja |

De eerste is de meest voelbare: een repeater kent twintig clients, en de
eenentwintigste past er niet bij. Voor een repeater die als beheerd knooppunt
draait is dat ruim; voor een repeater in een druk gebied niet.

## Wat er niet in het model zit

Er is geen object voor een netwerk, een buurman of een verbinding. Een node
weet wie hij kent en welk pad daarheen liep, maar heeft geen voorstelling van
de topologie. Repeaters houden wel een buurtellijst bij, maar die is voor
statistiek, niet voor routering.

Er is evenmin een object voor een bericht in de zin van een blijvend item.
Berichten zijn pakketten, en pakketten zijn vluchtig. De room server is de
enige rol die daarvan afwijkt en berichten bewaart; zie
[Posts en synchronisatie](../../techniek/roomserver/posts-and-sync.md).

## Bronnen

- [MeshCore `03b6ef4` — `src/Identity.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Identity.h)
- [MeshCore `03b6ef4` — `src/Packet.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Packet.h)
- [MeshCore `03b6ef4` — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore `03b6ef4` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
