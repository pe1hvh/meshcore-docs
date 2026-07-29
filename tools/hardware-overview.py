# -*- coding: utf-8 -*-
"""Reproduceert de tellingen uit de hoofdstukken in hardware/.

   Bron — een uitgepakte kloon van meshcore-dev/MeshCore op de commit die de
   hoofdstukken pinnen:
     variants/*/platformio.ini   79 varianten met hun build-flags
     variants/*/*.h              variant-headers die dezelfde vlaggen zetten

   Gebruik:
     python3 tools/hardware-overview.py --repo ../MeshCore

   Telmethode, voor elk cijfer gelijk:

   - **Uitgecommentarieerde regels tellen niet mee.** In een `.ini` is dat een
     regel die na inspringen met `;` begint, in een header een regel die met
     `//` begint. Een vlag die alleen uitgecommentarieerd voorkomt telt dus
     nergens mee, ook niet als het bestand verder wel genoemd wordt.
   - **Regels en bestanden zijn verschillende dingen.** Een variantbestand kan
     meerdere `[env:…]`-secties bevatten die elk dezelfde vlag zetten; dat is
     één bestand en meerdere regels. Per cijfer staat hieronder welke van de
     twee het hoofdstuk bedoelt.
   - **Sommige vlaggen staan óók in een header** binnen de variantmap. Waar dat
     zo is telt het script per variantmap en niet per bestand, omdat een map
     één bord is.

   De uitvoer is bedoeld om naast het hoofdstuk te leggen. Wijkt een cijfer af,
   dan is dat een discrepantie voor de opdrachtgever en geen reden om het
   hoofdstuk of het script eigenmachtig bij te stellen.
"""
import argparse
import os
import re
from collections import Counter

COMMIT = '03b6ef4'
VERSIE = 'v1.16.0'
DATUM = '28 juli 2026'


def is_commentaar(regel, pad):
    """Uitgecommentarieerd volgens de conventie van het bestandstype."""
    kaal = regel.lstrip()
    if pad.endswith('.ini'):
        return kaal.startswith(';')
    return kaal.startswith('//')


def variantbestanden(repo, alleen_ini=True):
    """Alle bestanden onder variants/, of alleen de platformio.ini's."""
    wortel = os.path.join(repo, 'variants')
    for map_naam in sorted(os.listdir(wortel)):
        map_pad = os.path.join(wortel, map_naam)
        if not os.path.isdir(map_pad):
            continue
        if alleen_ini:
            ini = os.path.join(map_pad, 'platformio.ini')
            if os.path.exists(ini):
                yield map_naam, ini
        else:
            for hier, _, namen in os.walk(map_pad):
                for naam in sorted(namen):
                    yield map_naam, os.path.join(hier, naam)


def tel(repo, patroon, alleen_ini=True, vang=False):
    """Telt actieve treffers. Geeft (regels, mappen, bestanden, waarden)."""
    rx = re.compile(patroon)
    regels = 0
    mappen = set()
    bestanden = set()
    waarden = Counter()
    for map_naam, pad in variantbestanden(repo, alleen_ini):
        try:
            tekst = open(pad, encoding='utf-8', errors='replace').read()
        except (OSError, UnicodeDecodeError):
            continue
        for regel in tekst.splitlines():
            if is_commentaar(regel, pad):
                continue
            m = rx.search(regel)
            if not m:
                continue
            regels += 1
            mappen.add(map_naam)
            bestanden.add(pad)
            if vang and m.groups():
                waarden[m.group(1).strip()] += 1
    return regels, len(mappen), len(bestanden), waarden


def tel_uitgecommentarieerd(repo, patroon, alleen_ini=True):
    """Telt juist de uitgecommentarieerde treffers, met hun mappen."""
    rx = re.compile(patroon)
    regels = 0
    mappen = set()
    for map_naam, pad in variantbestanden(repo, alleen_ini):
        try:
            tekst = open(pad, encoding='utf-8', errors='replace').read()
        except (OSError, UnicodeDecodeError):
            continue
        for regel in tekst.splitlines():
            if not is_commentaar(regel, pad):
                continue
            if rx.search(regel):
                regels += 1
                mappen.add(map_naam)
    return regels, sorted(mappen)


def kop(tekst):
    print()
    print(tekst)
    print('-' * len(tekst))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True,
                   help='pad naar een uitgepakte MeshCore-kloon')
    args = p.parse_args()
    repo = args.repo

    aantal_mappen = sum(1 for _ in variantbestanden(repo, alleen_ini=False)
                        if False) or len(
        [d for d in os.listdir(os.path.join(repo, 'variants'))
         if os.path.isdir(os.path.join(repo, 'variants', d))])

    print(f'hardware-overview.py — MeshCore {VERSIE}, commit {COMMIT}, {DATUM}')
    print('=' * 72)
    print(f'variantmappen: {aantal_mappen}')

    # ---- 1. RF-schakelaar --------------------------------------------------
    kop('1. SX126X_DIO2_AS_RF_SWITCH — hardware/radio/sx1262.md, antenna.md')
    print('   patroon: SX126X_DIO2_AS_RF_SWITCH, in platformio.ini én headers')
    print('   eenheid: variantmappen')
    r, m, b, _ = tel(repo, r'SX126X_DIO2_AS_RF_SWITCH', alleen_ini=False)
    r_ini, m_ini, _, _ = tel(repo, r'SX126X_DIO2_AS_RF_SWITCH', alleen_ini=True)
    print(f'   variantmappen        {m}')
    print(f'   waarvan in .ini      {m_ini}')
    print(f'   waarvan alleen header{m - m_ini:>4}  (mappen met beide tellen bij .ini)')
    print(f'   regels totaal        {r}')

    for naam, patroon in [
            ('SX126X_CURRENT_LIMIT', r'SX126X_CURRENT_LIMIT'),
            ('SX126X_RX_BOOSTED_GAIN', r'SX126X_RX_BOOSTED_GAIN'),
            ('SX126X_RXEN of TXEN', r'SX126X_(RXEN|TXEN)')]:
        _, m2, _, _ = tel(repo, patroon, alleen_ini=False)
        print(f'   {naam:<24} {m2:>3} mappen')

    # ---- 2. Zendvermogen ---------------------------------------------------
    kop('2. LORA_TX_POWER — hardware/radio/link-budget.md')
    print('   patroon: -D LORA_TX_POWER=<waarde>, alleen platformio.ini')
    print('   eenheid: regels, met de waardeverdeling')
    r, m, b, w = tel(repo, r'-D\s*LORA_TX_POWER\s*=\s*(\d+)', vang=True)
    print(f'   regels               {r}')
    print(f'   variantmappen        {m}')
    for waarde, n in sorted(w.items(), key=lambda x: -int(x[0])):
        print(f'   {waarde:>3} dBm            {n:>4} regels')

    # ---- 3 en 4. WiFi ------------------------------------------------------
    kop('3. WIFI_SSID actief — hardware/interfaces/wifi.md')
    print('   patroon: -D WIFI_SSID=, alleen platformio.ini')
    print('   eenheid: regels én bestanden')
    r, m, b, _ = tel(repo, r'-D\s*WIFI_SSID\s*=')
    print(f'   regels               {r}')
    print(f'   bestanden            {b}')

    kop('4. WIFI_SSID uitgecommentarieerd — hardware/interfaces/wifi.md')
    print('   patroon: hetzelfde, maar juist de regels die met ; beginnen')
    r, mappen = tel_uitgecommentarieerd(repo, r'-D\s*WIFI_SSID\s*=')
    print(f'   regels               {r}')
    print(f'   variantmappen        {", ".join(mappen)}')

    # ---- 5 en 6. Scherm ----------------------------------------------------
    kop('5. DISPLAY_CLASS — hardware/peripherals/display.md')
    print('   patroon: -D DISPLAY_CLASS=<klasse>, alleen platformio.ini')
    print('   eenheid: regels, bestanden en het aantal verschillende waarden')
    r, m, b, w = tel(repo, r'-D\s*DISPLAY_CLASS\s*=\s*(\S+)', vang=True)
    print(f'   regels               {r}')
    print(f'   bestanden            {b}')
    print(f'   verschillende waarden{len(w):>4}')
    for klasse, n in w.most_common():
        print(f'     {klasse:<22} {n:>3}')

    kop('6. NullDisplayDriver — hardware/peripherals/display.md')
    print('   patroon: -D DISPLAY_CLASS=NullDisplayDriver')
    print('   eenheid: regels')
    print(f'   regels               {w.get("NullDisplayDriver", 0)}')

    # ---- 7, 8 en 9. Knoppen, LEDs, zoemer ----------------------------------
    kop('7. PIN_USER_BTN — hardware/peripherals/buttons-and-leds.md')
    print('   patroon: -D PIN_USER_BTN=, alleen platformio.ini')
    print('   eenheid: het hoofdstuk noemt beide; regels en bestanden verschillen')
    r, m, b, _ = tel(repo, r'-D\s*PIN_USER_BTN\s*=')
    print(f'   regels               {r}')
    print(f'   bestanden            {b}')

    kop('8. LED-vlaggen — hardware/peripherals/buttons-and-leds.md')
    print('   patroon: -D <vlag>=, alleen platformio.ini')
    print('   eenheid: regels')
    for vlag in ('P_LORA_TX_LED', 'PIN_STATUS_LED', 'PIN_LED'):
        r, m, b, _ = tel(repo, rf'-D\s*{vlag}\s*=')
        print(f'   {vlag:<16} {r:>4} regels   {b:>3} bestanden')

    kop('9. PIN_BUZZER — hardware/peripherals/buttons-and-leds.md')
    print('   patroon: -D PIN_BUZZER=, alleen platformio.ini')
    print('   eenheid: regels én bestanden')
    r, m, b, _ = tel(repo, r'-D\s*PIN_BUZZER\s*=')
    print(f'   regels               {r}')
    print(f'   bestanden            {b}')

    kop('10. PIN_GPS_RX — hardware/peripherals/gps.md')
    print('   patroon: -D PIN_GPS_RX=, alleen platformio.ini')
    print('   eenheid: bestanden')
    r, m, b, _ = tel(repo, r'-D\s*PIN_GPS_RX\s*=')
    print(f'   regels               {r}')
    print(f'   bestanden            {b}')

    print()
    print('Klaar. Wijkt een cijfer af van het hoofdstuk, meld dat en wijzig niets.')


if __name__ == '__main__':
    main()
