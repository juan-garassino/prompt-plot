"""ORRERY r02 — ORBITS THAT MEAN.

The r01 orrery composition (a sun inside one dotted orbit, four planetary
systems Q, K, V, Z riding it, bundles between them) rebuilt so that every
radius, turn, line count and epicycle is a number out of GPT-2 small.

Source: ``gpt2_head.npz`` beside this file, written by ``mechanism.py``: a
numpy-only forward pass of GPT-2 small on
    "The pen plotter drew a black hole while the transformer watched itself think."
checked against HuggingFace/torch attention for all 12 layers (max |diff| 2.3e-6).
Head: layer 4, head 3, the head where " itself" looks hardest at " transformer"
(0.557; the strongest such head of all 144).  Query: " itself" (token 12).

THE MAPPING (one line each)
  sun ........ the softmax row A[itself, :].  Key j is one spiral groove of
               20*A_j turns at 0.85 mm pitch; grooves nest by weight, lightest
               inside, so a groove's radius is cumulative attention.
               ONE TURN = 5 % OF THE ATTENTION.
  dial ....... one tick per token on the sun's rim, the sentence left -> right
               across the top; each groove ends under its own tick.  Masked
               (future) tokens are open rings.
  Q, K, V .... every row of that matrix is a planet.  Radius = its true 64-d
               norm; bearing = its place in the sentence, left -> right across
               the side facing the sun.  Rings are the norm scale (one ring per
               4 units for Q and K, which share one scale, one per unit for V);
               the axis carries the outer ring's value.
  Z .......... z = sum_j A_j v_j as Ptolemy's epicycles: the weighted values
               chained head to tail, largest first, in the plane of z-hat and
               the first principal direction orthogonal to it.  Projection is
               linear, so the chain closes EXACTLY on z; the star is z's pole.
  red, blue .. one hairline from the query and one from each key that earns a
               line, meeting at that key's tick: the dot product q.k.
  ochre ...... round(20*A_j) parallel lines per value (keys under 2.5 % earn
               none).  ONE LINE = 5 %, the same unit as a turn.

Pens (plot order, light -> dark): 0 goldenrod V · 1 blue K · 2 crimson Q ·
3 green Z · 4 black sun, dial, orbit, star, type.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Circle, Rect, Union, clip, offset
from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

HERE = Path(__file__).resolve().parent
Pt = Tuple[float, float]
Poly = List[Pt]
Cmds = List[GCodeCommand]

OCHRE, BLUE, RED, GREEN, BLACK = 0, 1, 2, 3, 4

# design box = A4 portrait drawable (190 x 277 mm), origin bottom-left, y up
DW, DH = 190.0, 277.0

UNIT = 20.0          # one turn / one ribbon line = 1/20 of the attention
PITCH = 0.85         # groove pitch inside a key's band (mm)
GAP = 2.0            # gap between two keys' bands (mm)
LINE = 0.9           # ribbon line pitch (mm)
LANE_GAP = 2.4       # gap between two value ribbons where they land (mm)
LAND_MID = 8.0       # centre of the landing arc on Z's ring (deg)


# =========================================================================== data
def compute() -> Dict:
    d = np.load(HERE / "gpt2_head.npz")
    toks = [str(t) for t in d["tokens"]]
    A = d["A"].astype(np.float64)
    Q, K, V, Z = (d[k].astype(np.float64) for k in "QKVZ")
    T = len(toks)
    i = toks.index(" itself")
    n = i + 1
    a = A[i, :n]
    z = Z[i]
    tr = toks.index(" transformer")

    # epicycles: weighted values in the plane (z-hat, e2)
    arms = a[:, None] * V[:n]
    u = z / np.linalg.norm(z)
    Pa = arms - np.outer(arms @ u, u)
    _, sv, vt = np.linalg.svd(Pa, full_matrices=False)
    e2 = vt[0]
    if (arms[tr] @ e2) < 0:
        e2 = -e2
    ax, ay = arms @ e2, arms @ u                        # (horizontal, along the pole)
    order = [int(j) for j in np.argsort(-np.linalg.norm(arms, axis=1))]

    return dict(
        toks=toks, T=T, i=i, n=n, a=a, tr=tr,
        q_norm=np.linalg.norm(Q, axis=1), k_norm=np.linalg.norm(K, axis=1),
        v_norm=np.linalg.norm(V, axis=1), z_norm=float(np.linalg.norm(z)),
        arms_full=np.linalg.norm(arms, axis=1), ax=ax, ay=ay, order=order,
        chain_close=float(abs(ax.sum()) + abs(ay.sum() - np.linalg.norm(z))),
        z_err=float(np.abs(a @ V[:n] - z).max()),
        check_err=float(np.max(d["check_err"])) if "check_err" in d.files else float("nan"),
        layer=int(d["layer"]), head=int(d["head"]),
    )


# ====================================================================== geometry
def polm(c: Pt, r: float, deg: float) -> Pt:
    """deg CCW from east."""
    t = math.radians(deg)
    return (c[0] + r * math.cos(t), c[1] + r * math.sin(t))


def pole(c: Pt, r: float, th: float) -> Pt:
    """th degrees clockwise from up."""
    t = math.radians(th)
    return (c[0] + r * math.sin(t), c[1] + r * math.cos(t))


def ring_pts(c: Pt, r: float, a0: float = 0.0, a1: float = 360.0, step: float = 0.9) -> Poly:
    n = max(12, int(abs(math.radians(a1 - a0)) * r / step) + 1)
    return [polm(c, r, a0 + (a1 - a0) * k / n) for k in range(n + 1)]


def bez(p0: Pt, c1: Pt, c2: Pt, p3: Pt, n: int = 90) -> Poly:
    out = []
    for k in range(n + 1):
        t = k / n
        u = 1 - t
        out.append((
            u**3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t**3 * p3[1],
        ))
    return out


def arclen(p: Poly) -> List[float]:
    s = [0.0]
    for (x0, y0), (x1, y1) in zip(p, p[1:]):
        s.append(s[-1] + math.hypot(x1 - x0, y1 - y0))
    return s


def _sub(pts: Poly, s: List[float], a: float, b: float) -> Poly:
    out: Poly = []
    for k in range(1, len(pts)):
        if s[k] < a:
            continue
        if not out:
            t = (a - s[k - 1]) / max(1e-9, s[k] - s[k - 1])
            out.append((pts[k - 1][0] + (pts[k][0] - pts[k - 1][0]) * t,
                        pts[k - 1][1] + (pts[k][1] - pts[k - 1][1]) * t))
        if s[k] >= b:
            t = (b - s[k - 1]) / max(1e-9, s[k] - s[k - 1])
            out.append((pts[k - 1][0] + (pts[k][0] - pts[k - 1][0]) * t,
                        pts[k - 1][1] + (pts[k][1] - pts[k - 1][1]) * t))
            return out
        out.append(pts[k])
    return out


def trim_start(p: Poly, d: float) -> Poly:
    s = arclen(p)
    return _sub(p, s, d, s[-1]) if d < s[-1] else []


def trim_end(p: Poly, d: float) -> Poly:
    s = arclen(p)
    return _sub(p, s, 0.0, s[-1] - d) if d < s[-1] else []


def unit(v: Pt) -> Pt:
    L = math.hypot(v[0], v[1]) or 1.0
    return (v[0] / L, v[1] / L)


def rot(v: Pt, deg: float) -> Pt:
    t = math.radians(deg)
    return (v[0] * math.cos(t) - v[1] * math.sin(t), v[0] * math.sin(t) + v[1] * math.cos(t))


def add(p: Pt, v: Pt, k: float = 1.0) -> Pt:
    return (p[0] + v[0] * k, p[1] + v[1] * k)


# ========================================================================== type
def _glyph_extent(ch: str) -> Tuple[float, float]:
    strokes = _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
    xs = [x for s in strokes for x, _ in s]
    return (min(xs), max(xs)) if xs else (0.0, 0.0)


def layout(text: str, h: float, track: float = 1.0) -> Tuple[List[Tuple[str, float]], float]:
    """Place each glyph by its MEASURED extent (the engine's proportional
    advance for 'i' is 1.1 units while the glyph sits at x=1.8, so 'i' prints
    over its neighbour).  Returns [(char, x_origin)], width in mm."""
    sc = h / 6.0
    gap = 1.05 * track
    x = 0.0
    out = []
    for ch in text:
        if ch == " ":
            x += 2.6 * sc * track
            continue
        lo, hi = _glyph_extent(ch)
        out.append((ch, x - lo * sc))
        x += (hi - lo) * sc + gap * sc
    return out, max(0.0, x - gap * sc)


# ========================================================================= sheet
class Sheet:
    """(pen, polyline) in design mm; type on the black layer, knocked out of
    every other line by a halo."""

    def __init__(self) -> None:
        self.lines: List[Tuple[int, Poly, bool]] = []
        self.glyphs: List[Tuple[int, Poly]] = []
        self.boxes = []

    def line(self, pen: int, pts: Poly, knock: bool = True) -> None:
        if len(pts) >= 2:
            self.lines.append((pen, list(pts), knock))

    def ring(self, pen: int, c: Pt, r: float, a0=0.0, a1=360.0, knock=True) -> None:
        self.line(pen, ring_pts(c, r, a0, a1), knock)

    def dashed(self, pen: int, pts: Poly, on: float, off: float) -> None:
        s = arclen(pts)
        t = 0.0
        while t < s[-1]:
            b = min(s[-1], t + on)
            if b - t > 0.2:
                self.line(pen, _sub(pts, s, t, b))
            t += on + off

    def dot(self, pen: int, c: Pt, d: float, knock: bool = True) -> None:
        """Filled disc as ONE spiral stroke.  Pitch 0.3 mm is under the 0.8 mm
        floor on purpose and only inside discs <= 2.6 mm: a dot must read solid."""
        R = d / 2.0
        turns = max(1.5, R / 0.3)
        n = int(turns * 18)
        pts = [polm(c, R * k / n, 360.0 * turns * k / n) for k in range(n + 1)]
        pts += ring_pts(c, R, 360.0 * turns, 360.0 * turns + 360.0, 0.4)
        self.line(pen, pts, knock)

    def hollow(self, pen: int, c: Pt, d: float) -> None:
        self.ring(pen, c, d / 2.0)

    def text(self, s: str, x: float, y: float, h: float, anchor: str = "l",
             halo: bool = True, track: float = 1.0) -> Dict[int, Tuple[float, float]]:
        """Returns {char index: (x0, x1)} so callers can underline words."""
        placed, w = layout(s, h, track)
        if anchor == "c":
            x -= w / 2.0
        elif anchor == "r":
            x -= w
        sc = h / 6.0
        spans = {}
        k = 0
        for idx, ch in enumerate(s):
            if ch == " ":
                continue
            c, gx = placed[k]
            k += 1
            strokes = _GLYPHS.get(c) or _GLYPHS.get(c.upper()) or []
            lo, hi = _glyph_extent(c)
            spans[idx] = (x + gx + lo * sc, x + gx + hi * sc)
            for st in strokes:
                self.glyphs.append((BLACK, [(x + gx + px * sc, y + py * sc) for px, py in st]))
        if halo:
            self.boxes.append((x - 1.0, y - 0.35 * h - 0.5, x + w + 1.0, y + 1.1 * h + 0.5))
        return spans

    # ---------------------------------------------------------------- emit
    def emit(self, bounds, colors: int) -> Cmds:
        x0, y0, x1, y1 = bounds
        k = min((x1 - x0) / DW, (y1 - y0) / DH)
        ox = x0 + ((x1 - x0) - DW * k) / 2.0
        oy = y0 + ((y1 - y0) - DH * k) / 2.0

        def P(i: int) -> Optional[int]:
            return i % colors if colors > 1 else None

        def M(p: Pt) -> Pt:
            return (ox + p[0] * k, oy + p[1] * k)

        halo = Union(*[Rect(*b) for b in self.boxes]) if self.boxes else None
        frame = Rect(0.0, 0.0, DW, DH)
        out: Cmds = []
        for pen, pts, knock in self.lines:
            runs = clip(pts, halo, keep="outside") if (knock and halo is not None) else [pts]
            for r in runs:
                for rr in clip(r, frame, keep="inside"):
                    if arclen(rr)[-1] > 0.15:
                        out += _poly([M(p) for p in rr], color=P(pen), f=2000)
        for pen, pts in self.glyphs:
            out += _poly([M(p) for p in pts], color=P(pen), f=1800)
        return out


# ======================================================================= marks
def star(sh: Sheet, c: Pt) -> None:
    """Engraver's six-point star: z's pole, the one pole on the plate."""
    r0 = 0.8
    sh.line(BLACK, [pole(c, r0, 0), pole(c, 3.2, 0)])
    sh.line(BLACK, [pole(c, r0, 180), pole(c, 3.0, 180)])
    for t in (90, 270):
        sh.line(BLACK, [pole(c, r0, t), pole(c, 2.4, t)])
    for t in (55, 125, 235, 305):
        sh.line(BLACK, [pole(c, r0, t), pole(c, 2.0, t)])
    sh.ring(BLACK, c, r0)


def graticule(sh: Sheet, pen: int, c: Pt, scale: float, step: float, upto: float) -> List[float]:
    radii = []
    v = step
    while v <= upto + 1e-9:
        sh.ring(pen, c, v * scale)
        radii.append(v * scale)
        v += step
    return radii


def bearing(j: int) -> float:
    """Sun dial: the sentence left -> right across the TOP of the sun."""
    return 150.0 - 10.0 * j


def sys_bearing(j: int) -> float:
    """Systems: the same left -> right order across the BOTTOM of each
    system (the dial mirrored), so each system hands its sentence to the sun."""
    return -bearing(j)


def system(sh: Sheet, pen: int, hub: Pt, radii, scale: float, step: float, top: float,
           n_vis: int, big: Sequence[int], label: str, small: float = 1.1) -> Dict[int, Pt]:
    rings = graticule(sh, pen, hub, scale, step, top)
    R = max(rings)
    sh.line(pen, [hub, (hub[0], hub[1] + R + 2.2)])
    sh.text(label, hub[0], hub[1] + R + 3.4, 1.9, "c", track=1.7)
    pos: Dict[int, Pt] = {}
    for j, r in enumerate(radii):
        p = polm(hub, r * scale, sys_bearing(j))
        pos[j] = p
        if j < n_vis:
            sh.dot(pen, p, 1.8 if j in big else small)
        else:
            sh.hollow(pen, p, 1.4)
    sh.dot(pen, hub, 2.6)
    return pos


# ======================================================================= piece
def orrery_orbits_that_mean(rng: SeededRNG, bounds, colors: int = 5) -> Cmds:
    D = compute()
    toks, a, n, T, tr, qi = D["toks"], D["a"], D["n"], D["T"], D["tr"], D["i"]
    sh = Sheet()

    # ------------------------------------------------------------ layout
    C = (95.0, 147.0)            # the sun
    RE = 90.0                    # the head's orbit: all four systems ride it
    HQ = polm(C, RE, 139.0)
    HK = polm(C, RE, 45.0)
    HV = polm(C, RE, -38.0)
    HZ = polm(C, RE, -90.0)

    S_QK = 26.0 / D["k_norm"].max()        # Q and K share one scale (one space)
    S_V = 21.0 / D["v_norm"].max()
    S_Z = 27.0 / D["z_norm"]

    lines_per = [int(math.floor(UNIT * x + 0.5)) for x in a]
    carried = [j for j in range(n) if lines_per[j] >= 1]

    # ------------------------------------------------------------ the sun
    order = sorted(range(n), key=lambda j: a[j])                 # lightest inside
    r_in = 9.0
    band_end: Dict[int, Pt] = {}
    for j in order:
        tau = UNIT * a[j]
        r_out = r_in + tau * PITCH
        n_s = max(8, int(tau * 2 * math.pi * r_out / 0.9))
        pts = [polm(C, r_in + PITCH * (tau * k / n_s), bearing(j) - 360.0 * (tau - tau * k / n_s))
               for k in range(n_s + 1)]
        per = max(2, int(n_s / max(1.0, tau)))                   # one stroke per turn
        for k0 in range(0, len(pts) - 1, per):
            sh.line(BLACK, pts[k0:k0 + per + 1])
        band_end[j] = polm(C, r_out, bearing(j))
        r_in = r_out + GAP
    R_rim = r_in
    sh.ring(BLACK, C, R_rim)
    sh.ring(BLACK, C, R_rim)                                     # sum = 1, double pass
    for j in range(n):
        sh.dot(BLACK, band_end[j], 1.0)
    junction: Dict[int, Pt] = {}
    for j in range(T):
        if j < n:
            sh.line(BLACK, [polm(C, R_rim + 0.7, bearing(j)), polm(C, R_rim + 2.5, bearing(j))])
            if j in carried:
                junction[j] = polm(C, R_rim + 4.2, bearing(j))
                sh.dot(BLACK, junction[j], 1.7)
        else:
            sh.hollow(BLACK, polm(C, R_rim + 1.9, bearing(j)), 1.5)

    # core type: Q . K^T over softmax, with a real centred dot
    sh.text("Q", C[0] - 3.3, C[1] + 0.9, 3.0, "c", halo=False)
    sh.dot(BLACK, (C[0] - 0.4, C[1] + 2.3), 0.9, knock=False)
    sh.text("K", C[0] + 2.4, C[1] + 0.9, 3.0, "c", halo=False)
    sh.text("T", C[0] + 5.0, C[1] + 3.1, 1.5, "c", halo=False)
    sh.text("softmax", C[0], C[1] - 4.2, 2.1, "c", halo=False)

    # ------------------------------------------------------------ the head's orbit
    sh.dashed(BLACK, ring_pts(C, RE, 0, 360, 0.6), 2.2, 3.6)

    # ------------------------------------------------------------ Q, K, V systems
    kpos = system(sh, BLUE, HK, D["k_norm"], S_QK, 4.0, 28.0, n, carried, "|k| = 28")
    qpos = system(sh, RED, HQ, D["q_norm"], S_QK, 4.0, 12.0, T, [qi], "|q| = 12", small=0.75)
    vpos = system(sh, OCHRE, HV, D["v_norm"], S_V, 1.0, 5.0, n, carried, "|v| = 5")
    q_self = qpos[qi]

    # ------------------------------------------------------------ Z: epicycles
    RZ = D["z_norm"] * S_Z
    graticule(sh, GREEN, HZ, S_Z, 1.0, 2.0)
    sh.ring(GREEN, HZ, RZ)
    z_top = HZ[1] + RZ + 3.2
    sh.line(GREEN, [HZ, (HZ[0], z_top)])
    star(sh, (HZ[0], z_top + 1.3))
    cur = HZ
    joints = [cur]
    for idx, j in enumerate(D["order"]):
        dx, dy = D["ax"][j] * S_Z, D["ay"][j] * S_Z
        L = math.hypot(dx, dy)
        if idx == 0 or L >= 0.45:
            sh.ring(OCHRE, cur, L)                               # deferent / epicycle
        nxt = (cur[0] + dx, cur[1] + dy)
        sh.line(OCHRE, [cur, nxt])
        cur = nxt
        joints.append(cur)
    sh.dot(GREEN, joints[-1], 2.2)                               # z itself
    sh.dot(GREEN, HZ, 2.6)

    # ------------------------------------------------------------ Q . K lines
    def strand(P0: Pt, J: Pt, pen: int, lift: Pt, start_gap: float, side: float,
               backwards: bool = False) -> None:
        """Cubic from a planet to a junction.  It leaves along ``lift`` blended
        with the straight direction and arrives between the radial and the way
        back to its source, so it never overshoots the tick and hooks back."""
        L = math.hypot(J[0] - P0[0], J[1] - P0[1])
        d0 = unit((J[0] - P0[0], J[1] - P0[1]))
        out_dir = unit((J[0] - C[0], J[1] - C[1]))
        c1 = add(P0, unit(add(d0, lift)), 0.36 * L)
        back = (-d0[0], -d0[1])
        c2 = add(J, unit(add(rot(out_dir, side), back, 0.8)), 0.42 * L)  # from above, toward home
        runs = clip(bez(P0, c1, c2, J, 160), Circle(J[0], J[1], 1.5), keep="outside")
        if runs:
            pl = trim_start(runs[0], start_gap)
            # alternate direction so the layer zig-zags planet -> tick -> tick
            # -> planet instead of flying home empty after every strand
            sh.line(pen, pl[::-1] if backwards else pl)

    for k, j in enumerate(carried):
        strand(q_self, junction[j], RED, (0.1, 0.7), 1.5, 14.0, k % 2 == 1)    # the query arcs over
        strand(kpos[j], junction[j], BLUE, (0.3, 0.2), 1.4, -14.0, k % 2 == 1)  # each key swings in

    # ------------------------------------------------------------ V ribbons -> Z
    # Each carried value drops out of its planet and swings into Z, arriving
    # radially.  Landings run down Z's right-hand arc in the planets' left ->
    # right order, so the family nests instead of crossing.
    RL = RZ + 0.8
    land = sorted(carried, key=lambda j: vpos[j][0])
    arcs = [lines_per[j] * LINE for j in land]
    total = sum(arcs) + LANE_GAP * (len(land) - 1)
    ang = LAND_MID + math.degrees(total / RL) / 2.0
    for j, w in zip(land, arcs):
        m = lines_per[j]
        mid = ang - math.degrees((w / 2.0) / RL)
        ang -= math.degrees((w + LANE_GAP) / RL)
        P3 = polm(HZ, RL, mid)
        P0 = vpos[j]
        outward = unit((P3[0] - HZ[0], P3[1] - HZ[1]))
        c1 = (P0[0], P0[1] - (0.55 * abs(P0[1] - P3[1]) + 6.0))
        c2 = add(P3, outward, 0.50 * abs(P0[0] - P3[0]))
        centre = bez(P0, c1, c2, P3, 200)
        for kk in range(m):
            off = (kk - (m - 1) / 2.0) * LINE
            pl = offset(centre, off) if abs(off) > 1e-9 else centre
            pl = trim_start(pl, 1.3 + abs(off) / math.tan(math.radians(15.0)))
            runs = clip(pl, Circle(HZ[0], HZ[1], RL - 0.1), keep="outside") if pl else []
            if runs:
                sh.line(OCHRE, runs[0])

    # ------------------------------------------------------------ type
    sh.text("ATTENTION", DW / 2.0, 261.0, 6.0, "c", track=2.2)
    sh.text("gpt-2 small  ·  layer %d  ·  head %d" % (D["layer"], D["head"]), DW / 2.0, 253.0, 2.1, "c")

    sh.text("Q", HQ[0] - 14.0, HQ[1] + 9.0, 5.0, "c")
    sh.text("itself", q_self[0] + 2.0, q_self[1] - 3.6, 2.0, "l")
    sh.text("K", HK[0] + 22.0, HK[1] + 22.0, 5.0, "c")
    p = kpos[tr]
    sh.text("transformer", p[0] + 1.2, p[1] - 3.8, 2.0, "l")
    sh.text("V", HV[0] + 19.0, HV[1] + 17.0, 5.0, "c")
    sh.text("Z = AV", HZ[0], HZ[1] - RZ - 9.0, 4.2, "c")

    # key, flush left on Q's axis
    kx, ky, lead = HQ[0], 33.0, 4.2
    for row, s in enumerate((
        "one turn = one ochre line = 5 %",
        "ring = the norm of a row",
        "left to right = the sentence",
    )):
        sh.text(s, kx, ky - row * lead, 1.9, "l", track=1.35)

    sent = "The pen plotter drew a black hole while the transformer watched itself think."
    spans = sh.text(sent, DW / 2.0, 7.0, 2.6, "c")
    for word, pen in ((" transformer", BLUE), (" itself", RED)):
        s0 = sent.index(word) + 1
        s1 = s0 + len(word) - 2
        xa, xb = spans[s0][0], spans[s1][1]
        sh.line(pen, [(xa, 5.2), (xb, 5.2)], knock=False)

    for x, y in ((3.0, 3.0), (DW - 3.0, 3.0), (3.0, DH - 3.0), (DW - 3.0, DH - 3.0)):
        sh.line(BLACK, [(x - 3.0, y), (x + 3.0, y)], knock=False)
        sh.line(BLACK, [(x, y - 3.0), (x, y + 3.0)], knock=False)

    return sh.emit(bounds, colors)


if __name__ == "__main__":
    D = compute()
    a = D["a"]
    print("layer", D["layer"], "head", D["head"], "| max |A_numpy - A_torch| =", D["check_err"])
    print("|AV - z| =", D["z_err"], "| epicycle chain closes on z to", D["chain_close"])
    for j in np.argsort(-a):
        print("  %-13r A=%.4f turns=%.2f lines=%d |q|=%.2f |k|=%.2f |v|=%.2f arm=%.3f" % (
            D["toks"][j], a[j], 20 * a[j], int(math.floor(20 * a[j] + 0.5)),
            D["q_norm"][j], D["k_norm"][j], D["v_norm"][j], D["arms_full"][j]))
