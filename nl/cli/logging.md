# Logging

*RX-LOG · STARTEN · STOPPEN · WISSEN · TONEN*

Een node kan ontvangen pakketten naar een bestand schrijven. Bij de repeater is
dat `/packet_log` (`MyMesh.h` r.81). Vier commando's zetten dat aan en uit,
wissen het bestand en tonen het.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_repeater/MyMesh.h`, en de officiële `docs/cli_commands.md`.
> Regelnummers verwijzen naar deze commit en zijn te reproduceren met
> [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `log start` | | — | | `CommonCLI.cpp` r.458 |
| `log stop` | | — | | `CommonCLI.cpp` r.461 |
| `log erase` | | — | | `CommonCLI.cpp` r.464 |
| `log` | | — | ja | `CommonCLI.cpp` r.467 |

## Commando's

### log start

Begint met loggen. Het antwoord begint met drie spaties.

**Voorbeeld:**

```text
log start
  ->    logging on
```

### log stop

Stopt met loggen.

**Voorbeeld:**

```text
log stop
  ->    logging off
```

### log erase

Wist het logbestand.

**Voorbeeld:**

```text
log erase
  ->    log erased
```

### log

Schrijft het logbestand naar de seriële console (`MyMesh.cpp` r.1042) en sluit
af met `EOF`.

**Voorbeeld:**

```text
log
  ->    EOF
```

Bij een leeg logbestand is `EOF` het enige wat verschijnt.

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
