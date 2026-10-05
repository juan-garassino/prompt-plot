# ATTENTION AS TOPOGRAPHY — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/topo_scatter` |
| current render | `gallery/studio/topo_scatter/current/pp_topo_scatter_v16.png` |
| source | `studio/topography-scatter/rounds/r01/piece.py::attention_as_topography` |
| reference | `studio/topography-scatter/ref/reference.png` |
| paper · pens | a4 landscape (297×210 mm) · 0 crimson = Q blob + its connector bundle + two loose red dots + red dash-dot furniture · 1 dodgerblue = K blob + its connector bundle · 2 goldenrod = V blob + its connector bundle · 3 black = contour nest, softmax lens + stipple, dot column, Z terrain, all type, all furniture |
| status | unreviewed (no feedback file; NOTES.md records that Juan flagged the softmax flooding before r13) · 16 renders on disk |

## In one line
Self-attention drawn as a **scattered constellation** reproduced from a reference — three coloured amoeba blobs (Q, K, V) send curve bundles into a black contour nest (QKᵀ), which drains down a dot column through a stippled softmax lens into a profile-stack terrain (Z = AV) — every position measured off the raster.

## What is on the sheet
- **Contour nest `QKᵀ` (dominant black mass).** A domain-warped topographic nest, ~0.24 of sheet width, spanning u≈0.34–0.58, v≈0.29–0.52; ~20 rings, near-solid spiral at the summit (u≈0.43, v≈0.40), rings opening into a wider plateau to the right (u≈0.48–0.56); the outer two rings dashed and a dashed outrider loop swinging off right to u≈0.60. `QKᵀ` (raised T) above at u≈0.48–0.51, v≈0.26. A black line with end dots crosses the nest from u≈0.38, v≈0.31 to u≈0.50, v≈0.35. Vertical black rules pierce it at u≈0.43 (v≈0.18–0.57, dot at top v≈0.16) and dashed verticals at u≈0.45, 0.48.
- **Q (crimson).** Amoeba blob ~0.12 of width at u≈0.10–0.22, v≈0.10–0.27, filled with an even cross-hatched lattice (two ~0.9 mm passes) inside a keyline; two black nodes inside joined by thin black lines, one running out to u≈0.23, v≈0.15. `Q` (bold sans) at u≈0.10, v≈0.14. From its right edge a bundle of 7 crimson curves (solid, dashed, dash-dot) rises right then plunges down into the nest's left flank at u≈0.36–0.40, v≈0.36–0.43. Loose crimson dots at u≈0.09, v≈0.28 and u≈0.21, v≈0.19; red dash-dot verticals at u≈0.08 and 0.12 (v≈0.27–0.42) crossed by a black rule at v≈0.35.
- **K (blue).** Waisted amoeba (hourglass) ~0.10 of width at u≈0.11–0.21, v≈0.43–0.66, same lattice fill, black node at u≈0.15, v≈0.52 and a black line from u≈0.15, v≈0.60. `K` at u≈0.10–0.12, v≈0.56. A blue bundle of 8 curves (solid/dashed/dash-dot) runs right as a sagging hammock and lifts at the right into the nest's lower-left (u≈0.38–0.42, v≈0.46–0.55).
- **V (goldenrod).** Crescent/boomerang blob ~0.12 of width at u≈0.77–0.89, v≈0.09–0.34, lattice-filled, two black nodes with a black arc leaving it down-right to u≈0.93, v≈0.42. `V` at u≈0.80, v≈0.20. A wide goldenrod bundle of ~12 curves fans from V's lower half down-left: some loop back through the nest's right flank (u≈0.58–0.62, v≈0.35–0.55), the rest sweep down to converge on the Z terrain's summit at u≈0.69, v≈0.70.
- **Softmax lens + dot column (vertical axis at u≈0.455).** A thin tilted ellipse outline at u≈0.38–0.60, v≈0.57–0.60 holding a bounded black stipple that ramps from sparse at the left to mid-grey at u≈0.52, then stops; a large node dot at u≈0.455, v≈0.59. `softmax` (lower-case) at u≈0.33–0.39, v≈0.62. The column below/above: dots at v≈0.52, 0.54, 0.55, a small ring at v≈0.62, dots at v≈0.66, 0.68, a big dot at v≈0.72, a large plus at v≈0.81, a lone dot at v≈0.895.
- **Z terrain (second black mass).** A profile stack of ~25 crossing curves at u≈0.54–0.88, v≈0.70–0.86: flat and converging to a point at the left (u≈0.54, v≈0.80), a tall summit at u≈0.69, v≈0.70 (big node dot on top), a lower second mass at u≈0.77–0.80, and convergence at the right into a small bracket/rectangle (u≈0.85–0.88, v≈0.80–0.81). The base band bunches nearly solid along v≈0.80. `Z` (bold) at u≈0.835, v≈0.72. Bottom right: `Z = AV` (u≈0.88–0.93, v≈0.88) above a long rule with a small filled square at its left end (u≈0.815–0.93, v≈0.91).
- **Title.** `ATTENTION` / `AS` / `TOPOGRAPHY` in wide-spaced caps at u≈0.07–0.20, v≈0.85–0.90, with a short rule to its right (u≈0.23–0.30, v≈0.90).
- **Furniture (scattered, black).** A long thin arc from u≈0.19, v≈0.81 rising to u≈0.40, v≈0.69; a tall vertical rule at u≈0.31 (v≈0.31–0.73) with a plus at v≈0.65; a stepped bracket-and-arc at top centre (u≈0.50–0.54, v≈0.12–0.17) trailing a dashed curve to u≈0.67, v≈0.24; dashed/dash-dot strokes scattered u≈0.62–0.78, v≈0.25–0.70; a dashed rectangle corner at u≈0.55–0.64, v≈0.33; right-side vertical with crossbars at u≈0.93, v≈0.16–0.26 and a quarter arc u≈0.85–0.93, v≈0.26–0.42; another quarter arc at u≈0.92–0.93, v≈0.74–0.82; a dashed vertical at u≈0.87, v≈0.55–0.75; ~20 loose black dots of assorted size.
- **Quiet zones.** Lower-left u≈0.07–0.33, v≈0.68–0.84 (inside the big arc) and upper centre-right u≈0.55–0.75, v≈0.08–0.20.

## The science it encodes
Per `studio/topography-scatter/rounds/r01/NOTES.md` and the module docstring: "This is a REPRODUCTION, not a design." Nothing is computed from an attention layer. Blob silhouettes were traced from the reference's colour masks; dot centres and sizes came from a connected-component pass; the contour nest is marching squares on a domain-warped synthetic field with ring radii ∝ k^1.08; the terrain is a stack of 25 profiles of a sum of edge-centred 2-D gaussians chosen so fans cross; the softmax fill is `kit.tone_dots` (≤1.38 dots/mm² at cell 0.85). The mapping Q/K → QKᵀ → softmax → ·V → Z is purely positional (bundles converge where the equation says they would); no weight, score or distribution on the sheet is real.

## How it got here
16 renders in r01 (NOTES "Rounds"). Sampled trials:
- **v4**: huge terrain filling the lower centre with a thick, near-solid crossing bundle; softmax lens stippled solid black; a semicircle arc lower-left.
- **v7**: terrain flattened into a thin low band (the r5 "edge-centred masses that fan" turn); nest tight.
- **v10**: terrain gets a real summit and crossings; ochre bundle spread; lower-left arc becomes the long thin arc.
- **v13**: softmax fill replaced with `tone_dots` after Juan flagged the flooding; third blob scribble pass dropped; nest widened.
- **v16** (current): cell size tuned, shared lower-case font for `softmax`, node discs closed as solid dots.
Gained: plottable fills (no flooding), terrain character. Lost: the reference's saturated colour washes — blobs now read as an open lattice. Juan's feedback (as recorded in NOTES): the softmax ellipse was flooding in v8; no verdict on file.

## Keep — what works
- Asymmetric scatter on a landscape sheet with large white reserves — the three colour masses pin three corners (Q top-left, K mid-left, V top-right) and pull the eye through the black centre.
- The contour nest with a tight summit spiral opening to a warped plateau (u≈0.43, v≈0.40) — the strongest single form.
- Bundles converging INTO forms: crimson dives into the nest's left flank, goldenrod lands on Z's summit — flow reads as data arriving.
- The softmax lens: bounded `tone_dots` ramp inside a thin tilted ellipse on the dot-column axis; plottable and delicate.
- Z terrain's crossing profile fans and point convergence at both ends.
- Measured-reference method (traced silhouettes, component-detected dots) for any faithful round.

## Weak — what doesn't
- [concept] It is an annotated pipeline diagram (Q, K, V → QKᵀ → softmax → Z = AV, with the equation printed) — § 6 NO SCHEMATICS; and nothing on the sheet is computed from attention, so even the "topography" is decoration.
- [craft] Blob fills read as a regular diagonal lattice/netting (the two crossing passes) rather than a colour wash or a scribble — a mechanical texture at odds with the organic outlines.
- [craft] Z terrain's base bunches near-solid (v≈0.80, u≈0.56–0.66 and u≈0.80–0.87); the nest summit approaches a solid spiral.
- [grid] ~40 pieces of furniture (dashes, arcs, brackets, verticals, loose dots) placed at reference pixel positions with no shared axis — furniture checklist at scale.
- [hierarchy] Nest, three blobs and terrain are all ~0.12–0.34 of width; the nest wins only marginally.
- [space] The lower-left quiet zone is inside an arbitrary arc; the empty upper centre is a residue of the reference layout, not composed.
- [depth] Flat and undeclared except for the terrain's pseudo-3D profiles.

## Next versions
1. **real-attention-field** (mechanism) — Keep the scatter and pens, but compute it: take a real attention head (the repo already extracts GPT-2 attention via `scripts/extract_gpt2_attention.py`), draw the nest as the actual QKᵀ score field contoured by gradient (`kit.even_contour_levels`), the softmax lens stipple as the real row distribution, and Z's profile stack as the real output rows. Bundle widths = real weights. The same plate, but every mark carries data.
2. **three-sources-interfering** (abstract) — Transpose to INTERFERING: Q, K, V become three ring-sources in their pens whose contour families meet; QKᵀ is where the Q and K families' rings coincide (drawn black), and the V family's rings are shifted by those coincidences to produce Z. Drops blobs, bundles and furniture; the whole sheet is one field. Style: Psychedelic (deformation) as a declared canon.
3. **faithful-wash** (faithful) — Close the fidelity gaps honestly: replace the crossed lattice with a single meandering serpentine scribble at ≥0.86 mm plus a denser keyline band (reads as a wash, not a net), lobe the contour field to recover the reference's left notch and down-right tail, thin the terrain base rows, and prune furniture to the ~20 elements that share an axis with a form.

**If only iterating:**
- Replace the crossed diagonal lattice in Q/K/V with a single-direction meandering scribble following each blob's long axis; test: at 1 m the blobs read as colour masses, not mesh.
- Space Z's profile rows by gradient so no base band reads solid, and cap the nest summit ring pitch at 0.8 mm; test: white visible between every pair of rings/profiles.
- Cut furniture by half — keep only elements that align with a form's axis (the dot column u≈0.455, the nest's vertical, the terrain baseline); test: every remaining furniture stroke shares a line with a form within 1 mm.
