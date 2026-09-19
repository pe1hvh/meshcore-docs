# LoRa Modulatie

*CSS · SPREADING FACTORS · DEMODULATIE*

## LoRa in de netwerklagen

LoRa en MeshCore passen in het bekende OSI-model. LoRa zelf opereert op de fysieke laag (laag 1) — het vertaalt bits naar radiosignalen via Chirp Spread Spectrum.

## Synchronisatie zonder handshake

Er is geen handshaking bij LoRa. De zender zendt, en wie luistert, luistert. Synchronisatie gebeurt via de **preamble** — identieke chirps aan het begin van elk packet.

Symbool 0 is de referentie: een chirp die begint op de laagste frequentie en netjes naar boven loopt. De preamble bestaat uit 8× symbool 0, gevolgd door de data.

## Demodulatie: down-chirp mixing

De ontvanger vermenigvuldigt het ontvangen signaal met een lokaal gegenereerde down-chirp (dalende frequentie). Dit proces heet **dechirping**.

1. Ontvang up-chirp met onbekende startfrequentie
2. Vermenigvuldig met lokale down-chirp
3. Resultaat: constante toon (frequentie hangt af van startpositie)
4. Pas FFT toe op het gedechirpte signaal
5. Vind de piek in het spectrum
6. Piekpositie = symboolwaarde

## SF Orthogonaliteit

Verschillende spreading factors zijn (bijna) orthogonaal: een SF10 ontvanger negeert SF12 signalen, en vice versa. Dit komt doordat de chirp-duur verschilt per SF.

## Chirp Spread Spectrum (CSS)

LoRa gebruikt CSS: een modulatietechniek waarbij de frequentie lineair door de bandbreedte loopt. Dit maakt het signaal zeer robuust tegen:

- **Multipath** — reflecties zijn verschoven in tijd, niet in frequentie-evolutie
- **Interferentie** — andere signalen correleren niet met de chirp
- **Doppler** — frequentieverschuiving verschuift de hele chirp, niet de vorm

## De Encoding Pipeline

LoRa heeft een meervoudige encoding pipeline die data omzet naar chirps:

```text
1. Data → Whitening (pseudo-random XOR)
2. Whitened data → Hamming FEC (foutcorrectie)
3. FEC codewords → Interleaving (bits verspreiden)
4. Interleaved data → Gray coding
5. Gray-coded symbolen → Chirp modulatie
6. Preamble + Sync + Header + Payload + CRC → Packet
7. Packet → Radiosignaal
```

## Bits, Symbolen en Chips

| Term | Betekenis | Voorbeeld (SF12) |
|---|---|---|
| Bit | Kleinste informatie-eenheid | 0 of 1 |
| Symbool | Groep van SF bits | 12 bits → waarde 0–4095 |
| Chip | Eén frequentiestap in de chirp | 4096 chips per symbool |

Bij SF12 worden 12 bits verspreid over 4096 chips, wat een processing gain van ~36 dB oplevert.
