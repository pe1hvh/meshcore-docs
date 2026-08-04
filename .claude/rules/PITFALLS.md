# Known pitfalls

*Open defects and traps that are not tied to one file type.*

Loaded unconditionally: some of these decide whether a chapter may be
shortened at all.

- **The firmware default `set dutycycle` is 50 %**, far above H4 (10 %) and
  H5 (0.1 %). That fact must not be lost when shortening `regulations.md`.
- **Not every chapter has a source block yet.** If it is missing, add it
  when you verify the content; leave it empty if you were unable to check
  anything, rather than guessing a version.
- **`technical` occurs on two levels in the English tree.**
  `en/technical/` is the section that mirrors `nl/techniek/`;
  `en/design/technical/` is the subsection that mirrors
  `nl/ontwerp/technisch/`. They are unrelated. A relative link or an image
  path that resolves one level too high lands in the wrong one without
  erroring, so check the depth rather than the name.
- **MeshCore's `main` moves daily.** Note the commit you are basing
  yourself on, and do not assume that counts from an earlier session still
  hold. Between `a3a1aa5` (19 July 2026) and `03b6ef4` (28 July 2026), for
  instance, two build-target counts already shifted.
