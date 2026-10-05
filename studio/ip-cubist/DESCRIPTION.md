# ATTENTION AS RESONANCE (cubist oracle import) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/ip_cubist` |
| current render | `gallery/studio/ip_cubist/current/ip_cubist_oracle.png` (paired gcode `ip_cubist_oracle.gcode`: 67.2 m draw, 18.9 m travel, 47,632 commands, 7,118 pen cycles, 8 colour layers, bbox x 14.4–284.3 × y 41.4–378.6 mm) |
| source | **Nothing in PromptPlot generates it.** The plate is the ChatGPT "interpretive plotter" oracle SVG `gallery/references/oracles/interpretive_plotter/results/verification/cubist/cubist_attention_layered.svg` (7,118 paths, 8 layers, mm viewBox) run through the SVG importer (`promptplot/importers/svg_import.py`, mm-native `--no-fit`, grouped by Inkscape layer). The upstream generator is `gallery/references/oracles/interpretive_plotter/scenes/cubist/scene_cubist.py` (an image-specific authored scene on shapely; read-only, never import it). Our own native rebuild is briefed but **not built**: `studio/reconstructions/cubist-repro.md`, reference `studio/reconstructions/cubist-repro/ref/reference.png`. |
| paper · pens | A3 portrait (297 × 420), white. The oracle's pen plan (`.../cubist/pen_plan.json`) has 4 inks × 2 nibs: 0 black 0.10 (hatching, 5,414 paths, 50.3 m, ~75 % of all ink) · 1 red 0.10 · 2 yellow 0.10 · 3 blue 0.10 · 4 black 0.50 (silhouettes, big lettering) · 5 red 0.50 · 6 yellow 0.50 · 7 blue 0.50. **The preview does not show these inks.** It paints layers in matplotlib's default cycle, so yellow ink appears blue, blue ink appears green, black-0.50 appears purple, red-0.50 orange, yellow-0.50 brown and blue-0.50 pink. |
| status | unreviewed (no feedback) · 1 render + 1 gcode on disk |

## In one line
A transformer block drawn as a **Picasso-cubist stage of hatched planes (tessellated facets)**: queen = Q and king = K rake a chessboard (the score matrix) with coloured rays, the board drains through a SOFTMAX bowl into value ribbons, a cellist is V, a facet-room table is the FFN, and a bridge arc is the residual. The mapping is by label and allegory, not by data.

## What is on the sheet
Framed artwork box ≈ u 0.05–0.96, v 0.10–0.90 (a black-0.50 rectangle frame). Below it is a ≈ 40 mm empty band, above it ≈ 40 mm. Reading order:

- **Chessboard (focal).** A perspective board at u 0.27–0.72, v 0.30–0.44, with rank/file lines and dark squares hatched diagonally (in preview the hatch reads solid black).
  - About 20 small pieces stand on it: pawns, rooks, crowned queens/kings, a knight. Each is outlined in black-0.50 with one half hatched in a colour.
  - A hatched table-slab edge sits under the board (v 0.44–0.46).
- **Q, the queen (upper-left figure, u 0.22–0.45, v 0.15–0.44).** A faceted crowned profile facing right, with a crown of three spiked facets (yellow + red hatch).
  - Her cloak planes are hatched red-0.10 (large solid-reading red wedges at u 0.22–0.33, v 0.24–0.44) and black.
  - The label `Q` in red-0.50 sits at u ≈ 0.28, v 0.20.
  - About 12 red-0.10 **rays** leave her mouth and fan down onto the left half of the board.
- **K, the king (upper-right figure, u 0.55–0.72, v 0.13–0.46).** A faceted crowned profile facing left.
  - A blue-hatched crown and one blue-hatched square plane at the shoulder (u 0.63–0.66, v 0.25–0.30).
  - The label `K` in blue-0.50 at u ≈ 0.66, v 0.22.
  - About 10 blue-0.10 rays fan to the right half of the board.
  - His cloak is a large black-hatched mass (u 0.60–0.75, v 0.25–0.46).
- **Formula under the rays.** `Q . K` with a small `T`, over `√d` with a small `K`, in black-0.50 at u 0.45–0.53, v 0.24–0.28.
- **SOFTMAX bowl.** A funnel/bowl shape under the board centre (u 0.40–0.55, v 0.46–0.50), lettered `SOFTMAX`.
- **Value ribbons.** Seven parallel yellow-0.50 lines leave the bowl downward (v 0.50–0.56).
  - They split into a band that sweeps left to the cellist's scroll (u 0.22–0.45, v 0.51–0.53).
  - A second bundle (yellow + blue-0.50) drops to the `Z = AV` panel.
- **V, the cellist (left, u 0.05–0.28, v 0.50–0.78).** A faceted woman with a dark hatched dress and a yellow-hatched face plane and cello, the scroll at the top.
  - The label `V` in yellow-0.50 at u 0.07, v 0.50.
  - A hatched chair or arch at u 0.08, v 0.72–0.78.
- **Z = AV panel.** A tilted card at u 0.30–0.45, v 0.63–0.70, lettered `Z = AV`. Three yellow-0.10 connector curves run from it right into the FFN table.
- **FFN table (right-centre, u 0.57–0.92, v 0.47–0.74).** A box in a perspective frame (roof hat above, hatched plinth below). Its 3 × 4 grid has the column heads `W1`, `σ()`, `W2`.
  - Rows: an input piece (queen / knight / pawn) → a W1 fan-polygon of blue/yellow wedges → a σ() octagonal rosette → an output pawn.
  - Black-0.10 arrows between cells. Three yellow-0.50 lines leave the right side and loop down to the `Z' = FFN(Z)` card.
- **Z' = FFN(Z) card.** u 0.70–0.84, v 0.74–0.77.
- **Residual bridge (bottom band, u 0.10–0.75, v 0.72–0.95).** A long hatched parapet with six round-topped arch-niches (black half-hatched) receding diagonally.
  - On top stand the transformed tokens: a pawn, two crowned pieces, a knight, pawns, all half-hatched yellow.
  - A long yellow-0.50 + black curved arrow (the residual) runs from lower-left to u 0.52, v 0.86.
  - The card `H = Z' + X` / `RESIDUAL CONNECTION` sits at u 0.12–0.27, v 0.85–0.89.
- **Top-left title card** (u 0.10–0.28, v 0.13–0.20): `ATTENTION` / `AS` / `RESONANCE` in black-0.50 open stroke caps.
- **Input card.** `INPUT` / `TOKENS` / `X` + small `TOKENS` (u 0.05–0.13, v 0.24–0.29).
- **Input heads.** Three small faceted heads with long hair (u 0.05–0.18, v 0.33–0.42), hatched black.
- **Background.**
  - Hatched vertical slab planes everywhere: top-left, the centre tower with an arch, a moon/sphere at u 0.49, v 0.15.
  - A dove on a plinth, top-right (u 0.68–0.80, v 0.12–0.17; hidden under the legend in this render).
  - Tall horseshoe arches with hatched walls and a stair on the right (u 0.75–0.93, v 0.20–0.55).
  - Loose black-0.10 construction lines at the corners.
- **Registration crosses** at the frame corners (bottom-left, bottom-right).

## The science it encodes
Allegory, not computation. From the reference and the cubist-repro brief:
- The three named sources Q, K, V are **figures**.
- The score matrix is the **chessboard**, and Q·Kᵀ is literally rays from mouths to pieces.
- Softmax is a bowl, A·V is ribbons pouring from the bowl into V's instrument and into `Z = AV`, the FFN is a W1 → σ → W2 table applied per token row, and the residual `H = Z' + X` is the bridge arc.

**Nothing is computed.** The rays land on arbitrary pieces, the FFN wedges are decoration, and there are no weights.

**How faithful it is to the reference** (`studio/reconstructions/cubist-repro/ref/reference.png`):
- Kept: every major object and label is present.
- Dropped:
  - The whole right-hand word column (`QUERIES KEYS VALUES ATTENTION FEEDFORWARD REPRESENTATION`) and the lower-right `SAME INFORMATION DIFFERENT FOCUS DEEPER MEANING` column.
  - The `FEEDFORWARD (TRANSFORMATION)` header.
  - `X ∈ R^{n×d}`, replaced by `X TOKENS`.
  - All pigment texture.
- The `Q · Kᵀ` dot is a period.
- The oracle's own preview (`gallery/references/oracles/cubist_attention_preview.png`, drawn at true nib widths) reads light grey with bare lit planes. **This render reads almost black-and-white poster**, because the preview draws every 0.10 mm hatch at the same heavy width.

## How it got here
One render only: an import of the oracle's delivered SVG, no iterations. Upstream history lives in `gallery/references/oracles/interpretive_plotter/CHANGELOG.md` and `results/history/`. The PromptPlot-native rebuild (`cubist-repro`) has not started. No Juan feedback recorded.

## Keep — what works
- **The composition's two-headed diagonal.** Queen upper-left and king upper-right, both raking one board, then everything cascading down-left (cellist) and down-right (FFN) to the bridge. It is a real hierarchy with the board as the focus.
- **Plane discipline.** One hatch direction per facet, lit facets left bare (visible in the oracle preview), cross-hatch only on selected shadows. This is exactly the MATERIAL GRAMMAR cubist row, and the reason it is the oracle.
- **Semantic ink.**
  - Red belongs to Q (her cloak, her rays, her label).
  - Blue belongs to K (the shoulder plane, the rays, the label).
  - Yellow belongs to V and everything V carries (cello, ribbons, transformed tokens, residual arc).
  - Colour is scarce and meaningful.
- **Chessboard rank/file construction** with only dark squares hatched, and pieces as a shared glyph family: reads instantly.
- **FFN table as a 3 × 4 room**, with W1 fans turning into σ rosettes. It is the most diagrammatic zone, but it reads.
- **Plot budget.** 7,118 paths and 67 m of ink over 8 layers is heavy but finite, and the black-0.10 layer carries 75 % of it.

## Weak — what doesn't
- [craft] The preview is not the drawing. Hatches drawn at display width flood the 0.10 mm planes solid black, so AUTHORING acceptance question 5 (labels readable at true width) and question 4 (are the blacks intended?) cannot be answered from this png. The layer colours lie too (yellow ink shows blue, blue ink shows green). Judge only after a `pen_widths=` + real-hex re-render.
- [concept] NO SCHEMATICS / illustration. This is figuration with labels: named objects (queen, king, cellist, chess, bridge) carry the mechanism by allegory. The FFN table is a labelled box-and-arrow grid, which is a schematic by the rubric's definition. Nothing on the sheet is computed.
- [concept] The rays end on arbitrary squares and pieces. The one place attention could carry data (which key each query attends to, and how strongly) is decoration.
- [space] At full-weight preview the sheet is uniformly busy. Every background slab is hatched, so there is no generous quiet zone and the board fights the background for attention. The oracle's grey preview has more air, but even there the corners are filled for the sake of being filled.
- [grid] Labels float on tilted cards (`Z = AV`, `Z' = FFN(Z)`, `H = Z' + X`), each at its own angle and size. The title card and input card do not share an edge with the frame or with each other.
- [craft] The dropped reference labels (the word columns, `∈ R^{n×d}`, the `FEEDFORWARD` header) leave the right edge and the input card less informative than the reference. The `Q . K` has a period instead of a dot operator.
- [depth] Depth is by overlap and perspective only (board, arches, bridge recession). There is no line-weight falloff with distance: background slabs are as heavy as foreground figures.
- [concept] It is not ours. The engine this studio built (`scene/`, `CUBIST_RULES`, `hatch_polygon`) never drew a line of it, so every improvement to it is an improvement to someone else's SVG.

## Next versions
1. **native scene** (faithful) — Build `cubist-repro` for real as an authored `Scene` compiled by `compile_scene` with the `cubist_plate` preset and `CUBIST_RULES`. Follow the brief's naming (`queen veil plane`, `board rank 1`, `ffn expanded facet 2-1`, ...) so ink and width come from rules. Judge against the oracle for plane hierarchy, bare lit planes and budget, and render at true nib width. This is the only thesis that turns an imported oracle into a PromptPlot plate, and it is the reason the slug exists.
2. **the board is the matrix** (mechanism) — Keep the cubist stage but make the attention real:
   - Dark-square hatch density on the chessboard = an actual attention map (`attn_npz` from `scripts/extract_gpt2_attention.py`, one head, 8 × 8 tokens).
   - Red rays from Q's mouth go only to her row's top-k keys, with ray count ∝ weight.
   - Blue rays from K run along the column.
   - The FFN wedge angles come from a real W1 row.

   The allegory stays, but the board stops lying.
3. **planes only** (abstract) — Delete the figures. Keep only the cubist ORDER: tessellated facets whose hatch *direction* is a head's query direction and whose *spacing* is attention weight. The softmax becomes the one bare (lit) plane where all hatching stops. It is the collection's rule ("if a viewer can name an object that is not the mechanism, cut it") applied to the most figurative plate in the studio.

**If only iterating:**
- Re-render the gcode with `GCodeVisualizer.preview(pen_widths=...)` from `pen_plan.json` and the layers' real hex inks, and move the legend off the artwork. The next critique must see 0.10 hatches as grey and yellow as yellow.
- Restore the dropped reference labels as label marks: `X ∈ R^{n×d}`, `FEEDFORWARD (TRANSFORMATION)` over the table, and the two right-edge word columns on a shared left edge at u ≈ 0.86.
- Leave at least two background slabs (top-left corner and lower-right corner) as bare paper so the board and the two heads are the only fully hatched masses above v 0.5.
