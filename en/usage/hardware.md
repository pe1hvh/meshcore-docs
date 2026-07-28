# Hardware Overview

*DEVICES · COMPARISON · OFFLINE MAPS*

MeshCore supports a wide range of hardware. Devices fall into three categories: **Companion Radios** (require a smartphone), **Standalone Devices** (own screen and keyboard), and **Repeaters/Servers** (extending the network).

> [!WARNING]
> **Note:** Always check that the device has the correct frequency for Europe (868 MHz, not 915 MHz).

## Hardware

### LilyGO T-Deck Plus — €70–80

**LilyGO · ESP32-S3** · 2.8" LCD · QWERTY keyboard · GPS · Trackball · SMA connector

- ✓ Fully standalone
- ✓ Physical keyboard
- ✓ Built-in GPS
- ✓ External antenna possible
- ✗ Trackball can be sensitive
- ✗ Reset button can be pressed accidentally

**Best for:** Standalone use without smartphone

### Heltec WiFi LoRa 32 V3/V4 — €20–40

**Heltec · ESP32-S3 · SX1262** · 0.96" OLED · WiFi · BLE · V4: 28dBm TX

- ✓ Very affordable
- ✓ Compact, widely supported
- ✓ Suitable as companion and repeater
- ✗ Requires smartphone
- ✗ Small screen, no standard enclosure

**Best for:** Budget entry with smartphone

### RAK WisBlock RAK4631 — €40–60

**RAKwireless · nRF52840** · Modular system · Extremely low power · Expansion modules

- ✓ Extremely low power consumption (weeks/months on battery)
- ✓ Modular, perfect for solar
- ✓ Professional quality
- ✗ More expensive, no WiFi (BLE only)
- ✗ More complex setup

**Best for:** Low-power and modular solutions

### Seeed Studio T1000-E — €30–40

**Seeed Studio · nRF52840** · Credit card size · GPS · BLE · Low power

- ✓ Very compact
- ✓ Built-in GPS
- ✓ Low power, robust
- ✗ No display or buttons
- ✗ Requires smartphone for all interaction

**Best for:** Compact companion radio with GPS

> [!NOTE]
> **Chip versus board.** This page is about devices. Why the chip inside decides what the device can do — BLE, WiFi, display, OTA, flashing method — is covered in [MeshCore Platforms](../platform/platforms.md). What each family puts in the chip is covered in [The Four Platform Families](../platform/platform-families.md).

## Comparison table

| Device | Chip | Display | GPS | WiFi | Price |
|---|---|---|---|---|---|
| T-Deck Plus | ESP32-S3 | 2.8" LCD | Yes | Yes | €70–80 |
| Heltec V3/V4 | ESP32-S3 | 0.96" OLED | No | Yes | €20–40 |
| RAK4631 | nRF52840 | No | Module | No | €40–60 |
| T1000-E | nRF52840 | No | Yes | No | €30–40 |

## Offline Maps on T-Deck

The T-Deck Plus can display offline maps via a microSD card (max 32 GB, FAT32). Several methods are available:

- **Map Tiles Downloader** (recommended) — Tool by OM7TEK via `pipx install mt-downloader`
- **tdeck-maps script** — Python script for specific cities/regions
- **Ready-made maps** — Available via buymeacoffee.com/ripplebiz

> [!NOTE]
> **Tip:** Start with zoom level 8–12 for a good balance between detail and storage space. Deeper zoom (13+) requires an Ultra licence. The SD card must be inserted before powering on the T-Deck.

Translated from Dutch by Anthropic Claude
