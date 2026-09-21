"""Side-by-side: the SAME forms drawn machine-clean (left) and as gestures (right).

Not an image filter — this is the procedural side. Any polyline in, human strokes out.
"""
from __future__ import annotations

import math
from typing import List, Tuple

from promptplot.models import GCodeCommand

Pt = Tuple[float, float]


def _poly(pts, pen=0, f=1800):
    out = [GCodeCommand(command="G0", x=round(pts[0][0], 3), y=round(pts[0][1], 3)),
           GCodeCommand(command="M3", s=1000, color=pen)]
    for x, y in pts[1:]:
        out.append(GCodeCommand(command="G1", x=round(x, 3), y=round(y, 3), f=f, color=pen))
    out.append(GCodeCommand(command="M5"))
    return out


def _resample(pts: List[Pt], step: float) -> List[Pt]:
    out, acc = [pts[0]], 0.0
    for a, b in zip(pts, pts[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        if d < 1e-9:
            continue
        while acc + d >= step:
            t = (step - acc) / d
            a = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            out.append(a)
            d = math.hypot(b[0] - a[0], b[1] - a[1])
            acc = 0.0
        acc += d
    out.append(pts[-1])
    return out


def _normals(pts: List[Pt]) -> List[Pt]:
    n = []
    for i in range(len(pts)):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        n.append((-dy / L, dx / L))
    return n


def _extend(pts: List[Pt], mm: float) -> List[Pt]:
    """Overshoot: run the stroke past the form at both ends."""
    if len(pts) < 2 or mm <= 0:
        return pts
    def ext(p, q, d):
        dx, dy = p[0] - q[0], p[1] - q[1]
        L = math.hypot(dx, dy) or 1.0
        return (p[0] + dx / L * d, p[1] + dy / L * d)
    return [ext(pts[0], pts[1], mm)] + pts + [ext(pts[-1], pts[-2], mm)]


def gesture(pts: List[Pt], rng, *, overshoot=(2.0, 7.0), searching=(1, 3),
            wobble=0.9, break_up=True, step=1.2) -> List[List[Pt]]:
    """One polyline in -> a handful of human strokes out.

    The stroke's LENGTH comes from the form: a long arc yields a long sweep, a
    short detail yields a short mark. Nothing here has a fixed mark size, which
    is the whole difference from a halftone screen.
    """
    pts = _resample(pts, step)
    if len(pts) < 3:
        return [pts]
    nrm = _normals(pts)
    L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))

    # a long form gets found more times than a short one
    k = rng.randint(*searching) if L > 25 else 1
    strokes = []
    for s in range(k):
        # each searching pass covers a different span of the form; long forms
        # may be laid down as 2 overlapping strokes, short ones never are.
        if break_up and L > 90 and rng.random() < 0.55:
            spans = [(0.0, rng.uniform(0.55, 0.72)), (rng.uniform(0.3, 0.46), 1.0)]
        else:
            spans = [(0.0 if s == 0 else rng.uniform(0.0, 0.12),
                      1.0 if s == 0 else rng.uniform(0.88, 1.0))]
        off = 0.0 if s == 0 else rng.uniform(-1.4, 1.4)
        ph, amp = rng.uniform(0, 6.28), wobble * (0.5 + rng.random())
        for (u0, u1) in spans:
            i0, i1 = int(u0 * (len(pts) - 1)), int(u1 * (len(pts) - 1))
            if i1 - i0 < 3:
                continue
            seg = []
            for i in range(i0, i1 + 1):
                t = (i - i0) / max(1, i1 - i0)
                # taper the searching offset so strokes converge on the true form
                w = off * math.sin(math.pi * t) + amp * math.sin(ph + 5.0 * t) * 0.35
                seg.append((pts[i][0] + nrm[i][0] * w, pts[i][1] + nrm[i][1] * w))
            strokes.append(_extend(seg, rng.uniform(*overshoot)))
    return strokes


def _forms(cx: float, cy: float, sc: float) -> List[List[Pt]]:
    """An abstract figure: a few big sweeps plus small details, so the stroke
    lengths SHOULD come out over an order of magnitude."""
    F = []
    # three long nested sweeps (the "back")
    for j, (r, a0, a1) in enumerate([(52, 2.6, 5.5), (44, 2.8, 5.3), (34, 3.0, 5.1)]):
        F.append([(cx + r * sc * math.cos(a) * 1.15, cy + r * sc * math.sin(a) * 0.8)
                  for a in [a0 + (a1 - a0) * i / 90 for i in range(91)]])
    # one long diagonal (the "arm")
    F.append([(cx - 46 * sc + 96 * sc * t, cy - 18 * sc + 34 * sc * t * (1 - 0.5 * t))
              for t in [i / 60 for i in range(61)]])
    # a closed head-ish oval
    F.append([(cx + 20 * sc + 15 * sc * math.cos(a), cy + 30 * sc + 19 * sc * math.sin(a))
              for a in [6.283 * i / 70 for i in range(71)]])
    # four SHORT details (the "fingers") — these must stay short
    for i in range(4):
        x = cx - 8 * sc + i * 5.5 * sc
        F.append([(x, cy - 40 * sc), (x + 1.6 * sc, cy - 33 * sc), (x + 0.6 * sc, cy - 27 * sc)])
    return F


def gesture_demo(rng, bounds, colors: int = 3) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    out: List[GCodeCommand] = []
    sc = min(W / 260.0, H / 200.0)

    # LEFT — machine: each form as one clean polyline
    for f in _forms(x0 + W * 0.26, y0 + H * 0.54, sc):
        out += _poly(f, pen=0)

    # RIGHT — gesture: the same forms through the layer
    for f in _forms(x0 + W * 0.74, y0 + H * 0.54, sc):
        for s in gesture(f, rng):
            out += _poly(s, pen=0)

    return out
