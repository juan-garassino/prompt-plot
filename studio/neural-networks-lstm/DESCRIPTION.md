# LSTM — GATED MEMORY DYNAMICS / MEMORY IN TIME — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/neural-networks/lstm` |
| current render | `gallery/neural-networks/lstm/promoted/pp_lstm_gates.png` (A · gate mandala) · `gallery/neural-networks/lstm/promoted/pp_lstm_fig8_v2.png` (B · figure-8, with its predecessor `pp_lstm_fig8.png`) · `gallery/neural-networks/lstm/candidates/pp_bauhaus_memory_LSTM_v3_seed1.png` (C · twisted helix — **the one Juan promoted**) |
| source | A: `promptplot/generative/pieces/ml.py::lstm_gates` · B: `promptplot/generative/pieces/ml.py::bauhaus_memory` (earlier `bauhaus_memory_v1`) · C: `studio/neural-networks-lstm/rounds/r00/piece.py::bauhaus_memory_helix` — FROZEN ORIGINAL restored from the 2026-09-13 session (uncommitted edit on 2597b31; GCode byte-identical, see `rounds/r00/NOTES.md`); `bauhaus_memory` in the package was later rewritten into the figure-8 |
| paper · pens | a4 portrait (210 × 297 mm), cream · 1 crimson = accent (A: the four gate-value dots + one spiral per bundle; B: alternate lobe rings + LATENT marker; C: the UPDATE spiral + two state dots) · 2 black = everything else incl. all type |
| status | **PROMOTED** — `pp_bauhaus_memory_LSTM_v3_seed1.png` ("this is the one", 2026-09-20). A and B sit in `promoted/` without a recorded verdict · 18 renders on disk |

## In one line
Gated memory drawn three ways — A as a **radial** mandala (cell-state hub, four gate discs on a ring, log-spiral bundles carrying flow between them; each gate's 0→1 slider shows its value), B as an **orbital** figure-8 of precessing loops (REMEMBER lobe above, FORGET lobe below, crossing at the LATENT waist), C (Juan's pick) as a **twisted-strand / interlaced** column (a two-strand ribbon helix carrying state from INPUT up to OUTPUT, with gate spirals docked beside it).

## What is on the sheet
Coordinates normalised to the A4 sheet (u → right, v → down); drawable area u 0.07–0.93, v 0.05–0.95.

### A · gate mandala (`pp_lstm_gates.png`)
1. **Hub** — a double-ring disc r ≈ 15 mm (0.07 W) at u 0.50, v 0.46, holding `C E L L   S T A T E` (≈ 1.9 mm caps, the letters overrun the inner ring at both ends) and below the horizontal axis `M E M O R Y   I N   T I M E` (1.4 mm, crosses the ring at the right). A short black tick sits below the hub centre.
2. **Spiral bundles (dominant texture)** — around the hub, four bundles of ~6–14 concentric log-spiral arcs sweep clockwise out from the hub toward each gate, forming a pinwheel ≈ 0.40 W across (u 0.30–0.70, v 0.35–0.60). Arcs are broken into long dashes where they bunch (engine pause-resume). One crimson spiral arc per bundle: hub→FORGET (u 0.32–0.48, v 0.33–0.40), hub→INPUT (u 0.60–0.70, v 0.36–0.53), CANDIDATE→hub (u 0.34–0.40, v 0.48–0.57), hub→OUTPUT (u 0.54–0.64, v 0.57–0.62), plus short crimson fragments in the bundles.
3. **Gate discs** — four double-ring discs r ≈ 14 mm (0.07 W), placed at the four diagonal positions of a ring of radius ≈ 70 mm: `F O R G E T   G A T E` at u 0.31 v 0.31, `I N P U T   G A T E` at u 0.72 v 0.32, `C A N D I D A T E` at u 0.27 v 0.56, `O U T P U T   G A T E` at u 0.64 v 0.63. Each holds its label (overrunning the inner ring on FORGET, INPUT, OUTPUT), a horizontal slider rule with five small open circles and `0` / `1` end marks, one crimson spiral dot at the gate's value (FORGET ≈ 0.15, INPUT ≈ 0.85, CANDIDATE ≈ 0.75, OUTPUT ≈ 0.9), and a short black needle tick. Dashed-orbit dashes and needle-like stubs cross the disc rims.
4. **Orbits** — three concentric long-dash circles around the hub: r ≈ 45 mm, ≈ 61 mm, ≈ 83 mm (outer one spans u 0.13–0.93, v 0.21–0.72). Several small open circles (≈ 2 mm, 8 of them) sit on the orbits as tokens (e.g. u 0.55 v 0.27, u 0.72 v 0.43, u 0.45 v 0.62).
5. **Axes** — a vertical black rule through the hub from v 0.10 to v 0.90 with arrowheads at both ends, labelled `T I M E` at top (u 0.53, v 0.09) and `H T     O U T P U T` at bottom (u 0.53, v 0.89); a horizontal rule u 0.16–0.84 at v 0.46, arrow right, labelled `C   T - 1` (left, u 0.11) and `C   T` (right, u 0.87).
6. **Corner type** — four three-line captions in the four corners: top-left `SEQUENCES / CREATE / MEMORY` (u 0.10, v 0.08–0.10), top-right `PAST / PRESENT / FUTURE` (u 0.78), bottom-left `RECURSION / CREATES / PERSISTENCE` (u 0.10, v 0.82–0.85), bottom-right `A SMALL / MECHANISM / A LONG MEMORY` (u 0.76).
7. **Title** — bottom-centre `L S T M` (≈ 5 mm, u 0.45–0.55, v 0.91) over `G A T E D   M E M O R Y   D Y N A M I C S` (u 0.36–0.64, v 0.945).
8. **Quiet zones** — v 0.12–0.20 and v 0.73–0.80 (both crossed only by the vertical axis) — symmetric, left over.

### B · figure-8 (`pp_lstm_fig8_v2.png`)
1. **Two tilted lobes (dominant mass)** — nested elliptical loops tilted ≈ 30° up-right. Upper REMEMBER lobe: u 0.33–0.67, v 0.23–0.49; lower FORGET lobe, ≈ 1.6× larger: u 0.27–0.90, v 0.42–0.77, its right edge within 5 mm of the right margin. ~12 rings per lobe alternating crimson and black; the inner rings break into long dashes (pause-resume), the outer 2–3 rings are continuous crimson. The two lobes cross at a waist at u 0.49, v 0.47 marked by a small crimson circle and `L A T E N T` in crimson.
2. **Axis** — a vertical black rule at u 0.49 from v 0.21 to v 0.79, arrows at both ends: `O U T P U T` at top-right of the arrow (u 0.53, v 0.20), `I N P U T` at bottom (u 0.53, v 0.79). Small black spiral dots where the axis meets each lobe's outer ring (v 0.24 and v 0.76).
3. **Inner labels** — `R E M E M B E R` / `C   T` inside the upper lobe (u 0.46, v 0.36–0.38); `F O R G E T` / `C   T - 1` inside the lower lobe (u 0.47, v 0.62–0.64). Halos cut the rings around them.
4. **Gate callouts** — `O U T P U T   G A T E` / `O   T` (u 0.10, v 0.27) with a dashed leader dropping to the upper lobe (u 0.20, v 0.29–0.36); `I N P U T   G A T E` / `I   T` (u 0.74, v 0.44) with a dashed diagonal leader to the lower lobe; `F O R G E T   G A T E` / `F   T` (u 0.09, v 0.60) with a short dashed leader.
5. **Footer** — `L S T M     M E M O R Y   I N   T I M E` (u 0.12–0.35, v 0.87).
6. **Debris** — ~15 isolated 1–2 mm black dashes scattered over the empty sheet (e.g. u 0.19 v 0.18, u 0.42 v 0.12, u 0.64 v 0.19, u 0.74 v 0.27, u 0.88 v 0.35, u 0.14 v 0.70, u 0.29 v 0.80, u 0.74 v 0.88) — orphaned dash fragments.
7. **Quiet zones** — the whole top band v 0.05–0.19 and bottom band v 0.80–0.95 except the footer.
- `pp_lstm_fig8.png` (the predecessor) is identical except for a **black fan of ~20 radiating strokes** bursting from the LATENT waist toward the upper right (u 0.50–0.57, v 0.40–0.47); v2 removed it.

### C · twisted helix (`pp_bauhaus_memory_LSTM_v3_seed1.png` — PROMOTED; 614 px preview only)
1. **The column (dominant mass)** — a two-strand twisted ribbon, each strand a bundle of ~8 parallel hairlines, running vertically at u 0.43–0.53 from v 0.18 (top) to v 0.79 (bottom): ≈ 0.61 of sheet height, ≈ 0.10 W wide. It crosses itself ~12 times; at each crossing the bundles pinch to a black knot, between crossings they open into lens-shaped cells, so the column reads as a chain of twisted links with strong black-knot rhythm.
2. **Spine** — a dashed vertical centre line through the column (u 0.47) with an arrowhead above the top (`O U T P U T`, v 0.17, with a black dot) and a black dot + `I N P U T` at the bottom (v 0.78). Two crimson dots on the spine (v 0.40 and v 0.62) and one small crimson ring labelled `M E M O R Y` (u 0.48–0.61, v 0.47).
3. **Gate spirals** — three Archimedean spirals docked beside the column by short leader ticks: a **crimson** spiral r ≈ 15 mm at u 0.62, v 0.40 labelled `U P D A T E   G A T E` (u 0.62–0.75, v 0.31); a black spiral r ≈ 19 mm at u 0.32, v 0.62 labelled `F O R G E T   G A T E` (u 0.29–0.43, v 0.74); a smaller black spiral r ≈ 11 mm at u 0.60, v 0.71 labelled `C E L L   S T A T E` / `V O R T E X` (u 0.60–0.72, v 0.79–0.80, colliding with `I N P U T`).
4. **Title** — `L S T M` (u 0.17–0.30, v 0.08) and `M E M O R Y   I N   T I M E` (u 0.17–0.46, v 0.11), top-left.
5. **Footer glyph strip** — `P E R S I S T I N G   I N F O R M A T I O N` (u 0.17–0.49, v 0.89) followed by three icons: small helix → arrow → small spiral → arrow → small helix (u 0.52–0.75, v 0.90).
6. **Quiet zones** — the left third above v 0.55 and the right third below v 0.45: the column is flanked by open paper, the spirals break the symmetry.

## The science it encodes
- A (`lstm_gates` docstring, `promptplot/generative/pieces/ml.py`): "the LSTM as a gate mandala: the CELL STATE hub with four gate discs (FORGET, INPUT, CANDIDATE, OUTPUT), each holding a 0→1 slider; LOGARITHMIC-SPIRAL bundles stream between hub and gates (memory flowing through gates), crowd-controlled natively by the engine". The gate values are hard-coded constants (0.15, 0.85, 0.75, 0.9) — they do show on the sliders — but no LSTM is run; the spirals' geometry carries no numbers.
- B (`bauhaus_memory` docstring): "an LSTM as a figure-8 of PRECESSING loops (REMEMBER c_t above, FORGET c_{t-1} below, meeting at the carried-state waist), each iteration landing slightly rotated". Loop count 40, precession 0.5, growth 1.0 are free parameters, not LSTM dynamics; on the render the precession is barely visible because pause-resume turns the nested loops into ~12 near-concentric rings per lobe.
- C: restored 2026-09-28 as the frozen original `rounds/r00/piece.py::bauhaus_memory_helix` (byte-identical GCode; recovered from the 2026-09-13 session transcript — it was never committed). From the render: the twisted strands are the cell state carried through time, crossings are time steps, gates are spirals beside the column. Nothing on the sheet indicates computed values.
- Brief `studio/nets/lstm.md` (for B): "the cell state loops every step but takes a *different path each iteration*… ~40 continuous precessing figure-8 loops… Forget/input/output gates are red lateral attractors that warp the pathways". On B the gates are black text callouts, not red attractors, and the loops do not visibly bend toward them.
- Across all three, the one real LSTM idea — an additive cell-state highway that the gates multiply into — is only asserted by labels (`CELL STATE`, `C T-1 → C T`), not built by geometry.

## How it got here
- **v1 (`bauhaus_memory_LSTM_v1_seed1`)** — a bow-tie: ~25 nested crimson and black loops pinched at one waist, symmetric left/right, with a dashed spine carrying `OUTPUT / UPDATE / MEMORY / FORGET / INPUT` dots and labels to the right, a caption `INFORMATION LOOPS / SELECT WHAT TO KEEP / LET GO . MOVE FORWARD` and a footer of three circles with arrows. Heavy ink at the waist.
- **HELIX v1 (`LSTM_HELIX_v1_seed1`, prior-approved) → `LSTM_HELIX_inspect_v3`** — the figure-8 appears: two tilted lobes crossing at LATENT, gate callouts with dashed leaders; the waist is a dense black knot of ~40 overlapping loops (the ink piles to solid).
- **`pp_lstm_fig8` → `pp_lstm_fig8_v2`** (promoted) — Scene3D pause-resume thins the loops into ~12 broken rings; v2 also removes a black fan artefact at the waist. Gained: no flooding. Lost: the loops no longer read as one continuous precessing curve — they read as concentric ellipses.
- **v2/v3 helix (`LSTM_v3_seed1`)** — a different thesis under the same name: the twisted-strand column with docked gate spirals. **Juan: PROMOTE — "this is the one."** Its code was later overwritten by the figure-8 rewrite.
- **`pp_lstm_gates`** — a sibling "flavor" (docstring) introduced as the radial gate mandala; no verdict.
- Also in candidates: `bauhaus_conveyor_LONGNOW_v1/v2` (landscape, a separate THE LONG NOW piece) — not reviewed here.

## Keep — what works
### A · gate mandala
- The **pinwheel of log-spiral bundles** around the hub (u 0.30–0.70, v 0.35–0.60) — a genuine radial order with rotation; the dashes thinning where arcs bunch keep it plottable.
- The **slider with one crimson dot per gate** at the true gate value — the only place where a number is shown and the crimson is scarce and loud.
### B · figure-8
- The **two tilted lobes of unequal size** (lower ≈ 1.6× upper) — the only real asymmetry in the family; the lower lobe pushes toward the right margin and makes a diagonal.
- The **LATENT waist** as the single crossing point at u 0.49, v 0.47, marked in crimson.
### C · twisted helix (Juan's pick)
- The **black-knot rhythm** of ~12 crossings up a thin tall column — reads at 3 m as "a chain carried through time"; the strongest single image in the family.
- **Gate spirals off-axis and unequal** (crimson UPDATE right-high, big black FORGET left-low, small black VORTEX right-low) — they break the column's symmetry and the crimson one is the loud accent.
- Generous empty paper on both flanks — the column is a narrow dominant mass on a vast field (≈ 1:9 width ratio).

## Weak — what doesn't
### A · gate mandala
- [concept] It is a **labelled schematic**: a hub, four labelled discs with slider widgets, two labelled axes, four corner captions — an infographic of the LSTM cell, rubric § 6 NO SCHEMATICS. The sliders are UI widgets (an illustration of a control), not an order.
- [tension] **Dead-centre radial symmetry**: hub at u 0.50, gates on diagonals, axes cross at the centre, four corner captions mirror each other — the rubric's "subject floating dead-centre" and "furniture checklist" failure modes at once.
- [craft] Type collides everywhere: `CELL STATE` and `MEMORY IN TIME` overrun the hub ring and are cut by the horizontal axis; gate labels overrun their inner rings; orbit dashes and needle stubs cross gate rims. Travel (4.2 m) exceeds draw (4.0 m).
- [hierarchy] Hub, four gates and the orbit rings are all mid-sized; the pinwheel is the only mass and it is small (0.40 W).
- [space] v 0.12–0.20 and v 0.73–0.80 are leftover bands pierced by the axis; corners are filled with type.
- [depth] Flat and undeclared.
### B · figure-8
- [craft] ~15 **orphan dash fragments** scattered across the empty sheet — they read as dirt.
- [concept] Pause-resume turned the precessing loop into concentric ellipses: the "each iteration lands slightly rotated" idea is invisible. The alternating crimson/black rings use colour as pattern, not data.
- [grid] Gate callouts float at arbitrary positions with wandering dashed leaders; footer and callouts share no line.
- [space] The lobes are centred with ≈ 0.20 H empty above and below; the bottom band is leftover.
### C · twisted helix
- [concept] A double-helix column reads as **DNA** — an object the viewer can name that is not the mechanism (rubric § 6 "the illustration"). The footer icon strip (helix → spiral → helix with arrows) is a schematic.
- [craft] `CELL STATE VORTEX` collides with `INPUT` at v 0.79; `UPDATE GATE` label sits far from its spiral; crossing knots are ink-on-ink (8 hairlines converging to a point).
- [grid] Title top-left, gates scattered, footer strip bottom — no shared axis besides the spine.
- [depth] The twist gives implied depth but the strands have no over/under — neither strand passes behind the other.

## Next versions
1. **carousel-highway** (mechanism) — Build on Juan's pick C: keep the tall twisted column and its black-knot rhythm, but make it the **cell-state highway computed from a real LSTM run** on a short sequence: strand separation = |c_t|, twist phase advances by the input, and at each crossing the forget gate f_t sets how many of the ~8 hairlines survive into the next link (lines end where memory is forgotten, new ones start where i_t·g_t writes). Crimson only for writes. Order = **interlaced**, with real over/under at crossings. No DNA read once strands thin and thicken by data; drop the icon footer.
2. **precession-rose** (abstract) — B's figure-8 done as one CONTINUOUS curve whose each loop is rotated by a real hidden-state angle, drawn with duty-cycle dashes (not pause-resume rings) so the rotating family builds a rose/moiré; gates become nothing but where the loop's radius shrinks (forget) or grows (write). Asymmetric crop: let the larger lobe bleed off the right edge.
3. **gate-weave** (lens) — The radial mandala A reduced to its one true order: a spiral transport field on the whole sheet (no discs, no sliders, no axes), where four sectors carry spiral pitch = gate value, so the four gates are read as four densities of the same flow; one crimson line tracks one memory from outside to the hub.

**If only iterating:** (on C, the promoted render — recover or rewrite its code first)
1. Give the two strands real over/under at every crossing (the back strand breaks ≥ 1 mm around the front one) so the column reads as woven depth, and stop the 8 hairlines converging to a single point at each knot (keep a ≥ 0.8 mm pitch through the pinch).
2. Move `CELL STATE VORTEX` so it no longer touches `INPUT` (≥ 4 mm clear), set every gate label on a shared baseline with its spiral, and delete the footer icon strip (helix → spiral → helix).
3. Tie the strand width or line count to data along the column (e.g. lines drop out going up where the forget gate is low) so the column is visibly not uniform from bottom to top.
