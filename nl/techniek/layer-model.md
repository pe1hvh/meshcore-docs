# Het Lagenmodel van MeshCore

*4 LAGEN · RF TOT JURIDISCH*

MeshCore is opgebouwd uit vier strikt gescheiden lagen, elk met een specifieke functie.

## De vier lagen

Layer stack SVG

![Diagram 1 bij techniek-lagen](../../images/nl/layer-model-1.svg)

## Laag 1: RF-hardware

Microcontroller (ESP32/nRF52), LoRa-chip (SX1262), antenne en voeding. Dit is de fysieke basis van elke node.

## Laag 2: LoRa PHY

De modemlaag vertaalt bits naar radiosignalen via Chirp Spread Spectrum. Bandbreedte (BW), Spreading Factor (SF) en Coding Rate (CR) bepalen de balans tussen bereik en snelheid.

## Laag 3: Firmware en Netwerkstack

MeshCore firmware verzorgt routing, berichtafhandeling en netwerkbeheer. Elke node heeft een eigen identiteit in de vorm van een Ed25519-keypair; in pakketten en paden wordt die node aangeduid met de **eerste byte van zijn public key** (zie [MeshCore Packet Structuur](packet-structure.md)). Nodes kunnen routes leren naar andere nodes: **intelligente routing** in plaats van flooding zorgt voor efficiënt netwerkverkeer.

## Laag 4: Juridische modus

Bepaalt of het apparaat draait in HAM-modus (70 cm-band, geen encryptie, callsign verplicht) of ISM-modus (868 MHz, encryptie, anoniem mogelijk).

## Link Budget — Waarom LoRa zo ver komt

Link budget is het totaal aan signaalverlies dat een verbinding kan verdragen. LoRa haalt **150+ dB link budget**, waardoor:

- Lange afstanden met laag vermogen mogelijk zijn
- Verbindingen onder de ruisvloer nog decodeerbaar zijn
- Meshes met weinig nodes al regionaal kunnen schalen (via hops)
