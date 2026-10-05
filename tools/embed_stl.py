#!/usr/bin/env python3
"""Embed a lighter copy of the Windelo STL inside the simulator HTML (phone / file:// support).

Intégre une version allégée du modèle 3D dans le fichier HTML, pour qu'il fonctionne sur
téléphone sans lanceur ni serveur local.

    python3 tools/embed_stl.py "3D Windelo pour IHM test.stl"            # ~40 000 triangles
    python3 tools/embed_stl.py "3D Windelo pour IHM test.zip" --tris 60000
    python3 tools/embed_stl.py --remove                                  # take the copy out again

The STL (binary or ASCII, or a .zip holding one) is welded, decimated with quadric error
collapse (pip install fast-simplification; falls back to vertex clustering without it),
quantised to 16 bits over the original bounding box and written as base64 between the
WINDELO-MESH markers of the HTML. The page rebuilds an STL from it and loads it through the
same parser as the real file, so mast, wing and waterline land in the same place.

Requires numpy.
"""
import argparse
import base64
import html
import json
import os
import re
import struct
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_HTML = os.path.join(HERE, '..', 'interface_graphique EO3.html')
BEGIN, END = '<!-- WINDELO-MESH:BEGIN', '<!-- WINDELO-MESH:END -->'
BEGIN_LINE = BEGIN + ' — lighter Windelo model, written by tools/embed_stl.py (do not edit by hand) -->'


def read_stl_bytes(path):
    if path.lower().endswith('.zip'):
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if n.lower().endswith('.stl') and not n.startswith('__MACOSX')]
            if not names:
                sys.exit(f'no .stl inside {path}')
            return names[0], z.read(names[0])
    with open(path, 'rb') as f:
        return os.path.basename(path), f.read()


def parse_stl(data):
    """Return (triangles (n, 3, 3) float64, facet colours (n,) '#rrggbb' or None).
    Binary is detected by its exact size; colours follow the VisCAM convention
    (attribute bit 15 set, RGB555 in bits 14-0)."""
    if len(data) >= 84:
        n = struct.unpack_from('<I', data, 80)[0]
        if 84 + 50 * n == len(data):
            rec = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
            r = np.frombuffer(data, rec, n, 84)
            a = r['a'].astype(np.int64)
            cols = None
            if (a & 0x8000).any():
                rgb = np.stack([(a >> 10) & 31, (a >> 5) & 31, a & 31], 1) * 255 // 31
                cols = np.array(['#%02x%02x%02x' % tuple(c) for c in rgb])
            return r['v'].astype(np.float64), cols
    nums = re.findall(rb'vertex\s+(\S+)\s+(\S+)\s+(\S+)', data)
    tris = np.array(nums, dtype=np.float64).reshape(-1, 3, 3)
    if not len(tris):
        sys.exit('no triangles found (not an STL file?)')
    return tris, None


def weld(tris):
    """Merge coincident corners into shared vertices; drop degenerate and duplicate faces."""
    pts = tris.reshape(-1, 3)
    span = np.ptp(pts, axis=0).max() or 1.0
    keys = np.round(pts / (span * 1e-6)).astype(np.int64)
    _, first, inv = np.unique(keys, axis=0, return_index=True, return_inverse=True)
    verts, faces = pts[first], inv.ravel().reshape(-1, 3)
    ok = (faces[:, 0] != faces[:, 1]) & (faces[:, 1] != faces[:, 2]) & (faces[:, 0] != faces[:, 2])
    faces = faces[ok]
    _, keep = np.unique(np.sort(faces, axis=1), axis=0, return_index=True)
    return verts, faces[np.sort(keep)]


def cluster_decimate(verts, faces, target):
    """Dependency-free fallback: merge vertices on a grid, finest grid that meets the target."""
    lo, span = verts.min(0), np.ptp(verts, axis=0).max() or 1.0
    best = (verts, faces)
    for cells in (2048, 1448, 1024, 724, 512, 362, 256, 181, 128, 90, 64):
        ids = np.floor((verts - lo) / (span / cells)).astype(np.int64)
        _, inv = np.unique(ids, axis=0, return_inverse=True)
        inv = inv.ravel()
        cnt = np.bincount(inv)
        rep = np.stack([np.bincount(inv, verts[:, a]) / cnt for a in range(3)], 1)
        f = inv[faces]
        ok = (f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2])
        f = f[ok]
        _, keep = np.unique(np.sort(f, axis=1), axis=0, return_index=True)
        best = (rep, f[np.sort(keep)])
        if len(best[1]) <= target:
            break
    return best


def decimate(verts, faces, target, agg, preserve_border):
    if len(faces) <= target:
        return verts, faces, 'none (already under target)'
    try:
        import fast_simplification
    except ImportError:
        v, f = cluster_decimate(verts, faces, target)
        return v, f, 'vertex clustering (pip install fast-simplification for better quality)'
    v, f = fast_simplification.simplify(verts, faces.astype(np.int32), target_count=int(target),
                                        agg=agg, preserve_border=preserve_border)
    return v, f.astype(np.int64), 'quadric (fast-simplification)'


def encode(verts, faces, lo, hi, anchors, face_col=None):
    """uint16 positions over [lo, hi], then indices, then (optional) uint8 palette index per
    triangle; 6 zero-area anchor triangles keep the original bounding box (the page centres
    and scales the model from it)."""
    base = len(verts)
    verts = np.vstack([verts, anchors])
    faces = np.vstack([faces, np.repeat(np.arange(base, base + len(anchors))[:, None], 3, 1)])
    ext = np.where(hi - lo > 0, hi - lo, 1.0)
    q = np.clip(np.round((verts - lo) / ext * 65535), 0, 65535).astype('<u2')
    ib = 2 if len(verts) <= 65535 else 4
    payload = q.tobytes() + faces.astype('<u2' if ib == 2 else '<u4').tobytes()
    if face_col is not None:
        payload += np.concatenate([face_col, np.zeros(len(anchors), np.int64)]).astype('u1').tobytes()
    return payload, len(verts), len(faces), ib


def block(meta, payload, nl):
    b64 = base64.b64encode(payload).decode('ascii')
    lines = [b64[i:i + 120] for i in range(0, len(b64), 120)]
    return (f'{BEGIN_LINE}{nl}'
            f'    <script type="application/octet-stream" id="windelo-mesh" data-meta="{html.escape(json.dumps(meta))}">{nl}'
            + nl.join(lines) + f'{nl}    </script>{nl}    {END}')


def write_html(html_path, new_block):
    with open(html_path, 'rb') as f:
        text = f.read().decode('utf-8')
    nl = '\r\n' if '\r\n' in text else '\n'          # keep the file's line endings (CRLF today)
    i, j = text.find(BEGIN), text.find(END)
    if i < 0 or j < i:
        sys.exit(f'markers {BEGIN} … {END} not found in {html_path}')
    out = text[:i] + new_block(nl) + text[j + len(END):]
    with open(html_path, 'wb') as f:
        f.write(out.encode('utf-8'))
    return len(text.encode('utf-8')), len(out.encode('utf-8'))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('stl', nargs='?', help='STL file (binary/ASCII) or .zip containing one')
    ap.add_argument('--tris', type=int, default=40000, help='target triangle count (default 40000)')
    ap.add_argument('--html', default=DEFAULT_HTML, help='simulator HTML to update in place')
    ap.add_argument('--agg', type=float, default=7.0, help='decimation aggressiveness 0-10 (default 7)')
    ap.add_argument('--preserve-border', action='store_true', help='keep open mesh borders sharp')
    ap.add_argument('--remove', action='store_true', help='remove the embedded model from the HTML')
    a = ap.parse_args()

    if a.remove:
        before, after = write_html(a.html, lambda nl: f'{BEGIN_LINE}{nl}    {END}')
        print(f'embedded model removed: {before / 1024:.0f} KB -> {after / 1024:.0f} KB')
        return
    if not a.stl:
        ap.error('give the STL file (or --remove)')

    name, data = read_stl_bytes(a.stl)
    tris, cols = parse_stl(data)
    verts, faces = weld(tris)
    lo, hi = verts.min(0), verts.max(0)
    anchors = np.array([verts[np.argmin(verts[:, k])] for k in range(3)] + [verts[np.argmax(verts[:, k])] for k in range(3)])
    if cols is None:
        dv, df, how = decimate(verts, faces, a.tris, a.agg, a.preserve_border)
        face_col, palette = None, None
    else:
        # Coloured model: decimate each colour on its own so faces keep their colour.
        palette = sorted(set(cols))[:255]
        groups = [weld(tris[cols == c]) for c in palette]
        total = sum(len(f) for _, f in groups)
        dv, df, fc, off = [], [], [], 0
        for k, (gv, gf) in enumerate(groups):
            v, f, how = decimate(gv, gf, max(12, round(a.tris * len(gf) / total)), a.agg, a.preserve_border)
            dv.append(v); df.append(f + off); fc.append(np.full(len(f), k)); off += len(v)
        dv, df, face_col = np.vstack(dv), np.vstack(df), np.concatenate(fc)
    payload, nV, nT, ib = encode(dv, df, lo, hi, anchors, face_col)
    meta = {'format': 'accwing-mesh-1', 'source': name, 'sourceTriangles': int(len(tris)),
            'triangles': int(nT), 'vertices': int(nV), 'indexBytes': ib,
            'min': [round(float(x), 6) for x in lo], 'max': [round(float(x), 6) for x in hi]}
    if palette:
        meta['palette'] = palette
    before, after = write_html(a.html, lambda nl: block(meta, payload, nl))

    shrink = np.abs(np.concatenate([dv.min(0) - lo, hi - dv.max(0)])).max() / (np.ptp(verts, axis=0).max() or 1)
    print(f'{name}: {len(tris):,} triangles ({len(verts):,} welded vertices)')
    print(f'decimation: {how} -> {len(df):,} triangles, {len(dv):,} vertices '
          f'(bbox drift {shrink * 100:.2f}% of length, compensated by anchors)')
    print(f'embedded: {len(payload) / 1024:.0f} KB binary, HTML {before / 1024:.0f} KB -> {after / 1024:.0f} KB')


if __name__ == '__main__':
    main()
