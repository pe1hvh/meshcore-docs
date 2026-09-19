# SenseCap DFU

*TECHNICAL · OTA FIRMWARE UPDATE — SENSECAP SOLAR NODE P1-PRO*

Device: SenseCAP Solar Node P1-Pro
MCU: Nordic nRF52840
Bootloader: OTAFIX
Firmware: MeshCore
April 2026

The SenseCAP Solar Node P1-Pro is used in practice as a MeshCore repeater at hard-to-reach locations: rooftops, masts, outdoor installations. Once such a repeater is mounted, physical access is often difficult or not immediately possible.

Various internet sources contradict each other regarding a successful firmware update. This page is the result of thorough testing and an investigation into the background of the nRF52 DFU protocol, with the goal of finding a reliable method for firmware updates without having to climb onto the roof.

For the DFU update, the official [**nRF Device Firmware Update** app by Nordic Semiconductor ↗](https://play.google.com/store/apps/details?id=no.nordicsemi.android.dfu&hl=en-US&pli=1) (Android, Google Play) was used. This is the reference implementation of the Nordic Secure DFU protocol and the only app with which the procedure in this document works reliably.

⚠️ OTAFIX is not an option, but a requirement.
Before a SenseCAP Solar Repeater goes on the roof, the OTAFIX bootloader
must
be installed. Without OTAFIX: one failed OTA update = device unreachable via Bluetooth = physical access required for recovery.
The tests in this document used
sensecap_solar_bootloader-0.9.2-OTAFIX2.1.uf2
, downloaded via
meshcore.co.uk/flasher.html ↗
.
Table of Contents

1. Recommended DFU settings
2. The `start ota` CLI command
3. The complete OTA process step by step
4. Technical explanation of the two-phase DFU protocol
5. What to do if the process fails after Bootloader enabled
6. The two BLE advertisement names explained
7. Why OTAFIX
8. Overview table: correct vs. incorrect
9. Sources

## 1 · Recommended DFU settings

The following settings apply to the **nRF Device Firmware Update** app by Nordic Semiconductor (Android). They have been tested and work reliably with OTAFIX 2.1 on the SenseCAP Solar Node P1-Pro. With these settings the process runs fully automatically.

| Setting | Value | Notes |
|---|---|---|
| Packet Receipt Notification | ON | ACK every N packets |
| Number of Packets | `30` | Gives the bootloader sufficient timing window for phase transition |
| Reboot time | `0 ms` | No additional wait time needed |
| Scan Timeout | `2000 ms` | Search time for DFU device |
| Disable resume | ON ✅ | Essential — ensures the app rescans after disconnect instead of reconnecting by MAC |
| Force Scanning | ON ✅ | Works correctly in combination with `Disable resume: ON` — see §1 |
| Prepared Object delay | `0 ms` | No delay needed |

Note:
Disable resume: ON
is the critical setting.
Force Scanning: ON
without
Disable resume
causes a failed installation without
Disable resume: ON
(see §1). The combination of both makes the process fully automatic.

## 2 · The `start ota` CLI command

The CLI command `start ota` is part of the MeshCore repeater/room server firmware. It is executed via the Command Line tab in the MeshCore app, after remotely logging into the repeater with admin rights.

The MeshCore firmware internally calls the Nordic SoftDevice API and triggers a *buttonless DFU* (Device Firmware Update):

```text
start ota
    │
    ▼
MeshCore firmware calls Nordic SoftDevice API:
  sd_ble_gap_adv_set_configure()
  → advertisement data: name = "SENSECAP_SOLAR_OTA"
  → service UUID: Nordic DFU service (0xFE59)
    │
    ▼
Firmware triggers buttonless DFU:
  ble_dfu_buttonless
  → writes DFU flag to retained registers
  → starts advertising as DFU target
  → waits for connection from DFU client
```

> [!NOTE]
> Confirmation:
> After the command,
> OK
> appears in the CLI. The device then advertises via Bluetooth as
> SENSECAP_SOLAR_OTA
> . LoRa repeater functionality is
> no longer active
> until the update is complete.

## 3 · The complete OTA process step by step

With the recommended settings (see §1) the process runs fully automatically.

| Step | Action | Notes |
|---|---|---|
| 1 | Companion App CLI: `start ota` | Triggers DFU mode in firmware |
| 2 | CLI shows `OK: <mac address>` | Confirmation that DFU is active |
| 3 | Device advertises as `SENSECAP_SOLAR_OTA` | Application-layer DFU active |
| 4 | DFU app: select correct firmware `.zip` | The `sensecap_solar_repeater-vX.Y.Z.zip` |
| 5 | DFU app: select `SENSECAP_SOLAR_OTA` | Connect to application DFU |
| 6 | DFU app: Start update | Command Object (init packet) is sent — app handles the phase transition automatically |
| 7 | DFU app: transfer complete | Data Object (firmware binary) sent, hash verified, automatic reboot |

> [!NOTE]
> Result:
> Firmware written, hash verified, automatic reboot ✅

Bootloader enabled, but installation failed?
See §5.

## 4 · Technical explanation of the two-phase DFU protocol

The nRF52840 uses Nordic's **Secure DFU protocol** which operates in two strict phases:

```text
Phase 1 — Command Object (Init Packet)
│
│  ┌─────────────────────────────────────────────┐
│  │ • firmware metadata                         │
│  │ • hardware version check                    │
│  │ • firmware hash (SHA-256)                   │
│  │ • cryptographic signature                   │
│  └─────────────────────────────────────────────┘
│
│  → bootloader validates → "Bootloader enabled" ✅
│
│  ** Bootloader switches internal state         **
│  ** BLE connection is dropped                  **
│  ** Device re-advertises as XIAO_DFU           **
│
Phase 2 — Data Object (Firmware payload)
│
│  ┌─────────────────────────────────────────────┐
│  │ • actual firmware binary in chunks          │
│  │ • PRN (Packet Receipt Notification) every 8 │
│  │   packets an ACK                            │
│  │ • Execute → hash verify → reboot            │
│  └─────────────────────────────────────────────┘
```

The name change from `SENSECAP_SOLAR_OTA` to `XIAO_DFU` is **not a bug** — it is the designed behaviour of the OTAFIX bootloader. After successful validation of the Command Object, the bootloader exits the application-initiated DFU mode and transitions to the bootloader-native DFU mode with a different BLE advertisement identity.

## 5 · What to do if the process fails after Bootloader enabled

When the DFU app shows "Bootloader enabled" but the firmware transfer subsequently fails or stalls, there is no reason to panic. Thanks to the OTAFIX bootloader, the device does **not** restart into USB/UF2 mode on a failed OTA — it keeps advertising and remains reachable via Bluetooth.

After a failed transfer, the bootloader is in OTA DFU mode and the device advertises as `XIAO_DFU`. The process can be continued manually:

| Step | Action | Notes |
|---|---|---|
| 1 | DFU app: press ABORT if active | Cleanly terminate the current failed session |
| 2 | DFU app: scan for available devices | The device is now advertising as `XIAO_DFU` |
| 3 | Select `XIAO_DFU` as target device | This is the bootloader-native DFU mode of the OTAFIX bootloader |
| 4 | Restart the firmware transfer | Data Object (firmware binary) is sent, hash verified, automatic reboot |

> [!NOTE]
> Why this works:
> The OTAFIX bootloader falls back to OTA DFU mode (advertises as
> XIAO_DFU
> ) on a failed OTA instead of USB/UF2 mode. The device therefore remains fully reachable via Bluetooth — even on a roof or mast — and a new attempt is always possible without physical access.

## 6 · The two BLE advertisement names explained

The two names that appear during the OTA process come from **different layers** and have **different origins**:

**SENSECAP_SOLAR_OTA**

- **Phase 1 · Application layer** — Hardcoded in the MeshCore firmware for this board type. Active during
        Phase 1 (Command Object). Triggered by CLI command start ota .
        Just like other boards get their own name ( RAK4631_OTA , T114_OTA , etc.).

**XIAO_DFU**

- **Phase 2 · Bootloader layer** — Comes from the OTAFIX bootloader . Active during Phase 2 (Data Object).
        Without OTAFIX this would be AdaDFU — the generic Adafruit standard name.

| Name | Layer | Source | Without OTAFIX |
|---|---|---|---|
| `SENSECAP_SOLAR_OTA` | Application | MeshCore firmware | Same name — unchanged |
| `XIAO_DFU` | Bootloader | OTAFIX bootloader | `AdaDFU` (Adafruit generic) |

## 7 · Why OTAFIX

The reason is concrete and concerns one critical behavioural defect in the stock Adafruit bootloader:

**OTA fails → physical access required ❌**

- **Stock bootloader** — On a failed OTA, the stock bootloader falls back to UF2/CDC mode (USB drive,
        serial port). The device is no longer reachable via Bluetooth. For a repeater on a roof or mast
        this means: climbing up to it.

**OTA fails → recoverable via BLE ✅**

- **OTAFIX bootloader** — On a failed OTA, OTAFIX restarts in OTA DFU mode (Bluetooth, advertises
        as XIAO_DFU ). The device remains reachable via Bluetooth. Retry without physical access.

OTAFIX also resolves a **second problem**: the stock bootloader had `HCI_RX_BUF_QUEUE_SIZE = 8`. At the packet frequency of an OTA transfer, this buffer overflowed, resulting in random OTA failures. OTAFIX increased this to `HCI_RX_BUF_QUEUE_SIZE = 16`, making buffer overflow during normal OTA transfers practically non-existent.

| Issue | Stock bootloader | OTAFIX |
|---|---|---|
| Failed OTA → fallback behaviour | UF2/CDC (USB only) | OTA DFU (Bluetooth) |
| BLE HCI buffer during OTA transfer | 8 slots → overflow possible | 16 slots → stable |
| Physical access needed on failure | Yes | No |

> [!NOTE]
> The name says it literally:
> OTAFIX fixes the OTA process — not by making OTA better, but by keeping the
> consequences of a failed OTA manageable
> .

## 8 · Overview table: correct vs. incorrect

| Scenario | Result | Technical reason |
|---|---|---|
| Automated: `Force Scanning: ON` + `Disable resume: ON` + 30 packets | ✅ Works automatically | `Disable resume` ensures correct reconnection to `XIAO_DFU` after phase transition |
| Manual: ABORT after "Bootloader enabled", reconnect to `XIAO_DFU` | ✅ Fallback — always works | Follows exactly the two-phase state machine of the bootloader |
| `Force Scanning: ON` without `Disable resume` | ❌ Firmware written, no reboot | MAC-based reconnection skips the phase transition |
| OTA without OTAFIX bootloader, update fails | ❌ Brick | Stock bootloader falls back to UF2, not OTA DFU |
| OTA with OTAFIX bootloader, update fails | ✅ Recoverable via BLE | OTAFIX restarts in OTA DFU mode, not UF2 |

## Sources

| Source | Publisher | Subject |
|---|---|---|
| [MeshCore Flasher ↗](https://meshcore.co.uk/flasher.html) | meshcore.co.uk | Download of OTAFIX bootloader (`sensecap_solar_bootloader-0.9.2-OTAFIX2.1.uf2`) |
| [nRF Device Firmware Update (Android) ↗](https://play.google.com/store/apps/details?id=no.nordicsemi.android.dfu) | Nordic Semiconductor | Reference implementation of the Nordic Secure DFU protocol (Android app) |
| [Adafruit nRF52 Bootloader ↗](https://github.com/adafruit/Adafruit_nRF52_Bootloader) | Adafruit / GitHub | Source code of the stock bootloader on which OTAFIX is based |
| [OTAFIX Bootloader (GitHub) ↗](https://github.com/oltaco/Adafruit_nRF52_Bootloader_OTAFIX) | oltaco / GitHub | Source code and changelog of OTAFIX 2.0 and 2.1, including recommended settings per version |

Disclaimer
— This document has been carefully compiled on the basis of extensive practical tests conducted on 7 and 8 April 2026. At the time of testing, no other robust method was known for performing a reliable OTA firmware update on the SenseCAP Solar Node P1-Pro without physical access to the device. This does not exclude the possibility that alternative methods exist or have since become available. The described procedure is the result of reproducibly tested methods, but firmware updates are always carried out at your own risk. The author accepts no liability for damage to equipment or loss of functionality resulting from applying the information in this document. When in doubt, consult the current documentation from Nordic Semiconductor, Seeed Studio, and the MeshCore project.

Translated from Dutch by Anthropic Claude
