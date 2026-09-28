# RULED — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/ruled` |
| current render | `gallery/studio/ruled/current/pp_ruled_v2.png` |
| source | `studio/reaction-diffusion/rounds/r03/piece.py::studio_ruled` (round 03 of the REACTION-DIFFUSION family; the successor to VOICING r02, see `studio/voicing/DESCRIPTION.md`; brief `studio/physics/reaction-diffusion.md`). The regression baseline (A4 portrait, seed 7) gives draw 12,820.0 mm; v2 shows 12,818.2 mm. That is near-identical, so the code on disk is v2 or a hair after it. |
| paper · pens | A4 portrait (210 × 297, drawable 10–200 × 10–287), white · 0 black = the ruling (v-field isolines), all type, the crop rule · 1 crimson = everything imposed: two germ squares and five calipers |
| status | unreviewed (no feedback) · 2 renders on disk (v1, v2) |

## In one line
Turing pattern selection drawn as **lattice-with-defects laminae (a page of ruled lines that ruled itself)**: one Gray–Scott field grows on a diffusivity ramp D ×8 left→right, so the line pitch follows √D while the line direction wanders freely; red calipers cut to the predicted √D pitch sit on a Swiss module the black never obeys.

## What is on the sheet
- **The ruling (dominant by area).** Black closed and open isolines of v fill the band u 0–1, v ≈ 0.31–1.0 (y 10–194 mm, 8 of 12 module rows).
  - Pitch coarsens steadily left to right. At the left edge it is a dense labyrinth of tight worms and small closed blobs (≈ 3–4 mm line spacing). At the right edge it is long, sweeping, near-parallel lanes (≈ 10–15 mm), running roughly vertical in the top-right corner and diagonal/horizontal in the lower right.
  - Dislocations (line ends mid-field) and closed islands are scattered throughout.
  - Lines are continuous hairlines at one weight.
- **RULED (the one huge element).** Giant heavy stroke type at the top-left, flush left, 34 mm cap height, u 0.05–0.77, v 0.04–0.16. It is solid-weight mass built from ≈ 6 parallel passes per stem.
- **Caption stack**, flush left under the title (u 0.05):
  - `A PAGE THAT RULED ITSELF` (≈ 3.4 mm, spaced caps, v 0.18)
  - `THE SPACING IS DICTATED. THE DIRECTION IS NOT.` (≈ 2.1 mm, v 0.20)
  - gap
  - `RED IS IMPOSED AND SITS ON THE MODULE.` / `BLACK GREW AND IGNORES IT.` (v 0.23–0.24)
- **Parameter deck** (≈ 1.8 mm, v 0.27–0.36), ending right on top of the ruling:
  - `GRAY-SCOTT  DU 0.16  DV 0.08  F 0.030  K 0.057`
  - `D RAMPED X8.0 ALONG X  DT 0.75  STEPS 6200`
  - `D CHANGES 6 PCT PER WAVELENGTH`
  - `PITCH 7.3  8.4  10.5  12.3  14.8 MM`
  - `RED IS SQRT D  AGREES WITHIN 4 PCT`
  - `GERMS 6 AND 38 CELLS SAME D  PITCH 8.6 AND 8.5`
  - `MODULE 6 X 12`

  The last two lines sit at the top of the ruling band. Isoline fragments touch `MODULE 6 X 12`.
- **Crop rule.** The hard horizontal line at the top of the ruling band (y ≈ 194.7, v ≈ 0.31) is visible only from u ≈ 0.65 to 1.0. Label halos erase the rest, so the Swiss "hard module crop" mostly does not exist on paper.
- **Red calipers.** Five horizontal I-beam calipers (bar + end ticks ≈ 6 mm tall, double-passed) step diagonally down-right on module intersections: (u 0.13, v 0.47), (u 0.31, v 0.56), (u 0.49, v 0.66), (u 0.68, v 0.75), (u 0.86, v 0.85). Their lengths grow ≈ 7 → 15 mm. All are horizontal, whatever the local stripe direction.
- **Red germs.** Two squares with a centre cross, double-passed outline:
  - Small: ≈ 6 mm at (u 0.33, v 0.51), inside a ring of closed contours.
  - Large: ≈ 38 mm at u 0.23–0.43, v 0.75–0.88.

  Both are on the same module column. The ruling runs straight through the large square.
- **Footer** at v ≈ 0.99, one row edge to edge (≈ 2.1 mm): `SWISS   LATTICE WITH DEFECTS` then `PITCH FOLLOWS SQRT D`, which read as one run-on line. Orphaned ruling stubs (tiny dashes) sit between the footer and the bottom margin.
- **Quiet zone.** The right half of the header (u 0.6–1.0, v 0.18–0.30) is bare paper. It is the only negative space; the ruling band is uniformly busy.

## The science it encodes
From the docstring:

- **Model.** Gray–Scott on one lattice with both diffusivities ramped geometrically along x. The ramp is ×8.0 on the sheet (s 0.25 → 2.0); the docstring's "~4.3" is stale. Du:Dv, F, k, dt and the noise are held fixed. The boundary is periodic in y and zero-flux in x.
- **Why √D.** Scaling D by s is an exact similarity under x → x√s, so local pitch must follow √D wherever D changes slowly per wavelength. The sheet prints 6 % per wavelength.
- **Measurement.** At five module stations the local pitch is measured by the structure-factor first moment in 48-cell windows: 7.3 / 8.4 / 10.5 / 12.3 / 14.8 mm.
- **Prediction.** The red calipers are the prediction λ_ref · √(D/D_ref), agreeing within 4 %.
- **Control.** Germs of 6 and 38 cells on the same column (same D) give pitch 8.6 and 8.5, so the seed does not set the length.
- **What the render does not deliver:**
  - The calipers are horizontal while the stripes run at every angle. At station 5 the caliper lies nearly parallel to the stripes and spans no line pair.
  - The Swiss module (6 × 12) is never drawn, so "red sits on the module" cannot be seen.

## How it got here
- **v1.** The parameter deck was overprinted by the giant title and by the caption `A PAGE THAT RULED ITSELF / THE SPACING IS DICTATED...` (three text layers collided in v 0.15–0.23). The germs were solid red serpentine hatch squares covering the ruling. The crop rule was continuous across the full width at y 194. The footer was split left/right with a gap.
- **v2 (current).** The text was re-stacked cleanly: title, caption, principle, deck, top to bottom. The germs became outline + crosshair so the ruling shows through, which is better, since the ruling grew through the germ. The price: the deck now sits on the crop line and its halos erase ~⅔ of the crop rule, and the footer now runs edge to edge.
- No Juan feedback recorded.

## Keep — what works
- **The twist.** Ruled paper whose spacing is dictated and whose direction is not. `THE SPACING IS DICTATED. THE DIRECTION IS NOT.` is exactly one joke, and the Fourier-ring physics is the punchline.
- **The visible pitch gradient.** It runs left-to-right across the whole band, from dense labyrinth to broad lanes. The √D claim is legible at 3 m without reading anything.
- **The giant `RULED`.** Solid, poster-scale, flush left: a real Swiss dominant element with a 3:1+ ratio over everything else.
- **Two pens, one swap, with fixed semantics.** Red = imposed, black = grown.
- **Germs as outline + cross over the ruling (v2).** They show that the pattern grew straight through the seed, and 6 vs 38 cells gives the same texture.
- **The staircase of calipers.** One diagonal gesture across the field, growing in length. It gives the sheet its tension line.

## Weak — what doesn't
- [concept] The calipers are all horizontal, but the ruling's defining property is that it has no direction. Where stripes run horizontal (station 5, lower right) the caliper lies along them and spans nothing, so the falsification is unreadable exactly where the pitch is biggest.
- [grid] The Swiss module is invisible: no module ticks, no drawn grid, and the crop rule is erased for u < 0.65. "Red sits on the module" is asserted in text, not shown. The 6 × 12 module is the canon's whole point.
- [space] The deck's last two lines (`GERMS ...`, `MODULE 6 X 12`) sit on the top of the ruling band, and isolines touch the letters. The footer runs edge to edge, with ruling stubs orphaned under it. Both are collisions.
- [hierarchy] Two type sizes of caption plus a seven-line parameter deck make a grey mid-weight block (v 0.18–0.36) competing with the title. It is the scientific-figure deck again.
- [space] The ruling band is uniformly busy from edge to edge. Nothing in it is shaped as a quiet zone, so the dense-left / sparse-right gradient is the only rhythm.
- [craft] Every red element is double-passed with a 0.3 mm offset, which reads as a doubled line in preview. The crop rule and footer stubs show halo side-effects.
- [depth] Flat (Swiss is flat by canon), but not declared on the sheet or in notes.

## Next versions
1. **stationer's ruling** (lens) — Draw the imposed thing literally. Faint red horizontal rules across the whole band, spaced at the *predicted* local pitch (spacing grows left→right with √D, snapping to module rows at the stations), i.e. a stationer's ruled page that knows the physics. The black ruling grows over it at the same spacing and every angle.
   - Where the black happens to run horizontal it lies right on the red lines: the page ruled itself "both ways".
   - Delete the calipers and let the red ruling be the prediction.
   - Keep the germs.

   The joke becomes visible instead of captioned.
2. **wave-vector calipers** (faithful) — Keep the composition and fix the measurement:
   - Orient each caliper along the local wave vector (the structure-tensor normal at the station), cut to one predicted λ so its ticks land on two consecutive same-phase lines.
   - Draw the 6 × 12 module as hairline ticks at every module intersection in black (or dots).
   - Move the parameter deck up one module row so the crop rule runs unbroken across the full width.
3. **full-bleed page** (abstract) — Make the ruling the whole sheet:
   - The field fills all 12 module rows, and `RULED` is knocked out of it as a void (letters are un-ruled paper, cropped on module lines).
   - The deck is reduced to one footer line under the module crop.
   - Dislocations (line ends) get a single heavier black pass so the "defects" of lattice-with-defects are the second read.

   This gains a shaped negative space (the letters) and removes the figure-deck.

**If only iterating:**
- Rotate every caliper to the local stripe normal and verify on the render that each end-tick sits on a black line one line-pair apart.
- Make the crop rule at y ≈ 194.7 continuous from u 0 to u 1: lift the deck ≥ 6 mm clear of it and exclude the crop rule from label halos.
- Delete the ruling stubs under the footer (crop the field at y ≥ 16 mm) and split the footer into two separate module-aligned blocks with ≥ 1 module column between them.
