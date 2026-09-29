# Art critique — orrery r02 · canon: UNDECLARED (lineage Cellarius, *Harmonia Macrocosmica*; judged as orbital / radial data-viz) · 2026-09-28
render: gallery/studio/orrery/current/pp_orrery_orbits-that-mean_v13.png (gcode beside it, audited: 22 354 cmds, 5 layers)

## Scores
| # | dimension | score | note |
|---|---|---|---|
| 1 | hierarchy | 7 | The black sun (Ø104 mm) wins at 3 m. K (r 25.5) and V (r 22) are a clear second tier, Q (r 11) and Z third. Sun to K is only about 2:1, and the title is a hairline. |
| 2 | grid & alignment | 6 | Title, sun, star, Z, `Z = AV` and the footer share x = 105, and the systems sit on one orbit. The Q/K/V letters sit in a different place relative to each hub. `itself` and `transformer` land on geometry. The legend floats at (37–100, 35–45) with no edge to hang on. |
| 3 | tension & asymmetry | 5 | Everything structural hangs on the page's centre axis: title, sun, Z and footer are all centred. The only tension comes from the planet sizes (heavy right, light left), and the lineage does not buy symmetry because no canon is declared. |
| 4 | negative space | 4 | The lower-left quadrant (x 15–95, y 20–110) is leftover space holding a 3-line legend. Crowding by collision: the K system's lower half is a knot of blue hairlines, dots, ring, the dashed orbit and a label. The Q exit is a knot of 7 hairlines plus `itself`. The Z epicycles (three circles, r 1–2 mm) touch the green rim and the star. |
| 5 | craft for pen | 5 | 5 pens, one clean layer each, ordered light to dark, 660 cycles, about 43 min. But: same-pen near-parallel runs under 0.75 mm total 164 of 559 mm in crimson, 199 of 1136 in blue and 124 of 1472 in ochre, all at the fan roots. Black groove-to-arc gaps are 0.5 mm at r ≈ 28, 31, 34, 38 and 50. There are 29 lift/drops at a single point (blots mid-line: 9 at the Z epicycle start, 5 in a run on a groove at (147–153, 146–155)). Travel inside a layer crosses the sheet twice: blue (131,15)→(164,197) at 184 mm and crimson (154,15)→(141,201) at 187 mm, both from the footer underlines. The spiral seams show as radial stair-steps at the sun's 3 o'clock. |
| 6 | concept legibility | 4 | The data is real, but the plate reads as a labelled textbook diagram: planets named Q/K/V/Z, wired by threads to a hub marked `Q•Kᵀ softmax`, with `Z = AV` printed under it. The softmax lives in grooves nobody can count at 1 m. Nothing visible carries the sun's output into Z: the ochre goes V→Z directly, so the A in AV is not drawn. The joke is in the caption, not in the plate. |
| 7 | depth & dimensionality | 3 | Flat circles on a flat page, and the flatness is not declared. The only overlap is the ribbons being clipped at Z's rim. The dashed orbit runs straight through the K and V hubs with no over/under. Cellarius's order is nested orbits in perspective, and none of that has been taken. |

**avg 4.86 · min 3 · VERDICT: FAIL**

## Reads at a glance
At 3 m a stranger sees a black vinyl record in the middle of an infographic, with three coloured targets and a green one strung on a dashed circle and wired to it by coloured threads.

## Acceptance checks
There is no `encoding.md` or `BRIEF.md`, so there is no §11. These are the encodings and constraints HANDOFF declares, checked against the gcode:
- 1 ochre ribbon = 5 % attention: 18 ribbons (90 %, the remainder under 5 %). PASS
- 1 groove turn = 5 %: 19.8 turns ≈ 100 %. PASS
- Layer order 0→4, light→dark, each pen entered once: PASS
- Batching, no sheet-crossing travel between consecutive strokes: FAIL (blue 184 mm, crimson 187 mm, both from the footer underline to the planet)
- Spacing ≥ 0.8 mm: FAIL (the fan roots in crimson, blue and ochre; black arcs 0.5 mm off the grooves)
- Canon named in HANDOFF: FAIL (lineage only)
- Flatness declared: FAIL

AUTHORING §6 (reference `studio/orrery/ref/reference.png`, judged as an interpretation):
1. Main forms recognisable without colour fills: PASS (sun, four systems, orbit).
2. Shadow lines follow the surface: FAIL. There is no surface or volume grammar at all.
3. Fine lines that are two sides of one thick stroke: PASS. The only doubled line is the deliberate double-passed r = 52 ring.
4. Blackest regions intended: PARTIAL. The groove band is intended; the knots at the Q exit and the V ribbon root are accidental congestion.
5. Labels readable at real pen width: FAIL. `itself` sits on the crimson fan origin, and `transformer` sits on the blue ring and the dashed orbit.
6. Thick-pen knots: FAIL. The Q fan origin at (46,211); the Z epicycles plus star at (105–110, 90–97); the V dots riding the rings.
7. Wasted travel or tiny marks: FAIL. Travel is 5.13 m against 11.23 m of draw (46 %), with 29 zero-length lift/drops, 196 two-point strokes, and the two sheet-crossing travels above.
- Lineage test: it would not hold hung beside a Cellarius plate. It borrows the "sun + satellites" surface and none of the order (tilted, nested, occluding orbits).

## Biggest weakness
It is a flat, centred, labelled diagram in orrery costume. The data is exact, but the form is still wires between named circles on one page axis. The orbital order the lineage offers (orbits in perspective, near bodies passing in front of the sun and far bodies behind it) is exactly what would turn it from a figure into a plate, and it is absent.

## Mandates
1. **Tilt the head's orbit into a Cellarius ellipse and let it occlude.** Redraw the dashed orbit as an ellipse about 170 × 70 mm, centred on the sun. Scale each system by its depth on the ellipse: near side about 1.3×, far side about 0.7×. The near-side system(s) are drawn OVER the sun's rim, which is cut behind them. Far-side systems and the orbit dashes stop at the sun's edge. Test: the orbit is an ellipse; at least one satellite occludes the sun rim; zero orbit dashes cross the black disc; the dashed orbit no longer runs through any hub disc.
2. **Unknot the fans and fix the craft.** Spread each bundle's departures along its hub's outer ring over ≥ 20° of arc: the crimson origin at (46,211), the blue root at (150–185, 195–210) and the ochre root at (180–195, 60–90). Audit: no two same-pen hairlines closer than 0.8 mm for more than 2 mm. Keep black arcs ≥ 0.8 mm off the grooves. Give `itself` and `transformer` a ≥ 2 mm halo. Draw the two footer underlines as the last stroke of their layers so no travel inside a layer exceeds 80 mm. Merge the 29 zero-length lift/drops.
3. **Break the centre axis and shape the empty quadrant.** Move the sun and orbit about 15 mm left so the orbit crops at the left margin near y ≈ 150. Set the title, legend and footer flush-left on one vertical, the Q hub axis. Nothing structural may sit on x = 105. Draw the sun→Z path: the ochre ribbons pass through the groove band before falling into Z, so A visibly acts on V. Test: title, legend and footer share one left edge; the lower-left quadrant is either cropped orbit or deliberate void with no floating type; every ochre line reaching Z has touched the black disc.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | n/a | No `LEDGER.md` or `FEEDBACK.md` exists for orrery, so there are no open A*/J* mandates. For context, DESCRIPTION's "If only iterating" items: (1) curved V bundle: PARTIAL, the ribbons curve now but run V→Z, not sun→V; (2) kill the letterbox: FIXED, title at y 275 and footer at y 18; (3) centred dot in `Q•Kᵀ` and lowercase `softmax`: FIXED, though neither has a halo. |

**DESCRIPTION § Keep:**
- Central system as the dominant mass: STILL TRUE, stronger (Ø104 vs Ø82 mm).
- Asymmetric satellite placement: STILL TRUE, and now data-sized (Q small, K large).
- Enclosing dotted orbit ties the systems: PARTIAL. It is now heavy black dashes that run through the K and V hub discs.
- Economy and scarce colour: PARTIAL. Cycles fell from 1 900 to 660 and travel from 7.4 to 5.1 m, but ink rose from 7.7 to 11.2 m and ochre is now a mass, not scarce.
- Engraver's furniture (stars on hub verticals, moons, shared verticals): REGRESSED. Moons, hub stars, the dash-dot axis, the centreline and the title rule are all gone. One star remains.

## Regressions vs compare-to
- The engraving vocabulary was stripped (moons with hatched phase, stars on hub verticals, dash-dot horizontal axis, dotted centreline, title rule). That vocabulary was v6's link to the lineage, and without it the plate reads as an infographic.
- The sun went from layered, airy hairline rings with nodes (v6's closest thing to depth) to a flat black record, with seam stair-steps at 3 o'clock.
- The Z output stem is gone. v6's green wineglass carried the sun into Z; now nothing connects the sun to Z.
- The enclosing orbit went from a fine dotted line to a heavy dashed one that collides with the hubs.
- New label collisions (`itself`, `transformer`) and new ink knots (Q fan origin, Z epicycles against the star).
- A new empty lower-left quadrant replaces v6's moons and sight line, which occupied it.
