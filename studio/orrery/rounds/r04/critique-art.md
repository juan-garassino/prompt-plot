# Art critique — orrery r04 · canon: RADIAL DATA-VIZ · 2026-09-29
render: `gallery/studio/orrery/current/pp_orrery_iterate_v11.png` (+ `.gcode`, re-rendered from gcode at 20 px/mm with a 0.4 mm nib for the detail crops)

## Scores
| dim | score | why |
|---|---|---|
| 1 hierarchy | 7 | Disc is the clear mass, the title comes second, and the heavy ring and crimson sun are the focal accents. Inside the disc, though, 26 near-identical wavy hairlines give no ranking below the one heavy ring. |
| 2 grid & alignment | 7 | The spine at x=105 is a real axis. The weights column right-aligns to it, the tokens, title and caption left-align to it, and the question right-aligns to it. The wedge is inconsistent: the left edge is a vertical cut (every orbit ends at x≈95) and the right edge is a radial cut (ends step from x≈113 to 135), so the slot reads as ragged. |
| 3 tension & asymmetry | 5 | The disc centre sits at x=105.2 on a 210 sheet. Blue runs from x 13.7 to 196.3, which is dead centre with equal side margins (known failure mode 1). The wedge sits at 6 o'clock and the spine on the page centreline. The only asymmetry is the text block below. |
| 4 negative space | 6 | Blue stops 3.7 mm inside the drawable frame on the left and right and 4.1 mm below the top. The caption stops 4.4 mm from the right edge and 4.0 mm from the bottom. These are pressings, not crops. The ~30 mm stem band and the lower-left field are air, but they are leftover air, apart from the floating question. |
| 5 craft for pen | 8 | Measured: no blue pair is closer than 0.8 mm except the intentional 3-pass orbit (0.35 mm). The sun spiral is ≥0.8 mm pitch at Ø18.75. Max hop is 37 mm and there are 0 hops over 60 mm. There are 2 swaps. Type is 43.5 of the 65 minutes, and the stroke-font `mm` closes up to `nn` at caption size. |
| 6 concept legibility | 6 | Not a schematic and not a figure, but the order does not read. Every orbit, the "closing" one included, stops at the same 29 mm wedge (heavy orbit ends at (95.3, 116) and (124, 117)), so nothing visibly closes. Each miss is now two parallel hairlines 1.3–4.7 mm apart, which reads as uneven ring pitch, not as a failure to close. At 3 m it reads as a blue ripple target with a red lollipop spiral on a stick. |
| 7 depth & dimensionality | 5 | Flatness is declared (face-on orbital diagram). The one depth cue named, focus, is a single heavier ring among 26 lines of the same weight and amplitude. That is weight, not depth. |

avg **6.29** · min **5** · **VERDICT: FAIL**

## Reads at a glance
A centred blue fingerprint of wavy rings, a red spiral in the middle and a red stem dropping to the title, with one ring thicker than the rest. Nothing on the sheet shows the stranger that one ring closes and twelve do not.

## Acceptance checks
No `encoding.md` exists (S7), so these checks come from `rounds/r04/checks.py` and the LEDGER tests.
- Layer order 0/1/2, one clean layer per pen: **PASS**
- No in-layer travel over 60 mm (A10): **PASS** (max 37.2 mm; approach moves 139/177 mm)
- Zero blue strokes under 8 mm: **PASS**
- Glyph clearance ≥ 2 mm from blue: **PASS** (2.10 mm, tight)
- Sun Ø ≥ 18 mm and pitch ≥ 0.8 mm: **PASS** (Ø18.75; no crimson pair under 0.8 mm outside the glyphs)
- Closing orbit as 3 passes ≥ 0.3 mm apart: **PASS** (0.35 mm)
- Envelope ratio ≥ 3:1 on the 3 o'clock ray: **PASS** (3.23)
- At least 2 inter-band gaps ≥ 4 mm: **PASS**, marginally (exactly 2, 4.2 and 4.2 mm)
- Parallel strands < 0.8 mm: **PASS** (0 %)
- Every orbit ≥ 95 % drawn (S5): **FAIL**. 10 of 13 are under 95 % (`The` 81 %, `pen` 85 %, `plot` 88 % …) because the slot has constant width.
- Closure visible on the sheet (the thesis): **FAIL**. The closing orbit is cut by the same slot as every miss.

AUTHORING §6 (reference = the ChatGPT attention orrery, judged as an interpretation):
1. Main forms recognisable without fills: **PASS** (rings, sun, stem).
2. Shading follows the surface: **N/A** (no shading).
3. Fine lines that are really two sides of one stroke: **PASS**. The pairs are two turns, and the triple is declared weight.
4. Blackest regions intended: **PASS** (sun spiral, heavy ring).
5. Labels readable at real pen width: **PARTIAL**. The spine labels are fine. `sink` (~1.5 mm cap) and the 11-line caption (~2 mm x-height, `mm` → `nn`) will clog above a 0.4 mm nib. HANDOFF gives no nib widths.
6. Black knots from a thicker pen: **PASS** at 0.4 mm. The sun centre would flood with a POSCA.
7. Long empty travels or pointless tiny marks: **PASS**.

Interpretation: the reference's celestial grammar is gone: no bodies on the orbits, no dotted orbits, no second centre. The canon's mandatory "small glyph markers on the arcs" are also missing. The keys exist only as text in the slot, not as anything on their orbits.

## Biggest weakness
The thesis is invisible in the drawing. Resonance means one closed orbit against twelve that fail to close, but every orbit, the resonant one included, stops at the same 6 o'clock slot, and all 27 lines share one wave amplitude. The resonant ring differs only by weight, the misses read as uneven ring spacing, and only the caption says what happened. r03 at least carried the contrast in texture (braided annuli against one clean wave). r04 traded that for passing numbers.

## Mandates
1. **Make closure visible at the 6 o'clock slot, and on two radial edges.** The `transformer` orbit (the 3-pass ring at r≈75 mm, now ending at (95.3, 116) and (124, 117)) must run unbroken across the slot and cross the crimson spine as a chosen overlap. Every missing orbit keeps its open ends, and both slot edges must lie on rays from the sun centre (105.2, 191.5), so the left edge is no longer a vertical cut at x≈95. Test: on the full page, exactly one blue line is continuous through the 6 o'clock slot, and every blue end point sits within 0.5 mm of one of two rays.
2. **Take the disc off the centreline and off the frame.** Move the sun centre to x ≥ 125 (or x ≤ 85) and either crop the disc hard at one side margin, with at least 25 % of the outer ring past the edge, or shrink it so it clears the drawable frame by ≥ 10 mm on every uncropped side. The type block then takes the opened side instead of the bottom-right corner, with the caption ≥ 8 mm clear of the frame. The HANDOFF names which orbits the crop removes and says whether that breaks S5. Test: sun x ≠ 105 ± 10; blue-to-frame distance is either < 0 (a declared crop) or ≥ 10 mm on every side, never between 0 and 10 mm (it is 3.7 / 3.7 / 4.1 now).
3. **Canon palette.** Replace dodgerblue as the key pen with a desaturated hue (slate, grey-blue, sepia or olive; state the ink) so that crimson is the only saturated ink on the sheet, as RADIAL DATA-VIZ requires ("muted multi-hue on cream … NOT loud primaries"). This is the pen that carries 70 % of the ink (8.7 of 12.4 m). Test: the HANDOFF pen line names a muted ink for layer 0, and the preview shows the crimson sun and spine as the loudest colour at thumbnail size.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| A8 | FIXED (on its tests) | Envelope ratio 3.23 ≥ 3, and 2 gaps of 4.2 mm. But see the regression below: the wider miss now reads as spacing, not as a miss. |
| A9 | FIXED | Sun Ø18.75 with no crimson pair under 0.8 mm outside the glyphs. Closing orbit 3 passes at 0.35 mm. 0 blue strokes under 8 mm. |
| A10 | FIXED | Max in-layer hop is 37.2 mm, 0 over 60 mm, on all three layers. Travel is down from 6.6 m to 3.0 m. |
| A11 | FIXED | Blue-to-glyph clearance is 2.10 mm. Question and title clear the spine by ~2 mm. |
| A12 | FIXED | HANDOFF carries `canon:` and `flat: declared`. |
| A14 | REGRESSED | r03's disc sat off-axis (centre x≈70, cropped at the left margin). r04 recentres it at x=105.2, so the centre axis is back. The empty lower-left (x 10–95, y 10–55) is still leftover, holding only the floating question. |
| C1 | argued, unchanged | Still 3 pens. Juan's standing note allows more pens when batched. That is not needed here: mandate 3 re-inks a pen, it does not add one. |

## Regressions vs compare-to (r03 `pp_orrery_resonant-orbits_v14.png`)
- **The visible contrast between resonance and miss is gone.** In r03 each miss was a 4-turn braided cable and the resonant orbit was a single clean, larger, slower wave, so you could see the difference in texture from across a room. In r04 all 27 lines have the same small amplitude and lobe rhythm, and the resonant orbit differs only in weight. Concept went from "the twist lands" to "the caption explains it".
- **Recentred subject** (A14 above). Tension fell with it.
- **Frame pressure.** r03 cropped the disc at the left margin with intent. r04 leaves it 3.7–4.1 mm inside the frame on three sides, which reads as crowding rather than a crop.
- **The caption grew from 5 lines to 11** and now takes 43.5 of the 65 plot minutes. The sheet is sliding toward "the scientific figure" (known failure mode 7): the explanation is doing work the drawing should do.
- Gains to keep: travel is down from 6.6 m to 3.0 m and draw from 21.1 m to 12.4 m. The sun no longer floods, labels clear the geometry, and the question is correctly reworded and disclosed.

### DESCRIPTION.md § Keep (written for r01)
- Central system as the dominant mass: **still true**. The disc wins at 3 m.
- Asymmetric satellite placement around a centred sun: **no longer true**. There are no satellites, and the only asymmetry left is the type.
- Big dotted enclosing orbit tying the field: **gone**. There are no dotted runs at all (a C5 trade-off, but the canon's glyph markers went with it).
- Economy and scarce distinct colour: **partly true**. There are 3 pens and 12.4 m of ink and crimson is scarce, but blue carries the whole sheet at full saturation.
- Engraver's furniture on shared verticals: **gone** (accepted since r03).
