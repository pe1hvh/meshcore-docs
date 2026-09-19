# WiFi als companion-verbinding

*ÉÉN TRANSPORT TEGELIJK · TCP 5000 · INLOGGEGEVENS IN DE BINARY · ALLEEN ESP32*

WiFi is in MeshCore geen netwerklaag maar één van de manieren waarop een
companion-app met een node praat. Het vervangt de BLE-verbinding of de
seriële kabel — niet als instelling maar als buildkeuze. Dit hoofdstuk
beschrijft hoe die keuze valt, wat er over TCP gaat, en waarom de
inloggegevens van je netwerk in de firmware terechtkomen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `examples/companion_radio/main.cpp`,
> `src/helpers/esp32/SerialWifiInterface.cpp`,
> `src/helpers/BaseSerialInterface.h` en de `WIFI_SSID`-vlaggen in
> `variants/`.

![Blokschema van de companionverbinding: één van drie transporten wordt
ingecompileerd — WiFi over TCP, BLE, of seriële poort — allemaal achter
dezelfde interface BaseSerialInterface](../../../images/nl/wifi-1.svg)

## Drie transporten, één wordt gecompileerd

De companionfirmware kiest het transport met preprocessordirectieven, niet
met een instelling:

`examples/companion_radio/main.cpp` r.37-54

```cpp
#ifdef ESP32
  #ifdef WIFI_SSID
    #include <helpers/esp32/SerialWifiInterface.h>
    SerialWifiInterface serial_interface;
    #ifndef TCP_PORT
      #define TCP_PORT 5000
    #endif
  #elif defined(BLE_PIN_CODE)
    #include <helpers/esp32/SerialBLEInterface.h>
    SerialBLEInterface serial_interface;
  #elif defined(SERIAL_RX)
    #include <helpers/ArduinoSerialInterface.h>
    ArduinoSerialInterface serial_interface;
    HardwareSerial companion_serial(1);
  #else
    #include <helpers/ArduinoSerialInterface.h>
    ArduinoSerialInterface serial_interface;
  #endif
```

Dit is de meest bepalende regel van de hele interfacessectie. Het is een
`#elif`-ketting: staat `WIFI_SSID` gedefinieerd, dan wordt WiFi
ingecompileerd en komen BLE en de seriële variant er niet meer in. Een node
kan dus niet tegelijk over BLE en over WiFi met een app praten, en je kunt er
niet tussen wisselen zonder opnieuw te flashen.

> [!NOTE]
> Dat verklaart waarom nodes met dezelfde chip zich verschillend gedragen:
> welk transport ze spreken is een eigenschap van de firmware die erop staat,
> niet van het bord. Welke borden welke aansluitmogelijkheden hebben staat in
> [Nodematrix](../../platform/node-matrix.md).

## Alleen op ESP32

De keten hierboven staat binnen `#ifdef ESP32`. Op RP2040 staat dezelfde
constructie in het bestand, maar volledig uitgecommentarieerd. Dat is terug
te zien in de variantbestanden:

| `WIFI_SSID` | Aantal |
|---|---|
| actief | 17 regels in 15 variantmappen |
| uitgecommentarieerd | 4 regels, alle vier RP2040 |

Geteld over `variants/*/platformio.ini`; regels die met `;` beginnen zijn
uitgecommentarieerd en tellen niet als buildvlag. Meer regels dan mappen,
omdat een variantbestand meerdere `[env:…]`-secties kan bevatten.

De vier uitgecommentarieerde regels staan in `rak11310`, `rpi_picow`,
`waveshare_rp2040_lora` en `xiao_rp2040`. Het is dus geen vergetelheid maar
werk dat klaarligt: de code bestaat, de vlaggen bestaan, maar de RP2040-tak
is niet in gebruik.

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
klasse, in `main.cpp`. Wat er over de verbinding gaat is hetzelfde als bij
BLE en bij serieel: frames van maximaal 176 bytes, achter dezelfde
interface.

`src/helpers/BaseSerialInterface.h` r.5

```cpp
#define MAX_FRAME_SIZE  176   // +4 for transport codes (region scoping)
```

Dat is de reden dat de drie transporten uitwisselbaar zijn: ze
implementeren alledrie `BaseSerialInterface` met `writeFrame()` en
`checkRecvFrame()`, en de rest van de firmware weet niet welk transport
eronder zit. Hoe die frames er byte voor byte uitzien staat in
[USB-serieel](usb-serial.md).

## De inloggegevens staan in de binary

`WIFI_SSID` en `WIFI_PWD` zijn buildvlaggen. Ze worden bij het compileren
in de code gesubstitueerd:

`examples/companion_radio/main.cpp` r.216-217

```cpp
  WiFi.begin(WIFI_SSID, WIFI_PWD);
  serial_interface.begin(TCP_PORT);
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

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/main.cpp)
  — de `#elif`-ketting die het transport kiest, en `WiFi.begin()`
- [`src/helpers/esp32/SerialWifiInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/esp32/SerialWifiInterface.cpp)
  — de TCP-server en de zendwachtrij
- [`src/helpers/BaseSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/BaseSerialInterface.h)
  — de gedeelde interface en `MAX_FRAME_SIZE`

Verwante hoofdstukken:

- [BLE Architectuur](ble-architecture.md) — het transport dat WiFi vervangt
- [USB-serieel](usb-serial.md) — hetzelfde frame over een kabel
- [Hardware van een node](../introduction.md) — waar dit onderdeel zit
- [Nodematrix](../../platform/node-matrix.md) — welk bord WiFi aan boord
  heeft
- [De vier platformfamilies](../../platform/platform-families.md) — welke
  families WiFi kennen
