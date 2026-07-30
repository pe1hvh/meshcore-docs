#!/usr/bin/env python3
"""Resolve the build matrix of a MeshCore checkout.

Reads the root `platformio.ini` plus every `variants/*/platformio.ini` and
resolves each `[env:...]` section into the four facts the `ontwerp/` chapters
quote: which application it compiles, which platform family it belongs to,
which radio and display class are injected, and which optional subsystems are
switched on.

Three traps this script exists to avoid.

  1. The name of an `[env:...]` section proves nothing. `Generic_ESPNOW_room_svr`
     compiles the room server without saying so, and a section named
     `..._repeater` need not compile the repeater. The application is read from
     `build_src_filter`, never from the section name.

  2. `extends` and `${section.option}` are two different inheritance
     mechanisms and both have to be followed. A section inherits every option
     from the section it extends, and separately splices in text through
     `${...}` references. Six ikoka targets get their `build_src_filter` from a
     shared base section that is not an `[env:...]` itself.

  3. Three variant files use CRLF line endings. Without normalisation
     `esp32_base\\r` and `esp32_base` count as two different parents.

Counts are reported per resolved `[env:...]` section, never per matching line:
a naive line count overstates `companion_radio` by a factor of three because
that application spreads its source filter over several lines.

Usage:
    python3 tools/design-overview.py /path/to/MeshCore
    python3 tools/design-overview.py /path/to/MeshCore --json
    python3 tools/design-overview.py /path/to/MeshCore --targets simple_repeater

Part of https://github.com/pe1hvh/meshcore-docs - MIT licence.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, OrderedDict

# --------------------------------------------------------------------------
# Token table. Every count in the ontwerp/ chapters traces back to one of
# these patterns, so that a reader can rerun the search by hand.
# --------------------------------------------------------------------------

# An application is compiled when its directory is *included* by the resolved
# source filter. The leading '+' matters: '-<../examples/x>' excludes.
APPLICATIONS = OrderedDict([
    ("companion_radio",    "Companion radio"),
    ("simple_repeater",    "Repeater"),
    ("simple_room_server", "Room server"),
    ("simple_sensor",      "Sensor"),
    ("simple_secure_chat", "Terminal chat"),
    ("kiss_modem",         "KISS modem"),
])

# A platform family is identified by the macro its base section defines.
# esp32c6_base extends esp32_base and therefore carries ESP32_PLATFORM as
# well: it is a derived target inside the ESP32 family, not a fifth family.
PLATFORMS = OrderedDict([
    ("ESP32_PLATFORM",  "ESP32"),
    ("NRF52_PLATFORM",  "nRF52"),
    ("RP2040_PLATFORM", "RP2040"),
    ("STM32_PLATFORM",  "STM32"),
])

# Optional subsystems, each switched on by one macro.
SUBSYSTEMS = OrderedDict([
    ("WITH_RS232_BRIDGE",  "RS232 bridge"),
    ("WITH_ESPNOW_BRIDGE", "ESP-NOW bridge"),
    ("DISPLAY_CLASS",      "Display"),
    ("ENV_INCLUDE_GPS",    "GPS"),
    ("MESH_PACKET_LOGGING", "Packet logging"),
    ("MESH_DEBUG",         "Debug output"),
])

SECTION_RE = re.compile(r"^\[([^\]]+)\]\s*$")
OPTION_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_.]*)\s*=\s*(.*)$")
INTERP_RE = re.compile(r"\$\{([A-Za-z0-9_:.-]+)\.([A-Za-z0-9_.]+)\}")
MACRO_RE = re.compile(r"-D\s*([A-Za-z_][A-Za-z0-9_]*)(?:=(\S+))?")
INCLUDE_RE = re.compile(r"\+<([^>]+)>")


def strip_comment(line):
    """Remove a PlatformIO end-of-line comment.

    A ';' only starts a comment at the beginning of a line or after
    whitespace, so that '-D ADVERT_NAME=\";\"' survives intact.
    """
    out = []
    in_quote = None
    for i, ch in enumerate(line):
        if in_quote:
            out.append(ch)
            if ch == in_quote:
                in_quote = None
            continue
        if ch in "\"'":
            in_quote = ch
            out.append(ch)
            continue
        if ch == ";" and (i == 0 or line[i - 1].isspace()):
            break
        out.append(ch)
    return "".join(out)


def parse_ini(path):
    """Parse one PlatformIO ini file into {section: {option: raw_value}}.

    Line endings are normalised first; three variant files use CRLF and the
    stray carriage return would otherwise end up inside option values and
    section names.
    """
    with open(path, "rb") as handle:
        text = handle.read().decode("utf-8", errors="replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    sections = OrderedDict()
    current = None
    option = None
    for raw in text.split("\n"):
        line = strip_comment(raw)
        if not line.strip():
            continue
        match = SECTION_RE.match(line.strip())
        if match:
            current = match.group(1).strip()
            sections.setdefault(current, OrderedDict())
            option = None
            continue
        if current is None:
            continue
        if line[0] in " \t" and option is not None:
            # continuation of a multi-line value
            sections[current][option] += "\n" + line.strip()
            continue
        match = OPTION_RE.match(line.strip())
        if match:
            option = match.group(1)
            sections[current][option] = match.group(2).strip()
    return sections


def load_tree(root):
    """Load the root ini plus every variant ini, recording the source file."""
    files = [os.path.join(root, "platformio.ini")]
    variants_dir = os.path.join(root, "variants")
    for name in sorted(os.listdir(variants_dir)):
        candidate = os.path.join(variants_dir, name, "platformio.ini")
        if os.path.isfile(candidate):
            files.append(candidate)

    sections = OrderedDict()
    origin = {}
    for path in files:
        for name, options in parse_ini(path).items():
            if name in sections:
                sections[name].update(options)
            else:
                sections[name] = options
                origin[name] = os.path.relpath(path, root)
    return sections, origin, files


def parents(sections, name):
    """The sections named by `extends`, in order."""
    raw = sections.get(name, {}).get("extends", "")
    return [part.strip() for part in raw.replace("\n", ",").split(",") if part.strip()]


def resolve_option(sections, name, option, seen=None):
    """Resolve one option, following `extends` and expanding `${...}`.

    Returns the fully expanded text, or '' when neither the section nor any
    of its ancestors define the option.
    """
    if seen is None:
        seen = set()
    key = (name, option)
    if key in seen:
        return ""  # cycle guard
    seen = seen | {key}

    section = sections.get(name)
    if section is None:
        return ""

    if option in section:
        value = section[option]
    else:
        value = ""
        for parent in parents(sections, name):
            value = resolve_option(sections, parent, option, seen)
            if value:
                break
        return value

    def expand(match):
        return resolve_option(sections, match.group(1), match.group(2), seen)

    previous = None
    while previous != value:
        previous = value
        value = INTERP_RE.sub(expand, value)
    return value


def ancestry(sections, name, seen=None):
    """Every section reachable through `extends`, nearest first."""
    if seen is None:
        seen = []
    for parent in parents(sections, name):
        if parent in seen or parent not in sections:
            continue
        seen.append(parent)
        ancestry(sections, parent, seen)
    return seen


def macros(text):
    """The -D macros in a build_flags value, as {name: value_or_None}."""
    found = OrderedDict()
    for match in MACRO_RE.finditer(text):
        found[match.group(1)] = match.group(2)
    return found


def applications_of(filter_text):
    """Which applications the resolved source filter includes."""
    included = set()
    for match in INCLUDE_RE.finditer(filter_text):
        for key in APPLICATIONS:
            if "examples/" + key in match.group(1):
                included.add(key)
    return included


def analyse(root):
    sections, origin, files = load_tree(root)
    envs = [name for name in sections if name.startswith("env:")]

    records = []
    for name in envs:
        flags = resolve_option(sections, name, "build_flags")
        filt = resolve_option(sections, name, "build_src_filter")
        defined = macros(flags)

        family = None
        for macro, label in PLATFORMS.items():
            if macro in defined:
                family = label
                break

        apps = applications_of(filt)
        records.append({
            "env": name[len("env:"):],
            "file": origin.get(name, "?"),
            "applications": sorted(apps),
            "platform": family,
            "board": resolve_option(sections, name, "board") or None,
            "radio": defined.get("RADIO_CLASS"),
            "wrapper": defined.get("WRAPPER_CLASS"),
            "display": defined.get("DISPLAY_CLASS"),
            "subsystems": sorted(key for key in SUBSYSTEMS if key in defined),
            # True when the section's own text names no example directory and
            # the application only appears after extends and ${...} are
            # resolved. Those targets are invisible to a plain grep.
            "inherits_app": bool(apps) and not applications_of(
                sections[name].get("build_src_filter", "")),
            "ancestry": ancestry(sections, name),
        })

    return {
        "files": len(files),
        "variant_files": len(files) - 1,
        "sections": len(sections),
        "env_sections": len(envs),
        "base_sections": len(sections) - len(envs),
        "records": records,
    }


def report(data):
    records = data["records"]
    print("Build matrix")
    print("  ini files read           %4d  (1 root + %d variants)"
          % (data["files"], data["variant_files"]))
    print("  sections total           %4d" % data["sections"])
    print("  [env:...] sections       %4d" % data["env_sections"])
    print("  base sections            %4d" % data["base_sections"])

    inherited = sum(1 for r in records if r["inherits_app"])
    print("  envs inheriting the app  %4d  (invisible to a plain grep)" % inherited)

    print("\nApplications (counted on build_src_filter, never on the env name)")
    print("  %-20s %-18s %5s %5s" % ("", "", "envs", "dirs"))
    counts = Counter()
    spread = {key: set() for key in APPLICATIONS}
    for record in records:
        for app in record["applications"]:
            counts[app] += 1
            if record["file"].startswith("variants"):
                spread[app].add(record["file"].split(os.sep)[1])
    for key, label in APPLICATIONS.items():
        print("  %-20s %-18s %5d %5d"
              % (key, label, counts[key], len(spread[key])))
    none = sum(1 for r in records if not r["applications"])
    print("  %-20s %-18s %4d" % ("(none)", "no application", none))
    multiple = sum(1 for r in records if len(r["applications"]) > 1)
    print("  %-20s %-18s %4d" % ("(multiple)", "more than one", multiple))

    print("\nPlatform families")
    families = Counter(r["platform"] for r in records)
    for label in list(PLATFORMS.values()) + [None]:
        if families.get(label):
            print("  %-20s %4d" % (label or "(unresolved)", families[label]))

    print("\nBoards")
    boards = set(r["board"] for r in records if r["board"])
    directories = set(r["file"].split(os.sep)[1] for r in records
                      if r["file"].startswith("variants"))
    print("  distinct board ids   %4d" % len(boards))
    print("  variant directories  %4d" % len(directories))

    print("\nInjected classes")
    for field, label in (("radio", "RADIO_CLASS"), ("wrapper", "WRAPPER_CLASS"),
                         ("display", "DISPLAY_CLASS")):
        values = Counter(r[field] for r in records if r[field])
        print("  %-14s %3d distinct, %3d envs"
              % (label, len(values), sum(values.values())))

    print("\nOptional subsystems")
    subsystems = Counter()
    for record in records:
        for key in record["subsystems"]:
            subsystems[key] += 1
    for key, label in SUBSYSTEMS.items():
        print("  %-22s %-16s %4d" % (key, label, subsystems[key]))

    print("\nApplication by platform family")
    header = "  %-20s" % "" + "".join("%9s" % v for v in PLATFORMS.values())
    print(header)
    for key, label in APPLICATIONS.items():
        row = "  %-20s" % key
        for family in PLATFORMS.values():
            n = sum(1 for r in records
                    if key in r["applications"] and r["platform"] == family)
            row += "%9d" % n
        print(row)


# --------------------------------------------------------------------------
# Class census, for ontwerp/technisch/source-layout.md and class-model.md.
#
# Counted is a declaration of the form `class Name {` or `class Name : base {`
# with the brace on the same line. `struct` is excluded: those are data
# records, not parts of the design. A forward declaration without a body is
# excluded for the same reason - it declares nothing about structure.
#
# The three trees are reported separately because src/ + examples/ is the
# shared tree (119 classes) and variants/ is board-bound (77), and mixing the
# two hides exactly the skew the chapters are about.
# --------------------------------------------------------------------------
CLASS_DECL = re.compile(r"^\s*class\s+([A-Za-z_]\w*)\s*(?::\s*(.*?))?\s*\{")
CLASS_EXT = (".h", ".hpp", ".cpp")
CLASS_TREES = ("src", "examples", "variants")


def classes(root):
    """Every class declaration as (name, bases, relative path, line)."""
    found = []
    for tree in CLASS_TREES:
        for dirpath, _, names in os.walk(os.path.join(root, tree)):
            for name in sorted(names):
                if not name.endswith(CLASS_EXT):
                    continue
                path = os.path.join(dirpath, name)
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    body = fh.read()
                for number, text in enumerate(body.split("\n"), 1):
                    match = CLASS_DECL.match(text)
                    if match:
                        bases = [b.strip() for b in
                                 (match.group(2) or "").split(",") if b.strip()]
                        found.append((match.group(1), bases,
                                      os.path.relpath(path, root), number))
    return found


def class_report(root):
    found = classes(root)
    shared = [c for c in found if not c[2].startswith("variants" + os.sep)]
    variant = [c for c in found if c[2].startswith("variants" + os.sep)]

    print("Classes (declaration with a body, `struct` excluded)")
    print("  shared tree  src/ + examples/   %4d" % len(shared))
    print("  boards       variants/          %4d  (%d unique names)"
          % (len(variant), len({c[0] for c in variant})))
    print("  total                           %4d" % len(found))

    print("\nShared tree by directory")
    seen = Counter()
    for _, _, rel, _ in shared:
        directory = os.path.dirname(rel) + os.sep
        seen[directory] += 1
    for directory, number in sorted(seen.items()):
        print("  %-34s %4d" % (directory, number))

    print("\nvariants/ by contract filled")
    contracts = OrderedDict([
        ("Board", ("MainBoard", "Board")),
        ("Sensor management", ("SensorManager",)),
        ("Display", ("Display",)),
        ("Entropy", ("RNG",)),
    ])
    tally = Counter()
    for _, bases, _, _ in variant:
        text = " ".join(bases)
        for label, needles in contracts.items():
            if any(needle in text for needle in needles):
                tally[label] += 1
                break
    for label in contracts:
        print("  %-22s %4d" % (label, tally[label]))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("root", help="path to a MeshCore checkout")
    parser.add_argument("--json", action="store_true", help="dump raw records")
    parser.add_argument("--targets", metavar="APP",
                        help="list the env names that compile APP")
    parser.add_argument("--classes", action="store_true",
                        help="census of class declarations per tree")
    args = parser.parse_args()

    if not os.path.isfile(os.path.join(args.root, "platformio.ini")):
        sys.exit("no platformio.ini in %s" % args.root)

    if args.classes:
        class_report(args.root)
        return

    data = analyse(args.root)

    if args.json:
        print(json.dumps(data, indent=2))
        return
    if args.targets:
        names = sorted(r["env"] for r in data["records"]
                       if args.targets in r["applications"])
        print("\n".join(names))
        print("\n%d targets" % len(names))
        return
    report(data)


if __name__ == "__main__":
    main()
