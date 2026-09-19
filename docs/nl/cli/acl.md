# ACL

*RECHTEN · TABEL · MEELEZEN*

De ACL is de tabel met bekende clients en hun rechten. Twee commando's zitten
niet in `CommonCLI` maar in elke rol apart, met dezelfde code. Het inloggen zelf
staat in [Inloggen en de ACL](../technical/roomserver/login-and-acl.md).

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, `src/helpers/ClientACL.cpp`,
> `src/helpers/ClientACL.h`, `src/helpers/CommonCLI.cpp`, en de officiële
> `docs/cli_commands.md`. Regelnummers verwijzen naar deze commit en zijn te
> reproduceren met [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `setperm <pubkey> <permissions>` | | — | | R r.1218 · RS r.904 · S r.394 |
| `get acl` | | — | ja | R r.1240 · RS r.926 · S r.416 |
| `get allow.read.only` / `set allow.read.only <on\|off>` | `effect: room server` | `off` | | `CommonCLI.cpp` r.511, r.783 |

## Commando's

### setperm

Zet de rechten van een client: 0 gast, 1 alleen lezen, 2 lezen en schrijven, 3
beheerder (`ClientACL.h` r.7–11). Rechten 0 verwijdert de client; daarvoor
volstaat een prefix van de sleutel. Voor 1–3 is de volledige sleutel van 64
hextekens nodig (`ClientACL.cpp` r.121–143). Zonder rechtenwaarde is het
antwoord `Err - bad params`; de officiële documentatie zegt dat weglaten de
client verwijdert.

**Voorbeeld** *(voorbeeldsleutel uit `tools/dm-example.py`)*:

```text
setperm E3A0313ACE439E364C44894F5151D53A35E7D70523B45A69794CCD30E484FCE7 3
  -> OK
setperm E3A0313A 0
  -> OK
```

Andere antwoorden: `Err - bad pubkey` bij ongeldige hex en
`Err - invalid params` als de sleutel te kort is of niet bestaat.

### get acl

Schrijft de tabel naar de seriële console: per client de rechten in hex en de
volledige public key. Gasten staan er niet in. Het commando geeft zelf geen
antwoord, dus er is geen `  -> `. Over de radio bestaat het niet; zie
[Requests en CLI](../technical/roomserver/requests-and-cli.md).

**Voorbeeld:**

```text
get acl
ACL:
03 E3A0313ACE439E364C44894F5151D53A35E7D70523B45A69794CCD30E484FCE7
```

### allow.read.only

Alleen de room server gebruikt deze vlag: bij een fout wachtwoord krijgt de
client dan toch gastrechten (`simple_room_server/MyMesh.cpp` r.336).

**Voorbeeld:**

```text
set allow.read.only on
  -> OK
get allow.read.only
  -> > on
```

## Bronnen

- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
