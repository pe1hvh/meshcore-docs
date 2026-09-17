# Routing

*DOORSTUREN · VERTRAGING · DUTY CYCLE · ADVERTS · HOP-LIMIETEN*

Hoe een node verkeer doorgeeft: of hij doorstuurt, hoe lang hij wacht, hoeveel
zendtijd hij mag gebruiken, hoe vaak hij zichzelf aankondigt en hoe ver
flood-pakketten mogen reizen. Hier staan de meeste Nederlandse afspraken; ze
komen uit [Regelgeving & Duty Cycle](../gebruik/regulations.md).

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_repeater/MyMesh.h`, `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_room_server/MyMesh.h`,
> `examples/simple_sensor/SensorMesh.cpp`, en de officiële
> `docs/cli_commands.md`. Regelnummers verwijzen naar deze commit en zijn te
> reproduceren met [`tools/cli-commands.py`](../../tools/cli-commands.py).

> [!WARNING]
> De firmware-standaard van `dutycycle` is 50 %. Dat ligt ver boven de 10 % die
> in Nederland geldt. Een vers geflashte node is dus niet conform tot je
> `set dutycycle 10` geeft. Zie
> [Regelgeving & Duty Cycle](../gebruik/regulations.md).

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `get repeat` / `set repeat <on\|off>` | | R `on` · RS `off` · S `off` | | `CommonCLI.cpp` r.560, r.798 |
| `get path.hash.mode` / `set path.hash.mode <0\|1\|2>` | | `0` | | `CommonCLI.cpp` r.661, r.835 |
| `get loop.detect` / `set loop.detect <off\|minimal\|moderate\|strict>` | `effect: repeater` | `off` | | `CommonCLI.cpp` r.671, r.837 |
| `get txdelay` / `set txdelay <0-2>` | | `0.5` | | `CommonCLI.cpp` r.606, r.815 |
| `get direct.txdelay` / `set direct.txdelay <0-2>` | | R `0.3` · RS/S `0.2` | | `CommonCLI.cpp` r.642, r.823 |
| `get rxdelay` / `set rxdelay <0-20>` | | `0.0` | | `CommonCLI.cpp` r.597, r.813 |
| `get dutycycle` / `set dutycycle <1-100>` | | `50` | | `CommonCLI.cpp` r.483, r.770 |
| `get af` / `set af <value>` | | `1.0` | | `CommonCLI.cpp` r.495, r.775 |
| `get int.thresh` / `set int.thresh <value>` | | `0` | | `CommonCLI.cpp` r.499, r.777 |
| `get agc.reset.interval` / `set agc.reset.interval <seconds>` | | `0` | | `CommonCLI.cpp` r.503, r.779 |
| `get multi.acks` / `set multi.acks <0\|1>` | `effect: repeater, room server` | `0` | | `CommonCLI.cpp` r.507, r.781 |
| `get flood.advert.interval` / `set flood.advert.interval <hours>` | | R/RS `47` · S `0` | | `CommonCLI.cpp` r.515, r.785 |
| `get advert.interval` / `set advert.interval <minutes>` | | `2`, na de eerste opgeslagen wijziging `0` ¹ | | `CommonCLI.cpp` r.525, r.787 |
| `get flood.max` / `set flood.max <0-64>` | | `64` | | `CommonCLI.cpp` r.633, r.821 |
| `get flood.max.unscoped` / `set flood.max.unscoped <0-64>` | `effect: repeater, room server` | R/RS `64` · S `0` ¹ | | `CommonCLI.cpp` r.615, r.819 |
| `get flood.max.advert` / `set flood.max.advert <0-64>` | `effect: repeater, room server` | R/RS `8` · S `0` ¹ | | `CommonCLI.cpp` r.624, r.817 |

## Commando's

### repeat

Of de node pakketten doorstuurt. Alleen de waarde `off` zet het uit; elke andere
waarde zet het aan. Room server en sensor staan standaard uit
(`simple_room_server/MyMesh.cpp` r.646, `SensorMesh.cpp` r.726). De officiële
documentatie noemt `on` voor alle rollen.

**Voorbeeld:**

```text
set repeat off
  -> OK - repeat is now OFF
get repeat
  -> > off
```

**NL:** `on` op een repeater. Uitzetten betekent geen relay.

### path.hash.mode

De grootte van de hash waarmee de node zichzelf in het pad van zijn eigen
adverts zet: 0 = 1 byte, 1 = 2 bytes, 2 = 3 bytes. Andere waarden geven
`Error, must be 0,1, or 2`.

**Voorbeeld:**

```text
set path.hash.mode 1
  -> OK
get path.hash.mode
  -> > 1
```

### loop.detect

Gooit flood-pakketten weg waarin de eigen hash al te vaak in het pad staat.
Alleen de repeater gebruikt het (`MyMesh.cpp` r.440–444); room server en sensor
slaan de waarde op maar doen er niets mee. Een andere waarde geeft
`Error, must be: off, minimal, moderate, or strict`.

**Voorbeeld:**

```text
set loop.detect minimal
  -> OK
get loop.detect
  -> > minimal
```

**NL:** `set loop.detect minimal`.

### txdelay

Factor voor het willekeurige wachtvenster voordat een flood-pakket wordt
doorgestuurd. Buiten 0–2: `Error, must be 0-2`.

**Voorbeeld:**

```text
get txdelay
  -> > 0.5
```

**NL:** standaard laten.

### direct.txdelay

Hetzelfde voor direct verkeer. De repeater staat op 0,3 (`MyMesh.cpp` r.880); de
officiële documentatie noemt 0,2. Door de float-weergave toont `get` op room
server en sensor `0.1999999`.

**Voorbeeld** *(room server)*:

```text
get direct.txdelay
  -> > 0.1999999
```

**NL:** standaard laten.

### rxdelay

Basis voor een vertraging bij het verwerken van zwak ontvangen flood-pakketten;
0 zet het uit. Buiten 0–20: `Error, must be 0-20`.

**Voorbeeld:**

```text
get rxdelay
  -> > 0.0
```

### dutycycle

Maximaal percentage zendtijd. De firmware rekent het om naar de airtime factor:
`af = 100 / dutycycle − 1`. Buiten 1–100: `ERROR: dutycycle must be 1-100`.

**Voorbeeld:**

```text
get dutycycle
  -> > 50.0%
set dutycycle 10
  -> OK - 10.0%
```

**NL:** `set dutycycle 10`.

### af

De airtime factor zelf, verouderd sinds v1.15.0. `set af` controleert geen
grenzen; bij de volgende start beperkt de firmware de waarde tot 0–9
(`CommonCLI.cpp` r.100). De duty cycle is ongeveer `100 / (af + 1)` procent.

**Voorbeeld:**

```text
set af 9
  -> OK
get af
  -> > 9.0
```

**NL:** `set af 9` op firmware ouder dan v1.15.0.

### int.thresh

Drempel voor lokale storing; 0 zet de controle uit. Het commando controleert de
waarde niet.

**Voorbeeld:**

```text
get int.thresh
  -> > 0
```

### agc.reset.interval

Interval in seconden waarop de AGC van de ontvanger wordt gereset; 0 zet het
uit. De waarde wordt naar beneden afgerond op een veelvoud van 4.

**Voorbeeld:**

```text
set agc.reset.interval 17
  -> OK - interval rounded to 16
```

### multi.acks

Meerdere ACK's per bericht. `set` controleert de waarde niet; bij de volgende
start beperkt de firmware hem tot 0–1 (`CommonCLI.cpp` r.106). De sensor
gebruikt de instelling niet.

**Voorbeeld:**

```text
set multi.acks 1
  -> OK
```

### flood.advert.interval

Hoe vaak de node een flood advert uitstuurt, in uren: 3–168, of 0 voor uit.
Anders `Error: interval range is 3-168 hours`. De officiële documentatie noemt
12 als standaard voor de repeater; de firmware zet 47 (`MyMesh.cpp` r.891).

**Voorbeeld:**

```text
set flood.advert.interval 49
  -> OK
```

**NL:** `set flood.advert.interval 49`.

### advert.interval

Hoe vaak de node een zero-hop advert uitstuurt, in minuten: 60–240, of 0 voor
uit. Anders `Error: interval range is 60-240 minutes`. De waarde wordt intern
gehalveerd opgeslagen, dus oneven waarden worden naar beneden afgerond.

**Voorbeeld:**

```text
set advert.interval 240
  -> OK
get advert.interval
  -> > 240
```

¹ Een nieuwe installatie zendt elke 2 minuten. Bij de eerste wijziging die wordt
opgeslagen zet de firmware dat op 0, omdat het onder de 60 minuten ligt
(`CommonCLI.cpp` r.196–198). De officiële documentatie noemt 0.

**NL:** `set advert.interval 240`.

### flood.max

Maximaal aantal hops voor elk flood-pakket. Boven 64: `Error, max 64`.

**Voorbeeld:**

```text
get flood.max
  -> > 64
```

### flood.max.unscoped

Hetzelfde voor flood-pakketten zonder scope (`MyMesh.cpp` r.433). De officiële
documentatie beschrijft een waarde `0xFF` die `flood.max` volgt; die logica
staat niet in deze commit. Zie
[Regio's en Scopes](../techniek/regions-and-scopes.md).

**Voorbeeld:**

```text
set flood.max.unscoped 3
  -> OK
```

¹ De sensor zet deze waarde niet en gebruikt hem niet; `get` toont daar `0`.

**NL:** bijvoorbeeld `set flood.max.unscoped 3`, zie
[Aan de Slag](../gebruik/getting-started.md).

### flood.max.advert

Hetzelfde voor adverts (`MyMesh.cpp` r.434).

**Voorbeeld:**

```text
get flood.max.advert
  -> > 8
```

¹ Zie `flood.max.unscoped`.

**NL:** `8`, de standaard.

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.h)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
