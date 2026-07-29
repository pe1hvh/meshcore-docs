# Adafruit LittleFS for STM32

*PORT · VENDORED · LOCAL PATH · BUILD_HEX*

The STM32WL runs the same MeshCore code as the other platforms, but cannot use
the LittleFS implementation from the nRF52 core. `arch/stm32/` therefore holds
a stripped-down version of that library, which enters the build through a
local path.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini`, `arch/stm32/Adafruit_LittleFS_stm32/library.properties`,
> `arch/stm32/Adafruit_LittleFS_stm32/README.md` and
> `arch/stm32/build_hex.py`.

## What it does

LittleFS is a file system for flash memory: it spreads writes across the chip,
copes with blocks that go bad and survives a power cut in the middle of a
write. Adafruit wraps an Arduino layer around it as part of the nRF52 core,
under the name `Adafruit_LittleFS`.

That wrapper is entangled with the nRF52 environment. The version in
`arch/stm32/` has been stripped of it; the directory's `README.md` describes
that briefly and literally as: LittleFS from Adafruit, stripped of the things
that keep it from compiling on STM32 — references to TinyUSB and FreeRTOS,
mostly. The `library.properties` keeps version 0.11.0 and the original
Adafruit provenance.

## How MeshCore pulls it in

`platformio.ini` r.118-120

```text
lib_deps = ${arduino_base.lib_deps}
  file://arch/stm32/Adafruit_LittleFS_stm32
  SubGhz
```

A local path: PlatformIO compiles the directory in as a library. There is no
upstream to fetch from, no version range and no update path — what is in the
repo is what you get.

The `[stm32_base]` section has a second peculiarity from the same directory:

`platformio.ini` r.111

```text
extra_scripts = post:arch/stm32/build_hex.py
```

That script runs after the build and produces the `.hex` file the usual STM32
flashing tools expect.

## How MeshCore uses it

The port is not called any differently from the nRF52 version. In the example
sketches it runs in the same branch:

`examples/companion_radio/main.cpp` r.15-16

```cpp
#if defined(NRF52_PLATFORM) || defined(STM32_PLATFORM)
  #include <InternalFileSystem.h>
```

That the two platforms share a line here is exactly what this port is for: the
same include, the same class, a different implementation underneath.

Unlike on nRF52 there is no second volume on STM32 — `EXTRAFS` appears only in
`[nrf52_base]`. See [`custom-lfs.md`](custom-lfs.md).

## What it means for a node

An STM32WL node can keep settings, keys and contacts across a restart, just
like an nRF52 node. That the firmware for that platform carries its own copy
of the library also means improvements in the Adafruit version do not arrive
here by themselves: that copy is updated by hand or not at all.

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`arch/stm32/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/arch/stm32)
- [`arch/stm32/Adafruit_LittleFS_stm32/README.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/arch/stm32/Adafruit_LittleFS_stm32/README.md)
- [`arch/stm32/build_hex.py`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/arch/stm32/build_hex.py)
- [adafruit/Adafruit_nRF52_Arduino](https://github.com/adafruit/Adafruit_nRF52_Arduino)

Translated from Dutch by Anthropic Claude
