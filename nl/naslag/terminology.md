# Terminologie

*NASLAGWERK · AFKORTINGEN · TECHNISCHE TERMEN*

Alfabetisch overzicht van alle technische termen en afkortingen in deze documentatie.

| Term | Betekenis |
|---|---|
| 18650 | Cilindrische lithium-ioncel van 18 bij 65 mm; op nodes als losse cel in een houder of vast ingebouwd |
| 70 cm-band | Amateur radioband 430–440 MHz, licentie vereist |
| 868 MHz | ISM-band frequentie voor Europa |
| ACK | Acknowledgement — bevestiging dat een bericht is ontvangen |
| Advert/Beacon | Periodiek signaal voor aanwezigheidsmelding en public key uitwisseling |
| AES | Advanced Encryption Standard — versleutelingsalgoritme (128/256-bit) |
| Arduino-core | Implementatie van de Arduino-API voor één chipfamilie. MeshCore gebruikt er vier: Arduino-ESP32, Adafruit nRF52, arduino-pico en STM32duino |
| ATT | Attribute Protocol — onderliggend protocol van GATT in BLE |
| BLE | Bluetooth Low Energy — energiezuinige verbinding tussen node en smartphone |
| bootloader | Klein programma dat als eerste start en de eigenlijke firmware laadt of vervangt; bepaalt hoe je een node kunt flashen |
| build flag | Compileeroptie in `platformio.ini` (`-D NAAM=waarde`) die bepaalt welke code wordt meegecompileerd |
| build target | Eén `[env:…]`-sectie in `platformio.ini`: de combinatie van bord, rol en instellingen die tot één firmwarebestand leidt. MeshCore telt er 507, plus `[env:native]` voor de tests |
| BW | Bandwidth — bandbreedte in kHz (125/250/500), smaller = robuuster |
| Callsign | Roepnaam — unieke identificatie voor radioamateurs (bijv. PE1HVH) |
| CCCD | Client Characteristic Configuration Descriptor — aan/uit schakelaar voor BLE Notify |
| Channel | Gedeelde cryptografische sleutel (PSK) voor groepscommunicatie |
| Chirp | Frequentiesweep van laag naar hoog (up-chirp) of hoog naar laag (down-chirp) |
| Companion App | Smartphone applicatie om de MeshCore node te bedienen |
| Cortex-M0+/M4/M4F | ARM-processorkernen. M0+ is de eenvoudigste, M4 heeft signaalverwerkingsinstructies, M4F daarbovenop een floating-point-eenheid |
| CR | Coding Rate — foutcorrectieniveau (4/5 tot 4/8), meer = betrouwbaarder |
| CSS | Chirp Spread Spectrum — de modulatiemethode die LoRa gebruikt |
| dBm | Decibel-milliwatt — eenheid voor zendvermogen (14 dBm = 25 mW) |
| Dechirp | Demodulatie door ontvangen chirp te vermenigvuldigen met lokale down-chirp |
| `depends=` | Regel in `library.properties` waarmee een library opgeeft welke andere libraries hij nodig heeft; PlatformIO haalt die automatisch op |
| Dest hash / Src hash | Eerste byte van de public key van ontvanger respectievelijk afzender, onversleuteld in het pakket |
| DFU | Device Firmware Update — firmware updaten zonder programmer. Op nRF52 via Bluetooth, op STM32 via USB |
| Direct routing | Routeren langs een vooraf bekend pad; alleen de repeaters die in het pad staan sturen door |
| DM | Direct Message — privébericht tussen twee nodes, end-to-end versleuteld |
| Duty Cycle | Percentage zendtijd dat is toegestaan (EU: max 1% op 868 MHz) |
| E2E | End-to-End encryptie — alleen zender en ontvanger kunnen berichten lezen |
| Eindtrap (PA) | Power Amplifier — versterkertrap achter de radiochip die het zendvermogen optrekt, bijvoorbeeld van 22 naar 30 dBm |
| e-ink | Elektronisch papier; houdt het beeld vast zonder stroom en is bij daglicht goed leesbaar, maar ververst traag |
| EIRP | Effective Isotropic Radiated Power — effectief uitgestraald vermogen incl. antenne |
| Encrypt-then-MAC | Eerst versleutelen, daarna de MAC over de cijfertekst berekenen |
| ERP | Effective Radiated Power — effectief uitgestraald vermogen inclusief antenne-winst |
| ESP-IDF | Espressif IoT Development Framework — de native SDK van Espressif waar de Arduino-ESP32-core bovenop draait |
| ESP-NOW | Verbindingsloos radioprotocol van Espressif tussen ESP32-chips onderling; in MeshCore alleen op ESP32 beschikbaar |
| ESP32 | Populaire microcontroller van Espressif met WiFi en Bluetooth |
| FFT | Fast Fourier Transform — algoritme voor frequentieanalyse van gedechirpt signaal |
| Firmware | Software die permanent op de microcontroller van een node draait |
| First packet wins | Bij meerdere kopieën van hetzelfde floodbericht wordt de eerst binnengekomene verwerkt; dat pad wordt geleerd, niet per se het kortste |
| Flood | Routeermodus waarbij elke repeater het pakket doorstuurt en zijn hash aan het pad toevoegt |
| Flashen | Firmware installeren of updaten op een apparaat |
| frameworklibrary | Library die meekomt met het frameworkpakket van een platform en dus geen auteursprefix en geen versienummer heeft: `SPI`, `Wire` en `SubGhz` |
| GATT | Generic Attribute Profile — structuur voor BLE data-uitwisseling |
| GODMODE | Bouwvlag `RADIOLIB_GODMODE=1` die alle `private`- en `protected`-leden van RadioLib publiek maakt; MeshCore gebruikt dat om rechtstreeks bij de modulelaag te kunnen |
| GPIO | General Purpose Input/Output — aansluitpinnen voor externe apparaten |
| GPS/GNSS | Global Navigation Satellite System — satellietnavigatie voor locatiebepaling |
| HAL | Hardware Abstraction Layer — laag die chipspecifieke registers verbergt achter een uniforme API |
| HAM | Amateur radio modus — licentie vereist, geen encryptie toegestaan |
| Hop | Eén sprong tussen twee nodes in het mesh-netwerk |
| I²C | Inter-Integrated Circuit — bus voor aansluiten van sensoren en displays |
| IPEX/U.FL | Kleine click-on antenneconnector voor interne antennes |
| ISM-band | Industrial, Scientific, Medical — vrije frequentieband, 868 MHz in Europa |
| Key Rotation | Periodiek vervangen van cryptografische sleutels voor extra veiligheid |
| `lib_deps` | Sleutel in `platformio.ini` waarmee een sectie opgeeft welke libraries hij nodig heeft |
| Library Dependency Finder (LDF) | Onderdeel van PlatformIO dat de broncode op `#include`-regels scant en daar libraries bij zoekt, ook als die niet gedeclareerd zijn |
| `library.json` | Metadatabestand van een PlatformIO-library; de sleutel `"dependencies"` speelt dezelfde rol als `depends=` |
| `library.properties` | Metadatabestand van een Arduino-library, met naam, versie, auteur en de regel `depends=` |
| Link Budget | Totaal signaalverlies dat een verbinding kan verdragen en nog decodeerbaar is |
| LittleFS | Compact filesystem voor microcontrollers, bestand tegen stroomuitval; gebruikt op nRF52, RP2040 en STM32WL |
| LoRa | Long Range — gepatenteerde modulatietechniek voor langeafstandscommunicatie |
| LPCOMP | Low-Power Comparator in de nRF52 — kan de chip uit `SYSTEMOFF` wekken op een spanningsverandering |
| LPP | Low Power Payload — compact binair formaat voor sensordata; MeshCore gebruikt CayenneLPP als draadformaat voor telemetrie |
| LR1110 | Semtech-transceiver die LoRa combineert met GNSS- en WiFi-scanning voor locatiebepaling zonder losse GPS-module |
| MAC (cipher) | Message Authentication Code — HMAC-SHA256 over de cijfertekst, afgekapt op 2 bytes. MeshCore gebruikt de term MIC niet |
| MCU | Microcontroller Unit — de centrale processor van een node |
| Mesh | Netwerk waarbij elk apparaat berichten kan doorsturen naar anderen |
| Meshtastic | Alternatieve LoRa mesh firmware — niet compatibel met MeshCore |
| MIT-licentie | Open-source licentie voor vrij gebruik, aanpassen en distributie |
| Node | Een apparaat/knooppunt in het MeshCore netwerk |
| Node-hash | Verkorte aanduiding van een node in paden en pakketten: de eerste byte van zijn public key (in ruimere padmodi 2 of 3 bytes). Er is geen 4-byte Node-ID |
| nRF52840 | Nordic microcontroller met ultra-laag stroomverbruik en Bluetooth |
| NUS | Nordic UART Service — BLE service die seriële poort simuleert |
| OTA | Over-The-Air — draadloze firmware update |
| out_path | Het geleerde pad naar een contact, bewaard in de contactenlijst. `0xFF` (`OUT_PATH_UNKNOWN`) betekent: nog geen pad bekend |
| Path | Rij node-hashes in een pakket: bij flood het afgelegde pad, bij direct de te volgen route |
| PATH-pakket | Payloadtype `0x08`; meldt het afgelegde pad terug aan de afzender. In de FAQ "delivery report" genoemd |
| Payload type | 4 bits in de header die bepalen wat er in de payload staat (`0x00`-`0x0F`) |
| PHY | Physical Layer — de fysieke radiolaag die bits omzet naar radiosignalen |
| Platform | In MeshCore: een van de vier bouwdoelen `ESP32_PLATFORM`, `NRF52_PLATFORM`, `RP2040_PLATFORM` en `STM32_PLATFORM`. Niet hetzelfde als een bord of een chip |
| Platformfamilie | Verzameling SoC's die dezelfde platformbase in `platformio.ini` delen, bijvoorbeeld ESP32, S3, C3 en C6 onder `[esp32_base]` |
| PlatformIO environment | Eén `[env:]`-blok in een `platformio.ini`: de combinatie van bord, rol en build flags die samen één firmwarebestand oplevert |
| Preamble | Reeks identieke chirps aan het begin van elk packet voor synchronisatie |
| Private Key | Privésleutel — geheim gehouden, voor ontsleutelen van berichten |
| Processing Gain | Signaalversterking door spreiding over vele samples (SF12: ~36 dB) |
| PSK | Pre-Shared Key — vooraf gedeelde cryptografische sleutel voor channels |
| PSRAM | Pseudo-static RAM — extern geheugen naast het interne RAM, op sommige ESP32-borden tot 8 MB |
| Public Key | Publieke sleutel — vrij deelbaar, voor versleutelen van berichten |
| Regio | Benoemd gebied waarbinnen een repeater flood-verkeer doorlaat. De naam levert een sleutel; wat er over de lucht gaat is een 16-bits transport code |
| registry | Pakketindex van PlatformIO waaruit libraries op naam en versie worden opgehaald |
| Repeater | Node die berichten doorgeeft om het netwerkbereik te vergroten |
| RISC-V | Open processorarchitectuur; gebruikt in de ESP32-C3 en C6, tegenover Xtensa in de klassieke ESP32 en de S3 |
| Room Server | Fysieke node met BBS-functie voor store-and-forward (tot 32 berichten) |
| Routing | Het bepalen van de beste route voor een bericht door het netwerk |
| RP2040 | Microcontroller van Raspberry Pi met twee Cortex-M0+-kernen; de enige MeshCore-chip zonder ingebouwde radio |
| Scope | De regio die een afzender aan een pakket meegeeft, als `transport_codes[0]` in de header |
| semver-caret (`^`) | Versieaanduiding `^7.6.0`: minimaal 7.6.0, maar onder de volgende hoofdversie. `~2.0.6` is nauwer: onder 2.1.0 |
| transitieve afhankelijkheid | Library die niet zelf gedeclareerd is maar meekomt omdat een andere library hem nodig heeft |
| Transport code | De 16 bits in `transport_codes[0]`. **Geen identificatie van een regio** maar een HMAC over payload type en payload, gezet met de regiosleutel. Verandert bij elk bericht; een repeater herkent hem door hem zelf te herberekenen, niet door hem op te zoeken |
| Regiocode | In de context van UN/LOCODE (zie [Regio's: bedoeling en praktijk](../techniek/regions-in-practice.md)): de *naam* van een regio, zoals `nl-ov-zwo`. Blijft op de node en gaat nooit de lucht in. Niet te verwarren met de transport code |
| SF | Spreading Factor — bepaalt bereik vs snelheid (SF7–SF12), hoger = verder |
| SIG | Special Interest Group — organisatie achter Bluetooth standaarden |
| SMA | SubMiniature version A — schroefbare antenneconnector |
| SNR | Signal-to-Noise Ratio — verhouding tussen signaal en ruis in dB |
| SoC | System on Chip — chip die processor, geheugen en vaak ook een radio combineert. ESP32, nRF52840 en STM32WLE5 zijn SoC's, de RP2040 is dat niet |
| SoftDevice | Voorgecompileerde Bluetooth-stack van Nordic die naast de applicatie in de flash van een nRF52 staat |
| SPI | Serial Peripheral Interface — snelle bus voor LoRa chip en SD-kaart |
| SPIFFS | Eenvoudig filesystem voor flashgeheugen; op ESP32 gebruikt voor identiteit en contacten |
| Standalone | Firmwarerol voor een node met eigen scherm en toetsenbord, die zonder companion-app werkt |
| ST-Link | Programmeer- en debugadapter van STMicroelectronics; de gebruikelijke manier om een STM32WL te flashen |
| STM32WLE5 | SoC van STMicroelectronics met een Cortex-M4 en de LoRa-radio (SubGHz) op dezelfde die |
| Store-and-forward | Berichten opslaan totdat de ontvanger bereikbaar is |
| SubGHz-radio | De radio-eenheid binnen de STM32WL; functioneel gelijk aan een SX126x maar zonder SPI-bus ertussen |
| SX1262 | Semtech LoRa radiochip — nieuwere, efficiëntere versie |
| SX1276 | Semtech LoRa radiochip — oudere maar nog steeds gebruikte versie |
| Sync Word | Netwerk identifier (2 bytes) om verschillende netwerken te scheiden |
| SYSTEMOFF | Diepste slaapstand van de nRF52; vrijwel alles uit, wakker worden alleen via specifieke pinnen of LPCOMP |
| Telemetry | Meetgegevens van sensoren die via het netwerk worden verstuurd |
| UART | Universal Asynchronous Receiver-Transmitter — seriële communicatie interface |
| UF2 | USB Flashing Format — firmwarebestand dat je naar een USB-schijf sleept; gebruikt door nRF52 en RP2040 |
| UUID | Universally Unique Identifier — unieke identificatie voor BLE services |
| Variant | Map onder `variants/` met de bord-specifieke configuratie: pinnen, radiotype, display en de bijbehorende build-targets |
| vendoring | Het opnemen van externe code als kopie in de eigen repo, in plaats van hem als afhankelijkheid op te halen. MeshCore doet dat in `lib/` en `arch/` |
| Web Flasher | Browser-tool om firmware te installeren zonder speciale software |
| Wrap | Frequentie springt terug naar begin van de band (0) na bereiken van maximum |
| Xtensa | Processorarchitectuur van Cadence; LX6 in de klassieke ESP32, LX7 in de ESP32-S3 |
| Zero-hop | Direct routeren met een leeg pad: alleen directe buren horen het, niemand stuurt het door |
