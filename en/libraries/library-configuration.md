# Library Configuration

*OPT-OUT · OPT-IN · TYPE INJECTION · LIB_DEPS*

A library listed in `lib_deps` is not yet finished. What ends up in the
firmware and how it behaves depends on macros handed to the compiler. There is
no standard for how those macros work: one library assumes you want everything
and lets you leave things out, another assumes you want nothing and lets you
add things, and most have no switches at all. This chapter puts those
conventions side by side, because without that overview a line such as
`-D RADIOLIB_EXCLUDE_MORSE=1` cannot be read.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — `platformio.ini`, the
> seventy-nine `variants/*/platformio.ini`,
> `src/helpers/sensors/EnvironmentSensorManager.cpp`,
> `src/helpers/BaseChatMesh.h` and `examples/simple_repeater/main.cpp`.
> Also against the library sources themselves: RadioLib 7.6.0, both littlefs
> copies in the build tree, Adafruit SSD1306, Adafruit RTClib,
> `rweather/Crypto`, ESPAsyncWebServer and CustomLFS 0.2.2.

## Seventeen flags

Of all the macros MeshCore hands to the compiler, a small share is aimed at a
library. The rest is MeshCore's own configuration or a setting for an Arduino
core. The numbers are in the [inventory](#inventory); the core of it is this:
**seventeen** active macros touch a library, and **all seventeen** live in the
root `platformio.ini`. The seventy-nine variant files contribute none.

Sixteen of those seventeen are for RadioLib, one for littlefs. Library
configuration in MeshCore is therefore almost entirely centralised, and almost
entirely one library.

## Exclusion: the default state is everything

RadioLib has no macro to switch a driver *on*. The umbrella header includes
every module driver and every protocol unconditionally:

`RadioLib.h` r.76-124 (v7.6.0)

```text
#include "modules/CC1101/CC1101.h"
#include "modules/LLCC68/LLCC68.h"
...
#include "protocols/Morse/Morse.h"
#include "protocols/SSTV/SSTV.h"
```

The switch sits one level down, in the headers themselves, and is phrased
negatively:

`Morse.h` r.1

```text
#if !defined(_RADIOLIB_MORSE_H) && !RADIOLIB_EXCLUDE_MORSE
```

An undefined macro evaluates to `0` in the preprocessor. Without any flags
`!RADIOLIB_EXCLUDE_MORSE` is true and the class is compiled in. That is why
`BuildOpt.h` ships the list of exclusion macros commented out (r.182-204):
inclusion is the default state, exclusion is the action.

The library gives two reasons of its own for excluding — avoiding name
collisions with the platform, and shortening the build (`BuildOpt.h`
r.177-178). For MeshCore flash space is added to that: a build that has to fit
on an nRF52840 cannot carry drivers for radios the board does not have.

Two things are worth knowing when reading that list. First, the exclusions are
unidirectionally dependent: `SX1231` derives from `RF69` and `RFM2X` from
`SI443X`, so excluding the base class loses the derived one automatically —
not the other way round (`BuildOpt.h` r.179-181). Second, the list in
`BuildOpt.h` is incomplete: it holds twenty-three macros while the source
files use twenty-five. `RADIOLIB_EXCLUDE_ADSB` and `RADIOLIB_EXCLUDE_LR2021`
(`LR2021.h` r.6) are undocumented.

This mechanism is not unique to RadioLib. Two other libraries in the build
tree work exactly the same way:

| Library | Macro | Default without the macro | Does MeshCore set it? |
|---|---|---|---|
| RadioLib 7.6.0 | `RADIOLIB_EXCLUDE_*` | everything included | fourteen |
| littlefs | `LFS_NO_ASSERT` | asserts active | yes, on nRF52 |
| Adafruit SSD1306 | `SSD1306_NO_SPLASH` | splash bitmap compiled in | no |

`arch/stm32/Adafruit_LittleFS_stm32/src/littlefs/lfs_util.h` r.77-81

```text
#ifndef LFS_NO_ASSERT
#define LFS_ASSERT(test) assert(test)
#else
#define LFS_ASSERT(test)
#endif
```

And Adafruit ships its own commented out, just as RadioLib does:

`Adafruit_SSD1306.h` r.36

```text
// #define SSD1306_NO_SPLASH
```

For littlefs that mechanism has a consequence worth noting. littlefs appears
in no `lib_deps` line at all — it comes along inside other packages, and there
are two of them. On nRF52 the copy inside the forked Adafruit framework, on
STM32 the copy inside the repository itself
(`arch/stm32/Adafruit_LittleFS_stm32/src/littlefs/`). The flag
`-D LFS_NO_ASSERT=1` sits in `[nrf52_base]` (`platformio.ini` r.91) and not in
`[stm32_base]`. Same library, two builds, opposite states: nRF52 firmware
compiles littlefs without asserts, STM32 firmware with them. CustomLFS
contains no littlefs of its own; it is a wrapper around `Adafruit_LittleFS`
(`CustomLFS.h` r.30) — see [`core/custom-lfs.md`](core/custom-lfs.md).

## Inclusion: same problem, opposite convention

The other half of RadioLib's configuration is opt-in after all.
`RADIOLIB_GODMODE` and `RADIOLIB_STATIC_ONLY` are off by default and add
behaviour once defined; see [`core/radiolib.md`](core/radiolib.md) for what
MeshCore does with them.

For its own code MeshCore uses opt-in consistently. Every sensor driver sits
behind its own flag:

`platformio.ini` r.123-137

```text
[sensor_base]
build_flags =
  -D ENV_INCLUDE_GPS=1
  -D ENV_INCLUDE_AHTX0=1
  -D ENV_INCLUDE_BME280=1
  ...
```

`src/helpers/sensors/EnvironmentSensorManager.cpp` r.63

```text
#if ENV_INCLUDE_BME280
```

No flag, no driver. That is the mirror image of RadioLib, in the same
firmware, for the same purpose — saving flash. Anyone reading only
`radiolib.md` would conclude that exclusion is the norm; anyone reading only
[`other/sensors.md`](other/sensors.md) concludes the opposite. Both
conventions exist side by side and the choice belongs to the author of the
code, not to MeshCore.

## Override: a value with a default

A third form switches nothing on or off but moves a value. The pattern is
`#ifndef` with a default below it, so that a `-D` from outside wins.
ESPAsyncWebServer does this (`ESPAsyncWebServer.h` r.72), and so does
MeshCore:

`src/helpers/BaseChatMesh.h` r.36-38

```text
#ifndef MAX_CONTACTS
  #define MAX_CONTACTS  32
#endif
```

These macros cannot be recognised by their name and cannot be found by
searching `platformio.ini`: if nobody overrides them they appear nowhere in
the build and still apply. The only way to inventory them is to read the
library source.

## Type injection: a macro carrying a class name

The fourth form carries not a `1` but a type. `RADIO_CLASS`, `WRAPPER_CLASS`,
`DISPLAY_CLASS` and `EINK_DISPLAY_MODEL` hold the name of the class the
firmware has to instantiate:

`variants/heltec_v3/platformio.ini` r.18

```text
  -D RADIO_CLASS=CustomSX1262
```

Presence and identity sit in one macro, and the firmware uses both properties:

`examples/simple_repeater/main.cpp` r.6-8

```text
#ifdef DISPLAY_CLASS
  #include "UITask.h"
  static UITask ui_task(display);
```

`#ifdef` asks whether there is a screen; the value determines which one. This
is MeshCore's own mechanism rather than a library convention, but it does
decide which display library ends up in the build — see
[`other/displays.md`](other/displays.md).

## Libraries without switches

Most libraries in MeshCore have no configuration macros at all. `Crypto.h`
from `rweather/Crypto` holds a single `#ifndef`, and that is the include
guard. `RTClib.h` holds eight chip classes behind, also, one include guard.
What you get is decided by what you include and instantiate.

For libraries like that, exclusion moves up to the dependency level.
`adafruit/Adafruit SSD1306` appears in twenty-eight of the seventy-nine
variants; the other fifty-one builds do not contain the library because it is
not declared there. No macro needed — see
[`dependencies.md`](dependencies.md) and
[`introduction.md`](introduction.md) for how those declarations work.

That makes `lib_deps` the most powerful of the four exclusion mechanisms, with
one limitation: it works per `[env:…]` section. Flags in `[arduino_base]`
apply to all 507 build targets, so a driver one board needs has to stay in for
every board. That is why MeshCore excludes fourteen of the twenty-five
RadioLib macros and no more: the rest belong to chips that are used somewhere
in the range.

## Forks

When nothing else remains, MeshCore changes the library itself. That happens
in four ways: a copy inside the repository (`lib/ed25519`, `lib/nrf52`,
`arch/esp32/AsyncElegantOTA`, `arch/stm32/Adafruit_LittleFS_stm32`), a forked
framework (`platformio.ini` r.87, with the reason in the comment above it), a
library forked into another repository
(`variants/lilygo_techo_lite/platformio.ini` r.42) and a pinned archive
download. Configuration by changing the code, at the price that an upstream
update no longer arrives automatically.

## Where the macros enter

RadioLib offers two channels: `-D` flags, and a configuration file shipped
with the library for you to fill in.

`BuildOptUser.h` r.4-6

```text
// this file can be used to define any user build options
// most commonly, RADIOLIB_EXCLUDE_* macros
// or enabling debug output
```

That file is included from `TypeDef.h` r.5. MeshCore does not use it, and that
is consistent: PlatformIO manages the directory the library lives in and
fetches it again on a version change, which wipes out a manual edit to
`BuildOptUser.h`. A `-D` in `platformio.ini` lives in the repository and
survives that.

## Inventory

The table holds every active macro across the eighty `platformio.ini` files
that is consumed by a third-party library. Ownership does not follow from the
name, so it comes from a table inside the script recording, per namespace,
which source file reads the macro; those references were checked by hand
against the library source. Commented-out lines do not count: a
`; -D RADIOLIB_DEBUG_SPI=1` is part of no build.

<!-- config-flags:start -->

*Generated with `tools/config-flags.py` against commit `03b6ef4`.*

| Macro | Library | Mechanism | Section | Where |
|---|---|---|---|---|
| `LFS_NO_ASSERT` | `littlefs (via Adafruit_LittleFS)` | exclusion | `[nrf52_base]` | root |
| `RADIOLIB_EXCLUDE_AFSK` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_APRS` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_AX25` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_BELL` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_CC1101` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_HELLSCHREIBER` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_MORSE` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_RF69` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_RFM2X` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_RTTY` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_SI443X` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_SSTV` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_SX1231` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_EXCLUDE_SX128X` | `jgromes/RadioLib` | exclusion | `[arduino_base]` | root |
| `RADIOLIB_GODMODE` | `jgromes/RadioLib` | inclusion | `[arduino_base]` | root |
| `RADIOLIB_STATIC_ONLY` | `jgromes/RadioLib` | inclusion | `[arduino_base]` | root |

Of the 277 unique `-D` macros across the eighty `platformio.ini` files, 17 target a library, 6 an Arduino core or platform, and 254 MeshCore's own code.

Commented out, so active in no build: `RADIOLIB_DEBUG_BASIC`, `RADIOLIB_DEBUG_SPI`.

<!-- config-flags:end -->

The table covers only what is in `platformio.ini`. Override macros that are
never overridden, and libraries without switches, do not appear in it; they
are invisible in the build configuration by definition.

![Four mechanisms side by side: exclusion starts from everything and takes
away, inclusion starts from nothing and adds, override moves a default value
and type injection carries a class name; at the bottom lib_deps as exclusion
at project level](../../images/en/library-configuration-1.svg)

## What it means for a node

What a node can do is fixed the moment the firmware is built. There is no
setting that brings back an excluded protocol or loads an undeclared library
after the fact. Anyone missing something builds their own — and then needs to
know which of the four mechanisms the library in question uses, because adding
`-D SOMETHING_ENABLE=1` does nothing if the library expects
`SOMETHING_EXCLUDE`.

The seventeen flags in this chapter are the part of the 277 `-D` macros that
ends up at a library. The other 260 — six for an Arduino core and 254 for
MeshCore itself — are in
[Compile-time configuration](../design/technical/configuration.md), together
with the finding that 53 of them are read nowhere.

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/sensors/EnvironmentSensorManager.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/sensors/EnvironmentSensorManager.cpp)
- [`src/helpers/BaseChatMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/BaseChatMesh.h)
- [`examples/simple_repeater/main.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/main.cpp)
- [`RadioLib 7.6.0 — BuildOpt.h`](https://github.com/jgromes/RadioLib/blob/7.6.0/src/BuildOpt.h)
- [`RadioLib 7.6.0 — BuildOptUser.h`](https://github.com/jgromes/RadioLib/blob/7.6.0/src/BuildOptUser.h)
- [`Adafruit_SSD1306.h`](https://github.com/adafruit/Adafruit_SSD1306/blob/master/Adafruit_SSD1306.h)
- [`arch/stm32/Adafruit_LittleFS_stm32/src/littlefs/lfs_util.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/arch/stm32/Adafruit_LittleFS_stm32/src/littlefs/lfs_util.h)
- [`Adafruit_nRF52_Arduino — Adafruit_LittleFS/src/littlefs/lfs_util.h`](https://github.com/meshcore-dev/Adafruit_nRF52_Arduino/blob/d541301/libraries/Adafruit_LittleFS/src/littlefs/lfs_util.h)
- [`oltaco/CustomLFS`](https://github.com/oltaco/CustomLFS)
