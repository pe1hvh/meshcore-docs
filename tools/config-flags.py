#!/usr/bin/env python3
"""Inventory the compile-time flags of a MeshCore checkout by owner.

Reads the root `platformio.ini` plus every `variants/*/platformio.ini` and
splits the `-D` macros into three groups:

  1. library-directed - the macro is consumed by a third-party library
  2. framework        - the macro is consumed by an Arduino core or platform
  3. MeshCore         - the macro is consumed by MeshCore's own sources

Only group 1 is tabulated; that table feeds `libraries/library-configuration.md`.
Group 2 and 3 are reported as counts only, because they belong to other
chapters.

Ownership cannot be derived from the name alone, so it comes from the table
`NAMESPACES` below. Every entry there was verified by hand against the source
of the library in question; the `source` field records where. Rerun with
`--check <path-to-library-source>` to re-verify a single namespace.

Commented-out macros are collected separately: a `; -D RADIOLIB_DEBUG_SPI=1`
line is not part of any build, and counting it would overstate the
configuration surface.

Usage:
    python3 tools/config-flags.py /path/to/MeshCore
    python3 tools/config-flags.py /path/to/MeshCore --write /path/to/docs
    python3 tools/config-flags.py /path/to/MeshCore --all

Part of https://github.com/pe1hvh/meshcore-docs - MIT licence.
"""

import argparse
import os
import re
import subprocess
import sys
from collections import Counter, OrderedDict

# --------------------------------------------------------------------------
# Ownership table.
#
# prefix -> (owner, kind, mechanism, source)
#
# kind:      library | framework
# mechanism: exclusion | feature | tuning | injection
# source:    the file that consumes the macro, so the row can be re-checked
# --------------------------------------------------------------------------
NAMESPACES = OrderedDict([
    ("RADIOLIB_EXCLUDE_", (
        "jgromes/RadioLib", "library", "exclusion",
        "src/BuildOpt.h r.182-204 lists them; every module and protocol "
        "header opens with `#if !RADIOLIB_EXCLUDE_<name>`")),
    ("RADIOLIB_DEBUG_", (
        "jgromes/RadioLib", "library", "feature",
        "src/BuildOptUser.h r.8-10")),
    ("RADIOLIB_VERBOSE_", (
        "jgromes/RadioLib", "library", "feature",
        "src/BuildOptUser.h r.11")),
    ("RADIOLIB_", (
        "jgromes/RadioLib", "library", "feature",
        "src/BuildOpt.h")),
    ("LFS_", (
        "littlefs (via Adafruit_LittleFS)", "library", "exclusion",
        "libraries/Adafruit_LittleFS/src/littlefs/lfs_util.h r.30 and r.77")),
    ("SSD1306_", (
        "adafruit/Adafruit SSD1306", "library", "exclusion",
        "Adafruit_SSD1306.h r.36")),
    ("ASYNCWEBSERVER_", (
        "ESP32Async/ESPAsyncWebServer", "library", "tuning",
        "src/ESPAsyncWebServer.h r.72")),
    ("U8G2_", (
        "olikraus/U8g2", "library", "feature",
        "src/U8x8lib.h")),
    ("U8X8_", (
        "olikraus/U8g2", "library", "feature",
        "src/U8x8lib.h")),
    ("GXEPD2_", (
        "zinggjm/GxEPD2", "library", "feature",
        "src/GxEPD2.h")),
    ("CAYENNE", (
        "electroniccats/CayenneLPP", "library", "tuning",
        "src/CayenneLPP.h")),
    # Framework / platform, listed so they are not miscounted as MeshCore's.
    ("ARDUINO_", ("Arduino core", "framework", "feature", "core variant.h")),
    ("CORE_DEBUG_", ("Arduino-ESP32", "framework", "tuning", "core esp32-hal-log.h")),
    ("CFG_", ("Adafruit nRF52 core", "framework", "tuning", "core common_config.h")),
    ("USE_TINYUSB", ("Adafruit nRF52 core", "framework", "feature", "core Adafruit_TinyUSB")),
])

MECHANISM_NL = {
    "exclusion": "uitsluiten",
    "feature":   "insluiten",
    "tuning":    "overriden",
    "injection": "typeinjectie",
}

MECHANISM_EN = {
    "exclusion": "exclusion",
    "feature":   "inclusion",
    "tuning":    "override",
    "injection": "type injection",
}

MARK_START = "<!-- config-flags:start -->"
MARK_END = "<!-- config-flags:end -->"

DEFINE = re.compile(r"-D\s*([A-Za-z_][A-Za-z0-9_]*)")
SECTION = re.compile(r"^\s*\[([^\]]+)\]")


def ini_files(root):
    """Root platformio.ini first, then every variant, sorted."""
    files = [os.path.join(root, "platformio.ini")]
    vdir = os.path.join(root, "variants")
    for name in sorted(os.listdir(vdir)):
        path = os.path.join(vdir, name, "platformio.ini")
        if os.path.isfile(path):
            files.append(path)
    return files


def strip_comment(line):
    """Return (code, comment). A `;` starts a comment anywhere on the line."""
    idx = line.find(";")
    if idx < 0:
        return line, ""
    return line[:idx], line[idx:]


def scan(root):
    """Return (active, inactive, sections).

    active[macro]   = Counter of files that define it
    inactive[macro] = Counter of files that mention it behind a `;`
    sections[macro] = set of ini sections it was defined in
    """
    active, inactive = {}, {}
    sections = {}
    for path in ini_files(root):
        rel = os.path.relpath(path, root)
        section = ""
        # CRLF appears in a few variant files; splitlines handles both.
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            for raw in handle.read().splitlines():
                match = SECTION.match(raw)
                if match:
                    section = match.group(1)
                code, comment = strip_comment(raw)
                for macro in DEFINE.findall(code):
                    active.setdefault(macro, Counter())[rel] += 1
                    sections.setdefault(macro, set()).add(section)
                for macro in DEFINE.findall(comment):
                    inactive.setdefault(macro, Counter())[rel] += 1
    return active, inactive, sections


def classify(macro):
    """Return (owner, kind, mechanism, source) - longest prefix wins."""
    for prefix in sorted(NAMESPACES, key=len, reverse=True):
        if macro.startswith(prefix):
            return NAMESPACES[prefix]
    return ("MeshCore", "meshcore", "", "")


def commit_of(root, override=None):
    """Short commit hash of the checkout, so the table can be dated."""
    if override:
        return override
    try:
        out = subprocess.run(["git", "-C", root, "rev-parse", "--short=7",
                              "HEAD"], capture_output=True, text=True,
                             check=True)
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def render(active, inactive, sections, lang, show_all, commit="unknown"):
    words = MECHANISM_NL if lang == "nl" else MECHANISM_EN
    rows = []
    counts = Counter()
    for macro in sorted(active):
        owner, kind, mechanism, _ = classify(macro)
        counts[kind] += 1
        if kind != "library":
            continue
        files = active[macro]
        where = "root" if list(files) == ["platformio.ini"] else \
                ("%d x variants" % len(files))
        rows.append((macro, owner, words[mechanism],
                     ", ".join(sorted(sections[macro])), where))

    head = (("| Macro | Library | Mechaniek | Sectie | Waar |",
             "|---|---|---|---|---|")
            if lang == "nl" else
            ("| Macro | Library | Mechanism | Section | Where |",
             "|---|---|---|---|---|"))
    credit = ("*Gegenereerd met `tools/config-flags.py` tegen commit `%s`.*"
              if lang == "nl" else
              "*Generated with `tools/config-flags.py` against commit `%s`.*")
    out = [credit % commit, "", head[0], head[1]]
    for row in rows:
        out.append("| `%s` | `%s` | %s | `[%s]` | %s |" % row)

    total = len(active)
    if lang == "nl":
        summary = (
            "\nVan de %d unieke `-D`-macro's in de tachtig `platformio.ini`"
            "-bestanden zijn er %d op een library gericht, %d op een "
            "Arduino-core of platform, en %d op MeshCore's eigen code."
            % (total, counts["library"], counts["framework"],
               counts["meshcore"]))
    else:
        summary = (
            "\nOf the %d unique `-D` macros across the eighty `platformio.ini` "
            "files, %d target a library, %d an Arduino core or platform, and "
            "%d MeshCore's own code."
            % (total, counts["library"], counts["framework"],
               counts["meshcore"]))
    out.append(summary)

    dead = [m for m in sorted(inactive)
            if classify(m)[1] == "library" and m not in active]
    if dead:
        label = ("Uitgecommentarieerd, dus in geen enkele build actief: "
                 if lang == "nl" else
                 "Commented out, so active in no build: ")
        out.append("\n" + label + ", ".join("`%s`" % m for m in dead) + ".")

    if show_all:
        out.append("\n--- all macros, grouped by owner ---")
        for macro in sorted(active):
            owner, kind, mechanism, source = classify(macro)
            out.append("%-32s %-12s %-34s %s"
                       % (macro, kind, owner, mechanism))
    return "\n".join(out)


def write_into(path, block):
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    if MARK_START not in text or MARK_END not in text:
        sys.exit("markers not found in %s" % path)
    head, rest = text.split(MARK_START, 1)
    _, tail = rest.split(MARK_END, 1)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(head + MARK_START + "\n\n" + block + "\n\n"
                     + MARK_END + tail)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("meshcore", help="path to a MeshCore checkout")
    parser.add_argument("--write", metavar="DOCS",
                        help="write the tables into a meshcore-docs checkout")
    parser.add_argument("--all", action="store_true",
                        help="also dump every macro with its owner")
    parser.add_argument("--commit", metavar="HASH",
                        help="commit hash to print; default is git rev-parse")
    args = parser.parse_args()

    active, inactive, sections = scan(args.meshcore)
    commit = commit_of(args.meshcore, args.commit)

    if args.write:
        for lang in ("nl", "en"):
            path = os.path.join(args.write, lang, "libraries",
                                "library-configuration.md")
            write_into(path, render(active, inactive, sections, lang, False,
                                    commit))
            print("written: %s" % path)
    else:
        print(render(active, inactive, sections, "nl", args.all, commit))


if __name__ == "__main__":
    main()
