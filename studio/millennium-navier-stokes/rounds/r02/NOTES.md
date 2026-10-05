# millennium-navier-stokes r02 — abstract · parent: none · 2026-09-28

Lineage: **Bridget Riley, *Blaze 1* (1962), National Galleries of Scotland.** The order taken is one
line family at constant spacing whose curvature drift alone makes the surface turn. Riley's circles
look like a spiral. The plate answers her literally: in the plane a vortex really is circles (black,
Lamb–Oseen), and the spiral exists only in space (blue, Burgers), where the fluid leaves through the page.
Hybrid stated per encoding §1: an Op-Art line field on a Bauhaus sheet. The Bauhaus side supplies
furniture and type only.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-navier-stokes/rounds/r02/piece.py \
  --fn navier_stokes_blaze --seed 7 --paper a3 --margin 15 \
  --palette royalblue,black,black,crimson \
  --out gallery/studio/millennium_navier_stokes/trials/pp_millennium_navier_stokes_abstract_v15.png
```

- **Final:** `gallery/studio/millennium_navier_stokes/trials/pp_millennium_navier_stokes_abstract_v15.png` + `.gcode` (A3 portrait, seed 7).
- A4 portrait fallback, same code: `gallery/studio/millennium_navier_stokes/current/pp_millennium_navier_stokes_abstract_v16_a4.png` + `.gcode`.
  The layout scales by k = 0.674, which gives δ₀ = 13.5 mm. The 0.8 mm floor is held in real mm, so
  rungs 3–4 cull harder there. The measured blue–blue minimum gap is still ≥ 0.8 mm (0 violations).
- The seed only drives the per-arm termination dither. Seeds 7, 11 and 23 were rendered (v8, v9, v10)
  and are visually indistinguishable. 7 is kept.
- Iteration trail: v1 (classic J–L, dash-like fur) → v2 (rim arms in halving order: continuous
  arms, but the termination fronts drew RINGS inside the spiral) → v3 (rng termination dither
  removes the rings) → v4–v7 (type grid, pen floor made exact, self-wrap check fixed in the cull)
  → v8–v12 (seeds, captions, red share) → v13–v15 (recomposition: δ₀ 20, orbit factor 1.20, arm
  count derived from spacing).

## Mandate responses

No FEEDBACK.md, LEDGER.md or DESCRIPTION.md exist for this slug. This is a new plate, so there are
**no open J*/A*/S* mandates**. The binding brief is encoding.md §4 / §9 / §11 and the curator
note. Each is answered below.

| id | mandate | status |
|---|---|---|
| curator | streamlines from a real velocity field | FIXED. Every blue point is on the closed-form Burgers streamline θ(s); every black ring is an exact Lamb–Oseen ψ-isoline |
| curator | energy cascade "large → small" as real structure | FIXED. The NS-scaling ladder is λ = 2, 5 rungs, radii exactly 2.000:1 |
| curator | honest that the open question is 3D | FIXED. The plane (black) is captioned PROVED SMOOTH. The spiral is captioned as seen down the stretching axis |
| curator | one clean layer per pen, stated order, ≥ 0.8 mm, minutes per layer | FIXED, see Plot budget. Measured on the gcode: 0 blue pairs < 0.8 mm |
| curator | name the lineage | FIXED. Riley, *Blaze 1* |
| §9.1 | black rings closed, no spiral | FIXED. 20 closed circles, one stroke each, start angles staggered by the golden angle so no seam lines up |
| §9.2 | 3D caption on the spiral | FIXED. "IN SPACE: A SPIRAL / SEEN DOWN THE STRETCHING AXIS / THE FLUID LEAVES THROUGH THE PAGE" |
| §9.3 | no hand-tuned spirals | FIXED. Closed form only (E₁ by quadrature) |
| §9.4 | no pitch drift across rungs | FIXED. Core pitch measured 7.38° / 7.38° / 7.46° / 7.62° (rungs 0–3). The drift is the sampling window, not the field |
| §9.5 | no rung below the floor, nothing blue in the red ring | FIXED. Rung 5 is not drawn; red ring to rung-4 rim gap is 1.50 mm |
| §9.6 | no arrows | FIXED. None; the abstract thesis has no dotted line at all |
| §9.7 | no outlines | FIXED. Rims are where strokes start |
| §9.8 | no fills or hatching | FIXED |
| §9.9 | red only at L + stamp | FIXED. The ring, plus the stamp's "WITHOUT A PUSH: OPEN" line |
| §9.10 | no schematic furniture | FIXED |
| §9.11 | no status lies | FIXED. "CLAIMED 8 SEP 2026: BLOW-UP WITH A SMOOTH PUSH / FORCED CASE NOT YET VERIFIED · CLAY: NO AWARD / WITHOUT A PUSH: OPEN" |
| §9.12 | no "large → small" on 2D | FIXED. The 2D caption only says rings / eye only opens / proved smooth. The Kraichnan clause is in the notes corner |
| §9.13 | no pause-resume dashing | FIXED. Strokes terminate and never resume |
| §4 δ₀ = 22, orbit 1.10 | encoding numbers | ARGUED. δ₀ = **20** mm and orbit factor **1.20**. At 1.10 the red ring sits 0.82 mm from rung 4's rim: legal on the gcode, but at any viewing distance it reads as a touch, and the rubric calls that crowding. At 1.20 the rim gaps are 24 / 12 / 6 / 3 mm and then 1.5 mm to the red ring, so the halving rhythm itself runs into the limit. The longer chain (1.2·3·R₀) only fits the sheet with δ₀ = 20 (still within [12.8, 25.6), so rung 5 = 0.625 mm is still the first rung below the floor) |
| §4 red ring ≈ 7 mm | encoding estimate | ARGUED. The encoding's own formula \|C₅−L\| + R₅ gives 11.8 mm at its numbers and 11.5 mm here. The formula is kept; the "≈ 7" in the text does not follow from it |
| §6 red < 1 % of ink | accent budget | ARGUED, partly met. Red is 0.24 m of 17.98 m = **1.3 %**. Only the open clause of the stamp is red; the dated claim is black type |
| §5 stamp at x = 282 | placement | ARGUED. With L at (248.4, 52.4), a stamp under the ring would sit 1 mm off the frame. The L caption and stamp form one block right-aligned on x = 232, just outside the ring's left tangent (236.9) and under rung 4 |

## What changed from parent

There is no parent. The composition moves, as built from encoding §5 `[abstract]`:

- **One driving diagonal.** The hero is at C₀ = (62, 272), cropped 33 mm by the left frame. Four
  exact half-size copies step down a straight similarity orbit to L = (248.4, 52.4), where the empty
  red ring closes the sequence. The gaps halve with the rungs (24, 12, 6, 3, then 1.5 mm to red),
  so the eye reads the rhythm as converging.
- **The counter-weight** is the black ring disc at (228, 295), R = 40, off-axis upper right, on the
  hero's row, so the rings-vs-spiral comparison is a side glance at one height. It is 47 mm of bare
  paper from the hero rim.
- **The quiet zone** is the lower-left triangle under the orbit (≈ x 15–150, y 25–150). It is bare
  except the 2-line notes corner on the baseline.
- **Type on axes:** the title runs the full measure 15 → 282, three passes. The statement, hero
  caption and notes corner hang on x = 15. The ring and ladder captions are flush right on x = 282.
  The L + status block is flush right on x = 232.
- **Hero field construction (the key authoring decision).** Classic Jobard–Lefebvre seeding in a
  converging flow produced fur: hundreds of 10 mm stubs. The field is now 192 rim arms placed in
  halving order (6 base arms, then bisectors level by level). Each is traced rim → eye until it
  meets d_test. Later levels therefore die earlier, and the arm count halves toward the eye, like
  a polar LOD. Because the field is axisymmetric, every arm of one level died at the same radius
  and the stroke ends drew concentric RINGS inside the spiral, which is the one figure this plate
  reserves for the plane. Each arm now draws its own d_test from the rng in [0.70, 0.95]·d_sep,
  which scatters the ends. That is a pen decision, not physics: every drawn point is still on an
  exact streamline.

## Measurements / computations

Physics checks (numpy only, run on the piece's own functions):

- E₁(1) = 0.2193839 (reference 0.2193839344).
- Dossier C4: closed-form turned angle from r = 3δ to 3e⁻²δ is **8.732301 rad**. RK4 path-line
  (20 000 steps) gives r = 0.40600585, θ = 8.73230102, agreeing to 7 digits.
- Dossier C3: dθ/d ln r at the core = **−7.95774** (−Re/4π).
- Core pitch measured on the DRAWN strokes, by fitting ln r against θ over r < 0.5δ: tan β = 0.1294 /
  0.1295 / 0.1310 / 0.1338 on rungs 0–3, which is **β = 7.38° / 7.38° / 7.46° / 7.62°**. The analytic
  value is 7.16° at r → 0 and rises slightly toward 0.5δ, which is the averaging window.
- Ladder: R = 80, 40, 20, 10, 5 mm, ratios **2.000**. Centre gaps 144 / 72 / 36 / 18 mm. Centres are
  collinear to 2e-14 mm. Chain C₀→L = 1.20·3·80 = 288 mm. Red ring radius |C₅−L| + R₅ = 9.0 + 2.5 =
  **11.5 mm**; its gap to rung 4's rim is **1.50 mm**.
- Congruence: rung 1 scaled ×2 about its centre and placed on C₀ lands on the hero ink with a median
  error of **0.009 mm** and a p99 of **0.20 mm** (the 0.2 mm vertex decimation). No point is off by
  more than 0.5 mm away from the frame crop. The cull trimmed exactly 1 of 161 rung-1 strokes.
- Rings (Lamb–Oseen, r_c = δ₀ = 20 mm, out to 2 r_c): **20 rings** at equal Δψ = 0.09564 (in
  Γ/4π units), inner ring 6.26 mm, outer 38.90 mm. The **tightest gap is 1.500 mm**, centred at
  1.09 r_c; the continuous speed maximum is 1.121 r_c. The outer gap is 1.87 mm.
- Pen floor, cull per rung (in → out strokes): rung 0 134 → 132 (2 frame-crop fragments dropped),
  rung 1 161 → 161, rung 2 161 → 96, rung 3 161 → 24, rung 4 161 → 12. Rung 2 onward is where the
  floor bites, and the darkening saturates there as encoding §4 requires.
- Eyes: the innermost blue point sits 1.36 mm from the hero centre (0.068 δ). That is the single-arm
  termination. The last pair of wraps sits at the J–L gap (1.6 mm), at r ≈ 2.9 mm, as the encoding
  predicted.
- **Gcode spacing check** (own script: 0.1 mm resampling, cell hash, same-stroke pairs excluded only
  within 1.2 mm of arc): blue layer **0 pairs < 0.8 mm** on A3 (v15) and on A4 (v16).
- `promptplot preview --stats --score`: grade A. Efficiency 0.576 is the dominant issue, from the
  rim → eye travel returns.

## Plot budget

Leo: F600 = 10 mm/s draw, 2.5 s per lift/drop cycle, G0 at ≈ 33 mm/s. Order: blue → black rings →
black type (same ink, own layer, no swap needed) → red.

| layer | pen | strokes | draw | travel | ≈ min |
|---|---|---|---|---|---|
| 0 BLUE 0.3 | Burgers ladder, rim → eye, angular sweep per rung | 425 | 10.94 m | 9.26 m | 41 |
| 1 BLACK 0.1 | 20 rings, inner → outer | 20 | 2.91 m | 0.82 m | 6 |
| 2 BLACK 0.3 | type | 877 | 3.89 m | 4.24 m | 45 |
| 3 RED 0.5 | ring ×2 + open clause | 30 | 0.24 m | 0.14 m | 2 |
| **total** | | 1352 | **17.98 m** | 13.5 m | **≈ 94 min, 2 swaps** |

The longest stroke is 254 mm, one hero arm of about 25 s, so every stroke is a batch boundary.
Rungs are natural re-zero points. Travel is dominated by the rim → eye direction (each arm returns
pen-up to the rim), which encoding §10 mandates. 60 421 commands in total.

## Self-critique

1. **Hierarchy 8.** The hero dominates, the ring disc reads second and the ladder third. The hero
   to ring-disc area ratio is 4:1.
2. **Grid 7.** Three type axes (15, 282, 232), and the title spans the full measure. The x = 232
   axis is local, not structural.
3. **Tension 7.** There is one real diagonal and the hero crops at the frame. But five circles in a
   row is a known shape, and the plate's drama rests on the halving rhythm.
4. **Negative space 7.** The lower-left quiet triangle is shaped by the orbit. The void between the
   hero, the ring disc and the ladder caption (x 165–282, y 200–255) is closer to leftover.
5. **Craft for pen 8.** Measured floor, continuous arms, bare eyes and an exact congruence. But
   type costs as much time as the whole blue field (877 pen cycles).
6. **Concept 8.** Rings against spiral lands at a glance. The ladder converging on an empty red
   ring lands at 1 m. The punchline ("the pen stops first") is visible: rung 4 is 12 stubs.
7. **Depth 6, declared flat.** It is flat by lineage and a stated plan-view projection. The only
   recession is the similarity orbit.

**Single worst thing:** the type layer. It is 45 minutes and 877 pen cycles for about 350
characters of 2.3 mm single-stroke caps, as long as the hero itself. The captions are also the
only elements not on a strong shared structure with the geometry (the ladder caption floats in
the right pocket).

## Engine requests

- `kit`: a proportional caps mode whose side bearing handles `I`. Proportional mode currently
  isolates the `I` ("SHR INK ING"), so this plate uses fixed advance.
- `generators._GLYPHS`: `½ ¼ ⅛ δ Γ ω ψ –` are missing, so the captions spell 1/2, "CORE", "-".
