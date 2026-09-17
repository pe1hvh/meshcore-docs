# Na de gepinde commit

*MAIN · CAD · FEM-VERSTERKING · EXTRA SF · ETHERNET*

De rest van deze sectie is gepind op `03b6ef4`. Op `main` zijn daarna nog
commando's bijgekomen. Ze staan hier apart, zodat wie nieuwere firmware draait
ze niet mist, zonder dat de pin wordt losgelaten.

> [!WARNING]
> **Niet geverifieerd tegen de pin.** Deze pagina is gecontroleerd tegen `main`
> op commit `0679dbe`, 24 augustus 2026 — bestanden `src/helpers/CommonCLI.cpp`,
> `src/helpers/nrf52/EthernetCLI.h`, `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, en de officiële
> `docs/cli_commands.md` op die commit. `main` verandert voortdurend; controleer
> dit tegen de firmware die je draait. De lijst is te reproduceren met
> [`tools/cli-commands.py`](../../tools/cli-commands.py) en een tweede checkout.

## Overzicht

| Commando | Bron op `0679dbe` | Voorwaarde | In officiële documentatie |
|---|---|---|---|
| `get cad` / `set cad <on\|off>` | `CommonCLI.cpp` r.470, r.818 | — | ja |
| `get radio.fem.rxgain` / `set radio.fem.rxgain <on\|off>` | `CommonCLI.cpp` r.544, r.847 | board met regelbare FEM | ja |
| `get radio.fem.txgain` / `set radio.fem.txgain <on\|off>` | `CommonCLI.cpp` r.566, r.853 | board met regelbare FEM | ja |
| `get extra.sf` / `set extra.sf <sf>[,<sf>…]` | `CommonCLI.cpp` r.780, r.976 | `set`: `USE_LR2021` | nee |
| `eth.status` | `nrf52/EthernetCLI.h` r.89 | `ETHERNET_ENABLED` | ja |

## Commando's

### cad

Hardwarematige Channel Activity Detection vóór het zenden. `on` zet het aan,
elke andere waarde uit. Alle drie de rollen zetten de standaard op `off`
(`simple_repeater/MyMesh.cpp` r.909, `simple_room_server/MyMesh.cpp` r.667,
`SensorMesh.cpp` r.731). Volgens de officiële documentatie staat het los van
`int.thresh`. Dit is geen gecertificeerde LBT; de duty-cycle-limiet blijft
gelden, zie [Regelgeving & Duty Cycle](../gebruik/regulations.md).

**Voorbeeld:**

```text
set cad on
  -> OK
get cad
  -> > on
```

### radio.fem.rxgain

De LNA van een externe front-end module (FEM), los van `radio.rxgain`. Zonder
regelbare FEM is het antwoord `Error: unsupported`; een andere waarde dan
`on`/`off` geeft `Error: state must be on or off`. Standaard `on` bij alle drie
de rollen (bijvoorbeeld `simple_room_server/MyMesh.cpp` r.684).

**Voorbeeld:**

```text
set radio.fem.rxgain on
  -> OK - LoRa FEM RX gain on
```

### radio.fem.txgain

Idem voor de zendversterking van de FEM. Standaard `off`
(`simple_room_server/MyMesh.cpp` r.685). De officiële documentatie noemt de
Station G3 als voorbeeld en waarschuwt dat de gekozen stand aan de lokale
limieten moet voldoen.

**Voorbeeld:**

```text
get radio.fem.txgain
  -> Error: unsupported
```

### extra.sf

Niet in de officiële documentatie. `set` bestaat alleen in builds met
`USE_LR2021` en neemt tot drie extra spreading factors, gescheiden door komma's;
het antwoord is `OK - extra SFs set` of `Invalid extra SF config`. `get` toont
de lijst of `No extra SF configured`.

**Voorbeeld:**

```text
get extra.sf
  -> No extra SF configured
```

### eth.status

Status van de Ethernet-verbinding op nRF52-boards met Ethernet. Het antwoord is
`ETH: not connected` of het IP-adres met de TCP-poort voor de CLI, standaard 23
(`nrf52/EthernetCLI.h` r.21).

**Voorbeeld:**

```text
eth.status
  -> ETH: not connected
```

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/0679dbe/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/nrf52/EthernetCLI.h`](https://github.com/meshcore-dev/MeshCore/blob/0679dbe/src/helpers/nrf52/EthernetCLI.h)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/0679dbe/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/0679dbe/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/0679dbe/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/0679dbe/docs/cli_commands.md)
