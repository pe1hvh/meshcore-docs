# Hulplibraries

*BASE64 · CRC32 · ZESENZEVENTIG DECLARATIES · ÉÉN GEBRUIK*

Twee kleine libraries met een opvallende verhouding tussen hoe vaak ze
gedeclareerd worden en hoe vaak ze gebruikt worden. De ene staat in
zesenzeventig van de tachtig `platformio.ini`-bestanden en komt in precies
één bronbestand voor; de andere heeft een taak die je niet verwacht.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `src/helpers/BaseChatMesh.cpp`, `src/helpers/ui/GxEPDDisplay.h`,
> `src/helpers/ui/E213Display.h`, `src/helpers/ui/E290Display.h` en de
> negenenzeventig `variants/*/platformio.ini`.

## Hoe MeshCore deze groep aanroept

Anders dan de sensoren en de schermen zitten deze twee niet achter een
abstractie. Ze worden aangeroepen waar ze nodig zijn, achter een `#ifdef` op
een functievlag:

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

Base64 codeert willekeurige bytes als leesbare tekst — vier tekens per drie
bytes, uit een alfabet van vierenzestig. De library van densaugeo is een
minimale implementatie voor Arduino: coderen, decoderen, en het uitrekenen
van de benodigde bufferlengte, zonder dynamisch geheugen.

Deze library staat in zesenzeventig van de tachtig `platformio.ini`-bestanden
gedeclareerd — vaker dan welke andere ook. In de broncode wordt hij op één
plaats gebruikt, in de code hierboven: het decoderen van een kanaalsleutel
die als tekst wordt aangeleverd. Een gebruiker die `#zwolle` met een PSK
invoert, geeft die sleutel in base64 op; deze regel maakt er weer bytes van.

De verhouding tussen zesenzeventig declaraties en één gebruik is geen fout,
maar wel typerend voor hoe de variantbestanden zijn ontstaan: een variant
wordt gemaakt door een bestaande te kopiëren, en de `lib_deps` gaat mee.

## bakercp/CRC32

CRC32 rekent een controlegetal van tweeëndertig bits over een reeks bytes uit.
Het klassieke gebruik is foutdetectie bij overdracht of opslag. MeshCore
gebruikt hem daar niet voor.

Alle drie de plaatsen waar de library voorkomt zijn e-inkschermdrivers:

- `src/helpers/ui/GxEPDDisplay.h` r.15
- `src/helpers/ui/E213Display.h` r.8
- `src/helpers/ui/E290Display.h` r.8

Elk van die drie houdt een `CRC32 display_crc;` bij. Een e-inkscherm
verversen duurt een seconde of meer, is zichtbaar als geflikker en slijt het
paneel. Door een controlegetal over de te tekenen inhoud bij te houden, kan
de driver vaststellen dat het beeld niet veranderd is en de verversing
overslaan.

Vijftien varianten declareren de library — de e-inkvarianten en een aantal
die ervan afgeleid zijn.

## Overzicht

| Library | Versie | `.ini` | Bronbestanden | Gebruikt voor |
|---|---|---|---|---|
| `densaugeo/base64` | `~1.4.0` | 76 | 1 | decoderen van een kanaal-PSK |
| `bakercp/CRC32` | `^2.0.0` | 15 | 3 | overslaan van onnodige e-inkverversing |

## Bronnen

- [`src/helpers/BaseChatMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/BaseChatMesh.cpp)
- [`src/helpers/ui/GxEPDDisplay.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/GxEPDDisplay.h)
- [`src/helpers/ui/E213Display.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/E213Display.h)
- [`src/helpers/ui/E290Display.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/E290Display.h)
- [densaugeo/base64_arduino](https://github.com/densaugeo/base64_arduino)
- [bakercp/CRC32](https://github.com/bakercp/CRC32)
