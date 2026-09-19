# The source tree

*SRC · HELPERS · EXAMPLES · VARIANTS · ASYMMETRY*

The MeshCore source tree falls into four parts: a core of eleven files, a
collection of helper classes, six applications and seventy-nine variant
directories. This chapter describes what sits where and how much of it there
is. The most interesting finding is not in the numbers themselves but in
their asymmetry: one platform family has eight shared files, another has none.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — the complete source tree under
> `src/`, `examples/` and `variants/`.

## The four parts

![Four blocks side by side. On the left the core src with eleven files, next
to it src/helpers with thirty-eight loose files and seven subdirectories, then
examples with six applications, and on the right variants with seventy-nine
directories. Arrows run from right to left: every variant picks from helpers,
every application uses the core.](../../../images/en/source-layout-1.svg)

| Location | Contents |
|---|---|
| `src/` | 5 header pairs plus `MeshCore.h`; 14 classes; 2332 lines |
| `src/helpers/` | 38 loose files, 33 classes |
| `src/helpers/bridges/` | 3 classes — `BridgeBase`, `ESPNowBridge`, `RS232Bridge` |
| `src/helpers/esp32/` | 4 classes — ESP-NOW radio, BLE, WiFi, T-Beam board |
| `src/helpers/nrf52/` | 1 class — only `SerialBLEInterface` |
| `src/helpers/stm32/` | 1 class — only `STM32Board` |
| `src/helpers/radiolib/` | 14 classes, 16 files |
| `src/helpers/sensors/` | 6 classes |
| `src/helpers/ui/` | 18 class declarations, partly vendored code |
| `examples/` | 6 applications, 25 classes |
| `variants/` | 79 directories, 77 classes |

The 119 classes in `src/` and `examples/` together form the shared tree: code
that can take part in any build. The 77 in `variants/` belong to exactly one
board. Together 196. How those 196 are divided up is in
[The class model](class-model.md).

> [!NOTE]
> **Counting method.** Counted is every line of the form `class Name { …` or
> `class Name : base { …`, with the brace on the same line. `struct`
> declarations do not count: those are data records, not parts of the design.
> A forward declaration without a body does not count either. The script
> `tools/design-overview.py --classes` reproduces the table above.

## The core

`src/` holds five pairs of a header and an implementation file —
`Dispatcher`, `Identity`, `Mesh`, `Packet`, `Utils` — plus `MeshCore.h`, which
has no `.cpp` of its own. That one extra file holds the two contracts that
cover the hardware: `MainBoard` on line 45 and `RTCClock` on line 80.

Eleven files, 2332 lines. That is the entire shared core of a firmware that is
built in 508 variants. Everything larger sits underneath it in `helpers/`, or
alongside it in `variants/`.

## Helpers, and why there are seven subdirectories

The 38 files directly under `src/helpers/` are the parts that are not
platform-bound: the access list, the storage, the control, the region table,
the packet pool. The seven subdirectories are either platform-bound, or they
belong to one subject:

| Directory | Why separate |
|---|---|
| `bridges/` | Subject: coupling two networks |
| `radiolib/` | Subject: everything that adapts or wraps RadioLib |
| `sensors/` | Subject: measurements and location |
| `ui/` | Subject: displays and buttons |
| `esp32/` | Platform: code that only compiles on ESP32 |
| `nrf52/` | Platform: the same for nRF52 |
| `stm32/` | Platform: the same for STM32 |

## The asymmetry between the platform directories

This is the point of this chapter. The three platform directories are filled
extremely unevenly, and there is a fourth family with none at all.

| Family | Platform directory | Classes in it | Build targets |
|---|---|---|---|
| ESP32 | `src/helpers/esp32/` | 4 | 270 |
| nRF52 | `src/helpers/nrf52/` | 1 | 199 |
| STM32 | `src/helpers/stm32/` | 1 | 16 |
| RP2040 | none | — | 22 |

The temptation is to read this as a measure of support: ESP32 well supported,
RP2040 neglected. That is not right. nRF52 carries 199 build targets with one
shared class in its platform directory, and those targets work. What the table
measures is how much there was to share.

ESP32 has four classes in its platform directory because ESP32 chips can do
something the others cannot: BLE *and* WiFi *and* ESP-NOW, each with its own
interface class. Those are subjects, not platform differences. nRF52 only has
BLE and therefore only `SerialBLEInterface`. RP2040 has none of the three and
is left with nothing to share; its four board classes stand alone in
`variants/`. See [Platform realisation](platform-realisation.md).

## Vendored code in `src/helpers/ui/`

Eighteen class declarations in `ui/` is more than the number of display
drivers, and that is because not everything in that directory is MeshCore's.
`OLEDDisplay.h` contains code from ThingPulse, copied in literally rather than
included as a library.

Two things give that away. First, `OLEDDisplay` appears twice in the same
file, on line 159 and line 161, behind an `#if`: one version inherits from
`Print`, the other from `Stream`. Second, line 50 holds a declaration of
`String` — a forward reference that only makes sense inside the original
codebase.

> [!NOTE]
> Neither is MeshCore design. They are in the count because they are
> declarations in the source tree, but anyone reading the class model should
> know that three of the eighteen come from adopted code. Where MeshCore does
> include libraries as libraries is described in
> [Libraries in MeshCore](../../libraries/introduction.md).

## `examples/` is not a directory of examples

The name is misleading. `examples/` holds the six applications MeshCore can
be — companion radio, repeater, room server, sensor, terminal chat and KISS
modem — and every build compiles exactly one of them. They are not
demonstrations alongside the product; they *are* the product.

Twenty-five classes, of which a large share are display tasks (`UITask`
appears six times, in six applications) and five are literally called
`MyMesh`. Which role each application implements is described in
[Roles](../logical/roles.md).

## `variants/`: 79 directories, 77 classes

Every directory under `variants/` describes one board: which pins sit where,
which radio chip is on it, which display hangs off it. Two directories hold no
class — those supply only a `platformio.ini` and a `target.h`.

The 77 classes in them are strikingly uniform: 65 board classes, 7 sensor
managers, 3 displays and 2 entropy sources. They all implement a contract laid
down in the shared tree. That makes them together good for 39 % of all classes
in the firmware, while there is hardly any design in them — it is nearly all
pin assignment.

## Sources

- [MeshCore `03b6ef4` — `src/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/src)
- [MeshCore `03b6ef4` — `src/helpers/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/src/helpers)
- [MeshCore `03b6ef4` — `src/helpers/ui/OLEDDisplay.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/OLEDDisplay.h)
- [MeshCore `03b6ef4` — `examples/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/examples)
- [MeshCore `03b6ef4` — `variants/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/variants)

Translated from Dutch by Anthropic Claude
