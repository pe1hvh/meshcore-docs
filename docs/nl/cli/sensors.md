# Sensoren

*INSTELLINGEN · GPIO · VOORBEELD-HOOK*

Instellingen van de sensormanager op het board, plus twee commando's die alleen
de sensorfirmware kent en die niet in de officiële documentatie staan.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `src/helpers/SensorManager.h`,
> `examples/simple_sensor/SensorMesh.cpp`, `examples/simple_sensor/main.cpp`,
> `src/MeshCore.h`, en de officiële `docs/cli_commands.md`. Regelnummers
> verwijzen naar deze commit en zijn te reproduceren met
> [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `sensor list [start]` | | — | | `CommonCLI.cpp` r.328 |
| `sensor get <key>` / `sensor set <key> <value>` | | — | | `CommonCLI.cpp` r.309, r.317 |
| `io` / `io <hex>` / `io r<hex>` / `io s<hex>` / `io t<hex>` | `alleen sensor` | — | | `SensorMesh.cpp` r.427 |
| `magic` | `alleen sensor` | — | | `simple_sensor/main.cpp` r.35 |

## Commando's

### sensor list

Toont de instellingen als `naam=waarde`, na een regel met het aantal. Past niet
alles in het antwoord, dan eindigt het met `... next:<n>`; geef dat getal als
`start` mee. Heeft het board er geen, dan is het antwoord `no custom var`
(`SensorManager.h` r.21).

**Voorbeeld** *(board zonder instellingen)*:

```text
sensor list
  -> no custom var
```

### sensor get / sensor set

Leest of zet één instelling. Een onbekende sleutel geeft bij `get` het antwoord
`null` en bij `set` `can't find custom var`.

**Voorbeeld** *(board zonder instellingen)*:

```text
sensor get gps
  -> null
```

### io

Leest of schrijft de GPIO-uitgangen van het board als hexwaarde. `io` leest;
`io <hex>` zet de waarde, `r` wist bits, `s` zet bits en `t` keert bits om. Het
antwoord is altijd de waarde na de actie. De vergelijking kijkt alleen naar de
eerste twee tekens, dus elk commando dat met `io` begint komt hier terecht. Een
board dat geen GPIO aanbiedt geeft altijd `0` (`MeshCore.h` r.62–63).

**Voorbeeld** *(board zonder GPIO)*:

```text
io s1
  -> 0
```

### magic

Een voorbeeld van een eigen commando: `simple_sensor/main.cpp` laat zien hoe een
sensorbuild commando's kan toevoegen via `handleCustomCommand()`
(`SensorMesh.cpp` r.389). Het zit in elke build van deze voorbeeldfirmware en
doet verder niets.

**Voorbeeld:**

```text
magic
  -> **Magic now done**
```

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/SensorManager.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/SensorManager.h)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/main.cpp)
- [MeshCore firmware — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
