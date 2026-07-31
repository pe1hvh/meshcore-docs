# Adafruit LittleFS voor STM32

*PORT · MEEGELEVERD · LOKAAL PAD · BUILD_HEX*

De STM32WL draait dezelfde MeshCore-code als de andere platformen, maar kan
de LittleFS-implementatie van de nRF52-core niet gebruiken. In `arch/stm32/`
staat daarom een uitgeklede versie van die library, die via een lokaal pad de
build in komt.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, `arch/stm32/Adafruit_LittleFS_stm32/library.properties`,
> `arch/stm32/Adafruit_LittleFS_stm32/README.md` en `arch/stm32/build_hex.py`.

## Wat het doet

LittleFS is een bestandssysteem voor flashgeheugen: het verdeelt schrijfacties
over de chip, houdt rekening met blokken die stuk kunnen gaan en overleeft een
stroomonderbreking midden in een schrijfactie. Adafruit levert er een
Arduino-verpakking omheen als onderdeel van de nRF52-core, onder de naam
`Adafruit_LittleFS`.

Die verpakking is verweven met de nRF52-omgeving. De versie in `arch/stm32/`
is daarvan ontdaan; het `README.md` van de map beschrijft dat kort en
letterlijk als: LittleFS van Adafruit, ontdaan van de dingen die het op STM32
niet laten compileren — verwijzingen naar TinyUSB en FreeRTOS, hoofdzakelijk.
De `library.properties` houdt versie 0.11.0 en de oorspronkelijke
Adafruit-herkomst aan.

## Hoe MeshCore hem binnenhaalt

`platformio.ini` r.118-120

```text
lib_deps = ${arduino_base.lib_deps}
  file://arch/stm32/Adafruit_LittleFS_stm32
  SubGhz
```

Een lokaal pad: PlatformIO compileert de map als library mee. Er is geen
upstream om vanaf te halen, geen versiebereik en geen updatepad — wat er in
de repo staat, is wat je krijgt.

De sectie `[stm32_base]` heeft nog een tweede eigenaardigheid uit dezelfde
map:

`platformio.ini` r.111

```text
extra_scripts = post:arch/stm32/build_hex.py
```

Dat script draait na het bouwen en levert het `.hex`-bestand op dat de
gebruikelijke STM32-flashgereedschappen verwachten.

## Hoe MeshCore hem gebruikt

De port wordt niet anders aangeroepen dan de nRF52-versie. In de
voorbeeldschetsen loopt hij mee in dezelfde tak:

`examples/companion_radio/main.cpp` r.15-16

```cpp
#if defined(NRF52_PLATFORM) || defined(STM32_PLATFORM)
  #include <InternalFileSystem.h>
```

Dat de twee platformen hier op één regel staan, is precies waar deze port
voor bedoeld is: dezelfde include, dezelfde klasse, andere onderliggende
implementatie.

Anders dan op nRF52 is er op STM32 geen tweede volume — `EXTRAFS` staat
alleen in `[nrf52_base]`. Zie [`custom-lfs.md`](custom-lfs.md).

## Wat het voor een node betekent

Een STM32WL-node kan instellingen, sleutels en contacten bewaren over een
herstart heen, net als een nRF52-node. Dat de firmware voor dat platform een
eigen kopie van de library meedraagt, betekent ook dat verbeteringen in de
Adafruit-versie hier niet vanzelf terechtkomen: die kopie wordt met de hand
bijgewerkt of niet.

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`arch/stm32/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/arch/stm32)
- [`arch/stm32/Adafruit_LittleFS_stm32/README.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/arch/stm32/Adafruit_LittleFS_stm32/README.md)
- [`arch/stm32/build_hex.py`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/arch/stm32/build_hex.py)
- [adafruit/Adafruit_nRF52_Arduino](https://github.com/adafruit/Adafruit_nRF52_Arduino)
