# convolutions — encoding (VISUAL TRANSLATOR) · Status: encoding v1 · 2026-09-29

Input: there is no `dossier.md` for this slug. The truths come from `DESCRIPTION.md`, the r05
HANDOFF `rule:` line and the science critic's r05 check table. Every number below was
recomputed on 2026-09-29 from `rounds/r05/piece.py::build_model((10,10,287,200))`.

This file **codifies r05's wavefront-lattice order**. It is a specification of the working
encoding, not a Revision, so the designer-round count on this line stays at 4 of 5.
r07 (parent r05) is the last round, and a vote is forced after it. Nothing in the order,
lattice, kernel, stride, read set, card, crop or pen set changes here. This file only settles
the channel questions the r05 critics left open (A21, A22, A23, S10, S11).

---

## 1. STYLE assignment

**POP / Ben-Day (STYLES §4)**, lineage Roy Lichtenstein, *Modern Painting* series (1966–70).
Why the order fits: Pop's whole vocabulary is a strict dot lattice with dot area as tone,
fields of parallel stripes, and one fat black keyline. A sampled convolution uses exactly
three things: a lattice of samples, a continuous field, and one operator. So each Pop mark
carries one of them:
- **dots** = X read on the lattice (the read samples);
- **stripes** = X as a continuous field, not yet read;
- **keylines** = the operator's card (the heaviest line) and X's own edge (one figure line).

Declared deviations from the canon:
- **3 pens, not 4.** No yellow, because yellow would carry nothing.
- **Stripes follow X's level sets.** They are not rigid Lichtenstein parallels, because the
  stripes ARE X's isolines.

## 2. The one-glance statement

**At 3 m: one Y-shaped figure, drawn by one black outline. A heavy black card sits at its
fork. Below and left of a staircase, the figure has been converted into chains of coloured
targets. Above and right of it, the figure is still a pale field of stripes running out of
the frame.**

At 1 m you see that the targets sit only on the Y's spine and rim, while its broad
interior stayed blank. At 30 cm you see that the card's collars are gauges and that the dot
sizes are the same field as the stripes.

## 3. The abstract ORDER

**ORDER: one lattice crossed by one travelling front.** A single sampled field is swept by a
window. The staircase is the frontier between the part of the field that has been read and
the part that has not.

Exact mapping, one line each:
- **Position on the lattice = position in X.** 37×25 samples at 7.2 mm.
- **Behind the staircase = read. Ahead of it = unread.** Read windows are those with
  i + j ≤ 10.
- **Colour appears only where a window has been read.** Rings mark Y = K∗X, placed on the
  node's own input sample.
- **One outline = X's x = 0 edge**, the same line on both sides of the front.

## 4. Channel mapping

Lattice: the input cell is 7.2 mm. Sample centres sit at x = 21.2 + 7.2c, y = 20.6 + 7.2r
(c 0–36, r 0–24). The lattice box is (17.6, 17.0)–(284.0, 197.0), and its top and right
edges are the crop line. Output node (i, j) is centred on input (2i+2, 2j+2), at
**(35.6 + 14.4i, 35.0 + 14.4j)**.

| quantity | channel | exact rule |
|---|---|---|
| **x = X**, the depth inside X's outline in mm (cell mean of the exact distance field, 6×6 quadrature, \|∇d\| = 1) | **dot INK area** (read side) | Inked Ø = D·√(x/x_max), with D = 2.56 mm and x_max = 37.26 mm (the largest shown x). **Centreline Ø = D·√(x/x_max) − 0.30** (the nib). Each dot is one pen-down: a spiral at ≤ 0.25 mm pitch plus a rim, so it inks solid. **No dot for x < 1.5 mm** (4 % of max). This drops 36 of the 216 samples with x > 0, and all 36 have x ≤ 1.16 mm. The 180 drawn dots have x ≥ 1.62 mm and a centreline Ø from 0.23 to 2.26 mm (the largest dot is unchanged from r05). The threshold is the dot's zero code and is keyed. It also keeps every dot ≥ 0.8 mm off the keyline (measured: 12 sub-floor dots would otherwise graze or touch it) |
| x, unread (ahead of the front) | **stripes**: level sets of d | Levels **d = k · Δd, Δd = 2.1 mm** (every second r05 level), k ≥ 1. Because \|∇d\| = 1, the stripes are also 2.1 mm apart on paper. Single pass, 0.30 mm, the finest mark on the sheet. Tone ≈ 0.30 / 2.1 = 14 % (r05 was 28 %). **Only allowed fallback:** Δd = 3.15 mm (every third level), and only if check 11.2 fails; the key text then changes to match. Nothing in between |
| X's edge, x = 0 | **the keyline**: ONE open polyline, black, 2 passes | Pass 1 exactly on d = 0. Pass 2 offset **0.30 mm outward**, onto the x = 0 paper, so ink never covers X's interior. The line is about 0.60 mm wide. It is continuous from where it leaves the **top crop (x ≈ 166, y 197)**: round the left arm, down the stem, round the stem foot **(107.5, 27.8)**, up the stem's other flank, and out along the wing's lower flank to where it leaves the **right crop (x 284, y ≈ 153)**. It is about 581 mm per pass. It **crosses the staircase without a break**. It has exactly two ends, both on the crop |
| Y = K∗X, valid, stride 2, 17×11 | **ring count** | Count = rint(4\|y\| / max\|y\|), with max over the read nodes = 18.731. Rings are centred on the node's sample at r = 1.98 + k·1.02 mm (k = 0…3), single pass. **The outermost ring of every node with \|bin\| ≥ 3 gets a 2nd pass at +0.25 mm outward**, which fuses into one 0.55 mm line. There are 5 such nodes on the sheet: (107.6, 63.8) −4 · (107.6, 78.2) −3 · (107.6, 92.6) −3 · (78.8, 135.8) −3 · (50.0, 150.2) −4. (5,5) is −3 but lies under the card. **No ring: \|y\| < max\|y\|/8** |
| sign of y | **pen** | crimson = y > 0 (X bends up) · dodgerblue = y < 0 (X bends down) |
| K = 5×5 LoG, σ = 1 cell, zero-sum | **collars** round the 25 head-window samples | Ink area = 19.285 mm² · \|w\|: full passes at 0.32 mm pitch, then one clockwise arc from 12 o'clock carrying the remainder. Crimson +, blue −. The inner pass's ink edge is ≥ 0.60 mm off the dot's ink (the dot is now smaller, so the collar moves in with it) |
| where the kernel is now: head node (5,6) | **the card** | Window x 89.6–125.6, y 103.4–139.4. The keyline is 4 passes at 0.25 mm, fused to 1.05 mm (the heaviest line). A 3.2 mm shadow band on the right and bottom only, hatched at a falling 45° with 0.9 mm pitch. Field marks stop at the band. It hides outputs (4,5) 0, (5,5) −3, (4,6) −2 (declared in HANDOFF, not keyed) |
| read set, i + j ≤ 10 (66 windows) | **the staircase**: one black pass | The union boundary on cell lines, vertices exact to 0.01 mm: (53.6, 197.0) → … → (197.6, 53.0) → **(197.6, 24.2)**. The last riser **stops at y = 24.2**, the top line of lattice row 0. Row 0 carries x = 0 across its whole width (measured max 0.0), so the omitted 7.2 mm borders only blank paper on both sides. This is declared in §9a |

Nothing else is drawn. There is no scatter, no bracket, no plus mark, no arrow, no swatch
bar, and no ∇²X formula.

### 4b. Check numbers (for the science critic)

| quantity | value |
|---|---|
| output grid | (37−5)/2+1 × (25−5)/2+1 = **17 × 11** |
| read windows | **66** = 37 ring nodes + 26 blank + 3 under the card |
| kernel | centre −0.9813 · ortho −0.2846 · (±2,0) +0.1540 · (±2,±1) +0.1418 · corner +0.0736 · diagonal +0.0187 · Σw = 0 · 5 negative, 20 positive |
| collar ink | ∝ \|w\| within 0.4 % on 25/25 taps. Crimson ink = blue ink within 0.1 % |
| read-node bins | −4: 2 · −3: 4 · −2: 4 · −1: 7 · 0: 27 · +1: 21 · +2: 1 |
| Y recomputed from **inked** dot areas (this rule, floor included) | **66/66 bins exact** (63 visible + 3 under the card). Computed 2026-09-29 |
| dot ink error | 0 % in the disc model, so the budget is plotting error. Must be within ±20 % on all 180 drawn dots |
| dropped samples | 36, all x ≤ 1.16 mm (≤ 3.11 %). The next sample up is x = 1.62 mm |
| stripe pitch | 2.10 mm perpendicular (±0.05) |
| X area in crop | 21,277 mm²: read 9,541 · unread 11,736 |

## 5. Composition sketch

- **Paper and drawable area:** A4 landscape, cream. Drawable area 10–287 × 10–200. The crop
  line is 3 mm inside it: x 13–284, y 13–197.
- **Dominant mass: the X figure inside its keyline**, 21,277 mm². That is **13.7 : 1** over
  the card with its shadow (≈ 1,550 mm²).
  - The figure's loudest part is the **read** half: the stem column x ≈ 74–141 and the
    left arm up to y ≈ 178, carrying the target chains.
  - The unread wing (x 83–284, y 97–197) is **ground**: 14 % tone, running out through the
    top-right.
- **Accent: the card at the fork** (89.6–125.6 × 103.4–139.4). This is where the staircase
  (descending top-left → bottom-right) crosses the wing (ascending card → top-right). Both
  diagonals bleed off the frame.
- **Quiet zone 1 (shaped): the lower right** beyond the last riser, x 197.6–284 by
  y 17–~120 up to the wing's lower flank. The key and title stand in its lower part on one
  axis. Above the key (y ≈ 92–120) is bare paper.
- **Quiet zone 2 (shaped): the lower left**, outside the keyline. The stem foot and the left
  arm now bound it as X's outside (x = 0 paper). The only marks there are the crimson rim
  rings, which sit outside the keyline because the kernel's positive ring reaches X's edge.
- **Type axis: x = 204.8**, column line 26, exactly 7.2 mm right of the last riser at
  197.6. Every key icon's left ink edge and the title's left ink edge sit on it (±0.3).
  The key text column is **x = 215.6**, the centre of column 27. Nothing inks past x = 277.
- **Title:** `CONVOLUTIONS`, baseline **y 20.6** (row 0), from x 204.8 to 277.0. The cap
  height follows from that width (≈ 6.6 mm). Each glyph segment is its own serpentine band
  (0.5 mm weight, 3 passes, one pen-down per segment).
- **Key:** 8 lines, one per lattice row. Baselines are at rows 2…9 = **y 35.0, 42.2, 49.4,
  56.6, 63.8, 71.0, 78.2, 85.4** (±0.3). Cap height 2.2 mm, proportional stroke text. Each
  icon's vertical centre is at baseline + 1.1. Row 1 (27.8) stays empty, between the title
  and the key. The block (y 34–91) occupies the same box as r05's (34.3–88.5). It does not
  grow.

  | row (baseline y) | icon (left ink edge on 204.8) | text, exactly |
  |---|---|---|
  | 9 (85.4) | three black dots, x = 0.1 / 0.4 / 1.0 of max | `X  dot area = depth in keyline · none < 1.5 mm` |
  | 8 (78.2) | three horizontal 6 mm black strokes, 2.1 mm apart (vertical extent ±2.25) | `stripes: X not yet read · one line per 2.1 mm` |
  | 7 (71.0) | blue collar gauge round a black dot (as r05) | `K  card: 5×5 LoG, stride 2 · collar ink = \|w\|` |
  | 6 (63.8) | a 2-step black stair, 3 mm treads | `staircase: edge of the 66 windows read so far` |
  | 5 (56.6) | crimson rings round a dot, 3 rings with the outer one doubled (r ≤ 4.47 ink) | `Y = K ∗ X · 1-4 rings by \|y\| · none < max/8` |
  | 4 (49.4) | a lone small black dot, no ring | `blank  X straight (flat or constant slope)` |
  | 3 (42.2) | crimson ring round a dot | `crimson  X bends up (where it starts)` |
  | 2 (35.0) | blue ring round a dot | `blue  X bends down (ridge and tip)` |

  - **Row order:** the large Y icon (±4.47) sits between the small stair (±1.5) and blank
    (±0.5) icons, so every pair of icons is ≥ 0.8 mm apart at a 7.2 mm row pitch.
    Measured text widths (proportional, 2.2 mm cap) are ≤ 60.2 mm against the 61.4 mm
    available.
  - **Wording:** `none < 1.5 mm` is exact, because a dot is drawn iff x ≥ 1.5 mm.
    `one line per 2.1 mm` holds both on paper and in depth, because \|∇d\| = 1.

## 6. Pen budget: 3 pens, streamed in index order

| pen | MEANING | carries |
|---|---|---|
| 0 **crimson** | y > 0: X bends up | positive response rings, positive collars, key icons rows 5 and 3 |
| 1 **dodgerblue** | y < 0: X bends down | negative response rings, negative collars, key icons rows 7 and 2 |
| 2 **black** | X itself, plus the operator's frame | dots, stripes, keyline, staircase, card keyline + hatch, **text layer** |

- **Order:** crimson → dodgerblue → black, so black never lands under wet colour.
- **Text layer:** text is its own stroke group, emitted last in the black layer. It shares
  the black pen because Pop's budget carries no separate text ink. No halos are needed,
  because every key and title glyph stands on x = 0 paper in quiet zone 1. Declared.

## 7. Expressive levers, one decision each

- **Weight order (the A22 decision): card > Y targets > X keyline > dots > stripes.** It is
  carried by passes and pitch only, never by recolouring or resizing:
  - card: 1.05 mm solid line plus a hatched band;
  - targets: up to 4 coloured rings with a fused 0.55 mm outer ring, ≈ 39 % tone across an
    11 mm disc;
  - keyline: one 0.60 mm line, long but thin;
  - dots: discrete solid marks of 0.53–2.56 mm;
  - stripes: 0.30 mm hairlines at 14 % tone.

  Dots outrank stripes as marks (solid figure against hairline texture), not by average
  tone.
- **Proportion:** X figure : card = 13.7 : 1. The card is the loudest, the figure the
  largest.
- **Fill vs void:** the target chains are packed, the stem's ramp interior is blank (the
  finding), and the two quiet zones sit outside the keyline.
- **Density gradient:** across the front, a 14 % stripe field turns into a sparse dot
  lattice with coloured targets. The front is where the density changes character.
- **Colour play:** colour is scarce and appears only behind the front. Blue gathers on the
  spine (stem column, left-arm ridge) and crimson on the rim. The colour ratio is
  data-driven, never rebalanced.
- **Texture direction:** stripes follow X's form (isolines). The card's shadow hatch falls
  against their grain (r05), so the shadow never reads as more field.
- **Depth:** declared flat except for one lifted plane, the card. There is **one** defended
  overlap type, clip-behind at GAP = 0.85 mm, used in three places:
  - stripes stop at the staircase and at the card band;
  - response rings stop at the keyline's ink.

## 8. The twist

- **What the viewer holds:** a convolution makes a new picture of the input, like a blurred
  or edge-traced copy.
- **What the mechanism breaks:** a zero-sum symmetric kernel annihilates every straight
  ramp, and a distance field is a ramp almost everywhere. So the output is mostly
  **nothing**. Y survives only on X's spine (blue) and at X's rim (crimson), and the broad
  interior behind the front stays blank. This is why the finding row reads as
  `blank  X straight (flat or constant slope)`.
- **The keyline sharpens the twist:** the same outline encloses read and unread X, so the
  viewer sees one figure that the window turns mostly into blank paper.

## 9. Forbidden list

- No arrows. No second kernel, no confetti, no Memphis primitives (nothing from r06).
- **No keyline piece that ends at a riser, at the card, or anywhere but the crop.** The
  keyline is one open polyline with exactly two ends, both on the crop. It is never cut to
  make room: the rings give way, the keyline does not.
- Do not move a lattice node or change K, the stride, the read set, the ring pitch
  (1.02 mm), the ring radii, the collar rule or the card geometry.
- Do not fix hierarchy by shrinking or deleting the card, recolouring, or thickening
  stripes.
- No stripe pitch other than 2.1 mm, or the 3.15 mm fallback.
- **No lens where two stripe families meet with a tip gap < 0.8 mm** (A24: the whorl eye
  near (228, 183) and (150, 143)). Trim both tips back along the ring so bare paper is
  ≥ 0.8 mm. Measure gaps along the polyline, not the chord (the r05 `_bridge`).
- No response ring within 0.8 mm of keyline ink without being clipped.
  - Clip at 0.85 mm off the keyline ink and drop pieces < 3 mm.
  - Known cases: (2,5) +2 crosses the keyline; (3,1), (7,1) and (0,6) +1 graze it at
    0.28–0.43 mm.
  - A clipped ring stays a C open toward X's edge. Do not delete it.
- No dot drawn for x < 1.5 mm, and no dot under the pen floor as a tap. A sub-floor sample
  is paper, not a 0.30 mm blob.
- No black line below y = 24.2 except the title. No text line wider than 61.4 mm. No ink
  past x = 277 except the deliberate wing bleed on the crop.
- No formula line in the key (`rings = round(…)`, `∇²X ≈ 0`). No key growth beyond rows
  2–9.
- No stroke re-orderer in the piece to beat A19: `reorder_by_color` re-chains from (0,0)
  downstream, so it is an engine request.

### 9a. Lies list (the standard convolution list plus this plate's declared omissions)

| lie | status required |
|---|---|
| kernel not zero-sum / collar ink not ∝ \|w\| | clean (4b) |
| convolution vs cross-correlation flip | clean: the kernel is 180°-symmetric |
| output size / stride / window inconsistent | clean: 17×11, stride 2, 36 mm windows, exact staircase |
| rings not actually K∗X | must stay 63/63 visible bins, sign 37/37 |
| same quantity at two scales | one ring pitch, including the key icon |
| inputs hidden by outputs | 0 dots under a ring or hatch. Rings go behind the keyline, never over it |
| **drawn area not ∝ the declared quantity** | dot INK area within ±20 % of x on all 180 drawn dots (S10) |
| false zero | the zero codes are keyed: no dot means x < 1.5 mm, no ring means \|y\| < max/8 |
| caption the drawing does not support | the finding rows are worded as in §5 (S11). "Flat" alone is forbidden, because the blank nodes include constant-slope ramps |
| decorative marks posing as data | none: every mark type has a key row |
| declared omissions | (a) the last riser stops at y 24.2, not the lattice edge at 17.0. Row 0 is all x = 0, so nothing is misstated. (b) 3 finished outputs lie under the card (HANDOFF). (c) X is cell-averaged, not point-sampled. HANDOFF wording must say "cell-mean distance" and not "exact" |

## 10. Fabrication

- **Nib:** 0.30 mm fineliner on all pens.
- **Spacing floor 0.8 mm.** Hatch floor 2.4 × 0.30 = 0.72: card hatch 0.9 ✓, stripes 2.1 ✓,
  ring gaps 0.72 bare ✓.
- **Intentional fused passes:** card 0.25 pitch, keyline 0.30, doubled outer ring 0.25,
  collar passes 0.32.
- **Draw estimate:**
  - black ≈ 10.5–11 m: stripes ≈ 5.5 m (was 10.96), keyline ≈ 1.16 m, dots smaller and 36
    fewer;
  - crimson ≈ 0.5 m;
  - blue ≈ 0.85 m (+5 outer passes ≈ 0.17 m).
- **Pen-downs:** one per dot, per title segment, per stripe run and per ring pass. Black
  falls from 714 to about 620.
- **Time at Leo's settings** (F600, 1 s dwells), from r05's 58 min: black ≈ 43 min,
  crimson ≈ 3, blue ≈ 3.5, total ≈ 50 min. NOTES must give minutes per layer.
- **Pen swaps:** 2 (crimson → blue → black).
- **Flood risks:**
  - the fused 0.55 mm outer rings on blue: 2 passes only, never 3;
  - collar bands (fused by design);
  - stripe chevron tips on the wing ridge (spacing guardrail, ≥ 0.8 mm);
  - the dropped lens tips (A24).
- **Travel (A19):** engine-blocked. `postprocess.reorder_by_color` re-chains each layer
  greedily from (0,0). Report the max in-layer hop per pen in NOTES. Do not hack around it.
- **Determinism:** the gcode body is seed-independent (as r05).

## 11. Acceptance checks (the critics mark these pass/fail on the png and gcode)

1. **One X (A21).** At a 25 % thumbnail you can trace one Y from the stem foot
   (107.5, 27.8) round the left arm tip and out along the wing. In the gcode the keyline
   is one polyline per pass (2 passes, ≈ 581 mm each). Its only endpoints are on the crop,
   at (≈166, 197) and (284, ≈153). No black contour ends at a riser.
2. **The output outranks the input (A22).** At 25 % the blue stem column and the left-arm
   targets read as a chain of targets, second only to the card. The 5 doubled outer rings
   are present at the coordinates in §4. The wing reads as ground:
   - stripe perpendicular pitch 2.10 ± 0.05 mm;
   - wing ink ≤ 6 m (r05: 10.96 m);
   - the card keyline is the only line wider than 0.60 mm.

   NOTES gives ink metres per element in the §7 weight order. If this fails at 2.1 mm, the
   only allowed fallback is 3.15 mm plus the matching key text.
3. **Dots tell the truth (S10).**
   - 180 dots drawn;
   - inked Ø = centreline Ø + 0.30;
   - inked area within ±20 % of x on all 180;
   - Y recomputed from the inked areas: 63/63 visible bins (66/66 with the card);
   - no dot for x < 1.5 mm;
   - no dot ink within 0.8 mm of keyline ink.
4. **Grid (A23).**
   - The last riser ends at (197.6, 24.2), and no staircase ink is below y 24.2.
   - The title baseline is at 20.6, and the key baselines are at 35.0 … 85.4 (each ±0.3).
   - The title's and icons' left ink edges are at x = 204.8 (±0.3), and the riser-to-title
     gap is ≥ 7.2 mm.
5. **The key is exact and did not grow (S11).**
   - Exactly the 8 rows of §5, verbatim. They name dots, stripes, the card with its
     collars, the staircase, rings and the three-way finding.
   - The block stays inside x 204.8–277, y 34–92.
   - No formula line.
   - Plus the r05 preservation bar: the card is unchanged, collars ∝ \|w\| within 0.4 %,
     and no stripe-lens tip gap < 0.8 mm (A24).
