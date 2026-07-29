# -*- coding: utf-8 -*-
"""Reproduceert de tellingen uit de hoofdstukken in techniek/roomserver/.

   Bron — een uitgepakte kloon van meshcore-dev/MeshCore op de commit die de
   hoofdstukken pinnen:
     variants/*/platformio.ini        79 varianten met hun build-targets
     examples/simple_room_server/     de room-server-firmware zelf
     src/helpers/ClientACL.h          permissiemodel en MAX_CLIENTS

   Gebruik:
     python3 tools/room-server-overview.py --repo ../MeshCore

   Telmethode:

   - **Een room-server-build-target is een `[env:…]`-sectie waarvan de body
     `../examples/simple_room_server` in `build_src_filter` opneemt.** Niet de
     naam van de sectie: die eindigt meestal maar niet altijd op
     `_room_server`, en een naam is geen bewijs van wat er gecompileerd wordt.
     De body loopt tot de volgende `[`-sectie in hetzelfde bestand.
   - **Uitgecommentarieerde regels tellen niet mee.** In een `.ini` is dat een
     regel die na inspringen met `;` begint. Voor `ROOM_PASSWORD` telt het
     script beide apart, omdat één variant de vlag alleen uitgecommentarieerd
     heeft en dat verschil in het hoofdstuk staat.
   - **Targets en variantmappen zijn verschillende dingen.** Eén variantmap kan
     meerdere room-server-targets bevatten (bijvoorbeeld een tweede voor een
     ander scherm). Per cijfer staat hieronder welke van de twee het
     hoofdstuk bedoelt.
   - **Constanten worden uit de bron gelezen, niet overgetypt.** De `#define`s
     komen uit `MyMesh.h` en `MyMesh.cpp`; wijzigt de firmware ze, dan wijzigt
     de uitvoer mee en klopt het hoofdstuk niet langer.

   De uitvoer is bedoeld om naast het hoofdstuk te leggen. Wijkt een cijfer af,
   dan is dat een discrepantie voor de opdrachtgever en geen reden om het
   hoofdstuk of het script eigenmachtig bij te stellen.
"""
import argparse
import os
import re

COMMIT = '03b6ef4'
VERSIE = 'v1.16.0'
DATUM = '28 juli 2026'

VOORBEELD = os.path.join('examples', 'simple_room_server')
MARKERING = '../examples/simple_room_server'


def variantmappen(repo):
    """Alle mappen onder variants/, gesorteerd."""
    wortel = os.path.join(repo, 'variants')
    return sorted(d for d in os.listdir(wortel)
                  if os.path.isdir(os.path.join(wortel, d)))


def secties(pad):
    """Levert (sectienaam, regels) per `[…]`-sectie in een ini-bestand."""
    naam = None
    body = []
    for regel in open(pad, encoding='utf-8', errors='replace').read().splitlines():
        m = re.match(r'^\[([^\]]+)\]', regel)
        if m:
            if naam is not None:
                yield naam, body
            naam = m.group(1)
            body = []
        elif naam is not None:
            body.append(regel)
    if naam is not None:
        yield naam, body


def actief(regel):
    """Niet uitgecommentarieerd volgens de ini-conventie."""
    return not regel.lstrip().startswith(';')


def ouders(body):
    """Secties waar deze sectie van erft: `extends =` en `${sectie.sleutel}`."""
    namen = set()
    in_extends = False
    for regel in body:
        if not actief(regel):
            continue
        m = re.match(r'\s*extends\s*=\s*(.*)$', regel)
        if m:
            in_extends = True
            rest = m.group(1)
        elif in_extends and regel[:1] in (' ', '\t') and regel.strip():
            rest = regel
        else:
            if regel.strip() and not regel[:1] in (' ', '\t'):
                in_extends = False
            rest = ''
        for deel in rest.replace(',', ' ').split():
            if deel and not deel.startswith('$'):
                namen.add(deel)
    for regel in body:
        if actief(regel):
            for m in re.finditer(r'\$\{([^.}]+)\.[^}]+\}', regel):
                namen.add(m.group(1))
    return namen


def room_server_targets(repo):
    """(map, sectienaam) voor elk build-target dat de room server compileert.

       Een sectie telt mee als de markering in haar eigen body staat óf in een
       sectie waarvan zij erft. Zonder die overerving mist de telling de zes
       ikoka-targets, die hun `build_src_filter` uit een gedeelde basissectie
       halen; die basissectie is zelf geen `[env:…]` en is dus geen target.
    """
    for map_naam in variantmappen(repo):
        ini = os.path.join(repo, 'variants', map_naam, 'platformio.ini')
        if not os.path.exists(ini):
            continue
        alle = dict(secties(ini))

        def heeft(naam, gezien):
            if naam in gezien or naam not in alle:
                return False
            gezien.add(naam)
            body = alle[naam]
            if any(MARKERING in r for r in body if actief(r)):
                return True
            return any(heeft(o, gezien) for o in ouders(body))

        for naam in alle:
            if naam.startswith('env:') and heeft(naam, set()):
                yield map_naam, naam[4:]


def defines(pad, namen):
    """Leest `#define NAAM waarde` uit een bronbestand, met regelnummer."""
    gevonden = {}
    for nr, regel in enumerate(
            open(pad, encoding='utf-8', errors='replace').read().splitlines(), 1):
        m = re.match(r'\s*#define\s+(\w+)\s+(.+?)\s*(?://.*)?$', regel)
        if m and m.group(1) in namen:
            gevonden.setdefault(m.group(1), (m.group(2).strip(), nr))
    return gevonden


def kop(tekst):
    print()
    print(tekst)
    print('-' * len(tekst))


def hx(b, sep=' '):
    return sep.join(f'{x:02X}' for x in b)


def voorbeeld_push():
    """De payload die de server naar een client duwt, plus de verwachte ACK.

       De klaartekst is:  post_timestamp(4, LSB eerst) ‖ flags(1) ‖
       auteur-pubkey-prefix(4) ‖ tekst.  De verwachte ACK is
       sha256(klaartekst ‖ pubkey-van-de-client) afgekapt op 4 bytes, gelezen
       als uint32 met LSB eerst — precies wat `memcpy` op een little-endian
       platform doet.

       De voorbeeldidentiteiten zijn dezelfde afspraak als in dm-example.py:
       een publieke sleutel is `sha256("voorbeeld public key <call>")`. Een
       echte sleutel komt van het apparaat en is niet uit publieke gegevens te
       reproduceren; alles daarna is wel exact het firmwarepad.
    """
    import hashlib
    import struct

    TS = 1785412800
    AUTEUR = 'PE1RDP'
    CLIENT = 'PE1HVH'
    TEKST = 'Op Woensdag a.s. Blauwvingerdagen'

    pub_auteur = hashlib.sha256(f'voorbeeld public key {AUTEUR}'.encode()).digest()
    pub_client = hashlib.sha256(f'voorbeeld public key {CLIENT}'.encode()).digest()

    TXT_TYPE_SIGNED_PLAIN, POGING = 2, 0
    flags = (TXT_TYPE_SIGNED_PLAIN << 2) | (POGING & 3)

    klaartekst = (struct.pack('<I', TS) + bytes([flags])
                  + pub_auteur[:4] + TEKST.encode())
    ruwe_ack = hashlib.sha256(klaartekst + pub_client).digest()[:4]
    ack = struct.unpack('<I', ruwe_ack)[0]

    print(f'   post_timestamp       {TS}  ->  {hx(struct.pack("<I", TS))}')
    print(f'   flags                (2 << 2) | 0 = 0x{flags:02X}')
    print(f'   auteur {AUTEUR:<14}pubkey {hx(pub_auteur[:8])} …')
    print(f'   prefix in de payload {hx(pub_auteur[:4])}')
    print(f'   tekst                "{TEKST}"  ({len(TEKST)} tekens)')
    print(f'   payloadlengte        {len(klaartekst)} bytes  (4 + 1 + 4 + {len(TEKST)})')
    print(f'   klaartekst           {hx(klaartekst[:9])}')
    print(f'                        {hx(klaartekst[9:])}')
    print(f'   client {CLIENT:<14}pubkey {hx(pub_client[:8])} …')
    print(f'   verwachte ACK        {hx(ruwe_ack)}  ->  0x{ack:08X}  ({ack})')
    print(f'   ruimte over          {151 - len(TEKST)} van 151 tekens')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True,
                   help='pad naar een uitgepakte MeshCore-kloon')
    args = p.parse_args()
    repo = args.repo

    print(f'room-server-overview.py — MeshCore {VERSIE}, commit {COMMIT}, {DATUM}')
    print('=' * 72)
    print(f'variantmappen: {len(variantmappen(repo))}')

    # ---- 1. Build-targets --------------------------------------------------
    kop('1. Room-server-build-targets — roomserver/introduction.md')
    print(f'   patroon: [env:…] met {MARKERING} in de body,')
    print('            of in een sectie waarvan het target erft')
    print('   eenheid: het hoofdstuk noemt targets én variantmappen')
    targets = list(room_server_targets(repo))
    mappen = {m for m, _ in targets}
    print(f'   build-targets        {len(targets)}')
    print(f'   variantmappen        {len(mappen)}')
    print(f'   mappen zonder        {len(variantmappen(repo)) - len(mappen)}')
    meervoud = sorted({m for m in mappen
                       if sum(1 for a, _ in targets if a == m) > 1})
    print(f'   mappen met meer dan een target: {len(meervoud)}')
    for m in meervoud:
        namen = [n for a, n in targets if a == m]
        print(f'     {m}: {", ".join(namen)}')

    # ---- 2. ROOM_PASSWORD --------------------------------------------------
    kop('2. ROOM_PASSWORD — roomserver/login-and-acl.md')
    print('   patroon: -D ROOM_PASSWORD=, alleen platformio.ini')
    print('   eenheid: regels, actief en uitgecommentarieerd apart')
    rx = re.compile(r'-D\s*ROOM_PASSWORD\s*=\s*\'?"([^"]*)"')
    aan, uit, waarden = 0, 0, {}
    uit_mappen = []
    for map_naam in variantmappen(repo):
        ini = os.path.join(repo, 'variants', map_naam, 'platformio.ini')
        if not os.path.exists(ini):
            continue
        for regel in open(ini, encoding='utf-8', errors='replace').read().splitlines():
            m = rx.search(regel)
            if not m:
                continue
            if actief(regel):
                aan += 1
                waarden[m.group(1)] = waarden.get(m.group(1), 0) + 1
            else:
                uit += 1
                uit_mappen.append(map_naam)
    print(f'   actieve regels       {aan}')
    print(f'   uitgecommentarieerd  {uit}   {", ".join(sorted(set(uit_mappen)))}')
    for waarde, n in sorted(waarden.items()):
        print(f'   waarde "{waarde}"{"":<10} {n} regels')

    # ---- 3. Constanten uit de firmware -------------------------------------
    kop('3. Constanten — roomserver/posts-and-sync.md, limits-and-todos.md')
    print('   patroon: #define in de bron, waarde en regelnummer overgenomen')
    kop_h = os.path.join(repo, VOORBEELD, 'MyMesh.h')
    kop_c = os.path.join(repo, VOORBEELD, 'MyMesh.cpp')
    acl_h = os.path.join(repo, 'src', 'helpers', 'ClientACL.h')

    uit_h = defines(kop_h, {'MAX_UNSYNCED_POSTS', 'MAX_POST_TEXT_LEN',
                            'SERVER_RESPONSE_DELAY', 'TXT_ACK_DELAY',
                            'FIRMWARE_ROLE', 'ADMIN_PASSWORD'})
    uit_c = defines(kop_c, {'PUSH_NOTIFY_DELAY_MILLIS', 'SYNC_PUSH_INTERVAL',
                            'PUSH_ACK_TIMEOUT_FLOOD', 'PUSH_TIMEOUT_BASE',
                            'PUSH_ACK_TIMEOUT_FACTOR', 'POST_SYNC_DELAY_SECS',
                            'REPLY_DELAY_MILLIS', 'LAZY_CONTACTS_WRITE_DELAY',
                            'FIRMWARE_VER_LEVEL'})
    uit_a = defines(acl_h, {'MAX_CLIENTS', 'PERM_ACL_GUEST',
                            'PERM_ACL_READ_ONLY', 'PERM_ACL_READ_WRITE',
                            'PERM_ACL_ADMIN', 'PERM_ACL_ROLE_MASK'})

    for label, bron, uit in (('MyMesh.h', 'examples/simple_room_server/MyMesh.h', uit_h),
                             ('MyMesh.cpp', 'examples/simple_room_server/MyMesh.cpp', uit_c),
                             ('ClientACL.h', 'src/helpers/ClientACL.h', uit_a)):
        print(f'   {bron}')
        for naam in sorted(uit):
            waarde, nr = uit[naam]
            print(f'     {naam:<26} {waarde:<16} r.{nr}')

    if 'MAX_POST_TEXT_LEN' in uit_h:
        rauw = uit_h['MAX_POST_TEXT_LEN'][0]
        try:
            print(f'   MAX_POST_TEXT_LEN uitgerekend: {rauw} = '
                  f'{eval(rauw, {"__builtins__": {}}, {})} tekens')
        except Exception:
            print(f'   MAX_POST_TEXT_LEN niet uit te rekenen uit "{rauw}"')

    # ---- 4. Overrides in de varianten --------------------------------------
    kop('4. Overrides — roomserver/limits-and-todos.md')
    print('   patroon: -D MAX_UNSYNCED_POSTS= of -D MAX_CLIENTS= in de varianten')
    print('   eenheid: regels; het hoofdstuk stelt dat er geen zijn')
    for vlag in ('MAX_UNSYNCED_POSTS', 'MAX_CLIENTS'):
        n = 0
        for map_naam in variantmappen(repo):
            ini = os.path.join(repo, 'variants', map_naam, 'platformio.ini')
            if not os.path.exists(ini):
                continue
            for regel in open(ini, encoding='utf-8', errors='replace').read().splitlines():
                if actief(regel) and re.search(rf'-D\s*{vlag}\s*=', regel):
                    n += 1
        print(f'   {vlag:<20} {n} regels')

    # ---- 5. Omvang van de firmware -----------------------------------------
    kop('5. Omvang — roomserver/introduction.md')
    print(f'   patroon: regels per bestand in {VOORBEELD}/')
    wortel = os.path.join(repo, VOORBEELD)
    totaal = 0
    for naam in sorted(os.listdir(wortel)):
        pad = os.path.join(wortel, naam)
        if not os.path.isfile(pad):
            continue
        n = len(open(pad, encoding='utf-8', errors='replace').read().splitlines())
        totaal += n
        print(f'   {naam:<16} {n:>5} regels')
    print(f'   {"totaal":<16} {totaal:>5} regels')

    # ---- 6. Uitgewerkt voorbeeld -------------------------------------------
    kop('6. Post-push en ACK — roomserver/posts-and-sync.md')
    print('   gevolgd: MyMesh::pushPostToClient() r.53-90, Utils::sha256() r.23-28')
    print('   voorbeeldidentiteiten volgens dezelfde seed als tools/dm-example.py')
    voorbeeld_push()

    print()
    print('Klaar. Wijkt een cijfer af van het hoofdstuk, meld dat en wijzig niets.')


if __name__ == '__main__':
    main()
