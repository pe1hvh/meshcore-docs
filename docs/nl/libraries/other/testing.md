# Testlibraries

*GOOGLETEST · ENV:NATIVE · MOCKS · ÉÉN TESTBESTAND*

MeshCore heeft één testomgeving, één testbestand en één geteste functie. Dit
hoofdstuk beschrijft hoe die is opgezet en hoe klein hij is — als cijfer, niet
als oordeel.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `platformio.ini` r.158-168, `test/test_utils/test_tohex.cpp` en
> `test/mocks/`.

## Hoe MeshCore deze groep aanroept

De testomgeving staat los van alle andere. Hij erft niet van
`[arduino_base]`, gebruikt geen Arduino-framework en compileert bijna niets
van de firmware mee:

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

Vier dingen vallen daaraan op. `platform = native` betekent: compileren voor
de computer waar je op werkt, niet voor een microcontroller. Het
`build_src_filter` sluit eerst alles uit en laat daarna één bestand toe,
`src/Utils.cpp`. Het includepad zet `test/mocks` vóór de echte libraries.
En googletest is exact vastgepind op 1.17.0.

## google/googletest

googletest is het testraamwerk van Google voor C++. Een test schrijf je als
een `TEST(groep, naam)`-blok met daarin controles als `EXPECT_STREQ` en
`EXPECT_EQ`; het raamwerk verzamelt ze, draait ze en rapporteert wat er
faalde. Het is geen Arduino-library — het registrypakket bevat geen
`library.properties` of `library.json`, en het draait hier dan ook op een
gewone computer.

Het enige testbestand is `test/test_utils/test_tohex.cpp`:

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

Geteste functie: `Utils::toHex`, die bytes omzet naar een hexadecimale
string.

## De mocks

`src/Utils.cpp` includeert `<AES.h>` en `<SHA256.h>` uit `rweather/Crypto`.
Die library is een Arduino-library en compileert niet zomaar op een gewone
computer. In `test/mocks/` staan daarom vervangers: `AES.h`, `SHA256.h` en
`Stream.h`. Het `-I test/mocks` in de bouwvlaggen zorgt dat de compiler die
eerder vindt dan de echte.

Het gevolg is dat de testbuild de cryptografische code niet test — hij test
`toHex` in een omgeving waarin crypto en `Stream` leeg zijn.

## Wat de testdekking is

In cijfers, bij commit `03b6ef4`:

| | Aantal |
|---|---|
| Testomgevingen | 1 (`[env:native]`) |
| Testbestanden | 1 |
| Meegecompileerde firmwarebestanden | 1 (`src/Utils.cpp`) |
| Geteste functies | 1 (`Utils::toHex`) |
| Mocks | 3 (`AES.h`, `SHA256.h`, `Stream.h`) |

Ter vergelijking: de repo telt 590 bronbestanden met de extensie `.h`,
`.hpp`, `.c`, `.cpp` of `.ino`.

## Overzicht

| Library | Versie | Omgeving | Route |
|---|---|---|---|
| `google/googletest` | `1.17.0` | `[env:native]` | registry, exact vastgepind |

## Bronnen

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`test/test_utils/test_tohex.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/test/test_utils/test_tohex.cpp)
- [`test/mocks/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/test/mocks)
- [`src/Utils.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Utils.cpp)
- [google/googletest](https://github.com/google/googletest)
