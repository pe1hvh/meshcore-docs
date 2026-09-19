# MeshCore Platforms

*VERGELIJKEN · KIEZEN · WAT DE CHIP BEPAALT*

MeshCore draait op vier platformfamilies. Dezelfde broncode, hetzelfde
protocol, dezelfde radio — en toch kan de ene node dingen die de andere
niet kan. Dit hoofdstuk laat zien waarom het platform uitmaakt, hoe de vier
zich verhouden, wat er te koop is en hoe je kiest. Wat er in de chip zit,
staat in [De vier platformfamilies](platform-families.md).

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.17.1 (`FIRMWARE_BUILD_DATE "14 Aug 2026"`), commit
> `d929643`, 14 augustus 2026 — `platformio.ini`, `variants/*/platformio.ini`
> (87 mappen, 584 build-targets), `boards/*.json` (44 definities),
> `examples/companion_radio/main.cpp`, `src/helpers/IdentityStore.h` en
> `src/Utils.cpp`. Alle tellingen zijn ook tegen de vorige pin `03b6ef4`
> gedraaid; het verschil staat in
> [Wijzigingen in v1.17.1](../project/release-v1-17-1.md). De apparatenlijst
> komt uit `config.json` van
> [meshcore-dev/flasher.meshcore.io](https://github.com/meshcore-dev/flasher.meshcore.io),
> commit `b84f889`, 9 september 2026. Reproduceren kan
> met [`tools/platform-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/platform-overview.py).

## Waarom het platform uitmaakt

Neem het scherpste voorbeeld: een companion die via Bluetooth met je
telefoon praat. Die bestaat als build-target op ESP32 en op nRF52840, en
op geen van beide andere families. Niet omdat de hardware het niet kan —
de Raspberry Pi Pico W heeft Bluetooth aan boord — maar omdat de firmware
er geen implementatie voor heeft. In
`examples/companion_radio/main.cpp` r.55-66 staan de WiFi- en BLE-takken
voor RP2040 uitgecommentarieerd, en elke RP2040-variant zet
`lib_ignore = BLE`.

Zelfde protocol, zelfde radio, ander gedrag. Het platform bepaalt welke
transporten, opslag, displays en updatemethoden beschikbaar zijn.

Let op de woordkeuze. De firmware spreekt niet van microcontrollers maar
van **platforms**: de vier bouwdoelen heten `ESP32_PLATFORM`,
`NRF52_PLATFORM`, `RP2040_PLATFORM` en `STM32_PLATFORM`
(`platformio.ini` r.63, 90, 104, 113). En drie van de vier zijn strikt
genomen geen microcontroller maar een **SoC**: een chip met de radio erin.
Alleen de RP2040 is een kale microcontroller.

"MeshCore ondersteunt vier microcontrollers" is dus een dubbele
versimpeling. Het zijn vier platformbases in `platformio.ini`, met
minstens zeven verschillende SoC's en twee processorarchitecturen.

Wat een SoC precies onderscheidt van een MCU — en waarom elke SoC een MCU
bevat maar niet andersom — staat in
[Hardware van een node](../hardware/introduction.md).

## De vier families in één oogopslag

| Familie | SoC's | Core | Klok | RAM | Flash voor de app | Radio | Varianten | Build-targets |
|---|---|---|---|---|---|---|---|---|
| ESP32 | ESP32, S3, C3, C6 | Xtensa LX6/LX7 + RISC-V | 160–240 MHz | 320 KB, tot 8 MB met PSRAM | 4–16 MB | extern, via SPI | 43 | 332 |
| nRF52 | nRF52840 | Cortex-M4F | 64 MHz | 230 KB | 792–796 KB | extern, via SPI | 36 | 214 |
| RP2040 | RP2040 | 2× Cortex-M0+ | 133 MHz \* | 264 KB \* | 2 MB \* | extern, via SPI | 4 | 22 |
| STM32WL | STM32WLE5CCU | Cortex-M4 | 48 MHz | 64 KB | 224 KB | op de die (SubGHz) | 4 | 16 |

> [!NOTE]
> **\* Deze drie RP2040-cijfers staan niet in de MeshCore-repo.** De vier
> RP2040-borden gebruiken de ingebouwde bordendefinities van PlatformIO;
> er is geen `boards/*.json` voor. Bron voor kloksnelheid, RAM en flash is
> de [RP2040 Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)
> van Raspberry Pi Ltd. Alle overige cijfers in deze tabel komen uit
> `boards/*.json` en `variants/*/platformio.ini` in de firmware-repo.

![Vier kolommen naast elkaar met per platformfamilie de SoC, core, klok,
geheugen en een plus- of minteken voor BLE, WiFi, USB-serial, display, OTA
en ESP-NOW; onderaan het aantal apparaten in de web
flasher.](../../images/nl/platforms-1.svg)

Wat elke familie precies meebrengt — de SoC's onder de noemer, de cores,
het powermanagement en wat de chip vraagt aan geheugen en energie — staat
per familie uitgewerkt in
[De vier platformfamilies](platform-families.md).

## Vergelijking op zes assen

| As | ESP32 | nRF52840 | RP2040 | STM32WL |
|---|---|---|---|---|
| Rekenkracht | het hoogst, 160–240 MHz, S3 met vectorinstructies | 64 MHz met FPU | 133 MHz, twee cores, geen FPU | 48 MHz, het laagst |
| Geheugen | ruim; PSRAM mogelijk | ruim genoeg voor alle rollen | ruim genoeg voor alle rollen | krap: 64 KB RAM, 224 KB app-flash |
| Connectiviteit | BLE, WiFi, ESP-NOW, USB | BLE en USB | alleen USB | alleen USB |
| Opslag | SPIFFS op interne flash | `InternalFS` plus `EXTRAFS` | LittleFS | LittleFS-port in `arch/stm32/` |
| Energie | het hoogst; geen powermanagement in de firmware | het laagst; als enige actief ondersteund, maar op 5 van 19 borden | geen powermanagement in de firmware | zuinig van zichzelf; geen powermanagement in de firmware |
| Flashgemak | webflasher over USB | `.uf2` slepen, of OTA via Bluetooth | `.uf2` slepen | `.hex` met ST-Link of DFU |

> [!NOTE]
> **Geen verbruikscijfers.** In dit hoofdstuk staat geen enkel getal in mA.
> Die staan nergens in de firmware-repo, en cijfers uit datasheets zeggen
> weinig over een node met radio, display en GPS erbij. Voor het enige
> platform waar de firmware er echt iets aan doet, is
> `docs/nrf52_power_management.md` de plek om te kijken.

## Welke rollen draaien op welk platform

Harde telling van de `[env:]`-blokken in `variants/*/platformio.ini`. Een
getal is het aantal build-targets, niet het aantal borden — één bord
levert meestal vijf tot tien targets.

| Rol | ESP32 | nRF52 | RP2040 | STM32WL |
|---|---|---|---|---|
| companion BLE | 46 | 42 | 0 | 0 |
| companion WiFi | 25 | 0 | 0 | 0 |
| companion USB | 41 | 37 | 4 | 4 |
| companion serial | 3 | 0 | 0 | 0 |
| companion Ethernet | 1 | 1 | 0 | 0 |
| repeater | 95 | 45 | 6 | 5 |
| room server | 42 | 38 | 4 | **0** |
| sensor | 14 | 6 | **0** | 3 |
| KISS modem | 43 | 40 | 4 | 4 |
| terminal chat | 22 | 5 | 4 | 0 |
| **totaal** | **332** | **214** | **22** | **16** |

Twee gaten vallen op. STM32WL heeft geen enkele room server, en RP2040
geen enkele sensor-build. Dat is geen beperking van de chip maar een
keuze in de varianten: niemand heeft ze aangemaakt.

De rij *companion Ethernet* is nieuw in v1.17.1 en telt twee targets:
`RAK_4631_companion_radio_ethernet` en
`ThinkNode_M7_companion_radio_ethernet`. Er is ook één repeater en één room
server over Ethernet; die tellen mee in hun eigen rij. Wat je ermee kunt,
staat in [Ethernet](../cli/ethernet.md).

Van de 332 ESP32-targets komen er zestien van de drie C6-varianten: vijf
repeater, vijf companion BLE, drie KISS modem, twee room server en één
companion USB.

## Wat je vandaag kunt kopen en flashen

De firmware bouwt voor vier families. De
[web flasher](https://flasher.meshcore.io) — de weg die de meeste mensen
nemen — biedt er twee. In `config.json` van de flasher staan 66 regels voor
vijfenzestig apparaten; de LilyGo T-Lora Pager staat er twee keer in, één
keer per firmwareproject:

| Familie | Apparaten in de flasher | Aandeel | Varianten in de repo |
|---|---|---|---|
| ESP32 | 35 | 54 % | 43 |
| nRF52840 | 29 | 45 % | 36 |
| RP2040 | 1, en niet via de webflasher te flashen | 2 % | 4 |
| STM32WL | 0 | 0 % | 4 |

Negen van die vijfenzestig apparaten kunnen geen MeshCore draaien: de
flasher biedt er alleen Ripple-firmware voor aan. Welke dat zijn, staat in
[Nodematrix](node-matrix.md).

Het enige RP2040-apparaat in de lijst, de Pico met een WaveShare
SX1262-module, krijgt geen platform-icoon maar een generieke glyph. In de
configuratie van de flasher staat de reden: `"type": "noflash"`. Je krijgt
een link naar het `.uf2`-bestand en kopieert het zelf.

Voor STM32WL staat er niets. Wie zo'n node wil, compileert zelf en flasht
met ST-Link of DFU. Binnen MeshCore is STM32WL geen consumentenplatform
maar een bouwerplatform.

Binnen ESP32 is de S3 dominant: 28 van de 35 apparaten. Daarnaast vijf met
de klassieke ESP32 (Heltec v2, LilyGo LoRa32 v2.1_1.6 en de drie T-Beams)
en één met een C3 (Seeed Xiao C3); bij de T-Deck Pro v1.1 is het sub-SoC
onbekend. Op de vorige pin stonden hier vier klassieke ESP32's genoemd
terwijl het er vijf waren — de T-Beam 1W ontbrak in die opsomming. Van de C6, het sub-SoC met
het "experimenteel"-label, staat er geen enkel apparaat in de lijst.

> [!NOTE]
> **De flasherlijst is geen kopie van `variants/`.** Zeven ESP32-S3-
> apparaten in de lijst — de LilyGo T-Deck Max, T-Deck Pro, T-Display Pro,
> T-Lora Pager, T-Watch S3 Plus, T-Watch Ultra en T5 E-Paper S3 Pro —
> hebben geen variant in deze repo. Die draaien de gesloten Ripple GUI- of
> MeshOS-firmware. Andersom staan de vier STM32WL-varianten, drie van de
> vier RP2040-varianten, alle drie de C6-varianten en generieke doelen als
> `generic-e22` en `meshtiny` niet in de flasher.

## Hoe MeshCore de verschillen opvangt

### Eén API, vier cores

`framework = arduino` staat precies één keer in de hele repo:
`platformio.ini` r.17, in `[arduino_base]`. Alle vier de platformbases
erven daarvan, en geen van de 87 varianten overschrijft het.

Toch zijn het vier verschillende Arduino-cores: Arduino-ESP32 op ESP-IDF,
de Adafruit nRF52-core op de SoftDevice, de earlephilhower arduino-pico,
en STM32duino op de STM32 HAL. Dezelfde API, vier implementaties — vandaar
de `#ifdef`-ketens door de hele hulplaag.

Hoe scherp dat kan zijn, blijkt uit `examples/companion_radio/main.cpp`
r.5-6. Daar staat een eigen `_atoi()` met de opmerking dat de
standaard-C-functie op sommige platforms stuk is.

Een net voorbeeld van de omgekeerde beweging is
`src/helpers/IdentityStore.h` r.3-11, waar één macro vier gevallen
afdekt:

```text
#if defined(ESP32) || defined(RP2040_PLATFORM)
  #define FILESYSTEM  fs::FS
#elif defined(NRF52_PLATFORM) || defined(STM32_PLATFORM)
  #define FILESYSTEM  Adafruit_LittleFS
#endif
```

Alles daarboven — identiteiten opslaan, contacten bewaren — hoeft niet
meer te weten op welk platform het draait.

### De kern is niet Arduino-afhankelijk

De Arduino-afhankelijkheid zit in `src/helpers/` en `examples/`, niet in
de protocolkern. In `src/Utils.cpp` r.5-7 staat `#include <Arduino.h>`
achter `#ifdef ARDUINO`, en `src/MeshCore.h` r.25 en r.34 gebruiken
`ARDUINO` alleen om debug-uitvoer aan of uit te zetten.

Het bewijs staat onderaan `platformio.ini`: `[env:native]` (r.158-168)
bouwt tegen googletest, met `platform = native`, mocks uit `test/mocks/`
en zonder ook maar één regel Arduino. Daarom kan er een Zephyr-port van
MeshCore bestaan die precies hetzelfde protocol spreekt.

### Vier flashartefacten

| Platform | Buildscript | Resultaat | Hoe het op de node komt |
|---|---|---|---|
| ESP32 | `merge-bin.py` | één `.bin` | esptool of de webflasher |
| nRF52 | `create-uf2.py` | `.uf2` | slepen naar de USB-schijf, of OTA via Bluetooth |
| RP2040 | `upload_protocol = picotool` | `.uf2` | slepen naar de UF2-bootloader |
| STM32 | `arch/stm32/build_hex.py` | `.hex` via `objcopy -O ihex` | ST-Link of DFU |

Dat is meteen de verklaring voor de flashertabel hierboven. Alleen ESP32
en nRF52 hebben een artefact dat een webpagina rechtstreeks naar het
apparaat kan schrijven.

## Kiezen

![Beslisboom die begint met de vraag of de node met een telefoon moet
praten en via batterijduur en de behoefte aan WiFi, OTA of ESP-NOW
uitkomt op nRF52840, ESP32 of STM32WL.](../../images/nl/platforms-3.svg)

In woorden:

- **Koppeling met een telefoon nodig?** Dan ESP32 of nRF52840; de andere
  twee hebben geen BLE-companion.
- **Draait het op een batterij of zonnepaneel?** nRF52840 — maar
  controleer eerst of jouw bord in de tabel van
  `docs/nrf52_power_management.md` op "Implemented" staat.
- **WiFi, OTA of ESP-NOW nodig?** Alleen ESP32.
- **Kleine, zuinige repeater zonder telefoon, en je bouwt zelf?**
  STM32WL. Reken op 64 KB RAM en op flashen met ST-Link of DFU.
- **RP2040** is de keuze voor wie al een Pico heeft liggen en een
  repeater of USB-companion wil. Geen BLE, geen WiFi, geen display.

Welk concreet bord daarbij past, staat in
[Hardware Overzicht](../usage/hardware.md).

## Bronnen

Firmware: [meshcore-dev/MeshCore](https://github.com/meshcore-dev/MeshCore),
tag `companion-v1.17.1`, commit `d929643`, 14 augustus 2026, v1.17.1.

Apparatenlijst: `config.json` uit
[meshcore-dev/flasher.meshcore.io](https://github.com/meshcore-dev/flasher.meshcore.io),
commit `b84f889`, 9 september 2026.

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/platformio.ini)
  — r.16-53 `[arduino_base]` met `framework = arduino` op r.17; r.67-70
  `[esp32_ota]`; r.158-168 `[env:native]`
- [`variants/`](https://github.com/meshcore-dev/MeshCore/tree/d92964352441e53b93e8667b802e04f6e072b39e/variants)
  — 87 mappen met samen 584 `[env:]`-blokken
- [`boards/`](https://github.com/meshcore-dev/MeshCore/tree/d92964352441e53b93e8667b802e04f6e072b39e/boards)
  — 44 borddefinities met `mcu`, `f_cpu`, `maximum_ram_size` en
  `maximum_size`. Op de vorige pin stond hier 41; dat was het aantal
  bestanden in de map, inclusief vier linkerscripts, en niet het aantal
  `.json`-definities (37).
- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/companion_radio/main.cpp)
  — r.5-6 de eigen `_atoi()`
- [`src/helpers/IdentityStore.h`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/IdentityStore.h)
  — r.3-11 de `FILESYSTEM`-abstractie
- [`src/Utils.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/Utils.cpp)
  — r.5-7 `#ifdef ARDUINO`
- `merge-bin.py`, `create-uf2.py` en `arch/stm32/build_hex.py` — de drie
  buildscripts die de flashartefacten maken

Apparatenlijst: opgeslagen pagina van de
[MeshCore web flasher](https://flasher.meshcore.io), 27 juli 2026,
zestig apparaten.

Niet uit de firmware-repo:

- [RP2040 Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf),
  Raspberry Pi Ltd — kloksnelheid, SRAM en flash van de RP2040

Narekenen: [`tools/platform-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/platform-overview.py)
genereert tabel 1, 3 en 4 uit een kloon van de firmware-repo en een
opgeslagen flasherpagina.
