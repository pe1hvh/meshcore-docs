# Test libraries

*GOOGLETEST · ENV:NATIVE · MOCKS · ONE TEST FILE*

MeshCore has one test environment, one test file and one tested function. This
chapter describes how it is set up and how small it is — as a figure, not as a
judgement.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini` r.158-168, `test/test_utils/test_tohex.cpp` and
> `test/mocks/`.

## How MeshCore calls this group

The test environment stands apart from all the others. It does not inherit
from `[arduino_base]`, uses no Arduino framework and compiles almost none of
the firmware:

`platformio.ini` r.158-168

```text
[env:native]
platform = native
build_flags = -std=c++17
  -I src
  -I test/mocks
test_build_src = yes
build_src_filter =
  -<*>
  +<../src/Utils.cpp>
lib_deps =
  google/googletest @ 1.17.0
```

Four things stand out. `platform = native` means: compile for the machine you
are working on, not for a microcontroller. The `build_src_filter` first
excludes everything and then admits one file, `src/Utils.cpp`. The include
path puts `test/mocks` ahead of the real libraries. And googletest is pinned
exactly to 1.17.0.

## google/googletest

googletest is Google's C++ testing framework. You write a test as a
`TEST(group, name)` block containing checks such as `EXPECT_STREQ` and
`EXPECT_EQ`; the framework collects them, runs them and reports what failed.
It is not an Arduino library — the registry package contains no
`library.properties` or `library.json`, and it runs here on an ordinary
computer.

The only test file is `test/test_utils/test_tohex.cpp`:

`test/test_utils/test_tohex.cpp` r.1-15

```cpp
#include <gtest/gtest.h>
#include "Utils.h"

using namespace mesh;

#define HEX_BUFFER_SIZE(input) (sizeof(input) * 2 + 1)

TEST(UtilsToHex, ConvertSingleByte) {
    uint8_t input[] = {0xAB};
    char output[HEX_BUFFER_SIZE(input)];

    Utils::toHex(output, input, sizeof(input));

    EXPECT_STREQ("AB", output);
}
```

Function under test: `Utils::toHex`, which converts bytes to a hexadecimal
string.

## The mocks

`src/Utils.cpp` includes `<AES.h>` and `<SHA256.h>` from `rweather/Crypto`.
That library is an Arduino library and does not simply compile on an ordinary
computer. `test/mocks/` therefore holds replacements: `AES.h`, `SHA256.h` and
`Stream.h`. The `-I test/mocks` in the build flags makes the compiler find
those before the real ones.

The consequence is that the test build does not test the cryptographic code —
it tests `toHex` in an environment where crypto and `Stream` are empty.

## What the test coverage is

In figures, at commit `03b6ef4`:

| | Count |
|---|---|
| Test environments | 1 (`[env:native]`) |
| Test files | 1 |
| Firmware files compiled in | 1 (`src/Utils.cpp`) |
| Tested functions | 1 (`Utils::toHex`) |
| Mocks | 3 (`AES.h`, `SHA256.h`, `Stream.h`) |

For comparison: the repo holds 590 source files with extension `.h`, `.hpp`,
`.c`, `.cpp` or `.ino`.

## Overview

| Library | Version | Environment | Route |
|---|---|---|---|
| `google/googletest` | `1.17.0` | `[env:native]` | registry, pinned exactly |

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`test/test_utils/test_tohex.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/test/test_utils/test_tohex.cpp)
- [`test/mocks/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/test/mocks)
- [`src/Utils.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Utils.cpp)
- [google/googletest](https://github.com/google/googletest)

Translated from Dutch by Anthropic Claude
