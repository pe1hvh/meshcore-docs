# Ontwerp van MeshCore

*LOGISCH ONTWERP · TECHNISCH ONTWERP · AFBAKENING · LEESWIJZER*

Deze sectie beschrijft hoe MeshCore in elkaar zit. Niet wat er over de lucht
gaat — dat staat in [Techniek](../techniek/layer-model.md) — maar hoe de
firmware is opgedeeld, welke onderdelen welke verantwoordelijkheid dragen, en
hoe uit één codebase 508 verschillende builds ontstaan. De sectie valt uiteen
in een logisch en een technisch ontwerp.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — de volledige broncodestructuur, de
> root `platformio.ini` en alle 79 `variants/*/platformio.ini`.

## Twee lagen

Een logisch ontwerp beschrijft *wat* een systeem is. Welke onderdelen bestaan
er, waar is elk onderdeel verantwoordelijk voor, welke afspraken gelden tussen
die onderdelen, en welke gegevens gaan er tussen ze heen en weer. Het doet dat
zonder naar de implementatie te wijzen. Je kunt het lezen zonder C++ te kennen
en zonder te weten dat er een `Dispatcher.cpp` bestaat.

Een technisch ontwerp beschrijft *hoe* dat gerealiseerd is. Welke klasse welke
rol vervult, welke bestanden bij elkaar horen, hoe de vier platformfamilies
dezelfde abstractie op vier manieren implementeren, en hoe het buildsysteem de
juiste combinatie bij elkaar zoekt. Daar staan bestandsnamen en regelnummers
in.

De scheiding is niet cosmetisch. Het logisch ontwerp van MeshCore is
opmerkelijk stabiel: de rollen, de lagen en de contracten tussen die lagen
liggen al lang vast. Het technisch ontwerp beweegt daaronder wel degelijk — er
komen platformen bij, drivers veranderen, buildtargets verschijnen en
verdwijnen tussen twee commits. Wie de twee door elkaar leest, houdt een
document over dat om de maand achterhaald is.

![Het logisch ontwerp beschrijft rollen, componenten, contracten en gegevens;
het technisch ontwerp beschrijft klassen, platformrealisatie en het
buildsysteem. Pijlen lopen van logisch naar technisch: elk logisch onderdeel
heeft een technische tegenhanger.](../../images/nl/design-layers-1.svg)

## Wat hier niet staat

Deze sectie herhaalt geen inhoud uit andere secties. Waar het onderwerp raakt,
staat een verwijzing.

| Onderwerp | Staat in |
|---|---|
| Protocollagen en gedrag over de lucht | [Het Lagenmodel](../techniek/layer-model.md) |
| Byte-indeling van pakketten | [Pakketstructuur](../techniek/packet-structure.md) |
| Keuze tussen de vier platformfamilies | [De vier platformfamilies](../platform/platform-families.md) |
| Fysieke bussen en verbindingen | [Hardware van een node](../hardware/introduction.md) |
| Externe libraries en hun configuratie | [Libraries in MeshCore](../libraries/introduction.md) |

Kort gezegd: `techniek/` beschrijft het protocol, `hardware/` de fysieke node,
`libraries/` de code van derden, en `ontwerp/` de structuur van de code van
MeshCore zelf.

## Leeswijzer

**Logisch ontwerp**

- [Rollen](logisch/roles.md) — de zes applicaties die MeshCore kan zijn
- [Componenten](logisch/components.md) — wat er is en waar het over gaat
- [Contracten](logisch/interfaces.md) — de afspraken tussen componenten
- [Informatiemodel](logisch/information-model.md) — de gegevens en hun relaties
- [Variabiliteit](logisch/variability.md) — hoe één codebase 508 builds wordt
- [Ontwerpbeslissingen](logisch/decisions.md) — de keuzes en wat ze kosten

**Technisch ontwerp**

- [De broncodestructuur](technisch/source-layout.md) — wat waar staat, en de
  asymmetrie
- [Het klassenmodel](technisch/class-model.md) — contract, implementatie,
  zelfstandig
- [Platformrealisatie](technisch/platform-realisation.md) — vier families, één
  abstractie
- [Radiorealisatie](technisch/radio-realisation.md) — waar de radiokeuze valt
- [Het buildsysteem](technisch/build-system.md) — hoe 508 targets ontstaan
- [Compile-time configuratie](technisch/configuration.md) — 277 macro's en hun
  eigenaar
- [Traceerbaarheid](technisch/traceability.md) — logisch onderdeel naar
  bestand en regel

## Narekenen

Elk getal in deze sectie komt uit `tools/design-overview.py`. Dat script leest
een MeshCore-checkout en bepaalt per buildtarget welke applicatie wordt
gecompileerd, tot welke platformfamilie het target hoort en welke onderdelen
zijn ingeschakeld:

```bash
python3 tools/design-overview.py /pad/naar/MeshCore
```

Het script telt nooit op de naam van een `[env:...]`-sectie. Waarom dat een
val is, staat in [Variabiliteit](logisch/variability.md).

## Bronnen

- [MeshCore `03b6ef4` — `src/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/src)
- [MeshCore `03b6ef4` — `examples/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/examples)
- [MeshCore `03b6ef4` — `platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
