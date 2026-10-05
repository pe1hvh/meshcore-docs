# USB Serial

*FRAME FORMAT · `>` AND `<` · 16-BIT LENGTH · 176 BYTES · TWO DIRECTIONS*

The serial link is the transport without a radio, without a PIN code and
without a network: a cable to a computer. It is also the transport whose
format is easiest to read. WiFi and Ethernet put the same header in front of
every frame, BLE does not. This chapter describes the frame byte by byte, the
state machine that pulls it out of the byte stream, and how a command goes
out and a reply comes back.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.17.1, commit `d929643`, 14 August 2026 — files
> `src/helpers/BaseSerialInterface.h`, `src/helpers/MultiSerialInterface.h`,
> `src/helpers/ArduinoSerialInterface.cpp`,
> `src/helpers/ArduinoSerialInterface.h`,
> `src/helpers/esp32/SerialWifiInterface.cpp`,
> `src/helpers/ethernet/SerialEthernetInterface.cpp`,
> `src/helpers/TxtDataHelpers.h`, `examples/companion_radio/main.cpp`,
> `examples/companion_radio/MyMesh.cpp`, `examples/simple_repeater/main.cpp`
> and `examples/simple_repeater/MyMesh.cpp`. The byte example can be
> reproduced with
> [`tools/usb-serial-example.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/usb-serial-example.py).

![Frame layout of the serial link: start byte, length in two bytes least
significant first, followed by the payload, with the four states of the
receiving state machine](../../../images/en/usb-serial-1.svg)

## One interface, five transports

Everything a companion app exchanges with a node passes through
`BaseSerialInterface`. It prescribes seven functions. An eighth, `loop()`,
was added in v1.17.1 and has an empty default body, so an implementation
does not have to override it:

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

Three functions switch the interface on and off, `isConnected()` reports
whether there is a counterpart, and three handle the frame traffic.

Five classes implement the interface for a transport. Which of them end up
in the firmware is decided by the build flags in
`examples/companion_radio/main.cpp`:

| Class | Transport | Build flag | Declared in |
|---|---|---|---|
| `ArduinoSerialInterface` | USB, or a serial port on two pins | `ENABLE_USB_INTERFACE`, `SERIAL_RX` | `src/helpers/ArduinoSerialInterface.h` r.6 |
| `SerialBLEInterface` | BLE on ESP32 | `BLE_PIN_CODE` | `src/helpers/esp32/SerialBLEInterface.h` r.11 |
| `SerialBLEInterface` | BLE on nRF52 | `BLE_PIN_CODE` | `src/helpers/nrf52/SerialBLEInterface.h` r.10 |
| `SerialWifiInterface` | WiFi, ESP32 only | `WIFI_SSID` | `src/helpers/esp32/SerialWifiInterface.h` r.6 |
| `SerialEthernetInterface` | Ethernet | `ETHERNET_ENABLED` | `src/helpers/ethernet/SerialEthernetInterface.h` r.10 |

`SerialBLEInterface` exists twice under the same name; the platform decides
which one is compiled in. `SerialEthernetInterface` leaves reading and
writing individual bytes open, and `CH390EthernetInterface` or
`RAK13800EthernetInterface` fills that in.

The frame size is the same for every transport:

`src/helpers/BaseSerialInterface.h` r.5

```cpp
#define MAX_FRAME_SIZE  176   // +4 for transport codes (region scoping)
```

176 bytes.

### Everything goes through MultiSerialInterface

A sixth class, `MultiSerialInterface`, implements the same interface but is
not a transport itself. The companion firmware creates one, named
`interface_manager`, and registers with it every transport whose build flag
is set. For USB:

`examples/companion_radio/main.cpp` r.213-217

```cpp
// add usb interface
#if defined(ENABLE_USB_INTERFACE)
  usb_serial_interface.begin(Serial);
  interface_manager.addInterface(InterfaceType::USB, &usb_serial_interface);
#endif
```

Four things follow from this:

- **USB is a build-time choice.** Without `ENABLE_USB_INTERFACE` a companion
  does not talk to an app over the cable. In v1.16.0 the serial port was
  what remained when no other transport was chosen; in v1.17.1 a variant
  sets the flag in a build target of its own, such as
  `Heltec_WSL3_companion_radio_usb` in `variants/heltec_v3/platformio.ini`.
- **Several transports at once.** Each flag has its own `#if`. A build with
  `BLE_PIN_CODE` and `ENABLE_USB_INTERFACE` serves an app over BLE and an app
  on the cable side by side.
- **Four at most.** `MAX_INTERFACES` is 4
  (`src/helpers/MultiSerialInterface.h` r.5-8), while `main.cpp` can
  register five kinds. If a build sets all five flags, the last
  `addInterface()` finds no empty slot and returns `false`. `main.cpp` does
  not check that return value.
- **A reply goes to every transport.** `writeFrame()` writes to every
  enabled interface; see the fragment below.

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

In the other direction `checkRecvFrame()` takes the first frame waiting on
any of the interfaces (r.180-198). An app on the cable therefore also
receives the replies to commands that another app sent over BLE.

## The frame the node sends

Three header bytes, then the payload:

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

| Byte | Value | Meaning |
|---|---|---|
| 0 | `>` (`0x3E`) | node → computer |
| 1 | length low | LSB first |
| 2 | length high | MSB |
| 3… | payload | at most 176 bytes |

Direction sits in the start byte. The node sends with `>` and listens for
`<`: a frame going the other way therefore starts with a different
character. That is not encryption, but it makes it impossible to
accidentally read your own output as input.

A frame larger than 176 bytes is not truncated but not sent at all —
`writeFrame()` then returns zero.

WiFi and Ethernet put the same three bytes in front of every frame
(`src/helpers/esp32/SerialWifiInterface.cpp` r.91-94,
`src/helpers/ethernet/SerialEthernetInterface.cpp` r.66-69), Ethernet only
when `ETHERNET_RAW_LINE` is not set. BLE puts no header in front of the
frame.

## The state machine on the receiving side

Bytes arrive one at a time, so the receiver is a state machine with four
states:

```text
  IDLE        ── sees '<' ───▶  HDR_FOUND
  HDR_FOUND   ── length LSB ─▶  LEN1_FOUND
  LEN1_FOUND  ── length MSB ─▶  LEN2_FOUND   (or back to IDLE on length 0)
  LEN2_FOUND  ── payload ────▶  frame done, back to IDLE
```

Two details are worth noting:

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

An overlong frame *is* read in full but only kept up to 176 bytes; the rest
disappears. The counter keeps running so the state machine is at the right
point in the stream once the frame ends. And an announced length of zero
sends the machine straight back to `IDLE` — an empty frame does not exist.

## There is no connection detection

`src/helpers/ArduinoSerialInterface.cpp` r.16-18

```cpp
bool ArduinoSerialInterface::isConnected() const { 
  return true;   // no way of knowing, so assume yes
}
```

A serial port has no concept of a connection. The firmware therefore always
says yes. With BLE and WiFi it is different: there is a counterpart that
connects and drops away, and there the interface does track it. See
[BLE Architecture](ble-architecture.md).

Since v1.17.1 the companion firmware does not ask the transport itself but
`MultiSerialInterface`, which reports a connection as soon as one of its
interfaces does:

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

With USB in the build the answer is therefore always yes, even when only an
app over BLE is connected, or no app at all. That has a visible
consequence. For an incoming message the firmware only calls the
notification when no app is connected:

`examples/companion_radio/MyMesh.cpp` r.470-474

```cpp
  if (should_display && _ui) {
    _ui->newMsg(path_len, from.name, text, offline_queue_len);
    if (!_serial->isConnected()) {
      _ui->notify(UIEventType::contactMessage);
    }
```

On a node with a display and USB in the build, the message does appear on
the display (`newMsg()`), but the notification (`notify()`) never comes.

## Traffic in two directions

Traffic over the cable goes both ways. The app sends frames starting with
`<`, the node replies with `>`. The first payload byte is the opcode; how
commands, replies and push codes relate to each other is in
[The interaction model](../../companion/logical/interaction-model.md). Below
are three cases: a write command the node handles itself, a CLI command the
node forwards to a repeater, and a repeater that is itself on the cable.

![Sequence diagram with three participants, app, companion node and
repeater. Part A: the app sends CMD_SET_ADVERT_NAME with the name PE1HVH,
the node runs savePrefs() and replies with RESP_CODE_OK. Part B: the app
sends CMD_SEND_TXT_MSG with txt_type 1 and the text ver, the node replies
with RESP_CODE_SENT and sends a TXT_MSG over LoRa to the repeater; the
repeater checks isAdmin(), runs handleCommand() and sends the reply back as
TXT_TYPE_CLI_DATA; the node puts it in the offline queue, sends
PUSH_CODE_MSG_WAITING, the app fetches it with CMD_SYNC_NEXT_MESSAGE and
receives RESP_CODE_CONTACT_MSG_RECV_V3, and asks again until
RESP_CODE_NO_MORE_MESSAGES](../../../images/en/usb-serial-2.svg)

### A write command

Steps 1 to 3: the app sets the node name to `PE1HVH`. That takes two
frames:

| Direction | Bytes | Meaning |
|---|---|---|
| app → node | `3C 07 00 08 50 45 31 48 56 48` | `<`, length 7, `CMD_SET_ADVERT_NAME` (8), `PE1HVH` |
| node → app | `3E 01 00 00` | `>`, length 1, `RESP_CODE_OK` (0) |

The length field counts the payload only: the opcode plus six characters.
The node handles the command in a single pass:

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

A name that is too long is truncated, `savePrefs()` writes it away, and only
then does the OK follow. No push comes after it and nothing goes on air.

### A remote CLI command

Steps 4 to 15. The CLI screen in an app operates a repeater or room server
remotely; the companion itself only has the console from
[Companion: CLI Rescue](../../cli/companion-rescue.md). The app first has to
be logged in to the repeater as admin, because the repeater only executes a
command for a client with admin rights
(`examples/simple_repeater/MyMesh.cpp` r.702). See [ACL](../../cli/acl.md).

The command travels as a text message with a type of its own:

`src/helpers/TxtDataHelpers.h` r.6-8

```cpp
#define TXT_TYPE_PLAIN          0      // a plain text message
#define TXT_TYPE_CLI_DATA       1      // a CLI command
#define TXT_TYPE_SIGNED_PLAIN   2      // plain text, signed by sender
```

The node recognises that type in `CMD_SEND_TXT_MSG` and picks a different
send function than for an ordinary message:

`examples/companion_radio/MyMesh.cpp` r.1102-1105

```cpp
      if (txt_type == TXT_TYPE_CLI_DATA) {
        msg_timestamp = getRTCClock()->getCurrentTimeUnique(); // Use node's RTC instead of app timestamp to avoid tripping replay protection
        result = sendCommandData(*recipient, msg_timestamp, attempt, text, est_timeout);
        expected_ack = 0; // no Ack expected
```

Two things differ from a write command:

- **The first reply is not the execution.** `RESP_CODE_SENT` in step 5 means
  the packet is ready to be sent. No ACK is expected, so the app hears
  nothing more until the repeater's reply has arrived.
- **The reply comes back as a message.** The repeater executes the command
  with `handleCommand()` (`examples/simple_repeater/MyMesh.cpp` r.739) and
  sends the text back with type `TXT_TYPE_CLI_DATA` (r.749), after a delay
  of `CLI_REPLY_DELAY_MILLIS`, 600 ms (r.59). If the command produces no
  text, or the app repeats a command with the same timestamp, the repeater
  sends nothing back (r.736-742).

The companion puts the reply in the offline queue and nudges the app, steps 9
and 10:

`examples/companion_radio/MyMesh.cpp` r.459-465

```cpp
  addToOfflineQueue(out_frame, i);

  if (_serial->isConnected()) {
    uint8_t frame[1];
    frame[0] = PUSH_CODE_MSG_WAITING; // send push 'tickle'
    _serial->writeFrame(frame, 1);
  }
```

The app fetches it with `CMD_SYNC_NEXT_MESSAGE` and repeats that until the
queue is empty, steps 11 to 15:

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

The reply in step 12 is a `RESP_CODE_CONTACT_MSG_RECV_V3` with `txt_type` 1.
From that type the app can tell that the text belongs in the CLI screen and
not among the messages.

### A repeater directly on USB

![Sequence diagram with two participants, terminal and repeater: the
terminal sends the characters v, e, r and a CR without a start byte or
length, the repeater sends each character back, runs handleCommand(0,
command, reply) on the CR and sends back two spaces, an arrow and the reply,
only if that reply is not empty](../../../images/en/usb-serial-3.svg)

On a repeater the cable is not a companion link. The repeater firmware does
not use `ArduinoSerialInterface` and no frames travel over the cable: the
CLI reads plain text. Each character is echoed straight back, and on a CR
the firmware executes the command:

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

The commands are the same as remotely: in both cases handling goes through
`handleCommand()`. The difference is the packaging. Remotely it is an
encrypted text message over LoRa with a timestamp; here it is a line of text
without a timestamp, hence the `0` as first argument. The commands
themselves are in the [CLI reference](../../cli/introduction.md).

## Sources

Firmware, commit `d929643` (v1.17.1, 14 August 2026):

- [`src/helpers/BaseSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/BaseSerialInterface.h)
  — the shared interface and `MAX_FRAME_SIZE`
- [`src/helpers/MultiSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/MultiSerialInterface.h)
  — `MAX_INTERFACES`, sending to every transport, `isConnected()`
- [`src/helpers/ArduinoSerialInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/ArduinoSerialInterface.cpp)
  — `writeFrame()`, `checkRecvFrame()` and the four states
- [`src/helpers/esp32/SerialWifiInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/esp32/SerialWifiInterface.cpp)
  and [`src/helpers/ethernet/SerialEthernetInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/ethernet/SerialEthernetInterface.cpp)
  — the same header over TCP
- [`src/helpers/TxtDataHelpers.h`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/src/helpers/TxtDataHelpers.h)
  — `TXT_TYPE_CLI_DATA`
- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/companion_radio/main.cpp)
  — the build flag per transport and `interface_manager`
- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/companion_radio/MyMesh.cpp)
  — `CMD_SET_ADVERT_NAME`, `CMD_SEND_TXT_MSG`, `queueMessage()`,
  `CMD_SYNC_NEXT_MESSAGE`
- [`examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/simple_repeater/MyMesh.cpp)
  — executing and answering a remote CLI command
- [`examples/simple_repeater/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e/examples/simple_repeater/main.cpp)
  — the text CLI on the serial port

Script: [`tools/usb-serial-example.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/usb-serial-example.py)
— the byte example of the write command.

Related in this documentation:

- [The interaction model](../../companion/logical/interaction-model.md) —
  request, reply and push
- [The frame](../../companion/technical/frame-format.md) — opcode and
  payload inside the frame
- [WiFi as a Companion Link](wifi.md) — the same frame over TCP
- [BLE Architecture](ble-architecture.md) — the same frame over BLE
- [CLI reference](../../cli/introduction.md) — the commands
- [Companion: CLI Rescue](../../cli/companion-rescue.md) — the companion's
  own console
- [The Hardware of a Node](../introduction.md) — where this part sits

Translated from Dutch by Anthropic Claude
