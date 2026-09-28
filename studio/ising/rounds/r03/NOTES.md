# ising r03 — COASTLINE (abstract) · parent: r01 · 2026-09-28

Lineage: Bauhaus — Kandinsky, *Point and Line to Plane* (1926). The order taken: a domain
below the ruler is a POINT; every other domain is a LINE whose weight is the PLANE it encloses.
Twist: Mandelbrot, *How Long Is the Coast of Britain?* (1967), set as the title and answered
three different ways in the colophon.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/ising/rounds/r03/piece.py \
  --fn ising_coastline --seed 7 --paper a4 --palette black,crimson \
  --out ~/Downloads/pp_ising_COASTLINE_v8.png
```

- final PNG: `~/Downloads/pp_ising_COASTLINE_v8.png`
- final GCODE: `~/Downloads/pp_ising_COASTLINE_v8.gcode` (geometry byte-identical to v7, which confirms the run is deterministic)
- seed 7, a4 portrait, cream, 2 pens
- trials: v1 (log16 ladder, 1-site dots only), v2 (log8 ladder + dust), v3 (+ dotted divider walk),
  v4 (torus rolled to the widest bay), v5_s3 / v5_s13 (seed sweep), v6 (weighted title), v7 (Onsager check added to the colophon)
- runtime ~10–30 s (pure-python Wolff + BFS clusters on 42 240 sites)

## Mandate responses

There is no `FEEDBACK.md` or `LEDGER.md` for `ising` yet (no Juan verdicts, no critic
mandates). The open items are the **Weak** list in `DESCRIPTION.md` plus the COASTLINE brief,
and each is answered below.

| id | mandate | response |
|---|---|---|
| brief | full-bleed at larger L, drop deck/chart/footer, one colophon line, ladder = whole design | **FIXED.** 176×240 torus (42 240 sites, 2.6× r01's 128²) fills the drawable width and the full height above a 17 mm type band. Deck, blow-up rays and chart are deleted. Type is the title plus two colophon lines; I **ARGUE** the second line: it carries the weight key and the Onsager check, and neither fits on line 1. |
| W1 [concept] | the lower half is a scientific figure (deck + chart + colophon) | **FIXED.** Removed entirely. No axis, no plot, no panel. |
| W2 [hierarchy] | at 3 m the field is uniform confetti, and 1-site loops drown the mid rung | **FIXED.** Every domain under 8 sites (1217 of them) is now one pen touch at its centroid, so no loop is drawn. The ladder is now dust, then 109 one-pass islands, 9 two-pass, 1 three-pass continent, and the 4-pass crimson coast. At 3 m the crimson diagonal and the continent read first. |
| W3 [grid] | two type systems; the chart on its own baseline | **FIXED.** The title and both colophon lines share the field's left edge `fx0`, in one stroke face. The title uses the 2-pass rung weight, so the type sits on the same ladder as the walls. |
| W4 [space] | leftover bands at v 0.50–0.58 and right of the deck | **FIXED.** Those zones are gone. The quiet zone is now designed: the torus is **rolled** so that the widest crimson-free bay (47 sites, about 50 mm chessboard radius) sits at (u 0.30, v 0.34). The upper left becomes open sea with only islands and dust in it, and the coast runs as one diagonal from upper right to lower left. |
| W5 [craft] | ragged halo hole behind the title | **FIXED.** No halos. The type has its own band under the field's straight bottom edge. |
| W6 [depth] | flat, and not declared | **DECLARED FLAT.** A lattice configuration has no depth. Depth is carried only by weight (1, 2, 3 then 4 passes, which read as near and far planes) and by the dotted construction layer drawn over the coast. |
| W7 [concept] | cold plates empty, no body for the cold phase | **MOOT.** The plates are gone. |

## What changed from parent

- **One object, not a figure.** r01 was a hero, a deck, a chart and a footer. r03 is a single full-bleed lattice-with-defects plus a caption band.
- **The ladder is rebuilt as log8 of the enclosed area.** Passes are now `floor(log8 min(|A|,|B|))`, with dust at rung 0 and crimson at rung 4 (8⁴ = 4096 sites). r01 used 10/120 thresholds and drew every 1-site loop.
- **The twist is new.** The title is Mandelbrot's question. The crimson interface is walked with Richardson dividers, and the 16-step walk is drawn **dotted** over the coast (house law: construction lines are dotted, never arrows). The dotted chords cut every fjord narrower than 17 mm, which shows where the missing metres go. The colophon prints three lengths that disagree, plus the dimension against 11/8.
- **Composition comes from a physical symmetry.** Where the sheet cuts the torus open is a free choice under translation, so the widest bay is placed at a chosen point instead of wherever the RNG left it.
- **The lattice aspect follows the sheet.** The torus is rectangular (176×240), so nothing is cropped and nothing is stretched.

## Measurements / computations (seed 7, final render)

| quantity | value |
|---|---|
| lattice | 176 × 240 torus, pitch 1.0716 mm, 42 240 sites |
| sampler | 16 checkerboard Metropolis sweeps + 160 Wolff clusters (29.8 lattice-volumes flipped) burn-in, then 16 samples 14 clusters apart |
| symmetric-sector restriction | least \|m\| of the 16: **0.189**. The chain's \|m\| ranged 0.19–0.65, as expected at Tc for L≈200, where typical \|m\| ~ L^(−1/8) ≈ 0.5 |
| unsatisfied-bond fraction, chain mean | **0.1455** vs Onsager exact **0.146447** (−0.65 %). The drawn configuration alone gives 0.1493. |
| domains | 1338. Two giants hold 55.0 % and 31.2 % of the lattice; the next are 1.22 % and 1.19 % |
| rung populations (domains) | dust (<8) 1217 (765 singletons) · 8–63: 109 · 64–511: 9 · 512–4095: **1** (517 sites) · ≥4096: 2 giants |
| wall segments by rung | 2586 / 927 / 214 black + **2232 crimson** |
| roll applied | (52 rows, 43 cols); bay radius 47 sites |
| coast, Richardson dividers (sites) | r=1: 2232 · 2: 1592.8 · 4: 1310.4 · 8: 1042.1 · 16: 886.9 |
| coast length printed | **2.39 m** at 1.1 mm · **1.40 m** at 4.3 mm · **0.95 m** at 17 mm |
| dimension, divider slope over r 2–16 (printed) | **1.29** (exact 11/8 = 1.375) |
| dimension, sandbox M(R) over R 4/8/16 (diagnostic) | 1.30; local slopes rise with R (1.28, 1.33) |
| dimension, box counting over b 1/4/16 (diagnostic) | 1.22 |

**Honesty on D.** All three estimators come in under 11/8, and the local slopes climb toward it
as the scale grows. That is the usual lattice-scale correction at L ≈ 200: staircase roughness
flattens the small scales, and the torus cuts off the large ones. The divider value also depends
on where the frame cuts the coast. Unrolled, seed 7 gives 1.32; rolled, it gives 1.29. Seed 13
gives 1.35 and seed 3 gives 1.30. The sheet prints the measured value next to the exact one
rather than tuning the fit range until they match.

Rejected along the way:
- **The log16 ladder (v1).** At L ≈ 200 the 256–4095 rung held only 0–2 domains, and all the 2–15-site loops were still drawn, so the confetti problem remained.
- **Box counting as the printed D.** It saturates at b = 32 on a 176-wide lattice and read 1.17–1.21.
- **Seeds 3 and 13.** Their coasts run as horizontal bands, with no diagonal and no bay. Seed 7 is kept.

## Plot budget (v8)

- draw **17.1 m**, travel **11.9 m**, 28 118 commands, **2183 pen lifts**, 2 pens (1 swap)
- previewer's time estimate: 869 s at native feeds. On Leo (F600 draw, slow travel, G4 P1.0 dwells) expect about 28 min of drawing, about 6 min of travel and about 35–40 min of lift dwell, so **~70–75 min**.
- Travel is high because of the 1217 dust touches, which sit mostly one per stroke and are ordered by the colour-layer optimizer.

## Self-critique (rubric, honest)

1. **Hierarchy: 8.** At 3 m the crimson diagonal dominates. The one 3-pass continent sits in the open bay as the second read. Islands and dust come third, and the dotted ruler walk and the colophon reward 30 cm.
2. **Grid & alignment: 8.** One left edge carries the field, the title and both colophon lines. The field is flush to the top, left and right drawable edges. The band is a measured 17 mm.
3. **Tension & asymmetry: 8.** The coast crosses as one diagonal and the bay sits upper left. Coast fragments are cut off at the left and right frame (the torus seam), which is intentional because the coast continues off the sheet.
4. **Negative space: 7.** The bay is designed: it was chosen by computation and placed on purpose. But it is still dusted with points and dotted with 1-pass islands, so it is quiet rather than empty. The type band is thin.
5. **Craft for pen: 7.** Lattice pitch is 1.07 mm, above the 0.8 mm floor. The ladder widths are about 0.5 / 0.76 / 0.98 / 1.13 mm. However, **27 % of crimson wall edges have a parallel wall one site away**. Where the coast has a fjord one site wide, the two 4-pass banks fuse into a single ~2.2 mm crimson bar. I **ARGUE** this is honest: the pen tip is the finest ruler on the sheet, so it cannot resolve below its own width, which is the coastline point. It is still ink on ink. Caption type is 1.54 mm, small but legible.
6. **Concept legibility: 8.** It reads as a coastline map at every scale without the caption. The title's question and three disagreeing lengths land the joke, and the dotted chords show the answer geometrically. Nothing on the sheet is a figure.
7. **Depth: 6 (declared flat).** Only weight-as-plane and the dotted construction layer create depth.

**Single worst thing.** The 109 one-pass islands are near-identical in size and evenly scattered.
That middle texture is still a uniform "archipelago wallpaper" once you step past the red and the continent.
It is the physics (the power-law tail is steep), but the sheet does nothing to shape it.

## Engine requests

- A `dot`/pen-touch primitive that is a true zero-length touch (`M3`, dwell, `M5`). `_dot` is a 2r horizontal tick, and I use r = 0.22.
- A `_convex_region` / polygon-to-Region helper is still missing, as in r01. It was not needed here.
