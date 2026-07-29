#!/usr/bin/env python3
"""Rekent elk cijfer uit hardware/radio/link-budget.md opnieuw uit.

Firmwarewaarden en externe aannames worden strikt gescheiden gehouden.
Firmwarewaarden komen uit MeshCore v1.16.0, commit 03b6ef4 (28 juli 2026)
en worden waar mogelijk uit een uitgecheckte firmwareboom geteld. De twee
invoerwaarden die niet in de firmwarerepo staan -- het ruisgetal van de
ontvangketen en de benodigde SNR per spreidingsfactor -- staan hieronder
als constante en zijn in het hoofdstuk gemarkeerd met een graadteken.

Gebruik:
    python3 tools/link-budget.py [pad-naar-MeshCore-checkout]

Zonder argument gebruikt het script de ingebakken firmwarewaarden en slaat
het tellen over.
"""

import math
import pathlib
import re
import sys

COMMIT = "03b6ef4"
VERSION = "v1.16.0"
DATE = "28 juli 2026"

# --------------------------------------------------------------------------
# Firmwarewaarden -- wortel-platformio.ini van MeshCore op commit 03b6ef4
# --------------------------------------------------------------------------
LORA_FREQ_MHZ = 869.618      # -D LORA_FREQ=869.618
LORA_BW_KHZ = 62.5           # -D LORA_BW=62.5
LORA_SF_DEFAULT = 8          # -D LORA_SF=8
NOISE_FLOOR_CLAMP_DBM = -120  # RadioLibWrappers.cpp, ondergrens van de meting
SAMPLING_THRESHOLD_DB = 14    # RadioLibWrappers.cpp, SAMPLING_THRESHOLD
NUM_NOISE_FLOOR_SAMPLES = 64  # RadioLibWrappers.cpp

# --------------------------------------------------------------------------
# Externe aannames -- NIET uit de firmwarerepo, in het hoofdstuk met ° gemerkt
# --------------------------------------------------------------------------
RX_NOISE_FIGURE_DB = 6.0     # ° ruisgetal van de ontvangketen, ongeverifieerd
REQUIRED_SNR_DB = {          # ° benodigde SNR per SF, ongeverifieerd
    7: -7.5,
    8: -10.0,
    9: -12.5,
    10: -15.0,
    11: -17.5,
    12: -20.0,
}

THERMAL_NOISE_DBM_PER_HZ = -174.0  # kT bij kamertemperatuur, geen datasheet


def thermal_noise_dbm(bandwidth_khz: float) -> float:
    """Thermische ruisvloer over de gegeven bandbreedte."""
    return THERMAL_NOISE_DBM_PER_HZ + 10 * math.log10(bandwidth_khz * 1000.0)


def receiver_noise_dbm(bandwidth_khz: float) -> float:
    """Ruisvloer van de ontvanger: thermisch plus ruisgetal."""
    return thermal_noise_dbm(bandwidth_khz) + RX_NOISE_FIGURE_DB


def sensitivity_dbm(sf: int, bandwidth_khz: float = LORA_BW_KHZ) -> float:
    """Gevoeligheid bij een spreidingsfactor."""
    return receiver_noise_dbm(bandwidth_khz) + REQUIRED_SNR_DB[sf]


def fspl_db(distance_km: float, freq_mhz: float = LORA_FREQ_MHZ) -> float:
    """Vrijeruimteverlies."""
    return 32.44 + 20 * math.log10(freq_mhz) + 20 * math.log10(distance_km)


def range_km(path_loss_db: float, freq_mhz: float = LORA_FREQ_MHZ) -> float:
    """Afstand die bij een gegeven padverlies hoort, in vrije ruimte."""
    return 10 ** ((path_loss_db - 32.44 - 20 * math.log10(freq_mhz)) / 20.0)


def count_tx_power(firmware_root: pathlib.Path):
    """Telt actieve -D LORA_TX_POWER-regels in variants/*/platformio.ini."""
    pattern = re.compile(r"-D\s*LORA_TX_POWER\s*=\s*([0-9]+)")
    lines, files, values = 0, set(), {}
    for ini in sorted((firmware_root / "variants").rglob("platformio.ini")):
        for line in ini.read_text(errors="replace").splitlines():
            if line.strip().startswith(";"):
                continue
            match = pattern.search(line)
            if match:
                lines += 1
                files.add(ini.parent.name)
                value = int(match.group(1))
                values[value] = values.get(value, 0) + 1
    return lines, len(files), values


def main() -> None:
    print(f"link-budget.py -- MeshCore {VERSION}, commit {COMMIT}, {DATE}")
    print("=" * 72)

    print("\n1. Ruisvloer en gevoeligheid")
    print(f"   bandbreedte                      {LORA_BW_KHZ:>8.1f} kHz")
    print(f"   thermische ruis over die band    {thermal_noise_dbm(LORA_BW_KHZ):>8.1f} dBm")
    print(f"   ruisgetal ontvanger              {RX_NOISE_FIGURE_DB:>8.1f} dB   (extern)")
    print(f"   ruisvloer ontvanger              {receiver_noise_dbm(LORA_BW_KHZ):>8.1f} dBm")
    print(f"   ondergrens van de firmwaremeting {NOISE_FLOOR_CLAMP_DBM:>8.1f} dBm")

    print("\n2. Gevoeligheid per spreidingsfactor")
    print(f"   {'SF':>3}  {'SNR (dB)':>9}  {'gevoeligheid (dBm)':>19}")
    for sf in sorted(REQUIRED_SNR_DB):
        print(f"   {sf:>3}  {REQUIRED_SNR_DB[sf]:>9.1f}  {sensitivity_dbm(sf):>19.1f}")

    print("\n3. Budget bij 22 dBm zendvermogen en 2,15 dBi aan beide kanten")
    tx_power, ant_gain, cable_loss = 22.0, 2.15, 1.0
    eirp = tx_power + ant_gain - cable_loss
    print(f"   zendvermogen chip                {tx_power:>8.1f} dBm")
    print(f"   antennewinst                     {ant_gain:>8.2f} dBi")
    print(f"   kabelverlies                     {cable_loss:>8.1f} dB")
    print(f"   e.i.r.p.                         {eirp:>8.2f} dBm")
    print(f"\n   {'SF':>3}  {'budget (dB)':>12}  {'vrije ruimte (km)':>18}")
    for sf in sorted(REQUIRED_SNR_DB):
        budget = eirp + ant_gain - cable_loss - sensitivity_dbm(sf)
        print(f"   {sf:>3}  {budget:>12.1f}  {range_km(budget):>18.1f}")

    print("\n4. Wat een dB kost")
    base_sf = LORA_SF_DEFAULT
    budget = eirp + ant_gain - cable_loss - sensitivity_dbm(base_sf)
    print(f"   budget bij SF{base_sf}                    {budget:>8.1f} dB")
    for delta in (-6, -3, -1, 0, 1, 3, 6):
        print(f"   {delta:+3d} dB  ->  {range_km(budget + delta):>8.1f} km")

    print("\n5. Vrijeruimteverlies op enkele afstanden")
    for km in (0.1, 0.5, 1, 2, 5, 10, 20, 50):
        print(f"   {km:>6.1f} km  {fspl_db(km):>8.1f} dB")

    if len(sys.argv) > 1:
        root = pathlib.Path(sys.argv[1])
        lines, files, values = count_tx_power(root)
        print("\n6. LORA_TX_POWER in de firmwareboom")
        print(f"   actieve regels in variants/*/platformio.ini  {lines}")
        print(f"   variantmappen                                {files}")
        for value in sorted(values, reverse=True):
            print(f"   {value:>3} dBm  {values[value]:>4} regels")
    else:
        print("\n6. LORA_TX_POWER: geef een pad naar een MeshCore-checkout mee om te tellen")


if __name__ == "__main__":
    main()
