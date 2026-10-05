# resonance-backprop — r01

EXACT-RECREATION round for `studio/resonance-backprop/ref/reference.png`
(1122 × 1402 px). Reproduction, not design.

**Entry point:** `attention_as_resonance(rng, bounds, colors=5)` in `piece.py`.

**Render**

```
.venv/bin/python scripts/render_candidate.py studio/resonance-backprop/rounds/r01/piece.py \
  --fn attention_as_resonance --seed 7 --colors 5 --paper a4 --orientation portrait \
  --palette crimson,dodgerblue,goldenrod,forestgreen,black \
  --out gallery/studio/res_backprop/trials/pp_res_backprop_v1.png
```

`gallery/studio/res_backprop/trials/pp_res_backprop_v1.png` (+ `.gcode`).
**55,178 commands · 34,910 draw moves · 4,054 pen cycles · draw 11,389 mm ·
travel 11,904 mm · 0 bounds violations.** Siblings landed 21k–59k.

Pens: 0 red (Q, ∂L/∂Q) · 1 blue (K, ∂L/∂K) · 2 ochre (V, ∂L/∂V) ·
3 green (Z, ∂L/∂Z) · 4 black (frame, type, interference, softmax, ∂L/∂A).

---

## How the reference was measured

Not eyeballed. Colour-segmented row scans found every axis row
(Q/K 171·215·260·305·348, V 669·702·734·766, Z 819, ∂L/∂V 1025·1060,
∂L/∂Z 1060, ∂L/∂Q and ∂L/∂K 1210·1243·1281, ∂L/∂A baseline 1268); ASCII pixel
maps settled the node columns (Q home 127, mid 301; V 97/240; ∂L/∂Q 122/295);
ink-bbox probes gave the type metrics (title 254–882 × 27–47, subtitle
280–843 × 82–96); a long-vertical-run scan on column x = 37.5 gave the two
rails exactly (forward: T-bar 165, label 318–483, arrow tip 581; backward:
arrow tip 910, label 1013–1187, T-bar 1289); a black-column histogram gave the
nine droplines (383·433·475·512·560·608·643·689·735) and, with them, the two
interference sources at 384/736 → **d = 352 px, centre (560, 448)**.

Content box = the four corner crosses, `(17, 17, 1105, 1385)`, uniform
width-fit into the drawable area and vertically centred.

## Reused wholesale (not reinvented)

* **`interference`** — the approved Huygens construction from
  `studio/resonance/rounds/r01/piece.py`, via its port in
  `studio/resonance-clean`: crest ridges `r_s = m·L`, separation a whole number
  of wavelengths so crest *m* of one family meets crest *n−m* of the other ON
  the axis; `_Guard` ported verbatim (drop a point only when a neighbour is
  within 0.82 mm **and** within 25° of parallel, so crossings survive). The
  level-set of `cos(k r₁)/√r₁ + cos(k r₂)/√r₂` stays rejected.
* **`packet_curves` / `draw_packet` / `_trim`** — the wave-packet helper
  (carrier × gaussian envelope, envelope drawn as a dotted trace that lifts off
  the axis).
* `_spline`, `rdotted`, `rdisc`, `rcircle`, `rdot_run`, `radical`,
  `tracked_type`, `left_type`, the `P/L/PP` reference-px→mm frame.

## Built new for this plate

* the whole layout: 5-row Q/K at the new pitch, **V as FOUR ochre rows at
  mid-LEFT**, Z at 819 with `Z = AV` set BELOW it, the softmax row at 687;
* subtitle line + the four corner registration crosses and their dotted ticks;
* **the two rails** — `rail_type` sets the label rotated +90° (reads
  bottom-to-top, glyph tops pointing left), which is how the reference sets
  both "forward pass" and "backward pass";
* **the entire backward band**: `∂L/∂Z`, `∂L/∂A` (5-peak row), `∂L/∂Q`,
  `∂L/∂K`, `∂L/∂V`, the stacked fractions, and `arrowhead()` — every connector
  down there is dashed and carries a head. This is the one place on these
  plates where an arrowhead is correct: it marks gradient direction, not
  projection.

## The one construction parameter that had to change

The sibling used `d = 35·L`. Here `d` grew to 352 px, so 35 would have given a
1.66 mm fringe pitch — the v1 render came out as two plain bullseyes with no
comb. The invariant that matters is that **d is a whole number of
wavelengths**, so the plate uses **`d = 59·L`** (L = 5.97 ref px ≈ 1.04 mm),
which restores the sibling's physical pitch. Solid crests now split three ways
to match this reference's tone: `m = 1..9` solid (the bullseyes), `m = 10..50`
solid but clipped to a central lens 100 × 40 (the comb), `m = 10..63 step 3`
dashed inside a 300 × 98 oval (the tonal field).

## Three things furthest from the reference

1. **Interference fringe pitch and weight.** The reference's crests sit
   4.2–6 ref px apart (0.70–1.00 mm on A4) and are drawn as *grey hairlines*,
   so the figure reads airy. The plot floor is 0.8 mm, so ours sit at 1.04 mm:
   the bullseyes carry 9 rings where the reference carries ~13, and every line
   is full-black. Tone is faked with dash length (solid → 1.45/0.75 dashes →
   0.55/1.15 dots), which is the closest a pen gets, but the field is still
   heavier and coarser than the original. This is the largest single gap.
2. **Serif / italic type — known permanent gap, not chased.** The reference
   sets `Q·Kᵀ/√d_k`, `A = softmax(…)`, `Z = AV` and all five `∂L/∂·` in an
   italic serif; ours are upright single-stroke. Consequence: the fractions
   read as diagrams rather than as maths, and the `Q K V Z` display caps lose
   the reference's stressed serif weight (we fake it with `weight=0.34 mm`).
3. **The convergence fans are re-drawn, not traced.** Curve *counts*, entry
   rows, sweep direction and the red/blue end-dot chains match the reference;
   individual control points are mine. Same caveat for the per-row packet
   parameters: envelope size and position are measured, carrier phases and
   periods are invented so each row is distinct.

## Font: two glyphs missing centrally

`_stroke_text` / `giant_type` now carry lowercase and `proportional=True`, so
`softmax`, `forward pass`, `backward pass` and `d_k` all set correctly and no
local glyph table was built. Two maths signs are **not** in
`promptplot.generative.generators._GLYPHS` and are drawn here as bespoke
geometry on the font's own 4×6 grid (the same way the sibling draws its
radical):

* **`∂`** (U+2202, partial derivative) — `_PARTIAL` in `piece.py`, addressed as
  the sentinel character `"@"` by `math_text`/`frac`. Used 10× on this plate.
* **`√`** (U+221A, radical) — `radical()`, drawn as a polyline because it needs
  a variable-length overbar.

Both should be added to the central font; `∂` in particular is a plain glyph
and a fixed-width overbar-less `√` would cover most uses.

## Open / next round

* The forward Q→interference fan could be traced properly off the raster; right
  now it is a silhouette match.
* `A = softmax(QKᵀ/√d_k)` token positions are traced but the upright font is
  wider than the reference's italic, so the run is ~15 px long — it fits, but
  the internal spacing is looser than the original.
* Pen cycles (4,054) are high because almost every connector is dashed. If this
  goes to Leo, stream per colour layer and expect a long job.
