# Style & nuance — mandatory reading

Word-choice rules for this repository. **Read this file before creating or
changing any document**, in Dutch as well as in English, and confirm in your
first substantive response that you have read and understood it — see
*Mandatory reading before every assignment* in `CLAUDE.md`.

These are not matters of taste. Every rule below comes from a correction that
was already made in this repo; a new text that ignores them is sent back.

This document is written in English, like `CLAUDE.md` and `CHANGELOG.md`, and
is not translated. Example sentences quoted from chapters keep the language
they have in the repo.

Each rule follows the same layout: **core rule → decision table → examples
from this repo → exceptions**.

---

## Rule 1 — "kosten" / "cost" only for what is genuinely consumed or paid

### Core rule

`kosten` / `cost` is an **economic** word. Use it only where something is
genuinely given up out of a finite supply: money, effort, airtime, current,
computation, memory that can run out.

For anything that *takes time*, *takes up space*, *is required*, *causes
loss* or *demands effort*, use the concrete verb. The generic "cost" is not a
summary there but a missing description: it leaves the reader guessing which
mechanism is meant.

The same applies to the passive payment metaphor. `wordt betaald`,
`de prijs die … betaalt`, `is paid for` and `the price the design pays` are
**always wrong** in this documentation.

### Decision table

| What actually happens | Nederlands | English |
|---|---|---|
| Takes up space (bytes, flash, memory) | neemt … in beslag | takes up |
| Takes time (seconds, milliseconds) | duurt | takes |
| Is necessary for something to work | vereist / … is nodig | requires |
| Demands effort or extra code | vergt / vraagt (extra) | requires / demands |
| Draws on a budget (airtime, current) | verbruikt | consumes |
| Causes loss (dB, packets) | veroorzaakt / introduceert | causes / introduces |
| Yields no result | levert … niet op | gives / yields no … |
| Has consequences for a trade-off | heeft gevolgen voor | has consequences for |
| Forces the other party into something | dwingt … tot | forces … into |
| Is missing from a choice | je mist … | you miss … |

### Examples from this repo

Dutch, as corrected in August 2026:

| Wrong | Right |
|---|---|
| Het rekenwerk wordt betaald | Dit kost rekenwerk |
| De opcode kost één byte | De opcode neemt één byte in beslag |
| Eén bericht kost N transmissies | Eén bericht vereist N transmissies |
| Zero-hop adverts, kosten geen relay-capaciteit | Voor zero-hop adverts is geen relay-capaciteit nodig |
| Kabel is verlies. Op 868 MHz kost dunne coax enkele dB | Kabel introduceert verlies. Op 868 MHz veroorzaakt dunne coax enkele dB verlies |
| Wat een dB in afstand kost staat in … | De invloed van een dB op de afstand wordt besproken in … |
| Een e-inkscherm verversen kost een seconde | Een e-inkscherm verversen duurt een seconde |
| Dat kost flashruimte | Dat neemt flashruimte in beslag |
| Foutafhandeling kost code en geheugen | Foutafhandeling vraagt extra code en geheugen |
| Mislukte retransmissies kosten meer airtime | Mislukte retransmissies verbruiken meer airtime |
| Filteren op regio kost hem geen inzicht | Filteren op regio levert hem geen inzicht op |
| Stilte kost een aanvaller een timeout | Stilte dwingt een aanvaller tot een timeout |
| Dat is de prijs die het ontwerp bewust betaalt | Dat is een nadeel dat het ontwerp bewust accepteert |
| De scheidslijn kost af en toe uitleg | Het onderscheid vraagt af en toe om uitleg |
| … kost het volgen van één van de twee 28 buildtargets | … mis je 28 buildtargets als je maar één van de twee volgt |

English, same mechanisms in the same order:

| Wrong | Right |
|---|---|
| The computation is paid for | This costs computation |
| The opcode costs one byte | The opcode takes up one byte |
| One message costs N transmissions | One message requires N transmissions |
| Zero-hop adverts, cost no relay capacity | Zero-hop adverts require no relay capacity |
| Cable is loss. Thin coax costs several dB | Cable introduces loss. Thin coax causes several dB of loss |
| What a dB costs in distance is in … | The effect of a dB on distance is discussed in … |
| That costs flash space | That takes up flash space |
| Error handling costs code and memory | Error handling requires extra code and memory |
| Failed retransmissions cost more airtime | Failed retransmissions consume more airtime |
| Region filtering costs it no insight | Region filtering gives it no insight |
| Silence costs an attacker a full timeout | Silence forces an attacker into a full timeout |
| That is the price the design knowingly pays | That is a downside the design knowingly accepts |
| … following one of the two costs 28 build targets | … you miss 28 build targets if you follow just one of the two |

### Headings

A heading `Wat het kost` / `What it costs` is the counterpart of `**Waarom.**`
/ `**Why.**`. It names a drawback, not a price.

| Wrong | Right |
|---|---|
| `**Wat het kost.**` | `**De keerzijde.**` |
| `## Wat het kost` | `## De keerzijde` |
| `### Wat dit kost, en wat het niet garandeert` | `### Welke gevolgen dit heeft, en wat het niet garandeert` |
| `### Wat het zou kosten als het er wél was` | `### Welke gevolgen het zou hebben als het er wél was` |
| `**What it costs.**` | `**The downside.**` |
| `## What it costs` | `## The downside` |
| `### What this costs, and what it does not guarantee` | `### What consequences this has, and what it does not guarantee` |
| `### What it would cost if it were there` | `### What consequences it would have if it were there` |

> [!NOTE]
> When renaming a heading, check whether an anchor link points at it
> (`#wat-het-kost`, `#what-it-costs`) and update that link in the same
> session.

### Exceptions — where the word is correct and stays

- `ten koste van` / `at the cost of` — fixed expression.
- Literal money or effort: *In volgorde van moeite en kosten*, *In order of
  effort and cost*, *Zeer betaalbaar*.
- A literal draw on a finite budget:
  - *Een GPS-ontvanger die staat te zoeken kost meer stroom* / *A GPS receiver
    searching for satellites costs more current*
  - *Dat kost rekenwerk bij elke hop* / *That costs computation at every hop*
  - *Elk flood-pakket kost rekenwerk* / *Every flood packet costs computation*

Note the boundary: *Dit kost rekenwerk* is right and *Het rekenwerk wordt
betaald* is wrong. Same quantity — what failed was the payment metaphor, not
the word itself.

---

## Working method for a new or changed document

1. Read this file before you start, and state that you have done so.
2. Write the text.
3. Run the check below over every file you touched.
4. Walk through each hit: does it fall under the exceptions, or under the
   decision table? When in doubt, the decision table wins.
5. Keep NL and EN in step. A correction on one side is carried over to the
   other, unless the two texts diverge in content there — in that case report
   it explicitly instead of translating it silently.

```bash
# NL
grep -rniE "\bkost|\bbetaal" nl/
# EN — exclude payload, which is a false positive
grep -rniE "\bcosts?\b|\bpays\b|\bpaid\b|\bexpensive\b" en/ | grep -vi payload
```

Every hit that is not in the list of correct uses is an error.

---

## Adding new rules

When a second nuance surfaces, add it here as `## Rule 2` with the same four
parts: core rule, decision table, examples from this repo, exceptions. Real
sentences in a *wrong → right* pair carry more weight than a description of
the principle, so lead with those. Note the addition in `CHANGELOG.md` under
`[Unreleased]`, like any other change to a project-wide document.
