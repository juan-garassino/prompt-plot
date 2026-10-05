# CONVOLUTIONS — description

<!-- rewritten 2026-09-29 by the studio lead when r07 went to the vote. It describes the CURRENT best version (r07, the one-X wavefront lattice) so the next iteration starts from the truth. The r01 description (the laminar band X → 5 whorl tiles → Y, with a footnote row) is history: r01 remains the unscored craft benchmark. See rounds/r01 and LEDGER.md. -->

| | |
|---|---|
| gallery | `gallery/studio/convolutions` (r01 at `current/pp_convolutions_v1.png` until the curator syncs) |
| current render | `gallery/studio/convolutions/trials/pp_convolutions_iterate_v30.png`, with the gcode beside it. The seed sweep `_s3` and `_s11` gives byte-identical bodies. Pending the curator's sync |
| source | `studio/convolutions/rounds/r07/piece.py::convolutions_onex` (seed 7, a4 landscape, palette crimson,dodgerblue,black) |
| encoding | `studio/convolutions/encoding.md` v1 (codifies the wavefront-lattice order). There is no `dossier.md`. Encoding §4b is the check table |
| paper · pens | a4 landscape, cream · 0 crimson = y > 0 response rings, + collars, and key icons · 1 dodgerblue = y < 0 response rings, − collars, and key icons · 2 black = X (dots, stripes, the x = 0 keyline), the staircase, the card and its shadow hatch, and the key text and title |
| plot | crimson 49 strokes ≈ 3 min → dodgerblue 51 ≈ 3.5 min → black 795 ≈ 47 min. Total ≈ 54 min. Draw 12.65 m, travel 5.47 m. The fabrication gate is clean |
| status | r07 at vote. Art 7.29/7 FAIL · science 9/9/8 PASS. Juan's feedback: none recorded |

## In one line
**One X being read into Y.**
- One Y-shaped figure X is drawn by a single black outline, with a heavy black kernel card at its fork.
- A staircase is the frontier of the convolution's sweep. Below and left of it, X has been sampled into a Ben-Day dot lattice and turned into chains of crimson and blue targets (Y = K∗X).
- Above and right of it, X is still a pale field of level-set stripes, running out through the top-right corner.

## Lede
One shape, read by a convolution: the sweep's frontier is a **staircase**, with sampled dots and response rings behind it and pale stripes ahead.

## On the sheet
A black outline of a Y-shaped figure runs across the sheet, with a heavy card marking the kernel at its fork. Behind a black staircase, a lattice of black dots and chains of crimson and blue rings fill the lower left. The upper right holds pale black stripes running off the corner. A key and the title sit at lower right.

## The science
This is a real two-dimensional convolution with a five-by-five Laplacian-of-Gaussian kernel and stride two. Dot size encodes the input, ring count encodes response strength, and crimson or blue gives its sign. The kernel responds only where the shape bends, so straight interiors stay blank. Three outputs hidden under the card are declared in the notes.

## What is on the sheet
Reading order:
1. The card.
2. The blue target chain down the stem.
3. The one keyline.
4. The dot lattice.
5. The stripe wing.
6. The key and title in the lower-right wedge.

- **The lattice.** 37 × 25 samples at 7.2 mm, at centres x = 21.2 + 7.2c, y = 20.6 + 7.2r. Its top and right edges are the crop line (y 197, x 284).
- **The X keyline** (black, 2 passes, ≈ 0.60 mm).
  - One open polyline, 583 mm per pass.
  - It leaves the top crop at (166, 197), rounds the left arm (x ≈ 24–60, y ≈ 120–178), and runs down the stem (x ≈ 74–141).
  - It rounds the foot at (107.5, 27.8), climbs the stem's right flank, and runs out along the wing's lower flank to the right crop at (284, 153).
  - It crosses the staircase unbroken. Pass 2 sits 0.30 mm outward, on X's outside.
- **Dots (read side, black).** 180 dots, each one pen-down: a solid spiral whose INK area ∝ the cell-mean depth x. Inked Ø runs 0.54–2.56 mm. There is no dot for x < 1.5 mm.
- **Stripes (unread wing, black).**
  - Level sets of X's distance field at Δd = 2.1 mm: 5.18 m of 0.30 mm hairline, about 14 % tone.
  - The wing (x 83–284, y 97–197) rises to the top-right corner and bleeds off both crop edges.
- **The staircase** (black, 1 pass).
  - It is the exact union boundary of the 66 read windows (i + j ≤ 10), with vertices on cell lines.
  - It falls from (53.6, 197) to (197.6, 53.0), and the last riser stops at (197.6, 24.2).
- **Response rings** (crimson y > 0, blue y < 0).
  - 37 ring nodes, centred on their own input sample at (35.6 + 14.4i, 35.0 + 14.4j).
  - Each carries 1–4 rings at a 1.02 mm pitch. For |bin| ≥ 3 the outer ring is doubled (0.55 mm).
  - Blue chain: the stem column (107.6, 64 / 78 / 93), then (78.8, 135.8) and (50, 150.2).
  - Crimson: rims and stem flanks. Ten crimson nodes sit on bare paper outside the keyline, where the window reaches X's edge.
- **The card** (head node (5,6)).
  - Window 89.6–125.6 × 103.4–139.4. Keyline 4 passes, fused to 1.05 mm: the heaviest line.
  - A 3.2 mm hatched 45° shadow on the right and bottom.
  - The 25 kernel taps carry collars whose ink ∝ |w|: crimson +, blue −.
  - It hides outputs (4,5) 0, (5,5) −3 and (4,6) −2. This is declared.
- **Key** (lower-right wedge beyond the last riser).
  - 8 rows on lattice rows y 35.0 … 85.4. Icons sit on the axis x 204.8, and text starts at 215.6.
  - Rows: dots · stripes · K card · staircase · Y rings · blank · crimson · blue.
  - Bare paper sits above the key (y ≈ 92–120).
- **Title.** `CONVOLUTIONS` on row 0 (baseline y 20.6), x 204.8–277.0, 3-pass segment bands.

## The science it encodes
A 2D valid convolution with stride 2.
- **X** is the distance-inside-outline field of a 3-capsule Y. The dots show it as cell means (6×6 quadrature); the stripes show it as its own level sets.
- **K** is a 5×5 Laplacian-of-Gaussian with σ = 1 cell. It is zero-sum, with 5 negative and 20 positive taps.
- **Y = K∗X** is a 17 × 11 output, of which 66 windows are read. It is drawn as the ring count rint(4|y|/max|y|), with max|y| = 18.731. The pen carries the sign.

The finding on the sheet: the LoG responds only where X bends.
- It is blank where X is straight (flat or constant slope).
- It is blue where X bends down (the spine ridge and the tips).
- It is crimson where X bends up (where it starts, at the edge).

So the Y's broad interior stays blank.

**Checks the science critic reproduced independently from the gcode:**
- 17 × 11 grid; 66 read windows.
- Ring counts 37/37 and signs 37/37.
- Y recomputed from the inked dot areas: 66/66 bins.
- Dot area error −0.6 … +3.8 % on 180/180.
- Collar ink ∝ |w| to 0.36 %.
- Stripe level residual median 0.003 mm.
- Staircase exact to 0.01 mm.

**Declared omissions:**
- (a) The last riser stops at y 24.2.
- (b) Three outputs are hidden under the card.
- (c) X is cell-averaged. At the rim, a point-sampled reading would be off by up to 24 %.

## How it got here
- **r01**: a measured reconstruction of the reference (a pipeline band with whorl tiles and a footnote row). It is the craft benchmark.
- **r02 real-kernel** and **r03 sliding-window**: they computed the convolution but stayed a triptych.
- **r04**: the wavefront. ONE lattice with a staircase front and the LoG card at the fork. It read as a heart.
- **r05**: cropped the lattice at the top and right, added the stripe wing, the lifted card and the |w| collars.
- **r06**: the *Bacterio* wildcard, kept as a flavour.
- The translator then codified r05 as `encoding.md` v1.
- **r07**:
  - made X one keyline;
  - halved the wing ink;
  - doubled the strong rings;
  - nib-corrected the dots (ink area ∝ x);
  - closed the riser on row 0;
  - seated the key and title on lattice rows;
  - rewrote the key to name every mark.

  Science passed for the first time. The designer round cap (5 per encoding) is hit.

Ledger: `studio/convolutions/LEDGER.md`.

## Keep — what works
- **One X.** A single continuous keyline carries X across the read/unread front. It is the first round in this order where the figure is one contour, which is the r01 quality most often lost.
- **One lattice, one front.** The staircase is the exact read set. Colour appears only behind it. Every mark is data, and every mark type has a key row.
- **Exact channels on one scale.** Dot ink area ∝ x, ring count ∝ |y|, pen = sign, collar ink ∝ |w|, and stripe = isoline at 2.1 mm. All are recomputable from the sheet.
- **Two diagonals cross at the card.** The staircase falls ↘ and the wing rises ↗. Both bleed off the frame, and the card sits off-centre at their crossing.
- **The strict grid.** The riser, the title, the key baselines and the axis x 204.8 all sit on the 7.2 mm lattice.
- **Contour discipline in the field.** Wing tips ≥ 0.86 mm, rings ≥ 0.85 mm off the keyline, dots ≥ 0.93 mm off it, and collars ≥ 0.62 mm.
- **Plot contract.** 3 pens, one clean layer each, streamed crimson → dodgerblue → black, with seed-independent gcode.

## Weak — what doesn't
- **[hierarchy / canon]** The Pop outline does not dominate. At 0.60 mm the X keyline weighs the same as the doubled rings (0.55) and the stripes at 3 m. The plate reads as a precise dot diagram, not a Lichtenstein (A25).
- **[craft]** There are a few sub-floor contacts (A26):
  - 8 stripe tips stop 0.55 mm from the staircase;
  - dots at (100.4 / 107.6 / 114.8, 99.8) are 0.63 mm off the card hatch;
  - an orphan 4.5 mm stripe stub sits at (69–74, 169–171).
- **[craft]** The title's per-segment bands double-ink every chamfer corner (A27).
- **[space / legibility]** The lone crimson rim rings on bare paper read as strays until the key says why (A16 residue → S12a). The 8-row key edges toward a figure caption.
- **[travel]** Key swatches are drawn mid-layer, with blue hops up to 179 mm. This is engine-blocked (`reorder_by_color` re-chains from (0,0)).

## Next versions
1. **one-X r08 (REWORK, parent r07)**
   - First, encoding v1.1: X keyline in 3 passes (≈ 0.90 mm), card in 5 (≈ 1.30 mm), everything re-clipped ≥ 0.8 mm off the widened ink.
   - Then close A26 and A27, and add the S12 key clauses without growing the block.
2. ***Bacterio*** (flavour, r06): three kernel cards over unit-impulse confetti. Parked mandates W1–W3, including the regressed sign channel.
3. **sliding-window** (r03) / **real-kernel** (r02): earlier flavours on disk.

**If only iterating:**
- thicken the X keyline to 3 fused passes and the card to 5;
- butt or clear the 8 staircase stripe tips;
- trim the hatch off the row-y 99.8 dots;
- draw each title glyph as one band path;
- key crimson as "the window reaches X's edge".
