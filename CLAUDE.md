# meshcore-docs

Bilingual (NL/EN) documentation about MeshCore: usage, hardware,
regulations and the internals of the LoRa protocol. A DOMCA project
(Dutch Open MeshCore Activity), published at [domca.nl](https://domca.nl).

Repo: `https://github.com/pe1hvh/meshcore-docs` · branch `main` ·
text and diagrams CC BY-SA 4.0, code in `tools/` MIT.

## Purpose of this document

Guidance document for anyone working on this documentation: editors,
translators and AI assistants (Claude) in follow-up sessions. It holds the
binding rules, conventions and pitfalls that steer behaviour in **every**
task.

It does **not** describe what MeshCore is or how it works — that belongs in
the chapters themselves. It does **not** describe how the website is built.
For the table of contents: `nl/README.md` and `en/README.md`.

## Mandatory reading before every assignment

Two documents are mandatory reading before any work on this repo starts, for
every assignment, however small:

| Document | Covers |
|---|---|
| `CLAUDE.md` (this file) | binding rules, conventions, working process, pitfalls |
| `STYLE-NUANCE.md` | word choice and nuance in NL and EN, with the corrections already made |

**The AI states in its first substantive response that both have been read and
understood**, before anything else, on its own line and in this form:

```text
Mandatory reading: CLAUDE.md and STYLE-NUANCE.md read and understood.
```

Rules:

- The statement is only made after the files have actually been opened and
  read in this session. Knowing them from an earlier session does not count —
  they may have changed.
- Is one of them missing from the upload or the working directory? Then say
  so, name which one, and ask for it. That falls under 🛑 *Stop and ask*; do
  not start on the assignment.
- Was a rule from either document deliberately not applied? Say which one and
  why, in the same response.
- A new project-wide document with rules in it is added to this table in the
  same session in which it is created.

## The repo on one screen

```
├── nl/                  Dutch chapters (source)
│   ├── README.md        table of contents
│   ├── reading-guide.md sections and the background each one assumes
│   ├── gebruik/         usage, hardware, regulations, privacy
│   ├── techniek/        protocol, packets, encryption, repeaters
│   │   └── roomserver/  login, posts, synchronisation, limits
│   ├── ontwerp/         how the firmware is put together
│   │   ├── logisch/     roles, components, contracts, variability
│   │   └── technisch/   classes, platform realisation, build system
│   ├── companion/       how the firmware is put together
│   │   ├── logisch/     roles, components, contracts, variability
│   │   └── technisch/   classes, platform realisation, build system
│   ├── platform/        platform families, chip selection
│   ├── hardware/        what a node is made of
│   │   ├── radio/       transceiver, antenna, link budget
│   │   ├── interfaces/  BLE, WiFi, USB serial, I²C, SPI
│   │   └── peripherals/ display, GPS, buttons and LEDs
│   ├── libraries/       external libraries, dependencies
│   │   ├── core/        one chapter per core library
│   │   └── other/       supporting libraries, grouped by function
│   ├── naslag/          terminology, references, links
│   └── project/         about DOMCA, GitHub overview
├── en/                  English chapters (translation, 1-to-1 mirror)
│   ├── README.md
│   ├── reading-guide.md
│   ├── usage/
│   ├── technical/
│   │   └── roomserver/
│   ├── design/
│   │   ├── logical/
│   │   └── technical/
│   ├── companion/
│   │   ├── logical/
│   │   └── technical/
│   ├── platform/
│   ├── hardware/
│   │   ├── radio/
│   │   ├── interfaces/
│   │   └── peripherals/
│   ├── libraries/
│   │   ├── core/
│   │   └── other/
│   ├── reference/
│   └── project/
├── images/
│   ├── nl/              diagrams (SVG) and photos for the NL chapters
│   └── en/              diagrams (SVG) and photos for the EN chapters
├── tools/               recalculation scripts for the technical chapters
├── README.md            bilingual switchboard: language choice, disclaimer,
│                        layout, licence, community
├── CHANGELOG.md         Keep a Changelog + semver (English only)
└── LICENSE              CC BY-SA 4.0
```

- **NL is the source, EN is the translation.** Substantive changes start in
  the Dutch chapter and land in the English one afterwards.
- **`CLAUDE.md` and `CHANGELOG.md` are English only.** They are project-wide
  documents rather than chapters, so they have no Dutch counterpart; see
  🌐 *Language parity*.
- **File names are always English**, kebab-case, in the Dutch tree as well
  and for scripts, diagrams and attachments too. This applies to files;
  directory names are out of scope and follow the section mapping below. If
  no common English term exists, use the firmware term.
- **Directory names are lower case, a single word and carry no hyphen.** They
  follow the section mapping and are therefore language-specific at every
  level: `gebruik` ↔ `usage`, `techniek` ↔ `technical`, `naslag` ↔
  `reference`, `ontwerp` ↔ `design`, `logisch` ↔ `logical`, `technisch` ↔
  `technical`. Where the word is the same in both languages the two names
  coincide: `platform`, `hardware`, `libraries`, `project`, `radio`,
  `interfaces`. A section whose name is two words in prose contracts in the
  path: the Room Server section lives in `roomserver/` while its group label
  in the README indexes reads *Room Server*. Files inside such a directory
  keep kebab-case as normal (`roomserver/login-and-acl.md`), and so do the
  diagrams that belong to it (`room-server-login-1.svg`), because those are
  files and not directories.
- **Four third-level directories predate the rule above and carry an English
  name in the Dutch tree too**: `libraries/core/`, `libraries/other/`,
  `hardware/peripherals/` and `techniek/roomserver/`. They are not renamed
  without an explicit instruction — a rename breaks every relative link and
  every image path in the chapters concerned. `ontwerp/logisch/` and
  `ontwerp/technisch/` are the first third-level directories that do follow
  the mapping.
- **Slugs are English, kebab-case, without a section prefix, and identical
  in both languages.** Only the directory name differs: `gebruik` ↔ `usage`,
  `techniek` ↔ `technical`, `naslag` ↔ `reference`, `platform` ↔ `platform`,
  `hardware` ↔ `hardware`, `libraries` ↔ `libraries`, `project` ↔ `project`,
  `ontwerp` ↔ `design`. So `nl/techniek/packet-structure.md` ↔
  `en/technical/packet-structure.md`.
- **Four sections have a third level: `libraries/`, `hardware/`, `techniek/`
  ↔ `technical/` and `ontwerp/` ↔ `design/`.** Their chapters live in
  `libraries/core/`, `libraries/other/`, `hardware/radio/`,
  `hardware/interfaces/`, `hardware/peripherals/`, `techniek/roomserver/` ↔
  `technical/roomserver/` and `ontwerp/logisch/` ↔ `design/logical/` plus
  `ontwerp/technisch/` ↔ `design/technical/`. The first six subdirectory
  names are identical in both languages; the two under `ontwerp/` ↔
  `design/` follow the section mapping. In `libraries/` and `hardware/` the overview chapters —
  `libraries/introduction.md`, `libraries/dependencies.md` and
  `hardware/introduction.md` — stay on the second level. **`roomserver/` is
  the exception: its `introduction.md` sits inside the subdirectory**, so the
  whole section moves as one. That deviation was a client decision, not a
  pattern to copy. No further level is added without an explicit
  instruction.
- **A third level appears in the README indexes as a nested bullet** under a
  bold group label that names the subdirectory — *Core libraries* for
  `libraries/core/`, *Supporting libraries* for `libraries/other/`, *Radio*,
  *Interfaces* and *Peripherals* for the three under `hardware/`, and *Room
  Server* for `techniek/roomserver/`. That label
  is deliberately not a link: it is the placeholder standing in for the
  subdirectory, so the entry still reads as a group heading if the nested
  level is flattened. `README.md` in the repo root shows the same
  subdirectories in its structure tree.
- **Two tables of contents.** `nl/README.md` and `en/README.md` list the
  same chapters in the same order.
- **One chapter sits outside a section directory**: `nl/reading-guide.md` ↔
  `en/reading-guide.md`. It shares its link base with the index next to it,
  so both files point at the chapters in exactly the same way and cannot
  drift apart. It is reached from three places: the root `README.md`, a
  pointer line in the index above the first `##` section, and an index entry
  under *Project* / *Project* — that entry is what puts it in the site menu,
  even though the file itself does not live in `project/`. The pointer line
  deliberately carries no `##` heading of its own, so it adds no section to
  the menu. This is an exception granted by the client, not a pattern to
  copy; no further chapter is placed at the top of a language tree without an
  explicit instruction.
- **The narrative belongs to the language trees.** The introduction, the
  section table with assumed knowledge, the chapter and diagram counts and
  the four properties under *What this documentation aims for* live in
  `reading-guide.md`, once per language. The root `README.md` carries only
  what is language-neutral or has to be seen before the language choice: the
  badges, the two language links, the AI disclaimer in both languages, the
  layout tree, errata, licence and community. Do not restore a Dutch and an
  English narrative section there.
- **No shared image directory.** Every diagram exists twice, under the same
  file name: `images/nl/<slug>-<n>.svg` and `images/en/<slug>-<n>.svg`. Even
  when it contains no text.

## What this documentation aims for

Four properties set this project apart from an ordinary manual. They are
not a stylistic preference but the reason it exists:

1. **Byte by byte.** Packets are written out with real values, never with
   `XX XX`.
2. **Verified against the source code.** Technical claims state the
   firmware version, commit and the file they were checked against.
3. **Recomputable.** Worked examples can be reproduced with the scripts in
   `tools/`.
4. **Including what does *not* work.** Stub implementations, `TODO`s in the
   firmware and undocumented commands are simply included.

## Document conventions

### Page structure

- `#` H1 = page title.
- Below it an italic subtitle line in capitals, separated by `·` — for
  example `*HEADER · ROUTE · PATH · PAYLOAD · REGIO-SCOPE*`.
- Then an introductory paragraph (2–5 lines) summarising the whole page.
- Sections with `##`, subsections with `###`. **No `####`** at chapter
  level.
- Technical chapters end with `## Bronnen` (NL) / `## Sources` (EN).
- Every EN chapter ends with the line:
  `Translated from Dutch by Anthropic Claude`.

### Text

- New prose hard-wrapped at ±80 columns. (Older chapters still have long
  lines; wrap what you touch, do not reformat the rest unasked.)
- GitHub alerts: `> [!NOTE]` for clarification and source attribution,
  `> [!WARNING]` for risks and legal warnings.
- Tables with a separator row `|---|---|`; italic rows for fields that are
  strictly speaking out of scope (see `packet-structure.md`).
- Code blocks always with a language tag: ` ```text `, ` ```python `,
  ` ```bash `, ` ```cpp `. The list is not exhaustive; `cpp` is in use in
  `regions-in-practice.md`, `regions-and-scopes.md` and throughout
  `libraries/`.
- **Code quoted from the firmware** carries a line above the block naming the
  file and the line numbers, for example `` `src/Identity.cpp` r.17-23 ``.
  Excerpts are at most ±15 lines and are copied verbatim — nothing rewritten,
  nothing "clarified". Omitted lines become `// ...`. If a fragment is
  unreadable without context, pick a different fragment rather than editing
  it. Line numbers are those of the commit named in the source block; if the
  assignment states different ones, that contradiction goes to the client
  under 🛑 *Stop and ask*.
- Firmware identifiers, file names, commands and hex values in
  `` `backticks` ``.
- Matter-of-fact tone, no marketing language, no superlatives.

### Source attribution in technical chapters

At the top, directly after the introduction:

```markdown
> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `a3a1aa5`, 19 juli 2026 — bestanden
> `src/Packet.h`, `src/Dispatcher.cpp`, en de officiële
> `docs/packet_format.md`.
```

At the bottom a `## Bronnen` list with links to
`https://github.com/meshcore-dev/MeshCore/blob/<commit>/<path>`.

Pin the commit in the link, not `main` — `main` moves and makes the source
attribution inaccurate within weeks.

### Images

- Path from an NL chapter: `../../images/nl/<slug>-<n>.svg`.
- Path from an EN chapter: `../../images/en/<slug>-<n>.svg`.
- Path from a chapter on the third level (`libraries/core/`,
  `libraries/other/`, `hardware/radio/`, `hardware/interfaces/`,
  `hardware/peripherals/`, `techniek/roomserver/`, `ontwerp/logisch/` ↔
  `design/logical/`, `ontwerp/technisch/` ↔ `design/technical/`):
  `../../../images/nl/<slug>-<n>.svg` and
  `../../../images/en/<slug>-<n>.svg`. The image directory itself stays
  flat — no `images/nl/libraries/`.
- Both files always exist and carry the same name. If the diagram contains
  no text, the EN version is an identical copy.
- **`images/` is flat.** A slug that occurs in more than one section — such as
  `introduction` — therefore cannot use `<slug>-<n>.svg` twice. The second
  diagram is named after what it shows, not after the chapter it sits in:
  `node-blockdiagram-1.svg` for `hardware/introduction.md`. Image files are
  never moved or renamed to resolve this; only new files pick a different
  name.
- Alt text is descriptive and readable on its own — not
  `Diagram 1 bij layer-model`.
- **New diagrams as SVG**, not as PNG.
- SVG convention (see `images/nl/layer-model-1.svg` as a reference):
  `style="width:100%;margin:1rem 0"`, a `viewBox`, an embedded `<style>`
  with `:root` variables plus an `@media (prefers-color-scheme: dark)`
  block, all colours via `var(--…)`, text in `'JetBrains Mono',monospace`.

### Links

- Relative links within the same language tree. **Never** from `nl/` to
  `en/` or the other way round.
- References to the firmware point at the concrete file in
  `meshcore-dev/MeshCore`, not at the repo root.

## Binding rules

### 🛑 Stop and ask

**This rule overrides every other rule in this chapter.** If it is broken,
the rest of the work is worthless, however correctly it was otherwise
carried out. No assignment, deadline or apparent self-evidence sets it
aside.

- **When sources contradict each other: stop and ask.** Never settle it
  yourself, not even when one reading seems far more likely. Report which
  source says what and put the choice to the client.
- **An explicit signal is never explained away.** If something in the
  assignment, in this document or in the repo conflicts with your own
  observation, then your observation is the suspect — not the signal.
  "That will be a typo" and "that must be outdated" are forbidden
  conclusions.
- **Take a complete inventory.** Empty directories, hidden files and
  directory entries in an archive are part of the inventory. A method that
  does not show them is not an inventory: `find -type f` misses empty
  directories, `unzip -l` does not.
- **Read the client's words literally.** Plural means plural. Do not hold
  an instruction up against your own framing of the problem; when the two
  clash, the instruction wins.
- **An answer you were given is binding.** If you ask a question, you carry
  out the answer — especially when it goes against your own assumption.
  Otherwise you should not have asked.
- **Doubt belongs before the building.** Putting an open point underneath a
  delivery is not asking a question: by then the work has already been done
  on an assumption.
- **Checkpoint 2 is not optional.** Impact analysis and confirmation before
  the first line is written, also — and especially — for an assignment that
  looks exhaustive. The more detailed the assignment, the sharper the
  contradictions inside it.
- **A rule you record here, you apply to the repo in the same session.** If
  that is not possible, report it up front with the reason. Deciding for
  yourself that something is "a separate assignment" is not the executor's
  call.

### 🌐 Language parity

- **Every substantive change lands in both languages**, in the same
  session.
- Heading structure, table columns, alerts, images and ordering are
  identical in NL and EN. Only the language differs.
- The slug stays the same; only the directory name differs.
- New or renamed chapter → update `nl/README.md` **and** `en/README.md`, at
  the same position in the same section.
- If a correction only affects the translation (language error, missing
  section), the EN version may change on its own — report that explicitly.
- **`CLAUDE.md` and `CHANGELOG.md` are maintained in English and delivered
  in English, always.** They are project-wide documents, not chapters, so
  language parity does not apply to them: there is no Dutch counterpart and
  none should be created. This holds regardless of the language of the
  assignment — a request in Dutch still yields an English `CLAUDE.md` and
  `CHANGELOG.md`. New entries, new rules and new pitfalls are written in
  English straight away, not translated afterwards. Content-bound language
  is left exactly as it is: chapter titles, section names, subtitle lines,
  quoted chapter text, literal strings and example data keep the language
  they have in the repo. `README.md` stays bilingual and is not covered by
  this rule.

### 🔬 Verifiability

- Technical claims are checked against the MeshCore source code, not
  against forum posts or earlier chapters.
- State the firmware version, commit hash, date and files consulted.
- No packet examples with `XX XX`: real, recomputable values.
- If you cannot verify something, write it down as unconfirmed. **Invent
  nothing** — the disclaimer about AI hallucinations in `README.md` is
  there for a reason.
- Firmware defaults change from release to release. When touching a
  chapter: check whether the version stated is still current.
- Figures that do **not** come from the firmware repo (datasheets from
  Raspberry Pi, Espressif, Nordic, ST; the web flasher; web shops) are
  marked as an external source, with a footnote on the table or the figure.

### 🧮 Consistency of examples

- The example data is the same project-wide: region `nl-ov-zwo`, channel
  `#zwolle`, sender `PE1HVH`, timestamp `1785412800`, text
  `"Op Woensdag a.s. Blauwvingerdagen"`.
- If an example changes, `tools/example-calculation.py` changes with it —
  and vice versa.
- Every figure in a technical chapter must be reproducible with a script in
  `tools/`, or explicitly marked as an external source. If the text does
  not match the script output, the text is wrong.
- If a chapter generates its tables from the firmware, it ships its own
  script. Naming convention: English, kebab-case, such as
  `tools/example-calculation.py` and `tools/dm-example.py`.

### 📚 Terminology and reference

- `nl/naslag/terminology.md` and `en/reference/terminology.md` are sorted
  **alphabetically** — new terms are inserted in place, not tacked on at
  the bottom.
- If you introduce an abbreviation in a chapter, it also goes into the
  terminology table (both languages).
- New external source → `naslag/references.md` / `reference/references.md`;
  new tool or website → `naslag/links.md` / `reference/links.md`.
- **Adopt the firmware's wording where it is unambiguous.** The repo speaks
  of *platforms* (`ESP32_PLATFORM`, `NRF52_PLATFORM`, `RP2040_PLATFORM`,
  `STM32_PLATFORM`), not of microcontrollers. Use *platform* and *platform
  family* for the four build targets, *MCU* for the chip the firmware runs
  on, and *SoC* for an MCU that is packaged together with memory and usually
  a radio. The difference is explained in `hardware/introduction.md`; do not
  invent a third word for it. If you deliberately
  deviate because the reader's term is different, spell that out in the
  chapter itself — not silently.

### ✍️ Word choice and nuance

- **`STYLE-NUANCE.md` is binding and is read before you write.** It holds the
  word-choice rules for both languages, with the corrections already made in
  this repo as reference pairs.
- Rule 1 in short: `kosten` / `cost` only for what is genuinely consumed or
  paid — money, effort, airtime, current, computation. Everywhere else the
  concrete verb: *neemt in beslag*, *duurt*, *vereist*, *vergt*, *verbruikt*,
  *veroorzaakt* / *takes up*, *takes*, *requires*, *demands*, *consumes*,
  *causes*. The passive payment metaphor (`wordt betaald`, `is paid for`) is
  always wrong. The decision table, the exceptions and the heading convention
  are in `STYLE-NUANCE.md`; do not paraphrase them from memory.
- Before delivering, run the two grep checks from that document over every
  file you touched, and report the result under checkpoint 3.

### 🛡️ Existing content

- For every file you touch, inventory what is in it before you change
  anything.
- Whatever is not in the task is not changed, deleted or rewritten.
- No new top-level directories; no renamed or deleted files without an
  explicit instruction.
- Warnings about regulations, duty cycle and encryption in HAM mode are not
  softened, shortened or summarised away.
- The AI disclaimer in `README.md` and `project/about-domca.md` stays.
- When in doubt: **STOP and ask.**

### 📋 CHANGELOG and commits

- `CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/):
  sections `Added` / `Changed` / `Fixed` / `Removed` under `[Unreleased]`.
- Entries name the file paths of **both** language versions and explain
  *why* the change was made, not just what.
- Factual corrections belong under `Fixed` together with the incorrect
  claim — so that readers who know the old text know what was wrong.
- Commits follow Conventional Commits: `docs(regions-and-scopes): …`,
  `fix(regulations): …`, `chore(images): …`. Scope = chapter slug.

## Working process in a chat session

Four mandatory checkpoints. All four fall under 🛑 *Stop and ask*:
skipping a checkpoint because the assignment looks clear is itself the
mistake that rule addresses.

0. **Mandatory reading** (before anything else) — open and read `CLAUDE.md`
   and `STYLE-NUANCE.md`, then state that both have been read and understood,
   in the form given under *Mandatory reading before every assignment*.
1. **Source verification** (first, always) — inventory all available
   sources, including empty directories and directory entries in an
   archive; report which ones you see with timestamps; ask which one leads.
   Start every substantive response with *"Working with: [file name]
   (uploaded [timestamp])"*.
2. **Impact analysis** (before implementation) — which files and
   directories are affected (NL, EN, README indexes, `images/nl/`,
   `images/en/`, `terminology.md`, `CHANGELOG.md`, `tools/`), what is in
   them now, and which contradictions the assignment contains; ask for
   confirmation before you start.
3. **Delivery validation** (before delivery) — walk through the checklist
   below and report the result per item.

**Delivery checklist:**

- [ ] Mandatory reading stated at the start of the session
- [ ] `STYLE-NUANCE.md` grep checks run over every file touched, result
      reported
- [ ] NL and EN have the same sections, tables, alerts and images
- [ ] EN file ends with `Translated from Dutch by Anthropic Claude`
- [ ] All relative links point to existing files
- [ ] Every diagram exists in `images/nl/` **and** `images/en/`, under the
      same name
- [ ] New terms appear alphabetically in both terminology files
- [ ] Source block and `## Bronnen` match the firmware version and commit
      used; the links pin that commit
- [ ] Figures match the output of `tools/`, or are marked as an external
      source
- [ ] README index updated if chapters were added or renamed
- [ ] `CHANGELOG.md` entry under `[Unreleased]`, both languages named
- [ ] No leftover HTML→markdown conversion artefacts

**File source priority** (high to low): most recent upload > individual
files (by upload time) > the repo on GitHub (only on request or when
uploads are missing) > chat history (never as a text source). On conflict:
STOP and ask. That applies to this document too: if `CLAUDE.md` contradicts
the repo contents, the repo leads and `CLAUDE.md` is updated in the same
session.

## Output and delivery conventions

Per file: the path from the repo root, the full content, a short
explanation of what changes and why, and what has **not** changed. NL
first, EN after.

No fragments and no `…unchanged…` markers in markdown deliveries: the files
are pasted into the repo one-to-one.

For more than two files: one ZIP with the directory structure from the repo
root (`nl/`, `en/`, `images/`, …), naming convention
`meshcore_docs_[onderwerp]_result.zip`. At most 1 ZIP per chat.

## Known pitfalls

- **Alt texts do not yet meet the project's own rule.** Several chapters
  use `![Diagram 1 bij …](…)`. New chapters get it right; existing ones are
  picked up at the next substantive change.
- **Two naming styles in `images/`.** Legacy PNGs with a number prefix
  (`20-channel-structure-psk-1.png`) alongside SVGs with a chapter slug
  (`channel-structure-1.svg`). New files follow the slug style.
- **The firmware default `set dutycycle` is 50 %**, far above H4 (10 %) and
  H5 (0.1 %). That fact must not be lost when shortening `regulations.md`.
- **Not every chapter has a source block yet.** If it is missing, add it
  when you verify the content; leave it empty if you were unable to check
  anything, rather than guessing a version.
- **Figures counted over the firmware source tree need their counting method
  recorded.** `tools/library-overview.py` holds a token table for this; the
  chapters cite the figure it produces and the table names the search
  pattern. Figures whose method is unknown cannot be reproduced and must not
  be copied over.
- **Counting build targets by the name of the `[env:…]` section is wrong.**
  A section named `…_room_server` is not proof that the room server is
  compiled, and a target that does compile it need not carry the name —
  `Generic_ESPNOW_room_svr` does not. Count on `build_src_filter` containing
  `../examples/simple_room_server`, and resolve `extends` while doing so: six
  ikoka targets inherit that filter from a shared base section that is not an
  `[env:…]` itself. The naive name count gives 70 targets in 66 directories,
  the correct one 73 in 65. `tools/room-server-overview.py` does it the right
  way; the same trap applies to any other role.
- **`technical` occurs on two levels in the English tree.**
  `en/technical/` is the section that mirrors `nl/techniek/`;
  `en/design/technical/` is the subsection that mirrors
  `nl/ontwerp/technisch/`. They are unrelated. A relative link or an image
  path that resolves one level too high lands in the wrong one without
  erroring, so check the depth rather than the name.
- **`tools/design-overview.py` resolves both inheritance mechanisms.**
  PlatformIO sections inherit through `extends` *and* splice text through
  `${section.option}`; following only one of the two loses 28 of the 508
  build targets. The script also strips CRLF first, because three variant
  files use Windows line endings, and it skips commented-out `-D` macros —
  `MESH_DEBUG` appears 387 times in the ini files and is genuinely enabled in
  36 targets. Its room server count (73 targets in 65 directories) matches
  `tools/room-server-overview.py`, which is the cross-check that the resolver
  is right.
- **MeshCore's `main` moves daily.** Note the commit you are basing
  yourself on, and do not assume that counts from an earlier session still
  hold. Between `a3a1aa5` (19 July 2026) and `03b6ef4` (28 July 2026), for
  instance, two build-target counts already shifted.

## References

- **`nl/README.md` · `en/README.md`** — table of contents per language.
- **`README.md`** — landing page, structure overview, licence, disclaimer.
- **`CHANGELOG.md`** — what changed per revision and why.
- **`tools/example-calculation.py`** — reproduces the project-wide example
  data; referenced from `README.md`.
- **`tools/dm-example.py`** — reproduces the worked example in
  `direct-messages.md`.
- **`tools/room-server-overview.py`** — reproduces the counts and the worked
  push/ACK example in `techniek/roomserver/`.
- **`tools/design-overview.py`** — resolves the build matrix and reproduces
  every figure in `ontwerp/` ↔ `design/`.
- **`nl/naslag/terminology.md`** — glossary, authoritative for wording.
- **`nl/naslag/references.md`** — source list.
- **[meshcore-dev/MeshCore](https://github.com/meshcore-dev/MeshCore)** —
  firmware source code, the ground truth for technical chapters.
- **[docs.meshcore.io](https://docs.meshcore.io/)** — official
  documentation.
