# Art critique — resonance-backprop r04 · canon: none assigned (no encoding.md or BRIEF.md). Judged as a declared-flat engraving plate after the lineage (Helmholtz 1863 wave-composition figures) and as an interpretation of `ref/reference.png` · 2026-09-29
render: gallery/studio/res_backprop/current/pp_res_backprop_iterate_v3_plate.png (stream-order plate; gcode gallery/studio/res_backprop/current/pp_res_backprop_iterate_v3_plate.gcode) · nib crops `_nib_{subtitle,densest,comb,dq_fan}.png` + own crops of the hero, the V→Z band and both backward corners

## Scores
| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 7 | At 3 m the hero band dominates (two ring bullseyes, the comb, dotted halos). Q/K come second and Z third. But the scatter plus halos now weigh as much as the bullseyes, so the dominant element is a grey-black band rather than the two sources. |
| 2 | grid & alignment | 6 | The central axis, the Q/K node columns and the rail are shared. The V block (x 25–50) sits off the Q column (x 28–60). `∂L/∂V` hangs outboard at x ≈ 193, past the K column edge. The softmax label sits under the halo's lower rim with no set gap. `QK T` has a visible gap before the superscript. |
| 3 | tension & asymmetry | 6 | The lineage and the fold allow a bilateral mirror. V upper-left against ∂L/∂V lower-right gives one real diagonal. Otherwise the plate is centred and symmetric top and bottom. |
| 4 | negative space | 5 | The halos run under the lowest Q/K packet rows. Red and blue leaders thread through the black scatter. Goldenrod V loops cross each other and run over the Z diamond. ∂L/∂Q and ∂L/∂K arrowheads land on and inside their packet envelopes. The only quiet zones are leftover gutters (x 15–25 and y 12–30), not shaped ones. |
| 5 | craft for pen | 6 | Measured on the gcode, the dots are real round dots: 0.3 mm circles at 1.00 mm median pitch, with no pair under 0.6 mm. Five pens, each entered once in a stated light→dark order. The comb holds at the nib (≈1.2 mm pitch, ≈0.85 mm gap), and the subtitle stays open at 0.35 mm. Against that, 371 black dot pairs sit under 0.8 mm (clumped doublets in the scatter). Black travel (5.11 m) exceeds black draw (5.00 m). Blue and crimson each carry one sheet-crossing hop (106 and 138 mm). Arrowheads collide with packet ink. |
| 6 | concept legibility | 4 | The hero is a genuine INTERFERING order and reads. The rest is a labelled flow diagram: fractions, stage names and arrowed fans, all inherited from the reference. Held at 4 rather than ≤3 only because the hero and the fold carry real form. |
| 7 | depth & dimensionality | 6 | Flatness is declared. Every line is one weight and one pass, so the plate lacks the thin/thick alternation an engraving plate uses for rank. Flat, but not exploited. |

avg **5.71** · min **4** · VERDICT: **FAIL**

## Reads at a glance
At 3 m a stranger sees a black moth-like mass with two target eyes. Coloured wave packets are pinned to its wings, and a busier mirrored thicket of dotted arrows sits below.

## Acceptance checks
encoding §11: n/a (no encoding.md, no BRIEF.md). AUTHORING §6 against `ref/reference.png`:
1. Main forms recognisable without colour: **PASS**. Packets, bullseyes, comb, softmax peaks and Z diamond all read in black alone.
2. Shadow/tone lines follow the form: **PASS**. The dotted envelopes ride the packets, and the halos are concentric on the sources.
3. Fine lines that are two sides of one thick stroke: **PASS**. None found.
4. Blackest regions intended: **FAIL**. The reference's field is a soft grey lens of thin circles, with black only at the sources. Here 2,285 full-size black dots plus halos make the whole band as dark as the bullseyes. The tone is inverted relative to the reference.
5. Labels readable at pen width: **PASS** with a note. The subtitle crop is open at 0.35 mm. `A = softmax(QK T / √dₖ)` has a broken superscript gap.
6. Thicker pen makes knots: **FAIL**. The ∂L/∂Q fan heads touch each other and land on the packet (see `_nib_dq_fan`: one crimson head sits inside the envelope at the packet's left third). The same happens on the mirror at ∂L/∂K. The scatter has 371 sub-0.8 mm doublets.
7. Long empty travels / excessive tiny marks: **FAIL**. Travel is 11.69 m against 14.11 m of draw (83 %). Black travel exceeds black draw. Black batch 0 spans 190 × 158 mm. Blue has a 106 mm hop and crimson a 138 mm hop, from the upper block to the lower block. The scatter spends ~2,000 pen cycles on texture that reads as mass, not tone.

## Biggest weakness
The hero's tonal field is inverted. Carried over at one dot size, the halos and scatter are now as heavy as the sources. The two bullseyes and the comb (the plate's actual resonance) drown in a uniform black band, and on paper the reference's airy interference lens becomes a dark blot.

## Mandates
1. **Two-class dots in the hero band. Keep every dot's count and position; change only the mark.** Every scatter and halo dot becomes a single pen touch (nib-size, about 0.35 mm, no drawn circle). Leader/fan dots stay 0.3 mm circles. The 371 black texture pairs under 0.8 mm are nudged apart to ≥ 0.8 mm centre spacing, not deleted. Test: at arm's length the bullseyes and comb are the darkest marks in the band (x 40–170, y 165–215), the halo reads a clear step lighter than the Q/K leaders, and a nib crop of the densest scatter shows no touching doublets.
2. **No leader enters a packet.** Every ∂L/∂Q and ∂L/∂K arrowhead stops ≥ 1.5 mm outside its block's outer dotted envelope. That covers crimson at x 30–60, y 45–62 and blue mirrored at x 150–180. Converging heads sit ≥ 2 mm apart, with no two triangles touching. The goldenrod V loops clear the Z diamond (x 80–130, y 115–140) by ≥ 1.5 mm; they route around its tips, they are not removed. Test: the nib crops at both backward corners and at the Z diamond show paper between every head or loop and the packet ink.
3. **Batch the black layer and close the two sheet hops.** Reorder black so each 400-stroke batch is one region no larger than ~100 × 80 mm. Today batch 0 is 190 × 158 and batch 6 is 190 × 58. Black travel must end ≤ 0.6 × black draw. Blue and crimson must not hop between the upper block and the lower block mid-layer (106 / 138 mm today): finish one block, then enter the other at its nearest stroke. Test: the per-layer table in NOTES shows batch bboxes, hops > 80 mm = 0 except layer entry, and totals.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| J1 | PARTIAL | The mark is fixed: every dot is one 0.3 mm circle at 1.00 mm median pitch, and nothing sits under 0.6 mm. The lines read continuous at the nib. Converging rule missed at the ∂L/∂Q/∂L/∂K fan heads (≈1.6 mm apart, heads touching) and in 371 black texture pairs < 0.8 mm. |
| J2 | FIXED pending Juan (only he closes) | Element audit against v5: 5 Q, 5 K and 4 V rows, Z, ∂L/∂Z with its arcs, ∂L/∂V, ∂L/∂A, ∂L/∂Q and ∂L/∂K are all present. So are the halos, the scatter, the leaders and arrowheads, the rail, the crosses, title and subtitle, and all 5 pens. Nothing is removed. ∂L/∂A now carries 3–4 black arrowheads a side, as in v8, where v5 had 2. |
| A2 | NOT FIXED (blocked by J2) | Q, K, V, ∂L/∂Q and ∂L/∂K rows still braid (Q at x 35–55, y 205–245). |
| A3 | FIXED (gate passes) | The `_nib_comb` crop shows fringes at ≈1.2 mm pitch with ≈0.85 mm of paper between them at 0.35 mm. The comb stays a striped lozenge, not a flood. |
| A6 | NOT FIXED (blocked by J2) | The foot y 12–30 mm is still unshaped bare paper. |
| A7 | PARTIAL | The dots are now round and the softmax label has clearance. The halos still run under the bottom Q/K packet rows, and the red/blue leaders still cross the scatter. The two-class rule was applied as "same size for both classes", which made the band heavier (see M1). |
| A9 | PARTIAL | Clean: 5 layers, each entered once, light→dark, 230 min stated. Not clean: black travel > draw, black batches up to 190 × 158 mm, one 106 mm blue hop and one 138 mm crimson hop mid-layer. |
| A10 | FIXED | HANDOFF names Helmholtz, *On the Sensations of Tone* (1863), the stacked-partials order, and declares depth flat. |
| A11 | FIXED | The `_nib_subtitle` crop shows lowercase counters open at 0.35 mm, with no tracking change needed. |

## Regressions vs compare-to (v5, Juan's REWORK target)
- **The hero's tonal hierarchy is worse.** In v5 the halo and scatter read as a light grey haze behind two solid bullseyes. In r04 every texture point is a full dot, so the band has gone black and the bullseyes and comb lose primacy. Caveat: v5's preview under-drew the nib, and its micro-dashes would also plot heavier than shown. Still, as rendered, r04 is the heavier and muddier of the two.
- **The V→Z band is louder.** The goldenrod V fans are now continuous dotted loops. Between x 70 and 140 they outweigh the V packets themselves and tangle over the Z diamond. In v5 they were a light veil.
- **The backward fans are heavier.** With continuous dots and more black ∂L/∂A arrowheads, the lower half reads as a thicket more than it did in v5. The arrowhead-into-packet collision was already present in v5 and is now more visible.
- **The plot is longer.** Cycles went from 4,053 to 5,652 and draw from 11.1 to 14.1 m. Travel improved from 13.45 to 11.69 m. The time is accepted by J2, but see M1: ~2,000 cycles buy mass, not tone.
- DESCRIPTION § Keep: the fold is still true, and so are the left rail and the crosses with the centred title. The comb as "the densest, most resonant mark" is now weaker, because it competes with the scatter. The v5 claim "closest pen reading of the reference's soft tonal field" is **no longer true**: the field is not soft. The v8 compact-hero Keep does not apply, since the v5 field was chosen.
