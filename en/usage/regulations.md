# Regulations & Duty Cycle

*LICENSE-FREE TRANSMISSION · EU/NL · 868 MHz · H-RULES · ERP*

══════════════════════════════════════════════════════════════

For LoRa equipment in the 868 MHz band, no transmitting licence and no notification are required in the Netherlands — provided you stay within the rules. Three layers of regulation determine what is allowed: an EU equipment directive, an EU spectrum decision, and the Dutch regulation that implements them nationally.

══════════════════════════════════════════════════════════════

## The regulatory stack

The complete chain, from legal basis to concrete band rules:

| Level | Document | What does it govern? |
|---|---|---|
| NL — Act | Telecommunications Act, art. 3.9 | Legal basis for license-free use |
| NL — Decree | Frequency Decree 2013 | Delegates which categories are license-free |
| NL — Regulation | Regulation on use of frequency space without licence and without notification 2015, **Annex 11 Subcategory 1** | The concrete H-rules (H1–H7) for non-specific short-range devices, including LoRa |
| NL — Decree | Radio Equipment Decree 2016 | Dutch implementation of the EU equipment directive |
| EU — Directive | **Directive 2014/53/EU (RED)** | Requirements for the equipment itself (CE marking, essential requirements). Replaces the former R&TTE Directive 1999/5/EC. |
| EU — Decision | Decision 2006/771/EC (consolidated) | EU-wide harmonisation of SRD frequency bands |
| EU — Amendment | Implementing Decision (EU) 2025/105 | Latest update to 2006/771/EC (January 2025) |
| CEPT | ERC Recommendation 70-03 | CEPT recommendation on which the EU decision is based |
| ETSI | EN 300 220-1 & EN 300 220-2 | Harmonised measurement standards under RED |

> [!NOTE]
> **Note — outdated reference in the regulation text**
> The remarks column of Annex 11 still refers to *"Directive 1999/5/EC"* (R&TTE). That directive was **repealed on 13 June 2016** and replaced by Directive 2014/53/EU (RED). The regulation text has not yet been updated on this point, but the reference must be read as "the successor thereto", i.e. RED. For new equipment only RED applies.

══════════════════════════════════════════════════════════════

## Annex 11 Subcategory 1 — the H-rules for 868 MHz

The relevant rows from the Dutch regulation for MeshCore and comparable LoRa equipment. The dBm column is added for reference. The **CEPT 70-03** column shows the European equivalent identifier from ERC Recommendation 70-03, Annex 1 (non-specific SRD).

| NL row | CEPT 70-03 | Frequency band | Max. power | In dBm | Duty cycle | Alternative | Remark |
|---|---|---|---|---|---|---|---|
| H3 | h1.5 | 868.000–868.600 MHz | 25 mW e.r.p. | +14 dBm | < 1 % | LBT+AFA | Typical LoRaWAN EU868 uplink |
| H4 | h1.7 | 869.400–869.650 MHz | **500 mW e.r.p.** | **+27 dBm** | **< 10 %** | LBT+AFA | High-power regime — DC monitoring or LBT+AFA required |
| H5 | — | 869.400–869.650 MHz | **25 mW e.r.p.** | **+14 dBm** | **< 0.1 %** | LBT+AFA | No CEPT row; NL variant within h1.7 band |
| H6 | h1.8 | 869.700–870.000 MHz | 5 mW e.r.p. | +7 dBm | none | — | No DC restriction |
| H7 | h1.9 | 869.700–870.000 MHz | 25 mW e.r.p. | +14 dBm | < 1 % | LBT+AFA | Higher power, with DC restriction |

MeshCore in the Netherlands typically runs on **869.618 MHz** — within the H4/H5 band (= CEPT h1.7). The choice between H4 and H5 depends on how your device is certified.

══════════════════════════════════════════════════════════════

## H4 versus H5 — MeshCore uses H4

H4 and H5 are two regulatory profiles for non-specific SRD (telemetry, data, alarms) in the Dutch SRD regulation and CEPT guidelines. They cover exactly the same frequency band of 869.400–869.650 MHz, but with different limits. H4 offers more generous limits than H5, which makes it the default choice for MeshCore networks.

> [!NOTE]
> **⚠ Terminology — H4/H5 are Dutch table codes, not ETSI classes**
> "H4" and "H5" are row labels in Annex 11, Subcategory 1 of BWBR0036378 — purely Dutch regulatory codes. ETSI EN 300 220-1 only knows *receiver categories* 1, 1.5, 2 and 3 (reception performance), and CEPT ERC 70-03 uses lowercase codes such as `h1.7` for the same sub-band. There is therefore no "ETSI H4 class". What does apply: equipment for regime H4 or H5 must be certified under RED 2014/53/EU via that same ETSI EN 300 220, but then tested against the parameters belonging to the regime.

H4 allows 20× more transmit power and a 100× more generous duty cycle than H5, which makes it more suitable for mesh communication where repeaters regularly have to forward relay traffic.

### MeshCore community uses H4 as the default

The Dutch MeshCore community operates within the H4 profile. The VERON news article "MeshCore, de opvolger van Meshtastic" (22 December 2025, by Arno PE1RDP) states literally: *"Zo is het maximale RF vermogen 500mW ERP en de duty cycle 10%."* [So the maximum RF power is 500 mW ERP and the duty cycle 10 %.] These are exactly the H4 limits.

The practical configuration listed as standard on several Dutch MeshCore sources:

```text
Preset:       Netherlands
Frequency:    869.618 MHz
Bandwidth:    62.5 kHz
Spreading:    SF7
Coding rate:  4/5
Max. TX:      ≤500 mW e.r.p. (+27 dBm)
Duty cycle:   ≤10 %
```

This configuration falls within the H4 parameters from Annex 11 and is interoperable with other Dutch MeshCore nodes.

### Why not H5?

The H5 profile (25 mW / 0.1 %) is also permitted on the same frequency band in theory, but for a mesh network with routing and forwarding, 25 mW is limited in range and 3.6 seconds of transmit time per hour is limited in airtime. For single-purpose applications (a sensor that occasionally sends a short message) H5 is appropriate; for an active mesh relay node less so.

### Source

| Source | Confirmation |
|---|---|
| [VERON — MeshCore, de opvolger van Meshtastic](https://veron.nl/nieuws/meshcore-de-opvolger-van-meshtastic/) (Arno PE1RDP, 22-12-2025, Dutch) | 500 mW ERP, 10 % duty cycle; EU/UK Narrow preset, 62.5 kHz bandwidth |

══════════════════════════════════════════════════════════════

## What is a duty cycle?

A **duty cycle** is the maximum fraction of a continuous one-hour period (T<sub>obs</sub> = 1 h) during which your transmitter is allowed to transmit within the applicable band. The rule exists to prevent a single transmitter from monopolising a license-free band — everyone must share fairly.

| Duty cycle | Transmit time per hour | Regime |
|---|---|---|
| 0.1 % | 3.6 seconds | H5 |
| 1 % | 36 seconds | H3 / H7 |
| 10 % | 6 minutes | H4 |
| 100 % | unlimited | H6 (no DC restriction) |

### Alternative: LBT+AFA (polite spectrum access)

**Listen Before Talk + Adaptive Frequency Agility** is a "polite" protocol: your node first listens whether the frequency is clear before transmitting (LBT), and hops between channels (AFA) to avoid blocking any single one for long. Equipment that implements this correctly may in many cases exceed the duty cycle limit, provided it is demonstrably "polite" according to ETSI EN 300 220.

### Practice for MeshCore nodes

A typical MeshCore packet lasts 150–400 ms. Under H4 (10 %) your node may transmit for a maximum of 6 minutes per hour — ample for an average node. A repeater that relays a lot of traffic does need to watch out: during traffic peaks you can exhaust the DC budget faster than you think, especially at higher spreading factors where packets stay in the air longer.

### Duty cycle in a mesh — what differs from a standalone node

The H-rules describe a single transmitting device. CEPT defines duty cycle as Σ(T<sub>on</sub>)/T<sub>obs</sub>, where T<sub>on</sub> is the on-air time of **a single transmitter device** and T<sub>obs</sub> is one continuous hour. Three things follow from this for a mesh network:

**1. There is no network budget.** The regulation knows no collective limit for a mesh. Every node is assessed individually. Twenty repeaters each sitting at 9 % formally breach nothing — even if the band is heavily loaded locally.

**2. Relayed traffic counts against your own budget.** A packet your repeater forwards on someone else's behalf is legally your transmission. Where a standalone sensor can compute its duty cycle in advance, a repeater's is a function of third-party traffic — and your budget fills fastest exactly when the network is busiest.

**3. One message requires N transmissions.** MeshCore clients do not repeat; only repeaters and room servers with `repeat on` do. A single flood message is therefore transmitted once by *every* repeater that hears it. Load on the mesh scales with the number of repeaters, not the number of senders.

#### How many packets fit in 6 minutes?

Indicative, calculated with the standard LoRa time-on-air formula for SF7 / BW 62.5 kHz / CR 4/5 (the current Dutch parameters):

| Payload | Time-on-air | H4 — 6 min/hour | H5 — 3.6 s/hour |
|---|---|---|---|
| 20 bytes | ~170 ms | ~2,100 transmissions/hour | ~21 transmissions/hour |
| 50 bytes | ~320 ms | ~1,130 transmissions/hour | ~11 transmissions/hour |
| 80 bytes | ~485 ms | ~740 transmissions/hour | ~7 transmissions/hour |

Under H4 there is ample room for a normal repeater. Under H5 the same repeater would land at roughly ten forwards per hour — unusable in practice for a relay node. That is the real reason mesh repeaters need the H4 regime.

> [!WARNING]
> **⚠ The firmware default does not meet the Dutch limit**
> MeshCore's `set dutycycle` defaults to **50 %**, and the deprecated `set af` to `1.0` (also ~50 %). Both sit far above H4 (10 %) as well as H5 (0.1 %). A freshly flashed repeater is therefore **non-compliant** until you change this explicitly: `set dutycycle 10` (firmware v1.15.0 and later).

#### LBT+AFA is not an alternative for MeshCore

The regulation offers LBT+AFA as a way out of the duty cycle limit, but AFA stands for *Adaptive Frequency Agility* — hopping between channels. In the Netherlands MeshCore runs on a single fixed carrier, so that condition is not met. The `txdelay` and `rxdelay` mechanisms are collision avoidance, not certified LBT under ETSI EN 300 220. For Dutch nodes, in practice, only the duty cycle route applies.

#### Behavioural settings that relieve the mesh

These settings are no substitute for RED certification, but they are the practical way to stay within the H4 budget and keep the band liveable.

| Setting | Firmware default | NL recommendation | Why |
|---|---|---|---|
| `set dutycycle {1-100}` | 50 % | `10` | Hard limiter against the H4 ceiling (v1.15.0+) |
| `set af {0-9}` *(deprecated)* | `1.0` (~50 %) | `9` (~10 %) | Same purpose on firmware older than v1.15.0 |
| `set loop.detect` | `off` | `minimal` | Prevents packet storms caused by a node with deviant firmware (v1.14.0+) |
| `set flood.advert.interval {hours}` | 12 | `49` | Less background traffic; adverts are flood packets |
| `set advert.interval {minutes}` | 0 | `240` | Zero-hop adverts require no relay capacity |
| `set flood.max.advert` | 8 | 8 | Bounds how far an advert floods |
| `set flood.max.unscoped` | 64 | e.g. `3` | Keeps region-less floods local |
| `region` (scoping) | — | NL regions | Confines floods to your own region |
| `set txdelay` / `direct.txdelay` | `0.5` / `0.2` | default | Random window against simultaneous retransmissions |
| `set repeat` | `on` | `on` | Turning it off means no relaying |

A repeater should also generate as little traffic of its own as possible: where you can, use a separate device as your personal node.

> [!WARNING]
> **⚠ Who enforces this?**
> The **Dutch Authority for Digital Infrastructure (RDI — Rijksinspectie Digitale Infrastructuur)**, the successor to Agentschap Telecom as of 1 January 2023. In practice, enforcement on hobbyist LoRa is rare, but in the face of persistent interference complaints RDI can deploy measurement equipment and impose fines.

══════════════════════════════════════════════════════════════

## TX ≠ ERP — what counts?

The regulation refers to **e.r.p.** (Effective Radiated Power) — the total radiated power in the direction of maximum antenna gain, with a half-wave dipole as reference. This is *not* the same as the power your LoRa chip delivers. The formula:

```text
ERP (dBm) = TX power (dBm) + antenna gain (dBd) − cable/connector loss (dB)
```

### dBi versus dBd — mind the reference

Antennas are usually specified in **dBi** on the datasheet (gain relative to isotropic), but the regulation uses **dBd** (gain relative to a half-wave dipole). The conversion is a constant:

```text
dBi = dBd + 2.15
dBd = dBi − 2.15
```

So: a "3 dBi antenna" on the packaging only has 0.85 dBd gain — 2.15 dB less than you might think at first glance. For 2.4 GHz and above the regulation uses e.i.r.p. (dBi reference) instead; don't confuse the two.

### Practical table: SX1262 at +22 dBm

A standard SX1262 node at +22 dBm TX power with 0.2 dB cable loss, by antenna type:

| Antenna | Gain (dBi) | Gain (dBd) | ERP (dBm) | ERP (mW) | Status |
|---|---|---|---|---|---|
| Short rubber duck | 0 | −2.15 | 19.65 | 92 | Within H4 ✓ |
| ¼-wave whip | 2 | −0.15 | 21.65 | 146 | Within H4 ✓ |
| Dipole | 2.15 | 0 | 21.80 | 151 | Within H4 ✓ |
| Collinear 3 dBi | 3 | 0.85 | 22.65 | 184 | Within H4 ✓ |
| Collinear 5 dBi | 5 | 2.85 | 24.65 | 292 | Within H4 ✓ |
| **Collinear 8 dBi** | 8 | 5.85 | 27.65 | **582** | **⚠ Above H4** |
| Yagi 10 dBi | 10 | 7.85 | 29.65 | 923 | ⚠ Far above H4 |

Striking: at +22 dBm you are already above the H5 limit of 25 mW regardless of antenna. Strictly legally, you then fall under the H4 regime (with 10 % DC obligation and full ETSI EN 300 220 compliance against the H4 parameters). With an 8 dBi collinear you even exceed the H4 upper limit of 500 mW. Solution: lower TX power to +14 dBm (25 mW) to stay neatly within H5, or moderate the antenna gain.

══════════════════════════════════════════════════════════════

## Which regime applies to your node?

Per LoRa chip and module combination:

| Chip / module | Max. TX | In mW | Regime (with standard dipole antenna, ~0 dBd) |
|---|---|---|---|
| SX1276 RFO pin | +14 dBm | 25 mW | Exactly at the H5 limit ✓ |
| SX1276 PA_BOOST pin | +20 dBm | 100 mW | Above H5, below H4 — falls under H4 regime |
| SX1262 (standard) | +22 dBm | 158 mW | Above H5, below H4 — falls under H4 regime |
| LR1121 | +22 dBm | 158 mW | Same as SX1262 |
| Ebyte E22-900M30S (PA) | +30 dBm | 1000 mW | Above H4 limit — turn down the PA stage; `set tx` (1–22 dBm) drives only the LoRa chip |

> [!NOTE]
> **The SX1262 grey zone**
> Almost all hobbyist MeshCore boards (Heltec V3, RAK4631, LilyGO T-Deck) use the SX1262 at +22 dBm. That formally exceeds the H5 ceiling of 25 mW, so the device should comply with the heavier H4 regime — with ETSI EN 300 220 compliance against the H4 parameters (500 mW / <10 % DC) and active duty-cycle monitoring or polite spectrum access. In practice, most hobbyist hardware does not formally meet this.
> Want to stay strictly within the rules? Set your TX power to **+14 dBm** (25 mW) — then you fall neatly under the H5 regime and your device only needs to be certified against the H5 parameters. You give up ~8 dB of signal strength, but a decent antenna will easily make that back.

══════════════════════════════════════════════════════════════
> [!WARNING]
> **⚠ Disclaimer**
> This page is informative and **not legal advice**. Regulation is updated periodically. When in doubt, always consult the official sources below, or contact the Dutch Authority for Digital Infrastructure (RDI).

══════════════════════════════════════════════════════════════

## Sources

All regulation and standards on which this page is based, clickable and grouped by level. Most Dutch-language sources below link to the original Dutch government portal.

### Dutch legislation

| Document | Role |
|---|---|
| [Telecommunications Act, art. 3.9 (BWBR0009950)](https://wetten.overheid.nl/BWBR0009950) | Legal basis for license-free use |
| [Frequency Decree 2013 (BWBR0032895)](https://wetten.overheid.nl/BWBR0032895) | Delegation of license-free categories |
| [Regulation frequency space without licence and without notification 2015, Annex 11 (BWBR0036378)](https://wetten.overheid.nl/BWBR0036378/2025-07-01/0) | Concrete H-rules (H1–H7) — source for H4 and H5 |
| [Radio Equipment Decree 2016 (BWBR0038910)](https://wetten.overheid.nl/BWBR0038910) | NL implementation of RED 2014/53/EU |
| [Dutch Authority for Digital Infrastructure (RDI)](https://www.rdi.nl) | Enforcement agency (formerly Agentschap Telecom) |

### EU legislation

| Document | Role |
|---|---|
| [Directive 2014/53/EU (RED — Radio Equipment Directive)](https://eur-lex.europa.eu/eli/dir/2014/53/oj) | Equipment requirements; replaces 1999/5/EC |
| [Decision 2006/771/EC (SRD base decision, consolidated)](https://eur-lex.europa.eu/eli/dec/2006/771/oj) | EU-wide spectrum harmonisation |
| [Implementing Decision (EU) 2025/105](https://eur-lex.europa.eu/eli/dec_impl/2025/105/oj) | Latest SRD update (January 2025) |
| [Implementing Decision (EU) 2022/180](https://eur-lex.europa.eu/eli/dec_impl/2022/180/oj) | Previous SRD update (February 2022) |

### CEPT / ETSI standards

| Document | Role |
|---|---|
| [CEPT ERC Recommendation 70-03 (March 2024 edition)](https://docdb.cept.org/download/4635) | CEPT recommendation (source of the EU decision); Annex 1 contains the non-specific SRD bands with identifiers h1.5, h1.6, **h1.7**, h1.8, h1.9 |
| [ETSI EN 300 220-1 V3.1.1 (PDF)](https://www.etsi.org/deliver/etsi_en/300200_300299/30022001/03.01.01_60/en_30022001v030101p.pdf) | SRD measurement methods 25–1000 MHz; e.r.p. definition and source for the calculator formula |
| [ETSI EN 300 220-2 V3.3.1 (March 2025, PDF)](https://www.etsi.org/deliver/etsi_en/300200_300299/30022002/03.03.01_60/en_30022002v030301p.pdf) | Harmonised standard under RED — band/power tables |

### Historical

| Document | Status |
|---|---|
| [Directive 1999/5/EC (R&TTE)](https://eur-lex.europa.eu/eli/dir/1999/5/oj) | Repealed as of 13-06-2016, replaced by RED 2014/53/EU. Still mentioned in the remarks of Annex 11. |

> [!NOTE]
> This page originally contained an interactive calculator (transmit power/EIRP). Markdown cannot execute it; the formula is written out instead.

Translated from Dutch by Anthropic Claude
