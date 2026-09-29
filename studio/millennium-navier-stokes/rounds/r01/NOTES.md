# millennium-navier-stokes r01 — faithful · parent: none · 2026-09-28

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-navier-stokes/rounds/r01/piece.py \
  --fn navier_stokes_faithful --seed 7 --paper a3 --margin 15 \
  --palette royalblue,black,black,crimson \
  --out gallery/studio/millennium_navier_stokes/current/pp_millennium_navier_stokes_faithful_v6.png
```

- final: `gallery/studio/millennium_navier_stokes/current/pp_millennium_navier_stokes_faithful_v6.png` + `.gcode` (seed 7, A3 portrait, margin 15)
- trials: v1 (J–L seeding, fragmented arms, type collisions) · v2 (PolarLOD arms) · v3 (bottom row fixed)
  · v4 (hero d_test 1.7) · v5 (red 2nd pass moved inward) · v6 (T0 glyph)
- The piece uses no randomness. Every mark is an exact streamline, ring or level set, so every seed gives the same output. `rng` is accepted only to satisfy the contract.
- Lineage: **Bridget Riley, *Blaze 1* (1962)**. The order taken from it is one line family at constant spacing, where curvature drift alone makes the surface turn. Riley's concentric circles read as a spiral. Here the circles are the plane, and the spiral is real only in 3D.

## Mandate responses

| id | mandate | status |
|---|---|---|
| — | No FEEDBACK.md, LEDGER.md or DESCRIPTION.md exists for this slug (new plate) | n/a: first round, no open J*/A*/S* rows |
| curator | Streamlines come from a real velocity field; the cascade is real structure; say the open question is 3D | FIXED: exact Burgers streamlines (closed form); the ladder is exact NS scaling; the black disc is exact 2D Lamb–Oseen; the captions name 2D/3D |
| curator | Plottable: one layer per pen, stated order, spacing ≥ 0.8 mm, minutes per layer | FIXED: 4 layers, blue → hairline → type → red; min blue–blue gap on the gcode is 0.813 mm; see budget |
| curator | Name the lineage (Riley) | FIXED: *Blaze 1* |
| enc §4 | Seeding by Jobard–Lefebvre | ARGUED: v1 used a real J–L on the field (292 streams, 10.1 m). Its mid-field starts and stops read as dashes, which breaks §9.13's spirit. I switched to the dossier's other allowed seeding (§4: "rotated-copy arms, N equal shares of the axisymmetric inflow"). There are N = 256 arms, thinned toward the eye by the engine's `PolarLOD`, and the level radii are computed, not tuned (see below). Every line is still an exact streamline. The J–L function stays in the file. |
| enc §4 | d_sep 2.4 / d_test 1.6 | ARGUED: 256 arms give 1.94 mm at the rim. The halving rule keeps the spacing between 1.7 and 3.4 mm. d_test was raised to 1.7 so that rung 1 (0.85 mm) clears the floor and stays congruent with the hero. |
| enc §4 | Orbit gaps 1.10·(R_n + R_n+1) | ARGUED: with a curl Δφ ≠ 0, factor 1.10 puts the red ring ON rung 4 (the encoding's rule only works for Δφ = 0). I kept the binding outcome instead: the red ring encloses all rungs ≥ 5 and clears rung 4 by ≥ 0.8. That forces k/m = 2.2, so \|C0 − L\| = 3.3 R0 = 290.4 mm for any Δφ (this matches the encoding's 290). With Δφ = −20°, k = 1.35. |
| enc §5 | Red ring ≈ 7 mm | ARGUED: the encoding's own formula \|C5 − L\| + R5 gives 9.08 + 2.75 = **11.83 mm**. Drawn at 11.83 mm and 11.48 mm (2nd pass inward). |
| enc §6 | Red < 1 % of ink | ARGUED: measured 2.2 % (0.51 m of 23.8 m). A dated two-line stamp at 2.2 mm caps cannot go lower and stay legible. The ring itself is 0.15 m (0.6 %). |
| enc §9.10 | Sheet border only if the series adopts it | FIXED: no border drawn. The reference's frame rule and tick marks were dropped. |

## What changed from the reference (faithful layout fixes)

Measured off `ref/reference.png` (1122 × 1402 px) with colour masks, row/column scans and a least-squares circle fit:

| element | measured (px) | normalised (u, v↓) |
|---|---|---|
| frame rule | x 28–1093, y 32–1368 | u .025–.974, v .023–.976 |
| title caps | x 59–459, y 81–104 (cap 23 px = 1.64 % H) | u .053–.409, v .058–.074 |
| hero eye | (432, 562) | (.385, .401) |
| red circle | (834, 530), r 11 | (.743, .378) |
| eddy lobe | (865,260) (985,375) (980,535) (945,610) | u .77–.88, v .19–.44 |
| zoom inset | centre (858, 981), R 182.4 | (.765, .700), R .163 W |
| corner captions | cap 6 px, pitch 14.5 px, 20 px rule | TR .896–.949/.058–.099; L .067–.111/.667–.711; BR .892–.948/.908–.957 |

Fixes, one per reference fault:
1. **The upper-right eddy lobe (a flat picture of spirals, which is dossier lie 1) becomes the 2D ring disc.** Same quadrant, R = 44 mm. The one place the reference showed planar spirals now shows the only thing a plane allows.
2. **The circular "zoom" inset (its X is the Burgers side view) becomes a true side view.** Meridional streamlines r²\|z\| = C at equal Stokes Δψ, on the same scale as the plan, clipped to a 35 mm disc (the inset's circular window, with no outline). It moves from the lower right to directly under the hero, joined to the hero's eye vertical by one dotted projection line. The dashed zoom cone is dropped (§9.6).
3. **The red point at the saddle becomes the empty red ring at the ladder's limit L**, which is the smooth-or-not question placed where it belongs. The four eddies become the ladder rungs 1–4, curling down the right side (Δφ = −20° per rung, stated).
4. **The wave tail (lower left) is not drawn.** No exact solution in play has a non-axisymmetric inflow. The hero is instead cropped 37 mm by the left frame, and its far-field arms (nearly radial, β = 64° at 4δ) carry the "arriving flow". The lower-left becomes the quiet zone and holds the side view.
5. **The hero moved from u .385 to x = 66 mm.** Its centre leaves the sheet's middle third, and the frame crops it on purpose.
6. **Captions were rewritten honestly.** "LARGE SCALES TO SMALLER ONES" sits on the 3D ladder only, never on a 2D field. "MOTION CONNECTS SCALES" becomes "SAME EQUATIONS / EVERY SCALE". "SAME EQUATIONS DEEPER QUESTIONS" becomes the dated red stamp. The italic subtitle becomes the one-line statement.
7. **Title:** the reference's 6.7 mm cap was raised to 8 mm (encoding §5), drawn in 2 passes, flush with the x = 15 frame instead of indented at u .053.

## Measurements / computations

Physics (δ = 1, ν = 1, Re_Γ = 100, δ0 = 22 mm on A3):
- E1(1) = 0.2193839344, E1(2) = 0.0489005107 (series below 1.5, Lentz continued fraction above).
- Closed-form streamline vs RK4 path-line (dossier C4: r0 = 3δ, αT = 4): RK4 gives r = 0.4060058, turned 8.732301021 rad. Closed form θ(s) gives 8.732301021 rad, agreeing to 5 × 10⁻¹³.
- Core pitch: dθ/d ln r = −7.946 (theory −7.958). β0 = 7.17° (theory 7.162°). β = 11.2° at δ, 27.1° at 2δ, 48.5° at 3δ, 63.6° at 4δ.
- Arms: N = 256 rotated copies of θ(r). The perpendicular spacing of M arms is 2πr·sin β(r)/M, and it increases with r. Arms with 2-adic valuation k die where N/2^k arms reach 1.7 mm. **PolarLOD levels (hero, mm):** 1 → 80.6 · 2 → 55.5 · 4 → 41.5 · 8 → 31.1 · 16 → 22.1 · 32 → 14.2 · 64 → 8.1 · 128 → 4.3 · arm 0 → **eye 1.39 mm** (its own outer wrap reaches 1.7 mm; the outer wrap sits at ≈3.1 mm).
- Ladder (λ = 2): δ_n = 22, 11, 5.5, 2.75, 1.375 mm; R_n = 88, 44, 22, 11, 5.5 mm. Rung 5 (δ 0.69 mm) is under the floor and not drawn. Centres (mm): C0 (66.3, 268.9), C1 (202.2, 181.1), C2 (251.0, 116.6), C3 (262.9, 77.9), C4 (261.9, 57.8), L (250, 44). Centre gaps 161.8 / 80.9 / 40.4 / 20.2 (ratio exactly 2.000). Rim gaps 29.8 / 14.9 / 7.4 / 3.7.
- Cull pass at 0.82 mm, longest first, each stroke shortened from its inner end:

| rung | arms in | kept | length kept / uncut (m) |
|---|---|---|---|
| 0 (frame-cropped) | 212 pieces | 211 | 8.78 / 8.78 |
| 1 | 256 | 256 | 5.15 / 5.18 (99.3 % congruent with hero ×½) |
| 2 | 256 | 128 | 1.28 / 2.59 |
| 3 | 256 | 32 | 0.27 / 1.30 |
| 4 | 256 | 16 | 0.064 / 0.65 |

  The floor removes the finest PolarLOD levels, so the darkening saturates exactly where the pen gives out.
- **Measured on the gcode:** min blue–blue gap between strokes **0.813 mm**, min self gap (own wraps) 0.828 mm. The nearest blue to L is 12.84 mm, so rung 4 clears the ring's outer pass (11.83) by 1.0 mm.
- Lamb–Oseen disc: r_c = 22 mm, rings at equal Δf = 0.09 in f = ln s + E1(s) (ψ / (Γ/4π)) out to 2 r_c. **22 rings**, inner ring 6.18 mm, **tightest gap 1.55 mm at r = 23.6 mm** (1.07 r_c; the speed maximum is at 1.12 r_c), outer gap 1.98 mm. Each ring is one closed stroke, drawn inner → outer.
- Side view: Stokes ψ = α r² z / 2, levels C = 0.1, 0.3 … 1.5 δ³ (8 levels × 4 branches), in a 35 mm disc. The tightest gap is about 1.5 mm at the window's 55° diagonal. The axis is a solid line inside the window, and one dotted projection line (0.35 mm ticks every 2 mm) runs from y 148 to y 178 on x = 66.3, the hero's eye vertical.

## Plot budget

Measured on `…_v5.gcode` (v6 differs only by one caption glyph). Time uses Leo F600 = 10 mm/s draw, 33 mm/s travel, 2.5 s per lift/drop:

| order | pen | strokes | draw | travel | ≈ min |
|---|---|---|---|---|---|
| 1 | blue 0.3 (royalblue) — 3D streamlines | 643 | 15.54 m | 10.8 m | 58 |
| 2 | black 0.1 hairline — rings, side view, projection line | 70 | 4.61 m | 1.7 m | 12 |
| 3 | black 0.3 — type (same ink, own layer) | 873 | 3.12 m | 4.0 m | 44 |
| 4 | red 0.5 — empty ring (2 passes) + stamp | 107 | 0.51 m | 0.6 m | 6 |
| **total** | 4 layers, 2 real ink swaps | 1 693 | **23.8 m** | 17.3 m | **≈ 2 h** |

- The longest blue stroke is one hero arm (≈ 300 mm, ≈ 30 s), so every stroke can serve as a batch boundary. Rungs are natural re-zero points.
- Blue has 643 cycles, under the 900 cap.
- The type layer is the time sink (873 cycles). The 2-pass title alone is ≈ 60 cycles.
- `promptplot preview --stats --score`: grade A (efficiency 0.59, the dominant issue, from travel between rungs and caption blocks).
- Confirm with Juan that Leo takes A3 before plotting. On A4 the piece rescales uniformly and keeps the paper-mm floors (δ0 → 15.5 mm), and the cull removes more arms.

## Self-critique (rubric, honest)

| dim | score | note |
|---|---|---|
| Hierarchy | 8 | The hero dominates (cropped hero ≈ 3.4× the disc area). The disc and rung 1 are the second read, rungs 2–4 plus the red ring the third. Rung 1 is nearly as heavy as the disc, which dilutes the 2D/3D pair. |
| Grid & alignment | 7 | Left type is on x = 15 and right type on x = 282. The TR caption shares the statement baseline, and the bottom row shares baselines. The hero caption and ladder caption hang off local geometry rather than a sheet axis. |
| Tension & asymmetry | 8 | Frame-cropped hero, a hooked ladder down the right side, the disc off-axis. |
| Negative space | 7 | The channel between hero and disc and the lower-left quiet zone are shaped. The middle band (x 110–190, y 130–180) reads a little leftover. |
| Craft for pen | 8 | Floors hold on the gcode. Rings are closed and single-stroke. Arms run rim → eye. Type costs a lot of cycles. |
| Concept legibility | 8 | Rings vs spiral reads at 3 m. The ladder at exactly ½ and the empty red ring read at 1 m. |
| Depth | 7 | Flat by lineage (declared). Depth comes from the ladder's recession and the same-scale side view. |

**Single worst thing:** the reference's big gesture, the wave sweeping in from the lower left into the spiral, is gone. The hero is a cropped disc with a hard circular rim. That is exact (the Burgers field is axisymmetric and truncating it is a window) but less alive than the reference. No exact solution in play gives that tail honestly.

## Engine requests

- `PolarLOD` works as a level rule for radial line families outside `Scene3D`. A small public helper that computes levels from a spacing function g(r) and d_test would remove the hand bookkeeping here.
- A proportional, tracked type helper with `align=` (every Millennium round re-implements `_glyph`/`text` locally).
