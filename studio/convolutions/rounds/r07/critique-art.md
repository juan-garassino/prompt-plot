# Art critique — convolutions r07 · canon: Pop / Ben-Day (Lichtenstein, *Modern Painting*) · 2026-09-29
render: gallery/studio/convolutions/trials/pp_convolutions_iterate_v30.png  (gcode measured: gallery/studio/convolutions/trials/pp_convolutions_iterate_v30.gcode, 895 pen-downs, re-rendered at 16–30 px/mm with a 0.30 mm nib for the detail crops)

## Scores
| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 7 | At 3 m the order is now right. The card (1.05 mm fused) comes first. The blue stem column (107.6, 64/78/93) and the left-arm targets (50,150) and (78.8,136) come second. The wing has dropped to a ~14 % grey ground. What holds it at 7 is the Pop canon's rule that outlines must dominate: the X keyline is 0.60 mm, which at 3 m weighs the same as the stripe field's hairlines and the doubled rings (0.55). So the figure reads as a drawn diagram outline, not a Lichtenstein contour. The crimson pen is also spread across ~40 small marks, so it is not a scarce, loud accent. |
| 2 | grid & alignment | 8 | The lattice is strict. The staircase vertices sit on cell lines, and the last riser stops at (197.6, 24.2). The title's and every key icon's left ink edge share x ≈ 204.8. The key text column is at 215.8. The key baselines sit on lattice rows 2–9, and the title sits on row 0. The riser-to-title gap is 7.2 mm. Clean. |
| 3 | tension & asymmetry | 8 | Two diagonals cross at the card: the staircase falls left-to-right, and the wing rises and bleeds off the top and right crop. The card sits off-centre on the fork, and the round left-arm lobe counterweights it. This is still the plate's best quality. |
| 4 | negative space | 7 | Both quiet zones are now shaped. The keyline bounds the lower-left as X's outside, and the lower-right is a wedge beyond the last riser with bare paper above the key. The residue is the crimson rim rings that sit alone on bare paper and read as strays, not decisions. (35.6, 179.0) floats 10 mm above the arm beside the first riser. (151.2, 63.8) sits 14 mm off the stem, inside the quiet zone. (78.8, 35.0) and (136.4, 35.0) sit below the foot. The two clipped C-arcs at (64.4, 107) and (35.6, 121) read as broken glyphs at 1 m. |
| 5 | craft for pen | 7 | 3 pens, one swap each. Wing lens tips are ≥ 0.86 mm, collar-to-dot gaps are ≥ 0.62 mm, dot-to-keyline gaps are ≥ 0.93 mm, and ring-to-keyline gaps are ≥ 0.85 mm. The keyline passes sit 0.30 mm apart and fuse. Defects: (a) 8 stripe tips stop 0.55 mm (ink to ink) short of the staircase, which is a near-miss below the 0.8 floor, neither butted nor clear: (140.9,105.1) (135.1,111.5) (68.9,171.4) (73.6,169.1) (83.3,161.9) (97.7,151.6) (97.7,147.4) (97.7,143.1). (b) The dots at (100.4 / 107.6 / 114.8, 99.8) are 0.63 mm off the card's shadow hatch. (c) An orphan 4.5 mm stripe stub is trapped alone in the riser pocket at (68.9–73.6, 169–171.4). (d) Each title glyph segment is its own 3-pass band, so chamfers overlap the stems at every corner (e.g. C at 242.6–243.1, 21.6–22.0), giving double-inked knots about 0.8 mm across. (e) Travel is 5.47 m against 12.66 m of draw, which is engine-blocked (A19). |
| 6 | concept legibility | 7 | Not a schematic, and not a figure. The abstract order reads: one shape, a front that has swept part of it, targets left behind on the read side, and an untouched striped field ahead. The one Y now reads (A21). Against that, the 8-row prose key sits in the lower-right like a figure caption. It is the rubric's "measured caption" failure mode in miniature. The Lichtenstein lineage is honest in vocabulary, but it would not hold beside the work: in *Modern Painting* the black keyline is the loudest thing on the canvas. |
| 7 | depth & dimensionality | 7 | Declared flat (Pop), with one lifted plane. The 3.2 mm hatched shadow makes the card read as lifted at 1 m, and stripes stop cleanly at x 130.6 on its right. Nothing else claims depth, which is correct for the canon but earns no more than the floor. |

**avg 7.29 · min 7 · VERDICT: FAIL** (avg < 8)

## Reads at a glance
At 3 m: one rounded Y outlined in black, dotted and stamped with blue and red targets below a staircase, with a heavy black square at its fork, and its upper arm turning into a pale field of stripes that runs off the top-right corner.

## Acceptance checks
Encoding §11 (measured on the gcode):
1. **One X (A21): PASS.** The keyline is two polylines of 583.4 / 583.1 mm. Their only ends are at (284.0, 152.9 / 153.2) and (165.5 / 166.0, 197.0), both on the crop. The pass offset is 0.30 mm at the median and 0.306 at p95. At a 25 % thumbnail one Y traces from the stem foot round the left arm and out along the wing. No black contour ends at a riser.
2. **Output outranks input (A22): PASS.** Exactly 5 doubled outer rings, at the §4 coordinates. Stripe ink is ≈ 5.4 m (≤ 6). Stripe spacing is 2.25–2.39 mm vertical at x = 250 on ~20° slopes, so ≈ 2.1–2.2 perpendicular; the exact ±0.05 check is left to the science critic. The card keyline (1.05 mm) is the only LINE > 0.60 mm. Note: the title's glyph bands ink 0.80 mm. They are type, not line, but name it. At 25 %, the blue chain reads second to the card.
3. **Dots tell the truth (S10): PASS (structural).** 180 lattice dots are drawn, inked Ø 0.54–2.56 mm (max 2.56 as specified). Dot-to-keyline ink is ≥ 0.93 mm. The ±20 % area-vs-x check and Y recomputed from the ink are left to the science critic.
4. **Grid (A23): PASS.** The last riser ends at (197.6, 24.2), with no black ink below 24.2 except the title. The title's left edge is 204.95 at centreline (ink ≈ 204.8), and its baseline is on 20.6 (lowest centreline 20.35 in the O/C overshoot). Key rows sit on 35.0 … 85.4. The riser-to-title gap is 7.2 mm.
5. **Key exact, not grown (S11): PASS.** The 8 rows are verbatim to §5. The block spans x 204.95–275.13 and y 34.1–87.6. No formula line. Wing lens tips are ≥ 0.86 mm (A24). Card geometry is unchanged. Collar ∝ |w| is left to the science critic.

AUTHORING §6 (the reference is judged as an interpretation). It is a free Pop transposition: the reference's contour-striped blob X and its kernel square survive as the stripe field and the card. It is not a trace.
1. Main forms recognisable without colour: **PASS**. The Y keyline, the card and the staircase all read in black alone.
2. Shadow lines follow the surface: **PASS**. There is one 45° hatch, on the card only.
3. Fine lines that are two sides of one thick stroke: **PASS**. The keyline passes (0.30) and title passes (0.25) fuse.
4. Blackest regions intended: **PASS**. They are the card keyline and the stem's largest dots.
5. Labels readable at real pen width: **PASS**. 2.2 mm cap, rows ≤ 59.3 mm wide.
6. Thick-pen knots: **PARTIAL**. The title corners are double-inked where per-segment bands overlap.
7. Long travels or pointless tiny marks: **FAIL**. Travel is 43 % of draw. Crimson hops 142 mm and blue hops 179 mm, because the key swatches are still drawn mid-layer. The orphan 4.5 mm stripe stub adds nothing. Engine-blocked (A19).

## Biggest weakness
The Pop canon's first law is unmet: **the outline does not dominate.** The X keyline is correct and continuous now, but at 0.60 mm it carries the same visual weight as the doubled rings (0.55) and the stripe hairlines. At gallery distance the plate reads as a precise dot diagram with a legend, not as a Lichtenstein, where the black contour is the loudest mark after nothing. Everything else is aligned and truthful. Only weight separates it from the canon it claims.

## Mandates
1. **Pop keyline weight (needs an encoding amendment to §4/§9/§11.2, flagged to the translator).** Draw the X keyline in 3 passes (0, +0.30, +0.60 mm outward), fused to ≈ 0.90 mm. Raise the card keyline to 5 passes (≈ 1.30 mm) so the card stays the heaviest line. Test: the stroke-width ladder on the sheet is card 1.30 > keyline 0.90 > doubled ring 0.55 > everything else 0.30. At a 25 % thumbnail the Y outline is the darkest continuous line after the card. No dot or ring comes within 0.8 mm of the new outer pass: re-clip against the widened ink.
2. **Close or clear every near-miss.** The 8 stripe tips listed in dim 5(a) (now 0.55 mm ink-to-ink from the staircase) either butt the staircase at 0.00 or stop ≥ 0.80 mm clear. Pick one rule and apply it to all 8. Trim the card's shadow-hatch lines, not the dots, so that the dots at (100.4 / 107.6 / 114.8, 99.8) are ≥ 0.80 mm off hatch ink (now 0.63). Drop the isolated 4.5 mm stripe stub at (68.9–73.6, 169.1–171.4). Test: min ink gap over staircase tips, hatch-to-dot pairs and stripe tips ≥ 0.80 mm or exactly 0, and no black stripe piece < 6 mm.
3. **Title joins without knots.** Draw each glyph's connected strokes (e.g. the C's stem plus its two chamfers plus two arms) as ONE continuous 3-pass band path instead of per-segment bands. Test: no point of the title is covered by two different bands' passes (today every chamfer corner is double-inked, e.g. C at x 242.6–243.1, y 21.6–22.0). Pen-downs for the title fall from 60 to roughly one per glyph stroke chain.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| A16 | PARTIAL | The lower-left is now bounded as X's outside by the keyline, so it reads as a shaped zone, not residue. The key sits in the wedge's lower part with bare paper above (y 92–120). Residue: lone crimson rim rings at (35.6,179), (151.2,63.8), (78.8,35) and (136.4,35) still read as strays. |
| A18 | FIXED | The collar-to-dot ink gap is 0.62–1.58 mm on all 32 collar strokes inside the card (≥ 0.60). |
| A19 | NOT FIXED (engine-blocked, accepted) | Order crimson → blue → black holds. Crimson hops 142 mm and blue 179 mm to the key swatches mid-layer. Total travel 5.47 m. |
| A21 | FIXED | One 2-pass keyline, 583 mm per pass, ends only on the crop at (284, 153) and (166, 197). It crosses the staircase unbroken, and a 25 % thumbnail traces one Y. |
| A22 | FIXED | 5 doubled outer rings at the §4 coordinates. Stripe ink went from 10.96 to ≈ 5.4 m, and the wing reads as ground. The blue chain is second to the card at 25 %. (The residual hierarchy gap is the keyline weight, which is the new mandate 1.) |
| A23 | FIXED | The riser ends at (197.6, 24.2). The title and key sit on lattice rows, on axis x ≈ 204.8, with a 7.2 mm riser gap. |
| A24 | FIXED | The whorl-eye and all wing tip-to-stripe gaps are ≥ 0.86 mm ink. There is no lens contact. |

DESCRIPTION.md § Keep (the r01 bar):
- Contour discipline, min gap ≥ 0.86: **PARTIAL**. The wing itself holds (≥ 0.86), but the staircase tips (0.55) and the hatch-to-dot gaps (0.63) break it. See mandate 2.
- Depth by clipping, not collision: **HOLDS**. Rings are clipped to Cs off the keyline at 0.85 mm, and field marks stop at the card band.
- One axis ties zones: **HOLDS** in this order's terms (x 204.8 carries the riser offset, the icons and the title).
- Colour as a sequence, two bookend blobs, receptive-field cone, 14 mm gutter, equal gutters: **N/A**. These belong to r01's triptych layout, which this order replaced by design (A1).

## Regressions vs compare-to
- vs r05 (`pp_convolutions_iterate_v20.png`): **no regression in composition, grid or science marks.** One mild loss: the nib-corrected dots are smaller, so the Ben-Day lattice mass on the read side is lighter at 3 m (inked max is unchanged at 2.56, but the mid-tones shrank). It is correct, and it slightly weakens the "dot screen" read. Keep it: truth wins.
- The stripe-tip near-misses at the staircase (0.55 mm) were not measured in r05, so they cannot be called new. They breach the r01 Keep bar either way (mandate 2).
- vs r01 benchmark: r07 is the first round in this order where the figure is one continuous contour, which is the r01 quality most often lost. It is restored.
