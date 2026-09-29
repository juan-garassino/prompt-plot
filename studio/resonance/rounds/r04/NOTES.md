# resonance r04 — one-field (abstract) · parent: r01 · 2026-09-28

Lineage: **Op Art, Bridget Riley, *Current* (1964).** The order it takes from Riley is one
line family whose phase relation makes the surface move. Here there are two crest families,
and their phase difference decides where they fuse into one black line and where they cancel
to bare paper. The twist is **Thomas Young's two-source plate (*A Course of Lectures on
Natural Philosophy*, 1807)**. The most famous two-circle line drawing in physics comes back
with its screen reading as a softmax, and the colophon credits Young.

Canon: Op Art, which is optically flat (declared, see Self-critique §7). The type is
Swiss-restrained, flush left.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/resonance/rounds/r04/piece.py \
  --fn attention_one_field --seed 7 --paper a4 \
  --palette crimson,dodgerblue,black,black \
  --out gallery/studio/resonance/current/pp_resonance_one-field_v6.png
```

- final PNG: `gallery/studio/resonance/current/pp_resonance_one-field_v6.png`
- final GCODE: `gallery/studio/resonance/current/pp_resonance_one-field_v6.gcode`
- A4 portrait, cream, seed 7. **The plate is deterministic and seed-invariant.** `rng` is
  never used, and seeds 3, 7 and 13 give byte-identical commands (sha1 `fc669756dcf0`).
- trials: v1 (Q drawn first, K shredded by the r01 guard), v2 (agree→black and
  disagree→colour rule, 12λ), v3 (6λ plus the parallel/crossing regimes), v4 (nodes left as
  paper, tapered rays, type layer), v5 (λ 3.4, `fade_c` 0.4, serpentine heavy line), v6
  (colophon wording, final). Quick side-by-side layout trials were made outside Downloads.

## Mandate responses

There is no `LEDGER.md` or `FEEDBACK.md` for `resonance` (no J/A/S rows exist). The open
items are the curator note (C) and the DESCRIPTION **Weak** list (W).

| id | mandate | response |
|---|---|---|
| brief | one-field: blow the crest field up to about 80 % of the width, crop at both sides, Q/K become the two sources with packets folded into phase and wavelength, softmax read as intensity along one horizontal cut drawn as the single heavy line, delete every box/arrow/gradient label | **FIXED.** The field runs full-bleed and is cropped left, right and top. Q and K are the two sources, and each packet pair is folded into one resonant λ plus amplitude and phase (§Measurements). The heavy line is softmax(β·cross-term) along y = 79 mm, and the field stops exactly on it. Nothing from r01's apparatus survives. |
| C1 | keep family grammar (Q crimson, K blue, the two-source Huygens field as hero, V goldenrod, Z green, MoE/FFN violet) | **FIXED for Q/K/hero, ARGUED for V/Z/violet.** Crimson is Q's own crests and blue is K's, which is the family grammar with the packets folded into the sources. Black is the interference and the softmax, as in v13. This thesis has no V, Z or MoE stage, so no pen is given those meanings. No colour means anything different from the siblings, so the three plates still hang as one series. |
| C2 | no pen cap; each pen one clean colour layer with a stated order and meaning | **FIXED.** 4 layers, never re-entered: 0 crimson (Q crests + source + label), 1 blue (K), 2 black (sum crests + heavy line), 3 black fine (type only). Order runs light→dark, so black lands last over the colour ends at the knot rim. Layer 3 exists so the type can take a finer nib (0.2–0.3); if the same pen is kept, that swap is a no-op. |
| C3 | strokes spatially ordered for batching | **FIXED.** Each layer is ordered greedy nearest-neighbour **with reversal** in the piece. postprocess's no-reversal NN reproduces that order. Crest arcs alternate direction ring to ring. The heavy line's 3 passes are serpentine (r01's ran all passes left→right, which cost 2×190 mm dead travel). Intra-layer travel is 5.0 m for 10.5 m draw (48 %; r01 was 110 %). 7 hops exceed 50 mm (worst 175 mm), all greedy stragglers. The longest single stroke is one heavy-line pass (502 mm, about 1 min at F500), which is a clean batch boundary. |
| C4 | minutes per layer + total | **FIXED.** See Plot budget: 3.5 + 3.4 + 34.6 + 10.6 ≈ **52 min** plus 3 swaps. |
| C5 | 3471 pen cycles / 110 % travel, dotted runs must earn their cycles | **FIXED.** **851 pen cycles** (−75 %), **zero dotted runs on the sheet**. Every lift ends a crest arc at a real boundary: the edge of a bright fringe, the sheet edge, the heavy line or the knot rim. Slivers under 2 mm are dropped (21 strokes). |
| C6 | name the LINEAGE | **FIXED.** Riley *Current* (1964), plus Young 1807 as the twist (top of file; `lineage:` in HANDOFF). |
| W1 [concept] | it is a schematic (boxes-and-arrows flow) | **FIXED.** No labelled flow and no arrow. The order is INTERFERING. The only labels are `Q` and `K` beside their own sources, plus a title block. |
| W2 [hierarchy] | everything mid-size | **FIXED.** The field is 100 % of the width and ~72 % of the height. The heavy line is the second read (only 1 mm-weight line on the sheet). The crimson/blue knot (~55 mm) is the third read. Crossings reward 30 cm. |
| W3 [tension] | mirror-symmetric top half, centred title | **FIXED.** The source pair sits at u 0.30, v 0.18, with the axis tilted +28°. The fan sweeps down-right and the zero-order (Q·K resonance) fringe lands at x = 150 mm. Softmax peak heights fall left→right (0.85, 1.00, 0.94, 0.74, 0.50, 0.29). Title flush left. |
| W4 [craft] | six pens / five swaps; scatter dots muddy the net; crammed ∂L stack | **FIXED.** No scatter dots and no stipple: every mark is a crest, the heavy line or type. The ∂L stack is deleted. 4 layers, 3 swaps (and one can be skipped). |
| W5 [space] | no generous quiet zone | **FIXED.** A 52 mm band of bare paper sits between the heavy line and the title. The nodal rays inside the field are paper too, so the void enters the dense zone as rhythm. |
| W6 [depth] | flat, undeclared | **DECLARED FLAT (Op Art).** Recession comes from physics: the black rays are gated by an ABSOLUTE intensity, so they taper as I ∝ 1/r and thin toward the frame. |
| W7 [craft] | the reference's midline comb reduced to two diamond clusters; reads as two bullseyes, not one field | **FIXED by the thesis.** It is one field: the two bullseyes survive only as the resolvable knot, and everything else is their sum. |
| it-1 | delete the 60 scatter dots and stipple caps | **FIXED** (gone). |
| it-2 | hero up 1.5×, Q/K blocks down | **SUPERSEDED.** The hero is the sheet, and the Q/K blocks are folded into the sources. |
| it-3 | re-space ∂L stack | **MOOT** (deleted). |
| keep | Huygens crest loci, d a whole number of λ, crossing-safe guard | **KEPT / PROMOTED.** Crests are r_s = (m − φ_s/2π)L, and d = 6λ (whole). The guard's parallel test (25°) is now the regime boundary, so a crossing never meets a near-parallel neighbour. Measured crowding is below. |

## What changed from parent

- **The apparatus is gone and the phenomenon is the sheet.** r01 was a reproduction of a
  flow diagram with a 42 mm hero in the middle. r04 is one field, one cut and one caption.
- **One drawing rule makes the whole plate.** Draw each wave's crests (crimson, blue) where
  the pen can hold them apart, meaning they cross at more than 25°. Everywhere else, draw what
  they add up to: black crests of the SUM where the intensity clears a level, and bare paper
  where they cancel. The knot, the sunburst of rays and the white nodal rays all follow from
  that rule. Nothing is placed by hand except the source pair and the cut.
- **The screen is the softmax.** Where the field meets the cut, its edge is
  softmax(β · cross-term). The field is clipped exactly on that curve, so every black ray
  lands inside a peak: the same equation read in two places.
- **Q and K are the two sources, and each packet is folded into one complex amplitude.** The
  best pair by cosine is chosen, and both sources radiate at the frequency where their spectra
  overlap (§Measurements).
- **A whole-composition move against symmetry.** The source pair is upper-left and tilted, the
  fan sweeps to the lower right, and the peak heights descend.
- **Plot economy.** 851 cycles instead of 3471. Travel is 48 % of draw instead of 110 %. No
  dotted leaders.

## Measurements / computations (final parameters, seed-invariant)

**Fold** (`fold_packets`, xi from each block's node column toward the centre; r01's packet
tables verbatim):

- cosine matrix C_ij = S_ij / (|q_i||k_j|), rows Q1–Q5, columns K1–K5:
  ```
  [-0.115  0.109 -0.028  0.313  0.448]
  [-0.411  0.655 -0.059  0.406 -0.002]
  [ 0.006 -0.043 -0.335  0.019 -0.005]
  [-0.594  0.414  0.002  0.748  0.082]
  [ 0.086 -0.038 -0.039 -0.131 -0.712]
  ```
- best pair: **Q4 · K4, cos 0.748**, S = 12 475 (ref-px units). The Parseval check
  (1/π)Re∫Q̂K̂* dω = 12 475.057 agrees to 5 × 10⁻⁶ relative.
- resonant carrier ω0 = argmax|Q̂4 K̂4| = 0.4925 rad/px → λ0 = 12.758 ref px. On the sheet
  λ = 3.4 mm (drawing scale). The geometry depends only on d/λ = 6 and the angles.
- source amplitudes |Q̂4(ω0)| = 701.3, |K̂4(ω0)| = 621.2 → a_Q/a_K = 1.129.
- phases φ_Q = −2.1739, φ_K = −2.2673 → **Δφ = +0.0934 rad** (printed as 0.09 in the
  colophon's cos(…)).

**Geometry:** Q at (57.99, 232.35) mm and K at (76.01, 241.93) mm. d = 20.40 mm = 6λ exactly.
The screen is at y = 79.25 mm.

**Exactness of the drawn crests** (measured on the emitted polylines):
- black sum crests: |arg ψ| max 8.0 × 10⁻⁵ rad (≈ 4 × 10⁻⁵ mm); mean 1.9 × 10⁻⁸ rad.
- crimson/blue crests: crest-phase error max 4.6 × 10⁻³ rad (≈ 0.0025 mm, only at
  bisected run ends).

**The heavy line** (softmax over 761 keys, one every 0.25 mm, β = 6):

| peak x (mm) | height / max | attention mass | residual to antinode 2πj | order j |
|---|---|---|---|---|
| 27.50 | 0.845 | 0.223 | +0.006 rad | −4 |
| 61.00 | 1.000 | 0.212 | +0.023 | −3 |
| 90.25 | 0.939 | 0.187 | +0.022 | −2 |
| 119.00 | 0.741 | 0.156 | −0.010 | −1 |
| 150.25 | 0.500 | 0.125 | −0.037 | 0 (zero path difference) |
| 187.75 | 0.292 | 0.097 | −0.035 | +1 |

Every peak sits on an antinode (|residual| ≤ 0.037 rad, i.e. the black rays land inside the
peaks). The masses sum to 1.000. The entropy is 5.40 nats of a 6.63 maximum (exp H ≈ 221
effective keys). The zero-order fringe is not the tallest: the amplitude factor r0/√(r_Q r_K)
favours fringes nearer the sources, so the loudest resonance and the zero path difference
separate. That is visible as the descending peak heights. β is the one chosen number
(= |q||k|/√d_k; e.g. |q||k| = 48 at d_k = 64).

**Ray gating:** I_th is set so that cos Δ ≥ 0.4 at the screen point below the pair.
c_min = −0.6, so nodes are always paper.

**Line spacing** (r01's metric on the crest strokes only: 0.25 mm resampling, "crowded" =
another stroke within 0.8 mm AND within 25° of parallel):
- crest draw 7 659 mm (Q 1 012, K 1 014, SUM 5 634)
- crowded **120.5 mm = 1.57 %** (r01 hero 3.3 %, r01 plate 21.5 %)
- sustained runs ≥ 3 mm: **0 mm**; longest run 2.25 mm. These are the borderline 25–26°
  crossings at the knot rim and the black/colour hand-off there.
- The heavy line's three passes are 0.33 mm apart on purpose (weight). Type and labels are
  multi-pass on purpose (giant_type weight).

**Bounds:** ink bbox x 10.00–200.00, y 10.41–287.00 on a 10–200 × 10–287 drawable. Clean.
The field is cropped exactly on the frame.

## Plot budget (v6 gcode; Leo model F500 draw, F1800 travel, 1 s dwell per M3 and M5)

| layer | pen | meaning | strokes | draw | travel | ~min |
|---|---|---|---|---|---|---|
| 0 | crimson | Q: its own crests (knot), source, `Q` | 39 | 1.05 m | 0.26 m | 3.5 |
| 1 | dodgerblue | K: its own crests (knot), source, `K` | 33 | 1.05 m | 0.35 m | 3.4 |
| 2 | black 0.3–0.4 | the sum: bright-fringe crests + the heavy softmax line | 560 | 7.06 m | 3.21 m | 34.6 |
| 3 | black fine 0.2–0.3 | type only (title, colophon) | 219 | 1.35 m | 1.00 m | 10.6 |
| **total** | | | **851** | **10.51 m** | **5.03 m** | **≈ 52 + 3 swaps** |

31 804 commands. `preview --score`: grade A, 851 pen lifts. Suggested nib 0.3–0.4 for the
field (crest pitch 3.4 mm, far above the 0.8 mm floor).

## Self-critique (seven dimensions)

1. **Hierarchy 8.** At 3 m the sunburst reads first, then the one heavy line, then the colour
   knot. Crossings reward 30 cm.
2. **Grid & alignment 7.** The field, the heavy line and the type all hold the drawable edges,
   with the type flush left on x0. The source pair's position (u 0.30) is chosen by eye, not
   locked to a documented module.
3. **Tension 8.** Upper-left origin, diagonal sweep and descending peaks. No axis of symmetry
   survives.
4. **Negative space 8.** The paper band under the screen is shaped by the heavy line's
   horizon. The nodal rays bring the void into the dense zone.
5. **Craft 7.** Pitch is 3.4 mm, there are 0 mm of sustained crowding and no floods, and
   every lift is earned. Weakness: some rays end in short 2–4 mm ticks where a softmax spike
   splits them near the screen.
6. **Concept 7.** "Two sources, one screen" lands in a glance, and the rays visibly land in
   the peaks. That the screen is *attention* still depends on the title and colophon: the
   caption confirms rather than explains, but the plate cannot say "softmax" without it.
7. **Depth 6 (declared flat).** Op Art flatness, with intensity falloff giving the rays some
   recession. Nothing more.

**The single worst thing: the knot's rim.** The colour-to-black hand-off happens on the
25° inscribed-angle circles. The rule is exact, but at 1 m the two coloured lobes read a
little like discs pasted on the sunburst, rather than the sunburst growing out of them.

## Engine requests

- `postprocess.optimize_stroke_order` never reverses a stroke. Every piece has to
  pre-orient its strokes, and greedy stragglers still leave 50–175 mm hops. A
  reversal-aware NN plus a cheap 2-opt pass per colour layer would cut travel on every plate.
