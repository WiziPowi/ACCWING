#!/usr/bin/env python3
"""Procedural Energy Observer 2 catamaran, drawn from the side/3-4 renders, written as a
binary STL with facet colours (VisCAM RGB555) for tools/embed_stl.py.

    python3 tools/eo2_model.py eo2.stl && python3 tools/embed_stl.py eo2.stl

Metres, Z up, length along X (stern at 0, bow at +X), keel bottom at z = 0.
Proportions measured on the side render (people on deck ≈ 14 px/m): ~40 m long, silver hull
to 2.1 m above the waterline then a navy band up to the deck at 4.3 m, deckhouse 2.2 m under
a thin overhanging roof, wheelhouse forward. Change the numbers below to adjust the shape.
"""
import struct
import sys

import numpy as np

L = 40.0              # length overall
T = 1.5               # draft (waterline height above the keel)
ZD = T + 4.3          # deck
ZB = T + 2.1          # silver / navy boot line
YC, W0 = 6.6, 1.8     # hull centreline offset, hull half-beam  → overall beam 16.8 m
ZW = T + 2.0          # underside of the bridgedeck
COL = {'hull': '#9aa1a6', 'band': '#1f2b3e', 'deck': '#4a4f57', 'house': '#1b2232',
       'roof': '#101419', 'glass': '#a9bccd', 'helm': '#4f6378'}

tris, cols = [], []


def tri(a, b, c, col):
    tris.append((a, b, c)); cols.append(col)


def loft(rings, seg_cols, cap_col=None):
    """rings: list of closed rings (same point count); seg_cols[k] colours segment k→k+1."""
    R = np.array(rings, dtype=float)
    S, M, _ = R.shape
    for i in range(S - 1):
        for k in range(M):
            a, b, c, d = R[i, k], R[i, (k + 1) % M], R[i + 1, (k + 1) % M], R[i + 1, k]
            tri(a, b, c, seg_cols[k]); tri(a, c, d, seg_cols[k])
    if cap_col:
        for ring, rev in ((R[0], True), (R[-1], False)):
            ctr = ring.mean(0)
            for k in range(M):
                p, q = ring[k], ring[(k + 1) % M]
                tri(ctr, q, p, cap_col) if rev else tri(ctr, p, q, cap_col)


def hull(yc):
    rings, seg = [], None
    for x in np.linspace(0, L, 150):
        u = x / L
        w = W0 * (0.86 + 0.14 * min(1, u / 0.15) ** 0.5)                     # wide transom
        if u > 0.55:
            w = W0 * max(0.0, 1 - ((u - 0.55) / 0.45) ** 2) ** 0.7          # fine entry, plumb bow
        flare = 0.12 * max(0, (u - 0.6) / 0.4)
        zk = 0.0
        if u < 0.18: zk = (T - 0.25) * ((0.18 - u) / 0.18) ** 1.6          # buttocks rise to the transom
        if u > 0.88: zk = 1.0 * ((u - 0.88) / 0.12) ** 1.5                  # forefoot
        zd = ZD - 0.9 * max(0, 1 - u / 0.05)                                # stepped stern
        zt = max(T + 0.1, zk + 0.25)                                        # turn of bilge
        half = []                                                           # (y, z, colour of next segment)
        for fy, fz in ((0, 0), (0.32, .15), (0.62, .38), (0.84, .65), (0.96, .88), (1, 1)):
            half.append((fy * w, zk + fz * (zt - zk), 'hull'))
        for z in (zt + 0.4, ZB):
            half.append((w * (1 + flare * (z - T) / (ZD - T)), z, 'hull'))
        half[-1] = half[-1][:2] + ('band',)
        we = w * (1 + flare)
        half += [(we, zd - 0.25, 'band'), (max(0, we - 0.12), zd - 0.04, 'deck'),
                 (max(0, we - 0.3), zd, 'deck'), (0, zd, 'deck')]
        # closed section: outer half keel→deck centre, then the mirrored inner half back down.
        pts = [(yc + y, z) for y, z, _ in half] + [(yc - y, z) for y, z, _ in reversed(half[1:-1])]
        rings.append([(x, y, z) for y, z in pts])
        c = [c for _, _, c in half[:-1]]           # colour of segment i → i+1 on the outer half
        seg = c + c[::-1]
    loft(rings, seg, cap_col='band')


def plan_box(x0, x1, hw_of, zbot_of, ztop_of, side, top, n=40):
    """Rectangular-section loft along X: half-width / bottom / top vary with x."""
    rings = []
    for x in np.linspace(x0, x1, n):
        h, zb, zt = hw_of(x), zbot_of(x), ztop_of(x)
        rings.append([(x, -h, zb), (x, h, zb), (x, h, zt), (x, -h, zt)])
    loft(rings, [side, side, top, side], cap_col=side)


def rounded(hw, x0, x1, r0, r1):
    """Half-width with rounded aft (r0) / forward (r1) ends in plan."""
    def f(x):
        k = 1.0
        if r0 and x < x0 + r0: k = np.sqrt(max(0, 1 - ((x0 + r0 - x) / r0) ** 2))
        if r1 and x > x1 - r1: k = min(k, np.sqrt(max(0, 1 - ((x - (x1 - r1)) / r1) ** 2)))
        return max(0.05, hw * (0.35 + 0.65 * k))
    return f


hull(-YC); hull(YC)
# bridgedeck between the hulls, sloped forward face down to the wet deck
yb = YC - 0.5 * W0
plan_box(0.02 * L, 0.80 * L, lambda x: yb, lambda x: ZW,
         lambda x: ZD - 0.01 - max(0, (x - 0.72 * L) / (0.08 * L)) * (ZD - 0.01 - ZW - 0.05), 'band', 'deck')
# deckhouse (saloon)
xs0, xs1, hs = 0.21 * L, 0.62 * L, 5.6
plan_box(xs0, xs1, rounded(hs, xs0, xs1, 1.2, 1.5), lambda x: ZD, lambda x: ZD + 2.2, 'house', 'house')
for a, b in ((0.245, 0.29), (0.33, 0.36), (0.41, 0.48), (0.52, 0.56)):          # side windows
    for sgn in (-1, 1):
        y = sgn * (hs + 0.04)
        p = [(a * L, y, ZD + 0.6), (b * L, y, ZD + 0.6), (b * L, y, ZD + 1.8), (a * L, y, ZD + 1.8)]
        tri(p[0], p[1], p[2], 'glass'); tri(p[0], p[2], p[3], 'glass')
x = xs0 - 0.04                                                                # aft glazing
p = [(x, -3.2, ZD + 0.3), (x, 3.2, ZD + 0.3), (x, 3.2, ZD + 2.0), (x, -3.2, ZD + 2.0)]
tri(p[0], p[1], p[2], 'glass'); tri(p[0], p[2], p[3], 'glass')
# wheelhouse, raked windscreen
xw0, xw1 = 0.60 * L, 0.69 * L
plan_box(xw0, xw1, lambda x: 4.6 - 0.8 * max(0, (x - xw0) / (xw1 - xw0)) ** 2, lambda x: ZD,
         lambda x: ZD + 3.1 - max(0, (x - (xw1 - 0.025 * L)) / (0.025 * L)) * 1.0, 'house', 'house', n=30)
for sgn in (-1, 1):                                                            # wheelhouse glazing band
    y = sgn * (4.6 - 0.8 * 0.36 + 0.03)
    p = [(xw0 + 1.0, y, ZD + 2.35), (xw1 - 1.4, y, ZD + 2.35), (xw1 - 1.4, y, ZD + 2.95), (xw0 + 1.0, y, ZD + 2.95)]
    tri(p[0], p[1], p[2], 'helm'); tri(p[0], p[2], p[3], 'helm')
xf = xw1 + 0.02
p = [(xf - 0.5, -3.4, ZD + 2.3), (xf - 0.5, 3.4, ZD + 2.3), (xf - 1.0, 3.2, ZD + 2.95), (xf - 1.0, -3.2, ZD + 2.95)]
tri(p[0], p[1], p[2], 'helm'); tri(p[0], p[2], p[3], 'helm')
# solar roof, overhanging aft, on posts
xr0, xr1 = 0.07 * L, 0.66 * L
plan_box(xr0, xr1, rounded(8.0, xr0, xr1, 2.0, 3.0), lambda x: ZD + 2.2, lambda x: ZD + 2.55, 'roof', 'roof', n=50)
for py in (-7.0, -3.0, 3.0, 7.0):
    x0 = 0.09 * L
    q = [(x0, py - 0.09), (x0 + 0.18, py - 0.09), (x0 + 0.18, py + 0.09), (x0, py + 0.09)]
    for k in range(4):
        (xa, y1), (xb, y2) = q[k], q[(k + 1) % 4]
        a, b, c, d = (xa, y1, ZD), (xb, y2, ZD), (xb, y2, ZD + 2.2), (xa, y1, ZD + 2.2)
        tri(a, b, c, 'roof'); tri(a, c, d, 'roof')

out = sys.argv[1] if len(sys.argv) > 1 else 'eo2.stl'
v = np.array(tris, dtype='<f4')
rec = np.zeros(len(v), dtype=[('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
rec['v'] = v
q5 = lambda h: [int(h[i:i + 2], 16) * 31 // 255 for i in (1, 3, 5)]
rec['a'] = [0x8000 | (r << 10) | (g << 5) | b for r, g, b in (q5(COL[c]) for c in cols)]
with open(out, 'wb') as f:
    f.write(b'Energy Observer 2 (procedural, ACCWing sim)'.ljust(80, b' '))
    f.write(struct.pack('<I', len(v))); f.write(rec.tobytes())
z = v[..., 2]
print(f'{out}: {len(v):,} triangles, {L:.0f} m x {2 * (YC + W0 * 1.12):.1f} m, height {z.max():.1f} m, draft {T} m')
