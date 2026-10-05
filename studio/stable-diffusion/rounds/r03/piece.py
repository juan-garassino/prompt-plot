"""TWICE HERE — latent diffusion as a subdivision nested inside itself.

ABSTRACT ORDER (one line): *an orthogonal subdivision of the sheet, redrawn at
one eighth inside one of its own blocks — AREA is dimensionality, a PEN PASS is
a visit, so the big field is drawn twice and the small one is worked over fifty
times, and the sheet's own ink budget is the FLOP budget.*

Nothing is depicted and nothing is wired.  No encoder horn, no bowtie, no
arrows: a De Stijl plane divided by rules, and the same division again, 1/8 the
size, inside it.  The mechanism supplies every number and the order supplies the
form:

    area            = dimension.  f = 8, so the room is the field at 1/8 and
                      1/64 of its area.  512x512x3 -> 64x64x4 is 48 : 1.
    pen passes      = visits.  pixel space is entered twice (down, back up);
                      latent space is entered fifty times.  Hence
                      ink(field) : ink(room) = 2*786432 : 50*16384 = 1.92 : 1
                      over 64x the area -> the room is 33x denser.  The
                      detail-tick count is SOLVED to hold that ratio; it is not
                      a look.
    black           = x, the subdivision as it went in.
    crimson         = x~, the same subdivision decoded back out -- every rule
                      displaced, because the latent can only place a cut on its
                      own 8-pixel grid and because the loop returned a
                      DIFFERENT sample.  The same displacement is a hair in the
                      room and a centimetre in the field: that is what lossy
                      means.
    gold fog        = q(z_t | z_0) for all fifty steps at once, the marginal.
                      A cosine schedule, so a hard core (structure barely moves)
                      with a thin uniform halo (it collapses late and fast).
                      The halo is flat across the whole room: N(0, I).
    gold ring       = the room's own boundary IS the loop.  It closes.  Fifty
                      inward ticks on it, spaced and sized by the step's noise
                      level -- that is t entering, and that is the schedule.
    blue            = c.  A comb of preferred coordinates that the returning
                      cuts land on exactly.  It touches the RING and stops.
                      The fog ignores it completely: the forward process is
                      unconditional, and that asymmetry is drawn, not stated.
    sub-cell marks  = everything below one latent cell (6.09 mm on this sheet)
                      comes back as nothing.  Those ticks have no red twin.

NO NETWORK IS DRAWN.  The network is the only reason the ring's output lands on
the blue comb at all.

THE TWIST: a Mondrian is the most deliberately composed image the viewer knows,
and it is also a genuinely low-dimensional one -- a handful of cut coordinates.
So the plate lets the machine compose it, and the composition never happens in
the big picture.  It happens fifty times over in a rectangle 1/64 its area, and
what comes back out does not line up.  The punchline is measured on the sheet:
running the same loop out in the field costs 25x the ink and turns a ten-minute
plot into a two-hour one.  The pen is the GPU.

Style canon: DE STIJL (STYLES.md Sec.7) -- only horizontal and vertical rules,
blocks of red / yellow / blue on cream, asymmetric division of a rectangle, no
curve and no diagonal anywhere on the plate.  Declared FLAT (rubric dim 7): the
canon is flat by nature and the argument is an argument about AREA, which a
projection would corrupt.  The canon's primaries are kept but re-assigned:
colour encodes WHICH SPACE a mark lives in, never decoration.

Contract: stable_diffusion(rng, bounds, colors=3) -> list[GCodeCommand]
"""

from __future__ import annotations

import logging
import math
from typing import Dict, List, Optional, Sequence, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.engine import kit
from promptplot.generative.engine.kit import _poly, _stroke_text

logger = logging.getLogger(__name__)

Pt = Tuple[float, float]

# --------------------------------------------------------------------------
# the model's real numbers
# --------------------------------------------------------------------------

PIX_HW, PIX_C = 512, 3
LAT_HW, LAT_C = 64, 4
F_DOWN = PIX_HW // LAT_HW                     # 8
D_PIX = PIX_HW * PIX_HW * PIX_C               # 786432
D_LAT = LAT_HW * LAT_HW * LAT_C               # 16384
DIM_RATIO = D_PIX / D_LAT                     # 48.0
AREA_RATIO = float(F_DOWN * F_DOWN)           # 64.0

VISITS_PIX = 2                                # encode + decode
VISITS_LAT = 50                               # DDIM steps
INK_RATIO = (D_PIX * VISITS_PIX) / (D_LAT * VISITS_LAT)   # 1.92

FEED_MM_MIN = 600.0                           # Leo's draw feed (see MEMORY)

# cosine schedule, Nichol & Dhariwal
_S = 0.008


def _abar(u: float) -> float:
    u = 0.0 if u < 0.0 else (1.0 if u > 1.0 else u)
    return math.cos(0.5 * math.pi * (u + _S) / (1.0 + _S)) ** 2


STEPS = [(_i + 0.5) / VISITS_LAT for _i in range(VISITS_LAT)]

# --------------------------------------------------------------------------
# pens
# --------------------------------------------------------------------------

BLACK, RED, GOLD, BLUE = 0, 1, 2, 3

# --------------------------------------------------------------------------
# the subdivision, in unit coordinates of the field.  (orient, coord, a, b)
# orient 'V': a vertical rule at x=coord spanning y in [a, b].
# Guillotine, asymmetric, late-Mondrian sparse: nine rules is all the ink
# budget allows and all a Mondrian ever needed.
# --------------------------------------------------------------------------

CUTS: List[Tuple[str, float, float, float]] = [
    ("H", 0.860, 0.000, 1.000),   # title strip
    ("V", 0.545, 0.000, 0.860),   # the main division
    ("H", 0.460, 0.000, 0.545),   # left: display block over the rest
    ("V", 0.230, 0.000, 0.460),   # the data column
    ("H", 0.300, 0.545, 1.000),   # right: the room's shelf
    ("V", 0.800, 0.300, 0.860),   # right upper split
    ("H", 0.200, 0.230, 0.545),   # lower-left split
    ("V", 0.700, 0.000, 0.300),   # lower-right split
    ("H", 0.620, 0.800, 1.000),   # far-right split
]

# sub-cell rules: real cuts, too short to survive the latent grid.
MICRO: List[Tuple[str, float, float, float]] = [
    ("V", 0.365, 0.300, 0.318),
    ("H", 0.735, 0.900, 0.915),
    ("V", 0.905, 0.180, 0.196),
]

ROOM_U, ROOM_V = 0.545, 0.300      # the crossing the room is registered to
GUTTER = 8.0                       # the one gap size on the sheet, everywhere


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------


def _drawn_len(cmds: Sequence[GCodeCommand]) -> float:
    """Total pen-DOWN length in mm."""
    total = 0.0
    px = py = None
    down = False
    for c in cmds:
        if c.command == "M3":
            down = True
        elif c.command == "M5":
            down = False
        elif c.command == "G0":
            px, py = c.x, c.y
        elif c.command == "G1":
            if down and px is not None and c.x is not None and c.y is not None:
                total += math.hypot(c.x - px, c.y - py)
            px, py = c.x, c.y
    return total


def _snap(v: float, cell: float, origin: float = 0.0) -> float:
    return origin + round((v - origin) / cell) * cell


def _hms(minutes: float) -> str:
    h = int(minutes // 60)
    m = int(round(minutes - 60 * h))
    return f"{h} H {m:02d} M" if h else f"{m} MIN"


# --------------------------------------------------------------------------
# the plate
# --------------------------------------------------------------------------


def stable_diffusion(rng, bounds, colors: int = 3) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0

    def P(idx: int) -> Optional[int]:
        return kit._pen(idx, colors)

    pk, pr, pg, pb = P(BLACK), P(RED), P(GOLD), P(BLUE)

    # ---- coordinate maps -------------------------------------------------
    def FX(u: float) -> float:
        return x0 + u * W

    def FY(v: float) -> float:
        return y0 + v * H

    # the room: the field at 1/F, registered to the crossing + one gutter
    rw, rh = W / F_DOWN, H / F_DOWN
    rx0 = FX(ROOM_U) + GUTTER
    ry0 = FY(ROOM_V) + GUTTER
    rx1, ry1 = rx0 + rw, ry0 + rh

    def RX(u: float) -> float:
        return rx0 + u * rw

    def RY(v: float) -> float:
        return ry0 + v * rh

    # the latent grid, in sheet mm.  one latent cell = F pixels.
    px_mm = W / PIX_HW
    cell_mm = px_mm * F_DOWN                       # 6.09 mm out here
    cell_room = cell_mm / F_DOWN                   # 0.76 mm in there

    # ---- the conditioning comb c ----------------------------------------
    # a fixed set of preferred coordinates: the prompt.  Low-discrepancy so it
    # is structured, not noise, and visibly NOT aligned to the fog's cores.
    phi = 0.6180339887
    comb_u = sorted(((k + 1) * phi) % 1.0 for k in range(9))
    comb_v = sorted(((k + 3) * phi * phi) % 1.0 for k in range(6))

    def _pull(val: float, comb: Sequence[float]) -> float:
        return min(comb, key=lambda c: abs(c - val))

    # ---- encode / sample / decode ---------------------------------------
    # encode: the latent can only place a cut on its own grid.
    # sample: fifty conditioned steps land the cut on the nearest comb tick.
    # decode: the sampled latent, blown back up by F.
    z0: List[Tuple[str, float, float, float]] = []
    zhat: List[Tuple[str, float, float, float]] = []
    xtil: List[Tuple[str, float, float, float]] = []
    for orient, c, a, b in CUTS:
        span = W if orient == "H" else H
        grid = cell_mm / (W if orient == "V" else H)     # cell in unit coords
        cz = _snap(c, grid)
        z0.append((orient, cz, a, b))
        ch = _pull(cz, comb_u if orient == "V" else comb_v)
        # the loop keeps the extent it was given; only the coordinate moves.
        zhat.append((orient, ch, a, b))
        xtil.append((orient, ch, a, b))
        del span

    # =====================================================================
    # ROOM  —  latent space.  1/64 of the area, fifty visits.
    # =====================================================================
    room: List[GCodeCommand] = []

    # the ring: the room's boundary IS the loop, and it closes.
    room += _poly(
        [(rx0, ry0), (rx1, ry0), (rx1, ry1), (rx0, ry1), (rx0, ry0)], color=pg, f=1800
    )

    # fifty inward ticks on it.  position = cumulative noise level,
    # length = that step's noise level.  t enters here, and so does the
    # schedule: they bunch for forty steps and fan out over the last ten.
    peri = 2.0 * (rw + rh)
    noise = [math.sqrt(1.0 - _abar(u)) for u in STEPS]
    cum = 0.0
    cums = []
    for nz in noise:
        cum += nz
        cums.append(cum)
    for nz, cu in zip(noise, cums):
        s = (cu / cums[-1]) * peri * 0.999
        L = 1.1 + 2.6 * nz
        if s < rw:
            room += _poly([(rx0 + s, ry0), (rx0 + s, ry0 + L)], color=pg, f=1800)
        elif s < rw + rh:
            t = s - rw
            room += _poly([(rx1, ry0 + t), (rx1 - L, ry0 + t)], color=pg, f=1800)
        elif s < 2 * rw + rh:
            t = s - rw - rh
            room += _poly([(rx1 - t, ry1), (rx1 - t, ry1 - L)], color=pg, f=1800)
        else:
            t = s - 2 * rw - rh
            room += _poly([(rx0, ry1 - t), (rx0 + L, ry1 - t)], color=pg, f=1800)

    # z0 — the encoded latent, black, the subdivision the fog is eating.
    z0_segs: List[Tuple[Pt, Pt]] = []
    for orient, c, a, b in z0:
        if orient == "V":
            seg = ((RX(c), RY(a)), (RX(c), RY(b)))
        else:
            seg = ((RX(a), RY(c)), (RX(b), RY(c)))
        z0_segs.append(seg)
        room += _poly([seg[0], seg[1]], color=pk, f=1800)

    # z^0 — what fifty conditioned steps returned.  A different subdivision.
    zh_segs: List[Tuple[Pt, Pt]] = []
    for orient, c, a, b in zhat:
        if orient == "V":
            seg = ((RX(c), RY(a)), (RX(c), RY(b)))
        else:
            seg = ((RX(a), RY(c)), (RX(b), RY(c)))
        zh_segs.append(seg)
        room += _poly([seg[0], seg[1]], color=pg, f=1800)

    # c — the comb.  It crosses the ring and stops there.
    for u in comb_u:
        room += _poly([(RX(u), ry1 - 1.0), (RX(u), ry1 + 3.4)], color=pb, f=1800)
    for v in comb_v:
        room += _poly([(rx1 - 1.0, RY(v)), (rx1 + 3.4, RY(v))], color=pb, f=1800)

    # ---- the fog: q(z_t | z_0) for all fifty steps at once ---------------
    # centred normalised room coords; the prior fills the room at +-2.6 sigma
    SIG_P = 0.192

    def _marginal(sv: float, s0: float) -> float:
        acc = 0.0
        for u in STEPS:
            ab = _abar(u)
            sd = math.sqrt(max(1e-9, (1.0 - ab))) * SIG_P
            mu = math.sqrt(ab) * s0
            d = (sv - mu) / sd
            if abs(d) < 4.2:
                acc += math.exp(-0.5 * d * d) / sd
        return acc / VISITS_LAT

    # precompute a 1-D profile per cut, on a fine grid
    NPROF = 420
    profiles: List[Tuple[str, List[float], float, float]] = []
    for orient, c, a, b in z0:
        s0 = c - 0.5
        prof = [_marginal(-0.5 + k / (NPROF - 1), s0) for k in range(NPROF)]
        profiles.append((orient, prof, a, b))
    pmax = max(max(p) for _, p, _, _ in profiles)

    def _prof(orient: str, prof: List[float], t: float) -> float:
        k = t * (NPROF - 1)
        i = int(k)
        if i < 0:
            return prof[0]
        if i >= NPROF - 1:
            return prof[-1]
        fr = k - i
        return prof[i] * (1 - fr) + prof[i + 1] * fr

    # rule corridors stay clean: the fog yields to the rules that generated it
    clear_segs = z0_segs + zh_segs

    def _near_rule(px: float, py: float, r: float) -> bool:
        for (ax, ay), (bx, by) in clear_segs:
            if abs(ax - bx) < 1e-6:
                if min(ay, by) - r <= py <= max(ay, by) + r and abs(px - ax) < r:
                    return True
            else:
                if min(ax, bx) - r <= px <= max(ax, bx) + r and abs(py - ay) < r:
                    return True
        return False

    FOG_CELL = 1.02
    DASH = 0.86
    nx = int(rw / FOG_CELL)
    ny = int(rh / FOG_CELL)
    ox = (rw - nx * FOG_CELL) / 2.0
    oy = (rh - ny * FOG_CELL) / 2.0
    fog_cells = 0
    for jy in range(ny):
        for jx in range(nx):
            cx = rx0 + ox + (jx + 0.5) * FOG_CELL
            cy = ry0 + oy + (jy + 0.5) * FOG_CELL
            un = (cx - rx0) / rw
            vn = (cy - ry0) / rh
            best = 0.0
            best_or = "V"
            for orient, prof, a, b in profiles:
                if orient == "V":
                    if not (a - 0.02 <= vn <= b + 0.02):
                        continue
                    val = _prof(orient, prof, un)
                else:
                    if not (a - 0.02 <= un <= b + 0.02):
                        continue
                    val = _prof(orient, prof, vn)
                if val > best:
                    best, best_or = val, orient
            tone = min(1.0, (best / pmax) ** 0.52)
            if tone <= 0.02:
                continue
            if rng.random() > tone:
                continue
            if _near_rule(cx, cy, 0.85):
                continue
            h = DASH / 2.0
            if best_or == "V":
                room += _poly([(cx, cy - h), (cx, cy + h)], color=pg, f=1800)
            else:
                room += _poly([(cx - h, cy), (cx + h, cy)], color=pg, f=1800)
            fog_cells += 1

    room_ink = _drawn_len(room)
    room_area = rw * rh

    # =====================================================================
    # FIELD  —  pixel space.  64x the area, two visits.
    # =====================================================================
    field: List[GCodeCommand] = []

    def _rule(store, orient, c, a, b, pen, f=1800):
        if orient == "V":
            store += _poly([(FX(c), FY(a)), (FX(c), FY(b))], color=pen, f=f)
        else:
            store += _poly([(FX(a), FY(c)), (FX(b), FY(c))], color=pen, f=f)

    # visit 1 — x, on the way down.
    for orient, c, a, b in CUTS:
        _rule(field, orient, c, a, b, pk)
    for orient, c, a, b in MICRO:
        _rule(field, orient, c, a, b, pk)

    # the latent grid, shown only where it acts: three cells of it at each
    # rule, so the rounding is checkable with a ruler.
    for orient, c, a, b in CUTS:
        mid = 0.5 * (a + b)
        for k in (-1, 0, 1, 2):
            if orient == "V":
                gx = _snap(FX(c), cell_mm, x0) + k * cell_mm
                field += _poly([(gx, FY(mid) - 1.6), (gx, FY(mid) + 1.6)], color=pk, f=1800)
            else:
                gy = _snap(FY(c), cell_mm, y0) + k * cell_mm
                field += _poly([(FX(mid) - 1.6, gy), (FX(mid) + 1.6, gy)], color=pk, f=1800)

    # visit 2 — x~, on the way back out.  Nothing below one latent cell
    # returns, so MICRO has no red twin.
    for orient, c, a, b in xtil:
        _rule(field, orient, c, a, b, pr)

    rules_ink = _drawn_len(field)

    # ---- sub-cell detail: the dimensions the latent does not carry -------
    # its COUNT is solved so that ink(field) : ink(room) = 2*D_pix : 50*D_lat.
    TICK = 2.4
    want_field = INK_RATIO * room_ink
    n_detail = max(0, int(round((want_field - rules_ink) / TICK)))

    # two patches, both inside blocks, both on the gutter grid
    patches = [
        (FX(0.230) + GUTTER, FY(0.200) + GUTTER, FX(0.545) - GUTTER, FY(0.460) - GUTTER, 0.66),
        (FX(0.545) + GUTTER, FY(0.000) + GUTTER, FX(0.700) - GUTTER, FY(0.300) - GUTTER, 0.34),
    ]
    for ax, ay, bx, by, share in patches:
        n = int(round(n_detail * share))
        for _ in range(n):
            tx = rng.uniform(ax, bx - TICK)
            ty = rng.uniform(ay, by)
            if rng.random() < 0.5:
                field += _poly([(tx, ty), (tx + TICK, ty)], color=pk, f=1800)
            else:
                field += _poly([(tx, ty), (tx, ty + TICK)], color=pk, f=1800)

    field_ink = _drawn_len(field)

    # =====================================================================
    # TYPE  —  the size ratio between the two labels IS f.
    # =====================================================================
    typ: List[GCodeCommand] = []

    GIANT = 30.0
    gx = FX(0.0) + GUTTER
    typ += kit.giant_type("TWICE", gx, FY(0.460) + GUTTER + 38.0, GIANT,
                          pen=pk, weight=1.15, tip=0.52)
    typ += kit.giant_type("HERE", gx, FY(0.460) + GUTTER, GIANT,
                          pen=pk, weight=1.15, tip=0.52)

    SMALL = GIANT / F_DOWN
    lx = rx1 + GUTTER
    typ += _stroke_text("FIFTY", lx, ry0 + 2 * SMALL * 1.55, SMALL, color=pk, f=2000)
    typ += _stroke_text("TIMES", lx, ry0 + 1 * SMALL * 1.55, SMALL, color=pk, f=2000)
    typ += _stroke_text("HERE", lx, ry0, SMALL, color=pk, f=2000)

    # title strip
    tsy = FY(0.860) + 11.0
    typ += _stroke_text(" ".join("LATENT DIFFUSION"), gx, tsy, 5.0, color=pk, f=2000)
    typ += _stroke_text(
        "A SUBDIVISION NESTED INSIDE ITSELF AT ONE EIGHTH",
        gx, tsy - 8.0, 2.4, color=pk, f=2000,
    )
    typ += _stroke_text(
        "THE COMPOSITION IS NEVER MADE IN THE BIG PICTURE",
        gx, tsy - 12.6, 2.4, color=pk, f=2000,
    )

    # =====================================================================
    # FOOTER  —  every number measured off this sheet
    # =====================================================================
    total_ink = field_ink + room_ink + _drawn_len(typ)
    loop_out_here = field_ink / VISITS_PIX * VISITS_LAT
    t_now = total_ink / FEED_MM_MIN
    t_out = (total_ink - room_ink + loop_out_here) / FEED_MM_MIN
    disp_field = [abs(a - b) * (W if o == "V" else H)
                  for (o, a, _, _), (_, b, _, _) in zip(z0, zhat)]
    rms_f = math.sqrt(sum(d * d for d in disp_field) / len(disp_field))

    data = [
        "PIXEL SPACE  512 x 512 x 3 = 786432 DIM",
        "LATENT SPACE  64 x 64 x 4 =  16384 DIM",
        f"f = {F_DOWN}   AREA {AREA_RATIO:.0f} : 1   DIM {DIM_RATIO:.0f} : 1",
        f"VISITS  PIXEL {VISITS_PIX}   LATENT {VISITS_LAT}    {VISITS_LAT // VISITS_PIX} : 1",
        "",
        f"INK  FIELD {field_ink / 1000:.2f} M   ROOM {room_ink / 1000:.2f} M",
        f"     MEASURED {field_ink / room_ink:.2f} : 1   WANTED {INK_RATIO:.2f} : 1",
        f"DENSITY  {field_ink / (W * H):.3f}  {room_ink / room_area:.2f} MM/MM2",
        f"         {(room_ink / room_area) / (field_ink / (W * H)):.0f} : 1",
        "",
        "SCHEDULE  COSINE s 0.008   T 1000   50 STEPS",
        f"LATENT CELL {cell_mm:.2f} MM OUT   {cell_room:.2f} MM IN",
        f"ROUND TRIP  RMS {rms_f:.1f} MM OUT   {rms_f / F_DOWN:.2f} MM IN",
        f"LOST BELOW {cell_mm:.2f} MM  -  NO RED TWIN RETURNS",
    ]
    fx = FX(0.0) + GUTTER
    fy = FY(0.460) - GUTTER - 4.0
    foot: List[GCodeCommand] = []
    for ln in data:
        if ln:
            foot += _stroke_text(ln, fx, fy, 2.15, color=pk, f=2000)
        fy -= 4.6

    # the key — colour is the plate's key, so it is stated
    ky = fy - 3.0
    for pen, lab in ((pk, "x   THE SUBDIVISION AS IT WENT IN"),
                     (pr, "x~  DECODED BACK OUT  -  DISPLACED"),
                     (pg, "z   THE LATENT, ITS FOG, ITS LOOP"),
                     (pb, "c   CONDITION  -  TOUCHES THE RING")):
        foot += kit.fill_rect(fx, ky - 1.9, fx + 4.4, ky + 0.5, spacing=0.6, pen=pen)
        foot += _stroke_text(lab, fx + 7.0, ky - 1.5, 2.15, color=pk, f=2000)
        ky -= 5.6

    # the punchline, lower right
    punch = [
        "THE SAME LOOP RUN OUT HERE INSTEAD:",
        f"50 VISITS TO 786432 NUMBERS IS {loop_out_here / 1000:.1f} M",
        f"OF INK AND {_hms(t_out)} AT F600.",
        f"IN THERE IT IS {room_ink / 1000:.2f} M. THIS SHEET",
        f"DRAWS IN {_hms(t_now)}.",
        "",
        "THE PEN IS THE GPU.",
    ]
    pxx = FX(0.700) + GUTTER
    pyy = FY(0.300) - GUTTER - 4.0
    for ln in punch:
        if ln:
            foot += _stroke_text(ln, pxx, pyy, 2.6, color=pk, f=2000)
        pyy -= 5.6

    # two captions that confirm, never explain
    foot += _stroke_text(
        "c TOUCHES THE RING, NEVER THE FOG",
        rx1 + GUTTER, ry1 - 2.4, 2.15, color=pb, f=2000,
    )
    foot += _stroke_text(
        "NO NETWORK IS DRAWN",
        FX(0.800) + GUTTER, FY(0.620) - GUTTER - 4.0, 2.4, color=pk, f=2000,
    )
    foot += _stroke_text(
        "THE RING IS THE ONLY THING THAT CLOSES",
        FX(0.800) + GUTTER, FY(0.620) - GUTTER - 9.0, 2.4, color=pk, f=2000,
    )

    out = field + room + typ + foot
    logger.info(
        "field %.0f mm / room %.0f mm = %.2f (want %.2f) | fog %d | detail %d | total %.2f m",
        field_ink, room_ink, field_ink / room_ink, INK_RATIO, fog_cells, n_detail,
        _drawn_len(out) / 1000.0,
    )
    return out
