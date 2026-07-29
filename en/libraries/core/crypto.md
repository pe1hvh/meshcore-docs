# Crypto: rweather and ed25519

*ED25519 · SHA256 · AES · TWO IMPLEMENTATIONS*

MeshCore carries two Ed25519 implementations in the build. One comes from
`rweather/Crypto`, the other is vendored into `lib/ed25519`. Both are used, in
the same file, for different operations — and the reason for that is written
in the source as a comment.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `platformio.ini`, `src/Identity.cpp`, `src/Packet.cpp`, `src/Utils.cpp`,
> `src/helpers/RegionMap.cpp`, `src/helpers/TransportKeyStore.cpp`,
> `lib/ed25519/` and `test/mocks/`.

> [!NOTE]
> This chapter is about which library supplies which function and why there
> are two. How MeshCore's encryption works is described in
> [`../../technical/key-encryption.md`](../../technical/key-encryption.md).

## What it does

`rweather/Crypto` by Rhys Weatherley is a collection of cryptographic
algorithms for Arduino: AES in several key lengths and modes, the SHA family,
ChaCha, Poly1305, Curve25519 and Ed25519. The algorithms are optimised for
8-bit microcontrollers and work with a fixed, statically allocated state.
Documentation and background live at
[rweather/arduinolibs](https://github.com/rweather/arduinolibs).

`lib/ed25519` is something else: a compact C implementation of Ed25519 only,
present as source inside the MeshCore repo. PlatformIO compiles everything in
`lib/` automatically, so that code enters every build without a `lib_deps`
line.

## How MeshCore pulls it in

`platformio.ini` r.23

```text
  rweather/Crypto @ ^0.4.0
```

The line sits in `[arduino_base]` and therefore applies to all 507 build
targets. `lib/ed25519` has no line: that directory is picked up
automatically.

## How MeshCore uses it

`src/Identity.cpp` opens with both implementations side by side:

`src/Identity.cpp` r.3-5

```cpp
#define ED25519_NO_SEED  1
#include <ed_25519.h>
#include <Ed25519.h>
```

`ed_25519.h` is the vendored version, `Ed25519.h` the one from
`rweather/Crypto`. When verifying a signature, the first is deliberately
skipped:

`src/Identity.cpp` r.17-23

```cpp
bool Identity::verify(const uint8_t* sig, const uint8_t* message, int msg_len) const {
#if 0
  // NOTE:  memory corruption bug was found in this function!!
  return ed25519_verify(sig, message, msg_len, pub_key);
#else
  return Ed25519::verify(sig, this->pub_key, message, msg_len);
#endif
}
```

So verification goes through `rweather/Crypto`. Every other Ed25519 operation
*does* go through the vendored version: creating a key pair (r.48), deriving a
public key from a private one (r.53 and r.131), signing (r.136) and the key
exchange (r.79-82 and r.140).

`src/Identity.cpp` r.135-141

```cpp
void LocalIdentity::sign(uint8_t* sig, const uint8_t* message, int msg_len) const {
  ed25519_sign(sig, message, msg_len, pub_key, prv_key);
}

void LocalIdentity::calcSharedSecret(uint8_t* secret, const uint8_t* other_pub_key) const {
  ed25519_key_exchange(secret, other_pub_key, prv_key);
}
```

Outside `Identity.cpp`, `rweather/Crypto` supplies two other algorithms.
`SHA256` is included in `src/Packet.cpp` r.3, `src/helpers/RegionMap.cpp` r.3
and `src/helpers/TransportKeyStore.cpp` r.2; `AES` and `SHA256` together in
`src/Utils.cpp`:

`src/Utils.cpp` r.1-3

```cpp
#include "Utils.h"
#include <AES.h>
#include <SHA256.h>
```

For the test build the library is replaced. `test/mocks/` holds its own
`AES.h` and `SHA256.h`; `[env:native]` puts that directory on the include path
(`platformio.ini` r.162) so the tests run without the real implementation.

![The two Ed25519 paths in MeshCore: signing, key pairs, derived public keys
and the key exchange run through the vendored implementation in lib/ed25519,
verification runs through Ed25519 from rweather/Crypto, and the disabled
ed25519_verify path is drawn dashed](../../../images/en/crypto-1.svg)

## What it means for a node

Every node carries both implementations. That costs flash space, and it means
that a signature this node produces is made with different code from the code
it checks an incoming signature with. Both follow the same standard, so that
works — but anyone reading MeshCore's crypto code has to know that `Ed25519::`
and `ed25519_` are different libraries.

The note next to `verify` is not historical noise: the comment states that
memory corruption was found in `ed25519_verify`. That function has been behind
`#if 0` ever since.

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/Identity.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Identity.cpp)
- [`src/Utils.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Utils.cpp)
- [`src/Packet.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Packet.cpp)
- [`src/helpers/TransportKeyStore.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/TransportKeyStore.cpp)
- [`lib/ed25519/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/lib/ed25519)
- [`test/mocks/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/test/mocks)
- [rweather/arduinolibs](https://github.com/rweather/arduinolibs)

Translated from Dutch by Anthropic Claude
