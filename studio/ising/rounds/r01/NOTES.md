# CRITICAL — round 01 notes

Piece: `studio/ising/rounds/r01/piece.py`, entry `ising_critical`.
Render: `.venv/bin/python scripts/render_candidate.py studio/ising/rounds/r01/piece.py
--fn ising_critical --seed 7 --paper a4 --out ~/Downloads/pp_ising_v6.png`
Renders reviewed: v1 → v6 (`~/Downloads/pp_ising_v{1..6}.png`, plus seed sweeps
`pp_ising_v5_s{3,7,13}.png`). Nothing under `promptplot/` was modified.

## Algorithm (all real, all seeded, no faking)

- **Model**: 2D Ising, J = 1, zero field, square lattice, **periodic boundaries**.
  `Tc = 2/ln(1+sqrt2) = 2.269185…` (Onsager 1944).
- **Sampler**: checkerboard **Metropolis** (numpy, sublattice update — exact,
  because same-colour sites are conditionally independent given the other
  sublattice) for burn-in, then **Wolff single-cluster** with the exact
  `P_add = 1 − exp(−2βJ)` on a flat python list (the inner loop is 5–10× faster
  off numpy). Wolff is what defeats critical slowing down: Metropolis alone needs
  `τ ~ L^2.17` sweeps at Tc, i.e. ~2·10⁴ sweeps at L = 128, Wolff needs ~3 flips.
- **Hero lattice**: `L = 128` (16 384 sites), 16 Metropolis sweeps + 90 Wolff
  flips burn-in, then 16 further samples at 12 Wolff flips apart.
- **Plate lattices**: `L = 24`, 200 sweeps + 400 Wolff flips (tiny, so over-
  equilibrated on purpose).
- **Temperatures**: hero at Tc exactly; plates at `T/Tc = 0.75, 0.90, 1.00,
  1.20, 1.80` (the 1.00 plate is drawn EMPTY — its content is the hero).
- **Domains**: exact 4-connected same-spin components by iterative BFS with PBC.
- **Walls**: dual-lattice edges between disagreeing neighbours. Wrap bonds are
  *counted* (for the energy) but never *drawn* — the sheet is a window onto the
  torus. Segments are joined into polylines with `kit._chain_segments`.

### Measured, printed on the sheet (seed 7)
| quantity | value |
|---|---|
| |m| of the drawn configuration | 0.018 |
| domains | 464 |
| two largest domains | 45.5 % and 41.1 % of the lattice |
| unsatisfied-bond fraction, chain mean | 0.1501 (seed 7) / 0.1433 (seed 3) |
| Onsager exact at Tc | 0.146447 = (1 − 1/√2)/2 |
| wall segments by tier | 2368 / 1012 / 282 black (1/2/3 pass) + 1614 red |
| plate order parameters | 0.99, 0.88, —, 0.18, 0.06 |
| draw length / travel | 12.0 m / 6.9 m, 16 446 commands, 2 pens |

## The two encodings (this is the piece)

1. **Line weight = the scale of the domain the wall encloses.** Passes are keyed
   to `min(|A|,|B|)` over the two domains a wall separates: 1 pass under 10
   sites, 2 under 120, 3 above. At Tc all three rungs are occupied *at once* —
   that is scale invariance drawn rather than asserted, and it is why the hero
   reads as continents / islands / specks instead of uniform noise.
2. **Red = the top rung** (`min(|A|,|B|) ≥ 3 %` of the lattice). In the symmetric
   sector at Tc that is a single enormous fractal interface between the two
   coexisting phases — the only long-range object on the sheet.

## What I got wrong first, and had to fix (physics, not taste)

The brief's original red rule was "a wall is red iff it bounds a domain ≥ 6 % of
the lattice", with the claim *below Tc one sea → no red; above Tc nothing
macroscopic → no red*. **That claim is false.** I measured it: at L = 128 the
largest spin cluster is 50 % at 1.15 Tc and still 36 % at 1.6 Tc, and there are
3–4 domains over 6 % well above Tc. 2D Ising **spin** clusters have their
percolation point *at* Tc (Coniglio et al.), so a big domain is not by itself a
critical signature. I also tried and rejected:

- **wrapping/spanning domains** as the "macroscopic" test — measured: the second
  giant domain essentially never wraps, even at 43 % of the lattice, so the rule
  produced no red at all;
- **hull box-counting dimension** of the largest domain — measured 0.62 / 0.95 /
  1.28 / 1.47 / 1.50 across T/Tc = 0.70 … 1.60: monotone in T, *not* peaked at
  Tc, so it discriminates nothing at this L;
- **the log–log domain-size spectrum** as the footer chart — measured R² of the
  CCDF fit: 0.90 / 0.97 / **0.985** / 0.98 / 0.995. The Tc curve is *not* the
  straightest, so the chart would have been a lie. Replaced with the **exact
  Onsager/Yang m(T)** curve plus the measured plate values, which has a genuine
  knee at Tc.

The surviving exact check on the sheet is the **unsatisfied-bond fraction**:
the chain mean lands at 0.143–0.150 against the exact 0.146447.

## Declared restriction (stated on the sheet, not hidden)

At Tc a finite lattice fluctuates between a magnetised and a symmetric
configuration; I measured |m| ∈ [0.05, 0.71] across 9 seeds. A magnetised
critical configuration genuinely has no second macroscopic domain and therefore
no interface to ink. The hero is therefore drawn from the **symmetric sector**:
16 decorrelated Wolff samples are taken from the *one seeded chain* and the least
magnetised is kept. This is a declared restriction of the ensemble, not different
physics, and the footer prints `SYMMETRIC SECTOR` plus the resulting |m|. Verified
robust on seeds 3, 7, 13 — every one produced a long red interface.

## Engine primitives used

- `Scene3D(fit="none")` as the single output surface; `halo_labels` (title +
  two subtitles) so the field opens around the type, `poly(halos=True)` for the
  hero walls, `poly(halos=False)` for deck/axis/blow-up, `emit` for kit furniture.
- `engine/geometry.py`: `HalfPlane` + `Intersect` (via a local `_convex_region`
  helper that turns any convex polygon into an inflated region) and `clip(...,
  keep="outside")` for **all** occlusion — plate-over-plate in the deck and the
  blow-up rays cut around every plate and around the hero. No hand-rolled
  `hidden = ...` conditionals, no z-buffer in the piece. `geo.offset` builds the
  multi-pass line weights.
- `engine/kit.py`: `_chain_segments`, `_poly`, `_stroke_text`, `_text_width`.
- One `_Axo` basis (`a`, `cd = 0.55a`, `wy`) for the whole scene; plate spacing
  and the deck's position are **derived from the real projected extent**
  (`span = 4d + 1 + (0.65 + zr)` in units of `a`), so plates cannot
  interpenetrate and the temperature axis, which lives in the same world at
  `z = +0.72`, is inside the sheet by construction.

## What was missing / what I had to build

- No Ising, no lattice, no Monte-Carlo anywhere in `promptplot` — `grep -n
  "ising\|phase\|spin" promptplot/generative/registry.py` returns nothing, so the
  whole sampler is new in the candidate file.
- The engine has no convex-polygon region constructor (`geometry.Rect` is
  axis-aligned only); a parallelogram needs four `HalfPlane`s. `_convex_region`
  is the missing piece and is a good candidate to promote into
  `engine/geometry.py` if a second axonometric piece needs it.
- No dash helper and no convex hull in the engine; `_dashes` and `_hull` (Andrew
  monotone chain, used to find the two frustum rays of the blow-up
  automatically) are local.
- The stroke font has only `-.0123456789A-Z`, so `=`, `/`, `+`, `>`, `|` are
  impossible; every annotation is written around that.

## Honest self-critique vs DESIGN_RUBRIC.md

1. **Hierarchy — 8.** The 137 mm field dominates at 3 m; the deck diagonal + red
   1.00 tick is the clear second; the footer and micro-chart reward 30 cm. The
   weight ladder gives a real third read inside the hero.
2. **Grid & alignment — 7.** Title, subtitles, footer block and the axis title
   all flush at `x0 + 2/+4`; the hero is flush to the right and top edges; the
   deck's back corner is a derived 30 mm under the hero. Weakest link: the
   micro-chart is aligned right but sits on its own baseline rather than the
   footer's.
3. **Tension & asymmetry — 8.** Hero cropped at two edges, hard left gutter, the
   deck running counter-diagonally, the long blow-up ray cutting the lower right.
   Nothing is centred.
4. **Negative space — 7.** The left gutter and the block between the deck and the
   chart are genuinely quiet. But the blow-up ray crosses the right-hand void,
   which weakens it slightly (deliberate — it ties the two zones).
5. **Craft for pen — 7.** Minimum spacing 1.07 mm in the hero and 0.90 mm on the
   plates (both above the 0.8 mm floor); 2 pens, one swap; weights are 1–3
   passes at a 0.24 mm offset, i.e. real weight inside a 0.5 mm tip. 12 m of draw
   is a long plot (~50–70 min). Risk: the densest plate (1.80 Tc) is near
   saturation at ~1.2 mm mean spacing.
6. **Concept legibility — 8.** It reads as a coastline map with continents,
   islands and specks at once, which is the concept, and the caption confirms
   rather than explains. It is not a schematic — the subject is the phenomenon.
   Docked for the footer micro-chart, which *is* an axis plot (permitted by the
   science-poster canon as a subordinate data footer, but it is still the most
   textbook-ish element on the sheet).
7. **Depth & dimensionality — 6.** **Declared:** the hero is flat by nature — a
   lattice configuration has no depth, and faking one would be a lie. The depth
   budget is spent entirely on the deck, which is a true shared-basis axonometry
   with exact region occlusion and a dotted blow-up frustum. This is the piece's
   weakest rubric dimension and I am not going to fix it by inventing a 3D
   surface the physics does not have.

**Verdict: borderline pass.** Biggest weakness: the deck is subordinate to the
point of being *thin* — five 47 × 26 mm plates carrying only ~40 % of the
information they could, with the two cold plates nearly empty. The next round
should either make the deck physically larger (fewer plates, bigger world
footprint on the same basis) or replace it with the block-spin renormalisation
cascade — coarse-grain the *same* Tc configuration by factors of 2 and show that
the successive levels are statistically identical, which is the sharpest
statement of scale invariance available and would give the critical plate a
structural difference that no neighbour can imitate.
