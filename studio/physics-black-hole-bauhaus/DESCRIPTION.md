# GRAVITY IN BALANCE — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/physics/black-hole/bauhaus` |
| current render | `gallery/physics/black-hole/bauhaus/candidates/prior-approved/pp_black_hole_bauhaus_seed42_v1.png` (2026-09-12; later v2–v4 exist only as `.gcode` in `variants/`) |
| source | `promptplot/generative/generators.py::black_hole_bauhaus` |
| paper · pens | a4 landscape (297×210, 15 mm margins), white/cream · 0 dodgerblue = left isoradial family + swatch · 1 deeppink = right isoradial family + swatch · 2 black = bar, shadow disc, rules, orbits, quarter discs, planet, type |
| status | unreviewed in the viewer (tier: prior-approved; v4 plotted on Leo 2026-09-13 with fill_mm=1.4) · 1 render + 6 gcode variants on disk |

**Sibling:** `studio/physics-black-hole-engine` is the SAME generator 3 days later (v14, 4 pens). Iterate from v14; this file records the v1 state and what v14 fixed.

## In one line
The Luminet black-hole image drawn as **nested rings split by a vertical bar (nested + partitioned, Bauhaus poster)** — each ring is one exact isoradial (a disk radius seen through the lens) and the left/right halves are coloured blue/pink for the approaching/receding side.

## What is on the sheet
- **Vertical bar (dominant mass, u 0.44–0.56, v 0.08–0.92).** A full-height band of ~60 black vertical lines at ~0.55 mm pitch — reads nearly solid black. Around the shadow the bar opens in stepped rectangular notches (stair-step clearance, visible at v 0.35–0.42 and 0.58–0.65).
- **Shadow disc (u 0.50, v 0.50, Ø ≈ 0.14 W).** A tight black spiral at ~0.55 mm pitch — plots as a solid black disc — surrounded by an open ~4 mm white gap and a thin broken black ring (two arcs open at top-left and top-right).
- **Isoradial families.** Left: ~22 nested dodgerblue loops, rounded tips out at u 0.12, flattening toward the bar, spanning v 0.18–0.68, cut off ~2 mm before the bar (white gutter). Right: the exact mirror in deeppink, tips at u 0.88. The families are taller above the horizontal axis (to v 0.18) than below (to v 0.68) — the lensing asymmetry — but their domed tops are hidden behind the bar.
- **Rules.** Full-width black horizontal rule on v 0.50 (u 0.05–0.94); two full-height black verticals at u 0.28 and u 0.67.
- **Orbits.** A black circle Ø≈0.51 W centred (u 0.53, v 0.54), crossing both families and the bar; a larger dashed black circle Ø≈0.61 W around it.
- **Planet (u 0.67, v 0.24).** Black concentric disc Ø≈15 mm (≈10 rings) sitting on the right vertical rule, overlapped by the pink rings and the orbit circle.
- **Quarter-disc stack (u 0.28, v 0.72).** Two black quarter-disc fills (SW and NE quadrants, r≈17 mm) meeting at the left vertical rule, a small double circle at (u 0.28, v 0.79), and an outer black quarter-arc r≈28 mm.
- **Furniture.** Swatch bar top-left (u 0.09, v 0.13–0.28): black, blue, pink 5-line swatches. Plus marks at (u 0.10, v 0.33) and (u 0.90, v 0.72).
- **Type (black, spaced hairline caps, ~2.5 mm).** `G R A V I T Y / I N / B A L A N C E` with a short underline at (u 0.33–0.44, v 0.08–0.18). `M A S S / C U R V E S / S P A C E / T I M E` at (u 0.07–0.16, v 0.82–0.90). `M  1  8 0` at (u 0.84–0.93, v 0.90) — the source string is `M 1:80`; the colon glyph did not render.

## The science it encodes
Docstring (`generators.py::black_hole_bauhaus`): "the exact Luminet isoradials as a clean nested ring family (blue left | pink right), a solid-filled shadow disc, a full-height black bar the rings vanish behind…". The rings are computed from the same exact elliptic-integral impact-parameter solver as `black_hole` (Luminet 1979 eq. 13), inclination 72°, 26 radii up to r=28 M: that part is exact. Everything else is decoration: the bar, orbits, planet, quarter discs, rules and swatches carry no quantity. Blue/pink is categorical (left/right), not flux — the Doppler asymmetry that makes one side of a real disk far brighter is not encoded. Only the direct image (n=0) is drawn; the ghost image — the signature of the Luminet picture — is absent, and the dome of the direct image over the shadow sits behind the bar.

## How it got here
Single render (v1). Code history in the gcode names: v2/v3/v4 (+ `_slow` feeds) on 2026-09-13; v4 was plotted with `fill_mm=1.4` (coarser bar) after the near-solid 0.55 mm bar proved too dense. The code comment "bar narrowed by two columns per side (user feedback on the plotted piece)" records the one known note. The current code (4-pen legend layer, exact circle-clipped bar columns, broken photon-ring segments) is what `physics-black-hole-engine` v14 shows.

## Keep — what works
- The bar-as-occluder idea: the rings vanishing behind one heavy vertical at u 0.44–0.56 is the single strongest graphic move — it is the Bauhaus mass.
- The nested isoradial families themselves: 22 clean loops each side, taller above the axis than below — exact data drawn as pure order.
- The shadow disc at dead centre of the bar as the one solid black mass (the shadow as ink).
- Blue/pink tips reaching u 0.12 / 0.88 give the plate its horizontal span.

## Weak — what doesn't
- [craft] Bar at 0.55 mm pitch and shadow spiral at 0.55 mm pitch flood solid — both below the 0.8 mm floor; the plotted v4 had to coarsen to 1.4 mm.
- [craft] Stair-stepped rectangular notches where the bar clears the shadow; 2 mm white gutter between rings and bar looks like a clipping error.
- [grid] Furniture checklist: swatch bar, two plus marks, three crosshair rules, two orbit circles, quarter-disc stack, planet — exactly the rubric's known failure mode; none shares an axis with the type.
- [concept] The bar hides precisely what makes a black-hole image a black-hole image (the lensed dome over the shadow) and the ghost ring is not drawn; blue/pink is a category, not beaming.
- [tension] Perfectly centred, mirror-symmetric subject with even margins — "student work" by the rubric.
- [space] The planet disc (u 0.67, v 0.24) is overrun by pink rings, the orbit circle and the vertical rule — collision.
- [hierarchy] All type is 2.5 mm hairline caps; `M 1:80` loses its colon.

## Next versions
- **COSMIC CENSOR** (lens) — the bar becomes a *censor bar*, the pictogram everyone knows, and the joke is real physics: Penrose's cosmic-censorship conjecture says every singularity is hidden behind a horizon. Make the black bar exactly the shadow's width (b = 3√3 M on the plate's scale), horizontal or vertical, hiding the singularity and nothing else, while the full Luminet image — dome over the top AND ghost ring beneath — is drawn around it. Delete every piece of furniture. Hierarchy (one black mass), concept (a wink that is literally true) and depth (direct image passes in front of the bar's lower edge) all go up.
- **BEAMED** (mechanism) — keep nested rings but let Doppler flux drive pen passes: approaching side drawn 3× (bold), receding side single-pass and dash-thinned to 30% duty, pen chosen by flux band; the symmetric blue|pink split disappears. The mechanism becomes visible instead of labelled.
- **OFF-AXIS NEST** (abstract) — crop: enlarge the ring family so the outer loops leave the frame on the right, move the shadow to u≈0.38, keep only the bar and one line of type on the bar's edge.

**If only iterating:**
1. Build from v14 (the engine slug); delete swatch bar, both plus marks, the planet and the quarter-disc stack.
2. Narrow the bar to the shadow's diameter and draw the dome of the direct image and the n=1 ghost ring in front of / below it.
3. Make the approaching (left) family visibly heavier than the receding one — double-pass or doubled ring count — instead of a colour swap.
