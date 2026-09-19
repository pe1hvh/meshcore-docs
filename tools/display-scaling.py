#!/usr/bin/env python3
"""Genereert docs/images/{nl,en}/display-2.svg — de schaling van de NV3001B.

De drie rechthoeken staan op schaal ten opzichte van elkaar: 1 SVG-eenheid is
1 pixel. Het logische vlak is 128 x 64, het scherm 220 x 128. Het derde vlak
toont hetzelfde raster van 4 bij 2 cellen, een keer op logische maat
(vierkant) en een keer uitgerekt over het scherm (hoger dan breed).

Het stijlblok komt uit .claude/skills/diagram/assets/style-block.txt, zodat
er maar een bron is voor de kleurvariabelen en de donkermodus.

Gebruik:  python3 tools/display-scaling.py [--out docs/images]
"""
import argparse
import os

HIER = os.path.dirname(os.path.abspath(__file__))
STIJL = os.path.join(HIER, '..', '.claude', 'skills', 'diagram', 'assets', 'style-block.txt')
STYLE = open(STIJL, encoding='utf-8').read().rstrip('\n')

LOG_W, LOG_H = 128, 64
SCR_W, SCR_H = 220, 128
COLS, ROWS = 4, 2

TEKST = {
    'nl': {
        'kop': 'NV3001BDisplay — de enige driver die schaalt',
        'a': 'logisch vlak',
        'b': 'scherm',
        'c': 'logisch vlak, uitgerekt',
        'adim': '128 × 64 eenheden',
        'bdim': '220 × 128 pixels',
        'cdim': '× 1,72 horizontaal · × 2 verticaal',
        'slot': 'de verticale rek is groter dan de horizontale: een vierkant in de UI komt hoger dan breed uit',
    },
    'en': {
        'kop': 'NV3001BDisplay — the only driver that scales',
        'a': 'logical area',
        'b': 'screen',
        'c': 'logical area, stretched',
        'adim': '128 × 64 units',
        'bdim': '220 × 128 pixels',
        'cdim': '× 1.72 horizontal · × 2 vertical',
        'slot': 'the vertical stretch is larger than the horizontal: a square in the UI comes out taller than wide',
    },
}

MONO = "'JetBrains Mono',monospace"


def tekst(x, y, s, size=11, anchor='middle', fill='var(--text-secondary)', weight='400'):
    return ('<text x="%s" y="%s" text-anchor="%s" fill="%s" '
            'font-family="%s" font-size="%d" font-weight="%s">%s</text>'
            % (x, y, anchor, fill, MONO, size, weight, s))


def raster(x, y, w, h, fill, stroke):
    uit = ['<rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="%s" stroke="%s" stroke-width="2"/>'
           % (x, y, w, h, fill, stroke)]
    for c in range(1, COLS):
        cx = x + w * c / COLS
        uit.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1"/>'
                   % (cx, y, cx, y + h, stroke))
    for r in range(1, ROWS):
        cy = y + h * r / ROWS
        uit.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1"/>'
                   % (x, cy, x + w, cy, stroke))
    return uit


def bouw(taal):
    t = TEKST[taal]
    ax, bx, cx = 25, 193, 453
    mid = 150
    ay, by, cy = mid - LOG_H // 2, mid - SCR_H // 2, mid - SCR_H // 2

    d = ['<svg style="width:100%;margin:1rem 0" viewBox="0 0 700 310" xmlns="http://www.w3.org/2000/svg">',
         STYLE,
         '<rect x="0" y="0" width="700" height="310" fill="var(--bg)"/>',
         tekst(350, 32, t['kop'], 12, 'middle', 'var(--flow-ink)', '700')]

    d.append(tekst(ax + LOG_W / 2, 68, t['a'], 11, 'middle', 'var(--flow-ink)', '700'))
    d += raster(ax, ay, LOG_W, LOG_H, 'var(--flow-sw-fill)', 'var(--flow-sw-edge)')
    d.append(tekst(ax + LOG_W / 2, ay + LOG_H + 20, t['adim']))

    d.append(tekst(bx + SCR_W / 2, 68, t['b'], 11, 'middle', 'var(--flow-ink)', '700'))
    d.append('<rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="var(--flow-hw-fill)" '
             'stroke="var(--flow-hw-edge)" stroke-width="2"/>' % (bx, by, SCR_W, SCR_H))
    d.append(tekst(bx + SCR_W / 2, by + SCR_H + 20, t['bdim']))

    d.append(tekst(cx + SCR_W / 2, 68, t['c'], 11, 'middle', 'var(--flow-ink)', '700'))
    d += raster(cx, cy, SCR_W, SCR_H, 'var(--flow-sw-fill)', 'var(--flow-sw-edge)')
    d.append('<rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="none" '
             'stroke="var(--flow-hw-edge)" stroke-width="2"/>' % (cx, cy, SCR_W, SCR_H))
    d.append(tekst(cx + SCR_W / 2, cy + SCR_H + 20, t['cdim']))

    for x1, x2 in ((ax + LOG_W + 8, bx - 8), (bx + SCR_W + 8, cx - 8)):
        d.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="var(--line)" stroke-width="1.5"/>'
                 % (x1, mid, x2, mid))

    d.append('<rect x="25" y="258" width="650" height="34" rx="6" fill="var(--code-bg)" '
             'stroke="var(--code-border)" stroke-width="1.5"/>')
    d.append(tekst(350, 279, t['slot'], 11))
    d.append('</svg>')
    return '\n'.join(d) + '\n'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', default='docs/images')
    a = p.parse_args()
    for taal in ('nl', 'en'):
        pad = os.path.join(a.out, taal, 'display-2.svg')
        with open(pad, 'w', encoding='utf-8') as fh:
            fh.write(bouw(taal))
        print('geschreven:', pad)


if __name__ == '__main__':
    main()
