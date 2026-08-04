---
name: new-chapter
description: Use when adding, splitting, renaming or substantially rewriting a chapter in this bilingual MeshCore documentation repo — anything that creates or moves a file under nl/ or en/. Walks the mandatory checkpoints, lists every file a chapter touches in both languages, and packages the result under the required ZIP name.
---

# Adding or changing a chapter

A chapter is never one file. The count below is what a single new chapter
actually touched the last time this was done; the checklist exists because the
first impact analysis missed three of them.

## Before writing anything

Checkpoint 1 and checkpoint 2 from `CLAUDE.md` are not optional here.

**Checkpoint 1 — source verification.** Inventory what you have. If the
firmware is involved, pin the commit and say which one. Report contradictions
between the assignment and the source now, not after the delivery.

**Checkpoint 2 — impact analysis.** Present the table below filled in, with
what is currently in each file, and ask for confirmation. Do not write a line
before the answer comes back.

| File | When |
|---|---|
| `nl/<section>/<slug>.md` | always — Dutch is the source |
| `en/<section>/<slug>.md` | always — same slug, section name translated |
| `images/nl/<slug>-<n>.svg` | if the chapter has diagrams |
| `images/en/<slug>-<n>.svg` | always when the NL one exists, even without text |
| `nl/README.md`, `en/README.md` | new or renamed chapter, same position |
| `nl/reading-guide.md`, `en/reading-guide.md` | chapter count, diagram count, and the section row |
| `nl/naslag/terminology.md`, `en/reference/terminology.md` | every term or abbreviation the chapter introduces |
| `nl/naslag/references.md`, `en/reference/references.md` | every external source cited |
| `nl/naslag/links.md`, `en/reference/links.md` | new tool or website |
| `tools/<name>.py` | if the chapter carries figures that must be reproducible |
| `CHANGELOG.md` | always, under `[Unreleased]`, both language paths named |

The four that get forgotten: both reading guides and both reference lists.

## While writing

Read `.claude/rules/CHAPTERS.md` for page structure and source attribution,
and `.claude/rules/IMAGES.md` before touching a diagram. Both are path-scoped,
so in Claude Code they load when you open a matching file; in a chat session
you have to fetch them yourself.

Use `scripts/terminology-insert.py` for glossary rows rather than editing by
hand. `en/reference/terminology.md` is not consistently sorted — it has two
separate I-clusters and rows left in their Dutch sort position — so eyeballing
the alphabet gets it wrong. The script reports the neighbours it inserted
between; check them.

## Before delivering

Checkpoint 3. Walk the delivery checklist in `CLAUDE.md` and report per item,
including the two grep checks from `.claude/rules/STYLE-NUANCE.md`. The
PostToolUse hook runs those per file as you write, but the checklist still
wants the result reported.

Then `scripts/package.sh <topic>` for the ZIP. It packs from the repo root and
applies the required name.
