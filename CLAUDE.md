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

## The repo on one screen

```
├── nl/                  Dutch chapters (source)
│   ├── gebruik/         usage, hardware, regulations, privacy
│   ├── techniek/        protocol, packets, encryption, repeaters
│   ├── platform/        platform families, chip selection
│   ├── libraries/       external libraries, dependencies
│   │   ├── core/        one chapter per core library
│   │   └── other/       supporting libraries, grouped by function
│   ├── naslag/          terminology, references, links
│   └── project/         about DOMCA, GitHub overview
├── en/                  English chapters (translation, 1-to-1 mirror)
│   ├── usage/
│   ├── technical/
│   ├── platform/
│   ├── libraries/
│   │   ├── core/
│   │   └── other/
│   ├── reference/
│   └── project/
├── images/
│   ├── nl/              diagrams (SVG) and photos for the NL chapters
│   └── en/              diagrams (SVG) and photos for the EN chapters
├── tools/               recalculation scripts for the technical chapters
├── README.md            bilingual landing page
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
- **Slugs are English, kebab-case, without a section prefix, and identical
  in both languages.** Only the directory name differs: `gebruik` ↔ `usage`,
  `techniek` ↔ `technical`, `naslag` ↔ `reference`, `platform` ↔ `platform`,
  `libraries` ↔ `libraries`, `project` ↔ `project`. So
  `nl/techniek/packet-structure.md` ↔ `en/technical/packet-structure.md`.
- **`libraries/` is the only section with a third level.** Its chapters live
  in `libraries/core/` and `libraries/other/`; those subdirectory names are
  identical in both languages. The two overview chapters,
  `libraries/introduction.md` and `libraries/dependencies.md`, stay on the
  second level.
- **A third level appears in the README indexes as a nested bullet** under a
  bold group label that names the subdirectory — *Core libraries* for
  `libraries/core/`, *Supporting libraries* for `libraries/other/`. That label
  is deliberately not a link: it is the placeholder standing in for the
  subdirectory, so the entry still reads as a group heading if the nested
  level is flattened. `README.md` in the repo root shows the same
  subdirectories in its structure tree.
- **Two tables of contents.** `nl/README.md` and `en/README.md` list the
  same chapters in the same order.
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
  `libraries/other/`): `../../../images/nl/<slug>-<n>.svg` and
  `../../../images/en/<slug>-<n>.svg`. The image directory itself stays
  flat — no `images/nl/libraries/`.
- Both files always exist and carry the same name. If the diagram contains
  no text, the EN version is an identical copy.
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
  family* for the four build targets, *SoC* for the chip, and *MCU* only
  where the compute core is genuinely the subject. If you deliberately
  deviate because the reader's term is different, spell that out in the
  chapter itself — not silently.

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

Three mandatory checkpoints. All three fall under 🛑 *Stop and ask*:
skipping a checkpoint because the assignment looks clear is itself the
mistake that rule addresses.

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

- **Two orphaned SVGs with a Dutch section prefix.**
  `images/nl/techniek-chirp-2.svg` and `images/en/techniek-chirp-3.svg` do
  not meet the rule that file names are English, and on top of that are
  referenced nowhere — the chirp chapters point at `text-to-chirp-*.svg`.
  Renaming is impossible without colliding with those existing files; they
  ought to be deleted.
- **Conversion artefacts from the HTML→markdown migration.** Stray lines
  such as `Layer stack SVG` in `layer-model.md`, formulas and configuration
  blocks glued onto a single line, and `####` headings where `##` belongs.
  Fix them in the files you touch anyway. `regulations.md` still has
  `####` headings in both languages.
- **Alt texts do not yet meet the project's own rule.** Several chapters
  use `![Diagram 1 bij …](…)`. New chapters get it right; existing ones are
  picked up at the next substantive change.
- **Duplicate and orphaned images.** Some PNGs from the website export are
  identical (`05-group-communication-1.png` and `-2.png`) or are no longer
  referenced anywhere. Check before reusing them.
- **Two naming styles in `images/`.** Legacy PNGs with a number prefix
  (`20-channel-structure-psk-1.png`) alongside SVGs with a chapter slug
  (`channel-structure-1.svg`). New files follow the slug style.
- **The transport code is not a region identifier** — it changes per
  message. A common mistake in summaries of `packet-structure.md` and
  `regions-and-scopes.md`.
- **The firmware default `set dutycycle` is 50 %**, far above H4 (10 %) and
  H5 (0.1 %). That fact must not be lost when shortening `regulations.md`.
- **Not every chapter has a source block yet.** If it is missing, add it
  when you verify the content; leave it empty if you were unable to check
  anything, rather than guessing a version.
- **The generator supports a third directory level.** Confirmed by the client
  on 28 July 2026, on the introduction of `libraries/core/` and
  `libraries/other/`. `html/` and `include/` are absent from this repo, so
  the `MenuBuilder` cannot be read here; the confirmation is the only source
  for this. Sections other than `libraries/` remain flat.
- **Figures counted over the firmware source tree need their counting method
  recorded.** `tools/library-overview.py` holds a token table for this; the
  chapters cite the figure it produces and the table names the search
  pattern. Figures whose method is unknown cannot be reproduced and must not
  be copied over.
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
- **`nl/naslag/terminology.md`** — glossary, authoritative for wording.
- **`nl/naslag/references.md`** — source list.
- **[meshcore-dev/MeshCore](https://github.com/meshcore-dev/MeshCore)** —
  firmware source code, the ground truth for technical chapters.
- **[docs.meshcore.io](https://docs.meshcore.io/)** — official
  documentation.
