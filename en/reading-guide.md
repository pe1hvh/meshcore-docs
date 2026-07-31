# How to read this

*SECTIONS · ASSUMED KNOWLEDGE · WHAT MAKES THIS DIFFERENT*

MeshCore turns inexpensive LoRa radios into a network of their own. Messages
hop from node to node until they arrive — no internet, no cell towers, no
subscription. **DOMCA** — Dutch Open MeshCore Activity — exists to make that
knowledge accessible. This page says where to start and what each section
asks of you.

## What is here

The documentation holds 94 chapters in Dutch and the same 94 in English,
with 73 diagrams per language. The chapter count is the number of `.md` files
per language tree excluding the `README.md` indexes; the diagram count is the
number of SVGs a chapter references, not the number of files in `images/`.

The full index is in the [table of contents](README.md).

## What each section assumes

The chapters differ widely in the background they assume. This table states
per section what you need to bring, so you know what level of detail to
expect. Each section name links to its first chapter.

| Section | What you find there | Assumed knowledge |
|---|---|---|
| [Usage](usage/what-is-meshcore.md) | What MeshCore is, getting a node running, hardware, regulations, privacy | No programming knowledge required |
| [Technical](technical/layer-model.md) | Protocol, packet layout byte by byte, encryption, routing, repeaters, room server | A basic grasp of networking and hexadecimal notation helps; programming is not needed |
| [Platform](platform/platforms.md) | The four platform families and choosing between them | None beyond a general idea of microcontrollers |
| [Hardware](hardware/introduction.md) | Radio, antenna, link budget, BLE, WiFi, USB, I²C, SPI, display, GPS, buttons | Basic electronics recommended; a few chapters show C++ fragments |
| [Libraries](libraries/introduction.md) | The fifty-two external libraries that go into the firmware | Familiarity with PlatformIO build configurations recommended |
| [Design (node) → logical](design/logical/roles.md) | Roles, components, contracts, information model, variability, design decisions | Basic knowledge of classes and interfaces recommended; the text stays away from source code |
| [Design (node) → technical](design/technical/source-layout.md) | Source tree, class model, platform and radio realisation, build system, macros, traceability | C++ classes, inheritance and PlatformIO build configurations |
| [Design (companion) → logical](companion/logical/responsibilities.md) | Who keeps what, request-response and push, version negotiation, information model | A basic grasp of traffic between two systems; a few C++ fragments |
| [Design (companion) → technical](companion/technical/transports.md) | The three transports, the frame format, all fifty-eight commands, the layers of a client | Programming experience; familiarity with binary protocols helps |
| [Reference](reference/terminology.md) | Terminology, references, links | None. Meant for looking things up, not for reading through |
| [Project](project/about-domca.md) | About DOMCA, how the repository is organised | None |

If you hit a term you do not know, it is in
[Terminology](reference/terminology.md).

## What makes this different

The usage chapters do what you would expect. The technical chapters go a step
further, deliberately so:

- **Byte by byte.** Packets are written out with real values, not `XX XX`.
  You see where the header ends and the payload begins.
- **Verified against the source.** Technical claims name the firmware version
  and commit they were checked against, pointing at the relevant file in
  `meshcore-dev/MeshCore`.
- **Reproducible.** The examples in
  [Regions and Scopes](technical/regions-and-scopes.md) can be recomputed
  with [`tools/example-calculation.py`](../tools/example-calculation.py). If
  the text is wrong, you can see it for yourself.
- **Including what does not work.** Stub implementations, firmware `TODO`s
  and undocumented commands are described as such.

Translated from Dutch by Anthropic Claude
