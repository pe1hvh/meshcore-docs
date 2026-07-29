# SubGhz

*STM32WL · NO SPI · FRAMEWORK LIBRARY · INCLUDE PATH*

On every MeshCore platform the radio is a separate chip on the SPI bus. Not on
the STM32WL: there it sits on the same die as the processor. The SubGhz
library from the STM32duino core is the layer that makes that possible, and it
arrives in a different way from every other library in this overview.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini`, `src/helpers/radiolib/CustomSTM32WLx.h` and
> `src/helpers/radiolib/CustomSTM32WLxWrapper.h`.

## What it does

The STM32WL is a microcontroller with an integrated sub-GHz radio. That radio
is connected internally to the processor through its own SPI controller that
never comes out to the pins. STM32duino's SubGhz library provides the access
to it: it initialises that internal bus and supplies the low-level functions
through which the radio core can be addressed.

The library is part of the `framework-arduinoststm32` package. It is not in
the PlatformIO registry and has no version number of its own.

## How MeshCore pulls it in

Two lines are needed. First the include path, because the library lives inside
the framework package:

`platformio.ini` r.115

```text
  -I $PROJECT_PACKAGES_DIR/framework-arduinoststm32/libraries/SubGhz/src
```

And then the declaration itself:

`platformio.ini` r.120

```text
  SubGhz
```

No author prefix and no version — like `SPI` and `Wire` this is a framework
library. See [`wire-spi.md`](wire-spi.md). Both lines sit in `[stm32_base]`,
so only the two `wio-e5` variants get them.

## How MeshCore uses it

Not directly. MeshCore talks to the radio core through RadioLib, which has the
class `STM32WLx` and the module type `STM32WLx_Module` for it. The
MeshCore-side part consists of a `Custom` class and a wrapper:

`src/helpers/radiolib/CustomSTM32WLxWrapper.h` r.1-9

```cpp
#pragma once

#include "CustomSTM32WLx.h"
#include "RadioLibWrappers.h"
#include "SX126xReset.h"
#include <math.h>

class CustomSTM32WLxWrapper : public RadioLibWrapper {
public:
```

The STM32WL's radio core is related to the SX126x family, and it shows: the
same `SX126xReset.h` that recalibrates a discrete SX1262 is used here too. In
eleven of the 590 source files, `SubGhz` or `STM32WL` occurs.

## What it means for a node

There are no radio pins to wire up and no `P_LORA_*` definitions to get right:
the connection is inside the chip. That makes an STM32WL board simpler, and it
is also why the platform is more constrained in other respects — there is less
flash and less RAM than on the ESP32 and nRF52 boards.

The platform and its properties are described further in
[`../../platform/platform-families.md`](../../platform/platform-families.md).

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/radiolib/CustomSTM32WLx.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/radiolib/CustomSTM32WLx.h)
- [`src/helpers/radiolib/CustomSTM32WLxWrapper.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/radiolib/CustomSTM32WLxWrapper.h)
- [stm32duino/Arduino_Core_STM32](https://github.com/stm32duino/Arduino_Core_STM32)

Translated from Dutch by Anthropic Claude
