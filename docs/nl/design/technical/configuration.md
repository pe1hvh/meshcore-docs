# Compile-time configuratie

*330 MACRO'S · DRIE EIGENAREN · 55 ONGELEZEN · MEETMETHODE*

De achtentachtig `platformio.ini`-bestanden definiëren samen 330 unieke
`-D`-macro's. Dit hoofdstuk deelt ze in naar eigenaar — library, Arduino-core
of MeshCore zelf — en gaat daarna in op de belangrijkste bevinding: van de 302
MeshCore-macro's worden er 55 gedefinieerd en nergens gelezen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.17.1, commit `d929643`, 14 augustus 2026 — de root `platformio.ini`, alle
> 87 `variants/*/platformio.ini` en de volledige broncodestructuur onder
> `src/`, `examples/` en `variants/`.

## Drie eigenaren

Een macro hoort bij degene die hem leest, niet bij degene die hem definieert.
Alle 330 worden in MeshCores eigen ini-bestanden gezet, maar ze komen bij drie
verschillende partijen terecht.

| Groep | Macro's | Gelezen door |
|---|---|---|
| 1 — library | 17 | Een externe library |
| 2 — framework | 11 | Een Arduino-core |
| 3 — MeshCore | 302 | MeshCores eigen bronbestanden |

![Drie stapels. Links zeventien macro's met een pijl naar een blok externe
libraries, in het midden elf met een pijl naar een blok Arduino-core, rechts
driehonderdtwee met een pijl naar de MeshCore-broncodestructuur. Van
die derde stapel loopt een deel van vijfenvijftig naar een leeg vlak zonder
lezer.](../../../images/nl/configuration-1.svg)

Groep 1 staat uitgeschreven in
[Library-configuratie](../../libraries/library-configuration.md), waar hij
thuishoort: die macro's zeggen iets over de libraries, niet over MeshCore.

Zestien macro's komen uitsluitend op uitgecommentarieerde `-D`-regels voor
en zijn dus in geen enkele build actief. Ze tellen niet mee in de 330:

`ARDUHAL_LOG_LEVEL`, `BRIDGE_DEBUG`, `DEBUG_RP2040_CORE`,
`DEBUG_RP2040_PORT`, `DEBUG_RP2040_SPI`, `DEBUG_RP2040_WIRE`,
`ESPNOW_DEBUG_LOGGING`, `FORMAT_FS`, `GPS_NMEA_DEBUG`,
`HW_SPI1_DEVICE`, `MESH_PACKET_LOGGING`, `PICOW`,
`PIN_VIBRATION`, `RADIOLIB_DEBUG_BASIC`, `RADIOLIB_DEBUG_SPI`
en `STM32WL_TCXO_VOLTAGE`.

Op `03b6ef4` waren het er veertien; `GPS_NMEA_DEBUG` en `MESH_PACKET_LOGGING`
kwamen er in v1.17.1 bij. De lijst is te herhalen met
`tools/config-flags.py --commented`.

> [!NOTE]
> **Afwijking van de vorige uitgave.** Hier stond dat het er twee zijn:
> `RADIOLIB_DEBUG_BASIC` en `RADIOLIB_DEBUG_SPI`. Dat gold alleen voor de
> library-macro's van groep 1, niet voor het geheel.

## Groep 2 — framework (11)

| Macro | Consument |
|---|---|
| `ARDUINO_LOOP_STACK_SIZE` | Arduino-ESP32-core |
| `ARDUINO_RAKWIRELESS_RAK11300` | arduino-pico-core |
| `ARDUINO_USB_CDC_ON_BOOT` | Arduino-ESP32-core |
| `ARDUINO_USB_MODE` | Arduino-ESP32-core |
| `ARDUINO_heltec_wifi_lora_32_V3` | Arduino-ESP32-core |
| `BOARD_HAS_PSRAM` | Arduino-ESP32-core |
| `CORE_DEBUG_LEVEL` | Arduino-ESP32-core |
| `ENABLE_HWSERIAL2` | Arduino-ESP32-core |
| `NDEBUG` | C-standaardbibliotheek |
| `PIN_SERIAL_RX` | Adafruit nRF52-core |
| `PIN_SERIAL_TX` | Adafruit nRF52-core |

Acht van de elf zijn ESP32-macro's. Dat is geen toeval: de Arduino-ESP32-core
laat meer via buildvlaggen instellen dan de andere drie cores, met name rond
USB en het serieel-over-USB-gedrag bij het opstarten.

> [!NOTE]
> **Afwijking van de vorige uitgave.** Deze groep telde zes macro's. De laatste
> vijf — `BOARD_HAS_PSRAM`, `ENABLE_HWSERIAL2`, `NDEBUG`, `PIN_SERIAL_RX` en
> `PIN_SERIAL_TX` — stonden in groep 3 terwijl een core of de
> standaardbibliotheek ze leest. Ze hebben geen herkenbaar naamvoorvoegsel,
> waardoor de eigendomstabel `NAMESPACES` in `tools/config-flags.py` ze niet
> ving. Ze staan er nu als losse ingangen in. Groep 3 daalt daarmee van 307
> naar 302 en het aantal ongelezen macro's van 60 naar 55.

## Groep 3 — MeshCore (302)

Van de 307 MeshCore-macro's worden er **247** ergens in de broncodestructuur
gelezen en **60** nergens.

De 247 naar de plek waar ze voor het eerst voorkomen:

| Waar | Macro's |
|---|---|
| `variants/` | 63 |
| `src/helpers/ui/` | 47 |
| `src/helpers/` (kern) | 38 |
| `examples/` | 36 |
| `src/helpers/sensors/` | 27 |
| `src/helpers/esp32,nrf52,stm32/` | 21 |
| `src/helpers/radiolib/` | 11 |
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
| `WITH_RS232_BRIDGE` | `src/helpers/CommonCLI.cpp` r.737 |
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

## De 55 die nergens gelezen worden

Achttien procent van de MeshCore-macro's wordt gedefinieerd en nooit
getest. Ze vallen in drie groepen uiteen.

### Bordmarkeringen (42)

`EBYTE_EORA_S3`, `GENERIC_E22`, `HELTEC_HT_CT62`, `HELTEC_LORA_V2`,
`HELTEC_LORA_V4`, `HELTEC_MESH_POCKET`, `HELTEC_RC32`, `HELTEC_T1`,
`HELTEC_T114`, `HELTEC_TOWER_V2`, `HELTEC_V4_R8`, `HELTEC_WIRELESS_PAPER`,
`KEEPTEEN_LT1`, `LILYGO_T3S3`, `LILYGO_TETH_ELITE`, `LILYGO_TLORA`,
`LILYGO_T_ETH_ELITE_ESP32S3`, `MESHADVENTURER`, `MESHNOLOGY_W12`, `MESHTINY`,
`MESH_TRACKER_X1`, `NIBBLE_SCREEN_CONNECT`, `NIBBLE_ZERO_CONNECT`, `PROMICRO`,
`RAK_11310`, `RAK_3112`, `RAK_3401`, `RAK_3X72`, `SEEED_XIAO_S3`,
`STATION_G2`, `STATION_G3_ESP32`, `T1000_E`, `TBEAM_1W`, `THINKNODE_M2`,
`THINKNODE_M3`, `THINKNODE_M5`, `THINKNODE_M7`, `Vision_Master_E213`,
`Vision_Master_E290`, `WIO_TRACKER_L1`, `WIRELESS_PAPER`, `me25ls01`.

Elk variantbestand definieert zijn eigen naam als macro. Niets test erop,
omdat de variant al zijn eigen `-I`-pad meekrijgt en dus zijn eigen headers
ziet. Ze zijn documentatie in de vorm van een macro: je leest in de
`platformio.ini` welk bord het is, en de compiler doet er niets mee.

### Platformmarkering (1)

`ESP32_PLATFORM`. De andere drie platformmacro's — `NRF52_PLATFORM`,
`RP2040_PLATFORM`, `STM32_PLATFORM` — wórden gelezen; deze niet, omdat
ESP32-code de core-macro `ESP32` gebruikt die er toch al is. Zie
[Platformrealisatie](platform-realisation.md).

### Overig (12)

`DISABLE_DIAGNOSTIC_OUTPUT`, `DISPLAY_LINES`, `HAS_NEOPIXEL`, `HAS_TOUCH`,
`IO_EXPANDER_IRQ`, `LINE_LENGTH`, `NEOPIXEL_COUNT`, `NEOPIXEL_DATA`,
`NEOPIXEL_TYPE`, `PIN_RESET`, `UI_GPS_PAGE`,
`WITH_ESPNOW_BRIDGE_SECRET`.

Deze twaalf, waaronder `HAS_NEOPIXEL`, `NEOPIXEL_COUNT` en
`UI_GPS_PAGE`, wijzen naar functionaliteit die in deze commit niet bestaat. De
buildvlaggen zijn er, de code die erop reageert niet — of niet meer.

> [!NOTE]
> Tot en met `03b6ef4` telde deze lijst zeventien macro's, waaronder vijf die
> wél een lezer hebben. Die vijf staan nu in groep 2; zie de aantekening daar.
> `tools/config-flags.py --misfiled` laat zien welke het waren.

## Wat dit betekent

Een macro die nergens gelezen wordt is niet gevaarlijk, maar hij is wel
misleidend. Wie `HAS_TOUCH` in een `platformio.ini` ziet staan, mag aannemen
dat er iets met aanraakbediening gebeurt. Dat gebeurt niet.

Voor wie een bord toevoegt is dat praktisch van belang: de bordmarkering
kopiëren heeft geen effect, en `UI_GPS_PAGE` inschakelen levert geen
GPS-pagina op. Wat wél werkt, is te zien aan de 247 macro's die wel een lezer
hebben.

## Narekenen

```bash
python3 tools/config-flags.py /pad/naar/MeshCore
python3 tools/config-flags.py /pad/naar/MeshCore --owners
python3 tools/config-flags.py /pad/naar/MeshCore --consumption
python3 tools/config-flags.py /pad/naar/MeshCore --commented
python3 tools/config-flags.py /pad/naar/MeshCore --misfiled
```

`--owners` schrijft groep 2 en 3 als markdowntabel; `--consumption` geeft per
MeshCore-macro het eerste bestand en regelnummer waar hij voorkomt, met een
expliciete categorie *nergens gelezen*. `--commented` somt de macro's op die
alleen op uitgecommentarieerde regels staan, `--misfiled` de vijf die tot en
met v1.16.0 in de verkeerde groep stonden. Het script slaat regels achter een
`;` over, zodat uitgecommentarieerde macro's de configuratie-oppervlakte niet
opblazen.

## Bronnen

- [MeshCore `d929643` — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/d929643/platformio.ini)
- [MeshCore `d929643` — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/CommonCLI.cpp)
- [MeshCore `d929643` — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/examples/simple_repeater/MyMesh.cpp)
- [MeshCore `d929643` — `src/helpers/IdentityStore.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/IdentityStore.h)
