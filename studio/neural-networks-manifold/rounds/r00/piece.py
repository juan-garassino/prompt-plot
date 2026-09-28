"""MLP — NONLINEAR TRANSFORMATION (the FOLD braid). FROZEN ORIGINAL · do not edit.

Restored verbatim from the interim ``bauhaus_manifold`` in
``promptplot/generative/bauhaus.py`` at commit 58bdb22 (2026-09-13 14:03), with the
one parameter the gallery render actually used: ``twist=2.0``. The render
(``gallery/neural-networks/manifold/candidates/pp_bauhaus_manifold_MLP_FOLD_v1_seed{3,8}.png``,
13:49) was drawn from the working tree a minute BEFORE the edit that set the
committed default to ``twist=1.6`` — so the commit alone does not reproduce it.

Original frame: A4 portrait, margin 15 mm -> bounds (15, 15, 195, 282), palette
dodgerblue,crimson,black (colors=3). The piece uses no randomness: every seed
gives the same sheet.

Vendored (their package versions have changed since 58bdb22, so they are frozen
here): ``_stroke_text`` (now case-sensitive with a missing-glyph warning, formerly
``text.upper()`` + silent drop), the ``_GLYPHS`` subset this sheet uses (as of
58bdb22), and ``type_block`` (so it calls the vendored ``_stroke_text``).
Imported (still behave identically): ``_poly``, ``_dot`` from generators;
``_pen``, ``_spaced``, ``PINK``, ``BLACK`` from engine.kit.

Known flaws are kept on purpose (see NOTES.md). New versions go in r01+.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.engine.kit import BLACK, PINK, _pen, _spaced
from promptplot.generative.generators import _dot, _poly
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]

# ---------------------------------------------------------------------------
# vendored from 58bdb22 — do not replace with package imports
# ---------------------------------------------------------------------------

# Single-stroke glyphs (6-unit cap height), exactly as in generators._GLYPHS at
# 58bdb22, limited to the characters this sheet draws.
_GLYPHS = {
    ' ': [],
    'A': [[(0, 0), (2, 6), (4, 0)], [(1, 2.4), (3, 2.4)]],
    'C': [[(4, 1), (3, 0), (1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5)]],
    'D': [[(0, 0), (0, 6), (2, 6), (4, 4), (4, 2), (2, 0), (0, 0)]],
    'E': [[(4, 0), (0, 0), (0, 6), (4, 6)], [(0, 3), (3, 3)]],
    'F': [[(0, 0), (0, 6), (4, 6)], [(0, 3), (3, 3)]],
    'G': [[(4, 5), (3, 6), (1, 6), (0, 5), (0, 1), (1, 0), (3, 0), (4, 1), (4, 3), (2, 3)]],
    'H': [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3), (4, 3)]],
    'I': [[(2, 0), (2, 6)], [(1, 0), (3, 0)], [(1, 6), (3, 6)]],
    'K': [[(0, 0), (0, 6)], [(4, 6), (0, 2.5)], [(1.4, 3.4), (4, 0)]],
    'L': [[(0, 6), (0, 0), (4, 0)]],
    'M': [[(0, 0), (0, 6), (2, 3), (4, 6), (4, 0)]],
    'N': [[(0, 0), (0, 6), (4, 0), (4, 6)]],
    'O': [[(1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5), (4, 1), (3, 0), (1, 0)]],
    'P': [[(0, 0), (0, 6), (3, 6), (4, 5), (4, 3.6), (3, 3), (0, 3)]],
    'R': [[(0, 0), (0, 6), (3, 6), (4, 5), (4, 3.6), (3, 3), (0, 3)], [(2, 3), (4, 0)]],
    'S': [[(4, 5), (3, 6), (1, 6), (0, 5), (0, 4), (4, 2), (4, 1), (3, 0), (1, 0), (0, 1)]],
    'T': [[(2, 0), (2, 6)], [(0, 6), (4, 6)]],
    'U': [[(0, 6), (0, 1), (1, 0), (3, 0), (4, 1), (4, 6)]],
    'V': [[(0, 6), (2, 0), (4, 6)]],
    'Y': [[(0, 6), (2, 3), (4, 6)], [(2, 3), (2, 0)]],
}


def _stroke_text(text, x, y, height, color=None, f=2400):
    """Pen-drawn single-stroke text; (x, y) = left baseline (58bdb22 version)."""
    sc = height / 6.0
    adv = 5.6 * sc
    out = []
    cx = x
    for ch in text.upper():
        for stroke in _GLYPHS.get(ch, []):
            pts = [(cx + gx * sc, y + gy * sc) for gx, gy in stroke]
            out += _poly(pts, color=color, f=f)
        cx += adv
    return out


def type_block(
    lines: Sequence[str],
    x: float,
    y_top: float,
    height: float = 2.6,
    pen: Optional[int] = None,
    underline: bool = True,
    f: int = 2200,
) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    y = y_top
    for ln in lines:
        out += _stroke_text(_spaced(ln), x, y, height, color=pen, f=f)
        y -= height * 2.0
    if underline:
        out += _poly(
            [(x, y + height * 2.0 - 2.0), (x + 6.0, y + height * 2.0 - 2.0)], color=pen, f=f
        )
    return out


# ---------------------------------------------------------------------------
# the piece — body verbatim from 58bdb22 bauhaus_manifold (twist default 2.0)
# ---------------------------------------------------------------------------


def bauhaus_manifold_fold(
    rng,
    bounds: Bounds,
    colors: int = 3,
    nstream: int = 168,
    steps: int = 66,
    petals: int = 5,
    twist: float = 2.0,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """NONLINEAR TRANSFORMATION — an MLP as the FOLD of space. Streamlines fall
    from the INPUT plane (top), twist through a central petal-FOLD where the
    nonlinear activation introduces curvature — bending the sheet so different
    input points are matched to the SAME location (negative radius crosses the
    fold) — then open onto the OUTPUT plane (bottom). Same tokens, richer
    geometry. Bespoke fold geometry, black + red."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    accent, black = _pen(PINK, colors), _pen(BLACK, colors)  # PINK slot rendered crimson
    out: List[GCodeCommand] = []

    cx = x0 + 0.50 * W
    ylo, yhi = y0 + 0.13 * H, y0 + 0.86 * H  # OUTPUT (bottom), INPUT (top)
    span = yhi - ylo
    Rin, Rwaist, Rpetal, ell = 0.30 * W, 0.03 * W, 0.17 * W, 0.32

    def P(s, theta, r):
        return (cx + r * math.cos(theta), (yhi - s * span) + r * math.sin(theta) * ell)

    # the fold: input → activation petal-fold → output
    for i in range(nstream):
        th0 = 2 * math.pi * i / nstream
        pts = []
        for kk in range(steps + 1):
            s = kk / steps
            r_hour = Rwaist + (Rin - Rwaist) * abs(2 * s - 1)
            fold = Rpetal * (math.sin(math.pi * s) ** 1.4) * math.cos(petals * th0)
            r = r_hour + fold  # r<0 crosses the fold → different inputs, same cardinal
            pts.append(P(s, th0 + twist * s, r))
        out += _poly(pts, color=(accent if i % 3 == 0 else black), f=feed)

    # INPUT / OUTPUT planes: dot clouds + frame parallelogram
    def plane(y_at, label, above):
        g = 9
        for a in range(g):
            for b in range(g):
                gu, gv = -1 + 2 * a / (g - 1), -1 + 2 * b / (g - 1)
                out.extend(_dot(cx + gu * Rin, y_at + gv * Rin * ell, 0.45, color=black, f=feed))
        corners = [(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]
        out.extend(_poly([(cx + gu * Rin, y_at + gv * Rin * ell) for gu, gv in corners], color=black, f=feed))
        ly = y_at + (Rin * ell + 7 if above else -Rin * ell - 4)
        out.extend(_stroke_text(_spaced(label), cx - 0.10 * W, ly, 2.2, color=black, f=feed))

    plane(yhi, "INPUT SPACE", True)
    plane(ylo, "OUTPUT SPACE", False)

    # right-side stage labels
    rx = cx + 0.34 * W
    out += _stroke_text(_spaced("LINEAR TRANSFORM"), rx, yhi - 0.10 * H, 1.8, color=black, f=feed)
    out += _stroke_text(_spaced("NONLINEAR ACTIVATION"), rx, ylo + 0.50 * span, 1.8, color=accent, f=feed)
    out += _stroke_text(_spaced("LINEAR TRANSFORM"), rx, ylo + 0.10 * H, 1.8, color=black, f=feed)

    # title + caption
    xT = x0 + 0.03 * W
    out += type_block(["MLP"], xT, y1 - 6.0, height=4.2, pen=black, underline=False, f=feed)
    out += _stroke_text(_spaced("NONLINEAR TRANSFORMATION"), xT, y1 - 16.0, 2.2, color=black, f=feed)
    out += _stroke_text(_spaced("SAME TOKENS"), xT, y0 + 26.0, 2.0, color=black, f=feed)
    out += _stroke_text(_spaced("DIFFERENT GEOMETRY"), xT, y0 + 21.0, 2.0, color=black, f=feed)
    out += _stroke_text(_spaced("A RICHER SPACE"), xT, y0 + 16.0, 2.0, color=black, f=feed)

    # bottom mini-diagram: grid → S → S → fold (each layer bends the space more)
    my, gx, sq = y0 + 11.0, x0 + 0.52 * W, 11.0
    for c in range(4):
        bx = gx + c * (sq + 8)
        out += _poly([(bx, my - sq / 2), (bx + sq, my - sq / 2), (bx + sq, my + sq / 2), (bx, my + sq / 2), (bx, my - sq / 2)], color=black, f=feed)
        bend = c / 3.0
        curve = [
            (bx + sq * u / 20, my - sq / 2 + sq * (0.5 + 0.42 * math.sin(2 * math.pi * bend * u / 20 * 1.5)))
            for u in range(21)
        ]
        out += _poly(curve, color=accent, f=feed)
        if c < 3:
            out += _poly([(bx + sq + 1, my), (bx + sq + 7, my)], color=black, f=feed)
            out += _poly([(bx + sq + 5, my + 1.1), (bx + sq + 7, my), (bx + sq + 5, my - 1.1)], color=black, f=feed)
    return out
