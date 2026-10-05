#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproduceert het bytevoorbeeld in hardware/interfaces/usb-serial.md.

   Het voorbeeld is een schrijfopdracht over USB: de app zet de nodenaam op
   `PE1HVH` (de afzender uit de projectbrede voorbeelddata) met
   `CMD_SET_ADVERT_NAME`, en de node antwoordt met `RESP_CODE_OK`.

   Bron — een uitgepakte kloon van meshcore-dev/MeshCore op de commit die het
   hoofdstuk pint:
     examples/companion_radio/MyMesh.cpp      CMD_SET_ADVERT_NAME, RESP_CODE_OK
     src/helpers/BaseSerialInterface.h        MAX_FRAME_SIZE
     src/helpers/ArduinoSerialInterface.cpp   de header: '>' of '<', lengte LSB, MSB

   Gebruik:
     python3 tools/usb-serial-example.py --repo ../MeshCore

   Zonder --repo rekent het script met de waarden die op de gepinde commit
   gelden en zegt het dat het niets heeft nagekeken. Met --repo leest het de
   drie constanten uit de checkout; wijkt een waarde af van de gepinde, dan
   meldt het dat als discrepantie in plaats van stil verder te rekenen.

   Telmethode: niet van toepassing, er wordt niets geteld. Het frame wordt
   opgebouwd zoals ArduinoSerialInterface::writeFrame() het doet: één startbyte,
   de lengte van de payload in twee bytes met de minst belangrijke eerst, dan
   de payload zelf.
"""
import argparse
import os
import re
import sys

COMMIT = 'd929643'
VERSIE = 'v1.17.1'
DATUM = '14 augustus 2026'

GEPIND = {
    'CMD_SET_ADVERT_NAME': 8,
    'RESP_CODE_OK': 0,
    'MAX_FRAME_SIZE': 176,
}

NAAM = 'PE1HVH'


def lees_define(pad, naam):
    """Waarde van '#define NAAM <getal>' in pad, of None."""
    patroon = re.compile(r'^\s*#define\s+' + naam + r'\s+(\d+)\b')
    with open(pad, encoding='utf-8', errors='replace') as fh:
        for regel in fh:
            m = patroon.match(regel)
            if m:
                return int(m.group(1))
    return None


def constanten(repo):
    if repo is None:
        return dict(GEPIND), False
    bronnen = {
        'CMD_SET_ADVERT_NAME': 'examples/companion_radio/MyMesh.cpp',
        'RESP_CODE_OK': 'examples/companion_radio/MyMesh.cpp',
        'MAX_FRAME_SIZE': 'src/helpers/BaseSerialInterface.h',
    }
    waarden = {}
    for naam, rel in bronnen.items():
        pad = os.path.join(repo, rel)
        if not os.path.isfile(pad):
            sys.exit(f'bestand ontbreekt in de checkout: {rel}')
        waarde = lees_define(pad, naam)
        if waarde is None:
            sys.exit(f'{naam} niet gevonden in {rel}')
        waarden[naam] = waarde
    return waarden, True


def frame(startbyte, payload, max_frame):
    if len(payload) > max_frame:
        sys.exit(f'payload van {len(payload)} bytes is groter dan MAX_FRAME_SIZE {max_frame}')
    return bytes([ord(startbyte), len(payload) & 0xFF, len(payload) >> 8]) + payload


def hexstr(b):
    return ' '.join(f'{x:02X}' for x in b)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', help='uitgepakte kloon van meshcore-dev/MeshCore')
    args = p.parse_args()

    waarden, nagekeken = constanten(args.repo)

    print(f'MeshCore {VERSIE}, commit {COMMIT}, {DATUM}')
    if nagekeken:
        print(f'constanten gelezen uit: {args.repo}')
        for naam, gepind in GEPIND.items():
            if waarden[naam] != gepind:
                print(f'  DISCREPANTIE: {naam} is {waarden[naam]}, gepind {gepind}')
    else:
        print('geen --repo opgegeven: gerekend met de gepinde waarden, niets nagekeken')
    print()

    for naam in GEPIND:
        print(f'  {naam:20} {waarden[naam]}')
    print()

    heen = frame('<', bytes([waarden['CMD_SET_ADVERT_NAME']]) + NAAM.encode('ascii'),
                 waarden['MAX_FRAME_SIZE'])
    terug = frame('>', bytes([waarden['RESP_CODE_OK']]), waarden['MAX_FRAME_SIZE'])

    print('app -> node   ' + hexstr(heen))
    print(f'              \'<\', lengte {heen[1] | heen[2] << 8}, '
          f'CMD_SET_ADVERT_NAME ({waarden["CMD_SET_ADVERT_NAME"]}), {NAAM!r}')
    print('node -> app   ' + hexstr(terug))
    print(f'              \'>\', lengte {terug[1] | terug[2] << 8}, '
          f'RESP_CODE_OK ({waarden["RESP_CODE_OK"]})')


if __name__ == '__main__':
    main()
