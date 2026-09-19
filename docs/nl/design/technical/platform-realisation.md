# Platformrealisatie

*OPSLAG · BORDKLASSEN · ASYMMETRIE · VIER FAMILIES*

Vier platformfamilies, één codebase. Dit hoofdstuk beschrijft waar die vier
uit elkaar lopen en hoe de firmware dat opvangt. De scherpste scheidslijn ligt
niet bij de radio of het scherm maar bij het bestandssysteem, en de manier
waarop die keuze wordt gemaakt verraadt iets over hoe de ondersteuning is
gegroeid.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — `src/helpers/IdentityStore.h`,
> `src/helpers/ESP32Board.h`, `src/helpers/NRF52Board.h`,
> `src/helpers/stm32/STM32Board.h` en de bordklassen in `variants/`.

## Opslag is de scheidslijn

Welke bestandssysteemlaag een build gebruikt, wordt met een macro gekozen. De
vier families vallen daarbij in twee kampen.

`src/helpers/IdentityStore.h` r.3-11

```cpp
#if defined(ESP32) || defined(RP2040_PLATFORM)
  #include <FS.h>
  #define FILESYSTEM  fs::FS
#elif defined(NRF52_PLATFORM) || defined(STM32_PLATFORM)
  #include <Adafruit_LittleFS.h>
  #define FILESYSTEM  Adafruit_LittleFS

  using namespace Adafruit_LittleFS_Namespace;
#endif
```

ESP32 en RP2040 krijgen `fs::FS`, de Arduino-abstractie boven een
bestandssysteem. nRF52 en STM32 krijgen `Adafruit_LittleFS`, een aparte
implementatie met een eigen namespace. Geen enkele component vanaf
`IdentityStore` naar boven merkt nog verschil tussen beide bestandssystemen:
alles werkt met `FILESYSTEM`.

## De asymmetrie in de test zelf

Let op hoe de vier families in dat fragment worden herkend. Drie ervan aan hun
eigen `*_PLATFORM`-macro, één niet:

| Familie | Herkend aan | Van wie is die macro |
|---|---|---|
| ESP32 | `ESP32` | Arduino-ESP32-core |
| RP2040 | `RP2040_PLATFORM` | MeshCore |
| nRF52 | `NRF52_PLATFORM` | MeshCore |
| STM32 | `STM32_PLATFORM` | MeshCore |

MeshCore definieert wél een `ESP32_PLATFORM`, maar die wordt in de hele
broncodestructuur nergens gelezen — niet in `src/`, niet in `examples/`, niet
in `variants/`. Hij bestaat en doet niets, omdat ESP32-code de core-macro
`ESP32` gebruikt die er toch al is. Zie [Compile-time
configuratie](configuration.md).

Dat is geen fout: het werkt. Maar het betekent wel dat wie een vijfde familie
zou toevoegen, niet één patroon aantreft om na te volgen maar twee.

## Bordklassen per familie

Het bordcontract `mesh::MainBoard` (`src/MeshCore.h` r.45) legt vast wat elk
bord moet kunnen: batterijspanning geven, herstarten, slapen, de opstartreden
melden. Drie families implementeren dat met een gedeelde klasse waar de
variantklassen van erven. De vierde niet.

| Familie | Gedeelde bordklasse | Afgeleiden in `src/` | Targets |
|---|---|---|---|
| ESP32 | `ESP32Board` | `MeshadventurerBoard`, `TBeamBoard` | 270 |
| nRF52 | `NRF52Board` | `NRF52BoardDCDC` | 199 |
| STM32 | `STM32Board` | geen | 16 |
| RP2040 | **geen** | vier losse in `variants/` | 22 |

![Vier kolommen onder het contract mesh::MainBoard. Drie ervan hebben een
gedeelde bordklasse als tussenlaag met daaronder de variantklassen; de vierde
kolom, RP2040, verbindt vier variantklassen rechtstreeks met het contract
zonder tussenlaag.](../../../images/nl/platform-realisation-1.svg)

De vier RP2040-bordklassen — `RAK11310Board`, `PicoWBoard`, `WaveshareBoard`
en `XiaoRP2040Board` — erven rechtstreeks van `mesh::MainBoard` en schrijven
dus elk zelf uit wat de andere families van hun gedeelde ouder krijgen. Bij 22
targets is dat te overzien; het is de reden dat er geen `RP2040Board` is
gekomen.

## Hoeveel code er per familie gedeeld wordt

| Bestand | Regels |
|---|---|
| `src/helpers/ESP32Board.h` | 186 |
| `src/helpers/ESP32Board.cpp` | 47 |
| `src/helpers/NRF52Board.h` | 78 |
| `src/helpers/NRF52Board.cpp` | 366 |
| `src/helpers/stm32/STM32Board.h` | 44 |

De verhouding is omgekeerd aan wat je zou verwachten. nRF52 draagt minder
targets dan ESP32 maar heeft bijna acht keer zoveel implementatiecode: 366
regels tegen 47. Dat zit in het energiebeheer. De nRF52-borden schakelen
tussen een DC/DC-omzetter en een lineaire regelaar, lezen de batterij via een
ADC met eigen referentiespanning, en beheren de slaapstand zelf.
ESP32Board laat het meeste daarvan aan de Arduino-core over.

STM32 komt met 44 regels in één header toe en heeft geen `.cpp`. Er zijn 16
targets, alle op dezelfde SoC-familie, met dezelfde radio erop — er valt weinig
te variëren.

## Wat een familie verder deelt

Naast de bordklasse hebben ESP32, nRF52 en STM32 een eigen map onder
`src/helpers/`. Wat daarin staat, is geen platformverschil maar een
mogelijkheid die de andere families niet hebben:

| Map | Klassen | Waarom alleen daar |
|---|---|---|
| `esp32/` | `ESPNOWRadio`, `SerialBLEInterface`, `SerialWifiInterface`, `TBeamBoard` | ESP32 heeft BLE, WiFi én ESP-NOW |
| `nrf52/` | `SerialBLEInterface` | nRF52 heeft alleen BLE |
| `stm32/` | `STM32Board` | STM32 heeft geen van beide |

RP2040 heeft geen map. Een RP2040-node praat over USB-serieel met de
telefoon-app, niet over BLE of WiFi.

## De klok als tegenvoorbeeld

Niet elke abstractie splitst per familie. Het klokcontract `mesh::RTCClock`
(`src/MeshCore.h` r.80) wordt op drie manieren geïmplementeerd, en die drie
snijden dwars door de families heen:

| Implementatie | Plek | Wanneer |
|---|---|---|
| `ESP32RTCClock` | `src/helpers/ESP32Board.h` r.160 | ESP32 met interne RTC |
| `AutoDiscoverRTCClock` | `src/helpers/AutoDiscoverRTCClock.h` r.7 | Bord met een RTC-chip op I²C |
| `VolatileRTCClock` | `src/helpers/ArduinoHelpers.h` r.6 | Bord zonder RTC |

`AutoDiscoverRTCClock` zoekt bij het opstarten op de I²C-bus naar een bekende
RTC-chip en valt terug op een vluchtige klok als hij niets vindt. Dat is een
hardwareverschil dat niets met de platformfamilie te maken heeft: dezelfde
ESP32-familie bevat borden mét en zonder RTC-chip.

## Bronnen

- [MeshCore `03b6ef4` — `src/helpers/IdentityStore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/IdentityStore.h)
- [MeshCore `03b6ef4` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore `03b6ef4` — `src/helpers/ESP32Board.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ESP32Board.h)
- [MeshCore `03b6ef4` — `src/helpers/NRF52Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/NRF52Board.cpp)
- [MeshCore `03b6ef4` — `src/helpers/stm32/STM32Board.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/stm32/STM32Board.h)
