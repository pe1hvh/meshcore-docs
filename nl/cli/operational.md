# Bediening

*HERSTARTEN · KLOK · ADVERTS · OTA · WISSEN*

Commando's die iets met de node dóén in plaats van een instelling te veranderen:
herstarten, uitzetten, de klok zetten, een advert uitsturen, een firmware-update
starten en het bestandssysteem wissen. Geen van deze commando's heeft een
standaardwaarde.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/CommonCLI.cpp`, `src/MeshCore.h`, `src/helpers/ESP32Board.cpp`,
> `src/helpers/NRF52Board.cpp`, en de officiële `docs/cli_commands.md`.
> Regelnummers verwijzen naar deze commit en zijn te reproduceren met
> [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Overzicht

De markeringen in de kolom **Rol** zijn uitgelegd in de
[CLI-referentie](introduction.md). Een lege cel betekent: werkt op repeater,
room server en sensor.

| Commando | Rol | Standaard | Alleen serieel | Bron |
|---|---|---|---|---|
| `reboot` | | — | | `CommonCLI.cpp` r.218 |
| `poweroff` / `shutdown` | | — | | `CommonCLI.cpp` r.216 |
| `clkreboot` | | — | | `CommonCLI.cpp` r.220 |
| `clock` | | — | | `CommonCLI.cpp` r.246 |
| `clock sync` | | — | | `CommonCLI.cpp` r.232 |
| `time <epoch_seconds>` | | — | | `CommonCLI.cpp` r.250 |
| `advert` | | — | | `CommonCLI.cpp` r.228 |
| `advert.zerohop` | | — | | `CommonCLI.cpp` r.224 |
| `start ota` | | — | | `CommonCLI.cpp` r.242 |
| `erase` | | — | ja | `CommonCLI.cpp` r.302 |

## Commando's

### reboot

Herstart de node meteen. Er komt geen antwoord, omdat `_board->reboot()` niet
terugkeert.

**Voorbeeld:**

```text
reboot
```

**NL:** geen afspraak.

### poweroff / shutdown

Zet de node uit. De twee namen doen hetzelfde. Ook hier komt geen antwoord.

**Voorbeeld:**

```text
poweroff
```

**NL:** geen afspraak.

### clkreboot

Zet de klok op `1715770351` (15 mei 2024, 10:52:31 UTC) en herstart. Dat is de
uitweg als de klok in de toekomst staat: `time` en `clock sync` weigeren een
tijd die vóór de huidige ligt. Geen antwoord.

**Voorbeeld:**

```text
clkreboot
```

**NL:** geen afspraak.

### clock

Toont de huidige tijd in UTC, in de vorm `uu:mm - d/m/jjjj UTC`.

**Voorbeeld** *(klok op `1785412800`)*:

```text
clock
  -> 12:00 - 30/7/2026 UTC
```

**NL:** geen afspraak.

### clock sync

Zet de klok op de tijd van de afzender plus één seconde, maar alleen als die
later is dan de eigen klok. Over de seriële console is de afzendertijd altijd
`0`, dus daar geeft het commando altijd een fout. Het werkt alleen op afstand,
vanuit een app.

**Voorbeeld:**

```text
clock sync
  -> ERR: clock cannot go backwards
```

Op afstand, met afzendertijd `1785412800` en een klok die achterloopt, is het
antwoord `OK - clock set: 12:00 - 30/7/2026 UTC`.

**NL:** geen afspraak.

### time

Zet de klok op een Unix-tijd, maar alleen vooruit. Een tijd die niet later is
dan de huidige geeft `(ERR: clock cannot go backwards)` — met haakjes, anders
dan bij `clock sync`.

**Voorbeeld:**

```text
time 1785412800
  -> OK - clock set: 12:00 - 30/7/2026 UTC
```

**NL:** geen afspraak.

### advert

Stuurt een flood advert, 1500 ms na het antwoord zodat dat eerst weg kan. De
vergelijking kijkt alleen naar de eerste zes tekens; `advert.zerohop` wordt
daarom eerder afgevangen.

**Voorbeeld:**

```text
advert
  -> OK - Advert sent
```

**NL:** geen afspraak.

### advert.zerohop

Stuurt een zero-hop advert, alleen voor directe buren, eveneens na 1500 ms.

**Voorbeeld:**

```text
advert.zerohop
  -> OK - zerohop advert sent
```

**NL:** geen afspraak.

### start ota

Start een firmware-update over de lucht. Wat er gebeurt hangt af van het board.
Op ESP32 start een repeater of room server een WiFi-toegangspunt `MeshCore-OTA`
en antwoordt met `Started: http://<adres>/update` (`ESP32Board.cpp` r.13–16),
tenzij de build `DISABLE_WIFI_OTA` zet. Op nRF52 start BLE-DFU en is het
antwoord `OK - mac: ` met het BLE-adres (`NRF52Board.cpp` r.319–362). Andere
boards ondersteunen het niet (`MeshCore.h` r.66) en antwoorden `Error`.

**Voorbeeld** *(board zonder OTA)*:

```text
start ota
  -> Error
```

**NL:** geen afspraak.

### erase

Formatteert het bestandssysteem. Alleen via de seriële console.

**Voorbeeld:**

```text
erase
  -> File system erase: OK
```

> [!WARNING]
> Dit wist alles wat de node heeft opgeslagen, inclusief instellingen, regio's
> en de ACL. Er is geen bevestiging.

**NL:** geen afspraak.

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore firmware — `src/helpers/ESP32Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ESP32Board.cpp)
- [MeshCore firmware — `src/helpers/NRF52Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/NRF52Board.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
