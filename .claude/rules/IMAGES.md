---
paths:
  - "images/**"
---

# Images

*Paths, naming, alt text and the SVG convention.*

- Path from an NL chapter: `../../images/nl/<slug>-<n>.svg`.
- Path from an EN chapter: `../../images/en/<slug>-<n>.svg`.
- Path from a chapter on the third level (`libraries/core/`,
  `libraries/other/`, `hardware/radio/`, `hardware/interfaces/`,
  `hardware/peripherals/`, `techniek/roomserver/`, `ontwerp/logisch/` ↔
  `design/logical/`, `ontwerp/technisch/` ↔ `design/technical/`):
  `../../../images/nl/<slug>-<n>.svg` and
  `../../../images/en/<slug>-<n>.svg`. The image directory itself stays
  flat — no `images/nl/libraries/`.
- Both files always exist and carry the same name. If the diagram contains
  no text, the EN version is an identical copy.
- **`images/` is flat.** A slug that occurs in more than one section — such as
  `introduction` — therefore cannot use `<slug>-<n>.svg` twice. The second
  diagram is named after what it shows, not after the chapter it sits in:
  `node-blockdiagram-1.svg` for `hardware/introduction.md`. Image files are
  never moved or renamed to resolve this; only new files pick a different
  name.
- Alt text is descriptive and readable on its own — not
  `Diagram 1 bij layer-model`.
- **New diagrams as SVG**, not as PNG.
- SVG convention (see `images/nl/layer-model-1.svg` as a reference):
  `style="width:100%;margin:1rem 0"`, a `viewBox`, an embedded `<style>`
  with `:root` variables plus an `@media (prefers-color-scheme: dark)`
  block, all colours via `var(--…)`, text in `'JetBrains Mono',monospace`.

## Open defects

- **Alt texts do not yet meet the project's own rule.** Several chapters
  use `![Diagram 1 bij …](…)`. New chapters get it right; existing ones are
  picked up at the next substantive change.
- **Two naming styles in `images/`.** Legacy PNGs with a number prefix
  (`20-channel-structure-psk-1.png`) alongside SVGs with a chapter slug
  (`channel-structure-1.svg`). New files follow the slug style.
