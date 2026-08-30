#!/usr/bin/env python3
"""Hand-built hero art for the opening page — warm golden-hour vista,
an ivory cusped arch with jali columns, lush corner florals and a
glowing lantern.  Stylised, soft-focus, luxurious.  Pure SVG."""
import math

# ── shared palette ────────────────────────────────────────────────
CREAM   = "#FBF3E4"
IVORY   = "#F3E4C4"
IVORY_D = "#D8BE93"     # shadow side
IVORY_L = "#FFFBEF"     # lit side
GOLD    = "#C99A44"
GOLD_D  = "#8A6524"
GOLD_L  = "#F3DCA0"
SKY_TOP = "#EAD9B4"
SKY_MID = "#F6DCA8"
SKY_LOW = "#FBCE86"
SUN     = "#FFF0CE"
BLUSH   = "#F6E4D2"
SAGE    = "#C9CDB2"


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

    def dome(dcx, base, rw, rh):
        # warm-lit onion dome with a bright sun-side crescent and shadow side
        top = base - rh * 1.62
        return (
            f'<path d="M{dcx-rw},{base} C{dcx-rw},{base-rh*1.12} {dcx-rw*0.55},{base-rh*1.55} {dcx},{top} '
            f'C{dcx+rw*0.55},{base-rh*1.55} {dcx+rw},{base-rh*1.12} {dcx+rw},{base} Z" fill="#E3CDA2"/>'
            f'<path d="M{dcx},{top} C{dcx+rw*0.52},{base-rh*1.5} {dcx+rw},{base-rh*1.05} {dcx+rw},{base} '
            f'C{dcx+rw*0.5},{base} {dcx+rw*0.2},{base-rh*0.7} {dcx+rw*0.1},{top+rh*0.2} Z" fill="#FBF0D6"/>'
            f'<path d="M{dcx-rw},{base} C{dcx-rw},{base-rh*1.12} {dcx-rw*0.62},{base-rh*1.5} {dcx-rw*0.2},{top+rh*0.15} '
            f'C{dcx-rw*0.4},{base-rh*0.7} {dcx-rw*0.7},{base-rh*0.3} {dcx-rw*0.55},{base} Z" fill="#C7AC7E"/>'
            f'<path d="M{dcx},{top} C{dcx-rw*0.15},{top-rh*0.18} {dcx-rw*0.09},{top-rh*0.34} {dcx},{top-rh*0.46} '
            f'C{dcx+rw*0.09},{top-rh*0.34} {dcx+rw*0.15},{top-rh*0.18} {dcx},{top} Z" fill="#EADFC0"/>'
            f'<rect x="{dcx-2.5}" y="{top-rh*0.46-rh*0.18}" width="5" height="{rh*0.2}" fill="#C99A44"/>'
            f'<circle cx="{dcx}" cy="{top-rh*0.46-rh*0.2}" r="4" fill="#F3DCA0"/>'
        )

    def minaret(mcx, base, top, wd):
        return (
            f'<rect x="{mcx-wd/2}" y="{top}" width="{wd}" height="{base-top}" fill="url(#minG)"/>'
            f'<rect x="{mcx-wd*0.8}" y="{top+(base-top)*0.30}" width="{wd*1.6}" height="{wd*0.55}" fill="#E3CDA2"/>'
            f'<rect x="{mcx-wd*0.8}" y="{top+(base-top)*0.58}" width="{wd*1.6}" height="{wd*0.55}" fill="#E3CDA2"/>'
            + dome(mcx, top, wd*1.0, wd*1.15)
            + f'<rect x="{mcx-wd*0.95}" y="{top-3}" width="{wd*1.9}" height="{wd*0.5}" rx="2" fill="#F2E4C4"/>'
        )

    def y(v):  return horizon - v * M          # height above horizon, scaled
    def s(v):  return v * M                     # scaled length

    mos = ''
    mos += minaret(cx-s(360), horizon, y(620), s(30))
    mos += minaret(cx+s(360), horizon, y(620), s(30))
    mos += minaret(cx-s(250), horizon, y(520), s(24))
    mos += minaret(cx+s(250), horizon, y(520), s(24))
    mos += f'<rect x="{cx-s(235)}" y="{y(210)}" width="{s(470)}" height="{s(210)}" fill="#E3CDA2"/>'
    mos += f'<path d="M{cx-s(248)},{y(210)} H{cx+s(248)} L{cx+s(218)},{y(262)} H{cx-s(218)} Z" fill="#EFE0BE"/>'
    for i in range(-4, 5):
        ax = cx + i*s(54)
        mos += (f'<path d="M{ax-s(20)},{horizon} V{y(96)} A{s(20)},{s(26)} 0 0 1 {ax+s(20)},{y(96)} V{horizon} Z" '
                f'fill="#C7AC7E" opacity=".55"/>')
    mos += dome(cx-s(192), y(210), s(86), s(74))
    mos += dome(cx+s(192), y(210), s(86), s(74))
    mos += dome(cx, y(244), s(168), s(150))

    body = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#C9BCA0"/><stop offset=".18" stop-color="#DCC28C"/>
    <stop offset=".42" stop-color="#F0D194"/><stop offset=".6" stop-color="#FADFA4"/>
    <stop offset=".7" stop-color="#FFECBA"/><stop offset=".72" stop-color="#FFF3D2"/>
  </linearGradient>
  <radialGradient id="sun" cx="50%" cy="{(horizon-30)/H*100:.0f}%" r="40%">
    <stop offset="0" stop-color="#FFFCEF"/><stop offset=".12" stop-color="#FFF3D2"/>
    <stop offset=".32" stop-color="rgba(255,228,168,.6)"/><stop offset=".66" stop-color="rgba(255,222,160,.14)"/>
    <stop offset="1" stop-color="rgba(255,222,160,0)"/>
  </radialGradient>
  <linearGradient id="pool" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#F3D9A6"/><stop offset=".45" stop-color="#EACF9E"/>
    <stop offset="1" stop-color="#E6D0AE"/>
  </linearGradient>
  <linearGradient id="minG" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#C7AC7E"/><stop offset=".45" stop-color="#FBF0D6"/>
    <stop offset="1" stop-color="#E3CDA2"/>
  </linearGradient>
  <filter id="soft"><feGaussianBlur stdDeviation="1.6"/></filter>
  <filter id="softer"><feGaussianBlur stdDeviation="7"/></filter>
</defs>

<rect width="{W}" height="{H}" fill="url(#sky)"/>
<g filter="url(#softer)" opacity=".65">
  <ellipse cx="{W*0.28}" cy="{horizon-190}" rx="240" ry="24" fill="#FFF6E2"/>
  <ellipse cx="{W*0.74}" cy="{horizon-120}" rx="280" ry="26" fill="#FFF2D6"/>
  <ellipse cx="{W*0.52}" cy="{horizon-300}" rx="320" ry="26" fill="#FFF8EA"/>
</g>
<rect width="{W}" height="{H}" fill="url(#sun)"/>

<rect x="0" y="{horizon}" width="{W}" height="{H-horizon}" fill="url(#pool)"/>
<g transform="translate(0,{2*horizon}) scale(1,-1)" filter="url(#softer)" opacity=".4">{mos}</g>
<g filter="url(#soft)">{mos}</g>
<g stroke="#FFF7E4" stroke-width="2.5" opacity=".5">
  <line x1="0" y1="{horizon+50}" x2="{W}" y2="{horizon+50}"/>
  <line x1="0" y1="{horizon+120}" x2="{W}" y2="{horizon+120}"/>
  <line x1="0" y1="{horizon+210}" x2="{W}" y2="{horizon+210}"/>
  <line x1="0" y1="{horizon+320}" x2="{W}" y2="{horizon+320}"/>
</g>
<rect x="0" y="{horizon-18}" width="{W}" height="90" fill="url(#sun)" opacity=".4"/>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="rgba(240,222,190,0)"/><stop offset="1" stop-color="rgba(226,202,158,.72)"/>
</linearGradient>
<rect x="0" y="{H*0.8}" width="{W}" height="{H*0.2}" fill="url(#fade)"/>
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
            f'fill="none" stroke="{GOLD}" stroke-width="1.5" opacity=".55"/>'
            f'<rect x="14" y="14" width="24" height="24" fill="none" stroke="{GOLD}" '
            f'stroke-width="1.1" opacity=".4" transform="rotate(45 26 26)"/>'
            f'<circle cx="26" cy="26" r="3" fill="{GOLD}" opacity=".4"/></pattern>')

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
    <feDropShadow dx="0" dy="14" stdDeviation="22" flood-color="#5e4320" flood-opacity="0.38"/>
  </filter>
  <filter id="innerdark" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="0" stdDeviation="14" flood-color="#4a3416" flood-opacity="0.5"/>
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
  <!-- a soft shadow just inside the opening lip, so it reads as a deep cut -->
  <path d="{inner}" fill="none" stroke="#4a3416" stroke-width="20" opacity=".28" mask="url(#cut)" filter="url(#innerdark)"/>
  <!-- carved concentric mouldings around the opening -->
  <path d="{outer}" fill="none" stroke="{GOLD_D}" stroke-width="3" opacity=".7"/>
  <path d="{mid}"   fill="none" stroke="url(#gold)" stroke-width="6"/>
  <path d="{mid}"   fill="none" stroke="{IVORY_D}" stroke-width="2" opacity=".7"/>
  <path d="{inner}" fill="none" stroke="url(#gold)" stroke-width="7"/>
  <path d="{inner}" fill="none" stroke="{IVORY_L}" stroke-width="2" opacity=".9"/>
  <!-- keystone flourish at the apex -->
  <circle cx="{cx}" cy="{apex+10}" r="11" fill="url(#gold)"/>
  <path d="M{cx},{apex-10} l9,18 l-9,18 l-9,-18 Z" fill="url(#gold)"/>
  <!-- corner rosettes in the spandrels -->
  <g fill="url(#gold)" opacity=".8">
   <circle cx="{colW+26}" cy="{apex+120}" r="5"/><circle cx="{W-colW-26}" cy="{apex+120}" r="5"/>
  </g>
</g>
</svg>'''
    w("assets/hero-arch.svg", body)


# ══════════════════════════════════════════════════════════════════
# 3. a lush cream-rose / peony corner cluster
# ══════════════════════════════════════════════════════════════════
def _rose(cx, cy, r, tint):
    """An illustrated garden rose: a spiral of overlapping teardrop petals,
    each shaded light at the rim and warm at the base."""
    g = f'<ellipse cx="{cx:.1f}" cy="{cy+r*0.12:.1f}" rx="{r:.1f}" ry="{r*0.94:.1f}" fill="{tint}"/>'
    petals = 13
    for k in range(petals):
        f = k / petals
        ang = k * 137.5                       # golden-angle spiral
        rad = r * (0.22 + 0.72 * f)
        pr  = r * (0.30 + 0.42 * (1 - f))     # petal size shrinks outward a touch
        a = math.radians(ang)
        px, py = cx + math.cos(a) * rad * 0.55, cy + math.sin(a) * rad * 0.55
        perp = a + math.pi / 2
        wx, wy = math.cos(perp) * pr, math.sin(perp) * pr
        tx, ty = cx + math.cos(a) * rad, cy + math.sin(a) * rad
        g += (f'<path d="M{px:.1f},{py:.1f} '
              f'C{px-wx*0.9:.1f},{py-wy*0.9:.1f} {tx-wx*0.7:.1f},{ty-wy*0.7:.1f} {tx:.1f},{ty:.1f} '
              f'C{tx+wx*0.7:.1f},{ty+wy*0.7:.1f} {px+wx*0.9:.1f},{py+wy*0.9:.1f} {px:.1f},{py:.1f} Z" '
              f'fill="url(#pet)"/>'
              f'<path d="M{px:.1f},{py:.1f} '
              f'C{px-wx*0.9:.1f},{py-wy*0.9:.1f} {tx-wx*0.7:.1f},{ty-wy*0.7:.1f} {tx:.1f},{ty:.1f}" '
              f'fill="none" stroke="{tint}" stroke-width="1.1" stroke-opacity=".45"/>')
    # tight bud at the centre
    for k in range(4):
        a = math.radians(k * 90 + 20)
        g += (f'<path d="M{cx:.1f},{cy:.1f} q{math.cos(a)*r*0.28:.1f},{math.sin(a)*r*0.28:.1f} '
              f'{math.cos(a)*r*0.05:.1f},{math.sin(a)*r*0.34:.1f} z" fill="url(#pet)"/>')
    g += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.1:.1f}" fill="#E7CDA6"/>'
    return f'<g>{g}</g>'


def _leaf(cx, cy, ln, ang):
    a = math.radians(ang)
    tx, ty = cx + math.cos(a)*ln, cy + math.sin(a)*ln
    nx, ny = -math.sin(a), math.cos(a)
    return (f'<path d="M{cx:.1f},{cy:.1f} Q{cx+nx*ln*0.4:.1f},{cy+ny*ln*0.4:.1f} {tx:.1f},{ty:.1f} '
            f'Q{cx-nx*ln*0.4:.1f},{cy-ny*ln*0.4:.1f} {cx:.1f},{cy:.1f} Z" fill="url(#leaf)" opacity=".9"/>')


def _sprig(x, y, ln, ang, leaves=6):
    a = math.radians(ang)
    ex, ey = x + math.cos(a) * ln, y + math.sin(a) * ln
    g = f'<path d="M{x:.1f},{y:.1f} Q{(x+ex)/2 - math.sin(a)*ln*0.2:.1f},{(y+ey)/2 + math.cos(a)*ln*0.2:.1f} {ex:.1f},{ey:.1f}" fill="none" stroke="url(#leaf)" stroke-width="2"/>'
    for i in range(1, leaves + 1):
        t = i / (leaves + 1)
        lx, ly = x + (ex - x) * t, y + (ey - y) * t
        for s in (1, -1):
            la = a + s * 1.05
            gx, gy = lx + math.cos(la) * ln * 0.16, ly + math.sin(la) * ln * 0.16
            g += (f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{ln*0.11:.1f}" ry="{ln*0.05:.1f}" '
                  f'transform="rotate({math.degrees(la):.0f} {gx:.1f} {gy:.1f})" fill="url(#leaf)" opacity=".9"/>')
    return g


def floral():
    W = H = 640
    els = []
    # eucalyptus / greenery spilling out, behind the blooms
    for (x, y, ln, an) in [(150,150,190,25),(70,240,210,60),(250,80,170,-8),
                           (330,210,190,48),(110,110,150,-42),(210,300,160,88),
                           (300,320,150,70),(360,120,140,15)]:
        els.append(f'<g filter="url(#blur1)" opacity=".85">{_sprig(x,y,ln,an)}</g>')
    # blooms, corner-weighted, well spread, varied sizes
    blooms = [(140,140,88,"#E8CBA6"),(258,108,58,"#EAD9BE"),(96,262,78,"#E8CBA6"),
              (290,262,54,"#EAD9BE"),(44,150,50,"#EAD9BE"),(196,220,58,"#E8CBA6"),
              (350,180,44,"#EAD9BE"),(180,350,50,"#E8CBA6"),(388,270,38,"#EAD9BE"),
              (300,60,34,"#EAD9BE"),(70,360,40,"#E8CBA6")]
    for (x, y, r, t) in blooms:
        els.append(f'<g filter="url(#blur0)">{_rose(x,y,r,t)}</g>')
    # buds / ranunculus
    for (x, y, r) in [(355,120,17),(88,340,19),(320,315,15),(385,210,13),(210,66,14),(60,255,15)]:
        els.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#pet)" stroke="{BLUSH}" stroke-width="1" stroke-opacity=".4"/>')

    body = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<defs>
  <radialGradient id="pet" cx="36%" cy="30%" r="78%">
    <stop offset="0" stop-color="#FFFBF0"/><stop offset=".32" stop-color="#F8EAD0"/>
    <stop offset=".68" stop-color="#EAD3AC"/><stop offset="1" stop-color="#CDAF82"/>
  </radialGradient>
  <linearGradient id="leaf" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#CFD3B4"/><stop offset="1" stop-color="#9AA47B"/>
  </linearGradient>
  <filter id="blur0"><feGaussianBlur stdDeviation="0.4"/></filter>
  <filter id="blur1"><feGaussianBlur stdDeviation="2"/></filter>
  <filter id="drop" x="-40%" y="-40%" width="180%" height="180%">
    <feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="#7a5a30" flood-opacity="0.3"/>
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
