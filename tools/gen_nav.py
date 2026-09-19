#!/usr/bin/env python3
"""Genereer het nav-blok en de sectievertalingen in mkdocs.yml uit de README's.

De README van elke taal blijft de enige bron voor menuvolgorde en sectietitels.
Dit script schrijft twee blokken in mkdocs.yml, tussen markeringen:

    # BEGIN NAV  ...  # END NAV                  het menu, in README-volgorde
    # BEGIN NAV_TRANSLATIONS ... # END ...       de Engelse sectietitels

Waarom niet met .pages-bestanden: de i18n-plugin bouwt de navigatie per taal
opnieuw op en gooit daarbij weg wat awesome-pages heeft samengesteld. Het
resultaat is dan alfabetisch. Een nav: in mkdocs.yml overleeft dat wel.

Gebruik:  python3 tools/gen_nav.py [--check]
          --check schrijft niets en geeft exitcode 1 als er iets zou wijzigen.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

GROUP_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$")
BOLD_RE = re.compile(r"^\s*-\s+\*\*(?P<title>[^*]+)\*\*")
LINK_RE = re.compile(r"^(?P<indent>\s*)-\s+\[(?P<label>[^\]]+)\]\((?P<href>[^)#]+\.md)\)")
TOP_FILES = ("README.md", "reading-guide.md")


def parse(readme: Path):
    """-> [(groepstitel, [(subtitel|None, [pad, ...]), ...]), ...]"""
    groups: list[tuple[str, list]] = []
    sub = None
    for raw in readme.read_text(encoding="utf-8").splitlines():
        m = GROUP_RE.match(raw)
        if m:
            groups.append((m.group("title"), []))
            sub = None
            continue
        m = BOLD_RE.match(raw)
        if m and groups:
            sub = m.group("title").strip()
            continue
        m = LINK_RE.match(raw)
        if not m or not groups:
            continue
        # Een niet-ingesprongen regel staat weer op het niveau van de groep:
        # de subkop erboven is daarmee afgesloten. Zonder deze regel slikt
        # een subkop als "Room Server" de rest van het hoofdstuk op.
        if not m.group("indent"):
            sub = None
        href = m.group("href").strip()
        if href.startswith("../") or href.startswith("http") or "/" not in href:
            continue
        blocks = groups[-1][1]
        if not blocks or blocks[-1][0] != sub:
            blocks.append((sub, []))
        if href not in blocks[-1][1]:
            blocks[-1][1].append(href)
    return groups


def render_nav(groups, docs: Path, lang: str = "nl") -> str:
    out = ["nav:"]
    for f in TOP_FILES:
        if (docs / lang / f).exists():
            out.append(f"  - {lang}/{f}")
    for title, blocks in groups:
        out.append(f"  - {title}:")
        for sub, hrefs in blocks:
            if sub:
                out.append(f"      - {sub}:")
                out += [f"          - {lang}/{h}" for h in hrefs]
            else:
                out += [f"      - {lang}/{h}" for h in hrefs]
    return "\n".join(out)


def render_translations(nl, en) -> str:
    """Sectietitels per positie koppelen: nl[i] hoort bij en[i]."""
    pairs: list[tuple[str, str]] = []
    for (nt, nb), (et, eb) in zip(nl, en):
        pairs.append((nt, et))
        for (ns, _), (es, _) in zip(nb, eb):
            if ns and es and (ns, es) not in pairs:
                pairs.append((ns, es))
    lines = ["          nav_translations:"]
    lines += [f"            {n}: {e}" for n, e in pairs if n != e]
    return "\n".join(lines)


def splice(text: str, marker: str, block: str) -> str:
    begin, end = f"# BEGIN {marker}", f"# END {marker}"
    pat = re.compile(
        rf"([ \t]*){re.escape(begin)}[ \t]*\n.*?[ \t]*{re.escape(end)}[ \t]*(?=\n|$)",
        re.S,
    )
    m = pat.search(text)
    if not m:
        print(f"FOUT: markering {begin} niet gevonden in mkdocs.yml", file=sys.stderr)
        raise SystemExit(2)
    indent = m.group(1)
    return text[: m.start()] + f"{indent}{begin}\n{block}\n{indent}{end}" + text[m.end():]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--config", default="mkdocs.yml")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    docs = Path(args.docs)
    nl = parse(docs / "nl" / "README.md")
    en = parse(docs / "en" / "README.md")

    if len(nl) != len(en):
        print(
            f"FOUT: de README's hebben niet evenveel secties "
            f"({len(nl)} NL, {len(en)} EN); koppelen op positie kan niet.",
            file=sys.stderr,
        )
        return 2

    # controle: staat elk .md-bestand op schijf ook in de README?
    listed = {
        f"{lang}/{h}"
        for lang, groups in (("nl", nl), ("en", en))
        for _, blocks in groups
        for _, hrefs in blocks
        for h in hrefs
    } | {f"{lang}/{f}" for lang in ("nl", "en") for f in TOP_FILES}
    on_disk = {
        str(p.relative_to(docs)) for p in docs.rglob("*.md")
    }
    for missing in sorted(on_disk - listed):
        print(f"WAARSCHUWING: {missing} staat niet in de README en komt niet in het menu")
    for ghost in sorted(listed - on_disk):
        print(f"WAARSCHUWING: de README noemt {ghost}, maar dat bestand bestaat niet")

    config = Path(args.config)
    text = config.read_text(encoding="utf-8")
    new = splice(text, "NAV", render_nav(nl, docs))
    new = splice(new, "NAV_TRANSLATIONS", render_translations(nl, en))

    if new == text:
        print("ongewijzigd")
        return 0
    if args.check:
        print("FOUT: mkdocs.yml loopt achter op de README's", file=sys.stderr)
        return 1
    config.write_text(new, encoding="utf-8")
    print("gewijzigd")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
