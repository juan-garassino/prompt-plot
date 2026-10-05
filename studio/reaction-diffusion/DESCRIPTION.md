# MORPHOGENESIS / BACTERIO — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/reaction_diffusion` (MORPHOGENESIS, round 01) |
| gallery | `gallery/studio/bacterio` (BACTERIO, round 04) |
| current render | `gallery/studio/reaction_diffusion/current/pp_reaction_diffusion_v8.png` |
| current render | `gallery/studio/bacterio/current/pp_bacterio_v5.png` |
| source | MORPHOGENESIS: `studio/reaction-diffusion/rounds/r01/piece.py::studio_reaction_diffusion` · BACTERIO: `studio/reaction-diffusion/rounds/r04/piece.py::studio_bacterio` (r02 `::studio_pipe_rank` = gallery `studio/voicing`; r03 `::studio_ruled` = gallery `studio/ruled` — separate gallery subjects, same family) |
| paper · pens | both a4 portrait (210×297), cream. MORPHOGENESIS: 0 black = field, frames, type · 1 crimson = calipers, germ, S(q) peak ticks, swatch. BACTERIO: 0 black = the grown field + body copy · 1 crimson = the 12 germ outlines, one sine squiggle, one caption line · 2 forestgreen = the predicted-wavelength rules, frame, two caption lines · 3 dodgerblue = title, slab, subtitle |
| status | unreviewed (no feedback on either) · reaction_diffusion 10 renders, bacterio 5 renders |

## In one line
Gray-Scott reaction-diffusion drawn as a **lattice-with-defects** (a labyrinth with one pitch and no grain) — the selected wavelength follows √D. MORPHOGENESIS states it as an exploded axonometric deck of three separate runs at D 0.4 / 1.0 / 2.0 plus a magnified relief; BACTERIO states it as one sheet-filling field whose D ramps ×7 left→right, overprinted with green rules spaced at the predicted local wavelength and red germ outlines at true scale, dressed as Sottsass's Memphis *Bacterio* laminate.

## Lede
A chemical pattern-forming reaction drawn as a labyrinth with one natural pitch: the **spacing of its stripes grows with how fast the chemicals spread**.

## On the sheet
Both plates are dense black contour fields of a simulated pattern. One is a tilted deck of three plates and a large relief at upper right, with crimson scale bars at left. The other fills the sheet beneath a giant blue title, crossed by vertical green rules and outlined by crimson germ shapes. Captions run down the left side.

## The science
Both run the real equations of a two-chemical reaction. Letting the chemicals spread four times faster makes the stripes twice as wide, and the printed measurements agree within a few percent. On the second plate the green rules are the predicted spacing, not measured. Counting stripes between rules by eye is hard, and the starting shapes leave visible traces.

## What is on the sheet

### MORPHOGENESIS (reaction_diffusion v8)
Reading order: the big relief upper-right, then the rising diagonal deck lower-left → centre, then the left caption column, then the footer and inset.

- **Title block**, flush left at u≈0.06, v 0.05–0.12: `M O R P H O G E N E S I S` (spaced caps, ~7 mm, spans u 0.06–0.81); `A UNIFORM FIELD CHOOSES A LENGTH`; `GRAY-SCOTT REACTION-DIFFUSION. ONE SEEDED FIELD` / `THREE DIFFUSION SCALES. THE SPACING GOES AS SQRT D.` All black hairline stroke font.
- **Empty band** v 0.13–0.22 across the whole width.
- **Hero relief** (dominant mass): a flat axonometric rhombus, u 0.34–0.95 (≈0.61 of sheet width), v 0.22–0.45, right corner pressed onto the drawable edge. Inside, black isolines of v stacked on four terraces; the pause-resume hidden line leaves the back terraces as broken dashes, so the surface reads as many short parallel strokes plus closed lozenges, running roughly WSW–ENE. Some strokes poke outside the rhombus outline at the top corner (u≈0.62, v≈0.22) and down the right edge. Inside it, near the left front edge (u≈0.40, v≈0.35): label `LAMBDA 12.1` and a short crimson caliper laid along the front edge.
- **Left caption column** at u 0.06, v 0.34–0.53: `V IN RELIEF` / `ONE LEVEL SET PER TERRACE` / `WINDOW X4.0 OFF D 1.0`; `SELECTED WAVELENGTH` / `MEASURED OFF S Q`; three crimson I-beam bars of growing length (≈11, 17, 25 mm) labelled `D 0.4`, `D 1.0`, `D 2.0`; `CONTROL. SAME D   GERM X6`; two equal crimson bars (≈17 mm) `GERM 8`, `GERM 50`.
- **The deck**: four equal rhombi (≈0.22 of sheet width each) climbing a straight diagonal from lower-left to centre-right, chained by dotted lines between corners:
  - `T 0` / `UNIFORM PLUS NOISE` / `NO LENGTH SCALE` — centre u≈0.23, v≈0.79. Irregular closed speckle blobs; a small crimson germ diamond at its centre.
  - `D 0.4` / `LAMBDA 7.5` — u≈0.38, v≈0.73. The darkest plate: very tight labyrinth, lines nearly touching, a denser vertical seam down the middle and bilateral mirror symmetry.
  - `D 1.0` / `LAMBDA 12.1` — u≈0.52, v≈0.65. Labyrinth with **nested square rings** around the centre; a heavier inner rhombus marks the window lifted to the hero. Four dotted projection lines rise from it to the hero's corners.
  - `D 2.0` / `LAMBDA 17.4` — u≈0.67, v≈0.60. Open: 3–4 **concentric square rings** around a cross/plus motif — the germ's square symmetry, not a labyrinth.
- **Footer**, u 0.06, v 0.84–0.91, six lines: `DU 0.16  DV 0.08  F 0.030  K 0.057` / `GRID 128 PERIODIC  DT 0.75  STEPS 7000` / `LAMBDA CELLS 7.5  12.1  17.4` / `RATIO MEASURED 0.62 1.00 1.44` / `PREDICTED SQRT D 0.63 1.00 1.41` / `AGREE WITHIN 3 PERCENT OVER D X5`.
- **S(q) inset**, u 0.71–0.94, v 0.84–0.94: an L axis with three peaked curves (tall-narrow → low-wide, left→right), three crimson ticks on the baseline, labels `S Q` and `Q PER BOX`.
- Furniture: plus marks top-left (u 0.06, v 0.04) and bottom-right (u 0.94, v 0.96); a tiny black+crimson swatch stack top-right (u≈0.94, v≈0.05).

### BACTERIO (bacterio v5)
Reading order: the giant blue title, then the full-bleed black labyrinth, the red germs, the green rules.

- **Title** `BACTERIO`, dodgerblue giant type, u 0.05–0.87, v 0.05–0.14 (~25 mm cap height), each stroke built as 4–5 parallel passes (reads as an outlined/hollow heavy face). A blue triple-line slab under it, u 0.05–0.61, v≈0.14, sitting directly on the tops of the subtitle caps.
- **Caption stack**, flush left at u 0.05, v 0.15–0.32, ten lines in three colours:
  - blue: `SOTTSASS DREW IT. TURING EXPLAINED IT.`
  - green: `GREEN RULES ARE THE PREDICTION.` / `COUNT THE SQUIGGLES BETWEEN THEM.`
  - crimson: `12 SEEDS. 6X THE SIZE RANGE. ONE PITCH.`
  - black: `THE MEMPHIS LAMINATE IS A REACTION-DIFFUSION FIELD AND` / `EVERY SQUIGGLE HERE CAME OUT OF THE ACTUAL PDE.` / `GRAY-SCOTT  DU 0.16  DV 0.08  F 0.030  K 0.057` / `D RAMPED X7 ALONG X.  DT 0.75.  STEPS 6000.` / `PITCH 11.9 MM MID SHEET. SQRT D HOLDS TO 5 PCT.` / `SAME D. SEEDS 6 AND 38 CELLS. PITCH 9.4 AND 9.4 MM.`
  - Small black field fragments and ticks leak into the caption between these lines (around u 0.2–0.5, v 0.29–0.31).
- **The field** (dominant area, ~0.9 width × 0.65 height): black isolines of v, u 0.05–0.95, v 0.32–0.97, bleeding to the drawable frame on three sides. Left third: tight maze (~3–4 mm pitch), many dead-ends and U-turns. Right third: long, fairly parallel wavy stripes at ~8–10 mm pitch, oriented mostly vertically/diagonally. Uniform line weight, single pass.
- **Green rules**: 17 full-height vertical lines from the top of the title to the bottom frame, spacing widening left→right (≈8 mm at u 0.08 → ≈16 mm at u 0.9). They cross the blue title letters, become short dashes between caption lines, and run unbroken through the field. A green dotted rectangle frames the drawable area; one stray horizontal green line at v≈0.29, u 0.61–0.95.
- **Red germs** (crimson outlines, the only loud colour inside the field): a square u 0.06–0.21 × v 0.53–0.64 (the largest, holding a tighter horizontal-stripe pattern); a large circle centred u 0.32, v 0.54 (r≈0.09 of width); a mid circle u 0.53, v 0.58 with a small tangent circle beside it u 0.61, v 0.58; a tiny square u 0.31, v 0.82; a tall triangle u 0.43, v 0.74–0.82; a square u 0.51–0.59 × v 0.81–0.87; triangles at u 0.57 v 0.86–0.91 and u 0.65 v 0.82–0.90; a square u 0.71–0.83 × v 0.83–0.90; a small triangle u 0.87 v 0.67–0.70; a small circle u 0.84 v 0.79. Black lines run through all of them unbroken — no knockout. A crimson 3-wave sine squiggle floats at u 0.57–0.91, v≈0.33, over the field's top edge.

## The science it encodes
Gray-Scott, `du/dt = Du∇²u − uv² + F(1−u)`, `dv/dt = Dv∇²v + uv² − (F+k)v`, explicit Euler, 5-point Laplacian, F 0.030, k 0.057, Du:Dv 0.16:0.08, dt 0.75. Scaling both D by s is an exact similarity under x → x√s, so λ ∝ √D; nothing in the PDE has units of length.
- MORPHOGENESIS (`r01/NOTES.md`): three periodic 128² runs from one shared noise realisation at s = 0.4/1.0/2.0; λ measured from the first moment of the radial structure factor: 7.5 / 12.1 / 17.4 cells, ratios 0.62/1.00/1.44 vs √s 0.63/1.00/1.41 (within 3 %). Germ control: half-width swept 6× → λ spread ±4 %, no trend. All of this is computed; the numbers printed on the sheet are the measurement. dt caps s at 2.0 (stability), so the ×5 range is set by the integrator.
- BACTERIO (`r04/piece.py` docstring): one field, D ramped geometrically along x (docstring says 8×, the sheet prints `X7`), periodic in y, zero-flux in x; λ measured once mid-sheet, and every green rule placed by integrating dx/λ(x) with λ(x) = λ_mid√(D/D_mid) — the rules are pure prediction. Twelve germs in three shapes over a 6× size range; two at the same x give pitch 9.4 and 9.4 mm.
- Visibility check: on MORPHOGENESIS the D 1.0 and D 2.0 plates visibly print the square germ's symmetry (nested square rings, a central cross) — the "uniform field chooses a length" claim reads weaker than the numbers say. On BACTERIO the coarsening left→right is visible, but "one squiggle period per green cell" is not readable by eye: the maze's orientation varies, so counting squiggles between rules does not work except where the stripes run vertical.

## How it got here
- **r01 MORPHOGENESIS** (reaction_diffusion v1–v8, seeds 3/19): v3 had a surface hero with a central bullseye and red `LAMBDA` labels on the deck; by v5 the surface mesh was dropped for terraced isolines and the germ control bars appeared; v7→v8 only tidied the hero label (`LAMBDA 12.1` + caliper inside the relief). The layout (title / left captions / diagonal deck / footer / S(q) inset) never moved. NOTES self-scored ~7.4 with concept at 6: "the hero is the biggest thing on the sheet but not the arguing thing" and the S(q) inset risks the textbook-plot fail.
- **r02 VOICING** (gallery `studio/voicing`): the field wrapped on a rank of organ pipes cut to eight wavelengths, red √D ladders — an illustration (names an object), abandoned.
- **r03 RULED** (gallery `studio/ruled`): Swiss, giant `RULED`, one ramped field full-bleed, five red calipers + two germ squares on a module — the first single-field statement.
- **r04 BACTERIO** (v1–v5): went four-pen Memphis. v1 had the caption split top/bottom and a germ making a target-like bullseye; v2–v4 moved all copy to the top block, reshuffled the germs; v5 added the crimson sine squiggle top-right, trimmed the field to start under the caption, and settled the caption at ten lines.
- Gained: one continuous field (the argument IS the dominant mass), a real joke. Lost: the explicit side-by-side λ comparison and the germ-size control reading at a glance.
- Juan's feedback: none recorded.

## Keep — what works

### MORPHOGENESIS
- The diagonal deck climbing from T 0 (u 0.23, v 0.79) to D 2.0 (u 0.67, v 0.60) as a tone ramp — dark D 0.4 plate to open D 2.0 plate — makes "same field, different spacing" readable from 3 m.
- The five crimson calipers in the left column: three unequal, then two equal under `CONTROL` — the falsification drawn without prose.
- The near-empty `T 0` speckle plate with its crimson germ: the blank start is shown, not asserted.
- The hero cropping onto the right drawable edge at v≈0.33 and the dotted lines fanning up from the D 1.0 window.

### BACTERIO
- The concept: a Memphis laminate that is literally the PDE — the best twist in the family; keep the title and `SOTTSASS DREW IT. TURING EXPLAINED IT.`
- A single sheet-filling field whose pitch visibly opens from ~3 mm at the left edge to ~10 mm at the right — the gradient IS the result.
- Green rules as the prediction, widening left→right; red germs as scattered confetti in three shapes and many sizes (the big square u 0.06–0.21, v 0.53–0.64 and the big circle u 0.32, v 0.54 carry the eye).
- Field bleeding to the frame on three sides, no plate outlines.

## Weak — what doesn't

### MORPHOGENESIS
- [concept] It is the scientific figure the rubric names: relief + parameter deck + axis inset + measured caption. The S(q) inset (u 0.71–0.94, v 0.84–0.94) is a textbook axis plot and fails § 6 on its own.
- [concept] D 1.0 and D 2.0 show concentric square rings and a cross — the square germ's imprint — so the plates read as ornament grown from a seed, contradicting "a uniform field chooses a length".
- [hierarchy] The dominant relief does not argue anything; it is a magnified crop of D 1.0 whose pause-resume dashes read as shredded foil, and its four terraces are not legible as height.
- [craft] D 0.4 plate floods: contour pairs nearly touch and a dark vertical seam runs down its middle; the densest thing on the sheet is also the smallest.
- [craft] Hero strokes overshoot the rhombus outline at its top corner and right edge.
- [space] The band v 0.13–0.22 and the pocket between the caliper column and the deck (u 0.3–0.6, v 0.45–0.58) are leftover, crossed only by dotted lines.
- [depth] Axonometry is there but every plate is a flat card; the relief's height is not readable.

### BACTERIO
- [concept] "COUNT THE SQUIGGLES BETWEEN THEM" cannot be done: the maze's local orientation wanders, so the green rules do not index squiggle periods by eye; the prediction and the field never visibly lock.
- [hierarchy] Title, ten-line caption stack in four colours, 17 green rules, 12 red outlines and the field all shout at once; the green rules, full height and uniform weight, compete with the field instead of sitting under it.
- [craft] Green rules cross the blue title letters (green-on-blue collisions in every letter); the blue slab sits on the subtitle's cap tops; black field fragments leak into the caption between v 0.29–0.31; a stray green horizontal at v≈0.29, u 0.61–0.95 and the red sine at v≈0.33 look like leftovers.
- [concept] The germs are outlines drawn over the pattern with black running through them — they do not read as the thing the pattern grew from; the "two germs at the same D, same pitch" control is invisible (nothing pairs them).
- [grid] Memphis is claimed but not built: no fat keylines, no Ben-Day, no slab colour blocks — four hairline pens as categories; the canon reads as "coloured technical drawing".
- [space] No quiet zone: the field fills everything below v 0.32 edge to edge and the copy fills everything above it.
- [depth] Declared flat (Memphis) — acceptable, but the promised layering (germs knocking out the field) is not drawn.

## Next versions
1. **LAMINATE** (abstract) — Commit to BACTERIO as a true Memphis surface: the field is the only full-bleed element; germs become solid fat-keylined confetti that KNOCK OUT the field (pattern visibly radiates from each); the prediction moves from 17 hairlines to a short ruler band along one edge (the only green on the sheet, ticks spaced at predicted λ(x)), so field and ruler lock where they touch. Title shrinks to one Memphis slab block; copy to three lines. Hierarchy and concept both rise: one mass, one loud accent, one measurable edge.
2. **ONE FIELD, ONE RAMP** (mechanism) — Return to the r01 NOTES recommendation: a single ramped field as the hero, but magnified and cut into three windows at D-stations stacked in axonometry, each window's own λ caliper cut from √D (red) lying across a stripe crest; no deck, no S(q), no terraces. The germ control becomes two same-x germs whose outlines are the only red in the field. Scores higher on concept (the dominant mass argues) and removes the square-germ ornament.
3. **NO GRAIN** (lens) — Draw the thing a Turing field uniquely has: one pitch, every direction. Centre-off a large circular window whose field is transformed to its Fourier ring (a single thin circle of power at 1/λ), with the physical labyrinth surrounding it; D-ramp makes the ring an ellipse-to-spiral across the sheet. Radial order, strong single figure, no plot furniture.

**If only iterating:**
- BACTERIO: remove the green rules from the title/caption band and stop them at v 0.32; clip the black field and the green rules out of every red germ (a 1.5 mm knockout ring) so germs read as seeds, not stickers.
- BACTERIO: cut the caption to three lines (blue subtitle, one green line, one black data line) and delete the stray green horizontal at v≈0.29 and the crimson sine at v≈0.33.
- MORPHOGENESIS: delete the S(q) inset and replace the square germ with an off-axis irregular blob so D 1.0 / D 2.0 plates show labyrinths, not nested squares; widen the D 0.4 plate pitch above 2 mm.
