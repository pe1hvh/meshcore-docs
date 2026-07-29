# Voeding en energiemeting

*PMU · INA · ACCU · ZONNEPANEEL*

Zes libraries houden zich bezig met stroom: één voor de
energiebeheerchips op de T-Beam-borden, vier voor stroommeters en één voor
een accubeheersysteem op zonne-energie. Ze verschillen van de sensorgroep
doordat ze niet alleen meten maar ook regelen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, `src/helpers/esp32/TBeamBoard.h`,
> `src/helpers/esp32/TBeamBoard.cpp`,
> `src/helpers/sensors/EnvironmentSensorManager.cpp` en
> `variants/heltec_mesh_solar/platformio.ini`.

## Hoe MeshCore deze groep aanroept

De vier INA-libraries volgen het patroon uit [`sensors.md`](sensors.md): een
`ENV_INCLUDE_INA*`-vlag, een `init_`- en een `query_`-functie, een regel in
de sensortabel. `XPowersLib` staat daarbuiten: die zit in de bordlaag, niet
in de sensorlaag, en wordt bij het opstarten van het bord aangeroepen.

`src/helpers/esp32/TBeamBoard.cpp` r.130

```cpp
      PMU = new XPowersAXP2101(PMU_WIRE_PORT, PIN_BOARD_SDA1, PIN_BOARD_SCL1, I2C_PMU_ADD);
```

## lewisxhe/XPowersLib

De T-Beam-borden hebben een aparte energiebeheerchip: de AXP192 op de oudere
borden, de AXP2101 op de nieuwere. Zo'n chip regelt de laadstroom van de
accu, schakelt de voedingsrails naar de radio en de GPS afzonderlijk in en
uit, en meet de accuspanning. XPowersLib van Lewis He ondersteunt beide
chips achter één interface:

`src/helpers/esp32/TBeamBoard.h` r.87

```cpp
#include "XPowersLib.h"
```

MeshCore houdt één `XPowersLibInterface*` aan en beslist bij het opstarten
welke chip erachter zit. Drie varianten gebruiken de library:
`lilygo_tbeam_SX1262`, `lilygo_tbeam_SX1276` en
`lilygo_tbeam_supreme_SX1262`.

## De vier INA-libraries

De INA-chips van Texas Instruments meten stroom over een shuntweerstand, en
daarnaast de spanning. Ze verschillen in bereik, resolutie en het aantal
kanalen.

**`adafruit/Adafruit INA219`** — één kanaal, bus- en shuntspanning apart
uitleesbaar, tot 26 V. In drie varianten. Zijn `depends=` vraagt om
NeoPixel, GFX en SSD1306 voor de voorbeeldschetsen; zie
[`../dependencies.md`](../dependencies.md).

**`robtillaart/INA226`** — nauwkeuriger dan de INA219, met een instelbare
middeling over meerdere metingen. In één variant, `lilygo_tdeck`.

**`adafruit/Adafruit INA260 Library`** — heeft de shuntweerstand ingebouwd,
zodat er niets berekend hoeft te worden. In één variant, `lilygo_tdeck`.

**`adafruit/Adafruit INA3221 Library`** — drie kanalen op één chip, met een
`sub_ch`-argument in de `query_`-functie om aan te geven welk kanaal bedoeld
wordt. In drie varianten.

## meshsolar

Voor `heltec_mesh_solar` wordt een zip van een volledige commit-hash
opgehaald:

`variants/heltec_mesh_solar/platformio.ini` r.25

```text
  https://github.com/NMIoT/meshsolar/archive/dfc5330dad443982e6cdd37a61d33fc7252f468b.zip
```

Het gaat om de ondersteuning voor het accubeheersysteem op dat bord, dat een
zonnepaneel, een accu en de belasting tegen elkaar afstemt. Anders dan bij
een registrypakket ligt hier precies vast welke code je krijgt: de hash wijst
één commit aan.

## Overzicht

| Library | Versie | Varianten | Borden |
|---|---|---|---|
| `lewisxhe/XPowersLib` | `^0.2.7` | 3 | LilyGo T-Beam (AXP192, AXP2101) |
| `adafruit/Adafruit INA219` | `^1.2.3` | 3 | T-Deck, MinewSemi ME25LS01, ProMicro |
| `robtillaart/INA226` | `^0.6.4` | 1 | T-Deck |
| `adafruit/Adafruit INA260 Library` | `^1.5.3` | 1 | T-Deck |
| `adafruit/Adafruit INA3221 Library` | `^1.0.1` | 3 | T-Deck, MinewSemi ME25LS01, ProMicro |
| `NMIoT/meshsolar` | `dfc5330` | 1 | Heltec Mesh Solar |

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/esp32/TBeamBoard.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/esp32/TBeamBoard.h)
- [`src/helpers/esp32/TBeamBoard.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/esp32/TBeamBoard.cpp)
- [`variants/heltec_mesh_solar/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/heltec_mesh_solar/platformio.ini)
- [lewisxhe/XPowersLib](https://github.com/lewisxhe/XPowersLib)
- [RobTillaart/INA226](https://github.com/RobTillaart/INA226)
