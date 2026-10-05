"""GAN — NO FIXED POINT, round 02: THE ESCAPE SPIRAL.  parent: r01 (minimax_duel).

Contract (promptplot/studio/loop.py:_render_code_payload):

    escape_spiral(rng: SeededRNG, bounds, colors: int = 3) -> list[GCodeCommand]

WHAT IS COMPUTED (all exact, scalar, no fitting)
------------------------------------------------
The Dirac-GAN (Mescheder, Geiger, Nowozin 2018): real data delta_0, generator
delta_theta, discriminator D_psi(x) = psi*x, objective
V(theta, psi) = f(psi*theta) + f(0) with f(t) = -log(1 + e^-t).  Simultaneous
gradient descent-ascent with learning rate h:

    g      = f'(psi*theta) = sigmoid(-psi*theta)       (the force both feel)
    theta <- theta - h * psi * g                        (generator descends)
    psi   <- psi   + h * theta * g                      (discriminator ascends)

Continuous time conserves theta^2 + psi^2 (a closed orbit, the dotted circle).
Each discrete step multiplies r^2 by exactly (1 + h^2 g^2), so the run provably
spirals OUT of the equilibrium (0, 0), which is never reached.

THE ORDER: ORBITAL — Kandinsky, *Point and Line to Plane* (1926)
----------------------------------------------------------------
Kandinsky's line is the trace of a point driven by forces: two forces acting
TOGETHER bend it into a curve; two forces acting in ALTERNATION break it into
an angular line.  The Dirac-GAN is exactly that pair.  In continuous time the
two players act together and the point circles forever (the curve, drawn
dotted); a training step is the generator's push (a horizontal leg, crimson,
theta only) and then the discriminator's answer (a vertical leg, black, psi
only) — their sum is exactly the simultaneous update — and the alternation
breaks the circle into a widening zig-zag that never closes.  Line WEIGHT is
the force g (1-3 passes).  Where psi*theta > 0 the force vanishes
(f' -> 0, Goodfellow's saturating loss): the legs fall under the pen's
resolution, the staircase becomes a hairline crawl, and hundreds of steps pass
on a short arc.  The point Kandinsky starts from — the equilibrium — is the
only thing on the sheet made of bare paper.

The plane is drawn in plan: theta right, psi up, flat by declaration (the
Bauhaus canon is flat; the depth here is line weight falling from the heavy
outer flights to the hairline crawls).
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.engine import Scene3D
from promptplot.generative.engine.kit import (
    _dot,
    _pen,
    _poly,
    _spaced,
    _stroke_text,
    _text_width,
    giant_type,
    giant_type_width,
    plus_mark,
)

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]


# ---------------------------------------------------------------------------
# the mathematics
# ---------------------------------------------------------------------------


def _sigmoid(t: float) -> float:
    if t >= 0.0:
        return 1.0 / (1.0 + math.exp(-t))
    e = math.exp(t)
    return e / (1.0 + e)


def _force(th: float, ps: float) -> float:
    """g = f'(psi*theta) = sigmoid(-psi*theta)."""
    return _sigmoid(-th * ps)


def simulate(r_start: float, a0: float, h: float, stop, max_iters: int):
    """Simultaneous GDA on the Dirac-GAN.  Returns [(th, ps, dth, dps, g)].

    ``stop(th, ps) -> bool`` ends the run after the step that lands there."""
    th, ps = r_start * math.cos(a0), r_start * math.sin(a0)
    steps = []
    for _ in range(max_iters):
        g = _force(th, ps)
        dth = -h * ps * g
        dps = h * th * g
        steps.append((th, ps, dth, dps, g))
        th, ps = th + dth, ps + dps
        if stop(th, ps):
            break
    return steps


# ---------------------------------------------------------------------------
# drawing helpers
# ---------------------------------------------------------------------------


def _clip_seg_runs(pts: Sequence[Pt], box: Bounds) -> List[List[Pt]]:
    """Split a polyline into runs inside ``box`` (exact edge intersection)."""
    bx0, by0, bx1, by1 = box

    def ins(p):
        return bx0 <= p[0] <= bx1 and by0 <= p[1] <= by1

    def cut(a, b):
        # parametric clip of segment a->b against the box (Liang-Barsky)
        t0, t1 = 0.0, 1.0
        dx, dy = b[0] - a[0], b[1] - a[1]
        for p, q in ((-dx, a[0] - bx0), (dx, bx1 - a[0]), (-dy, a[1] - by0), (dy, by1 - a[1])):
            if abs(p) < 1e-12:
                if q < 0:
                    return None
                continue
            r = q / p
            if p < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
        if t0 > t1:
            return None
        return (a[0] + dx * t0, a[1] + dy * t0), (a[0] + dx * t1, a[1] + dy * t1)

    runs: List[List[Pt]] = []
    cur: List[Pt] = []
    for a, b in zip(pts[:-1], pts[1:]):
        c = cut(a, b)
        if c is None:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
            continue
        pa, pb = c
        if not cur:
            cur = [pa]
        elif (cur[-1][0] - pa[0]) ** 2 + (cur[-1][1] - pa[1]) ** 2 > 1e-10:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [pa]
        cur.append(pb)
        if not ins(b):
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    return runs


def _offset(pts: Sequence[Pt], d: float) -> List[Pt]:
    """Offset an open polyline by d (mitred at the joins)."""
    if abs(d) < 1e-9 or len(pts) < 2:
        return list(pts)
    out = []
    n = len(pts)
    for i in range(n):
        if i == 0:
            ax, ay = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
            bx, by = ax, ay
        elif i == n - 1:
            ax, ay = pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]
            bx, by = ax, ay
        else:
            ax, ay = pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]
            bx, by = pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]
        la = math.hypot(ax, ay) or 1.0
        lb = math.hypot(bx, by) or 1.0
        nx = -(ay / la + by / lb)
        ny = ax / la + bx / lb
        ln = math.hypot(nx, ny) or 1.0
        nx, ny = nx / ln, ny / ln
        # mitre length
        cos_half = max(0.35, (nx * (-ay / la) + ny * (ax / la)))
        out.append((pts[i][0] + nx * d / cos_half, pts[i][1] + ny * d / cos_half))
    return out


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------


def _runs(steps, k_mm: float, min_stroke: float):
    """Split the run into alternating FLIGHT / CRAWL stretches.

    A step is a flight when both of its legs are at least ``min_stroke`` mm on
    paper — the pen can draw them as two distinct moves.  Below that the
    staircase is finer than the pen, and the exact polyline through the
    iterates IS the staircase at plotting resolution (corner deviation
    < min_stroke / sqrt 2)."""
    out = []
    for i, (t0, p0, dth, dps, g) in enumerate(steps):
        fl = abs(dth) * k_mm >= min_stroke and abs(dps) * k_mm >= min_stroke
        kind = "flight" if fl else "crawl"
        if not out or out[-1][0] != kind:
            out.append([kind, []])
        out[-1][1].append(i)
    return out


def escape_spiral(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    step: float = 0.26,           # h — shared learning rate
    r_start: float = 0.74,        # initial ||(theta, psi)||
    k_mm: float = 31.0,           # mm per unit of (theta, psi)
    centre: Tuple[float, float] = (0.56, 0.36),   # equilibrium, sheet (u, v from top)
    min_stroke: float = 1.2,      # legs shorter than this (mm) merge into the crawl
    pass_gap: float = 0.5,        # mm between the passes of a weighted leg
    max_iters: int = 400000,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """NO FIXED POINT — the Dirac-GAN's discrete training run, drawn whole,
    from the equilibrium it leaves to the sheet edge it crosses."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    black = _pen(0, colors)
    red = _pen(1, colors)
    blue = _pen(2, colors) if colors >= 3 else black

    def U(u: float) -> float:
        return x0 + u * W

    def V(v: float) -> float:            # v measured from the TOP of the sheet
        return y1 - v * H

    ex, ey = U(centre[0]), V(centre[1])

    def P(th: float, ps: float) -> Pt:
        return ex + k_mm * th, ey + k_mm * ps

    box = (x0 + 0.5, y0 + 0.5, x1 - 0.5, y1 - 0.5)

    def off_sheet(th, ps):
        X, Y = P(th, ps)
        return not (x0 < X < x1 and y0 < Y < y1)

    # ---- the run: every step until the iterate lands off the sheet -----------
    a0 = 0.62 + rng.uniform(-0.55, 0.55)
    steps = simulate(r_start, a0, step, off_sheet, max_iters)
    n_steps = len(steps)
    t_e, p_e = steps[-1][0] + steps[-1][2], steps[-1][1] + steps[-1][3]
    r_end = math.hypot(t_e, p_e)
    runs = _runs(steps, k_mm, min_stroke)

    scene = Scene3D(rng, bounds, feed=feed, fit="none", tip=0.5)
    rc = r_start * k_mm


    # ---- the angular line: flights as legs, crawls as the iterate path -------
    # Weight is the force: 1-3 passes.  Butt joints: every corner belongs to
    # the discriminator's (vertical) band, which runs through it by the half
    # width of the generator's band; the generator's band stops at its edge,
    # so the two pens never ink the same corner twice.
    occ = scene.occupancy(1.1)            # the orbit keeps clear of the run's ink

    def n_pass(g):
        return 1 + (g > 0.30) + (g > 0.72)

    def half(g):
        return 0.5 * (n_pass(g) - 1) * pass_gap

    def mark(pts):
        for (ax_, ay_), (bx_, by_) in zip(pts[:-1], pts[1:]):
            L = math.hypot(bx_ - ax_, by_ - ay_)
            n = max(1, int(L / 0.4))
            for i in range(n + 1):
                occ.add(ax_ + (bx_ - ax_) * i / n, ay_ + (by_ - ay_) * i / n)

    def band(p, q, g, pen, cut_p, cut_q):
        """Leg p->q as a band of passes; trim (cut>0) or extend (cut<0) each end."""
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        if L < 1e-9:
            return
        ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
        p2 = (p[0] + ux * cut_p, p[1] + uy * cut_p)
        q2 = (q[0] - ux * cut_q, q[1] - uy * cut_q)
        if (q2[0] - p2[0]) * ux + (q2[1] - p2[1]) * uy <= 0.05:
            return
        m = n_pass(g)
        for kx in range(m):
            d = (kx - (m - 1) / 2.0) * pass_gap
            pts = _offset([p2, q2], d)
            for run in _clip_seg_runs(pts, box):
                scene.poly(run, pen=pen)
                mark(run)

    flight_idx = set(i for kind, idx in runs if kind == "flight" for i in idx)

    def hw(i):
        return half(steps[i][4]) if i in flight_idx else 0.0

    run_marks = []   # (kind, n_steps, mid point, outward angle)
    for kind, idx in runs:
        if kind == "flight":
            for i in idx:
                t0, p0, dth, dps, g = steps[i]
                a, c, b = P(t0, p0), P(t0 + dth, p0), P(t0 + dth, p0 + dps)
                band(a, c, g, red, hw(i - 1) if i > 0 else 0.0, hw(i))   # G pushes theta
                band(c, b, g, black, -hw(i), -hw(i + 1))                  # D answers in psi
        else:
            pts = [P(steps[idx[0]][0], steps[idx[0]][1])]
            for i in idx:
                t0, p0, dth, dps, g = steps[i]
                q = P(t0 + dth, p0 + dps)
                if math.hypot(q[0] - pts[-1][0], q[1] - pts[-1][1]) >= 0.3:
                    pts.append(q)
            last = steps[idx[-1]]
            pts.append(P(last[0] + last[2], last[1] + last[3]))
            for run in _clip_seg_runs(pts, box):
                scene.poly(run, pen=black)
                mark(run)
        im = idx[len(idx) // 2]
        leg = max(abs(steps[im][2]), abs(steps[im][3])) * k_mm
        run_marks.append((kind, len(idx), steps[im][0], steps[im][1], leg))

    # ---- the curve: continuous time, both forces together, forever ----------
    # Drawn after the run and gated by its occupancy: where the discrete run
    # still lies on the orbit (its first steps) the orbit gives way, and it
    # reappears exactly where the run has pulled away from it.
    rc = r_start * k_mm
    for kk in range(0, 360, 4):
        seg = []
        for j in range(5):
            aa = math.radians(kk + 0.5 * j)
            q = (ex + rc * math.cos(aa), ey + rc * math.sin(aa))
            if occ.crowded(*q):
                break
            seg.append(q)
        if len(seg) >= 2:
            scene.poly(seg, pen=blue)

    # ---- the plane: the two knives where psi*theta = 0 (force exactly 1/2) ---
    # Dotted, and gated by the run's occupancy so they pass UNDER it.
    def dotted(a, b, on=0.6, per=2.4, pen=black):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = int(L / per)
        for i in range(n):
            t0, t1 = i * per / L, min(1.0, (i * per + on) / L)
            p = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
            q = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            if occ.crowded(*p) or occ.crowded(*q):
                continue
            scene.poly([p, q], pen=pen)

    r_hole = rc - 3.5
    dotted((ex + r_hole, ey), (x1 - 0.5, ey))
    dotted((ex - r_hole, ey), (x0 + 0.5, ey))
    dotted((ex, ey + r_hole), (ex, y1 - 0.5))
    dotted((ex, ey - r_hole), (ex, y0 + 0.5))

    # ---- step counts: one per quarter-turn where the force dies (psi*theta>0)
    # The run is cut at every knife crossing; the steps spent in each crawl
    # quarter are counted and set along the arc's diagonal, outside it.
    quarters = []                                  # [quadrant, [step idx]]
    for i, (t0, p0, dth, dps, g) in enumerate(steps):
        qd = (t0 >= 0, p0 >= 0)
        if not quarters or quarters[-1][0] != qd:
            quarters.append([qd, []])
        quarters[-1][1].append(i)
    crawl_counts = []
    for qd, idx in quarters:
        if qd[0] != qd[1]:                         # psi*theta < 0: a flight quarter
            continue
        n = len(idx)
        crawl_counts.append(n)
        im = max(idx, key=lambda i: steps[i][0] * steps[i][1])   # the diagonal
        th, ps = steps[im][0], steps[im][1]
        r = math.hypot(th, ps)
        if r * k_mm < rc + 4.0:
            continue
        ang = math.atan2(ps, th)
        txt = _spaced(f"{n}  STEPS")
        hgt = 1.8
        w = _text_width(txt, hgt)
        rr = r * k_mm + 3.0
        tdeg = math.degrees(ang) - 90.0            # tangent; keep it readable
        if math.cos(math.radians(tdeg)) < 0:
            tdeg += 180.0
            rr += hgt
        ta = math.radians(tdeg)
        cx, cy = ex + rr * math.cos(ang), ey + rr * math.sin(ang)
        sx, sy = cx - 0.5 * w * math.cos(ta), cy - 0.5 * w * math.sin(ta)
        ex2, ey2 = sx + w * math.cos(ta), sy + w * math.sin(ta)
        if not all(x0 + 2 < qx < x1 - 2 and y0 + 2 < qy < y1 - 2
                   for qx, qy in ((sx, sy), (ex2, ey2))):
            continue
        scene.emit(giant_type(txt, sx, sy, hgt, pen=black, angle=tdeg, f=feed))

    # ---- the equilibrium: a mark on bare paper ------------------------------
    scene.emit(plus_mark(ex, ey, s=1.8, pen=red, f=feed))

    out = scene.render()

    # ---- the quiet band: type as mass left of the psi knife, the key right ---
    xT = x0 + 2.0
    gut = 6.0                                  # the same gutter both sides of the knife
    base = y0 + 2.0                            # the one shared bottom baseline
    top = base + 30.0                          # baseline of the title's first line
    # the title fills its column exactly: left margin -> knife minus the gutter
    th_h = (ex - gut - xT) * 6.0 / (len("NO FIXED") * 5.6)
    tw = 1.3
    out += giant_type("NO FIXED", xT, top, th_h, pen=black, weight=tw, tip=0.45, f=feed)
    out += giant_type("POINT", xT, top - th_h * 1.45, th_h, pen=black, weight=tw, tip=0.45,
                      f=feed)
    out += _stroke_text(_spaced("NEITHER PLAYER EVER ARRIVES"), xT, base, 1.9,
                        color=black, f=feed)

    xk = ex + gut
    lh = 1.8
    pitch = 5.0
    rows = [
        ("G", "G PUSHES THETA", red),
        ("D", "D ANSWERS PSI", black),
        ("C", "f' NEAR 0  THE CRAWL", black),
        ("O", "THE ORBIT AT h = 0", blue),
    ]
    stats = [f"{n_steps} STEPS  h {step:.2f}", f"r {r_start:.2f} TO {r_end:.2f}"]
    yk = top + th_h - lh                       # key cap line = title cap line
    for kind, txt, pen in rows:
        yc = yk + 0.5 * lh
        if kind == "G":
            for kx in range(3):
                d = (kx - 1) * pass_gap
                out += _poly([(xk, yc + d), (xk + 6.0, yc + d)], color=pen, f=feed)
        elif kind == "D":
            for kx in range(3):
                d = (kx - 1) * pass_gap
                out += _poly([(xk + 3.0 + d, yc - 1.8), (xk + 3.0 + d, yc + 1.8)],
                             color=pen, f=feed)
        elif kind == "C":
            out += _poly([(xk, yc), (xk + 6.0, yc)], color=pen, f=feed)
        elif kind == "O":
            out += _poly([(xk, yc), (xk + 1.4, yc)], color=pen, f=feed)
            out += _poly([(xk + 2.8, yc), (xk + 4.2, yc)], color=pen, f=feed)
        out += _stroke_text(_spaced(txt), xk + 9.0, yk, lh, color=black, f=feed)
        yk -= pitch
    for i, txt in enumerate(stats):               # bottom row sits on the shared baseline
        out += _stroke_text(_spaced(txt), xk + 9.0, base + pitch * (len(stats) - 1 - i), lh,
                            color=black, f=feed)
    return out
