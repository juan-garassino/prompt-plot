# resonance-backprop r03 — gradient-as-phase (mechanism) · parent: r01 · 2026-09-28

**Lineage.** Bridget Riley, *Current* (1964), Op Art. The order taken from it: one line family
whose phase drift makes the surface. Here the drift is the gradient. The backward pass is the
forward crest family moved by a phase, either 0 or half a wavelength. It is not a second
diagram. (resonance r05 took Thomas Young, 1807. This plate avoids sharing it.)

## Render

```
.venv/bin/python scripts/render_candidate.py studio/resonance-backprop/rounds/r03/piece.py \
  --fn gradient_as_phase --seed 7 --paper a4 \
  --palette goldenrod,dodgerblue,forestgreen,crimson,black \
  --out gallery/studio/res_backprop/current/pp_res_backprop_gradient-as-phase_v9.png
```

- final: `gallery/studio/res_backprop/current/pp_res_backprop_gradient-as-phase_v9.png` + `.gcode`, seed 7
- **Seed-independent.** The piece draws no random numbers. Seeds 7 and 11 gave byte-identical
  G-code bodies on v7 (md5 `865c6608…`).
- The palette order is the stream order, light to dark. Colour meanings are the family's.
- `python studio/resonance-backprop/rounds/r03/piece.py` prints every statistic quoted below.

## Mandate responses

`studio/resonance-backprop/` has no LEDGER.md, so there are no numbered J/A/S rows. The work order
was FEEDBACK.md (Juan), the curator note and DESCRIPTION.md (the Weak list and the
gradient-as-phase paragraph). Every item from those three is listed here.

| id | mandate | status |
|---|---|---|
| J1 | DOTTED LINES: continuous dots, a tight constant pitch, no micro-dashes, both ends anchored, the same pitch across the family | FIXED. `_dotted` draws a round touch-dot (a 0.06 mm pen touch, never a dash) every 1.0 mm. It is end-anchored: n = round(len/1.0) intervals and n+1 dots, so both ends carry a dot. The only dotted lines left on the plate are the Q and K packet envelopes (88 dots). Every other connector of r01 was removed by the thesis, not replaced by dashes |
| C1 | keep the family grammar: Q crimson / K blue packets, the two-source field, V goldenrod, Z green | FIXED. All five colours carry their family meaning. The black two-source crest field is the hero |
| C2 | no pen cap; each pen one clean layer, order stated | FIXED. 5 pens, each a single layer that is never re-entered, streamed light to dark (see Plot budget) |
| C3 | strokes spatially ordered for batching | FIXED as far as the piece can. `_order` walks each pen greedily by nearest END and reverses strokes, so the post-processor's nearest-start pass gets strokes that are already oriented. Longest stroke is 315 mm (a full outer ring, 32 s). Every stroke can be a batch boundary |
| C4 | minutes per layer and total | FIXED (table below) |
| C5 | waste: 4053 pen cycles, 105 % travel | FIXED. **585 cycles (−86 %), travel 3.99 m = 35 % of draw** |
| C6 | name the LINEAGE | FIXED: Riley, *Current* |
| W1 | [concept] schematic: arrowed fans, stacked fractions, labelled stages (≤ 3) | FIXED by thesis. No arrows, fans, fractions or stage boxes. The backward pass lives inside the hero as a phase. What stays schematic-leaning: the three small output rows (Z, V₁, ∂L/∂Z) and the colophon at the foot |
| W2 | [craft] packet rows braid into knots (amplitude > row pitch) | FIXED. Every packet is a single row. The only stack (Z / V₁ / ∂L/∂Z) is at 14 mm pitch with amplitude ≤ 5 mm |
| W3 | [craft] the central comb floods to a black lozenge | FIXED. The comb was the two families running near-parallel on the axis. The ≥ 25° crossing rule leaves one family there, so no two lines run within 0.8 mm at a grazing angle |
| W4 | [hierarchy] the Z axis is the widest element, not the hero | FIXED. The hero is 172 × 163 mm, about 90 % of the sheet width. Next largest is a 40 mm packet |
| W5 | [tension] mirror-symmetric about u 0.50, centred title and Z | FIXED. The source axis tilts −24°. Q sits top-left and K bottom-right on that diagonal, the title is flush-left, the outputs sit bottom-left, and the upper right is left empty |
| W6 | [space] dead foot, a thicket of dotted arrows in the backward half | FIXED. The thicket is gone. The quiet zones are shaped by the diagonal: upper right (≈ 70 × 45 mm) and centre right below the field |
| W7 | v5: halo and scatter grey the band | FIXED. There is no halo and no scatter. Tone comes only from crest crossings |
| W8 | v8: dashed crest arcs break into noise | FIXED. There are no dashed crests. Every crest is continuous, and where the colour takes a crest over, the pen changes at a bisected point with no gap and no overlap |
| L1 | house law: never arrows | FIXED. There are none (r01 had 30+) |
| L2 | house law: text on its own layer with halos | FIXED (halos), ARGUED (layer). Every label and value window clears the field by 0.9–1.1 mm with the exact `engine.geometry` Rect/Union clip. Type stays on the pen of the tensor it names, because colour is the label's meaning. All the black type is in the black layer |
| B1 | brief: "offset by half a wavelength in a second colour … one sheet, two pens" | FIXED on the offset. ARGUED on "two pens": the curator note (binding) keeps every family colour. The exact maths also turned out to be sharper than the brief: the offset is exactly 0 **or** exactly ½λ, set by the sign of ∂L/∂s, not a continuous shift (see below) |

## What changed from parent

This is a new composition, not an edit of r01. r01 traced the reference: 5-row Q/K blocks, a
fraction, a softmax row, V rows, a Z row, and a backward band of arrowed fans below a mirror line.
All of that is replaced by **one field**:

1. **The hero.** Two coherent sources, 10 λ apart (λ = 3 mm), each radiating 24 full crest rings
   out to R = 72 mm. The source axis is tilted −24°. The field's left and right extremes land on
   the type grid (x = 14 and x = 186 in the design frame).
2. **The moiré, bounded by exact geometry.** The two families are drawn together only where they
   cross at ≥ 25°. The locus of a constant crossing angle is a circle through both sources
   (inscribed angle), so the moiré stops on two circular arcs, and beyond them only the nearer
   source's rings run. This replaces r01's point-dropping guard, which made the dashes and the
   black comb.
3. **The backward pass as phase.** Three token patches in the moiré (V₁, V₂, V₃), each holding
   its value packet in a cleared window. Around each one the gradient crests surface:
   - crimson = ∂L/∂Q, which is the **key's** wave, so it lies on K's rings;
   - blue = ∂L/∂K, the **query's** wave, on Q's rings;
   - where g = ∂L/∂s > 0 (V₂, V₃, the tokens the loss wants less of), the gradient crest is the
     forward crest, and the colour takes the crest over;
   - where g < 0 (V₁, the answer), the gradient crest lies exactly half a wavelength off the
     forward crest, so a second family interleaves at 1.5 mm and the patch doubles in density.
     V₁ becomes the plate's focal point for that reason, not by styling.
4. **The output, in the same carrier.** Z = AV (small, because the three phases partly cancel),
   V₁ (the target), and ∂L/∂Z. ∂L/∂Z is V₁ half a wavelength over (correlation −0.998), which
   echoes the field at the foot.
5. **Q and K packets** are single rows at the field's own wavelength, on the diagonal corners, with
   continuous-dot envelopes.

## Measurements / computations

All computed in `piece.py` (`Head`). Nothing is traced.

**Model.** q(x) = e^{i(k|x−Q|+φ_Q)}, k(x) = e^{i(k|x−K|+φ_K)} (rotary encoding, where position is
the path length). Then:
- s = β·Re(q k̄) = β cos ψ
- A = softmax over tokens
- V(x) = w_i(x)·u_i, where u_i is a Gaussian packet on the λ carrier with phase 0°, 120° or 240°
  and w_i is a flat-top weight exp(−(ρ/R_i)⁸)
- Z = Σ A V
- L = ½ Σ (Z − u₁)² dt

**Backward** (closed form):
- ∂L/∂Z = Z − u₁
- ∂L/∂A = ⟨Z − u₁, V⟩
- g = A(∂L/∂A − Σ A ∂L/∂A)
- **∂L/∂q = β g k** and **∂L/∂k = β g q**

A real factor β·g can only leave the phase alone (g > 0) or add π, which is half a wavelength
(g < 0).

| quantity | value |
|---|---|
| tokens (0.25 mm lattice in 3 patches, R = 17 / 14 / 11 mm) | 47,536 |
| β | 1.0 |
| attention mass α on V₁, V₂, V₃ | 0.277 / 0.188 / 0.117 |
| loss | 1.3652 |
| c_i = ⟨Z − u₁, u_i⟩ | −3.104 / +1.740 / +1.364 |
| Σ A ∂L/∂A | −0.3732 |
| max \|g\| | 1.232e-4 |
| sign of g by patch (+ / −) | V₁ 5,157 / 17,529 (the + tokens are the rim, where w·c₁ < Σ A ∂L/∂A) · V₂ 15,373 / 0 · V₃ 9,477 / 0 |
| **finite-difference check** (central, h = 1e-6, Re and Im of q and k at the 6 largest-\|g\| tokens) | worst relative error **9.4e-6** |
| one real SGD step on every token's q, k, η = 1e3 | loss 1.365 → **1.198** (printed on the sheet) |
| η = 1e2 / 1e4 | 1.349 / 0.059 |
| corr(∂L/∂Z, V₁) | −0.998 (∂L/∂Z is V₁ half a wave over) |
| gradient gate (a coloured crest is drawn where \|g\| ≥ 6 % of max) | Crests break along the dark fringes, where A (and so g) is small. This is the softmax made visible |
| min coloured-run length (shorter runs go back to black) | 2.5 mm |

**Craft measurements** (every non-type stroke sampled at 0.3 mm, joints excluded):
- Near-parallel crowding (< 0.8 mm and < 25° to another stroke): **0.89 %** of line length, all
  black, all within ~2 mm of the 25° moiré arcs where far rings end. For comparison, with the 20°
  rule of v8 it was 5.9 %.
- Interleave spacing (V₁) = λ/2 = **1.5 mm**. Parallel crest pitch everywhere else = 3.0 mm.
- Bounds: 0.0–200.0 × 0.0–285.0 (the 0,0 is the park move). Drawn ink lies inside 10–200 × 10–287.

## Plot budget

Model (Leo-safe profile): draw F600, pen-up travel F2000, `G4 P1.0` after both M3 and M5 (2 s per
cycle), 2 min per swap. Stream order = palette index = light to dark, so black crests and type
land last over the coloured crests they cross.

| # | pen | meaning | cycles | draw | travel | min |
|---|---|---|---|---|---|---|
| 0 | goldenrod | V₁ V₂ V₃ value packets, V₁ target row, labels | 14 | 0.25 m | 0.34 m | 1.1 |
| 1 | dodgerblue | K packet (+44 envelope dots), ∂L/∂K crests on Q's rings, label | 100 | 0.68 m | 0.71 m | 4.8 |
| 2 | forestgreen | Z = AV, ∂L/∂Z, labels | 15 | 0.16 m | 0.15 m | 0.8 |
| 3 | crimson | Q packet (+44 envelope dots), ∂L/∂Q crests on K's rings, label | 102 | 0.71 m | 0.70 m | 4.9 |
| 4 | black | forward crests (116 strokes, 8.68 m), title, colophon, crosses, sources | 354 | 9.55 m | 2.08 m | 28.8 |
| | **total** | | **585** | **11.35 m** | **3.99 m (35 %)** | **40.4 + 10 swap = 50.4 min** |

r01 v8 for comparison: 4,054 cycles, 11.39 m draw, 11.90 m travel. In this plate the pen cycles
are 39 % of the time, and in r01 they were ~70 %. Largest single hops are the layer-entry moves
from park (≤ 345 mm). Within a layer the hops are ≤ 191 mm. Suggested nib 0.3–0.4 mm: the
tightest pitch is 1.5 mm.

## Self-critique (rubric, honest)

| dimension | score | why |
|---|---|---|
| hierarchy | 7 | The field dominates at 3 m, V₁'s doubled patch is the clear second, and the packets come third. The coloured patches are only ~8 % of the field area, so the backward pass is secondary at 3 m by design |
| grid & alignment | 7 | Title, Q label, row labels and the field's left edge share x = 14. The field's right edge, K label end and colophon share x = 186. The rows' packets are not tied to anything |
| tension & asymmetry | 6 | The −24° diagonal with Q and K in opposite corners works. The field itself is still one large central mass |
| negative space | 6 | The upper-right quiet zone is real and shaped by the diagonal. The foot is busier: three rows plus a colophon |
| craft for pen | 8 | Continuous crests, a pen change at exact points, 0.89 % grazing, 1.5 mm minimum pitch, 585 cycles, 35 % travel, no dashes, no floods |
| concept legibility | 6 | "The gradient is the key's wave, in phase or half a wave over" is visible in V₁ vs V₂/V₃ once you know the colours. Without the subtitle, the recoloured V₂/V₃ read as "coloured patches" |
| depth | 4 (declared flat) | Op Art is flat by canon. The only depth cue is the moiré |

**Single worst thing:** the recoloured patches (V₂, V₃) do not show the g > 0 case as strongly as
V₁ shows g < 0. "The colour takes the crest over" is exact, but it only reads as a hue change,
with no change in structure. Second: the foot (three output rows and a two-line colophon) is the
last trace of a figure.

## Engine requests

1. **`kit.dotted(path, pitch)`**: the end-anchored touch-dot run used here (`_dotted`), so the
   family's pitch lives in one place.
2. **Reversal-aware ordering in `postprocess.reorder_by_color`** (repeating resonance r05's
   request). The piece pre-orients its strokes to work around it.
3. **A 2D `halo_clip(strokes, boxes, pad)`** in `engine/kit` (also repeating r05's request).
