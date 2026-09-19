# Statistieken

*CORE · RADIO · PAKKETTEN · RESET*

Drie commando's geven tellers en meetwaarden als een JSON-object, één zet de
tellers terug. Alle drie de rollen gebruiken dezelfde opmaak uit
`src/helpers/StatsFormatHelper.h`. De drie leescommando's werken alleen via de
seriële console.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `src/helpers/StatsFormatHelper.h`,
> `examples/simple_repeater/MyMesh.cpp`,
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
| `clear stats` | | — | | `CommonCLI.cpp` r.295 |
| `stats-core` | | — | ja | `CommonCLI.cpp` r.474 |
| `stats-radio` | | — | ja | `CommonCLI.cpp` r.472 |
| `stats-packets` | | — | ja | `CommonCLI.cpp` r.470 |

## Commando's

### clear stats

Zet de tellers van de node terug.

**Voorbeeld:**

```text
clear stats
  -> (OK - stats reset)
```

### stats-core

Batterijspanning in mV, uptime in seconden, foutvlaggen en de lengte van de
zendwachtrij (`StatsFormatHelper.h` r.12–13).

**Voorbeeld** *(formaat; de waarden hangen af van de node)*:

```text
stats-core
  -> {"battery_mv":<mV>,"uptime_secs":<s>,"errors":<n>,"queue_len":<n>}
```

### stats-radio

Ruisvloer, RSSI en SNR van het laatste pakket, en de zend- en ontvangsttijd in
seconden (`StatsFormatHelper.h` r.27–28). De SNR heeft twee decimalen.

**Voorbeeld** *(formaat)*:

```text
stats-radio
  -> {"noise_floor":<dBm>,"last_rssi":<dBm>,"last_snr":<dB>,"tx_air_secs":<s>,"rx_air_secs":<s>}
```

### stats-packets

Pakkettellers: ontvangen, verzonden, flood en direct per richting, en
ontvangstfouten (`StatsFormatHelper.h` r.44–45).

**Voorbeeld** *(formaat)*:

```text
stats-packets
  -> {"recv":<n>,"sent":<n>,"flood_tx":<n>,"direct_tx":<n>,"flood_rx":<n>,"direct_rx":<n>,"recv_errors":<n>}
```

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/StatsFormatHelper.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/StatsFormatHelper.h)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
