# Wijzigingen in v1.17.1

*RELEASE · DIFF · PIN · STAND VAN DE DOCUMENTATIE*

MeshCore v1.17.1 verscheen op 14 augustus 2026. Deze pagina zet op een rij wat
er verandert ten opzichte van de commit waarop deze documentatie tot nu toe was
gepind, welke hoofdstukken al opnieuw zijn getoetst en welke nog niet. Wat hier
staat is afgeleid uit de broncode zelf; de officiële release notes zijn als
index gebruikt, niet als bewijs.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.17.1, commit `d929643`, 14 augustus 2026, vergeleken met de vorige pin
> `03b6ef4` van 28 juli 2026. De vergelijking is te reproduceren met
> [`tools/diff-impact.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/diff-impact.py)
> en twee checkouts. De officiële aankondigingen staan op
> [blog.meshcore.io](https://blog.meshcore.io/2026/08/14/release-1-17-1).

## Wat er gepind is

De tags `companion-v1.17.1`, `repeater-v1.17.1` en `room-server-v1.17.1` wijzen
alle drie naar dezelfde commit, `d929643`. In die commit staat
`FIRMWARE_VERSION` op `v1.17.1`.

De vorige pin `03b6ef4` was geen release maar een momentopname van `main` van 28
juli 2026, waarin `FIRMWARE_VERSION` nog `v1.16.0` aangaf. De tag
`companion-v1.16.0` wijst naar een oudere commit, `07a3ca9` van 6 juni 2026.
Wat deze documentatie tot nu toe "v1.16.0" noemde, lag dus tussen de releases
v1.16.0 en v1.17.0 in. Een deel van wat de release notes van v1.17.0 opsommen,
zat daardoor al in de gepinde tekst.

## Wat er nieuw is

De vergelijking `03b6ef4` → `d929643` omvat 366 bestanden, met 12.026
toegevoegde en 1.783 verwijderde regels. Per onderwerp, met het bewijs in de
broncode:

| Onderwerp | Bewijs | Hoofdstuk |
|---|---|---|
| Configuratie in JSON, in `/prefs.json` | `src/helpers/ConfigSerializer.{h,cpp}` nieuw; `CommonCLI.cpp` r.30–47 | [CLI-referentie](../cli/introduction.md) |
| `get`/`set cad` — hardwarematige CAD vóór het zenden | `CommonCLI.cpp` r.470, r.818 | [Radio](../cli/radio.md) |
| `get`/`set radio.fem.rxgain` en `radio.fem.txgain` | `CommonCLI.cpp` r.544, r.566, r.847, r.853 | [Radio](../cli/radio.md) |
| `get`/`set extra.sf`, `set` alleen in `USE_LR2021`-builds | `CommonCLI.cpp` r.780, r.976 | [Radio](../cli/radio.md) |
| `radio.rxgain` niet langer achter een buildoptie; room server past hem nu ook toe | `CommonCLI.cpp` r.535; `simple_room_server/MyMesh.cpp` r.727 | [Radio](../cli/radio.md) |
| `eth.status` en Ethernet-ondersteuning (RAK13800, CH390, serieel) | `src/helpers/ethernet/`, `nrf52/EthernetCLI.h` nieuw | [Ethernet](../cli/ethernet.md) |
| Naam in de advert afgekapt op een UTF-8-codepointgrens | `AdvertDataHelpers.cpp` r.21, `UTF8Helpers.h` nieuw | [Systeem](../cli/system.md) |
| `room.post` — een room server plaatst zelf een bericht | `simple_room_server/MyMesh.cpp` r.977 | nog niet verwerkt |
| LR2021-radio | `src/helpers/radiolib/CustomLR2021.h` nieuw | nog niet verwerkt |
| Tot vier seriële interfaces naast elkaar op de companion | `src/helpers/MultiSerialInterface.h` nieuw | nog niet verwerkt |
| Hardwarecrypto (CC310) op nRF52 | `nRFCrypto` in vier bestanden, in `03b6ef4` nog nergens | nog niet verwerkt |
| Nieuw kleurenschema op de companion-UI | `UIColor` in 32 bestanden, in `03b6ef4` nog nergens | nog niet verwerkt |
| Negen nieuwe varianten: `heltec_tower_v2`, `heltec_rc32`, `heltec_v4_r8`, `meshnology_w12`, `meshtracker_x1`, `nibble_zero_connect`, `station_g3_esp32`, `thinknode_m7`, `thinknode_m9` | nieuwe mappen onder `variants/` | nog niet verwerkt |

Twee dingen uit de release notes van v1.17.0 zaten al ín de vorige pin en zijn
dus geen wijziging voor deze documentatie: `get pwrmgt.bootreason` en de
ST7735-schermdriver.

## Wat er vervallen is

Niets in de commandoregel. Tussen beide commits telt de firmware 40 commando's
in `CommonCLI.cpp`, in beide gevallen dezelfde 40. Het aantal instellingen
onder `get`/`set` gaat van 80 naar 88; alle 80 oude bestaan nog.

De vergelijking verwijdert drie bestanden, geen daarvan een functie van een
node:

| Bestand | Wat ermee gebeurde |
|---|---|
| `.vscode/extensions.json` | ontwikkelbestand, geen firmware |
| `variants/minewsemi_me25ls01/NullDisplayDriver.h` | verplaatst naar de gedeelde `src/helpers/ui/NullDisplayDriver.cpp` |
| `variants/wio-e5-mini/NullDisplayDriver.h` | idem |

Binnen deze documentatie is wél iets vervallen: de pagina *Na de gepinde
commit*. Die beschreef de commando's die alleen op `main` bestonden —
`cad`, `radio.fem.rxgain`, `radio.fem.txgain`, `extra.sf` en `eth.status`. Ze
horen alle vijf bij v1.17.1 en staan nu op [Radio](../cli/radio.md) en
[Ethernet](../cli/ethernet.md).

## Wat nog op de oude pin staat

> [!WARNING]
> De documentatie draagt op dit moment **twee pins**. Alleen de hoofdstukken in
> de tabel hieronder zijn tegen `d929643` getoetst. Alle andere hoofdstukken
> noemen in hun eigen `Bron.`-blok nog `03b6ef4` en zijn dus niet opnieuw
> gecontroleerd. Ga bij elk hoofdstuk af op het bronblok bovenaan die pagina,
> niet op deze pagina.

Wel getoetst tegen v1.17.1:

| Hoofdstuk | Wat er is bijgewerkt |
|---|---|
| [CLI-referentie](../cli/introduction.md) | regelnummers, JSON-configuratie, standaardwaarden, afwijkingentabel |
| [Radio](../cli/radio.md) | vier nieuwe commando's, `radio.rxgain` gecorrigeerd |
| [Systeem](../cli/system.md) | regelnummers, naamlengte en UTF-8-afkapping |
| [Ethernet](../cli/ethernet.md) | nieuw hoofdstuk |

Nog niet hertoetst, gemeten met
[`tools/diff-impact.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/diff-impact.py):
83 van de 114 hoofdstukken per taal noemen in hun bronblok minstens één bestand
dat tussen `03b6ef4` en `d929643` is gewijzigd. Vijf daarvan zijn de hierboven
genoemde hoofdstukken plus deze pagina; de overige 78 staan nog op de oude pin.
Een gewijzigd bronbestand is geen bewijs dat de tekst fout is, maar het is wel
de lijst die nagelopen moet worden. De zwaartepunten zijn
`design/technical/class-model.md`, de `platform/`-sectie en de
`companion/`-sectie.

## Bronnen

- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/ConfigSerializer.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ConfigSerializer.cpp)
- [MeshCore firmware — `src/helpers/AdvertDataHelpers.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/AdvertDataHelpers.cpp)
- [MeshCore firmware — `src/helpers/MultiSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/MultiSerialInterface.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/examples/simple_room_server/MyMesh.cpp)
- [MeshCore release notes v1.17.1](https://blog.meshcore.io/2026/08/14/release-1-17-1)
- [MeshCore release notes v1.17.0](https://blog.meshcore.io/2026/08/09/release-1-17-0)
