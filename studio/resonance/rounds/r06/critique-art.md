# Art critique — resonance r06 · canon: none assigned (faithful reproduction of the reference poster under J2; lineage Thomas Young 1807, Plate XX Fig. 267) · 2026-09-29
render: `gallery/studio/resonance/current/pp_resonance_iterate_v5.png` (+ `.gcode`, re-rendered by the critic from the gcode at 0.35 mm nib for the detail crops)

## Scores
| # | dimension | score | evidence |
|---|---|---|---|
| 1 | hierarchy | 7 | At 3 m the black ring pair is the one dark mass. The Q/K wings are clearly second and the Z / MoE / Y band third, with the ∂L notes paying off at 30 cm. The coloured packets are loud enough to compete with the hero in colour, which holds this at 7. |
| 2 | grid & alignment | 7 | Shared rails are real: the Q/K node columns, the ∂L node column at x≈58, and one axis (y≈75) carrying Z, router, MoE and Y. Left leaders and the ∂L column share x≈18. Faults: side margins are 18.1 vs 13.8 mm. The right-hand ∂L fraction bars start at x 185.6 / 180.6 / 181.6, so they share no edge. A three-dot stub floats above `Q·Kᵀ` at (105, 215–222). |
| 3 | tension & asymmetry | 5 | The top half mirrors itself (Q/K, a centred title, a centred fraction, a centred hero). Only V hanging off to the right and the Z-left / MoE-right split break the symmetry. No canon licenses that symmetry. |
| 4 | negative space | 5 | The top-centre void between the wings is shaped, and it is good. Below it, several overlaps are collisions rather than decisions: K rows 1/2 packet envelopes touch at (170, 247); V row-2 lobe tips land on V row-3's axis at x 152–162, y≈121; 11 gold link dots land on green packet ink; 9 green ∂L/∂Z dots cross the top expert packet and lane; the green line passes through the word `experts`; 2 dots touch `router`. A new 100 mm gold run at y≈108 fences off the band between softmax and `MoE`. |
| 5 | craft for pen | 7 | Dots are 0.2 mm touches at a median 1.00 mm pitch, the same in all six pens, and they read continuous at nib width. Ink coverage of 3 or more passes totals only about 4 mm². The six layers are contiguous, stream once each light→dark, and are never re-entered. The ∂L stack has clear air. Against that: two packet-envelope knots, about 67 fan dots within 0.6 mm of a neighbour where the Q/K fans braid near-tangent, and 70 % travel. The gcode's G1 feeds are F1200–F2600, not the F600 the HANDOFF estimate assumes, so confirm that the streamer clamps them. |
| 6 | concept legibility | 3 | NO SCHEMATICS. Outside the hero, this is a labelled transformer + MoE + backprop flowchart with arrowheads (`router`, `experts`, `top-2`, ∂L/∂·). It could sit in a slide deck. The hero does carry an INTERFERING order, but its overlap is a narrow seam: the nodal structure shows only as two small diamond clusters at the cusps, not as the hyperbolae across a broad overlap that make Young's figure. |
| 7 | depth & dimensionality | 6 | Flatness is declared in the HANDOFF ("reproduction of a flat plate diagram"). That is accepted, but the licence is the reference rather than a canon. There is some real layering: fans over rings, packets over rails, ghost lanes behind solid ones. |

**avg 5.71 · min 3 · VERDICT: FAIL**

## Reads at a glance
Two fused black bullseyes fed by red and blue fans of wave rows from the upper corners, sitting on top of a labelled green-and-violet flowchart.

## Acceptance checks
- encoding §11: **none**. There is no `encoding.md` or `BRIEF.md` for resonance (S0), so no §11 checks exist to run.
- AUTHORING §6, judged against `ref/attention-as-resonance.png` as an interpretation:
  1. Main forms recognisable without colour: **PASS**. The packets, ring nests, softmax peaks and fork all read in line alone.
  2. Shadow lines follow the surface, no random mesh: **PASS**. The crest loci are an ordered net (1.41 mm pitch, identical to v13).
  3. Any fine lines that are really two sides of one thick stroke: **PASS**. None.
  4. Blackest regions intended: **PASS**. The ring nests and the stipple caps are intended, and the caps no longer flood.
  5. Labels readable at real nib width: **PASS**. `softmax` has 0.91 mm clear and `Z = AV` 1.03 mm; `router` and `experts` are each grazed by about 2 dots.
  6. Thicker pen makes knots: **FAIL**. The K row 1/2 and V row 2/3 envelopes are in contact, the fans braid below 0.6 mm, and the bullseye centres fuse into blobs.
  7. Long empty travels or wasted tiny marks: **PASS**. Travel is 70 % with a longest hop of 88 mm (the Q/K → ∂L floors). About 4,300 dot cycles (~2.4 h) are earned, because continuity is the brief (J1).
- Lineage (Young, Plate XX Fig. 267): hung beside Young, the hero is a quotation with its overlap too narrow to show the nodal fan. The rest of the sheet answers a textbook, not Young.

## Biggest weakness
The schematic apparatus (dim 6) caps this plate under the rubric, and J2 locks that apparatus in, so it cannot PASS as designed. Juan has to rule on that. Within J2, the actionable weakness is the lower half, where overlap is a symptom. The re-aimed leaders land on ink: gold on the green packets, green through the top expert and the word `experts`. Stacked packet rows touch (K 1/2, V 2/3). The V connector has become a U-turn plus a 100 mm fence at y≈108.

## Mandates
1. **Re-land the gold links on bare axis.** Every softmax→Z gold link should end on a small open node on Z's axis, inside a carrier gap: x≈70–83 between the big packet's tail and the small packet, or x≈90–97 after it. Test: zero gold dots within 0.8 mm of green ink (now 11). Draw the V connector as one continuous sweep from V row 3's end to its target, with no reversal at x≈185–200 and no horizontal run longer than 30 mm (the y≈108 run is now ~100 mm).
2. **Separate the touching packet rows without deleting anything.** Move K row 1 and row 2 apart until the row-1 big packet's lower envelope (x≈165–175, y≈245) clears row 2's upper envelope by at least 1.5 mm. Do the same for V row 2's big packet against V row 3's axis and packet (x≈150–162, y≈121). Test: no packet ink within 1.5 mm of another row's ink, in any of the Q/K/V blocks.
3. **Keep the MoE fork and its labels clean.** End the black ∂L/∂A and green ∂L/∂Z return curves at the router node (≈100, 75) from below, as in the reference, instead of threading them through the router fan and the top expert packet up to y≈92–97. Test: zero non-violet dots within 0.5 mm of violet ink (now 11), and at least 1 mm of clear air around `router` and `experts`. While you are there, start the blue tap at x≈74 on Z's axis (y≈75), as red does, rather than in mid-air at y≈66.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| J1 | PARTIAL | The mark is right: a single 0.2 mm touch at 1.00 mm median pitch, the same in all six pens, reading continuous at nib width. It is never a dash (r10's `-` ticks are gone). The "converging paths ≥ 2 pitches" clause fails in the Q/K funnel braid, where about 67 dots sit within 0.6 mm of a neighbouring path. Only Juan closes it. |
| J2 | PARTIAL | Every named element is present: all packets, halos, scatter, leaders, MoE, six pens. But the dot fields are thinner than r10: 847 vs 1,614 hero dots, and the stipple caps 303 vs 684. That is the A13a fix, but it is thinning. The halo ellipses are now open C-arcs. The V connector is re-routed. Only Juan closes it. |
| A3 | FIXED | The ∂L/∂· stack is at ≈10 mm pitch with clear air between each denominator and the next numerator. r06 carries it. |
| A4 | PARTIAL | Travel is 70 % (r10 117 %). Layers are contiguous light→dark with stated minutes (my recount comes to ≈187 min). Blue 87.5 mm and crimson 88.2 mm hops are over 80 (claimed floors, plausible: Q/K rows → ∂L stubs). The batch table cannot be checked blind (it lives in NOTES). |
| A5 | PARTIAL | Red and gold taps now join their ∂L curves. The blue tap still starts in mid-air (x≈74, y≈66). V rows 2/3 still touch (x 152–162, y≈121). About 2 dots graze `router`, and the green line crosses `experts`. |
| A9 | FIXED | The HANDOFF declares "flat — a reproduction of a flat plate diagram". |
| A12 | NOT FIXED | Margins are 18.1 / 13.8 mm. The right ∂L bars start at 185.6 / 180.6 / 181.6 (deferred by lead). |
| A13 | PARTIAL | (a) FIXED: the caps are now separable dots, not mud. (b) PARTIAL: the flat chords and the right-hand stub are gone, but the halos are now open arcs where the reference draws whole ellipses. (c) FIXED: all field marks are round dots. |
| S1a (visual) | PARTIAL | The gold links now terminate on Z's axis, but 11 dots land on packet ink (mandate 1). |
| S1b | ACCEPT gold | Gold reads as the weighted V flowing into Z and matches the reference's colour. Do not black it. |
| S3b | open (deferred) | No change visible. |

## Regressions vs compare-to (r10 `pp_resonance_continuous-dots_v1`, v13)
- **V connector gesture lost.** r10/v13 had one graceful gold arc from V down to Y (the reference's route). r06 has a U-turn loop near the right margin plus a ~100 mm horizontal gold run at y≈108, which fences the band just above `— MoE —`.
- **New ink-on-ink.** The S1a re-aim lands 11 gold dots on the green Z packets (the big packet's right flank and the small packet). In r10 those links did not touch Z's packets.
- **Halos changed shape.** Closed ellipses (with clip chords) became open C-arcs. That is cleaner, but further from the reference and arguably against J2's "the dotted halos/ellipses".
- **Hero dot fields ~48 % thinner than r10.** The caps and spoke dots are much sparser. This is legitimate as the A13a fix, but it is a J2 exposure Juan should see. The small ◎ spoke glyphs on the rails became plain solid dots.
- DESCRIPTION § Keep:
  - Hero construction verbatim: TRUE. Solid crest line is 2.35 m with 1.41 mm pitch, byte-for-byte equal to r10/v13.
  - Funnel of crimson and blue fans onto the rim: TRUE. The fans still dive into the upper ring nest, as in r10.
  - Hero pen economy, no flood: TRUE, and improved (the caps no longer mud).
  - Packet vocabulary consistent: TRUE. The K 1/2 and V 2/3 contacts are inherited from v13, not new.
  - MoE fork, two solid + three ghost lanes: TRUE. The ghost packets are now dot clusters and slightly louder, but they still read as ghosts.
