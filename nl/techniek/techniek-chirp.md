# Van Tekst naar Chirp

Hoe LoRa data codeert — een stap-voor-stap uitleg van bits naar radiosignaal.

## Je wilt "Test" versturen

Laten we beginnen met iets concreets: je wilt het woord "Test" versturen via LoRa. Hoe wordt dat een radiosignaal dat kilometers ver kan reizen?

### Letters worden bits

Elke letter heeft een ASCII-code, en die code is een getal dat we als bits kunnen schrijven:

| Letter | ASCII | Binair |
|---|---|---|
| T | 84 | 01010100 |
| e | 101 | 01100101 |
| s | 115 | 01110011 |
| t | 116 | 01110100 |

Samen is "Test" dus **32 bits**.

## Bits worden symbolen

Nu komt de **Spreading Factor (SF)** in beeld. Bij SF12 groeperen we bits in groepjes van 12.

### Waarom 12 bits?

SF12 betekent: elk symbool draagt 12 bits informatie. Die 12 bits vormen samen een getal van 0 tot 4095 (want 2¹² = 4096 mogelijke waarden).

We pakken onze 32 bits en verdelen ze in groepjes van 12. Het woord "Test" wordt zo **drie symbolen**: 1350, 1395 en 1860.

Bit grouping visualization

![Diagram 1 bij techniek-chirp](../../images/techniek-chirp-1.svg)

## Symbolen worden chirps

Nu de cruciale stap: hoe wordt een getal (bijvoorbeeld 1350) een radiosignaal?

### De frequentieladder

Stel je de 125 kHz bandbreedte voor als een ladder met **4096 treden**. Elk symboolnummer correspondeert met een startpositie op die ladder.

Frequency ladder diagram (tall version for visibility)

![Diagram 2 bij techniek-chirp](../../images/techniek-chirp-2.svg)

### De chirp loopt de ladder op

Een chirp begint op zijn startpositie en loopt dan alle treden af, omhoog. Bij de top **wrapt** hij naar beneden en gaat verder tot hij weer bij zijn startpunt is.

Two chirps: symbol 0 (no wrap) vs symbol N (with wrap)

![Diagram 3 bij techniek-chirp](../../images/techniek-chirp-3.svg)

## Hoe weet de ontvanger welk symbool het was?

De ontvanger doet een slimme wiskundige truc: hij vermenigvuldigt de ontvangen chirp met een lokaal gegenereerde **down-chirp** (dalende frequentie).

Stijgende frequentie × dalende frequentie = **constante toon**. De hoogte van die toon hangt af van waar de oorspronkelijke chirp begon.

Dechirp process diagram

![Diagram 4 bij techniek-chirp](../../images/techniek-chirp-4.svg)

De **FFT** (Fast Fourier Transform) analyseert de toon en geeft een spectrum met 4096 bins. De bin waar de energie geconcentreerd is = het symboolnummer.

### Fouttolerantie: Processing Gain

De kracht van LoRa zit in redundantie. Bij SF12 worden 12 bits verspreid over 4096 frequentiestappen. Dit is **341× meer bandbreedte dan strikt nodig**. Deze "processing gain" (~36 dB) maakt detectie onder de ruisvloer mogelijk.

## Samenvatting

De complete keten van tekst naar radiosignaal:

Pipeline flow diagram

![Diagram 5 bij techniek-chirp](../../images/techniek-chirp-5.svg)
