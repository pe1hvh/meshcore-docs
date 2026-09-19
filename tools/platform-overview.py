# -*- coding: utf-8 -*-
"""Reproduceert de tabellen uit het hoofdstuk 'MeshCore Platforms'.

   Bron 1 — een uitgepakte kloon van meshcore-dev/MeshCore:
     platformio.ini              de vier platformbases en hun build-flags
     variants/*/platformio.ini   79 varianten, 507 [env:]-blokken
     boards/*.json               board-definities met mcu, f_cpu, ram, flash

   Bron 2 — config.json uit een kloon van meshcore-dev/flasher.meshcore.io,
   de bronrepo van de MeshCore web flasher (MIT). Het veld "device" is een
   lijst apparaten met "name", "maker", "type" (esp32 / nrf52 / noflash) en
   per apparaat de firmwarerollen die de flasher aanbiedt. Pin deze bron op
   een commit, net als de firmware; een opgeslagen HTML-pagina is niet meer
   nodig.

   Gebruik:
     python3 tools/platform-overview.py --repo ../MeshCore [--flasher-config ../flasher.meshcore.io/config.json]

   Zonder --flasher-config blijft tabel 4 leeg; de overige tabellen werken dan wel.
   Alle getallen in het hoofdstuk moeten met de uitvoer van dit script
   overeenkomen. Cijfers die hier niet uit komen (RP2040-datasheet,
   Espressif-datasheets) staan in het hoofdstuk als externe bron gemarkeerd.
"""
import argparse, glob, json, os, re
from collections import Counter, defaultdict

FAMILIES = ['ESP32', 'nRF52', 'RP2040', 'STM32WL']

# ---- welke [*_base] hoort bij welke familie ---------------------------------
BASE_TO_FAMILY = {
    'esp32_base':   'ESP32',
    'esp32c6_base': 'ESP32',      # erft van esp32_base, platformio.ini r.75
    'nrf52_base':   'nRF52',
    'rp2040_base':  'RP2040',
    'stm32_base':   'STM32WL',
}


def lees_varianten(repo):
    """Loopt variants/*/platformio.ini af en bepaalt per variant de familie."""
    varianten = []
    for pad in sorted(glob.glob(os.path.join(repo, 'variants', '*', 'platformio.ini'))):
        naam = os.path.basename(os.path.dirname(pad))
        tekst = open(pad, encoding='utf-8', errors='replace').read()
        extends = ' '.join(re.findall(r'^\s*extends\s*=\s*(.+)$', tekst, re.M))
        familie = c6 = None
        for base, fam in BASE_TO_FAMILY.items():
            if base in extends:
                familie = fam
                c6 = (base == 'esp32c6_base')
                break
        if familie is None:
            continue
        varianten.append({
            'naam':    naam,
            'familie': familie,
            'c6':      c6,
            'boards':  sorted(set(re.findall(r'^\s*board\s*=\s*(\S+)', tekst, re.M))),
            'envs':    re.findall(r'^\[env:([^\]]+)\]', tekst, re.M),
            'display': bool(re.search(r'DISPLAY_CLASS', tekst)),
            'espnow':  'espnow' in tekst.lower(),
            'ota':     'esp32_ota' in tekst,
        })
    return varianten


def rol_van(env):
    """Leidt de rol af uit de env-naam.

       De suffixen zijn projectbreed vrijwel gelijk, maar niet helemaal:
       er bestaan namen met een afsluitende underscore
       (`..._companion_radio_ble_`), namen zonder `radio`
       (`..._companion_ble`) en een handvol afkortingen in de
       generic-espnow-variant (`..._comp_radio_usb`, `..._repeatr`,
       `..._room_svr`). Daarom wordt eerst genormaliseerd.
    """
    n = env.strip().strip('_').lower()
    if 'companion' in n or '_comp_radio' in n:
        for staart, rol in (('ble', 'companion BLE'), ('wifi', 'companion WiFi'),
                            ('usb', 'companion USB'), ('serial', 'companion serial'),
                            ('ethernet', 'companion Ethernet')):
            if n.endswith(staart):
                return rol
        return 'companion ?'
    if n.endswith('room_server') or n.endswith('room_svr') or n.endswith('room_server_ethernet'):
        return 'room server'
    if n.endswith('kiss_modem'):
        return 'KISS modem'
    if n.endswith('sensor'):
        return 'sensor'
    if n.endswith('terminal_chat'):
        return 'terminal chat'
    if 'repeater' in n or n.endswith('repeatr'):
        return 'repeater'
    return 'overig'


def lees_boards(repo):
    """Haalt mcu, kloksnelheid, RAM en app-flash uit boards/*.json."""
    boards = {}
    for pad in sorted(glob.glob(os.path.join(repo, 'boards', '*.json'))):
        d = json.load(open(pad, encoding='utf-8'))
        build, upload = d.get('build', {}), d.get('upload', {})
        boards[os.path.basename(pad)[:-5]] = {
            'mcu':   build.get('mcu'),
            'f_cpu': build.get('f_cpu'),
            'ram':   upload.get('maximum_ram_size'),
            'flash': upload.get('maximum_size'),
        }
    return boards


def lees_flasher(pad):
    """Leest config.json van de web flasher: (familie, fabrikant, naam, rollen)."""
    with open(pad, encoding='utf-8') as fh:
        config = json.load(fh)
    makers = {k: v.get('name', k) for k, v in config.get('maker', {}).items()}
    familie_van = {'esp32': 'ESP32', 'nrf52': 'nRF52'}
    apparaten = []
    for dev in config.get('device', []):
        rollen = sorted({fw.get('role') for fw in dev.get('firmware', []) if fw.get('role')})
        apparaten.append({
            'familie': familie_van.get(dev.get('type'), dev.get('type') or 'onbekend'),
            'fabrikant': makers.get(dev.get('maker'), dev.get('maker') or ''),
            'naam': dev.get('name', '').strip(),
            'rollen': rollen,
        })
    return apparaten


def kop(titel):
    print()
    print(titel)
    print('=' * len(titel))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True, help='pad naar een kloon van meshcore-dev/MeshCore')
    p.add_argument('--flasher-config', dest='flasher_config',
                   help='pad naar config.json van meshcore-dev/flasher.meshcore.io')
    args = p.parse_args()

    varianten = lees_varianten(args.repo)
    boards = lees_boards(args.repo)

    # -- controle op de aannames uit het hoofdstuk ---------------------------
    kop('CONTROLES')
    pio = open(os.path.join(args.repo, 'platformio.ini'), encoding='utf-8').read()
    fw = open(os.path.join(args.repo, 'examples', 'simple_repeater', 'MyMesh.h'),
              encoding='utf-8').read()
    versie = re.search(r'FIRMWARE_VERSION\s+"([^"]+)"', fw)
    datum = re.search(r'FIRMWARE_BUILD_DATE\s+"([^"]+)"', fw)
    print('firmwareversie                :', versie.group(1) if versie else '?')
    print('build date                    :', datum.group(1) if datum else '?')
    aantal = sum(1 for r in open(os.path.join(args.repo, 'platformio.ini'),
                                 encoding='utf-8')
                 if r.strip().startswith('framework = arduino'))
    print('"framework = arduino" in root :', aantal, '(verwacht: 1)')
    override = [v['naam'] for v in varianten
                if re.search(r'^\s*framework\s*=',
                             open(os.path.join(args.repo, 'variants', v['naam'],
                                               'platformio.ini'),
                                  encoding='utf-8', errors='replace').read(), re.M)]
    print('varianten die framework zetten:', override or 'geen')
    fork = [v['naam'] for v in varianten
            if v['familie'] == 'nRF52'
            and 'platform_packages' in open(
                os.path.join(args.repo, 'variants', v['naam'], 'platformio.ini'),
                encoding='utf-8', errors='replace').read()]
    print('nRF52-varianten die de core-fork overschrijven:', ', '.join(fork) or 'geen')
    print('"experimental" bij esp32c6_base:', 'experimental' in pio)

    # -- tabel 1 -------------------------------------------------------------
    kop('TABEL 1 — de vier families')
    print('%-9s %10s %14s %8s' % ('familie', 'varianten', 'build-targets', 'display'))
    for fam in FAMILIES:
        vs = [v for v in varianten if v['familie'] == fam]
        print('%-9s %10d %14d %8d'
              % (fam, len(vs), sum(len(v['envs']) for v in vs),
                 sum(1 for v in vs if v['display'])))
    print('%-9s %10d %14d' % ('totaal', len(varianten),
                              sum(len(v['envs']) for v in varianten)))
    print()
    print('sub-SoC binnen ESP32 (uit board = ... en boards/*.json):')
    socs = Counter()
    for v in varianten:
        if v['familie'] != 'ESP32':
            continue
        for b in v['boards']:
            socs[boards.get(b, {}).get('mcu') or 'PlatformIO-ingebouwd: ' + b] += 1
    for soc, n in sorted(socs.items(), key=lambda x: -x[1]):
        print('  %-40s %3d' % (soc, n))
    print()
    print('geheugen per familie (alleen boards/*.json, dus niet compleet):')
    for fam in FAMILIES:
        namen = {b for v in varianten if v['familie'] == fam for b in v['boards']}
        rams = sorted({boards[b]['ram'] for b in namen if b in boards and boards[b]['ram']})
        fls = sorted({boards[b]['flash'] for b in namen if b in boards and boards[b]['flash']})
        print('  %-8s RAM %s  flash %s' % (fam, rams or '—', fls or '—'))

    # -- tabel 3 -------------------------------------------------------------
    kop('TABEL 3 — rollen per familie (aantal build-targets)')
    rollen = defaultdict(Counter)
    for v in varianten:
        for e in v['envs']:
            rollen[v['familie']][rol_van(e)] += 1
    volgorde = ['companion BLE', 'companion WiFi', 'companion USB',
                'companion serial', 'companion Ethernet', 'repeater',
                'room server', 'sensor',
                'KISS modem', 'terminal chat', 'overig']
    print('%-18s %7s %7s %7s %9s' % ('rol', *FAMILIES))
    for rol in volgorde:
        print('%-18s %7d %7d %7d %9d'
              % (rol, *[rollen[f][rol] for f in FAMILIES]))
    print()
    for kenmerk in ('espnow', 'ota'):
        print('%-18s %7d %7d %7d %9d' % (
            kenmerk + ' (varianten)',
            *[sum(1 for v in varianten if v['familie'] == f and v[kenmerk])
              for f in FAMILIES]))
    c6 = [v for v in varianten if v['c6']]
    c6rollen = Counter(rol_van(e) for v in c6 for e in v['envs'])
    print()
    print('waarvan ESP32-C6: %d varianten, %d build-targets (%s)'
          % (len(c6), sum(len(v['envs']) for v in c6),
             ', '.join(v['naam'] for v in c6)))
    print('  rollen:', dict(c6rollen))

    # -- tabel 4 -------------------------------------------------------------
    kop('TABEL 4 — apparaten in de web flasher')
    if not args.flasher_config:
        print('(geen --flasher-config opgegeven)')
        return
    apparaten = lees_flasher(args.flasher_config)
    telling = Counter(a['familie'] for a in apparaten)
    print('totaal apparaten:', len(apparaten))
    for fam, n in telling.most_common():
        print('  %-12s %3d' % (fam, n))
    rolteller = Counter(r for a in apparaten for r in a['rollen'])
    print('rollen over alle apparaten:')
    for rol, n in sorted(rolteller.items()):
        print('  %-14s %3d' % (rol, n))
    for fam in sorted(telling):
        print()
        print('%s (%d):' % (fam, telling[fam]))
        for a in apparaten:
            if a['familie'] == fam:
                print('  - %-45s %-14s %s' % (a['naam'], a['fabrikant'], ' '.join(a['rollen'])))


if __name__ == '__main__':
    main()
