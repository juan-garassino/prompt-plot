"""r03 acceptance audit on the design geometry (encoding section 11 + ledger S1-S3, A1-A2).

    .venv/bin/python studio/millennium-bsd/rounds/r03/audit.py
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import piece as P  # noqa: E402

L = P.build_layers()
R = P.REPORT
CH = R["chords"]


def dense(runs, step=0.2):
    out = []
    for r in runs:
        for a, b in zip(r, r[1:]):
            n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
            for t in np.linspace(0, 1, n + 1):
                out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return np.asarray(out)


# exactness
bad = [n for n, (x, y) in P.ORB.items() if y * y + y != x ** 3 - x]
col = [c["k"] for c in CH if c["k"] > 1 and P.ORB[c["k"]][0] * P.ORB[-(c["k"] + 1)][1]
       - P.ORB[c["k"]][1] * P.ORB[-(c["k"] + 1)][0] != 0]
print(f"orbit +-61 on E: {not bad}; 60 chords collinear with P: {not col}")

# S2(a) oval marks
marked = [m for m in R["marks"]]
print(f"S2a oval points of chords 1-60 marked: {len(marked)} + P (gold disc) = {len(marked) + 1} / 62 "
      f"(-P and 61P lie on no chord); unmarked {len(R['unmarked'])}:")
for u in R["unmarked"]:
    print("    ", u)
print("   new marks:", [m for m in marked if m[1] != "ray"])

# S2(b) inner ends vs DRAWN E
E = dense(L["curves"], 0.1)
viol = []
for c in CH:
    own = [t for t, _ in c["pts"]]
    for a, b in c["iv"]:
        h = a if abs(a) < abs(b) else b
        if any(abs(h - t) < 0.05 for t in own):
            continue
        p = P._pt(c, h)
        d = float(np.hypot(E[:, 0] - p[0], E[:, 1] - p[1]).min())
        if d < 1.5:
            viol.append((c["k"], round(abs(h), 2), round(d, 2)))
print(f"S2b inner ray ends < 1.5 mm from drawn E and not on their own point: {viol or 'none'}")
print("    inner-end rule moves:", R.get("inner_end_rule"))

# S2(c) tangent
c1 = CH[0]
a, b = c1["iv"][0]
print(f"S2c tangent pass-1 spans t {min(abs(a), abs(b)):.2f} .. {max(abs(a), abs(b)):.2f} mm from P; 2nd pass offset {c1['off']:+.2f}")
seg = [P._pt(c1, a), P._pt(c1, b)]
pts = dense([seg], 0.02)
near = []
for n, (x, y) in P.ORB.items():
    if n in (1, -2):
        continue
    X, Y = P.sx(float(x)), P.sy(float(y))
    d = float(np.hypot(pts[:, 0] - X, pts[:, 1] - Y).min())
    if d < 1.2:
        near.append((n, round(d, 2)))
print(f"    non-own orbit points within 1.2 mm of the tangent's ink: {near or 'none'}")
egg_near = [p for p in E if math.hypot(p[0] - P.PX, p[1] - P.PY) < 20 and p[1] < P.PY and p[0] > P.PX]
if egg_near:
    dmin = min(math.hypot(p[0] - P.PX, p[1] - P.PY) for p in egg_near)
    print(f"    egg on the kissing (lower-right) side resumes {dmin:.2f} mm from P")
tan_d = dense([seg], 0.1)
kiss = min(float(np.hypot(tan_d[:, 0] - p[0], tan_d[:, 1] - p[1]).min()) for p in egg_near)
print(f"    min centre distance tangent pass-1 <-> drawn egg: {kiss:.2f} mm")

# A1 gold
g = L["gold"][-1]
print(f"A1 crossing angle {R['cross_angle']:.3f} deg at x = {R['zero_x']:.2f}; gold stretch {R['gold_len']:.2f} mm, "
      f"band = 2 passes at +-{P.GOLD_HALF} (0.7 nib => {2 * P.GOLD_HALF + 0.7:.2f} mm wide)")

# A2 / S3 type
bx = R["boxes"]
for k in ("statement", "series0", "series1", "right", "ziggurat", "zig_caption", "s1"):
    print(f"    box {k:11s}", [round(v, 2) for v in bx[k]])
T = dense(L["text"], 0.3)
left_mid = T[(T[:, 0] < 140) & (T[:, 1] > 250) & (T[:, 1] < 375)]
print(f"A2 text on the left at y 250-375: {len(left_mid)} samples; ray crop y = {P.FIELD_TOP} (= grid(81) = {P.grid(81):.1f})")
rc = bx["right"]
Tr = T[(T[:, 0] >= rc[0] - 0.01) & (T[:, 1] <= rc[3] + 0.01) & (T[:, 1] >= rc[1] - 0.01)]
arm = dense([r for r in L["curves"] if max(p[0] for p in r) > 140], 0.3)
d_arm = min(float(np.hypot(arm[:, 0] - p[0], arm[:, 1] - p[1]).min()) for p in Tr[::3])
print(f"S3d right column right edge {rc[2]:.2f} (target 282), left {rc[0]:.2f}; min distance to the lower arm {d_arm:.2f} mm")
cap_stmt = P.grid(84) + 2.5
print(f"    statement cap line {cap_stmt:.2f}; series caption top {bx['series0'][3]:.2f}; right edge {bx['series0'][2]:.2f}")
G = dense(L["hair"] + L["chords"] + L["curves"] + L["gold"], 0.5)
best = 1e9
for i in range(0, len(T), 2000):
    d = np.hypot(T[i:i + 2000, None, 0] - G[None, :, 0], T[i:i + 2000, None, 1] - G[None, :, 1])
    best = min(best, d.min())
print(f"closest type ink to any line ink: {best:.2f} mm")
print("zig lens", R["zig_lens"])
print("mate trims (k, was, now):", R.get("mate_trim"))
