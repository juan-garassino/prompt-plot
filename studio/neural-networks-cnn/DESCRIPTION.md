# CNN — FROM PIXELS TO MEANING — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/neural-networks/cnn` |
| current render | `gallery/neural-networks/cnn/promoted/pp_cnn_dashes.png` (gcode beside it: `pp_cnn_dashes.gcode`) |
| source | `promptplot/generative/pieces/ml.py::bauhaus_locality` (earlier `bauhaus_locality_v1` in the same file) |
| paper · pens | a4 portrait (210 × 297 mm), cream · 1 crimson = receptive-field frustum (cap mesh on the top terrain, draped window squares, 4 dashed rails, centre dots) · 2 black = all five terrain meshes, top-layer contours, axis, all type |
| status | unreviewed (no FEEDBACK.md; sits in `promoted/`, three earlier renders in `prior-approved/`) · 12 renders on disk |

## In one line
Convolutional abstraction drawn as a **stratified / laminar stack** of five hidden-line wireframe terrains rising up the sheet — layer depth is blur (crunchy near-flat PIXELS at the bottom → one smooth tall OBJECTS peak at the top), and a crimson frustum that widens upward is the growing receptive field.

## What is on the sheet
Coordinates are normalised to the A4 sheet (u → right, v → down). Drawable area (green dotted in preview) is u 0.07–0.93, v 0.05–0.95.

1. **The terrain stack (dominant mass)** — five isometric wireframe terrains, each ≈ 0.60 of sheet width, stacked bottom-to-top and staggered right by ≈ 0.04 per step, so the stack climbs slightly to the right. Each is a draped (u,v) mesh of ~42 × 42 quads with z-buffer hidden-line removal.
   - **PIXELS** (bottom): u 0.14–0.75, v 0.76–0.81. Almost flat (amplitude ≈ 0), a thin parallelogram. Its near (lower) half inks nearly **solid black** — the foreshortened grid rows sit closer than the pen can separate.
   - **EDGES**: u 0.17–0.79, v 0.61–0.69. Low, high-frequency ripple; the mesh reads as short broken dashes along the ridges.
   - **TEXTURES**: u 0.21–0.82, v 0.45–0.55. Medium rolling relief; ragged fringe on the far/right edge (u ≈ 0.75–0.80) with loose zig-zag fragments.
   - **PARTS**: u 0.25–0.87, v 0.26–0.41. Tall, deep undulations, heaviest mesh on the sheet; detached quad fragments float at the right end (u 0.80–0.87, v 0.27–0.31).
   - **OBJECTS** (top): u 0.29–0.90, v 0.12–0.28. One steep smooth peak whose summit (u 0.45–0.60, v 0.12–0.19) is meshed in **crimson** — the only crimson mass on the sheet. Faint black iso-contours (marching squares) run on this top surface.
2. **The receptive-field frustum (crimson)** — at each terrain, a draped crimson square outline around (u 0.42, v 0.42 of that terrain), growing layer by layer; a small crimson dot at each square's centre; and **four dashed crimson rails** (dash 1.8 mm / gap 3.6 mm) joining the corresponding corners. At the bottom the rails start ≈ 7 mm apart at u 0.38–0.45 (v 0.80); at the top they have fanned to u 0.40–0.71 (v 0.24–0.28). The rails and squares are drawn over the meshes with **no occlusion** — the squares show through the terrains in front of them. On the OBJECTS layer the "square" is so large its edges become two long straight crimson chords from u 0.29 v 0.28 up to the cap.
3. **Left axis** — one black vertical rule with open arrowheads at both ends, u 0.11, from v 0.19 to v 0.81 (≈ 0.62 of sheet height). Label above: `M O R E   A B S T R A C T I O N` (u 0.12–0.26, v 0.175); label below: `S P A T I A L   R E S O L U T I O N` (u 0.12–0.28, v 0.835).
4. **Layer labels** — letter-spaced hairline caps just right of each terrain's right end: `P I X E L S` (u 0.67, v 0.79), `E D G E S` (u 0.70, v 0.70), `T E X T U R E S` (u 0.73, v 0.50), `P A R T S` (u 0.76, v 0.34), `O B J E C T S` (u 0.81, v 0.15). Several are grazed by their own terrain's fringe (TEXTURES' first letter is clipped by the mesh at u 0.73).
5. **Title block** (top-left) — `C N N` (≈ 4 mm cap height, u 0.10–0.16, v 0.085) and beneath it `F R O M   P I X E L S   T O   M E A N I N G` (u 0.10–0.46, v 0.115). The subtitle's right half sits directly over the OBJECTS summit at ≈ 4 mm clearance.
6. **Footer** — `M 1:80` at bottom-right (u 0.77–0.88, v 0.93); the colon does not render, it reads `M   1   8 0`.
7. **Quiet zones** — a band v 0.84–0.92 across the full width (the footer floats alone in it), the left strip u 0.13–0.20 between the axis and the stack, and the right margin u 0.88–0.93 beside the lower three terrains.

## The science it encodes
From the `bauhaus_locality` docstring (`promptplot/generative/pieces/ml.py`): "a CNN as a rising valley of feature terrains … each layer changing MORPHOLOGY with depth via a depth-varying box-blur: crunchy PIXELS → smooth OBJECT peaks. One crimson RECEPTIVE-FIELD frustum climbs from a small input patch to the tallest high-level peak — the single thread of data being abstracted."
- Brief `studio/nets/cnn.md` (Essence: "a network distils raw pixels into meaning by stacking increasingly abstract feature maps… A single input patch's influence widens up the stack") also asks for a bottom mini-diagram "receptive field shrinking grid → window → single cell" — present in v3–v5, absent from the current render.
- **Computed:** each terrain is seeded fbm at a falling frequency (11 → 1.6) and rising amplitude (0.004 → 0.19 H), box-blurred `i` times at layer `i`; the top layer is re-weighted by a Gaussian around its argmax to force one dominant peak. The crimson window half-width grows linearly `0.045 + 0.052·i` in surface units.
- **Decoration / not real:** no convolution is computed, no trained weights are used, the frustum growth is a linear rule not a kernel/stride calculation, and the fbm seed is unrelated between layers — the "parts" do not compose into the "object". The render shows smoothing-with-depth faithfully; it does not show locality (a kernel window acting on its neighbourhood) except as the crimson square.

## How it got here
- **v1–v3 (`bauhaus_locality_CNN_v3_seed7`)** — title `LOCALITY IN SPACE`, five sparse coarse meshes, one dashed crimson vertical through the stack, a small crimson cross on each layer, a footer of three 6×6 kernel grids joined by dashes plus the caption `SMALL WINDOWS / DEEPER PATTERNS / A LARGER PICTURE` (overprinted onto the `PIXELS` axis label at preview size). Light, legible, schematic.
- **v4/v5 (prior-approved, `v5_seed2`)** — four layers (PIXELS / LOW-LEVEL / MID-LEVEL / HIGH-LEVEL), denser mesh, first crimson summit cap. `pp_CNN_engine_v1` is the cleanest of the lineage: fine lines, tall crimson cap, the three kernel grids and three-line caption in the bottom band. That bottom band is what gave the sheet a grounded base.
- **p0 (`pp_p0_bauhaus_locality`)** — rename to `FROM PIXELS TO MEANING`, five semantic layers (PIXELS→OBJECTS), the frustum becomes four **solid** crimson rails fanning from the pixel patch to the peak, `M 1:80` footer, kernel-grid footer dropped. Code note: "plot feedback: the solid red wires dominated the terrains".
- **current (`pp_cnn_dashes`)** — the same composition with the rails turned into sparse dashes. Gained: the terrains now dominate and the rails whisper. Lost vs engine_v1: the bottom caption/kernel band (the sheet now has an empty bottom 15 %), and the top layer's cap is less clean (see Weak).
- No verdict from Juan on record.

## Keep — what works
- The **morphology gradient up the stack**: near-flat dense PIXELS (v 0.78) → rippled EDGES → rolling TEXTURES → deep PARTS → one smooth peak. Read bottom-to-top it is the idea, without the labels.
- The **single crimson summit** (u 0.45–0.60, v 0.12–0.19) as the one loud accent — scarce and at the top, the reading destination.
- The **dashed rails fanning upward** (≈ 7 mm apart at the bottom → ≈ 60 mm at the top): the receptive field growing is legible, and as dashes it no longer out-shouts the meshes.
- The **rightward stagger** of the stack (≈ 0.04 W per layer) — a gentle diagonal instead of a centred totem.
- Hidden-line occlusion on the terrains themselves: near ridges hide far ones, each layer reads as a solid surface.

## Weak — what doesn't
- [craft] **Straight black chords across the crimson cap** (u 0.46–0.62, v 0.13–0.17): the top-layer contour loop `continue`s over points inside the cap instead of breaking the polyline, so each contour jumps across the cap in a straight line. Same layer: the jagged broken ridge fragments just below the cap (v 0.15–0.18).
- [craft] **Crimson geometry is not occluded**: window squares and rails are appended after the scene and show through the terrains in front of them (visible inside TEXTURES at v 0.50 and PARTS at v 0.33). On OBJECTS the window is so large its 4-corner "square" becomes two long straight crimson chords (u 0.29→0.47, v 0.28→0.19) that don't drape at all.
- [craft] **PIXELS floods**: the near half of the bottom layer (v 0.79–0.81) is nearly solid black — foreshortened row pitch well under 0.8 mm. EDGES breaks into crumbs for the same reason (thinning cuts rows into dashes).
- [craft] Travel ≈ draw (17.7 m vs 17.9 m) — the fragmented meshes cost as much air as ink; detached quad debris floats off PARTS (u 0.80–0.87) and TEXTURES (u 0.75–0.80).
- [concept] It is a **scientific figure / textbook diagram**: stacked layers + a labelled two-headed axis (`MORE ABSTRACTION` / `SPATIAL RESOLUTION`) + per-layer labels is exactly the Zeiler–Fergus slide. Rubric § 6 NO SCHEMATICS. The terrains are seeded noise, so "PARTS" has no relation to "OBJECTS"; the order (laminar stack) is asserted by labels, not built by the data.
- [tension] The stack is a centred column with even left/right air; the only diagonal is a 0.04 W stagger. Nothing crops at the frame.
- [space] The bottom band v 0.84–0.92 is leftover, not shaped — the footer floats alone in it; the gaps between terrains are uniform (~0.15 H), so rhythm is metronomic.
- [hierarchy] Five terrains of near-equal width compete; only the crimson cap separates the top. At 3 m it reads as "five similar grey smudges".
- [grid] Labels hang wherever each terrain ends (u 0.67 → 0.81, a ragged diagonal) and several collide with mesh fringe; the title block's left edge (u 0.10) and the axis (u 0.11) almost but don't share an edge; `M 1:80` loses its colon.
- [depth] Depth exists within each terrain but the stack itself has no atmospheric falloff — the far (upper) layers are heavier than the near ones, inverting the usual cue.

## Next versions
1. **pooling-cascade** (abstract) — Replace terrains with the actual geometry of convolution: a laminar cascade of square lattices, each layer's cell pitch = previous × stride, cells inked by `tone_dots` from a real feature map of one image through a small trained CNN (or a fixed Sobel → Gabor → pooled bank). The receptive field is the only crimson: one cell at the top and the exact k×k·stride footprint it sees on every layer below, nested squares. Order = **nested / tessellated**; mapping "cell pitch is stride, crimson footprint is exact receptive field". Kills the schematic reading because nothing is labelled a layer; the halving lattice IS the depth.
2. **one-valley** (mechanism) — Keep terrains but make them ONE computation: layer i = real activation map (e.g. from a real image) at conv depth i, so the top peak sits where the object actually is and the crimson frustum is the computed receptive field of that argmax unit. Drop the axis and per-layer labels; one title. Push the stack into a strong diagonal that crops the top-right corner, give PIXELS the whole bottom width, fix occlusion (crimson through the z-buffer) and flooding (row thinning on the near edge).
3. **blur-as-tone** (lens) — A single large terrain seen once, with the sheet's vertical axis as depth: bottom rows drawn at pixel resolution (short dashes, high frequency), each band upward re-sampled coarser, so the same landscape "zooms out into meaning" continuously — a density gradient, not five slabs. Crimson carries only the window.

**If only iterating:**
1. Break the top-layer contour polylines at the cap boundary (no straight black chords across the crimson summit) and route crimson squares/rails through the Scene3D z-buffer so they hide behind nearer terrain; drape the top window along the surface instead of 4 straight corners.
2. Thin the PIXELS near edge and the EDGES rows so no two rows sit < 0.8 mm apart; remove floating quad debris (any mesh chain < 3 quads).
3. Replace the labelled two-headed axis with nothing (or one quiet word), and use the freed left strip + the empty bottom band to push the stack into a real diagonal that crops at the right or top frame.
