# References & Sources

*REFERENCE · DATASHEETS · PAPERS · DOCUMENTATION*

Comprehensive source list organised by category.

## Datasheets

| Title | Source | Description |
|---|---|---|
| [SX1276/77/78/79 Datasheet](https://cdn-shop.adafruit.com/product-files/3179/sx1276_77_78_79.pdf) | Semtech | Official datasheet for legacy SX127x LoRa transceivers with spreading factors and modulation specs |
| [SX1262 Product Page](https://www.semtech.com/products/wireless-rf/lora-connect/sx1262) | Semtech | Product information for the newer SX1262 LoRa transceiver |

## Application Notes

| Title | Source | Description |
|---|---|---|
| [AN1200.22 LoRa Modulation Basics](https://www.frugalprototype.com/wp-content/uploads/2016/08/an1200.22.pdf) | Semtech | Fundamental application note on Chirp Spread Spectrum modulation and processing gain |
| [AN1200.13 LoRa Modem Designer's Guide](https://www.openhacks.com/uploadsproductos/loradesignguide_std.pdf) | Semtech | Technical guide on SNR requirements and spread spectrum processing gain calculations |
| [RSSI and SNR for LoRa Modulation](https://www.st.com/resource/en/application_note/an5664-rssi-and-snr-for-lora-modulation-on-stm32wl-series-stmicroelectronics.pdf) | STMicroelectronics | Application note on processing gain calculation and detection of signals below the noise floor |

## Academic Papers

| Title | Source | Description |
|---|---|---|
| [From Demodulation to Decoding: Complete LoRa PHY](https://dl.acm.org/doi/10.1145/3546869) | ACM TOSN | In-depth analysis of the LoRa encoding pipeline, dechirping, and FFT peak detection |
| [Complete Reverse Engineering of LoRa PHY](https://www.epfl.ch/labs/tcl/wp-content/uploads/2020/02/Reverse_Eng_Report.pdf) | EPFL | Detailed reverse engineering report of the LoRa physical layer |
| [A Tutorial on CSS for LoRaWAN](https://arxiv.org/abs/2310.10503) | arXiv | Comprehensive academic tutorial on CSS modulation in LoRaWAN systems |
| [LoRaWAN Mesh Networks: A Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC7435450/) | PMC/MDPI | Extensive overview of multihop mechanisms and mesh topologies for LoRaWAN |
| [NELoRa: Ultra-low SNR LoRa Communication](https://cse.msu.edu/~caozc/papers/sensys21-li.pdf) | SenSys'21 | Research on dechirp signal concentration and SNR threshold analysis |
| [FTrack: Parallel Decoding for LoRa](https://www4.comp.polyu.edu.hk/~csyqzheng/papers/FTrack_Sensys19.pdf) | SenSys'19 | Paper on FFT peak detection in dechirped signals |
| [Design of a Baseband LoRa Demodulator](https://ieeexplore.ieee.org/document/8836176/) | IEEE | Paper on digital LoRa demodulator design with the de-chirp method and FFT |

## Educational Resources

| Title | Source | Description |
|---|---|---|
| [LoRa/CSS: Overview and Decoding](https://gyulab.github.io/lora/) | Gyujun Jeong | Comprehensive tutorial on CSS modulation, dechirping, and FFT-based symbol detection |
| [Understanding LoRa PHY](https://wirelesspi.com/understanding-lora-phy-long-range-physical-layer/) | Wireless Pi | Accessible explanation of LoRa physical layer concepts and de-chirping |
| [LoRa modem with LimeSDR](https://myriadrf.org/news/lora-modem-limesdr/) | MyriadRF | Practical guide on dechirping via conjugate chirp multiplication |
| [The Hidden Side of LoRa](https://www.disk91.com/2024/technology/lora/the-hidden-side-of-lora/) | disk91 | Explanation of the internal LoRa packet structure |
| [LoRa Link Budget Calculations](https://www.techplayon.com/lora-link-budget-sensitivity-calculations-example-explained/) | Techplayon | Practical explanation of spread spectrum processing gain and SNR requirements |

## Standards and Specifications

| Title | Source | Description |
|---|---|---|
| [Spreading Factors](https://www.thethingsnetwork.org/docs/lorawan/spreading-factors/) | TTN | Official documentation on spreading factors and receiver sensitivity |
| [ETSI EN 300 220](https://www.etsi.org/) | ETSI | European standard for short-range devices in the 868 MHz ISM band |
| [LoRa Alliance Regional Parameters](https://www.lora-alliance.org/) | LoRa Alliance | Official specifications for regional frequency plans (EU868, US915) |
| [LoRa (Wikipedia)](https://en.wikipedia.org/wiki/LoRa) | Wikipedia | Overview of cyclically shifted chirps, spreading factor selection (SF5–SF12) |

## MeshCore Documentation

| Title | Source | Description |
|---|---|---|
| [MeshCore Official Website](https://meshcore.co.uk/) | MeshCore | Official website with product information, downloads, and documentation |
| [MeshCore GitHub Repository](https://github.com/meshcore-dev/MeshCore) | GitHub | Open-source repository with MeshCore firmware and sample code |
| [MeshCore FAQ](https://github.com/meshcore-dev/MeshCore/wiki/FAQ) | GitHub Wiki | Frequently asked questions about advertising, frequencies, firmware, and licences |
| [MeshCore Web Flasher](https://flasher.meshcore.co.uk/) | MeshCore | Web-based firmware flash tool for supported devices |
| [MeshCore Companion Apps](https://meshcore.co.uk/apps.html) | MeshCore | Overview of available client applications for Android, iOS, and web |
| [MeshCore Discord Server](https://discord.gg/ZVH2ujy9ex) | Discord | Official community server for support and development discussion |
| [MeshCore Map](https://map.meshcore.dev/) | MeshCore | Live map with active MeshCore nodes, repeaters, and room servers |
| [MeshCore Dutch Forum](https://forum.meshcore-net.nl/) | Community | Dutch-language forum for MeshCore users |

## Hardware Documentation

| Title | Source | Description |
|---|---|---|
| [Heltec WiFi LoRa 32 V3](https://heltec.org/project/wifi-lora-32-v3/) | Heltec | Product page for Heltec V3 development board with ESP32-S3 and SX1262 |
| [Heltec WiFi LoRa 32 V4](https://heltec.org/project/wifi-lora-32-v4/) | Heltec | Product page for Heltec V4 with 28dBm transmit power |
| [RAKwireless WisBlock](https://store.rakwireless.com/) | RAKwireless | Modular IoT hardware system with RAK4631 (nRF52840 + SX1262) |
| [LilyGO T-Deck](https://www.lilygo.cc/) | LilyGO | Standalone MeshCore device with screen and keyboard |
| [Seeed Studio T1000-E](https://www.seeedstudio.com/) | Seeed Studio | Compact GPS tracker with nRF52840 and LoRa |

Translated from Dutch by Anthropic Claude
