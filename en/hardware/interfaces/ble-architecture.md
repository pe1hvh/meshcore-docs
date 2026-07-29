# BLE Architecture

*BLUETOOTH LOW ENERGY · GATT · NUS*

This chapter describes how MeshCore communicates with companion devices via **Bluetooth Low Energy (BLE)**, and provides an analysis of the BLE stack and GATT services.

## BLE vs. Classic Bluetooth

Since Bluetooth 4.0 (2010) there are two separate radio systems within the Bluetooth standard — they are **different radio protocols** that do not communicate directly with each other.

| Property | Classic Bluetooth (BR/EDR) | BLE |
|---|---|---|
| Power consumption | High | Very low |
| Data rate | High | Low |
| Kanalen | 79 × 1 MHz | 40 × 2 MHz |
| Typical use | Audio, files | Sensors, IoT, MeshCore |

The T1000-E is a **BLE-only** device. Your smartphone is dual-mode: it talks to your Bluetooth headphones (Classic) and to your MeshCore radio (BLE).

## The BLE Stack (7 layers)

BLE Stack SVG

![Diagram 1 bij ble-architectuur](../../../images/en/ble-architecture-1.svg)

## GATT — Generic Attribute Profile

GATT is the structure through which BLE devices offer their data. Think of it as a digital notice board:

```text
Service (categorie)
  └── Characteristic (specifiek datapunt)
        └── Descriptor (extra configuratie)
```

### NUS — Nordic UART Service

NUS is a standard BLE service from Nordic Semiconductor that simulates a serial port (UART) over Bluetooth. MeshCore uses NUS for all communication with companion devices.

```text
Nordic UART Service (NUS)
  ├── RX Characteristic → data van radio naar computer
  └── TX Characteristic → data van computer naar radio

UUID: 6e400001-b5a3-f393-e0a9-e50e24dcca9e
```

> [!NOTE]
> **NUS is not a protocol** — it is a service specification. GATT is the protocol; NUS is a service offered via GATT.

## Official vs. Custom Services

| Type | UUID | Wie mag maken? | Voorbeeld |
|---|---|---|---|
| Officieel (SIG) | 16-bit | Alleen Bluetooth SIG | Heart Rate (0x180D) |
| Custom | 128-bit | Iedereen | NUS, MeshCore Companion |

### Well-known official services

| Service | UUID | Application |
|---|---|---|
| Battery Service | 0x180F | Battery level |
| Device Information | 0x180A | Manufacturer, model, firmware |
| Heart Rate | 0x180D | Heart rate monitors |
| Environmental Sensing | 0x181A | Temperature, humidity, pressure |
| HID over GATT | 0x1812 | Keyboards, mice |
| Generic Access | 0x1800 | Required — device name |

## Notify vs. Read

| Method | How it works | When |
|---|---|---|
| Read | You actively request data | One-time values (e.g. battery status) |
| Notify | Device sends automatically when new data arrives | Continuous data stream (e.g. messages) |

For MeshCore you use **Notify** — you want to know when a message arrives. The CCCD (Client Characteristic Configuration Descriptor) is the on/off switch for Notify.

> [!WARNING]
> **Crucial:** Only one client at a time can activate Notify. A second client will receive the error `Notify acquired`.

## Pairing, Bonding, and Trust

| Step | What happens | Analogy |
|---|---|---|
| Pairing | Exchange cryptographic keys | Exchange phone numbers |
| Bonding | Permanently store keys | Save number in contacts |
| Trust | Automatically trust device | Add someone to favourites |

```text
# Controleer in Linux:
bluetoothctl info AA:BB:CC:DD:EE:FF | egrep -i "Paired|Bonded|Trusted"

# Verwacht:
Paired: yes
Bonded: yes
Trusted: yes
```

## BLE Channel Layout

The 2.4 GHz ISM band (2400–2483.5 MHz) is divided into **40 channels of 2 MHz each**:

| Type | Channels | Function |
|---|---|---|
| Advertising | 3 (nrs. 37, 38, 39) | Finding devices, initiating connections |
| Data | 37 (nrs. 0–36) | Actual communication |

Advertising channels are strategically chosen to avoid **Wi-Fi interference** — they sit between Wi-Fi channels 1, 6, and 11. Communication uses **frequency hopping**: one channel at a time, constantly changing.

## Serial vs. Structured

NUS is a **serial service** — it simulates a UART port with unstructured bytes. Official SIG services are **structured** with fixed fields.

| Aspect | Serial (NUS) | Structured (SIG) |
|---|---|---|
| Data format | Free, self-defined | Fixed, by specification |
| Parsing | Build custom parser | Standard parser possible |
| Interoperability | Own software only | Any conforming app/device |
| Flexibility | Maximum | Limited to spec |

### Why MeshCore chooses NUS

- **Flexibility** — The Companion Protocol needs its own framing
- **No suitable SIG service** — There is no "Mesh Radio Service" standard
- **Bidirectional** — NUS offers both RX and TX characteristics
- **Simplicity** — No complex SIG specification to implement

## Ownership — The core problem

**Ownership** indicates which client holds the active GATT session with Notify. This sits at **OSI layer 5 (session)**. Only one listener may be connected at a time.

| Typical "owner" | Problem | Solution |
|---|---|---|
| GNOME Bluetooth GUI | Notify acquired | Close GUI |
| bluetoothctl connect | Tool fails on notify | Always disconnect first |
| Phone Bluetooth on | Phone claims connection | Turn BT off on phone |
| Multiple scripts | First wins, rest fails | One tool at a time |

## BLE Pairing on Headless Linux

When developing MeshCore applications on a **desktop Linux system** (Ubuntu, Fedora with GNOME or KDE), BLE PIN pairing typically works without issue. The desktop environment automatically registers a Bluetooth pairing agent via D-Bus, which handles PIN requests in the background.

On **headless systems** — such as a Raspberry Pi, server, or embedded Linux without a graphical environment — there is no default pairing agent active. The BlueZ `bluetoothd` daemon does not handle pairing itself: it delegates every PIN request via D-Bus to a registered agent. Without an agent, PIN requests go unanswered and the BLE connection fails.

This makes the problem hard to detect during development: on a desktop everything works, but when deploying to the headless target system — precisely the most common use case for `meshcore_py` — the connection fails.

### Overview per environment

| Environment | Standaard agent? | PIN-pairing werkt? |
|---|---|---|
| Ubuntu/Fedora Desktop (GNOME/KDE) | ✅ Desktop BT agent | ✅ Yes — agent handles PIN silently |
| Raspberry Pi OS (headless) | ❌ No agent | ❌ No — PIN requests unanswered |
| Raspberry Pi OS (with desktop) | ✅ Desktop BT agent | ✅ Probably yes |
| Fedora/Debian server (headless) | ❌ No agent | ❌ No — same problem |

### Oplossing

The fix is simple: register a custom D-Bus pairing agent before connecting. This works on all Linux environments — with or without a desktop. See the source reference below for a detailed technical description and sample code.

## Conclusion

MeshCore BLE companion works correctly on Linux. The only requirement is: **exactly one active BLE client per radio**. The GATT/NUS architecture ensures reliable communication between node and companion device. On headless systems, a custom D-Bus pairing agent is additionally required for successful PIN verification.

*The section on BLE pairing on headless Linux is based on a contribution by PE1HVH to [meshcore_py issue #33 ↗](https://github.com/meshcore-dev/meshcore_py/issues/33#issuecomment-3902438474).*

Translated from Dutch by Anthropic Claude
