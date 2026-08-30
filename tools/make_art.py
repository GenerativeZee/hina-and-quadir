#!/usr/bin/env python3
"""
Procedural SVG art generator for the Nikkah invitation.

Everything is drawn as OPEN OUTLINES (no fills). Each motif is then painted
three times - a warm shadow offset down-right, a white highlight offset
up-left, and the paper colour dead centre - which reads as a real blind
emboss pressed into cotton stock.
"""
import math, random, os

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)
R = random.Random


def _f(v):
    return f"{v:.1f}"


# ---------------------------------------------------------------- primitives

def petal(cx, cy, a, r_in, r_out, spread, bulge=1.35):
    """One open petal loop springing outward from the flower centre."""
    a1, a2 = a - spread, a + spread
    x1, y1 = cx + math.cos(a1) * r_in, cy + math.sin(a1) * r_in
    x2, y2 = cx + math.cos(a2) * r_in, cy + math.sin(a2) * r_in
    tx, ty = cx + math.cos(a) * r_out, cy + math.sin(a) * r_out
    c1x = cx + math.cos(a1) * r_out * bulge
    c1y = cy + math.sin(a1) * r_out * bulge
    c2x = cx + math.cos(a2) * r_out * bulge
    c2y = cy + math.sin(a2) * r_out * bulge
    return (f'<path d="M{_f(x1)},{_f(y1)} C{_f(c1x)},{_f(c1y)} {_f(tx)},{_f(ty)} '
            f'{_f(tx)},{_f(ty)} C{_f(tx)},{_f(ty)} {_f(c2x)},{_f(c2y)} {_f(x2)},{_f(y2)}"/>')


def rose(cx, cy, r, rot=0.0):
    """Layered garden rose: three rings of petals wrapped round a spiral heart."""
    p = []
    for scale, n, inner in ((1.00, 8, .46), (.70, 6, .40), (.46, 5, .34)):
        rr = r * scale
        off = rot + scale * 3.1
        for i in range(n):
            a = off + i * (2 * math.pi / n)
            p.append(petal(cx, cy, a, rr * inner, rr, math.pi / n * .92))
    pts = []
    for i in range(30):
        t = i / 29
        a = t * 3.9 * math.pi + rot
        rad = r * .30 * (1 - t * .94)
        pts.append(f"{_f(cx + math.cos(a)*rad)},{_f(cy + math.sin(a)*rad)}")
    p.append(f'<polyline points="{" ".join(pts)}"/>')
    return "".join(p)


def blossom(cx, cy, r, rot=0.0, n=5):
    p = [petal(cx, cy, rot + i * (2 * math.pi / n), r * .22, r, math.pi / n * .95, 1.5)
         for i in range(n)]
    p.append(f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(r*.16)}"/>')
    return "".join(p)


def bud(cx, cy, r, a):
    x2, y2 = cx + math.cos(a) * r * 1.9, cy + math.sin(a) * r * 1.9
    return (f'<ellipse cx="{_f(cx)}" cy="{_f(cy)}" rx="{_f(r*.62)}" ry="{_f(r)}" '
            f'transform="rotate({_f(math.degrees(a)+90)} {_f(cx)} {_f(cy)})"/>'
            f'<path d="M{_f(cx)},{_f(cy)} L{_f(x2)},{_f(y2)}"/>')


def leaf(cx, cy, ln, ang, w=.34):
    a = math.radians(ang)
    tx, ty = cx + math.cos(a) * ln, cy + math.sin(a) * ln
    nx, ny = -math.sin(a), math.cos(a)
    mx, my = cx + math.cos(a) * ln * .45, cy + math.sin(a) * ln * .45
    ow = ln * w
    return (f'<path d="M{_f(cx)},{_f(cy)} Q{_f(mx+nx*ow)},{_f(my+ny*ow)} {_f(tx)},{_f(ty)} '
            f'Q{_f(mx-nx*ow)},{_f(my-ny*ow)} {_f(cx)},{_f(cy)} Z"/>'
            f'<path d="M{_f(cx)},{_f(cy)} L{_f(tx)},{_f(ty)}"/>')


def vine(x0, y0, x1, y1, bend, leaves=6, lsize=13, seed=0, buds=True):
    rnd = R(seed)
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    c1 = (x0 + dx * .30 + nx * bend, y0 + dy * .30 + ny * bend)
    c2 = (x0 + dx * .70 + nx * bend, y0 + dy * .70 + ny * bend)
    out = [f'<path d="M{_f(x0)},{_f(y0)} C{_f(c1[0])},{_f(c1[1])} '
           f'{_f(c2[0])},{_f(c2[1])} {_f(x1)},{_f(y1)}"/>']

    def bez(t):
        u = 1 - t
        return (u**3*x0 + 3*u*u*t*c1[0] + 3*u*t*t*c2[0] + t**3*x1,
                u**3*y0 + 3*u*u*t*c1[1] + 3*u*t*t*c2[1] + t**3*y1)

    for i in range(leaves):
        t = .12 + (i / max(1, leaves - 1)) * .84
        bx, by = bez(t)
        nx2, ny2 = bez(min(1, t + .02))
        base = math.degrees(math.atan2(ny2 - by, nx2 - bx))
        out.append(leaf(bx, by, lsize * rnd.uniform(.70, 1.18), base + (54 if i % 2 else -54)))
        if buds and i % 3 == 1:
            out.append(blossom(nx2, ny2, lsize * .34, rnd.uniform(0, 6)))
        elif buds and i % 5 == 3:
            out.append(bud(nx2, ny2, lsize * .22, math.radians(base)))
    out.append(f'<path d="M{_f(x1)},{_f(y1)} c{_f(nx*lsize*1.2)},{_f(ny*lsize*1.2)} '
               f'{_f(nx*lsize*.4+dx*.04)},{_f(ny*lsize*.4+dy*.04)} '
               f'{_f(dx*.07)},{_f(dy*.07)}"/>')
    return "".join(out)


# ---------------------------------------------------------------- emboss wrap

def emboss(w, h, motif, paper="#EFE0D4", hi="#FFFFFF", sh="#B0917C",
           depth=1.6, hi_op=.9, sh_op=.40, sw=2.0, bg=True, slice_=True):
    bgr = f'<rect x="-2" y="-2" width="{w+4}" height="{h+4}" fill="{paper}"/>' if bg else ""
    par = ' preserveAspectRatio="xMidYMid slice"' if slice_ else ""
    uid = f"m{abs(hash(motif)) % 100000}"

    def layer(dx, dy, col, op, width):
        return (f'<use href="#{uid}" transform="translate({dx},{dy})" stroke="{col}" '
                f'stroke-width="{width}" opacity="{op}"/>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"{par}>'
            f'<defs><g id="{uid}">{motif}</g></defs>'
            f'<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
            f'{bgr}{layer(depth, depth, sh, sh_op, sw)}'
            f'{layer(-depth*.9, -depth*.9, hi, hi_op, sw)}'
            f'{layer(0, 0, paper, 1, sw * 1.05)}</g></svg>')


# ---------------------------------------------------------------- compositions

def cluster(cx, cy, s, seed, arms=8, reach=1.0):
    rnd = R(seed)
    out = [rose(cx, cy, 27 * s, rnd.uniform(0, 6)),
           rose(cx - 36 * s, cy + 18 * s, 18 * s, rnd.uniform(0, 6)),
           rose(cx + 35 * s, cy + 14 * s, 19 * s, rnd.uniform(0, 6)),
           rose(cx + 4 * s, cy - 34 * s, 15 * s, rnd.uniform(0, 6)),
           blossom(cx - 20 * s, cy - 26 * s, 10 * s, rnd.uniform(0, 6)),
           blossom(cx + 26 * s, cy - 22 * s, 9 * s, rnd.uniform(0, 6)),
           blossom(cx - 4 * s, cy + 34 * s, 9 * s, rnd.uniform(0, 6))]
    step = 360 / arms
    for k in range(arms):
        ang = k * step + rnd.uniform(-11, 11)
        a = math.radians(ang)
        ln = 100 * s * reach * rnd.uniform(.74, 1.22)
        out.append(vine(cx + math.cos(a) * 22 * s, cy + math.sin(a) * 22 * s,
                        cx + math.cos(a) * ln, cy + math.sin(a) * ln,
                        26 * s * rnd.choice((-1, 1)), leaves=6,
                        lsize=13.5 * s, seed=seed * 31 + k))
    return "".join(out)


def envelope_panel():
    """Dense all-over floral sheet, heaviest at the top and bottom thirds."""
    W, H = 900, 1400
    m = [cluster(450, 175, 1.60, 1),
         cluster(450, 1215, 1.60, 2),
         cluster(126, 700, 1.05, 3),
         cluster(776, 700, 1.05, 4),
         cluster(230, 372, .82, 5),
         cluster(672, 374, .82, 6),
         cluster(224, 1024, .82, 7),
         cluster(676, 1026, .82, 8),
         cluster(450, 560, .70, 9, arms=7),
         cluster(450, 845, .70, 10, arms=7),
         cluster(60, 120, .74, 11),
         cluster(842, 122, .74, 12),
         cluster(62, 1280, .74, 13),
         cluster(840, 1282, .74, 14)]
    rnd = R(77)
    for i in range(70):
        x, y = rnd.uniform(10, 890), rnd.uniform(10, 1390)
        k = rnd.random()
        if k < .42:
            m.append(blossom(x, y, rnd.uniform(6, 12), rnd.uniform(0, 6)))
        elif k < .70:
            m.append(leaf(x, y, rnd.uniform(14, 26), rnd.uniform(0, 360)))
        elif k < .86:
            m.append(bud(x, y, rnd.uniform(4, 7), rnd.uniform(0, 6)))
        else:
            m.append(vine(x, y, x + rnd.uniform(-70, 70), y + rnd.uniform(-70, 70),
                          rnd.uniform(-24, 24), leaves=4, lsize=11, seed=i))
    return emboss(W, H, "".join(m), sw=1.9)


def corner_spray(seed=11, flip=False):
    W = H = 560
    rnd = R(seed)
    m = [rose(126, 112, 42, .4), rose(224, 62, 28, 1.2), rose(56, 214, 26, 2.1),
         rose(196, 176, 20, 3.0),
         blossom(96, 40, 14, 2.4), blossom(278, 130, 12, 1.1),
         blossom(40, 118, 12, .5), bud(250, 208, 8, 1.0)]
    for a, ln in ((16, 380), (44, 340), (72, 300), (2, 280), (330, 170), (98, 250)):
        m.append(vine(140, 132, 140 + math.cos(math.radians(a)) * ln,
                      132 + math.sin(math.radians(a)) * ln, 48, leaves=8,
                      lsize=20, seed=seed + a))
    for i in range(10):
        m.append(blossom(rnd.uniform(20, 380), rnd.uniform(20, 330),
                         rnd.uniform(5, 9), rnd.uniform(0, 6)))
    body = "".join(m)
    if flip:
        body = f'<g transform="translate({W},0) scale(-1,1)">{body}</g>'
    return emboss(W, H, body, paper="#F7ECE2", hi="#FFFFFF", sh="#BB9C84",
                  depth=1.5, sh_op=.46, sw=2.0, bg=False, slice_=False)


# ---------------------------------------------------------------- gold line art

def gold(w, h, motif, sw=2.0, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
            f'<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="0" x2="{w}" y2="{h}">'
            f'<stop offset="0" stop-color="#D8B476"/><stop offset=".34" stop-color="#B4884A"/>'
            f'<stop offset=".60" stop-color="#EDD5A4"/><stop offset="1" stop-color="#A2763E"/>'
            f'</linearGradient></defs>{extra}'
            f'<g fill="none" stroke="url(#g)" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{motif}</g></svg>')


def arch_points(cx, base_y, w, h, n=60):
    """Sample a two-centred pointed (Mughal) arch from left springline to right."""
    half = w / 2
    d = max((h * h - half * half) / w, 0.001)   # horizontal offset of the two centres
    Rr = half + d
    left_c = (cx + d, base_y)
    a_start = math.pi                                   # left springline
    a_end = math.atan2(-h, -d)                          # apex
    while a_end <= a_start:                             # always sweep up and over
        a_end += 2 * math.pi
    pts = []
    for i in range(n + 1):
        a = a_start + (a_end - a_start) * (i / n)
        pts.append((left_c[0] + math.cos(a) * Rr, left_c[1] + math.sin(a) * Rr))
    mirrored = [(2 * cx - x, y) for x, y in reversed(pts[:-1])]
    return pts + mirrored


def cusped_arch(cx, base_y, w, h, cusps=11, bulge=1.0, close_base=False, sweep=1):
    """Multifoil arch: the pointed profile broken into scalloped foils."""
    pts = arch_points(cx, base_y, w, h, cusps)
    d = [f"M{_f(pts[0][0])},{_f(pts[0][1])}"]
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]
        x1, y1 = pts[i]
        chord = math.hypot(x1 - x0, y1 - y0)
        r = max(chord / 2 * bulge, chord / 2 + .01)
        d.append(f"A{_f(r)},{_f(r)} 0 0 {sweep} {_f(x1)},{_f(y1)}")
    if close_base:
        d.append("Z")
    return f'<path d="{" ".join(d)}"/>'


def plain_arch(cx, base_y, w, h, drop=0):
    pts = arch_points(cx, base_y, w, h, 40)
    d = [f"M{_f(pts[0][0])},{_f(pts[0][1] + drop)}",
         f"L{_f(pts[0][0])},{_f(pts[0][1])}"]
    d += [f"L{_f(x)},{_f(y)}" for x, y in pts[1:]]
    d.append(f"L{_f(pts[-1][0])},{_f(pts[-1][1] + drop)}")
    return f'<path d="{" ".join(d)}"/>'


def divider():
    """Fine gold rule: a rose at the centre with leafed vines tapering outward."""
    W, H = 660, 110
    cx, cy = W / 2, H / 2
    p = [rose(cx, cy, 15, .6)]
    for s in (-1, 1):
        p.append(vine(cx + s * 17, cy, cx + s * 150, cy - 10, -16 * s,
                      leaves=6, lsize=13, seed=int(4 + s), buds=True))
        p.append(vine(cx + s * 17, cy, cx + s * 132, cy + 12, 14 * s,
                      leaves=5, lsize=11, seed=int(9 + s), buds=False))
        p.append(f'<path d="M{_f(cx+s*150)},{_f(cy-8)} H{_f(cx+s*300)}"/>')
        p.append(f'<circle cx="{_f(cx+s*310)}" cy="{_f(cy-8)}" r="3.5"/>')
        p.append(blossom(cx + s * 120, cy - 22, 8, 1.1))
    return gold(W, H, "".join(p), 1.5)


def arch_ornament():
    """Small filigree multifoil arch used to punctuate the timeline."""
    W, H = 250, 300
    p = [plain_arch(125, 268, 186, 168),
         cusped_arch(125, 262, 158, 142, cusps=9, bulge=1.02),
         rose(125, 168, 20, .3),
         blossom(125, 128, 10, .8),
         f'<path d="M22,272 H228"/>',
         f'<path d="M30,280 H220"/>',
         '<circle cx="125" cy="292" r="4"/>']
    for s_ in (-1, 1):
        p.append(f'<path d="M{_f(125+s_*20)},176 c{_f(s_*22)},14 {_f(s_*30)},34 {_f(s_*30)},62"/>')
        p.append(blossom(125 + s_ * 52, 244, 8, 1.4))
    return gold(W, H, "".join(p), 1.9)


def crest():
    """Laurel crest that sits above the couple's names."""
    W, H = 360, 150
    cx, base = 180, 126
    p = [rose(cx, 60, 20, .9), blossom(cx, 26, 12, .4)]
    for s in (-1, 1):
        p.append(vine(cx + s * 14, 66, cx + s * 148, base - 6, -34 * s,
                      leaves=8, lsize=15, seed=int(31 + s)))
        p.append(vine(cx + s * 12, 74, cx + s * 104, base + 6, 20 * s,
                      leaves=5, lsize=11, seed=int(51 + s), buds=False))
        p.append(f'<circle cx="{_f(cx+s*158)}" cy="{_f(base-4)}" r="3.5"/>')
    return gold(W, H, "".join(p), 1.6)


def lantern():
    """Hanging masjid lantern with a multifoil window."""
    W, H = 130, 330
    p = ['<path d="M65,0 V22"/>', '<circle cx="65" cy="28" r="6"/>',
         '<path d="M65,34 V44"/>',
         '<path d="M43,68 C43,54 52,44 65,44 C78,44 87,54 87,68"/>',
         '<path d="M31,68 H99"/>', '<path d="M35,80 H95"/>',
         '<path d="M38,80 V184"/>', '<path d="M92,80 V184"/>',
         '<path d="M38,184 L65,248 L92,184"/>',
         '<path d="M35,184 H95"/>',
         '<path d="M38,100 H92"/>',
         cusped_arch(65, 176, 40, 60, cusps=7, bulge=1.02),
         '<path d="M45,176 H85"/>',
         '<path d="M65,248 V262"/>', '<circle cx="65" cy="270" r="7"/>',
         '<path d="M65,277 V292"/>', '<circle cx="65" cy="296" r="3"/>']
    return gold(W, H, "".join(p), 1.9)


def wax_seal():
    """Champagne wax seal with an irregular poured edge and a beaded inner ring.
    The monogram itself is HTML text laid over this, so it stays editable."""
    S = 300
    c = S / 2
    rnd = R(7)
    pts = []
    n = 46
    for i in range(n):
        a = i * 2 * math.pi / n
        wob = 1 + math.sin(a * 5.3 + .7) * .022 + math.sin(a * 9.1 + 2.2) * .014
        rr = 118 * wob * rnd.uniform(.985, 1.015)
        pts.append((c + math.cos(a) * rr, c + math.sin(a) * rr))
    d = [f"M{_f(pts[0][0])},{_f(pts[0][1])}"]
    for i in range(n):
        p0, p1 = pts[i], pts[(i + 1) % n]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        d.append(f"Q{_f(p0[0])},{_f(p0[1])} {_f(mx)},{_f(my)}")
    d.append("Z")
    blob = " ".join(d)

    beads = "".join(
        f'<circle cx="{_f(c + math.cos(i*2*math.pi/44)*88)}" '
        f'cy="{_f(c + math.sin(i*2*math.pi/44)*88)}" r="2" fill="#B0904F" opacity=".6"/>'
        for i in range(44))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}">
<defs>
<radialGradient id="wax" cx=".36" cy=".30" r=".82">
<stop offset="0" stop-color="#FDF4E0"/><stop offset=".38" stop-color="#F1DEB6"/>
<stop offset=".72" stop-color="#DEC28E"/><stop offset="1" stop-color="#C2A26A"/>
</radialGradient>
<radialGradient id="dish" cx=".42" cy=".36" r=".75">
<stop offset="0" stop-color="#DCC094"/><stop offset=".55" stop-color="#EBDAB2"/>
<stop offset="1" stop-color="#F8EED4"/>
</radialGradient>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
<feGaussianBlur stdDeviation="4"/></filter>
</defs>
<path d="{blob}" transform="translate(3,7)" fill="#7A5326" opacity=".28" filter="url(#soft)"/>
<path d="{blob}" fill="url(#wax)"/>
<path d="{blob}" fill="none" stroke="#B08F55" stroke-width="1.4" opacity=".4"/>
<circle cx="{c}" cy="{c}" r="97" fill="none" stroke="#C2A26A" stroke-width="1.8" opacity=".42"/>
<circle cx="{c}" cy="{c}" r="93" fill="url(#dish)" opacity=".92"/>
<circle cx="{c}" cy="{c}" r="93" fill="none" stroke="#FBEBC6" stroke-width="1.2" opacity=".6"/>
{beads}
<ellipse cx="{c-34}" cy="{c-44}" rx="40" ry="26" fill="#FFF6DF" opacity=".26"
 filter="url(#soft)" transform="rotate(-28 {c-34} {c-44})"/>
</svg>'''


if __name__ == "__main__":
    files = {
        "envelope-emboss.svg": envelope_panel(),
        "corner-spray.svg": corner_spray(11, False),
        "corner-spray-flip.svg": corner_spray(11, True),
        "divider.svg": divider(),
        "arch-ornament.svg": arch_ornament(),
        "crest.svg": crest(),
        "lantern.svg": lantern(),
        "seal.svg": wax_seal(),
    }
    for name, data in files.items():
        with open(os.path.join(OUT, name), "w") as f:
            f.write(data)
        print(f"{name:26} {len(data)/1024:7.1f} KB")
