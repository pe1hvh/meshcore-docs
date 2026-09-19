# SenseCap DFU

*TECHNIEK · OTA FIRMWARE UPDATE — SENSECAP SOLAR NODE P1-PRO*

meta
Device: SenseCAP Solar Node P1-Pro
MCU: Nordic nRF52840
Bootloader: OTAFIX
Firmware: MeshCore
April 2026
inleiding

De SenseCAP Solar Node P1-Pro wordt in de praktijk ingezet als MeshCore repeater op moeilijk bereikbare locaties: daken, masten, buiteninstallaties. Op het moment dat zo'n repeater eenmaal gemonteerd is, is fysieke toegang vaak moeilijk of niet direct mogelijk.

Diverse internet bronnen spreken elkaar tegen als het gaat om een succesvolle firmware update. Deze pagine is het resultaat van een gedegen aantal testen en een onderzoek van de achtergrond van het nRF52 DFU-protocol. Met als doel een betrouwbare werkwijze te vinden voor de firmware update, zonder dat je daar voor het dak op moet.

Voor de DFU-update is gebruikgemaakt van de officiële [**nRF Device Firmware Update** app van Nordic Semiconductor ↗](https://play.google.com/store/apps/details?id=no.nordicsemi.android.dfu&hl=en-US&pli=1) (Android, Google Play). Dit is de referentie-implementatie van het Nordic Secure DFU-protocol en de enige app waarmee de procedure in dit document betrouwbaar werkt.

⚠️ OTAFIX is geen optie, maar een vereiste.
Voordat een SenseCAP Solar Repeater op het dak gaat,
moet
de OTAFIX bootloader geïnstalleerd zijn. Zonder OTAFIX geldt: één mislukte OTA-update = apparaat onbereikbaar via Bluetooth = fysieke toegang vereist voor herstel.
Voor de tests in dit document is gebruikgemaakt van
sensecap_solar_bootloader-0.9.2-OTAFIX2.1.uf2
, gedownload via
meshcore.co.uk/flasher.html ↗
.
inhoudsopgave
Inhoudsopgave

1. Aanbevolen DFU-instellingen
2. Het `start ota` CLI-commando
3. Het volledige OTA-proces stap voor stap
4. Technische verklaring van het twee-fasen DFU-protocol
5. Wat te doen als het proces fout gaat na Bootloader enabled
6. De twee BLE-advertentienamen verklaard
7. Waarom de OTAFIX
8. Overzichtstabel: goed vs. fout
9. Bronnen

1

## 1 · Aanbevolen DFU-instellingen

De onderstaande instellingen gelden voor de **nRF Device Firmware Update** app van Nordic Semiconductor (Android). Ze zijn getest en werken betrouwbaar met OTAFIX 2.1 op de SenseCAP Solar Node P1-Pro. Met deze instellingen verloopt het proces volledig geautomatiseerd.

| Instelling | Waarde | Toelichting |
|---|---|---|
| Packet Receipt Notification | AAN | ACK elke N packets |
| Number of Packets | `30` | Geeft bootloader voldoende timing-venster voor fase-overgang |
| Reboot time | `0 ms` | Geen extra wachttijd nodig |
| Scan Timeout | `2000 ms` | Zoektijd voor DFU-device |
| Disable resume | AAN ✅ | Essentieel — zorgt dat de app na disconnect opnieuw scant i.p.v. op MAC herverbindt |
| Force Scanning | AAN ✅ | Werkt correct in combinatie met `Disable resume: ON` — zie §1 |
| Prepared Object delay | `0 ms` | Geen vertraging nodig |

Let op:
Disable resume: ON
is de kritieke instelling.
Force Scanning: ON
zonder
Disable resume
veroorzaakt een een foute installatie zonder
Disable resume: ON
(zie §1). De combinatie van beide maakt het proces volledig automatisch.
2

## 2 · Het `start ota` CLI-commando

Het CLI-commando `start ota` is onderdeel van de MeshCore repeater/room server firmware. Het wordt uitgevoerd via de Command Line tab in de MeshCore-app, nadat je remote met admin-rechten bent ingelogd op de repeater.

De MeshCore firmware roept intern de Nordic SoftDevice API aan en triggert een *buttonless DFU* (Device Firmware Update):

```text
start ota
    │
    ▼
MeshCore firmware roept Nordic SoftDevice API aan:
  sd_ble_gap_adv_set_configure()
  → advertisement data: name = "SENSECAP_SOLAR_OTA"
  → service UUID: Nordic DFU service (0xFE59)
    │
    ▼
Firmware triggert buttonless DFU:
  ble_dfu_buttonless
  → schrijft DFU-flag naar retained registers
  → start adverteren als DFU-target
  → wacht op verbinding van DFU-client
```

> [!NOTE]
> Bevestiging:
> Na het commando verschijnt
> OK
> in de CLI. Het apparaat adverteert vanaf dat moment via Bluetooth als
> SENSECAP_SOLAR_OTA
> . De LoRa-repeater-functionaliteit is
> niet meer actief
> totdat de update voltooid is.

2

## 3 · Het volledige OTA-proces stap voor stap

Met de aanbevolen instellingen (zie §1) verloopt het proces volledig geautomatiseerd.

| Stap | Actie | Toelichting |
|---|---|---|
| 1 | Companion App CLI: `start ota` | Triggert DFU-modus in firmware |
| 2 | CLI toont `OK: <mac address>` | Bevestiging dat DFU actief is |
| 3 | Device adverteert als `SENSECAP_SOLAR_OTA` | Applicatielaag DFU actief |
| 4 | DFU app: selecteer juiste firmware `.zip` | De `sensecap_solar_repeater-vX.Y.Z.zip` |
| 5 | DFU app: selecteer `SENSECAP_SOLAR_OTA` | Verbinding met applicatie-DFU |
| 6 | DFU app: Start update | Command Object (init packet) wordt verstuurd — app handelt de fase-overgang automatisch af |
| 7 | DFU app: transfer voltooid | Data Object (firmware binary) verstuurd, hash geverifieerd, automatische reboot |

> [!NOTE]
> Resultaat:
> Firmware geschreven, hash geverifieerd, automatische reboot ✅

Bootloader enabled, maar installatie mislukt?
Zie §5.
3

## 4 · Technische verklaring van het twee-fasen DFU-protocol

De nRF52840 gebruikt Nordic's **Secure DFU protocol** dat in twee strikte fasen werkt:

```text
Fase 1 — Command Object (Init Packet)
│
│  ┌─────────────────────────────────────────────┐
│  │ • firmware metadata                         │
│  │ • hardware version check                    │
│  │ • firmware hash (SHA-256)                   │
│  │ • cryptografische signature                 │
│  └─────────────────────────────────────────────┘
│
│  → bootloader valideert → "Bootloader enabled" ✅
│
│  ** Bootloader wisselt intern van toestand    **
│  ** BLE verbinding wordt verbroken            **
│  ** Apparaat re-adverteert als XIAO_DFU       **
│
Fase 2 — Data Object (Firmware payload)
│
│  ┌─────────────────────────────────────────────┐
│  │ • eigenlijke firmware binary in chunks      │
│  │ • PRN (Packet Receipt Notification) elke 8  │
│  │   packets een ACK                           │
│  │ • Execute → hash verify → reboot            │
│  └─────────────────────────────────────────────┘
```

De naamswijziging van `SENSECAP_SOLAR_OTA` naar `XIAO_DFU` is **geen bug** — het is het ontworpen gedrag van de OTAFIX bootloader. Na succesvolle validatie van het Command Object verlaat de bootloader de applicatie-geïnitieerde DFU-modus en stapt over naar de bootloader-native DFU-modus met een andere BLE-advertisement identity.

4

## 5 · Wat te doen als het proces fout gaat na Bootloader enabled

Wanneer de DFU-app "Bootloader enabled" toont maar de firmware-overdracht vervolgens mislukt of vastloopt, is er geen reden tot paniek. Dankzij de OTAFIX bootloader herstart het apparaat bij een mislukte OTA **niet** naar USB/UF2-modus — het blijft adverteren en is bereikbaar via Bluetooth.

Na een mislukte overdracht bevindt de bootloader zich in OTA DFU-modus en adverteert het apparaat als `XIAO_DFU`. Het proces kan handmatig worden voortgezet:

| Stap | Actie | Toelichting |
|---|---|---|
| 1 | DFU app: druk op ABORT indien actief | Verbreek de huidige mislukte sessie netjes |
| 2 | DFU app: scan naar beschikbare devices | Het apparaat adverteert nu als `XIAO_DFU` |
| 3 | Selecteer `XIAO_DFU` als target device | Dit is de bootloader-native DFU-modus van de OTAFIX bootloader |
| 4 | Start de firmware-overdracht opnieuw | Data Object (firmware binary) wordt verstuurd, hash geverifieerd, automatische reboot |

> [!NOTE]
> Waarom dit werkt:
> De OTAFIX bootloader valt bij een mislukte OTA terug op OTA DFU-modus (adverteert als
> XIAO_DFU
> ) in plaats van op USB/UF2-modus. Het apparaat blijft daardoor volledig bereikbaar via Bluetooth — ook op een dak of mast — en een nieuwe poging is altijd mogelijk zonder fysieke toegang.

5

## 6 · De twee BLE-advertentienamen verklaard

De twee namen die tijdens het OTA-proces verschijnen, komen uit **verschillende lagen** en hebben **verschillende bronnen**:

**SENSECAP_SOLAR_OTA**

- **Fase 1 · Applicatielaag** — Hardcoded in de MeshCore firmware voor dit boardtype. Actief tijdens
        Fase 1 (Command Object). Getriggerd door CLI-commando start ota .
        Net zoals andere boards hun eigen naam krijgen ( RAK4631_OTA , T114_OTA , etc.).

**XIAO_DFU**

- **Fase 2 · Bootloader-laag** — Afkomstig van de OTAFIX bootloader . Actief tijdens Fase 2 (Data Object).
        Zonder OTAFIX zou hier AdaDFU staan — de generieke Adafruit standaard naam.

| Naam | Laag | Bron | Zonder OTAFIX |
|---|---|---|---|
| `SENSECAP_SOLAR_OTA` | Applicatie | MeshCore firmware | Zelfde naam — ongewijzigd |
| `XIAO_DFU` | Bootloader | OTAFIX bootloader | `AdaDFU` (Adafruit generiek) |

8

## 7 · Waarom de OTAFIX

De reden is concreet en betreft één kritiek gedragsdefect in de stock Adafruit bootloader:

**OTA mislukt → fysieke toegang vereist ❌**

- **Stock bootloader** — Bij mislukte OTA valt de stock bootloader terug op UF2/CDC modus (USB drive,
        seriële poort). Het apparaat is niet meer bereikbaar via Bluetooth. Voor een repeater op een
        dak of mast betekent dit: ernaar toe klimmen.

**OTA mislukt → herstelbaar via BLE ✅**

- **OTAFIX bootloader** — Bij mislukte OTA herstart OTAFIX in OTA DFU modus (Bluetooth, adverteert
        als XIAO_DFU ). Het apparaat blijft bereikbaar via Bluetooth. Opnieuw proberen
        zonder fysieke toegang.

OTAFIX lost daarnaast ook een **tweede probleem** op: de stock bootloader had `HCI_RX_BUF_QUEUE_SIZE = 8`. Bij de pakketfrequentie van een OTA-transfer liep deze buffer over, wat resulteerde in willekeurige OTA-mislukkingen. OTAFIX verhoogde deze naar `HCI_RX_BUF_QUEUE_SIZE = 16`, waardoor buffer overflow bij normale OTA-transfers praktisch niet meer voorkomt.

| Probleem | Stock bootloader | OTAFIX |
|---|---|---|
| Mislukte OTA → terugvalgedrag | UF2/CDC (USB only) | OTA DFU (Bluetooth) |
| BLE HCI buffer bij OTA-transfer | 8 slots → overflow mogelijk | 16 slots → stabiel |
| Fysieke toegang nodig bij mislukking | Ja | Nee |

> [!NOTE]
> De naam zegt het letterlijk:
> OTAFIX fixt het OTA-proces — niet door OTA beter te maken, maar door de
> gevolgen van een mislukte OTA beheersbaar te houden
> .

10

## 8 · Overzichtstabel: goed vs. fout

| Scenario | Resultaat | Technische reden |
|---|---|---|
| Geautomatiseerd: `Force Scanning: ON` + `Disable resume: ON` + 30 packets | ✅ Werkt geautomatiseerd | `Disable resume` zorgt voor correcte herverbinding met `XIAO_DFU` na fase-overgang |
| Handmatig: ABORT na "Bootloader enabled", herverbind met `XIAO_DFU` | ✅ Fallback — altijd goed | Volgt exact de twee-fasen toestandsmachine van de bootloader |
| `Force Scanning: ON` zonder `Disable resume` | ❌ Firmware geschreven, geen reboot | MAC-gebaseerde herverbinding overslaat de fase-transitie |
| OTA zonder OTAFIX bootloader, update mislukt | ❌ Brick | Stock bootloader valt terug op UF2, niet op OTA DFU |
| OTA met OTAFIX bootloader, update mislukt | ✅ Herstelbaar via BLE | OTAFIX herstart in OTA DFU modus, niet in UF2 |

footer

## Bronnen

| Bron | Uitgever | Onderwerp |
|---|---|---|
| [MeshCore Flasher ↗](https://meshcore.co.uk/flasher.html) | meshcore.co.uk | Download van OTAFIX bootloader (`sensecap_solar_bootloader-0.9.2-OTAFIX2.1.uf2`) |
| [nRF Device Firmware Update (Android) ↗](https://play.google.com/store/apps/details?id=no.nordicsemi.android.dfu) | Nordic Semiconductor | Referentie-implementatie van het Nordic Secure DFU-protocol (Android app) |
| [Adafruit nRF52 Bootloader ↗](https://github.com/adafruit/Adafruit_nRF52_Bootloader) | Adafruit / GitHub | Broncode van de stock bootloader waarop OTAFIX is gebaseerd |
| [OTAFIX Bootloader (GitHub) ↗](https://github.com/oltaco/Adafruit_nRF52_Bootloader_OTAFIX) | oltaco / GitHub | Broncode en changelog van OTAFIX 2.0 en 2.1, inclusief aanbevolen instellingen per versie |

Disclaimer
— Dit document is met zorg samengesteld op basis van uitgebreide praktijktests uitgevoerd op 7 en 8 april 2026. Op het moment van testen was geen andere robuuste methode bekend voor het uitvoeren van een betrouwbare OTA firmware-update op de SenseCAP Solar Node P1-Pro zonder fysieke toegang tot het apparaat. Dit sluit niet uit dat er alternatieve methoden bestaan of in de tussentijd beschikbaar zijn gekomen. De beschreven werkwijze is het resultaat van reproduceerbaar geteste procedures, maar firmware-updates worden altijd uitgevoerd op eigen verantwoordelijkheid. De auteur aanvaardt geen aansprakelijkheid voor schade aan apparatuur of verlies van functionaliteit als gevolg van het toepassen van de informatie in dit document. Raadpleeg bij twijfel de actuele documentatie van Nordic Semiconductor, Seeed Studio en het MeshCore-project.
