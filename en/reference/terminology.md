# Terminology

*REFERENCE · ABBREVIATIONS · TECHNICAL TERMS*

Alphabetical overview of all technical terms and abbreviations used in this documentation.

| Term | Meaning |
|---|---|
| 70 cm band | Amateur radio band 430–440 MHz, licence required |
| 868 MHz | ISM band frequency for Europe |
| ACK | Acknowledgement — confirmation that a message has been received |
| Advert/Beacon | Periodic signal for presence announcement and public key exchange |
| AES | Advanced Encryption Standard — encryption algorithm (128/256-bit) |
| ATT | Attribute Protocol — underlying protocol of GATT in BLE |
| BLE | Bluetooth Low Energy — energy-efficient connection between node and smartphone |
| BW | Bandwidth — bandwidth in kHz (125/250/500), narrower = more robust |
| Callsign | Call sign — unique identification for radio amateurs (e.g. PE1HVH) |
| CCCD | Client Characteristic Configuration Descriptor — on/off switch for BLE Notify |
| Channel | Shared cryptographic key (PSK) for group communication |
| Chirp | Frequency sweep from low to high (up-chirp) or high to low (down-chirp) |
| Companion App | Smartphone application to control the MeshCore node |
| CR | Coding Rate — error correction level (4/5 to 4/8), more = more reliable |
| CSS | Chirp Spread Spectrum — the modulation method LoRa uses |
| dBm | Decibel-milliwatt — unit for transmit power (14 dBm = 25 mW) |
| Dechirp | Demodulation by multiplying received chirp with local down-chirp |
| DFU | Device Firmware Update — update firmware via Bluetooth |
| DM | Direct Message — private message between two nodes, end-to-end encrypted |
| Duty Cycle | Percentage of transmit time allowed (EU: max 1% on 868 MHz) |
| E2E | End-to-End encryption — only sender and receiver can read messages |
| EIRP | Effective Isotropic Radiated Power — effective radiated power including antenna |
| ERP | Effective Radiated Power — effective radiated power including antenna gain |
| ESP32 | Popular microcontroller from Espressif with WiFi and Bluetooth |
| FFT | Fast Fourier Transform — algorithm for frequency analysis of dechirped signal |
| Firmware | Software permanently running on the microcontroller of a node |
| Flood | Routing mode in which every repeater forwards the packet and appends its hash to the path |
| Flashing | Installing or updating firmware on a device |
| GATT | Generic Attribute Profile — structure for BLE data exchange |
| GPIO | General Purpose Input/Output — connection pins for external devices |
| GPS/GNSS | Global Navigation Satellite System — satellite navigation for location |
| HAM | Amateur radio mode — licence required, no encryption permitted |
| Hop | One jump between two nodes in the mesh network |
| I²C | Inter-Integrated Circuit — bus for connecting sensors and displays |
| IPEX/U.FL | Small click-on antenna connector for internal antennas |
| ISM band | Industrial, Scientific, Medical — free frequency band, 868 MHz in Europe |
| Key Rotation | Periodic replacement of cryptographic keys for extra security |
| Link Budget | Total signal loss a connection can sustain and still be decodable |
| LoRa | Long Range — patented modulation technique for long-range communication |
| MAC (cipher) | Message Authentication Code — HMAC-SHA256 over the ciphertext, truncated to 2 bytes. MeshCore does not use the term MIC |
| MCU | Microcontroller Unit — the central processor of a node |
| Mesh | Network where every device can forward messages to others |
| Meshtastic | Alternative LoRa mesh firmware — not compatible with MeshCore |
| MIT licence | Open-source licence for free use, modification and distribution |
| Node | A device/node in the MeshCore network |
| Node hash | Short form of a node in paths and packets: the first byte of its public key (2 or 3 bytes in the wider path modes). There is no 4-byte Node-ID |
| nRF52840 | Nordic microcontroller with ultra-low power consumption and Bluetooth |
| NUS | Nordic UART Service — BLE service that simulates a serial port |
| OTA | Over-The-Air — wireless firmware update |
| Path | Sequence of node hashes in a packet: the route travelled for flood, the route to follow for direct |
| Payload type | 4 bits in the header determining what the payload contains (`0x00`-`0x0F`) |
| PHY | Physical Layer — the physical radio layer that converts bits to radio signals |
| Preamble | Series of identical chirps at the start of each packet for synchronisation |
| Private Key | Secret key — kept private, used to decrypt messages |
| Processing Gain | Signal amplification from spreading over many samples (SF12: ~36 dB) |
| PSK | Pre-Shared Key — pre-shared cryptographic key for channels |
| Public Key | Public key — freely shareable, used to encrypt messages |
| Region | Named area within which a repeater passes flood traffic. The name yields a key; what travels over the air is a 16-bit transport code |
| Repeater | Node that forwards messages to extend network range |
| Room Server | Physical node with BBS function for store-and-forward (up to 32 messages) |
| Routing | Determining the best route for a message through the network |
| Scope | The region a sender attaches to a packet, as `transport_codes[0]` in the header |
| Transport code | The 16 bits in `transport_codes[0]`. **Not an identifier of a region** but an HMAC over payload type and payload, keyed with the region key. It changes with every message; a repeater recognises it by recomputing it, not by looking it up |
| Region code | In the [UN/LOCODE](../technical/techniek-locode.md) sense: the *name* of a region, such as `nl-ov-zwo`. It stays on the node and never goes on air. Not to be confused with the transport code |
| SF | Spreading Factor — determines range vs speed (SF7–SF12), higher = further |
| SIG | Special Interest Group — organisation behind Bluetooth standards |
| SMA | SubMiniature version A — threaded antenna connector |
| SNR | Signal-to-Noise Ratio — ratio of signal to noise in dB |
| SPI | Serial Peripheral Interface — fast bus for LoRa chip and SD card |
| Store-and-forward | Storing messages until the recipient is reachable |
| SX1262 | Semtech LoRa radio chip — newer, more efficient version |
| SX1276 | Semtech LoRa radio chip — older but still widely used version |
| Sync Word | Network identifier (2 bytes) to separate different networks |
| Telemetry | Measurement data from sensors transmitted via the network |
| UART | Universal Asynchronous Receiver-Transmitter — serial communication interface |
| UUID | Universally Unique Identifier — unique identification for BLE services |
| Web Flasher | Browser tool to install firmware without special software |
| Wrap | Frequency jumps back to the start of the band (0) after reaching the maximum |

Translated from Dutch by Anthropic Claude
