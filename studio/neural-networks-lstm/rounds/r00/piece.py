"""LSTM — MEMORY IN TIME, the twisted helix.  FROZEN ORIGINAL (r00) — do not edit.

This is the ``bauhaus_memory`` that drew
``gallery/neural-networks/lstm/candidates/pp_bauhaus_memory_LSTM_v3_seed1.png``,
PROMOTED by Juan on 2026-09-20 ("this is the one").  It lived in
``promptplot/generative/bauhaus.py`` for ~15 minutes on 2026-09-13 (an uncommitted
edit on top of commit 2597b31) and was overwritten by the figure-8 rewrite that
landed in 58bdb22.  Restored verbatim from the session transcript; see NOTES.md.

The geometry below is byte-for-byte the original body.  Only three things were
added around it, none of which change a coordinate when rendered the original way:

* the function is renamed ``bauhaus_memory_helix`` (studio contract);
* ``_stroke_text`` / ``type_block`` and the glyphs they use are VENDORED as they
  were at 2597b31 — the package's ``_stroke_text`` has since changed (case-aware
  glyph lookup, missing-glyph warnings, ``proportional=``), so the frozen type
  must not depend on it;
* ``margin_mm``: the original was composed on the A4 drawable area at a 15 mm
  margin (bounds 15,15,195,282).  ``scripts/render_candidate.py`` builds paper
  with the default 10 mm margin, so by default the piece recovers the sheet
  from the (symmetric) bounds it is given and re-insets it at 15 mm.  Pass
  ``margin_mm=None`` to draw into the bounds exactly as given.

Pens (palette ``dodgerblue,crimson,black``): index 1 = crimson accent (UPDATE
spiral + its leader, two spine dots, MEMORY ring), index 2 = black (all else).
Index 0 is unused.  ``rng`` is unused — the plate is fully deterministic.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence

from promptplot.generative.engine.kit import _pen, _spaced, circle, fill_disc
from promptplot.generative.generators import _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = tuple

PINK, BLACK = 1, 2  # kit palette slots as at 2597b31 (PINK slot renders crimson)
ORIGINAL_MARGIN_MM = 15.0

# --------------------------------------------------------------------------- #
# VENDORED from promptplot/generative/generators.py @ 2597b31 — the glyphs this
# plate uses, and the stroke-text routine exactly as it was (unconditional
# .upper(), fixed 5.6-unit advance, silent on missing glyphs).
# --------------------------------------------------------------------------- #
_GLYPHS = {
    " ": [],
    "A": [[(0, 0), (2, 6), (4, 0)], [(1, 2.4), (3, 2.4)]],
    "C": [[(4, 1), (3, 0), (1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5)]],
    "D": [[(0, 0), (0, 6), (2, 6), (4, 4), (4, 2), (2, 0), (0, 0)]],
    "E": [[(4, 0), (0, 0), (0, 6), (4, 6)], [(0, 3), (3, 3)]],
    "F": [[(0, 0), (0, 6), (4, 6)], [(0, 3), (3, 3)]],
    "G": [[(4, 5), (3, 6), (1, 6), (0, 5), (0, 1), (1, 0), (3, 0), (4, 1), (4, 3), (2, 3)]],
    "I": [[(2, 0), (2, 6)], [(1, 0), (3, 0)], [(1, 6), (3, 6)]],
    "L": [[(0, 6), (0, 0), (4, 0)]],
    "M": [[(0, 0), (0, 6), (2, 3), (4, 6), (4, 0)]],
    "N": [[(0, 0), (0, 6), (4, 0), (4, 6)]],
    "O": [[(1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5), (4, 1), (3, 0), (1, 0)]],
    "P": [[(0, 0), (0, 6), (3, 6), (4, 5), (4, 3.6), (3, 3), (0, 3)]],
    "R": [[(0, 0), (0, 6), (3, 6), (4, 5), (4, 3.6), (3, 3), (0, 3)], [(2, 3), (4, 0)]],
    "S": [[(4, 5), (3, 6), (1, 6), (0, 5), (0, 4), (4, 2), (4, 1), (3, 0), (1, 0), (0, 1)]],
    "T": [[(2, 0), (2, 6)], [(0, 6), (4, 6)]],
    "U": [[(0, 6), (0, 1), (1, 0), (3, 0), (4, 1), (4, 6)]],
    "V": [[(0, 6), (2, 0), (4, 6)]],
    "X": [[(0, 0), (4, 6)], [(0, 6), (4, 0)]],
    "Y": [[(0, 6), (2, 3), (4, 6)], [(2, 3), (2, 0)]],
}


def _stroke_text(text, x, y, height, color=None, f=2400):
    """Pen-drawn single-stroke text; (x, y) = left baseline. Returns commands."""
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


# VENDORED from promptplot/generative/bauhaus.py @ 2597b31 (unchanged source today,
# but it must call the vendored _stroke_text above, not the package's).
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


def _original_frame(bounds: Bounds, margin_mm: Optional[float]) -> Bounds:
    """Re-inset symmetric drawable bounds at the original margin (see module doc)."""
    if margin_mm is None:
        return bounds
    x0, y0, x1, y1 = bounds
    sheet_w, sheet_h = x0 + x1, y0 + y1  # symmetric margins: x1 = W - m, x0 = m
    return (margin_mm, margin_mm, sheet_w - margin_mm, sheet_h - margin_mm)


def bauhaus_memory_helix(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    strands: int = 3,
    bundle: int = 6,
    turns: float = 3.4,
    steps: int = 460,
    feed: int = 2200,
    margin_mm: Optional[float] = ORIGINAL_MARGIN_MM,
) -> List[GCodeCommand]:
    """MEMORY IN TIME — an LSTM as TEMPORAL FLOW: braided strands of state wind up
    an INPUT→OUTPUT axis, pinching to a thread at the carried MEMORY waist and
    opening at the gates. Spiral VORTICES sit at the FORGET, UPDATE (red) and
    CELL-STATE gates — information swirling in and out. Fine-line, black + red.
    Bespoke braid + vortex geometry (not the shared kit)."""
    # ---- original body from here down (only the frame line is added) ----
    x0, y0, x1, y1 = _original_frame(bounds, margin_mm)
    W, H = x1 - x0, y1 - y0
    accent, black = _pen(PINK, colors), _pen(BLACK, colors)  # PINK slot rendered crimson
    out: List[GCodeCommand] = []

    cx = x0 + 0.46 * W
    ybot, ytop = y0 + 0.13 * H, y0 + 0.86 * H
    span = ytop - ybot
    Abase = 0.085 * W

    def Y(ny):
        return ybot + ny * span

    def amp_of(ny):
        # pinch to a thread at the MEMORY waist (ny=0.5), open toward the ends
        return Abase * (0.35 + 0.65 * abs(math.cos(math.pi * ny)))

    # braided strands winding up the axis (black), each a fine ribbon bundle
    for s in range(strands):
        ph0 = 2 * math.pi * s / strands
        for bnd in range(bundle):
            da = (bnd - (bundle - 1) / 2) * 0.8
            pts = []
            for k in range(steps + 1):
                ny = k / steps
                a = amp_of(ny) + da
                x = cx + a * math.cos(2 * math.pi * turns * ny + ph0)
                pts.append((x, Y(ny)))
            out += _poly(pts, color=black, f=feed)

    # gate spiral vortices — information swirling at each gate
    def spiral(cxp, cyp, rmax, tn, pen, cw):
        pts = []
        n = int(tn * 90)
        for k in range(n + 1):
            th = 2 * math.pi * tn * k / n
            r = rmax * k / n
            pts.append((cxp + cw * r * math.cos(th), cyp + r * math.sin(th)))
        return _poly(pts, color=pen, f=feed)

    fx, fy = cx - 0.18 * W, Y(0.32)
    ux, uy = cx + 0.18 * W, Y(0.66)
    vx, vy = cx + 0.15 * W, Y(0.16)
    out += spiral(fx, fy, 0.10 * W, 3.6, black, 1)  # FORGET vortex
    out += spiral(ux, uy, 0.085 * W, 3.3, accent, -1)  # UPDATE vortex (red)
    out += spiral(vx, vy, 0.072 * W, 3.0, black, -1)  # CELL STATE vortex
    # light connectors peeling the braid into the gate vortices
    out += _poly([(cx - amp_of(0.32), fy), (fx + 0.10 * W, fy)], color=black, f=feed)
    out += _poly([(cx + amp_of(0.66), uy), (ux - 0.085 * W, uy)], color=accent, f=feed)

    # gate axis (dash-dot) INPUT (bottom) → OUTPUT (top)
    yv, dash = ybot - 8, 0
    while yv < ytop + 8:
        if dash % 2 == 0:
            out += _poly([(cx, yv), (cx, min(ytop + 8, yv + 4.0))], color=black, f=feed)
        yv += 6.0
        dash += 1
    out += _poly([(cx - 1.6, ytop + 5), (cx, ytop + 9), (cx + 1.6, ytop + 5)], color=black, f=feed)

    # nodes on the axis + labels
    out += fill_disc(cx, ytop, 1.7, spacing=0.5, pen=black, f=feed)
    out += fill_disc(cx, ybot, 1.7, spacing=0.5, pen=black, f=feed)
    out += fill_disc(cx, Y(0.32), 1.6, spacing=0.5, pen=accent, f=feed)
    out += fill_disc(cx, Y(0.66), 1.6, spacing=0.5, pen=accent, f=feed)
    out += circle(cx, Y(0.5), 2.0, pen=accent, f=feed)  # MEMORY — hollow carried state
    out += _stroke_text(_spaced("OUTPUT"), cx + 6, ytop - 1.2, 2.2, color=black, f=feed)
    out += _stroke_text(_spaced("INPUT"), cx + 6, ybot - 1.2, 2.2, color=black, f=feed)
    out += _stroke_text(_spaced("MEMORY"), cx + 6, Y(0.5) - 1.2, 2.2, color=black, f=feed)
    out += _stroke_text(_spaced("FORGET GATE"), fx - 0.11 * W, fy - 0.10 * H, 2.0, color=black, f=feed)
    out += _stroke_text(_spaced("UPDATE GATE"), ux - 0.02 * W, uy + 0.09 * H, 2.0, color=black, f=feed)
    out += _stroke_text(_spaced("CELL STATE"), vx - 0.01 * W, vy - 0.10 * H, 2.0, color=black, f=feed)
    out += _stroke_text(_spaced("VORTEX"), vx - 0.01 * W, vy - 0.10 * H - 5, 2.0, color=black, f=feed)

    # title + caption
    xT = x0 + 0.03 * W
    out += type_block(["LSTM"], xT, y1 - 6.0, height=4.2, pen=black, underline=False, f=feed)
    out += _stroke_text(_spaced("MEMORY IN TIME"), xT, y1 - 16.0, 2.4, color=black, f=feed)
    out += _stroke_text(_spaced("PERSISTING INFORMATION"), xT, y0 + 18.0, 2.0, color=black, f=feed)

    # bottom mini-diagram: twisted flow → spiral → twisted flow
    my = y0 + 12.0
    for c, kind in enumerate(("braid", "spiral", "braid")):
        mcx = x0 + 0.50 * W + c * 26
        if kind == "braid":
            for s in range(2):
                pts = [
                    (mcx + 5 * math.cos(2 * math.pi * 1.5 * u / 20 + s * math.pi), my - 6 + 12 * u / 20)
                    for u in range(21)
                ]
                out += _poly(pts, color=black, f=feed)
        else:
            out += spiral(mcx, my, 5.0, 2.4, black, 1)
        if c < 2:
            out += _poly([(mcx + 7, my), (mcx + 17, my)], color=black, f=feed)
            out += _poly([(mcx + 15, my + 1.1), (mcx + 17, my), (mcx + 15, my - 1.1)], color=black, f=feed)
    return out
