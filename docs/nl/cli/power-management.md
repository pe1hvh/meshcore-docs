# Energiebeheer (nRF52)

*BOOTLOADER · VOEDING · RESETREDEN · SPANNING BIJ OPSTARTEN*

Vijf leescommando's voor nRF52-boards. De officiële documentatie zet ze onder
*Bridge*, maar in de firmware hangen ze af van het platform: `NRF52_PLATFORM` en
`NRF52_POWER_MANAGEMENT` (`CommonCLI.cpp` r.884–928).

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `src/helpers/NRF52Board.cpp`,
> `variants/sensecap_solar/platformio.ini`, en de officiële
> `docs/cli_commands.md`. Regelnummers verwijzen naar deze commit en zijn te
> reproduceren met [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `get bootloader.ver` | `build flag` | — | | `CommonCLI.cpp` r.884 |
| `get pwrmgt.support` | `build flag` | — | | `CommonCLI.cpp` r.903 |
| `get pwrmgt.source` | `build flag` | — | | `CommonCLI.cpp` r.909 |
| `get pwrmgt.bootreason` | `build flag` | — | | `CommonCLI.cpp` r.915 |
| `get pwrmgt.bootmv` | `build flag` | — | | `CommonCLI.cpp` r.923 |

## Commando's

### bootloader.ver

Versie van de bootloader, of `> unknown`. Op andere platforms:
`ERROR: unsupported`.

**Voorbeeld** *(ESP32)*:

```text
get bootloader.ver
  -> ERROR: unsupported
```

### pwrmgt.support

`> supported` als de build `NRF52_POWER_MANAGEMENT` zet, zoals de SenseCap Solar
(`variants/sensecap_solar/platformio.ini` r.13), anders `> unsupported`.

**Voorbeeld** *(SenseCap Solar)*:

```text
get pwrmgt.support
  -> > supported
```

### pwrmgt.source

`> external` of `> battery`. Zonder energiebeheer:
`ERROR: Power management not supported`.

**Voorbeeld:**

```text
get pwrmgt.source
  -> > battery
```

### pwrmgt.bootreason

Reden van de laatste reset en van de laatste uitschakeling, als tekst
(`NRF52Board.cpp` r.69 en verder).

**Voorbeeld** *(board zonder energiebeheer)*:

```text
get pwrmgt.bootreason
  -> ERROR: Power management not supported
```

Met energiebeheer is de vorm `> Reset: <reden>; Shutdown: <reden>`, bijvoorbeeld
met resetreden `Reset Pin`.

### pwrmgt.bootmv

Spanning bij het opstarten, als `> <n> mV`.

**Voorbeeld** *(board zonder energiebeheer)*:

```text
get pwrmgt.bootmv
  -> ERROR: Power management not supported
```

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/NRF52Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/NRF52Board.cpp)
- [MeshCore firmware — `variants/sensecap_solar/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/sensecap_solar/platformio.ini)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
