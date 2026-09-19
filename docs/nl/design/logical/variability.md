# Variabiliteit

*DRIE ASSEN · 508 BUILDS · WAAROM TELLEN OP NAAM FOUT GAAT*

Uit één codebase komen 508 verschillende buildtargets. Dit hoofdstuk beschrijft
hoe dat werkt: langs welke assen MeshCore varieert, welk deel van de
theoretisch mogelijke combinaties daadwerkelijk bestaat, en waarom je de
aantallen niet kunt aflezen aan de namen van de targets.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — de root `platformio.ini` en alle
> 79 `variants/*/platformio.ini`. Alle aantallen komen uit
> `tools/design-overview.py`.

## Drie assen

MeshCore varieert langs drie onafhankelijke assen. Een buildtarget is een punt
in die ruimte: één rol, één platformfamilie, één bord.

![Drie assen in een blokdiagram: rol, platformfamilie en bord. Daarnaast een
losse kolom met de aanvullende buildopties die onafhankelijk van de assen aan
of uit kunnen: radio, scherm, brug, sensoren en logging.](../../../images/nl/variability-1.svg)

| As | Waarden | Vastgelegd door |
|---|---|---|
| Rol | 6 | Welke applicatiedirectory wordt meegecompileerd |
| Platformfamilie | 4 | Welke platformmacro is gedefinieerd |
| Bord | 79 varianten | Welk variantbestand het target definieert |

Daarnaast zijn er aanvullende buildopties die los van de assen staan: welke
radiochip, welk schermtype, of er een brug is, of er sensoren zijn, en of
logging aan staat.

## De aantallen

```
ini-bestanden gelezen        80   (1 root + 79 varianten)
secties totaal              616
[env:...]-secties           508
basissecties                108
```

Van de 508 targets compileren er 507 één applicatie; het 508e is het
testtarget dat op de ontwikkelmachine draait.

| Rol | Targets | Variantdirectory's |
|---|---|---|
| Companion radio | 174 | 76 |
| Repeater | 136 | 75 |
| KISS-modem | 80 | 74 |
| Room server | 73 | 65 |
| Terminal chat | 26 | 24 |
| Sensor | 18 | 16 |

| Platformfamilie | Targets |
|---|---|
| ESP32 | 270 |
| nRF52 | 199 |
| RP2040 | 22 |
| STM32 | 16 |

En de kruistabel, die laat zien dat de assen niet volledig onafhankelijk zijn:

| Rol | ESP32 | nRF52 | RP2040 | STM32 |
|---|---|---|---|---|
| Companion radio | 91 | 75 | 4 | 4 |
| Repeater | 83 | 42 | 6 | 5 |
| KISS-modem | 36 | 36 | 4 | 4 |
| Room server | 34 | 35 | 4 | 0 |
| Terminal chat | 17 | 5 | 4 | 0 |
| Sensor | 9 | 6 | 0 | 3 |

Drie cellen staan op nul. Er is geen room server en geen terminal chat op
STM32, en geen sensor op RP2040. Dat is geen technische onmogelijkheid maar
een keuze: niemand heeft die combinatie nodig gehad.

## Niet alle combinaties worden ondersteund

Zes rollen op negenenzeventig borden zou 474 combinaties opleveren. Er zijn er
507. Dat is geen tegenspraak maar het gevolg van de aanvullende buildopties:
dezelfde rol op hetzelfde bord bestaat meermaals, in varianten met en zonder
brug, met verschillende schermen of met een andere zendtransport.

Tegelijk is de configuratiematrix niet volledig gevuld. Lang niet elk bord
kent alle zes de rollen. De companion radio bestaat op 76 van de 79 borden, de
sensor op 16.

| Aanvullende buildopties | Targets |
|---|---|
| GPS ingeschakeld | 323 |
| Scherm aanwezig | 309 |
| ESP-NOW brug | 33 |
| RS232 brug | 13 |
| Debug-uitvoer aan | 36 |
| Pakketlogging aan | 10 |

## Klassen kiezen tijdens het compileren

De aanvullende buildopties werken via één mechanisme: het buildsysteem geeft
een klassenaam door als macro, en de code gebruikt die naam alsof hij er
altijd al stond. Zo kiest een variantbestand welke radio en welk scherm er in
de binary komen, zonder dat de applicatie ervan weet.

| Macro | Verschillende waarden | Targets die hem zetten |
|---|---|---|
| `RADIO_CLASS` | 5 | 501 |
| `WRAPPER_CLASS` | 5 | 501 |
| `DISPLAY_CLASS` | 11 | 309 |

De vijf radiowaarden dekken vijf chipfamilies. Er is een zesde implementatie
in de broncode aanwezig die door geen enkel target wordt gekozen; hij is
beschikbaar voor wie hem in een eigen variant nodig heeft.

Zeven targets zetten geen `RADIO_CLASS`. Vijf daarvan zijn ESP-NOW-varianten
die geen LoRa-radio gebruiken, en het zesde is het testtarget. Het zevende is
een fout; zie hieronder.

## Waarom tellen op naam fout gaat

Dit is de belangrijkste waarschuwing van dit hoofdstuk, en de reden dat er een
script bij zit.

De naam van een `[env:...]`-sectie is vrije tekst. Hij zegt niets af over wat
er wordt gecompileerd. Drie manieren waarop de naam misleidt:

**De naam noemt de rol niet.** `Generic_ESPNOW_room_svr` compileert de room
server, maar wie op `_room_server` zoekt vindt hem niet. Er zijn ook targets
met `_repeatr` en `_Repeater` in de naam.

**De naam noemt een rol die er niet is.** Omgekeerd is een naam die op
`_repeater` eindigt geen bewijs dat de repeater erin zit.

**De rol staat niet in de sectie zelf.** 28 van de 508 targets noemen nergens
in hun eigen tekst een applicatiedirectory. Ze erven die via `extends` of via
een tekstverwijzing naar een andere sectie. Een zoekopdracht op het bestand
ziet ze niet.

De juiste methode is: de sectie volledig oplossen — `extends` volgen en
tekstverwijzingen uitvouwen — en dan kijken welke applicatiedirectory in het
bronfilter wordt ingesloten. `tools/design-overview.py` doet dat:

```bash
python3 tools/design-overview.py /pad/naar/MeshCore --targets simple_room_server
```

Ter controle: die aanroep levert 73 targets in 65 variantdirectory's, hetzelfde
getal als `tools/room-server-overview.py` langs een andere weg vindt.

## Twee valkuilen bij het tellen

**Tel secties, geen regels.** Een naïeve zoekopdracht op `examples/` telt
regels en overdrijft de companion radio met een factor drie, omdat die
applicatie zijn bronfilter over meerdere regels verdeelt.

**Negeer uitgecommentarieerde macro's.** Zoek je met een tekstzoekopdracht naar
`MESH_DEBUG`, dan vind je er 387. Werkelijk ingeschakeld is hij in 36 targets;
in de rest staat de regel uitgeschakeld in het bestand als voorbeeld. Hetzelfde
geldt voor pakketlogging: 385 vermeldingen, 10 daadwerkelijk aan.

## Drie variantbestanden met andere regeleinden

`variants/minewsemi_me25ls01`, `variants/nibble_screen_connect` en
`variants/wio_wm1110` gebruiken Windows-regeleinden. Wie de bestanden regel
voor regel leest zonder te normaliseren, houdt een onzichtbaar teken over aan
het eind van elke waarde. De ouder mét dat teken en de ouder zonder tellen dan
als twee verschillende secties, en de helft van de overervingsketen valt weg.
Het script normaliseert de regeleinden voordat het iets anders doet.

## Eén target dat niet kan compileren

`Generic_E22_kiss_modem` erft van de basissectie `Generic_E22` en neemt daarmee
ook het bronfilter over dat `variants/generic-e22/` insluit. In dat bestand
staat:

`variants/generic-e22/target.cpp` r.8-13

```cpp
  RADIO_CLASS radio = new Module(P_LORA_NSS, P_LORA_DIO_1, P_LORA_RESET, P_LORA_BUSY, spi);
```

Maar noch het target, noch de basissectie, noch een van de bovenliggende
secties definieert `RADIO_CLASS`. De zusjes van dit target doen dat wel — elk
kiest per target tussen de SX1262- en de SX1268-uitvoering — maar de
KISS-modemvariant is overgeslagen. Dit target is daarmee het enige van de 508
dat niet vertaalt.

## Bronnen

- [MeshCore `03b6ef4` — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [MeshCore `03b6ef4` — `variants/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/variants)
- [MeshCore `03b6ef4` — `variants/heltec_v3/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/heltec_v3/platformio.ini)
- [PlatformIO — Project Configuration File](https://docs.platformio.org/en/latest/projectconf/index.html)
