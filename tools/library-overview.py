#!/usr/bin/env python3
"""Generate the library tables for the `libraries/` section of meshcore-docs.

Reads the root `platformio.ini` of a MeshCore checkout plus every
`variants/*/platformio.ini`, and produces three tables:

  1. inventory      - one row per declared library (introduction.md)
  2. dependencies   - one row per `depends=` / `"dependencies"` entry of the
                      upstream libraries (dependencies.md)
  3. usage          - how many firmware source files mention a library token

Table 2 needs the `library.properties` / `library.json` of the upstream
repositories. Those are fetched from raw.githubusercontent.com, or read from
the bundled snapshot when `--offline` is given.

The tables are written between the markers

    <!-- library-overview:start -->
    <!-- library-overview:end -->

so the surrounding prose in the chapter is left untouched.

Usage:
    python3 tools/library-overview.py /path/to/MeshCore
    python3 tools/library-overview.py /path/to/MeshCore --write /path/to/docs
    python3 tools/library-overview.py /path/to/MeshCore --offline --refresh-snapshot

Part of https://github.com/pe1hvh/meshcore-docs - MIT licence.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter, OrderedDict

SNAPSHOT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "library-metadata-snapshot.json")

SOURCE_EXTENSIONS = {".h", ".hpp", ".c", ".cpp", ".ino"}
SOURCE_ROOTS = ["src", "examples", "test", "arch", "lib", "variants"]

# Chapter each library is described in. Key = library name without the
# author prefix and without the version specification.
CHAPTER = {
    "SPI": ("core/wire-spi.md", "core"),
    "Wire": ("core/wire-spi.md", "core"),
    "RadioLib": ("core/radiolib.md", "core"),
    "Crypto": ("core/crypto.md", "core"),
    "RTClib": ("core/rtclib.md", "core"),
    "Melopero RV3028": ("core/rv3028.md", "core"),
    "CayenneLPP": ("core/cayenne-lpp.md", "core"),
    "ESPAsyncWebServer": ("core/espasyncwebserver.md", "core"),
    "AsyncElegantOTA": ("core/asyncelegantota.md", "core"),
    "CustomLFS": ("core/custom-lfs.md", "core"),
    "Adafruit_LittleFS_stm32": ("core/littlefs-stm32.md", "core"),
    "SubGhz": ("core/subghz.md", "core"),

    "Adafruit SSD1306": ("other/displays.md", "supporting"),
    "Adafruit SH110X": ("other/displays.md", "supporting"),
    "Adafruit GFX Library": ("other/displays.md", "supporting"),
    "Adafruit BusIO": ("other/displays.md", "supporting"),
    "Adafruit ST7735 and ST7789 Library": ("other/displays.md", "supporting"),
    "Adafruit EPD": ("other/displays.md", "supporting"),
    "GxEPD2": ("other/displays.md", "supporting"),
    "U8g2": ("other/displays.md", "supporting"),
    "LovyanGFX": ("other/displays.md", "supporting"),
    "heltec-eink-modules": ("other/displays.md", "supporting"),

    "Adafruit AHTX0": ("other/sensors.md", "supporting"),
    "Adafruit BME280 Library": ("other/sensors.md", "supporting"),
    "Adafruit BMP280 Library": ("other/sensors.md", "supporting"),
    "Adafruit BMP085 Library": ("other/sensors.md", "supporting"),
    "Adafruit BME680 Library": ("other/sensors.md", "supporting"),
    "Adafruit SHTC3 Library": ("other/sensors.md", "supporting"),
    "Sensirion I2C SHT4x": ("other/sensors.md", "supporting"),
    "Arduino_LPS22HB": ("other/sensors.md", "supporting"),
    "Adafruit MLX90614 Library": ("other/sensors.md", "supporting"),
    "Adafruit_VL53L0X": ("other/sensors.md", "supporting"),
    "BME280": ("other/sensors.md", "supporting"),
    "BSEC Software Library": ("other/sensors.md", "supporting"),
    "Adafruit LIS3DH": ("other/peripherals.md", "supporting"),
    "Adafruit SHT4x Library": ("other/sensors.md", "supporting"),

    "MicroNMEA": ("other/gps.md", "supporting"),
    "SparkFun u-blox GNSS Arduino Library": ("other/gps.md", "supporting"),

    "XPowersLib": ("other/power.md", "supporting"),
    "Adafruit INA219": ("other/power.md", "supporting"),
    "Adafruit INA260 Library": ("other/power.md", "supporting"),
    "Adafruit INA3221 Library": ("other/power.md", "supporting"),
    "INA226": ("other/power.md", "supporting"),
    "meshsolar": ("other/power.md", "supporting"),
    "GxEPD2.git": ("other/displays.md", "supporting"),

    "Adafruit NeoPixel": ("other/peripherals.md", "supporting"),
    "NonBlockingRTTTL": ("other/peripherals.md", "supporting"),
    "PCA9557-arduino": ("other/peripherals.md", "supporting"),

    "base64": ("other/utilities.md", "supporting"),
    "CRC32": ("other/utilities.md", "supporting"),

    "googletest": ("other/testing.md", "supporting"),
}

# Token searched for per library when counting source files. Keeping this
# table in the script is what makes the figures in the prose reproducible.
USAGE_TOKENS = OrderedDict([
    ("RadioLib", r"RadioLib"),
    ("Wire", r"\bWire\b"),
    ("SPI", r"\bSPI\b"),
    ("RTClib", r"RTClib"),
    ("Melopero RV3028", r"RV3028"),
    ("CayenneLPP", r"CayenneLPP"),
    ("Crypto (rweather)", r"<AES\.h>|<SHA256\.h>|<Ed25519\.h>"),
    ("ed25519 (vendored)", r"ed25519_|ed_25519\.h"),
    ("CustomLFS", r"CustomLFS"),
    ("SubGhz", r"SubGhz|STM32WL"),
    ("ESPAsyncWebServer", r"ESPAsyncWebServer|AsyncWebServer"),
    ("AsyncElegantOTA", r"AsyncElegantOTA"),
    ("MicroNMEA", r"MicroNMEA"),
    ("SparkFun u-blox GNSS", r"SFE_UBLOX|u-blox_GNSS"),
    ("base64", r"base64\.hpp|decode_base64|encode_base64"),
    ("CRC32", r"<CRC32\.h>"),
    ("NonBlockingRTTTL", r"rtttl::|NonBlockingRtttl"),
    ("XPowersLib", r"XPowers"),
    ("PCA9557-arduino", r"PCA9557"),
    ("googletest", r"gtest/gtest\.h"),
])

# Upstream metadata locations. `None` means: deliberately not fetched,
# with the reason recorded in NO_METADATA.
METADATA_URL = {
    "jgromes/RadioLib": "https://raw.githubusercontent.com/jgromes/RadioLib/master/library.properties",
    "rweather/Crypto": "https://raw.githubusercontent.com/rweather/arduinolibs/master/libraries/Crypto/library.json",
    "adafruit/RTClib": "https://raw.githubusercontent.com/adafruit/RTClib/master/library.properties",
    "electroniccats/CayenneLPP": "https://raw.githubusercontent.com/ElectronicCats/CayenneLPP/master/library.json",
    "ESP32Async/ESPAsyncWebServer": "https://raw.githubusercontent.com/ESP32Async/ESPAsyncWebServer/main/library.json",
    "adafruit/Adafruit SSD1306": "https://raw.githubusercontent.com/adafruit/Adafruit_SSD1306/master/library.properties",
    "adafruit/Adafruit SH110X": "https://raw.githubusercontent.com/adafruit/Adafruit_SH110x/master/library.properties",
    "adafruit/Adafruit GFX Library": "https://raw.githubusercontent.com/adafruit/Adafruit-GFX-Library/master/library.properties",
    "adafruit/Adafruit BusIO": "https://raw.githubusercontent.com/adafruit/Adafruit_BusIO/master/library.properties",
    "adafruit/Adafruit ST7735 and ST7789 Library": "https://raw.githubusercontent.com/adafruit/Adafruit-ST7735-Library/master/library.properties",
    "adafruit/Adafruit EPD": "https://raw.githubusercontent.com/adafruit/Adafruit_EPD/master/library.properties",
    "zinggjm/GxEPD2": "https://raw.githubusercontent.com/ZinggJM/GxEPD2/master/library.properties",
    "olikraus/U8g2": "https://raw.githubusercontent.com/olikraus/U8g2_Arduino/master/library.properties",
    "lovyan03/LovyanGFX": "https://raw.githubusercontent.com/lovyan03/LovyanGFX/master/library.properties",
    "adafruit/Adafruit AHTX0": "https://raw.githubusercontent.com/adafruit/Adafruit_AHTX0/master/library.properties",
    "adafruit/Adafruit BME280 Library": "https://raw.githubusercontent.com/adafruit/Adafruit_BME280_Library/master/library.properties",
    "adafruit/Adafruit BMP280 Library": "https://raw.githubusercontent.com/adafruit/Adafruit_BMP280_Library/master/library.properties",
    "adafruit/Adafruit BMP085 Library": "https://raw.githubusercontent.com/adafruit/Adafruit-BMP085-Library/master/library.properties",
    "adafruit/Adafruit BME680 Library": "https://raw.githubusercontent.com/adafruit/Adafruit_BME680/master/library.properties",
    "adafruit/Adafruit SHTC3 Library": "https://raw.githubusercontent.com/adafruit/Adafruit_SHTC3/master/library.properties",
    "sensirion/Sensirion I2C SHT4x": "https://raw.githubusercontent.com/Sensirion/arduino-i2c-sht4x/master/library.properties",
    "adafruit/Adafruit SHT4x Library": "https://raw.githubusercontent.com/adafruit/Adafruit_SHT4X/master/library.properties",
    "arduino-libraries/Arduino_LPS22HB": "https://raw.githubusercontent.com/arduino-libraries/Arduino_LPS22HB/master/library.properties",
    "adafruit/Adafruit MLX90614 Library": "https://raw.githubusercontent.com/adafruit/Adafruit-MLX90614-Library/master/library.properties",
    "adafruit/Adafruit_VL53L0X": "https://raw.githubusercontent.com/adafruit/Adafruit_VL53L0X/master/library.properties",
    "adafruit/Adafruit LIS3DH": "https://raw.githubusercontent.com/adafruit/Adafruit_LIS3DH/master/library.properties",
    "adafruit/Adafruit INA219": "https://raw.githubusercontent.com/adafruit/Adafruit_INA219/master/library.properties",
    "adafruit/Adafruit INA260 Library": "https://raw.githubusercontent.com/adafruit/Adafruit_INA260/master/library.properties",
    "adafruit/Adafruit INA3221 Library": "https://raw.githubusercontent.com/adafruit/Adafruit_INA3221/main/library.properties",
    "robtillaart/INA226": "https://raw.githubusercontent.com/RobTillaart/INA226/master/library.properties",
    "adafruit/Adafruit NeoPixel": "https://raw.githubusercontent.com/adafruit/Adafruit_NeoPixel/master/library.properties",
    "stevemarple/MicroNMEA": "https://raw.githubusercontent.com/stevemarple/MicroNMEA/master/library.properties",
    "sparkfun/SparkFun u-blox GNSS Arduino Library": "https://raw.githubusercontent.com/sparkfun/SparkFun_u-blox_GNSS_Arduino_Library/main/library.properties",
    "lewisxhe/XPowersLib": "https://raw.githubusercontent.com/lewisxhe/XPowersLib/master/library.properties",
    "end2endzone/NonBlockingRTTTL": "https://raw.githubusercontent.com/end2endzone/NonBlockingRTTTL/master/library.properties",
    "maxpromer/PCA9557-arduino": "https://raw.githubusercontent.com/maxpromer/PCA9557-arduino/master/library.properties",
    "densaugeo/base64": "https://raw.githubusercontent.com/densaugeo/base64_arduino/master/library.properties",
    "bakercp/CRC32": "https://raw.githubusercontent.com/bakercp/CRC32/master/library.properties",
    "boschsensortec/BSEC": "https://raw.githubusercontent.com/boschsensortec/Bosch-BSEC2-Library/master/library.properties",
    "finitespace/BME280": "https://raw.githubusercontent.com/finitespace/BME280/master/library.properties",
}

NO_METADATA = {
    "google/googletest":
        "no Arduino metadata; the registry package carries no library.json",
    "melopero/Melopero RV3028":
        "repository not found under the expected name on GitHub",
    "SPI": "framework library, ships with the platform package",
    "Wire": "framework library, ships with the platform package",
    "SubGhz": "framework library, ships with framework-arduinoststm32",
}


# --------------------------------------------------------------------------
# platformio.ini parsing
# --------------------------------------------------------------------------

def read_ini(path):
    """Read an ini file and normalise CRLF. Some variant files use CRLF."""
    with open(path, "rb") as handle:
        raw = handle.read()
    return raw.decode("utf-8", "replace").replace("\r\n", "\n")


def parse_lib_deps(path):
    """Return (declarations, interpolations) for one platformio.ini.

    `${section.lib_deps}` references are *not* resolved: they are reported
    separately so it stays visible which variant inherits from which base.
    """
    declarations, interpolations = [], []
    in_lib_deps = False
    for line in read_ini(path).split("\n"):
        if re.match(r"^\s*\[", line):
            in_lib_deps = False
            continue
        match = re.match(r"^\s*lib_deps\s*=(.*)$", line)
        if match:
            in_lib_deps = True
            rest = match.group(1).strip()
            if rest:
                (interpolations if rest.startswith("${") else
                 declarations).append(rest)
            continue
        if not in_lib_deps:
            continue
        if not line.strip() or line.strip().startswith(";"):
            in_lib_deps = False
            continue
        if re.match(r"^\s*[\w.]+\s*=", line) or not line[:1].isspace():
            in_lib_deps = False
            continue
        entry = line.strip()
        (interpolations if entry.startswith("${") else
         declarations).append(entry)
    return declarations, interpolations


def split_entry(entry):
    """Split a lib_deps entry into (name, version specification)."""
    if entry.startswith(("http://", "https://", "file://")):
        return entry, ""
    if "@" in entry:
        name, _, version = entry.partition("@")
        return name.strip(), version.strip()
    return entry.strip(), ""


def display_name(name):
    """Readable, unambiguous name for the inventory table."""
    if name.startswith("file://"):
        return name
    if name.startswith(("http://", "https://")):
        path = name.split("#")[0].rstrip("/")
        parts = path.split("/")
        if "archive" in parts:
            index = parts.index("archive")
            return "%s/%s" % (parts[index - 2], parts[index - 1])
        tail = parts[-1]
        for suffix in (".git", ".zip"):
            if tail.endswith(suffix):
                tail = tail[: -len(suffix)]
        return "%s/%s" % (parts[-2], tail)
    return name


def pinned_revision(name):
    """The commit or tag a git/zip URL pins, if any."""
    if "#" in name:
        return name.rsplit("#", 1)[1]
    if name.endswith(".zip"):
        return name.rsplit("/", 1)[-1][: -len(".zip")][:7]
    return ""


def route_of(entry, version):
    if entry.startswith("file://"):
        return "local path"
    if entry.startswith(("http://", "https://")):
        return "git/zip URL"
    if not version:
        return ("framework package" if "/" not in entry
                else "registry, no version")
    if version.startswith("^") or version.startswith("~"):
        return "registry, range"
    return "registry, pinned"


def short_name(name):
    """Strip the author prefix and any URL decoration."""
    if name.startswith("file://"):
        return name.rsplit("/", 1)[-1]
    if name.startswith(("http://", "https://")):
        path = name.split("#")[0].rstrip("/")
        parts = path.split("/")
        if "archive" in parts:                    # .../<user>/<repo>/archive/<sha>.zip
            return parts[parts.index("archive") - 1]
        tail = parts[-1]
        for suffix in (".git", ".zip"):
            if tail.endswith(suffix):
                tail = tail[: -len(suffix)]
        return tail
    return name.split("/", 1)[-1] if "/" in name else name


def collect(meshcore):
    root_ini = os.path.join(meshcore, "platformio.ini")
    if not os.path.isfile(root_ini):
        sys.exit("error: %s is not a MeshCore checkout" % meshcore)
    variant_inis = sorted(
        os.path.join(meshcore, "variants", d, "platformio.ini")
        for d in os.listdir(os.path.join(meshcore, "variants"))
        if os.path.isfile(os.path.join(meshcore, "variants", d,
                                       "platformio.ini")))
    files = [root_ini] + variant_inis

    per_file, interp = {}, {}
    for path in files:
        declarations, interpolations = parse_lib_deps(path)
        per_file[path] = declarations
        interp[path] = interpolations

    entries, file_count, in_root = {}, Counter(), set()
    for path, declarations in per_file.items():
        for entry in set(declarations):
            name, version = split_entry(entry)
            key = name
            file_count[key] += 1
            entries.setdefault(key, set()).add(version)
            if path == root_ini:
                in_root.add(key)
    return files, root_ini, entries, file_count, in_root, interp


def commit_of(meshcore):
    try:
        out = subprocess.run(["git", "-C", meshcore, "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=10)
        if out.returncode == 0:
            return out.stdout.strip()[:7]
    except (OSError, subprocess.SubprocessError):
        pass
    return "unknown"


# --------------------------------------------------------------------------
# table 1: inventory
# --------------------------------------------------------------------------

HEADERS = {
    "nl": ("| Library | Versie | Route | `.ini` | Soort | Hoofdstuk |",
           "| Library | Token | Bronbestanden |",
           "| Library | Hangt af van | Bron |"),
    "en": ("| Library | Version | Route | `.ini` | Kind | Chapter |",
           "| Library | Token | Source files |",
           "| Library | Depends on | Source |"),
}
KIND = {"nl": {"core": "kern", "supporting": "ondersteunend"},
        "en": {"core": "core", "supporting": "supporting"}}


def inventory_table(entries, file_count, in_root, lang):
    header = HEADERS[lang][0]
    rows = [header, "|---|---|---|---|---|---|"]
    for name in sorted(entries, key=lambda n: short_name(n).lower()):
        versions = sorted(v for v in entries[name] if v)
        if versions:
            version = " · ".join("`%s`" % v for v in versions)
        else:
            revision = pinned_revision(name)
            version = "`%s`" % revision if revision else "—"
        route = route_of(name, versions[0] if versions else "")
        chapter, kind = CHAPTER.get(short_name(name), ("—", "supporting"))
        display = display_name(name)
        marker = " **·**" if name in in_root else ""
        rows.append("| `%s`%s | %s | %s | %d | %s | `%s` |" % (
            display, marker, version, route, file_count[name],
            KIND[lang][kind], chapter))
    return "\n".join(rows)


# --------------------------------------------------------------------------
# table 2: dependencies
# --------------------------------------------------------------------------

def fetch(url, timeout=20):
    request = urllib.request.Request(url, headers={"User-Agent":
                                                   "meshcore-docs/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "replace")


def parse_metadata(text, url):
    """Return the list of declared dependencies."""
    if url.endswith(".json"):
        try:
            data = json.loads(text)
        except ValueError:
            return []
        deps = data.get("dependencies", [])
        if isinstance(deps, dict):
            return sorted(deps)
        return [d.get("name", str(d)) if isinstance(d, dict) else str(d)
                for d in deps]
    for line in text.split("\n"):
        if line.lower().startswith("depends="):
            return [d.strip() for d in line.split("=", 1)[1].split(",")
                    if d.strip()]
    return []


def build_metadata(offline):
    if offline:
        if not os.path.isfile(SNAPSHOT):
            sys.exit("error: --offline given but %s is missing" % SNAPSHOT)
        with open(SNAPSHOT, encoding="utf-8") as handle:
            return json.load(handle)
    snapshot = {}
    for library, url in sorted(METADATA_URL.items()):
        try:
            snapshot[library] = {"url": url,
                                 "depends": parse_metadata(fetch(url), url)}
        except (urllib.error.URLError, OSError) as error:
            snapshot[library] = {"url": url, "depends": None,
                                 "error": str(error)}
    for library, reason in sorted(NO_METADATA.items()):
        snapshot[library] = {"url": None, "depends": None, "error": reason}
    return snapshot


def dependency_table(metadata, lang):
    rows = [HEADERS[lang][2], "|---|---|---|"]
    unknown = "niet opgehaald" if lang == "nl" else "not retrieved"
    for library in sorted(metadata, key=lambda n: short_name(n).lower()):
        record = metadata[library]
        depends = record.get("depends")
        if depends is None:
            cell = "*%s — %s*" % (unknown, record.get("error", ""))
        elif not depends:
            cell = "—"
        else:
            cell = ", ".join("`%s`" % d for d in depends)
        source = "`library.json`" if (record.get("url") or "").endswith(
            ".json") else ("`library.properties`" if record.get("url")
                           else "—")
        rows.append("| `%s` | %s | %s |" % (short_name(library), cell, source))
    return "\n".join(rows)


# --------------------------------------------------------------------------
# table 3: source file usage
# --------------------------------------------------------------------------

def usage_table(meshcore, lang):
    files = []
    for root in SOURCE_ROOTS:
        base = os.path.join(meshcore, root)
        for directory, _, names in os.walk(base):
            for name in names:
                if os.path.splitext(name)[1] in SOURCE_EXTENSIONS:
                    files.append(os.path.join(directory, name))
    contents = []
    for path in files:
        with open(path, "rb") as handle:
            contents.append(handle.read().decode("utf-8", "replace"))
    rows = [HEADERS[lang][1], "|---|---|---|"]
    for library, token in USAGE_TOKENS.items():
        pattern = re.compile(token)
        count = sum(1 for text in contents if pattern.search(text))
        rows.append("| `%s` | `%s` | %d |" % (library, token, count))
    return "\n".join(rows), len(files)


# --------------------------------------------------------------------------
# writing between markers
# --------------------------------------------------------------------------

START = "<!-- library-overview:start -->"
END = "<!-- library-overview:end -->"


def write_between_markers(path, block):
    if not os.path.isfile(path):
        print("  skipped (not found): %s" % path)
        return False
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    if START not in text or END not in text:
        print("  skipped (no markers): %s" % path)
        return False
    head, _, rest = text.partition(START)
    _, _, tail = rest.partition(END)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(head + START + "\n\n" + block + "\n\n" + END + tail)
    print("  written: %s" % path)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("meshcore", help="path to a MeshCore checkout")
    parser.add_argument("--write", metavar="DOCS",
                        help="write the tables into a meshcore-docs checkout")
    parser.add_argument("--commit", metavar="SHA",
                        help="commit to report when the checkout has no .git")
    parser.add_argument("--offline", action="store_true",
                        help="use the bundled metadata snapshot")
    parser.add_argument("--refresh-snapshot", action="store_true",
                        help="fetch upstream metadata and update the snapshot")
    args = parser.parse_args()

    meshcore = os.path.abspath(args.meshcore)
    files, root_ini, entries, file_count, in_root, interp = collect(meshcore)
    commit = args.commit[:7] if args.commit else commit_of(meshcore)

    metadata = build_metadata(args.offline)
    if args.refresh_snapshot and not args.offline:
        with open(SNAPSHOT, "w", encoding="utf-8") as handle:
            json.dump(metadata, handle, indent=2, sort_keys=True)
            handle.write("\n")
        print("snapshot written: %s" % SNAPSHOT)

    interpolated = sum(len(v) for v in interp.values())
    print("MeshCore checkout : %s" % meshcore)
    print("commit            : %s" % commit)
    print("platformio.ini    : %d (root + %d variants)"
          % (len(files), len(files) - 1))
    print("unique libraries  : %d (root declares %d)"
          % (len(entries), len(in_root)))
    print("interpolations    : %d `${...}` references, not resolved"
          % interpolated)
    print()

    usage, source_files = usage_table(meshcore, "nl")
    print("source files scanned: %d" % source_files)
    print()

    for lang in ("nl", "en"):
        print("=" * 70)
        print("### inventory (%s)" % lang)
        print(inventory_table(entries, file_count, in_root, lang))
        print()
        print("### dependencies (%s)" % lang)
        print(dependency_table(metadata, lang))
        print()
        print("### usage (%s)" % lang)
        print(usage_table(meshcore, lang)[0])
        print()

    if args.write:
        docs = os.path.abspath(args.write)
        print("writing tables into %s" % docs)
        for lang in ("nl", "en"):
            note = ("*Gegenereerd met `tools/library-overview.py` tegen commit "
                    "`%s`.*" if lang == "nl" else
                    "*Generated with `tools/library-overview.py` against commit "
                    "`%s`.*") % commit
            intro = "\n\n".join([
                note,
                inventory_table(entries, file_count, in_root, lang),
                usage_table(meshcore, lang)[0]])
            deps = "\n\n".join([note,
                                dependency_table(metadata, lang)])
            write_between_markers(
                os.path.join(docs, lang, "libraries", "introduction.md"), intro)
            write_between_markers(
                os.path.join(docs, lang, "libraries", "dependencies.md"), deps)


if __name__ == "__main__":
    main()
