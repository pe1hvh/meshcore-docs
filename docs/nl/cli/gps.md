# GPS

*AAN/UIT · TIJD · LOCATIE · ADVERTBELEID*

Commando's voor een GPS-ontvanger op de node. Ze bestaan alleen als de build
`ENV_INCLUDE_GPS=1` zet (`CommonCLI.cpp` r.355–433); anders geeft elk ervan
`Unknown command`.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, en de officiële
> `docs/cli_commands.md`. Regelnummers verwijzen naar deze commit en zijn te
> reproduceren met [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `gps` | `build flag` | — | | `CommonCLI.cpp` r.415 |
| `gps on` / `gps off` | `build flag` | `off` | | `CommonCLI.cpp` r.356, r.364 |
| `gps sync` | `build flag` | — | | `CommonCLI.cpp` r.372 |
| `gps setloc` | `build flag` | — | | `CommonCLI.cpp` r.380 |
| `gps advert` / `gps advert <none\|share\|prefs>` | `build flag` | `prefs` | | `CommonCLI.cpp` r.385 |

## Commando's

### gps

Toont de toestand: `off` als de ontvanger uit staat, anders
`on, <active|deactivated>, <fix|no fix>, <n> sats`. Zonder ontvanger:
`Can't find GPS`.

**Voorbeeld** *(board zonder GPS-ontvanger)*:

```text
gps
  -> Can't find GPS
```

### gps on / gps off

Zet de ontvanger aan of uit en slaat dat op. Zonder schakelbare ontvanger:
`gps toggle not found`. De officiële documentatie schrijft dit als
`gps <state>`.

**Voorbeeld:**

```text
gps on
  -> ok
```

### gps sync

Zet de klok gelijk met de GPS-tijd. Zonder ontvanger: `gps provider not found`.

**Voorbeeld:**

```text
gps sync
  -> ok
```

### gps setloc

Neemt de GPS-positie over als `lat` en `lon` en slaat die op.

**Voorbeeld:**

```text
gps setloc
  -> ok
```

### gps advert

Welke locatie in de adverts gaat: geen (`none`), de actuele GPS-positie
(`share`) of de opgeslagen `lat`/`lon` (`prefs`). Een andere waarde geeft
`error`.

**Voorbeeld:**

```text
gps advert
  -> > prefs
gps advert none
  -> ok
```

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
