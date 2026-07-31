# Crypto: rweather en ed25519

*ED25519 · SHA256 · AES · TWEE IMPLEMENTATIES*

MeshCore heeft twee Ed25519-implementaties in de build zitten. De ene komt
uit `rweather/Crypto`, de andere staat meegeleverd in `lib/ed25519`. Ze worden
allebei gebruikt, in hetzelfde bestand, voor verschillende bewerkingen — en
de reden daarvoor staat als commentaar in de broncode.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini`, `src/Identity.cpp`, `src/Packet.cpp`, `src/Utils.cpp`,
> `src/helpers/RegionMap.cpp`, `src/helpers/TransportKeyStore.cpp`,
> `lib/ed25519/` en `test/mocks/`.

> [!NOTE]
> Dit hoofdstuk gaat over welke library welke functie levert en waarom er
> twee zijn. Hoe de versleuteling van MeshCore werkt, staat in
> [`../../techniek/key-encryption.md`](../../techniek/key-encryption.md).

## Wat het doet

`rweather/Crypto` van Rhys Weatherley is een verzameling
cryptografiealgoritmen voor Arduino: AES in verschillende sleutellengtes en
modi, SHA-familie, ChaCha, Poly1305, Curve25519 en Ed25519. De algoritmen
zijn geoptimaliseerd voor 8-bit microcontrollers en werken met een vaste,
statisch toegewezen state. Documentatie en achtergrond staan in
[rweather/arduinolibs](https://github.com/rweather/arduinolibs).

`lib/ed25519` is iets anders: een compacte C-implementatie van alleen
Ed25519, die als broncode in de MeshCore-repo zelf staat. PlatformIO
compileert alles in `lib/` automatisch mee, dus die code komt zonder
`lib_deps`-regel in elke build terecht.

## Hoe MeshCore hem binnenhaalt

`platformio.ini` r.23

```text
  rweather/Crypto @ ^0.4.0
```

De regel staat in `[arduino_base]` en geldt dus voor alle 507 build-targets.
`lib/ed25519` heeft geen regel: die map wordt automatisch meegenomen.

## Hoe MeshCore hem gebruikt

`src/Identity.cpp` begint met beide implementaties naast elkaar:

`src/Identity.cpp` r.3-5

```cpp
#define ED25519_NO_SEED  1
#include <ed_25519.h>
#include <Ed25519.h>
```

`ed_25519.h` is de meegeleverde versie, `Ed25519.h` die uit `rweather/Crypto`.
Bij het verifiëren van een handtekening wordt de eerste bewust overgeslagen:

`src/Identity.cpp` r.17-24

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

Verifiëren gaat dus via `rweather/Crypto`. Alle andere Ed25519-bewerkingen
gaan wél via de meegeleverde versie: het aanmaken van een sleutelpaar (r.48),
het afleiden van een publieke sleutel uit een private (r.53 en r.131), het
ondertekenen (r.136) en de key exchange (r.79-82 en r.140).

`src/Identity.cpp` r.135-141

```cpp
void LocalIdentity::sign(uint8_t* sig, const uint8_t* message, int msg_len) const {
  ed25519_sign(sig, message, msg_len, pub_key, prv_key);
}

void LocalIdentity::calcSharedSecret(uint8_t* secret, const uint8_t* other_pub_key) const {
  ed25519_key_exchange(secret, other_pub_key, prv_key);
}
```

Buiten `Identity.cpp` levert `rweather/Crypto` twee andere algoritmen.
`SHA256` wordt geïncludeerd in `src/Packet.cpp` r.3,
`src/helpers/RegionMap.cpp` r.3 en `src/helpers/TransportKeyStore.cpp` r.2;
`AES` en `SHA256` samen in `src/Utils.cpp`:

`src/Utils.cpp` r.1-3

```cpp
#include "Utils.h"
#include <AES.h>
#include <SHA256.h>
```

Voor de testbuild wordt de library vervangen. In `test/mocks/` staan een
eigen `AES.h` en `SHA256.h`; `[env:native]` zet die map op het includepad
(`platformio.ini` r.162), zodat de tests draaien zonder de echte
implementatie.

![De twee Ed25519-paden in MeshCore: ondertekenen, sleutelparen, afgeleide
publieke sleutels en key exchange lopen via de meegeleverde implementatie in
lib/ed25519, verifiëren loopt via Ed25519 uit rweather/Crypto, en het
uitgeschakelde pad van ed25519_verify is gestippeld
weergegeven](../../../images/nl/crypto-1.svg)

## Wat het voor een node betekent

Elke node draagt beide implementaties mee. Dat kost flashruimte, en het
betekent dat een handtekening die deze node zet, met andere code wordt
gemaakt dan waarmee hij een binnenkomende handtekening controleert. Beide
volgen dezelfde standaard, dus dat werkt — maar wie de crypto-code van
MeshCore leest, moet weten dat `Ed25519::` en `ed25519_` verschillende
libraries zijn.

De opmerking bij `verify` is geen historische ruis: de commentaarregel meldt
dat in `ed25519_verify` geheugencorruptie is gevonden. Die functie staat
sindsdien achter `#if 0`.

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/Identity.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Identity.cpp)
- [`src/Utils.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Utils.cpp)
- [`src/Packet.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Packet.cpp)
- [`src/helpers/TransportKeyStore.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/TransportKeyStore.cpp)
- [`lib/ed25519/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/lib/ed25519)
- [`test/mocks/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/test/mocks)
- [rweather/arduinolibs](https://github.com/rweather/arduinolibs)
