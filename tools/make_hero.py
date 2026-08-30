#!/usr/bin/env python3
"""Hand-built hero art for the opening page — a soft ivory vista through a
carved arch, glowing jhoomar lanterns and cream corner florals.  Palette
matches the rest of the site (ivory / paper / warm ink / gold)."""
import math

# ── shared palette — the site tokens ─────────────────────────────
CREAM   = "#FBF4EA"    # --ivory
IVORY   = "#F1E6D2"
IVORY_D = "#DECBA6"    # shadow side
IVORY_L = "#FEF9EE"    # lit side
GOLD    = "#946323"    # --gold
GOLD_D  = "#573914"    # --gold-deep
GOLD_L  = "#D9B87C"    # --gold-lt
SKY_TOP = "#EFE4CF"
SKY_MID = "#F6EEDC"
SKY_LOW = "#FBF4E6"
SUN     = "#FFFCF3"
BLUSH   = "#F7ECDD"


def w(path, s):
    open(path, "w", encoding="utf-8").write(s)
    print("wrote", path, len(s), "bytes")


# ══════════════════════════════════════════════════════════════════
# 1. the vista seen through the arch — sky, sun, mosque, reflection
# ══════════════════════════════════════════════════════════════════
def vista():
    W, H = 1000, 1560
    horizon = H * 0.72
    cx = W / 2
    M = 0.72                                   # overall mosque scale

    DBASE, DLIT, DSHAD, DTIP = "#ECDFC4", "#FEFAF0", "#DCCAA6", "#F3EAD6"

    def dome(dcx, base, rw, rh):
        # a soft onion dome: pale ivory, a gentle lit crescent, a soft shadow
        top = base - rh * 1.62
        return (
            f'<path d="M{dcx-rw},{base} C{dcx-rw},{base-rh*1.12} {dcx-rw*0.55},{base-rh*1.55} {dcx},{top} '
            f'C{dcx+rw*0.55},{base-rh*1.55} {dcx+rw},{base-rh*1.12} {dcx+rw},{base} Z" fill="{DBASE}"/>'
            f'<path d="M{dcx},{top} C{dcx+rw*0.52},{base-rh*1.5} {dcx+rw},{base-rh*1.05} {dcx+rw},{base} '
            f'C{dcx+rw*0.5},{base} {dcx+rw*0.2},{base-rh*0.7} {dcx+rw*0.1},{top+rh*0.2} Z" fill="{DLIT}" opacity=".85"/>'
            f'<path d="M{dcx-rw},{base} C{dcx-rw},{base-rh*1.12} {dcx-rw*0.62},{base-rh*1.5} {dcx-rw*0.2},{top+rh*0.15} '
            f'C{dcx-rw*0.4},{base-rh*0.7} {dcx-rw*0.7},{base-rh*0.3} {dcx-rw*0.55},{base} Z" fill="{DSHAD}" opacity=".8"/>'
            f'<path d="M{dcx},{top} C{dcx-rw*0.15},{top-rh*0.18} {dcx-rw*0.09},{top-rh*0.34} {dcx},{top-rh*0.46} '
            f'C{dcx+rw*0.09},{top-rh*0.34} {dcx+rw*0.15},{top-rh*0.18} {dcx},{top} Z" fill="{DTIP}"/>'
            f'<rect x="{dcx-2.2}" y="{top-rh*0.46-rh*0.18}" width="4.4" height="{rh*0.2}" fill="{GOLD}"/>'
            f'<circle cx="{dcx}" cy="{top-rh*0.46-rh*0.2}" r="3.6" fill="{GOLD_L}"/>'
        )

    def minaret(mcx, base, top, wd):
        return (
            f'<rect x="{mcx-wd/2}" y="{top}" width="{wd}" height="{base-top}" fill="url(#minG)"/>'
            f'<rect x="{mcx-wd*0.8}" y="{top+(base-top)*0.30}" width="{wd*1.6}" height="{wd*0.55}" fill="{DBASE}"/>'
            f'<rect x="{mcx-wd*0.8}" y="{top+(base-top)*0.58}" width="{wd*1.6}" height="{wd*0.55}" fill="{DBASE}"/>'
            + dome(mcx, top, wd*1.0, wd*1.15)
            + f'<rect x="{mcx-wd*0.95}" y="{top-3}" width="{wd*1.9}" height="{wd*0.5}" rx="2" fill="{DLIT}"/>'
        )

    def y(v):  return horizon - v * M          # height above horizon, scaled
    def s(v):  return v * M                     # scaled length

    mos = ''
    mos += minaret(cx-s(360), horizon, y(620), s(30))
    mos += minaret(cx+s(360), horizon, y(620), s(30))
    mos += minaret(cx-s(250), horizon, y(520), s(24))
    mos += minaret(cx+s(250), horizon, y(520), s(24))
    mos += f'<rect x="{cx-s(235)}" y="{y(210)}" width="{s(470)}" height="{s(210)}" fill="{DBASE}"/>'
    mos += f'<path d="M{cx-s(248)},{y(210)} H{cx+s(248)} L{cx+s(218)},{y(262)} H{cx-s(218)} Z" fill="{DTIP}"/>'
    for i in range(-4, 5):
        ax = cx + i*s(54)
        mos += (f'<path d="M{ax-s(20)},{horizon} V{y(96)} A{s(20)},{s(26)} 0 0 1 {ax+s(20)},{y(96)} V{horizon} Z" '
                f'fill="{DSHAD}" opacity=".45"/>')
    mos += dome(cx-s(192), y(210), s(86), s(74))
    mos += dome(cx+s(192), y(210), s(86), s(74))
    mos += dome(cx, y(244), s(168), s(150))

    body = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#E6DABE"/><stop offset=".26" stop-color="#F0E6CF"/>
    <stop offset=".5" stop-color="#F6EEDC"/><stop offset=".66" stop-color="#FAF3E5"/>
    <stop offset=".72" stop-color="#FDF9F0"/>
  </linearGradient>
  <radialGradient id="sun" cx="50%" cy="{(horizon-24)/H*100:.0f}%" r="30%">
    <stop offset="0" stop-color="#FFFEF9"/><stop offset=".2" stop-color="rgba(255,251,238,.55)"/>
    <stop offset=".55" stop-color="rgba(255,247,228,.12)"/><stop offset="1" stop-color="rgba(255,247,228,0)"/>
  </radialGradient>
  <linearGradient id="pool" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#F5EDDB"/><stop offset=".5" stop-color="#EFE4CE"/>
    <stop offset="1" stop-color="#EBDFC7"/>
  </linearGradient>
  <linearGradient id="minG" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{DSHAD}"/><stop offset=".45" stop-color="{DLIT}"/>
    <stop offset="1" stop-color="{DBASE}"/>
  </linearGradient>
  <filter id="soft"><feGaussianBlur stdDeviation="1.3"/></filter>
  <filter id="softer"><feGaussianBlur stdDeviation="8"/></filter>
</defs>

<rect width="{W}" height="{H}" fill="url(#sky)"/>
<g filter="url(#softer)" opacity=".55">
  <ellipse cx="{W*0.28}" cy="{horizon-190}" rx="240" ry="22" fill="#FFFBF0"/>
  <ellipse cx="{W*0.74}" cy="{horizon-120}" rx="280" ry="24" fill="#FEF8EC"/>
  <ellipse cx="{W*0.52}" cy="{horizon-300}" rx="320" ry="24" fill="#FFFCF4"/>
</g>
<rect width="{W}" height="{H}" fill="url(#sun)"/>

<rect x="0" y="{horizon}" width="{W}" height="{H-horizon}" fill="url(#pool)"/>
<g transform="translate(0,{2*horizon}) scale(1,-1)" filter="url(#softer)" opacity=".32">{mos}</g>
<g filter="url(#soft)">{mos}</g>
<g stroke="#FFFBF0" stroke-width="2.5" opacity=".45">
  <line x1="0" y1="{horizon+52}" x2="{W}" y2="{horizon+52}"/>
  <line x1="0" y1="{horizon+128}" x2="{W}" y2="{horizon+128}"/>
  <line x1="0" y1="{horizon+224}" x2="{W}" y2="{horizon+224}"/>
  <line x1="0" y1="{horizon+340}" x2="{W}" y2="{horizon+340}"/>
</g>
<rect x="0" y="{horizon-16}" width="{W}" height="72" fill="url(#sun)" opacity=".35"/>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="rgba(251,244,234,0)"/><stop offset="1" stop-color="rgba(251,244,234,.92)"/>
</linearGradient>
<rect x="0" y="{H*0.74}" width="{W}" height="{H*0.26}" fill="url(#fade)"/>
</svg>'''
    w("assets/hero-vista.svg", body)


# ══════════════════════════════════════════════════════════════════
# 2. the ivory cusped arch frame + jali columns  (transparent centre)
# ══════════════════════════════════════════════════════════════════
def ogee(cx, apexY, springY, halfw, botY, cusp=0):
    """A clean symmetric Mughal onion/ogee arch opening that runs straight
    down between the columns to botY.  `cusp` adds shallow foils along the
    curve when > 0 (kept subtle, never spiky)."""
    xL, xR = cx - halfw, cx + halfw
    h = springY - apexY
    if not cusp:
        return (f'M{xL:.1f},{botY:.1f} L{xL:.1f},{springY:.1f} '
                f'C{xL:.1f},{springY-h*0.52:.1f} {cx-halfw*0.30:.1f},{apexY+h*0.16:.1f} {cx:.1f},{apexY:.1f} '
                f'C{cx+halfw*0.30:.1f},{apexY+h*0.16:.1f} {xR:.1f},{springY-h*0.52:.1f} {xR:.1f},{springY:.1f} '
                f'L{xR:.1f},{botY:.1f} Z')
    # foiled version: sample the clean curve, then bump inward with arcs
    def curveL(t):                                   # t 0..1 spring->apex
        # de Casteljau on the left cubic
        p0 = (xL, springY); p1 = (xL, springY-h*0.52)
        p2 = (cx-halfw*0.30, apexY+h*0.16); p3 = (cx, apexY)
        a = lambda u,v: ((u[0]+(v[0]-u[0])*t),(u[1]+(v[1]-u[1])*t))
        q0,q1,q2 = a(p0,p1),a(p1,p2),a(p2,p3)
        r0,r1 = a(q0,q1),a(q1,q2)
        return a(r0,r1)
    N = cusp
    pts = [curveL(i/N) for i in range(N+1)]
    d = f'M{xL:.1f},{botY:.1f} L{pts[0][0]:.1f},{pts[0][1]:.1f} '
    for i in range(1, len(pts)):
        px,py = pts[i-1]; x,y = pts[i]
        r = math.hypot(x-px,y-py)/2
        d += f'A{r:.1f},{r:.1f} 0 0 0 {x:.1f},{y:.1f} '     # lobe bulging into the opening
    # mirror
    mpts = [(cx+(cx-x), y) for (x,y) in reversed(pts)]
    for i in range(1, len(mpts)):
        px,py = mpts[i-1]; x,y = mpts[i]
        r = math.hypot(x-px,y-py)/2
        d += f'A{r:.1f},{r:.1f} 0 0 0 {x:.1f},{y:.1f} '
    d += f'L{xR:.1f},{botY:.1f} Z'
    return d


def arch():
    W, H = 840, 1680
    cx = W / 2
    spring = H * 0.40
    apex   = H * 0.05
    colW   = 108
    openHW = (W - 2 * colW) / 2 + 4

    inner = ogee(cx, apex + 24, spring, openHW,       H, cusp=9)
    mid   = ogee(cx, apex + 12, spring, openHW + 20,  H, cusp=0)
    outer = ogee(cx, apex,      spring, openHW + 50,  H, cusp=0)

    # jali lattice tile — interlaced eight-point stars
    jali = ('<pattern id="jali" width="52" height="52" patternUnits="userSpaceOnUse">'
            f'<path d="M26 2 L34 18 L50 26 L34 34 L26 50 L18 34 L2 26 L18 18 Z" '
            f'fill="none" stroke="{GOLD}" stroke-width="1.3" opacity=".42"/>'
            f'<rect x="14" y="14" width="24" height="24" fill="none" stroke="{GOLD}" '
            f'stroke-width="1" opacity=".3" transform="rotate(45 26 26)"/>'
            f'<circle cx="26" cy="26" r="2.6" fill="{GOLD}" opacity=".32"/></pattern>')

    def column(flip):
        tf = f'transform="translate({W},0) scale(-1,1)"' if flip else ''
        return f'''<g {tf}>
      <rect x="0" y="{spring-70}" width="{colW}" height="{H}" fill="url(#stone)"/>
      <rect x="18" y="{spring-30}" width="{colW-36}" height="{H}" fill="url(#jali)"/>
      <rect x="18" y="{spring-30}" width="{colW-36}" height="{H}" fill="none" stroke="url(#gold)" stroke-width="2" opacity=".5"/>
      <rect x="-4" y="{spring-70}" width="{colW+8}" height="40" fill="url(#capG)"/>
      <rect x="-4" y="{spring-34}" width="{colW+8}" height="7" fill="url(#gold)"/>
      <rect x="-4" y="{spring-78}" width="{colW+8}" height="9" fill="url(#gold)"/>
      <path d="M-4,{spring-70} h{colW+8} l-16,-26 h-{colW-24} Z" fill="url(#stone)"/>
    </g>'''

    body = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">
<defs>
  <linearGradient id="stone" x1="0" y1="0" x2="0.15" y2="1">
    <stop offset="0" stop-color="{IVORY_L}"/><stop offset=".45" stop-color="{IVORY}"/>
    <stop offset="1" stop-color="{IVORY_D}"/>
  </linearGradient>
  <linearGradient id="capG" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{IVORY_D}"/><stop offset=".5" stop-color="{IVORY_L}"/>
    <stop offset="1" stop-color="{IVORY_D}"/>
  </linearGradient>
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{GOLD_D}"/><stop offset=".5" stop-color="{GOLD_L}"/>
    <stop offset="1" stop-color="{GOLD_D}"/>
  </linearGradient>
  {jali}
  <filter id="cast" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#6e4c1e" flood-opacity="0.24"/>
  </filter>
  <filter id="innerdark" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="0" stdDeviation="12" flood-color="#6e4c1e" flood-opacity="0.32"/>
  </filter>
  <mask id="cut">
    <rect width="{W}" height="{H}" fill="#fff"/>
    <path d="{inner}" fill="#000"/>
  </mask>
  <mask id="ring">
    <path d="{inner}" fill="#fff"/><path d="{mid}" fill="#000"/>
  </mask>
</defs>

<g filter="url(#cast)">
  <!-- full ivory face, opening punched out -->
  <rect width="{W}" height="{H}" fill="url(#stone)" mask="url(#cut)"/>
  {column(False)}
  {column(True)}
  <!-- the faintest shadow just inside the opening lip -->
  <path d="{inner}" fill="none" stroke="#6e4c1e" stroke-width="16" opacity=".16" mask="url(#cut)" filter="url(#innerdark)"/>
  <!-- fine carved concentric mouldings around the opening -->
  <path d="{outer}" fill="none" stroke="{GOLD_D}" stroke-width="2" opacity=".5"/>
  <path d="{mid}"   fill="none" stroke="url(#gold)" stroke-width="3.5"/>
  <path d="{mid}"   fill="none" stroke="{IVORY_D}" stroke-width="1.4" opacity=".6"/>
  <path d="{inner}" fill="none" stroke="url(#gold)" stroke-width="4.5"/>
  <path d="{inner}" fill="none" stroke="{IVORY_L}" stroke-width="1.6" opacity=".95"/>
  <!-- keystone flourish at the apex -->
  <circle cx="{cx}" cy="{apex+10}" r="9" fill="url(#gold)"/>
  <path d="M{cx},{apex-9} l7,15 l-7,15 l-7,-15 Z" fill="url(#gold)"/>
  <g fill="url(#gold)" opacity=".7">
   <circle cx="{colW+26}" cy="{apex+120}" r="4"/><circle cx="{W-colW-26}" cy="{apex+120}" r="4"/>
  </g>
</g>
</svg>'''
    w("assets/hero-arch.svg", body)


# ══════════════════════════════════════════════════════════════════
# 3. an all-flower corner cluster — cream roses, peonies, buds
# ══════════════════════════════════════════════════════════════════
def _petal(px, py, tx, ty, wfrac):
    """A single petal from base (px,py) to tip (tx,ty); wfrac = width/len."""
    dx, dy = tx - px, ty - py
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    w1 = L * wfrac
    mx, my = (px + tx) / 2, (py + ty) / 2
    return (f'<path d="M{px:.1f},{py:.1f} '
            f'C{mx+nx*w1:.1f},{my+ny*w1:.1f} {tx+nx*w1*0.35:.1f},{ty+ny*w1*0.35:.1f} {tx:.1f},{ty:.1f} '
            f'C{tx-nx*w1*0.35:.1f},{ty-ny*w1*0.35:.1f} {mx-nx*w1:.1f},{my-ny*w1:.1f} {px:.1f},{py:.1f} Z" '
            f'fill="url(#pet)" stroke="#CBAE78" stroke-width="1.1" stroke-opacity=".6"/>')


def _rose(cx, cy, r):
    """A layered garden rose — a warm shaded heart wrapped in petal rings."""
    g = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*1.02:.1f}" fill="url(#core)"/>'
    for rr, n, off, wf in [(1.0, 7, 0, .5), (0.72, 6, 26, .55), (0.46, 5, 14, .6), (0.24, 4, 30, .7)]:
        for k in range(n):
            a = math.radians(k * (360 / n) + off)
            bx, by = cx + math.cos(a) * r * rr * 0.16, cy + math.sin(a) * r * rr * 0.16
            tx, ty = cx + math.cos(a) * r * rr, cy + math.sin(a) * r * rr
            g += _petal(bx, by, tx, ty, wf)
    g += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.13:.1f}" fill="#E2C99C"/>'
    for k in range(5):
        a = math.radians(k * 72 + 12)
        g += f'<circle cx="{cx+math.cos(a)*r*0.1:.1f}" cy="{cy+math.sin(a)*r*0.1:.1f}" r="1.5" fill="{GOLD_L}" opacity=".8"/>'
    return f'<g>{g}</g>'


def _peony(cx, cy, r):
    """A fuller, looser bloom — many soft ruffled petals."""
    g = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*1.02:.1f}" fill="url(#core)"/>'
    for rr, n, off, wf in [(1.0, 11, 0, .42), (0.78, 9, 20, .48), (0.55, 7, 12, .55), (0.32, 5, 26, .66)]:
        for k in range(n):
            a = math.radians(k * (360 / n) + off)
            bx, by = cx + math.cos(a) * r * rr * 0.2, cy + math.sin(a) * r * rr * 0.2
            tx, ty = cx + math.cos(a) * r * rr, cy + math.sin(a) * r * rr
            g += _petal(bx, by, tx, ty, wf)
    g += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.16:.1f}" fill="#E6CFA2"/>'
    for k in range(8):
        a = math.radians(k * 45)
        g += f'<circle cx="{cx+math.cos(a)*r*0.16:.1f}" cy="{cy+math.sin(a)*r*0.16:.1f}" r="1.8" fill="{GOLD_L}" opacity=".7"/>'
    return f'<g>{g}</g>'


def _blossom(cx, cy, r):
    """A simple open five-petal blossom with a gold centre."""
    g = ''
    for k in range(5):
        a = math.radians(k * 72 - 90)
        tx, ty = cx + math.cos(a) * r, cy + math.sin(a) * r
        g += _petal(cx, cy, tx, ty, .82)
    g += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.24:.1f}" fill="#EBD3A6"/>'
    for k in range(6):
        a = math.radians(k * 60)
        g += f'<circle cx="{cx+math.cos(a)*r*0.14:.1f}" cy="{cy+math.sin(a)*r*0.14:.1f}" r="1.7" fill="{GOLD}" opacity=".6"/>'
    return f'<g>{g}</g>'


def floral():
    W = H = 640
    els = []
    els.append(f'<g filter="url(#blur1)">{_peony(150,148,98)}</g>')
    els.append(f'<g filter="url(#blur1)">{_rose(66,270,86)}</g>')
    for (fn, x, y, r) in [(_rose,258,108,62),(_peony,286,258,66),(_rose,196,222,54),
                          (_rose,50,146,48),(_rose,344,182,44),(_rose,182,348,52),
                          (_blossom,352,262,34),(_blossom,300,54,30),(_blossom,392,210,26),
                          (_blossom,60,356,32),(_blossom,214,60,26),(_blossom,120,110,24),
                          (_blossom,332,322,24),(_rose,108,108,38)]:
        els.append(f'<g filter="url(#blur0)">{fn(x,y,r)}</g>')

    body = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<defs>
  <radialGradient id="pet" cx="34%" cy="26%" r="82%">
    <stop offset="0" stop-color="#FFFEF9"/><stop offset=".3" stop-color="#F8EEDA"/>
    <stop offset=".64" stop-color="#EBD8B4"/><stop offset="1" stop-color="#D6BC90"/>
  </radialGradient>
  <radialGradient id="core" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#CBAF80"/><stop offset=".65" stop-color="#E0CBA0"/>
    <stop offset="1" stop-color="#ECDCBC"/>
  </radialGradient>
  <filter id="blur0"><feGaussianBlur stdDeviation="0.3"/></filter>
  <filter id="blur1"><feGaussianBlur stdDeviation="0.5"/></filter>
  <filter id="drop" x="-40%" y="-40%" width="180%" height="180%">
    <feDropShadow dx="0" dy="6" stdDeviation="9" flood-color="#6b4f2a" flood-opacity="0.24"/>
  </filter>
</defs>
<g filter="url(#drop)">{''.join(els)}</g>
</svg>'''
    w("assets/floral-cluster.svg", body)


# ══════════════════════════════════════════════════════════════════
# 4. an ornate glowing gold lantern
# ══════════════════════════════════════════════════════════════════
def lantern():
    W, H = 150, 360
    cx = W/2
    body = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="brass" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#7C5A22"/><stop offset=".28" stop-color="#D9A94C"/>
    <stop offset=".5" stop-color="#F6E1A6"/><stop offset=".72" stop-color="#D9A94C"/>
    <stop offset="1" stop-color="#7C5A22"/>
  </linearGradient>
  <radialGradient id="flame" cx="50%" cy="54%" r="60%">
    <stop offset="0" stop-color="#FFF6DC"/><stop offset=".4" stop-color="#FFE0A0"/>
    <stop offset=".75" stop-color="#F7B25A"/><stop offset="1" stop-color="rgba(244,160,70,0)"/>
  </radialGradient>
  <radialGradient id="halo" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="rgba(255,224,160,.75)"/><stop offset="1" stop-color="rgba(255,224,160,0)"/>
  </radialGradient>
  <filter id="lg"><feGaussianBlur stdDeviation="1"/></filter>
</defs>
<line x1="{cx}" y1="0" x2="{cx}" y2="54" stroke="url(#brass)" stroke-width="3"/>
<circle cx="{cx}" cy="60" r="7" fill="none" stroke="url(#brass)" stroke-width="3"/>
<path d="M{cx-4},66 L{cx+4},66 L{cx+2},80 L{cx-2},80 Z" fill="url(#brass)"/>
<!-- glow -->
<ellipse cx="{cx}" cy="180" rx="70" ry="96" fill="url(#halo)"/>
<!-- cap -->
<path d="M{cx-34},92 L{cx+34},92 L{cx+20},70 L{cx-20},70 Z" fill="url(#brass)"/>
<path d="M{cx-20},70 L{cx+20},70 L{cx+8},54 L{cx-8},54 Z" fill="url(#brass)"/>
<circle cx="{cx}" cy="50" r="4" fill="#F6E1A6"/>
<!-- body: six-sided glass lantern -->
<path d="M{cx-38},96 L{cx+38},96 L{cx+30},250 L{cx-30},250 Z" fill="rgba(255,240,205,.30)" stroke="url(#brass)" stroke-width="4"/>
<path d="M{cx-30},250 L{cx+30},250 L{cx+20},270 L{cx-20},270 Z" fill="url(#brass)"/>
<g filter="url(#lg)"><ellipse cx="{cx}" cy="176" rx="26" ry="46" fill="url(#flame)"/></g>
<!-- ribs -->
<line x1="{cx}" y1="96" x2="{cx}" y2="250" stroke="url(#brass)" stroke-width="2.5" opacity=".8"/>
<line x1="{cx-19}" y1="96" x2="{cx-15}" y2="250" stroke="url(#brass)" stroke-width="2" opacity=".55"/>
<line x1="{cx+19}" y1="96" x2="{cx+15}" y2="250" stroke="url(#brass)" stroke-width="2" opacity=".55"/>
<path d="M{cx-30},150 Q{cx},140 {cx+30},150" fill="none" stroke="url(#brass)" stroke-width="2.5"/>
<path d="M{cx-32},210 Q{cx},200 {cx+32},210" fill="none" stroke="url(#brass)" stroke-width="2.5"/>
<!-- finial + tassel -->
<circle cx="{cx}" cy="278" r="5" fill="url(#brass)"/>
<line x1="{cx}" y1="283" x2="{cx}" y2="300" stroke="url(#brass)" stroke-width="2"/>
<circle cx="{cx}" cy="304" r="4" fill="#D9A94C"/>
</svg>'''
    w("assets/lantern-lux.svg", body)


vista()
arch()
floral()
lantern()
