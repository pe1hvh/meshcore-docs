---
paths:
  - "nl/**/*.md"
  - "en/**/*.md"
---

# Chapters

*Page structure, text, source attribution and links.*

### Page structure

- `#` H1 = page title.
- Below it an italic subtitle line in capitals, separated by `·` — for
  example `*HEADER · ROUTE · PATH · PAYLOAD · REGIO-SCOPE*`.
- Then an introductory paragraph (2–5 lines) summarising the whole page.
- Sections with `##`, subsections with `###`. **No `####`** at chapter
  level.
- Technical chapters end with `## Bronnen` (NL) / `## Sources` (EN).
- Every EN chapter ends with the line:
  `Translated from Dutch by Anthropic Claude`.

### Text

- New prose hard-wrapped at ±80 columns. (Older chapters still have long
  lines; wrap what you touch, do not reformat the rest unasked.)
- GitHub alerts: `> [!NOTE]` for clarification and source attribution,
  `> [!WARNING]` for risks and legal warnings.
- Tables with a separator row `|---|---|`; italic rows for fields that are
  strictly speaking out of scope (see `packet-structure.md`).
- Code blocks always with a language tag: ` ```text `, ` ```python `,
  ` ```bash `, ` ```cpp `. The list is not exhaustive; `cpp` is in use in
  `regions-in-practice.md`, `regions-and-scopes.md` and throughout
  `libraries/`.
- **Code quoted from the firmware** carries a line above the block naming the
  file and the line numbers, for example `` `src/Identity.cpp` r.17-23 ``.
  Excerpts are at most ±15 lines and are copied verbatim — nothing rewritten,
  nothing "clarified". Omitted lines become `// ...`. If a fragment is
  unreadable without context, pick a different fragment rather than editing
  it. Line numbers are those of the commit named in the source block; if the
  assignment states different ones, that contradiction goes to the client
  under 🛑 *Stop and ask*.
- Firmware identifiers, file names, commands and hex values in
  `` `backticks` ``.
- Matter-of-fact tone, no marketing language, no superlatives.

### Source attribution in technical chapters

At the top, directly after the introduction:

```markdown
> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `a3a1aa5`, 19 juli 2026 — bestanden
> `src/Packet.h`, `src/Dispatcher.cpp`, en de officiële
> `docs/packet_format.md`.
```

At the bottom a `## Bronnen` list with links to
`https://github.com/meshcore-dev/MeshCore/blob/<commit>/<path>`.

Pin the commit in the link, not `main` — `main` moves and makes the source
attribution inaccurate within weeks.

### Links

- Relative links within the same language tree. **Never** from `nl/` to
  `en/` or the other way round.
- References to the firmware point at the concrete file in
  `meshcore-dev/MeshCore`, not at the repo root.
