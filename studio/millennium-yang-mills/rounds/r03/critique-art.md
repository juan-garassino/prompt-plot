# Art critique — millennium-yang-mills r03 · canon: Bauhaus (Kandinsky, *Punkt und Linie zu Fläche*) · abstract thesis · 2026-09-29
render: gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_iterate_v7.png (physical-width preview `_v7_phys.png` judged for tone; gcode `_v7.gcode` parsed for the measurements below)

## Scores
| # | dimension | score | note |
|---|---|---|---|
| 1 | hierarchy | 8 | There are three clear weights. The ruled plane is the mass, the red L (bar plus 0++ curve) is the accent, and the Ø9.2 disc is now a real full-stop that counterweighs the plane from the bottom-left. The shells sit third. The type load pulls against this: there are 13 lines of explanation (3 in the statement, 7 in the key, 3 in the colophon), where r02 had 7. |
| 2 | grid & alignment | 8 | The spine x=40 carries the title, statement, strata, shells, red bar and disc. The x=262 stop cuts every element, and the tags hang flush-left at 265. The key block is flush-right at 282. The colophon is still on x=15, off the spine grid. The Δ glyph floats at x≈27–37 in its own column. |
| 3 | tension & asymmetry | 8 | The ghost diagonal drives the plate: mass upper-left, open spacelike void lower-right, and the sheaf of lines all leaning one way. The right-edge comb of r02 is gone. The 7-line key parked in the far corner of the void takes some of the tension out of the diagonal's destination. |
| 4 | negative space | 7 | The lens is clean and has a shape (cone below, red above), and it is the strongest passage on the sheet. The quiet zone now carries a 7-line text wall reaching y≈52, level with the vacuum. The statement's lowest ink is at y=379.1, 9.1 mm above the plane top (370), so title, statement and plane stack into one crowded band. |
| 5 | craft for pen | 7 | Strata pitch is 1.00 mm, cone dashes are 6.05/4.04, there are 3 swaps, and red clears the disc. Shell/tag spacing at the stop is ≥ 2.8 mm. Two faults. (a) The `*` in `0++*` and in the caption's `2++*` is drawn at the same size and height as the `+` before it, so it reads "0+++" at the proof scale and at arm's length. (b) The lowest strata still run tangent into the rim near its vertex: the y=251 stratum is 0.75 mm off the rim at x=50 and 0.44 mm at x=55, which thickens the rim over x 40–60. The disc is a Ø9.2 spiral with the 0.3 nib and shows pinholes in the phys preview, which is acceptable. TEXT is now 44 min of an 86-min job. |
| 6 | concept legibility | 7 | Point / line / plane reads at once, with no axis furniture: the tags are at the line ends, the disc is its own element, and the bar is the measure. The silence has a shape. It still reads as a chart in two ways. The 7-line key ("THE POINT: … EACH LINE: … RED LINE: … RULED PLANE: …") is a legend in everything but the box. And the 0.1 grey cone, the object the twist hijacks, is the weakest mark on the sheet. |
| 7 | depth & dimensionality | 7 | Flat by declaration (§1). The weights now make planes: ghost 0.1 dashed behind, the 0.2 tonal field, the 0.3 lines, the 0.5 red, and the solid disc on top. The 0-D/1-D/2-D ladder carries the layering. |

**avg 7.43 · min 7 · VERDICT: FAIL** (avg < 8)

## Reads at a glance
At 3 m you see a ruled grey-black block top-left whose lower edge sweeps up to the right, a sheaf of fine curves under it, a red stem-and-curve rising from a heavy black dot, a faint dashed diagonal, and a wide empty wedge, framed by more text than the image needs.

## Acceptance checks (encoding §11; measured on the gcode)
1. **EMPTY TIP: PASS.** I clipped every G1 against {|p| < E < √(p²+1)}, origin (40,50), s=100. There are 0 black or text segments inside. The only non-red hit is a grey dash lying on E=|p| itself (the lower boundary, numerical). The lens holds only the red bar. The Δ glyph is outside the half-section.
2. **ONE-TO-ONE: PASS.** Vacuum 50 → red vertex 150 → rim vertex 250 gives 100 : 100. The ruling runs (40,50)→(262,272), which is exactly 45°.
3. **IRREGULAR STAFF: PASS.** The black vertices sit at y 193.7 / 204.9 / 221.9 / 228.1 / 235.6, which is +43.7 / 54.9 / 71.9 / 78.1 / 85.6 above red. The gaps are visibly unequal, and the tightest pair stays two lines to the stop.
4. **PLANE ON THE RIM: PASS.** The strata start 1.0 mm above the rim vertex. There is no stratum below the rim or between shells. In the phys preview the plane is the darkest mass at 3 m. (See the craft note on tangency near the vertex.)
5. **NOTHING ON THE CONE: PASS.** No black or red ink lies within 0.5 mm of the ruling. At x=262 the red is at y=293.5 and the ruling at 272.0, a 21.5 mm gap (≥ 18). There is one red group, the lens is enclosed, and the spacelike field is open. (Four colophon strokes near (15,25) touch the cone's extension *below* the apex, E<0, where no ruling is drawn. That is harmless, but it is a coincidence worth avoiding.)

AUTHORING §6 (reference = interpretation brief):
1. Main forms read without fills: YES.
2. Shadow follows surface: N/A (flat). The strata run cross-grain to the shells, as specified.
3. Fine lines doubling a thick stroke: NO. The red bar is a deliberate solid.
4. Blackest regions intended: YES (plane, disc). The one accidental thickening is the rim over x 40–60.
5. Labels readable at true width: MOSTLY. The `*` merges into "+++".
6. Thick-pen knots: none. The disc is the one sanctioned solid.
7. Long empty travel or pointless tiny marks: travel grew to 5.2 m, mostly in TEXT. There are no pointless marks.

Against the reference, the architecture is kept (upper mass, silent middle, red Δ measure, point below), and the reference's ornament is correctly cut.

## Biggest weakness
**The plate is over-captioned.** The science fixes arrived as volume. The statement is now three lines, 9 mm off the plane top, and the corner caption has become a 7-line key that walks the viewer through each element ("THE POINT: … EACH LINE: … RED LINE: … RULED PLANE: …"). That is a legend without a box (§4, §9.8), and it sits in the quiet zone the diagonal points into. The geometry now reads as Kandinsky on its own, and the text is dragging it back to "annotated figure".

## Mandates
1. **Compress the bottom-right key to ≤ 4 lines, with its top ink at y ≤ 40** (below the disc's lower edge at 45.4). Keep S1's words by merging, e.g. `POINT: THE VACUUM. LINES: GLUEBALLS, MASS AT THE LEFT END. RED: 0++, MASS Δ.` / `RULED PLANE: GLUEBALL PAIRS, FROM EXACTLY 2Δ.` / `HEIGHT ENERGY, WIDTH MOMENTUM, ONE SCALE. PURE SU(3). ATHENODOROU-TEPER 2020.` / `2++* LIES ON 2Δ WITHIN ERRORS. STATES ABOVE 2Δ OMITTED.`. Test: count the lines. The max y of text ink with x > 150 and y < 100 is ≤ 40, and its last baseline equals the colophon's last baseline.
2. **Cut the statement to ≤ 2 lines and open the band above the plane.** Keep S2's twist, e.g. `CLASSICAL WAVES RUN AT LIGHT SPEED, ON THE DASHED LINE. THE QUANTUM THEORY PUTS NO STATE THERE.` / `THE CONE HOLDS ONLY ITS TIP, THE VACUUM. THEN NOTHING, UP TO Δ.`. Test: the min y of statement ink is ≥ 384 (≥ 14 mm clear of the plane top at 370), and the TEXT layer estimate is ≤ 32 min.
3. **Make the `*` unmistakable from `+`** in the `0++*` tag and in the caption's `2++*`. Draw it as a 6-arm star (3 strokes at 90°/30°/150°, no horizontal arm) that is ≥ 1.2× the `+` height, with ≥ 0.8 mm clear after the preceding `+`. Test: on a 25 % downsample of the phys preview, the tag reads "0++*" and not "0+++". Decode the tag's strokes from the gcode and show that none of the `*` strokes is horizontal.

Polish carried (not a mandate this round): A7, the strata tangent to the rim over x 40–60.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| A1 | FIXED | The disc is Ø9.2 (r=4.60) at (40,50), a spiral in the 0.3 nib. That is ≈ 7× the 1.3 mm bar width, and at 3 m it is the third element opposite the plane, not the bar's foot. The bar and cone start at its edge, and 1:1 is measured from its centre. |
| A2 | FIXED | Every element stops at x=262, and the tags are flush-left at 265 on their own line ends. There is zero glyph ink left of x=40 in y 140–260 (the Δ glyph is at y≈95–105). The comb at the frame is gone, and 0++ is untagged. |
| A3 | FIXED | 31 grey dashes at 6.05–6.07 mm with 4.04 mm gaps. The first dash starts at the disc edge (43.4,53.4). |
| A4 | FIXED (at threshold) | Concept legibility went from 5 to 7. The axis read is gone. The remaining "figure" pull is the text key (mandate 1), not the hyperbola family, so the translator watch does **not** fire. |
| A5 | FIXED | `phys_preview_v7.png` was shipped (nib widths on cream), and the strata read as tone, not a slab. |
| A7 | NOT FIXED | The y=251 stratum ends at x=56.86, 0.44 mm above the rim at x=55 and 0.75 mm at x=50. The rim still reads thickened over x 40–60. |
| S1 | FIXED (science) — art cost | "GLUEBALL" and "PAIR" appear, and each carrier is named. It was delivered as a 7-line key, which is the regression below. |
| S2 | FIXED (science) — art cost | The statement now carries the twist (light speed, dashed line, no massless gluon). It grew to 3 lines, 9 mm off the plane. |
| S3 | PARTIAL | The superscripts are ≈ 1.4–1.6 mm, the sign gaps are ≈ 0.8 mm, and `⁻⁺` no longer fuses. The `*` is still read as a third `+` in both `0++*` and `2++*` (mandate 3). |
| S4 | FIXED | The caption reads "2++* LIES ON 2Δ WITHIN ERRORS". |

## Regressions vs compare-to (r02, `pp_millennium_yang_mills_abstract_v7.png`)
- **Text volume doubled.** The statement went from 1 line to 3, and the corner caption from 4 lines to 7. The TEXT layer went from 21.2 to 44.3 min, and the total job from ≈ 64 to ≈ 86 min. Travel went from 3.96 to 5.22 m. This is the direct cost of S1/S2 delivered as sentences.
- **The top band closed up.** In r02 the one-line statement sat ≈ 15 mm above the plane top. It now sits 9.1 mm above it, and the title, statement and plane read as one crowded block.
- **The quiet zone is occupied.** The r02 bottom-right caption topped out at y≈30. The r03 key climbs to y≈52, level with the vacuum, and fills the corner the diagonal aims at.
- Kept from r02, and not worse: the lens, the 1:1, the 45° diagonal, the plane mass, the spine grid, and the red scarcity (0.59 m of red against 20 m of black).
- There is no DESCRIPTION.md § Keep for this slug, so nothing to check there.
