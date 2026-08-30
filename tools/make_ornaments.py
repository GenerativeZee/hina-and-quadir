#!/usr/bin/env python3
"""Generate golden 3D-relief ornaments echoing the printed invitation:
   a string of hanging lanterns, a damask flourish, a laurel date badge,
   and a circular monogram wreath.  Line art, warm gold, soft cast shadow."""
import math

_STOPS = (
    '<stop offset="0" stop-color="#8a5f22"/>'
    '<stop offset=".2" stop-color="#c99433"/>'
    '<stop offset=".4" stop-color="#f1d791"/>'
    '<stop offset=".5" stop-color="#fff6dc"/>'
    '<stop offset=".62" stop-color="#e6c169"/>'
    '<stop offset=".8" stop-color="#b5852f"/>'
    '<stop offset="1" stop-color="#7a521d"/>'
)


def gold_defs(W, H):
    """A diagonal gold sweep in userSpaceOnUse so it paints thin lines too."""
    return (
        f'<linearGradient id="g" gradientUnits="userSpaceOnUse" '
        f'x1="{W*0.1:.0f}" y1="0" x2="{W*0.2:.0f}" y2="{H:.0f}">{_STOPS}</linearGradient>'
        f'<linearGradient id="gv" gradientUnits="userSpaceOnUse" '
        f'x1="0" y1="0" x2="0" y2="{H:.0f}">{_STOPS}</linearGradient>'
    )

SHADOW = (
    '<filter id="d" x="-60%" y="-60%" width="220%" height="220%">'
    '<feDropShadow dx="0" dy="2.4" stdDeviation="2.6" flood-color="#241505" flood-opacity="0.5"/>'
    '</filter>'
    '<filter id="dsoft" x="-80%" y="-80%" width="260%" height="260%">'
    '<feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#241505" flood-opacity="0.38"/>'
    '</filter>'
)


def svg(vb, body, extra_defs=""):
    _, _, W, H = (float(n) for n in vb.split())
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="none">'
        f'<defs>{gold_defs(W, H)}{SHADOW}{extra_defs}</defs>{body}</svg>'
    )


# ─────────────────────────────────────────────────────────────────────
# 1. hanging lantern / ornament string
# ─────────────────────────────────────────────────────────────────────
def ornament(kind, x, drop):
    """Return an ornament hung from y=0 at column x, string length `drop`."""
    s = f'<path d="M{x},0 V{drop}"/>'
    y = drop
    if kind == 'lantern':
        s += f'<path d="M{x-5},{y} h10"/>'
        s += (f'<path d="M{x},{y} C{x-19},{y} {x-19},{y+34} {x},{y+38} '
              f'C{x+19},{y+34} {x+19},{y} {x},{y} Z" fill="url(#g)" fill-opacity=".14"/>')
        for dx in (-9, 0, 9):
            rx = 19 - abs(dx)
            s += f'<path d="M{x},{y+2} C{x+dx-rx*0.2},{y+12} {x+dx-rx*0.2},{y+26} {x},{y+36}"/>'
        s += f'<path d="M{x-6},{y+38} h12"/>'
        s += f'<path d="M{x},{y+38} V{y+48}"/><circle cx="{x}" cy="{y+52}" r="3.2" fill="url(#g)" fill-opacity=".22"/>'
        s += f'<path d="M{x},{y+55} V{y+62}"/>'
    elif kind == 'lamp':
        r = 15
        s += (f'<path d="M{x},{y} l{r},{r} l{-r},{r} l{-r},{-r} Z" fill="url(#g)" fill-opacity=".12"/>')
        s += (f'<path d="M{x},{y+5} l{r-5},{r-5} l{-(r-5)},{r-5} l{-(r-5)},{-(r-5)} Z"/>')
        s += f'<path d="M{x},{y+2*r} V{y+2*r+9}"/><circle cx="{x}" cy="{y+2*r+13}" r="2.6" fill="url(#g)" fill-opacity=".22"/>'
    elif kind == 'fan':
        r = 21
        s += (f'<path d="M{x},{y} m{-r},0 a{r},{r} 0 0 1 {2*r},0 Z" '
              f'fill="url(#g)" fill-opacity=".12"/>')
        for a in range(-60, 61, 24):
            rad = math.radians(a)
            s += f'<path d="M{x},{y} L{x+math.sin(rad)*r:.1f},{y+math.cos(rad)*r:.1f}"/>'
        s += f'<path d="M{x},{y+r+1} V{y+r+8}"/><circle cx="{x}" cy="{y+r+11}" r="2.4" fill="url(#g)" fill-opacity=".22"/>'
    elif kind == 'drop':
        s += (f'<path d="M{x},{y} C{x-11},{y+10} {x-9},{y+30} {x},{y+34} '
              f'C{x+9},{y+30} {x+11},{y+10} {x},{y} Z" fill="url(#g)" fill-opacity=".14"/>')
        s += f'<circle cx="{x}" cy="{y+18}" r="4.5"/>'
        s += f'<path d="M{x},{y+34} V{y+42}"/><circle cx="{x}" cy="{y+45}" r="2.2" fill="url(#g)" fill-opacity=".22"/>'
    elif kind == 'orbs':
        for i, dy in enumerate((0, 9, 18)):
            rr = 6 - i * 1.4
            s += f'<circle cx="{x}" cy="{y+dy+rr}" r="{rr:.1f}" fill="url(#g)" fill-opacity=".16"/>'
    return s


def lantern_string():
    W, H = 1240, 250
    kinds = ['lantern', 'fan', 'lamp', 'drop', 'orbs', 'lantern', 'lamp', 'fan', 'drop', 'lantern', 'orbs']
    drops = [78, 132, 40, 150, 96, 60, 118, 30, 140, 84, 108]
    xs = [40 + i * ((W - 80) / (len(kinds) - 1)) for i in range(len(kinds))]
    inner = '<path d="M0,3 H%d" opacity=".5"/>' % W          # the rail the strings hang from
    for k, x, d in zip(kinds, xs, drops):
        inner += ornament(k, round(x), d)
    body = (f'<g stroke="url(#g)" stroke-width="2.1" stroke-linecap="round" '
            f'stroke-linejoin="round" filter="url(#d)">{inner}</g>')
    return svg(f'0 0 {W} {H}', body)


# ─────────────────────────────────────────────────────────────────────
# 2. damask flourish (mirrored scrolls around a centre palmette)
# ─────────────────────────────────────────────────────────────────────
def damask():
    W, H = 420, 96
    cx, cy = W / 2, H / 2
    half = (
        f'<path d="M{cx},{cy} C{cx-14},{cy-6} {cx-30},{cy-18} {cx-30},{cy-34} '
        f'C{cx-30},{cy-46} {cx-20},{cy-50} {cx-16},{cy-42}"/>'
        f'<path d="M{cx},{cy+2} C{cx-24},{cy+2} {cx-52},{cy-6} {cx-70},{cy-24} '
        f'C{cx-84},{cy-38} {cx-78},{cy-52} {cx-64},{cy-46} '
        f'C{cx-54},{cy-42} {cx-52},{cy-30} {cx-60},{cy-24}"/>'
        f'<path d="M{cx},{cy+6} C{cx-40},{cy+14} {cx-96},{cy+10} {cx-140},{cy-6} '
        f'C{cx-170},{cy-18} {cx-186},{cy-2} {cx-176},{cy+12} '
        f'C{cx-168},{cy+22} {cx-150},{cy+20} {cx-148},{cy+8}"/>'
        f'<circle cx="{cx-150}" cy="{cy+13}" r="2.4" fill="url(#g)" fill-opacity=".3"/>'
        f'<circle cx="{cx-92}" cy="{cy-14}" r="2" fill="url(#g)" fill-opacity=".3"/>'
        f'<path d="M{cx-30},{cy+30} C{cx-44},{cy+30} {cx-54},{cy+20} {cx-52},{cy+8}"/>'
    )
    centre = (
        f'<path d="M{cx},{cy-36} C{cx-9},{cy-24} {cx-9},{cy-8} {cx},{cy+4} '
        f'C{cx+9},{cy-8} {cx+9},{cy-24} {cx},{cy-36} Z" fill="url(#g)" fill-opacity=".16"/>'
        f'<path d="M{cx},{cy+4} V{cy+30}"/>'
        f'<circle cx="{cx}" cy="{cy-40}" r="3.4" fill="url(#g)" fill-opacity=".28"/>'
        f'<circle cx="{cx}" cy="{cy+34}" r="3" fill="url(#g)" fill-opacity=".28"/>'
    )
    body = (
        f'<g stroke="url(#g)" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round" filter="url(#d)">'
        f'{centre}{half}'
        f'<g transform="matrix(-1,0,0,1,{W},0)">{half}</g>'
        f'</g>'
    )
    return svg(f'0 0 {W} {H}', body)


# ─────────────────────────────────────────────────────────────────────
# 3. laurel date badge — two branches curving up around a diamond
# ─────────────────────────────────────────────────────────────────────
def laurel_badge():
    W, H = 340, 240
    cx, cy = W / 2, H / 2
    d = 50
    diamond = (
        f'<path d="M{cx},{cy-d} L{cx+d},{cy} L{cx},{cy+d} L{cx-d},{cy} Z"/>'
        f'<path d="M{cx},{cy-d+9} L{cx+d-9},{cy} L{cx},{cy+d-9} L{cx-d+9},{cy} Z" opacity=".55"/>'
        f'<circle cx="{cx}" cy="{cy-d-9}" r="3.4" fill="url(#g)" fill-opacity=".28"/>'
        f'<circle cx="{cx}" cy="{cy+d+9}" r="3" fill="url(#g)" fill-opacity=".28"/>'
    )

    def sprig(sign):
        # a calm arc hugging the diamond, from bottom to top on one side
        x0, y0 = cx + sign * 10, cy + d + 16
        xm, ym = cx + sign * (d + 52), cy
        x1, y1 = cx + sign * 12, cy - d - 16
        stem = (f'<path d="M{x0:.0f},{y0:.0f} Q{xm:.0f},{y0-6:.0f} {xm:.0f},{ym:.0f} '
                f'Q{xm:.0f},{y1+6:.0f} {x1:.0f},{y1:.0f}"/>')
        leaves = ''
        for t in [i / 10 for i in range(1, 10)]:
            if t < 0.5:
                u = t * 2
                px = (1-u)**2*x0 + 2*(1-u)*u*xm + u*u*xm
                py = (1-u)**2*y0 + 2*(1-u)*u*(y0-6) + u*u*ym
            else:
                u = (t - 0.5) * 2
                px = (1-u)**2*xm + 2*(1-u)*u*xm + u*u*x1
                py = (1-u)**2*ym + 2*(1-u)*u*(y1+6) + u*u*y1
            tang = -70 * (1 if t < .5 else -1)          # rough leaf tilt
            for s2 in (1, -1):
                cx2 = px + sign * 10 * s2
                cy2 = py - 3 * s2
                rot = (35 if s2 > 0 else -35) + (0 if sign > 0 else 180)
                leaves += (f'<ellipse cx="{cx2:.1f}" cy="{cy2:.1f}" rx="8.5" ry="3.6" '
                           f'transform="rotate({rot} {cx2:.1f} {cy2:.1f})" '
                           f'fill="url(#g)" fill-opacity=".18"/>')
        return stem + leaves

    body = (
        f'<g stroke="url(#g)" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round" filter="url(#d)">'
        f'{sprig(-1)}{sprig(1)}{diamond}'
        f'</g>'
    )
    return svg(f'0 0 {W} {H}', body)


# ─────────────────────────────────────────────────────────────────────
# 4. circular monogram wreath
# ─────────────────────────────────────────────────────────────────────
def wreath():
    S = 220
    c = S / 2
    R = 84
    inner = ''
    # two leafy arcs, gap at very top and very bottom
    for side in (-1, 1):
        a0, a1 = (108, 252) if side < 0 else (-72, 72)
        n = 15
        for i in range(n + 1):
            ang = math.radians(a0 + (a1 - a0) * i / n)
            x, y = c + math.cos(ang) * R, c + math.sin(ang) * R
            deg = math.degrees(ang)
            # a pair of slim leaves at each station, angled along the ring
            for k, out in ((0, 1), (1, -1)):
                lx = x + math.cos(ang) * 9 * out
                ly = y + math.sin(ang) * 9 * out
                inner += (f'<ellipse cx="{lx:.1f}" cy="{ly:.1f}" rx="9" ry="3.4" '
                          f'transform="rotate({deg + 90:.1f} {lx:.1f} {ly:.1f})" '
                          f'fill="url(#g)" fill-opacity=".16"/>')
    # two small five-petal roses flanking the bottom gap
    for side in (-1, 1):
        rx, ry = c + side * 18, c + R + 4
        for k in range(5):
            a = math.radians(k * 72 - 90)
            px, py = rx + math.cos(a) * 5.5, ry + math.sin(a) * 5.5
            inner += (f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="4.2" ry="2.4" '
                      f'transform="rotate({k*72:.0f} {px:.1f} {py:.1f})" '
                      f'fill="url(#g)" fill-opacity=".2"/>')
        inner += f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="2.4" fill="url(#g)" fill-opacity=".35"/>'
    # thin guide ring
    inner += f'<circle cx="{c}" cy="{c}" r="{R}" opacity=".3"/>'
    body = (f'<g stroke="url(#g)" stroke-width="1.9" stroke-linecap="round" '
            f'stroke-linejoin="round" filter="url(#d)">{inner}</g>')
    return svg(f'0 0 {S} {S}', body)


OUT = {
    'assets/lantern-string.svg': lantern_string(),
    'assets/damask.svg': damask(),
    'assets/laurel-badge.svg': laurel_badge(),
    'assets/monogram-wreath.svg': wreath(),
}
for path, data in OUT.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)
    print(f'wrote {path}  ({len(data)} bytes)')
