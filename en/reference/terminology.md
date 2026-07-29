# Terminology

*REFERENCE · ABBREVIATIONS · TECHNICAL TERMS*

Alphabetical overview of all technical terms and abbreviations used in this documentation.

| Term | Meaning |
|---|---|
| 18650 | Cylindrical lithium-ion cell of 18 by 65 mm; on nodes either a loose cell in a holder or built in |
| 70 cm band | Amateur radio band 430–440 MHz, licence required |
| 868 MHz | ISM band frequency for Europe |
| ACK | Acknowledgement — confirmation that a message has been received |
| Advert/Beacon | Periodic signal for presence announcement and public key exchange |
| AES | Advanced Encryption Standard — encryption algorithm (128/256-bit) |
| Arduino core | Implementation of the Arduino API for one chip family. MeshCore uses four: Arduino-ESP32, Adafruit nRF52, arduino-pico and STM32duino |
| ATT | Attribute Protocol — underlying protocol of GATT in BLE |
| BLE | Bluetooth Low Energy — energy-efficient connection between node and smartphone |
| bootloader | Small program that runs first and loads or replaces the actual firmware; determines how a node can be flashed |
| build flag | Compile option in `platformio.ini` (`-D NAME=value`) that decides which code is compiled in |
| build target | One `[env:…]` section in `platformio.ini`: the combination of board, role and settings that yields one firmware file. MeshCore counts 507 of them, plus `[env:native]` for the tests |
| BUSY | Signal line from an SX126x radio to the SoC: active while the chip is processing a command. In MeshCore the build flag `P_LORA_BUSY` |
| BW | Bandwidth — bandwidth in kHz (125/250/500), narrower = more robust |
| Callsign | Call sign — unique identification for radio amateurs (e.g. PE1HVH) |
| CCCD | Client Characteristic Configuration Descriptor — on/off switch for BLE Notify |
| Channel | Shared cryptographic key (PSK) for group communication |
| Chirp | Frequency sweep from low to high (up-chirp) or high to low (down-chirp) |
| Companion App | Smartphone application to control the MeshCore node |
| Cortex-M0+/M4/M4F | ARM processor cores. M0+ is the simplest, M4 adds signal-processing instructions, M4F adds a floating-point unit on top |
| CP437 | The character set of the original IBM PC. MeshCore uses one character from it, the full block `0xDB`, as a replacement for every non-ASCII character on screen |
| CR | Coding Rate — error correction level (4/5 to 4/8), more = more reliable |
| CSS | Chirp Spread Spectrum — the modulation method LoRa uses |
| dBd | Antenna gain relative to a half-wave dipole. The regulations on 868 MHz count in this. `dBd = dBi − 2.15` |
| dBi | Antenna gain relative to an isotropic radiator — the imagined antenna radiating equally in every direction. Datasheets usually use this reference |
| dBm | Decibel-milliwatt — unit for transmit power (14 dBm = 25 mW) |
| debouncing | Suppressing the repeated switching a mechanical button causes on a single press |
| Dechirp | Demodulation by multiplying received chirp with local down-chirp |
| `depends=` | Line in `library.properties` by which a library states which other libraries it needs; PlatformIO fetches those automatically |
| Dest hash / Src hash | First byte of the public key of recipient and sender respectively, unencrypted in the packet |
| DFU | Device Firmware Update — updating firmware without a programmer. Over Bluetooth on nRF52, over USB on STM32 |
| Direct routing | Routing along a previously known path; only the repeaters listed in the path forward |
| DM | Direct Message — private message between two nodes, end-to-end encrypted |
| Duty Cycle | Percentage of transmit time allowed (EU: max 1% on 868 MHz) |
| E2E | End-to-End encryption — only sender and receiver can read messages |
| e-ink | Electronic paper; holds its image without power and reads well in daylight, but refreshes slowly |
| EIRP | Effective Isotropic Radiated Power — effective radiated power including antenna |
| Encrypt-then-MAC | Encrypt first, then compute the MAC over the ciphertext |
| e-paper | Display technology holding its image without power. Recognisable in MeshCore by `isEink()` and by a lower refresh rate |
| ERP | Effective Radiated Power — effective radiated power including antenna gain |
| ESP32 | Popular microcontroller from Espressif with WiFi and Bluetooth |
| ESP-IDF | Espressif IoT Development Framework — Espressif's native SDK, on which the Arduino-ESP32 core is built |
| ESP-NOW | Connectionless radio protocol from Espressif between ESP32 chips; in MeshCore available on ESP32 only |
| FFT | Fast Fourier Transform — algorithm for frequency analysis of dechirped signal |
| Firmware | Software permanently running on the microcontroller of a node |
| First packet wins | With multiple copies of the same flood message the first to arrive is processed; that path is learned, not necessarily the shortest |
| Flashing | Installing or updating firmware on a device |
| Flood | Routing mode in which every repeater forwards the packet and appends its hash to the path |
| framework library | Library shipped inside a platform's framework package, and therefore carrying no author prefix and no version number: `SPI`, `Wire` and `SubGhz` |
| FSPL | Free Space Path Loss — the loss over distance without obstacles. `20·log10(km) + 20·log10(MHz) + 32.44` |
| GATT | Generic Attribute Profile — structure for BLE data exchange |
| GNSS | Global Navigation Satellite System — collective name for GPS, Galileo, GLONASS and BeiDou together |
| GODMODE | Build flag `RADIOLIB_GODMODE=1` that makes all `private` and `protected` members of RadioLib public; MeshCore uses it to reach the module layer directly |
| GPIO | General Purpose Input/Output — connection pins for external devices |
| GPS/GNSS | Global Navigation Satellite System — satellite navigation for location |
| HAL | Hardware Abstraction Layer — layer that hides chip-specific registers behind a uniform API |
| HAM | Amateur radio mode — licence required, no encryption permitted |
| Hop | One jump between two nodes in the mesh network |
| I²C | Inter-Integrated Circuit — bus for connecting sensors and displays |
| IPEX/U.FL | Small click-on antenna connector for internal antennas |
| ISM band | Industrial, Scientific, Medical — free frequency band, 868 MHz in Europe |
| Key Rotation | Periodic replacement of cryptographic keys for extra security |
| `lib_deps` | Key in `platformio.ini` by which a section states which libraries it needs |
| Library Dependency Finder (LDF) | Part of PlatformIO that scans the source code for `#include` lines and looks for matching libraries, even undeclared ones |
| `library.json` | Metadata file of a PlatformIO library; the `"dependencies"` key plays the same role as `depends=` |
| `library.properties` | Metadata file of an Arduino library, holding name, version, author and the `depends=` line |
| Link Budget | Total signal loss a connection can sustain and still be decodable |
| LittleFS | Compact filesystem for microcontrollers, resilient to power loss; used on nRF52, RP2040 and STM32WL |
| LNA | Low Noise Amplifier — amplifier in the receive path, right behind the antenna |
| LoRa | Long Range — patented modulation technique for long-range communication |
| LPCOMP | Low-Power Comparator in the nRF52 — can wake the chip from `SYSTEMOFF` on a voltage change |
| LPP | Low Power Payload — compact binary format for sensor data; MeshCore uses CayenneLPP as the wire format for telemetry |
| LR1110 | Semtech transceiver combining LoRa with GNSS and WiFi scanning for positioning without a separate GPS module |
| MAC (cipher) | Message Authentication Code — HMAC-SHA256 over the ciphertext, truncated to 2 bytes. MeshCore does not use the term MIC |
| MCU | Microcontroller Unit — the central processor of a node |
| Mesh | Network where every device can forward messages to others |
| Meshtastic | Alternative LoRa mesh firmware — not compatible with MeshCore |
| MISO | Master In Slave Out — the SPI line the attached device sends data to the SoC on |
| MIT licence | Open-source licence for free use, modification and distribution |
| MOSI | Master Out Slave In — the SPI line the SoC sends data to the attached device on |
| NMEA | Line-based text format a GNSS receiver sends position, time and satellite count in. One sentence fits in the hundred-byte buffer |
| Node | A device/node in the MeshCore network |
| Node hash | Short form of a node in paths and packets: the first byte of its public key (2 or 3 bytes in the wider path modes). There is no 4-byte Node-ID |
| noise floor | The noise level a receiver has to listen through. MeshCore measures it itself over 64 samples and clamps it at −120 dBm |
| nRF52840 | Nordic microcontroller with ultra-low power consumption and Bluetooth |
| NSS | Chip select of the SPI bus: low while the SoC is addressing this one device. In MeshCore `P_LORA_NSS`; also called CS |
| NUS | Nordic UART Service — BLE service that simulates a serial port |
| OLED | Organic LED — the small self-illuminating screen on many nodes, usually an SSD1306 or SH1106 on the I²C bus |
| OTA | Over-The-Air — wireless firmware update |
| out_path | The learned path to a contact, kept in the contact list. `0xFF` (`OUT_PATH_UNKNOWN`) means no path is known yet |
| Path | Sequence of node hashes in a packet: the route travelled for flood, the route to follow for direct |
| PATH packet | Payload type `0x08`; reports the travelled path back to the sender. Called a "delivery report" in the FAQ |
| Payload type | 4 bits in the header determining what the payload contains (`0x00`-`0x0F`) |
| PHY | Physical Layer — the physical radio layer that converts bits to radio signals |
| Platform | In MeshCore: one of the four build targets `ESP32_PLATFORM`, `NRF52_PLATFORM`, `RP2040_PLATFORM` and `STM32_PLATFORM`. Not the same as a board or a chip |
| Platform family | Set of SoCs sharing the same platform base in `platformio.ini`, for example ESP32, S3, C3 and C6 under `[esp32_base]` |
| PlatformIO environment | One `[env:]` block in a `platformio.ini`: the combination of board, role and build flags that yields a single firmware file |
| Power amplifier (PA) | Amplifier stage behind the radio chip that raises the transmit power, for example from 22 to 30 dBm |
| Preamble | Series of identical chirps at the start of each packet for synchronisation |
| Private Key | Secret key — kept private, used to decrypt messages |
| Processing Gain | Signal amplification from spreading over many samples (SF12: ~36 dB) |
| PSK | Pre-Shared Key — pre-shared cryptographic key for channels |
| PSRAM | Pseudo-static RAM — external memory alongside the internal RAM, up to 8 MB on some ESP32 boards |
| Public Key | Public key — freely shareable, used to encrypt messages |
| Region | Named area within which a repeater passes flood traffic. The name yields a key; what travels over the air is a 16-bit transport code |
| Region code | In the UN/LOCODE sense (see [Regions: intent and practice](../technical/regions-in-practice.md)): the *name* of a region, such as `nl-ov-zwo`. It stays on the node and never goes on air. Not to be confused with the transport code |
| registry | PlatformIO's package index, from which libraries are fetched by name and version |
| Repeater | Node that forwards messages to extend network range |
| RISC-V | Open processor architecture; used in the ESP32-C3 and C6, as opposed to Xtensa in the classic ESP32 and the S3 |
| Room Server | Physical node with BBS function for store-and-forward (up to 32 messages) |
| Routing | Determining the best route for a message through the network |
| RP2040 | Microcontroller from Raspberry Pi with two Cortex-M0+ cores; the only MeshCore chip without a built-in radio |
| RSSI | Received Signal Strength Indicator — the received signal level in dBm. MeshCore samples it to determine its noise floor |
| RTTTL | Ring Tone Text Transfer Language — Nokia's ringtone format. MeshCore stores its startup and shutdown sound in it |
| SCL | Serial Clock — the clock line of the I²C bus (`PIN_BOARD_SCL`) |
| SCLK | Serial Clock — the clock line of the SPI bus (`P_LORA_SCLK`). Not to be confused with SCL, the clock line of I²C |
| Scope | The region a sender attaches to a packet, as `transport_codes[0]` in the header |
| SDA | Serial Data — the data line of the I²C bus (`PIN_BOARD_SDA`) |
| semver caret (`^`) | Version specification `^7.6.0`: at least 7.6.0, but below the next major version. `~2.0.6` is narrower: below 2.1.0 |
| SF | Spreading Factor — determines range vs speed (SF7–SF12), higher = further |
| SIG | Special Interest Group — organisation behind Bluetooth standards |
| SMA | SubMiniature version A — threaded antenna connector |
| SNR | Signal-to-Noise Ratio — ratio of signal to noise in dB |
| SoC | System on Chip — chip combining processor, memory and often a radio. The ESP32, nRF52840 and STM32WLE5 are SoCs, the RP2040 is not |
| SoftDevice | Precompiled Bluetooth stack from Nordic that sits alongside the application in an nRF52's flash |
| SPI | Serial Peripheral Interface — fast bus for LoRa chip and SD card |
| SPIFFS | Simple filesystem for flash memory; used on ESP32 for identity and contacts |
| Standalone | Firmware role for a node with its own display and keyboard, working without a companion app |
| ST-Link | Programming and debug adapter from STMicroelectronics; the usual way to flash an STM32WL |
| STM32WLE5 | SoC from STMicroelectronics with a Cortex-M4 and the LoRa radio (SubGHz) on the same die |
| Store-and-forward | Storing messages until the recipient is reachable |
| SubGHz radio | The radio unit inside the STM32WL; functionally equivalent to an SX126x but without an SPI bus in between |
| SWR | Standing Wave Ratio — the degree to which transmit power is reflected back by the antenna. 1:1 is perfect, infinite is a disconnected antenna |
| SX1262 | Semtech LoRa radio chip — newer, more efficient version |
| SX1276 | Semtech LoRa radio chip — older but still widely used version |
| Sync Word | Network identifier (2 bytes) to separate different networks |
| SYSTEMOFF | Deepest sleep mode of the nRF52; almost everything off, waking only through specific pins or LPCOMP |
| TCP | Transmission Control Protocol — connection-oriented transport layer. A node with a WiFi build opens a server on port 5000 with it |
| TCXO | Temperature Compensated Crystal Oscillator — clock source holding its frequency across temperature. On an SX126x it is fed by DIO3 |
| Telemetry | Measurement data from sensors transmitted via the network |
| transitive dependency | Library that is not declared itself but comes along because another library needs it |
| Transport code | The 16 bits in `transport_codes[0]`. **Not an identifier of a region** but an HMAC over payload type and payload, keyed with the region key. It changes with every message; a repeater recognises it by recomputing it, not by looking it up |
| TwoWire | Arduino class for one I²C bus. `Wire` is the first bus, `Wire1` the optional second one for telemetry sensors |
| UART | Universal Asynchronous Receiver-Transmitter — serial communication interface |
| UF2 | USB Flashing Format — firmware file you drag onto a USB drive; used by nRF52 and RP2040 |
| USB CDC-ACM | Communications Device Class / Abstract Control Model — the USB class a node uses to present itself to the operating system as a serial port |
| UUID | Universally Unique Identifier — unique identification for BLE services |
| Variant | Directory under `variants/` holding the board-specific configuration: pins, radio type, display and the matching build targets |
| vendoring | Including external code as a copy in your own repo instead of fetching it as a dependency. MeshCore does this in `lib/` and `arch/` |
| Web Flasher | Browser tool to install firmware without special software |
| Wrap | Frequency jumps back to the start of the band (0) after reaching the maximum |
| XBM | X BitMap — simple monochrome image format living as a C array in the firmware. `drawXbm()` puts it on the screen |
| Xtensa | Processor architecture from Cadence; LX6 in the classic ESP32, LX7 in the ESP32-S3 |
| Zero-hop | Direct routing with an empty path: only direct neighbours hear it, nobody forwards it |

Translated from Dutch by Anthropic Claude
