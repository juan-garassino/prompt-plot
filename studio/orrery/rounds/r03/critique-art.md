# Art critique — orrery r03 · canon: UNDECLARED (lineage John Whitney Sr., *Permutations*; judged as orbital / Op-Art kinetic abstraction) · 2026-09-29
render: gallery/studio/orrery/current/pp_orrery_resonant-orbits_v14.png (gcode beside it, audited: 30 333 cmds, 722 strokes, 3 layers, draw 21.07 m, travel 6.63 m)

## Scores
| # | dimension | score | note |
|---|---|---|---|
| 1 | hierarchy | 7 | At 3 m the ring disc (Ø ≈ 210 mm, cropped at the left margin) wins, and the one bold closed orbit is a clear second. `RESONANT ORBITS` in bold caps is third, and the token column rewards 30 cm. But the query sun, the crimson heart of the idea, is only a Ø10 mm dot, so the scarce accent is under-scaled against 18.7 m of blue. |
| 2 | grid & alignment | 7 | The crimson spine sits at x = 70, the sun's axis. The words and the title/caption block share a left edge at x ≈ 72, and the weights are right-aligned at x ≈ 66 against the spine. The disc crops exactly on the left margin. The right edge of the disc (x ≈ 185) and the caption's right edge (x ≈ 180) share no line. |
| 3 | tension & asymmetry | 7 | The sun is at 1/3 width and the disc is cropped hard left. The text mass sits low-right under the disc. The plate is off-axis and holds. The only diagonal energy is the rings' own waviness. |
| 4 | negative space | 6 | The lower-left corner (x 10–68, y 10–60) and the right strip (x 185–200) are the quiet zones: acceptable, but more leftover than shaped. Inside the disc the density is uniform. Rings are at a constant ~7.5 mm pitch, every band fills a ~6 mm envelope, and the gaps are a constant 1.5–2 mm, so nothing inside the disc is quiet. The label corridor is crowding: 32 blue fragments 4–7 mm long hover over and between the words (e.g. above `hole`, `while`, `the`, `a`, `drew`), and glyph-to-orbit clearance is 0.72–0.87 mm at 25 type strokes. |
| 5 | craft for pen | 5 | Three pens, one clean layer each, ~70 min: fine. Braid crossings are clean, and no unintended same-pen parallels are under 0.8 mm. But: (a) the sun is a spiral at **0.47 mm pitch** (10.7 turns in r = 5 mm), which floods crimson; (b) the bold orbit is **4 passes at 0.25 mm offset**, over the 1–3-pass rule and a paper-pilling risk; (c) the blue layer has **23 inter-stroke travels > 60 mm, 13 > 100 mm, max 164 mm**, which breaks the batching rule directly; (d) the 32 crumbs of point (c) in dimension 4. |
| 6 | concept legibility | 7 | One orbit among thirteen closes into a clean bold line while the others fail to close and braid. The odd-one-out reads without the caption. The sentence column carries a real twist: the query is `itself`, the plate asks "what does itself refer to?", and the closed ring answers `transformer` (.557). The weights sum to 1.000, which is honest. But the MISS is weakly drawn. `.005 drew` and `.063 hole` sit in the same ~6 mm envelope and differ only in how the 4 strands interleave, so the distribution is invisible at 1 m. |
| 7 | depth & dimensionality | 5 | The braided strands read partly as twisted cable, which is some volume. There is no over/under, no occlusion and no weight falloff, and flatness is not declared in HANDOFF. |

**avg 6.29 · min 5 · VERDICT: FAIL**

## Reads at a glance
At 3 m a stranger sees a big blue target of braided rope rings around a small red dot, cropped at the left edge, with one ring drawn as a single bold wave and a column of words running down from the dot.

## Acceptance checks
There is no `encoding.md` or `BRIEF.md`, so there is no §11. These are the encodings and constraints HANDOFF declares, checked against the gcode:
- 13 causal keys shown, weights sum to 1: PASS (.114 … .012 = 1.000).
- Only the argmax orbit closes: PASS. The single bold ring (strokes 95/99/101/103 + 96) terminates at the `.557 transformer` row, y ≈ 84.
- Pen meanings (blue = keys, crimson = query sun/spine/question, black = type): PASS.
- Layer order 0→1→2, each pen entered once: PASS.
- Batching, no sheet-crossing travel between consecutive strokes: FAIL (blue has 13 travels > 100 mm).
- Spacing ≥ 0.8 mm / no floods: FAIL (sun spiral pitch 0.47 mm; the bold ring's 4 passes at 0.25 mm).
- Bounds: PASS (ink bbox x 10.0–185.1, y 21.5–279.6 on A4; no ink runs along the clip line).
- Seed invariance: not verified (the critic does not run the piece).
- Canon named in HANDOFF: FAIL (lineage only, second round running).
- Flatness declared: FAIL.

AUTHORING §6 (reference `studio/orrery/ref/reference.png`, judged as an interpretation; this is the abstract thesis, so only the orbital order is owed):
1. Main forms recognisable without colour: PASS (disc of orbits, sun, spine).
2. Shadow lines follow the surface: PARTIAL. Strands follow their orbit, but there is no volume grammar.
3. Fine lines that are two sides of one thick stroke: PASS. The bold ring's 4 offset passes are deliberate weight, and they merge.
4. Blackest regions intended: PARTIAL. The bold ring is intended; the sun floods below the pitch floor.
5. Labels readable at real pen width: FAIL. At 0.72–0.87 mm clearance, blue arcs touch `hole`, `the`, `transformer` and `itself` at a 0.5 mm nib.
6. Thick-pen knots: PARTIAL. The 4-strand braid pinch points converge at shallow angles and will pool with a POSCA.
7. Long empty travels or tiny marks: FAIL. 13 blue travels > 100 mm, and 32 blue fragments of 4–7 mm with no visible benefit.
- Lineage test (beside Whitney's *Permutations*): half-held. The order is genuinely Whitney's: a figure appears only at whole-number ratio. But Whitney's non-resonant states are open clouds that make the resonant figure snap. Here the misses are a tidy, uniform cable texture of equal width, so the snap is carried by line weight, not by the dynamics.

## Biggest weakness
The disc is wallpaper. Thirteen bands sit at a constant ~7.5 mm pitch in a constant ~6 mm envelope, so the one quantity the plate exists to show (how far each key misses) changes only the internal braid phase and never the space a band takes. The attention distribution (.557 vs .005) is invisible at 1 m, and the disc has no quiet interior to make the closed orbit ring out.

## Mandates
1. **Let the miss take space.** Make each non-resonant band's envelope width grow with its dot-product shortfall, keeping the mapping exact and stated in NOTES. Near-best keys (`.114 The`, `.063 hole`, `.062 watched`) should be ≤ 2 mm tight cables and the worst (`.005 drew`, `.006 a`) should be ≥ 6 mm open annuli, with the freed radius left as bare paper between bands. Test: on a ray from the sun at 3 o'clock, the widest/narrowest band envelope is ≥ 3:1, and at least two inter-band gaps are ≥ 4 mm.
2. **Fix the pen craft and the batching.** (a) Redraw the sun as a spiral at ≥ 0.8 mm pitch and enlarge it to Ø ≥ 18 mm so the scarce crimson wins at 3 m. (b) Draw the bold resonant orbit as 3 passes at ≥ 0.3 mm offset, not 4 at 0.25 mm. (c) Reorder the blue layer spatially so no inter-stroke travel exceeds 60 mm; it is now 23 > 60 mm and max 164 mm. Test: all three are measurable in the gcode.
3. **Cut a clean label slot.** End every orbit on two chord lines either side of the token column, e.g. x ≈ 55 and x ≈ 90, with a ≥ 2 mm halo around every glyph. Delete every blue stroke shorter than 8 mm; there are 32 now, 4–7 mm, all in x 61–85. Also add `canon:` and a `flat: declared — <reason>` line to HANDOFF, or give the braids an over/under. Test: zero blue ink within 2 mm of any glyph, zero blue strokes < 8 mm, and HANDOFF names a canon.

## Follow-up on open mandates
There is no `LEDGER.md` or `FEEDBACK.md` for orrery, so there are no A*/J* ids. The r02 art mandates were written for the other thesis (`orbits-that-mean`). They are carried here where they still apply:
| id | status | evidence |
|---|---|---|
| r02-M1 tilt the orbit into an occluding ellipse | NOT FIXED (superseded) | The thesis changed to face-on rings; there is still no occlusion anywhere, and depth scores 5. |
| r02-M2 craft: parallels < 0.8, 2 mm label halo, no travel > 80 mm, no zero-length lifts | PARTIAL | Unintended same-pen parallels are gone. The halo is 0.72 mm, not 2 mm. Blue travel reaches 164 mm (13 > 100 mm). The sun floods at 0.47 mm pitch. |
| r02-M3 break the centre axis, flush-left type column, shape the lower-left | PARTIAL | FIXED: the axis is broken (sun at x = 70, crop at the left margin), and the title and caption are flush-left on the word column. NOT FIXED: the lower-left (x 10–68, y 10–60) is still leftover void. |

**DESCRIPTION § Keep** (written about v6):
- Central system as the dominant mass: PARTIAL. The ring disc dominates, but the "sun" itself shrank from an Ø82 mm system to an Ø10 mm dot.
- Asymmetric satellite placement: GONE (thesis change); the asymmetry now comes from the crop.
- Enclosing dotted orbit tying the field: GONE. Every ring now is the orbit, which is acceptable for this thesis.
- Economy and scarce colour: PARTIAL. Crimson is scarce and loud (396 mm), pens dropped 5→3, and travel fell 7.45→6.63 m. But ink rose 7.7→21.1 m, and blue alone takes 43.6 min.
- Engraver's furniture on shared verticals: GONE. The spine and the flush-left column are the only shared verticals left.
- DESCRIPTION's resonant-orbits spec ("closes, or fills an annulus"): PARTIAL. It closes; it never fills an annulus (see mandate 1).

## Regressions vs compare-to
Compare-to: `gallery/studio/orrery/current/pp_orrery_v6.png`.
- Ink is 2.7× v6 (21.1 m vs 7.7 m), almost all of it one uniform blue texture. v6's hairline economy is gone.
- The query/sun lost its presence: Ø10 mm, and flooded at 0.47 mm pitch, against v6's airy Ø82 mm ring system.
- Labels are grazing geometry again (0.72 mm clearance plus 32 crumbs), the same failure r02 flagged at `itself` and `transformer`, now across the whole column.
- In-layer sheet-crossing travel got worse: 13 blue travels > 100 mm, where r02 had 2.
- Improved vs v6/r02: the title is real display weight instead of hairline caps, the axis is broken, the data is exact and the twist lands in the plate itself, and there are 3 pens instead of 5.
