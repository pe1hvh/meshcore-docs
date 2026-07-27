# Repeater TX/RX flow

*TECHNIEK · HARDWARE-SOFTWARE SCHEIDING VAN EEN MESHCORE REPEATER*

Twee diagrammen die laten zien hoe een repeater een ontvangen pakket verwerkt en doorstuurt. Het **blokschema** toont welke componenten erbij betrokken zijn en wie wat doet; het **sequence diagram** daaronder toont de tijdsvolgorde van een complete Receive (RX) → Transmit (TX) cyclus. Amber = hardware (de LoRa-chip), blauw = software: de MeshCore firmware op de Microcontroller Unit (MCU).

Hardware (LoRa-chip, bv. SX1262)
Software (MeshCore firmware)
Foutpad / forceer-conditie
RF / hardware-pad
Software-aanroep
Polling / wachten
===========================================================
BLOCK DIAGRAM
===========================================================

## [1] Blokschema — componenten en datapaden

De LoRa-chip draait continu in RX-modus en doet zelf preamble-detectie en demodulatie in hardware. De MCU/firmware ziet daarvan alleen het resultaat via Interrupt Request (IRQ)-flags en Serial Peripheral Interface (SPI)-uitlezingen. Voor het zenden geldt het omgekeerde: de firmware besluit wanneer en wat, de chip doet de daadwerkelijke modulatie en Radio Frequency (RF)-uitvoer.

![Blokschema MeshCore repeater](../../images/repeater-flow-1.svg)

### Wat hier opvalt

- De `LoRa demodulator` staat *altijd aan* tijdens RX en zet zelf de IRQ-flags. Wat in sommige documenten "software-CAD" wordt genoemd is feitelijk: de chip doet Channel Activity Detection (CAD) in hardware via de correlator, de firmware leest alleen de flag uit.
- De firmware praat altijd via SPI met de chip, behalve de Digital Input/Output 1 (DIO1)-lijn die asynchroon de MCU triggert wanneer een pakket binnen of weg is.
- Het `noise_floor`-getal dat Listen Before Talk (LBT) gebruikt wordt door de software opgebouwd uit 64 Received Signal Strength Indicator (RSSI)-samples. De hardware levert alleen losse RSSI-waarden — de "noise floor" is een softwareconstruct.
- Repeaters hebben een queue van 32 slots; bij overstroom wordt het *nieuwste* pakket gedropt, niet het oudste.
- **Waarom CAD/LBT in software?** MeshCore ondersteunt 6+ radiochips (SX126x, SX127x, LR11xx, STM32WL) die niet allemaal dezelfde hardware-CAD/LBT-interface bieden. Door de detectielogica in de firmware te houden blijft de Hardware Abstraction Layer (HAL) chip-agnostisch.
- **Queue-prioriteit is niet alleen hop-count.** Pakketten krijgen een vaste priority per type, waarbij *lager = eerder verzonden*:  De queue sorteert eerst op `scheduled_for`, dan op priority, dan FIFO. Zie `src/Mesh.cpp` regels 61, 101, 338, 375–385, 641–645, 711.
  - priority 0: direct routed packets, acks, zero-hop messages
  - priority 1: eigen flood messages
  - priority 2: eigen path messages
  - priority 3: eigen adverts
  - priority 5: direct trace packets
  - flooded retransmits: priority = hop-count

### CAD-gevoeligheid per Spreading Factor

- De chirp-correlator van de LoRa demodulator detecteert pakketten *onder* de ruisvloer — hoe hoger de Spreading Factor (SF), hoe gevoeliger de detectie:
  - SF7 → tot `−7.5 dB` onder noise floor
  - SF8 → tot `−10 dB` onder noise floor
  - SF9 → tot `−12.5 dB` onder noise floor
  - SF10 → tot `−15 dB` onder noise floor
  - SF11 → tot `−17.5 dB` onder noise floor
  - SF12 → tot `−20 dB` onder noise floor

- Dit verklaart waarom CAD veel sterker is dan LBT: LBT meet via RSSI alleen energie boven de noise floor, terwijl de correlator door processing gain signalen ziet die voor RSSI onzichtbaar zijn.
- Belangrijke beperking: CAD herkent alleen LoRa-chirps op *dezelfde SF* waarop de chip luistert. Een SF8-zender is voor een SF7-luisteraar onzichtbaar voor CAD (wel zichtbaar voor LBT als RSSI hoog genoeg is).

===========================================================
SEQUENCE DIAGRAM
===========================================================

## [2] Sequence diagram — één complete RX → TX cyclus

De tijd loopt van boven naar beneden. Elke verticale lijn is een actor (HW of SW). Pijlen zijn aanroepen of signalen tussen actors. De gestreepte stukken zijn wacht-/polling-periodes waarin de firmware doorgaat met andere werk maar dit pakket nog niet aan de beurt is.

![Sequence diagram MeshCore repeater RX-TX flow](../../images/repeater-flow-2.svg)

### Lezen van het sequence diagram

- **Fase 1** draait volledig in hardware. De firmware "ziet" alleen het eindresultaat via de IRQ.
- **Fase 2–3** is software-only: parsen, een routing-besluit nemen, een TX-delay uitrekenen, in de queue zetten.
- **Fase 4** is geen actieve fase — de queue heeft een `scheduled_for` in de toekomst, de loop slaat dit pakket steeds over.
- **Fase 5** bevat de CAD/LBT-check. Stappen ⑰–⑱ zijn altijd actief (CAD via IRQ-flag uitlezen). Stap ⑲ (LBT via RSSI) is standaard uit (`int.thresh = 0`) en wordt dan overgeslagen.
- **De rode terugkoppel-lus** bij ㉑ is de zwakke plek bij druk verkeer: als de chip onafgebroken preambles ziet, wordt na 4 seconden geforceerd gezonden — met risico op collision.
- **tx_delay en het 4 s CAD-window zijn onafhankelijk.** De random tx_delay wordt verwerkt in `scheduled_for` (Fase 3–4). Het 4 s CAD-timeout window begint *pas* bij stap ⑭ in Fase 5, nadat `scheduled_for` is bereikt. Een hoge `tx_delay_factor` verkort het CAD-window dus niet — wat soms wordt gesuggereerd klopt niet.
- **Fase 6** is grotendeels hardware: alleen het commando "begin met zenden" komt uit software, de rest doet de chip. Pas via een nieuwe IRQ weet de firmware dat het klaar is.

### Belangrijkste broncode-locaties

- `src/Dispatcher.cpp` — `loop()`, `checkRecv()`, `checkSend()`, `getCADFailRetryDelay() = 200`, `getCADFailMaxDuration() = 4000`
- `src/helpers/radiolib/RadioLibWrappers.cpp` — `isReceiving()`, `isChannelActive()`, noise floor sampling (`NUM_NOISE_FLOOR_SAMPLES = 64`)
- `src/helpers/radiolib/CustomSX1262.h` — `isReceiving()`: leest IRQ-flags `PREAMBLE_DETECTED` en `HEADER_VALID`
- `src/helpers/StaticPoolPacketManager.cpp` — wachtrij-implementatie, drop-bij-vol gedrag
- `examples/simple_repeater/MyMesh.cpp` — `getRetransmitDelay()`: `random(0, 5·airtime·tx_delay_factor + 1)`

Laatst bijgewerkt: 24 mei 2026. Gegenereerd op basis van MeshCore broncode (meshcore-dev/MeshCore, main branch). Diagrammen zijn vereenvoudigd voor leesbaarheid; randzaken (foutafhandeling, watchdogs, AGC-reset, deep-sleep) zijn weggelaten.
Voor operationele aanbevelingen (
tx_delay_factor
- en
int.thresh
-tuning, aanbevelingen voor SF7/SF8 cohabitation): zie
MeshWiki — De techniek achter verzenden en ontvangen (HvM)
.
