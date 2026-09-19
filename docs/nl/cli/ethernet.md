# Ethernet

*ETH.STATUS · RAK13800 · CH390 · TCP-POORT*

Een deel van de boards kan naast LoRa ook aan een bekabeld netwerk hangen. Op
die builds is er één extra commando, `eth.status`, en luistert de node op een
TCP-poort. Deze pagina beschrijft wat de firmware daar doet en welke builds het
betreft.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.17.1, commit `d929643`, 14 augustus 2026 — bestanden
> `src/helpers/nrf52/EthernetCLI.h`, `src/helpers/ethernet/EthernetInterface.h`,
> `src/helpers/ethernet/SerialEthernetInterface.h`,
> `src/helpers/ethernet/ch390/CH390EthernetInterface.h`,
> `variants/rak4631/platformio.ini`, `variants/thinknode_m7/platformio.ini`, en
> de officiële `docs/cli_commands.md`. Regelnummers verwijzen naar deze commit.

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md).

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `eth.status` | `build flag` `ETHERNET_ENABLED` · niet companion | — | | `nrf52/EthernetCLI.h` r.89 |

`eth.status` staat niet in `CommonCLI.cpp` maar in `nrf52/EthernetCLI.h`. Het
script [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py)
telt daarom `eth.status` als een commando dat wel in de officiële documentatie
staat en niet in de door het script gescande bestanden.

## Commando's

### eth.status

Status van de Ethernet-verbinding. Is de interface niet actief, dan is het
antwoord `ETH: not connected`; anders het via DHCP verkregen IP-adres met de
TCP-poort van de CLI (`nrf52/EthernetCLI.h` r.89–100). De poort is standaard 23
en is met de buildoptie `ETHERNET_TCP_PORT` te wijzigen (r.20–22). Na een
mislukte start probeert de firmware het elke 30 seconden opnieuw
(`ETHERNET_RETRY_INTERVAL_MS`, r.28).

**Voorbeeld:**

```text
eth.status
  -> ETH: not connected
```

Met verbinding ziet het antwoord er zo uit:

```text
eth.status
  -> ETH: 192.168.2.234:23
```

## Welke builds

De Ethernet-code wordt alleen meegecompileerd met de buildoptie
`ETHERNET_ENABLED`. In `03b6ef4` bestond die nog niet; hij is met v1.17.0
toegevoegd.

| Build | Hardware | Wat er luistert |
|---|---|---|
| `RAK_4631_repeater_ethernet` | RAK4631 met RAK13800 (W5100S) | CLI op TCP 23 |
| `RAK_4631_room_server_ethernet` | RAK4631 met RAK13800 (W5100S) | CLI op TCP 23 |
| `RAK_4631_companion_radio_ethernet` | RAK4631 met RAK13800 (W5100S) | companion-protocol op TCP 5000 |
| `ThinkNode_M7_companion_radio_ethernet` | ThinkNode M7 met CH390 | companion-protocol op TCP 5000 |

De companion heeft geen commandoregel; over Ethernet spreekt hij hetzelfde
binaire protocol als over BLE en USB, op poort 5000
(`ethernet/SerialEthernetInterface.h` r.5–6). Zie
[De companion-interface](../companion/introduction.md) en
[Transportlagen](../companion/technical/transports.md). Voor noodgevallen is er
[Companion: CLI Rescue](companion-rescue.md).

> [!WARNING]
> De CLI op TCP 23 kent geen versleuteling en geen aparte toegangscontrole: wie
> het IP-adres kan bereiken, krijgt dezelfde commandoregel als via de seriële
> console. Zet zo'n node niet zonder afscherming op een netwerk dat verder reikt
> dan je eigen LAN, en wijzig in elk geval het standaardwachtwoord, zie
> [Systeem](system.md).

## Bronnen

- [MeshCore firmware — `src/helpers/nrf52/EthernetCLI.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/nrf52/EthernetCLI.h)
- [MeshCore firmware — `src/helpers/ethernet/EthernetInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ethernet/EthernetInterface.h)
- [MeshCore firmware — `src/helpers/ethernet/SerialEthernetInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ethernet/SerialEthernetInterface.h)
- [MeshCore firmware — `src/helpers/ethernet/ch390/CH390EthernetInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ethernet/ch390/CH390EthernetInterface.h)
- [MeshCore firmware — `variants/rak4631/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/d929643/variants/rak4631/platformio.ini)
- [MeshCore firmware — `variants/thinknode_m7/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/d929643/variants/thinknode_m7/platformio.ini)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/d929643/docs/cli_commands.md)
