# LSTM — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/lstm_spirals` |
| current render | `gallery/studio/lstm_spirals/current/pp_lstm_spirals_v10.png` |
| source | `studio/lstm-spirals/rounds/r01/piece.py::lstm_spirals` |
| reference | `studio/lstm-spirals/ref/reference.png` |
| paper · pens | a4 portrait (210×297 mm), white preview · 0 black = hidden-state vortex h_t, input-sequence streams, axis, dotted gate lines, all black type · 1 crimson = cell-state vortex c_t, its labels, red t-ring labels |
| status | unreviewed (no feedback on file) · 10 renders on disk (v1–v9 trials, v10 current) |

## In one line
LSTM recursion drawn as a **flow-to-attractor** order — two spiral sinks stacked on one vertical axis, black hidden state above and red cell state below, whose streamlines interleave around a genuine stagnation saddle between them — a reproduction of the reference with both centres moved onto the axis.

## Lede
An LSTM drawn as a flow field: **two spiral sinks on one axis**, short-term hidden state above and long-term cell state below, joined by a saddle point.

## On the sheet
Two interleaved spirals fill the centre of the sheet along a vertical axis: black above for the hidden state, crimson below for the cell state. Black input streams enter from the left, gate labels sit on both sides, and the title runs across the top left. The standard LSTM equations and a flow legend form a band along the bottom.

## The science
The streamlines are traced through a real flow field with two equal spiral drains, so a still point sits exactly halfway between them. That field is a visual metaphor for the cell. The gate names, the equations and the legend are the standard LSTM definitions, stated in text rather than computed from a trained network.

## What is on the sheet
- **The two vortices (dominant mass).** A vertical double-spiral occupying u≈0.19–0.86, v≈0.14–0.79.
  - **Black (hidden state)**: a tightly wound spiral whose eye is at u≈0.50, v≈0.35; its outer streamlines sweep as long arcs across the top (u≈0.25–0.80, v≈0.14–0.25) and hang down the left in a dense diagonal sheaf of near-parallel lines running from u≈0.26, v≈0.28 to u≈0.45, v≈0.63, interleaving into the red lobe. Chevron arrowheads ride the lines, all indicating counter-clockwise inward flow.
  - **Red (cell state)**: a mirror spiral whose eye is at u≈0.50, v≈0.63; its outer lines sweep the bottom (u≈0.20–0.72, v≈0.67–0.79) and climb the right side as a tall sheaf of red arcs (u≈0.56–0.81, v≈0.32–0.72) that interleaves up into the black lobe. The two lobes are 180°-rotations of each other about the saddle.
  - **Saddle**: between the eyes at u≈0.50, v≈0.49 the lines bend sharply away from each other (visible as a black hairpin at u≈0.46, v≈0.48 and a red hook at u≈0.52, v≈0.49); there is no single pinch point drawn.
  - Dotted and dash-dot black/red "gate interaction" and "information flow" lines, and dashed eccentric t-rings, run through the field but are mostly swallowed by the solid streamlines.
- **The axis.** One black vertical rule at u=0.50 from an up-arrowhead at v≈0.11 to a down-arrowhead at v≈0.79, through both eyes. `OUTPUT` above (v≈0.13) and `h_t  /  y_t` (v≈0.15); `INPUT` / `x_t` below the bottom arrowhead (u≈0.47–0.50, v≈0.81–0.83).
- **Left labels (black).** `OUTPUT  GATE` / `o_t` (u≈0.06–0.30, v≈0.30–0.33), with a dashed leader toward the field; `INPUT` / `SEQUENCE` / `x_t` (u≈0.06–0.18, v≈0.39–0.45); six small circle-dots in a column (u≈0.10, v≈0.45–0.53) each feeding a black arrowed stream that slides down-right into the field; `•••` at u≈0.05, v≈0.50; `INPUT  GATE` / `i_t` (u≈0.06–0.20, v≈0.57–0.60) with a dashed leader. `t = 3`, `t = 2`, `t = 1` step labels at u≈0.25–0.29, v≈0.29–0.36 inside the black lobe.
- **Right labels.** `hidden state   h_t` (u≈0.74–0.93, v≈0.32), `⊙ hidden state flow` / `(short-term output)` beneath; `FORGET  GATE` / `f_t` (u≈0.78–0.94, v≈0.42–0.44) with a dashed leader; `t = T` (u≈0.72, v≈0.24). In crimson: `cell state   c_t` (u≈0.76–0.93, v≈0.62), `⊙ cell state flow` / `(long-term memory)` (v≈0.64–0.66) — red streamlines pass straight through this label block; red `t = 1`, `t = 2`, `t = 3` (u≈0.23–0.32, v≈0.65–0.71) and `t = T` (u≈0.72, v≈0.79).
- **Title block.** Giant thin `L S T M` (u≈0.06–0.32, v≈0.06–0.11) with a plus-mark overlapping the L's top-left; `LONG SHORT-TERM MEMORY` / `RECURSIVE MEMORY` / `THROUGH TIME` (v≈0.14–0.16). Top-right: `MEMORY` / `THROUGH` / `RECURSION` / `THROUGH` / `TIME` (u≈0.80–0.91, v≈0.06–0.11).
- **Footer band (v≈0.80–0.90).** Three columns separated by vertical rules at u≈0.06, 0.57, 0.82: `LSTM EQUATIONS` with `c_t = f_t ⊙ c_{t-1} + i_t ⊙ c̃_t` and `h_t = o_t ⊙ tanh(c_t)` (u≈0.07–0.41); `FLOW LEGEND` with four swatch rows `hidden state flow (h_t)`, `cell state flow (c_t)`, `gate interactions`, `information flow` (u≈0.61–0.78); `SAME STATE` / `REPEATED T TIMES` / `RECURSION` / `CREATES MEMORY` / rule / `LSTM` / `A DYNAMICAL` / `MEMORY SYSTEM` (u≈0.83–0.91). Bottom centre `— MEMORY LIVES IN RECURSION —` (u≈0.30–0.70, v≈0.95). Plus marks at all four drawable corners.
- **Quiet zones.** Left strip u≈0.06–0.20, v≈0.17–0.60 around the gate labels; right strip u≈0.86–0.94, v≈0.45–0.60.

## The science it encodes
From `studio/lstm-spirals/rounds/r01/NOTES.md` and the module docstring: the streamlines are RK4-integrated from a real 2-D field of two spiral sinks (point sink + point vortex, 1/r falloff, m=1.0, g=3.0, s²=4) at 0.662H and 0.367H on the axis, plus an x_t injection drift (U=0.115, L=25 mm) so the input streams feed the cell. Equal strength and circulation give an exact stagnation point halfway between the centres. The labels, equations and legend are the standard LSTM cell equations copied from the reference. What is exact is the fluid field; the mapping to LSTM is metaphorical (hidden state ≙ upper vortex, cell state ≙ lower vortex) — no gate value or sequence is computed. Notes report 0.08 % near-parallel sub-0.8 mm ink.

## How it got here
Ten renders in one round (r01). Sampled trials:
- **v3**: all-caps type without subscripts (`HT / YT`, `C T = F T (•) C T-1…`), same double vortex, red streams cross the lower third densely.
- **v5**: same, plus a stray red horizontal rule across the bottom (u≈0.26–0.76, v≈0.79) labelled `t = T`.
- **v7**: type rebuilt in mixed case with real subscripts (`h_t`, `c_t`, `c_{t-1}`, `c̃_t`), the bottom rule gone.
- **v9 → v10**: input-sequence markers become circle-dots, minor streamline/arrow placement changes; composition unchanged since v7.
Gained: typographic fidelity (subscripts, ⊙, tilde). Unchanged throughout: the congruent symmetric lobes. No feedback from Juan on file.

## Keep — what works
- Two streamline families from one real field meeting at a genuine saddle on the axis (u≈0.50, v≈0.49) — the interleaving sheaves (black down the left, red up the right) are the plate's best passage.
- The axis as spine: OUTPUT arrow at top, INPUT arrow at bottom, both eyes on it — one straight vertical read.
- Black/red as the only two pens, each owning one vortex — colour is mass, not category.
- The input sequence: six dots at the left edge feeding arrowed streams into the field (u≈0.10–0.30, v≈0.45–0.60).
- Crowd control: the dense sheaves stay separate lines with no ink flooding.

## Weak — what doesn't
- [concept] It is a reproduction of a textbook-poster schematic: labelled gates with dashed leaders, a flow legend, the cell equations. The LSTM mechanism (gates scaling what is kept) is not in the geometry; a fluid double-vortex with LSTM labels on it.
- [tension] The two lobes are exact 180° rotations about the centre of the sheet on a centred axis — the symmetric, inevitable-but-static layout the notes themselves flag; the reference's larger, leaning black lobe had more tension.
- [craft] Red streamlines run straight through `⊙ cell state flow / (long-term memory)` (u≈0.76–0.90, v≈0.63–0.66); the `L` of `LSTM` is crossed by a corner plus mark.
- [hierarchy] The dotted t-rings and gate/information families are swallowed by solid lines — the third layer the legend promises does not read.
- [grid] Left labels (OUTPUT GATE, INPUT SEQUENCE, INPUT GATE) sit in leftover white at u≈0.06 with dashed leaders that end nowhere specific; right labels are ragged against the frame.
- [space] Left third is emptier than the reference (the notes say so); the empty zone is residue of the axis correction, not shaped.
- [depth] Flat and undeclared — no weight fall-off toward the eyes, no over/under at the interleave.

## Next versions
1. **forget-gate-vortex** (mechanism) — Make the gates physical: the red cell-state vortex's sink strength is the forget gate f_t, the black vortex's the output gate o_t, computed from a real small LSTM run over a short sequence; draw T stacked time slices so the red spiral visibly retains its winding (f≈1) while the black one resets. The labels and legend shrink to a footer line. Mechanism in the geometry beats labels on a fluid.
2. **asymmetric-reference** (faithful) — Restore the reference's asymmetry while keeping both eyes on the axis: unequal strengths (black ~1.4× red) so the saddle drops below centre and the black lobe dominates the top 60 %, add the reference's right-side cell-state convergence node (u≈0.78, v≈0.64) as a third sink, and give the dotted t-rings occupancy priority so they read as a separate layer.
3. **memory-strata** (abstract) — Transpose to NESTED: one large red log-spiral as the cell state carrying constant pitch across the whole sheet (long-term memory = one continuous line), with the black hidden state as short spiral fragments that each start at an input dot and die within one turn. Scarce red, abundant black, the difference in persistence is the whole point.

**If only iterating:**
- Make the black vortex ~1.4× the red one's strength so the saddle sits at v≈0.55 and the black lobe dominates; test: the two lobes are visibly unequal in area.
- Clear a halo around every label block (esp. `cell state flow` at u≈0.76–0.90, v≈0.63–0.66) and move the top-left plus mark off the `L`; test: no stroke crosses any glyph.
- Give the dotted t-rings first claim on the occupancy grid so four eccentric dotted rings read as a separate layer at 1 m.
