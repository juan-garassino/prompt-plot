# WARPED FRAME — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/physics/warped-frame` |
| current render | `gallery/physics/warped-frame/candidates/pp_bauhaus_warped_frame_v2_seed8.png` |
| trials | `candidates/pp_bauhaus_warped_frame_v1_seed2.png`, `…_v1_seed8.png`, `…_v2_seed2.png` |
| source | `promptplot/generative/pieces/abstract.py::bauhaus_warped_frame` |
| paper · pens | a4 portrait (210×297, 15 mm margins), cream · 0 dodgerblue = the most-deflected rulings · 1 deeppink = photon ring (3 passes) + echo ring · 2 black = the warped lattice, singularity plus mark, type |
| status | unreviewed in the viewer (tier: candidates; CLAUDE.md lists it among the APPROVED Bauhaus pieces) · 4 renders on disk |

## In one line
Gravitational lensing drawn as **a lattice with one defect (lattice-with-defects)** — a straight square grid is pushed outward by the exact point-lens map θ = ½(β + √(β² + 4θ_E²)), so every ruling bends around a bare-paper void and never enters it; the rulings that bend hardest turn blue, and one pink ring sits at b = 3√3·M.

## What is on the sheet
- **Warped lattice (dominant, full bleed of the drawable area u 0.07–0.93, v 0.05–0.95).** ~34 black horizontal and ~34 black vertical rulings (~7–8 mm pitch, lightly jittered). Far from the void they are straight; near it they bow outward around it: horizontals arch over the top (v 0.3–0.4) and sag under the bottom (v 0.75–0.85), verticals bulge left and right (u 0.1–0.2 and 0.55–0.65). Rulings run off all four margins.
- **The void (centre u 0.37, v 0.61 in v2; v 0.55 in v1).** A disc of bare paper Ø≈80 mm (≈0.38 W) bounded by the **pink photon ring** — a bold ring of 3 tight passes — with a thin pink echo ring ≈1 mm outside it, and a tiny black `+` at the centre.
- **Blue rulings.** The 8 rulings passing closest to the void, in blue: two near-vertical pairs pinch together into thin waists above (u 0.33–0.42, v 0.05–0.45) and below (v 0.78–0.95) the void; two horizontal pairs pinch to the left and right (v 0.55–0.68). Near the ring they flatten into arcs that hug the pink ring within 1–3 mm (u 0.22–0.52, v 0.47–0.75), so the ring is wrapped by a tight blue/pink bundle.
- **Type band (bottom-left, u 0.09–0.44, v 0.86–0.94).** The lattice is cleared from a rectangle there (rulings end abruptly on its top edge, v 0.86, and on its right edge, u 0.44). `W A R P E D / F R A M E` black spaced caps ~3 mm with a short underline, then `G R A V I T Y   I S   T H E   G R I D` ~2 mm below — at this size the `G`s render as a malformed hook glyph. Two blue rulings pass through the band's right half.
- **Footer (bottom-right, u 0.64–0.93, v 0.95).** `B   3 S Q R T 3   M` in spaced caps (the `=` in "B = 3 SQRT3 M" is missing) — printed directly over the lattice rulings.
- **Swatches (u 0.89, v 0.88–0.90).** Three tiny black/blue/pink squares ≈2 mm, pressed against the right margin on top of the lattice.

### Version differences
- v1 (seed 2, seed 8): void higher (v 0.55), pink ring the same; blue rulings' waists slightly wider.
- v2 (seed 2, seed 8): void lowered to v≈0.61, echo ring tighter; seed 8 vs seed 2 differ only by lattice jitter.

## The science it encodes
Docstring (`pieces/abstract.py::bauhaus_warped_frame`): "A straight Bauhaus lattice bent by an exact closed-form Schwarzschild point-lens around an off-center void. The outer-image map θ=½(β+√(β²+4θ_E²)) guarantees θ≥θ_E, so the shadow interior is provably never inked — the event horizon is bare paper. One loud pink photon ring sits at the critical impact parameter b=3√3·M; the innermost, most-deflected rulings turn blue." The echo ring is "one plottable self-similar echo (e^-π out)". Exact: the outer-image mapping and the guarantee that no ink enters the void. A stylistic identification: the code sets the Einstein radius θ_E equal to the shadow radius (3√3 M); for a real lens θ_E depends on observer–lens–source distances and is usually far larger than the shadow, so the plate merges two different radii. Only the outer image is drawn — a point lens always makes a second (inner) image, which is absent. Lattice jitter is seeded decoration.

## How it got here
v1 → v2: the void moved lower (v 0.55 → 0.61), putting more lattice above it and a clearer vertical tension; echo ring tightened. Otherwise unchanged. No viewer feedback on file.

## Keep — what works
- The concept is already an abstract order, not a figure: a lattice with one defect — the grid IS spacetime, no object drawn. It passes §6.
- Bare paper as the horizon — the void at (u 0.37, v 0.61) is the plate's dominant form and it is made of absence.
- Rulings running off all four margins: the field is infinite and the sheet is a window.
- The blue waists pinching above and below the void (u 0.33–0.42) — the strongest visible sign that space is being squeezed.
- The off-centre void (left of centre, below middle) — real asymmetry.

## Weak — what doesn't
- [craft] The pink ring is a 3-pass bold ring plus an echo ring ≈1 mm outside it plus blue rulings hugging within 1–3 mm — a tight coloured bundle that will muddy (pink-on-blue, sub-mm gaps); the echo reads as a registration error, not a e^-π echo.
- [space] Footer `B 3 SQRT3 M` printed over the rulings and the swatches pressed into the right margin on top of the lattice — collisions.
- [grid] The type band is a hard rectangular hole cut out of a curved field; rulings stop on its edges at arbitrary points; the type does not share any line with the lattice.
- [hierarchy] Type at 2–3 mm hairline; `GRAVITY IS THE GRID` glyphs malformed at 2 mm; the `=` is missing in the footer.
- [depth] Flat lattice with uniform line weight — lensing is a depth phenomenon (light coming around the far side); no weight or duty change with deflection except the blue swap.
- [concept] Only the outer image; θ_E ≡ shadow radius conflation is undeclared.

## Next versions
- **SECOND IMAGE** (mechanism) — draw what a lens really does: every ruling also forms an inner image, θ₋ = ½(β − √(β² + 4θ_E²)), squeezed into a thin annulus just outside the photon ring and flipped — so the grid appears twice, the second copy compressed and inverted, with duty (dash fraction) set by the image's magnification |μ|. The ring is then earned by the pile-up of images instead of drawn as a separate loud circle. Lattice-with-defects becomes lattice-with-its-own-reflection; the physics goes from half to whole.
- **GRAPH PAPER** (lens) — the sheet is a page of engineer's graph paper (fine 1 mm and bold 10 mm grids, a printed title strip, margin line) and the hole bends the paper's own printed grid, title strip and all; the type is the paper's printed header, warped. Everyone owns graph paper; the twist is that the reference frame you measure with is the thing that bends. Type finally shares the grid.
- **CROPPED DEFECT** (abstract) — move the void so its ring crops the left frame edge at v≈0.6, halve the ruling count (pitch ~14 mm), make the ring a single 3-pass stroke with the echo removed, and set the type in the lattice's straightest cell top-right, aligned to a ruling. Tension up, craft clean.

**If only iterating:**
1. Remove the echo ring or push it ≥ 3 mm outside the photon ring, and cut blue rulings to stop ≥ 2 mm from the pink ring.
2. Move the footer and swatches onto a cleared strip (or into the type band) so nothing is printed over rulings; add the missing `=` glyph.
3. Replace the rectangular type cut-out with a band bounded by two actual (warped) rulings, and set `GRAVITY IS THE GRID` at ≥ 3 mm so the G glyphs resolve.
