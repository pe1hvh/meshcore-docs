# Het buildsysteem

*INI-BESTANDEN · BASISSECTIES · OVERERVING · BRONFILTER*

Uit één codebase komen 508 firmwarebestanden. Dit hoofdstuk beschrijft de
machinerie die dat doet: tachtig `platformio.ini`-bestanden, 108 basissecties
en twee verschillende overervingsmechanismen die allebei gevolgd moeten
worden. Wie er maar één volgt, mist 28 buildtargets zonder dat iets stukgaat.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — de root `platformio.ini` en alle
> 79 `variants/*/platformio.ini`.

## De cijfers

| Wat | Aantal |
|---|---|
| `platformio.ini`-bestanden | 80 (1 root + 79 varianten) |
| Secties totaal | 616 |
| `[env:...]`-secties (buildtargets) | 508 |
| Basissecties | 108 |
| Targets die hun applicatie alleen via overerving hebben | 28 |

Een basissectie is een sectie zonder het voorvoegsel `env:`. PlatformIO bouwt
hem niet, maar andere secties kunnen er via `extends` van erven. De 108
basissecties dragen dus de gedeelde instellingen van de 508 targets.

![Een piramide. Onderaan arduino_base met 507 targets eronder; daarboven de
vier familiebasissecties esp32_base, nrf52_base, rp2040_base en stm32_base;
daarboven de bordspecifieke basissecties; bovenaan de individuele
env-secties.](../../../images/nl/build-system-1.svg)

## Twee overervingsmechanismen

PlatformIO kent er twee, en ze werken anders.

**`extends`** neemt alle opties van de genoemde sectie over. Een sectie die
`extends = esp32_base` heeft, krijgt elke optie die daar staat, tenzij hij hem
zelf overschrijft.

**`${sectie.optie}`** splitst tekst in. Dat is geen overerving maar
tekstvervanging: op de plek van de verwijzing komt letterlijk de waarde van
die ene optie te staan.

Een sectie kan beide gebruiken, en veel secties doen dat. Wie alleen `extends`
volgt, mist de opties die via `${...}` binnenkomen; wie alleen `${...}` volgt,
mist alles wat via `extends` erft. In MeshCore `03b6ef4` kost het volgen van
één van de twee 28 buildtargets: die krijgen hun `build_src_filter` — en dus
hun applicatie — van een gedeelde basissectie die zelf geen `[env:...]` is.

## Hoeveel targets uit welke basissectie komen

| Basissectie | Targets die eruit erven |
|---|---|
| `arduino_base` | 507 |
| `esp32_base` | 270 |
| `nrf52_base` | 199 |
| `rp2040_base` | 22 |
| `esp32c6_base` | 16 |
| `stm32_base` | 16 |
| `nibble_screen_connect_base` | 8 |
| `Heltec_E213_base` | 6 |
| `Heltec_E290_base` | 6 |
| `Heltec_T190_base` | 6 |
| `Heltec_tracker_base` | 6 |
| `Heltec_Wireless_Paper_base` | 6 |

`arduino_base` staat onder alles: 507 van de 508 targets erven ervan. De
enige uitzondering is `[env:native]`, de sectie waarmee de tests op een pc
draaien.

De vier familiebasissecties eronder — 270 + 199 + 22 + 16 — tellen samen op tot
507. Elk target hoort bij precies één platformfamilie.

`esp32c6_base` is geen vijfde familie. Die sectie erft zelf van `esp32_base`
en zit dus binnen de ESP32-familie; de 16 targets eronder zijn ook in de 270
meegeteld. De ESP32-C6 is een RISC-V-chip in plaats van een Xtensa, wat een
paar afwijkende compileropties nodig maakt, maar voor de firmware is het
dezelfde familie.

## De naam van een sectie bewijst niets

Dit is de belangrijkste valkuil van dit hoofdstuk, en hij geldt voor elke
telling over de buildmatrix.

Welke applicatie een target compileert, staat in `build_src_filter` — de optie
die bepaalt welke bronbestanden meegaan. Niet in de naam van de sectie. Een
sectie die `Generic_ESPNOW_room_svr` heet, compileert de room server zonder
dat er `room_server` in de naam staat; omgekeerd hoeft een naam op
`_room_server` niets te bewijzen.

Tellen op de naam geeft 70 room-servertargets in 66 directory's. Tellen op het
opgeloste bronfilter geeft er 73 in 65. Dat verschil van drie targets en één
directory komt geheel uit de twee overervingsmechanismen hierboven.

| Rol | Targets |
|---|---|
| Companion radio | 174 |
| Repeater | 136 |
| KISS-modem | 80 |
| Room server | 73 |
| Terminal chat | 26 |
| Sensor | 18 |

Samen 507, plus `[env:native]` zonder applicatie. Welke rol wat doet, staat in
[Rollen](../logisch/roles.md).

## Aanvullende buildopties

Boven op de combinatie van bord en rol komen de losse schakelaars. Ze staan
los van elkaar aan of uit, en verklaren waarom er meer targets zijn dan
borden maal rollen:

| Schakelaar | Targets |
|---|---|
| `ENV_INCLUDE_GPS` | 323 |
| `DISPLAY_CLASS` | 309 |
| `MESH_DEBUG` | 36 |
| `WITH_ESPNOW_BRIDGE` | 33 |
| `WITH_RS232_BRIDGE` | 13 |
| `MESH_PACKET_LOGGING` | 10 |

`MESH_DEBUG` verdient een waarschuwing. De macro komt 387 keer voor in de
tachtig ini-bestanden, maar staat in slechts 36 targets werkelijk aan. De rest
staat uitgecommentarieerd achter een `;`. Wie op tekst zoekt in plaats van op
actieve regels, overschat de foutopsporing met een factor tien.
`MESH_PACKET_LOGGING` gaat net zo: 385 vermeldingen, 10 targets.

## Drie bestanden met CRLF

`variants/minewsemi_me25ls01/`, `variants/nibble_screen_connect/` en
`variants/wio_wm1110/` gebruiken Windows-regeleinden. Zonder normalisatie
lezen `esp32_base\r` en `esp32_base` als twee verschillende ouders, en vallen
die targets buiten elke telling.

`tools/design-overview.py` normaliseert de regeleinden daarom voordat het iets
anders doet.

## Wat er niet compileert

`Generic_E22_kiss_modem` compileert niet. De sectie bestaat en wordt door
PlatformIO herkend, maar de combinatie van opties levert een bouwfout op. Het
target zit in de tellingen omdat het een `[env:...]`-sectie is; wie een
firmwarebestand verwacht, krijgt er geen.

`platformio.local.ini` staat in `extra_configs` van de root, maar zit niet in
de repo. Dat is opzet: het is de plek voor lokale instellingen die je niet
meecommit. PlatformIO slaat een ontbrekend bestand in `extra_configs` over
zonder te klagen.

`FIRMWARE_BUILD_DATE` staat op `"6 Jun 2026"` in vier van de zes applicaties,
terwijl deze commit van 28 juli is. De waarde is handmatig, wordt zelden
bijgewerkt, en is dus geen betrouwbare aanduiding van wanneer een build is
gemaakt.

## Narekenen

```bash
python3 tools/design-overview.py /pad/naar/MeshCore
python3 tools/design-overview.py /pad/naar/MeshCore --targets simple_room_server
```

Het script lost `extends` en `${sectie.optie}` allebei op, normaliseert CRLF,
en slaat uitgecommentarieerde regels over. Zijn room-servertelling (73 targets
in 65 directory's) komt overeen met `tools/room-server-overview.py`, dat langs
een andere weg tot hetzelfde getal komt — die kruiscontrole is het bewijs dat
de oplosser klopt.

## Bronnen

- [MeshCore `03b6ef4` — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [MeshCore `03b6ef4` — `variants/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/variants)
- [MeshCore `03b6ef4` — `variants/heltec_v3/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/heltec_v3/platformio.ini)
- [PlatformIO — Section extension](https://docs.platformio.org/en/latest/projectconf/section_env.html)
