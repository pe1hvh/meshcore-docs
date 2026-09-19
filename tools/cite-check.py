#!/usr/bin/env python3
"""Toets de regelcitaties in een hoofdstuk tegen een MeshCore-checkout.

Een citatie heeft in de hoofdstukken twee vormen:

  `pad/naar/bestand.h` r.45              — één regel, meestal in een tabel
  `pad/naar/bestand.cpp` r.183-192       — een bereik, gevolgd door een
                                           codeblok met die regels erin

Voor de eerste vorm controleert het script of de regel bestaat en, als in
dezelfde tabelrij een naam tussen backticks staat, of die naam daar ook
werkelijk gedeclareerd wordt. Voor de tweede vorm vergelijkt het het codeblok
met de regels uit het bestand. Wijkt het af, dan zoekt het script het blok
elders in het bestand en meldt het juiste bereik.

Gebruik:

    python3 tools/cite-check.py /pad/naar/MeshCore docs/nl/.../hoofdstuk.md
    python3 tools/cite-check.py /pad/naar/MeshCore --alle
    python3 tools/cite-check.py /pad/naar/MeshCore --alle --alleen-fouten

Uitgecommentarieerde regels tellen hier wél mee: het gaat om de vraag of de
geciteerde tekst op de genoemde plek staat, niet om een telling.
"""

import argparse
import os
import re
import sys

CITATIE = re.compile(r"`([A-Za-z0-9_./-]+\.(?:h|cpp|hpp|c|ini|json|py))`\s+r\.(\d+)(?:-(\d+))?")
NAAM = re.compile(r"`([A-Za-z_][A-Za-z0-9_:]*)`")
DECLARATIE = r"(?:class|struct|enum|#define|void|bool|int|uint\d+_t|static|virtual)"

OK = "goed"
VERSCHOVEN = "verschoven"
NIET_GEVONDEN = "niet gevonden"
BESTAND_WEG = "bestand weg"


def lees(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def regels_van(root, rel):
    vol = os.path.join(root, rel)
    if not os.path.isfile(vol):
        return None
    return lees(vol).split("\n")


def codeblok_na(regels, index):
    """Het fenced codeblok dat direct na regel `index` begint, of None."""
    i = index + 1
    while i < len(regels) and not regels[i].strip():
        i += 1
    if i >= len(regels) or not regels[i].startswith("```"):
        return None
    begin = i + 1
    i = begin
    while i < len(regels) and not regels[i].startswith("```"):
        i += 1
    if i >= len(regels):
        return None
    return regels[begin:i]


def normaliseer(blok):
    return [r.rstrip() for r in blok]


def zoek_blok(bron, blok):
    """Waar staat `blok` in `bron`? Geeft het 1-gebaseerde beginnummer."""
    blok = [r for r in normaliseer(blok) if r.strip()]
    if not blok:
        return None
    bron_n = normaliseer(bron)
    eerste = blok[0]
    for i, regel in enumerate(bron_n):
        if regel != eerste:
            continue
        j, k = i, 0
        while j < len(bron_n) and k < len(blok):
            if not bron_n[j].strip():
                j += 1
                continue
            if bron_n[j] != blok[k]:
                break
            j += 1
            k += 1
        if k == len(blok):
            return i + 1, j
    return None


def toets_bereik(bron, blok, begin, eind):
    verwacht = normaliseer(bron[begin - 1:eind])
    gezien = normaliseer(blok)
    if [r for r in verwacht if r.strip()] == [r for r in gezien if r.strip()]:
        return OK, None
    plek = zoek_blok(bron, blok)
    if plek:
        return VERSCHOVEN, "r.%d-%d" % plek
    return NIET_GEVONDEN, None


def toets_regel(bron, nummer, naam):
    if nummer > len(bron):
        return NIET_GEVONDEN, "bestand telt %d regels" % len(bron)
    if not naam:
        return OK, None
    tekst = bron[nummer - 1]
    kaal = naam.split("::")[-1]
    if re.search(r"\b%s\b" % re.escape(kaal), tekst):
        return OK, None
    patroon = re.compile(r"^\s*%s.*\b%s\b" % (DECLARATIE, re.escape(kaal)))
    treffers = [i + 1 for i, r in enumerate(bron) if patroon.match(r)]
    if len(treffers) == 1:
        return VERSCHOVEN, "r.%d" % treffers[0]
    if treffers:
        return VERSCHOVEN, "r." + ", r.".join(str(t) for t in treffers)
    return NIET_GEVONDEN, None


def toets_hoofdstuk(root, doc):
    regels = lees(doc).split("\n")
    uitslag = []
    in_blok = False
    for index, regel in enumerate(regels):
        if regel.startswith("```"):
            in_blok = not in_blok
            continue
        if in_blok:
            continue
        match = CITATIE.search(regel)
        if not match:
            continue
        rel, begin, eind = match.group(1), int(match.group(2)), match.group(3)
        bron = regels_van(root, rel)
        etiket = "%s r.%s%s" % (rel, begin, "-" + eind if eind else "")
        if bron is None:
            uitslag.append((index + 1, etiket, BESTAND_WEG, None))
            continue
        if eind:
            blok = codeblok_na(regels, index)
            if blok is None:
                staat, extra = toets_regel(bron, begin, None)
                uitslag.append((index + 1, etiket, staat, extra or "geen codeblok"))
                continue
            staat, extra = toets_bereik(bron, blok, begin, int(eind))
        else:
            namen = NAAM.findall(regel)
            namen = [n for n in namen if not n.endswith((".h", ".cpp", ".hpp", ".c"))]
            staat, extra = toets_regel(bron, begin, namen[0] if namen else None)
        uitslag.append((index + 1, etiket, staat, extra))
    return uitslag


def alle_hoofdstukken():
    gevonden = []
    for taal in ("nl", "en"):
        for pad, _, namen in os.walk(os.path.join("docs", taal)):
            for naam in sorted(namen):
                if naam.endswith(".md"):
                    gevonden.append(os.path.join(pad, naam))
    return sorted(gevonden)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("root", help="pad naar een MeshCore-checkout")
    p.add_argument("docs", nargs="*", help="hoofdstukken om te toetsen")
    p.add_argument("--alle", action="store_true", help="alle hoofdstukken")
    p.add_argument("--alleen-fouten", action="store_true")
    args = p.parse_args()

    docs = alle_hoofdstukken() if args.alle else args.docs
    if not docs:
        p.error("geef hoofdstukken op, of --alle")

    totaal = {OK: 0, VERSCHOVEN: 0, NIET_GEVONDEN: 0, BESTAND_WEG: 0}
    fout = False
    for doc in docs:
        uitslag = toets_hoofdstuk(args.root, doc)
        if not uitslag:
            continue
        kop = False
        for nummer, etiket, staat, extra in uitslag:
            totaal[staat] += 1
            if staat != OK:
                fout = True
            if args.alleen_fouten and staat == OK:
                continue
            if not kop:
                print("\n%s" % doc)
                kop = True
            print("  r.%-5d %-12s %s%s"
                  % (nummer, staat, etiket, "  → " + extra if extra else ""))

    print("\nTotaal: %d goed, %d verschoven, %d niet gevonden, %d bestand weg"
          % (totaal[OK], totaal[VERSCHOVEN], totaal[NIET_GEVONDEN], totaal[BESTAND_WEG]))
    return 1 if fout else 0


if __name__ == "__main__":
    sys.exit(main())
