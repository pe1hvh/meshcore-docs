# Node Matrix

*SIXTY BOARDS · MCU · RADIO · PERIPHERALS · PRICE*

Every device the MeshCore web flasher offers, side by side on platform
family, memory, radio, peripherals and price. This chapter is a reference
table, not a buying guide: why the platform matters is in
[MeshCore Platforms](platforms.md), and what each family puts inside the
chip is in [The Four Platform Families](platform-families.md).

> [!NOTE]
> **Source.** This page has **not** been verified against the firmware,
> and cannot be: not a single column comes from the firmware repo. The
> device list is the saved page of the
> [MeshCore web flasher](https://flasher.meshcore.io) of 27 July 2026,
> sixty devices — the same list the counts in
> [MeshCore Platforms](platforms.md) rest on. RAM, clock speed and link
> options follow from the SoC and are in the datasheets; radio, display,
> GPS, battery, enclosure and price come from manufacturer and community
> sources. Provenance per column is listed under [Sources](#sources).
> There is no script in `tools/` that recomputes these figures.

## What is in the list

Sixty devices across three platform families: 32 with an ESP32, 27 with an
nRF52840 and one with an RP2040. The flasher offers nothing for STM32WL.
Why the split looks like this is explained in
[MeshCore Platforms](platforms.md).

One device has no LoRa radio at all. The LilyGo T-Display Pro appears in
the flasher as an ESP-NOW board; ESP-NOW works on 2.4 GHz and is not LoRa.
It is still listed below, with `n/a` in the TX power column.

## How to read these tables

The four tables describe the same sixty devices in the same order, keyed
on the node name.

- **`°` after the name** — at least one value for this device is still
  unconfirmed. Which one is listed under
  [To be confirmed](#to-be-confirmed). Twenty-five of the sixty devices
  carry the mark.
- **yes · option · no** in the GPS, WiFi, BLE and USB columns. *Option*
  means: depends on the version, the revision or a separate module.
- **Prices** are indicative street prices in euros, excluding shipping and
  VAT.

### Companion, standalone and repeater

MeshCore splits its firmware into roles, and the role decides whether you
need a phone. A **companion** node is a radio without an interface of its
own: you operate it with the MeshCore app, over BLE, USB or WiFi. Boards
with both a display and a keyboard run **standalone** firmware and work
without a phone. **Repeaters** and room servers need no app while running
either — only while being set up.

## Table 1 — identity and MCU

RAM and clock speed follow from the SoC, not from the board. Two devices
with the same chip therefore carry the same figures here, however
different they are otherwise.

| Node | Vendor | Platform family | Core | RAM | Speed |
|---|---|---|---|---|---|
| ThinkNode M1 | Elecrow | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| ThinkNode M2 | Elecrow | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| ThinkNode M3° | Elecrow | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| ThinkNode M5 | Elecrow | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| ThinkNode M6 | Elecrow | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| GAT562 30s | GAT-IoT | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| GAT562 Tracker° | GAT-IoT | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| Wireless Paper | Heltec | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| Mesh Node T096 | Heltec | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| Mesh Node T1° | Heltec | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| MeshPocket° | Heltec | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| MeshSolar / MeshTower | Heltec | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| T114 | Heltec | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| WiFi LoRa 32 v2 | Heltec | ESP32 | ESP32 · 2× Xtensa LX6 | 520 KB | 240 MHz |
| WiFi LoRa 32 v3 | Heltec | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| WiFi LoRa 32 v4° | Heltec | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| v4 + Expansion Kit (Touch)° | Heltec | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| Vision Master E213 | Heltec | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| Vision Master E290 | Heltec | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| Wireless Tracker | Heltec | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| Wireless Tracker v2° | Heltec | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| Wireless Stick Lite v3 | Heltec | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| Nano° | Ikoka | nRF52 | nRF52840 · Cortex-M4F (XIAO) | 256 KB | 64 MHz |
| Stick° | Ikoka | nRF52 | nRF52840 · Cortex-M4F (XIAO) | 256 KB | 64 MHz |
| LT1° | Keepteen | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| LoRa32 v2.1_1.6 | LilyGo | ESP32 | ESP32 · 2× Xtensa LX6 | 520 KB | 240 MHz |
| T-Beam (SX1262) | LilyGo | ESP32 | ESP32 · 2× Xtensa LX6 | 520 KB | 240 MHz |
| T-Beam 1.2 (SX1276) | LilyGo | ESP32 | ESP32 · 2× Xtensa LX6 | 520 KB | 240 MHz |
| T-Beam 1W° | LilyGo | ESP32 | ESP32 · 2× Xtensa LX6 | 520 KB | 240 MHz |
| T-Beam Supreme | LilyGo | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB + 8 MB PSRAM | 240 MHz |
| T-Deck | LilyGo | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB + 8 MB PSRAM | 240 MHz |
| T-Deck Max° | LilyGo | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB + PSRAM | 240 MHz |
| T-Deck Pro° | LilyGo | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB + 8 MB PSRAM | 240 MHz |
| T-Display Pro° | LilyGo | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB + PSRAM | 240 MHz |
| T-Echo | LilyGo | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| T-Echo Card° | LilyGo | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| T-Echo Lite° | LilyGo | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| T-Lora Pager° | LilyGo | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB + 8 MB PSRAM | 240 MHz |
| T-Watch S3 Plus | LilyGo | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB + 8 MB PSRAM | 240 MHz |
| T-Watch Ultra° | LilyGo | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB + PSRAM | 240 MHz |
| T3 S3 (SX126x) | LilyGo | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| T3 S3 (SX127x) | LilyGo | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| T5 E-Paper S3 Pro° | LilyGo | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB + PSRAM | 240 MHz |
| R1 Neo | Muzi Works | nRF52 | nRF52840 · Cortex-M4F (RAK4631) | 256 KB | 64 MHz |
| ProMicro nRF52 (faketec)° | DIY | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| WisBlock / WisMesh RAK4631 | RAK | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| WisBlock 3112 | RAK | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| WisMesh 1W Booster | RAK | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| WisMesh Tag° | RAK | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| Pico 2040 + WaveShare SX1262° | Raspberry Pi | RP2040 | RP2040 · 2× Cortex-M0+ | 264 KB | 133 MHz |
| SenseCAP Solar | Seeed | nRF52 | nRF52840 · Cortex-M4F (XIAO Plus) | 256 KB | 64 MHz |
| SenseCAP T1000-E | Seeed | nRF52 | nRF52840 · Cortex-M4F (WM1110) | 256 KB | 64 MHz |
| Wio Tracker L1 EINK° | Seeed | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| Wio Tracker L1 Pro° | Seeed | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| Xiao C3 | Seeed | ESP32 | ESP32-C3 · RISC-V single-core | 400 KB | 160 MHz |
| Xiao nRF52 WIO | Seeed | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| Xiao S3 WIO | Seeed | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB + 8 MB PSRAM | 240 MHz |
| Nano G2 Ultra | UnitEng | nRF52 | nRF52840 · Cortex-M4F | 256 KB | 64 MHz |
| Station G2 | UnitEng | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |
| Voyage Station G3° | UnitEng / B&Q | ESP32 | ESP32-S3 · 2× Xtensa LX7 | 512 KB | 240 MHz |

## Table 2 — radio and TX power

> [!WARNING]
> **TX power is not permission.** The value in this table is the power of
> the radio or of the power amplifier, not the power you are legally
> allowed to use. On 868 MHz the EU limit is far lower. Deliberately turn
> boards above 22 dBm back down, and read
> [Regulations & Duty Cycle](../usage/regulations.md) before switching on
> a power amplifier.

| Node | Platform family | Chip (radio) | TX power |
|---|---|---|---|
| ThinkNode M1 | nRF52 | SX1262 | 22 dBm |
| ThinkNode M2 | ESP32 | SX1262 | 22 dBm |
| ThinkNode M3° | nRF52 | LR1110 | 22 dBm |
| ThinkNode M5 | ESP32 | SX1262 | 22 dBm |
| ThinkNode M6 | nRF52 | SX1262 (nRFLR1262) | 22 dBm |
| GAT562 30s | nRF52 | SX1262 + 30 dBm PA | 30 dBm |
| GAT562 Tracker° | nRF52 | SX1262 | 22 dBm |
| Wireless Paper | ESP32 | SX1262 | 21 dBm |
| Mesh Node T096 | nRF52 | SX1262 + 28 dBm PA | 28 dBm |
| Mesh Node T1° | nRF52 | SX1262 | 22 dBm |
| MeshPocket° | nRF52 | SX1262 | 22 dBm |
| MeshSolar / MeshTower | nRF52 | SX1262 + PA up to 1 W | 30 dBm |
| T114 | nRF52 | SX1262 | 22 dBm |
| WiFi LoRa 32 v2 | ESP32 | SX1276 | 20 dBm |
| WiFi LoRa 32 v3 | ESP32 | SX1262 | 21 dBm |
| WiFi LoRa 32 v4° | ESP32 | SX1262 + PA | 27 dBm |
| v4 + Expansion Kit (Touch)° | ESP32 | SX1262 + PA | 27 dBm |
| Vision Master E213 | ESP32 | SX1262 | 21 dBm |
| Vision Master E290 | ESP32 | SX1262 | 21 dBm |
| Wireless Tracker | ESP32 | SX1262 | 21 dBm |
| Wireless Tracker v2° | ESP32 | SX1262 | 21 dBm |
| Wireless Stick Lite v3 | ESP32 | SX1262 | 21 dBm |
| Nano° | nRF52 | SX1262 (EBYTE E22) | 22 dBm |
| Stick° | nRF52 | SX1262 (E22-900M30S/33S) | 33 dBm |
| LT1° | nRF52 | SX1262 | 22 dBm |
| LoRa32 v2.1_1.6 | ESP32 | SX1276 | 20 dBm |
| T-Beam (SX1262) | ESP32 | SX1262 | 22 dBm |
| T-Beam 1.2 (SX1276) | ESP32 | SX1276 | 20 dBm |
| T-Beam 1W° | ESP32 | SX1262 + 1 W PA | 30 dBm |
| T-Beam Supreme | ESP32 | SX1262 | 22 dBm |
| T-Deck | ESP32 | SX1262 | 22 dBm |
| T-Deck Max° | ESP32 | SX1262 | 22 dBm |
| T-Deck Pro° | ESP32 | SX1262 | 22 dBm |
| T-Display Pro° | ESP32 | no LoRa · ESP-NOW | n/a |
| T-Echo | nRF52 | SX1262 | 22 dBm |
| T-Echo Card° | nRF52 | SX1262 | 22 dBm |
| T-Echo Lite° | nRF52 | SX1262 | 22 dBm |
| T-Lora Pager° | ESP32 | SX1262 (SX1280 option) | 22 dBm |
| T-Watch S3 Plus | ESP32 | SX1262 | 22 dBm |
| T-Watch Ultra° | ESP32 | SX1262 | 22 dBm |
| T3 S3 (SX126x) | ESP32 | SX1262 | 22 dBm |
| T3 S3 (SX127x) | ESP32 | SX1276 | 20 dBm |
| T5 E-Paper S3 Pro° | ESP32 | SX1262 | 22 dBm |
| R1 Neo | nRF52 | SX1262 | 22 dBm |
| ProMicro nRF52 (faketec)° | nRF52 | SX1262 / E22 | 22 dBm |
| WisBlock / WisMesh RAK4631 | nRF52 | SX1262 | 22 dBm |
| WisBlock 3112 | ESP32 | SX1262 | 22 dBm |
| WisMesh 1W Booster | nRF52 | SX1262 + 1 W PA | 30 dBm |
| WisMesh Tag° | nRF52 | SX1262 | 22 dBm |
| Pico 2040 + WaveShare SX1262° | RP2040 | SX1262 (WaveShare HAT) | 22 dBm |
| SenseCAP Solar | nRF52 | SX1262 | 22 dBm |
| SenseCAP T1000-E | nRF52 | LR1110 | 22 dBm |
| Wio Tracker L1 EINK° | nRF52 | LR1110 | 22 dBm |
| Wio Tracker L1 Pro° | nRF52 | LR1110 | 22 dBm |
| Xiao C3 | ESP32 | SX1262 (Wio module) | 22 dBm |
| Xiao nRF52 WIO | nRF52 | SX1262 (Wio module) | 22 dBm |
| Xiao S3 WIO | ESP32 | SX1262 (Wio module) | 22 dBm |
| Nano G2 Ultra | nRF52 | SX1262 | 22 dBm |
| Station G2 | ESP32 | SX1262 + 37 dBm PA | 37 dBm |
| Voyage Station G3° | ESP32 | SX1262 + PA | 37 dBm |

## Table 3 — peripherals

The WiFi, BLE and USB columns say by which route the MeshCore app can talk
to the node. On the single RP2040 device that is USB only in practice: the
Pico W does have the hardware for BLE and WiFi, but the firmware leaves
both out of the build — hence *option* rather than *yes*.

| Node | Display | GPS | Companion app | WiFi | BLE | USB |
|---|---|---|---|---|---|---|
| ThinkNode M1 | 1.54″ e-ink 200×200 | yes | yes | no | yes | yes |
| ThinkNode M2 | 1.3″ OLED | no | yes | yes | yes | yes |
| ThinkNode M3° | none | yes | yes | no | yes | yes |
| ThinkNode M5 | 1.54″ e-ink | yes | yes | yes | yes | yes |
| ThinkNode M6 | none | yes | yes | no | yes | yes |
| GAT562 30s | 1.3″ OLED | yes | yes | no | yes | yes |
| GAT562 Tracker° | 1.3″ OLED | yes | yes | no | yes | yes |
| Wireless Paper | 2.13″ e-ink | no | yes | yes | yes | yes |
| Mesh Node T096 | 0.96″ OLED | yes | yes | no | yes | yes |
| Mesh Node T1° | OLED | yes | yes | no | yes | yes |
| MeshPocket° | none (LED) | no | yes | no | yes | yes |
| MeshSolar / MeshTower | none | option | no (repeater) | no | yes | yes |
| T114 | 1.14″ TFT (option) | option | yes | no | yes | yes |
| WiFi LoRa 32 v2 | 0.96″ OLED | no | yes | yes | yes | yes |
| WiFi LoRa 32 v3 | 0.96″ OLED | no | yes | yes | yes | yes |
| WiFi LoRa 32 v4° | 0.96″ OLED (option) | no | yes | yes | yes | yes |
| v4 + Expansion Kit (Touch)° | touch-TFT | no | no (standalone) | yes | yes | yes |
| Vision Master E213 | 2.13″ e-ink | no | yes | yes | yes | yes |
| Vision Master E290 | 2.9″ e-ink | no | yes | yes | yes | yes |
| Wireless Tracker | 0.96″ TFT | yes | yes | yes | yes | yes |
| Wireless Tracker v2° | 0.96″ TFT | yes | yes | yes | yes | yes |
| Wireless Stick Lite v3 | none | no | yes | yes | yes | yes |
| Nano° | none | no | yes | no | yes | yes |
| Stick° | SSD1306 OLED (option) | no | yes | no | yes | yes |
| LT1° | 1.3″ display | yes | yes | no | yes | yes |
| LoRa32 v2.1_1.6 | 0.96″ OLED | no | yes | yes | yes | yes |
| T-Beam (SX1262) | 0.96″ OLED | yes | yes | yes | yes | yes |
| T-Beam 1.2 (SX1276) | 0.96″ OLED | yes | yes | yes | yes | yes |
| T-Beam 1W° | 0.96″ OLED | yes | yes | yes | yes | yes |
| T-Beam Supreme | 0.96″ OLED | yes | yes | yes | yes | yes |
| T-Deck | 2.8″ IPS touch + QWERTY | option | no (standalone) | yes | yes | yes |
| T-Deck Max° | large IPS touch + QWERTY | yes | no (standalone) | yes | yes | yes |
| T-Deck Pro° | 3.1″ e-ink touch + QWERTY | yes | no (standalone) | yes | yes | yes |
| T-Display Pro° | IPS touch | no | no (standalone) | yes | yes | yes |
| T-Echo | 1.54″ e-ink | yes | yes | no | yes | yes |
| T-Echo Card° | e-ink | yes | yes | no | yes | yes |
| T-Echo Lite° | e-ink | option | yes | no | yes | yes |
| T-Lora Pager° | 2.33″ IPS + QWERTY | yes | no (standalone) | yes | yes | yes |
| T-Watch S3 Plus | 1.54″ touch | no | no (standalone) | yes | yes | yes |
| T-Watch Ultra° | AMOLED touch | no | no (standalone) | yes | yes | yes |
| T3 S3 (SX126x) | 0.96″ OLED | no | yes | yes | yes | yes |
| T3 S3 (SX127x) | 0.96″ OLED | no | yes | yes | yes | yes |
| T5 E-Paper S3 Pro° | 4.7″ e-paper touch | no | no (standalone) | yes | yes | yes |
| R1 Neo | none | no | yes | no | yes | yes |
| ProMicro nRF52 (faketec)° | OLED (option) | option | yes | no | yes | yes |
| WisBlock / WisMesh RAK4631 | OLED (option) | option | yes | no | yes | yes |
| WisBlock 3112 | none | no | yes | yes | yes | yes |
| WisMesh 1W Booster | none | no | no (repeater) | no | yes | yes |
| WisMesh Tag° | none | yes | yes | no | yes | yes |
| Pico 2040 + WaveShare SX1262° | none | no | yes (over USB) | option | option | yes |
| SenseCAP Solar | none | yes | no (repeater) | no | yes | yes |
| SenseCAP T1000-E | none | yes | yes | no | yes | yes |
| Wio Tracker L1 EINK° | e-ink | yes | yes | no | yes | yes |
| Wio Tracker L1 Pro° | 1.3″ LCD | yes | yes | no | yes | yes |
| Xiao C3 | none | no | yes | yes | yes | yes |
| Xiao nRF52 WIO | none | no | yes | no | yes | yes |
| Xiao S3 WIO | none | no | yes | yes | yes | yes |
| Nano G2 Ultra | 1.3″ OLED | yes | yes | no | yes | yes |
| Station G2 | none | no | no (repeater) | yes | yes | yes |
| Voyage Station G3° | none | no | no (repeater) | yes | yes | yes |

## Table 4 — power, enclosure and price

Battery and enclosure are the weakest columns of this matrix.
Manufacturers change them per revision and many sources say nothing about
them; see [About the figures](#about-the-figures).

| Node | Battery | Enclosure | Price |
|---|---|---|---|
| ThinkNode M1 | 1200 mAh internal | plastic, optional case | €38–55 |
| ThinkNode M2 | 1000 mAh internal | plastic, optional case | €22–42 |
| ThinkNode M3° | internal, small | weatherproof, lanyard eyelet | €38–42 |
| ThinkNode M5 | 1200 mAh internal | plastic, optional case | €48–58 |
| ThinkNode M6 | 7000 mAh + 6 W solar | IP65 outdoor enclosure | €70–82 |
| GAT562 30s | external | bare board, case optional | €65–75 |
| GAT562 Tracker° | internal | bare board, case optional | €60–88 |
| Wireless Paper | external (JST) | bare board | €20–25 |
| Mesh Node T096 | external (JST) | bare board | €30–40 |
| Mesh Node T1° | internal | plastic enclosure | €35–50 |
| MeshPocket° | 6000 mAh power bank | plastic, Qi2 magnet | €45–55 |
| MeshSolar / MeshTower | 3× 18650 + 10 W solar | outdoor enclosure, weatherproof | €95–120 |
| T114 | external (JST) | bare board, case optional | €25–45 |
| WiFi LoRa 32 v2 | external (JST) | bare board | €14–24 |
| WiFi LoRa 32 v3 | external (JST) | bare board | €16–32 |
| WiFi LoRa 32 v4° | external (JST) | bare board | €16–28 |
| v4 + Expansion Kit (Touch)° | external (JST) | bare board + touch module | €35–55 |
| Vision Master E213 | external (JST) | bare board | €17–28 |
| Vision Master E290 | external (JST) | bare board | €27–37 |
| Wireless Tracker | external (JST) | bare board | €21–31 |
| Wireless Tracker v2° | external (JST) | bare board | €25–35 |
| Wireless Stick Lite v3 | external (JST) | bare board | €13–30 |
| Nano° | external (LiPo) | DIY, no case | €23–37 |
| Stick° | external (LiPo) | DIY, no case | €32–50 |
| LT1° | internal | plastic enclosure | €45–55 |
| LoRa32 v2.1_1.6 | external (JST) | bare board | €18–28 |
| T-Beam (SX1262) | 18650 holder | bare board | €28–38 |
| T-Beam 1.2 (SX1276) | 18650 holder | bare board | €28–34 |
| T-Beam 1W° | 18650 holder | bare board | €45–60 |
| T-Beam Supreme | 18650 holder | bare board | €44–62 |
| T-Deck | 2000 mAh (Plus) | plastic, metal on the Plus | €40–90 |
| T-Deck Max° | internal | plastic/metal | €95–130 |
| T-Deck Pro° | internal | plastic enclosure | €75–90 |
| T-Display Pro° | internal | plastic enclosure | €45–65 |
| T-Echo | 850 mAh internal | plastic enclosure | €50–62 |
| T-Echo Card° | internal | card-format enclosure | €55–70 |
| T-Echo Lite° | internal | plastic enclosure | €40–55 |
| T-Lora Pager° | internal (18650) | plastic enclosure | €80–105 |
| T-Watch S3 Plus | approx. 300 mAh internal | watch case | €55–70 |
| T-Watch Ultra° | internal | watch case | €85–110 |
| T3 S3 (SX126x) | external (JST) | bare board | €22–28 |
| T3 S3 (SX127x) | external (JST) | bare board | €20–26 |
| T5 E-Paper S3 Pro° | internal | plastic enclosure | €75–100 |
| R1 Neo | internal | weatherproof, SMA | €80–90 |
| ProMicro nRF52 (faketec)° | external | DIY, no case | €12–25 |
| WisBlock / WisMesh RAK4631 | external (JST) | bare board, case optional | €26–38 |
| WisBlock 3112 | external (JST) | bare board | €25–40 |
| WisMesh 1W Booster | external | bare board | €35–50 |
| WisMesh Tag° | internal | waterproof, card format | €27–45 |
| Pico 2040 + WaveShare SX1262° | via USB | DIY, no case | €12–25 |
| SenseCAP Solar | internal + 5 W solar | IPX5 outdoor enclosure | €70–130 |
| SenseCAP T1000-E | 700 mAh internal | IP65 card format | €32–42 |
| Wio Tracker L1 EINK° | external | bare board | €28–38 |
| Wio Tracker L1 Pro° | internal | plastic enclosure | €37–45 |
| Xiao C3 | external | bare board | €10–18 |
| Xiao nRF52 WIO | external | bare board | €12–19 |
| Xiao S3 WIO | external | bare board | €10–19 |
| Nano G2 Ultra | internal, approx. 3.5 days | plastic enclosure | €80–95 |
| Station G2 | USB-PD powered | plastic enclosure | €100–115 |
| Voyage Station G3° | USB-PD powered | plastic enclosure | €110–140 |

## Quick filters

Six cross-sections through the same sixty devices.

**With GPS (32)** — including devices where GPS is optional or
depends on the version.

ThinkNode M1 · ThinkNode M3 · ThinkNode M5 · ThinkNode M6 · GAT562 30s ·
GAT562 Tracker · Mesh Node T096 · Mesh Node T1 · MeshSolar / MeshTower ·
T114 · Wireless Tracker · Wireless Tracker v2 · LT1 · T-Beam (SX1262) ·
T-Beam 1.2 (SX1276) · T-Beam 1W · T-Beam Supreme · T-Deck · T-Deck Max ·
T-Deck Pro · T-Echo · T-Echo Card · T-Echo Lite · T-Lora Pager ·
ProMicro nRF52 (faketec) · WisBlock / WisMesh RAK4631 · WisMesh Tag ·
SenseCAP Solar · SenseCAP T1000-E · Wio Tracker L1 EINK · Wio Tracker L1 Pro ·
Nano G2 Ultra

**With a display (42)** — including optional display modules.
The MeshPocket does not count here: it only has an LED.

ThinkNode M1 · ThinkNode M2 · ThinkNode M5 · GAT562 30s · GAT562 Tracker ·
Wireless Paper · Mesh Node T096 · Mesh Node T1 · T114 · WiFi LoRa 32 v2 ·
WiFi LoRa 32 v3 · WiFi LoRa 32 v4 · v4 + Expansion Kit (Touch) ·
Vision Master E213 · Vision Master E290 · Wireless Tracker ·
Wireless Tracker v2 · Stick · LT1 · LoRa32 v2.1_1.6 · T-Beam (SX1262) ·
T-Beam 1.2 (SX1276) · T-Beam 1W · T-Beam Supreme · T-Deck · T-Deck Max ·
T-Deck Pro · T-Display Pro · T-Echo · T-Echo Card · T-Echo Lite ·
T-Lora Pager · T-Watch S3 Plus · T-Watch Ultra · T3 S3 (SX126x) ·
T3 S3 (SX127x) · T5 E-Paper S3 Pro · ProMicro nRF52 (faketec) ·
WisBlock / WisMesh RAK4631 · Wio Tracker L1 EINK · Wio Tracker L1 Pro ·
Nano G2 Ultra

**Works without a phone app (14)** — standalone boards,
repeaters and room servers.

MeshSolar / MeshTower · v4 + Expansion Kit (Touch) · T-Deck · T-Deck Max ·
T-Deck Pro · T-Display Pro · T-Lora Pager · T-Watch S3 Plus · T-Watch Ultra ·
T5 E-Paper S3 Pro · WisMesh 1W Booster · SenseCAP Solar · Station G2 ·
Voyage Station G3

**With WiFi (32)** — all ESP32; the Pico W drops out because
MeshCore does not build WiFi for it.

ThinkNode M2 · ThinkNode M5 · Wireless Paper · WiFi LoRa 32 v2 ·
WiFi LoRa 32 v3 · WiFi LoRa 32 v4 · v4 + Expansion Kit (Touch) ·
Vision Master E213 · Vision Master E290 · Wireless Tracker ·
Wireless Tracker v2 · Wireless Stick Lite v3 · LoRa32 v2.1_1.6 ·
T-Beam (SX1262) · T-Beam 1.2 (SX1276) · T-Beam 1W · T-Beam Supreme · T-Deck ·
T-Deck Max · T-Deck Pro · T-Display Pro · T-Lora Pager · T-Watch S3 Plus ·
T-Watch Ultra · T3 S3 (SX126x) · T3 S3 (SX127x) · T5 E-Paper S3 Pro ·
WisBlock 3112 · Xiao C3 · Xiao S3 WIO · Station G2 · Voyage Station G3

**28 dBm or more (8)** — read the warning at table 2 first.

GAT562 30s · Mesh Node T096 · MeshSolar / MeshTower · Stick · T-Beam 1W ·
WisMesh 1W Booster · Station G2 · Voyage Station G3

**With an onboard battery (31)** — a cell or holder on the
board, not a bare JST connector.

ThinkNode M1 · ThinkNode M2 · ThinkNode M3 · ThinkNode M5 · ThinkNode M6 ·
GAT562 Tracker · Mesh Node T1 · MeshPocket · MeshSolar / MeshTower · LT1 ·
T-Beam (SX1262) · T-Beam 1.2 (SX1276) · T-Beam 1W · T-Beam Supreme · T-Deck ·
T-Deck Max · T-Deck Pro · T-Display Pro · T-Echo · T-Echo Card · T-Echo Lite ·
T-Lora Pager · T-Watch S3 Plus · T-Watch Ultra · T5 E-Paper S3 Pro · R1 Neo ·
WisMesh Tag · SenseCAP Solar · SenseCAP T1000-E · Wio Tracker L1 Pro ·
Nano G2 Ultra

## To be confirmed

Twenty-five devices carry a `°`. What is unconfirmed per device is listed
below, in the wording of the source.

- **ThinkNode M3** — Tracker; GNSS via the LR1110, no display — to be
  confirmed · battery capacity and TX unconfirmed
- **GAT562 Tracker** — battery capacity unconfirmed
- **Mesh Node T1** — New model — display size and GPS variant to be confirmed
  · TX and battery unconfirmed
- **MeshPocket** — TX unconfirmed
- **WiFi LoRa 32 v4** — exact TX power of the PA unconfirmed
- **v4 + Expansion Kit (Touch)** — Standalone role depends on the firmware
  build · TX unconfirmed
- **Wireless Tracker v2** — Revised version — specifications to be confirmed
- **Nano** — TX depends on the E22 module
- **Stick** — 30 dBm with the E22-900M30S, 33 dBm with the M33S
- **LT1** — battery capacity unconfirmed
- **T-Beam 1W** — Price varies widely per seller
- **T-Deck Max** — New model — display size and GPS to be confirmed · TX and
  battery unconfirmed
- **T-Deck Pro** — battery capacity unconfirmed
- **T-Display Pro** — The flasher marks this board as ESP-NOW, not LoRa · no
  LoRa radio; ESP-NOW works on 2.4 GHz
- **T-Echo Card** — Card format — display size to be confirmed · battery
  capacity unconfirmed
- **T-Echo Lite** — GPS depends on the version · GPS and battery vary per
  version
- **T-Lora Pager** — battery type varies per version
- **T-Watch Ultra** — New model — GPS and display size to be confirmed · TX,
  GPS and battery unconfirmed
- **T5 E-Paper S3 Pro** — Radio module and GPS differ per version · radio
  module, GPS and battery vary per version
- **ProMicro nRF52 (faketec)** — TX depends on the radio module chosen (22-33
  dBm)
- **WisMesh Tag** — battery capacity unconfirmed
- **Pico 2040 + WaveShare SX1262** — WiFi/BLE only on the Pico W; the MeshCore
  link runs over USB · WiFi/BLE only on the Pico W; the link runs over USB
- **Wio Tracker L1 EINK** — Radio IC differs per revision — to be confirmed ·
  radio IC differs per revision
- **Wio Tracker L1 Pro** — Radio IC differs per revision — to be confirmed ·
  radio IC differs per revision
- **Voyage Station G3** — New model — power and equipment to be confirmed · TX
  and equipment unconfirmed

## About the figures

RAM, clock speed and link options follow from the SoC itself; those are
hard and can be looked up in the datasheets from Nordic, Espressif and
Raspberry Pi. Radio, display and GPS come from manufacturer and community
sources and were checked per board, though not in every case against a
primary manufacturer source.

Battery and enclosure are the least reliable. Manufacturers change them
per revision, sellers copy each other's specifications and many product
pages are silent about them. Where the source hesitates, there is a `°`.

Prices are indicative street prices in euros at European sellers,
excluding shipping and VAT, sampled in July 2026. They move faster than
the rest of this table.

Which concrete board suits which role is covered in
[Hardware Overview](../usage/hardware.md).

## Sources

This page has not been verified against the firmware. Every column comes
from outside
[meshcore-dev/MeshCore](https://github.com/meshcore-dev/MeshCore).

Device list: saved page of the
[MeshCore web flasher](https://flasher.meshcore.io), 27 July 2026, sixty
devices.

Not from the firmware repo:

- **RAM, clock speed, cores and link options** — datasheets from Nordic
  Semiconductor (nRF52840), Espressif (ESP32, ESP32-S3, ESP32-C3) and
  [Raspberry Pi](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)
  (RP2040)
- **Radio chip, TX power, display, GPS, battery and enclosure** — product
  pages from Elecrow, GAT-IoT, Heltec, Ikoka, Keepteen, LilyGo, Muzi
  Works, RAK, Seeed Studio and UnitEng, supplemented with community
  sources
- **Prices** — indicative street prices at European sellers, excluding
  shipping and VAT, July 2026

Related in this documentation:

- [MeshCore Platforms](platforms.md) — why the platform matters, and how
  these sixty devices divide across the four families
- [The Four Platform Families](platform-families.md) — what each family
  puts inside the chip
- [Hardware Overview](../usage/hardware.md) — four devices discussed at
  length
- [Regulations & Duty Cycle](../usage/regulations.md) — what you may
  actually transmit on 868 MHz

Translated from Dutch by Anthropic Claude
