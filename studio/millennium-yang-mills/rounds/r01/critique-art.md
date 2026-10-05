# Art critique — millennium-yang-mills r01 (faithful) · canon: Bauhaus, Kandinsky branch (flat by declaration) · 2026-09-28
render: gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_faithful_v10.png (+ physical-width preview studio/millennium-yang-mills/rounds/r01/phys_preview_v10.png; gcode gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_faithful_v10.gcode measured for §11)

## Scores
| dim | score | note |
|---|---|---|
| 1 hierarchy | 8 | The plane dominates at 3 m. Red is a clear second, the shell band third. The vacuum point (Ø 3 mm) disappears at 3 m, so the bottom 40 % has no counterweight. |
| 2 grid & alignment | 7 | Title, statement, plane and left caption share x=15. The title's right end lines up with the plane and shell stop at x≈266, and x=282 carries the cone exit and the right caption. One break: the red 0++ runs past the x=266 stop to the frame, so its tag at x=269 floats 2 mm above the red line instead of sitting at its end. |
| 3 tension & asymmetry | 5 | Every curve is mirror-symmetric about x=122, which is only 26 mm (9 %) left of centre. The asymmetric crop is too timid to register. At 3 m the plate reads as a centred bowl on a stem over a V: a goblet. |
| 4 negative space | 8 | The lens is a shaped silence, closed by the cone below and the red above. The spacelike field stays open, so the two kinds of blank read as different. The quiet zone earns the plane's loudness. |
| 5 craft for pen | 8 | Strata are 1.0 mm apart on a 0.2 pen. The tightest shell pair is 3.8 mm. Strata stop on the rim with no strip, the plate needs 3 swaps, and travel is 4.4 m against 28 m of draw. Two minor issues: the right leg of the Δ glyph is 3 passes of the 0.5 red converging at the apex (small wet knot), and the 1 mm superscripts at 0.2 lose the `*` (the tag reads "0+++" and the caption reads "2***"). |
| 6 concept legibility | 4 | The gap lands at a glance: silence, then red, then lines, then a mass. But the form is the textbook spectral figure (Peskin & Schroeder Fig. 7.2: one-particle hyperbolae, shaded two-particle continuum, J^PC tags at the right ends) with the axes removed. The Kandinsky order is argued in the encoding but not visible. Point and line have no Kandinsky weight, and only the plane is transposed. |
| 7 depth & dimensionality | 7 | Flat by declaration, and the flatness serves the (p,E) plane. Depth comes from weight: 0.1 grey, then 0.2 plane, then 0.3 spectrum, then 0.5 red. Acceptable. |

avg 6.71 · min 4 · **VERDICT: FAIL**

## Reads at a glance
A stack of nested bowls under a ruled black block, with a red bowl standing on a thin red stem over a dashed V and a tiny dot: a chalice-shaped physics figure with a very clean empty middle.

## Acceptance checks
Encoding §11 (measured on the gcode, then confirmed on the png):
1. EMPTY TIP: **PASS**. When G1 segments are clipped to {|p|<E<√(p²+1)}, the only non-red ink inside is the vacuum disc at the apex, which the encoding allows. Red inside is the bar (61.9→101.3, 118.7→160.0) and the Δ glyph only. The 0++ tag sits outside, 2.06 mm above the red.
2. ONE-TO-ONE: **PASS**. Vacuum 60.0, red vertex 160.0, rim vertex 260.0, so 100 : 100. The cone dashes run at 135°/45° exactly.
3. IRREGULAR STAFF: **PASS**. Vertices sit at +43.73, 54.95, 71.95, 78.12 and 85.61 mm with visibly unequal gaps. The 0++*/1+- pair stays distinct (6.2 mm on the axis, 3.8 mm at the stop).
4. PLANE ON THE RIM: **PASS**. The first stratum is at 261 over a rim at 260 (equal to the pitch, so no strip). No strata appear below the rim, and the plane is the darkest mass.
5. NOTHING ON THE CONE: **PASS**. Cone ink starts 2.3 mm from the apex (0.8 mm clear of the disc). Red sits 28 mm above the ruling at the right frame and 39 mm above it at the left. There is one red group, and the lens is enclosed.

AUTHORING §6 (the reference as an interpretation brief):
1. Forms recognisable without fills: **PASS**.
2. Shade lines follow the surface: **PASS**. The strata are declared cross-grain iso-energy and do not follow the hyperbolae.
3. Double outlines of one thick stroke: **PASS**. None.
4. Blackest regions intended: **PASS**. The only black regions are the plane and the disc.
5. Labels readable at the true pen width: **FAIL**. The 1 mm superscripts at 0.2 lose the `*` (0++* reads 0+++, 2++* reads 2***).
6. Thick-pen knots: **PARTIAL**. The Δ glyph's right leg is 3 converging 0.5 passes, which leaves a red knot at the apex.
7. Empty travels / pointless tiny marks: **PASS**.

As an interpretation, it keeps the reference's architecture (dense top, silent middle, red Δ I-beam, bottom anchor) and correctly cuts the knots, orbits and field-line bump. What it loses is the reference's one strength: the upper zone as a *field of objects with presence*. The replacement is correct but reads as a chart.

## Biggest weakness
The plate is the textbook spectral figure centred on the sheet. Mirror-symmetric hyperbolae about a near-central axis, a V under a stem, and a tag column at the right ends all say "Fig. 7.2 without axes". The Kandinsky transposition claimed in the encoding happened only to the plane. The point has no weight, and the composition has no working diagonal.

## Mandates
1. **Move the p=0 axis (vacuum, red bar, all shell vertices) from x=122 to x ≤ 85.** Keep s = 100 mm/Δ, the 45° cone and 1 : 1 unchanged. The left cone ruling must then exit the left margin below y=130, and the plane becomes a mass that tapers from ~100 mm tall at the left edge to ~40 mm at the x=266 stop, so the rim becomes a rising diagonal instead of a centred bowl. Test: at 3 m the vertex column sits in the left third (x < 99), and no mirror partner of the bowl is visible inside the frame.
2. **Give the vacuum point Kandinsky weight: redraw it as a solid concentric-ring/spiral disc of Ø 9–10 mm** (0.3 black, ring pitch ≥ 0.45 mm, centre still exactly at E=0). The red bar and the cone dashes still start at its edge. Test: at 3 m the point reads as the plate's third element, a dark full-stop that counterweighs the plane, and it is no longer a pinprick. The 1 : 1 measure stays centre-to-vertex.
3. **Make the right-hand stop one rule.** End the red 0++ at the same x as the black shells (266 at the current axis, or its equivalent after mandate 1), and set its `0++` tag flush-left at stop+3 mm, vertically centred on the red end point. That leaves every tag centred on its own line's end with ≥ 2.5 mm clearance, and nothing but the cone crosses the tag column. At the same time, raise the superscripts to ≥ 1.3 mm and draw the `*` as a 3-stroke star so that `0++*` and the caption's `2++*` read correctly at 30 cm.

## Follow-up on open mandates
id | status | evidence
— | — | First round: no LEDGER.md, FEEDBACK.md or DESCRIPTION.md exists, so there are no open A*/J* mandates.

## Regressions vs compare-to
None to judge (compare-to: none, new plate). Against the reference, the plate is a gain on truth (no invented glueball shapes, exact gap) and a loss on presence (the upper zone is a chart, not a field of objects). Do not trade away any §11 PASS while executing mandate 1: the 1 : 1, the 45° and the empty lens must survive the shift.
