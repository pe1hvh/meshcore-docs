# CHANGELOG

All notable changes to meshcore-docs are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).

---

## [2026-08-01] Correct Dutch radio parameters to SF7 / CR5

### Fixed

- `nl/gebruik/getting-started.md`, `en/usage/getting-started.md` — the step 3
  configuration table gave the pre-switch Dutch radio profile: preset
  `EU/UK (narrow)`, `SF8`, `CR 4/8`. The MeshCore app now carries a
  **Netherlands** preset of its own (869.618 MHz / BW 62.5 kHz / SF7 / CR5) and
  the Dutch network moved to SF7 / CR5 in May 2026. A node left on SF8 no longer
  hears the mesh, so the table actively misconfigured new readers. Preset name,
  spreading factor and coding rate corrected in both languages; frequency and
  bandwidth were already right. A note added for readers whose app does not show
  the preset (fall back to Custom) and naming the old SF8 / CR8 values, so those
  coming from older guides recognise what changed.
- `nl/gebruik/regulations.md`, `en/usage/regulations.md` — the preset in the
  practical-configuration block read `Nederland (EU/UK Narrow)` and
  `Netherlands (EU/UK Narrow)`; both now read `Netherlands`. The app UI is
  English and `Netherlands` is a preset in its own right, so the parenthetical
  named a different preset than the one the reader has to select. The SF7 /
  CR 4/5 figures in that block were already correct — it was
  `getting-started.md` that contradicted them. The VERON source row further
  down still quotes `EU/UK Narrow`, because that is what the source says.

### Added

- `nl/hardware/radio/sx1262.md`, `en/hardware/radio/sx1262.md`,
  `nl/hardware/radio/link-budget.md`, `en/hardware/radio/link-budget.md` — note
  that `LORA_SF=8` is the compile-time default from the root `platformio.ini`
  and not the setting the Dutch network runs on, linking to *Aan de Slag* /
  *Getting Started*. The flag values themselves are unchanged: they describe the
  build correctly, but stood one chapter away from a table naming SF7 as the
  network setting. In `link-budget.md` the note also gives the figures at SF7
  (sensitivity −127.5 dBm, budget 2.5 dB lower); the worked example still runs
  on the firmware default SF8, as `tools/link-budget.py` does.

---

## [2026-07-31] Add Companion section, reading guide, terminology overhaul

### Added

- **`nl/reading-guide.md` and `en/reading-guide.md` — the reading guide as a
  chapter of its own**, at the top of each language tree rather than inside a
  section directory, so that it shares its link base with the index beside it
  and the two cannot drift apart. It holds what the root `README.md` used to
  carry twice: the introduction, the chapter and diagram counts, the section
  table stating the background each section assumes, and the four properties
  that set this documentation apart. The section names in that table now link
  to the first chapter of each section instead of to a directory; directory
  links render on GitHub but have no generated page on the site, which would
  have turned them into dead links the moment the table became a published
  chapter.
- **New `companion/` section: the interface between a companion app and a
  node.** Eight chapters per language — `nl/companion/introduction.md`,
  `nl/companion/logisch/responsibilities.md`,
  `nl/companion/logisch/interaction-model.md`,
  `nl/companion/logisch/information-model.md`,
  `nl/companion/technisch/transports.md`,
  `nl/companion/technisch/frame-format.md`,
  `nl/companion/technisch/command-groups.md`,
  `nl/companion/technisch/client-architecture.md`, with
  `en/companion/introduction.md` and the same seven under
  `en/companion/logical/` and `en/companion/technical/`. The official
  MeshCore Companion App is closed source, so no design can be read out of an
  app repository; what is public is the contract every app has to fit, and
  that is what these chapters describe. Written to be normative — how to
  build your own client — with an explicit disclaimer in the introduction and
  repeated in the two chapters where it matters most, because there is no
  official specification to defer to.
- **Six diagrams per language**, `images/nl/companion-*.svg` and
  `images/en/companion-*.svg`: `companion-context-1`,
  `companion-responsibilities-1`, `companion-interaction-1`,
  `companion-information-model-1`, `companion-transports-1`,
  `companion-architecture-1`. All six carry a `companion-` prefix rather than
  the chapter slug, because `images/` is flat and `information-model-1.svg`
  was already taken by `ontwerp/logisch/information-model.md`.
- **`tools/companion-opcodes.py` and `tools/companion-opcodes-snapshot.json`.**
  Reads the opcode table out of `examples/companion_radio/MyMesh.cpp`,
  compares coverage against `meshcore_py`, `meshcore.js` and the official
  `docs/companion_protocol.md`, and resolves the companion build targets to
  report the real values of `MAX_CONTACTS`, `OFFLINE_QUEUE_SIZE` and
  `MAX_GROUP_CHANNELS`. Its target count (174) matches
  `tools/design-overview.py`, which is the cross-check that the resolver is
  right.
- **Six terms in both terminology files**, inserted alphabetically:
  `app_target_ver`, Companion-protocol / Companion protocol,
  `FIRMWARE_VER_CODE`, Frame, Opcode, Pushcode / Push code.

### Changed

- **`README.md` is now a bilingual switchboard instead of a bilingual
  article.** It went from 230 to 138 lines and keeps only what is
  language-neutral or has to be seen before the language choice: badges, the
  two language links with a one-line pitch each, the AI disclaimer in both
  languages, the layout tree, errata, licence and community. Reason: a new
  section had to be registered in six places (the Dutch table in root, the
  English table in root, both structure trees and both indexes), the reading
  guide sat one click away from the index it described, and a reader entering
  through a language index — which is how the site is read — never saw any of
  it. The `## Nederlands` and `## English` sections are gone; the disclaimer
  is one block with a Dutch and an English paragraph.
- **`nl/README.md`, `en/README.md`** — a pointer to the reading guide above
  the first section, deliberately without a `##` heading of its own so no
  empty section appears in the site menu, plus an index entry under
  *Project*, which is what puts the chapter in the menu at all.
- **`CLAUDE.md`** — the layout tree shows both README indexes and the two
  reading guides; the root `README.md` is described as a switchboard; two new
  rules record that one chapter sits outside a section directory and that the
  narrative belongs to the language trees, so it is not restored in root
  later on.
- The chapter count in the reading guide reads 94 per language, up from the
  93 the root `README.md` stated, because the reading guide itself is a
  chapter. The diagram count is unchanged at 73 per language.
- **Review of the Dutch `companion/` section processed** — all eight Dutch
  chapters revised for readability: key terms are now defined at first use, a
  glossary table was added to `nl/companion/introduction.md`, and unnecessary
  English terms in running prose were replaced by Dutch ones with the source
  term in brackets on first use: `advert` → aankondiging, `scope` →
  verspreidingsgebied, `build target` → compilatiedoel, `build flag` →
  compilatieoptie, `binary` → firmwarebestand, `libraries` →
  softwarebibliotheken, `clientbouwer` → ontwikkelaar van een client. Names of
  commands and constants (`CMD_SEND_SELF_ADVERT`, `PUSH_CODE_ADVERT`,
  `flood.max.unscoped`) are unchanged, as is the chapter title
  `Regio's en Scopes` and every link to it.
- **Headings made accurate rather than allusive**, in both languages:
  `De grenzen zijn geen constanten` → `De maximale aantallen verschillen per
  firmwarevariant` (they are compile-time constants; only their value differs
  per variant), `Eén transport per binary` → `Eén verbindingstype per
  firmwarevariant`, `Alle achtenvijftig zijn echt` → `Alle 58 commando's
  worden door de firmware afgehandeld`, `Serieel: geen verbindingsbegrip` →
  `Serieel: de firmware detecteert geen verbroken kabel`, `Advert en pad` →
  `Aankondigingen en routes`, `Laag 6 — Gevel met cache` → `Laag 6 —
  Publieke API met cache` (NL only; EN keeps *facade*).
- **Wording corrected where it was imprecise**: sixty milliseconds is a
  minimum interval and therefore a theoretical maximum of roughly sixteen
  notifications per second; a frame that is too large is refused only after
  it has been sent, not "over de lijn"; failing to check the length may lead
  to reading bytes outside the frame as valid fields or to a read error,
  rather than "reading memory that is not there"; a new TCP connection drops
  the existing one without a protocol notification, rather than a "stille
  aflossing".
- **Conceptual explanation separated from source evidence** in
  `nl/companion/logisch/responsibilities.md` and its EN counterpart: the
  counting method behind the 174 build targets moved from the running text to
  `## Bronnen` / `## Sources`, and the halved contact count in the
  `CMD_DEVICE_QUERY` response became a warning with a worked example
  (175 × 2 = 350).
- **`nl/naslag/terminology.md`** — `Opcode` now reads *de eerste byte*
  (`byte` is a de-word in Dutch); the `Advert/Beacon` and `Scope` entries name
  the Dutch term used in running prose.
- **`images/nl/companion-architecture-1.svg`,
  `images/nl/companion-information-model-1.svg`,
  `images/nl/companion-responsibilities-1.svg`** — diagram labels follow the
  revised Dutch terms. The English diagrams are unchanged, since English keeps
  the source terms.
- `nl/README.md`, `en/README.md` — new `Companion` section between Hardware
  and Libraries, at the same position in both trees.
- `README.md` — `companion/` added to the layout tree in both language
  columns.
- `nl/techniek/regions-and-scopes.md`, `en/technical/regions-and-scopes.md` —
  the existing note that four scope commands are missing from
  `docs/companion_protocol.md` now points at the new command chapter and puts
  the gap in proportion: seven of the fifty-eight commands are documented,
  not fifty-four of fifty-eight.
- `nl/hardware/interfaces/ble-architecture.md`,
  `en/hardware/interfaces/ble-architecture.md` — closing cross-reference to
  `companion/technisch/transports.md`, so the reader who has just learned how
  the link works can find out what travels over it.

### Fixed

- `nl/project/github.md`, `en/project/github.md` — the description of
  `meshcore.js` said it was a "JavaScript/TypeScript library for decoding
  MeshCore mesh packets". It is not a packet decoder; it is a companion
  client library that connects to a node over Web Bluetooth, Web Serial,
  serial or TCP. Corrected in both languages.
- `nl/project/github.md`, `en/project/github.md` — added a note that the
  MeshCore firmware points at two different sets of repositories for the same
  libraries: `README.md` r.70-71 names `liamcottle/meshcore.js` and
  `fdlamotte/meshcore-cli`, while `docs/companion_protocol.md` r.16-17 names
  the `meshcore-dev` variants. The projects moved to the organisation and the
  README did not follow.
- `README.md` — the chapter and diagram counts said 70 chapters and 52
  diagrams per language. Both were already stale before this change: the
  repository held 85 chapters and 67 referenced diagrams. With this section
  added the figures are 93 and 73, and the README now says so.

### Note on structure

`CLAUDE.md` states under 🛡️ *Existing content* that no new top-level
directories are to be created. `companion/` is one. The client chose that
placement explicitly over the two alternatives (folding the material into
`ontwerp/`, or splitting it across `hardware/interfaces/` and `techniek/`),
because `ontwerp/` scopes itself to the structure of the firmware and the
companion interface is a contract between two systems. The rule is recorded
here as knowingly set aside, not overlooked. `CLAUDE.md` has not been changed
in this session.

---

## [2026-07-31] Result of first review session

### Changed

- **Terminology overhaul across both language trees**, following an external
  readability review of `nl/ontwerp/`. The Dutch chapters had grown a set of
  coined terms that readers had to learn before the technical content became
  accessible. Each has been replaced by the common software term, and the
  English tree follows so that the two stay in step. Earlier CHANGELOG entries
  still use the old wording; the table below maps them.

  | Dutch — was | Dutch — is | English — was | English — is |
  |---|---|---|---|
  | bronboom / gedeelde boom | broncodestructuur / gedeelde broncode | source tree | source tree (unchanged) |
  | invulling | implementatie | filler | implementation |
  | contractdefiniërend | interfaceklasse | contract-defining | interface class |
  | contractvullend | implementatieklasse | contract-filling | implementation class |
  | bijmenging | aanvullende buildoptie | mixin / admixture | optional build feature |
  | productvlak | configuratiematrix | product space | configuration matrix |
  | injectiepunt | koppelpunt | injection point | coupling point |
  | dubbelpaar | chipdriver en MeshCore-wrapper | double pair | chip driver and MeshCore wrapper |
  | pakketvoorraad | pakketpool | packet pool | packet pool (unchanged) |
  | toevalsbron | entropiebron | entropy source | entropy source (unchanged) |
  | draagvlak | netwerkinfrastructuur / transportmedium | carrier / fabric | network infrastructure / transport medium |
  | scheefheid | asymmetrie | skew | asymmetry |
  | gevendord | meegeleverd | vendored | vendored (unchanged) |

- The verb followed the noun: *een contract invullen* is now *een contract
  implementeren*, and *to fill a contract* is *to implement a contract*.
- `nl/techniek/packet-structure.md` is titled **MeshCore Pakketstructuur**
  instead of *MeshCore Packet Structuur*; the ten link texts that name the
  chapter were updated with it. The file name is unchanged, so no link breaks.
- Four sentences reworded on the review's style points: the memory
  fragmentation metaphor, the impersonal `IdentityStore` sentence, the
  unresolved references in the battery-voltage paragraph, and the judgemental
  opening of the traceability matrix. Both languages.
- `tools/config-flags.py` emits *broncodestructuur* rather than *bronboom* in
  its Dutch output, so the reproduced text matches the chapter again.
- Eight Dutch and five English SVG diagrams carry the new labels:
  `class-model-1`, `components-1`, `interfaces-1`, `variability-1`,
  `source-layout-1`, `configuration-1`, `design-layers-1` and
  `radio-realisation-2`.

### Added

- **Reading guide in `README.md`**, both languages: a table stating per section
  what background a reader needs, from *no programming knowledge required* for
  the usage chapters to *C++ classes, inheritance and PlatformIO build
  configurations* for the technical design. The review asked for this per
  chapter; it lands in the README instead, so the reader can pick a starting
  point before opening anything.
- Thirteen glossary entries in `nl/naslag/terminology.md` and
  `en/reference/terminology.md`, inserted alphabetically: application,
  bridge, component, entropy source, hardware variant, implementation, macro,
  packet pool, scheduler, seen table, source tree, vendored code and wrapper.
  Both files now hold 195 terms.
- First-mention explanations in `nl/ontwerp/logisch/components.md` for the
  seen table, the packet pool and the entropy source, so the short term can be
  used from then on.

### Note

- The review proposed reading *gevendord* as *outdated or leftover code*. That
  reading is wrong: vendoring means a dependency is kept as a copy in the
  repository instead of being fetched by the package manager, and says nothing
  about age or use. The vendored Ed25519 in `lib/ed25519` is the actively used
  implementation for key generation and key exchange. The Dutch coinage was
  dropped, but in favour of *meegeleverd* rather than the proposed wording, and
  the `vendoring` glossary entry now names both.
- The review's request for a glossary was already met by
  `naslag/terminology.md`; it was extended rather than duplicated.

## [2026-07-30] Add Design section — technical design

### Added

- `nl/ontwerp/technisch/` and `en/design/technical/`: seven chapters
  completing the Design section. The logical design described *what* MeshCore
  is; these chapters describe *how* it is realised, with file names and line
  numbers throughout, so that every claim can be checked against the firmware
  rather than believed.
- `nl/ontwerp/technisch/source-layout.md`,
  `en/design/technical/source-layout.md`: what sits where in the source tree,
  and the skew between the platform directories — ESP32 has four classes in
  its platform directory, nRF52 and STM32 one each, RP2040 none at all. The
  chapter argues that this measures how much there was to share, not how well
  a platform is supported.
- `nl/ontwerp/technisch/class-model.md`, `en/design/technical/class-model.md`:
  the 196 classes split three ways — 14 contract-defining, 50
  contract-filling, 55 standalone, plus the 77 in `variants/` as a summary.
  Includes what is *not* a contract, because `ESP32Board`, `BridgeBase` and
  `RadioLibWrapper` are borderline cases that a reader will otherwise
  misfile.
- `nl/ontwerp/technisch/platform-realisation.md`,
  `en/design/technical/platform-realisation.md`: how four platform families
  fill one abstraction, with storage as the sharpest dividing line, and why
  nRF52 needs 366 lines of board code where ESP32 needs 47.
- `nl/ontwerp/technisch/radio-realisation.md`,
  `en/design/technical/radio-realisation.md`: the injection point sits in the
  variant rather than the core, and there are two classes per radio chip
  because adapting a RadioLib driver and filling the MeshCore contract are
  different jobs. Records that LLCC68 exists in full and is chosen by no build
  target.
- `nl/ontwerp/technisch/build-system.md`,
  `en/design/technical/build-system.md`: 80 ini files, 616 sections, 508 build
  targets, 108 base sections, and the two inheritance mechanisms that both
  have to be followed — following only one loses 28 targets silently.
- `nl/ontwerp/technisch/configuration.md`,
  `en/design/technical/configuration.md`: the 277 `-D` macros by owner, and
  the finding that 53 of the 254 MeshCore macros are defined and read nowhere.
  Includes the traversal order the distribution table depends on, because a
  different order moves up to 22 macros between buckets.
- `nl/ontwerp/technisch/traceability.md`,
  `en/design/technical/traceability.md`: every component from
  `logisch/components.md` pointed out in the source tree, plus two empty rows
  for the routing table and the task model. The empty rows stay in on purpose:
  a matrix without them suggests everything has been realised.
- `images/nl/` and `images/en/`: eight new diagrams, both languages —
  `source-layout-1`, `class-model-1`, `class-model-2`,
  `platform-realisation-1`, `radio-realisation-1`, `radio-realisation-2`,
  `build-system-1`, `configuration-1`.
- `tools/config-flags.py`: `--owners` writes groups 2 and 3 as a markdown
  table; `--consumption` gives per MeshCore macro the first place its name
  occurs in the source tree, with an explicit *read nowhere* category;
  `--misfiled` lists the five macros the ownership table groups wrongly.
  `--lang` selects the language of those tables. The existing output for
  `libraries/library-configuration.md` is unchanged byte for byte, verified by
  running the script before and after and comparing with `diff`.
- `tools/design-overview.py`: `--classes` reports the class census the two
  class chapters quote — 119 in the shared tree, 77 in `variants/` under 73
  unique names, and the per-directory breakdown. Added beyond the assignment
  because without it those figures are not reproducible from `tools/`, which
  the verifiability rule requires; flagged rather than done silently.
- `nl/naslag/terminology.md`, `en/reference/terminology.md`: ten new terms
  each, inserted alphabetically — board class, contract-defining,
  contract-filling, shared tree, injection point, platform macro, text
  splicing, traceability matrix, virtual inheritance, standalone class. The
  last one carries an explicit warning that it is not the firmware role
  *Standalone*, which was already in the list.

### Changed

- `nl/README.md`, `en/README.md`: new group **Technisch ontwerp** /
  **Technical design** under Design, with the seven chapters in reading order.
- `nl/ontwerp/introduction.md`, `en/design/introduction.md`: the paragraph
  announcing a second delivery replaced by links to the seven chapters, since
  they now exist.
- `nl/platform/platform-families.md`, `en/platform/platform-families.md`:
  pointer to `platform-realisation.md`, so a reader comparing the four
  families can follow through to how the firmware absorbs the differences.
- `nl/libraries/library-configuration.md`,
  `en/libraries/library-configuration.md`: pointer to `configuration.md`,
  placing the seventeen library flags in the context of all 277 macros.

### Fixed

- Three figures in the source analysis for this delivery did not match the
  firmware and were corrected before writing, not afterwards:
  - `src/helpers/` was stated as holding 40 loose files; it holds **38**. The
    class count of 33 was correct.
  - `RADIO_CLASS` and `WRAPPER_CLASS` were stated as occurring on two comment
    lines in `src/helpers/esp32/TBeamBoard.cpp`, r.313 and r.334. There are
    **four**: `RADIO_CLASS` on r.313 and r.334, `WRAPPER_CLASS` on r.314 and
    r.335.
  - The two unrealised logical components were named as routing and an error
    model. `logisch/components.md` names the **routing table** and the **task
    model**, and no error model appears anywhere in the logical design; the
    matrix follows the chapter it maps from.

### Known issues

- `images/en/` holds two files with no counterpart in `images/nl/`:
  `05-group-communication-2.png` and `techniek-chirp-3.svg`. That breaks the
  rule that every diagram exists twice under the same name. Pre-existing and
  outside the scope of this delivery, so reported rather than repaired.
- `tools/config-flags.py` still classifies `NDEBUG`, `BOARD_HAS_PSRAM`,
  `PIN_SERIAL_RX`, `PIN_SERIAL_TX` and `ENABLE_HWSERIAL2` as MeshCore macros
  while a framework reads them. Not corrected in `NAMESPACES`, because moving
  them changes the group counts the chapter quotes; `--misfiled` lists them
  and `configuration.md` states the correction in the text.

---

## [2026-07-30] Add Design section — logical design

### Added

- `nl/ontwerp/` and `en/design/`: new section describing how the firmware is
  put together, split into a logical and a technical design. This delivery
  contains the section introduction and the complete logical design; the
  seven technical chapters follow separately, which is why they are not yet
  listed in the README indexes.
- `nl/ontwerp/introduction.md`, `en/design/introduction.md`: positions the two
  layers against each other and against `techniek/`, `platform/`, `hardware/`
  and `libraries/`, so the section repeats nothing that already exists
  elsewhere.
- `nl/ontwerp/logisch/` and `en/design/logical/`: six chapters — `roles.md`
  (the six applications and why exactly one lands in each build),
  `components.md` (responsibilities and, more usefully, what each part does
  not know), `interfaces.md` (the eight contracts, with the split between
  mandatory and optional agreements), `information-model.md` (the seven data
  objects and what survives a restart), `variability.md` (three axes plus
  mixins, and why counting on target names is wrong), `decisions.md` (seven
  choices and what each one costs).
- `tools/design-overview.py`: resolves the build matrix of a MeshCore
  checkout. Follows both PlatformIO inheritance mechanisms — `extends` and
  `${section.option}` — normalises CRLF before parsing and skips
  commented-out `-D` macros. Every figure in the section comes from this
  script. Cross-checked against `tools/room-server-overview.py`: both arrive
  at 73 room server targets in 65 variant directories by different routes.
- Twelve diagrams in `images/nl/` and `images/en/`: `design-layers-1.svg`,
  `roles-1.svg`, `components-1.svg`, `interfaces-1.svg`,
  `information-model-1.svg`, `variability-1.svg`.
- Ten terms in `nl/naslag/terminology.md` and `en/reference/terminology.md`:
  base section, mixin, source filter, contract, `extends`, KISS, logical
  design, role, technical design, variability.

### Changed

- `CLAUDE.md`: the rule stating that directory names are English was wrong
  about the repo's own second level — `gebruik`, `techniek` and `naslag` are
  Dutch. Rewritten to say that directory names follow the section mapping at
  every level, with the four third-level directories that predate the rule
  recorded as a documented exception rather than silently renamed. Also: three
  sections with a third level becomes four, the image-path rule and the slug
  mapping list the new directories, and two pitfalls were added — `technical`
  now occurring on two levels in the English tree, and what
  `tools/design-overview.py` has to resolve.
- `nl/README.md`, `en/README.md`: new `## Ontwerp` / `## Design` section after
  Techniek respectively Technical.
- `README.md`: structure tree extended with `ontwerp/` and `design/`.

### Notes

Three findings surfaced while verifying against firmware v1.16.0, commit
`03b6ef4`, 28 July 2026, and are documented in the chapters rather than
silently corrected. First, `Generic_E22_kiss_modem` cannot compile: it inherits
a source filter that pulls in `variants/generic-e22/target.cpp`, which uses
`RADIO_CLASS`, while neither the target nor any section above it defines that
macro — its sibling targets do. Second, RP2040 has no shared board class;
ESP32, nRF52 and STM32 each have one in `src/helpers/`, while the four RP2040
variants each write their own, which is why the board contract has seven
implementations and not four. Third, `MESH_DEBUG` occurs 387 times in the ini
files and is genuinely enabled in 36 targets; the rest sit commented out.

The firmware compiles `FIRMWARE_BUILD_DATE "6 Jun 2026"` in four of the six
applications, which is not the same as the commit date this section is pinned
to.

---

## [2026-07-30] Add Library configuration

### Added

- `nl/libraries/library-configuration.md` and
  `en/libraries/library-configuration.md`: new overview chapter in the
  `libraries/` section, alongside `introduction.md` and `dependencies.md`. It
  answers a question `core/radiolib.md` raised but did not settle: why a
  library is configured by *excluding* things when you would expect to include
  them. The answer is that there is no shared convention, so the chapter
  documents four of them side by side — exclusion (default is everything),
  inclusion (default is nothing), override (a value with a default behind
  `#ifndef`) and type injection (a macro carrying a class name) — plus
  `lib_deps` as exclusion at project level and forking as the last resort.
  Verified against firmware v1.16.0, commit `03b6ef4`, 28 July 2026, and
  against the library sources themselves: RadioLib 7.6.0, both littlefs copies
  in the build tree, Adafruit SSD1306, Adafruit RTClib, `rweather/Crypto`,
  ESPAsyncWebServer and CustomLFS 0.2.2.
- `tools/config-flags.py`: reproducibility script behind the chapter's
  inventory table. Reads the root `platformio.ini` plus every
  `variants/*/platformio.ini`, splits the `-D` macros by owner (library,
  framework, MeshCore) and tabulates the library-directed ones. Ownership does
  not follow from the macro name, so it comes from a table in the script that
  records, per namespace, which library source file consumes the macro. Writes
  between `<!-- config-flags:start -->` and `<!-- config-flags:end -->`, so the
  surrounding prose is untouched. Commented-out `-D` lines are reported
  separately rather than counted, because they are part of no build.
- `images/nl/library-configuration-1.svg` and
  `images/en/library-configuration-1.svg`: the four mechanisms side by side,
  each with its default state and what the macro changes.
- Terminology: *opt-in / opt-out*, *uitsluitmacro* / *exclusion macro* and
  *typeinjectie* / *type injection* in both language trees.

### Changed

- `nl/libraries/core/radiolib.md` and `en/libraries/core/radiolib.md`: added
  the missing explanation before the block of fourteen `-D` flags —
  `RadioLib.h` r.76-124 includes every module driver and every protocol
  unconditionally and each class sits behind `#if !RADIOLIB_EXCLUDE_<name>`, so
  exclusion is the only knob the library offers. Cross-reference to the new
  chapter for the wider picture.
- `nl/libraries/core/custom-lfs.md` and `en/libraries/core/custom-lfs.md`:
  recorded that `LFS_NO_ASSERT` does not touch CustomLFS itself, which contains
  no littlefs but wraps `Adafruit_LittleFS` (`CustomLFS.h` r.30). The build tree
  holds two littlefs copies and the flag sits in `[nrf52_base]` only, so
  nRF52 firmware compiles littlefs without asserts and STM32 firmware with them.
- `nl/libraries/other/displays.md`, `en/libraries/other/displays.md`,
  `nl/libraries/other/sensors.md` and `en/libraries/other/sensors.md`:
  cross-references naming the mechanism each chapter is an example of — type
  injection for `DISPLAY_CLASS`, opt-in for `ENV_INCLUDE_*`.
- `nl/README.md` and `en/README.md`: menu entry for the new chapter.

### Fixed

- `nl/libraries/core/radiolib.md` and `en/libraries/core/radiolib.md`: the
  fourteen `RADIOLIB_EXCLUDE_*` flags were described twice as fourteen
  *protocols*. They are six module drivers and eight protocols, as the
  paragraph below the code block already stated correctly.

---

## [2026-07-29] New Hardware section / RoomServer

### Added

- **Hardware** (`nl/hardware/`, `en/hardware/`): new top-level section
  describing what a MeshCore node is made of — the radio, the connections to
  the outside world, and the devices hanging off the buses of the SoC. Until
  now the SX1262, the OLED display and USB serial had no place in the repo:
  `platform/` covers which board has what, `techniek/` covers the protocol,
  and the components themselves fell between the two. The section takes a
  third directory level after the model of `libraries/`, with `radio/`,
  `interfaces/` and `peripherals/` identical in both language trees.
- `nl/hardware/introduction.md` and `en/hardware/introduction.md`: block
  diagram of a node, how the firmware names those blocks (`RADIO_CLASS`,
  `BaseSerialInterface`, `DisplayDriver`, `SensorManager`), and the criterion
  separating the three subsections. Verified against firmware v1.16.0, commit
  `03b6ef4`, 28 July 2026. The chapter also settles the three different
  meanings of *randapparatuur* / *peripherals* in this documentation, which
  until now collided silently between `platform/node-matrix.md` table 3 and
  `libraries/other/peripherals.md`.
- `images/nl/node-blockdiagram-1.svg` and `images/en/node-blockdiagram-1.svg`.
  Named after what the diagram shows rather than after its chapter slug:
  `images/` is flat and `introduction-1.svg` was already taken by
  `libraries/introduction.md`. No existing image file was moved or renamed.
- **`hardware/interfaces/`**: four new chapters per language on how a node
  connects to the outside world and to what is on the board — `wifi.md`,
  `usb-serial.md`, `i2c.md` and `spi.md`. Verified against firmware v1.16.0,
  commit `03b6ef4`, 28 July 2026. The load-bearing finding is that BLE, WiFi
  and serial are mutually exclusive: `examples/companion_radio/main.cpp`
  r.37-54 compiles in exactly one of them, so which transport a node speaks
  is a build choice and not a setting. Also documented: the WiFi credentials
  end up as plain text in the binary, the serial framing byte by byte
  (`>` / `<` plus a 16-bit length, LSB first, payload up to 176 bytes), the
  I²C autodetection over addresses `0x08`–`0x77`, and the per-platform
  differences in how the SPI pins reach RadioLib.
- Eight diagrams (`images/nl/`, `images/en/`): `wifi-1.svg`,
  `usb-serial-1.svg`, `i2c-1.svg` and `spi-1.svg`, each in both languages.
- **`hardware/radio/`**: three new chapters per language — `sx1262.md`,
  `antenna.md` and `link-budget.md`. Verified against firmware v1.16.0,
  commit `03b6ef4`, 28 July 2026. The firmware supports six radio families
  through one pattern, retries initialisation with the TCXO voltage at zero
  when it fails with `-706`/`-707`, patches register `0x8B5` on three boards
  while the comment names only one, and measures its own noise floor over 64
  RSSI samples clamped at −120 dBm. The scope is deliberately narrow: the
  radiation pattern and the dead zone stay in `techniek/dead-zone.md`, and
  e.r.p., the dBi/dBd conversion and the duty cycle stay in
  `gebruik/regulations.md`. Both are referenced, neither is repeated.
- **`tools/link-budget.py`**: reproduces every figure in `link-budget.md`.
  Firmware values and external assumptions are kept strictly apart in the
  script; the two inputs that are not in the firmware repo — receiver noise
  figure and required SNR per spreading factor — are constants at the top and
  are marked with `°` in the chapters, following the convention of
  `platform/node-matrix.md`.
- Six diagrams (`images/nl/`, `images/en/`): `sx1262-1.svg`, `antenna-1.svg`
  and `link-budget-1.svg`, each in both languages.
- **`hardware/peripherals/`**: three new chapters per language —
  `display.md`, `gps.md` and `buttons-and-leds.md`. Verified against firmware
  v1.16.0, commit `03b6ef4`, 28 July 2026. Documented for the first time:
  `DISPLAY_CLASS` has eleven values across 164 build-flag lines, one of which
  is a complete do-nothing driver used by fifteen targets; the display
  abstraction replaces every non-ASCII character with a single CP437 block,
  which is why accented characters show as blocks on an OLED; a shared power
  rail is reference-counted rather than switched, so one part cannot cut
  power to another; the GPS enable pin is resolved through a four-layer
  `#ifndef` cascade that silently ends at `-1`; and one button yields five
  events with a fixed 280 ms multi-click window.
- Three diagrams (`images/nl/`, `images/en/`): `display-1.svg`, `gps-1.svg`
  and `buttons-and-leds-1.svg`, each in both languages.
- Eight terms in `nl/naslag/terminology.md` and `en/reference/terminology.md`,
  inserted alphabetically: CP437, debouncing, e-paper, GNSS, NMEA, OLED,
  RTTTL and XBM. *e-ink* and *GPIO* were already present and were left
  untouched.
- Eight terms in `nl/naslag/terminology.md` and `en/reference/terminology.md`,
  inserted alphabetically: dBd, dBi, FSPL, LNA, noise floor, RSSI, SWR and
  TCXO. *Link budget* and *Power amplifier (PA)* were already present and
  were left untouched.
- Ten terms in `nl/naslag/terminology.md` and `en/reference/terminology.md`,
  inserted alphabetically: `BUSY`, `MISO`, `MOSI`, `NSS`, `SCL`, `SCLK`,
  `SDA`, TCP, `TwoWire` and USB CDC-ACM.
- **`tools/hardware-overview.py`**: recomputes the ten counts that the
  `hardware/` chapters state, against the pinned commit. Every figure carries
  its search pattern and its unit, because the difference between a line and a
  file is where the earlier errors came from: a variant file can hold several
  `[env:…]` sections that each set the same flag. Commented-out lines are
  excluded inside the script rather than in the invocation, and flags that
  appear both in `platformio.ini` and in a variant header are counted per
  variant directory.

- **Room Server** (`nl/techniek/roomserver/`, `en/technical/roomserver/`):
  new subsection of five chapters per language covering the room-server
  firmware, positioned in both indexes directly after *Direct Messages*
  because a post travels in the same payload type. `techniek/` ↔
  `technical/` thereby gains a third directory level, after the model of
  `libraries/` and `hardware/`. Unlike those two, the overview chapter
  `introduction.md` lives *inside* the subdirectory rather than one level up,
  so the section moves as a unit; that was an explicit client decision.
  Verified against firmware v1.16.0, commit `03b6ef4`, 28 July 2026.
- `nl/techniek/roomserver/introduction.md` and
  `en/technical/roomserver/introduction.md`: the room server in plain
  language — the channel-versus-e-mail comparison from the official FAQ, the
  four steps a user goes through, and a table of four things that are
  commonly assumed and that the firmware does not do.
- `nl/techniek/roomserver/login-and-acl.md` and
  `en/technical/roomserver/login-and-acl.md`: the `ANON_REQ` login with its
  extra `sync_since` field, the three password paths, the 13-byte reply byte
  by byte, and the permission model. The load-bearing finding is that a wrong
  password produces *no reply at all* (`MyMesh.cpp` r.339-340), so a typo is
  indistinguishable from an unreachable server.
- `nl/techniek/roomserver/posts-and-sync.md` and
  `en/technical/roomserver/posts-and-sync.md`: the cyclic queue, the
  `TXT_TYPE_SIGNED_PLAIN` payload written out with real values, and the
  expected ACK as `sha256(plaintext ‖ client pubkey)` truncated to four
  bytes. `sync_since` advances only on a received ACK, which is what makes
  the counter the entire bookkeeping.
- `nl/techniek/roomserver/requests-and-cli.md` and
  `en/technical/roomserver/requests-and-cli.md`: request types `0x01`,
  `0x02`, `0x03` and `0x05`, the keep-alive ACK that carries the unsynced
  counter as an appended byte, and the room-specific CLI commands. Records
  that `0x05` is admin-only *and* filters out everything that is not an
  admin.
- `nl/techniek/roomserver/limits-and-todos.md` and
  `en/technical/roomserver/limits-and-todos.md`: what the firmware does not
  do, including all eight `TODO`/`REVISIT` lines in `MyMesh.cpp`. New finding
  not previously described anywhere: if all 20 ACL slots hold administrators,
  `ClientACL::putClient()` r.99 leaves `oldest` pointing at `clients[19]` and
  overwrites an *administrator* — the only path by which an admin leaves the
  ACL without `setperm`.
- `images/nl/room-server-overview-1.svg`, `-login-1.svg`, `-sync-1.svg`,
  `-requests-1.svg` and their `images/en/` counterparts. Named after what
  they show rather than after their chapter slug: `images/` is flat and
  `introduction-1.svg` was already taken by `libraries/introduction.md`.
- `tools/room-server-overview.py`: reproduces the build-target counts, the
  `ROOM_PASSWORD` defaults, the firmware constants read straight from the
  source, and the worked push/ACK example. The example identities follow the
  same convention as `tools/dm-example.py`.

### Fixed

- `nl/gebruik/communication.md`, `en/usage/communication.md`: the *Room
  Servers* section claimed a **member list** ("je ziet wie er in de Room
  zit") and **management** ("moderators kunnen leden toevoegen en
  verwijderen"). Neither exists. The only list is `REQ_TYPE_GET_ACCESS_LIST`
  (`0x05`), which is admin-only and skips every non-admin entry
  (`MyMesh.cpp` r.192); administration is one `setperm` command that sets
  rights on a public key. The same section called the queue **persistence**
  ("tot 32 berichten worden bewaard") — the 32 slots are an array in RAM that
  no restart survives, which is now stated as a warning. The comparison table
  gained a *survives a restart* row and had its *member list* value corrected
  from yes to no.
- `nl/gebruik/node-types.md`, `en/usage/node-types.md`: "Beheert een of
  meerdere Rooms" — the firmware has one room per node and no room concept at
  all beyond the node itself. Also "Vereist Ultra-licentie voor beheer op
  afstand": that term appears neither in the firmware nor in the official
  documentation. `docs/faq.md` describes a T-Deck registration key and an
  unlock in the smartphone apps, both restrictions in the *client*, and the
  entry now says that instead.
- `nl/naslag/terminology.md`, `en/reference/terminology.md`: the *Room
  Server* entry said "tot 32 berichten" without saying where they live; it
  now records that the queue is in working memory and does not survive a
  restart.
- `nl/gebruik/node-types.md`: removed the stray line `Network diagram SVG`, a
  leftover from the original HTML-to-Markdown conversion. It had no
  counterpart in the English file, so this correction is Dutch-only.
- `nl/gebruik/node-types.md`, `en/usage/node-types.md`: the alt text
  `Diagram 1 bij node-types` replaced by a description that stands on its
  own, per the project's own rule.
- `images/nl/node-types-1.svg`, `images/en/node-types-1.svg`: the diagram
  showed four of the five node types the chapter lists — the standalone
  device was missing. Added as a sixth circle at (180, 200) in the empty
  lower-left quadrant, with a dashed link to the room server in the existing
  style; no other coordinate moved and the viewBox is unchanged. The two
  files were byte-identical before this change and still are: every label in
  this diagram (`COMPANION`, `REPEATER`, `ROOM SERVER`, `TELEMETRY`,
  `STANDALONE`) is the same in both languages. The alt text now names all
  five types.

### Changed

- `nl/README.md`, `en/README.md`: **Hardware** index section added between
  *Platform* and *Libraries*. It lists only `introduction.md`; the chapters of
  the later phases are deliberately absent rather than present as dead links.
- `README.md`: `hardware/` with its three subdirectories added to the
  structure tree in both language trees; chapter count 54 → 55 per language.
- `README.md`: both count sentences corrected to the state after the
  `hardware/` section — 55 → 65 chapters per language and 38 → 48 diagrams per
  language. The counts had stood at the pre-`hardware/` state and were
  therefore untrue. The counting method is now named in the sentence itself:
  chapters are `.md` files per language tree excluding the `README.md`
  indexes, diagrams are the SVGs a chapter actually references. That second
  method matters because `images/en/` holds one SVG no chapter links to, so
  files on disk and diagrams in use are 49 and 48.
- `nl/hardware/peripherals/buttons-and-leds.md`,
  `en/hardware/peripherals/buttons-and-leds.md`: two counts corrected after
  `tools/hardware-overview.py` disagreed with them. `PIN_USER_BTN` read
  forty-four variant files; forty-four is the line count, the file count is
  forty-two, and the `grep -rl` quoted alongside it returned a third number
  because it also counted a file where the flag appears only commented out.
  The sentence now names both units and explains the difference — `rak4631`
  sets the flag in three `[env:…]` sections. `PIN_BUZZER` read fifteen variant
  files; in one of those, `minewsemi_me25ls01`, the line is commented out, so
  fourteen is the count under the project's own rule. The quoted `grep`
  invocations were replaced by a reference to the script. No other figure in
  `hardware/` changed: the remaining eight counts the script produces already
  matched their chapters.
- `nl/naslag/terminology.md`, `en/reference/terminology.md`: the two
  consecutive alphabetical runs merged into one. Both lists had a second run
  starting again at *Regiocode* / *Region code* after `XBM`. In the English
  list *Power amplifier (PA)* additionally sat in front of *EIRP* and now sits
  between *PlatformIO environment* and *Preamble*. 154 terms before, 154
  terms after, in both languages; no term was added, removed or reworded. The
  sort key ignores case and punctuation, otherwise `ESP-NOW` sorts before
  `ESP32` and `Standalone` after `ST-Link`.
- **Moved** `nl/techniek/ble-architecture.md` → `nl/hardware/interfaces/ble-architecture.md`
  and `en/technical/ble-architecture.md` → `en/hardware/interfaces/ble-architecture.md`.
  BLE is a connection to a companion, not a protocol internal, so it belongs
  beside WiFi and USB serial rather than in the protocol section. The slug is
  unchanged and the content is unchanged; the only edit inside the files is
  one extra `../` in the image path, because the chapters moved from the
  second to the third level. `images/nl/ble-architecture-1.svg` and
  `images/en/ble-architecture-1.svg` stayed exactly where they were —
  image files are not moved. The unreferenced legacy PNG
  `18-ble-architecture-1.png` likewise stayed untouched in both image
  directories.
- `nl/README.md`, `en/README.md`: the BLE entry moved from *Techniek* /
  *Technical* to a nested bullet under the non-linking group label
  **Interfaces**, together with the four new chapters. A second group label
  **Radio** was added above it with the three `hardware/radio/` chapters, and
  a third, **Randapparatuur** / **Peripherals**, below it with the three
  `hardware/peripherals/` chapters.
- `CLAUDE.md`: section mapping extended with `hardware` ↔ `hardware`. The rule
  that `libraries/` is the only section with a third level was true when it
  was written and no longer is; it now names both sections. The image rules
  gained a paragraph on slug collisions in the flat `images/` directory,
  written because `hardware/introduction.md` ran into
  `libraries/introduction.md` over `introduction-1.svg`.

- `nl/naslag/terminology.md`, `en/reference/terminology.md`: five terms added
  in alphabetical position — ACL, BBS, Keep-alive, Post and `sync_since`.
- `nl/README.md`, `en/README.md`: **Room Server** group added to the
  *Techniek* / *Technical* section, directly after *Direct Messages*.
- `README.md`: chapter count 65 → 70 and diagram count 48 → 52 in both
  language halves; `roomserver/` added to the structure tree under
  `techniek/` and `technical/`.
- `CLAUDE.md`: the rule naming `libraries/` and `hardware/` as the only
  sections with a third level now names three, and records that
  `roomserver/` deviates by keeping its `introduction.md` inside the
  subdirectory. Added a rule that directory names are a single word without
  hyphens — true of all fourteen directories in the repo, but never written
  down, and the reason this section is `roomserver/` while its label reads
  *Room Server*. Added a pitfall about counting build targets by section
  name: that method gives 70 targets in 66 directories where the correct
  count is 73 in 65.

---

## [2026-07-29] Add libraries section

### Added

- **Libraries** (`nl/libraries/`, `en/libraries/`): new top-level section of
  twenty chapters per language describing which external code enters the
  MeshCore firmware, along which route, and how it is called. Until now the
  repo described what MeshCore does and which platforms it runs on, but not
  what it is built out of: the eighty `platformio.ini` files declare
  fifty-two libraries, six more arrive as undeclared transitive dependencies,
  and three pieces of external code bypass `lib_deps` altogether. None of
  that was documented anywhere.
- `libraries/introduction.md` and `libraries/dependencies.md` carry the two
  generated tables; the eleven chapters in `libraries/core/` cover one
  library each, and the seven in `libraries/other/` group the supporting
  libraries by function.
- **`tools/library-overview.py`** and `tools/library-metadata-snapshot.json`:
  the inventory and dependency tables are too large and change too often to
  maintain by hand. The script parses the root `platformio.ini` plus all
  seventy-nine variant files, reports `${section.lib_deps}` references
  separately rather than resolving them, fetches upstream `depends=` metadata
  from `raw.githubusercontent.com`, and writes between markers so surrounding
  prose survives. `--offline` uses the bundled snapshot.
- Twelve diagrams (`images/nl/`, `images/en/`): `introduction-1.svg`,
  `dependencies-1.svg`, `radiolib-1.svg`, `crypto-1.svg`, `displays-1.svg`
  and `sensors-1.svg`, each in both languages.
- Thirteen terms in `nl/naslag/terminology.md` and
  `en/reference/terminology.md`, inserted alphabetically: `lib_deps`,
  Library Dependency Finder, `library.properties`, `library.json`,
  `depends=`, transitive dependency, vendoring, semver caret, framework
  library, registry, GODMODE, LPP and build target.
- A `## Library Repositories` section in `nl/naslag/references.md` and
  `en/reference/references.md` with the upstream repositories of the eleven
  core libraries.

### Changed

- `nl/README.md` and `en/README.md`: `## Libraries` inserted after
  `## Platform`, listing all twenty chapters in the order of the section. The
  eighteen chapters on the third level are nested under a bold group label
  naming `libraries/core/` and `libraries/other/`, so the index shows the same
  structure as the directory tree.
- `README.md`: the `## Structuur · Layout` tree now shows `libraries/` with its
  `core/` and `other/` subdirectories, in both language branches.

### Fixed

- `README.md`: the chapter and diagram counts in both language sections were
  stale — they read 30 chapters and 25 diagrams per language while the repo
  held 34 chapters and 32 SVG diagrams before this change. They now read 54
  chapters per language and 38 SVG diagrams per language, counted as `.md`
  files under `nl/` and `en/` excluding `README.md`, and `.svg` files under
  `images/nl/` and `images/en/`. The twenty legacy PNGs are not counted; see
  *Known pitfalls* in `CLAUDE.md`.
- `README.md`: removed the paragraph pointing at `RECONCILIATIE.md` and
  `OPENSTAAND.md`. Neither file exists in the repository, so both links were
  dead.
- `CLAUDE.md`: repo tree, section mapping and image-path rule extended for
  the third directory level; the convention for firmware code excerpts (file
  and line numbers above the block, ±15 lines, `// ...` for omissions) added
  under *Document conventions*; two entries added under *Known pitfalls* —
  the third level being supported, and the requirement that figures counted
  over the firmware source tree record their counting method.
- `nl/platform/platform-families.md` and `en/platform/platform-families.md`:
  the SubGhz paragraph now links to `libraries/core/subghz.md`. The library
  is described there instead of being explained twice.

---

## [2026-07-27] Add NodeMatrix

### Added

- **Node Matrix** (`nl/platform/node-matrix.md`, `en/platform/node-matrix.md`):
  new platform chapter, converted from a standalone HTML page holding the
  sixty devices of the MeshCore web flasher. Until now the repo counted those
  devices per family (`platform/platforms.md`) and discussed four of them at
  length (`gebruik/hardware.md`), but the per-device figures — core, RAM,
  clock speed, radio IC, TX power, display, GPS, link, battery, enclosure and
  price — existed nowhere. The chapter is a reference table, not a buying
  guide, and links to `platforms.md` for the reasoning.
- The seventeen columns of the HTML page are split into four tables keyed on
  the node name — identity and MCU, radio and TX power, peripherals, power and
  price — because a seventeen-column markdown table is unreadable on GitHub.
  The *Link* column of the HTML page was dropped: on all sixty rows it repeats
  exactly those of WiFi, BLE and USB that read *yes*. The boolean columns were
  kept because they also carry *option*, which is what distinguishes the Pico W
  — the hardware is there, the firmware does not build for it — and the Link
  column could not express that.
- Section *To be confirmed* listing all twenty-five devices that carry a `°`,
  with the reservation quoted in the wording of the source. In the HTML page
  this was a tooltip, which markdown has no equivalent for. Dropping it would
  have hidden that roughly 40 % of the rows contain at least one unverified
  value.
- Section *Quick filters*: six derived lists (GPS, display, works without a
  phone app, WiFi, 28 dBm or more, onboard battery) replacing the interactive
  filter chips of the HTML page, which do not survive the conversion.
- A `> [!WARNING]` at table 2 stating that TX power is not permission: the
  value is that of the radio or the power amplifier, not what EU rules allow
  on 868 MHz. Eight of the sixty devices are at 28 dBm or above.
- Both chapters listed in `nl/README.md` and `en/README.md` under *Platform* /
  *Platform*, directly after *De vier platformfamilies* / *The Four Platform
  Families*.
- Five terms added to `nl/naslag/terminology.md` and
  `en/reference/terminology.md`: *18650*, *e-ink*, *Eindtrap (PA)* /
  *Power amplifier (PA)*, *LR1110* and *Standalone*.

### Fixed

- Prices in `nl/gebruik/hardware.md` and `en/usage/hardware.md`, which
  contradicted the node matrix. The matrix leads. T-Deck Plus was €70–80 and
  is now €40–90; Heltec V3/V4 was €20–40 and is now €16–32; RAK WisBlock
  RAK4631 was €40–60 and is now €26–38; Seeed T1000-E was €30–40 and is now
  €32–42. Both the section headings and the comparison table were affected.
- The T-Deck Plus was listed with built-in GPS in `gebruik/hardware.md` and
  `usage/hardware.md`; the matrix marks GPS on the T-Deck as
  version-dependent. Bullet and comparison table now say so.
- The Heltec V4 was listed at 28 dBm TX in both hardware chapters. The matrix
  gives 27 dBm and marks the exact power of the amplifier as unconfirmed; the
  text now states both.

### Changed

- The `> [!NOTE]` about chip versus board in `nl/gebruik/hardware.md` and
  `en/usage/hardware.md` now also points at the node matrix and records that
  the prices and specifications on that page follow it.
- This file gained an `[Unreleased]` section. `CLAUDE.md` prescribes one for
  new entries, but the file only had dated sections; the existing dated
  sections were left untouched.

### Notes

- `nl/platform/node-matrix.md` and `en/platform/node-matrix.md` carry a source
  block stating explicitly that the page is **not** verified against the
  firmware and cannot be: no column comes from `meshcore-dev/MeshCore`. RAM,
  clock speed and link options come from the Nordic, Espressif and Raspberry
  Pi datasheets; radio, display, GPS, battery, enclosure and price from
  manufacturer and community sources; the device list from the saved web
  flasher page of 27 July 2026, the same page `platforms.md` uses. No script
  was added to `tools/`, so the figures are marked as an external source
  instead of being recomputable.
- No new diagrams; `images/nl/` and `images/en/` are unchanged.
- The family split in the matrix — 32 ESP32, 27 nRF52840, 1 RP2040, 0 STM32WL
  — matches the table in `platform/platforms.md` exactly.

---

## [2026-07-28] Add docs about Direct Messages/Platforms

### Added

- **Direct Messages** (`nl/techniek/direct-messages.md`,
  `en/technical/direct-messages.md`): new technical chapter describing the four
  phases of a DM — first message as a scoped flood, PATH reply, learned path,
  acknowledgement — and answering the question why a directly routed DM carries
  no transport code. Until now that question was only touched on in a single
  table row of `regions-and-scopes.md`, without substantiation. The chapter also
  names the flip side: the path discovery around it *is* scoped, so a region
  error breaks DMs to new contacts.
- Both chapters listed in `nl/README.md` and `en/README.md` under
  *Techniek* / *Technical*, directly after *Regio's: bedoeling en praktijk*.
- Three diagrams in `images/nl/` and `images/en/`:
  `direct-messages-1.svg` (the four phases), `direct-messages-2.svg` (the same
  packet in both route types, byte by byte) and `direct-messages-3.svg` (a
  repeater's decision tree, showing that the region branch hangs off the flood
  side only).
- `tools/dm-example.py`: reproduces the DM example from the new chapter —
  plaintext, ciphertext, transport code, both frame lengths and the ACK — using
  the same example data as `tools/example-calculation.py`.
- Seven terms added to `nl/naslag/terminology.md` and
  `en/reference/terminology.md`: *Dest hash / Src hash*, *Direct routing*,
  *Encrypt-then-MAC*, *First packet wins*, *out_path*, *PATH-pakket* and
  *Zero-hop*.
- **MeshCore Platforms** (`nl/techniek/platforms.md`,
  `en/technical/platforms.md`): new technical chapter about the four platform
  families MeshCore builds on — ESP32, nRF52840, RP2040 and STM32WL. It answers
  the question why not every node can do the same thing: the same firmware, but
  different transports, storage, displays, update methods and flash artefacts
  per family. Until now the docs did describe devices (`gebruik/hardware.md`),
  but nowhere the chip behind them.
- The chapter deliberately uses the term *platform* and not *microcontroller*.
  The firmware itself speaks of platforms (`ESP32_PLATFORM`, `NRF52_PLATFORM`,
  `RP2040_PLATFORM`, `STM32_PLATFORM`, `platformio.ini` lines 63, 90, 104, 113),
  and three of the four chips are an SoC and not a bare microcontroller.
- Both chapters listed in `nl/README.md` and `en/README.md` under
  *Techniek* / *Technical*, directly after *SenseCap DFU*.
- Three diagrams in `images/nl/` and `images/en/`: `platforms-1.svg` (the four
  families side by side, showing per family what is and is not there),
  `platforms-2.svg` (a discrete SX1262 over SPI versus the SubGHz radio on the
  STM32WL die) and `platforms-3.svg` (decision tree for platform selection).
- `tools/platform-overview.py`: generates the three count tables from a clone of
  `meshcore-dev/MeshCore` and a saved page of the web flasher, so that the
  chapter stays recomputable at the next release. The script also checks the
  assumptions in the text, such as that `framework = arduino` occurs exactly
  once in the repo.
- Twenty-five terms added to `nl/naslag/terminology.md` and
  `en/reference/terminology.md`: *Arduino-core*, *bootloader*, *build flag*,
  *Cortex-M0+/M4/M4F*, *ESP-IDF*, *ESP-NOW*, *HAL*, *LittleFS*, *LPCOMP*,
  *Platform*, *Platformfamilie*, *PlatformIO environment*, *PSRAM*, *RISC-V*,
  *RP2040*, *SoC*, *SoftDevice*, *SPIFFS*, *ST-Link*, *STM32WLE5*,
  *SubGHz-radio*, *SYSTEMOFF*, *UF2*, *Variant* and *Xtensa*.
- Four external datasheets added to `nl/naslag/references.md` and
  `en/reference/references.md`: RP2040, ESP32 series, nRF52840 and STM32WLE5.
  The RP2040 figures in the chapter come from there and not from the firmware
  repo; a footnote on the table says so as well.
- **De vier platformfamilies** (`nl/platform/platform-families.md`,
  `en/platform/platform-families.md`): new chapter in the `platform/` section,
  holding the four family descriptions — ESP32, nRF52840, RP2040 and STM32WL —
  that used to live in `platforms.md`. Reason for the split: that file served
  two different reading goals. Someone *comparing and choosing* needs different
  text from someone *going deep on one family*, and the two were interleaved. A
  split per processor was considered and rejected: only 29 % of the text can be
  attributed to a single family, so four pages would consist largely of
  boilerplate and the source block would go from two places to ten. The result
  is two full chapters of roughly 1900 and 1050 words, not stubs.
- Both language versions listed in `nl/README.md` and `en/README.md` under a new
  heading *Platform*, between *Techniek* / *Technical* and *Naslag* /
  *Reference*. The two chapters first appeared in the Techniek list; now that
  the `platform/` directory exists, the table of contents follows the directory
  structure. `README.md` and `CLAUDE.md` also name `platform/` in their
  structure overview — the directory was still missing there.
- Four cross-references between the two chapters: from *MeshCore Platforms* to
  *De vier platformfamilies* at the bottom of the introduction and at the end of
  *De vier families in één oogopslag*, and back from the introduction and the
  STM32WL section of the new chapter.

### Changed

- `nl/techniek/regions-and-scopes.md`, `en/technical/regions-and-scopes.md`: the
  table row about direct routes now points to the new chapter for the
  substantiation.
- `nl/gebruik/communication.md`, `en/usage/communication.md`: the *Direct
  Messages* section refers to the technical chapter at the bottom. The user
  story stays here.
- `nl/techniek/key-encryption.md`, `en/technical/key-encryption.md`: the
  *Routing en bevestiging* section points to the new chapter for path learning
  and routing. ECDH stays here, so that no second description arises.
- `nl/gebruik/hardware.md`, `en/usage/hardware.md`: a NOTE block above the
  comparison table separates the two subjects. This page continues to be about
  devices; the chip inside them and what it determines lives in *MeshCore
  Platforms* from now on.
- `nl/naslag/terminology.md`, `en/reference/terminology.md`: the *DFU* entry
  described only the Bluetooth variant. DFU is broader — on STM32 it goes over
  USB — and the entry was widened accordingly.
- `CLAUDE.md`: the conventions were brought in line with the repo. Slugs are
  English and carry no section prefix (the document still prescribed Dutch
  slugs), diagrams live per language in `images/nl/` and `images/en/` under the
  same name (the document described a shared directory with `-en.svg` variants),
  and the file names `terminology.md` and `references.md` were corrected. Added:
  pinning commits in source links instead of `main`, marking external figures,
  and the rule that the repo wins when this document contradicts the repo.
- **MeshCore Platforms** was moved from `nl/techniek/platforms.md` and
  `en/technical/platforms.md` to `nl/platform/platforms.md` and
  `en/platform/platforms.md`. The two platform chapters thereby sit in their own
  `platform/` section, which carries the same name in both language trees. The
  slug `platforms` is unchanged. Links from `nl/README.md`, `en/README.md`,
  `nl/gebruik/hardware.md` and `en/usage/hardware.md` moved with it.
- `nl/platform/platforms.md`, `en/platform/platforms.md`: shortened to the
  comparative part. The four family sections were moved word for word to
  `platform-families.md`; what remains is *waarom het platform uitmaakt*, the
  four families at a glance, the comparison on six axes, the roles table, the
  flasher list, how the firmware absorbs the differences and the selection
  guide. The subtitle became `*VERGELIJKEN · KIEZEN · WAT DE CHIP BEPAALT*`, and
  the introduction no longer promises what now lives on the other page. The
  footnote on the RP2040 figures and the NOTE about the missing mA values stay
  here, with the tables they belong to.
- `images/nl/platforms-2.svg` and `images/en/platforms-2.svg` were renamed to
  `platform-families-1.svg`. The diagram belongs to the new chapter, and the
  convention is `images/<language>/<slug>-<n>.svg`. The contents of the SVG
  files were not changed, only the name and the reference.
- `nl/gebruik/hardware.md`, `en/usage/hardware.md`: the NOTE block above the
  comparison table now points to both chapters — to *MeshCore Platforms* for
  what the chip determines, and to *De vier platformfamilies* for what each
  family contains.
- Not a single figure was changed by this revision. This is a reorganisation of
  existing, already verified text, not a re-verification: the firmware repo was
  not fetched again and `tools/platform-overview.py` was not run again. Both
  chapters pin the same commit `03b6ef4` (28 July 2026, v1.16.0) and note that
  the counts are identical on `a3a1aa5` as well.
- `CLAUDE.md`: file names are now explicitly always English, kebab-case, in the
  Dutch tree as well and for scripts and diagrams too. That was not stated yet:
  the rule applied only to chapter slugs, and for `tools/` it even said the
  opposite — that naming convention prescribed Dutch. The three existing scripts
  and two orphaned SVGs with a `techniek-` prefix do not yet comply and are
  recorded as a pitfall; renaming them touches links in `README.md`,
  `CHANGELOG.md` and four chapters and is a separate assignment. The rule is
  explicitly about files, not directories: directory names follow the section
  mapping, which was extended with `platform` ↔ `platform`.
- The three scripts in `tools/` were renamed to English names:
  `bereken-voorbeeld.py` → `example-calculation.py`, `dm-voorbeeld.py` →
  `dm-example.py` and `platform-overzicht.py` → `platform-overview.py`. The code
  itself was not changed; only two self-references in comments and in the usage
  line were carried along. Also moved were the references in `README.md`,
  `CLAUDE.md`, `nl/techniek/direct-messages.md`,
  `en/technical/direct-messages.md`, the four platform chapters and the caption
  in `images/nl/direct-messages-2.svg` and `images/en/direct-messages-2.svg`,
  where the script name appears in the diagram.

### Fixed

- `nl/gebruik/communication.md`, `en/usage/communication.md`: the warning
  *"Adverts worden NIET doorgestuurd door repeaters. Beide nodes moeten elkaar
  direct kunnen horen voor de key-uitwisseling"* was incorrect. Repeaters do
  forward flood adverts, up to the separate hop limit `flood.max.advert` and at
  reduced priority; only a *zero-hop* advert stays with the neighbours. The old
  text gave readers a wrong picture of how contacts find each other.
- `nl/techniek/key-encryption.md`, `en/technical/key-encryption.md`: the ACK was
  described as *"een 4-byte SHA256-hash"*. For an ordinary DM the ACK payload is
  6 bytes: 4 hash bytes, 1 byte attempt number and 1 random byte, of which only
  the first 4 are compared.
- `nl/techniek/regions-and-scopes.md`, `en/technical/regions-and-scopes.md`,
  `nl/naslag/terminology.md`, `en/reference/terminology.md`: dead links to
  `techniek-locode.md`, a file that is not in the repo. The references now point
  to `regions-in-practice.md`, where the naming agreements live.

---

## [2026-07-27] Removed
- Deleted unlinked files

## [2026-07-27] Major changes

### Added

- **Privacy & Beveiliging** (`nl/gebruik/privacy.md`, `en/usage/privacy.md`):
  its own chapter, split off from `regulations.md`. Covers what is always
  visible (beacons for routing), what is never visible in ISM mode, and the
  comparison table of HAM versus ISM mode.
- **Praktische Toepassingen** (`nl/gebruik/applications.md`,
  `en/usage/applications.md`): its own chapter, split off from
  `what-is-meshcore.md`. Four scenarios: family mesh, Morse club, Amateur Radio
  Mesh and Remote Station.
- Both chapters listed in `nl/README.md` and `en/README.md` under
  *Gebruik* / *Usage*, directly after *Communicatie* / *Communication*.
- **Regelgeving & Duty Cycle** (`nl/gebruik/regulations.md`,
  `en/usage/regulations.md`): new section *Duty cycle in een mesh — wat er
  anders is dan bij een solo-node*. Covers the fact that the duty cycle applies
  per transmitting device and not per network, that forwarded traffic counts
  towards the repeater's own hourly budget, and that one flood message costs one
  transmission at *every* repeater that hears it. With a time-on-air budget
  table (SF7 / BW 62.5 kHz / CR 4/5) and a table of behavioural rules that ease
  the load on the mesh.
- Warning that the MeshCore firmware default `set dutycycle` is **50 %** (and
  the deprecated `set af` is `1.0`, likewise ~50 %), far above both H4 (10 %)
  and H5 (0.1 %). A freshly flashed repeater is non-compliant until
  `set dutycycle 10` has been set. Checked against
  `docs.meshcore.io/cli_commands` (firmware v1.15.0).
- Explanation of why the LBT+AFA escape route is not available to MeshCore in
  the Netherlands: AFA requires frequency agility, whereas MeshCore runs on a
  single fixed carrier.

### Changed

- **Image material separated per language** (`images/nl/`, `images/en/`):
  `images/` was one shared directory, which meant the English chapters showed a
  diagram with Dutch text in 19 of 25 places. Both languages now have their own
  directory with identical file names, so that images follow the same mirroring
  rule as the chapters: only the directory name differs. All 50 references in
  `nl/` and `en/` moved with them; nothing was deleted.
- The `-en` suffix has been dropped. The five `techniek-packets-1..5-en.svg`
  ended up in `images/en/` via `git mv` and are now called
  `packet-structure-1..5.svg`. That suffix was a one-off solution for a single
  chapter series and departed from the agreement that file names are identical
  in both languages.
- **File names to English.** Chapter and image files carried Dutch or half-Dutch
  names (`dode-zone.md`, `techniek-packets-1.svg`) while the English directories
  were already called `usage/`, `technical/` and `reference/`. 22 of the 30
  slugs were renamed, 8 were already English or neutral. The `techniek-` prefix
  was dropped: it repeated the directory name. The 25 diagrams follow their
  chapter, so `techniek-packets-1.svg` → `packet-structure-1.svg`,
  `dode-zone-1.svg` → `dead-zone-1.svg`, `techniek-lagen-1.svg` →
  `layer-model-1.svg`. All via `git mv`, both languages in the same step,
  because `DocsGenerator` only publishes a slug if it exists in `nl/` *and*
  `en/`.
- The underlying agreement is now explicit: **what is shared between the
  languages is in English, what belongs to one language is in that language.**
  File names are shared and therefore English; directory names belong to one
  language and therefore remain `gebruik/` alongside `usage/`.
- **Diagrams in `images/en/` translated.** The translation round has been
  carried out: all diagrams with Dutch text are now in English. 176 text nodes
  changed, accounting for 731 Dutch words. The remaining text nodes in those
  files were already English — code identifiers, register names, hex bytes,
  figures — and were left untouched. `node-types-1.svg` is language-neutral and
  the five `packet-structure` diagrams had already been translated; those six
  were not touched.
- Only the text content inside `<text>` elements was changed. For each file it
  was verified that attributes, coordinates, CSS variables, formatting and byte
  order remained identical.
- The example message *"Op Woensdag a.s. Blauwvingerdagen"* in
  `packet-structure-5.svg` stays untranslated. That is the payload of the
  example packet, not interface text; on the English document page that line is
  untranslated as well.
- README: the structure block shows the new layout, and the count *50 diagrams*
  was corrected to *25 diagrams per language*. The old count included 20 unused
  PNG files.
- Of those 20 PNGs, 10 were regenerated from the translated SVGs, at exactly the
  same size: `18-ble-architecture-1`, `20-channel-structure-psk-1..4`,
  `23-repeater-flow-1..2` and `24-dead-zone-1..3`. The render parameters were
  reconstructed by re-rendering the Dutch SVG and comparing it with the
  original; for the `20-*` series that reproduction is pixel-exact. The two
  `23-repeater-flow` PNGs turned out not to have been rendered at viewBox size
  but at 2770 px wide with a 25 px white margin, and for `-2` with the bottom
  whitespace cropped off.
- The page layout of the website is being followed again: `privacy` and
  `applications` had been merged with `regulations` and `what-is-meshcore`
  respectively during the HTML→markdown migration. That merge has been undone;
  both are separate chapters again, just as on domca.nl. The text was moved
  unchanged — including the corrections made earlier to the encryption line and
  the power row.
- Headings in the split-off chapters from `####` back to `##`, and the page
  title as an H1 again with the subtitle line beneath it, in line with the other
  chapters.
- Configuration block updated from **SF8 to SF7** and extended with the coding
  rate, in line with the current Dutch network parameters (BW 62.5 kHz / SF7 /
  CR 4/5).
- Power row in the ISM/HAM table corrected from `25 mW ERP (EU)` to
  `500 mW e.r.p. (H4) of 25 mW e.r.p. (H5)`; the old value contradicted the
  page's own H4 conclusion.
- Note on the Ebyte E22-900M30S extended: turning the power down happens via the
  PA step, because `set tx` (1–22 dBm) only drives the LoRa chip.

### Fixed

- **Factual error:** the relationship between spreading factor and time-on-air
  was stated the wrong way round (*"lagere spreading factors waar pakketten
  langer in de lucht zijn"*). A *higher* SF gives a longer time-on-air. Both
  language versions.
- Conversion artefacts from the original HTML→markdown migration repaired: the
  duty cycle cards are now a table, and the configuration block and the dBi/dBd
  formulas are no longer glued onto a single line.
- **Count of diagrams to be translated corrected from 18 to 19.**
  `text-to-chirp-5.svg` (formerly `techniek-chirp-5.svg`) had been marked as
  language-neutral, but contains the six-line summary of the chirp chain in
  Dutch (*Tekst → ASCII → Bits*, *Chirp doorloopt alle treden, wrappend bij de
  top*, and so on). Only `node-types-1.svg` is genuinely language-neutral: it
  contains four role labels plus emoji. The diagram was included in the
  translation round after all.
- The figure of *357 tekstnodes* belonged to those 18 files; with the twelve
  nodes of `text-to-chirp-5.svg` added it is 369. Of those, 176 contain Dutch
  text. The estimate of *~1140 woorden* counted all text nodes; the number of
  Dutch words actually translated is 731.
- **Duplicate image names in `images/en/` cleaned up.** The directory held 47
  SVG files for 25 unique diagrams: 22 byte-identical pairs under two naming
  schemes, because the rename to English slugs had been carried out as a copy
  instead of as a move. No diagram was lost — the old names were not a second
  image but an unfinished `git mv`. The English scheme stays; that is what the
  50 references in `nl/` and `en/` actually call. Both directories now contain
  25 SVG files with identical names.
- Internal link `../techniek/techniek-locode.md` in `terminology.md` points to a
  chapter that does not exist, in both language versions. Not yet repaired; see
  *Open punten*.

### Removed

- Section *De exacte specificaties* / *The exact specifications*. Every data
  point in it already appeared in the H-rule table above it, in the opening
  sentence of the same section, or in *Wat is een duty cycle?*. No information
  is lost.

### Fixed (EN-versie)

- Missing section break before *Which regime applies to your node?* restored, so
  that the EN version has the same structure as the NL version.
- Duplicate translation footnote removed and the remaining Dutch-language
  `[!NOTE]` about the deleted calculation aid translated.
- Duplicate translation footnote in `en/usage/what-is-meshcore.md` removed; it
  had been left behind when `applications` was merged in.

### Open punten

- **The 20 PNG files do not follow the new naming scheme.** They still carry the
  numbered scheme from before the directory layout (`18-ble-architecture-1`,
  `24-dead-zone-1`). That scheme is English — it is even the source the current
  slugs were derived from — but the number part refers to a chapter ordering
  that no longer exists. As long as no chapter calls them, that is harmless.
- Ten of the 20 PNG files still contain Dutch text and have no SVG source in the
  directory: `05-group-communication-1` and `-2` (byte-identical to each other),
  `08-practical-applications-1`, `12-text-to-chirp-1..4`,
  `14-lora-modulation-1`, `15-layer-model-1` and `16-remote-control-1`. They
  were made in a different house style from the SVG set and cannot be translated
  without rebuilding them. Their content largely overlaps with the SVG diagrams
  that *are* in use. What happens to them still has to be decided; the git
  history preserves them either way.
- Still to be answered: why were ten unused PNGs regenerated? If they are called
  nowhere, they cost maintenance without any reader seeing them. If they *are*
  used elsewhere — outside this repo — then marking them as *ongebruikt* is
  wrong and that belongs on record here.
- In `16-remote-control-1.png` characters are missing: `[Phone]`, `[Radio]`,
  `[Rot]`, `[Rel]` and `[Rig]` appear on screen as literal placeholders and
  various emoji and check marks render as empty boxes. An existing render
  problem, not a translation matter.
- `terminology.md` links in both languages to `techniek-locode.md`, a chapter
  that does not exist. Either write the chapter or remove the link.

### Voor beheerders van domca.nl

- **`DocsGenerator` has been adjusted and is included.** It created one
  `MarkdownConverter` with a fixed `$imageDir` (`docsRoot/images`), outside the
  language loop, and therefore did not know which language it was working in.
  There is now one converter per language, with
  `$this->docsRoot . '/images/' . $config['dir']`; `self::LANGUAGES` already
  contained the directory names `nl` and `en`. Warning collection runs across
  all converters.
- Added: `controleerBeeldmappen()`, called at the start of `run()`. It reports
  files that are in `images/nl` but not in `images/en` or the other way round.
  Chapters already had that protection; images did not, even though the same
  thing can go wrong there after the split. Visible with `--dry-run`, so before
  it goes live.
- **`MarkdownConverter` has not been reviewed yet.** If it only rewrites paths,
  there is nothing to do. If it copies the files to the web root, then
  `images/nl/layer-model-1.svg` and `images/en/layer-model-1.svg` collide on the
  same target name and the target directory has to be separated per language as
  well.
- **Old fragments remain on the web root.** The generator has no cleanup step,
  so after the rename `content/<old-slug>.html` and `.en.html` are still there.
  That is convenient: `navigateTo()` fetches fragments directly, bypassing the
  menu, so shared links such as `#dode-zone` keep working. They do freeze on the
  content from before the rename, though. Removing them is possible, but then
  those links show *"Deze pagina is nog in ontwikkeling"*.
- Routing runs via `window.location.hash`, so the slug sits behind a `#` and is
  never sent to the server. The rename therefore costs no search rankings.
- `'live-intro'` in `HANDMATIGE_GROEPEN` falls outside the rename and outside
  the menu markers in `index.html`. Unchanged, but it remains manual work.
- **Separate problem: the diagrams do not follow the theme switch.** `router.js`
  sets the theme as `body.light` via `localStorage`, while all 30 SVGs use
  `@media (prefers-color-scheme: dark)`. Those two are not linked: the page
  follows the 🌙☀️ button, the diagrams follow the OS setting. A reader with a
  dark operating system gets dark diagrams on a light page. It does not affect
  the translation, but it does affect every diagram.
