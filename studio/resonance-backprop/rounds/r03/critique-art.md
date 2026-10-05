# Art critique — resonance-backprop r03 · canon: none assigned (no encoding.md / BRIEF.md). Judged against the HANDOFF lineage, Bridget Riley *Current* (1964, Op Art), plus DESIGN_RUBRIC · 2026-09-29
render: gallery/studio/res_backprop/current/pp_res_backprop_gradient-as-phase_v9.png (gcode beside it; a4 portrait, cream, 5 pens, thesis "gradient-as-phase")

## Scores
| # | dimension | score | evidence |
|---|---|---|---|
| 1 | hierarchy | 7 | The double ring field (two concentric 3 mm families centred at about (96,156) and (124,144), outer radius about 70 mm) dominates at 3 m without contest. The second read is weak. The three red/blue gradient patches around V₁/V₂/V₃ are each only about 35×30 mm inside a 170 mm field. At 1 m the Q and K packets (about 45×10 mm) read as small corner glyphs, not as the sources of the field. |
| 2 | grid & alignment | 6 | The left edge is shared at x≈24 by the title, subtitle, Q, and the key labels (Z=AV, V₁, ∂L/∂Z). The right edge is not shared. The footer ends at x≈196, K's glyph at x≈188, and the ring field at x≈196, which is 4 mm from the frame against 14 mm on the left. There are only three registration crosses: (14,283), (14,16), (196,16). The top-right corner is empty. The key wavelets (x 55–82) sit on no column that anything else uses. |
| 3 | tension & asymmetry | 6 | The Q top-left / K bottom-right diagonal and the offset of the two ring centres work. But the hero's bounding box (x 24–196, y 85–228) is centred on the sheet to within about 5 mm horizontally, and it floats with a band of paper around it. That is failure mode 1, only partly rescued by the diagonal. |
| 4 | negative space | 6 | There is a generous void from y 230 to 265 at x 100–200 and around the hero. It is leftover, not shaped. The bottom band (y 20–65) has three unrelated groups (the key stack, K, and the formula footer) that neither cluster nor align. The white rectangular knockouts behind V₁/V₂/V₃ cut the rings cleanly. That overlap is chosen and defensible. |
| 5 | craft for pen | 6 | Good: the 3.00 mm crest pitch holds, the half-over crests in the V₁ patch sit at about 1.5 mm from black (above 0.8), there are no floods, the solid source dots are small, and 5 clean layers are streamed light→dark with one swap each. Bad: the batching is poor. Travel is 4.04 m against 11.35 m of draw (35 %). Layer 1 travels 709 mm to draw 677 mm, and layer 3 travels 703 mm to draw 711 mm, because they hop between patches. There are 11 rapids over 80 mm, including 210 mm (144,201)→(26,27) on blue and 237 mm (40,247)→(14,12) on red. Black visits the crosses out of order: (14,285)→(70,127), then (127,99)→(196,277). The subtitle (about 3 mm caps) and the footer set at the real 0.3–0.4 mm nib clog: "pass is" reads "pass ß", "mm" fuses, and "gradient" loses its i. |
| 6 | concept legibility | 5 | The order is legitimately INTERFERING, and the thesis ("the gradient crest is the forward crest, or half a wavelength off it") is exact and witty. But it is only legible at 30 cm, and in two of the three patches (V₂, V₃, on-crest) it lives only in hue: in monochrome those patches vanish into the black field. Two target discs overlapping is also the textbook two-source (Young) figure. The bottom-left key stack (label + wavelet ×3) is a figure legend. |
| 7 | depth & dimensionality | 4 | The overlapping ring families give a mild moiré shimmer and nothing more. There is no occlusion, weight falloff, or dash-density falloff. The flatness is undeclared in HANDOFF. |

**avg 5.71 · min 4 · VERDICT: FAIL**

## Reads at a glance
From 3 m a stranger sees a big black double target, two ripples overlapping, with three small red-and-blue striped patches and a few squiggles around it. It reads as "interference". It does not read as "backprop is the same wave, shifted".

## Acceptance checks
There is no encoding.md, so there are no §11 checks. The reference is in play, so these are AUTHORING §6's seven questions:
1. Main forms recognisable without colour fills? **FAIL.** The ring field and the packets survive. The on-crest gradient patches (V₂, V₃) are recoloured black crests, so they disappear entirely in monochrome, and the thesis goes with them.
2. Shadow lines follow the surface? **PASS (n/a).** Nothing is shaded. The gradient crests ride the ring families exactly.
3. Fine lines that are two sides of one thick stroke? **PASS.** Everything is centreline.
4. Blackest regions intended? **PASS.** The densest zone is the lens between the sources, where both families cross at 3 mm. That is intended, and it is not flooded.
5. Labels readable at real pen width? **FAIL.** The subtitle and footer clog, as noted in dimension 5. The title (about 5 mm, spaced) and the V/Q/K glyphs are fine.
6. Thicker pen makes black knots? **PASS.** The source dots are about 1 mm. The ring crossings stay open.
7. Long empty travels or pointless tiny marks? **FAIL.** 35 % travel, the blue and red layers travel as much as they draw, and 11 hops exceed 80 mm.

Interpretation verdict: this is an honest *reduction* of the reference to one idea (backprop as phase), not an interpretation of it. Softmax A, ∂L/∂A, ∂L/∂V, the fans, the halo field and the fold are all absent.

Lineage: Riley's *Current* is ONE line family whose frequency and phase drift buckles the surface. Here there are two concentric target families with colour overlays laid on top, and the phase shift never deforms the black lines themselves. Hung beside *Current* this plate borrows the moiré shimmer, not the order: surface texture, not lineage. It would not hold its own.

## Biggest weakness
The plate's one idea, "half a wavelength over", is drawn as three small coloured overlays instead of as a phase dislocation in the line field itself. At 3 m, and in monochrome, the mechanism disappears and what remains is a centred double bullseye.

## Mandates
(These apply only if "gradient-as-phase" continues as a separate alternative plate. See the follow-up below: Juan's binding note says the res_backprop plate itself must restart from r01/v13.)
1. **Draw the phase shift in the black lines, Riley-style.** Inside each gradient zone, the black crest family itself must jog by λ/2 (1.5 mm), with the rings visibly stepping or bending across the zone boundary. The coloured crests can stay as a secondary cue. Test: a greyscale print of the plate still shows three dislocation zones, and V₂/V₃ are distinguishable from V₁ (on-crest vs half-over) without hue.
2. **Uncentre the hero and delete the key.** Move or grow the ring field so it crops off one frame edge by ≥ 25 mm (for example, the right disc bleeding past x=200). Put the two source centres on a sheet third (x≈70 or ≈140). Remove the three-row wavelet legend at bottom-left (Z=AV / V₁ / ∂L/∂Z, x 24–82, y 25–60), or fold those wavelets into the field as real rows. Test: the hero centroid is ≥ 20 mm off x=105, and no label+wavelet stack stands outside the field.
3. **Batch each layer as one spatial sweep, and fix the small type.** Order blue and red patch by patch in a single pass (no return trips), and draw the four crosses as one corner loop. Targets: total travel ≤ 20 % of draw, no G0 > 100 mm except layer entry and park, and layer 1 and layer 3 travel each ≤ 40 % of their draw. Set the subtitle and footer at cap height ≥ 4 mm, or use a thinner nib layer, so "pass is", "mm" and "gradient" stay open at 0.35 mm width. Test: the gcode stats meet those numbers, and a crop of the subtitle at nib width reads cleanly.

## Follow-up on open mandates
There is no LEDGER.md, so no A*/J* ids exist. Below are Juan's FEEDBACK note, the r02 art mandates, and DESCRIPTION "If only iterating".

| id | status | evidence |
|---|---|---|
| J (FEEDBACK 2026-09-28T23:39: "KEEP THE ORIGINAL — v13/r01 is the design, keep EVERY element, only fix dot continuity; don't remove anything to save plot time"; also in QUEUE.md) | **REGRESSED** | This render is timestamped 23:48, *after* the note. It still removes the Q/K/V/∂L/∂Q/∂L/∂K packet blocks, all dotted leaders and fans, the halo field, the scattered dots, the comb, softmax A, ∂L/∂A, ∂L/∂V and the rail. It is a new thesis, not the dot-continuity fix. Dot continuity is untested, because there is almost no dotted line left (only the faint dotted envelopes on Q and K). |
| r02-A1 quiet zone + dominant | PARTIAL | There is now one clear dominant (the ring field). The quiet space is leftover, not shaped. |
| r02-A2 backward half readable in monochrome | NOT FIXED | Same failure in a new form: the gradient is hue-only in V₂/V₃. |
| r02-A3 V as a real row, bead craft | PARTIAL | V is now three wavelets plus a key row, with no bead knots. There is still no row of attention weights. |
| iter-1 amplitude ≤ 0.45 × row pitch | FIXED (moot) | There are no stacked rows left to braid. The key rows are 22 mm apart. |
| iter-2 comb fringes ≥ 1.0 mm | FIXED (moot) | The comb was replaced by 3 mm crossing families. None is flooded. |
| iter-3 use the dead foot | PARTIAL | The foot band y 15–65 now carries the key, K and the footer, but as scattered groups. |

**DESCRIPTION § Keep:**
- v8 tight dashed oval: GONE.
- v5 wide dotted halo: GONE.
- The fold with ∂L/∂Z directly under Z = AV: PARTIAL. The two are stacked in the key 22 mm apart, but there is no fold.
- Comb lozenge: GONE. Replaced by a two-family crest lattice.
- Left rail with arrows: GONE (in r02 the words were still there).
- Corner crosses + title: PARTIAL. The title is back (left-set, not centred), but only 3 of 4 crosses.

## Regressions vs compare-to (gallery/studio/res_backprop/current/pp_res_backprop_v8.png)
- **Binding-feedback violation.** Juan asked for v13/r01 unchanged except dot continuity. r03 is a ground-up redesign made 9 minutes after that note. This is the headline regression, and it outranks the scores.
- The data stages softmax A, ∂L/∂A, ∂L/∂V, the Q/K/V row blocks and the fans are gone. The plate now reads two stages (forward field + gradient patches), where v8 read seven.
- The left rail (forward-down / backward-up axis) is gone. It survived partially in r02.
- The fourth corner cross is gone. The title moved from centred to flush-left, which is not wrong in itself, but the frame no longer closes.
- Against r02: travel rose from 2.6 m to 4.0 m, and the ring-weight falloff by pass count (3/2/1 turns) is gone, so depth dropped.
- Genuine gains to carry into the r01 restart: travel 4.0 m vs v8's 11.9 m, 585 pen cycles vs v8's 4 054, no braided packet knots, no flooded comb, and exact 3 mm crests.
