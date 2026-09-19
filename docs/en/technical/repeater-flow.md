# Repeater TX/RX flow

*TECHNICAL · HARDWARE-SOFTWARE SEPARATION OF A MESHCORE REPEATER*

Two diagrams that show how a repeater processes and forwards a received packet. The **block diagram** shows which components are involved and who does what; the **sequence diagram** below shows the time order of a complete Receive (RX) → Transmit (TX) cycle. Amber = hardware (the LoRa chip), blue = software: the MeshCore firmware on the Microcontroller Unit (MCU).

Hardware (LoRa chip, e.g. SX1262)
Software (MeshCore firmware)
Error path / forced condition
RF / hardware path
Software call
Polling / waiting
===========================================================
BLOCK DIAGRAM
===========================================================

## [1] Block diagram — components and data paths

The LoRa chip runs continuously in RX mode and performs preamble detection and demodulation itself in hardware. The MCU/firmware only sees the result via Interrupt Request (IRQ) flags and Serial Peripheral Interface (SPI) reads. For transmission the reverse applies: the firmware decides when and what, the chip does the actual modulation and Radio Frequency (RF) output.

![Block diagram MeshCore repeater](../../images/en/repeater-flow-1.svg)

### What stands out

- The `LoRa demodulator` is *always on* during RX and sets the IRQ flags itself. What some documents call "software CAD" is actually: the chip does Channel Activity Detection (CAD) in hardware via the correlator, the firmware only reads the flag.
- The firmware always talks to the chip via SPI, except for the Digital Input/Output 1 (DIO1) line which asynchronously triggers the MCU when a packet has arrived or been sent.
- The `noise_floor` value used by Listen Before Talk (LBT) is built up by the software from 64 Received Signal Strength Indicator (RSSI) samples. The hardware only delivers individual RSSI values — the "noise floor" is a software construct.
- Repeaters have a queue of 32 slots; on overflow the *newest* packet is dropped, not the oldest.
- **Why CAD/LBT in software?** MeshCore supports 6+ radio chips (SX126x, SX127x, LR11xx, STM32WL) which do not all offer the same hardware CAD/LBT interface. Keeping the detection logic in firmware keeps the Hardware Abstraction Layer (HAL) chip-agnostic.
- **Queue priority is not just hop count.** Packets get a fixed priority per type, where *lower = sent earlier*:  The queue sorts first on `scheduled_for`, then on priority, then FIFO. See `src/Mesh.cpp` lines 61, 101, 338, 375–385, 641–645, 711.
  - priority 0: direct routed packets, acks, zero-hop messages
  - priority 1: own flood messages
  - priority 2: own path messages
  - priority 3: own adverts
  - priority 5: direct trace packets
  - flooded retransmits: priority = hop count

### CAD sensitivity per Spreading Factor

- The chirp correlator in the LoRa demodulator detects packets *below* the noise floor — the higher the Spreading Factor (SF), the more sensitive the detection:
  - SF7 → down to `−7.5 dB` below noise floor
  - SF8 → down to `−10 dB` below noise floor
  - SF9 → down to `−12.5 dB` below noise floor
  - SF10 → down to `−15 dB` below noise floor
  - SF11 → down to `−17.5 dB` below noise floor
  - SF12 → down to `−20 dB` below noise floor

- This explains why CAD is much stronger than LBT: LBT measures via RSSI only energy above the noise floor, while the correlator's processing gain reveals signals invisible to RSSI.
- Important limitation: CAD only recognises LoRa chirps on the *same SF* the chip is listening on. An SF8 transmitter is invisible to a CAD-equipped SF7 listener (but still visible to LBT if RSSI is high enough).

===========================================================
SEQUENCE DIAGRAM
===========================================================

## [2] Sequence diagram — one complete RX → TX cycle

Time runs from top to bottom. Each vertical line is an actor (HW or SW). Arrows are calls or signals between actors. The dashed parts are wait/polling periods during which the firmware continues with other work but this packet is not yet up.

![Sequence diagram MeshCore repeater RX-TX flow](../../images/en/repeater-flow-2.svg)

### Reading the sequence diagram

- **Phase 1** runs entirely in hardware. The firmware only "sees" the final result via the IRQ.
- **Phases 2–3** are software-only: parse, take a routing decision, compute a TX delay, put it in the queue.
- **Phase 4** is not an active phase — the queue has a `scheduled_for` in the future, the loop keeps skipping this packet.
- **Phase 5** contains the CAD/LBT check. Steps ⑰–⑱ are always active (CAD via IRQ flag readout). Step ⑲ (LBT via RSSI) is off by default (`int.thresh = 0`) and is then skipped.
- **The red feedback loop** at ㉑ is the weak spot in heavy traffic: if the chip sees preambles continuously, it forces a transmit after 4 seconds — with risk of collision.
- **tx_delay and the 4 s CAD window are independent.** The random tx_delay is folded into `scheduled_for` (Phase 3–4). The 4 s CAD timeout window only starts at step ⑭ in Phase 5, after `scheduled_for` is reached. A high `tx_delay_factor` therefore does not shorten the CAD window — a misconception that is sometimes suggested.
- **Phase 6** is mostly hardware: only the "start transmitting" command comes from software, the chip does the rest. Only through a new IRQ does the firmware know it has finished.

### Key source code locations

- `src/Dispatcher.cpp` — `loop()`, `checkRecv()`, `checkSend()`, `getCADFailRetryDelay() = 200`, `getCADFailMaxDuration() = 4000`
- `src/helpers/radiolib/RadioLibWrappers.cpp` — `isReceiving()`, `isChannelActive()`, noise floor sampling (`NUM_NOISE_FLOOR_SAMPLES = 64`)
- `src/helpers/radiolib/CustomSX1262.h` — `isReceiving()`: reads IRQ flags `PREAMBLE_DETECTED` and `HEADER_VALID`
- `src/helpers/StaticPoolPacketManager.cpp` — queue implementation, drop-on-full behaviour
- `examples/simple_repeater/MyMesh.cpp` — `getRetransmitDelay()`: `random(0, 5·airtime·tx_delay_factor + 1)`

Last updated: 24 May 2026. Generated from MeshCore source code (meshcore-dev/MeshCore, main branch). Diagrams are simplified for readability; peripheral issues (error handling, watchdogs, AGC reset, deep-sleep) have been omitted.
For operational recommendations (
tx_delay_factor
and
int.thresh
tuning, SF7/SF8 cohabitation): see
MeshWiki — De techniek achter verzenden en ontvangen (HvM)
[in Dutch].
