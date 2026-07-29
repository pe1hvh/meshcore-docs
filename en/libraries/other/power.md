# Power and energy measurement

*PMU · INA · BATTERY · SOLAR*

Six libraries deal with power: one for the power management chips on the
T-Beam boards, four for current meters and one for a solar battery management
system. They differ from the sensor group in that they do not only measure but
also regulate.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini`, `src/helpers/esp32/TBeamBoard.h`,
> `src/helpers/esp32/TBeamBoard.cpp`,
> `src/helpers/sensors/EnvironmentSensorManager.cpp` and
> `variants/heltec_mesh_solar/platformio.ini`.

## How MeshCore calls this group

The four INA libraries follow the pattern from [`sensors.md`](sensors.md): an
`ENV_INCLUDE_INA*` flag, an `init_` and a `query_` function, a row in the
sensor table. `XPowersLib` sits outside that: it belongs to the board layer,
not the sensor layer, and is called when the board starts up.

`src/helpers/esp32/TBeamBoard.cpp` r.130

```cpp
      PMU = new XPowersAXP2101(PMU_WIRE_PORT, PIN_BOARD_SDA1, PIN_BOARD_SCL1, I2C_PMU_ADD);
```

## lewisxhe/XPowersLib

The T-Beam boards have a separate power management chip: the AXP192 on the
older boards, the AXP2101 on the newer ones. Such a chip regulates the
battery's charge current, switches the power rails to the radio and the GPS
independently on and off, and measures the battery voltage. XPowersLib by
Lewis He supports both chips behind one interface:

`src/helpers/esp32/TBeamBoard.h` r.87

```cpp
#include "XPowersLib.h"
```

MeshCore keeps one `XPowersLibInterface*` and decides at start-up which chip
sits behind it. Three variants use the library: `lilygo_tbeam_SX1262`,
`lilygo_tbeam_SX1276` and `lilygo_tbeam_supreme_SX1262`.

## The four INA libraries

The INA chips from Texas Instruments measure current across a shunt resistor,
and voltage alongside it. They differ in range, resolution and channel count.

**`adafruit/Adafruit INA219`** — one channel, bus and shunt voltage readable
separately, up to 26 V. In three variants. Its `depends=` asks for NeoPixel,
GFX and SSD1306 for the example sketches; see
[`../dependencies.md`](../dependencies.md).

**`robtillaart/INA226`** — more accurate than the INA219, with configurable
averaging over several measurements. In one variant, `lilygo_tdeck`.

**`adafruit/Adafruit INA260 Library`** — has the shunt resistor built in, so
nothing needs calculating. In one variant, `lilygo_tdeck`.

**`adafruit/Adafruit INA3221 Library`** — three channels on one chip, with a
`sub_ch` argument in the `query_` function to say which channel is meant. In
three variants.

## meshsolar

For `heltec_mesh_solar` a zip of a full commit hash is fetched:

`variants/heltec_mesh_solar/platformio.ini` r.25

```text
  https://github.com/NMIoT/meshsolar/archive/dfc5330dad443982e6cdd37a61d33fc7252f468b.zip
```

It provides the support for that board's battery management system, which
balances a solar panel, a battery and the load against each other. Unlike a
registry package, exactly which code you get is fixed here: the hash points at
one commit.

## Overview

| Library | Version | Variants | Boards |
|---|---|---|---|
| `lewisxhe/XPowersLib` | `^0.2.7` | 3 | LilyGo T-Beam (AXP192, AXP2101) |
| `adafruit/Adafruit INA219` | `^1.2.3` | 3 | T-Deck, MinewSemi ME25LS01, ProMicro |
| `robtillaart/INA226` | `^0.6.4` | 1 | T-Deck |
| `adafruit/Adafruit INA260 Library` | `^1.5.3` | 1 | T-Deck |
| `adafruit/Adafruit INA3221 Library` | `^1.0.1` | 3 | T-Deck, MinewSemi ME25LS01, ProMicro |
| `NMIoT/meshsolar` | `dfc5330` | 1 | Heltec Mesh Solar |

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/esp32/TBeamBoard.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/esp32/TBeamBoard.h)
- [`src/helpers/esp32/TBeamBoard.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/esp32/TBeamBoard.cpp)
- [`variants/heltec_mesh_solar/platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/heltec_mesh_solar/platformio.ini)
- [lewisxhe/XPowersLib](https://github.com/lewisxhe/XPowersLib)
- [RobTillaart/INA226](https://github.com/RobTillaart/INA226)

Translated from Dutch by Anthropic Claude
