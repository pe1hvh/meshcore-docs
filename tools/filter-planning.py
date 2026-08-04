#!/usr/bin/env python3
"""Rekent elk cijfer uit hardware/radio/filters.md opnieuw uit.

Het hoofdstuk gaat over ontvangerverstoring naast een sterke zendmast en
over de filters die daartegen helpen. Vrijwel geen enkel getal in dat
hoofdstuk komt uit de MeshCore-firmware; het is radiotechniek en het
gedrag van een specifieke zendmast. Dit script maakt de scheiding hard:

  * firmwarewaarden staan onder FIRMWARE en zijn gepind op commit 03b6ef4
  * mastgegevens staan onder ANTENNEREGISTER en komen uit het openbare
    Antenneregister voor postcode 8043LX te Zwolle
  * alles wat een aanname is staat onder AANNAMES, met de gevoeligheid
    van de uitkomst voor die aanname expliciet in de uitvoer

Gebruik:
    python3 tools/filter-planning.py
"""

import math

# --------------------------------------------------------------------------
# FIRMWARE -- MeshCore v1.16.0, commit 03b6ef4, 28 juli 2026
# --------------------------------------------------------------------------
COMMIT = "03b6ef4"
VERSION = "v1.16.0"
DATE = "28 juli 2026"

LORA_FREQ_MHZ = 869.618        # -D LORA_FREQ=869.618 in platformio.ini
LORA_BW_KHZ = 62.5             # -D LORA_BW=62.5
TX_POWER_MAX_DBM = 22          # -D LORA_TX_POWER=22
NOISE_FLOOR_CLAMP_DBM = -120   # RadioLibWrappers.cpp, ondergrens

# --------------------------------------------------------------------------
# ANTENNEREGISTER -- opstelpunt Zwolle 8043LX, antennes op 30,4 m
# Middenfrequentie in MHz, vermogen in dBW zoals geregistreerd.
# --------------------------------------------------------------------------
MAST = [
    ("5G n28", 773.0, 34.0),
    ("4G B20", 816.0, 34.5),
    ("2G/4G 900", 940.0, 34.9),
    ("L-band SDL", 1474.5, 36.4),
    ("4G B3", 1815.0, 39.2),
    ("5G n1", 2160.0, 40.5),
    ("4G/5G 2600", 2660.0, 35.9),
    ("5G n78", 3700.0, 48.2),
]
GSM_BLOCK = (935.2, 945.0)     # het enige blok dat het register als bereik geeft

# --------------------------------------------------------------------------
# AANNAMES -- geen van deze waarden staat in een bron
# --------------------------------------------------------------------------
SLANT_M = 40.0                 # schuine afstand node tot paneel
PATTERN_SUPPRESSION_DB = 25.0  # onderdrukking onder de hoofdbundel
RX_ANT_GAIN_DBI = 0.0          # winst van een 868-antenne buiten zijn band
INSERTION_LOSS_DB = 2.0        # invoegverlies van het filter
TX_LIMIT_DBM = 20              # vermogensgrens van het filter

# Blokbreedte rond de geregistreerde middenfrequentie. Het register geeft
# voor 4G en 5G alleen een middenfrequentie, niet de kanaalbreedte.
NARROW_HALFWIDTH_MHZ = 10.0
BAND_EDGES_WIDE = {            # nominale banddowlinks, ruimste aanname
    940.0: (925.0, 960.0),
    1815.0: (1805.0, 1880.0),
    2660.0: (2620.0, 2690.0),
}


def fspl_db(f_mhz, d_m):
    return 32.45 + 20 * math.log10(f_mhz) + 20 * math.log10(d_m / 1000.0)


def rule(title):
    print()
    print(title)
    print("-" * len(title))


def main():
    print(f"filter-planning.py -- firmware {VERSION}, commit {COMMIT}, {DATE}")
    print(f"repeater: {LORA_FREQ_MHZ} MHz, BW {LORA_BW_KHZ} kHz, "
          f"max {TX_POWER_MAX_DBM} dBm")

    rule("1. Geschat niveau per band aan de antenne-ingang")
    print(f"aannames: schuine afstand {SLANT_M:.0f} m, patroononderdrukking "
          f"{PATTERN_SUPPRESSION_DB:.0f} dB, ontvangantenne "
          f"{RX_ANT_GAIN_DBI:.0f} dBi buiten band")
    print()
    print(f"{'band':<14}{'MHz':>9}{'dBW':>8}{'FSPL dB':>10}{'aan ingang dBm':>16}")
    total_mw = 0.0
    for name, f, dbw in MAST:
        eirp_dbm = dbw + 30.0
        loss = fspl_db(f, SLANT_M)
        rx = eirp_dbm - PATTERN_SUPPRESSION_DB - loss + RX_ANT_GAIN_DBI
        total_mw += 10 ** (rx / 10.0)
        print(f"{name:<14}{f:>9.1f}{dbw:>8.1f}{loss:>10.1f}{rx:>16.1f}")
    print(f"{'composiet':<14}{'':>9}{'':>8}{'':>10}"
          f"{10 * math.log10(total_mw):>16.1f}")
    print("Eén sector. Drie sectoren samen liggen enkele dB hoger.")

    rule("2. Tweede-orde verschilproducten rond de repeaterfrequentie")
    pairs = [(1815.0, 940.0), (2660.0, 1815.0), (2160.0, 1474.5),
             (3700.0, 2660.0), (2660.0, 1474.5)]
    print(f"{'paar':<18}{'smal (+/-10 MHz)':>26}{'ruim (nominale band)':>28}")
    for hi, lo in pairs:
        n_lo = (hi - NARROW_HALFWIDTH_MHZ) - (lo + NARROW_HALFWIDTH_MHZ)
        n_hi = (hi + NARROW_HALFWIDTH_MHZ) - (lo - NARROW_HALFWIDTH_MHZ)
        hit_n = "RAAK" if n_lo <= LORA_FREQ_MHZ <= n_hi else "mis"
        if hi in BAND_EDGES_WIDE and lo in BAND_EDGES_WIDE:
            w_lo = BAND_EDGES_WIDE[hi][0] - BAND_EDGES_WIDE[lo][1]
            w_hi = BAND_EDGES_WIDE[hi][1] - BAND_EDGES_WIDE[lo][0]
            hit_w = "RAAK" if w_lo <= LORA_FREQ_MHZ <= w_hi else "mis"
            wide = f"{w_lo:.0f}-{w_hi:.0f} MHz  {hit_w}"
        else:
            wide = "geen bandedges bekend"
        print(f"{hi:.0f}-{lo:.0f}".ljust(18)
              + f"{n_lo:.0f}-{n_hi:.0f} MHz  {hit_n}".rjust(26)
              + wide.rjust(28))
    g_lo = (1815.0 - NARROW_HALFWIDTH_MHZ) - GSM_BLOCK[1]
    g_hi = (1815.0 + NARROW_HALFWIDTH_MHZ) - GSM_BLOCK[0]
    print()
    print(f"Met het enige geregistreerde blokbereik ({GSM_BLOCK[0]}-"
          f"{GSM_BLOCK[1]} MHz) tegen 1815 +/-10: {g_lo:.1f}-{g_hi:.1f} MHz "
          f"-- {'RAAK' if g_lo <= LORA_FREQ_MHZ <= g_hi else 'mis'}")

    rule("3. De kwartgolfresonator")
    quarter_mm = 299792458.0 / (LORA_FREQ_MHZ * 1e6) / 4 * 1000
    print(f"kwart golflengte op {LORA_FREQ_MHZ} MHz: {quarter_mm:.1f} mm")
    print("capacitieve topbelasting maakt de geleider korter en schuift de")
    print("eerstvolgende resonantie omhoog; hoeveel hangt af van het ontwerp")
    print()
    for n in (3, 5, 7):
        print(f"{n}f = {n * LORA_FREQ_MHZ:.1f} MHz")
    near = min(MAST, key=lambda b: abs(b[1] - 3 * LORA_FREQ_MHZ))
    print(f"dichtstbijzijnde mastband bij 3f: {near[0]} op {near[1]:.0f} MHz, "
          f"afstand {abs(near[1] - 3 * LORA_FREQ_MHZ):.1f} MHz")

    rule("4. Wanneer een filter loont")
    tx_loss = (TX_POWER_MAX_DBM - TX_LIMIT_DBM) + INSERTION_LOSS_DB
    print(f"zendverlies = ({TX_POWER_MAX_DBM} - {TX_LIMIT_DBM}) + "
          f"{INSERTION_LOSS_DB:.0f} = {tx_loss:.0f} dB")
    print(f"ontvangstwinst = desense - {INSERTION_LOSS_DB:.0f} dB")
    print(f"break-even bij desense = {tx_loss + INSERTION_LOSS_DB:.0f} dB")
    print()
    print(f"{'desense dB':>12}{'RX-winst dB':>14}{'TX-verlies dB':>16}{'netto':>10}")
    for d in (2, 4, 6, 10, 15, 20, 27):
        gain = d - INSERTION_LOSS_DB
        if abs(gain - tx_loss) < 1e-9:
            verdict = "gelijk"
        else:
            verdict = "winst" if gain > tx_loss else "verlies"
        print(f"{d:>12}{gain:>14.0f}{tx_loss:>16.0f}{verdict:>10}")

    rule("5. Meetbereik van de firmware")
    measured_bad = -90
    print(f"gerapporteerde vloer bij de mast: {measured_bad} dBm")
    print(f"ondergrens van de firmware: {NOISE_FLOOR_CLAMP_DBM} dBm")
    print(f"maximaal aantoonbare verbetering: "
          f"{measured_bad - NOISE_FLOOR_CLAMP_DBM} dB")
    thermal = -174 + 10 * math.log10(LORA_BW_KHZ * 1000)
    print(f"thermische ruis over {LORA_BW_KHZ} kHz: {thermal:.1f} dBm")


if __name__ == "__main__":
    main()
