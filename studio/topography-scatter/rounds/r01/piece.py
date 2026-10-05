"""ATTENTION AS TOPOGRAPHY — exact recreation, r01.

This is a REPRODUCTION, not a design.  Every element position is read off
``studio/topography-scatter/ref/reference.png`` in normalised (u, v) sheet
coordinates (u = 0 left .. 1 right, v = 0 top .. 1 bottom) and mapped into the
drawable area.  The three amoeboid silhouettes (Q / K / V) are NOT invented:
they were traced out of the reference with marching squares on the colour masks
and are baked in below as ``Q_OUT`` / ``K_OUT`` / ``V_OUT``.

Pens (``colors=4``): 0 red, 1 blue, 2 ochre, 3 black.

Entry point: ``attention_as_topography``.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.generators import (
    _chain_segments,
    _marching_squares,
    _poly,
    _stroke_text,
    _text_width,
)
from promptplot.generative.kit import tone_dots
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

RED, BLUE, OCHRE, BLACK = 0, 1, 2, 3

# --------------------------------------------------------------------------
# traced silhouettes  (normalised sheet coords, closed loops)
# --------------------------------------------------------------------------

Q_OUT = [
    (0.1742, 0.0499), (0.1687, 0.0509), (0.1634, 0.0527), (0.1581, 0.0549), (0.1527, 0.0568), (0.1473, 0.0583),
    (0.1419, 0.0594), (0.1364, 0.0606), (0.1311, 0.0624), (0.1259, 0.0652), (0.1211, 0.0690), (0.1166, 0.0736),
    (0.1126, 0.0791), (0.1094, 0.0856), (0.1066, 0.0925), (0.1041, 0.0996), (0.1018, 0.1068), (0.0992, 0.1139),
    (0.0965, 0.1209), (0.0937, 0.1278), (0.0906, 0.1344), (0.0872, 0.1406), (0.0836, 0.1466), (0.0799, 0.1525),
    (0.0765, 0.1588), (0.0736, 0.1656), (0.0708, 0.1724), (0.0688, 0.1799), (0.0695, 0.1878), (0.0715, 0.1952),
    (0.0743, 0.2020), (0.0778, 0.2083), (0.0811, 0.2147), (0.0843, 0.2211), (0.0877, 0.2274), (0.0911, 0.2337),
    (0.0948, 0.2397), (0.0991, 0.2445), (0.1043, 0.2468), (0.1097, 0.2451), (0.1143, 0.2408), (0.1182, 0.2353),
    (0.1217, 0.2290), (0.1250, 0.2227), (0.1285, 0.2165), (0.1322, 0.2106), (0.1365, 0.2057), (0.1415, 0.2022),
    (0.1466, 0.1995), (0.1514, 0.1954), (0.1557, 0.1905), (0.1599, 0.1854), (0.1639, 0.1799), (0.1676, 0.1740),
    (0.1702, 0.1670), (0.1714, 0.1592), (0.1720, 0.1513), (0.1725, 0.1433), (0.1735, 0.1354), (0.1748, 0.1277),
    (0.1771, 0.1204), (0.1800, 0.1137), (0.1831, 0.1071), (0.1859, 0.1002), (0.1878, 0.0927), (0.1898, 0.0853),
    (0.1927, 0.0785), (0.1942, 0.0710), (0.1930, 0.0633), (0.1895, 0.0572), (0.1848, 0.0530), (0.1797, 0.0504),
]

K_OUT = [
    (0.1338, 0.4222), (0.1276, 0.4256), (0.1225, 0.4316), (0.1184, 0.4391), (0.1153, 0.4476), (0.1130, 0.4566),
    (0.1111, 0.4658), (0.1087, 0.4748), (0.1056, 0.4833), (0.1021, 0.4915), (0.0991, 0.5000), (0.0984, 0.5095),
    (0.1001, 0.5188), (0.1028, 0.5276), (0.1055, 0.5363), (0.1076, 0.5454), (0.1084, 0.5550), (0.1074, 0.5644),
    (0.1047, 0.5731), (0.1011, 0.5813), (0.0971, 0.5889), (0.0926, 0.5960), (0.0881, 0.6030), (0.0842, 0.6107),
    (0.0818, 0.6196), (0.0823, 0.6291), (0.0849, 0.6379), (0.0889, 0.6456), (0.0934, 0.6527), (0.0985, 0.6588),
    (0.1040, 0.6640), (0.1099, 0.6685), (0.1161, 0.6718), (0.1227, 0.6729), (0.1293, 0.6734), (0.1359, 0.6748),
    (0.1424, 0.6764), (0.1489, 0.6752), (0.1543, 0.6698), (0.1581, 0.6620), (0.1587, 0.6525), (0.1582, 0.6429),
    (0.1565, 0.6336), (0.1538, 0.6249), (0.1504, 0.6167), (0.1466, 0.6088), (0.1430, 0.6006), (0.1399, 0.5921),
    (0.1377, 0.5831), (0.1379, 0.5736), (0.1403, 0.5647), (0.1439, 0.5566), (0.1475, 0.5485), (0.1502, 0.5398),
    (0.1517, 0.5304), (0.1548, 0.5220), (0.1597, 0.5156), (0.1653, 0.5105), (0.1710, 0.5058), (0.1767, 0.5008),
    (0.1818, 0.4947), (0.1855, 0.4868), (0.1862, 0.4774), (0.1830, 0.4691), (0.1783, 0.4623), (0.1729, 0.4566),
    (0.1673, 0.4515), (0.1616, 0.4466), (0.1561, 0.4412), (0.1509, 0.4353), (0.1457, 0.4293), (0.1402, 0.4241),
]

V_OUT = [
    (0.8397, 0.0448), (0.8330, 0.0493), (0.8277, 0.0568), (0.8254, 0.0668), (0.8278, 0.0768), (0.8329, 0.0847),
    (0.8386, 0.0917), (0.8440, 0.0992), (0.8484, 0.1078), (0.8521, 0.1172), (0.8550, 0.1272), (0.8561, 0.1378),
    (0.8555, 0.1486), (0.8538, 0.1591), (0.8514, 0.1693), (0.8484, 0.1793), (0.8446, 0.1885), (0.8397, 0.1966),
    (0.8342, 0.2040), (0.8291, 0.2118), (0.8241, 0.2198), (0.8185, 0.2269), (0.8126, 0.2335), (0.8068, 0.2404),
    (0.8017, 0.2482), (0.7975, 0.2571), (0.7944, 0.2669), (0.7935, 0.2776), (0.7954, 0.2880), (0.7984, 0.2978),
    (0.8018, 0.3075), (0.8053, 0.3170), (0.8096, 0.3258), (0.8161, 0.3308), (0.8231, 0.3279), (0.8292, 0.3216),
    (0.8347, 0.3143), (0.8406, 0.3079), (0.8474, 0.3034), (0.8546, 0.3005), (0.8619, 0.2986), (0.8693, 0.2976),
    (0.8763, 0.2940), (0.8827, 0.2884), (0.8883, 0.2813), (0.8929, 0.2728), (0.8958, 0.2629), (0.8972, 0.2523),
    (0.8989, 0.2417), (0.9015, 0.2316), (0.9050, 0.2221), (0.9095, 0.2135), (0.9142, 0.2051), (0.9173, 0.1954),
    (0.9177, 0.1846), (0.9161, 0.1741), (0.9135, 0.1640), (0.9108, 0.1539), (0.9078, 0.1440), (0.9047, 0.1342),
    (0.9017, 0.1243), (0.8987, 0.1144), (0.8954, 0.1047), (0.8920, 0.0951), (0.8885, 0.0855), (0.8844, 0.0766),
    (0.8796, 0.0683), (0.8741, 0.0610), (0.8680, 0.0548), (0.8615, 0.0496), (0.8545, 0.0459), (0.8471, 0.0441),
]

# --------------------------------------------------------------------------
# type
# --------------------------------------------------------------------------


def _tracked_text(text, x, y, height, color=None, tracking=1.0, f=2400) -> List[GCodeCommand]:
    """``_stroke_text`` with a letterspacing multiplier.

    Case comes from the shared font (which is case-aware), so ``softmax`` sets
    lower case. Only the advance needs overriding: the reference letterspaces
    the titling wide (3.9 mm pitch at 2.8 mm caps) and sets the ``softmax``
    caption slightly tight.
    """
    adv = 5.6 * (height / 6.0) * tracking
    out: List[GCodeCommand] = []
    cx = x
    for ch in text:
        if ch != " ":
            out += _stroke_text(ch, cx, y, height, color=color, f=f)
        cx += adv
    return out


def _bold_text(text, x, y, height, color=None, weight=0.20, passes=4) -> List[GCodeCommand]:
    """Serif-ish weight faked by re-stroking the glyph on a small circle."""
    out: List[GCodeCommand] = []
    for k in range(passes):
        a = 2 * math.pi * k / passes
        out += _stroke_text(text, x + weight * math.cos(a), y + weight * math.sin(a),
                            height, color=color)
    out += _stroke_text(text, x, y, height, color=color)
    return out


# --------------------------------------------------------------------------
# geometry helpers
# --------------------------------------------------------------------------


def _closed_smooth(pts: Sequence[Pt], subdiv: int = 4) -> List[Pt]:
    """Catmull-Rom through a CLOSED control loop."""
    n = len(pts)
    out: List[Pt] = []
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        for k in range(subdiv):
            t = k / subdiv
            t2, t3 = t * t, t * t * t
            x = 0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t
                       + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t
                       + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(out[0])
    return out


def _inside(poly: Sequence[Pt], x: float, y: float) -> bool:
    n = len(poly)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y):
            xc = xi + (y - yi) * (xj - xi) / (yj - yi)
            if x < xc:
                inside = not inside
        j = i
    return inside


def _shrink(poly: Sequence[Pt], d: float) -> List[Pt]:
    """Move every vertex ``d`` toward the centroid-ish inward normal."""
    n = len(poly)
    out = []
    for i in range(n):
        px, py = poly[(i - 1) % n]
        cx, cy = poly[i]
        nx, ny = poly[(i + 1) % n]
        tx, ty = nx - px, ny - py
        L = math.hypot(tx, ty) or 1.0
        out.append((cx + d * (ty / L), cy - d * (tx / L)))
    return out


def _signed_area(poly: Sequence[Pt]) -> float:
    s = 0.0
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        s += x0 * y1 - x1 * y0
    return 0.5 * s


def _bez(p0: Pt, p1: Pt, p2: Pt, p3: Pt, n: int = 90) -> List[Pt]:
    out = []
    for k in range(n + 1):
        t = k / n
        m = 1 - t
        out.append((
            m ** 3 * p0[0] + 3 * m * m * t * p1[0] + 3 * m * t * t * p2[0] + t ** 3 * p3[0],
            m ** 3 * p0[1] + 3 * m * m * t * p1[1] + 3 * m * t * t * p2[1] + t ** 3 * p3[1],
        ))
    return out


def _arc(cx: float, cy: float, r: float, a0: float, a1: float, n: int = 64) -> List[Pt]:
    return [(cx + r * math.cos(a0 + (a1 - a0) * k / n),
             cy + r * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]


def _resample(pts: Sequence[Pt], step: float) -> List[Pt]:
    if len(pts) < 2:
        return list(pts)
    out = [pts[0]]
    carry = 0.0
    for i in range(1, len(pts)):
        ax, ay = pts[i - 1]
        bx, by = pts[i]
        seg = math.hypot(bx - ax, by - ay)
        if seg <= 1e-9:
            continue
        t = step - carry
        while t <= seg:
            out.append((ax + (bx - ax) * t / seg, ay + (by - ay) * t / seg))
            t += step
        carry = (carry + seg) % step
    out.append(pts[-1])
    return out


def _dash(pts: Sequence[Pt], pattern: Sequence[float]) -> List[List[Pt]]:
    """Split a polyline into ON runs following a repeating on/off pattern (mm)."""
    runs: List[List[Pt]] = []
    cur: List[Pt] = []
    idx = 0
    left = pattern[0]
    on = True
    prev = pts[0]
    if on:
        cur = [prev]
    for i in range(1, len(pts)):
        ax, ay = prev
        bx, by = pts[i]
        seg = math.hypot(bx - ax, by - ay)
        pos = 0.0
        while seg - pos > left:
            pos += left
            px = ax + (bx - ax) * pos / seg
            py = ay + (by - ay) * pos / seg
            if on:
                cur.append((px, py))
                if len(cur) >= 2:
                    runs.append(cur)
                cur = []
            else:
                cur = [(px, py)]
            on = not on
            idx = (idx + 1) % len(pattern)
            left = pattern[idx]
        left -= (seg - pos)
        if on:
            cur.append((bx, by))
        prev = (bx, by)
    if on and len(cur) >= 2:
        runs.append(cur)
    return runs


DASH = (2.6, 2.0)
FINE_DASH = (1.5, 1.4)
DOT = (0.45, 1.5)
DASHDOT = (3.2, 1.5, 0.5, 1.5)


def _styled(pts: Sequence[Pt], style: str, pen: Optional[int], f: int = 2200) -> List[GCodeCommand]:
    if style == "solid":
        return _poly(pts, color=pen, f=f)
    pat = {"dash": DASH, "fine": FINE_DASH, "dot": DOT, "dashdot": DASHDOT}[style]
    out: List[GCodeCommand] = []
    for run in _dash(_resample(pts, 0.6), pat):
        out += _poly(run, color=pen, f=f)
    return out


def _disc(cx: float, cy: float, r: float, pen: Optional[int], spacing: float = 0.34) -> List[GCodeCommand]:
    """Solid dot as an Archimedean spiral + a closing rim.

    The reference's nodes are solid black dots, so these fill on purpose — but
    the pitch is held at the pen tip rather than driven below it, and small dots
    get a turn floor so they close up instead of printing as a ring.
    """
    turns = max(3, int(r / spacing))
    n = turns * 26
    pts = [(cx + r * (k / n) * math.cos(2 * math.pi * turns * k / n),
            cy + r * (k / n) * math.sin(2 * math.pi * turns * k / n)) for k in range(n + 1)]
    pts += _arc(cx, cy, r, 0, 2 * math.pi, 40)
    return _poly(pts, color=pen, f=1600)


def _ring(cx: float, cy: float, r: float, pen: Optional[int], n: int = 48) -> List[GCodeCommand]:
    return _poly(_arc(cx, cy, r, 0, 2 * math.pi, n), color=pen)


def _band(pts: Sequence[Pt], width: float, pen: Optional[int], tip: float = 0.28) -> List[GCodeCommand]:
    """A keyline drawn as a narrow band of parallel offsets."""
    passes = max(2, int(round(width / tip)) + 1)
    out: List[GCodeCommand] = []
    n = len(pts)
    for k in range(passes):
        d = -width / 2.0 + width * k / (passes - 1)
        off = []
        for i in range(n):
            px, py = pts[(i - 1) % n]
            nx, ny = pts[(i + 1) % n]
            tx, ty = nx - px, ny - py
            L = math.hypot(tx, ty) or 1.0
            off.append((pts[i][0] + d * (ty / L), pts[i][1] - d * (tx / L)))
        out += _poly(off, color=pen)
    return out


# --------------------------------------------------------------------------
# the scribble fill — the expensive part
# --------------------------------------------------------------------------


def _scribble(
    poly: Sequence[Pt],
    rng: SeededRNG,
    pen: Optional[int],
    spacing: float,
    angle: float,
    warp: float,
    freq: float,
    step: float = 0.9,
    phase: float = 0.0,
) -> List[GCodeCommand]:
    """A continuous wandering serpentine clipped to ``poly``.

    Rows run along ``angle``; each sample is displaced by smooth 2D value noise
    so the rows meander instead of ruling — the pen still never lays two rows
    closer than ``spacing``/2 on average, which is what keeps it plottable.
    """
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    diag = math.hypot(max(xs) - min(xs), max(ys) - min(ys)) * 0.62
    ca, sa = math.cos(angle), math.sin(angle)

    runs: List[List[Pt]] = []
    cur: List[Pt] = []
    nrows = int(2 * diag / spacing) + 1
    flip = False
    for j in range(nrows):
        t = -diag + j * spacing
        line: List[Pt] = []
        m = int(2 * diag / step) + 1
        for i in range(m + 1):
            s = -diag + i * step
            if flip:
                s = diag - i * step
            x = cx + s * ca - t * sa
            y = cy + s * sa + t * ca
            nx = rng.noise2d(x * freq + phase, y * freq) - 0.5
            ny = rng.noise2d(x * freq + 31.7 + phase, y * freq + 12.3) - 0.5
            line.append((x + warp * nx, y + warp * ny))
        flip = not flip
        for p in line:
            if _inside(poly, p[0], p[1]):
                cur.append(p)
            else:
                if len(cur) >= 2:
                    runs.append(cur)
                cur = []
        if len(cur) >= 2:
            runs.append(cur)
        cur = []

    out: List[GCodeCommand] = []
    for r in runs:
        out += _poly(r, color=pen, f=2600)
    return out


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------


def attention_as_topography(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 4,
) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0

    def P(u: float, v: float) -> Pt:
        return (x0 + u * W, y1 - v * H)

    def S(du: float) -> float:
        """normalised-u length -> mm"""
        return du * W

    def pen(i: int) -> Optional[int]:
        return i % colors if colors > 1 else None

    RD, BL, OC, BK = pen(RED), pen(BLUE), pen(OCHRE), pen(BLACK)

    out: List[GCodeCommand] = []

    # ---------------------------------------------------------------- blobs
    blobs = (
        (Q_OUT, RD, 3),
        (K_OUT, BL, 11),
        (V_OUT, OC, 23),
    )
    for k, (ctrl, pn, ph) in enumerate(blobs):
        loop = _closed_smooth([P(u, v) for u, v in ctrl], subdiv=4)
        inner = _shrink(loop, -0.45 if _signed_area(loop) > 0 else 0.45)
        if not _inside(loop, inner[0][0], inner[0][1]):
            inner = _shrink(loop, 0.45 if _signed_area(loop) > 0 else -0.45)
        # two near-orthogonal meandering passes: solid tone with a swirl grain,
        # never two rows closer than ~0.85 mm inside one pass.
        # TWO near-orthogonal meandering passes, both at >= 0.86 mm. A third
        # crossing pass pushed effective coverage past the pen tip and the fill
        # flooded; two is enough to read as the reference's filled amoeba.
        out += _scribble(inner, rng, pn, 0.86, math.radians(21 + 9 * k), 1.05, 0.16, 0.9, ph)
        out += _scribble(inner, rng, pn, 0.92, math.radians(112 + 13 * k), 1.15, 0.13, 0.9, ph + 5)
        out += _band(loop, 0.26, pn, tip=0.22)

    # blob labels + interior nodes -------------------------------------
    out += _bold_text("Q", *P(0.0690, 0.1180), 5.2, color=BK)
    out += _bold_text("K", *P(0.0720, 0.5745), 5.2, color=BK)
    out += _bold_text("V", *P(0.8150, 0.1780), 5.2, color=BK)
    out += _bold_text("Z", *P(0.8510, 0.7590), 5.2, color=BK)

    q_a, q_b, q_c = P(0.1399, 0.1278), P(0.1426, 0.1617), P(0.1190, 0.1430)
    out += _disc(*q_a, 1.06, BK)
    out += _disc(*q_b, 0.88, BK)
    out += _disc(*q_c, 0.28, BK)
    q_hub = P(0.1755, 0.1855)
    out += _poly([q_a, q_c, q_b, q_hub], color=BK, f=2600)
    out += _poly([q_a, P(0.2050, 0.1345)], color=BK, f=2600)
    out += _poly([q_b, q_hub], color=BK, f=2600)
    out += _disc(*P(0.1880, 0.1545), 0.85, RD)
    out += _disc(*P(0.0643, 0.2545), 0.78, RD)

    k_a, k_b = P(0.1340, 0.5196), P(0.1276, 0.6232)
    out += _disc(*k_a, 0.86, BK)
    out += _disc(*k_b, 0.26, BK)
    k_hub = P(0.1660, 0.5215)
    out += _poly([k_a, k_hub], color=BK, f=2600)
    out += _poly([k_b, P(0.1720, 0.5980)], color=BK, f=2600)

    v_a, v_b = P(0.8819, 0.1697), P(0.8448, 0.2544)
    out += _disc(*v_a, 1.32, BK)
    out += _disc(*v_b, 0.86, BK)
    out += _poly(_bez(v_a, P(0.8680, 0.1930), P(0.8560, 0.2150), v_b, 40), color=BK, f=2600)
    out += _poly([v_b, P(0.8630, 0.2480)], color=BK, f=2600)
    out += _disc(*P(0.8720, 0.2430), 0.20, BK)

    # ---------------------------------------------------------- contour map
    out += _contour_map(rng, P, S, BK)

    # ------------------------------------------------------------- softmax
    out += _softmax(rng, P, S, BK)

    # ---------------------------------------------------------- dot column
    out += _dot_column(P, S, BK)

    # ------------------------------------------------------------- terrain
    out += _terrain(rng, P, S, BK)

    # ---------------------------------------------------------- connectors
    out += _connectors(P, RD, BL, OC, BK)

    # ----------------------------------------------------------- furniture
    out += _furniture(P, S, RD, BK)

    # ----------------------------------------------------------------- type
    out += _typography(P, S, BK)

    return out


# --------------------------------------------------------------------------


def _contour_map(rng, P, S, BK) -> List[GCodeCommand]:
    """QK^T — nested iso-rings over a two-peak field, tight nest at the peak."""
    U0, U1, V0, V1 = 0.325, 0.625, 0.245, 0.545
    nx, ny = 190, 190

    def raw(u, v):
        f = 0.0
        for (cu, cv, a, su, sv) in (
            (0.4238, 0.4035, 1.00, 0.0255, 0.0275),   # the sharp peak (measured)
            (0.4620, 0.3640, 0.54, 0.0460, 0.0420),   # the broad shoulder
            (0.4180, 0.4620, 0.42, 0.0360, 0.0310),
            (0.5020, 0.4120, 0.42, 0.0410, 0.0380),
            (0.5330, 0.3720, 0.22, 0.0360, 0.0290),
            (0.3830, 0.4300, 0.22, 0.0330, 0.0340),
            (0.3720, 0.3960, 0.26, 0.0460, 0.0400),   # the left shoulder
            (0.5400, 0.3380, 0.14, 0.0330, 0.0260),
            (0.4760, 0.4760, 0.21, 0.0340, 0.0250),
            (0.4560, 0.3040, 0.26, 0.0380, 0.0300),   # the upper lobe
            (0.5100, 0.3200, 0.18, 0.0330, 0.0270),
            (0.5560, 0.4260, 0.14, 0.0300, 0.0250),
        ):
            f += a * math.exp(-(((u - cu) / su) ** 2 + ((v - cv) / sv) ** 2) / 2)
        return f

    def field(u, v):
        # domain warp: this is what stops the rings reading as a bullseye
        wu = 0.016 * (rng.fbm(u * 13.0 + 2.0, v * 13.0 + 5.0, octaves=3) - 0.5)
        wv = 0.016 * (rng.fbm(u * 13.0 + 21.0, v * 13.0 + 17.0, octaves=3) - 0.5)
        f = raw(u + wu, v + wv)
        return f * (0.90 + 0.20 * rng.fbm(u * 24.0 + 9.0, v * 24.0 + 3.0, octaves=3))

    us = [U0 + (U1 - U0) * i / (nx - 1) for i in range(nx)]
    vs = [V0 + (V1 - V0) * j / (ny - 1) for j in range(ny)]
    F = [[field(u, v) for u in us] for v in vs]
    fmax = max(max(r) for r in F)

    # levels chosen from a nominal gaussian so ring RADII grow like k**1.45 —
    # dense nest at the summit, open rings on the flanks (as in the reference).
    N = 20
    sig, rmax = 0.044, 0.096
    levels = [fmax * math.exp(-((rmax * (k / N) ** 1.08) / sig) ** 2 / 2)
              for k in range(1, N + 1)]

    out: List[GCodeCommand] = []
    for li, lv in enumerate(levels):
        segs = _marching_squares(F, us, vs, lv)
        if not segs:
            continue
        for chain in _chain_segments(segs):
            pts = [P(u, v) for u, v in chain]
            if len(pts) < 5:
                continue
            style = "dash" if li in (0, 3) else ("fine" if li == 1 else "solid")
            out += _styled(pts, style, BK, f=2400)

    # the two loose dashed outriders that wander off to the right
    out += _styled(_bez(P(0.4500, 0.2560), P(0.5450, 0.2620), P(0.6050, 0.3450),
                        P(0.5800, 0.4350), 90), "dash", BK, f=2400)
    out += _styled(_bez(P(0.5800, 0.4350), P(0.5600, 0.5100), P(0.4700, 0.5450),
                        P(0.4050, 0.5100), 90), "dash", BK, f=2400)
    return out


def _softmax(rng, P, S, BK) -> List[GCodeCommand]:
    """Flat tilted ellipse + an inner mass that ramps as a bounded DOT CLOUD.

    The obvious way to draw this gradient — let tone drive the stipple spacing —
    floods solid the moment the spacing falls under the pen tip, which is exactly
    what happened in r01/v8. ``tone_dots`` removes the failure mode by
    construction: tone sets the PROBABILITY a cell is inked, one dot per cell,
    cell never below the tip, so peak density is capped at 1/cell**2 dots/mm**2.
    """
    CU, CV = 0.4870, 0.5975
    AU, BV = 0.1160, 0.0200
    cx, cy = P(CU, CV)
    a_mm = S(AU)
    b_mm = abs(P(0.0, CV)[1] - P(0.0, CV + BV)[1]) * 0.92   # v-length in mm
    tilt = math.radians(2.0)                # right end sits slightly higher
    ct, st = math.cos(tilt), math.sin(tilt)

    def E(s: float, t: float) -> Pt:
        """s in [-1,1] along the major axis, t in [-1,1] across."""
        return (cx + a_mm * s * ct - b_mm * t * st,
                cy + a_mm * s * st + b_mm * t * ct)

    out: List[GCodeCommand] = []
    out += _poly([E(math.cos(2 * math.pi * k / 200), math.sin(2 * math.pi * k / 200))
                  for k in range(201)], color=BK, f=2400)

    # the mass: s from S0 (fades in) to S1 (rounded solid tip)
    S0, S1 = -0.95, 0.44
    STIP = -0.06       # s where the tone is already fully solid

    def half(s: float) -> float:
        h = math.sqrt(max(0.0, 1.0 - s * s)) * 0.96
        if s > STIP:   # round the right tip off well inside the rim
            h *= math.sqrt(max(0.0, 1.0 - ((s - STIP) / (S1 - STIP)) ** 2)) ** 0.55
        return h

    def dens(s: float) -> float:
        t = (s - S0) / (STIP - S0)
        return min(1.0, 0.04 + 0.96 * max(0.0, t) ** 1.05)

    # invert E(): mm -> (s, t), so tone() can be evaluated on the raw grid
    def local(x: float, y: float) -> Tuple[float, float]:
        dx, dy = x - cx, y - cy
        return ((dx * ct + dy * st) / a_mm, (-dx * st + dy * ct) / b_mm)

    def tone(x: float, y: float) -> float:
        s, t = local(x, y)
        if s < S0 or s > S1 or abs(t) > half(s):
            return 0.0
        return dens(s)

    pad = 1.0
    corners = [E(sg * 1.0, tg * 1.0) for sg in (-1, 1) for tg in (-1, 1)]
    xs = [p[0] for p in corners]
    ys = [p[1] for p in corners]
    region = (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)
    out += tone_dots(region, tone, rng, pen=BK, cell=0.85, jitter=0.55, r=0.18, f=2000)

    out += _tracked_text("softmax", *P(0.3150, 0.6370), 3.0, color=BK, tracking=0.92)
    return out


def _dot_column(P, S, BK) -> List[GCodeCommand]:
    """The vertical string of growing dots through the softmax lens."""
    u = 0.4534
    out: List[GCodeCommand] = []
    spec = [
        (0.5215, 0.80), (0.5442, 0.92), (0.5634, 1.24),
        (0.6000, 2.35), (0.6680, 1.10), (0.7030, 1.24), (0.7480, 2.78),
        (0.9362, 1.10),
    ]
    for v, r in spec:
        out += _disc(*P(u, v), r, BK)
    out += _ring(*P(u, 0.6340), 0.62, BK, 30)

    # the thin spine that threads them
    out += _poly([P(u, 0.5680), P(u, 0.6300)], color=BK, f=2400)
    out += _poly([P(u, 0.6390), P(u, 0.6620)], color=BK, f=2400)
    out += _poly([P(u, 0.6740), P(u, 0.6960)], color=BK, f=2400)
    for run in _dash([P(u, 0.7650), P(u, 0.8190)], (3.0, 2.4)):
        out += _poly(run, color=BK, f=2400)

    # the big plus below
    out += _poly([P(0.4325, 0.8415), P(0.4745, 0.8415)], color=BK, f=2400)
    out += _poly([P(u, 0.8020), P(u, 0.8860)], color=BK, f=2400)
    return out


def _terrain(rng, P, S, BK) -> List[GCodeCommand]:
    """Z — a stack of terrain profiles, one line family, no occlusion.

    The reference's curves cross one another freely, so this is a profile
    stack (rows of the surface) rather than a hidden-line surface.
    """
    U0, U1 = 0.5450, 0.8900
    VBASE = 0.8380
    AMP = 0.0900            # measured: summit 0.123 v above base
    DEPTH = 0.0090          # far->near baseline drift
    rows, nu = 25, 230

    # (u, v, amp, sigma_u, sigma_v).  sigma_v is LARGE and the centres sit at or
    # beyond the depth extremes, so each mass' height varies MONOTONICALLY from
    # the far row to the near row: that is what makes the profiles open into
    # nested fans that cross one another, which is the reference's whole look.
    # The summits sit in the RIGHT half — the reference's left third is a long,
    # nearly flat approach.
    peaks = (
        (0.449, -0.12, 1.26, 0.062, 0.58),      # the dominant summit (u=0.700)
        (0.710, 1.12, 0.94, 0.062, 0.60),       # the second mass (u=0.790)
        (0.855, 0.18, 0.34, 0.048, 0.52),       # the low right shoulder
        (0.335, 1.02, 0.52, 0.058, 0.52),
        (0.235, 0.08, 0.26, 0.052, 0.46),
        (0.580, 0.52, 0.42, 0.046, 0.36),
        (0.790, 0.88, 0.30, 0.046, 0.42),
    )
    dips = (
        (0.400, 1.26, 0.72, 0.095, 0.44),
        (0.650, 1.30, 0.66, 0.105, 0.44),
        (0.250, 1.22, 0.44, 0.085, 0.42),
        (0.880, 1.26, 0.34, 0.075, 0.42),
    )

    def ramp(t):
        t = min(1.0, max(0.0, t))
        return t * t * (3 - 2 * t)

    def h(u, v):
        e = ramp(u / 0.22) * ramp((1.0 - u) / 0.085)
        f = 0.0
        for (cu, cv, a, su, sv) in peaks:
            f += a * math.exp(-(((u - cu) / su) ** 2 + ((v - cv) / sv) ** 2) / 2)
        for (cu, cv, a, su, sv) in dips:
            f -= a * math.exp(-(((u - cu) / su) ** 2 + ((v - cv) / sv) ** 2) / 2)
        f += 0.12 * (rng.fbm(u * 11.0 + 3.0, v * 5.0 + 9.0, octaves=3) - 0.5)
        return e * f

    out: List[GCodeCommand] = []
    for j in range(rows):
        v = j / (rows - 1)
        gain = 0.95 + 0.10 * rng.random()       # small jitter; the fan is ordered
        drift = 0.0022 * (rng.random() - 0.5)
        pts = []
        for i in range(nu + 1):
            u = i / nu
            gu = U0 + (U1 - U0) * (0.5 + (u - 0.5) * (0.945 + 0.090 * v)) + 0.0050 * v
            gv = VBASE + DEPTH * (v - 0.5) + drift - AMP * gain * h(u, v)
            pts.append(P(gu, gv))
        out += _poly(pts, color=BK, f=2600)

    # the tail that runs off to the right and lands on a node
    tail = [P(0.8850, 0.8330), P(0.9000, 0.8315), P(0.9120, 0.8305)]
    for run in _dash(_resample(tail, 0.5), (2.0, 1.4)):
        out += _poly(run, color=BK, f=2400)
    return out


def _connectors(P, RD, BL, OC, BK) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []

    # --- red: Q -> the contour peak -------------------------------------
    red = [
        ((0.1760, 0.1880), (0.2600, 0.1180), (0.3560, 0.1520), (0.3530, 0.3760), "solid"),
        ((0.1762, 0.1800), (0.2720, 0.1330), (0.3700, 0.1950), (0.3660, 0.3900), "solid"),
        ((0.1755, 0.1610), (0.2560, 0.1120), (0.3460, 0.1800), (0.3440, 0.3200), "dash"),
        ((0.1770, 0.1910), (0.2780, 0.1680), (0.3800, 0.2550), (0.3760, 0.3820), "dashdot"),
        ((0.1768, 0.1960), (0.2950, 0.1960), (0.4000, 0.3200), (0.3900, 0.4120), "solid"),
        ((0.1758, 0.1690), (0.2680, 0.1260), (0.3600, 0.2180), (0.3560, 0.3020), "fine"),
        ((0.1885, 0.1560), (0.2500, 0.1380), (0.3150, 0.1400), (0.3900, 0.1220), "dash"),
        ((0.1770, 0.1875), (0.2600, 0.1700), (0.3400, 0.1690), (0.3960, 0.1520), "solid"),
    ]
    for a, b, c, d, st in red:
        out += _styled(_bez(P(*a), P(*b), P(*c), P(*d), 110), st, RD, f=2400)

    # --- blue: K -> the contour foot ------------------------------------
    blue = [
        ((0.1862, 0.5060), (0.2750, 0.5450), (0.3550, 0.5450), (0.3990, 0.4180), "solid"),
        ((0.1836, 0.5220), (0.2800, 0.5640), (0.3620, 0.5620), (0.4020, 0.4420), "dash"),
        ((0.1760, 0.5620), (0.2750, 0.5980), (0.3620, 0.5940), (0.4000, 0.4700), "dashdot"),
        ((0.1706, 0.5940), (0.2800, 0.6240), (0.3680, 0.6180), (0.3980, 0.4960), "solid"),
        ((0.1650, 0.6220), (0.2850, 0.6480), (0.3740, 0.6400), (0.3950, 0.5250), "dash"),
        ((0.1600, 0.6460), (0.2900, 0.6680), (0.3800, 0.6580), (0.3920, 0.5560), "fine"),
        ((0.1855, 0.4980), (0.2700, 0.5100), (0.3480, 0.5080), (0.4140, 0.4520), "dashdot"),
    ]
    for a, b, c, d, st in blue:
        out += _styled(_bez(P(*a), P(*b), P(*c), P(*d), 110), st, BL, f=2400)

    # --- ochre: V -> a wide left sweep that loops back down into Z --------
    # each is two joined cubics so the bundle crosses itself the way the
    # reference does (out to the left, back down to the right).
    ochre = [
        ((0.8560, 0.1560), (0.7700, 0.2280), (0.6700, 0.2760), (0.5940, 0.3400),
         (0.5420, 0.3860), (0.5380, 0.4400), (0.5900, 0.4700)),
        ((0.8300, 0.2180), (0.7420, 0.2680), (0.6480, 0.3220), (0.5790, 0.3880),
         (0.5360, 0.4340), (0.5500, 0.4940), (0.6140, 0.5240)),
        ((0.8060, 0.2900), (0.7200, 0.3350), (0.6400, 0.3980), (0.5840, 0.4640),
         (0.5520, 0.5080), (0.5860, 0.5620), (0.6520, 0.5880)),
        ((0.8010, 0.3130), (0.7300, 0.3800), (0.6640, 0.4520), (0.6220, 0.5180),
         (0.5990, 0.5620), (0.6420, 0.6100), (0.7020, 0.6350)),
        ((0.8290, 0.3290), (0.7800, 0.4180), (0.7180, 0.5080), (0.6780, 0.5820),
         (0.6560, 0.6320), (0.6980, 0.6820), (0.7270, 0.7100)),
        ((0.8620, 0.3050), (0.8300, 0.4200), (0.7760, 0.5450), (0.7330, 0.6450),
         (0.7170, 0.6980), (0.7220, 0.7400), (0.7190, 0.7780)),
        ((0.8880, 0.2980), (0.8650, 0.4100), (0.8150, 0.5550), (0.7580, 0.6720),
         (0.7320, 0.7220), (0.7160, 0.7540), (0.7090, 0.7820)),
        ((0.8740, 0.1790), (0.9020, 0.2900), (0.8800, 0.4400), (0.8280, 0.5620),
         (0.7900, 0.6420), (0.7420, 0.7220), (0.7150, 0.7640)),
        ((0.8960, 0.2320), (0.9160, 0.3400), (0.8960, 0.4900), (0.8430, 0.6050),
         (0.8060, 0.6750), (0.7570, 0.7400), (0.7230, 0.7720)),
    ]
    for a, b, c, d, e, f2, g in ochre:
        C, D = P(*c), P(*d)
        # reflect the incoming handle so the two cubics join without a cusp
        E = (D[0] + 0.55 * (D[0] - C[0]), D[1] + 0.55 * (D[1] - C[1]))
        pts = _bez(P(*a), P(*b), C, D, 80)
        pts += _bez(D, E, P(*f2), P(*g), 70)[1:]
        out += _poly(pts, color=OC, f=2400)

    # --- black wandering dashed arcs -------------------------------------
    black = [
        ((0.1120, 0.3080), (0.1500, 0.3050), (0.1720, 0.2350), (0.1750, 0.1500), "dash"),
        ((0.5450, 0.1560), (0.5900, 0.2100), (0.6250, 0.2150), (0.6600, 0.2080), "dash"),
        ((0.4750, 0.3120), (0.5350, 0.3600), (0.5750, 0.4250), (0.5700, 0.5000), "dash"),
        ((0.5950, 0.4160), (0.6450, 0.4700), (0.6700, 0.5400), (0.6400, 0.6100), "dash"),
        ((0.3760, 0.6200), (0.4100, 0.6700), (0.4550, 0.6950), (0.4860, 0.6920), "dot"),
        ((0.4860, 0.6920), (0.5400, 0.6880), (0.5950, 0.7550), (0.6350, 0.7900), "dash"),
        ((0.6350, 0.7900), (0.6700, 0.8100), (0.6950, 0.7600), (0.7020, 0.7230), "dash"),
        ((0.6300, 0.2960), (0.6900, 0.3500), (0.7150, 0.4300), (0.6900, 0.4900), "dot"),
        ((0.3700, 0.2930), (0.4200, 0.3050), (0.4550, 0.3200), (0.4930, 0.3220), "solid"),
        ((0.4930, 0.3220), (0.5400, 0.3250), (0.5700, 0.3900), (0.5950, 0.4170), "dash"),
        ((0.6900, 0.5900), (0.7250, 0.6400), (0.7200, 0.6900), (0.7020, 0.7230), "dash"),
        ((0.2050, 0.2750), (0.2450, 0.2600), (0.2850, 0.2250), (0.3050, 0.1900), "dashdot"),
    ]
    for a, b, c, d, st in black:
        out += _styled(_bez(P(*a), P(*b), P(*c), P(*d), 110), st, BK, f=2400)
    return out


def _furniture(P, S, RD, BK) -> List[GCodeCommand]:
    """Short rules, brackets, corner marks, crosses, loose dots — off-grid."""
    out: List[GCodeCommand] = []

    def seg(a, b, style="solid", pn=BK):
        out.extend(_styled([P(*a), P(*b)], style, pn, f=2400))

    # --- upper-left cluster ---------------------------------------------
    seg((0.0450, 0.2620), (0.0450, 0.4060), "dashdot", RD)
    seg((0.0900, 0.2930), (0.0900, 0.3360), "dashdot", RD)
    seg((0.0310, 0.3340), (0.1200, 0.3340))
    seg((0.0345, 0.3300), (0.0345, 0.3390))

    # --- top-middle corner figure ----------------------------------------
    out += _poly([P(0.4790, 0.0480), P(0.4980, 0.0480)], color=BK, f=2400)
    cxq, cyq = P(0.4980, 0.1150)
    rq = S(0.0205)
    out += _poly(_arc(cxq, cyq, rq, math.pi / 2, 0.0, 40), color=BK, f=2400)
    out += _poly([P(0.5185, 0.1150), P(0.5430, 0.1150)], color=BK, f=2400)
    out += _poly([P(0.5430, 0.1150), P(0.5430, 0.1360)], color=BK, f=2400)

    # --- verticals -------------------------------------------------------
    seg((0.4307, 0.0050), (0.4307, 0.1180), "dot")
    seg((0.4307, 0.1380), (0.4307, 0.5770))
    seg((0.4520, 0.2020), (0.4520, 0.5000), "dashdot")
    seg((0.3000, 0.2930), (0.3000, 0.7490))
    seg((0.5670, 0.2450), (0.5670, 0.3170))
    seg((0.5050, 0.3060), (0.6510, 0.3060), "dash")
    seg((0.4100, 0.2700), (0.4100, 0.3550), "dashdot")
    seg((0.3810, 0.5000), (0.3810, 0.6600), "dashdot")
    seg((0.4040, 0.4950), (0.4040, 0.6450), "dashdot")
    seg((0.4830, 0.5000), (0.4830, 0.6200), "dashdot")
    seg((0.6130, 0.5000), (0.6130, 0.7800), "dash")
    seg((0.8510, 0.5000), (0.8510, 0.5810))
    seg((0.8720, 0.5090), (0.8720, 0.5380), "dot")
    seg((0.6910, 0.3570), (0.6910, 0.4390), "dashdot")
    seg((0.0430, 0.5950), (0.0430, 0.6790), "dot")

    # --- crosses / plus marks --------------------------------------------
    seg((0.2750, 0.6650), (0.3330, 0.6650))
    seg((0.5540, 0.5030), (0.5780, 0.5030), "fine")
    seg((0.5660, 0.4930), (0.5660, 0.5140), "fine")
    seg((0.8980, 0.6510), (0.9170, 0.6510))
    seg((0.9080, 0.6150), (0.9080, 0.7780), "dash")
    out += _poly(_bez(P(0.9080, 0.7780), P(0.9200, 0.8300), P(0.9420, 0.8500),
                      P(0.9650, 0.8550), 60), color=BK, f=2400)

    # --- right-hand bracket + big arc -------------------------------------
    seg((0.9610, 0.1240), (0.9610, 0.2400))
    seg((0.9510, 0.2400), (0.9740, 0.2400))
    seg((0.9150, 0.2390), (0.9410, 0.2390))
    cxa, cya = P(0.9640, 0.2450)
    out += _poly(_arc(cxa, cya, S(0.1120), -math.pi / 2, -math.pi, 60), color=BK, f=2400)
    seg((0.8340, 0.3420), (0.8650, 0.3420))
    seg((0.8500, 0.3420), (0.8500, 0.4300))

    # --- lower-left arc ----------------------------------------------------
    out += _poly(_bez(P(0.1680, 0.8380), P(0.2100, 0.7620), P(0.2900, 0.7120),
                      P(0.3900, 0.7050), 90), color=BK, f=2400)

    # --- lower-right stack --------------------------------------------------
    out += _poly([P(0.8700, 0.8380), P(0.8990, 0.8380), P(0.8990, 0.8555),
                  P(0.8700, 0.8555), P(0.8700, 0.8380)], color=BK, f=2400)
    seg((0.8690, 0.8300), (0.8690, 0.8580))
    out += _poly([P(0.8830, 0.8210), P(0.8830, 0.8090), P(0.8970, 0.8090)], color=BK, f=2400)
    seg((0.8640, 0.8120), (0.8640, 0.8260))
    # filled square + long rule
    out += _poly([P(0.8352, 0.9460), P(0.8420, 0.9460), P(0.8420, 0.9570),
                  P(0.8352, 0.9570), P(0.8352, 0.9460)], color=BK, f=1800)
    out += _poly([P(0.8360, 0.9490), P(0.8412, 0.9490)], color=BK, f=1800)
    out += _poly([P(0.8360, 0.9530), P(0.8412, 0.9530)], color=BK, f=1800)
    seg((0.8540, 0.9490), (0.9650, 0.9490))

    # --- scatter in the right half (the reference is not empty there, and the
    #     marks sit at assorted angles rather than on one axis) --------------
    seg((0.6880, 0.4620), (0.6960, 0.5310), "dashdot")
    seg((0.7440, 0.4120), (0.7620, 0.4880), "dash")
    seg((0.8060, 0.4360), (0.8180, 0.4700), "dot")
    seg((0.6480, 0.6560), (0.6620, 0.7280), "dashdot")
    seg((0.7830, 0.6200), (0.7960, 0.6900), "dash")
    seg((0.9400, 0.3160), (0.9480, 0.3760), "dot")
    seg((0.7230, 0.2330), (0.7620, 0.2280), "fine")
    seg((0.6210, 0.1420), (0.6120, 0.1940))
    seg((0.9620, 0.4260), (0.9700, 0.4580), "fine")
    seg((0.7640, 0.1680), (0.7960, 0.1550), "dash")
    seg((0.2380, 0.7700), (0.2760, 0.7620), "fine")
    seg((0.3420, 0.1780), (0.3180, 0.2180), "dot")
    out += _poly([P(0.7700, 0.7950), P(0.7700, 0.8250), P(0.7980, 0.8250)],
                 color=BK, f=2400)
    out += _poly([P(0.5980, 0.2280), P(0.5980, 0.2000), P(0.6250, 0.2000)],
                 color=BK, f=2400)
    out += _styled(_bez(P(0.6060, 0.8250), P(0.6450, 0.8700), P(0.6950, 0.8800),
                        P(0.7350, 0.8650), 70), "dot", BK, f=2400)
    out += _styled(_bez(P(0.2700, 0.3900), P(0.3100, 0.4300), P(0.3350, 0.4900),
                        P(0.3300, 0.5400), 70), "dot", BK, f=2400)
    out += _styled(_bez(P(0.7600, 0.1250), P(0.7900, 0.1600), P(0.7850, 0.2100),
                        P(0.7550, 0.2450), 60), "dot", BK, f=2400)

    # --- loose dots (sizes read off the reference) -------------------------
    dots = [
        (0.0240, 0.0480, 0.28), (0.7145, 0.1112, 0.52), (0.9280, 0.1082, 0.92),
        (0.4307, 0.1274, 0.92), (0.6894, 0.3072, 0.82), (0.4932, 0.3216, 0.95),
        (0.5956, 0.4173, 1.06), (0.7370, 0.5001, 0.88), (0.0546, 0.5156, 0.55),
        (0.1806, 0.5336, 0.73), (0.5892, 0.6070, 0.82), (0.4854, 0.6915, 0.82),
        (0.7019, 0.7219, 1.60), (0.0774, 0.7278, 0.52), (0.8808, 0.8300, 0.82),
        (0.3730, 0.2930, 0.72), (0.7770, 0.8300, 0.30), (0.2600, 0.4400, 0.22),
        (0.6300, 0.2960, 0.22), (0.9660, 0.4430, 0.20),
    ]
    for u, v, r in dots:
        out += _disc(*P(u, v), r, BK)
    return out


def _typography(P, S, BK) -> List[GCodeCommand]:
    """Metrics read off the reference: TOPOGRAPHY is 39 mm wide at 2.8 mm caps."""
    out: List[GCodeCommand] = []
    TR = 1.52       # title tracking -> 3.9 mm pitch
    out += _tracked_text("ATTENTION", *P(0.0365, 0.8935), 2.8, color=BK, tracking=TR)
    out += _tracked_text("AS", *P(0.0365, 0.9175), 2.8, color=BK, tracking=TR)
    out += _tracked_text("TOPOGRAPHY", *P(0.0365, 0.9420), 2.8, color=BK, tracking=TR)
    out += _poly([P(0.2050, 0.9320), P(0.2800, 0.9320)], color=BK, f=2400)

    # QK^T — 6.4 mm wide overall, superscript T
    qx, qy = P(0.4810, 0.2405)
    out += _stroke_text("QK", qx, qy, 3.3, color=BK)
    out += _stroke_text("T", qx + _text_width("QK", 3.3) * 0.98, qy + 1.9, 2.0, color=BK)

    out += _tracked_text("Z=AV", *P(0.9080, 0.9250), 2.7, color=BK, tracking=1.42)
    return out
