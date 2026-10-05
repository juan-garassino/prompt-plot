# Art critique — resonance r05 · canon: none assigned (faithful reproduction of the reference poster; lineage Thomas Young, Plate XX Fig. 267) · 2026-09-28
render: gallery/studio/resonance/current/pp_resonance_benchmark_kept_v7.png (+ .gcode, measured directly: 6 contiguous colour layers, 1,960 strokes, draw 9.97 m, travel 9.21 m)

## Scores

| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 6 | The black interference core reads first at 3 m. But it is only ~75 mm across (x 71–146), about the same weight as each Q/K packet stack and the Z packet, so the second tier is crowded and there is no clear third tier. |
| 2 | grid & alignment | 6 | The Q/K rails, node columns and the ∂L ladder (x≈25, x≈58) share axes. The right-hand ∂L labels sit on no common edge (∂L/∂Y x≈188, the others x≈195), and content runs from x 18 to x 196, so the side margins are uneven (18 vs 14 mm). |
| 3 | tension & asymmetry | 5 | Title, fraction, core and softmax are all centred, and the top half is a mirror of itself. Only the lower half (Z left, MoE/V right) breaks the symmetry, and no canon licenses that symmetry here. |
| 4 | negative space | 4 | The only quiet zones are the margins. The lower half is a web of dotted curves. Collisions: the V rows 2 and 3 carriers run through each other (x 140–150, y 118–132). The backprop fans cut through the router/"router" label (x 88–110, y 60–80). The dotted-ellipse dots sit on the solid rings. |
| 5 | craft for pen | 5 | Good: layers are clean and ordered light to dark, and lens arcs are about 1 mm apart at 0.35 mm nib. Problems: the crosshatch lens ends on a toothed horizontal seam about ±9 mm off the axis. Dots land on rings and form knots. Same-pen ink crosses ink in V. Three taps under the Z rail dangle (x≈67/74/80). 1,179 of 1,960 pen cycles are 0.45–0.5 mm micro-dashes. There are 10 in-layer travel jumps over 80 mm (black max 285 mm, blue 246 mm). |
| 6 | concept legibility | 3 | NO SCHEMATICS. The plate is a labelled pipeline: Q,K → QKᵀ/√d_k → softmax → Z=AV → router/experts/top-2 → Y, plus a ∂L/∂· legend ladder. It could go straight into a slide deck. Young's interfering rings are the one abstract order, and they cover about 15 % of the sheet. |
| 7 | depth & dimensionality | 4 | Flat, and the HANDOFF does not declare it. One weight per pen, and nothing reads as near or far. The overlapping ring discs give only a little layering. |

avg **4.71** · min **3** · **VERDICT: FAIL**

## Reads at a glance
From 3 m: a colourful transformer-architecture diagram, with a black double bullseye in the middle and wave-packet rows feeding in from both top corners.

## Acceptance checks
There is no encoding.md, so there are no §11 checks. A reference is in play, so these are the AUTHORING §6 questions:

1. Main forms recognisable without colour? **PASS.** Labels and position carry Q/K/V/Z/Y.
2. Structure follows the form rather than a random mesh? **FAIL.** The crosshatch lens follows both crest families, but it stops on a toothed seam (teeth ~1 mm) above and below the axis band, and that seam reads as a cut in the mesh.
3. Fine lines that are really two sides of one thick stroke? **PASS.** The heavy letters are deliberate multi-pass weight.
4. Blackest regions intended? **FAIL.** The core is intended. The V pile-up (rows 2/3) and the dot-on-ring knots inside both discs are accidental.
5. Labels readable at real pen width? **PASS**, with one exception: "router" is crossed by the gold/blue/black fans.
6. Thicker pen makes black knots? **FAIL.** Dotted-ellipse dots of 0.7–1 mm sitting on 0.35 mm rings merge into blobs, about 40 of them across the two discs.
7. Long empty travels or excess tiny marks? **FAIL.** Travel is 92 % of draw, there are 10 jumps over 80 mm, and 60 % of pen cycles are sub-mm micro-dashes that read as neither dots nor dashes.

As an interpretation of the reference it is faithful and honest for pen. The reference's grey tonal core became solid rings, the pale ghost experts became dotted lenses, and the arrowheads were dropped, as the house law requires. As a result it inherits every weakness the reference has as a schematic.

## Biggest weakness
The hero never takes over. Young's interference, the one thing on the sheet that is an order and not an apparatus, is a 75 mm figure boxed in by wiring. Its own surface is marred by a toothed hatch seam and by black dots dropped onto the rings, so even the part that should carry the plate reads as a crowded figure.

## Mandates
1. **Hero.** Scale the interference core to at least 105 mm across (now x 71–146, about 75 mm). Take the room from the Q/K stacks (70 %). No black dot may sit within 0.8 mm of a solid crest inside the two discs; clip the dotted ellipses/dot field outside the disc rims. The crosshatch lens must either run continuously through the axis band or end on one smooth boundary curve: no teeth at y≈158/176.
2. **Collisions.** Re-pitch the V rows so that no gold carrier crosses a neighbouring gold rail (row pitch ≥ tallest packet height + 1 mm; now 7 mm against ~12 mm packets at x 140–150). Route the gold/blue/black/green backprop fans so none of them enters the router/experts box x 95–160, y 55–95 or crosses the word "router". Delete the three dangling vertical taps under the Z rail at x≈67, 74, 80.
3. **Dotted lines (Juan's J1).** Every dotted path becomes round dots of one fixed size, a pen touch or tiny closed circle, never a 0.45–0.5 mm micro-dash. Dots sit at a constant 0.9–1.1 mm centre pitch, end-anchored so both ends carry a dot, with the same pitch family-wide. Converging leaders (Q/K fans, the ∂L rails) must stay ≥ 2 pitches apart. Test: on an isolated leader such as the ∂L/∂Q rail, the same-pen dot nearest-neighbour median is ≤ 1.1 mm. Pen cycles will rise; that is accepted. Fix the in-layer ordering so that no consecutive travel exceeds 80 mm.

## Follow-up on open mandates
There is no LEDGER.md. The open items are taken from FEEDBACK.md (J1) and from DESCRIPTION.md § Next versions 3 "benchmark-kept" plus the "if only iterating" list (D1–D5).

| id | status | evidence |
|---|---|---|
| J1 dotted lines "more continuous dots" | **REGRESSED** | Measured from the gcode: v13 dots were 0.39 mm marks at ~2.2 mm pitch (2,704 dots). v7 dots are 0.45–0.5 mm micro-dashes at 2.8 mm median, 3.4–3.7 mm per pen (1,179 dots). The dots got sparser and more dash-like, the opposite of the note. Pen cycles fell from 3,471 to 1,960, which is the dots-for-cycles trade Juan explicitly forbade. |
| D1 cut to 4 pens | **N/A (superseded)** | Juan (2026-09-28) lifted the pen cap in favour of layer discipline. The 6 layers are now contiguous and ordered light to dark: correct. |
| D2 remove seeded scatter dots from rings | **PARTIAL** | The stipple caps above and below the midpoint are gone. About 40 black dots still sit on the solid rings of both discs. |
| D3 ∂L/∂· stack at 1.5× pitch | **FIXED** | Fractions now sit on a 10 mm pitch (y 56/46/36/26/16), and no numerator touches the denominator above it. |
| D4 scale hero 1.5× | **NOT FIXED** | The hero is still x ≈ 71–146, the same as v13. |
| D5 shrink Q/K blocks to 70 % | **NOT FIXED** | The Q/K stacks are the same size and position as in v13. |

Keep items (DESCRIPTION § Keep):
- Hero construction "verbatim": **no longer true.** The midline changed from v13's two small diamond clusters to a large crosshatch lens. The field now reads more as one interference (good), but the change introduced the toothed seam.
- Q/K funnel as the one gestural shape: **weakened.** The sparser micro-dashes turn the ten-and-ten fans into dash scatter instead of drawn curves.
- Hero pen economy, open net with no flood: **still true.** Lens cells stay open at 0.35 mm.
- Packet vocabulary consistent: **still true.**
- MoE fork, 2 solid and 3 ghost lanes: **still true.** The ghost experts as dotted lenses are a fair pen reading.

## Regressions vs compare-to (v13)
- **Dotted lines** (J1, above): sparser and more dash-like than v13, directly against Juan's REWORK note.
- **Hero midline:** a new toothed seam where the enlarged crosshatch lens is cut back to a single family around the axis. v13's small diamond clusters had no visible seam.
- **Funnel gesture:** reads weaker because of the dot thinning.
- Unchanged, carried over from v13 and still open: the V row pile-up, the dangling taps under Z, the fans crossing the router, and the centred symmetric top half.
- Improvements: light-to-dark layer order; the ∂L stack is re-spaced; arrowheads dropped; travel down from 11.3 m to 9.2 m.
