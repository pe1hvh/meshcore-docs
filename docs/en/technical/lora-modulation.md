# LoRa Modulation

*CSS · SPREADING FACTORS · DEMODULATION*

## LoRa in the network layers

LoRa and MeshCore fit into the familiar OSI model. LoRa itself operates at the physical layer (layer 1) — it translates bits into radio signals via Chirp Spread Spectrum.

## Synchronisation without handshake

There is no handshaking with LoRa. The transmitter transmits, and whoever is listening, listens. Synchronisation happens via the **preamble** — identical chirps at the start of every packet.

Symbol 0 is the reference: a chirp that starts at the lowest frequency and sweeps neatly upward. The preamble consists of 8× symbol 0, followed by the data.

## Demodulation: down-chirp mixing

The receiver multiplies the received signal by a locally generated down-chirp (descending frequency). This process is called **dechirping**.

1. Receive up-chirp with unknown start frequency
2. Multiply by local down-chirp
3. Result: constant tone (frequency depends on start position)
4. Apply FFT to the dechirped signal
5. Find the peak in the spectrum
6. Peak position = symbol value

## SF Orthogonality

Different spreading factors are (almost) orthogonal: an SF10 receiver ignores SF12 signals, and vice versa. This is because the chirp duration differs per SF.

## Chirp Spread Spectrum (CSS)

LoRa uses CSS: a modulation technique where the frequency sweeps linearly through the bandwidth. This makes the signal highly robust against:

- **Multipath** — reflections are shifted in time, not in frequency evolution
- **Interference** — other signals do not correlate with the chirp
- **Doppler** — frequency shift displaces the entire chirp, not its shape

## The Encoding Pipeline

LoRa has a multi-stage encoding pipeline that converts data into chirps:

```text
1. Data → Whitening (pseudo-random XOR)
2. Whitened data → Hamming FEC (error correction)
3. FEC codewords → Interleaving (spreading bits)
4. Interleaved data → Gray coding
5. Gray-coded symbols → Chirp modulation
6. Preamble + Sync + Header + Payload + CRC → Packet
7. Packet → Radio signal
```

## Bits, Symbols, and Chips

| Term | Meaning | Example (SF12) |
|---|---|---|
| Bit | Smallest unit of information | 0 or 1 |
| Symbol | Group of SF bits | 12 bits → value 0–4095 |
| Chip | One frequency step in the chirp | 4096 chips per symbol |

At SF12, 12 bits are spread over 4096 chips, yielding a processing gain of ~36 dB.

Translated from Dutch by Anthropic Claude
