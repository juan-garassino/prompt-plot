# GRAVITY IN BALANCE (v14) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/physics/black-hole/engine` |
| current render | `gallery/physics/black-hole/engine/candidates/prior-approved/pp_bh_v14.png` (+ `pp_bh_v14.gcode`; 13 earlier gcode-only variants in `variants/`: original, v5–v13, trim, trim2, check) |
| source | **none named on disk** for `pp_bh_*` (no script references it; `scripts/gallery_import.py` only routes the filename). The render matches the current `promptplot/generative/generators.py::black_hole_bauhaus` run with `colors=4` (4th LEGEND pen, `R_center` boundary circle, broken photon-ring segments, bar columns ending on the clearance circle) — treat that as the source. |
| paper · pens | a4 landscape (297×210, 15 mm margins), white/cream · 0 dodgerblue = left isoradials + swatch · 1 red = right isoradials + swatch · 2 black = bar, shadow spiral, rules, quarter discs, planet · 3 dimgray (fine 0.1) = boundary circle, photon-ring arcs, orbit circles, all type |
| status | unreviewed in the viewer (tier: prior-approved) · 1 render + 14 gcode on disk |

**Sibling:** `studio/physics-black-hole-bauhaus` is v1 of the same generator. This is the later, plotter-hardened state; iterate from here.

## In one line
The Luminet black-hole image drawn as **nested rings partitioned by a vertical bar (nested + partitioned, Bauhaus poster)** — each ring is one exact isoradial at inclination 72°, clipped exactly on the bar edge, blue left / red right for the two sides of the disk.

## What is on the sheet
- **Vertical bar (dominant mass, u 0.45–0.55, v 0.08–0.92).** 21 black vertical lines at ≈1.4 mm pitch, full height; each line ends exactly on a gray clearance circle around the shadow — the bar reads as a striped column, no longer solid.
- **Shadow (u 0.50, v 0.50).** A loose black Archimedean spiral Ø≈26 mm (~9 turns, ≈1.4 mm pitch); around it three concentric broken dimgray ring segments with staggered gaps; then a full dimgray boundary circle Ø≈46 mm (≈0.155 W) that the bar lines and the rings stop on.
- **Isoradial families.** Left: 18 nested dodgerblue loops, rounded tips at u 0.12, running into the bar with a crisp vertical cut on its left edge at u 0.45; they rise to v 0.20 near the bar and fall to v 0.66. Right: 18 red loops, exact mirror, tips at u 0.89. Inner loops pinch into sharp near-cusps close to the bar at v≈0.55.
- **Rules.** Full-width black horizontal rule on v 0.50 (u 0.06–0.94) through the spiral centre. Full-height black verticals at u 0.28 and u 0.67.
- **Orbits (dimgray).** Solid circle Ø≈0.51 W centred (u 0.53, v 0.54) crossing both families and the planet; dashed circle Ø≈0.61 W around it.
- **Planet (u 0.67, v 0.24).** Black concentric disc Ø≈15 mm (5 rings) on the right vertical rule, sitting on top of the red loops and the gray orbit.
- **Quarter-disc stack (u 0.28, v 0.72).** Two black concentric-arc quarter discs (SW and NE, r≈17 mm) meeting on the left vertical rule, a small black double circle below at (u 0.28, v 0.79), and a thin black quarter-arc r≈28 mm to the SW.
- **Furniture.** Swatch bar top-left (u 0.09, v 0.13–0.28): black, blue, red 5-line swatches. Plus marks at (u 0.10, v 0.33) and (u 0.90, v 0.72).
- **Type (dimgray, spaced hairline caps ~2.5 mm).** `G R A V I T Y / I N / B A L A N C E` + short underline at (u 0.33–0.44, v 0.08–0.16), jammed against the bar's left edge. `M A S S / C U R V E S / S P A C E / T I M E` at (u 0.07–0.16, v 0.82–0.90). `M  1  8 0` at (u 0.84–0.94, v 0.90) — `M 1:80` with the colon missing.

## The science it encodes
Same generator as the bauhaus slug (`generators.py::black_hole_bauhaus` docstring: "the exact Luminet isoradials as a clean nested ring family … a full-height black bar the rings vanish behind … Flat, geometric, reduced"). The isoradials are exact (Luminet 1979 eq. 13, elliptic-integral solver, inclination 72°, r up to 28 M) and are now clipped with the exact `geometry` engine (straight cut on the bar edge, arcs cut on the circle). Nothing else carries data: the spiral, broken rings, orbits, planet, quarter discs, rules and swatches are Bauhaus furniture. The left/right colour split is categorical — the render shows no Doppler brightness asymmetry and no ghost (n=1) image; the dome of the direct image over the shadow is behind the bar.

## How it got here
From v1 (2026-09-12) through 13 gcode iterations on 2026-09-15 to v14: the near-solid 0.55 mm bar became 21 striped columns at ~1.4 mm; the bar was narrowed by two columns per side after the Leo plot ("user feedback on the plotted piece", code comment); stair-step notches became exact clips on a clearance circle; the solid shadow spiral opened to a legible ~1.4 mm pitch with broken photon-ring arcs; rings now meet the bar with no white gutter; a 4th fine (0.1) dimgray pen took the circles and all type; pink became red. Gained: plottability and craft. Lost: the solid black mass of v1's shadow — the centre is now gray line-work and the plate has no single black focus. No viewer feedback on file.

## Keep — what works
- The exact clip: blue and red loops stop dead on the bar's straight edges (u 0.45 / 0.55) — crisp occlusion, the best craft on the sheet.
- The striped bar at ≈1.4 mm pitch — plottable, still reads as one mass at 3 m.
- The vertical asymmetry of the families (taller above the axis) — the one visible trace of lensing.
- The dimgray fine pen reserved for secondary circles and type — a working weight hierarchy.

## Weak — what doesn't
- [concept] The bar hides the lensed dome and there is no ghost ring: the plate shows a pair of ellipse families, which a viewer cannot tell from a planet's rings — the black hole is asserted by the caption, not seen.
- [grid] Furniture checklist in full: swatch bar, two plus marks, three crosshair rules, two orbits, a planet, a quarter-disc stack — none aligned with the type; `GRAVITY IN BALANCE` grazes the bar edge.
- [tension] Centred, left/right mirror-symmetric subject with a horizontal rule through its centre — static.
- [space] Planet at (u 0.67, v 0.24) collides with red loops, the gray orbit and the vertical rule.
- [hierarchy] With the shadow opened up, nothing on the sheet is black mass except the bar; the eye has no focal point at 1 m. All type is 2.5 mm hairline.
- [craft] Innermost loops pinch into cusps a fraction of a mm apart next to the bar (u 0.43, v 0.55) — local flooding; colon glyph missing in `M 1:80`.
- [depth] Declared flat ("Flat, geometric, reduced") — acceptable for Bauhaus, but the one depth cue the physics offers (disk passing in front of the hole) is thrown away.

## Next versions
- **COSMIC CENSOR** (lens) — the bar becomes a censor bar and the joke is real physics (Penrose's cosmic censorship: singularities are always hidden behind a horizon). The bar is exactly the shadow's width, hides the singularity and nothing else; around it the full Luminet image is drawn — the dome of the far disk arching over the bar, the near disk crossing in front of its lower half, the ghost ring beneath. Furniture deleted; one line of type on the bar's edge. One black mass, a true wink, and the depth cue restored.
- **BEAMED** (mechanism) — keep the partitioned nest but make the Doppler shift the mapping: approaching-side loops at 3 passes / full duty, receding side single pass with dash duty ∝ observed flux (Luminet eq. 19 × Page–Thorne), so one side glows and the other dissolves. The colour pair becomes a real quantity instead of a category.
- **SOLID EYE** (faithful) — keep v14's clean clip and bar, restore v1's solid shadow as bold spiral at 0.9 mm pitch (one black focal disc), move the whole subject to u≈0.40 so the right family crops at the frame, and cut every furniture item except the swatch bar aligned to the type column.

**If only iterating:**
1. Delete planet, quarter-disc stack, both plus marks and the two orbit circles; keep bar, rings, shadow, one rule.
2. Fill the shadow to one black mass (spiral pitch 0.9 mm) so it is the focal point inside the bar.
3. Draw the n=1 ghost ring below the shadow and let the bar's lower half be crossed by the near-side isoradials (disk in front of the hole).
