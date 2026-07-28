# Hardware Overzicht

*APPARATEN · VERGELIJKING · OFFLINE KAARTEN*

MeshCore ondersteunt een breed scala aan hardware. De apparaten zijn in te delen in drie categorieën: **Companion Radios** (vereisen smartphone), **Standalone Apparaten** (eigen scherm en toetsenbord), en **Repeaters/Servers** (uitbreiden van het netwerk).

> [!WARNING]
> **Let op:** Controleer altijd of het apparaat de juiste frequentie voor Europa heeft (868 MHz, niet 915 MHz).

## Hardware

### LilyGO T-Deck Plus — €70–80

**LilyGO · ESP32-S3** · 2.8" LCD · QWERTY toetsenbord · GPS · Trackball · SMA connector

- ✓ Volledig zelfstandig
- ✓ Fysiek toetsenbord
- ✓ GPS ingebouwd
- ✓ Externe antenne mogelijk
- ✗ Trackball soms gevoelig
- ✗ Reset knop kan per ongeluk ingedrukt worden

**Beste voor:** Standalone gebruik zonder smartphone

### Heltec WiFi LoRa 32 V3/V4 — €20–40

**Heltec · ESP32-S3 · SX1262** · 0.96" OLED · WiFi · BLE · V4: 28dBm TX

- ✓ Zeer betaalbaar
- ✓ Compact, breed ondersteund
- ✓ Geschikt als companion én repeater
- ✗ Vereist smartphone
- ✗ Klein scherm, geen behuizing standaard

**Beste voor:** Budget instap met smartphone

### RAK WisBlock RAK4631 — €40–60

**RAKwireless · nRF52840** · Modulair systeem · Extreem laag verbruik · Uitbreidingsmodules

- ✓ Extreem laag verbruik (weken/maanden op batterij)
- ✓ Modulair, perfect voor solar
- ✓ Professionele kwaliteit
- ✗ Duurder, geen WiFi (alleen BLE)
- ✗ Complexere setup

**Beste voor:** Energiezuinige en modulaire oplossingen

### Seeed Studio T1000-E — €30–40

**Seeed Studio · nRF52840** · Creditcard-formaat · GPS · BLE · Laag verbruik

- ✓ Zeer compact
- ✓ Ingebouwde GPS
- ✓ Laag verbruik, robuust
- ✗ Geen display of knoppen
- ✗ Vereist smartphone voor alle interactie

**Beste voor:** Compacte companion radio met GPS

> [!NOTE]
> **Chip versus bord.** Deze pagina gaat over apparaten. Waarom de chip erin bepaalt wat het apparaat kan — BLE, WiFi, display, OTA, flashmethode — staat in [MeshCore Platforms](../platform/platforms.md). Wat er per familie precies in de chip zit, staat in [De vier platformfamilies](../platform/platform-families.md).

## Vergelijkingstabel

| Apparaat | Chip | Display | GPS | WiFi | Prijs |
|---|---|---|---|---|---|
| T-Deck Plus | ESP32-S3 | 2.8" LCD | Ja | Ja | €70–80 |
| Heltec V3/V4 | ESP32-S3 | 0.96" OLED | Nee | Ja | €20–40 |
| RAK4631 | nRF52840 | Nee | Module | Nee | €40–60 |
| T1000-E | nRF52840 | Nee | Ja | Nee | €30–40 |

## Offline Kaarten op T-Deck

De T-Deck Plus kan offline kaarten weergeven via een microSD-kaart (max 32 GB, FAT32). Meerdere methoden zijn beschikbaar:

- **Map Tiles Downloader** (aanbevolen) — Tool van OM7TEK via `pipx install mt-downloader`
- **tdeck-maps script** — Python script voor specifieke steden/regio's
- **Kant-en-klare kaarten** — Beschikbaar via buymeacoffee.com/ripplebiz

> [!NOTE]
> **Tip:** Begin met zoomlevel 8–12 voor een goede balans tussen detail en opslagruimte. Diepere zoom (13+) vereist een Ultra-licentie. De SD-kaart moet geplaatst zijn vóór het inschakelen van de T-Deck.
