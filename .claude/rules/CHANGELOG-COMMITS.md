---
paths:
  - "CHANGELOG.md"
---

# CHANGELOG and commits

*Entry format and commit message convention.*

- `CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/):
  sections `Added` / `Changed` / `Fixed` / `Removed` under `[Unreleased]`.
- Entries name the file paths of **both** language versions and explain
  *why* the change was made, not just what.
- Factual corrections belong under `Fixed` together with the incorrect
  claim — so that readers who know the old text know what was wrong.
- Commits follow Conventional Commits: `docs(regions-and-scopes): …`,
  `fix(regulations): …`, `chore(images): …`. Scope = chapter slug.
