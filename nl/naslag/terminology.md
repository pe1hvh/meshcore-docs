# Terminologie

*NASLAGWERK · AFKORTINGEN · TECHNISCHE TERMEN*

Alfabetisch overzicht van alle technische termen en afkortingen in deze documentatie.

| Term | Betekenis |
|---|---|
| 70 cm-band | Amateur radioband 430–440 MHz, licentie vereist |
| 868 MHz | ISM-band frequentie voor Europa |
| ACK | Acknowledgement — bevestiging dat een bericht is ontvangen |
| Advert/Beacon | Periodiek signaal voor aanwezigheidsmelding en public key uitwisseling |
| AES | Advanced Encryption Standard — versleutelingsalgoritme (128/256-bit) |
| ATT | Attribute Protocol — onderliggend protocol van GATT in BLE |
| BLE | Bluetooth Low Energy — energiezuinige verbinding tussen node en smartphone |
| BW | Bandwidth — bandbreedte in kHz (125/250/500), smaller = robuuster |
| Callsign | Roepnaam — unieke identificatie voor radioamateurs (bijv. PE1HVH) |
| CCCD | Client Characteristic Configuration Descriptor — aan/uit schakelaar voor BLE Notify |
| Channel | Gedeelde cryptografische sleutel (PSK) voor groepscommunicatie |
| Chirp | Frequentiesweep van laag naar hoog (up-chirp) of hoog naar laag (down-chirp) |
| Companion App | Smartphone applicatie om de MeshCore node te bedienen |
| CR | Coding Rate — foutcorrectieniveau (4/5 tot 4/8), meer = betrouwbaarder |
| CSS | Chirp Spread Spectrum — de modulatiemethode die LoRa gebruikt |
| dBm | Decibel-milliwatt — eenheid voor zendvermogen (14 dBm = 25 mW) |
| Dechirp | Demodulatie door ontvangen chirp te vermenigvuldigen met lokale down-chirp |
| DFU | Device Firmware Update — firmware updaten via Bluetooth |
| DM | Direct Message — privébericht tussen twee nodes, end-to-end versleuteld |
| Duty Cycle | Percentage zendtijd dat is toegestaan (EU: max 1% op 868 MHz) |
| E2E | End-to-End encryptie — alleen zender en ontvanger kunnen berichten lezen |
| EIRP | Effective Isotropic Radiated Power — effectief uitgestraald vermogen incl. antenne |
| ERP | Effective Radiated Power — effectief uitgestraald vermogen inclusief antenne-winst |
| ESP32 | Populaire microcontroller van Espressif met WiFi en Bluetooth |
| FFT | Fast Fourier Transform — algoritme voor frequentieanalyse van gedechirpt signaal |
| Firmware | Software die permanent op de microcontroller van een node draait |
| Flood | Routeermodus waarbij elke repeater het pakket doorstuurt en zijn hash aan het pad toevoegt |
| Flashen | Firmware installeren of updaten op een apparaat |
| GATT | Generic Attribute Profile — structuur voor BLE data-uitwisseling |
| GPIO | General Purpose Input/Output — aansluitpinnen voor externe apparaten |
| GPS/GNSS | Global Navigation Satellite System — satellietnavigatie voor locatiebepaling |
| HAM | Amateur radio modus — licentie vereist, geen encryptie toegestaan |
| Hop | Eén sprong tussen twee nodes in het mesh-netwerk |
| I²C | Inter-Integrated Circuit — bus voor aansluiten van sensoren en displays |
| IPEX/U.FL | Kleine click-on antenneconnector voor interne antennes |
| ISM-band | Industrial, Scientific, Medical — vrije frequentieband, 868 MHz in Europa |
| Key Rotation | Periodiek vervangen van cryptografische sleutels voor extra veiligheid |
| Link Budget | Totaal signaalverlies dat een verbinding kan verdragen en nog decodeerbaar is |
| LoRa | Long Range — gepatenteerde modulatietechniek voor langeafstandscommunicatie |
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
| Path | Rij node-hashes in een pakket: bij flood het afgelegde pad, bij direct de te volgen route |
| Payload type | 4 bits in de header die bepalen wat er in de payload staat (`0x00`-`0x0F`) |
| PHY | Physical Layer — de fysieke radiolaag die bits omzet naar radiosignalen |
| Preamble | Reeks identieke chirps aan het begin van elk packet voor synchronisatie |
| Private Key | Privésleutel — geheim gehouden, voor ontsleutelen van berichten |
| Processing Gain | Signaalversterking door spreiding over vele samples (SF12: ~36 dB) |
| PSK | Pre-Shared Key — vooraf gedeelde cryptografische sleutel voor channels |
| Public Key | Publieke sleutel — vrij deelbaar, voor versleutelen van berichten |
| Regio | Benoemd gebied waarbinnen een repeater flood-verkeer doorlaat. De naam levert een sleutel; wat er over de lucht gaat is een 16-bits transport code |
| Repeater | Node die berichten doorgeeft om het netwerkbereik te vergroten |
| Room Server | Fysieke node met BBS-functie voor store-and-forward (tot 32 berichten) |
| Routing | Het bepalen van de beste route voor een bericht door het netwerk |
| Scope | De regio die een afzender aan een pakket meegeeft, als `transport_codes[0]` in de header |
| Transport code | De 16 bits in `transport_codes[0]`. **Geen identificatie van een regio** maar een HMAC over payload type en payload, gezet met de regiosleutel. Verandert bij elk bericht; een repeater herkent hem door hem zelf te herberekenen, niet door hem op te zoeken |
| Regiocode | In de context van [UN/LOCODE](../techniek/techniek-locode.md): de *naam* van een regio, zoals `nl-ov-zwo`. Blijft op de node en gaat nooit de lucht in. Niet te verwarren met de transport code |
| SF | Spreading Factor — bepaalt bereik vs snelheid (SF7–SF12), hoger = verder |
| SIG | Special Interest Group — organisatie achter Bluetooth standaarden |
| SMA | SubMiniature version A — schroefbare antenneconnector |
| SNR | Signal-to-Noise Ratio — verhouding tussen signaal en ruis in dB |
| SPI | Serial Peripheral Interface — snelle bus voor LoRa chip en SD-kaart |
| Store-and-forward | Berichten opslaan totdat de ontvanger bereikbaar is |
| SX1262 | Semtech LoRa radiochip — nieuwere, efficiëntere versie |
| SX1276 | Semtech LoRa radiochip — oudere maar nog steeds gebruikte versie |
| Sync Word | Netwerk identifier (2 bytes) om verschillende netwerken te scheiden |
| Telemetry | Meetgegevens van sensoren die via het netwerk worden verstuurd |
| UART | Universal Asynchronous Receiver-Transmitter — seriële communicatie interface |
| UUID | Universally Unique Identifier — unieke identificatie voor BLE services |
| Web Flasher | Browser-tool om firmware te installeren zonder speciale software |
| Wrap | Frequentie springt terug naar begin van de band (0) na bereiken van maximum |
