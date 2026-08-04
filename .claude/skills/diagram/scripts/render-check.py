#!/usr/bin/env python3
"""Renders an SVG with the CSS variables resolved, and flags text overflow.

cairosvg does not resolve CSS custom properties. A plain render of a DOMCA
diagram therefore shows the shapes and none of the text, which makes it
useless as a visual check and actively misleading: an empty canvas looks like
a clean layout.

This script substitutes the light-mode values from the :root block before
rendering, and additionally estimates the width of every <text> element to
report labels that run outside the viewBox.

Usage:
    python3 render-check.py images/nl/filters-1.svg [out.png]
"""
import pathlib
import re
import sys

LIGHT = {
    '--bg': '#FFFFFF',
    '--text-primary': '#0a2540',
    '--text-secondary': '#3d6380',
    '--text-muted': '#7a9bb5',
    '--card-bg': '#f5f9fc',
    '--card-border': '#dbe7f0',
    '--line': '#0096C7',
    '--node': '#0077B6',
    '--grid': '#023E8A',
}
CHAR_W = 0.6  # monospace, fraction of the font size


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix('.check.png')
    svg = src.read_text(encoding='utf-8')

    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if not m:
        sys.exit('no viewBox found')
    width = float(m.group(1))

    problems = []
    for t in re.finditer(r'<text([^>]*)>(.*?)</text>', svg, re.S):
        attrs, body = t.group(1), re.sub(r'<[^>]+>', '', t.group(2))
        if 'rotate' in attrs:
            continue
        x = re.search(r'\bx="([-\d.]+)"', attrs)
        size = re.search(r'font-size="([\d.]+)"', attrs)
        if not x or not size:
            continue
        anchor = re.search(r'text-anchor="(\w+)"', attrs)
        w = len(body.strip()) * float(size.group(1)) * CHAR_W
        left = float(x.group(1))
        if anchor and anchor.group(1) == 'middle':
            left -= w / 2
        elif anchor and anchor.group(1) == 'end':
            left -= w
        if left < 0 or left + w > width:
            problems.append(f'  {body.strip()[:50]!r}  x={left:.0f}..{left + w:.0f}  viewBox 0..{width:.0f}')

    resolved = svg
    for k, v in LIGHT.items():
        resolved = resolved.replace(f'var({k})', v)

    try:
        import cairosvg
    except ImportError:
        sys.exit('cairosvg not installed: pip install cairosvg --break-system-packages')
    cairosvg.svg2png(bytestring=resolved.encode(), write_to=str(out), scale=1.5)

    print(f'rendered: {out}')
    if problems:
        print(f'\n{len(problems)} label(s) outside the viewBox:')
        print('\n'.join(problems))
        sys.exit(1)
    print('no label runs outside the viewBox')
    print('\nNow look at the PNG. Overlap between a label and a shape is not')
    print('detected here.')


if __name__ == '__main__':
    main()
