"""Acceptance audit (encoding section 11) on the design geometry + orbit exactness.

    .venv/bin/python studio/millennium-bsd/rounds/r02/audit.py
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import piece as P  # noqa: E402

L = P.build_layers()
CH = P.REPORT["chords"]

# exactness: every orbit point on E, collinearity of every chord with P
bad = [n for n, (x, y) in P.ORB.items() if y * y + y != x ** 3 - x]
col = [c["k"] for c in CH if c["k"] > 1 and P.ORB[c["k"]][0] * P.ORB[-(c["k"] + 1)][1]
       - P.ORB[c["k"]][1] * P.ORB[-(c["k"] + 1)][0] != 0]
odd_egg = all((float(P.ORB[n][0]) <= P.E2) == (n % 2 == 1) for n in range(1, 62))
print(f"orbit +-61 on E: {not bad}; chords collinear with P: {not col}; odd<->egg parity: {odd_egg}")

# 1. one hub: inner ends
inner = []
for c in CH:
    ivs = c.get("iv", [])
    if ivs:
        inner.append((c["k"], c["tier"], min(min(abs(a), abs(b)) for a, b in ivs)))
at7 = [k for k, _, r in inner if r < 7.05]
print("chords reaching the 7 mm hub circle:", at7)
print("inner ends k:r  ", " ".join(f"{k}:{r:.1f}" for k, _, r in inner))
for tier in ("heavy", "medium", "fine"):
    rs = [r for k, t, r in inner if t == tier]
    print(f"  {tier:6s} n={len(rs):2d} median inner end {np.median(rs):5.1f} mm")
print("lens-rule moves:", {c['k']: c['lens'] for c in CH if c.get('lens')})
print("pieces dropped by clearance:", {c['k']: c['dropped'] for c in CH if c.get('dropped')})
# every chord line passes through P (by construction: _seg from PX,PY along u)
ink = [np.asarray(r) for k in ("hair", "chords") for r in L[k]]
off = 0.0
for r in L["hair"][:-0] or []:
    pass
dmin_disc = min(np.hypot(r[:, 0] - P.PX, r[:, 1] - P.PY).min() for r in ink if len(r) > 1)
print(f"closest ray ink to hub centre {dmin_disc:.2f} mm (disc R {P.DISC_R})")

# 2. two pieces: no curve ink between the egg tip and the branch vertex on the mirror
cur = np.vstack([np.asarray(r) for r in L["curves"][:0]] or [np.zeros((0, 2))])
curves = [np.asarray(r) for r in L["curves"]]
gap = [p for r in curves for p in r if 101.7 < p[0] < 131.0 and abs(p[1] - 200) < 20
       and not (152 < p[0])]
egg = P.egg_loop()
print(f"curve ink in the gap band: {len(gap)} points; egg x {egg[:, 0].min():.1f}..{egg[:, 0].max():.1f},"
      f" y {egg[:, 1].min():.1f}..{egg[:, 1].max():.1f} (mirror 200)")

# 4. crossing
print(f"L crossing at x={P.REPORT['zero_x']:.2f}, angle {P.REPORT['cross_angle']:.3f} deg,"
      f" min {P.REPORT['L_min']:.5f} at s={P.REPORT['s_min']:.3f}, L(1.5)={P.REPORT['L15']:.5f},"
      f" L(2)={P.REPORT['L2']:.5f}, gold {P.REPORT['gold_len']:.2f} mm")


# 5. type clearance to line ink
def pts(runs, step=0.3):
    out = []
    for r in runs:
        for a, b in zip(r, r[1:]):
            n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
            for t in np.linspace(0, 1, n + 1):
                out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return np.asarray(out)


T = pts(L["text"], 0.5)
G = pts(L["hair"] + L["chords"] + L["curves"] + L["gold"], 0.5)
best = 1e9
for i in range(0, len(T), 2000):
    d = np.hypot(T[i:i + 2000, None, 0] - G[None, :, 0], T[i:i + 2000, None, 1] - G[None, :, 1])
    best = min(best, d.min())
print(f"closest type ink to any line ink: {best:.2f} mm")
bz = P.REPORT["boxes"]["ziggurat"]
zig = T[(T[:, 0] <= bz[2] + 0.01) & (T[:, 1] >= bz[1] - 0.01) & (T[:, 1] <= bz[3] + 0.01) & (T[:, 0] < 90)]
dz = min(np.hypot(zig[i:i + 2000, None, 0] - G[None, :, 0], zig[i:i + 2000, None, 1] - G[None, :, 1]).min()
         for i in range(0, len(zig), 2000))
print(f"ziggurat right edge x={bz[2]:.1f}; clearance to nearest ray {dz:.1f} mm; line lengths {P.REPORT['zig_lens']}")
