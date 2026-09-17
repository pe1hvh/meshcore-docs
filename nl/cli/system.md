# Systeem

*NAAM · LOCATIE · SLEUTELS · WACHTWOORDEN · ROL*

Instellingen die de node zelf beschrijven: naam, locatie, eigenaar, sleutelpaar
en wachtwoorden, plus de batterijcorrectie en de energiebesparing van de
repeater.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `src/helpers/CommonCLI.h`,
> `examples/simple_repeater/MyMesh.cpp`, `examples/simple_repeater/main.cpp`,
> `examples/simple_repeater/MyMesh.h`, `examples/simple_room_server/MyMesh.h`,
> `examples/simple_sensor/SensorMesh.h`, `src/MeshCore.h`, en de officiële
> `docs/cli_commands.md`. Regelnummers verwijzen naar deze commit en zijn te
> reproduceren met [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `get name` / `set name <name>` | | R `repeater` · RS `Test BBS` · S `sensor` ¹ | | `CommonCLI.cpp` r.552, r.796 |
| `get lat` / `set lat <degrees>` / `get lon` / `set lon <degrees>` | | `0.0` | | `CommonCLI.cpp` r.589, r.593, r.800, r.802 |
| `get prv.key` / `set prv.key <private_key>` | | — | alleen `get` | `CommonCLI.cpp` r.539, r.791 |
| `password <new_password>` | | `password` | | `CommonCLI.cpp` r.289 |
| `get guest.password` / `set guest.password <password>` | `effect: repeater, room server` | RS `ROOM_PASSWORD` ¹, anders leeg | | `CommonCLI.cpp` r.535, r.789 |
| `get owner.info` / `set owner.info <text>` | `effect: repeater` | `leeg` | | `CommonCLI.cpp` r.651, r.825 |
| `get adc.multiplier` / `set adc.multiplier <value>` | | `0.0` (waarde van het board) | | `CommonCLI.cpp` r.749, r.895 |
| `get public.key` | | — | | `CommonCLI.cpp` r.851 |
| `get role` | | — | | `CommonCLI.cpp` r.854 |
| `powersaving` / `powersaving on` / `powersaving off` | `effect: repeater` | `off` | | `CommonCLI.cpp` r.434–458 |

## Commando's

### name

De naam in de adverts. Het veld is 32 bytes (`CommonCLI.h` r.24). De tekens
`[ ] \ : , ? *` zijn niet toegestaan; dan is het antwoord `Error, bad chars`.

**Voorbeeld:**

```text
set name PE1HVH Repeater
  -> OK
get name
  -> > PE1HVH Repeater
```

¹ Terugvalwaarden van `ADVERT_NAME`; de meeste builds zetten een eigen naam.

### lat / lon

Breedte- en lengtegraad in decimale graden, zonder controle op het bereik. `get`
gebruikt dezelfde float-weergave als `get radio`. De locatie gaat mee in de
adverts, afhankelijk van `gps advert`.

**Voorbeeld:**

```text
set lat 52.5168
  -> OK
get lat
  -> > 52.5167999
set lon 6.083
  -> OK
get lon
  -> > 6.0830001
```

### prv.key

Het sleutelpaar van de node. `set` verwacht de privésleutel als 128 hextekens
(`PRV_KEY_SIZE` 64, `MeshCore.h` r.9), controleert hem, en antwoordt met de
nieuwe public key; de wissel gaat in na een herstart. `get` werkt alleen via de
seriële console. De officiële documentatie spreekt van 64 hextekens.

**Voorbeeld:**

```text
set prv.key 00
  -> Error, bad key
```

Bij een geldige sleutel is het antwoord `OK, reboot to apply! New pubkey: `
gevolgd door 64 hextekens.

### password

Het beheerderswachtwoord, maximaal 15 tekens (`CommonCLI.h` r.26). Het antwoord
herhaalt het nieuwe wachtwoord.

**Voorbeeld:**

```text
password Zwolle2026
  -> password now: Zwolle2026
```

> [!WARNING]
> De standaard `password` is voor iedereen bekend. Zolang die staat, kan elke
> client met dat wachtwoord de node beheren.

### guest.password

Het wachtwoord voor gewone deelnemers, maximaal 15 tekens (`CommonCLI.h` r.34).
Repeater en room server gebruiken het bij het inloggen
(`simple_repeater/MyMesh.cpp` r.104, `simple_room_server/MyMesh.cpp` r.334). Zie
[Inloggen en de ACL](../techniek/roomserver/login-and-acl.md).

**Voorbeeld:**

```text
set guest.password zwolle
  -> OK
get guest.password
  -> > zwolle
```

¹ Alleen als de build `ROOM_PASSWORD` zet (`simple_room_server/MyMesh.cpp`
r.653–655). De officiële documentatie noemt leeg als standaard.

### owner.info

Vrije tekst over de eigenaar, maximaal 119 tekens (`CommonCLI.h` r.62). Een `|`
wordt opgeslagen als regeleinde en bij `get` weer als `|` getoond. Alleen de
repeater doet er iets mee (`simple_repeater/MyMesh.cpp` r.179, r.376).

**Voorbeeld:**

```text
set owner.info PE1HVH|Zwolle
  -> OK
get owner.info
  -> > PE1HVH|Zwolle
```

### adc.multiplier

Correctiefactor voor de batterijmeting. `0` zet de waarde van het board terug.
Ondersteunt het board het niet, dan is het antwoord
`Error: unsupported by this board`; `get` geeft datzelfde antwoord als het board
geen factor heeft.

**Voorbeeld:**

```text
set adc.multiplier 1.05
  -> OK - multiplier set to 1.050
set adc.multiplier 0
  -> OK - using default board multiplier
```

### public.key

De public key van de node als 64 hextekens.

**Voorbeeld** *(voorbeeldsleutel uit `tools/dm-example.py`)*:

```text
get public.key
  -> > EA1F69C38A415ABDD55590ECC796DE3D04FE6D80FAEE006A37021432804CBDCC
```

### role

De rol waarvoor de firmware is gebouwd: `repeater`, `room_server` of `sensor`
(`FIRMWARE_ROLE` in de drie rolbestanden).

**Voorbeeld:**

```text
get role
  -> > repeater
```

### powersaving

Laat de repeater slapen als er niets te doen is. Alleen de hoofdlus van de
repeater leest de vlag (`simple_repeater/main.cpp` r.155). Het antwoord op
`powersaving on` hangt af van het platform: op nRF52 `on - Immediate effect`, op
ESP32 `on - After 2 minutes`, bij een build met bridge `Bridge not supported` en
elders `Board not supported`. Zonder argument toont het commando `on` of `off`.

**Voorbeeld** *(nRF52, zoals de SenseCap Solar)*:

```text
powersaving on
  -> on - Immediate effect
powersaving
  -> on
```

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/CommonCLI.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.h)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_repeater/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/main.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.h)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.h)
- [MeshCore firmware — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
