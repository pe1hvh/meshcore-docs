# De transporten

*BLE · USB · TCP · ETHERNET · WACHTRIJEN · ÉÉN CLIENT · HERVERBINDEN*

Het companion-protocol loopt over vijf soorten verbinding, en de firmware
kent het verschil niet: boven `BaseSerialInterface` bestaat alleen nog een
frame.
Voor een client ligt dat anders. Dit hoofdstuk beschrijft wat elk transport
oplegt aan de kant die de app bouwt — niet hoe de bytes eruitzien, want dat
staat elders.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.17.1, commit `d929643`, 14 augustus 2026 — bestanden
> `examples/companion_radio/main.cpp`,
> `src/helpers/esp32/SerialBLEInterface.cpp`,
> `src/helpers/esp32/SerialBLEInterface.h`,
> `src/helpers/nrf52/SerialBLEInterface.h`,
> `src/helpers/esp32/SerialWifiInterface.cpp`,
> `src/helpers/MultiSerialInterface.h` en
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

## Meer dan één verbindingstype tegelijk

Tot en met v1.16.0 zat er precies één transport in een build en sloten de
takken in `main.cpp` elkaar uit. Sinds v1.17.1 is dat niet meer zo.
`MultiSerialInterface` is zelf een `BaseSerialInterface` die een reeks
andere interfaces onder zich houdt en ze alle tegelijk bedient; `main.cpp`
meldt ze één voor één aan en geeft de verzameling daarna als één interface
door aan de mesh:

`examples/companion_radio/main.cpp` r.188-191

```cpp
#if defined(BLE_PIN_CODE)
  bluetooth_interface.begin(BLE_NAME_PREFIX, the_mesh.getNodePrefs()->node_name, the_mesh.getBLEPin());
  interface_manager.addInterface(InterfaceType::Bluetooth, &bluetooth_interface);
#endif
```

De blokken erna zijn gelijkvormig en onafhankelijk: `WIFI_SSID` voegt WiFi
toe, `ENABLE_USB_INTERFACE` de USB-console, `ETHERNET_ENABLED` ethernet en
`SERIAL_RX` een tweede hardwarematige seriële poort. Het zijn geen
`else`-takken meer, dus een build kan er meerdere hebben. Welke transporten
erin zitten wordt nog steeds tijdens het compileren bepaald en is geen
instelling.

Vijf soorten dus. `InterfaceType` kent `Bluetooth`, `USB`, `WiFi`,
`Ethernet` en `HardwareSerial`
(`src/helpers/MultiSerialInterface.h` r.10-17).

> [!WARNING]
> **Vijf soorten, vier plekken.** `MAX_INTERFACES` staat standaard op vier,
> met als toelichting `ble, usb, wifi, ethernet`
> (`src/helpers/MultiSerialInterface.h` r.5-8). `addInterface()` zoekt de
> eerste vrije plek en geeft `false` terug als er geen is; in `main.cpp`
> wordt die uitkomst nergens gecontroleerd. Een build die alle vijf de
> `#define`s zet, verliest de laatste dus stilzwijgend. Onder de
> opgeleverde varianten komt die combinatie niet voor — de twee
> ethernettargets, `thinknode_m7` en `rak4631`, zetten geen `SERIAL_RX` —
> maar wie zelf een variant bouwt, loopt tegen een grens aan die geen
> foutmelding geeft.

Voor een client betekent dat: het transport is een eigenschap van het
apparaat dat iemand in handen heeft, niet iets wat de app kan kiezen — maar
een apparaat kan er nu meer dan één aanbieden. Een volwaardige client
ondersteunt daarom BLE, serieel en TCP. `meshcore_py` doet dat met
`ble_cx`, `serial_cx` en `tcp_cx` achter één gemeenschappelijke
protocolafspraak (*protocol interface*); zie
[Architectuur van een client](client-architecture.md).

> [!NOTE]
> `isConnected()` op `MultiSerialInterface` geeft `true` zodra één van de
> onderliggende interfaces verbonden is, en `writeFrame()` schrijft naar
> alle verbonden interfaces. Twee clients die tegelijk op verschillende
> transporten aanhangen, zien daardoor elkaars antwoorden. Het protocol
> gaat nog steeds uit van één client tegelijk; zie *Wat een client van elk
> transport moet aannemen*.

## BLE: de node zendt met tussenpozen

De BLE-implementatie schrijft niet direct maar zet frames in een wachtrij en
haalt die met een vaste minimumtussentijd leeg:

`src/helpers/esp32/SerialBLEInterface.cpp` r.189-198

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
[Verantwoordelijkheden](../logical/responsibilities.md) al noemde: wie het
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
[Het interactiemodel](../logical/interaction-model.md).

## Bronnen

Firmware, commit `d929643` (v1.17.1, 14 augustus 2026):

- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/companion_radio/main.cpp)
  — welke interface bij welke compilatieoptie hoort
- [`src/helpers/esp32/SerialBLEInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/esp32/SerialBLEInterface.cpp)
  — `BLE_WRITE_MIN_INTERVAL` en de verzendwachtrij
- [`src/helpers/esp32/SerialWifiInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/esp32/SerialWifiInterface.cpp)
  — het verdringen van een bestaande client
- [`src/helpers/ArduinoSerialInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/ArduinoSerialInterface.cpp)
  — `isConnected()`, dat altijd bevestigend antwoordt
- [`src/helpers/MultiSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/MultiSerialInterface.h)
  — `InterfaceType`, `MAX_INTERFACES` en `addInterface()`

Verwante hoofdstukken:

- [USB-serieel](../../hardware/interfaces/usb-serial.md) — het frame byte
  voor byte
- [BLE Architectuur](../../hardware/interfaces/ble-architecture.md) — GATT,
  NUS en pairing
- [WiFi als companion-verbinding](../../hardware/interfaces/wifi.md) — de
  opzet van de TCP-variant
- [Het frame](frame-format.md) — wat er in de 176 bytes past
