# SPARSE ROUTING — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/moe` |
| current render | `gallery/studio/moe/current/pp_moe_v1.png` |
| source | `studio/moe/rounds/r01/piece.py::studio_moe` (docstring refers to a NOTES.md that is not on disk) |
| paper · pens | a4 portrait (210×297 mm), white preview · as rendered: 2 forestgreen = routing-margin terrain (cells, terraces, dashed second-expert walls), load bar chart, all type · 1 crimson = the tokens (one short dash each), the hero's two bars · 0 black = a handful of short wall fragments only. (Code names the pens BLUE / PINK / BLACK; the preview shows the default palette.) |
| status | unreviewed (no feedback on file) · 1 render on disk |

## In one line
Mixture-of-experts routing drawn as a **tessellated** order — the exact argmax partition of a 2-D token space by a 16-expert linear gate, lifted into faceted confidence tents by the routing margin, after a simulated rich-get-richer collapse — with the tokens as red dashes and every dead expert left as bare paper.

## Lede
Mixture-of-experts routing drawn as **faceted green tents over a speckle of red tokens**, showing a collapsed router in which most of sixteen experts never fire.

## On the sheet
A cluster of green terraced tents fills the upper centre and right, drawn as nested triangles and chevrons, some edges dashed. Hundreds of tiny crimson dashes speckle two of the tents. Spaced title letters sit top left, a small green bar chart of expert load bottom left, and an empty band between.

## The science
A router sends each token to one of sixteen experts, carving the plane into territories; height shows how confidently a token is routed, with terraces as level lines. A simulated rich-get-richer training run collapses it: five experts hold territory, eleven never fire, and the top one takes 46 percent. The figures are printed in text; nothing on the sheet marks the missing experts.

## What is on the sheet
- **The terrain (dominant mass).** An isometric cluster of faceted tents, ~0.72 of sheet width, spanning u≈0.21–0.93, v≈0.15–0.67, drawn in green as nested terrace rings (polygon offsets) with no mesh fill.
  - **Upper chevron stack**: nested V-shaped terraces pointing down, apex column around u≈0.62, v≈0.15–0.36; its outer terraces are solid on the right face and broken into dashes and `>`/`<` chevrons on the left face.
  - **Left broad tent** (the hero cell): long parallel diagonal terraces running down-right from u≈0.21 to u≈0.60, v≈0.30–0.60, forming a wide sloped plane; its lowest terrace ends in a point at u≈0.47, v≈0.60. At its far left edge a small stack of `<` chevrons with a dotted vertical (u≈0.21, v≈0.33–0.44).
  - **Right tent**: the most legible form — a nested set of ~8 triangles whose apex sits at u≈0.70, v≈0.50 and which open to the right edge of the drawable area (u≈0.93, v≈0.43–0.63); the upper edges are near-horizontal parallel lines (v≈0.43–0.47), the lower ones diagonals.
  - **Lower small tent**: three nested triangles, apex u≈0.59, v≈0.57, at the bottom of the terrain (u≈0.50–0.62, v≈0.55–0.63).
  - Dashed green verticals (the k=2 second-expert walls, per code) at u≈0.70, v≈0.52–0.62 and u≈0.62–0.64, v≈0.56–0.67; a few short black fragments at u≈0.62, v≈0.38 and u≈0.59, v≈0.62.
- **The tokens.** ~900 tiny crimson dashes scattered over two fields: a large loose cloud on the left tent and upper-left (u≈0.33–0.62, v≈0.21–0.50) and a denser band on the upper face of the right tent (u≈0.66–0.93, v≈0.33–0.46). Each dash is ~0.5 mm; at sheet scale they read as a pink speckle, not individual marks.
- **Hero label.** `E05` (u≈0.40–0.44, v≈0.25) and `46  OF  TOKENS` (u≈0.39–0.54, v≈0.26) — the percent sign does not render, so it reads "46 OF TOKENS". A token dash touches the `4`.
- **Title block.** `SPARSE` / `ROUTING` (spaced caps ~5.4 mm, u≈0.07–0.37, v≈0.06–0.10, underline under `R`), `SIXTEEN EXPERTS . TWO FIRE . THE REST IS PAPER` (u≈0.07–0.82, v≈0.13), a small `+` at u≈0.08, v≈0.16. Three-pen swatch stack at u≈0.90, v≈0.06–0.09.
- **Load chart.** At u≈0.07–0.30, v≈0.81–0.86: a green baseline with 16 slots (short dashes under it), green vertical bars at a few slots — two short ones near u≈0.12–0.13, two crimson bars at u≈0.14–0.15, a tiny pair at u≈0.21, and four tall bars at u≈0.28–0.30. Caption `LOAD PER EXPERT   K   2` (v≈0.88; the `=` does not render) and `5 OF 16 HOLD TERRITORY . 11 NEVER FIRE . TOP EXPERT 46` (u≈0.07–0.63, v≈0.89).
- **Footer.** `Y   SUM GI  X   EI  X` (u≈0.54–0.90, v≈0.95) — `=` and parentheses do not render.
- **Quiet zones.** A full-width empty band v≈0.67–0.80 (≈0.13 of sheet height), the left strip u≈0.07–0.20 from v≈0.17 to v≈0.80, and the upper-right u≈0.70–0.93, v≈0.13–0.30.

## The science it encodes
From the `studio_moe` docstring: a real linear gate l_i(x)=w_i·x+b_i over a 2-D token space, N=16 experts, top-k=2. argmax over affine functions gives exact convex cells (Sutherland-Hodgman half-plane clipping, no sampling). Height = routing margin D(x)=l₍₁₎−l₍₂₎, zero on the cell walls; each terrace ring is an exact level set, 8 terraces. Imbalance is simulated: 9 rounds of the un-regularised rich-get-richer update b_i += η(f_i−1/N), η=0.62, until the router collapses. Tokens (900) sit on the terrain at their own margin. The caption reports the result: 5 of 16 experts hold territory, 11 never fire, top expert 46 %. Inside the dominant cell, dotted walls split it by each token's second expert.

What reads: faceted tents and a pink speckle. What does not read: that there were 16 experts and 11 vanished (nothing marks the missing ones), which cell is the 46 % winner (the E05 label floats above a field of speckle), and the k=2 subdivision (the dashed verticals look like construction lines).

## How it got here
Single render (v1, round r01); no trials on disk and no feedback from Juan. The brief (`studio/nets/moe.md`) asked for a black token stream shattering on a gate plane into sparse red paths into wireframe expert cubes; this round replaced that illustration with the exact gate partition.

## Keep — what works
- "Sparsity is the absence of drawing" — the tagline `SIXTEEN EXPERTS . TWO FIRE . THE REST IS PAPER` and the decision to leave dead experts as bare paper.
- The right tent's nested triangles (apex u≈0.70, v≈0.50) — clean, exact, the one form with real presence; it crops against the right margin with intent.
- Tokens as the red ink, sitting at their own margin: load is the ink, not a symbol for it.
- The load chart's baseline with 16 slots, most empty — the collapse stated in one glance at 1 m.
- The exact half-plane geometry: cell walls are true straight lines, no sampling stagger.

## Weak — what doesn't
- [hierarchy] The hero (46 % expert) is not the dominant mass — the right tent is, and it is unlabelled; the E05 label floats over speckle at u≈0.40, v≈0.25.
- [concept] The 11 missing experts are invisible — absence only reads if the full partition is implied (a faint ghost of the unbiased 16-cell tiling, or slot marks on the terrain edge).
- [craft] Glyph gaps: `%`, `=`, `(`, `)` do not render — `46 OF TOKENS`, `K   2`, `Y   SUM GI  X   EI  X`.
- [craft] Tokens at ~0.5 mm dashes are below legibility at sheet scale — the "traffic" reads as a pink haze; a token dash collides with the `4` of `46`.
- [craft] Terrace rings on the left faces break into orphan `<`/`>` chevrons and dashes (u≈0.21–0.40, v≈0.20–0.33 and u≈0.50–0.62, v≈0.18–0.30) — it reads as fragmentary, not as depth.
- [space] The empty band v≈0.67–0.80 and the tiny chart stranded bottom-left are leftover, not composed; the chart is ~0.23 of sheet width against a 0.72 terrain.
- [grid] Footer formula on its own baseline right, captions left, swatch floating top-right — furniture checklist.
- [concept] The load bar chart is an axis plot — the scientific-figure habit.
- [depth] Isometric terraces give some depth but there is no weight or density fall-off; front and back facets are identical strokes.

## Next versions
1. **ghost-of-sixteen** (mechanism) — Draw the unbiased 16-cell partition first as a faint dotted tiling across the whole sheet, then the collapsed 5-cell terrain over it in solid pen: the 11 dead experts are dotted cells with nothing in them. Make the 46 % cell the largest, loudest tent (0.5 of sheet width, cropping one edge) and put its token count on its apex. Absence becomes visible because the promise is drawn.
2. **territory-map** (abstract) — Transpose to TESSELLATED, flat by declaration (De Stijl): the gate partition as a planar map of convex cells at full sheet size, each surviving cell filled with `tone_dots` whose density is its token share, dead cells left bare with a hairline border; the k=2 second-expert walls as a second, thinner partition inside the winner. No 3D, no terraces; the collapse reads as one giant cell eating the map.
3. **shatter** (faithful) — Return to the brief's gesture with the exact data: a single dense black token column falling from the top, hitting the gate's cell walls drawn as one angled plane, and fanning into only the red paths that actually fire, landing on 5 expert blocks sized by load with 11 empty outlines beside them.

**If only iterating:**
- Label the dominant cell on its apex (not in open space) and make it the largest tent; test: at 3 m the eye lands on the winner first.
- Add `%`, `=`, `(`, `)` glyphs or route through `_rich`-style geometry so every caption reads verbatim; test: `46% OF TOKENS`, `K = 2`, `Y = SUM G_I(X) E_I(X)`.
- Draw tokens as 1.0–1.2 mm dots at ≥1 mm spacing and drop the orphan terrace chevrons on the left faces; move the load chart up to share the terrain's baseline so the v≈0.67–0.80 gap closes.
