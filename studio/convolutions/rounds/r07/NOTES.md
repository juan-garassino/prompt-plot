# convolutions r07 — iterate · parent: r05 · 2026-09-29

Encoding: `studio/convolutions/encoding.md` v1. It was written by the translator pass
(05:06, before this designer run). It codifies r05's wavefront-lattice order, so this round
is round 5 of 5 on that line, and a vote is forced after it.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/convolutions/rounds/r07/piece.py \
  --fn convolutions_onex --seed 7 --paper a4 --orientation landscape \
  --palette crimson,dodgerblue,black \
  --out gallery/studio/convolutions/trials/pp_convolutions_iterate_v30.png
```

- final PNG: `gallery/studio/convolutions/trials/pp_convolutions_iterate_v30.png`
- final GCODE: `gallery/studio/convolutions/trials/pp_convolutions_iterate_v30.gcode`
- seed 7. The piece draws no random numbers. The gcode bodies for seeds 3, 7 and 11 are
  byte-identical (`v30_s3`, `v30_s11`; body md5 `bbd34950…`).
- Provenance: this round directory already held a `piece.py` from an interrupted run of
  this same dispatch, with renders v24–v26 and no NOTES. That run had already built the
  one-keyline, the 2.1 mm stripes, the S10 dots, the doubled outer rings, the A23 grid and
  the rewritten key. I re-rendered it unchanged as v27 (gcode body identical to v26),
  measured it against encoding §11, and iterated from there:
  - v28: the wing's stripe guardrail was raised to a 1.15 mm centreline floor, and a local
    tip trim was added. The engine guardrail had left a 0.80 mm lens at the whorl eye
    (229, 183) and 0.87 mm lenses at chevron tips, because its lookback counter runs across
    strokes, so an arm chained tip-to-tip onto its partner is exempt.
  - v29: the tip trim also eats the chevron apex left as a hook on the end of an arm.
    There were 7 of these, with a self-gap down to 0.67 mm at (186, 161).
  - v30: the collar gauge scale is pinned at the encoding's a0 = 19.285 mm²/|w|. The
    smaller S10 dots had let the computed maximum drift to 19.516.

## Mandate responses

| id | mandate | status |
|---|---|---|
| A16 | Heart/quadrant; crop; no empty > 80×80; one axis. Residue: lower-left reads as leftover, key fills the quiet zone | FIXED (residue). The lower-left (x 17–80, y 17–100) is now bounded by the keyline's stem foot and left-arm underside, so it reads as X's outside (x = 0 paper). It carries only the crimson rim rings, which are real y > 0 responses on x = 0 samples. The key occupies the lower part of the quiet zone beyond the last riser; above it, y ≈ 92–150 is bare paper up to the wing's lower flank. |
| A18 | Collars: ≥ 0.60 mm paper to the ink edge on all 25 taps | FIXED. COLLAR_PAPER = 0.63. Measured inner-pass ink edge to dot ink edge = 0.630 mm on all 25 taps. Ink = 19.285·\|w\| mm², with 0.00 % error on all 25 taps in the polyline model. Crimson = blue = 40.878 mm². |
| A19 | Order crimson → blue → black; swatches last; max hop < 120 mm | ARGUED (engine-blocked, as the SYNTH rules). The order crimson → dodgerblue → black is held. The in-layer max hops between consecutive strokes of one pen are **crimson 118.6 mm (212,61 → 122,138), blue 179.3 mm (52,165 → 207,74), black 136.2 mm (216,35 → 284,153)**. Black rose from 104.7 because the greedy tour now leaves the key text for the keyline's pass-2 start on the right crop. `reorder_by_color` re-chains from (0,0). No piece-side re-orderer was added (encoding §9). |
| A21 | One X, one keyline, no break at any riser | FIXED. The x = 0 contour is ONE open polyline per pass (2 passes, 583.1 and 583.4 mm). Pass 1 runs from the top crop (166.0, 197.0) round the left arm, down the stem, round the foot (107.5, 27.8), up the stem's right flank and out along the wing to the right crop (284.0, 153.2). Pass 2 is 0.30 mm outward and runs back. `keyline_passes` raises if the crop ever yields more than one piece. It crosses the staircase at (80.3, 168.2) and (141.5, 96.8) unbroken. No black contour ends at a riser. The rings give way to it: 3 rings are clipped to Cs at ≥ 0.85 mm ink-to-ink ((2,5) +2, (0,6) +1 and the grazes), and none is deleted. |
| A22 | Output outranks input: doubled outer rings for \|bin\| ≥ 3; wing to ground; weight order | FIXED (measured; the thumbnail call is the critic's). All 5 visible \|bin\| ≥ 3 responses get a +0.25 mm outer pass: (107.6, 63.8) −4, (107.6, 78.2) −3, (107.6, 92.6) −3, (78.8, 135.8) −3, (50.0, 150.2) −4. (5,5) −3 is under the card. Stripes 10.96 m → **5.18 m** (≤ 6 m target), perpendicular pitch median 2.098 mm. Ink per element in the §7 weight order: card keyline 0.59 m (1.05 mm line) + hatch 0.22 m · Y response rings 0.94 m (+ collars 0.27 m) · X keyline 1.17 m (0.60 mm) · dots 2.07 m (180 solid marks) · stripes 5.18 m (0.30 mm hairlines, 14 % tone). Lines wider than 0.60 mm: the card keyline (1.05) and the title glyphs (0.5 weight + nib = 0.8, specified by encoding §5); no field line. |
| A23 | Last riser at the lowest lattice row; title and key baselines on rows; ≥ 7.2 mm riser → title | FIXED. The last riser ends at (197.6, 24.20), with no staircase ink below 24.2. The title baseline is at 20.6 (row 0); its ink spans x 204.80–277.00, y 20.20–28.17, cap 7.17 mm (set from the width). Key baselines are at 35.0, 42.2, 49.4, 56.6, 63.8, 71.0, 78.2 and 85.4 (rows 2–9, exact). Every icon's left ink edge is at 204.80 (±0.01), the text column is 215.6, and riser → title/icon ink = 7.2 mm. |
| A24 | No stripe lens with tip contact < 0.8 mm | FIXED. There are 0 stripe samples within 1.10 mm centreline of another stripe (≥ 0.8 mm bare paper). The min is 1.163 mm, at (199.0, 167.7). The whorl eye (229, 183) is now 1.16 or more; it was 0.80 in v27. The self-gap of any stripe to itself (> 3 mm back along the line) is ≥ 2.10 mm, so no chevron hooks remain. |
| S5 | No encoding.md | FIXED (translator pass). `encoding.md` v1 exists and this round follows it. Deviations are listed under Measurements. |
| S9 | The card hides 3 outputs | ARGUED, accepted in r05. It is declared in HANDOFF as omission (b). Not keyed. |
| S10 | Dot ink area ∝ x | FIXED. 180 dots, for x ≥ 1.5 mm (36 samples at x ≤ 1.16 mm dropped; the next sample up is x = 1.62). Centreline Ø 0.233–2.260 mm, inked Ø = centreline + 0.30. Inked area / (π(2.56/2)²·x/37.261) − 1 = **0.00 %** on all 180 in the disc model; the ±20 % budget is left entirely to the plotter. Y recomputed from the inked areas (floor included) gives **66/66 signed bins** (63 visible + 3 under the card). Dot ink is ≥ 0.925 mm from keyline ink. |
| S11 | The key names every mark and states the finding exactly | FIXED. 8 rows, verbatim encoding §5: `X  dot area = depth in keyline · none < 1.5 mm` · `stripes: X not yet read · one line per 2.1 mm` · `K  card: 5×5 LoG, stride 2 · collar ink = \|w\|` · `staircase: edge of the 66 windows read so far` · `Y = K ∗ X · 1-4 rings by \|y\| · none < max/8` · `blank  X straight (flat or constant slope)` · `crimson  X bends up (where it starts)` · `blue  X bends down (ridge and tip)`. The block's ink sits in x 204.8–277.0, y 33.9–87.8, inside the r05 footprint. It did not grow, and it has no formula line. |
| W1–W3 | *Bacterio* flavour backlog | DEFERRED. That flavour is not continued (SYNTH). |

## What changed from parent

1. **X became one figure.** In r05 the x = 0 outline existed only on the unread wing, so the
   read side was a free-floating dot blob and the plate read as two objects. Now one black
   keyline draws the whole capsule-Y (left arm, stem, foot and wing) and crosses the
   staircase unbroken. The dots, the rings and the stripes all sit inside one silhouette.
   The crimson rim rings sit just outside it, where the kernel's positive ring reaches X's
   edge.
2. **The wing became ground.** It has half the stripes (every second level, 2.1 mm) and
   5.2 m of ink instead of 11. With the chevron hooks and lenses opened, it reads as a 14 %
   field running out of the frame, not as the headline.
3. **Y came forward.** The five strongest responses carry a fused 0.55 mm outer ring, so the
   blue spine of the stem (63.8 → 78.2 → 92.6) and the left-arm pair (78.8, 135.8) and
   (50.0, 150.2) read as a chain of targets leading to the card.
4. **Housekeeping to the grid.** The last riser stops at row 0's top line. The title and the
   key stand on lattice rows, on column line 26, one cell right of the riser. The key names
   the stripes and the staircase and states the three-way finding.

Kept exactly: the lattice, crop, K, stride, read set, card (keyline, hatch, band), collar
rule (a0 = 19.285), ring radii and pitch, pens and layer order.

## Measurements / computations

- **Model** (unchanged from r05):
  - max\|y\| over read nodes = 18.731, pmax = 37.261 mm;
  - read bins −4:2 · −3:4 · −2:4 · −1:7 · 0:27 · +1:21 · +2:1;
  - K Σ = 0.
- **Keyline:** 2 × 583 mm, and the only endpoints are on the crop.
  - Stripe ink is ≥ 1.79 mm from keyline ink.
  - Ring ink is ≥ 0.849 mm from keyline ink (the (2,5) C at 66.3, 106.6).
  - Ring ink is ≥ 13.8 mm from the staircase.
- **Stripes:** 51 strokes, 5.18 m.
  - Nearest other stripe: min 1.167, p1 1.607, median 2.098 mm.
  - The engine guardrail runs at 1.15 mm centreline (resample 0.25, short_exempt 3). Then
    `_trim_tips` pulls ends back 0.2 mm per round, both partners of a lens in the same round,
    until each end is ≥ 1.15 mm from other stripes and from its own line more than 2.3 mm
    back. Douglas-Peucker at 0.01 mm then drops the working points again. This took the
    commands from 50,270 to 29,134.
- **Dots:** see S10. The spiral pitch is ≤ 0.20 mm (≤ nib), so every dot inks solid.
- **Collars:** a0 = 19.285 (the fit limit is 19.516). The 25 taps are ∝ \|w\| exactly in the
  model, and the dot-to-collar paper is 0.630 mm.
- **Deviations from encoding.md v1, declared:**
  - (1) Title cap height is 7.17 mm, not ≈ 6.6, because it follows from the 204.8–277.0
    width as §5 prescribes.
  - (2) Black pen-downs are 795, not ≈ 620. The longer, exact key rows add glyph strokes:
    key + title = 1.97 m of ink.
  - (3) Black time is 47.2 min, not ≈ 43, for the same reason.

## Plot budget

| | |
|---|---|
| draw | 12.65 m (crimson 0.50 · blue 0.85 · black 11.30), r05 17.13 |
| travel | 5.47 m (crimson 0.97 · blue 0.66 · black 3.75) |
| commands | 29,134 (r05 74,381) |
| pen-downs | crimson 49 · blue 51 · black 795 |
| max in-layer hop | crimson 118.6 · blue 179.3 · black 136.2 mm (engine-blocked, A19) |
| pens | 3, streamed crimson → dodgerblue → black (2 swaps) |
| est. time (Leo: F600 draw, F2000 travel, 1 s dwell per lift and drop) | **crimson 3.0 min · blue 3.5 min · black 47.2 min · total ≈ 54 min** |
| scorer | grade A (composition 0.937, efficiency 0.797) |

## Self-critique (rubric)

| dimension | score | notes |
|---|---|---|
| Hierarchy | 7 | Card > blue target chain > keyline > dots > stripes holds in ink and in line weight. At thumbnail the wing is still the largest textured area. It is ground by tone but not by area, so the critic may still see it as co-equal with the target chain. |
| Grid & alignment | 8 | Everything is on the 7.2 mm lattice: riser end, title baseline, 8 key baselines and the 204.8 axis, all measured exact. |
| Tension | 8 | Same two opposed diagonals (staircase ↘, wing ↗) with the card at the crossing, both bleeding off the frame. |
| Negative space | 7 | The lower-left is now X's outside, bounded by the keyline, and the upper-middle is bare. The lower-right holds the key under ~60 mm of paper. |
| Craft for pen | 8 | ≥ 0.8 mm bare paper everywhere in the field, no hooks, no crumbs < 3 mm. Clipped rings stay Cs, and the collars have 0.63 mm clearance. Blue's 179 mm hop remains (engine). |
| Concept legibility | 7 | One Y, read below-left of the staircase into targets on its spine and rim and left blank in its interior; the key states the finding exactly. The rim rings outside the keyline need the key to be understood. |
| Depth | 7 | Flat plus one lifted card, as r05. |

**Single worst thing:** the unread wing is still the largest mass on the sheet by area.
Halving its ink made it ground in tone, but its 200 × 100 mm footprint still competes with the
target chain at thumbnail. The encoding forbids thinning it further except to the 3.15 mm
fallback, and I did not take the fallback because §11.2 passes numerically (5.18 m ≤ 6 m).
Minor: a 5.6 mm stripe fragment of the unread left-arm sliver at (69–74, 167–170) reads as a
stray tick between the riser and the keyline.

## Engine requests

- `policies.enforce_line_spacing`: the `lookback` exemption compares a global point counter,
  so the first ~3·min_dist of a stroke is exempt against the tail of the PREVIOUS stroke.
  Chevron arms chained tip-to-tip keep sub-floor lenses (0.80–0.87 mm here). The counter
  should reset per stroke. Worked around locally with `_trim_tips`.
- `postprocess.reorder_by_color`: honour authored order or add 2-opt with stroke reversal
  (A19; carried from r05).
