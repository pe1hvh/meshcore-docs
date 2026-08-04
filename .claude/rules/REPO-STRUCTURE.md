# Repo structure

*Layout, directory and slug conventions, and where the key files live.*

Loaded unconditionally: these conventions decide where new work goes,
before any file is opened.

Everything under `.claude/` governs how this documentation is written.
Everything outside it is about MeshCore, or about the project itself.

> [!NOTE]
> **The tree itself is in `.claude/REPO-TREE.md`.** It is not a rule file
> and nothing loads it automatically; read it when you add a directory, a
> section or a new chapter. The conventions below are what you cannot
> derive from that tree.

- **NL is the source, EN is the translation.** Substantive changes start in
  the Dutch chapter and land in the English one afterwards.
- **`CLAUDE.md` and `CHANGELOG.md` are English only.** They are project-wide
  documents rather than chapters, so they have no Dutch counterpart; see
  🌐 *Language parity*.
- **Chapter, script, diagram and attachment file names are English**,
  kebab-case, in the Dutch tree as well. Process documents keep their
  conventional upper-case names, in the repo root and under
  `.claude/rules/`: `README.md`, `CHANGELOG.md`, `CLAUDE.md`, `LICENSE`
  and every rule file. This applies to files;
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

## Language of the project-wide documents

`CLAUDE.md`, `CHANGELOG.md` and every file in `.claude/rules/` are maintained
in English and delivered in English, always. They are project-wide documents,
not chapters, so 🌐 *Language parity* does not apply to them: there is no
Dutch counterpart and none should be created. This holds regardless of the
language of the assignment — a request in Dutch still yields an English
`CLAUDE.md`. New entries, new rules and new pitfalls are written in English
straight away, not translated afterwards.

Content-bound language is left exactly as it is: chapter titles, section
names, subtitle lines, quoted chapter text, literal strings and example data
keep the language they have in the repo. `README.md` stays bilingual and is
not covered by this rule.

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
