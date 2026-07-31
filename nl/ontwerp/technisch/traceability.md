# Traceerbaarheid

*LOGISCH NAAR TECHNISCH · BESTAND EN REGEL · LEGE REGELS*

Het logisch ontwerp beschrijft zeventien componenten. Dit hoofdstuk wijst elk
van die zeventien aan in de broncodestructuur, met bestand en regelnummer. Het
sluit af met de twee dingen die het logisch ontwerp expliciet níét heeft — en
die dus ook geen realisatie hebben.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — elk regelnummer in de matrix is
> nagelopen in de genoemde bestanden.

## Waar deze matrix voor is

Door ieder logisch onderdeel aan de broncode te koppelen wordt het ontwerp
controleerbaar en verifieerbaar. Deze tabel legt die koppeling vast: wie
twijfelt of de mesh-logica werkelijk niets van de radio weet, kan `src/Mesh.h`
r.26 opslaan en zelf kijken.

De matrix loopt één kant op. Van logische component naar realisatie, niet
andersom — niet elke klasse in de broncodestructuur hoort bij een logische
component. De 55 zelfstandige klassen uit [het klassenmodel](class-model.md)
zijn grotendeels hulpmiddelen zonder tegenhanger in het logisch ontwerp.

## De matrix

| Logische component | Realisatie |
|---|---|
| Pakketafhandeling | `Dispatcher`, `src/Dispatcher.h` r.116 |
| Mesh-logica | `Mesh`, `src/Mesh.h` r.26 |
| Applicatie | `MyMesh` / `SensorMesh` / `KissModem` in `examples/` |
| Radio | `mesh::Radio`, `src/Dispatcher.h` r.22 |
| Bord | `mesh::MainBoard`, `src/MeshCore.h` r.45 |
| Klok | `mesh::RTCClock`, `src/MeshCore.h` r.80 |
| Entropiebron | `mesh::RNG`, `src/Utils.h` r.9 |
| Pakketpool | `mesh::PacketManager`, `src/Dispatcher.h` r.85; implementatie `StaticPoolPacketManager`, `src/helpers/StaticPoolPacketManager.h` r.21 |
| Gezien-tabel | `mesh::MeshTables`, `src/Mesh.h` r.16; implementatie `SimpleMeshTables`, `src/helpers/SimpleMeshTables.h` r.11 |
| Identiteit | `mesh::Identity`, `src/Identity.h` r.11; `LocalIdentity` r.54 |
| Rechtenlijst | `ClientACL`, `src/helpers/ClientACL.h` r.40; `ClientInfo` r.15 |
| Opslag | `IdentityStore`, `src/helpers/IdentityStore.h` r.14 |
| Bediening | `CommonCLI`, `src/helpers/CommonCLI.h` r.117; contract `CommonCLICallbacks` r.68 |
| Koppelvlak | `BaseSerialInterface`, `src/helpers/BaseSerialInterface.h` r.7 |
| Scherm | `DisplayDriver`, `src/helpers/ui/DisplayDriver.h` r.6 |
| Brug | `AbstractBridge`, `src/helpers/AbstractBridge.h` r.5; `BridgeBase` r.21 in `bridges/BridgeBase.h` |
| Sensorbeheer | `SensorManager`, `src/helpers/SensorManager.h` r.12 |
| Routeringstabel | *geen — paden reizen met het pakket mee* |
| Takenmodel | *geen — alles draait in één lus* |

## Wat de matrix laat zien

Drie dingen vallen op.

**De kern is klein.** Zeven van de zeventien componenten wijzen naar een
bestand in `src/`, en die zeven bestanden zijn samen 2332 regels. De overige
tien zitten in `src/helpers/` of in `examples/`.

**Zeven componenten zijn een contract, geen klasse.** Radio, bord, klok,
entropiebron, koppelvlak, scherm en sensorbeheer wijzen naar een
interfaceklasse. Wat er in een concrete build onder hangt, hangt
van het buildtarget af — zie [Platformrealisatie](platform-realisation.md) en
[Radiorealisatie](radio-realisation.md).

**Twee componenten hebben geen enkele klasse.** De applicatie wijst naar drie
verschillende klassen in zes mappen, omdat er per build precies één
applicatie compileert. Het gaat om `MyMesh` (vijf keer, in vijf verschillende
bestanden), `SensorMesh` en `KissModem`.

## De twee lege regels

Onderaan de matrix staan twee regels zonder realisatie. Ze zijn er met opzet,
en ze horen in de tabel te blijven staan: een matrix waaruit de lege regels
zijn weggelaten, suggereert dat alles gerealiseerd is.

**Routeringstabel.** MeshCore bouwt geen kaart van het netwerk op. Een node
weet niet welke buren er zijn of via welke weg een bestemming te bereiken is;
het pad reist met het pakket mee. Er is dus geen klasse die het onderhoudt, en
ook geen bestand waar hij zou moeten staan. Zie
[Route traceren](../../techniek/route-tracing.md) voor hoe dat dan wél werkt.

**Takenmodel.** Er is geen scheduler en geen takenmodel. Alles draait in één
lus, en componenten krijgen om beurten de kans iets te doen. Een component die
te lang blijft hangen, houdt de rest op. De afwezigheid is een keuze en geen
gebrek; [Ontwerpbeslissingen](../logisch/decisions.md) gaat in op wat die
keuze kost.

> [!NOTE]
> Beide zijn in [Componenten](../logisch/components.md) onder *Wat er niet is*
> beschreven. Ze staan hier als lege regel omdat de matrix anders de indruk
> wekt dat het logisch ontwerp uitsluitend uit gerealiseerde onderdelen
> bestaat.

## Bronnen

- [MeshCore `03b6ef4` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Dispatcher.h)
- [MeshCore `03b6ef4` — `src/Mesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Mesh.h)
- [MeshCore `03b6ef4` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore `03b6ef4` — `src/Identity.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Identity.h)
- [MeshCore `03b6ef4` — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore `03b6ef4` — `src/helpers/CommonCLI.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.h)
