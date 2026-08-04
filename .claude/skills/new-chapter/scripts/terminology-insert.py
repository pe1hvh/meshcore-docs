#!/usr/bin/env python3
"""Inserts a glossary row and reports which rows it landed between.

Both terminology files are meant to be alphabetical, but en/reference/
terminology.md is not consistently sorted: it has two separate I-clusters and
several rows left in the sort position of their Dutch counterpart. Sorting by
eye therefore puts new rows in the wrong place, which has happened.

This script does not resort the file. It finds the position, inserts, and
prints the neighbours so a human can see whether the result is sensible.

Usage:
    python3 terminology-insert.py nl/naslag/terminology.md "Term" "Meaning"
    python3 terminology-insert.py --after "| Callsign |" en/reference/terminology.md "Term" "Meaning"
"""
import pathlib
import sys


def rows(lines):
    for i, ln in enumerate(lines):
        if ln.startswith('| ') and not ln.startswith('|---') and not ln.startswith('| Term'):
            yield i, ln.split('|')[1].strip()


def main():
    args = sys.argv[1:]
    anchor = None
    if args and args[0] == '--after':
        anchor = args[1]
        args = args[2:]
    if len(args) != 3:
        sys.exit(__doc__)
    path, term, meaning = args
    p = pathlib.Path(path)
    lines = p.read_text(encoding='utf-8').split('\n')
    row = f'| {term} | {meaning} |'

    if anchor:
        hits = [i for i, ln in enumerate(lines) if ln.startswith(anchor)]
        if len(hits) != 1:
            sys.exit(f'anchor matched {len(hits)} rows, expected exactly 1')
        idx = hits[0] + 1
    else:
        key = term.casefold()
        idx = None
        for i, existing in rows(lines):
            if existing.casefold() == key:
                sys.exit(f'{term!r} already exists on line {i + 1}')
            if existing.casefold() > key:
                idx = i
                break
        if idx is None:
            sys.exit('no insertion point found; pass --after "| SomeRow |"')

    lines.insert(idx, row)
    p.write_text('\n'.join(lines), encoding='utf-8')

    before = lines[idx - 1].split('|')[1].strip() if idx > 0 else '(start)'
    after = lines[idx + 1].split('|')[1].strip() if idx + 1 < len(lines) else '(end)'
    print(f'{path}: inserted at line {idx + 1}')
    print(f'  after : {before}')
    print(f'  >>>   : {term}')
    print(f'  before: {after}')
    print('\nCheck those two neighbours. This file is not guaranteed to be')
    print('sorted, so a correct alphabetical position can still look wrong.')


if __name__ == '__main__':
    main()
