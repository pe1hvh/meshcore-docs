# CLI-referentie

*COMMANDOREGEL · ROLLEN · STANDAARDWAARDEN · AFWIJKINGEN*

Repeaters, room servers en sensoren hebben een commandoregel, via de seriële
console of op afstand vanuit een app. Deze sectie beschrijft elk commando dat de
firmware kent, per categorie: voor welke rol het werkt, de standaardwaarde, een
voorbeeld en de Nederlandse invulling. De companion heeft zo'n commandoregel
niet, alleen een console voor noodgevallen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `src/helpers/CommonCLI.h`,
> `examples/simple_repeater/MyMesh.cpp`, `examples/simple_repeater/main.cpp`,
> `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, `examples/simple_sensor/main.cpp`,
> `platformio.ini`, en de officiële `docs/cli_commands.md`. Regelnummers
> verwijzen naar deze commit en zijn te reproduceren met
> [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Waar de commando's vandaan komen

Repeater, room server en sensor gebruiken dezelfde commandoverwerking:
`src/helpers/CommonCLI.cpp`. Daarvóór handelt elke rol in zijn eigen
`handleCommand()` een paar commando's af: `setperm` en `get acl` bij alle drie,
`discover.neighbors` bij de repeater, en `io` en `magic` bij de sensor.
`CommonCLI` kijkt nergens naar de rol. Verschillen tussen rollen ontstaan op
twee andere plekken: callbacks die per rol anders zijn ingevuld, en instellingen
die alleen sommige rollen lezen.

De companion gebruikt `CommonCLI` niet. Zijn instellingen lopen via het
companion-protocol, zie [De companion-interface](../companion/introduction.md).
Wel is er een console voor noodgevallen:
[Companion: CLI Rescue](companion-rescue.md).

## Hoe je een commando geeft

Via de seriële console typ je het commando en druk je op Enter. De repeater zet
`  -> ` voor elk antwoord (`simple_repeater/main.cpp` r.127); een antwoord is
hoogstens 159 tekens (r.124). Bij een antwoord over meerdere regels krijgt
alleen de eerste regel dat voorvoegsel.

Op afstand stuurt een beheerder hetzelfde commando vanuit een app, zie
[Remote Bediening](../techniek/remote-control.md) en
[Requests en CLI](../techniek/roomserver/requests-and-cli.md). Dan is de
afzendertijd niet `0`, en daardoor werken de commando's in de kolom **Alleen
serieel** niet. Een commando mag beginnen met een voorvoegsel van drie tekens
zoals `01|`; de node zet dat terug voor het antwoord (repeater r.1211, room
server r.897, sensor r.382).

## Markeringen

Elke categoriepagina begint met een overzichtstabel. De kolom **Rol** is leeg
als het commando op repeater, room server en sensor hetzelfde werkt. Anders
staat er een van deze markeringen:

| Markering | Betekenis |
|---|---|
| `alleen <rol>` | Alleen die rol voert het commando uit; de andere rollen kennen het niet of antwoorden met `not supported` |
| `niet <rol>` | Die rol accepteert het commando, maar het werkt daar niet |
| `effect: <rol>` | Elke rol accepteert en bewaart de instelling, maar alleen de genoemde rol gebruikt hem |
| `build flag` | Het commando bestaat alleen in een build met een bepaalde optie; de pagina noemt welke |

Of een rol een instelling gebruikt, is vastgesteld door te zoeken waar de rol de
instelling buiten zijn constructor leest. In de kolom **Standaard** staat R voor
repeater, RS voor room server en S voor sensor. De kolom **Alleen serieel** is
gevuld als de firmware controleert dat het commando van de seriële console komt.

## De categorieën

- [Bediening](operational.md) — herstarten, klok, adverts, OTA, wissen
- [Buren](neighbors.md) — de burenlijst van de repeater
- [Statistieken](statistics.md) — tellers en meetwaarden
- [Logging](logging.md) — het ontvangstlog
- [Informatie](info.md) — firmwareversie en board
- [Radio](radio.md) — frequentie, SF, zendvermogen
- [Systeem](system.md) — naam, locatie, sleutels, wachtwoorden
- [Routing](routing.md) — doorsturen, duty cycle, adverts, hop-limieten
- [ACL](acl.md) — rechten van clients
- [Regio's](regions.md) — regioboom en scope
- [GPS](gps.md) — GPS-ontvanger
- [Sensoren](sensors.md) — sensorinstellingen, GPIO
- [Bridge](bridge.md) — RS232- en ESP-NOW-bridge
- [Energiebeheer (nRF52)](power-management.md) — nRF52-voeding en bootloader
- [Companion: CLI Rescue](companion-rescue.md) — de console voor noodgevallen van de companion
- [Na de gepinde commit](after-pinned-commit.md) — commando's die alleen op `main` bestaan

## Standaardwaarden per rol

Deze waarden zet de firmware in de constructor van elke rol
(`simple_repeater/MyMesh.cpp` r.876–925, `simple_room_server/MyMesh.cpp`
r.632–669, `simple_sensor/SensorMesh.cpp` r.710–736). Ze gelden voor een vers
geflashte node; heeft de node al een instellingenbestand, dan overschrijft
`loadPrefs()` ze (`CommonCLI.cpp` r.40–130). Een ⚠ betekent dat de officiële
documentatie iets anders noemt.

| Instelling | Repeater | Room server | Sensor |
|---|---|---|---|
| `radio` ⚠ | `869.618,62.5,8,5` | idem | idem |
| `tx` | per board, terugvalwaarde `20` | per board, terugvalwaarde `20` | per board, terugvalwaarde `20` |
| `radio.rxgain` ⚠ | `on` (SX1262/SX1268) | `off` | `off` |
| `name` | `repeater` | `Test BBS` | `sensor` |
| `lat` / `lon` | `0.0` | `0.0` | `0.0` |
| `password` | `password` | `password` | `password` |
| `guest.password` ⚠ | leeg | `ROOM_PASSWORD` of leeg | leeg |
| `owner.info` | leeg | leeg | leeg |
| `adc.multiplier` | `0.0` | `0.0` | `0.0` |
| `powersaving` | `off` | `off` | `off` |
| `repeat` ⚠ | `on` | `off` | `off` |
| `path.hash.mode` | `0` | `0` | `0` |
| `loop.detect` | `off` | `off` | `off` |
| `txdelay` | `0.5` | `0.5` | `0.5` |
| `direct.txdelay` ⚠ | `0.3` | `0.2` | `0.2` |
| `rxdelay` | `0.0` | `0.0` | `0.0` |
| `dutycycle` / `af` | `50` / `1.0` | `50` / `1.0` | `50` / `1.0` |
| `int.thresh` | `0` | `0` | `0` |
| `agc.reset.interval` | `0` | `0` | `0` |
| `multi.acks` | `0` | `0` | `0` |
| `flood.advert.interval` ⚠ | `47` | `47` | `0` |
| `advert.interval` ⚠ | `2` → `0` | `2` → `0` | `2` → `0` |
| `flood.max` | `64` | `64` | `64` |
| `flood.max.unscoped` ⚠ | `64` | `64` | `0` |
| `flood.max.advert` | `8` | `8` | `0` |
| `allow.read.only` | `off` | `off` | `off` |
| `gps` / `gps advert` | `off` / `prefs` | `off` / `prefs` | `off` / `prefs` |
| `bridge.enabled` ⚠ | `on` | — | — |
| `bridge.delay` / `bridge.source` | `500` / `logTx` | — | — |
| `bridge.baud` / `bridge.channel` | `115200` / `1` | — | — |
| `bridge.secret` ⚠ | `LVSITANOS` | — | — |

`advert.interval` staat op 2 minuten tot de eerste opgeslagen wijziging en
daarna op 0; zie [Routing](routing.md). De naam is de terugvalwaarde van
`ADVERT_NAME`; de meeste builds zetten een eigen naam.

## Afwijkingen van de officiële documentatie

Deze referentie volgt de firmware. Waar `docs/cli_commands.md` op dezelfde
commit iets anders zegt, staat dat bij het commando. Het overzicht:

| Onderwerp | Officiële documentatie | Firmware op `03b6ef4` | Pagina |
|---|---|---|---|
| standaard `radio` | `869.525,250,11,5` | `869.618,62.5,8,5` | [Radio](radio.md) |
| standaard `radio.rxgain` | `on` | `on` alleen bij de repeater in SX1262/SX1268-builds | [Radio](radio.md) |
| grenzen `tempradio` | 300–2500 MHz, 7,8–500 kHz | 150–2500 MHz, 7–500 kHz | [Radio](radio.md) |
| `neighbors`, tweede veld | timestamp | seconden geleden | [Buren](neighbors.md) |
| `set prv.key` | 64 hextekens | 128 hextekens | [Systeem](system.md) |
| standaard `guest.password` | leeg | `ROOM_PASSWORD` op de room server, als die flag is gezet | [Systeem](system.md) |
| standaard `repeat` | `on` | `off` op room server en sensor | [Routing](routing.md) |
| standaard `direct.txdelay` | `0.2` | `0.3` op de repeater | [Routing](routing.md) |
| standaard `flood.advert.interval` | `12` (repeater) | `47` | [Routing](routing.md) |
| standaard `advert.interval` | `0` | `2`, na de eerste opgeslagen wijziging `0` | [Routing](routing.md) |
| `flood.max.unscoped` | `0xFF` volgt `flood.max` | geen `0xFF`-logica | [Routing](routing.md) |
| `setperm` zonder rechten | verwijdert de client | `Err - bad params`; verwijderen gaat met `0` | [ACL](acl.md) |
| `region list` | alleen serieel | ook op afstand | [Regio's](regions.md) |
| `region load <name> [flag]` | argumenten | argumenten worden genegeerd | [Regio's](regions.md) |
| standaard `bridge.enabled` | `off` | `on` | [Bridge](bridge.md) |
| waarden `bridge.source` | `logRx`, `logTx` | alleen een waarde die met `rx` begint zet `logRx` | [Bridge](bridge.md) |
| standaard `bridge.secret` | per board | `LVSITANOS` | [Bridge](bridge.md) |
| `bootloader.ver`, `pwrmgt.*` | onder *Bridge* | nRF52-platform | [Energiebeheer](power-management.md) |
| `io`, `magic` | ontbreken | sensorcommando's | [Sensoren](sensors.md) |

## Nederlandse invulling in het kort

De afspraken komen uit [Regelgeving & Duty Cycle](../gebruik/regulations.md) en
[Aan de Slag](../gebruik/getting-started.md). Bij elk commando staat de
invulling ook op de categoriepagina.

| Commando | Nederlandse invulling | Pagina |
|---|---|---|
| `set radio` | `869.618,62.5,7,5` | [Radio](radio.md) |
| `set dutycycle` | `10` | [Routing](routing.md) |
| `set af` | `9` (firmware ouder dan v1.15.0) | [Routing](routing.md) |
| `set loop.detect` | `minimal` | [Routing](routing.md) |
| `set flood.advert.interval` | `49` | [Routing](routing.md) |
| `set advert.interval` | `240` | [Routing](routing.md) |
| `set flood.max.advert` | `8` | [Routing](routing.md) |
| `set flood.max.unscoped` | bijvoorbeeld `3` | [Routing](routing.md) |
| `set txdelay` / `set direct.txdelay` | standaard | [Routing](routing.md) |
| `set repeat` | `on` op een repeater | [Routing](routing.md) |
| `region put` / `region default` | `eu` → `nl` → provincie | [Regio's](regions.md) |

## Nieuwere firmware

Commando's die na `03b6ef4` zijn toegevoegd staan apart, gemarkeerd als niet
geverifieerd tegen de pin: [Na de gepinde commit](after-pinned-commit.md).

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/CommonCLI.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.h)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_repeater/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/main.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/main.cpp)
- [MeshCore firmware — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
