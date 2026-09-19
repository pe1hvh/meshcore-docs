# Buren

*NEIGHBORS · VERWIJDEREN · DISCOVERY*

Een repeater houdt bij welke andere repeaters hij rechtstreeks hoort. Deze drie
commando's tonen die lijst, halen er items uit en vragen de buren zich te
melden. Alleen de repeater heeft zo'n lijst.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_repeater/MyMesh.h`, `examples/simple_room_server/MyMesh.h`,
> `examples/simple_sensor/SensorMesh.h`, `src/Utils.cpp`, en de officiële
> `docs/cli_commands.md`. Regelnummers verwijzen naar deze commit en zijn te
> reproduceren met [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `neighbors` | `alleen repeater` | — | | `CommonCLI.cpp` r.261 |
| `neighbor.remove <pubkey_prefix>` | `effect: repeater` | — | | `CommonCLI.cpp` r.263 |
| `discover.neighbors` | `alleen repeater` | — | | `simple_repeater/MyMesh.cpp` r.1251 |

## Commando's

### neighbors

Elke regel is `<eerste 4 bytes public key>:<seconden geleden>:<SNR × 4>`,
nieuwste eerst (`MyMesh.cpp` r.1084–1100). Deel de laatste waarde door 4 voor de
SNR in dB (`MyMesh.h` r.68). De lijst stopt zodra het antwoord 134 tekens lang
is (`MyMesh.cpp` r.1088); zonder buren is het antwoord `-none-`. Room server en
sensor antwoorden `not supported` (`simple_room_server/MyMesh.h` r.207,
`simple_sensor/SensorMesh.h` r.71). De officiële documentatie noemt het tweede
veld een timestamp; de firmware geeft het aantal seconden geleden.

**Voorbeeld** *(voorbeeldsleutels uit `tools/dm-example.py`)*:

```text
neighbors
  -> E3A0313A:312:26
EA1F69C3:1840:-6
```

`E3A0313A` is 312 seconden geleden gehoord met SNR 6,5 dB, `EA1F69C3` 1840
seconden geleden met −1,5 dB. Alleen de eerste regel krijgt het voorvoegsel
`  -> `.

### neighbor.remove

Verwijdert elke buur waarvan de public key met het opgegeven hex-prefix begint
(`MyMesh.cpp` r.1112–1121). Het prefix moet een even aantal hextekens hebben,
anders is het antwoord `ERR: bad pubkey` (`src/Utils.cpp` r.124). Een leeg
prefix — het commando eindigt direct na de spatie — verwijdert alle buren. Room
server en sensor antwoorden `OK`, maar doen niets (`CommonCLI.h` r.83–85).

**Voorbeeld:**

```text
neighbor.remove E3A0313A
  -> OK
```

### discover.neighbors

Stuurt een discovery-verzoek naar directe buren. Het commando kent geen opties;
met extra tekst is het antwoord `Err - discover.neighbors has no options`.

**Voorbeeld:**

```text
discover.neighbors
  -> OK - Discover sent
```

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.h)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.h)
- [MeshCore firmware — `src/Utils.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Utils.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
