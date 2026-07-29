# CustomLFS

*LITTLEFS · SECOND FILE SYSTEM · EXTRAFS · QSPI*

On nRF52, MeshCore has two file systems. The internal one from the Adafruit
core holds the settings and keys; alongside it, CustomLFS creates a second
LittleFS volume on another piece of flash, or on an external QSPI chip. Only
nRF52 does this.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini` and `examples/companion_radio/main.cpp`.

## What it does

CustomLFS by `oltaco` extends the LittleFS support in the Adafruit nRF52 core.
Where that core knows one fixed internal volume, CustomLFS lets you define one
yourself: you give a start address, a size and a block size, and you get a
LittleFS on it. The `CustomLFS_QSPIFlash` variant does the same on an external
flash chip on the QSPI bus. The repository is at
[github.com/oltaco/CustomLFS](https://github.com/oltaco/CustomLFS).

## How MeshCore pulls it in

`platformio.ini` r.95

```text
  https://github.com/oltaco/CustomLFS#0.2.2
```

Not a registry package but a git URL, with the tag `0.2.2` after `#`. The line
sits in `[nrf52_base]`, so only nRF52 variants get it.

Two build flags in the same section belong with it:

`platformio.ini` r.91-92

```text
  -D LFS_NO_ASSERT=1
  -D EXTRAFS=1
```

`EXTRAFS` switches on the second volume. `LFS_NO_ASSERT` strips the asserts
out of LittleFS: an inconsistency in the file system then lets the node carry
on rather than halting it.

## How MeshCore uses it

The choice between internal, extra and QSPI falls at compile time:

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

The three numbers on `CustomLFS ExtraFS` are the start address in flash
(`0xD4000`), the size (`0x19000`, 102,400 bytes) and the block size.
`DataStore` then receives one or two volumes. If there is a second, contacts
and channels go there and the rest stays on the internal volume:

`examples/companion_radio/DataStore.h` r.54

```cpp
  FILESYSTEM* _getContactsChannelsFS() const { if (_fsExtra) return _fsExtra; return _fs;};
```

The text `CustomLFS` occurs in two source files; the accompanying `InternalFS`
in twelve.

## What it means for a node

The second volume provides space that does not count against the internal file
system. On a companion node the contacts and channels end up there, separated
from the settings and keys on the internal volume.

That this exists only on nRF52 comes down to the flash layout there being
known and stable: the nRF52 core reserves a fixed region, and what follows is
free. On ESP32 the layout is set by a partition table, on RP2040 by the core
itself. On STM32WL there is simply too little flash.

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`examples/companion_radio/DataStore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/DataStore.h)
- [`examples/companion_radio/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/companion_radio/main.cpp)
- [oltaco/CustomLFS](https://github.com/oltaco/CustomLFS)

Translated from Dutch by Anthropic Claude
