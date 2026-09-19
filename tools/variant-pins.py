# -*- coding: utf-8 -*-
"""Reproduceert de pintabellen per variant uit de MeshCore-firmware.

   Bron — een uitgepakte kloon van meshcore-dev/MeshCore:
     variants/<naam>/*.h              #define-regels met signaalnaam en pin
     variants/<naam>/platformio.ini   -D-vlaggen in build_flags

   De nRF52-varianten zetten hun pinnen in variant.h of pins_arduino.h, de
   ESP32-varianten in de build_flags van platformio.ini. Het script leest
   beide en geeft per signaal de waarde met bestand en regelnummer, zodat
   elke regel in het hoofdstuk naar een bronregel te herleiden is.

   Uitgecommentarieerde regels tellen niet mee: een #define achter // of in
   een /* */-blok wordt overgeslagen, net als een -D-vlag achter een ;.
   #define-regels binnen #if 0 blijven wel staan; die kan het script niet
   onderscheiden en dat staat zo ook in het hoofdstuk.

   Gebruik:
     python3 tools/variant-pins.py --repo ../MeshCore heltec_tower_v2
     python3 tools/variant-pins.py --repo ../MeshCore --alle --markdown
     python3 tools/variant-pins.py --repo ../MeshCore --familie nRF52 --markdown

   Zonder --markdown is de uitvoer platte tekst voor controle; met
   --markdown een tabel die rechtstreeks in een hoofdstuk kan.
"""
import argparse, glob, os, re

# Signaalgroepen, in de volgorde waarin ze in het hoofdstuk staan.
GROEPEN = [
    ('LoRa-radio',      re.compile(r'^(P_LORA_|LORA_|SX126X_|SX128X_|LR11X0_|LR2021_|RADIO_)')),
    ('I2C',             re.compile(r'^(PIN_WIRE_|PIN_BOARD_SDA|PIN_BOARD_SCL|I2C_)')),
    ('SPI',             re.compile(r'^(PIN_SPI|SPI_)')),
    ('Display',         re.compile(r'^(DISP|PIN_DISP|TFT_|OLED_|EINK_|PIN_TFT)')),
    ('GPS',             re.compile(r'^(GPS_|PIN_GPS)')),
    ('Knoppen en LED',  re.compile(r'^(PIN_BUTTON|BUTTON_|PIN_USER_BTN|PIN_LED|LED_|PIN_STATUS_LED)')),
    ('Voeding en accu', re.compile(r'^(PIN_VBAT|PIN_VEXT|BATTERY_|PIN_BAT|VEXT_)')),
]
REST = 'Overig'

# Het hoofdstuk bestaat in twee talen; de tabel komt uit hetzelfde script.
VERTALING = {
    'LoRa-radio': 'LoRa radio', 'I2C': 'I2C', 'SPI': 'SPI', 'Display': 'Display',
    'GPS': 'GPS', 'Knoppen en LED': 'Buttons and LED',
    'Voeding en accu': 'Power and battery', 'Overig': 'Other',
}
KOLOMMEN = {'nl': ('Signaal', 'Waarde', 'Bron'), 'en': ('Signal', 'Value', 'Source')}
REGEL = {'nl': 'r.', 'en': 'l.'}

# Namen die op een pin lijken maar er geen zijn: radio-instellingen die in
# dezelfde build_flags staan. Ze worden apart gemeld, niet in de pintabel.
GEEN_PIN = {
    'LORA_TX_POWER', 'SX126X_CURRENT_LIMIT', 'SX126X_DIO3_TCXO_VOLTAGE',
    'SX126X_DIO2_AS_RF_SWITCH', 'SX126X_RX_BOOSTED_GAIN',
    'SX126X_REGULATOR_MODE_DCDC', 'LORA_FREQ', 'LORA_BW', 'LORA_SF', 'LORA_CR',
    'SX128X_CURRENT_LIMIT', 'LR11X0_DIO3_TCXO_VOLTAGE', 'BLE_PIN_CODE',
}

# Welke [*_base] hoort bij welke platformfamilie; gelijk aan de tabel in
# tools/platform-overview.py.
BASE_TO_FAMILY = {
    'esp32_base': 'ESP32', 'esp32c6_base': 'ESP32', 'nrf52_base': 'nRF52',
    'rp2040_base': 'RP2040', 'stm32_base': 'STM32WL',
}
EXTENDS_RE = re.compile(r'^\s*extends\s*=\s*([A-Za-z0-9_]+)\s*$', re.M)

DEFINE_RE = re.compile(r'^\s*#define\s+([A-Za-z_][A-Za-z0-9_]*)\s+(.+?)\s*$')
FLAG_RE = re.compile(r'^\s*-D\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$')
PIN_ACHTIG = re.compile(r'(^|_)(PIN|GPIO)S?(_|$)|^P_LORA_|^SX126X_|^LORA_|^PIN_')


def strip_blokcommentaar(regels):
    """Vervangt /* ... */ door lege ruimte, regelnummers blijven kloppen."""
    uit, in_blok = [], False
    for regel in regels:
        resultaat = ''
        i = 0
        while i < len(regel):
            if in_blok:
                eind = regel.find('*/', i)
                if eind == -1:
                    break
                in_blok = False
                i = eind + 2
                continue
            start = regel.find('/*', i)
            if start == -1:
                resultaat += regel[i:]
                break
            resultaat += regel[i:start]
            in_blok = True
            i = start + 2
        uit.append(resultaat)
    return uit


def lees_headers(variantdir):
    """-> [(signaal, waarde, bestand, regelnummer)] uit de *.h-bestanden."""
    gevonden = []
    for pad in sorted(glob.glob(os.path.join(variantdir, '*.h'))):
        with open(pad, encoding='utf-8', errors='replace') as fh:
            regels = fh.read().split('\n')
        for nr, regel in enumerate(strip_blokcommentaar(regels), start=1):
            regel = regel.split('//', 1)[0]
            m = DEFINE_RE.match(regel)
            if not m:
                continue
            naam, waarde = m.group(1), m.group(2).strip()
            if not PIN_ACHTIG.search(naam):
                continue
            gevonden.append((naam, waarde, os.path.basename(pad), nr))
    return gevonden


def lees_buildflags(variantdir):
    """-> [(signaal, waarde, 'platformio.ini', regelnummer)] uit build_flags."""
    pad = os.path.join(variantdir, 'platformio.ini')
    if not os.path.exists(pad):
        return []
    gevonden = []
    with open(pad, encoding='utf-8', errors='replace') as fh:
        for nr, regel in enumerate(fh.read().split('\n'), start=1):
            if regel.lstrip().startswith(';'):
                continue
            m = FLAG_RE.match(regel.split(';', 1)[0])
            if not m:
                continue
            naam, waarde = m.group(1), m.group(2).strip()
            if not PIN_ACHTIG.search(naam):
                continue
            gevonden.append((naam, waarde, 'platformio.ini', nr))
    return gevonden


def familie_van(repo, variant):
    """-> 'ESP32' | 'nRF52' | 'RP2040' | 'STM32WL' | None, uit extends = *_base."""
    pad = os.path.join(repo, 'variants', variant, 'platformio.ini')
    if not os.path.exists(pad):
        return None
    with open(pad, encoding='utf-8', errors='replace') as fh:
        for basis in EXTENDS_RE.findall(fh.read()):
            if basis in BASE_TO_FAMILY:
                return BASE_TO_FAMILY[basis]
    return None


def groep_van(naam):
    for titel, patroon in GROEPEN:
        if patroon.match(naam):
            return titel
    return REST


def verzamel(repo, variant):
    variantdir = os.path.join(repo, 'variants', variant)
    if not os.path.isdir(variantdir):
        raise SystemExit('variant bestaat niet: %s' % variantdir)
    rijen = lees_headers(variantdir) + lees_buildflags(variantdir)
    instellingen = [r for r in rijen if r[0] in GEEN_PIN]
    # Eerste vindplaats wint; een herdefinitie verderop is een alias.
    gezien, uniek = set(), []
    for naam, waarde, bestand, nr in rijen:
        if naam in gezien:
            continue
        gezien.add(naam)
        uniek.append((naam, waarde, bestand, nr))
    uniek = [r for r in uniek if r[0] not in GEEN_PIN]
    volgorde = {titel: i for i, (titel, _) in enumerate(GROEPEN)}
    volgorde[REST] = len(GROEPEN)
    uniek.sort(key=lambda r: (volgorde[groep_van(r[0])], r[0]))
    return uniek, instellingen


def druk_plat(variant, rijen):
    print()
    print(variant)
    print('=' * len(variant))
    huidige = None
    for naam, waarde, bestand, nr in rijen:
        groep = groep_van(naam)
        if groep != huidige:
            huidige = groep
            print('-- %s' % groep)
        print('   %-28s %-22s %s r.%d' % (naam, waarde, bestand, nr))
    print('   totaal: %d signalen' % len(rijen))


def druk_markdown(variant, rijen, niveau=4, taal='nl'):
    print()
    print('%s `%s`' % ('#' * niveau, variant))
    print()
    huidige = None
    for naam, waarde, bestand, nr in rijen:
        groep = groep_van(naam)
        if groep != huidige:
            if huidige is not None:
                print()
            huidige = groep
            print('**%s**' % (groep if taal == 'nl' else VERTALING[groep]))
            print()
            print('| %s | %s | %s |' % KOLOMMEN[taal])
            print('|---|---|---|')
        print('| `%s` | `%s` | `%s` %s%d |' % (naam, waarde, bestand, REGEL[taal], nr))
    print()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True, help='pad naar een kloon van meshcore-dev/MeshCore')
    p.add_argument('--alle', action='store_true', help='alle varianten in variants/')
    p.add_argument('--familie', help='alleen varianten van deze familie (ESP32, nRF52, RP2040, STM32WL)')
    p.add_argument('--markdown', action='store_true', help='uitvoer als Markdown-tabel')
    p.add_argument('--taal', choices=('nl', 'en'), default='nl',
                   help='taal van de kolomkoppen en signaalgroepen in Markdown')
    p.add_argument('--kopniveau', type=int, default=4,
                   help='kopniveau van de variantkop in Markdown (standaard 4)')
    p.add_argument('varianten', nargs='*', help='namen van varianten')
    args = p.parse_args()

    namen = args.varianten
    if args.familie:
        args.alle = True
    if args.alle:
        namen = sorted(os.path.basename(d) for d in
                       glob.glob(os.path.join(args.repo, 'variants', '*'))
                       if os.path.isdir(d))
    if args.familie:
        doel = args.familie.lower()
        namen = [n for n in namen if (familie_van(args.repo, n) or '').lower() == doel]
        if not namen:
            raise SystemExit('geen varianten in familie %s' % args.familie)
    if not namen:
        raise SystemExit('geef variantnamen op of gebruik --alle of --familie')

    for variant in namen:
        rijen, instellingen = verzamel(args.repo, variant)
        if args.markdown:
            druk_markdown(variant, rijen, args.kopniveau, args.taal)
        else:
            druk_plat(variant, rijen)
        if instellingen and not args.markdown:
            print('   radio-instellingen (geen pin): %s'
                  % ', '.join(sorted({naam for naam, _, _, _ in instellingen})))


if __name__ == '__main__':
    main()
