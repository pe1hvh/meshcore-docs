---
description: Draft a Conventional Commits message for the staged changes, in the format required by .claude/rules/CHANGELOG-COMMITS.md
---

Read `.claude/rules/CHANGELOG-COMMITS.md`, then inspect the staged changes
with `git diff --cached --stat` and `git diff --cached`.

Produce two things:

1. **A subject line** in Conventional Commits form, scope = chapter slug or
   the area touched: `docs(filters): …`, `fix(regulations): …`,
   `chore(rules): …`. Imperative mood, no trailing period.

2. **A body** that explains *why*, not just what. Name the file paths of both
   language versions where both changed. If the commit corrects something,
   state the incorrect claim as well, so a reader who knows the old text knows
   what was wrong.

Do not commit anything. Output the message for review.
