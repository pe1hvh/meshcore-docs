---
paths:
  - "nl/naslag/*.md"
  - "en/reference/*.md"
---

# Terminology and reference

*Glossary, source list and link list.*

- `nl/naslag/terminology.md` and `en/reference/terminology.md` are sorted
  **alphabetically** — new terms are inserted in place, not tacked on at
  the bottom.
- If you introduce an abbreviation in a chapter, it also goes into the
  terminology table (both languages).
- New external source → `naslag/references.md` / `reference/references.md`;
  new tool or website → `naslag/links.md` / `reference/links.md`.
- **Adopt the firmware's wording where it is unambiguous.** The repo speaks
  of *platforms* (`ESP32_PLATFORM`, `NRF52_PLATFORM`, `RP2040_PLATFORM`,
  `STM32_PLATFORM`), not of microcontrollers. Use *platform* and *platform
  family* for the four build targets, *MCU* for the chip the firmware runs
  on, and *SoC* for an MCU that is packaged together with memory and usually
  a radio. The difference is explained in `hardware/introduction.md`; do not
  invent a third word for it. If you deliberately
  deviate because the reader's term is different, spell that out in the
  chapter itself — not silently.
