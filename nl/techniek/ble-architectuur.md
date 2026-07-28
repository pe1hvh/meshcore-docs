# BLE Architectuur

*BLUETOOTH LOW ENERGY · GATT · NUS*

Dit hoofdstuk beschrijft hoe MeshCore via **Bluetooth Low Energy (BLE)** communiceert met companion-apparaten, en biedt een analyse van de BLE-stack en GATT-services.

## BLE vs. Classic Bluetooth

Sinds Bluetooth 4.0 (2010) zijn er twee afzonderlijke radiosystemen binnen de Bluetooth-standaard — het zijn **verschillende radioprotocollen** die niet rechtstreeks met elkaar communiceren.

| Eigenschap | Classic Bluetooth (BR/EDR) | BLE |
|---|---|---|
| Stroomverbruik | Hoog | Zeer laag |
| Datasnelheid | Hoog | Laag |
| Kanalen | 79 × 1 MHz | 40 × 2 MHz |
| Typisch gebruik | Audio, bestanden | Sensoren, IoT, MeshCore |

De T1000-E is een **BLE-only** apparaat. Je smartphone is dual-mode: hij praat met je Bluetooth-koptelefoon (Classic) én met je MeshCore radio (BLE).

## De BLE-stack (7 lagen)

BLE Stack SVG

![Diagram 1 bij ble-architectuur](../../images/nl/ble-architectuur-1.svg)

## GATT — Generic Attribute Profile

GATT is de structuur waarmee BLE-apparaten hun data aanbieden. Zie het als een digitaal prikbord:

```text
Service (categorie)
  └── Characteristic (specifiek datapunt)
        └── Descriptor (extra configuratie)
```

### NUS — Nordic UART Service

NUS is een standaard BLE-service van Nordic Semiconductor die een seriële poort (UART) simuleert over Bluetooth. MeshCore gebruikt NUS voor alle communicatie met companion-apparaten.

```text
Nordic UART Service (NUS)
  ├── RX Characteristic → data van radio naar computer
  └── TX Characteristic → data van computer naar radio

UUID: 6e400001-b5a3-f393-e0a9-e50e24dcca9e
```

> [!NOTE]
> **NUS is geen protocol** — het is een servicespecificatie. GATT is het protocol, NUS is een service die via GATT wordt aangeboden.

## Officiële vs. Custom Services

| Type | UUID | Wie mag maken? | Voorbeeld |
|---|---|---|---|
| Officieel (SIG) | 16-bit | Alleen Bluetooth SIG | Heart Rate (0x180D) |
| Custom | 128-bit | Iedereen | NUS, MeshCore Companion |

### Bekende officiële services

| Service | UUID | Toepassing |
|---|---|---|
| Battery Service | 0x180F | Batterijniveau |
| Device Information | 0x180A | Fabrikant, model, firmware |
| Heart Rate | 0x180D | Hartslagmeters |
| Environmental Sensing | 0x181A | Temperatuur, vochtigheid, druk |
| HID over GATT | 0x1812 | Toetsenborden, muizen |
| Generic Access | 0x1800 | Verplicht — apparaatnaam |

## Notify vs. Read

| Methode | Werking | Wanneer |
|---|---|---|
| Read | Jij vraagt actief om data | Eenmalige waarden (bijv. batterijstatus) |
| Notify | Apparaat stuurt automatisch bij nieuwe data | Continue datastroom (bijv. berichten) |

Voor MeshCore gebruik je **Notify** — je wilt weten wanneer er een bericht binnenkomt. De CCCD (Client Characteristic Configuration Descriptor) is de aan/uit-schakelaar voor Notify.

> [!WARNING]
> **Cruciaal:** Slechts één client tegelijk kan Notify activeren. Een tweede client krijgt de foutmelding `Notify acquired`.

## Pairing, Bonding en Trust

| Stap | Wat gebeurt er | Analogie |
|---|---|---|
| Pairing | Cryptografische sleutels uitwisselen | Telefoonnummers uitwisselen |
| Bonding | Sleutels permanent opslaan | Nummer opslaan in contacten |
| Trust | Apparaat automatisch vertrouwen | Iemand in favorieten zetten |

```text
# Controleer in Linux:
bluetoothctl info AA:BB:CC:DD:EE:FF | egrep -i "Paired|Bonded|Trusted"

# Verwacht:
Paired: yes
Bonded: yes
Trusted: yes
```

## BLE Kanaalindeling

De 2.4 GHz ISM-band (2400–2483.5 MHz) wordt verdeeld in **40 kanalen van elk 2 MHz**:

| Type | Kanalen | Functie |
|---|---|---|
| Advertising | 3 (nrs. 37, 38, 39) | Apparaten vinden, verbinding starten |
| Data | 37 (nrs. 0–36) | Daadwerkelijke communicatie |

Advertising-kanalen zijn strategisch gekozen om **Wi-Fi interferentie** te vermijden — ze zitten tussen de Wi-Fi kanalen 1, 6 en 11. Communicatie gebruikt **frequency hopping**: één kanaal tegelijk, steeds wisselend.

## Serieel vs. Gestructureerd

NUS is een **seriële service** — het simuleert een UART-poort met ongestructureerde bytes. Officiële SIG-services zijn **gestructureerd** met vaste velden.

| Aspect | Serieel (NUS) | Gestructureerd (SIG) |
|---|---|---|
| Data-indeling | Vrij, zelf bepalen | Vast, door specificatie |
| Parsing | Eigen parser bouwen | Standaard parser mogelijk |
| Interoperabiliteit | Alleen eigen software | Elke conforme app/device |
| Flexibiliteit | Maximaal | Beperkt tot spec |

### Waarom MeshCore NUS kiest

- **Flexibiliteit** — Het Companion Protocol heeft eigen framing nodig
- **Geen passende SIG-service** — Er bestaat geen "Mesh Radio Service" standaard
- **Bidirectioneel** — NUS biedt RX én TX characteristics
- **Eenvoud** — Geen complexe SIG-specificatie implementeren

## Ownership — Het kernprobleem

**Ownership** geeft aan welke client de actieve GATT-sessie met Notify bezit. Dit zit op **OSI laag 5 (sessie)**. Er mag maar één luisteraar tegelijk verbonden zijn.

| Typische "eigenaar" | Probleem | Oplossing |
|---|---|---|
| GNOME Bluetooth GUI | Notify acquired | GUI sluiten |
| bluetoothctl connect | Tool faalt bij notify | Altijd disconnect eerst |
| Telefoon Bluetooth aan | Telefoon claimt verbinding | BT uit op telefoon |
| Meerdere scripts | Eerste wint, rest faalt | Één tool tegelijk |

## BLE Pairing op Headless Linux

Bij het ontwikkelen van MeshCore toepassingen op een **desktop Linux-systeem** (Ubuntu, Fedora met GNOME of KDE) werkt BLE PIN-pairing doorgaans probleemloos. De desktopomgeving registreert automatisch een Bluetooth pairing agent via D-Bus, die PIN-verzoeken op de achtergrond afhandelt.

Op **headless systemen** — zoals een Raspberry Pi, server of embedded Linux zonder grafische omgeving — is er géén standaard pairing agent actief. De BlueZ `bluetoothd` daemon handelt pairing namelijk niet zelf af: hij delegeert elk PIN-verzoek via D-Bus naar een geregistreerde agent. Zonder agent blijven PIN-verzoeken onbeantwoord en mislukt de BLE-verbinding.

Dit maakt het probleem lastig te detecteren tijdens ontwikkeling: op een desktop werkt alles, maar bij deployment naar het headless doelsysteem — juist de meest voorkomende use case voor `meshcore_py` — faalt de verbinding.

### Overzicht per omgeving

| Omgeving | Standaard agent? | PIN-pairing werkt? |
|---|---|---|
| Ubuntu/Fedora Desktop (GNOME/KDE) | ✅ Desktop BT agent | ✅ Ja — agent handelt PIN stilletjes af |
| Raspberry Pi OS (headless) | ❌ Geen agent | ❌ Nee — PIN-verzoeken onbeantwoord |
| Raspberry Pi OS (met desktop) | ✅ Desktop BT agent | ✅ Waarschijnlijk wel |
| Fedora/Debian server (headless) | ❌ Geen agent | ❌ Nee — zelfde probleem |

### Oplossing

De fix is eenvoudig: registreer vóór het verbinden een eigen D-Bus pairing agent. Dit werkt op alle Linux-omgevingen — met of zonder desktop. Zie de bronvermelding hieronder voor een uitgebreide technische beschrijving en voorbeeldcode.

## Conclusie

MeshCore BLE companion werkt correct op Linux. Het enige vereiste is: **exact één actieve BLE client per radio**. De GATT/NUS-architectuur zorgt voor betrouwbare communicatie tussen node en companion-apparaat. Op headless systemen is daarnaast een eigen D-Bus pairing agent nodig voor succesvolle PIN-verificatie.

*De sectie over BLE pairing op headless Linux is gebaseerd op een bijdrage van PE1HVH aan [meshcore_py issue #33 ↗](https://github.com/meshcore-dev/meshcore_py/issues/33#issuecomment-3902438474).*
