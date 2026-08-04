# meshcore-docs

Binding rules, conventions and pitfalls for anyone working on this
documentation: editors, translators and AI assistants. They steer
behaviour in **every** task.

Not what MeshCore is, not how the website is built — that is in the
chapters. What the project is and under which licence: `README.md`.
Table of contents: `nl/README.md` and `en/README.md`.

## Mandatory reading before every assignment

Two kinds of document govern work on this repo. `CLAUDE.md` holds the rules
that must apply before any file is opened. `.claude/rules/` holds the rest,
split by subject.

| Document | Covers | Loads |
|---|---|---|
| `CLAUDE.md` (this file) | binding rules, working process, delivery | always |
| `.claude/rules/STYLE-NUANCE.md` | word choice and nuance in NL and EN | always |
| `.claude/rules/REPO-STRUCTURE.md` | layout, directory and slug conventions, key files | always |
| `.claude/rules/PITFALLS.md` | open defects and traps not tied to one file type | always |
| `.claude/rules/CHAPTERS.md` | page structure, text, source attribution, links | on `nl/**/*.md`, `en/**/*.md` |
| `.claude/rules/IMAGES.md` | paths, naming, alt text, SVG convention | on `images/**` |
| `.claude/rules/TERMINOLOGY.md` | glossary, source list, link list | on `nl/naslag/*.md`, `en/reference/*.md` |
| `.claude/rules/TOOLS.md` | recalculation scripts and counting traps | on `tools/**/*.py` |
| `.claude/rules/CHANGELOG-COMMITS.md` | entry format and commit convention | on `CHANGELOG.md` |
| `.claude/REPO-TREE.md` | the current layout, one screen | on request |

The four marked *always* are mandatory reading before any work starts, for
every assignment, however small. **The AI states in its first substantive
response that all four have been read and understood**, on its own line, in
this form:

```text
Mandatory reading: CLAUDE.md, STYLE-NUANCE.md, REPO-STRUCTURE.md and PITFALLS.md read and understood.
```

The five path-scoped files are deliberately outside that statement: they
enter context after it is made, so claiming to have read them at the start
would be untrue. Reading them when the work reaches them is not optional.

Rules:

- The statement is made only after the four files have been opened and read
  in this session. Knowing them from an earlier session does not count.
- Is one missing from the upload or the working directory? Say so, name it,
  and ask for it. That falls under 🛑 *Stop and ask*; do not start.
- Was a rule from any of the nine deliberately not applied? Say which and
  why, in the same response.
- A new rule file joins the table in the session it is created, and the
  statement too if it loads unconditionally.
- **Adding a directory, a section or a new chapter?** Read
  `.claude/REPO-TREE.md` first. It is reference, not a rule, so nothing loads
  it for you.
- **In the chat interface nothing loads automatically.** Path scoping is a
  Claude Code mechanism; in a chat session every file has to be supplied or
  fetched before it can be applied. The same holds for `.claude/hooks/`,
  `.claude/skills/` and `.claude/commands/`: none of them fire here, so what
  a hook would have enforced has to be done by hand and reported.

## Automation

Three mechanisms sit alongside the rules. They run in Claude Code only.

| Where | What | Fires |
|---|---|---|
| `.claude/hooks/session-start.sh` | prints the checkpoint 0 reminder | at session start |
| `.claude/hooks/style-check.sh` | the two grep checks from `STYLE-NUANCE.md`, per file | after every `Write` or `Edit` |
| `.claude/skills/new-chapter/` | the full chapter procedure, the file table and the packaging script | when the task is adding or changing a chapter |
| `.claude/skills/diagram/` | style block, SVG conventions and the render check | when the task is a diagram |
| `.claude/commands/commit-msg.md` | drafts the commit message | when you type `/commit-msg` |

Hooks run regardless of what Claude decides; skills are model-invoked and
only load when the description matches the request. Nothing here replaces a
rule — the delivery checklist still wants the grep result reported, whether a
hook produced it or not.

## Binding rules

Consistency of examples, terminology and CHANGELOG format are equally binding
and live in `.claude/rules/`; they load when the work reaches a matching file.

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
  on an assumption. Checkpoint 2 is therefore not optional, also — and
  especially — for an assignment that looks exhaustive.
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
- **Process documents are English only** and are not covered by parity. Which
  documents those are, and what counts as content-bound language that keeps
  the language it has, is in `.claude/rules/REPO-STRUCTURE.md`.

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

### ✍️ Word choice and nuance

- **`.claude/rules/STYLE-NUANCE.md` is binding and is read before you write.**
  It holds the word-choice rules for both languages, with the corrections
  already made in this repo as reference pairs.
- Rule 1: the economic register — `kosten` / `cost` and its negation
  `gratis` / `free` — only for what is genuinely consumed, paid, or literally
  free of charge. Everywhere else the concrete verb. The passive payment
  metaphor is always wrong.
- Rule 2: no invented terms. A word that does not exist in the target language
  is not created, not even as an obvious-looking translation. Your own earlier
  output is not a source.
- Both rules carry a decision table, exceptions and worked wrong/right pairs
  in the rule file. Do not paraphrase them from memory.
- Before delivering, run the two grep checks from that file over every file
  you touched and report the result under checkpoint 3. Rule 2 has no grep:
  list the terms introduced and name a source per term.

### 🛡️ Existing content

- For every file you touch, inventory what is in it before you change
  anything.
- Whatever is not in the task is not changed, deleted or rewritten.
- No new top-level directories; no renamed or deleted files without an
  explicit instruction.
- Warnings about regulations, duty cycle and encryption in HAM mode are not
  softened, shortened or summarised away.
- The AI disclaimer in `README.md` and `project/about-domca.md` stays.

## Working process in a chat session

Four mandatory checkpoints, all under 🛑 *Stop and ask*.

0. **Mandatory reading** (before anything else) — open and read the four
   unconditional files listed under *Mandatory reading before every
   assignment*, then state that all four have been read and understood, in
   the form given there.
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
- [ ] `.claude/rules/STYLE-NUANCE.md` grep checks run over every file
      touched, result reported
- [ ] Every term the delivery introduces listed with the source that uses
      it, or the chapter that defines it (Rule 2)
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
STOP and ask. That applies to this document and to every file in
`.claude/rules/` too: if a rule contradicts the repo contents, the repo
leads and the rule is updated in the same session.

## Output and delivery conventions

Per file: the path from the repo root, the full content, a short
explanation of what changes and why, and what has **not** changed. NL
first, EN after.

No fragments and no `…unchanged…` markers in markdown deliveries: the files
are pasted into the repo one-to-one.

For more than two files: one ZIP with the directory structure from the repo
root (`nl/`, `en/`, `images/`, …), naming convention
`meshcore_docs_[onderwerp]_result.zip`. At most 1 ZIP per chat.
