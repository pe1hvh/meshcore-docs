#!/usr/bin/env bash
# Packages the changed and new files as one ZIP with the required name.
#
# Usage:  .claude/skills/new-chapter/scripts/package.sh <topic>
# Result: meshcore_docs_<topic>_result.zip in the repo root, containing only
#         files that git reports as new or modified, with their paths from the
#         repo root intact.
set -euo pipefail

TOPIC=${1:-}
if [ -z "$TOPIC" ]; then
  echo "usage: $0 <topic>   e.g. $0 filters" >&2
  exit 1
fi

ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT"
OUT="meshcore_docs_${TOPIC}_result.zip"

mapfile -t FILES < <(git status --porcelain | awk '{print $NF}' | sort -u)
if [ ${#FILES[@]} -eq 0 ]; then
  echo "no changed or new files — nothing to package" >&2
  exit 1
fi

rm -f "$OUT"
printf '%s\n' "${FILES[@]}" | zip -q "$OUT" -@
echo "$OUT"
printf '%s\n' "${FILES[@]}" | sed 's/^/  /'
echo
echo "${#FILES[@]} files. One ZIP per assignment; a new ZIP replaces the previous"
echo "one within the same assignment."
