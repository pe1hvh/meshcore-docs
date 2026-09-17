# Regio's

*REGIOBOOM · FLOODRECHTEN · THUISREGIO · SCOPE · OPSLAAN*

Met deze commando's bouw je de regioboom van een node, bepaal je welke regio's
flood-verkeer mogen doorsturen en met welke scope de node zelf verstuurt. Wat
regio's en scopes zijn staat in
[Regio's en Scopes](../techniek/regions-and-scopes.md); de Nederlandse indeling
in [Regio's: bedoeling en praktijk](../techniek/regions-in-practice.md).

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `src/helpers/RegionMap.cpp`,
> `src/helpers/RegionMap.h`, `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, en de officiële
> `docs/cli_commands.md`. Regelnummers verwijzen naar deze commit en zijn te
> reproduceren met [`tools/cli-commands.py`](../../tools/cli-commands.py).

> [!NOTE]
> Wijzigingen via `put`, `def`, `allowf`, `denyf`, `home` en `remove` gelden
> direct, maar gaan pas na `region save` naar het bestandssysteem. De sensor kan
> regio's niet opslaan: `saveRegions()` is daar niet ingevuld (`CommonCLI.h`
> r.97–99), dus zijn regio-instellingen zijn na een herstart weg.

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `region` | | — | | `CommonCLI.cpp` r.1005–1007 |
| `region put <name> [parent_name]` | | — | | `CommonCLI.cpp` r.1078 |
| `region def <token> [<token> ...]` | | — | | `CommonCLI.cpp` r.991 |
| `region load` | `niet sensor` | — | | `CommonCLI.cpp` r.1008 |
| `region save` | `niet sensor` | — | | `CommonCLI.cpp` r.1010–1014 |
| `region allowf <name>` / `region denyf <name>` | | — | | `CommonCLI.cpp` r.1015, r.1023 |
| `region get <name>` | | — | | `CommonCLI.cpp` r.1031 |
| `region home` / `region home <name>` | | — | | `CommonCLI.cpp` r.1043, r.1051 |
| `region default` / `region default {<name>\|<null>}` | | — | | `CommonCLI.cpp` r.1054, r.1075 |
| `region remove <name>` | | — | | `CommonCLI.cpp` r.1091 |
| `region list <allowed\|denied>` | | — | | `CommonCLI.cpp` r.1102 |

## Commando's

### region

Toont de boom, één regio per regel, ingesprongen per niveau. `F` betekent dat
flood is toegestaan, `^` markeert de thuisregio (`RegionMap.cpp` r.285–302). Een
`#` voor de naam wordt weggelaten.

**Voorbeeld** *(na de basisconfiguratie hieronder)*:

```text
region
  -> * F
 eu F
  nl F
   nl-ov F
```

### region put

Maakt een regio aan onder de opgegeven ouder, of onder `*` als die ontbreekt.
Een nieuwe regio mag altijd flooden. Andere antwoorden: `Err - unknown parent`
en `Err - unable to put`.

**Voorbeeld:**

```text
region put nl-ov nl
  -> OK - (flood allowed)
```

**NL:** de basisconfiguratie uit [Aan de Slag](../gebruik/getting-started.md),
hier voor Overijssel:

```text
region put eu
region put nl eu
region put nl-ov nl
region default nl-ov
region save
```

### region def

Bouwt een boom op één regel. Elk token wordt een kind van de cursor, die begint
bij `*`; `naam|sprong` maakt `naam` aan en zet de cursor daarna op `sprong`. Het
antwoord is de nieuwe boom, of een fout zoals `Err - unknown jump: <naam>`
(`CommonCLI.cpp` r.969–978). Regio's die vóór de fout zijn aangemaakt blijven
staan.

**Voorbeeld:**

```text
region def eu nl nl-ov
  -> * F
 eu F
  nl F
   nl-ov F
```

### region load

Laadt een boom regel voor regel. Het aantal spaties aan het begin bepaalt het
niveau (1–7), een `F` achter de naam staat flood toe; een lege regel sluit af
(`simple_repeater/MyMesh.cpp` r.1175–1207). Een geladen boom vervangt de hele
bestaande boom: `resetFrom()` begint leeg (`RegionMap.h` r.52). Een regio die al
bestond houdt zijn id en flood-recht. Op de sensor doet het commando niets.
Extra argumenten achter `load`, zoals de officiële documentatie ze noemt,
negeert de firmware.

**Voorbeeld:**

```text
region load
 eu F
  nl F
   nl-ov F

  -> OK - loaded 3 regions
```

### region save

Schrijft de regio's naar het bestandssysteem. De sensor antwoordt
`Err - save failed`.

**Voorbeeld:**

```text
region save
  -> OK
```

### region allowf / region denyf

Staat flood-verkeer voor een regio toe of verbiedt het. De naam mag een prefix
zijn; `*` is de regio voor pakketten zonder scope. Onbekende naam:
`Err - unknown region`.

**Voorbeeld:**

```text
region denyf eu
  -> OK
```

**NL:** `region denyf *` alleen volgens de afspraken in
[Aan de Slag](../gebruik/getting-started.md).

### region get

Toont één regio: naam, ouder tussen haakjes en `F` als flood is toegestaan. Het
antwoord begint met een spatie.

**Voorbeeld:**

```text
region get nl-ov
  ->  nl-ov (nl) F
```

### region home

Toont of zet de thuisregio. Zonder thuisregio is het antwoord ` home is *`.

**Voorbeeld:**

```text
region home nl-ov
  ->  home is now nl-ov
```

### region default

Toont of zet de scope waarmee de node zelf verstuurt. Een onbekende naam wordt
aangemaakt; de regio krijgt flood-recht en wordt direct opgeslagen. `<null>`
wist de scope.

**Voorbeeld:**

```text
region default nl-ov
  ->  default scope is now nl-ov
```

**NL:** de eigen provincie, zie [Aan de Slag](../gebruik/getting-started.md).

### region remove

Verwijdert een regio. De naam moet exact kloppen. Een regio met kinderen geeft
`Err - not empty`, een onbekende `Err - not found`.

**Voorbeeld:**

```text
region remove nl-ov
  -> OK
```

### region list

Namen van de regio's die flood wel of niet mogen doorsturen, gescheiden door
komma's; `-none-` als er geen zijn. De officiële documentatie noemt dit commando
alleen-serieel; de firmware controleert dat niet.

**Voorbeeld:**

```text
region list allowed
  -> *,eu,nl,nl-ov
```

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/RegionMap.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/RegionMap.cpp)
- [MeshCore firmware — `src/helpers/RegionMap.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/RegionMap.h)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
