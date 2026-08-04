#!/usr/bin/env bash
# Prints the checkpoint 0 reminder at session start.
#
# CLAUDE.md requires four files to be read and the reading to be stated before
# any work begins. Claude Code loads them, but loading is not the same as
# stating it, and a session that skips the statement also tends to skip the
# checkpoints. This hook makes the omission visible immediately.
cat <<'MSG'
Checkpoint 0 — mandatory reading, before anything else:
  CLAUDE.md
  .claude/rules/STYLE-NUANCE.md
  .claude/rules/REPO-STRUCTURE.md
  .claude/rules/PITFALLS.md
State on its own line, in the first substantive response:
  Mandatory reading: CLAUDE.md, STYLE-NUANCE.md, REPO-STRUCTURE.md and PITFALLS.md read and understood.
Then checkpoint 1 (source verification) and checkpoint 2 (impact analysis,
with confirmation) before the first line is written.
MSG
