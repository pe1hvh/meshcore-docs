#!/usr/bin/env bash
#
# hernoem-bestanden.sh — hoort bij meshcore_docs_ontbrekende-inhoud_result.zip
#
# Een ZIP kan een hernoeming niet uitdrukken: hij levert feedback.md aan maar
# laat buttons-and-leds.md staan, en dan staat het hoofdstuk er twee keer in.
# Dit script doet de hernoeming met `git mv`, zodat de geschiedenis meeloopt.
#
# Draaien vanuit de repo-root, VOORDAT de rest van de ZIP wordt uitgepakt:
#
#     bash hernoem-bestanden.sh
#     unzip -o meshcore_docs_ontbrekende-inhoud_result.zip
#     python3 tools/gen_nav_pages.py && python3 tools/gen_nav.py --check
#
# Dit script hoort niet in de repository thuis. Gooi het na gebruik weg.

set -euo pipefail

OUD='hardware/peripherals/buttons-and-leds.md'
NIEUW='hardware/peripherals/feedback.md'

if [ ! -d .git ] || [ ! -d docs/nl ] || [ ! -d docs/en ]; then
  echo "FOUT: draai dit script vanuit de root van pe1hvh/meshcore-docs." >&2
  exit 1
fi

verplaatst=0
for taal in nl en; do
  van="docs/$taal/$OUD"
  naar="docs/$taal/$NIEUW"
  if [ -f "$van" ]; then
    git mv "$van" "$naar"
    echo "hernoemd: $van -> $naar"
    verplaatst=$((verplaatst + 1))
  elif [ -f "$naar" ]; then
    echo "overgeslagen: $naar bestaat al"
  else
    echo "FOUT: noch $van noch $naar bestaat." >&2
    exit 1
  fi
done

if [ "$verplaatst" -eq 0 ]; then
  echo "Niets te doen; de hernoeming was al gedaan."
fi

# De navigatie wordt uit de README's afgeleid. Zolang die nog naar het oude pad
# wijzen — dus zolang de ZIP nog niet is uitgepakt — zouden de generatoren het
# oude pad terugschrijven. Daarom pas draaien als de README bij is.
if grep -q "$NIEUW" docs/nl/README.md && grep -q "$NIEUW" docs/en/README.md; then
  python3 tools/gen_nav_pages.py
  python3 tools/gen_nav.py
  echo "Navigatie bijgewerkt."
else
  echo
  echo "De README's wijzen nog naar het oude pad. Pak nu de ZIP uit en draai"
  echo "daarna:  python3 tools/gen_nav_pages.py && python3 tools/gen_nav.py"
fi
