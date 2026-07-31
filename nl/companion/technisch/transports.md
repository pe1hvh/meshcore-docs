# De drie transporten

*BLE · USB · TCP · WACHTRIJEN · ÉÉN CLIENT · HERVERBINDEN*

Het companion-protocol loopt over drie verbindingen, en de firmware kent het
verschil niet: boven `BaseSerialInterface` bestaat alleen nog een frame.
Voor een client ligt dat anders. Dit hoofdstuk beschrijft wat elk transport
oplegt aan de kant die de app bouwt — niet hoe de bytes eruitzien, want dat
staat elders.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `examples/companion_radio/main.cpp`,
> `src/helpers/esp32/SerialBLEInterface.cpp`,
> `src/helpers/esp32/SerialBLEInterface.h`,
> `src/helpers/nrf52/SerialBLEInterface.h`,
> `src/helpers/esp32/SerialWifiInterface.cpp` en
> `src/helpers/ArduinoSerialInterface.cpp`.

![Boven een gedeelde interface leeft één frameformaat; daaronder drie
implementaties met elk eigen eisen aan de client](../../../images/nl/companion-transports-1.svg)

> [!NOTE]
> De bytelay-out van de frameheader, de vier ontvangsttoestanden en de
> BLE-stack met GATT en NUS staan niet hier maar in
> [USB-serieel](../../hardware/interfaces/usb-serial.md),
> [WiFi als companion-verbinding](../../hardware/interfaces/wifi.md) en
> [BLE Architectuur](../../hardware/interfaces/ble-architecture.md). Dit
> hoofdstuk gaat over de gevolgen daarvan voor een client.

## Eén verbindingstype per firmwarevariant

Welke van de drie erin zit, wordt gekozen tijdens het compileren en is geen
instelling. De
takken in `main.cpp` sluiten elkaar uit: met `WIFI_SSID` wordt het TCP, met
`BLE_PIN_CODE` wordt het BLE, en anders serieel. Een node die als
BLE-companion is geflasht heeft geen TCP-poort, en omgekeerd.

Voor een client betekent dat: het transport is een eigenschap van het
apparaat dat iemand in handen heeft, niet iets wat de app kan kiezen. Een
volwaardige client ondersteunt daarom alle drie. `meshcore_py` doet dat met
`ble_cx`, `serial_cx` en `tcp_cx` achter één gemeenschappelijke
protocolafspraak (*protocol interface*); zie
[Architectuur van een client](client-architecture.md).

## BLE: de node zendt met tussenpozen

De BLE-implementatie schrijft niet direct maar zet frames in een wachtrij en
haalt die met een vaste minimumtussentijd leeg:

`src/helpers/esp32/SerialBLEInterface.cpp` r.183-192

```cpp
#define  BLE_WRITE_MIN_INTERVAL   60

bool SerialBLEInterface::isWriteBusy() const {
  return millis() < _last_write + BLE_WRITE_MIN_INTERVAL;   // still too soon to start another write?
}

size_t SerialBLEInterface::checkRecvFrame(uint8_t dest[]) {
  if (send_queue_len > 0   // first, check send queue
    && millis() >= _last_write + BLE_WRITE_MIN_INTERVAL    // space the writes apart
  ) {
```

Tussen twee notificaties zit dus minstens zestig milliseconden. Hierdoor kan
de node theoretisch hooguit ongeveer zestien notificaties per seconde
versturen. Bij het ophalen van driehonderdvijftig contacten is dat merkbaar,
en het is de reden dat `CMD_GET_CONTACTS` een tijdstempel accepteert om
alleen wijzigingen op te halen.

De verzendwachtrij is klein en verschilt per platform:

| Platform | `FRAME_QUEUE_SIZE` | Bestand |
|---|---|---|
| ESP32, BLE | 4 | `src/helpers/esp32/SerialBLEInterface.h` r.26 |
| ESP32, WiFi | 4 | `src/helpers/esp32/SerialWifiInterface.h` r.27 |
| nRF52, BLE | 12 | `src/helpers/nrf52/SerialBLEInterface.h` r.24 |

Loopt die wachtrij vol, dan geeft `writeFrame()` nul terug en is het frame
weg — er komt geen foutmelding naar de app. Een client die veel commando's
snel achter elkaar verstuurt zonder op antwoord te wachten, kan daardoor
ongemerkt antwoorden missen. Wachten op het antwoord voordat het volgende
commando gaat, is dus geen beleefdheid maar een eis.

## TCP: één client tegelijk

De WiFi-implementatie accepteert een nieuwe verbinding door de bestaande weg
te gooien:

`src/helpers/esp32/SerialWifiInterface.cpp` r.57-68

```cpp
  auto newClient = server.available();
  if (newClient) {

    // disconnect existing client
    deviceConnected = false;
    client.stop();

    // switch active connection to new client
    client = newClient;

    // forget received frame header
    resetReceivedFrameHeader();
```

Twee apps op dezelfde node over TCP is dus geen gedeelde toegang: de nieuwe
verbinding verbreekt zonder protocolmelding de bestaande. De verdrongen
client merkt alleen dat zijn netwerkverbinding (*socket*) dicht is. Bij BLE
geldt hetzelfde langs een andere weg: één GATT-verbinding per radio, waarbij
GATT de laag in Bluetooth Low Energy is waarover deze frames lopen. Zie
[BLE Architectuur](../../hardware/interfaces/ble-architecture.md).

Dat is de technische onderbouwing van wat
[Verantwoordelijkheden](../logisch/responsibilities.md) al noemde: wie het
eerst synchroniseert, leegt de wachtrij, en de tweede app ziet die berichten
nooit.

## Serieel: de firmware detecteert geen verbroken kabel

De seriële implementatie kan niet weten of er iets aan de andere kant zit en
antwoordt daarom altijd bevestigend op `isConnected()`. Voor een client
betekent dat: er komt geen gebeurtenis wanneer de kabel eruit gaat. De
enige detectie die overblijft is een uitblijvend antwoord binnen een
tijdslimiet.

## Wat een client van elk transport moet aannemen

Bij serieel en TCP komt er een doorlopende reeks bytes binnen — een
bytestroom — zonder markering waar het ene frame ophoudt en het volgende
begint. De client bepaalt die grens zelf aan de hand van de header die
[USB-serieel](../../hardware/interfaces/usb-serial.md) beschrijft. Bij BLE
levert GATT elke notificatie als een afgerond blok af.

| | BLE | USB-serieel | TCP |
|---|---|---|---|
| Framegrens | door GATT gegeven | zelf uit de bytestroom halen | zelf uit de bytestroom halen |
| Verbinding valt weg | merkbaar | niet merkbaar | merkbaar |
| Meerdere clients | nee | nee | nee, de nieuwe verdringt |
| Tempo | ten minste 60 ms per frame | zo snel als de poort | zo snel als het netwerk |
| Herverbinden nodig | ja, regelmatig | zelden | bij netwerkwissel |

De onderste rij is de belangrijkste. Na elke herverbinding is
`app_target_ver` op de node weer nul en moet de opening opnieuw: eerst
`CMD_APP_START`, dan `CMD_DEVICE_QUERY`. Zie
[Het interactiemodel](../logisch/interaction-model.md).

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/main.cpp)
  — welke interface bij welke compilatieoptie hoort
- [`src/helpers/esp32/SerialBLEInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/esp32/SerialBLEInterface.cpp)
  — `BLE_WRITE_MIN_INTERVAL` en de verzendwachtrij
- [`src/helpers/esp32/SerialWifiInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/esp32/SerialWifiInterface.cpp)
  — het verdringen van een bestaande client
- [`src/helpers/ArduinoSerialInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ArduinoSerialInterface.cpp)
  — `isConnected()`, dat altijd bevestigend antwoordt

Verwante hoofdstukken:

- [USB-serieel](../../hardware/interfaces/usb-serial.md) — het frame byte
  voor byte
- [BLE Architectuur](../../hardware/interfaces/ble-architecture.md) — GATT,
  NUS en pairing
- [WiFi als companion-verbinding](../../hardware/interfaces/wifi.md) — de
  opzet van de TCP-variant
- [Het frame](frame-format.md) — wat er in de 176 bytes past
