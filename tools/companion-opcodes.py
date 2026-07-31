# -*- coding: utf-8 -*-
"""Reproduceert de opcodetabellen en dekkingscijfers uit companion/.

   Bron — uitgepakte klonen van drie officiële repositories op de commits die
   de hoofdstukken pinnen:
     meshcore-dev/MeshCore      examples/companion_radio/MyMesh.cpp
                                examples/companion_radio/MyMesh.h
                                src/helpers/BaseSerialInterface.h
                                docs/companion_protocol.md
     meshcore-dev/meshcore_py   src/meshcore/packets.py
     meshcore-dev/meshcore.js   src/constants.js

   Gebruik:
     python3 tools/companion-opcodes.py --repo ../MeshCore \\
         --meshcore-py ../meshcore_py --meshcore-js ../meshcore.js

   Alleen `--repo` is verplicht. Ontbreekt een van de twee libraries, dan
   blijft de bijbehorende kolom in de dekkingstabel leeg en zegt de uitvoer
   dat erbij. Een ontbrekende bron wordt nooit als nul geteld.

   Telmethode:

   - **Een opcode is een `#define` op kolom 0 in `MyMesh.cpp`.** De vier
     families worden op naam onderscheiden: `CMD_`, `RESP_`, `PUSH_CODE_` en
     `ERR_CODE_`. `STATS_TYPE_`, `AUTO_ADD_` en `MAX_`-constanten zijn geen
     opcodes en tellen niet mee, ook al staan ze in hetzelfde blok.
   - **`RESP_ALLOWED_REPEAT_FREQ` hoort bij de antwoordcodes.** Die ene naam
     mist het `_CODE`-deel dat de 28 andere wel hebben. Op naamprefix `RESP_`
     tellen levert 29; op `RESP_CODE_` tellen levert er 28 en dat is fout.
   - **Nummerruimtes overlappen.** Antwoordcodes lopen vanaf 0, pushcodes
     vanaf `0x80`. Ze zitten in hetzelfde eerste frame-byte en worden daarom
     samen geteld waar het over "wat de node terugstuurt" gaat.
   - **Een commando geldt als afgehandeld** wanneer de naam voorkomt in een
     vergelijking `cmd_frame[0] == <naam>`. Dat is de vorm die de
     else-if-keten in `MyMesh.cpp` gebruikt; een `#define` zonder zo'n
     vergelijking is een gereserveerd nummer, geen werkend commando.
   - **Dekking door de officiële spec wordt op naam gemeten**, niet op
     nummer: `docs/companion_protocol.md` schrijft commando's voluit als
     `CMD_APP_START`. Een commando dat alleen in proza omschreven staat
     zonder zijn constante te noemen, telt niet als gedekt — dat is streng,
     maar het is de enige maat die reproduceerbaar is.
   - **Dekking door de libraries wordt op nummer gemeten.** Beide libraries
     hernoemen de constanten (`DEVICE_QEURY`, `SendChannelData`), dus de
     naam is geen betrouwbare sleutel en het nummer wel.
   - **Grenswaarden worden per build-target geteld, niet uit de header
     gelezen.** `MAX_CONTACTS`, `OFFLINE_QUEUE_SIZE` en
     `MAX_GROUP_CHANNELS` staan in `MyMesh.h` achter `#ifndef` of komen daar
     helemaal niet voor; de werkelijke waarde komt uit een `-D`-vlag in
     `platformio.ini`. Een companion-target is een `[env:…]`-sectie waarvan
     `build_src_filter` `../examples/companion_radio` bevat, met `extends`
     en `${sectie.optie}` opgelost — beide overervingsmechanismen, want wie
     er maar een volgt, mist targets. Uitgecommentarieerde `-D`-regels
     tellen niet mee. De uitkomst wordt tegen `tools/design-overview.py`
     gelegd: die telt op dezelfde manier en moet hetzelfde aantal targets
     opleveren.

   De uitvoer is bedoeld om naast het hoofdstuk te leggen. Wijkt een cijfer
   af, dan is dat een discrepantie voor de opdrachtgever en geen reden om het
   hoofdstuk of het script eigenmachtig bij te stellen.
"""
import argparse
import json
import os
import re

COMMIT = '03b6ef4'
VERSIE = 'v1.16.0'
DATUM = '28 juli 2026'

MYMESH_CPP = os.path.join('examples', 'companion_radio', 'MyMesh.cpp')
MYMESH_H = os.path.join('examples', 'companion_radio', 'MyMesh.h')
BASE_SERIAL = os.path.join('src', 'helpers', 'BaseSerialInterface.h')
SPEC = os.path.join('docs', 'companion_protocol.md')

# Clusters waarin het hoofdstuk de commando's presenteert. De sleutel is de
# clusternaam, de waarde een lijst commandonummers. Elk nummer komt in precies
# een cluster voor; het script controleert dat en klaagt als dat niet klopt.
CLUSTERS = [
    ('Sessie en apparaat', [1, 22, 5, 6, 19, 51, 37, 20, 56, 43, 21, 38]),
    ('Identiteit en advert', [7, 8, 14, 23, 24, 42, 33, 34, 35]),
    ('Contacten', [4, 9, 15, 16, 17, 18, 30, 58, 59]),
    ('Kanalen', [31, 32]),
    ('Berichten', [2, 3, 10, 62, 25, 65]),
    ('Verbinding met andere nodes', [26, 27, 28, 29, 39, 50, 55, 57]),
    ('Radio en pad', [11, 12, 13, 36, 52, 61, 60]),
    ('Regio en scope', [54, 63, 64]),
    ('Eigen variabelen', [40, 41]),
]


def lees(pad):
    """Leest een bestand als tekst; CRLF wordt genormaliseerd naar LF."""
    with open(pad, encoding='utf-8', errors='replace') as f:
        return f.read().replace('\r\n', '\n')


def defines(tekst, prefix):
    """Alle `#define <prefix>…` op kolom 0, als {naam: nummer}.

    Decimaal en hexadecimaal worden allebei gelezen; `int(x, 0)` leidt de
    basis af uit de `0x`-prefix.
    """
    patroon = r'^#define\s+(' + prefix + r'\w+)\s+(0[xX][0-9A-Fa-f]+|\d+)'
    return {naam: int(waarde, 0)
            for naam, waarde in re.findall(patroon, tekst, re.M)}


def afgehandeld(tekst, namen):
    """Welke commandonamen in een `cmd_frame[0] == …`-vergelijking staan."""
    return {naam for naam in namen
            if re.search(r'cmd_frame\[0\]\s*==\s*' + naam + r'\b', tekst)}


def constante(tekst, naam):
    """Een enkele `#define <naam> <waarde>`, of None.

    De waarde loopt tot het einde van de regel of tot een `//`-commentaar,
    want `FIRMWARE_BUILD_DATE` bevat spaties. Omringende aanhalingstekens
    worden verwijderd.
    """
    m = re.search(r'^#define\s+' + naam + r'\s+(.+?)\s*(?://.*)?$', tekst, re.M)
    if not m:
        return None
    return m.group(1).strip().strip('"')


def py_nummers(pad):
    """Commandonummers uit `CommandType` en antwoordnummers uit `PacketType`."""
    tekst = lees(pad)
    uit = {}
    for blok, sleutel in (('CommandType', 'cmd'), ('PacketType', 'resp')):
        m = re.search(r'class ' + blok + r'\(Enum\):(.*?)(?=\nclass |\Z)',
                      tekst, re.S)
        if not m:
            uit[sleutel] = None
            continue
        uit[sleutel] = {int(w, 0) for w in
                        re.findall(r'^\s+\w+\s*=\s*(0[xX][0-9A-Fa-f]+|\d+)',
                                   m.group(1), re.M)}
    return uit


def js_nummers(pad):
    """Commandonummers uit `Constants.CommandCodes` in meshcore.js."""
    tekst = lees(pad)
    m = re.search(r'CommandCodes\s*=\s*\{(.*?)\n\s*\}', tekst, re.S)
    if not m:
        return None
    return {int(w) for w in re.findall(r':\s*(\d+)\s*,', m.group(1))}


def spec_dekking(tekst, namen):
    """Welke opcodenamen letterlijk in de officiële spec voorkomen."""
    return {naam for naam in namen if naam in tekst}


MARKERING = '../examples/companion_radio'
GRENZEN = ('MAX_CONTACTS', 'OFFLINE_QUEUE_SIZE', 'MAX_GROUP_CHANNELS')


def ini_bestanden(repo):
    """De root-ini plus elke variants/*/platformio.ini."""
    paden = [os.path.join(repo, 'platformio.ini')]
    wortel = os.path.join(repo, 'variants')
    for d in sorted(os.listdir(wortel)):
        pad = os.path.join(wortel, d, 'platformio.ini')
        if os.path.isfile(pad):
            paden.append(pad)
    return paden


def zonder_commentaar(regel):
    """Strip `;`-commentaar, maar niet binnen een `-D`-waarde met puntkomma."""
    kaal = regel.strip()
    if kaal.startswith(';'):
        return ''
    return regel


def lees_secties(repo):
    """Alle `[sectie]`-blokken uit alle ini-bestanden, als {naam: {optie: tekst}}."""
    secties = {}
    for pad in ini_bestanden(repo):
        naam = None
        optie = None
        for regel in lees(pad).split('\n'):
            regel = zonder_commentaar(regel)
            if not regel.strip():
                continue
            m = re.match(r'^\[([^\]]+)\]', regel)
            if m:
                naam = m.group(1)
                secties.setdefault(naam, {})
                optie = None
                continue
            if naam is None:
                continue
            m = re.match(r'^(\w+)\s*=\s*(.*)$', regel)
            if m:
                optie = m.group(1)
                secties[naam][optie] = m.group(2)
            elif regel[:1] in ' \t' and optie:
                secties[naam][optie] += '\n' + regel.strip()
    return secties


def voorouders(secties, naam, gezien=None):
    """Elke sectie die via `extends` bereikbaar is, dichtstbijzijnde eerst."""
    gezien = gezien or set()
    if naam in gezien or naam not in secties:
        return []
    gezien.add(naam)
    uit = [naam]
    for ouder in re.split(r'[,\s]+', secties[naam].get('extends', '').strip()):
        if ouder:
            uit += voorouders(secties, ouder, gezien)
    return uit


def optie(secties, naam, sleutel, diepte=0):
    """Een optie, met `extends` gevolgd en `${sectie.optie}` uitgevouwen."""
    if diepte > 8:
        return ''
    waarde = None
    for s in voorouders(secties, naam):
        if sleutel in secties.get(s, {}):
            waarde = secties[s][sleutel]
            break
    if waarde is None:
        return ''

    def vervang(m):
        return optie(secties, m.group(1), m.group(2), diepte + 1)

    return re.sub(r'\$\{([^.}]+)\.([^}]+)\}', vervang, waarde)


def companion_targets(secties):
    """De `[env:…]`-secties die companion_radio compileren."""
    uit = []
    for naam in secties:
        if not naam.startswith('env:'):
            continue
        if MARKERING in optie(secties, naam, 'build_src_filter'):
            uit.append(naam)
    return sorted(uit)


def grenswaarden(secties, targets):
    """Per grensconstante een {waarde: aantal targets}-verdeling."""
    uit = {g: {} for g in GRENZEN}
    for naam in targets:
        vlaggen = optie(secties, naam, 'build_flags')
        for g in GRENZEN:
            m = re.search(r'-D\s*' + g + r'\s*=\s*(\d+)', vlaggen)
            sleutel = int(m.group(1)) if m else 'niet gezet'
            uit[g][sleutel] = uit[g].get(sleutel, 0) + 1
    return uit


def tabel(rijen, koppen):
    """Markdown-tabel met een scheidingsrij."""
    uit = ['| ' + ' | '.join(koppen) + ' |',
           '|' + '|'.join(['---'] * len(koppen)) + '|']
    for rij in rijen:
        uit.append('| ' + ' | '.join(str(c) for c in rij) + ' |')
    return '\n'.join(uit)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--repo', required=True,
                   help='pad naar een kloon van meshcore-dev/MeshCore')
    p.add_argument('--meshcore-py', default=None,
                   help='pad naar een kloon van meshcore-dev/meshcore_py')
    p.add_argument('--meshcore-js', default=None,
                   help='pad naar een kloon van meshcore-dev/meshcore.js')
    p.add_argument('--json', default=None,
                   help='schrijf de momentopname naar dit pad')
    args = p.parse_args()

    cpp = lees(os.path.join(args.repo, MYMESH_CPP))
    hdr = lees(os.path.join(args.repo, MYMESH_H))
    ser = lees(os.path.join(args.repo, BASE_SERIAL))
    spec = lees(os.path.join(args.repo, SPEC))

    cmds = defines(cpp, 'CMD_')
    resp = defines(cpp, 'RESP_')
    push = defines(cpp, 'PUSH_CODE_')
    errs = defines(cpp, 'ERR_CODE_')
    klaar = afgehandeld(cpp, cmds)

    ver_code = constante(hdr, 'FIRMWARE_VER_CODE')
    fw_versie = constante(hdr, 'FIRMWARE_VERSION')
    bouwdatum = constante(hdr, 'FIRMWARE_BUILD_DATE')
    max_contacts = constante(hdr, 'MAX_CONTACTS')
    queue = constante(hdr, 'OFFLINE_QUEUE_SIZE')
    frame = constante(ser, 'MAX_FRAME_SIZE')

    print('MeshCore %s, commit %s, %s' % (VERSIE, COMMIT, DATUM))
    print('bron: %s' % MYMESH_CPP)
    print()
    print('Constanten')
    print('  FIRMWARE_VER_CODE    %s' % ver_code)
    print('  FIRMWARE_VERSION     %s' % fw_versie)
    print('  FIRMWARE_BUILD_DATE  %s' % bouwdatum)
    print('  MAX_FRAME_SIZE       %s' % frame)
    print('  MAX_CONTACTS         %s' % max_contacts)
    print('  OFFLINE_QUEUE_SIZE   %s' % queue)
    print()
    print('Opcodes')
    print('  CMD_          %3d  waarvan afgehandeld: %d' % (len(cmds), len(klaar)))
    print('  RESP_         %3d' % len(resp))
    print('  PUSH_CODE_    %3d' % len(push))
    print('  ERR_CODE_     %3d' % len(errs))
    print()

    # Gereserveerde nummers: gaten in de reeks 1..hoogste commandonummer.
    gebruikt = sorted(cmds.values())
    gaten = [n for n in range(1, max(gebruikt) + 1) if n not in gebruikt]
    print('Ongebruikte commandonummers in 1..%d: %s' %
          (max(gebruikt), ', '.join(str(g) for g in gaten)))
    print()

    # Dekking.
    namen_cmd = set(cmds)
    namen_resp = set(resp) | set(push)
    spec_cmd = spec_dekking(spec, namen_cmd)
    spec_resp = spec_dekking(spec, namen_resp)

    py = py_nummers(os.path.join(args.meshcore_py, 'src', 'meshcore',
                                 'packets.py')) if args.meshcore_py else None
    js = js_nummers(os.path.join(args.meshcore_js, 'src',
                                 'constants.js')) if args.meshcore_js else None

    nummers_cmd = set(cmds.values())
    nummers_resp = set(resp.values()) | set(push.values())

    def cel(deel, geheel):
        if deel is None:
            return 'niet opgegeven'
        return '%d/%d' % (len(deel & geheel), len(geheel))

    rijen = [
        ['firmware `MyMesh.cpp`',
         '%d/%d' % (len(klaar), len(cmds)),
         '%d/%d' % (len(namen_resp), len(namen_resp))],
        ['`meshcore_py`',
         cel(py['cmd'] if py else None, nummers_cmd),
         cel(py['resp'] if py else None, nummers_resp)],
        ['`meshcore.js`',
         cel(js, nummers_cmd),
         'niet vergeleken'],
        ['`docs/companion_protocol.md`',
         '%d/%d' % (len(spec_cmd), len(namen_cmd)),
         '%d/%d' % (len(spec_resp), len(namen_resp))],
    ]
    print('Dekking')
    print(tabel(rijen, ['Bron', 'Commando\'s', 'Antwoord- en pushcodes']))
    print()

    if py and py['cmd'] is not None:
        mist = sorted(nummers_cmd - py['cmd'])
        omgekeerd = {v: k for k, v in cmds.items()}
        print('Niet in meshcore_py: %s' %
              ', '.join('%s (%d)' % (omgekeerd[n], n) for n in mist))
    if js is not None:
        mist = sorted(nummers_cmd - js)
        omgekeerd = {v: k for k, v in cmds.items()}
        print('Niet in meshcore.js: %s' %
              ', '.join('%s (%d)' % (omgekeerd[n], n) for n in mist))
    print()

    # Clustercontrole: elk commandonummer precies een keer.
    geclusterd = [n for _, ns in CLUSTERS for n in ns]
    dubbel = sorted({n for n in geclusterd if geclusterd.count(n) > 1})
    ontbreekt = sorted(nummers_cmd - set(geclusterd))
    onbekend = sorted(set(geclusterd) - nummers_cmd)
    if dubbel or ontbreekt or onbekend:
        print('LET OP — clusterindeling klopt niet met de firmware:')
        if dubbel:
            print('  dubbel ingedeeld: %s' % dubbel)
        if ontbreekt:
            print('  niet ingedeeld:   %s' % ontbreekt)
        if onbekend:
            print('  bestaat niet:     %s' % onbekend)
    else:
        print('Clusterindeling dekt alle %d commando\'s precies een keer.'
              % len(nummers_cmd))
    print()

    secties = lees_secties(args.repo)
    targets = companion_targets(secties)
    verdeling = grenswaarden(secties, targets)
    print('Companion build-targets: %d' % len(targets))
    print('  (tools/design-overview.py telt op dezelfde manier; wijkt dit af,')
    print('   dan is een van de twee resolvers stuk)')
    for g in GRENZEN:
        kaal = constante(hdr, g)
        deel = ', '.join('%s: %d' % (k, v) for k, v in
                         sorted(verdeling[g].items(), key=lambda kv: str(kv[0])))
        print('  %-20s header: %-12s targets: %s'
              % (g, kaal if kaal else 'niet in MyMesh.h', deel))
    print()

    omgekeerd = {v: k for k, v in cmds.items()}
    for naam, nummers in CLUSTERS:
        print('%s (%d)' % (naam, len(nummers)))
        for n in nummers:
            print('  %3d  %s' % (n, omgekeerd[n]))
        print()

    momentopname = {
        'meshcore': {'versie': VERSIE, 'commit': COMMIT, 'datum': DATUM},
        'constanten': {
            'FIRMWARE_VER_CODE': ver_code,
            'FIRMWARE_VERSION': fw_versie,
            'FIRMWARE_BUILD_DATE': bouwdatum,
            'MAX_FRAME_SIZE': frame,
            'MAX_CONTACTS': max_contacts,
            'OFFLINE_QUEUE_SIZE': queue,
        },
        'aantallen': {
            'commandos': len(cmds),
            'afgehandeld': len(klaar),
            'antwoordcodes': len(resp),
            'pushcodes': len(push),
            'foutcodes': len(errs),
        },
        'ongebruikte_nummers': gaten,
        'companion_targets': len(targets),
        'grenswaarden_per_target': {
            g: {str(k): v for k, v in sorted(verdeling[g].items(),
                                             key=lambda kv: str(kv[0]))}
            for g in GRENZEN
        },
        'commandos': {naam: nummer for naam, nummer in sorted(cmds.items(),
                                                             key=lambda kv: kv[1])},
        'antwoordcodes': {naam: nummer for naam, nummer in sorted(resp.items(),
                                                                  key=lambda kv: kv[1])},
        'pushcodes': {naam: nummer for naam, nummer in sorted(push.items(),
                                                              key=lambda kv: kv[1])},
        'foutcodes': {naam: nummer for naam, nummer in sorted(errs.items(),
                                                              key=lambda kv: kv[1])},
        'dekking': {
            'spec_commandos': len(spec_cmd),
            'spec_antwoordcodes': len(spec_resp),
            'meshcore_py_commandos': (len(py['cmd'] & nummers_cmd)
                                      if py and py['cmd'] is not None else None),
            'meshcore_py_antwoordcodes': (len(py['resp'] & nummers_resp)
                                          if py and py['resp'] is not None else None),
            'meshcore_js_commandos': (len(js & nummers_cmd)
                                      if js is not None else None),
        },
    }
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(momentopname, f, indent=2, ensure_ascii=False,
                      sort_keys=False)
            f.write('\n')
        print('Momentopname geschreven naar %s' % args.json)


if __name__ == '__main__':
    main()
