# From Text to Chirp

How LoRa encodes data — a step-by-step explanation from bits to radio signal.

## You want to send "Test"

Let's start with something concrete: you want to send the word "Test" via LoRa. How does that become a radio signal that can travel kilometres?

### Letters become bits

Every letter has an ASCII code, and that code is a number we can write as bits:

| Letter | ASCII | Binary |
|---|---|---|
| T | 84 | 01010100 |
| e | 101 | 01100101 |
| s | 115 | 01110011 |
| t | 116 | 01110100 |

Together, "Test" is **32 bits**.

## Bits become symbols

Now the **Spreading Factor (SF)** comes into play. With SF12 we group bits in groups of 12.

### Why 12 bits?

SF12 means: each symbol carries 12 bits of information. Those 12 bits together form a number from 0 to 4095 (because 2¹² = 4096 possible values).

We take our 32 bits and divide them into groups of 12. The word "Test" thus becomes **three symbols**: 1350, 1395 and 1860.

![Diagram 1 bij techniek-chirp](../../images/en/text-to-chirp-1.svg)

## Symbols become chirps

Now the crucial step: how does a number (for example 1350) become a radio signal?

### The frequency ladder

Imagine the 125 kHz bandwidth as a ladder with **4096 rungs**. Each symbol number corresponds to a starting position on that ladder.

![Diagram 2 bij techniek-chirp](../../images/en/text-to-chirp-2.svg)

### The chirp climbs the ladder

A chirp starts at its start position and then traverses all rungs upward. At the top it **wraps** back to the bottom and continues until it returns to its starting point.

![Diagram 3 bij techniek-chirp](../../images/en/text-to-chirp-3.svg)

## How does the receiver know which symbol it was?

The receiver performs a clever mathematical trick: it multiplies the received chirp by a locally generated **down-chirp** (descending frequency).

Rising frequency × falling frequency = **constant tone**. The pitch of that tone depends on where the original chirp started.

![Diagram 4 bij techniek-chirp](../../images/en/text-to-chirp-4.svg)

The **FFT** (Fast Fourier Transform) analyses the tone and produces a spectrum with 4096 bins. The bin where the energy is concentrated = the symbol number.

### Fault tolerance: Processing Gain

The power of LoRa lies in redundancy. With SF12, 12 bits are spread over 4096 frequency steps. This is **341× more bandwidth than strictly necessary**. This "processing gain" (~36 dB) makes detection below the noise floor possible.

## Summary

The complete chain from text to radio signal:

![Diagram 5 bij techniek-chirp](../../images/en/text-to-chirp-5.svg)

Translated from Dutch by Anthropic Claude
