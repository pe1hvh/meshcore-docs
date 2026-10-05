# USB-serieel

*FRAMEFORMAAT · `>` EN `<` · 16-BITS LENGTE · 176 BYTES · TWEE RICHTINGEN*

De seriële verbinding is het transport zonder radio, zonder pincode en
zonder netwerk: een kabel naar een computer. Het is ook het transport
waarvan het formaat het duidelijkst te lezen is. WiFi en Ethernet zetten
dezelfde header voor elk frame, BLE niet. Dit hoofdstuk beschrijft het frame
byte voor byte, de toestandsmachine die het uit de bytestroom haalt, en hoe
een commando heen gaat en een antwoord terugkomt.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.17.1, commit `d929643`, 14 augustus 2026 — bestanden
> `src/helpers/BaseSerialInterface.h`, `src/helpers/MultiSerialInterface.h`,
> `src/helpers/ArduinoSerialInterface.cpp`,
> `src/helpers/ArduinoSerialInterface.h`,
> `src/helpers/esp32/SerialWifiInterface.cpp`,
> `src/helpers/ethernet/SerialEthernetInterface.cpp`,
> `src/helpers/TxtDataHelpers.h`, `examples/companion_radio/main.cpp`,
> `examples/companion_radio/MyMesh.cpp`, `examples/simple_repeater/main.cpp`
> en `examples/simple_repeater/MyMesh.cpp`. Het bytevoorbeeld is te
> reproduceren met
> [`tools/usb-serial-example.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/usb-serial-example.py).

![Frameopbouw van de seriële verbinding: startbyte, lengte in twee bytes
laagste eerst, gevolgd door de payload, met de vier toestanden van de
ontvangende toestandsmachine](../../../images/nl/usb-serial-1.svg)

## Eén interface, vijf transporten

Alles wat een companion-app met een node uitwisselt loopt door
`BaseSerialInterface`. Die schrijft zeven functies voor. Een achtste,
`loop()`, is in v1.17.1 toegevoegd en heeft een lege standaardinvulling, zodat
een implementatie hem niet hoeft te overschrijven:

`src/helpers/BaseSerialInterface.h` r.12-21

```cpp
  virtual void enable() = 0;
  virtual void disable() = 0;
  virtual bool isEnabled() const = 0;

  virtual bool isConnected() const = 0;
  virtual void loop() {};

  virtual bool isWriteBusy() const = 0;
  virtual size_t writeFrame(const uint8_t src[], size_t len) = 0;
  virtual size_t checkRecvFrame(uint8_t dest[]) = 0;
```

Drie functies zetten de interface aan en uit, `isConnected()` meldt of er een
tegenpartij is, en drie regelen het verkeer van frames.

Vijf klassen vullen de interface in voor een transport. Welke er in de
firmware zitten, bepalen de buildvlaggen in
`examples/companion_radio/main.cpp`:

| Klasse | Transport | Buildvlag | Gedeclareerd in |
|---|---|---|---|
| `ArduinoSerialInterface` | USB, of een seriële poort op twee pinnen | `ENABLE_USB_INTERFACE`, `SERIAL_RX` | `src/helpers/ArduinoSerialInterface.h` r.6 |
| `SerialBLEInterface` | BLE op ESP32 | `BLE_PIN_CODE` | `src/helpers/esp32/SerialBLEInterface.h` r.11 |
| `SerialBLEInterface` | BLE op nRF52 | `BLE_PIN_CODE` | `src/helpers/nrf52/SerialBLEInterface.h` r.10 |
| `SerialWifiInterface` | WiFi, alleen ESP32 | `WIFI_SSID` | `src/helpers/esp32/SerialWifiInterface.h` r.6 |
| `SerialEthernetInterface` | Ethernet | `ETHERNET_ENABLED` | `src/helpers/ethernet/SerialEthernetInterface.h` r.10 |

`SerialBLEInterface` bestaat twee keer onder dezelfde naam; het platform
bepaalt welke wordt meegecompileerd. `SerialEthernetInterface` laat het lezen
en schrijven van losse bytes open, en `CH390EthernetInterface` of
`RAK13800EthernetInterface` vult dat in.

De framegrootte is voor alle transporten gelijk:

`src/helpers/BaseSerialInterface.h` r.5

```cpp
#define MAX_FRAME_SIZE  176   // +4 for transport codes (region scoping)
```

176 bytes.

### Alles loopt via MultiSerialInterface

Een zesde klasse, `MultiSerialInterface`, implementeert dezelfde interface
maar is zelf geen transport. De companionfirmware maakt er één van, onder de
naam `interface_manager`, en meldt daar elk transport bij aan waarvan de
buildvlag gezet is. Voor USB:

`examples/companion_radio/main.cpp` r.213-217

```cpp
// add usb interface
#if defined(ENABLE_USB_INTERFACE)
  usb_serial_interface.begin(Serial);
  interface_manager.addInterface(InterfaceType::USB, &usb_serial_interface);
#endif
```

Daaruit volgen vier dingen:

- **USB is een keuze bij het bouwen.** Zonder `ENABLE_USB_INTERFACE` praat een
  companion niet via de kabel met een app. In v1.16.0 was de seriële poort
  nog wat overbleef als geen ander transport gekozen was; in v1.17.1 zet een
  variant de vlag in een eigen buildtarget, zoals
  `Heltec_WSL3_companion_radio_usb` in `variants/heltec_v3/platformio.ini`.
- **Meerdere transporten tegelijk.** Elke vlag heeft zijn eigen `#if`. Een
  build met `BLE_PIN_CODE` en `ENABLE_USB_INTERFACE` bedient een app over BLE
  en een app aan de kabel naast elkaar.
- **Hooguit vier.** `MAX_INTERFACES` is 4
  (`src/helpers/MultiSerialInterface.h` r.5-8), terwijl `main.cpp` vijf
  soorten kan aanmelden. Zet een build alle vijf de vlaggen, dan vindt de
  laatste `addInterface()` geen vrije plaats en geeft `false` terug.
  `main.cpp` controleert die returnwaarde niet.
- **Een antwoord gaat naar alle transporten.** `writeFrame()` schrijft naar
  elke ingeschakelde interface; zie het fragment hieronder.

`src/helpers/MultiSerialInterface.h` r.166-174

```cpp
    // write frame to all enabled interfaces
    bool allSuccessful = true;
    for(auto iface : _interfaces){
      if(iface.instance && iface.instance->isEnabled()){
        if(iface.instance->writeFrame(src, len) != len){
          allSuccessful = false;
        }
      }
    }
```

De andere kant op neemt `checkRecvFrame()` het eerste frame dat bij één van
de interfaces klaarstaat (r.180-198). Een app aan de kabel krijgt dus ook de
antwoorden op commando's die een andere app over BLE stuurde.

## Het frame dat de node verstuurt

Drie bytes header, dan de payload:

`src/helpers/ArduinoSerialInterface.cpp` r.24-37

```cpp
size_t ArduinoSerialInterface::writeFrame(const uint8_t src[], size_t len) {
  if (len > MAX_FRAME_SIZE) {
    // frame is too big!
    return 0;
  }

  uint8_t hdr[3];
  hdr[0] = '>';
  hdr[1] = (len & 0xFF);  // LSB
  hdr[2] = (len >> 8);    // MSB

  _serial->write(hdr, 3);
  return _serial->write(src, len);
}
```

| Byte | Waarde | Betekenis |
|---|---|---|
| 0 | `>` (`0x3E`) | node → computer |
| 1 | lengte laag | LSB eerst |
| 2 | lengte hoog | MSB |
| 3… | payload | maximaal 176 bytes |

De richting zit in de startbyte. De node zendt met `>` en luistert naar `<`:
een frame dat de andere kant op gaat begint dus met een ander teken. Dat is
geen versleuteling maar het maakt het onmogelijk om per ongeluk je eigen
uitvoer als invoer te lezen.

Een frame groter dan 176 bytes wordt niet afgekapt maar helemaal niet
verstuurd — `writeFrame()` geeft dan nul terug.

WiFi en Ethernet zetten dezelfde drie bytes voor elk frame
(`src/helpers/esp32/SerialWifiInterface.cpp` r.91-94,
`src/helpers/ethernet/SerialEthernetInterface.cpp` r.66-69), Ethernet
alleen als `ETHERNET_RAW_LINE` niet gezet is. BLE zet geen header voor het
frame.

## De toestandsmachine aan de ontvangkant

Bytes komen los binnen, dus de ontvanger is een toestandsmachine met vier
toestanden:

```text
  IDLE        ── ziet '<' ──▶  HDR_FOUND
  HDR_FOUND   ── lengte LSB ─▶ LEN1_FOUND
  LEN1_FOUND  ── lengte MSB ─▶ LEN2_FOUND   (of terug naar IDLE bij lengte 0)
  LEN2_FOUND  ── payload ────▶ frame af, terug naar IDLE
```

Twee details zijn de moeite waard:

`src/helpers/ArduinoSerialInterface.cpp` r.59-69

```cpp
      default:
        if (rx_len < MAX_FRAME_SIZE) {
          rx_buf[rx_len] = (uint8_t)c;   // rest of frame will be discarded if > MAX
        }
        rx_len++;
        if (rx_len >= _frame_len) {  // received a complete frame?
          if (_frame_len > MAX_FRAME_SIZE) _frame_len = MAX_FRAME_SIZE;    // truncate
          memcpy(dest, rx_buf, _frame_len);
          _state = RECV_STATE_IDLE;  // reset state, for next frame
          return _frame_len;
        }
```

Een te lang frame wordt wél volledig ingelezen maar slechts tot 176 bytes
bewaard; de rest verdwijnt. De teller loopt door, zodat de toestandsmachine
weer op het juiste punt in de stroom staat als het frame afgelopen is. En
een aangekondigde lengte van nul brengt de machine meteen terug naar
`IDLE` — een leeg frame bestaat niet.

## Er is geen verbindingsdetectie

`src/helpers/ArduinoSerialInterface.cpp` r.16-18

```cpp
bool ArduinoSerialInterface::isConnected() const { 
  return true;   // no way of knowing, so assume yes
}
```

Een seriële poort heeft geen begrip van verbinding. De firmware zegt daarom
altijd ja. Bij BLE en WiFi is dat anders: daar is er een tegenpartij die
verbindt en wegvalt, en daar houdt de interface dat wél bij. Zie
[BLE Architectuur](ble-architecture.md).

Sinds v1.17.1 vraagt de companionfirmware het niet aan het transport zelf
maar aan `MultiSerialInterface`, en die meldt een verbinding zodra één van
zijn interfaces dat doet:

`src/helpers/MultiSerialInterface.h` r.117-128

```cpp
  bool isConnected() const override {
    // not connected when disabled
    if(!_enabled){
      return false;
    }
    
    // check if any interface is connected
    for(auto iface : _interfaces){
      if(iface.instance && iface.instance->isConnected()) {
        return true;
      }
    }
```

Met USB in de build is het antwoord dus altijd ja, ook als alleen een app
over BLE verbonden is of helemaal geen app. Dat heeft een zichtbaar gevolg.
Bij een binnengekomen bericht roept de firmware de melding alleen aan als er
geen app verbonden is:

`examples/companion_radio/MyMesh.cpp` r.470-474

```cpp
  if (should_display && _ui) {
    _ui->newMsg(path_len, from.name, text, offline_queue_len);
    if (!_serial->isConnected()) {
      _ui->notify(UIEventType::contactMessage);
    }
```

Op een node met scherm en USB in de build verschijnt het bericht wel op het
scherm (`newMsg()`), maar de melding (`notify()`) komt nooit.

## Verkeer in twee richtingen

Over de kabel gaat verkeer beide kanten op. De app stuurt frames die met `<`
beginnen, de node antwoordt met `>`. De eerste byte van de payload is de
opcode; hoe commando's, antwoorden en pushcodes zich tot elkaar verhouden
staat in [Het interactiemodel](../../companion/logical/interaction-model.md).
Hieronder drie gevallen: een schrijfopdracht die de node zelf afhandelt, een
CLI-commando dat de node doorstuurt naar een repeater, en een repeater die
zelf aan de kabel hangt.

![Verloop van de frames tussen drie deelnemers, app, companion-node en
repeater, van boven naar beneden in de tijd. Deel
A: de app stuurt CMD_SET_ADVERT_NAME met de naam PE1HVH, de node voert
savePrefs() uit en antwoordt met RESP_CODE_OK. Deel B: de app stuurt
CMD_SEND_TXT_MSG met txt_type 1 en de tekst ver, de node antwoordt met
RESP_CODE_SENT en stuurt een TXT_MSG via LoRa naar de repeater; die
controleert isAdmin() en voert handleCommand() uit, en stuurt het antwoord
als TXT_TYPE_CLI_DATA terug; de node zet het in de offline queue, stuurt
PUSH_CODE_MSG_WAITING, de app haalt het op met CMD_SYNC_NEXT_MESSAGE en
krijgt RESP_CODE_CONTACT_MSG_RECV_V3, en vraagt opnieuw tot
RESP_CODE_NO_MORE_MESSAGES](../../../images/nl/usb-serial-2.svg)

### Een schrijfopdracht

Stap 1 tot 3: de app zet de nodenaam op `PE1HVH`. Dat zijn twee frames:

| Richting | Bytes | Betekenis |
|---|---|---|
| app → node | `3C 07 00 08 50 45 31 48 56 48` | `<`, lengte 7, `CMD_SET_ADVERT_NAME` (8), `PE1HVH` |
| node → app | `3E 01 00 00` | `>`, lengte 1, `RESP_CODE_OK` (0) |

Het lengteveld telt alleen de payload: de opcode plus zes tekens. De node
handelt het commando in één doorgang af:

`examples/companion_radio/MyMesh.cpp` r.1212-1218

```cpp
  } else if (cmd_frame[0] == CMD_SET_ADVERT_NAME && len >= 2) {
    int nlen = len - 1;
    if (nlen > sizeof(_prefs.node_name) - 1) nlen = sizeof(_prefs.node_name) - 1; // max len
    memcpy(_prefs.node_name, &cmd_frame[1], nlen);
    _prefs.node_name[nlen] = 0; // null terminator
    savePrefs();
    writeOKFrame();
```

Een te lange naam wordt afgekapt, `savePrefs()` schrijft hem weg, en pas
daarna volgt het OK. Er komt geen push achteraan en er gaat niets de lucht
in.

### Een CLI-commando op afstand

Stap 4 tot 15. Het CLI-scherm in een app bedient een repeater of room server
op afstand; de companion zelf heeft alleen de console uit
[Companion: CLI Rescue](../../cli/companion-rescue.md). De app moet bij de
repeater eerst als admin ingelogd zijn, want de repeater voert een commando
alleen uit voor een client met adminrechten
(`examples/simple_repeater/MyMesh.cpp` r.702). Zie [ACL](../../cli/acl.md).

Het commando gaat als tekstbericht met een eigen type:

`src/helpers/TxtDataHelpers.h` r.6-8

```cpp
#define TXT_TYPE_PLAIN          0      // a plain text message
#define TXT_TYPE_CLI_DATA       1      // a CLI command
#define TXT_TYPE_SIGNED_PLAIN   2      // plain text, signed by sender
```

De node herkent dat type in `CMD_SEND_TXT_MSG` en kiest een andere
verzendfunctie dan voor een gewoon bericht:

`examples/companion_radio/MyMesh.cpp` r.1102-1105

```cpp
      if (txt_type == TXT_TYPE_CLI_DATA) {
        msg_timestamp = getRTCClock()->getCurrentTimeUnique(); // Use node's RTC instead of app timestamp to avoid tripping replay protection
        result = sendCommandData(*recipient, msg_timestamp, attempt, text, est_timeout);
        expected_ack = 0; // no Ack expected
```

Twee dingen verschillen van een schrijfopdracht:

- **Het eerste antwoord is geen uitvoering.** `RESP_CODE_SENT` in stap 5
  betekent dat het pakket klaarstaat om te verzenden. Er wordt geen ACK
  verwacht, dus de app hoort daarna niets meer tot het antwoord van de
  repeater binnen is.
- **Het antwoord komt terug als bericht.** De repeater voert het commando uit
  met `handleCommand()` (`examples/simple_repeater/MyMesh.cpp` r.739) en
  stuurt de tekst terug met type `TXT_TYPE_CLI_DATA` (r.749), na een
  wachttijd van `CLI_REPLY_DELAY_MILLIS`, 600 ms (r.59). Levert het commando
  geen tekst op, of herhaalt de app een commando met dezelfde tijdstempel,
  dan stuurt de repeater niets terug (r.736-742).

De companion zet het antwoord in de offline queue en tikt de app aan, stap 9
en 10:

`examples/companion_radio/MyMesh.cpp` r.459-465

```cpp
  addToOfflineQueue(out_frame, i);

  if (_serial->isConnected()) {
    uint8_t frame[1];
    frame[0] = PUSH_CODE_MSG_WAITING; // send push 'tickle'
    _serial->writeFrame(frame, 1);
  }
```

De app haalt het op met `CMD_SYNC_NEXT_MESSAGE` en herhaalt dat tot de queue
leeg is, stap 11 tot 15:

`examples/companion_radio/MyMesh.cpp` r.1368-1378

```cpp
  } else if (cmd_frame[0] == CMD_SYNC_NEXT_MESSAGE) {
    int out_len;
    if ((out_len = getFromOfflineQueue(out_frame)) > 0) {
      _serial->writeFrame(out_frame, out_len);
#ifdef DISPLAY_CLASS
      if (_ui) _ui->msgRead(offline_queue_len);
#endif
    } else {
      out_frame[0] = RESP_CODE_NO_MORE_MESSAGES;
      _serial->writeFrame(out_frame, 1);
    }
```

Het antwoord in stap 12 is een `RESP_CODE_CONTACT_MSG_RECV_V3` met
`txt_type` 1. Aan dat type kan de app zien dat de tekst in het CLI-scherm
hoort en niet bij de berichten.

### Een repeater direct aan USB

![Verloop tussen twee deelnemers, terminal en repeater: de terminal
stuurt de tekens v, e, r en een CR zonder startbyte of lengte, de repeater
stuurt elk teken terug, voert bij de CR handleCommand(0, command, reply) uit
en stuurt twee spaties, een pijl en het antwoord terug, alleen als dat
antwoord niet leeg is](../../../images/nl/usb-serial-3.svg)

Op een repeater is de kabel geen companion-verbinding. De repeater-firmware
gebruikt geen `ArduinoSerialInterface` en er gaan geen frames over de kabel:
de CLI leest gewone tekst. Elk teken komt meteen terug, en bij een CR voert
de firmware het commando uit:

`examples/simple_repeater/main.cpp` r.141-155

```cpp
  if (len > 0 && command[len - 1] == '\r') {  // received complete line
    Serial.print('\n');
    command[len - 1] = 0;  // replace newline with C string null terminator
    char reply[160];
    reply[0] = 0;
#ifdef ETHERNET_ENABLED
    if (!ethernet_handle_command(command, reply)) {
      the_mesh.handleCommand(0, command, reply);
    }
#else
    the_mesh.handleCommand(0, command, reply);  // NOTE: there is no sender_timestamp via serial!
#endif
    if (reply[0]) {
      Serial.print("  -> "); Serial.println(reply);
    }
```

De commando's zijn dezelfde als op afstand: in beide gevallen loopt de
afhandeling via `handleCommand()`. Het verschil zit in de verpakking. Op
afstand is het een versleuteld tekstbericht via LoRa met een tijdstempel,
hier een regel tekst zonder tijdstempel, vandaar de `0` als eerste argument.
De commando's zelf staan in de [CLI-referentie](../../cli/introduction.md).

## Bronnen

Firmware, commit `d929643` (v1.17.1, 14 augustus 2026):

- [`src/helpers/BaseSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/BaseSerialInterface.h)
  — de gedeelde interface en `MAX_FRAME_SIZE`
- [`src/helpers/MultiSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/MultiSerialInterface.h)
  — `MAX_INTERFACES`, verzenden naar alle transporten, `isConnected()`
- [`src/helpers/ArduinoSerialInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/ArduinoSerialInterface.cpp)
  — `writeFrame()`, `checkRecvFrame()` en de vier toestanden
- [`src/helpers/esp32/SerialWifiInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/esp32/SerialWifiInterface.cpp)
  en [`src/helpers/ethernet/SerialEthernetInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/ethernet/SerialEthernetInterface.cpp)
  — dezelfde header over TCP
- [`src/helpers/TxtDataHelpers.h`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/TxtDataHelpers.h)
  — `TXT_TYPE_CLI_DATA`
- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/companion_radio/main.cpp)
  — de buildvlaggen per transport en `interface_manager`
- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/companion_radio/MyMesh.cpp)
  — `CMD_SET_ADVERT_NAME`, `CMD_SEND_TXT_MSG`, `queueMessage()`,
  `CMD_SYNC_NEXT_MESSAGE`
- [`examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/simple_repeater/MyMesh.cpp)
  — een CLI-commando op afstand uitvoeren en beantwoorden
- [`examples/simple_repeater/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/simple_repeater/main.cpp)
  — de CLI in gewone tekst op de seriële poort

Script: [`tools/usb-serial-example.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/usb-serial-example.py)
— het bytevoorbeeld van de schrijfopdracht.

Verwante hoofdstukken:

- [Het interactiemodel](../../companion/logical/interaction-model.md) —
  vraag, antwoord en push
- [Het frame](../../companion/technical/frame-format.md) — opcode en payload
  binnen het frame
- [WiFi als companion-verbinding](wifi.md) — hetzelfde frame over TCP
- [BLE Architectuur](ble-architecture.md) — hetzelfde frame over BLE
- [CLI-referentie](../../cli/introduction.md) — de commando's
- [Companion: CLI Rescue](../../cli/companion-rescue.md) — de console van
  de companion zelf
- [Hardware van een node](../introduction.md) — waar dit onderdeel zit
