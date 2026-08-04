# Repo tree

*The current layout, one screen.*

Reference, not a rule. Nothing loads this file automatically: it sits
outside `.claude/rules/` on purpose. Read it when you add a directory, a
section or a new chapter, as `CLAUDE.md` instructs. For the conventions
that go with it — directory naming, slugs, the exceptions — see
`.claude/rules/REPO-STRUCTURE.md`.

A `find . -type d -not -path "./.git/*"` reproduces the directory part of
this tree; the annotations are what it does not give you.

```
├── .claude/
│   └── rules/           process rules, loaded by Claude Code
│       ├── STYLE-NUANCE.md       word choice and nuance
│       ├── REPO-STRUCTURE.md     this file
│       ├── PITFALLS.md           open defects and traps
│       ├── CHAPTERS.md           page structure and text
│       ├── IMAGES.md             diagrams and alt text
│       ├── TERMINOLOGY.md        glossary and source lists
│       ├── TOOLS.md              recalculation scripts
│       └── CHANGELOG-COMMITS.md  entry and commit format
├── nl/                  Dutch chapters (source)
│   ├── README.md        table of contents
│   ├── reading-guide.md sections and the background each one assumes
│   ├── gebruik/         usage, hardware, regulations, privacy
│   ├── techniek/        protocol, packets, encryption, repeaters
│   │   └── roomserver/  login, posts, synchronisation, limits
│   ├── ontwerp/         how the firmware is put together
│   │   ├── logisch/     roles, components, contracts, variability
│   │   └── technisch/   classes, platform realisation, build system
│   ├── companion/       how the firmware is put together
│   │   ├── logisch/     roles, components, contracts, variability
│   │   └── technisch/   classes, platform realisation, build system
│   ├── platform/        platform families, chip selection
│   ├── hardware/        what a node is made of
│   │   ├── radio/       transceiver, antenna, link budget
│   │   ├── interfaces/  BLE, WiFi, USB serial, I²C, SPI
│   │   └── peripherals/ display, GPS, buttons and LEDs
│   ├── libraries/       external libraries, dependencies
│   │   ├── core/        one chapter per core library
│   │   └── other/       supporting libraries, grouped by function
│   ├── naslag/          terminology, references, links
│   └── project/         about DOMCA, GitHub overview
├── en/                  English chapters (translation, 1-to-1 mirror)
│   ├── README.md
│   ├── reading-guide.md
│   ├── usage/
│   ├── technical/
│   │   └── roomserver/
│   ├── design/
│   │   ├── logical/
│   │   └── technical/
│   ├── companion/
│   │   ├── logical/
│   │   └── technical/
│   ├── platform/
│   ├── hardware/
│   │   ├── radio/
│   │   ├── interfaces/
│   │   └── peripherals/
│   ├── libraries/
│   │   ├── core/
│   │   └── other/
│   ├── reference/
│   └── project/
├── images/
│   ├── nl/              diagrams (SVG) and photos for the NL chapters
│   └── en/              diagrams (SVG) and photos for the EN chapters
├── tools/               recalculation scripts for the technical chapters
├── README.md            bilingual switchboard: language choice, disclaimer,
│                        layout, licence, community
├── CHANGELOG.md         Keep a Changelog + semver (English only)
└── LICENSE              CC BY-SA 4.0
```
