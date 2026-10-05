"""Audit for r01: spacing floors, crossing geometry, column check, ink balance, text clearance.
    .venv/bin/python studio/millennium-riemann/rounds/r01/audit.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import piece as P  # noqa: E402


def dense(poly, step=0.25):
    out = []
    for a, b in zip(poly, poly[1:]):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        for k in range(n):
            out.append((a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n))
    out.append(poly[-1])
    return np.asarray(out)


def min_gap(groups, exclude, cell=2.0):
    """min distance between points of DIFFERENT polylines, outside `exclude` discs."""
    pts, ids = [], []
    for i, p in enumerate(groups):
        d = dense(p)
        pts.append(d)
        ids.append(np.full(len(d), i))
    pts = np.vstack(pts)
    ids = np.concatenate(ids)
    ok = np.ones(len(pts), bool)
    for (cx, cy, r) in exclude:
        ok &= np.hypot(pts[:, 0] - cx, pts[:, 1] - cy) > r
    pts, ids = pts[ok], ids[ok]
    grid = {}
    for k, (x, y) in enumerate(pts):
        grid.setdefault((int(x // cell), int(y // cell)), []).append(k)
    best = (1e9, None)
    for (gx, gy), ks in grid.items():
        cand = [j for dx in (-1, 0, 1) for dy in (-1, 0, 1) for j in grid.get((gx + dx, gy + dy), [])]
        cand = np.asarray(cand)
        for k in ks:
            m = ids[cand] != ids[k]
            if not m.any():
                continue
            c = cand[m]
            d = np.hypot(pts[c, 0] - pts[k, 0], pts[c, 1] - pts[k, 1])
            j = int(np.argmin(d))
            if d[j] < best[0]:
                best = (float(d[j]), (tuple(np.round(pts[k], 2)), tuple(np.round(pts[c[j]], 2))))
    return best


def main():
    A, B, red, centres, worst = P.build_field()
    T, stats, rul = P.build_text(B)
    L = lambda ps: sum(P._plen(p) for p in ps)
    print(f"branch-through-rho max miss: {worst:.3f} mm")
    print(f"strokes A {len(A)}  B {len(B)}  red {len(red)}  text {len(T)}")
    print(f"draw m: B {L(B)/1000:.2f}  A {L(A)/1000:.2f}  text {L(T)/1000:.2f}  red {L(red)/1000:.3f}")
    left = sum(P._plen(p) for p in A + B if max(q[0] for q in p) < P.X0)
    right = sum(P._plen(p) for p in A + B if min(q[0] for q in p) > P.X0)
    print(f"ink wholly left of column {left/1000:.2f} m, wholly right {right/1000:.2f} m")
    # right-of-column ink, by clipping each poly at x = X0
    from promptplot.generative.engine.geometry import HalfPlane, clip
    rh = HalfPlane(-1.0, 0.0, P.X0)  # inside where x >= X0
    rl = sum(P._plen(q) for p in A + B for q in clip(p, rh, keep="inside"))
    ll = L(A + B) - rl
    print(f"ink right of X0 {rl/1000:.2f} m  left {ll/1000:.2f} m  ratio {rl/ll:.3f}")
    # crossings: centres and tilt of the hairline arm
    zs = P._zeros()
    for n, c in enumerate(centres[:8:2]):
        print(f"centre rho_{n+1}: x={c[0]:.3f} y={c[1]:.3f}")
    # angle between red arms at rho_1, rho_2, rho_4 (upper)
    for n in (1, 2, 4):
        c = P.to_sheet(0.5, zs[n - 1])
        arms = [p for p in red if P._nearest(p, c)[0] < 0.05]
        angs = []
        for p in arms:
            a = np.asarray(p)
            k = P._nearest(p, c)[1]
            d = a[k + 1] - a[k]
            angs.append(math.degrees(math.atan2(d[1], d[0])))
        rel = abs(((angs[0] - angs[1]) + 90) % 180 - 90)
        hair = ((angs[1] + 90) % 180) - 90
        print(f"rho_{n}: arm angles {angs[0]:.1f}, {angs[1]:.1f} -> meet {rel:.1f} deg; hairline arm {hair:+.1f} deg")
    # the same angles from the RAW marching-squares data (no decimation), in plane units
    raw = P._xray()
    for n in (1, 2, 4):
        c = (0.5, zs[n - 1])
        dirs = []
        for key in ("re0", "im0"):
            best = (9, None)
            for pl in raw[key]:
                d, k = P._nearest([tuple(q) for q in pl], c)
                if d < best[0]:
                    best = (d, (pl[k], pl[k + 1]))
            (a0, a1) = best[1]
            dirs.append(math.degrees(math.atan2(a1[1] - a0[1], a1[0] - a0[0])))
        rel = abs(((dirs[0] - dirs[1]) + 90) % 180 - 90)
        print(f"RAW rho_{n}: meet {rel:.2f} deg; hairline arm {((dirs[1] + 90) % 180) - 90:+.2f} deg")
    # spacing floors
    ex = [(c[0], c[1], P.R_RED + 1.0) for c in centres]
    # real-axis crossings (trivial zeros / pole): exclude a thin band around the axis
    band = [(x, P.Y_AXIS, 1.2) for x in np.arange(15, 283, 0.6)]
    g, where = min_gap(A + B, ex + band)
    print(f"min A/B gap away from zeros and the real axis: {g:.3f} mm at {where}")
    gA, wA = min_gap(A, ex + band)
    print(f"min A-A gap: {gA:.3f} mm at {wA}")
    # text vs field
    field = A + B
    fp = np.vstack([dense(p, 0.3) for p in field])
    tp = np.vstack([dense(p, 0.3) for p in T])
    body = tp[tp[:, 1] > 50]
    dmin = 1e9
    for x, y in body:
        m = (np.abs(fp[:, 0] - x) < 6) & (np.abs(fp[:, 1] - y) < 6)
        if m.any():
            dmin = min(dmin, float(np.hypot(fp[m, 0] - x, fp[m, 1] - y).min()))
    print(f"min text-to-field clearance: {dmin:.2f} mm")
    allp = np.vstack([dense(p, 1.0) for p in A + B + T + red])
    print("sheet bbox of ink:", np.round(allp.min(0), 2), np.round(allp.max(0), 2))
    print("psi footer:", stats)
    print("rulings at text column:", [round(y, 2) for y in rul])


if __name__ == "__main__":
    main()
