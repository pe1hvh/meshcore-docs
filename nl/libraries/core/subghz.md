# SubGhz

*STM32WL · GEEN SPI · FRAMEWORKLIBRARY · INCLUDEPAD*

Op alle MeshCore-platformen zit de radio als losse chip aan de SPI-bus.
Op de STM32WL niet: daar zit hij op dezelfde die als de processor. De
SubGhz-library uit de STM32duino-core is de laag die dat mogelijk maakt, en
hij komt op een andere manier binnen dan elke andere library in dit
overzicht.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, `src/helpers/radiolib/CustomSTM32WLx.h` en
> `src/helpers/radiolib/CustomSTM32WLxWrapper.h`.

## Wat het doet

De STM32WL is een microcontroller met een geïntegreerde sub-GHz-radio. Die
radio is intern verbonden met de processor via een eigen SPI-controller die
niet naar buiten komt. De SubGhz-library van STM32duino biedt daar de
toegang toe: hij initialiseert die interne bus en levert de
laagniveaufuncties waarmee de radiokern aangesproken kan worden.

De library is onderdeel van het frameworkpakket `framework-arduinoststm32`.
Hij staat niet in de PlatformIO-registry en heeft geen eigen versienummer.

## Hoe MeshCore hem binnenhaalt

Twee regels zijn ervoor nodig. Eerst het includepad, want de library ligt
binnen het frameworkpakket:

`platformio.ini` r.115

```text
  -I $PROJECT_PACKAGES_DIR/framework-arduinoststm32/libraries/SubGhz/src
```

En daarna de declaratie zelf:

`platformio.ini` r.120

```text
  SubGhz
```

Geen auteursprefix en geen versie — net als `SPI` en `Wire` is dit een
frameworklibrary. Zie [`wire-spi.md`](wire-spi.md). Beide regels staan in
`[stm32_base]`, dus alleen de twee `wio-e5`-varianten krijgen ze.

## Hoe MeshCore hem gebruikt

Niet rechtstreeks. MeshCore praat met de radiokern via RadioLib, die daarvoor
de klasse `STM32WLx` en het moduletype `STM32WLx_Module` heeft. Het
MeshCore-eigen deel bestaat uit een `Custom`-klasse en een wrapper:

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

De radiokern van de STM32WL is verwant aan de SX126x-familie, en dat is te
zien: dezelfde `SX126xReset.h` die de losse SX1262 opnieuw kalibreert, wordt
hier ook gebruikt. In elf van de 590 bronbestanden komt `SubGhz` of
`STM32WL` voor.

## Wat het voor een node betekent

Er zijn geen radiopennen om te bedraden en geen `P_LORA_*`-definities om te
kloppen te krijgen: de verbinding zit in de chip. Dat maakt een
STM32WL-bord eenvoudiger, en het is ook de reden dat het platform op andere
punten juist beperkter is — er is minder flash en minder RAM dan op de
ESP32- en nRF52-borden.

Het platform en zijn eigenschappen staan verder beschreven in
[`../../platform/platform-families.md`](../../platform/platform-families.md).

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/radiolib/CustomSTM32WLx.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/radiolib/CustomSTM32WLx.h)
- [`src/helpers/radiolib/CustomSTM32WLxWrapper.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/radiolib/CustomSTM32WLxWrapper.h)
- [stm32duino/Arduino_Core_STM32](https://github.com/stm32duino/Arduino_Core_STM32)
