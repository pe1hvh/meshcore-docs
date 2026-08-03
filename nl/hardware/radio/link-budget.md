# Linkbudget

*ZENDVERMOGEN · PADVERLIES · GEVOELIGHEID · MARGE*

Een verbinding werkt als er aan de ontvangkant meer signaal aankomt dan de
chip nodig heeft. Alles ertussen is decibellen optellen en aftrekken. Dit
hoofdstuk zet die som op, met de firmwarewaarden waar ze bestaan en met
expliciet gemarkeerde aannames waar ze niet bestaan.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — de wortel-
> `platformio.ini`, `src/helpers/radiolib/RadioLibWrappers.cpp` en de
> `LORA_TX_POWER`-vlaggen in `variants/`. Elk cijfer op deze pagina wordt
> opnieuw uitgerekend door [`tools/link-budget.py`](../../../tools/link-budget.py).

![Staafdiagram van het linkbudget: zendvermogen plus antennewinst min
kabelverlies min padverlies, tot aan de gevoeligheid van de ontvanger, met
de overgebleven marge](../../../images/nl/link-budget-1.svg)

> [!WARNING]
> Twee invoerwaarden komen **niet** uit de firmwarerepo en zijn hieronder
> gemarkeerd met `°`: het ruisgetal van de ontvangketen en de benodigde SNR
> per spreidingsfactor. Ze staan als constante boven in
> `tools/link-budget.py` en zijn niet tegen een datasheet geverifieerd. Elk
> cijfer dat eruit volgt draagt dezelfde onzekerheid.

## Wat de firmware vastlegt

Drie waarden staan in de wortel-`platformio.ini` en gelden voor elk bord dat
ze niet overschrijft:

| Vlag | Waarde |
|---|---|
| `LORA_FREQ` | 869.618 MHz |
| `LORA_BW` | 62.5 kHz |
| `LORA_SF` | 8 |

> [!NOTE]
> `LORA_SF=8` is de compile-time default uit `platformio.ini`, niet de
> instelling waarop het Nederlandse netwerk draait. De radioparameters worden
> na het flashen door de node-configuratie overschreven; het preset
> *Netherlands* zet **SF7** met CR5 — zie
> [Aan de Slag](../../gebruik/getting-started.md). De som verderop op deze
> pagina rekent met de firmwaredefault SF8 (−130,0 dBm). Met SF7 is de
> gevoeligheid −127,5 dBm en valt het budget 2,5 dB lager uit.

Het zendvermogen ligt per bord vast. Geteld over
`variants/*/platformio.ini`, alleen actieve regels:

| `LORA_TX_POWER` | Regels |
|---|---|
| 22 dBm | 93 |
| 20 dBm | 13 |
| 19 dBm | 1 |
| 10 dBm | 1 |
| 9 dBm | 4 |
| 8 dBm | 1 |
| 7 dBm | 2 |

Samen 115 actieve regels over 76 variantmappen. Meer regels dan mappen,
omdat een variantbestand meerdere `[env:…]`-secties kan bevatten die elk hun
eigen vlag zetten. De lage waarden zijn geen zuinige borden maar borden met
een externe eindtrap: 7 dBm bij de chip wordt ruim 27 dBm aan de connector.
Zie [Antenne](antenna.md).

## De ruisvloer

Onder aan de som staat het ruisniveau. Thermische ruis is −174 dBm per hertz
bij kamertemperatuur; over 62,5 kHz is dat −126,0 dBm. Daar komt het
ruisgetal van de ontvangketen bij:

| Post | Waarde |
|---|---|
| thermische ruis over 62,5 kHz | −126,0 dBm |
| ruisgetal ontvangketen `°` | 6,0 dB |
| **ruisvloer ontvanger** | **−120,0 dBm** |

> [!NOTE]
> Dat de berekende vloer precies uitkomt op de −120 dBm waarop de firmware
> zijn eigen meting afkapt, is met dit ruisgetal toeval en geen bewijs. Het
> ruisgetal is een aanname; verander die in 5 of 7 dB en de gelijkheid is
> weg. De afkapping zelf staat wél in de firmware — zie
> [De LoRa-transceiver](sx1262.md).

## Gevoeligheid per spreidingsfactor

LoRa ontvangt onder de ruisvloer. Hoeveel eronder hangt af van de
spreidingsfactor:

| SF | Benodigde SNR `°` | Gevoeligheid |
|---|---|---|
| 7 | −7,5 dB | −127,5 dBm |
| 8 | −10,0 dB | −130,0 dBm |
| 9 | −12,5 dB | −132,5 dBm |
| 10 | −15,0 dB | −135,0 dBm |
| 11 | −17,5 dB | −137,5 dBm |
| 12 | −20,0 dB | −140,0 dBm |

Elke stap in SF levert 2,5 dB gevoeligheid en verdubbelt de zendtijd. De
invloed van die zendtijd op de duty cycle wordt besproken in
[Regelgeving & Duty Cycle](../../gebruik/regulations.md).

## De som

Neem een node op 22 dBm, aan beide kanten een halvegolfdipool van 2,15 dBi
en 1 dB kabelverlies:

```text
  zendvermogen chip          +22,00 dBm
  antennewinst zender         +2,15 dBi
  kabelverlies zender          −1,00 dB
  ------------------------------------
  e.i.r.p.                   +23,15 dBm

  antennewinst ontvanger      +2,15 dBi
  kabelverlies ontvanger       −1,00 dB
  gevoeligheid bij SF8      −130,00 dBm
  ------------------------------------
  budget                     154,30 dB
```

Dat budget mag opgaan aan padverlies. In vrije ruimte is het padverlies
32,44 + 20·log(f in MHz) + 20·log(d in km):

| Afstand | Vrijeruimteverlies |
|---|---|
| 100 m | 71,2 dB |
| 1 km | 91,2 dB |
| 5 km | 105,2 dB |
| 10 km | 111,2 dB |
| 50 km | 125,2 dB |

154 dB budget zou in vrije ruimte op meer dan duizend kilometer uitkomen.
Dat getal is correct en tegelijk nutteloos: vrije ruimte bestaat niet op
aardoppervlak. De aarde kromt weg, er staan gebouwen en bomen in de weg, en
de fresnelzone raakt de grond lang voordat het budget op is. Het
vrijeruimteverlies is een bovengrens, geen voorspelling. Waarom de praktijk
er zo ver vanaf ligt staat in
[Hoger en sterker is niet altijd beter](../../techniek/dead-zone.md).

## Wat een dB waard is

Nuttiger dan een absolute afstand is de verhouding. Elke 6 dB verdubbelt de
afstand in vrije ruimte, elke 6 dB minder halveert hem:

| Verandering | Factor op de afstand |
|---|---|
| −6 dB | × 0,50 |
| −3 dB | × 0,71 |
| −1 dB | × 0,89 |
| +1 dB | × 1,12 |
| +3 dB | × 1,41 |
| +6 dB | × 2,00 |

Daar zit de praktische waarde van het hele hoofdstuk. Een slechte connector
met 3 dB verlies vermindert je bereik met bijna 30 procent. Een SF-stap erbij
levert 2,5 dB en dus ruim 30 procent — maar verdubbelt de zendtijd. En een
antenne één meter hoger levert vaak meer dan beide, omdat die het obstakel
uit de weg haalt in plaats van erdoorheen te proberen te zenden.

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/platformio.ini)
  — `LORA_FREQ`, `LORA_BW` en `LORA_SF`
- [`src/helpers/radiolib/RadioLibWrappers.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/radiolib/RadioLibWrappers.cpp)
  — de gemeten ruisvloer en de ondergrens van −120 dBm
- [`variants/heltec_v3/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/heltec_v3/platformio.ini)
  — `LORA_TX_POWER=22`

In deze repository:

- [`tools/link-budget.py`](../../../tools/link-budget.py) — rekent elk cijfer
  op deze pagina opnieuw uit

Niet uit de firmwarerepo: het ruisgetal van de ontvangketen en de benodigde
SNR per spreidingsfactor, beide met `°` gemarkeerd. De thermische ruisvloer
van −174 dBm/Hz is geen datasheetwaarde maar volgt uit *kT* bij
kamertemperatuur.

Verwante hoofdstukken:

- [De LoRa-transceiver](sx1262.md) — waar het zendvermogen wordt gezet
- [Antenne](antenna.md) — winst en verlies aan de RF-poort
- [Hoger en sterker is niet altijd beter](../../techniek/dead-zone.md) —
  waarom vrije ruimte geen praktijk is
- [Regelgeving & Duty Cycle](../../gebruik/regulations.md) — hoeveel van dit
  budget je werkelijk mag gebruiken
