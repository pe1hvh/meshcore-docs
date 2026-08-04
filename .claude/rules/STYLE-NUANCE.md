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

## Rule 1 — the economic register only for what is genuinely consumed or paid

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

**The negation belongs to the same register.** `gratis` / `free` is the
opposite of `kosten` / `cost` and fails the same test: it says that nothing
is given up without saying what *would* have been given up. `is geen gratis
verbetering` / `is not a free improvement` names no mechanism at all — it
only denies one. Name what actually happens instead, or what does not
happen. The word stays where something is literally free of charge or where
`free` carries a technical meaning that has nothing to do with price.

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
| Improves one thing at the expense of another | verbetert niet alles tegelijk | does not improve everything at once |
| Demands nothing extra | vraagt niets extra's | requires nothing extra |
| Has no drawback | heeft geen keerzijde | has no downside |
| Is given up without anything in return | zonder er iets voor terug te krijgen | without getting anything in return |

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
| Een filter is geen gratis verbetering | Een filter verbetert niet alles tegelijk |
| … levert nu gratis het enige in wat de crypto hem te bieden had | … levert nu het enige in wat de crypto hem te bieden had, zonder er iets voor terug te krijgen |
| … is een uitgebreide regioboom dus niet gratis | … verbruikt een uitgebreide regioboom dus merkbaar rekentijd |

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
| A filter is not a free improvement | A filter does not improve everything at once |
| … currently gives away for free the one thing … | … currently gives away the one thing …, without getting anything in return |
| … an elaborate region tree is therefore not free | … an elaborate region tree therefore consumes noticeable computing time |

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

For `gratis` / `free` the exceptions are:

- Literally free of charge: *De kern is volledig gratis* / *The core is
  completely free*, *gratis te gebruiken* / *free to use*.
- `free` in a technical sense that has nothing to do with price:
  *free-space path loss*, *free-form names*, *license-free band*, *free
  text*, *free choice of pins*, *the free end of a resonator*, *the top six
  bits are free*. Dutch uses *vrij* there, not *gratis*, so the ambiguity
  exists only in English.

Note the boundary: *Dit kost rekenwerk* is right and *Het rekenwerk wordt
betaald* is wrong. Same quantity — what failed was the payment metaphor, not
the word itself. In the same way *De kern is volledig gratis* is right and
*geen gratis verbetering* is wrong: the first is a price, the second is a
missing description.

---

## Rule 2 — no invented terms

### Core rule

A term that does not exist in the target language is never created on the
spot, however reasonable the translation looks. Where the field uses the
English word in Dutch as well, the chapter uses the English word. Where a
concept has no name, describe the thing instead of labelling it.

An invented term does real damage because it is indistinguishable from an
established one: it reads as jargon the reader is supposed to know already, it
cannot be looked up, and the next author takes it as precedent. It is the word
equivalent of an unverified figure, and 🔬 *Verifiability* in `CLAUDE.md`
applies to it unchanged — **invent nothing**.

The test is short. Can you name a source that uses this word: a datasheet, a
standard, the firmware, an existing chapter, a technical text in that language?
If not, you made it up. Your own earlier output is not a source.

### Decision table

| Situation | What to do |
|---|---|
| The field uses the English term in Dutch as well | keep the English term, untranslated |
| A term exists in the target language and is in use | use it, and be able to name where |
| The concept has no name in either language | describe it; do not label it |
| The project itself defines the concept | coining is allowed — see the exceptions |
| You are not sure whether the term exists | 🛑 *Stop and ask*; do not translate on the spot |
| The only place the word occurs is your own earlier text | that is not a source; drop the word |

### Examples from this repo

August 2026, `hardware/radio/filters.md`:

| Wrong | Right |
|---|---|
| `Coaxholte` as the row label in the filter type table | `Cavity filter` |
| `Cavity filter (coaxholte)` | `Cavity filter` |
| … in het Nederlands ook coaxholte of coaxiale holteresonator | Het Nederlands kent geen eigen term; ook in Nederlandstalige praktijk heet dit filter cavity filter |

Neither *coaxholte* nor *coaxiale holteresonator* is in use in Dutch. Both were
produced while writing, as literal renderings of *coaxial cavity*, and both
were presented as though they were established. Dutch radio practice calls this
filter a cavity filter. The chapter now says so, and `terminology.md` states
that Dutch has no term of its own, so that no reader goes hunting for one.

The English side needed a correction as well, for a different reason:
`Cavity filter (coaxial cavity)` was accurate, but the bracket existed only to
mirror the invented Dutch one. When an invented term goes, check what was built
on top of it.

**The rule is not "when in doubt, use English".** In the same chapter
*kwartgolfresonator* stays exactly as it is. Dutch antenna literature uses the
*kwartgolf-* compound throughout — *kwartgolfstraler*, *kwartgolfstub*,
*kwartgolf radialen* — and *resonator* is ordinary Dutch technical vocabulary.
The difference with *coaxholte* is attestation, not language:

| Term | Verdict | Why |
|---|---|---|
| *kwartgolfresonator* | keep | regular compound of parts that are in use in Dutch antenna literature |
| *coaxholte* | remove | occurs nowhere but in the text that introduced it |

So the question is never which language a word looks like. It is whether
anyone outside this repository already uses it.

### Exceptions

- **A term the project defines itself.** `frameworklibrary` is this
  documentation's own word, coined because Arduino's *core library* means
  something else. Coining is allowed on three conditions: the chapter defines
  it where it first appears, it lands in both terminology files in the same
  session, and the chapter says why the obvious word was not usable.
- **Firmware identifiers, file names and macros.** Those are names, not
  translations. They are quoted verbatim in backticks and never translated.
- **Ordinary compounds that make no claim to be terms of art.** *zendpad*,
  *ontvangstpad*, *opstelpunt* are plain language. The line: if it would belong
  in `terminology.md`, it needs a source.

### Check

Rule 2 cannot be grepped. It is checked at checkpoint 3 by listing every term
the delivery introduces and naming, per term, the source that uses it or the
chapter that defines it.

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
grep -rniE "\bkost|\bbetaal|\bgratis" nl/
# EN — the exclusions are the technical senses of "free" and the word payload
grep -rniE "\bcosts?\b|\bpays\b|\bpaid\b|\bexpensive\b|\bfree\b" en/ \
  | grep -viE "payload|free[- ]space|free-form|licen[cs]e-free|free text|free choice|free end|ends free"
```

Every hit that is not in the list of correct uses is an error.

---

## Adding new rules

When a further nuance surfaces, add it here as `## Rule 3` with the same four
parts: core rule, decision table, examples from this repo, exceptions. Real
sentences in a *wrong → right* pair carry more weight than a description of
the principle, so lead with those. Note the addition in `CHANGELOG.md` under
`[Unreleased]`, like any other change to a project-wide document.
