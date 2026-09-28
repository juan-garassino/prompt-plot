# CONVOLUTIONS — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/convolutions` |
| current render | `gallery/studio/convolutions/current/pp_convolutions_v1.png` |
| source | `studio/convolutions/rounds/r01/piece.py::convolutions` |
| reference | `studio/convolutions/ref/reference.png` (1536×1024, the reconstruction target) |
| paper · pens | a4 landscape, cream · 0 black = input blob X, type, furniture, dots, receptive-field cone · 1 crimson = tiles 1 & 5, kernel cells, first connector fan, one feature map · 2 dodgerblue = tile 3, kernel cells, output connectors, one feature map · 3 olive = output blob Y, tile 4, kernel cells, one feature map |
| status | unreviewed (no FEEDBACK.md) · 1 render on disk · **the studio's quality benchmark** (memory: "the best plate is r01, not v13") |

## In one line
A convolution pipeline drawn as a **laminar flow band with nested whorls** — input field X (black trefoil of distance-field rings) → five kernel tiles (concentric rings around a starburst) → output field Y (olive trefoil), with the kernel bank, receptive field and feature maps as a three-part footnote row beneath.

## What is on the sheet
All positions normalised to the sheet (u → right, v → down). The ink lives inside a 13 mm frame on all four edges.

**1. The flow band (dominant mass, v ≈ 0.20–0.53).** A horizontal left→right reading across the full width.
- **Blob X** (black) at u 0.04–0.20, v 0.21–0.48 — a three-lobed trefoil (lobes pointing left, up-right, down), ~0.16 sheet width. Filled with ~11 nested dashed/solid rings that follow the outline inward (distance-field contours) with a small eye in the left lobe. ~20 solid black dots of varying size sit on the rings; two little clusters of short crossed dashes sit inside the left lobe (u≈0.12, v≈0.28) and the lower lobe (u≈0.13, v≈0.40). Letter **`X`** at u≈0.10, v≈0.41, outside the blob's lower-left.
- **Hub**: a large black dot on blob X's right rim (u≈0.18, v≈0.33), from which a fan of ~10 curves (alternating black solid, black dashed, crimson solid) spreads right to the first tile. Small black dots ride several curves.
- **Tile strip**: five portrait rectangles (each ≈ 0.063 sheet wide × 0.107 tall, black keyline), u 0.29–0.71, v 0.33–0.43, on a regular ~8 mm gap, centred on u = 0.50. Colours in order: **crimson, black, blue, olive, crimson**. Each tile holds dashed concentric rings around a central starburst of ~20 straight rays and a solid centre dot, with scattered solid dots. In each gap: a column of three dots (u-centred in the gap) and short connector stubs that disappear behind the tiles and reappear in the next gap. A short vertical tick sits above each tile (v≈0.29).
- **Display labels** above the strip: **`K * X`** centred at u≈0.49, v≈0.28 and **`σ(·)`** at u≈0.63, v≈0.28 (sigma drawn as a mark). A dashed black ellipse arc terminates just left of the `K`, reading as a small `>` pointer.
- **Dashed ellipses**: five large dashed ellipses (black ×3, blue, olive, one crimson arc above) loop above and below the strip, reaching down to v≈0.53; they are clipped out of the strip slab, so they appear to pass behind it.
- **Output connectors**: blue and olive curves from tile 5 converge on a dot at blob Y's left rim (u≈0.81, v≈0.33).
- **Blob Y** (olive) at u 0.80–0.96, v 0.22–0.45 — a second trefoil (lobes up-left, right, down), ~11 nested rings, dots, **`Y`** at u≈0.90, v≈0.41 just outside its lower right.
- **Vertical dashed spines**: one at u = 0.505 running the full height from v 0.08 down through the strip, the gutter and the cone to v≈0.87; a second at u≈0.845 from v 0.08 to v≈0.50, cutting through blob Y.

**2. Title block (top-left, v 0.07–0.17).** `CONVOLUTIONS` in spaced caps at u 0.04–0.20, v≈0.08; a short rule under it; then three spaced lowercase lines: `local patterns` / `global structures` / `continuous perception`. Below blob X: a crosshair rule (u 0.04–0.16, v≈0.505) carrying the label `input x`.

**3. Top-right note (u 0.89–0.96, v 0.08–0.12).** Four tiny spaced lines `stride` / `padding` / `dilation` / `channels`, underlined, a dot on the rule's left end. Sits pressed against the top-right corner of the frame.

**4. Furniture.** Four quarter-circle "corner bracket" marks (u≈0.18, 0.38, 0.49 top; u≈0.55 v 0.26; u≈0.87 v 0.60), plus marks (u≈0.10 v 0.44, u≈0.25 v 0.28, u≈0.75 v 0.67), a hollow square at u≈0.86 v 0.67 joined to the plus by a hairline, and ~30 solid black dots of 3 sizes scattered through the band and the gutter.

**5. Gutter (v 0.54–0.61).** Clear paper across the whole width apart from the two spines and three dots.

**6. Lower row (v 0.60–0.87), three zones on one baseline, equal gutters.**
- **Kernel bank** (u 0.04–0.27): 3 × 3 grid of square cells (~0.07 sheet wide each), each cell subdivided 3 × 3 by coloured rules; inside: a dashed ring whorl, a solid centre dot and grid dots; four cells carry a diagonal-hatched corner or edge sub-square. Colours by row: crimson/black/blue · olive/crimson/crimson · blue/olive/black. Caption `kernel bank` below at v≈0.90.
- **Receptive field** (u 0.39–0.61, apex v≈0.60, base v≈0.87): a black dashed parabola/triangle envelope over ~9 nested closed teardrops (solid), pointed at the top, widest ~63 % down, open to the base; flanks outside the teardrops filled with sparse short horizontal dashes (stipple). The centre spine runs through its axis; a large dot sits in the smallest teardrop, two dots above the apex. Caption `receptive field` at v≈0.90.
- **Feature maps** (u 0.73–0.96, v 0.77–0.87): three landscape tiles, crimson / blue / olive, each filled with ~6–10 widely spaced wavy contour lines and 2–3 black dots. Caption `feature maps` at v≈0.90.

## The science it encodes
From `piece.py` docstring and `rounds/r01/NOTES.md`: a 2D convolution `Y = σ(K ∗ X)` — an input field is swept by a bank of kernels whose local responses stack into output feature maps; the dashed ellipses read as **overlapping receptive fields**, the cone as how the receptive field grows with depth. What is exact: every contour ladder (blob rings are level sets of a distance-to-boundary field with |∇d| = 1, so pitch = level step; whorls are conical `a·exp(−r/σ)` cusps with a geometric ladder `F_k = a·e^(−k·pitch/σ)`); measured min spacings 0.86–1.18 mm in every family; all tones are `kit.tone_dots`. What is decoration: blob shapes (seeded trefoil harmonics), kernel-cell contents, feature-map contours (seeded fbm) — no real convolution is computed; the feature maps are **not** the output of the drawn kernels on the drawn X. The placement of every element was measured off the reference raster and recorded in normalised coordinates in the source header.

## How it got here
One round (r01), six internal iterations in NOTES.md: `_dash` float-phase hang fixed → gaps and ellipse routing → metaball blobs collapsed to an egg and the cone contoured in a wedge came out a solid black triangle (both reverted) → trefoil harmonics tested side-by-side, cone rebuilt as measured parabola + teardrops → teardrops closed at the mouth → geometric level ladders and spacing verified. Versus the reference: nothing clipped (reference bleeds off the bottom), ellipses routed behind the strip instead of across it, three lower zones on one baseline with equal 36 mm gutters (reference: 33/17 mm, three different bottoms), a 14.2 mm empty gutter where the reference had 1.3 mm of air full of arcs, tile gap 0.28× → 0.43× tile width. Lost vs. reference: blob ring count (~15 → 11), the reference's fine grey wash, serif/italic type, denser whorls with rays breaking out of the tiles. No feedback from Juan recorded.

## Keep — what works
Why this is the benchmark — it was **measured, not guessed**, and every spacing decision is structural:
- **One axis ties three zones**: u = 0.50 carries the strip centre, the dashed spine and the cone apex; the spine runs uninterrupted v 0.08 → 0.87, so the upper and lower bands lock together.
- **Gutters equal by construction**: the kernel bank and the feature maps are built from the same `3 × cell + 2 × gap` width and the cone sits on the centreline, so both lower gutters are 36.1 mm whatever the cell size; one bottom baseline (v≈0.87) and one caption baseline (v≈0.90) for all three.
- **The 14 mm empty gutter at v 0.54–0.61** is treated as a zone (scatter, ellipses and furniture excluded) — it is why the flow band reads as one mass and the lower row as a footnote.
- **Depth by clipping, not by collision**: connector curves vanish behind each tile (+1.1 mm) and reappear in the gaps; the dashed ellipses pass behind the strip slab. Every overlap on the sheet is one of these two defended cases.
- **Contour discipline**: blob rings from a distance field (constant pitch to the medial axis, no flooding), whorls from geometric level ladders — rings stay continuous, which is the plate's dominant texture. Min gap ≥ 0.86 mm everywhere.
- **Colour as a sequence**: the tile strip runs crimson → black → blue → olive → crimson, and the pen identity travels — X is black, Y is olive, the first fan is black+crimson, the last is blue+olive — so colour carries the transformation left→right.
- **Two blobs as bookends**: similar trefoil mass (~0.16 width each) at the two ends of the band at the same height, one black one olive, is a strong input/output rhyme.
- **Receptive-field cone**: mostly white paper inside a dashed envelope, teardrops closing at the mouth, stipple only in the flanks — the one element in the lower row that reads at 1 m.

## Weak — what doesn't
- [concept] It is a **pipeline schematic**: input → labelled operator `K * X` → `σ(·)` → output, plus captioned inset panels (`kernel bank`, `feature maps`). By § 6 NO SCHEMATICS this is textbook-figure territory; it survives on craft, not on an abstract order.
- [concept] Nothing is computed: the feature maps are not the convolution of anything on the sheet, the tiles are identical whorls in different pens. The mechanism (a small kernel sliding and summing) is never visible as a *process*.
- [tension] The composition is bilaterally symmetric about u = 0.50 (blob / strip / blob, bank / cone / maps). Balanced and calm, but by the rubric centred-symmetric caps tension.
- [concept] ~30 scattered black dots, four quarter-circle brackets, plus marks and the hollow square carry no data — decoration inherited from the reference.
- [craft] Tile interiors: 20 straight rays overprint the dashed rings and dots; at 1 m each tile reads as a muddy starburst, not a whorl. Crossed-dash clusters inside blob X (u≈0.12 v≈0.28, u≈0.13 v≈0.40) read as scribble over the rings.
- [craft] The dashed ellipse clipped at the `K` box leaves a `>` pointer shape in front of `K`, i.e. an accidental arrow.
- [space] The `stride / padding / dilation / channels` block is jammed into the top-right corner against the frame, and the second spine at u≈0.845 cuts straight through blob Y.
- [hierarchy] All type is hairline spaced caps/lowercase at caption size; the title does not dominate anything. Dominant mass is the band as a whole, not one element — the two blobs and the strip compete at similar weight.
- [depth] Apart from the behind-the-tile clipping, the plate is flat and the flatness is undeclared.

## Next versions
- **real-kernel** (mechanism) — Compute it. Draw X as the field, pick three real kernels (edge, blur, Gabor), convolve numerically, and make the three feature maps the true iso-contours of `K_i ∗ X`; the tiles become the actual 5×5 kernels as signed Ben-Day discs (radius = |w|, pen = sign). Same layout, same spine, same gutters — but every ring on the right is caused by the rings on the left. Scores higher on [concept] without losing the benchmark craft.
- **sliding-window** (abstract) — Transpose to a **lattice-with-a-travelling-window** order: one large field X fills the left 60 % as a distance-field whorl; a single kernel square is stamped along a diagonal path at stride s, each stamp leaving its response as a nested ring of proportional count; the stamps overlap by exactly (k − s) cells, so dilation/stride become visible spacings. No boxes, no labels except the title. Breaks the symmetry with a working diagonal [tension] and drops the schematic reading [concept].
- **receptive-cone** (lens) — Promote the receptive-field teardrop to the dominant mass (0.5 of sheet height, cropped at the bottom edge), with each nested teardrop being one layer's receptive field computed from kernel size and stride, and the input blob drawn tiny at the apex. Hierarchy becomes 3:1 at a glance; the pipeline shrinks to a footnote.
- **If only iterating:**
  1. Replace the straight-ray starbursts in all five tiles with the whorl rings alone (or ≤ 6 rays that stop at the first ring) so each tile reads as a clean eye at 1 m.
  2. Delete the decorative scatter dots and quarter brackets that sit in the band (u 0.2–0.8, v 0.05–0.53) and move the `stride…channels` block down to share the title block's top line at v≈0.08, 13 mm off the right frame.
  3. Clip the dashed ellipse 3 mm short of the `K * X` label box so no `>` shape points into the `K`, and drop the second spine at u≈0.845 or stop it above blob Y (v ≤ 0.20).
