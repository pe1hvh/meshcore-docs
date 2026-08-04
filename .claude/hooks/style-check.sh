#!/usr/bin/env bash
# Runs the two grep checks from .claude/rules/STYLE-NUANCE.md over one file.
#
# Wired to PostToolUse on Write|Edit in .claude/settings.json. Reads the hook
# JSON on stdin and takes the path from tool_input.file_path. Exits 2 with the
# hits on stderr when it finds something, so the result reaches Claude instead
# of depending on Claude remembering to run the check.
set -uo pipefail

INPUT=$(cat)
# python3 instead of jq: this repo already requires python3 for tools/, jq is
# not a dependency anywhere else.
FILE=$(printf '%s' "$INPUT" | python3 -c \
  'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' \
  2>/dev/null)
[ -z "$FILE" ] && exit 0
[ -f "$FILE" ] || exit 0

case "$FILE" in
  *nl/*.md) PATTERN='\bkost|\bbetaal|\bgratis' ; EXCLUDE='kost rekenwerk|volledig gratis|gratis te gebruiken|ten koste van' ;;
  *en/*.md) PATTERN='\bcosts?\b|\bpays\b|\bpaid\b|\bexpensive\b|\bfree\b'
            EXCLUDE='payload|free[- ]space|free-form|licen[cs]e-free|free text|free choice|free end|ends free|free use|free frequency|costs computation|costs current|at the cost of' ;;
  *) exit 0 ;;
esac

HITS=$(grep -niE "$PATTERN" "$FILE" | grep -viE "$EXCLUDE" || true)
[ -z "$HITS" ] && exit 0

{
  echo "STYLE-NUANCE rule 1 — possible hits in $FILE:"
  echo "$HITS"
  echo
  echo "Check each against the decision table in .claude/rules/STYLE-NUANCE.md."
  echo "If it falls under the documented exceptions, say so in the delivery."
} >&2
exit 2
