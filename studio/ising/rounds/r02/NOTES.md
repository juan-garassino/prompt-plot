# ising r02 — COOLING STRIP (mechanism) · parent: r01 · 2026-09-28

## Render
```
.venv/bin/python scripts/render_candidate.py studio/ising/rounds/r02/piece.py \
  --fn ising_cooling_strip --seed 7 --paper a4 --orientation landscape \
  --palette black,crimson --out ~/Downloads/pp_ising_COOLING_STRIP_v9.png
```
Final: `~/Downloads/pp_ising_COOLING_STRIP_v9.png` / `.gcode`, seed 7. (v9 is byte-identical
to v8 in geometry; v9 only drops dead helpers from the source.) Seed sweep:
`pp_ising_COOLING_STRIP_v6_s3.png`, `pp_ising_COOLING_STRIP_v8_s13.png`.
Iterations: v1 spin walls (maze) → v2 FK weights + FK shore → v3 FK bond sticks + ruled sea (mud,
40 m) → v4 small droplets as dots → v5 type set on the ruling → v6/v7 clearance + colophon →
v8/v9 title spans three ruling gaps.

## Mandate responses
There is no LEDGER.md and no FEEDBACK.md for `ising` yet, so there are no open J*/A*/S* rows. The
DESCRIPTION.md "Weak" list is treated as the work order (D1–D7):

| id | mandate | status |
|---|---|---|
| D1 | [concept] lower half is a scientific figure (deck + m(T) chart + 6-line colophon) | FIXED — deck, chart, plates and blow-up rays deleted. One lattice with T ramping 0.70→1.80 Tc along x; the transition is where the crimson line is. The only furniture is a tick ruler along the top |
| D2 | [hierarchy] field reads as uniform confetti at 3 m | FIXED — three zones by density: ruled sea (calm) / crimson frontier + a dark band of large droplets just past Tc / thinning dots toward 1.8 Tc. Ink peaks at the transition because droplet size (= susceptibility) peaks there |
| D3 | [grid] two type systems; the chart sits on its own baseline | FIXED — one unspaced stroke mono. Every line of type sits in a gap of the sea's ruling (pitch 3.9 mm = 3 lattice rows), all flush on one left axis (fx0 + 5 mm). The title spans exactly three gaps with 1.3 mm clearance above and below |
| D4 | [space] leftover band v 0.50–0.58 and the empty block right of the deck | FIXED by deletion — the field fills the drawable area. Honest caveat: the plate has no bare-paper zone now; the quiet zone is the ruled sea, which is a line-screen |
| D5 | [craft] the halo behind the title leaves a ragged hole | FIXED — the halo cuts only the two straight rules the title spans, so it reads as a clean slot in the ruling. Nothing may cut the crimson line (halos off), and type is sized to the measured shore position so the shore never reaches it (clearance 4 mm) |
| D6 | [depth] field is flat and not declared | ARGUED — declared flat. A lattice configuration has no third dimension; the plate's second axis is temperature, carried by density and not by depth |
| D7 | [concept] the cold plates are empty; the cold phase has no body | FIXED — the ordered phase is a ruled line-screen: one rule per 3 rows over the held droplet, broken wherever a lake (a minority fluctuation) interrupts it |
| Keep | crimson single long-range line, weight ladder, flush crops, exact dual-lattice staircases | kept: crimson is still the only long-range object, still a dual-lattice staircase with 3 passes, still cut at the top and bottom edges (the strip wraps in y). The weight ladder carries on, but now keyed to FK droplet size (1/2/3 passes at <40 / <400 / ≥400 sites) |

## What changed from parent
- **The composition.** r01 was a square hero at Tc with a five-plate axonometric deck, a chart and a
  footer. r02 is one landscape strip filling the drawable area, with temperature as the horizontal
  axis. The ordered phase on the left is a ruled line-screen, the crimson frontier sits at the Tc
  column, and the disordered phase on the right is droplet graphs thinning into dots. All type
  lives inside the ordered sea, set on its ruling. A thermometer ruler runs along the top (ticks
  every 0.05; the 1.00 tick and label in crimson), and a single black rule at the left edge marks
  the held-up reservoir.
- **The object drawn.** r01 drew spin-domain walls. I measured that the spin-domain frontier
  sits at 1.23–1.45 Tc, not at Tc, so it cannot mark the transition. r02 draws Fortuin–Kasteleyn
  droplets instead (see below).
- **The draw, not the numbers.** v1–v3 drew every wall or bond and read as a maze. Droplets of
  2–9 sites now collapse to one dot each at their centroid, and singletons draw nothing.

## Measurements / computations (seed 7 unless noted)
Model: 2D Ising, J = 1, 212 × 137 sites at pitch 1.3 mm. Periodic in y (wrap bonds are counted
but not drawn). The left edge is coupled to a fixed +1 ghost column; the right edge is free.
T(x) = Tc·(0.70 + 1.10·x/NX), with Tc = 2/ln(1+√2). Couplings are K_ij = 1/T(x_ij): a vertical
bond takes its column's T, a horizontal bond the T at its midpoint. This is an ordinary
equilibrium ensemble with inhomogeneous couplings, so both samplers are exact:
- Checkerboard Metropolis with local field Σ K_ij s_j.
- Wolff with P_add = 1−exp(−2K_ij) per bond. A cluster that bonds to the reservoir is frozen
  and not flipped. This is Swendsen–Wang restricted to the seed's cluster. Frozen fraction: 0.27.

Schedule: 8 burn-in rounds of (40 sweeps + 1500 Wolff clusters) from all-up, then 6 production
states of (10 sweeps + 750 clusters). Runtime is about 25 s.

**Sampler check against Onsager's exact <s_i s_j>(K)**, using vertical bonds only, 20 bands,
averaged over the 6 states. The exact values come from an AGM-based K1 (no scipy):

| T/Tc | 0.73 | 0.83 | 0.93 | 0.985 | 1.04 | 1.14 | 1.25 | 1.40 | 1.56 | 1.76 |
|---|---|---|---|---|---|---|---|---|---|---|
| sim | .9572 | .9100 | .8005 | .6983 | .6496 | .5197 | .4482 | .3737 | .3178 | .2798 |
| exact | .9573 | .9091 | .8210 | .7398 | .6319 | .5184 | .4480 | .3763 | .3263 | .2785 |

RMS over the bands is 0.013 (seed 3: 0.011, seed 13: 0.017); per column it is 0.033, which is
single-sample noise. The largest deviations are at 0.93–1.04 Tc. That is expected: the gradient
cuts the correlation length off at the front width, so the finite-gradient curve is smoother than
Onsager's through Tc.

**Where the frontier sits**, from the mean x of the vertical hull edges, over 6 states per chain:

| chain | FK droplet hull | spin-domain hull |
|---|---|---|
| seed 3, all-up start | 1.024 ± 0.014 Tc | 1.225 ± 0.052 |
| seed 3, random start | 1.015 ± 0.014 | 1.277 ± 0.066 |
| seed 7, all-up start | 1.018 ± 0.018 | 1.290 ± 0.104 |
| seed 7, random start | 1.024 ± 0.014 | 1.230 ± 0.115 |

The FK frontier does not depend on the start and sits at +0.02 Tc, which is the expected
finite-gradient offset. The spin frontier is 0.2–0.3 Tc too hot, as r01 predicted (spin clusters
percolate at Tc only from below). **This is the physics reason the plate draws droplets.**

The drawn state (seed 7):
- Shore at 1.03 Tc (x = 93.3 mm, 8 mm right of the 1.00 tick); spread σ 0.062 Tc; range 0.93–1.18.
- 487 hull edges. The held droplet covers 26.2 % of the lattice.
- Largest free droplets: 441, 154, 133, 119 and 99 sites.
- Mean free-droplet size by band: 1.2 (0.74), 3.0 (0.89), 20 (0.97), **49 (1.05)**, 39 (1.13),
  14 (1.28), 7.6 (1.44) and 3.3 (1.83). This is a susceptibility peak just past Tc, and it is
  what darkens the band beside the crimson line.
- Marks: 4743 / 1776 / 502 bond segments at 1/2/3 passes, 2819 droplet dots and 195 ruled runs.

## Plot budget
Draw 20.75 m, travel 20.41 m, 49,001 commands, 5,958 pen lifts. Two pens, one swap (black, then
crimson). The previewer estimates 20.6 min; at Leo's F600 with 1 s dwells, expect roughly 2–3.5 h,
dominated by the lifts (2,819 of them are dots). Line spacing is 1.3 mm between parallel lattice
strokes. For 3-pass strokes (±0.22 mm) the gap between neighbours is 0.86 mm, above the
0.8 mm floor.

## Self-critique (rubric, honest)
1. Hierarchy — 7. At 3 m: the ruled block, the crimson coast, then the dark coral band. The
   title is only 7.5 mm (it is fitted to the room left of the shore; seed 13 gives 9.1).
2. Grid & alignment — 8. Type and lattice share one vertical module, the ruler is locked to the
   field, and there is one left axis.
3. Tension & asymmetry — 8. The field splits at one third, the frontier is crooked, and the field
   is cropped top and bottom.
4. Negative space — 6. There is no bare paper: the quiet zone is a line-screen and the hot end is
   a light dot tone. It is shaped, but it is not empty.
5. Craft for pen — 6. Spacing is legal and there are two pens, but 5,958 lifts is a long job, and
   ruled lines pass about 1 mm from the type (a deliberate ruled-paper setting that a critic may
   call grazing).
6. Concept legibility — 8. The phase transition reads as a coastline on a temperature axis with no
   caption. "TC IS A PLACE" confirms it; the ruled notebook of order is the small joke.
7. Depth — 5, declared flat (see D6).

**Single worst thing:** the right 55 % is a uniform light texture of sticks and dots. It is honest
(the droplets thin out), but it is the largest area on the sheet and carries the least. Tied with
this: there is no truly blank paper anywhere.

## Engine requests
- `Scene3D.halo_box(x0, y0, x1, y1)` as a public call. The weighted `giant_type` title needs a
  halo without also drawing a hairline label, so the piece appends to `sc._boxes` directly.
- A lattice/polyomino helper (dual-lattice hull of a cell mask) would serve every lattice plate:
  ising r01, r02 and hitomezashi-like pieces.
