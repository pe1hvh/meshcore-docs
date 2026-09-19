# Radio

*FREQUENTIE · BANDBREEDTE · SF · CR · ZENDVERMOGEN*

De radioparameters van de node: frequentie, bandbreedte, spreading factor en
coding rate, het zendvermogen van de chip en de ontvangst-versterking.
Wijzigingen in de radioparameters gaan pas in na een herstart; `tempradio`
probeert ze tijdelijk uit.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.17.1, commit `d929643`, 14 augustus 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `platformio.ini`,
> `examples/simple_repeater/MyMesh.cpp`, `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, `src/helpers/TxtDataHelpers.cpp`, en de
> officiële `docs/cli_commands.md`. Regelnummers verwijzen naar deze commit en
> zijn te reproduceren met
> [`tools/cli-commands.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/cli-commands.py).

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `get radio` / `set radio <freq>,<bw>,<sf>,<cr>` | | `869.618,62.5,8,5` | | `CommonCLI.cpp` r.588, r.859 |
| `get tx` / `set tx <dbm>` | | per board, terugvalwaarde 20 | | `CommonCLI.cpp` r.708, r.898 |
| `tempradio <freq>,<bw>,<sf>,<cr>,<timeout_mins>` | | — | | `CommonCLI.cpp` r.241 |
| `get freq` / `set freq <frequency>` | | `869.618` | alleen `set` | `CommonCLI.cpp` r.713, r.900 |
| `get radio.rxgain` / `set radio.rxgain <on\|off>` | `effect: repeater, room server` | R/RS `on` ¹ · S `off` | | `CommonCLI.cpp` r.535, r.845 |
| `get cad` / `set cad <on\|off>` | | `off` | | `CommonCLI.cpp` r.470, r.818 |
| `get radio.fem.rxgain` / `set radio.fem.rxgain <on\|off>` | board met regelbare FEM | `on` | | `CommonCLI.cpp` r.544, r.847 |
| `get radio.fem.txgain` / `set radio.fem.txgain <on\|off>` | board met regelbare FEM | `off` | | `CommonCLI.cpp` r.566, r.853 |
| `get extra.sf` / `set extra.sf <sf>[,<sf>…]` | `build flag` (`set`) | — | | `CommonCLI.cpp` r.780, r.976 |

De standaard `869.618,62.5,8,5` komt uit `platformio.ini` r.29–31 (frequentie,
bandbreedte, SF) en de terugvalwaarde `LORA_CR 5`; geen enkele variant
overschrijft ze. De officiële documentatie noemt `869.525,250,11,5`. Een
ongewijzigde build staat dus op **SF8**, terwijl het Nederlandse netwerk SF7
gebruikt.

## Commando's

### radio

Frequentie in MHz (150–2500), bandbreedte in kHz (7–500), SF (5–12) en CR (5–8).
Buiten die grenzen is het antwoord `Error, invalid radio params`. `get radio`
toont de frequentie met de float-weergave van de firmware, daarom `869.6179809`
(`TxtDataHelpers.cpp` r.52–130).

**Voorbeeld:**

```text
get radio
  -> > 869.6179809,62.5,8,5
set radio 869.618,62.5,7,5
  -> OK - reboot to apply
```

**NL:** `set radio 869.618,62.5,7,5`, zie
[Aan de Slag](../usage/getting-started.md). Het netwerk is in mei 2026
overgestapt op SF7; een node op SF8 hoort de rest niet.

### tx

Zendvermogen van de LoRa-chip in dBm. Het gaat direct in. `set tx` controleert
geen grenzen; bij de volgende start beperkt de firmware de waarde tot −9…30
(`CommonCLI.cpp` r.116). Een versterker op het board komt daar nog bovenop.

**Voorbeeld:**

```text
set tx 20
  -> OK
get tx
  -> > 20
```

**NL:** zie [Regelgeving & Duty Cycle](../usage/regulations.md) voor het
verschil tussen zendvermogen en uitgestraald vermogen (ERP).

### tempradio

Zet de radioparameters tijdelijk, voor het opgegeven aantal minuten. Niets wordt
opgeslagen. De grenzen zijn 150–2500 MHz, 7–500 kHz, SF 5–12, CR 5–8 en een tijd
groter dan 0; anders `Error, invalid params`. De officiële documentatie noemt
300–2500 MHz en 7,8–500 kHz.

**Voorbeeld:**

```text
tempradio 869.618,62.5,7,5,30
  -> OK - temp params for 30 mins
```

### freq

Alleen de frequentie. `set freq` werkt alleen via de seriële console en gaat in
na een herstart.

**Voorbeeld:**

```text
set freq 869.618
  -> OK - reboot to apply
get freq
  -> > 869.6179809
```

**NL:** 869,618 MHz, zie [Aan de Slag](../usage/getting-started.md). Dat is
ook de build-standaard.

### radio.rxgain

Boosted gain van de ontvanger. Tot v1.16.0 bestond het commando alleen in
builds met `USE_SX1262`, `USE_SX1268` of `USE_LR1110`; sinds v1.17.1 staat het
er altijd in en antwoordt een board dat het niet kan met `Error: unsupported`.
Repeater en room server passen de instelling toe, bij het opstarten en direct na
`set` (`simple_repeater/MyMesh.cpp` r.981, r.1080,
`simple_room_server/MyMesh.cpp` r.727). De sensor doet er niets mee. De
officiële documentatie noemt `on` als standaard voor alle rollen.

**Voorbeeld:**

```text
set radio.rxgain on
  -> OK
get radio.rxgain
  -> > on
```

¹ Voor SX1262/SX1268-builds, tenzij `SX126X_RX_BOOSTED_GAIN` iets anders zegt
(`simple_repeater/MyMesh.cpp` r.927–933, `simple_room_server/MyMesh.cpp`
r.677–683). In LR1110-builds zetten ze de waarde niet en is hij `off`. De room
server zette hem tot v1.16.0 ook niet; dat is met v1.17.1 gelijkgetrokken met de
repeater.

### cad

Hardwarematige Channel Activity Detection vóór het zenden. `on` zet het aan,
elke andere waarde uit. Alle drie de rollen zetten de standaard op `off`
(`simple_repeater/MyMesh.cpp` r.909, `simple_room_server/MyMesh.cpp` r.667,
`simple_sensor/SensorMesh.cpp` r.731). Volgens de officiële documentatie staat
het los van `int.thresh`. Dit is geen gecertificeerde LBT; de duty-cycle-limiet
blijft gelden, zie [Regelgeving & Duty Cycle](../usage/regulations.md).

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

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/d929643/platformio.ini)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `src/helpers/TxtDataHelpers.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/TxtDataHelpers.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/d929643/docs/cli_commands.md)
