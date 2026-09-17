# Informatie

*VERSIE · BOARD*

Twee commando's die zeggen welke firmware op welk board draait. De rol en de
public key staan bij [Systeem](system.md).

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `examples/simple_repeater/MyMesh.h`,
> `variants/sensecap_solar/SenseCapSolarBoard.h`, en de officiële
> `docs/cli_commands.md`. Regelnummers verwijzen naar deze commit en zijn te
> reproduceren met [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `ver` | | — | | `CommonCLI.cpp` r.305 |
| `board` | | — | | `CommonCLI.cpp` r.307 |

## Commando's

### ver

Firmwareversie en builddatum. Beide komen uit `FIRMWARE_VERSION` en
`FIRMWARE_BUILD_DATE`; zonder build flag zijn dat `v1.16.0` en `6 Jun 2026`
(`simple_repeater/MyMesh.h` r.71–76).

**Voorbeeld** *(terugvalwaarden)*:

```text
ver
  -> v1.16.0 (Build: 6 Jun 2026)
```

**NL:** geen afspraak.

### board

De naam die het board zelf opgeeft.

**Voorbeeld** *(SenseCap Solar, `SenseCapSolarBoard.h` r.36–38)*:

```text
board
  -> Seeed SenseCap Solar
```

**NL:** geen afspraak.

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore firmware — `variants/sensecap_solar/SenseCapSolarBoard.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/sensecap_solar/SenseCapSolarBoard.h)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
