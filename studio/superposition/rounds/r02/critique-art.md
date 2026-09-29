# Art critique — superposition r02 · canon: none assigned (lineage: Manfred Mohr, systems art) · 2026-09-29
render: gallery/studio/superposition/current/pp_superposition_SUPERPOSITION-COMPUTED_v15.png (checked against the gcode, re-rendered at 12 px/mm for the crops)

No encoding.md and no BRIEF.md exist for this slug, so HANDOFF is the only brief. No STYLES canon is
named, and the sheet is drawn in neutral hairline drafting. Rubric §6 says STYLE IS NOT OPTIONAL,
so the missing canon counts against the plate. It is judged against the HANDOFF's own lineage
(Mohr: "the rule IS the image").

## Scores
| dim | score | why |
|---|---|---|
| 1 hierarchy | 5 | The triangle is the biggest shape, but it is an empty hairline outline. At 3 m the crimson/blue bands and the gold V band are as loud as it is. Five stacked bands at similar weight, and all type at caption size. |
| 2 grid & alignment | 5 | Q/K sit in the top corners, V is on the left edge at y≈105, and Z = AV floats right at y≈37, so the station labels share no edge. Every band has a different left edge: Q x≈27, V x≈13, triangle x≈29, softmax x≈43, Z x≈53. Title and footer are centred hairline strips. |
| 3 tension & asymmetry | 4 | The whole plate is a centred top-to-bottom cascade: triangle apex on x=105, softmax centred, Z bell centred. Only the right-heavy contour cloud inside the triangle breaks the symmetry. This is student-work symmetry, and Mohr is not a symmetric canon. |
| 4 negative space | 5 | The quiet zones are leftovers, not shaped: x 10–45 / y 90–150 around a lonely "V", and x 150–200 / y 80–145. The gold V→Z strands stop in mid-air short of the bell, so that gap reads as running out of room. |
| 5 craft for pen | 6 | Layer discipline is good: 5 pens, each layer entered once, gold→blue→crimson→green→black, 1 123 cycles, 22.5 k commands. But the twin eye at (118–140, 155–180) has broken ghost arcs where two ring nests cross. The corner eye at (160–182, 141–152) is chopped by the triangle edge into crumbs. Contour pinches under 0.8 mm at (110–140, 160–200). 102 gold strokes are under 1.5 mm (dash crumbs on the V→Z strands). The Z partial-sum curves cross each other and start in mid-air. The black layer has a 241 mm sheet-crossing travel. |
| 6 concept legibility | 3 | It is the attention equation as a labelled pipeline: Q, K → Q·Kᵀ → softmax (with a 1/13 threshold) → V → Z = AV, joined by strands. It could go straight into a slide deck. The oscillator-eigenstate basis (the actual "superposition" twist) cannot be seen at a glance. The witty title sentence is 2 mm hairline and cannot be read beyond 50 cm. |
| 7 depth & dimensionality | 5 | Flat is declared. The hidden-line gaps in the Q/K ridge families give a little over/under, but nowhere else uses it (triangle, V, Z are pure flat line). The declared flatness does not do any work. |

avg **4.71** · min **3** · VERDICT: **FAIL**

## Reads at a glance
A tidy explainer diagram of transformer attention: red and blue wave bands rain dashes onto a triangle of little bullseyes, which drops to a row of spikes, a yellow wave band and a green bell.

## Acceptance checks
No encoding §11 exists. The HANDOFF declarations are checked instead:
- Lineage holds beside Mohr's *Cubic Limit*: **FAIL**. Mohr shows the rule with no annotation. Here the rule (projection onto oscillator eigenstates) is invisible and the stage labels do the explaining.
- Declared flat, depth by over/under only: **PASS** (declared, and gaps present on Q/K). The declaration is not exploited.
- Each pen has one stated meaning and gets one clean layer, light→dark: **PASS** (order 0,1,2,3,4, no re-entry).
- Layers stream well in batches: **PARTIAL**. Pens 1/2/3 have max intra-layer hops of 41/27/21 mm. Pen 0 has one 103 mm hop and pen 4 has a 241 mm sheet-crossing hop. Travel is 5.28 m against 6.78 m of draw.
- No run of tiny marks that isn't worth its cycles: **FAIL**. 102 gold strokes are under 1.5 mm on the V→Z strands.
- Spacing ≥ 0.8 mm, no floods: **FAIL**. Contour pinches in the merged eyes (110–140, 160–200).

AUTHORING §6 (reference: studio/superposition/ref/reference.png):
1. Main forms recognisable without fills: **PASS**.
2. Shadow lines follow the surface: **PASS**. The Q/K hidden-line gaps follow the front bumps.
3. Fine lines that are really two sides of one stroke: **PASS**, none.
4. Blackest regions intended: **FAIL**. The darkest spot is the twin eye's accidental tangle of crossing, broken ring fragments.
5. Labels readable at pen width: **PASS** for token names and Q/K/V. Title and footer (~2 mm) are marginal.
6. Thicker pen knots / filled eyes: **FAIL**. Sub-0.8 mm contour pinches will close under a 0.5 mm nib, and the filled dots over the softmax apexes nearly touch the spikes.
7. Long empty travels / excess tiny marks: **FAIL**. The 241 mm black hop and the 102 gold crumbs.

Interpretation vs the reference: the reference's organising idea is nested bells sharing centres, all on one spine. That idea has been swapped for rows of shifted single bumps with no spine. The data is now real, but the "superposition" that names the plate no longer reads.

## Biggest weakness
It is still the textbook figure of attention: five labelled stations stacked on a centred axis. The one thing the title promises (a vector drawn as a visible superposition of basis bumps, summed into Z) is not what the eye gets. The triangle, meant as the hero, is an empty outline with scattered bullseyes, so nothing dominates.

## Mandates
1. **Replace the pipeline with the five attended threads.** Delete the captions `Q·Kᵀ`, `softmax` and `1/13` and the dashed threshold. Draw each of the five selected tokens (hole, transformer, plot, ter, watched) as ONE unbroken strand in its own route: slice circle → its softmax spike → its V bump → landing ON the Z bell. The other V→Z strands must also touch the bell, with no gold stroke under 1.5 mm. Test: between the Q/K bands and the footer the only text is token names and `Z = AV`, and every gold strand ends on a green curve.
2. **Make the triangle the dominant, asymmetric mass by drawing the causal matrix as a right triangle.** Its vertical side sits on the left margin (x≈13, the same edge as the Q and V labels), its base spans ≥ 0.85 of the drawable width, and its apex sits top-left, not on x=105. Test: at thumbnail size the triangle is the darkest and largest element, and the sheet no longer mirrors about x=105.
3. **Re-contour the similarity field as one gradient-stepped field so every ring is continuous.** Two checks. First, the twin eye now at (118–140, 155–180) shows closed nested rings with no ghost arc fragments inside. Second, the corner eye stops cleanly on the triangle edge with no crumbs. Test: zero black stroke pairs closer than 0.8 mm inside the triangle, and no contour fragment under 3 mm.

## Follow-up on open mandates
There is no LEDGER.md or FEEDBACK.md for this slug, so no A*/J* mandates are open. Judged instead against DESCRIPTION.md "Weak" and "If only iterating":

| id | status | evidence |
|---|---|---|
| W-concept schematic | NOT FIXED | Still labelled stations Q, K, Q·Kᵀ, softmax, V, Z = AV on one axis. |
| W-curves carry no data | FIXED | GPT-2 L11 H8 on " itself". The footer equation carries real weights (.26 hole …). |
| W-symmetric | PARTIAL | Q/K no longer mirror each other and the contour cloud is right-heavy, but the cascade is still centred on x=105. |
| W-hierarchy (map 0.36 w) | PARTIAL | The triangle now spans ~0.8 of the width, but as an empty outline it does not dominate at 3 m. |
| W-stipple/debris, cost | FIXED | Wash and debris are gone. Commands 69 k → 22.5 k, travel 11.1 → 5.3 m. |
| W-third vortex | N/A | The field has been replaced. |
| W-flat undeclared | FIXED | Flatness is declared in HANDOFF. |
| iterate: enlarge map + off-axis | PARTIAL | Enlarged, but still on the axis. |

## Regressions vs compare-to
- **The two-eyed contour map (Keep #2, "best-crafted element") has REGRESSED.** Continuous evenly pitched nested rings have become scattered bullseyes, a twin eye with broken ghost arcs, and an edge-chopped corner eye with crumbs.
- **The vertical spine (Keep #1) is only PARTIAL.** The drawn axis and its open-ring stations are gone. The stack survives as five separate bands, and the mass/line alternation is weaker because the map is now an outline.
- **The connector fans (Keep #3) have REGRESSED.** They no longer leave, run and converge. Q/K strands are near-parallel rails that stop at the triangle edges without arriving anywhere (only the "itself" strand reaches the slice), so the "pour into" read is lost. The V→Z strands end short of the bell.
- **The superposition motif has REGRESSED.** The parent's nested bells sharing centres (Q, K, V and the Z bell's ~10 clean nested curves) became rows of single shifted bumps. The Z partial sums now cross each other and start in mid-air.
- Keep #4 (colour as provenance, black for operations): still true.
- Keep #5 (wide V band against narrow Z bell): still true.
- Real gains that must not be traded away in r03: computed data, 3× fewer commands, half the travel, clean 5-layer order.
