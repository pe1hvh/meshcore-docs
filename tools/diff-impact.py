#!/usr/bin/env python3
"""Which chapters cite a firmware file that changed between two commits?

Every technical chapter lists the firmware files it was verified against, both
in its `> [!NOTE] **Bron.**` block and in its `## Bronnen` / `## Sources`
section. A chapter therefore has to be re-verified when one of those files
changed between the old pin and the new one. This script produces that list.

Usage:
    git clone https://github.com/meshcore-dev/MeshCore.git
    python3 tools/diff-impact.py MeshCore 03b6ef4 d929643
    python3 tools/diff-impact.py MeshCore 03b6ef4 d929643 --lang nl

Counting method
---------------
* The set of changed files is `git diff --name-only <old> <new>` in the
  MeshCore checkout, so renames count as one deletion plus one addition.
* A citation is any path in the chapter that starts with a top-level directory
  of the firmware repository (`src/`, `examples/`, `variants/`, `arch/`,
  `lib/`, `test/`, `boards/`, `docs/`, `include/`), whether it appears in
  backticks or inside a `https://github.com/meshcore-dev/MeshCore/blob/<ref>/`
  link. A trailing `.` or `,` is stripped.
* Short forms such as `MyMesh.cpp` without a directory are NOT counted: they
  cannot be resolved to one file without guessing.
* A chapter counts once, however often it cites the same file.

The output is a list, not a verdict. A changed file means the chapter has to be
read again, not that its text is wrong.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

TOP = ("src", "examples", "variants", "arch", "lib", "test", "boards", "docs", "include")
PATH_RE = re.compile(
    r"(?:MeshCore/blob/[0-9a-zA-Z._-]+/|`)((?:" + "|".join(TOP) + r")/[A-Za-z0-9_./{},-]+)"
)


def changed_files(checkout: pathlib.Path, old: str, new: str) -> set[str]:
    out = subprocess.run(
        ["git", "-C", str(checkout), "diff", "--name-only", old, new],
        capture_output=True, text=True, check=True).stdout
    return {line.strip() for line in out.splitlines() if line.strip()}


def citations(text: str) -> set[str]:
    found = set()
    for m in PATH_RE.finditer(text):
        ref = m.group(1).rstrip(".,")
        # `ConfigSerializer.{h,cpp}` is shorthand for two files
        brace = re.match(r"(.+)\.\{([^}]+)\}$", ref)
        if brace:
            for ext in brace.group(2).split(","):
                found.add(f"{brace.group(1)}.{ext.strip()}")
        else:
            found.add(ref)
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("checkout", help="path to a MeshCore checkout")
    ap.add_argument("old", help="old pin, e.g. 03b6ef4")
    ap.add_argument("new", help="new pin, e.g. d929643")
    ap.add_argument("--docs", default="docs", help="documentation root (default: docs)")
    ap.add_argument("--lang", default="nl", help="language tree to scan (default: nl)")
    args = ap.parse_args()

    checkout = pathlib.Path(args.checkout)
    if not (checkout / ".git").exists():
        print(f"{checkout} is not a git checkout", file=sys.stderr)
        return 2

    changed = changed_files(checkout, args.old, args.new)
    root = pathlib.Path(args.docs) / args.lang
    chapters = sorted(root.rglob("*.md"))

    hits = []
    for p in chapters:
        refs = citations(p.read_text(encoding="utf-8", errors="replace"))
        touched = sorted(r for r in refs if r in changed)
        if touched:
            hits.append((p.relative_to(root).as_posix(), len(refs), touched))

    print(f"MeshCore {args.old} -> {args.new}: {len(changed)} changed files")
    print(f"{args.lang}: {len(hits)} of {len(chapters)} chapters cite at least one of them\n")
    for rel, total, touched in sorted(hits, key=lambda h: -len(h[2])):
        print(f"{rel:48s} {len(touched):3d}/{total:3d}  {', '.join(touched[:3])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
