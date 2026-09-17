# Companion: CLI Rescue

*CONSOLE VOOR NOODGEVALLEN · BLE-PINCODE · BESTANDSSYSTEEM*

De companion-firmware gebruikt geen `CommonCLI`; zijn instellingen lopen via het
companion-protocol, zie [De companion-interface](../companion/introduction.md).
Wel heeft hij een console voor noodgevallen op de seriële poort, met zeven
commando's om de BLE-pincode te zetten, het bestandssysteem te bekijken of te
wissen, en te herstarten.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `examples/companion_radio/MyMesh.cpp`,
> `examples/companion_radio/ui-tiny/UITask.cpp`,
> `examples/companion_radio/ui-new/UITask.cpp`,
> `examples/companion_radio/ui-orig/UITask.cpp`, en de officiële
> `docs/cli_commands.md`. Regelnummers verwijzen naar deze commit en zijn te
> reproduceren met [`tools/cli-commands.py`](../../tools/cli-commands.py).

## Starten

Druk de knop lang in binnen 8 seconden na het opstarten (`ui-tiny/UITask.cpp`
r.766–767, `ui-new/UITask.cpp` r.866–867, `ui-orig/UITask.cpp` r.451–452). Dat
kan dus alleen op een board met een knop en een UI. De console meldt
`========= CLI Rescue =========` (`examples/companion_radio/MyMesh.cpp` r.2006)
en herhaalt elk getypt teken. Er komt geen `  -> ` voor een antwoord; de
antwoorden beginnen meestal met twee spaties. Een onbekend commando geeft
`  Error: unknown command`.

## Overzicht

| Commando | Werking | Bron |
|---|---|---|
| `set pin <nnnnnn>` | BLE-pincode vastzetten | r.2028 |
| `rebuild` | Bestandssysteem wissen en identiteit, instellingen, contacten en kanalen opnieuw wegschrijven | r.2035 |
| `erase` | Bestandssysteem wissen | r.2046 |
| `ls [pad]` | Bestanden tonen | r.2053 |
| `cat <pad>` | Bestand tonen, in hex | r.2101 |
| `rm <pad>` | Bestand verwijderen | r.2138 |
| `reboot` | Herstarten | r.2171 |

## Commando's

### set pin

Zet een vaste BLE-pincode van zes cijfers. Met `0` kiest de firmware zelf: op
een board met scherm en de standaardcode 123456 een willekeurige code per
sessie, anders `BLE_PIN_CODE` (r.939–950). Een andere instelling dan `pin` geeft
`  Error: unknown config: <naam>`.

**Voorbeeld:**

```text
set pin 123456
  > pin is now 123456
```

### rebuild

Formatteert het bestandssysteem en schrijft daarna de identiteit, de
instellingen, de contacten en de kanalen uit het geheugen terug. Mislukt het
formatteren: `  Error: erase failed`.

**Voorbeeld:**

```text
rebuild
  > erase and rebuild done
```

### erase

Formatteert het bestandssysteem zonder iets terug te schrijven.

**Voorbeeld:**

```text
erase
  > erase done
```

> [!WARNING]
> Na `erase` is de identiteit van de companion weg. Gebruik `rebuild` als je die
> wilt houden.

### ls

Toont mappen en bestanden. Een pad dat met `UserData/` begint verwijst naar het
gewone bestandssysteem, `ExtraFS/` naar het tweede. Elke regel begint met
`[dir]` of `[file]`; bij een bestand staat de grootte erachter.

**Voorbeeld:**

```text
ls UserData/
Listing files in /
[dir]  UserData//<map>
[file] UserData//<bestand> (<n> bytes)
```

### cat

Toont de inhoud van een bestand als hex. Het pad moet met `UserData/` of
`ExtraFS/` beginnen, anders
`Invalid path provided, must start with UserData/ or ExtraFS/`.

**Voorbeeld:**

```text
cat notes.txt
Invalid path provided, must start with UserData/ or ExtraFS/
```

### rm

Verwijdert een bestand. Een leeg pad of `/` geeft `Invalid path provided`; een
bestand dat niet weg kan `Failed to remove file`. Het voorbeeld gebruikt het
bestand uit het commentaar in de broncode (r.2139).

**Voorbeeld:**

```text
rm UserData/adv_blobs
File removed
```

### reboot

Herstart de companion. Geen antwoord.

**Voorbeeld:**

```text
reboot
```

Stuur je vanuit de companion-app een commando naar een repeater, dan voert de
repeater het uit. Daarvoor gelden de andere pagina's van deze sectie.

## Bronnen

- [MeshCore firmware — `examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/MyMesh.cpp)
- [MeshCore firmware — `examples/companion_radio/ui-tiny/UITask.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/ui-tiny/UITask.cpp)
- [MeshCore firmware — `examples/companion_radio/ui-new/UITask.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/ui-new/UITask.cpp)
- [MeshCore firmware — `examples/companion_radio/ui-orig/UITask.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/ui-orig/UITask.cpp)
