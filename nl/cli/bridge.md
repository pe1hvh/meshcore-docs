# Bridge

*RS232 · ESP-NOW · VERTRAGING · BRON*

Een bridge geeft pakketten door over een tweede weg naast LoRa: RS232 of
ESP-NOW. Behalve `get bridge.type` bestaan deze commando's alleen in een build
met `WITH_RS232_BRIDGE` of `WITH_ESPNOW_BRIDGE`, en alleen de repeater leidt
daaruit `WITH_BRIDGE` af (`simple_repeater/MyMesh.h` r.16–24).

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `examples/simple_repeater/MyMesh.h`,
> `examples/simple_repeater/MyMesh.cpp`, en de officiële `docs/cli_commands.md`.
> Regelnummers verwijzen naar deze commit en zijn te reproduceren met
> [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `get bridge.type` | | — | | `CommonCLI.cpp` r.856 |
| `get bridge.enabled` / `set bridge.enabled <on\|off>` | `alleen repeater` · `build flag` | `on` | | `CommonCLI.cpp` r.701, r.867 |
| `get bridge.delay` / `set bridge.delay <ms>` | `alleen repeater` · `build flag` | `500` | | `CommonCLI.cpp` r.706, r.869 |
| `get bridge.source` / `set bridge.source <rx\|tx>` | `alleen repeater` · `build flag` | `logTx` | | `CommonCLI.cpp` r.715, r.871 |
| `get bridge.baud` / `set bridge.baud <rate>` | `alleen repeater` · `build flag` | `115200` | | `CommonCLI.cpp` r.721, r.875 |
| `get bridge.channel` / `set bridge.channel <1-14>` | `alleen repeater` · `build flag` | `1` | | `CommonCLI.cpp` r.733, r.879 |
| `get bridge.secret` / `set bridge.secret <secret>` | `alleen repeater` · `build flag` | `LVSITANOS` | | `CommonCLI.cpp` r.743, r.881 |

## Commando's

### bridge.type

Welk type bridge in de build zit: `rs232`, `espnow` of `none`.

**Voorbeeld:**

```text
get bridge.type
  -> > none
```

### bridge.enabled

Zet de bridge aan of uit, direct. De firmware zet de standaard op `on`
(`MyMesh.cpp` r.898); de officiële documentatie noemt `off`.

**Voorbeeld:**

```text
get bridge.enabled
  -> > on
set bridge.enabled off
  -> OK
```

### bridge.delay

Vertraging in milliseconden voor pakketten via de bridge, 0–10000. Anders
`Error: delay must be between 0-10000 ms`.

**Voorbeeld:**

```text
set bridge.delay 1000
  -> OK
```

### bridge.source

Of de bridge ontvangen (`logRx`) of verzonden (`logTx`) pakketten doorgeeft.
`set` kijkt alleen of de waarde met `rx` begint; al het andere wordt `logTx`. De
officiële documentatie noemt `logRx` en `logTx` als waarden, maar
`set bridge.source logRx` zet dus **logTx**.

**Voorbeeld:**

```text
set bridge.source rx
  -> OK
get bridge.source
  -> > logRx
```

### bridge.baud

Alleen RS232. Snelheid van 9600 tot 115200 (`BRIDGE_MAX_BAUD`, `CommonCLI.cpp`
r.9); de bridge herstart direct.

**Voorbeeld:**

```text
set bridge.baud 57600
  -> OK
```

### bridge.channel

Alleen ESP-NOW. WiFi-kanaal 1–14; anders `Error: channel must be between 1-14`.

**Voorbeeld:**

```text
set bridge.channel 6
  -> OK
```

### bridge.secret

Alleen ESP-NOW. Sleutel voor de XOR-versleuteling van bridge-pakketten, maximaal
15 tekens (`CommonCLI.h` r.53). De firmware zet `LVSITANOS` (`MyMesh.cpp`
r.904); de officiële documentatie zegt dat de standaard per board verschilt.

**Voorbeeld:**

```text
get bridge.secret
  -> > LVSITANOS
```

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.h)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
