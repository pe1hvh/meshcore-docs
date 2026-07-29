# Utility libraries

*BASE64 · CRC32 · SEVENTY-SIX DECLARATIONS · ONE USE*

Two small libraries with a striking ratio between how often they are declared
and how often they are used. One sits in seventy-six of the eighty
`platformio.ini` files and occurs in exactly one source file; the other has a
job you would not expect.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `src/helpers/BaseChatMesh.cpp`, `src/helpers/ui/GxEPDDisplay.h`,
> `src/helpers/ui/E213Display.h`, `src/helpers/ui/E290Display.h` and the
> seventy-nine `variants/*/platformio.ini`.

## How MeshCore calls this group

Unlike the sensors and the displays, these two do not sit behind an
abstraction. They are called where they are needed, behind an `#ifdef` on a
feature flag:

`src/helpers/BaseChatMesh.cpp` r.865-873

```cpp
#ifdef MAX_GROUP_CHANNELS
#include <base64.hpp>

ChannelDetails* BaseChatMesh::addChannel(const char* name, const char* psk_base64) {
  if (num_channels < MAX_GROUP_CHANNELS) {
    auto dest = &channels[num_channels];

    memset(dest->channel.secret, 0, sizeof(dest->channel.secret));
    int len = decode_base64((unsigned char *) psk_base64, strlen(psk_base64), dest->channel.secret);
```

## densaugeo/base64

Base64 encodes arbitrary bytes as readable text — four characters per three
bytes, from an alphabet of sixty-four. The library by densaugeo is a minimal
Arduino implementation: encoding, decoding, and working out the required
buffer length, without dynamic memory.

This library is declared in seventy-six of the eighty `platformio.ini` files —
more often than any other. In the source it is used in one place, in the code
above: decoding a channel key supplied as text. A user entering `#zwolle` with
a PSK gives that key in base64; this line turns it back into bytes.

The ratio of seventy-six declarations to one use is not a mistake, but it is
typical of how the variant files came about: a variant is made by copying an
existing one, and the `lib_deps` comes along.

## bakercp/CRC32

CRC32 computes a thirty-two-bit check value over a sequence of bytes. The
classic use is error detection during transmission or storage. MeshCore does
not use it for that.

All three places where the library occurs are e-ink display drivers:

- `src/helpers/ui/GxEPDDisplay.h` r.15
- `src/helpers/ui/E213Display.h` r.8
- `src/helpers/ui/E290Display.h` r.8

Each of the three keeps a `CRC32 display_crc;`. Refreshing an e-ink panel
takes a second or more, is visible as flicker and wears the panel out. By
keeping a check value over the content to be drawn, the driver can establish
that the image has not changed and skip the refresh.

Fifteen variants declare the library — the e-ink variants and a number derived
from them.

## Overview

| Library | Version | `.ini` | Source files | Used for |
|---|---|---|---|---|
| `densaugeo/base64` | `~1.4.0` | 76 | 1 | decoding a channel PSK |
| `bakercp/CRC32` | `^2.0.0` | 15 | 3 | skipping an unnecessary e-ink refresh |

## Sources

- [`src/helpers/BaseChatMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/BaseChatMesh.cpp)
- [`src/helpers/ui/GxEPDDisplay.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/GxEPDDisplay.h)
- [`src/helpers/ui/E213Display.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/E213Display.h)
- [`src/helpers/ui/E290Display.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/E290Display.h)
- [densaugeo/base64_arduino](https://github.com/densaugeo/base64_arduino)
- [bakercp/CRC32](https://github.com/bakercp/CRC32)

Translated from Dutch by Anthropic Claude
