# ATTENTION AS RESONANCE (Dalí engraving oracle import) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/ip_engraving` |
| current render | `gallery/studio/ip_engraving/current/ip_engraving_oracle.png` (paired gcode `ip_engraving_oracle.gcode`: 59.7 m draw, 34.0 m travel, 171,932 commands, 24,678 pen cycles, 4 layers, bbox x 3.9–270.9 × y 84.1–417.0 mm) |
| source | **Nothing in PromptPlot generates it.** The plate is the oracle SVG `gallery/references/oracles/interpretive_plotter/results/verification/dali_engraving/dali_attention_engraved.svg` (24,678 paths in 4 nib layers) run through the SVG importer (`promptplot/importers/svg_import.py`). The upstream generator is `gallery/references/oracles/interpretive_plotter/scenes/dali_engraving/reconstruct_surreal.py` + `engrave_surreal.py` + `plot_engine.py` (read-only). The native rebuild is briefed, **not built**: `studio/reconstructions/engraving-repro.md`, reference `studio/reconstructions/engraving-repro/ref/reference.png`. |
| paper · pens | A3 portrait (297 × 420), white. **All four layers are black ink at different nibs** (oracle `pen_plan.json`): 0 = 0.10 mm broken highlights + fine shading (17,889 paths) · 1 = 0.18 mm form lines, hair, internal detail (6,247) · 2 = 0.25 mm structure, lettering, flows (479) · 3 = 0.35 mm silhouette accents + deep shade (63). The preview paints them black / red / blue / green, so every red or blue mark in the png is black ink on paper. |
| status | unreviewed (no feedback) · 1 render + 1 gcode on disk |

## In one line
The same transformer block as a **surreal copper-plate engraving (flow-to-attractor draped over a stage)**: melting crowned figures Q and K breathe rays onto a chessboard, the board drips into an `A = softmax(QKᵀ/√d_k)` basin whose root-like flows feed `Z = AV`, the FFN is three vaulted chambers (W₁ · σ() · W₂), and the residual is a swoosh under them. All tone is made of real line: dashes, nets and guided families.

## What is on the sheet
Positions are on the A3 page as rendered. **The whole plate sits too high and too far left** (see Weak).

- **Chessboard (focal, u 0.25–0.75, v 0.29–0.37).**
  - A perspective board with dark squares hatched (0.18, red in preview) and about 20 engraved pieces (bishops, queens, pawns, a knight, a rook) in 0.18/0.10.
  - The slab underneath is dense 0.10 dash-screen with long melting drips (0.35 outlines) hanging to v ≈ 0.44.
  - `A = softmax(QKᵀ/√d_k)` in 0.25 lettering on the slab front (u 0.36–0.53, v 0.40–0.43).
- **Q (upper-left figure, u 0.10–0.35, v 0.02–0.40).**
  - A long melting robed figure, crowned (0.25 + 0.18 crown with ball finials).
  - Its face is engraved as a 0.10 dash/dot screen (reads as a black halftone in the preview) with hair as 0.18 flow families.
  - The robe is a warped net of broken rows with drips ending at v ≈ 0.40, and a hatched arch-hole through the body at u 0.13–0.17.
  - Label `Q` at u 0.34, v 0.26. About 8 straight 0.18 rays go from its mouth to the board.
- **K (upper-right figure, u 0.58–0.82, v 0.03–0.33).**
  - A crowned figure with a cross finial, holding a sceptre topped by an orb (u 0.68–0.72, v 0.25–0.40).
  - Its robe drapes and drips over a hatched block on the right edge (u 0.73–0.82, v 0.28–0.47).
  - Label `K` at u 0.70, v 0.25. About 6 rays to the board.
- **Between the heads, top-centre.**
  - A glass sphere with a liquid meniscus (u 0.44–0.58, v 0.03–0.13) and a drip stem. A black spike artefact sticks out of its top at v ≈ 0.02 where the plate hits the top margin.
  - Two tall 0.25 arches, hatched inside (u 0.34–0.37 and 0.45–0.48, v 0.10–0.21).
  - Four long horizon lines (0.10) from u 0.10 to 0.82 at v 0.17–0.21, with cypress spikes (0.18) and a distant mountain.
  - `Q K^T / √d_k` above the board at u 0.46–0.52, v 0.20–0.23.
- **Floating tables with tiny figures** (right, u 0.78–0.90, v 0.02–0.12 and 0.21–0.27), with drips. A **melting clock** on the right block edge (u 0.78–0.88, v 0.28–0.36), numerals `1 2 3 7 4 5 6`.
- **V, the cellist (left, u 0.04–0.30, v 0.33–0.56).**
  - A seated figure with hair streaming left in 0.18 flow lines (u 0.04–0.10, v 0.34–0.36).
  - The cello in 0.25 with an engraved body, the bow and a hand. Label `V` at u 0.06, v 0.37.
  - Her robe is a deep 0.10/0.18 net, the darkest mass on the sheet.
- **Flows.**
  - A bundle of ~8 parallel 0.25 lines from the cello sweeps right to the slab stem (u 0.30–0.50, v 0.47–0.53).
  - About 13 root-like 0.25 flows descend from the slab and fan out, each ending in a small bead circle on the chamber roof at v ≈ 0.49.
  - Three free bubble circles float at u 0.40–0.43, v 0.46–0.49.
  - `Z = AV` at u 0.48–0.54, v 0.48. `FEEDFORWARD` (0.25) at u 0.73–0.82, v 0.45.
- **FFN chambers (u 0.33–0.80, v 0.50–0.65).** Three vaulted rooms in one hatched block:
  - `W₁`: four pawns inside tilted glass frames.
  - `σ()`: hyperboloid hourglasses, one large central.
  - `W₂`: pawns becoming hourglasses.
  - Tiny arrows join the rooms. An entry pawn sits on the left shelf (u 0.26) and an exit pawn with label `Z'` on the right shelf (u 0.83, v 0.56–0.61).
- **Residual.** A long lens-shaped swoosh (0.35 outline) under the chambers (u 0.28–0.70, v 0.63–0.66). A basin below with deep drips down to v ≈ 0.80 (the lowest drip is filled solid dark in 0.18).
  - `H = Z' + X` / `(RESIDUAL CONNECTION)` at u 0.41–0.60, v 0.67–0.70.
- **Lower-left.** A dead tree (0.25) and a melting clock (`1 2 9 3 6`) at u 0.05–0.25, v 0.63–0.75. A horizon line with mountain bumps at v 0.75. Stacked 0.18 dashes (the reflection) at v 0.76–0.78.
- **Type columns** (0.18, small caps):
  - Left: `QUERIES / KEYS / VALUES / ATTENTION / FEEDFORWARD / REPRESENTATION` + a rule (u 0.06–0.18, v 0.16–0.24) and `INPUT / TOKENS / X ∈ ℝ^{nxd}` (u 0.06–0.18, v 0.29–0.34).
  - Lower-right: `SAME / INFORMATION / DIFFERENT / FOCUS / DEEPER / MEANING` + a rule (u 0.83–0.88, v 0.73–0.78).
- **Title.** `ATTENTION` / `AS` / `RESONANCE` in 0.25 open caps, top-left (u 0.05–0.28, v 0.00–0.10). `ATTENTION` is cut by the top margin and hidden under the preview's stats box.
- **Bottom 20 % (v 0.80–0.98) is empty paper**, because of the misplacement.

## The science it encodes
Allegory, no computation. Same block as `ip-cubist`: Q and K are figures whose breath (rays) scores the board, softmax is a basin, `Z = AV` is roots feeding the chambers, the FFN is W₁ → σ → W₂ rooms, and `H = Z' + X` is the swoosh. The rays land on arbitrary pieces.

The oracle SVG's own `<desc>` says: "source diagram labels are retained, not independently validated as a complete transformer block."

**How faithful it is to the reference** (`studio/reconstructions/engraving-repro/ref/reference.png`):
- Every object is kept: both crowned figures, the sphere, arches, floating tables, melting clocks, cellist, board with drips, chambers, the residual swoosh, the tree, and both word columns.
- `QKᵀ` is typeset as `Q K^T`.
- Pigment and paper tone are dropped, as intended.
- The oracle's own preview (`.../dali_engraving/dali_attention_engraved_preview.png`, true nib widths) reads as a silver-grey engraving with open faces. This preview reads as a black dot-screen, because every 0.10 dash is drawn at display width. The faces in particular look like a halftone, which is the failure TRACING IS NOT AUTHORING names, though here it is a preview artefact, not the geometry.

## How it got here
One render, a straight import. There is no PromptPlot iteration. Upstream versions are in `gallery/references/oracles/interpretive_plotter/results/history/` and `CHANGELOG.md`. The native rebuild is expected to "drive most of the tuning in `engine/material.py`" (`studio/reconstructions/README.md`). No Juan feedback recorded.

## Keep — what works
- **Material grammar by object**, the reason this is the oracle for `material.py`:
  - skin and cloth as warped nets of broken rows (`surface_grid` + `cut_tone`);
  - hair, drips and flows as guided families with a travelling highlight (`flow_family`);
  - deep shadow only as crossed nets;
  - eyes and lips left open.
- **Four nibs by role**: fine shading 0.10, form 0.18, structure/type 0.25, silhouette accents 0.35. The heavy line is scarce (63 paths) and lands only on silhouettes.
- **The drip vocabulary.** The board slab, robes and basin all melt the same way. It unifies the sheet and is the Dalí signature.
- **The root flows from slab to chambers ending in bead circles.** It is the one flow-to-attractor gesture that actually carries "A is applied to V" as a direction.
- **Composition.** Two figures leaning in, a central board, a descending cascade to the chambers, and a residual swoosh underneath. There is a strong vertical spine, and the left cellist balances the right clock block.

## Weak — what doesn't
- [grid] **The plate is misplaced on the page.**
  - The import bbox is x 3.9–270.9, y 84.1–417.0 mm. The oracle places the same art at ≈ x 12–285, y 40–380, centred with ~40 mm margins.
  - So it is ~8 mm left and ~25–36 mm high: the title and the sphere run past the 10 mm top margin (the sphere top is truncated into spikes), the cellist's hair is at x 3.9, and the bottom 80 mm is blank.
  - Likely cause: this is the only one of the three oracle SVGs in px units with an outer `<g transform="translate(49.3,162.1)">`, and the importer did not honour it. Verify in `svg_import.py` before any plot.
- [craft] The preview is not the drawing. At display width the 0.10 broken-highlight layer turns faces and robes into a black dot-screen. AUTHORING acceptance question 4 ("are the blackest regions intended?") and question 5 (label legibility at true width) cannot be judged from this png, and the layer colours imply inks that do not exist.
- [concept] NO SCHEMATICS / illustration. This is figuration with equations hung on objects: kings, queens, a cellist, clocks. The rubric's collection rule cuts it outright. The only defence is that it is a reference reconstruction, judged as an interpretation.
- [concept] The rays hit arbitrary pieces, and the chambers' pawns → hourglasses → pawns are decorative. Nothing the eye can check is a real attention quantity.
- [craft] Plot cost: 24,678 pen cycles and 34 m of travel. The brief estimates a 12–15 h plot, which Leo cannot hold without the unbuilt re-zero checkpoints.
- [space] The upper half is crowded (heads, sphere, arches, horizon lines, floating tables, clock, two word columns all above v 0.4) while the lower 20 % is empty. The emptiness is a placement accident, not a shaped quiet zone.
- [hierarchy] Title and word columns are fine-nib small caps; the title is a caption, not a dominant element. On the reference too, the board rather than the title is the only 3 m read.

## Next versions
1. **native engraving** (faithful) — Build `engraving-repro` as an authored `Scene` with the material layer: `surface_grid` + `gauss_tone` per face and robe, `flow_family` with highlight on hair and drips, `dark_edge` on the 0.35 nib, and `suppress_parallel` before compile. Place it with the oracle's 12 / 39 mm offsets, render at true nib widths, and run AUTHORING §6 on a face, a drip, the board, the lettering and a flow junction. This is what the slug is for, and it will tune `material.py`.
2. **two-nib, half-time** (craft) — Keep the oracle geometry but make it plottable on Leo:
   - Merge 0.10 + 0.18 into one 0.2 fine layer by thinning the broken-highlight rows to the `physical_spacing` floor.
   - Merge 0.25 + 0.35 into one 0.4 structure layer.
   - Cap pen cycles at ~10k and travel under 15 m, and add re-zero checkpoints between layers.

   This buys a real plotted proof, which beats a perfect screen render that never reaches paper.
3. **rays that mean it** (mechanism) — Keep the surreal stage, but let the one computable gesture be true:
   - Q's rays go to the top-k keys of a real attention row (GPT-2 `attn_npz`), with ray multiplicity ∝ weight.
   - K's rays trace the transpose.
   - The number of root flows from the slab into each chamber = the actual output token count.
   - The drip lengths under the board = the per-row softmax entropy.

**If only iterating:**
- Fix placement: re-import honouring the SVG's outer translate (or shift by the measured offset) so the artwork box sits at ≈ x 12–285, y 40–380. Confirm the title `ATTENTION` and the sphere top are whole, with ≥ 10 mm clearance from every edge.
- Re-render with `pen_widths=[0.10, 0.18, 0.25, 0.35]` in black only, with the legend off the artwork. Faces must read as open, broken-line engraving, not a dot-screen.
- Check the black spike cluster above the sphere and the solid-dark drip under the basin (u ≈ 0.28, v 0.74–0.80). Either justify each or thin it to the 0.10 spacing floor.
