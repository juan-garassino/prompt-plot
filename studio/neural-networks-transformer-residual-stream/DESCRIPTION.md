# Residual river (untitled on the sheet) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/neural-networks/transformer/residual-stream` |
| current render | `gallery/neural-networks/transformer/residual-stream/candidates/pp_residual_river_glitch.png` |
| source | `promptplot/generative/generators.py::residual_river` (+ the `--anaglyph --glitch` effect from `promptplot/generative/engine/looks.py` for the current render; `wobble>0` for the wobble trial) |
| paper · pens | a4 landscape, white preview · current: 0 cyan · 1 red · 2 gold · 3 black — the four anaglyph/glitch copies of every line (default anaglyph palette) · base trial: 0 navy · 1 crimson · 2 goldenrod by channel index mod 3; last pen also carries the skip arcs |
| status | unreviewed (candidates tier only, no feedback) · 3 renders on disk |

## In one line
The transformer residual stream drawn as **laminar flow** — 22 parallel channel lines cross
the sheet left to right, braiding at four "attention stations" (seeded neighbour swaps)
and bulging at four "FFN lenses" (the band expands 2.4× and contracts); the current
version runs every line through a 4-pen anaglyph glitch.

## What is on the sheet

### current — `pp_residual_river_glitch.png`
- **Dominant mass:** a horizontal river spanning the full drawable width (u 0.06–0.94),
  its resting band at v 0.30–0.60, centred v≈0.47.
- **Four spikes, evenly spaced** at u 0.21, 0.44, 0.66, 0.89: at each the upper half of
  the band shoots up into a narrow tower (peak v≈0.14) and the lower half plunges into a
  matching trough (bottom v≈0.83). Each tower/trough is ≈ 0.07 W wide, so the "lens" reads
  as a sharp vertical spike, not a lens. The four spikes are nearly identical.
- **Every line is drawn four times** (cyan, red, gold, black) with ≈ 1–1.5 mm lateral
  offset, giving each channel a chromatic fringe; with 22 channels this is ≈ 88 lines.
- **Middle band (v 0.40–0.55)** is a tangle: channels wobble (fbm), cross, and carry small
  Z-shaped glitch steps — horizontal jumps of a few mm where a slice was displaced.
- **The troughs** (v 0.70–0.83) end in faceted, polygonal knots: the four-pen copies fold
  into hexagon-like kinks at the bottom of every trough (glitch displacement on steep
  segments), the densest and muddiest zone on the sheet.
- **Four shallow U-arcs** along the bottom (v 0.84–0.87), each ≈ 0.18 W wide, one under
  each block, also four-fold — the "skip connections".
- **No type, no furniture.** Quiet zones: the strips above the towers between spikes
  (v 0.10–0.30) and the band between the troughs and the skip arcs.

### trial — `pp_residual_river.png` (base, 3 pens)
- The same geometry without effects: 22 clean parallel horizontals at v 0.35–0.65,
  S-curve crossings at the stations (e.g. u 0.31–0.38, 0.54–0.61, 0.77–0.83), then four
  smooth nested Gaussian spikes (goldenrod outermost reaching v 0.15 / 0.85); crimson and
  navy nest inside. Channels closest to the centre barely move. Four single goldenrod U-arcs
  at the bottom. Reads as clean but schematic — like an oscilloscope trace.

### trial — `pp_residual_river_wobble.png`
- Base + fbm wobble: lines meander between stations; the spikes grow until the outermost
  channels **clip flat against the top and bottom margins** (flat-topped goldenrod and
  crimson at v 0.07 and v 0.93) — the `_clamp` shows as plateaus.

## The science it encodes
`residual_river` docstring: "parallel channel lines flow across the page; each block is an
attention station (channels weave and swap) followed by an FFN lens (the band expands ~4x
and contracts, phase-continuous). Skip-connection arcs bridge every station. Pens follow
the original channel index, so the weaving mixes the colors downstream." Nothing is
computed from a model: swaps are seeded random neighbour transpositions (7 per block),
the lens is a sin² envelope (2.4×, not ~4× as the docstring says), and the skip arcs are
fixed sagging curves. Two claims the render does not bear out: (1) "skip-connection arcs
bridge every station" — they are drawn *below* the band (`top = cy − h0·expand − 3` is
below centre in plotter y-up coordinates) and sag away from it, so they bridge nothing;
(2) "the weaving mixes the colors downstream" — in the glitch version colour is the
anaglyph copy, not the channel, so the mixing is lost entirely. The real point of a
residual stream — that every block only *adds* to a persistent stream — is not shown;
the spikes look like transforms that replace it.

## How it got here
Base → wobble (organic meander, gained life, introduced margin clipping) → glitch (4-pen
anaglyph + slice glitch on top of wobble: gained chromatic vibration and 37 m of ink,
lost the clean weave, the channel-colour logic and legibility of the stations). No
feedback in `studio/feedback.jsonl`.

## Keep — what works
- The river as the only form: a horizontal laminar band crossing the whole sheet is a
  genuine abstract order for "a stream every layer writes into".
- The four-beat rhythm of blocks (u 0.21, 0.44, 0.66, 0.89) — a clear, countable
  structure: four layers.
- The station crossings in the base trial: smooth S-curves where two channels trade lanes
  are the most elegant marks in the family.
- The chromatic fringe of the glitch version gives the flat band a vibrating, printed feel
  — worth keeping as texture if it carries data.

## Weak — what doesn't
- [concept] The FFN is drawn as a spike, not a lens: the envelope multiplies the offset,
  so centre channels stay flat and outer ones shoot out — it reads as four identical
  oscilloscope pulses. Nothing says "added to a persistent stream".
- [concept] Skip arcs sag below the band and are disconnected from it; they read as four
  smiles along the bottom. The docstring's "bridge every station" is false on the sheet.
- [concept] Glitch colour is decoration: four copies of every line carry no data, and they
  erase the "pens follow channel index" mapping the piece was built on.
- [hierarchy] Four identical spikes at equal spacing; no block is dominant, nothing grows
  or changes across depth.
- [tension] Perfectly periodic, left-to-right symmetric, band centred on the sheet.
- [craft] Trough knots (v 0.70–0.83) are ink-on-ink mud: 4 pens × ~10 channels folding
  into faceted polygons within a few mm; 37 m draw + 25 m travel, 34.5 k commands.
- [craft] Wobble trial clips peaks flat against the margins.
- [space] Quiet zones are just the gaps between spikes — leftover, repeated four times.
- [depth] Flat and undeclared; the anaglyph offset suggests depth without using it.

## Next versions
1. **the stream accrues** (mechanism) — make the residual idea visible: the stream starts
   as a few thin channels at the left and every block *adds* channels/passes (the
   write-back), so the band thickens left to right; attention stations are braids that
   draw from far lanes, FFN writes are short additive strokes that merge into the band,
   never replacing it. The stream's growth becomes the dominant diagonal of the plate.
2. **real routing** (faithful) — keep the river, but drive the weave from a real model:
   lane swaps from the top attention movements of GPT-2 per layer, lens height from the
   measured residual-norm growth per block (it grows roughly geometrically), and channel
   colour = channel identity. The four blocks then differ, giving hierarchy and a truthful
   caption.
3. **skip as the main road** (lens) — invert the emphasis: the skip path is the loud
   continuous black river drawn straight across the sheet; each block is a small crimson
   side-loop that leaves and rejoins it (an oxbow), cropped at the top frame. The twist: in
   a residual network the detour is optional and the highway is identity.

**If only iterating:**
1. Draw the skip arcs above the band (flip the sign), anchored exactly on the stream at
   each station's start and the lens's end, so they visibly bridge a block.
2. Replace the glitch 4-copy fringe with colour by channel index (3 pens), and apply the
   slice glitch to at most one block as a single accent.
3. Make the lens a lens: widen each lens window from ≈ 0.07 W to ≥ 0.15 W so the band
   swells instead of spiking, and give each block a different expansion (e.g. 1.4×, 1.8×,
   2.4×, 3.0×) so depth reads left to right.
