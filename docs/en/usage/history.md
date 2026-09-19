# Origin and History

*FROM RADAR TECHNOLOGY TO OFF-GRID MESH*

The technological evolution from World War II radar technology to modern off-grid mesh communication via LoRa and MeshCore.
## Timeline
### Chirp Spread Spectrum (the 1940s)


The roots of MeshCore lie in Chirp Spread Spectrum (CSS), a modulation technique developed in the 1940s for radar applications. CSS spreads a signal over a wide bandwidth by letting the frequency rise or fall linearly (chirps). This makes the signal robust against multipath fading, interference and jamming.Multipath fading A radio signal can reach the receiver via multiple paths: directly, but also via reflections off buildings, mountains or other objects. These signals arrive at slightly different times and can reinforce or cancel each other out (fading). CSS is robust against this because the frequency changes continuously - a reflection that arrives slightly later has a different frequency and therefore does not interfere destructively with the direct signal.

**Interference Other radio sources on the same or nearby frequencies can disrupt your signal. Think of WiFi, other LoRa transmitters, or industrial equipment. CSS spreads the signal over a wide bandwidth and a long duration. A brief interferer only affects a small part of your chirp, and the FFT can still reconstruct the symbol from the remaining samples.**

**Jamming Deliberate disruption by a transmitter that continuously emits noise or a strong signal on your frequency. CSS is difficult to jam because:**

- You have to disrupt the entire 64 kHz (in NL) bandwidth at once (not just one frequency)

- The processing gain ensures your signal remains detectable as long as the jammer is not extremely strong

- Different spreading factors are orthogonal, so a jammer on SF7 does not disturb SF12

**In this context, orthogonal means "independent" or "non-interfering".For a more detailed explanation, see section 14.4**

### LoRa: from idea to chip (2009-2012)


In 2009, two French engineers, Nicolas Sornin and Olivier Seller, began developing a long-range, low-power modulation technique based on CSS. In 2010, François Sforza joined them and together they founded Cycleo in France. In May 2012, Cycleo was acquired by Semtech Corporation, which commercialized the technology under the brand name LoRa (Long Range).

### Accessible hardware (2016-2018)


The real breakthrough for hobbyists came with the combination of Semtech's LoRa chips (SX1276/SX1262) and Espressif's ESP32 microcontroller. Manufacturers such as Heltec and LILYGO brought integrated development boards to market for ~\$20-30.

### Meshtastic: the first mesh wave (2019-2020)


In 2019, American software engineer Kevin Hester (GitHub: geeksville) started the Meshtastic project. Meshtastic uses a flooding mesh protocol in which every device forwards messages. In large networks this led to congestion.

### MeshCore: intelligent routing (2024-2025)


In late 2024, Australian developer Scott Powell (Ripple Radios) started work on a new protocol. In early 2025, together with Andy Kirby (UK) and Liam Cottle (NZ), he launched the MeshCore project featuring:

- Hybrid routing: first contact via flood, then learned routes for efficiency
- Role separation: Companion Radios, Repeaters and Room Servers as separate functions
- Scalability: up to 64 hops, state-aware network, AES-128 encryption
- Lightweight C++: no dynamic memory allocation, embedded-first design

### MeshCore Team split (2026)


In April 2026, the MeshCore development team split. Founder Scott Powell (firmware), Liam Cottle (app), Recrof (map/flasher), FDLamotte (Python/STM32) and Oltaco (bootloader) now form the "core team" at meshcore.io.Andy Kirby (UK) - previously responsible for branding, community and the meshcore.co.uk domain - split off after filing a trademark application for "MeshCore" without consultation, and after rewriting large parts of the ecosystem tools with Claude Code without disclosing it.Andy himself states that the application was purely to protect the brand, and that the launch of meshcore.io without his knowledge was what actually caused the split.He is now continuing his own work as the separate MeshOS project at meshcore.co.uk, while the core team regards the GitHub repository (meshcore-dev/MeshCore) as the sole source of truth for the firmware (and IMO the meshcore community does too).
