# gan r05 — iterate (first build of encoding.md rev 1, Red Meander proper) · parent: r04 · 2026-09-29

## Render
```
.venv/bin/python scripts/render_candidate.py studio/gan/rounds/r05/piece.py \
  --fn gan_meander --seed 7 --paper a4 --palette dodgerblue,crimson,black \
  --out gallery/studio/gan/trials/pp_gan_iterate_v24.png
```
- final: `gallery/studio/gan/trials/pp_gan_iterate_v24.png` + `gallery/studio/gan/trials/pp_gan_iterate_v24.gcode` (seed 7, a0 0.42622). v24 is byte-identical to v23 apart from the header. The only change was the docstring.
- trials:
  - v17: first build.
  - v18: tie-downs and legend.
  - v19/v20: reed 2.8 and the legend "T".
  - v21/v22: seeds 3 and 11, for comparison only. The encoding binds seed 7.
  - v23: hole-rim cut.

## Mandate responses
| id | mandate | status |
|---|---|---|
| S1 | title truth, `+` labelled | FIXED, held: `THE FIXED POINT REPELS`, one black `+`, `NASH EQUILIBRIUM` / `θ = ψ = 0` |
| S2 | perceived float = Σ moves | FIXED by the encoding. No float claims a length any more, and no text equates a float, dash or width with a move. Floats carry only the on-top bit. Every along-thread gap is 2.40 mm of gcode, which leaves 1.9 mm of paper at a 0.5 tip |
| S3 | no thread inside r0, full labelled h→0 circle | FIXED, held: min thread ρ 39.98 mm vs circle 38.48. The circle is 360°, dashes start at a0 (through z_0) and it is labelled `h → 0: THE FLOW CIRCLES` |
| S4 | simultaneous updates, no turn-taking words | FIXED, held. There are no L-steps either: the ribbon is the straight chord polygon |
| S5 | stats match the sheet | FIXED, held: `STEP 70 R 1.33 LEAVES THE CLOTH` is recomputed (r 1.3287, exit at (9.36, 120.90), left edge) |
| S6 | no encoding | FIXED: `encoding.md` rev 1 exists, and this round builds it |
| S8 | every in-frame iterate carries cloth; caption outside the window | FIXED for the caption: the footer tops out at y 25.3 (< 37.3) and the cloth's cut edge is the window. The iterates are ARGUED, see below |
| S8 (iterates) | as above | 196 iterates in frame. 189 lie on the ribbon centreline inside cloth. **z_0…z_6 (ρ 38.48–39.98 mm; z_6 sits exactly on the cloth edge) lie in the 1.5 mm unwoven ring between the flow circle and the cloth edge (39.98), which the encoding itself mandates.** They cannot be on cloth without inking the circle. The ribbon there is the circle-clipped half band that the encoding §10 accepts |
| S9 | on-top key in words | FIXED: footer line 3 is `WARP ON TOP: D SPOTS THE FAKE (ψθ > 0) · WEFT ON TOP: G FOOLS D (ψθ < 0)` |
| A1 | one continuous body, no jogs or orphans | FIXED by construction. The ribbon is one seamless union of chord cells, from step 0 to the crops. Its edge is quantised only by the reed. There are no L-blocks, and there are no run blocks at all |
| A2 | off-centre, hard crops | FIXED, held: `+` at (78, 113). Crops per the §5 table (measured below) |
| A3 | plot craft | FIXED: 14,686 cmds, travel 11.98 m < draw 23.10 m, min inked stroke 2.505 mm |
| A4 | shaped negative space, 12 mm gutter | FIXED per encoding §7: the only paper in the window is the hole. The 12.0 mm gutters are tagline→window and footer cap-line→window |
| A5 | accent scarce and loud | FIXED per encoding §7. Blue and crimson are co-equal players (blue 10.38 m / crimson 9.52 m of cloth ink, 52/48). Black appears in the window only as the `+`, the circle and two hole labels |
| A6 | weight advances outward | FIXED per encoding §7. The ribbon width is 0.2 ρ, so each lap is ≈1.5× wider and heavier (double-pass floats) |
| A7 | figure carried by on-top | FIXED by construction. The ribbon has no outline, channel, pen change or drawn edge. It is only where one family floats unbroken inside a 2/2 basket of the same two threads. Set every crossing to the basket rule and the sheet is a uniform checker |
| A13 | symmetric player labels | FIXED, held: `WEFT G MOVES θ` / `WARP D MOVES ψ`, flush right on x 200 |
| A14 | declared flatness | held: flat Bauhaus weaving canon |
| A17 | paper channel ≥ 3 mm, even N/E/S/W | SUPERSEDED by the encoding (no paper between laps, A7). The equivalent check is the basket channel: min 10.0 mm, channel ÷ ρ 0.233–0.272 on 8 rays (encoding asks 0.22–0.28) |
| A18 | cloth, not ladders | FIXED: one reed at 2.8 mm. The white between double-pass floats is 2.8 − 0.4 − 0.5 = 1.9 mm (≤ 2) |
| A19 | title top and end axis, brief annotation | FIXED: cap-tops at y 284.0, title ink ends at x 200.0 (cap 9.33 mm), `MIN G MAX D V(D,G)` flush right on footer line 4 |

## What changed from parent
- **Figure and ground are inverted.** r04 laid a tape on paper. r05 weaves the whole 190 × 214 mm window. The run is the region where the winning player's thread floats. The only paper is the r0 hole.
- **Every quantity moved into geometry.** The ribbon is the iterates' chord polygon scaled by 0.9–1.1 about the equilibrium. Its corners are the steps and its width is 0.2 ρ. The face is sign(ψθ). The ground is a 2/2 hopsack phase-locked half a pitch off the axes.
- **Tie-downs (my build decision, not in the encoding).** In v17 the basket over-pairs next to a float fused onto it, which extended floats by up to 2 crossings. That erased the channels between laps and turned the axis seams into continuous crosshair lines. Now a float ends by going under: the first ground crossing beyond each float end sets the floating thread under (223 flips at 441 sites). Where a warp float and a weft float would both claim one crossing, the basket rule stands.
- **Double pass is counted on ribbon crossings only.** A piece is double if it covers ≥ 3 over-crossings that lie in the ribbon. The tie-downs can make a 3-crossing basket run at the ribbon edge. Doubling those would draw a heavy outline, which A7 forbids.
- **Reed 2.8 mm, not 2.6 (the encoding §6 fallback).** At 2.6 the gcode had 16,008 cmds and 2,324 pen-downs, over both ceilings. Chaining glyph strokes saved only 4 lifts.
- **Hole-rim cut.** A crossing just inside the hole is not woven, but its warp and weft could both reach it from the rim (0.44 mm apart at (90.6, 75.2)). Both now leave the under-gap there.
- **Pens re-indexed** so that the gcode layer order IS the plot order: 0 dodgerblue → 1 crimson → 2 black.
- **Footer:** 4 lines at 1.7 mm caps, tracking 1.18, baselines 23.6 / 19.4 / 15.2 / 11.0.
- **Legend:** real 3-crossing floats (8.8 mm = 4p − g) as a "T". The weft is on line 1, and the warp hangs one reed pitch under it.

## Measurements / computations
All numbers are from `gan_meander.stats` and from a gcode parser, seed 7.

**The run**
- |λ| at r → 0: 1.00841.
- Exit at step 70, r 1.3287, at (9.36, 120.90).
- 3,641 states are computed, so the ribbon covers every window corner.

**Crossings and faces**
- Reed: 68 warps × 76 wefts, 4,528 woven crossings.
- In the ribbon: 2,333 crossings. Face = sign(ψθ) at **2,333 / 2,333 (100 %)**.
- Ground: 2,195 crossings. The pure basket (1,754, no tie-down involved) is 879 warp-over = **50.1 %**. With the tie-downs the ground is 48.6 %: ties sit at float ends and there are more warp-float ends. This is the one §11.3 number to read with care.

**Ribbon geometry**
- The ribbon spans exactly [0.9, 1.1] × chord radius on every ray (by construction).
- Chord radii per lap, 8 rays (mm):
  - 0°: 56.5 / 85.7 / 130.6
  - 45°: 39.2 / 59.0 / 88.7 / 133.2
  - 90°: 41.1 / 61.4 / 91.0 / 135.0
  - 135°: 43.3 / 65.2 / 97.8 / 146.2
  - 180°: 46.0 / 69.5 / 105.9 / 160.5
  - 225°: 48.1 / 72.3 / 108.7 / 163.3
  - 270°: 50.3 / 74.8 / 110.8 / 164.5
  - 315°: 53.1 / 79.6 / 118.9 / 178.4
- These agree with the encoding §4.1 to within 0.2.
- Basket channel between laps: min 10.0 mm (45°, 90°). Channel ÷ ρ is 0.233–0.272.

**Crops (clears ≥ 6 mm, or the edge cuts ≥ ⅓ of the width)**
- lap 0 clears every edge: L 17.3, B 20.4.
- lap 1 is cut L 8.7/14.0 and B 6.8/15.0. It clears R by 27.3 and T by 70.9.
- lap 2 is cut R 22.1/26.2 (**visible 4.1 mm**) and fully cut L/B. It clears T by 38.0.
- lap 3 is cut T 10.1/27.0 (visible 16.9).
- All pass the encoding's rule.

**Thread geometry**
- Min thread ρ 39.98 mm.
- Every along-thread gap is 2.40 mm.
- Min inked piece 2.505 mm.
- Double-pass pieces: 270.

**Ink-on-ink (gcode parser, every segment pair)**
- 0 crossings or < 0.5 mm approaches between different pens.
- Same-pen crossings exist only inside black glyphs.

**Type**
- Title cap 9.33 mm, weight 0.9 (4 passes). Ink from x 10.0 to 200.0, cap-top y 284.0.
- Tagline baseline 263.5.

## Plot budget
Leo: F600 draw, G1 F2000 travel, 2.3 s per pen cycle (G4 P1.0 × 2 plus lift).

| order | pen | draw | travel | pen-downs | est |
|---|---|---|---|---|---|
| 1 | dodgerblue (D, warp) | 10.38 m | 4.55 m | 743 | 48 min |
| 2 | crimson (G, weft) | 9.52 m | 4.28 m | 712 | 45 min |
| 3 | black (truths + type) | 3.20 m | 3.11 m | 655 | 32 min |

- Totals: 23.10 m draw, 11.98 m travel, **2,110 pen-downs** (≤ 2,300), **14,686 commands** (< 15k), **≈ 2 h 05 min** (≤ 2 h 10), 2 swaps.
- Black runs 14 min over the encoding's estimate: the footer is ~300 glyphs.
- Batching: each layer goes in reed order, boustrophedon. The longest stroke is one float, so any stroke is a safe batch boundary.

## Self-critique
- **Hierarchy 7.** At 3 m (blurred check) the first read is the crimson/blue ribbon turning colour every quarter-turn and widening outward. The hole with its `+` is second and the title third. The basket reads as a violet checker.
- **Grid 7.** Title flush 10 → 200, footer and legend on shared baselines, 12 mm gutters. The legend "T" is a little ad hoc.
- **Tension 7.** The off-axis hole and the hard crops on four sides work. The axis seams give a pinwheel cross that is partly a crosshair echo.
- **Negative space 7.** One loud void and nothing else. That is the point, but the plate is dense.
- **Craft 7.** Zero ink-on-ink, one reed, duty-based tone. In the preview the double-pass floats read only slightly heavier than the basket.
- **Concept 7.** Figure-by-float lands. The first quarter-lap from z_0 is only 1–2 threads wide (hole-clipped), so "it starts at the rim" is weak at a0.
- **Lineage 8.** This is Red Meander's order literally: same threads, only on-top differs.

**Single worst thing:** the lap-2 crop on the right edge. It leaves a 4.1 mm sliver: two long blue warp floats at x 197.0 and 199.8, running y 113–195, that hug the frame like a drawn border. The encoding's ⅓ rule passes it (22.1 of 26.2 cut), but at 1 m it reads as a graze. The fix needs a different centre or scale, which §4 fixes.

## Engine requests
- `kit.weave(crossing_rule, reed, extent, gap, double_rule)`: the per-crossing over/under lattice → gapped thread pieces, built locally here (`thread_pieces` plus tie-downs).
- ψ glyph in `_GLYPHS` (still local).
