---
paths:
  - "tools/**/*.py"
---

# Tools

*Recalculation scripts, worked examples and counting traps.*

- The example data is the same project-wide: region `nl-ov-zwo`, channel
  `#zwolle`, sender `PE1HVH`, timestamp `1785412800`, text
  `"Op Woensdag a.s. Blauwvingerdagen"`.
- If an example changes, `tools/example-calculation.py` changes with it —
  and vice versa.
- Every figure in a technical chapter must be reproducible with a script in
  `tools/`, or explicitly marked as an external source. If the text does
  not match the script output, the text is wrong.
- If a chapter generates its tables from the firmware, it ships its own
  script. Naming convention: English, kebab-case, such as
  `tools/example-calculation.py` and `tools/dm-example.py`.

## Counting traps

- **Figures counted over the firmware source tree need their counting method
  recorded.** `tools/library-overview.py` holds a token table for this; the
  chapters cite the figure it produces and the table names the search
  pattern. Figures whose method is unknown cannot be reproduced and must not
  be copied over.
- **Counting build targets by the name of the `[env:…]` section is wrong.**
  A section named `…_room_server` is not proof that the room server is
  compiled, and a target that does compile it need not carry the name —
  `Generic_ESPNOW_room_svr` does not. Count on `build_src_filter` containing
  `../examples/simple_room_server`, and resolve `extends` while doing so: six
  ikoka targets inherit that filter from a shared base section that is not an
  `[env:…]` itself. The naive name count gives 70 targets in 66 directories,
  the correct one 73 in 65. `tools/room-server-overview.py` does it the right
  way; the same trap applies to any other role.
- **`tools/design-overview.py` resolves both inheritance mechanisms.**
  PlatformIO sections inherit through `extends` *and* splice text through
  `${section.option}`; following only one of the two loses 28 of the 508
  build targets. The script also strips CRLF first, because three variant
  files use Windows line endings, and it skips commented-out `-D` macros —
  `MESH_DEBUG` appears 387 times in the ini files and is genuinely enabled in
  36 targets. Its room server count (73 targets in 65 directories) matches
  `tools/room-server-overview.py`, which is the cross-check that the resolver
  is right.
