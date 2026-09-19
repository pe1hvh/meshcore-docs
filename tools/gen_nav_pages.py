#!/usr/bin/env python3
"""Genereer awesome-pages .pages-bestanden uit de README-volgorde.

De README van elke taal is de enige bron voor menuvolgorde en menutitels.
Dit script leest docs/<lang>/README.md, leidt daaruit de volgorde af en
schrijft per map een .pages-bestand. Idempotent: twee keer draaien geeft
hetzelfde resultaat.

Gebruik:  python3 tools/gen_nav_pages.py [--docs docs] [--check]
          --check schrijft niets en geeft exitcode 1 als er iets zou wijzigen.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import OrderedDict
from pathlib import Path

GROUP_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$")
BOLD_RE = re.compile(r"^(?P<indent>\s*)-\s+\*\*(?P<title>[^*]+)\*\*")
LINK_RE = re.compile(r"^(?P<indent>\s*)-\s+\[(?P<label>[^\]]+)\]\((?P<href>[^)#]+\.md)\)")
TOP_FILES = ("README.md", "reading-guide.md")


def parse_readme(readme: Path):
    """-> (order, titles): order[dir] = [child, ...], titles[dir] = 'Titel'."""
    order: "OrderedDict[str, list[str]]" = OrderedDict()
    titles: dict[str, str] = {}
    group_title = None
    pending_sub_title = None

    for raw in readme.read_text(encoding="utf-8").splitlines():
        m = GROUP_RE.match(raw)
        if m:
            group_title = m.group("title")
            pending_sub_title = None
            continue
        m = BOLD_RE.match(raw)
        if m:
            pending_sub_title = m.group("title").strip()
            continue
        m = LINK_RE.match(raw)
        if not m:
            continue
        href = m.group("href").strip()
        if href.startswith("../") or href.startswith("http"):
            continue
        parts = href.split("/")
        if len(parts) == 1:
            continue  # los bestand naast de README
        directory = "/".join(parts[:-1])
        filename = parts[-1]
        # registreer elk niveau van het pad
        for depth in range(1, len(parts)):
            parent = "/".join(parts[:depth - 1])
            child = parts[depth - 1]
            order.setdefault(parent, [])
            if child not in order[parent]:
                order[parent].append(child)
        order.setdefault(directory, [])
        if filename not in order[directory]:
            order[directory].append(filename)
        if group_title and "/" not in directory:
            titles.setdefault(directory, group_title)
        if pending_sub_title and "/" in directory:
            titles.setdefault(directory, pending_sub_title)
            pending_sub_title = None
    return order, titles


def render_pages(entries: list[str], title: str | None) -> str:
    lines = []
    if title:
        lines.append(f"title: {title}")
    lines.append("nav:")
    lines.extend(f"  - {e}" for e in entries)
    return "\n".join(lines) + "\n"


def sync_dir(base: Path, rel: str, order, titles, check: bool, warnings: list[str]) -> bool:
    directory = base / rel if rel else base
    listed = order.get(rel, [])
    on_disk = sorted(
        p.name for p in directory.iterdir()
        if (p.is_dir() and not p.name.startswith(".")) or p.suffix == ".md"
    )
    entries = [e for e in listed if (directory / e).exists()]
    missing = [e for e in listed if not (directory / e).exists()]
    for e in missing:
        warnings.append(f"README noemt {rel}/{e} maar dat bestaat niet op schijf")
    if not rel:  # hoofdmap van de taal: README en leeswijzer vooraan
        entries = [f for f in TOP_FILES if (directory / f).exists()] + entries
    extra = [e for e in on_disk if e not in entries and e != ".pages"]
    for e in extra:
        warnings.append(f"{rel}/{e} staat niet in de README; alfabetisch achteraan geplaatst")
    entries += extra

    target = directory / ".pages"
    content = render_pages(entries, titles.get(rel))
    current = target.read_text(encoding="utf-8") if target.exists() else None
    if current == content:
        return False
    if not check:
        target.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    changed = False
    warnings: list[str] = []
    for lang in ("nl", "en"):
        base = Path(args.docs) / lang
        readme = base / "README.md"
        if not readme.exists():
            print(f"FOUT: {readme} ontbreekt", file=sys.stderr)
            return 2
        order, titles = parse_readme(readme)
        for rel in [""] + [d for d in order if d]:
            if not (base / rel).is_dir():
                continue
            changed |= sync_dir(base, rel, order, titles, args.check, warnings)

    for w in sorted(set(warnings)):
        print(f"WAARSCHUWING: {w}")
    if args.check and changed:
        print("FOUT: .pages-bestanden lopen achter op de README", file=sys.stderr)
        return 1
    print("gewijzigd" if changed else "ongewijzigd")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
