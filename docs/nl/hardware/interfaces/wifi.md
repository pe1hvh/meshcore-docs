# WiFi als companion-verbinding

*NAAST ANDERE TRANSPORTEN · TCP 5000 · INLOGGEGEVENS IN DE BINARY · ALLEEN ESP32*

WiFi is in MeshCore geen netwerklaag maar één van de manieren waarop een
companion-app met een node praat. Sinds v1.17.1 komt het niet meer in de
plaats van de BLE-verbinding of de seriële kabel, maar ernaast: welke
transporten erin zitten is een buildkeuze, en een build kan er meerdere
bevatten. Dit hoofdstuk beschrijft hoe die keuze valt, wat er over TCP gaat,
en waarom de inloggegevens van je netwerk in de firmware terechtkomen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.17.1, commit `d929643`, 14 augustus 2026 — bestanden
> `examples/companion_radio/main.cpp`,
> `src/helpers/esp32/SerialWifiInterface.cpp`,
> `src/helpers/BaseSerialInterface.h`, `src/helpers/MultiSerialInterface.h`
> en de `WIFI_SSID`-vlaggen in `variants/`. De tellingen zijn te reproduceren
> met
> [`tools/hardware-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/hardware-overview.py)
> met `--pin d929643`.

![Blokschema van de companionverbinding: MultiSerialInterface bovenaan, met
daaronder vijf transporten die elk door een eigen buildvlag worden
toegevoegd — WiFi over TCP, BLE, USB, een seriële poort op pinnen en
Ethernet; de WiFi-rij is gemarkeerd](../../../images/nl/wifi-1.svg)

## Elke vlag voegt een transport toe

De companionfirmware kiest de transporten met preprocessordirectieven, niet
met een instelling. Voor WiFi:

`examples/companion_radio/main.cpp` r.34-46

```cpp
// include wifi interface
#ifdef WIFI_SSID
  #ifndef TCP_PORT
    #define TCP_PORT 5000
  #endif
  #ifdef ESP32
    // include esp32 wifi interface
    #include <helpers/esp32/SerialWifiInterface.h>
    SerialWifiInterface wifi_interface;
  #else
    #error "SerialWifiInterface is not defined for this platform"
  #endif
#endif
```

In v1.16.0 stond hier een `#elif`-ketting: was `WIFI_SSID` gedefinieerd, dan
kwamen BLE en de seriële variant er niet meer in. In v1.17.1 heeft elk
transport zijn eigen `#if`. Bij het opstarten meldt de firmware WiFi aan bij
`interface_manager`, een `MultiSerialInterface`:

`examples/companion_radio/main.cpp` r.208-210

```cpp
  WiFi.begin(WIFI_SSID, WIFI_PWD);
  wifi_interface.begin(TCP_PORT);
  interface_manager.addInterface(InterfaceType::WiFi, &wifi_interface);
```

Een node kan dus tegelijk over BLE en over WiFi met een app praten, als de
build beide vlaggen zet. Wisselen zonder opnieuw te flashen kan nog steeds
niet: wat er niet in gecompileerd is, is er niet. Hoe `MultiSerialInterface`
de transporten samen bedient, en welke grens er aan het aantal zit, staat in
[USB-serieel](usb-serial.md).

> [!NOTE]
> Dat verklaart waarom nodes met dezelfde chip zich verschillend gedragen:
> welk transport ze spreken is een eigenschap van de firmware die erop staat,
> niet van het bord. Welke borden welke aansluitmogelijkheden hebben staat in
> [Nodematrix](../../platform/node-matrix.md).

## Alleen op ESP32

Op een ander platform stopt een build met `WIFI_SSID` met een foutmelding
(`examples/companion_radio/main.cpp` r.43-45). Dat is terug te zien in de
variantbestanden:

| `WIFI_SSID` | Aantal |
|---|---|
| actief | 25 regels in 21 variantmappen |
| uitgecommentarieerd | 4 regels, alle vier RP2040 |

Geteld over `variants/*/platformio.ini`; regels die met `;` beginnen zijn
uitgecommentarieerd en tellen niet als buildvlag. Meer regels dan mappen,
omdat een variantbestand meerdere `[env:…]`-secties kan bevatten.

De vier uitgecommentarieerde regels staan in `rak11310`, `rpi_picow`,
`waveshare_rp2040_lora` en `xiao_rp2040`. In v1.16.0 stond in `main.cpp` nog
een uitgecommentarieerde RP2040-tak die naar een `SerialWifiInterface` voor
RP2040 verwees. Die tak is in v1.17.1 verdwenen, en zo'n klasse bestaat in de
firmware niet. Wie een van de vier regels aanzet, krijgt de foutmelding.

## Wat er over de verbinding gaat

`SerialWifiInterface` opent een TCP-server. De poort is `TCP_PORT`, en als de
variant die niet zet is het 5000.

`src/helpers/esp32/SerialWifiInterface.cpp` r.4-7

```cpp
void SerialWifiInterface::begin(int port) {
  // wifi setup is handled outside of this class, only starts the server
  server.begin(port);
}
```

De klasse doet zelf niets aan het netwerk — verbinden gebeurt buiten de
klasse, in `main.cpp`. Daar staat sinds v1.17.1 ook dat de node niet gaat
slapen zolang WiFi actief is (r.195), en dat hij na een verbroken verbinding
elke tien seconden opnieuw verbindt (r.198-206 en r.265-273). Wat er over de
verbinding gaat is hetzelfde als bij BLE en bij serieel: frames van maximaal
176 bytes, achter dezelfde interface.

`src/helpers/BaseSerialInterface.h` r.5

```cpp
#define MAX_FRAME_SIZE  176   // +4 for transport codes (region scoping)
```

Elk frame krijgt over TCP dezelfde header als over de kabel, `>` of `<` en
twee lengtebytes (`src/helpers/esp32/SerialWifiInterface.cpp` r.91-94); een
frame dat niet met `<` begint slaat de node over (r.143-144). Alle
transporten implementeren `BaseSerialInterface` met `writeFrame()` en
`checkRecvFrame()`, en de rest van de firmware ziet alleen
`MultiSerialInterface`, niet welk transport eronder zit. Hoe die frames er
byte voor byte uitzien staat in [USB-serieel](usb-serial.md).

## De inloggegevens staan in de binary

`WIFI_SSID` en `WIFI_PWD` zijn buildvlaggen. Ze worden bij het compileren
in de code gesubstitueerd:

`examples/companion_radio/main.cpp` r.208-209

```cpp
  WiFi.begin(WIFI_SSID, WIFI_PWD);
  wifi_interface.begin(TCP_PORT);
```

> [!WARNING]
> De naam en het wachtwoord van je WiFi-netwerk komen als leesbare tekst in
> het firmwarebestand terecht. Wie de binary heeft — of de node uitleest —
> heeft je netwerkwachtwoord. Deel geen zelfgebouwde WiFi-firmware en zet
> een node met WiFi-firmware niet op een netwerk dat je niet kwijt wilt.
> Voor een gastnetwerk of een apart VLAN is dit precies de situatie waar
> die voor bedoeld zijn.

Dit is een andere afweging dan bij BLE, waar een pincode in de firmware
staat maar geen netwerkgeheim. Zie [BLE Architectuur](ble-architecture.md).

## Bronnen

Firmware, commit `d929643` (v1.17.1, 14 augustus 2026):

- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/companion_radio/main.cpp)
  — de `#if` per transport, het aanmelden bij `interface_manager`,
  `WiFi.begin()` en het opnieuw verbinden
- [`src/helpers/esp32/SerialWifiInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/esp32/SerialWifiInterface.cpp)
  — de TCP-server, de header en de zendwachtrij
- [`src/helpers/BaseSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/BaseSerialInterface.h)
  — de gedeelde interface en `MAX_FRAME_SIZE`
- [`src/helpers/MultiSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/MultiSerialInterface.h)
  — de klasse die alle transporten samen bedient

Verwante hoofdstukken:

- [BLE Architectuur](ble-architecture.md) — het transport dat sinds v1.17.1
  naast WiFi in één build kan zitten
- [USB-serieel](usb-serial.md) — hetzelfde frame over een kabel, en
  `MultiSerialInterface`
- [Hardware van een node](../introduction.md) — waar dit onderdeel zit
- [Nodematrix](../../platform/node-matrix.md) — welk bord WiFi aan boord
  heeft
- [De vier platformfamilies](../../platform/platform-families.md) — welke
  families WiFi kennen
