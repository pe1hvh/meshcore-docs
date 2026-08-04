---
name: diagram
description: Use when creating or editing an SVG diagram for this documentation repo, anything under images/nl/ or images/en/. Supplies the DOMCA style block, the viewBox and font conventions, and a render check that resolves the CSS variables so text and lines are visible in the preview instead of invisible.
---

# Diagrams

Read `.claude/rules/IMAGES.md` for the naming and path rules. This skill
covers the making of the file itself.

## The style block is not optional and not to be retyped

Every diagram carries the same inline `<style>` with the DOMCA variables and
an `@media (prefers-color-scheme: dark)` block. It is in
`assets/style-block.txt`. Copy it verbatim. Do not reconstruct it from another
SVG by hand, and do not copy it from `images/nl/dead-zone-1.svg` — that file
predates the convention and lacks both the `style` attribute and the font
family.

## The skeleton

```
<svg style="width:100%;margin:1rem 0" viewBox="0 0 680 <height>"
     xmlns="http://www.w3.org/2000/svg">
<style> … from assets/style-block.txt … </style>
<rect x="0" y="0" width="680" height="<height>" fill="var(--bg)"/>

<title>Short title</title>
…
</svg>
```

- `viewBox` around 680 units wide. Anything wider gets scaled down and the
  text stops being readable at column width.
- All colours through `var(--…)`. The accent fill in use is `#F59E0B` with
  stroke `#854F0B`.
- Every `<text>` carries `font-family="'JetBrains Mono',monospace"`.
- Minimum font size 11. Labels 12, headings 13 with `font-weight="600"`.
- Monospace is roughly 0.6 em per character: at size 12 that is 7.2 px. Use
  that to check a label fits before you place it.

## Always run the render check

`scripts/render-check.py <file.svg>` writes a PNG with the CSS variables
resolved to their light-mode values, and reports any text that runs outside
the viewBox.

This step exists because of a specific failure: `cairosvg` does not resolve
CSS custom properties, so a plain render shows the coloured shapes and nothing
else. Three diagrams were checked that way and passed, while one label ran off
the canvas, another sat on top of a shape, and a third carried a figure that
contradicted the chapter.

Look at the PNG. Do not conclude anything from a render in which the text is
invisible.

## Both languages

A diagram exists twice, under the same name, in `images/nl/` and
`images/en/` — even when it contains no text. Generate both from one script so
they cannot drift apart; only the strings differ.
