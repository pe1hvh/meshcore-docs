# De vier platformfamilies

*ESP32 · NRF52840 · RP2040 · STM32WL*

Vier families, één firmware. ESP32, nRF52840, RP2040 en STM32WL delen
dezelfde broncode, maar elke chip brengt zijn eigen cores, geheugen,
transporten en beperkingen mee. Dit hoofdstuk loopt ze één voor één langs:
wat de chip meebrengt en wat hij kost. De vergelijking, de apparatenlijst
en de keuzehulp staan in [MeshCore Platforms](platforms.md).

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0 (`FIRMWARE_BUILD_DATE "6 Jun 2026"`), commit
> `03b6ef4`, 28 juli 2026 — `platformio.ini`, `variants/*/platformio.ini`
> (79 mappen, 507 build-targets), `boards/*.json` (41 definities),
> `examples/companion_radio/main.cpp` en
> `docs/nrf52_power_management.md`. Alle tellingen in dit hoofdstuk zijn
> ook gecontroleerd op commit `a3a1aa5` (19 juli 2026) en daar identiek.
> Reproduceren kan met [`tools/platform-overview.py`](../../tools/platform-overview.py).

## ESP32 — het veelzijdige werkpaard

### Vier SoC's onder één noemer

`[esp32_base]` (`platformio.ini` r.57-65) dekt vier verschillende chips.
De 37 varianten verdelen zich grofweg zo: ongeveer 24 gebruiken een
ESP32-S3, zes de klassieke ESP32, vier een C3 en drie een C6. Dat zijn ook
twee verschillende processorarchitecturen: Xtensa LX6 in de klassieke
ESP32, Xtensa LX7 in de S3, en RISC-V in de C3 en C6.

De C6 is een randgeval. `[esp32c6_base]` (r.72-76) erft van `esp32_base`,
maar haalt zijn platform van een andere URL — pioarduino met
Arduino-ESP32 3.x. Daarboven staat in de repo zelf de opmerking dat het
experimenteel is en mogelijk minder stabiel dan de andere platforms
(r.73). Drie varianten, zestien build-targets, en — zie de tabel verderop
— geen enkel kant-en-klaar apparaat in de web flasher.

### Wat je ervoor terugkrijgt

ESP32 is de enige familie met WiFi (17 build-targets), de enige met OTA
(36 varianten laden `[esp32_ota]`, r.67-70) en de enige met ESP-NOW
(`src/helpers/esp32/ESPNOWRadio.cpp`, 32 varianten). Daarbij 4 tot 16 MB
flash, PSRAM op de duurdere borden, en de meeste displayondersteuning na
nRF52.

`src/helpers/esp32/` is dan ook de dikste hulpmap van de vier: BLE, WiFi,
ESP-NOW, bordklassen. Ter vergelijking: `src/helpers/nrf52/` bevat
alleen een BLE-interface, en `src/helpers/rp2040/` bestaat niet.

### Wat het kost

De hoogste kloksnelheid van de vier — 240 MHz — en het hoogste verbruik.
De firmware heeft voor ESP32 geen ingebouwd powermanagement zoals nRF52
dat wel heeft. Er is een build-flag `ESP32_CPU_FREQ` in `platformio.ini`
(r.64), maar die staat uitgecommentarieerd; verlagen doe je zelf.

## nRF52840 — de zuinige

### Een eigen fork van de Adafruit-core

`[nrf52_base]` (r.80-95) gebruikt geen standaard Arduino-core maar een
eigen fork:

```text
platform_packages =
  framework-arduinoadafruitnrf52 @
    https://github.com/meshcore-dev/Adafruit_nRF52_Arduino#d541301
```

De reden staat er in het commentaar bij: een patch op de BLE-stack die
firmware-lockups voorkomt bij snel achter elkaar verbinden en verbreken
(PR #1177 en #1295).

Op twee van de 34 nRF52-varianten geldt dat niet:
`variants/heltec_mesh_solar/platformio.ini` r.4 en
`variants/mesh_pocket/platformio.ini` r.4 zetten
`platform_packages = framework-arduinoadafruitnrf52` zonder URL, dus de
gewone Adafruit-core, plus een ouder SoftDevice-linkerscript
(`nrf52840_s140_v6.ld`). Wie daar BLE-problemen ziet, weet nu waar te
kijken.

Verder: 64 MHz, 230 KB RAM, 792 tot 796 KB flash voor de applicatie, en
twee filesystems — `InternalFS` plus een extra volume dat via `EXTRAFS=1`
wordt meegecompileerd.

### Powermanagement: wat er is en waar het ontbreekt

`docs/nrf52_power_management.md` (217 regels) beschrijft wat er kan:
wakker worden op LPCOMP of VBUS, `SYSTEMOFF`, en het vastleggen van de
reden van een shutdown. Dit is het enige platform waar de firmware
hier echt iets aan doet.

Maar lees de tabel *Supported Boards* (r.38-57) erbij: van de negentien
vermelde borden staan er **vijf** op "Implemented" — XIAO nRF52840,
RAK4631, Heltec T114, GAT562 Mesh Watch13 en SenseCAP Solar. De andere
veertien staan op "No", waaronder populaire keuzes als T-Echo, T1000-E,
Nano G2 Ultra, ProMicro, Mesh Pocket en de ThinkNode M1/M3/M6.

"nRF52 is de zuinige familie" klopt op chipniveau. Of jouw bord die
zuinigheid ook echt benut, staat in die tabel.

### De meeste BLE-targets van allemaal

Veertig van de 199 nRF52-build-targets zijn een BLE-companion. Dat is er
twee meer dan de hele ESP32-familie, die drie keer zoveel targets heeft.

## RP2040 — de eenvoudige

### Alleen USB-serial

Vier varianten, 22 build-targets, geen enkele met BLE of WiFi. De takken
staan er wel, maar uitgecommentarieerd
(`examples/companion_radio/main.cpp` r.55-66), en alle vier de varianten
zetten `lib_ignore = BLE`. Dat geldt ook voor de Pico W, die de hardware
er wél voor heeft.

Wat overblijft: repeater, room server, KISS modem, terminal chat en een
companion over USB. Geen enkele variant heeft een display, en er is geen
`src/helpers/rp2040/`-map.

De vier borden gebruiken de ingebouwde definities van PlatformIO, niet een
eigen `boards/*.json`. Daarom staan de RP2040-cijfers in tabel 1 met een
sterretje.

## STM32WL — de geïntegreerde

### De radio zit op de die

Alle vier de STM32WL-varianten zetten `SPI_INTERFACES_COUNT=0` en
`RADIO_CLASS=CustomSTM32WLx`, en `[stm32_base]` laadt de
SubGhz-bibliotheek uit de STM32duino-core (`platformio.ini` r.115, 120).
Er is geen losse SX126x en geen SPI-bus naar de radio: de LoRa-transceiver
zit op dezelfde die als de processor. Hoe die library binnenkomt en wat
MeshCore ermee doet, staat in [SubGhz](../libraries/core/subghz.md).

![Twee blokschema's naast elkaar. Links een MCU met zes SPI-lijnen naar
een losse SX1262-radiochip. Rechts één STM32WLE5-blok met de SubGHz-radio
erin en geen SPI-verbinding.](../../images/nl/platform-families-1.svg)

### 64 KB RAM en 224 KB flash

Uit `boards/rak3172.json` en `boards/tiny_relay.json`: `stm32wle5ccu`,
48 MHz, 65536 bytes RAM en 262144 bytes flash. Van die flash blijft niet
alles over voor de applicatie. Alle vier de varianten zetten:

```text
board_upload.maximum_size = 229376 ; 32kb for FS
```

Dus 224 KB voor de app en 32 KB voor het filesystem. Dat is een factor
drie minder RAM dan nRF52 en een factor twintig minder flash dan een ruim
bemeten ESP32. Het raakt direct aan instellingen als `MAX_CONTACTS` en
`MAX_NEIGHBOURS`, die per build-target worden gezet.

Eén van de vier varianten heeft een display (`wio-e5-mini`). Een
companion is er alleen over USB.

Hoe deze vier zich op rekenkracht, geheugen, connectiviteit, opslag,
energie en flashgemak tot elkaar verhouden — en welk platform bij welke
rol past — staat in [MeshCore Platforms](platforms.md).

Hoe de firmware de vier verschillen technisch opvangt — welke bordklasse per
familie gedeeld wordt, waarom RP2040 er als enige geen heeft, en waarom de
opslagkeuze de scherpste scheidslijn is — staat in
[Platformrealisatie](../ontwerp/technisch/platform-realisation.md).

## Bronnen

Firmware: [meshcore-dev/MeshCore](https://github.com/meshcore-dev/MeshCore),
branch `main`, commit `03b6ef4`, 28 juli 2026, v1.16.0.

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/platformio.ini)
  — r.57-65 `[esp32_base]`; r.72-76 `[esp32c6_base]` met het
  "experimental"-commentaar op r.73; r.80-95 `[nrf52_base]` met de eigen
  Adafruit-fork; r.98-104 `[rp2040_base]`; r.108-120 `[stm32_base]` met de
  SubGhz-bibliotheek op r.115 en 120
- [`variants/heltec_mesh_solar/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/heltec_mesh_solar/platformio.ini)
  r.4 en
  [`variants/mesh_pocket/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/mesh_pocket/platformio.ini)
  r.4 — de core-override zonder URL
- [`variants/rak3x72/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/rak3x72/platformio.ini)
  r.4 en
  [`variants/tiny_relay/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/variants/tiny_relay/platformio.ini)
  r.4 — `board_upload.maximum_size`
- [`boards/rak3172.json`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/boards/rak3172.json),
  [`boards/tiny_relay.json`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/boards/tiny_relay.json)
  en
  [`boards/rak4631.json`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/boards/rak4631.json)
  — `mcu`, `f_cpu`, `maximum_ram_size` en `maximum_size`
- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/main.cpp)
  — r.15-35 het filesystem per platform; r.37-85 de transportlaag per
  platform; r.55-66 de uitgecommentarieerde WiFi- en BLE-takken voor
  RP2040
- [`docs/nrf52_power_management.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/docs/nrf52_power_management.md)
  — 217 regels, met de tabel *Supported Boards* op r.38-57

Niet uit de firmware-repo:

- [RP2040 Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf),
  Raspberry Pi Ltd — kloksnelheid, SRAM en flash van de RP2040
- Espressif-datasheets — de specificaties per ESP32-sub-SoC
