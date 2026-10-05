# Art critique — millennium-yang-mills r02 · canon: Bauhaus (Kandinsky, *Point and Line to Plane*) · abstract thesis · 2026-09-28
render: gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_abstract_v7.png (gcode `_v7.gcode` parsed for the measurements below)

## Scores
| # | dimension | score | note |
|---|---|---|---|
| 1 | hierarchy | 7 | The plane dominates, red comes second, the shells third. The **point** is lost: a Ø3 mm disc at the foot of a 1.3 mm red bar reads at 3 m as the bar's terminal blob, so Kandinsky's first element has no weight of its own. |
| 2 | grid & alignment | 8 | The spine x=40 carries the title, statement, strata, shells and red bar. The tags are right-aligned at x≈35.6. The colophon sits on x=15, off the spine grid. |
| 3 | tension & asymmetry | 8 | The ghost diagonal drives the plate, with the mass upper-left and the void lower-right. The right margin is a comb: 6 black shells, the red curve and 120 strata all guillotine on x=282. |
| 4 | negative space | 7 | The lens is clean and shaped (cone below, red above), and it is the best thing on the sheet. The x∈[15,40] strip is dead except for a lone Δ glyph, and the bottom band holds only two small captions. |
| 5 | craft for pen | 8 | Strata pitch is 1.00 mm, the tightest shell pair is 2.82 mm perpendicular (0++*/1+-), 3 swaps, and red stays off the disc (0.15 mm clear). Where each stratum meets the rim near its vertex, the gap between them falls under 0.8 mm for its last few mm. That leaves a thickened rim at x 40–57. The cone runs 9.0/3.0 mm dashes against the §4 spec of 6/4. |
| 6 | concept legibility | 5 | The point/line/plane order is present and the empty tip lands. But the plate is visibly the textbook spectral-condition figure (Glimm–Jaffe): mass hyperbola, ruled continuum above 2m, and cone. The J^PC tags stacked on the spine at the vertex heights read as y-axis tick labels, and the red bar as the y-axis. This is the "scientific figure" failure, one step from an axis plot. |
| 7 | depth & dimensionality | 6 | Flat by declaration (§1), and the 0-D/1-D/2-D ladder is a legitimate stand-in. The sheet still has no layering, no overlap and no weight play beyond strata vs line. |

**avg 7.00 · min 5 · VERDICT: FAIL**

## Reads at a glance
At 3 m you see a finely ruled black wedge top-left, a sheaf of curves sweeping to the upper right, and a red L (tall stem plus curve) over a faint dashed diagonal. It reads as a graph with its axes erased.

## Acceptance checks (encoding §11, measured on the gcode)
1. **EMPTY TIP: PASS.** Clipped against {0≤p<E<√(p²+1)}, the only non-red ink is the vacuum disc's own spiral straddling the apex, which is sanctioned. Text hits appear only at x<40 (outside the half-section). Red is limited to the bar (x 39.6/40.0/40.4, y 52.05→150) and the glyph.
2. **ONE-TO-ONE: PASS.** Vacuum 50 → red vertex 150 → rim 250 gives 100 : 100. The cone measures exactly 45.0°.
3. **IRREGULAR STAFF: PASS.** The vertices sit at +43.73 / 54.95 / 71.95 / 78.12 / 85.61 mm. The 0++*/1+- pair keeps a minimum 2.82 mm perpendicular gap and stays two lines.
4. **PLANE ON THE RIM: PASS.** There are 120 strata at 1.00 mm, each ending 0.29 mm above the rim, none below it and none between shells. It is the darkest mass (in the stock preview; no physical-width preview was supplied this round, unlike r01).
5. **NOTHING ON THE CONE: PASS.** No black or red ink touches the ruling. At the stop x=282 the red is at y=311.85 and the cone at 292.0, a vertical gap of 19.85 mm (≥ 18). There is one red group, and the lens is enclosed.

Additional deviation: the cone dash is 9.0 mm dash / 3.0 mm gap (29 dashes), where §4 specifies 6/4. That is 75 % duty, which reads near-solid at 3 m.

AUTHORING §6 (reference = interpretation brief):
1. Main forms are recognisable without fills: YES (point, shells, plane, cone).
2. Shadow lines follow the surface: N/A (flat). The strata correctly run cross-grain to the shells.
3. Fine lines as two sides of one thick stroke: NO. The 3-pass red bar is intended as one solid bar.
4. Blackest regions intended: YES (the plane). The one accidental thickening is the rim/strata tangency at x 40–57.
5. Labels readable at true pen width: YES, at 1.8 mm caps. The tag stack on the spine is legible but it is the axis read.
6. Thick-pen knots: none at corners. The bar foot fuses visually with the disc, giving a "point on a stem" read that echoes forbidden #5 in spirit.
7. Long empty travels or pointless tiny marks: none significant. The text layer carries most of the pen-lifts (1442 segs).

Against the reference: architecture kept (upper mass, silent middle, red Δ measure, point below). All the reference's lushness is gone, and what replaced it is a chart rather than a Kandinsky plate.

## Biggest weakness
It reads as the textbook energy-momentum spectrum figure. The J^PC tag stack sits on the spine at the vertex heights (x 26–36, y 150–250) and works as a y-axis scale. The heavy red bar is the y-axis stub, and the tiny vacuum disc is its foot. Together they turn Kandinsky's point/line/plane into "hyperbolae plotted on an axis, labels on the left". The abstract order is there, but the furniture declares "figure".

## Mandates
1. **Take the tags off the spine.** Move all seven tags (0++ … 2-+, 2Δ) to the right-stop tag column from §5A: stop the shells and the red at x=262 and set the tags flush-left at x=265, inside [265,282]. Verify by looking: zero black glyph ink left of x=40 between y=140 and y=260, and the right margin no longer shows a comb of line-ends cut at x=282.
2. **Make the point a point, not the foot of a red stem.** Enlarge the vacuum disc to Ø 6 mm (this amends encoding §4's Ø 3; it is still the only solid) and start the red bar at the new disc edge. Verify by downsampling the render to 10 % width: the black disc must read as a distinct element whose width is ≥ 4× the red bar's width. It must not read as a blob terminating the bar.
3. **Put the ghost back in the cone.** Restore the ruling to 6 mm dash / 4 mm gap per §4 (≈ 34 dashes, first dash at the disc edge). Verify in the gcode: every grey dash except the clipped last one is 6.0 ± 0.1 mm, the gaps are 4.0 ± 0.1 mm, and at 3 m the diagonal reads as broken rather than as a continuous grey rule along E=|p|.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | — | There is no LEDGER.md, FEEDBACK.md or DESCRIPTION.md for this slug, so no mandates are open. compare-to: none. r02 is the abstract thesis built in parallel with r01 (faithful), not a child of it. |

## Regressions vs compare-to
None assessable (new plate, compare-to: none). Process note: r01 shipped a physical-width preview (`phys_preview_v10.png`) because the stock preview draws the 0.2 mm strata as a slab. r02 did not, so the plane's 3 m tone is judged on the stock preview and is overstated.
