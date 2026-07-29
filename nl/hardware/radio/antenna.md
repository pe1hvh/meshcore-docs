# Antenne

*CONNECTOR · SWR · RF-SCHAKELAAR · PRAKTISCHE KEUZE*

De antenne is het enige onderdeel van een node dat geen firmware kent en
toch het grootste deel van je bereik bepaalt. Wat de firmware er wél over
weet is de schakelaar ertussen: één antenne moet zowel zenden als
ontvangen, en de chip moet weten hoe die omschakeling loopt. Dit hoofdstuk
beschrijft die schakelaar, de connector en de verhouding tussen staande golf
en gereflecteerd vermogen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/radiolib/CustomSX1262.h` en de RF-vlaggen in `variants/`.
> Connectoren, SWR en antennetypen komen niet uit de firmware; dat is
> algemene radiotechniek en is als zodanig gemarkeerd.

![Schema van het RF-pad: van de chip via de RF-schakelaar naar de connector
en de antenne, met DIO2 dat het zendpad schakelt en RXEN dat het
ontvangstpad schakelt](../../../images/nl/antenna-1.svg)

## Eén antenne, twee paden

Zenden en ontvangen gebeuren over dezelfde antenne, maar niet over hetzelfde
pad: het zendpad loopt door de eindtrap, het ontvangstpad door de LNA. Er
zit dus een schakelaar tussen chip en connector. MeshCore kent daar twee
invullingen voor, en ze sluiten elkaar niet uit.

| Aansturing | Vlag | Variantmappen |
|---|---|---|
| DIO2 van de chip stuurt de schakelaar | `SX126X_DIO2_AS_RF_SWITCH` | 60 van 79 |
| losse GPIO-pinnen sturen de schakelaar | `SX126X_RXEN` · `SX126X_TXEN` | 24 van 79 |

Geteld per variantmap over `variants/`, zowel `-D`-vlaggen in
`platformio.ini` als `#define`-regels in een header binnen die map;
uitgecommentarieerde regels tellen niet mee.

De eerste is de eenvoudigste: de chip zet DIO2 hoog zodra hij gaat zenden en
laag zodra hij luistert. De firmware hoeft niets te doen behalve de vlag
doorgeven aan RadioLib, wat gebeurt in `std_init()` — zie
[De LoRa-transceiver](sx1262.md).

De tweede komt voor op borden met een externe eindtrap of een losse LNA,
waar één lijn niet genoeg is. Ontbreekt één van de twee pinnen, dan vult de
wrapper hem aan met `RADIOLIB_NC`.

## Een bord dat beide gebruikt

De T-Beam 1W combineert ze, en het commentaar in de variant zegt precies
hoe:

`variants/lilygo_tbeam_1w/platformio.ini` r.22-28

```ini
  ; RF switch configuration:
  ;   DIO2 controls TX path (PA enable) via SX126X_DIO2_AS_RF_SWITCH
  ;   GPIO21 controls RX path (LNA enable) via SX126X_RXEN
  ; Truth table: DIO2=1,RXEN=0 → TX | DIO2=0,RXEN=1 → RX
  -D SX126X_DIO2_AS_RF_SWITCH=true
  -D SX126X_RXEN=21
  -D SX126X_DIO3_TCXO_VOLTAGE=3.0
```

DIO2 schakelt het zendpad, GPIO21 het ontvangstpad. `SX126X_TXEN` is niet
gezet en wordt dus `RADIOLIB_NC`. Hetzelfde bestand legt ook uit wat er
achter die schakelaar zit:

`variants/lilygo_tbeam_1w/platformio.ini` r.33-34

```ini
  ; TX power: 22dBm to SX1262, PA module adds ~10dB for 32dBm total
  -D LORA_TX_POWER=22
```

De chip staat op 22 dBm, de externe eindtrap maakt er ongeveer 32 dBm van.
Dat is de reden dat je `LORA_TX_POWER` nooit los kunt lezen: het is het
vermogen dat de chip levert, niet het vermogen dat de antenne verlaat. Wat
je daarvan mag uitstralen staat in
[Regelgeving & Duty Cycle](../../gebruik/regulations.md).

> [!WARNING]
> Zenden zonder antenne, of met een antenne voor de verkeerde band, laat het
> vermogen terugkomen in de eindtrap. Bij 22 dBm is dat al niet gezond, bij
> een bord met externe eindtrap is het fataal. Sluit de antenne aan vóór je
> voeding geeft.

## Connector en kabel

Niet uit de firmware — algemene radiotechniek.

| Connector | Waar | Opmerking |
|---|---|---|
| SMA | op de meeste ontwikkelborden | pin in het midden van de kabelzijde |
| RP-SMA | veel WiFi-hardware | omgekeerde pin; past mechanisch, werkt niet |
| IPEX/U.FL | op modules en compacte nodes | fragiel, bedoeld voor een pigtail |

SMA en RP-SMA schroeven op elkaar zonder contact te maken in het midden. Dat
is de meest voorkomende fout bij een node die wel zendt maar niets bereikt.

Kabel is verlies. Op 868 MHz kost dunne coax al snel enkele dB per tien
meter. Een node dicht bij de antenne met een korte kabel wint het van een
node binnen met een lange kabel. Wat een dB in afstand kost staat in
[Linkbudget](link-budget.md).

## SWR: wat er terugkomt

Niet uit de firmware — dit is de standaardomrekening van staandegolfverhouding
naar gereflecteerd vermogen.

| SWR | Gereflecteerd | Praktijk |
|---|---|---|
| 1,0 : 1 | 0 % | theoretisch perfect |
| 1,5 : 1 | 4 % | prima |
| 2,0 : 1 | 11 % | acceptabel |
| 3,0 : 1 | 25 % | te hoog, aanpassing nodig |
| ∞ | 100 % | open of kortgesloten |

De SX1262 heeft geen SWR-meting aan boord en de firmware leest er dus ook
niets over uit. Je merkt een slechte aanpassing alleen aan bereik dat
tegenvalt en aan een eindtrap die warm wordt.

## Drie praktische regels

1. **Meer winst is richting, geen vermogen.** Een antenne met hogere winst
   kijkt platter en verliest boven en onder. Waarom meer winst zelfs tegen
   je kan werken staat in
   [Hoger en sterker is niet altijd beter](../../techniek/dead-zone.md); het
   stralingsdiagram en de dode zone horen daar en worden hier niet herhaald.
2. **Een halvegolfdipool is bijna altijd genoeg.** 2,15 dBi, geen
   groundplane nodig, en precies de referentie die de regelgeving gebruikt.
3. **Hoogte wint van vermogen.** Een meter hoger levert vaker meer op dan
   een dB erbij, omdat het obstakels uit de eerste fresnelzone haalt.

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`src/helpers/radiolib/CustomSX1262.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/radiolib/CustomSX1262.h)
  — `setDio2AsRfSwitch()` en `setRfSwitchPins()`
- [`variants/lilygo_tbeam_1w/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/lilygo_tbeam_1w/platformio.ini)
  — de waarheidstabel van de RF-schakelaar en de externe eindtrap

Niet uit de firmwarerepo: connectoren, SWR en antennetypen. Dat is algemene
radiotechniek; de SWR-tabel is de standaardomrekening van
staandegolfverhouding naar gereflecteerd vermogen.

Verwante hoofdstukken:

- [De LoRa-transceiver](sx1262.md) — wat er aan de andere kant van de
  schakelaar zit
- [Linkbudget](link-budget.md) — wat winst en verlies waard zijn in afstand
- [Hoger en sterker is niet altijd beter](../../techniek/dead-zone.md) —
  stralingsdiagram, antennewinst en dekking
- [Regelgeving & Duty Cycle](../../gebruik/regulations.md) — wat je mag
  uitstralen
- [Nodematrix](../../platform/node-matrix.md) — welk bord welke connector
  heeft
