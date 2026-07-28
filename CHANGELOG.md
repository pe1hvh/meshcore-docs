# CHANGELOG

All notable changes to meshcore-docs are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).

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
