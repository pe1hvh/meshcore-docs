#!/usr/bin/env python3
"""Deel de klassen van MeshCore in de drie groepen van het klassenmodel in.

Groep 1 — de contracten — is een benoemde lijst. Dat is bewust: of een klasse
een contract is, valt niet mechanisch af te lezen. `DisplayDriver` heeft
`width()` en `height()` met een body en is toch een contract; `ESP32Board`
heeft virtuele methoden en is er toch geen. De maatstaf staat in het hoofdstuk
zelf: beschrijft de klasse wat een ander onderdeel mag verwachten, kent de
gebruiker alleen het contract, en zijn de implementaties onderling
verwisselbaar.

Groep 2 en groep 3 volgen daar mechanisch uit: alles wat — rechtstreeks of via
tussenliggende klassen — van een klasse uit groep 1 erft, staat in groep 2; de
rest staat in groep 3.

Gebruik:

    python3 tools/class-groups.py /pad/naar/MeshCore
    python3 tools/class-groups.py /pad/naar/MeshCore --groep 1 --markdown
    python3 tools/class-groups.py /pad/naar/MeshCore --variants
    python3 tools/class-groups.py /pad/naar/MeshCore --vergelijk /pad/naar/oude

De klassentelling zelf komt uit `tools/design-overview.py`; dit script
hergebruikt die parser, zodat beide hoofdstukken op dezelfde telmethode
staan. `struct` telt niet mee, voorwaartse declaraties zonder body evenmin.
"""

import argparse
import importlib.util
import os
import sys
from collections import Counter, OrderedDict

HIER = os.path.dirname(os.path.abspath(__file__))

# Groep 1 — de contracten, met het Nederlandse etiket dat het hoofdstuk
# gebruikt in de kolom *Contract* van groep 2.
CONTRACTEN = OrderedDict([
    ("DataStoreHost", "Opslag"),
    ("MillisecondClock", "Klok"),
    ("Radio", "Radio"),
    ("PacketManager", "Pakketbeheer"),
    ("MeshTables", "Meshtabellen"),
    ("MainBoard", "Bord"),
    ("RTCClock", "Realtimeklok"),
    ("RNG", "Entropiebron"),
    ("AbstractBridge", "Brug"),
    ("BaseSerialInterface", "Seriële verbinding"),
    ("CommonCLICallbacks", "CLI-terugroep"),
    ("SensorManager", "Sensorbeheer"),
    ("LocationProvider", "Plaatsbepaling"),
    ("DisplayDriver", "Scherm"),
    # Nieuw op d929643:
    ("ConfigSerializer", "Instellingenblok"),
    ("ExternalWatchdogManager", "Externe watchdog"),
    ("RotaryInput", "Draaiknop"),
])

# De Engelse spiegel gebruikt dezelfde volgorde en dezelfde sleutels.
CONTRACTEN_EN = OrderedDict([
    ("DataStoreHost", "Storage"),
    ("MillisecondClock", "Millisecond clock"),
    ("Radio", "Radio"),
    ("PacketManager", "Packet pool"),
    ("MeshTables", "Seen table"),
    ("MainBoard", "Board"),
    ("RTCClock", "Clock"),
    ("RNG", "Entropy"),
    ("AbstractBridge", "Bridge"),
    ("BaseSerialInterface", "Interface"),
    ("CommonCLICallbacks", "CLI callback"),
    ("SensorManager", "Sensor management"),
    ("LocationProvider", "Location"),
    ("DisplayDriver", "Display"),
    ("ConfigSerializer", "Settings block"),
    ("ExternalWatchdogManager", "External watchdog"),
    ("RotaryInput", "Rotary input"),
])

ETIKET = CONTRACTEN


def laad_parser():
    pad = os.path.join(HIER, "design-overview.py")
    spec = importlib.util.spec_from_file_location("design_overview", pad)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def kale_naam(basis):
    """`public mesh::Radio` → `Radio`."""
    for woord in ("public", "protected", "private", "virtual"):
        basis = basis.replace(woord + " ", "")
    return basis.strip().split("::")[-1].split("<")[0].strip()


def indeling(gevonden):
    """(groep, naam, pad, regel, basissen) per klasse."""
    basissen = {}
    for naam, bases, _, _ in gevonden:
        basissen.setdefault(naam, set()).update(kale_naam(b) for b in bases)

    def erft_van_contract(namen, gezien=None):
        """Elk contract uit groep 1 dat vanaf deze basissen bereikbaar is.

        De aanroeper geeft de basissen van één declaratie mee, niet een
        klassenaam: `MyMesh` bestaat vijf keer met verschillende ouders, en
        een naamsleutel zou die vijf op één hoop gooien.
        """
        gezien = gezien if gezien is not None else set()
        uit = []
        for basis in namen:
            if basis in gezien:
                continue
            gezien.add(basis)
            if basis in CONTRACTEN:
                if basis not in uit:
                    uit.append(basis)
                continue
            for dieper in erft_van_contract(basissen.get(basis, ()), gezien):
                if dieper not in uit:
                    uit.append(dieper)
        return uit

    uit = []
    for naam, bases, pad, regel in gevonden:
        if naam in CONTRACTEN:
            groep, contract = 1, []
        else:
            contract = erft_van_contract([kale_naam(b) for b in bases])
            groep = 2 if contract else 3
        uit.append((groep, naam, pad, regel,
                    [kale_naam(b) for b in bases], contract))
    return uit


def tabel(rijen, groep):
    if groep == 1:
        print("| Klasse | Plek |")
        print("|---|---|")
        for _, naam, pad, regel, _, _ in rijen:
            print("| `%s` | `%s` r.%d |" % (naam, pad, regel))
    elif groep == 2:
        print("| Klasse | Contract | Plek | Erft van |")
        print("|---|---|---|---|")
        for _, naam, pad, regel, bases, contract in rijen:
            print("| `%s` | %s | `%s` r.%d | %s |"
                  % (naam, ", ".join(ETIKET[c] for c in contract), pad, regel,
                     ", ".join(bases) or "—"))
    else:
        print("| Klasse | Plek |")
        print("|---|---|")
        for _, naam, pad, regel, _, _ in rijen:
            print("| `%s` | `%s` r.%d |" % (naam, pad, regel))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("root", help="pad naar een MeshCore-checkout")
    p.add_argument("--groep", type=int, choices=(1, 2, 3))
    p.add_argument("--variants", action="store_true",
                   help="de klassen uit variants/ in plaats van de gedeelde boom")
    p.add_argument("--markdown", action="store_true", help="als tabelrijen")
    p.add_argument("--taal", choices=("nl", "en"), default="nl",
                   help="taal van de contractnamen in de kolom Contract")
    p.add_argument("--vergelijk", metavar="ROOT",
                   help="toon het verschil met een tweede checkout")
    args = p.parse_args()

    global ETIKET
    ETIKET = CONTRACTEN_EN if args.taal == "en" else CONTRACTEN

    do = laad_parser()
    gevonden = do.classes(args.root)
    alles = indeling(gevonden)

    if args.vergelijk:
        oud = {(n, p) for _, n, p, _, _, _ in indeling(do.classes(args.vergelijk))}
        nu = {(n, p) for _, n, p, _, _, _ in alles}
        print("Erbij (%d)" % len(nu - oud))
        for naam, pad in sorted(nu - oud):
            groep = next(g for g, n, p, _, _, _ in alles if (n, p) == (naam, pad))
            print("  groep %d  %-30s %s" % (groep, naam, pad))
        print("\nEraf (%d)" % len(oud - nu))
        for naam, pad in sorted(oud - nu):
            print("  %-30s %s" % (naam, pad))
        return 0

    gedeeld = [r for r in alles if not r[2].startswith("variants" + os.sep)]
    variant = [r for r in alles if r[2].startswith("variants" + os.sep)]
    rijen = variant if args.variants else gedeeld

    if args.groep:
        gekozen = sorted([r for r in rijen if r[0] == args.groep],
                         key=lambda r: (r[2], r[3]))
        if args.markdown:
            tabel(gekozen, args.groep)
        else:
            for _, naam, pad, regel, bases, contract in gekozen:
                print("%-34s %s r.%d%s" % (naam, pad, regel,
                      "   ← " + ", ".join(contract) if contract else ""))
        print("\n(%d klassen)" % len(gekozen) if not args.markdown else "")
        return 0

    telling = Counter(r[0] for r in gedeeld)
    print("Gedeelde boom  src/ + examples/")
    print("  groep 1 — contracten          %4d" % telling[1])
    print("  groep 2 — implementaties      %4d" % telling[2])
    print("  groep 3 — zelfstandig         %4d" % telling[3])
    print("  totaal                        %4d" % len(gedeeld))

    telling = Counter(r[0] for r in variant)
    print("\nvariants/")
    print("  groep 2 — implementaties      %4d" % telling[2])
    print("  groep 3 — zelfstandig         %4d" % telling[3])
    print("  totaal                        %4d  (%d unieke namen)"
          % (len(variant), len({r[1] for r in variant})))

    print("\nvariants/ per contract")
    per = Counter(r[5][0] for r in variant if r[5])
    for contract in CONTRACTEN:
        if per[contract]:
            print("  %-24s %-20s %4d"
                  % (ETIKET[contract], contract, per[contract]))
    los = [r for r in variant if not r[5]]
    if los:
        print("  %-24s %-20s %4d" % ("zonder contract", "—", len(los)))
        for _, naam, pad, _, _, _ in sorted(los, key=lambda r: r[2]):
            print("      %-28s %s" % (naam, pad))

    print("\nbordklassen per gedeelde ouder")
    ouders = Counter()
    for _, naam, pad, _, bases, contract in variant:
        if contract and contract[0] in ("MainBoard", "Board"):
            ouders[bases[0] if bases else "—"] += 1
    for ouder, aantal in ouders.most_common():
        print("  %-24s %4d" % (ouder, aantal))
    return 0


if __name__ == "__main__":
    sys.exit(main())
