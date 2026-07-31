# Compile-time configuratie

*277 MACRO'S · DRIE EIGENAREN · 53 ONGELEZEN · MEETMETHODE*

De tachtig `platformio.ini`-bestanden definiëren samen 277 unieke
`-D`-macro's. Dit hoofdstuk deelt ze in naar eigenaar — library, Arduino-core
of MeshCore zelf — en gaat daarna in op de belangrijkste bevinding: van de 254
MeshCore-macro's worden er 53 gedefinieerd en nergens gelezen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — de root `platformio.ini`, alle 79
> `variants/*/platformio.ini` en de volledige broncodestructuur onder `src/`,
> `examples/` en `variants/`.

## Drie eigenaren

Een macro hoort bij degene die hem leest, niet bij degene die hem definieert.
Alle 277 worden in MeshCores eigen ini-bestanden gezet, maar ze komen bij drie
verschillende partijen terecht.

| Groep | Macro's | Gelezen door |
|---|---|---|
| 1 — library | 17 | Een externe library |
| 2 — framework | 6 | Een Arduino-core |
| 3 — MeshCore | 254 | MeshCores eigen bronbestanden |

![Drie stapels. Links zeventien macro's met een pijl naar een blok externe
libraries, in het midden zes met een pijl naar een blok Arduino-core, rechts
tweehonderdvierenvijftig met een pijl naar de MeshCore-broncodestructuur. Van
die derde stapel loopt een deel van drieënvijftig naar een leeg vlak zonder
lezer.](../../../images/nl/configuration-1.svg)

Groep 1 staat uitgeschreven in
[Library-configuratie](../../libraries/library-configuration.md), waar hij
thuishoort: die macro's zeggen iets over de libraries, niet over MeshCore.

Twee macro's staan uitgecommentarieerd en zijn dus in geen enkele build
actief: `RADIOLIB_DEBUG_BASIC` en `RADIOLIB_DEBUG_SPI`. Ze tellen niet mee in
de 277.

## Groep 2 — framework (6)

| Macro | Consument |
|---|---|
| `ARDUINO_LOOP_STACK_SIZE` | Arduino-ESP32-core |
| `ARDUINO_RAKWIRELESS_RAK11300` | arduino-pico-core |
| `ARDUINO_USB_CDC_ON_BOOT` | Arduino-ESP32-core |
| `ARDUINO_USB_MODE` | Arduino-ESP32-core |
| `ARDUINO_heltec_wifi_lora_32_V3` | Arduino-ESP32-core |
| `CORE_DEBUG_LEVEL` | Arduino-ESP32-core |

Vijf van de zes zijn ESP32-macro's. Dat is geen toeval: de Arduino-ESP32-core
laat meer via buildvlaggen instellen dan de andere drie cores, met name rond
USB en het serieel-over-USB-gedrag bij het opstarten.

## Groep 3 — MeshCore (254)

Van de 254 MeshCore-macro's worden er **201** ergens in de broncodestructuur
gelezen en **53** nergens.

De 201 naar de plek waar ze voor het eerst voorkomen:

| Waar | Macro's |
|---|---|
| `variants/` | 48 |
| `src/helpers/ui/` | 35 |
| `examples/` | 29 |
| `src/helpers/` (kern) | 28 |
| `src/helpers/sensors/` | 28 |
| `src/helpers/esp32,nrf52,stm32/` | 21 |
| `src/helpers/radiolib/` | 8 |
| `src/` | 2 |
| `src/helpers/bridges/` | 2 |

Twee macro's in `src/` — dat is de hele kern. Alles wat met een buildvlag te
sturen valt, zit in de lagen eromheen. De kern zelf is niet configureerbaar en
compileert in elke build hetzelfde.

Een paar voorbeelden van plekken waar zo'n macro wordt gelezen. Dit zijn
representatieve leesplekken, niet noodzakelijk het eerste voorkomen dat de
tabel hierboven telt:

| Macro | Gelezen in |
|---|---|
| `ADVERT_NAME` | `examples/simple_repeater/MyMesh.cpp` r.22 |
| `MAX_NEIGHBOURS` | `examples/simple_repeater/MyMesh.cpp` r.64 |
| `DISPLAY_CLASS` | `examples/simple_repeater/main.cpp` r.6 |
| `WITH_RS232_BRIDGE` | `src/helpers/CommonCLI.cpp` r.720 |
| `P_LORA_NSS` | `src/helpers/MeshadventurerBoard.h` r.7 |

> [!NOTE]
> **Meetmethode.** De verdelingstabel telt per macro het **eerste voorkomen**
> van de naam in de broncodestructuur, doorlopen in de volgorde `src/` →
> `examples/` → `variants/` en binnen elke map alfabetisch. Die volgorde hoort
> bij het cijfer: een andere doorloopvolgorde verschuift de tabel met tot 22
> macro's.
>
> Eerste voorkomen is niet hetzelfde als eerste *lezing*. `P_LORA_NSS` in
> `MeshadventurerBoard.h` r.7 is een `#define`, dus een herdefinitie en geen
> test. De macro's in de voorbeeldtabel hierboven zijn gekozen omdat ze
> illustratief zijn, niet omdat ze het eerste voorkomen zijn.

## De 53 die nergens gelezen worden

Eenentwintig procent van de MeshCore-macro's wordt gedefinieerd en nooit
getest. Ze vallen in drie groepen uiteen.

### Bordmarkeringen (35)

`EBYTE_EORA_S3`, `GENERIC_E22`, `HELTEC_HT_CT62`, `HELTEC_LORA_V2`,
`HELTEC_LORA_V3`, `HELTEC_LORA_V4`, `HELTEC_MESH_POCKET`, `HELTEC_T114`,
`HELTEC_WIRELESS_PAPER`, `KEEPTEEN_LT1`, `LILYGO_T3S3`, `LILYGO_TETH_ELITE`,
`LILYGO_TLORA`, `LILYGO_T_ETH_ELITE_ESP32S3`, `MESHADVENTURER`, `MESHTINY`,
`NIBBLE_SCREEN_CONNECT`, `PROMICRO`, `RAK_11310`, `RAK_3112`, `RAK_3401`,
`RAK_3X72`, `SEEED_XIAO_S3`, `STATION_G2`, `STATION_G3_ESP32`, `T1000_E`,
`TBEAM_1W`, `THINKNODE_M2`, `THINKNODE_M3`, `THINKNODE_M5`,
`Vision_Master_E213`, `Vision_Master_E290`, `WIO_TRACKER_L1`,
`WIRELESS_PAPER`, `me25ls01`.

Elk variantbestand definieert zijn eigen naam als macro. Niets test erop,
omdat de variant al zijn eigen `-I`-pad meekrijgt en dus zijn eigen headers
ziet. Ze zijn documentatie in de vorm van een macro: je leest in de
`platformio.ini` welk bord het is, en de compiler doet er niets mee.

### Platformmarkering (1)

`ESP32_PLATFORM`. De andere drie platformmacro's — `NRF52_PLATFORM`,
`RP2040_PLATFORM`, `STM32_PLATFORM` — wórden gelezen; deze niet, omdat
ESP32-code de core-macro `ESP32` gebruikt die er toch al is. Zie
[Platformrealisatie](platform-realisation.md).

### Overig (17)

`BOARD_HAS_PSRAM`, `DISABLE_DIAGNOSTIC_OUTPUT`, `DISPLAY_LINES`,
`ENABLE_HWSERIAL2`, `HAS_NEOPIXEL`, `HAS_TOUCH`, `IO_EXPANDER_IRQ`,
`LINE_LENGTH`, `NDEBUG`, `NEOPIXEL_COUNT`, `NEOPIXEL_DATA`, `NEOPIXEL_TYPE`,
`PIN_SERIAL_RX`, `PIN_SERIAL_TX`, `P_LORA_TX_LED_ON`, `UI_GPS_PAGE`,
`WITH_ESPNOW_BRIDGE_SECRET`.

> [!IMPORTANT]
> Deze zeventien zijn niet allemaal dood. `NDEBUG` is standaard C en wordt
> door de standaardbibliotheek gelezen; `BOARD_HAS_PSRAM`, `PIN_SERIAL_RX`,
> `PIN_SERIAL_TX` en `ENABLE_HWSERIAL2` worden door een Arduino-core gelezen.
> Die vijf horen dus in groep 2 en niet in groep 3. De eigendomstabel
> `NAMESPACES` in `tools/config-flags.py` deelt ze verkeerd in, omdat die op
> naamvoorvoegsel werkt en deze vijf geen herkenbaar voorvoegsel hebben. Het
> script kan ze sinds deze oplevering apart tonen, maar de indeling is niet
> stil rechtgezet: dat vraagt een aparte beslissing.

De overige twaalf, waaronder `HAS_NEOPIXEL`, `NEOPIXEL_COUNT` en
`UI_GPS_PAGE`, wijzen naar functionaliteit die in deze commit niet bestaat. De
buildvlaggen zijn er, de code die erop reageert niet — of niet meer.

## Wat dit betekent

Een macro die nergens gelezen wordt is niet gevaarlijk, maar hij is wel
misleidend. Wie `HAS_TOUCH` in een `platformio.ini` ziet staan, mag aannemen
dat er iets met aanraakbediening gebeurt. Dat gebeurt niet.

Voor wie een bord toevoegt is dat praktisch van belang: de bordmarkering
kopiëren heeft geen effect, en `UI_GPS_PAGE` inschakelen levert geen
GPS-pagina op. Wat wél werkt, is te zien aan de 201 macro's die wel een lezer
hebben.

## Narekenen

```bash
python3 tools/config-flags.py /pad/naar/MeshCore
python3 tools/config-flags.py /pad/naar/MeshCore --owners
python3 tools/config-flags.py /pad/naar/MeshCore --consumption
```

`--owners` schrijft groep 2 en 3 als markdowntabel; `--consumption` geeft per
MeshCore-macro het eerste bestand en regelnummer waar hij voorkomt, met een
expliciete categorie *nergens gelezen*. Het script slaat regels achter een `;`
over, zodat uitgecommentarieerde macro's de configuratie-oppervlakte niet
opblazen.

## Bronnen

- [MeshCore `03b6ef4` — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [MeshCore `03b6ef4` — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore `03b6ef4` — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore `03b6ef4` — `src/helpers/IdentityStore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/IdentityStore.h)
