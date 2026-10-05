# BIG BANG → GREAT ATTRACTOR — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/physics/big-bang` |
| current render | `gallery/physics/big-bang/candidates/prior-approved/pp_big_bang_v1_ORIGINAL_seed7_v1.png` (the ORIGINAL, `big_bang_v1`) · `gallery/physics/big-bang/candidates/prior-approved/pp_big_bang_seed7_v1.png` (the REWORK, `big_bang` — the newer composition; both files dated 2026-09-13) |
| source | `promptplot/generative/generators.py::big_bang_v1` (original) · `promptplot/generative/generators.py::big_bang` (rework, the registry's primary) |
| paper · pens | a4 portrait (210×297, 15 mm margins), cream/white · 0 green = source eruption, escaping field lines, "BIG BANG" · 1 red = attractor hub, inflow, "GREAT ATTRACTOR" · 2 goldenrod = braid of particle trails · 3 darkgray = dotted celestial sphere, rule, footer |
| status | unreviewed in the viewer (tier: prior-approved; listed as "earlier approved" in the 2026-09-13 checkpoint) · 2 renders on disk |

## In one line
A cosmological source–sink drawn as a **2D unequal dipole field (flow-to-attractor on an orbital sphere)** — field-line density is the source/sink strength ratio (1 : 0.32), so most lines escape and a minority bundle falls into the attractor; the ORIGINAL is a centred, balanced dipole inside a small sphere, the REWORK is an asymmetric eruption top-left with a giant cropped sphere and poster type.

## What is on the sheet

### ORIGINAL (`pp_big_bang_v1_ORIGINAL_seed7_v1.png`) — the batch's "current"
- **Dipole lune bundle (dominant, centre).** ~10 green and ~9 red field lines drawn as nested lune arcs from the source at (u 0.40, v 0.33) to the sink at (u 0.65, v 0.62); outermost arcs bulge out to u≈0.14 on the left and u≈0.88 on the right; the bundle spans v 0.25–0.77, width ≈ 0.75 of the sheet. Green and red lines run as near-parallel **pairs** 1–2 mm apart — each lune is effectively drawn twice in two colours.
- **Source (u 0.40, v 0.33).** Tiny green spiral core Ø≈5 mm with a few particle specks; 8 green arrowed rays escape up-left, arrowheads at v 0.23–0.37, u 0.12–0.55.
- **Sink (u 0.65, v 0.62).** Red double ring Ø≈5 mm with ~16 short spokes; 6 red rays leave down/right and end loose around v 0.7–0.77 with no arrowheads.
- **Type.** `B I G   B A N G` green spaced caps ~3 mm, immediately right of the source at (u 0.45–0.74, v 0.33) — printed straight across the green/red arcs. `G R E A T   A T T R A C T O R` red spaced caps at (u 0.27–0.65, v 0.62), running left from the hub and **through** 4–5 lune lines.
- **Gold braid.** A barely visible trail of gold dots on the straight diagonal source→sink.
- **Sphere.** Faint gray dotted latitude/longitude texture filling a disc of Ø≈0.8 sheet width centred near (u 0.50, v 0.50) — reads as gray noise, not as a globe.
- **Quiet zones.** Top band v 0.05–0.22 and bottom band v 0.78–0.95 are completely empty: unshaped leftover.

### REWORK (`pp_big_bang_seed7_v1.png`)
- **Celestial sphere (ground).** A giant gray dotted sphere cropped by the left (u 0.07) and top (v 0.05) margins; its limb is visible as a dashed gray arc down the right side (u 0.72→0.89, v 0.1→0.5) and along the bottom (v≈0.78). Interior dotted lat/long grid is so faint it reads as dust.
- **Eruption (dominant, u 0.30, v 0.17).** Green spiral core Ø≈10 mm (~5 turns); a burst of ~40 short radial spokes out to r≈12 mm; 6 broken concentric "shock" arc fragments at r 15–30 mm; scattered short green particle dashes. ~14 long green field lines with open arrowheads escape: six arrowheads stacked against the left margin (u 0.07, v 0.06–0.44), five against the top margin (v 0.06, u 0.18–0.55), three on the right limb (u 0.75–0.84, v 0.12–0.35); one long line runs down-left to an arrowhead at (u 0.40, v 0.75).
- **Infall bundle.** ~8 green field lines leave the source downward and curve right in wide lunes (the widest reaches u 0.29 at v 0.52 and bottoms at v 0.66) into the sink.
- **Gold braid.** 6–7 parallel gold dashed curves (dashes lengthening downstream) ride the most direct field line from (u 0.33, v 0.2) to the sink at (u 0.7, v 0.55); one green line runs inside the braid.
- **Attractor (u 0.70, v 0.57).** Red double ring Ø≈6 mm, ~24 short spokes, ~12 red inflow curves with inward arrowheads from ~25 mm out — a small red asterisk-flower. A single gray hairline leader drops straight down from the hub to the caption.
- **Type band (v 0.86–0.95).** `BIG BANG` green, stroke display caps ~12 mm tall, flush left at u 0.07–0.45, v 0.86–0.90. `GREAT ATTRACTOR` red ~5 mm caps at u 0.70–0.93, v 0.90, its left edge on the hub's leader. Full-width gray rule at v 0.92. Gray footers ~2 mm: `01 EXPANSION FIELD` flush left, `02 LANIAKEA FLOW - 520 MLY` flush right (v 0.94).
- **Quiet zones.** Right column u 0.89–0.93 and the lower-left quadrant inside the sphere (u 0.1–0.6, v 0.6–0.78) are near-empty.

## The science it encodes
From the docstrings of `big_bang` / `big_bang_v1` (`generators.py` §43, "astro series 01"): a softened 2D dipole `v = SA·r̂_A/|r_A|² − SB·r̂_B/|r_B|²` with SA=1.0, SB=0.32, integrated by fixed-step Euler (step 1.1 mm); lines stop on the sphere, the frame, or inside the sink. That field is exact for what it is, but everything cosmological is **metaphor**: the source strength, sink strength, the softening (+3 mm²), spiral, shock arcs and "Hubble-scaled particle dashes" are authored decoration; only the footer figure (Laniakea ≈ 520 Mly) is a real number and it maps to nothing on the sheet. Physically the plate encodes a known misconception — the Big Bang drawn as a point explosion *in* space, with the Great Attractor as a sink competing with it. The Big Bang has no centre; the Great Attractor is a peculiar-velocity basin on top of a uniform Hubble expansion. The render does not show "Hubble scaling" legibly (the particle dashes read as random specks).

## How it got here
ORIGINAL (`big_bang_v1`): symmetric-ish dipole centred on the sheet, small sphere, type in the field. REWORK (`big_bang`): gained tension (source top-left, sphere cropping the frame), a real type band with a leader locking the hub to its caption, an unequal dipole so the source dominates, and a legible gold braid; lost the doubled green/red lunes (good) but also lost the sink's presence — the attractor is now a small flower at 1/5 the source's visual mass. No viewer feedback on file.

## Keep — what works
- REWORK: the source crammed top-left with lines exploding off the left and top frame edges — the only element with real energy; the frame crop at u 0.07 / v 0.05 is the right idea.
- REWORK: the hairline leader that drops from the hub (u 0.70) to the left edge of `GREAT ATTRACTOR` — the one true shared grid line on the sheet.
- REWORK: gold dashes lengthening along the braid toward the sink — motion encoded by duty, plottable.
- REWORK: the scale contrast between the 12 mm `BIG BANG` and the 5 mm red caption.
- Both: the unequal-dipole idea (most lines escape, a minority falls in) as the one mapping the plate is built on.

## Weak — what doesn't
### ORIGINAL
- [tension] Dipole centred on the sheet with empty top and bottom bands — "subject floating dead-centre".
- [craft] Every lune drawn twice (green + red) 1–2 mm apart — double ink, reads as misregistration.
- [space] Both captions printed through the field lines (`GREAT ATTRACTOR` crosses 4–5 arcs) — collision, not overlap.
- [depth] The sphere is gray noise; no globe is perceived.
### REWORK
- [concept] The central claim is a textbook misconception: a point Big Bang in space opposite a sink. The collection should not ship a wrong mental model, however pretty; it is also a schematic dipole (field-lines-with-arrowheads = physics-textbook figure, §6 NO SCHEMATICS).
- [space] Six arrowheads pile against the left margin and five against the top — elements pressed against the frame read as crowding, not crop (§4).
- [hierarchy] The attractor (u 0.70, v 0.57) is a small red asterisk with no mass; the second read at 1 m is the gold braid, not the sink the caption names.
- [craft] The gold braid runs under a green field line — ink-on-ink along its whole length; the sphere's dot grid is sub-visible and will plot as specks.
- [depth] The sphere is claimed but not drawn: no limb weight, no latitude falloff, the "globe" reads as a dashed boundary only.
- [grid] `BIG BANG` sits at v 0.86–0.90 while `GREAT ATTRACTOR` baseline is at v 0.90 — two baselines 3 mm apart, neither shared.

## Next versions
- **NO CENTRE** (lens) — replace the point source with the Hubble law itself: two copies of one lattice of dots (galaxies), the second scaled by 1.08 about an arbitrary point, joined dot-to-dot by short green strokes — every stroke points away from wherever the eye lands, so the plate visibly has no centre (the twist: "where did the Big Bang happen? — here"). Then the Great Attractor enters as the one real defect: in one off-centre basin the red strokes bend toward a sink by the peculiar velocity. Order: lattice-with-defects; mapping: stroke length = distance × H₀, red deflection = peculiar velocity. Fixes the misconception, kills the schematic, and gives the sink real mass (a whole region of the lattice), so it should jump hierarchy and concept scores.
- **LANIAKEA BASIN** (mechanism) — drop the Big Bang entirely and draw the flow-to-attractor order of Laniakea: evenly-spaced streamlines of a (published, simplified) peculiar-velocity field converging on the Great Attractor, basin boundary left as bare paper, the Milky Way a single red dot on one streamline. Scores on concept exactness; risk: too close to WATERSHED.
- **ERUPTION CROPPED** (faithful) — keep the rework's composition but make it honest furniture-free poster: sphere drawn as a real globe (latitude ellipses with dash density falling to the limb), source moved so its burst crops at the corner, arrowheads removed (lines just leave the frame), sink enlarged to a real mass (concentric infall rings Ø≥30 mm).

**If only iterating:**
1. Remove all arrowheads that land within 3 mm of the margin; let those lines run off the frame instead.
2. Enlarge the attractor hub to Ø ≥ 25 mm (concentric infall rings in red) so it is the clear second mass at 1 m.
3. Offset the gold braid ≥ 2 mm clear of every green line and draw the sphere's latitude circles as visible dashed ellipses whose dash density falls toward the limb.
