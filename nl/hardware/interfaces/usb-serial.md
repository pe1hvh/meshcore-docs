# USB-serieel

*FRAMEFORMAAT · `>` EN `<` · 16-BITS LENGTE · 176 BYTES*

De seriële verbinding is het transport zonder radio, zonder pincode en
zonder netwerk: een kabel naar een computer. Het is ook het transport
waarvan het formaat het duidelijkst te lezen is, en dat formaat is
hetzelfde als bij BLE en WiFi. Dit hoofdstuk beschrijft het frame byte voor
byte en de toestandsmachine die het uit de bytestroom haalt.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/ArduinoSerialInterface.cpp`,
> `src/helpers/ArduinoSerialInterface.h` en
> `src/helpers/BaseSerialInterface.h`.

![Frameopbouw van de seriële verbinding: startbyte, lengte in twee bytes
laagste eerst, gevolgd door de payload, met de vier toestanden van de
ontvangende toestandsmachine](../../../images/nl/usb-serial-1.svg)

## Eén interface, drie invullingen

Alles wat een companion-app met een node uitwisselt loopt door
`BaseSerialInterface`. Die kent maar twee functies:

`src/helpers/BaseSerialInterface.h` r.16-20

```cpp
  virtual bool isConnected() const = 0;

  virtual bool isWriteBusy() const = 0;
  virtual size_t writeFrame(const uint8_t src[], size_t len) = 0;
  virtual size_t checkRecvFrame(uint8_t dest[]) = 0;
```

`ArduinoSerialInterface`, `SerialBLEInterface` en `SerialWifiInterface`
vullen die drie in. Welke er in de firmware zit is een buildkeuze; zie
[WiFi als companion-verbinding](wifi.md).

De framegrootte is voor alledrie gelijk:

`src/helpers/BaseSerialInterface.h` r.5

```cpp
#define MAX_FRAME_SIZE  176   // +4 for transport codes (region scoping)
```

176 bytes, met het commentaar dat er vier bij komen voor transportcodes.
Wat die transportcodes zijn staat in
[Regio's en Scopes](../../techniek/regions-and-scopes.md).

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

`src/helpers/ArduinoSerialInterface.cpp` r.59-68

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
een aangekondigde lengte van nul brengt de machine meteen terug naar `IDLE`
— een leeg frame bestaat niet.

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

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`src/helpers/ArduinoSerialInterface.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ArduinoSerialInterface.cpp)
  — `writeFrame()`, `checkRecvFrame()` en de vier toestanden
- [`src/helpers/BaseSerialInterface.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/BaseSerialInterface.h)
  — de gedeelde interface en `MAX_FRAME_SIZE`

Verwante hoofdstukken:

- [WiFi als companion-verbinding](wifi.md) — hetzelfde frame over TCP
- [BLE Architectuur](ble-architecture.md) — hetzelfde frame over BLE
- [Regio's en Scopes](../../techniek/regions-and-scopes.md) — de vier bytes
  transportcode waar het commentaar naar verwijst
- [Hardware van een node](../introduction.md) — waar dit onderdeel zit
