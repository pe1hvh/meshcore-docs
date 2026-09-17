#!/usr/bin/env python3
"""Reproduces the tables and examples in the CLI reference (nl/cli/, en/cli/).

Reads a MeshCore checkout and prints every CLI command the firmware
recognises, the line it is recognised on, whether it is serial-only, which
preprocessor guard it sits under, the defaults per role, which role actually
reads each setting, the differences with docs/cli_commands.md, and the example
replies used in the chapters.

Usage:
    git clone https://github.com/meshcore-dev/MeshCore.git
    git -C MeshCore checkout 03b6ef4
    python3 tools/cli-commands.py MeshCore
    python3 tools/cli-commands.py MeshCore MeshCore-main   # also list newer commands

With a second checkout (for example `main`), the script also prints the
commands that exist there and not in the first, with their line and guard.
That list feeds the page "Na de gepinde commit" / "After the pinned commit".

Counting method
---------------
* A command is a string literal compared with `memcmp`, `strcmp` or
  `strncmp` against the command buffer (`command`, `config`, `cmd`,
  `cli_command`, `parts[1]`). Commented-out code does not count: `//` and
  `/* */` comments are blanked before matching.
* Inside `handleGetCmd` the literal gets the prefix `get `, inside
  `handleSetCmd` the prefix `set `, inside `handleRegionCmd` the prefix
  `region ` (except `region def`, which is matched in full). The two
  dispatch literals `get ` and `set ` in `handleCommand` are not commands.
* Literals that are the value of a preceding command rather than a command
  (`off`, `minimal`, `moderate`, `strict`, `none`, `share`, `prefs`) are
  reported as values, not as commands.
* A command is serial-only when its own line tests `sender_timestamp == 0`.
* A default is the last `_prefs.<field> = <value>;` (or
  `strncpy(_prefs.<field>, ...)`) after `memset(&_prefs, 0, ...)` in the
  role's constructor; guarded assignments are all listed. A field that is not
  assigned there stays 0 through the memset. Macros are resolved first from
  the `-D` flags in `[arduino_base]` of platformio.ini, then from the
  `#ifndef` fallback in the role's own files.
* A setting counts as read by a role when `_prefs.<field>` or `-><field>`
  occurs in that role's example directory outside the constructor, file
  reads and writes excluded.
"""
import datetime
import hashlib
import pathlib
import re
import struct
import subprocess
import sys

PINNED = "03b6ef4"

CMD_RE = re.compile(
    r'\b(?:memcmp|strcmp|strncmp)\(\s*'
    r'(command|config|cmd|cli_command|parts\[1\])\s*,\s*"([^"]*)"')
VALUES = {"off", "minimal", "moderate", "strict", "none", "share", "prefs"}
FUNC_RE = re.compile(r'^\s*(?:static\s+)?(?:void|bool)\s+(?:(\w+)::)?(\w+)\s*\(')
PREF_ASSIGN_RE = re.compile(r'_prefs\.(\w+)\s*=\s*([^;]+);')
PREF_COPY_RE = re.compile(r'strncpy\(_prefs\.(\w+),\s*([^,]+),')

CTOR = {
    "repeater": "examples/simple_repeater/MyMesh.cpp",
    "room server": "examples/simple_room_server/MyMesh.cpp",
    "sensor": "examples/simple_sensor/SensorMesh.cpp",
}
ROLE_DIR = {
    "repeater": "examples/simple_repeater",
    "room server": "examples/simple_room_server",
    "sensor": "examples/simple_sensor",
}
HEADER = {
    "repeater": "examples/simple_repeater/MyMesh.h",
    "room server": "examples/simple_room_server/MyMesh.h",
    "sensor": "examples/simple_sensor/SensorMesh.h",
}
FALLBACKS = {
    "repeater": "examples/simple_repeater/MyMesh.cpp",
    "room server": "examples/simple_room_server/MyMesh.h",
    "sensor": "examples/simple_sensor/SensorMesh.cpp",
}

# pref field -> CLI setting, for the defaults table
FIELDS = [
    ("freq/bw/sf/cr", "radio"), ("tx_power_dbm", "tx"),
    ("rx_boosted_gain", "radio.rxgain"), ("node_name", "name"),
    ("node_lat", "lat"), ("node_lon", "lon"), ("password", "password"),
    ("guest_password", "guest.password"), ("owner_info", "owner.info"),
    ("adc_multiplier", "adc.multiplier"),
    ("powersaving_enabled", "powersaving"), ("disable_fwd", "repeat (inverted)"),
    ("path_hash_mode", "path.hash.mode"), ("loop_detect", "loop.detect"),
    ("tx_delay_factor", "txdelay"), ("direct_tx_delay_factor", "direct.txdelay"),
    ("rx_delay_base", "rxdelay"), ("airtime_factor", "af / dutycycle"),
    ("interference_threshold", "int.thresh"),
    ("agc_reset_interval", "agc.reset.interval (x4)"),
    ("multi_acks", "multi.acks"),
    ("flood_advert_interval", "flood.advert.interval"),
    ("advert_interval", "advert.interval (x2)"), ("flood_max", "flood.max"),
    ("flood_max_unscoped", "flood.max.unscoped"),
    ("flood_max_advert", "flood.max.advert"),
    ("allow_read_only", "allow.read.only"), ("gps_enabled", "gps"),
    ("advert_loc_policy", "gps advert"), ("bridge_enabled", "bridge.enabled"),
    ("bridge_delay", "bridge.delay"), ("bridge_pkt_src", "bridge.source"),
    ("bridge_baud", "bridge.baud"), ("bridge_channel", "bridge.channel"),
    ("bridge_secret", "bridge.secret"),
]
READ_CHECK = ["loop_detect", "powersaving_enabled", "allow_read_only",
              "flood_max", "flood_max_unscoped", "flood_max_advert", "disable_fwd",
              "rx_boosted_gain", "bridge_enabled", "path_hash_mode",
              "tx_delay_factor", "direct_tx_delay_factor", "rx_delay_base",
              "airtime_factor", "interference_threshold", "agc_reset_interval",
              "multi_acks", "flood_advert_interval", "advert_interval",
              "gps_enabled", "guest_password", "owner_info"]
FAMILIES = ("get", "set", "region", "gps", "sensor", "log", "clock", "start",
            "clear", "powersaving")


def blank_comments(text):
    """Blank // and /* */ comments, keep line structure and string literals."""
    out, i, n = [], 0, len(text)
    in_str = in_line = in_block = False
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if in_line:
            if c == "\n":
                in_line = False
                out.append(c)
            else:
                out.append(" ")
        elif in_block:
            if c == "*" and nxt == "/":
                in_block = False
                out.append("  ")
                i += 1
            else:
                out.append("\n" if c == "\n" else " ")
        elif in_str:
            out.append(c)
            if c == "\\":
                out.append(nxt)
                i += 1
            elif c in ('"', "\n"):
                in_str = False
        elif c == '"':
            in_str = True
            out.append(c)
        elif c == "/" and nxt == "/":
            in_line = True
            out.append(" ")
        elif c == "/" and nxt == "*":
            in_block = True
            out.append(" ")
        else:
            out.append(c)
        i += 1
    return "".join(out).split("\n")


def read(root, rel):
    return blank_comments((root / rel).read_text(errors="replace"))


def scan(root, rel, only_funcs=None):
    """Yield (line, func, command, serial_only, guard) for one file."""
    func, guards, last_cmd = None, [], None
    for no, ln in enumerate(read(root, rel), 1):
        s = ln.strip()
        m = FUNC_RE.match(ln)
        if m:
            func = m.group(2)
        if s.startswith("#if"):
            guards.append(s)
        elif s.startswith("#elif") and guards:
            guards[-1] = s
        elif s.startswith("#else") and guards:
            guards[-1] = "not(" + guards[-1] + ")"
        elif s.startswith("#endif") and guards:
            guards.pop()
        if only_funcs and func not in only_funcs:
            continue
        for mm in CMD_RE.finditer(ln):
            buf, tok = mm.group(1), mm.group(2).strip()
            if tok in VALUES:
                yield (no, func, f"  value of {last_cmd}: {tok}", False, "")
                continue
            if tok in ("get", "set") and func == "handleCommand":
                continue
            if func == "handleGetCmd":
                tok = "get " + tok
            elif func == "handleSetCmd":
                tok = "set " + tok
            elif func == "handleRegionCmd" and buf == "parts[1]":
                tok = "region " + tok
            elif func == "checkCLIRescueCmd" and buf == "config":
                tok = "set " + tok
            last_cmd = tok
            yield (no, func, tok, "sender_timestamp == 0" in ln, " && ".join(guards))


def ctor_defaults(root, rel):
    lines = read(root, rel)
    start = next(i for i, l in enumerate(lines) if "memset(&_prefs" in l)
    vals, guards = {}, []
    for no in range(start + 1, len(lines)):
        ln = lines[no]
        if ln.startswith("}"):
            return vals, (start + 1, no + 1)
        s = ln.strip()
        if s.startswith("#if"):
            guards.append(s)
        elif s.startswith("#else") and guards:
            guards[-1] = "not(" + guards[-1] + ")"
        elif s.startswith("#endif") and guards:
            guards.pop()
        for f, v in PREF_ASSIGN_RE.findall(ln) + PREF_COPY_RE.findall(ln):
            vals.setdefault(f, []).append((no + 1, v.strip(), " && ".join(guards)))
    return vals, (start + 1, len(lines))


def macros(root, fallback):
    found = {}
    section = None
    ini = blank_comments((root / "platformio.ini").read_text().replace(";", "//"))
    for ln in ini:
        m = re.match(r"\[(.+)\]", ln.strip())
        if m:
            section = m.group(1)
        if section == "arduino_base":
            for k, v in re.findall(r"-D\s*(\w+)=(\S+)", ln):
                found[k] = (v, "platformio.ini [arduino_base]")
    text = read(root, fallback)
    for i, ln in enumerate(text):
        m = re.match(r"\s*#define\s+(\w+)\s+(.+?)\s*$", ln)
        if m and i > 0 and re.match(r"\s*#ifndef\s+" + m.group(1) + r"\b", text[i - 1]):
            found.setdefault(m.group(1), (m.group(2), f"{fallback} r.{i + 1} (#ifndef)"))
    return found


def variant_radio_overrides(root):
    n = 0
    for p in (root / "variants").rglob("platformio.ini"):
        for ln in blank_comments(p.read_text(errors="replace").replace(";", "//")):
            n += len(re.findall(r"-D\s*LORA_(?:FREQ|BW|SF|CR)=", ln))
    return n


def readers(root, role, field, rel_ctor, span):
    hits = []
    for p in sorted((root / ROLE_DIR[role]).rglob("*")):
        if p.suffix not in (".cpp", ".h"):
            continue
        rel = str(p.relative_to(root))
        for no, ln in enumerate(read(root, rel), 1):
            if rel == rel_ctor and span[0] <= no <= span[1]:
                continue
            if re.search(r"(_prefs\.|->)" + field + r"\b", ln) and "file." not in ln:
                hits.append(f"{rel}:{no}")
    return hits


def norm(words):
    """First word, or first two for command families, without placeholders."""
    words = [w for w in words if not w.startswith(("<", "{", "["))]
    if not words:
        return None
    if words[0] in FAMILIES and len(words) > 1:
        return " ".join(words[:2])
    return words[0]


def doc_commands(root):
    """Commands named in the Usage blocks of docs/cli_commands.md."""
    cmds, in_usage = set(), False
    for ln in (root / "docs/cli_commands.md").read_text().splitlines():
        if ln.startswith("**Usage:**"):
            in_usage = True
            for u in re.findall(r"`([^`]+)`", ln):
                cmds.add(norm(u.split()))
            continue
        if in_usage:
            m = re.match(r"\s*-\s+`([^`]+)`", ln)
            if m:
                cmds.add(norm(m.group(1).split()))
            elif ln.strip() and not ln.strip().startswith("-"):
                in_usage = False
    cmds.discard(None)
    return cmds


def head_of(root):
    try:
        return subprocess.run(["git", "-C", str(root), "rev-parse", "--short=7", "HEAD"],
                              capture_output=True, text=True).stdout.strip() or "?"
    except OSError:
        return "?"


def main(root):
    head = head_of(root)
    print(f"MeshCore checkout: {root}  HEAD {head}")
    if head != PINNED:
        print(f"WARNING: the chapters are pinned to {PINNED}; line numbers will differ")

    print("\n== Common CLI: src/helpers/CommonCLI.cpp ==")
    common = []
    for no, func, tok, serial, guard in scan(root, "src/helpers/CommonCLI.cpp",
                                              {"handleCommand", "handleSetCmd",
                                               "handleGetCmd", "handleRegionCmd"}):
        print(f"r.{no:<5} {tok:<28} {'SERIAL' if serial else '':<7} {guard}")
        if not tok.startswith("  value"):
            common.append(tok)

    for role in CTOR:
        rel = CTOR[role]
        print(f"\n== Role-specific: {role} ({rel}, handleCommand) ==")
        for no, func, tok, serial, guard in scan(root, rel, {"handleCommand"}):
            print(f"r.{no:<5} {tok:<28} {'SERIAL' if serial else '':<7} {guard}")

    print("\n== Custom command hook: sensor (examples/simple_sensor/main.cpp) ==")
    for no, func, tok, serial, guard in scan(root, "examples/simple_sensor/main.cpp",
                                              {"handleCustomCommand"}):
        print(f"r.{no:<5} {tok}")

    print("\n== Companion rescue CLI (examples/companion_radio/MyMesh.cpp) ==")
    for no, func, tok, serial, guard in scan(root, "examples/companion_radio/MyMesh.cpp",
                                              {"checkCLIRescueCmd"}):
        print(f"r.{no:<5} {tok}")

    print("\n== Callback overrides per role ==")
    for role in CTOR:
        h = (root / HEADER[role]).read_text()
        names = sorted(set(re.findall(
            r"\b(formatNeighborsReply|removeNeighbor|startRegionsLoad|saveRegions|"
            r"setRxBoostedGain|setBridgeState|restartBridge)\b[^;{]*override", h)))
        ns = "formatNeighborsReply -> not supported" if '"not supported"' in h else ""
        print(f"{role:<12} {', '.join(names)}  {ns}")

    print("\n== Macros ==")
    mac = {r: macros(root, FALLBACKS[r]) for r in CTOR}
    for k in ["LORA_FREQ", "LORA_BW", "LORA_SF", "LORA_CR", "LORA_TX_POWER"]:
        print(f"{k:<15} {mac['repeater'].get(k)}")
    print(f"-D LORA_FREQ/BW/SF/CR in variants/**/platformio.ini: "
          f"{variant_radio_overrides(root)}")
    for role in CTOR:
        print(f"{role:<12} ADVERT_NAME={mac[role].get('ADVERT_NAME', ('-',))[0]}  "
              f"ADMIN_PASSWORD={mac[role].get('ADMIN_PASSWORD', ('-',))[0]}")

    print("\n== Defaults per role (constructor, after memset) ==")
    ctor = {}
    for role, rel in CTOR.items():
        vals, span = ctor_defaults(root, rel)
        ctor[role] = (vals, span)
        print(f"{role:<12} {rel} r.{span[0]}-{span[1]}")

    def res(role, v):
        return mac[role].get(v, (v,))[0]

    print(f"{'setting':<26} " + " | ".join(f"{r:<22}" for r in CTOR))
    for field, name in FIELDS:
        cells = []
        for role in CTOR:
            vals = ctor[role][0]
            fs = field.split("/")
            if len(fs) > 1:
                cell = ",".join(res(role, vals[f][-1][1]) if f in vals else "0" for f in fs)
            elif field in vals:
                chosen = vals[field] if vals[field][-1][2] else vals[field][-1:]
                cell = "; ".join(f"{res(role, v)} (r.{ln}{' if ' + g if g else ''})"
                                 for ln, v, g in chosen)
            else:
                cell = "0 (memset)"
            cells.append(f"{cell:<22}")
        print(f"{name:<26} " + " | ".join(cells))

    print("\n== Which role reads the setting outside its constructor ==")
    for field in READ_CHECK:
        for role in CTOR:
            hits = readers(root, role, field, CTOR[role], ctor[role][1])
            print(f"{field:<24} {role:<12} {len(hits):>2}  {' '.join(hits[:2])}")

    print("\n== docs/cli_commands.md versus firmware ==")
    fw = {norm(t.split()) for t in common}
    fw |= {"setperm", "get acl", "discover.neighbors", "io", "magic"}
    doc = doc_commands(root)
    print("in firmware, not in doc:", ", ".join(sorted(fw - doc)) or "-")
    print("in doc, not in firmware:", ", ".join(sorted(doc - fw)) or "-")


def ftoa(f, precision=7):
    """StrHelper::ftoa (src/helpers/TxtDataHelpers.cpp): truncating, float32."""
    if f == 0.0:
        return "0.0"
    bits = struct.unpack("<i", struct.pack("<f", f))[0]
    exp2 = ((bits >> 23) & 0xFF) - 127
    mant = (bits & 0xFFFFFF) | 0x800000
    ip = fp = 0
    if exp2 >= 23:
        ip = mant << (exp2 - 23)
    elif exp2 >= 0:
        ip = mant >> (23 - exp2)
        fp = (mant << (exp2 + 1)) & 0xFFFFFF
    else:
        fp = (mant & 0xFFFFFF) >> -(exp2 + 1)
    out = ("-" if bits < 0 else "") + (str(ip) if ip else "0") + "."
    if fp == 0:
        return out + "0"
    digits = ""
    for _ in range(precision):
        fp = (fp << 3) + (fp << 1)
        digits += chr((fp >> 24) + 48)
        fp &= 0xFFFFFF
    return out + (digits.rstrip("0") or "0")


def ftoa3(f):
    """StrHelper::ftoa3: rounded to three decimals, trailing zeros removed."""
    v = int(f * 1000.0 + (0.5 if f >= 0 else -0.5))
    return f"{v // 1000}.{abs(v % 1000):03d}".rstrip("0").rstrip(".")


def examples():
    """Recomputes the example replies used in the chapters."""
    print("\n== Example replies ==")
    keys = {c: hashlib.sha256(("voorbeeld public key " + c).encode()).hexdigest().upper()
            for c in ("PE1HVH", "PE1RDP")}
    for c, k in keys.items():
        print(f"example public key {c} (as in tools/dm-example.py): {k}")
    for c, secs, snr4 in (("PE1RDP", 312, 26), ("PE1HVH", 1840, -6)):
        print(f"neighbors line {c}: {keys[c][:8]}:{secs}:{snr4}  (SNR {snr4 / 4} dB)")
    ts = 1785412800
    dt = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)
    print(f"clock at {ts} -> {dt.hour:02d}:{dt.minute:02d} - {dt.day}/{dt.month}/{dt.year} UTC")
    clk = datetime.datetime.fromtimestamp(1715770351, datetime.timezone.utc)
    print(f"clkreboot sets 1715770351 = {clk.isoformat()}")
    for dc in (50, 10):
        af = 100.0 / dc - 1.0
        act = 100.0 / (af + 1.0)
        print(f"set dutycycle {dc} -> af {af} -> OK - "
              f"{int(act)}.{int((act - int(act)) * 10 + 0.5)}%")
    print(f"get af (af 9) -> > {ftoa(9.0)}   get af (default) -> > {ftoa(1.0)}")
    print(f"get radio (build default) -> > {ftoa(869.618)},{ftoa3(62.5)},8,5")
    print(f"get radio (after set radio 869.618,62.5,7,5) -> > {ftoa(869.618)},{ftoa3(62.5)},7,5")
    print(f"get freq -> > {ftoa(869.618)}")
    print(f"get lat 52.5168 -> > {ftoa(52.5168)}   get lon 6.083 -> > {ftoa(6.083)}")
    for v in (0.5, 0.3, 0.2, 0.0):
        print(f"ftoa({v}) -> {ftoa(v)}")
    print(f"set agc.reset.interval 17 -> OK - interval rounded to {17 // 4 * 4}")
    print(f"set advert.interval 240 -> stored {240 // 2}, get -> > {240 // 2 * 2}")
    print(f"set adc.multiplier 1.05 -> OK - multiplier set to {1.05:.3f}")


def all_commands(root):
    out = {}
    for no, func, tok, serial, guard in scan(root, "src/helpers/CommonCLI.cpp",
                                              {"handleCommand", "handleSetCmd",
                                               "handleGetCmd", "handleRegionCmd"}):
        if not tok.startswith("  value"):
            out.setdefault(tok, f"src/helpers/CommonCLI.cpp r.{no} {guard}".strip())
    for p in sorted((root / "src/helpers").rglob("*CLI*.h")):
        rel = str(p.relative_to(root))
        for no, func, tok, serial, guard in scan(root, rel):
            if not tok.startswith("  value"):
                out.setdefault(tok, f"{rel} r.{no} {guard}".strip())
    return out


def newer(root, other):
    print(f"\n== Commands in {other} (HEAD {head_of(other)}) and not in {root} ==")
    a, b = all_commands(root), all_commands(other)
    for tok in sorted(set(b) - set(a)):
        print(f"{tok:<28} {b[tok]}")


if __name__ == "__main__":
    first = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "MeshCore")
    main(first)
    examples()
    if len(sys.argv) > 2:
        newer(first, pathlib.Path(sys.argv[2]))
