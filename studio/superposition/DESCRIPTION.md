# SUPERPOSITION (Q · Kᵀ → softmax → Z = AV) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/superposition` |
| current render | `gallery/studio/superposition/current/pp_superposition_v16.png` |
| reference | `studio/superposition/ref/reference.png` |
| source | `studio/superposition/rounds/r01/piece.py::superposition` |
| paper · pens | a4 portrait, cream · 0 crimson = Q bump family · 1 dodgerblue = K bump family · 2 goldenrod = V bump family + connector fans · 3 forestgreen = Z bell · 4 black = Q·Kᵀ contour map, softmax row, axis, labels |
| status | unreviewed (no feedback) · 16 renders on disk |

## In one line
Attention drawn as **superposed Gaussian bumps flowing down a central axis** — Q and K families (mirror images) pour dotted connector fans into a contoured two-eyed similarity field, which drops to a five-spike softmax row, fans out to a wide V family and converges into a nested green bell (Z = AV); an exact, measured recreation of an AI-made reference, with no redesign.

## What is on the sheet
Reading order: the black contour map at the centre, the red and blue families above it, then down the axis through softmax, V and Z. There is no title.

- **Q family** (crimson), u 0.08–0.45, baseline v 0.24: ~21 overlapping Gaussian bump curves (some solid, some dotted) on one baseline, the tallest peaking at v 0.11 at u 0.26; above each bump's apex a dotted dropline rising to a terminal dot, apex markers as filled disc / open ring / bullseye, a row of dots on the baseline, dotted baseline tails beyond both ends. Label `Q` (hairline, crimson) at u 0.15, v 0.12.
- **K family** (dodgerblue), exact mirror at u 0.55–0.92, baseline v 0.24, tallest peak at u 0.74, v 0.11; `K` at u 0.85, v 0.12.
- **Connector fans**: from each Q and K baseline dot, dotted curves (in the family's colour) leave vertically downward, run flat, and arrive at the top rim of the map — two funnels converging on u 0.40–0.62, v 0.30–0.35.
- **Axis**: a black dotted vertical at u 0.50 from v 0.25 to v 0.95; a dotted horizontal at the map's height (v 0.39) from u 0.24 to u 0.76 with open rings at u 0.27, 0.50, 0.73.
- **Label** `Q·Kᵀ` (black, ~4 mm) at u 0.50, v 0.29.
- **The Q·Kᵀ map** (black, the dominant dark mass, ≈0.36 of width): a horizontal lozenge u 0.32–0.68, v 0.33–0.44. Three dotted outer contours hugging the boundary, then ~12 solid nested contours closing on two eyes — a tighter whorl at u 0.57, v 0.36 and one at u 0.44, v 0.40; a saddle between them. The interior is sprinkled with a stipple of small dots (the "wash") and larger scattered dots; a spray of loose black dots trails below the lozenge (v 0.43–0.49). A few crimson and blue dots sit on the upper rim where the fans land.
- **Softmax row** (black), baseline v 0.61, u 0.28–0.72: five narrow spikes of heights ascending to the central one (peak v 0.50 at u 0.50) and descending, each with a dotted dropline and marker; faint wide dotted bells underneath; label `softmax` (lower-case, u 0.60, v 0.52). Dotted verticals from the map down to the spikes at u 0.44, 0.50, 0.57.
- **V fan-out**: ochre dotted curves leave the softmax baseline dots and spread to the V family's dots — a diverging fan u 0.10–0.90, v 0.62–0.71.
- **V family** (goldenrod), the widest element, baseline v 0.77, u 0.06–0.93 (dotted tails to the drawable edges): seven groups of overlapping bumps with droplines and markers, symmetric about the axis. `V` at u 0.09, v 0.68.
- **V→Z fan**: ochre dotted curves from under the V baseline converge onto the Z bell (v 0.78–0.84).
- **Z bell** (forestgreen), baseline v 0.91, u 0.25–0.75: ~10 nested bells of increasing height sharing one centre at u 0.50, crest at v 0.83, green markers on the baseline and crest, dotted tails. `Z = AV` (green, spaced) at u 0.65–0.80, v 0.86.
- Quiet zones: the top strip v 0.03–0.08; the corners beside the map (u 0.05–0.25 and 0.75–0.95, v 0.30–0.60); below Z (v 0.93–0.97).

## The science it encodes
From `r01/NOTES.md`: a reproduction, "no redesign" — every position is measured off hue-classified ink masks of the 1122×1402 reference and mapped to the sheet. The Q/K/V/Z curves are Gaussian bumps placed at measured reference centres; they are not computed from vectors, and softmax/Z are not computed from Q/K/V. The one real computation is the map: a 2-D scalar field (11 broad Gaussians + 3 conical cusps + seeded fbm) contoured by marching squares, with conical eyes so rings stay evenly pitched (the general lesson recorded in NOTES and `DESIGN_RUBRIC.md` § 5). NOTES says the field has THREE vortex centres (a small σ=21 cluster between the two eyes); on the render only two eyes are distinguishable. The stipple "wash" is gated on the field's core.

## How it got here
Sixteen renders, one round, all on the reference's layout. v4: map as a denser mess of contours with scattered dots, `SOFTMAX` in caps, Z label left-of-centre; v7–v10: map filled out, black debris dots spread widely around it, V and Z families thickened; v13: debris trimmed, map smoothed, labels resized (NOTES: labels were ~30 % oversized until v14); v16: lower-case `softmax`, cusp eyes, measured label sizes. Against the reference: positions and families match closely; lost are the reference's graded line weight (ghost curves), serif italic type, the grey tonal wash (here a speckle), and the reference's tighter whorl eyes (limited by the 0.8 mm floor, per NOTES). Juan's feedback: none recorded.

## Keep — what works
- The vertical spine: five stations on one axis at u 0.50 with a clean alternation of mass (map) and line (spikes, bumps) — a legible top-to-bottom rhythm.
- The two-eyed contour map (u 0.32–0.68, v 0.33–0.44) with conical eyes and evenly pitched rings — the one real field on the sheet and its best-crafted element.
- The dotted connector fans that leave vertically, run flat and arrive vertically — elegant, plottable, and they visibly carry Q/K into the map and V into Z.
- Colour as provenance (red/blue/ochre/green) with black for the operations.
- The V family as the widest band (u 0.06–0.93) against the narrow Z bell — a real contraction read.

## Weak — what doesn't
- [concept] A schematic of the attention equation: labelled stations stacked on an axis, inputs to output — the slide figure § 6 fails; and a traced reproduction of someone else's figure, not an authored order.
- [concept] The curves carry no data: Q/K/V bumps are placed at reference pixels, softmax spikes and the Z bell are not computed from them; the map is a hand-built field. Rigorous-looking, numerically empty.
- [tension] Perfectly symmetric about u 0.50 (Q mirrors K, V symmetric, Z centred) — centred-symmetric, ≤4 by the rubric.
- [hierarchy] The map is only ≈0.36 of width; the V band is wider and the Q/K families brighter — at 3 m nothing dominates.
- [craft] The stipple wash inside the map reads as dirt, and the spray of loose black dots below it (v 0.43–0.49) reads as debris; ~69 k commands and 11 m of travel for 8.7 m of draw (dotted lines are expensive).
- [craft] The third vortex claimed in NOTES is not visible; the saddle reads as two blobs.
- [depth] Flat, not declared.

## Next versions
1. **SUPERPOSITION, COMPUTED** (mechanism) — Keep the reference's vertical rhythm but make every curve data: draw real Q and K vectors (e.g. from a small GPT-2 head, as `attention_arcs` already extracts) as bump families, compute QKᵀ as the contoured field, softmax row from it, and Z as the actual weighted superposition of the V bumps — so the green bell is visibly the sum of the ochre curves above it. Same beauty, now falsifiable.
2. **INTERFERENCE FIELD** (abstract) — Collapse the pipeline into the one element that works: a full-sheet contoured similarity field whose eyes are the attended key positions, with the Q and K families reduced to two edge rulers (red top, blue left) that define it as an outer product. Nested/flow order, dominant mass, asymmetric by the data, no stage labels.
3. **THE WEIGHTED SUM** (lens) — Make Z = AV the whole plate: seven V bumps drawn full width, each re-drawn in green scaled by its softmax weight and stacked, so the green envelope forms by visible addition from the ochre originals (the twist: "superposition" read literally). Crop V's outer bumps at the frame for tension.

**If only iterating:**
- Delete the interior stipple and the loose black dots below the map; let rings and paper carry the tone.
- Enlarge the map to ≥ 0.55 of sheet width and shift it off-axis (e.g. centre at u 0.58) so the plate has one dominant, asymmetric mass.
- Make the small third vortex visible (σ larger, 4+ rings) or remove it from the field.
