# CustomLFS

*LITTLEFS · TWEEDE BESTANDSSYSTEEM · EXTRAFS · QSPI*

Op nRF52 heeft MeshCore twee bestandssystemen. Het interne van de
Adafruit-core houdt de instellingen en sleutels bij; daarnaast maakt
CustomLFS een tweede LittleFS-volume aan op een ander stuk flash, of op een
externe QSPI-chip. Alleen nRF52 doet dit.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, `examples/companion_radio/main.cpp` en
> `examples/companion_radio/DataStore.h`.

## Wat het doet

CustomLFS van `oltaco` is een uitbreiding op de LittleFS-ondersteuning van de
Adafruit nRF52-core. Waar die core één vast intern volume kent, laat
CustomLFS je zelf een volume definiëren: beginadres, grootte en blokgrootte
geef je op, en je krijgt er een LittleFS op terug. De variant
`CustomLFS_QSPIFlash` doet hetzelfde op een externe flashchip aan de
QSPI-bus. De repo staat op
[github.com/oltaco/CustomLFS](https://github.com/oltaco/CustomLFS).

## Hoe MeshCore hem binnenhaalt

`platformio.ini` r.95

```text
  https://github.com/oltaco/CustomLFS#0.2.2
```

Geen registrypakket maar een git-URL, met achter `#` de tag `0.2.2`. De regel
staat in `[nrf52_base]`, dus alleen nRF52-varianten krijgen hem.

Twee bouwvlaggen in dezelfde sectie horen erbij:

`platformio.ini` r.91-92

```text
  -D LFS_NO_ASSERT=1
  -D EXTRAFS=1
```

`EXTRAFS` schakelt het tweede volume in. `LFS_NO_ASSERT` haalt de asserts uit
LittleFS: een inconsistentie in het bestandssysteem laat de node dan
doorlopen in plaats van hem te laten stoppen.

## Hoe MeshCore hem gebruikt

De keuze tussen intern, extra en QSPI valt bij het compileren:

`examples/companion_radio/main.cpp` r.15-26

```cpp
#if defined(NRF52_PLATFORM) || defined(STM32_PLATFORM)
  #include <InternalFileSystem.h>
  #if defined(QSPIFLASH)
    #include <CustomLFS_QSPIFlash.h>
    DataStore store(InternalFS, QSPIFlash, rtc_clock);
  #else
  #if defined(EXTRAFS)
    #include <CustomLFS.h>
    CustomLFS ExtraFS(0xD4000, 0x19000, 128);
    DataStore store(InternalFS, ExtraFS, rtc_clock);
  #else
    DataStore store(InternalFS, rtc_clock);
```

De drie getallen bij `CustomLFS ExtraFS` zijn het beginadres in de flash
(`0xD4000`), de grootte (`0x19000`, 102 400 bytes) en de blokgrootte.
`DataStore` krijgt vervolgens één of twee volumes mee. Is er een tweede, dan
gaan contacten en kanalen daarheen en blijft de rest op het interne volume:

`examples/companion_radio/DataStore.h` r.54

```cpp
  FILESYSTEM* _getContactsChannelsFS() const { if (_fsExtra) return _fsExtra; return _fs;};
```

De tekst `CustomLFS` komt in twee bronbestanden voor; het bijbehorende
`InternalFS` in twaalf.

## Wat het voor een node betekent

Het tweede volume geeft ruimte die niet meetelt bij het interne
bestandssysteem. Op een companion-node komen de contacten en kanalen daarop
te staan, gescheiden van de instellingen en sleutels op het interne volume.

Dat dit alleen op nRF52 bestaat, komt doordat de flashindeling daar bekend en
stabiel is: de nRF52-core reserveert een vast gebied, en wat daarna komt is
vrij. Op ESP32 wordt de indeling door een partitietabel bepaald, op RP2040
door de core zelf. Op STM32WL is er domweg te weinig flash.

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`examples/companion_radio/DataStore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/DataStore.h)
- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/main.cpp)
- [oltaco/CustomLFS](https://github.com/oltaco/CustomLFS)
