# Radio

*FREQUENTIE · BANDBREEDTE · SF · CR · ZENDVERMOGEN*

De radioparameters van de node: frequentie, bandbreedte, spreading factor en
coding rate, het zendvermogen van de chip en de ontvangst-versterking.
Wijzigingen in de radioparameters gaan pas in na een herstart; `tempradio`
probeert ze tijdelijk uit.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `platformio.ini`,
> `examples/simple_repeater/MyMesh.cpp`, `src/helpers/TxtDataHelpers.cpp`, en de
> officiële `docs/cli_commands.md`. Regelnummers verwijzen naar deze commit en
> zijn te reproduceren met
> [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `get radio` / `set radio <freq>,<bw>,<sf>,<cr>` | | `869.618,62.5,8,5` | | `CommonCLI.cpp` r.571, r.808 |
| `get tx` / `set tx <dbm>` | | per board, terugvalwaarde 20 | | `CommonCLI.cpp` r.691, r.847 |
| `tempradio <freq>,<bw>,<sf>,<cr>,<timeout_mins>` | | — | | `CommonCLI.cpp` r.274 |
| `get freq` / `set freq <frequency>` | | `869.618` | alleen `set` | `CommonCLI.cpp` r.696, r.849 |
| `get radio.rxgain` / `set radio.rxgain <on\|off>` | `build flag` · `effect: repeater` | R `on` ¹ · RS/S `off` | | `CommonCLI.cpp` r.565, r.805 |

De standaard `869.618,62.5,8,5` komt uit `platformio.ini` r.28–30 (frequentie,
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
[Aan de Slag](../gebruik/getting-started.md). Het netwerk is in mei 2026
overgestapt op SF7; een node op SF8 hoort de rest niet.

### tx

Zendvermogen van de LoRa-chip in dBm. Het gaat direct in. `set tx` controleert
geen grenzen; bij de volgende start beperkt de firmware de waarde tot −9…30
(`CommonCLI.cpp` r.105). Een versterker op het board komt daar nog bovenop.

**Voorbeeld:**

```text
set tx 20
  -> OK
get tx
  -> > 20
```

**NL:** zie [Regelgeving & Duty Cycle](../gebruik/regulations.md) voor het
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

**NL:** 869,618 MHz, zie [Aan de Slag](../gebruik/getting-started.md). Dat is
ook de build-standaard.

### radio.rxgain

Boosted gain van de ontvanger. Bestaat alleen in builds met `USE_SX1262`,
`USE_SX1268` of `USE_LR1110`. Alleen de repeater past de instelling toe, bij het
opstarten en direct na `set` (`MyMesh.cpp` r.965, r.1063). De officiële
documentatie noemt `on` als standaard voor alle rollen.

**Voorbeeld:**

```text
set radio.rxgain on
  -> OK
get radio.rxgain
  -> > on
```

¹ Voor SX1262/SX1268-builds, tenzij `SX126X_RX_BOOSTED_GAIN` iets anders zegt
(`MyMesh.cpp` r.913–919). In LR1110-builds zet de repeater de waarde niet en is
hij `off`.

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `src/helpers/TxtDataHelpers.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/TxtDataHelpers.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
