# LUMINET BLACK HOLE — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/physics/black-hole/luminet` |
| current render | `gallery/physics/black-hole/luminet/promoted/pp_black_hole_luminet_seed42.png` (4-pen flux lines) |
| other renders | promoted: `pp_black_hole_flow_seed42.png`, `pp_black_hole_lines_seed42.png`, `pp_black_hole_scatter_seed42.png`, `pp_black_hole_scatter_hot_seed42.png`, `pp_black_hole_scatter_inferno_seed42.png` · candidates: `pp_black_hole_flow_full_seed42_v1.png`, `…_v2_SMOOTH.png`, `pp_black_hole_poster_seed42_v1.png`, `…_v2_CLEAN.png`, `pp_black_hole_retro80_field_seed42_v1.png`, `pp_black_hole_retro80_tron_seed42_v1.png` |
| source | `promptplot/generative/generators.py::black_hole` (modes `lines` / `dots` / `flow`; `backdrop`, `poster`, `stars`, `planets`, `disk_pens` options produce the poster/retro80 variants) |
| paper · pens | a4 landscape (297×210, 15 mm margins), white · 0 gold = highest-flux band · 1 darkorange = high · 2 crimson = mid · 3 navy = lowest flux and the shadow-edge rings |
| status | PROMOTED tier (no viewer verdict text on file) · 12 renders on disk |

## In one line
The Luminet-1979 black hole drawn as **nested lensed orbits (orbital / nested, one family folded over itself)** — every line is one exact isoradial of the disk seen through the hole's lens, direct image domed over the shadow and ghost image looped beneath, with pen = binned observed flux.

## What is on the sheet
- **Direct image (dominant, u 0.08–0.93, v 0.25–0.63).** ~40 nested isoradial loops forming a wide "hat": pointed tips at u 0.08 (left) and u 0.93 (right) on v≈0.55, rising into a dome that peaks at v 0.25 over the centre. Pens graded by flux: gold and darkorange concentrated in the inner-left loops (u 0.2–0.55), crimson for the outer-left loops and a band through the dome, navy for the outermost right-side loops (u 0.62–0.93) — the left (approaching) half is warm, the right half cold.
- **Shadow (u 0.50, v 0.55).** A bare-paper hole Ø≈0.19 W bounded by a tight bundle of 3–4 navy/crimson rings (the photon-ring edge); above it an open white arch where the inner isoradials lift clear of the shadow (u 0.42–0.64, v 0.38–0.47).
- **Near side.** Below the shadow's equator the direct loops run almost flat and horizontal across the hole's lower half (v 0.62–0.66), in front of it.
- **Ghost image (u 0.50, v 0.62–0.74).** A U-shaped nest of ~15 crimson/gold/navy rings hanging under the shadow, bottoming at v 0.74, overlapping the near-side lines.
- **Densest zone (u 0.42–0.60, v 0.58–0.68).** Where near-side flat lines, ghost rings and the shadow edge overlap: a moiré of orange/crimson that plots as ink-on-ink flood.
- **Seam.** A vertical dotted white gap at u 0.50 through the dome top (the α=0 wrap of every loop).
- **Nothing else.** No type, no furniture; the lower band v 0.75–0.93 and upper band v 0.07–0.24 are empty paper.

### Earlier theses (trials)
- `flow` (promoted): one black pen, isoradials broken into flux-duty dashes (dense short dashes on the left, sparse long dashes on the right), shadow as one clean black circle; ghost ring as dashes below.
- `retro80_field`: horizontal black field lines across the whole drawable area bend around the hole; the disk in magenta/deepskyblue dashes; a cluster of ~25 magenta star crosses at right (u 0.7–0.9, v 0.35–0.5); footer `SCHWARZSCHILD  M 1  I 80` (colons dropped).
- `poster_v1`: 5 pens; lensed horizontal field top half, a perspective fan of lines below that tangles into a crumpled knot under the shadow (u 0.45–0.6, v 0.62–0.68); stars, two hatched planets, four registration crosshairs on the frame midpoints; type `G R A V I T Y / B E N D S / L I G H T` top-left, `M 1 80 / G 6.674E-11 / C 299 792 458` bottom-left, `E V E N T  H O R I Z O N / A C C R E T I O N  D I S K / S P A C E T I M E` bottom-right.
- `poster_v2_CLEAN`: same minus planets and most stars; the knot under the shadow remains.
- `scatter*`: flux-weighted dot clouds (black / hot / inferno palettes) — Luminet's photographic-plate look, 120–157k commands.

## The science it encodes
Docstring (`generators.py::black_hole`): "Luminet-1979 black hole with the EXACT elliptic-integral solver. Ported from 007-eventHorizon (Luminet eq. 13 impact parameters, eq. 19 redshift, Page–Thorne flux): the direct image (n=0) domes over the shadow and the TRUE ghost image (n=1) forms the bright lensed ring below." CLAUDE.md records it verified against bgmeulem/luminet at machine precision. Exact: every loop's shape (impact parameter b(α, r)), the n=1 ghost, the flux used to bin pens (Doppler + gravitational redshift × Page–Thorne). Seeded: inclination 72–85° when not given, ring count ±2. Render check: the warm-left/cold-right split visibly shows beaming; the ghost ring is present. The near-side lines crossing the shadow are physically correct (disk in front of the hole).

## How it got here
All 2026-09-12/13. The pure `lines` plate (1 pen, A4 portrait, small subject) → `flow` (flux as dash duty, 1 pen) → this 4-pen flux-binned `luminet` plate (promoted) → poster/retro80 experiments adding backdrops, stars, type and furniture → `poster_v2_CLEAN` trimming them. Gained along the poster branch: a lensed backdrop that shows spacetime bending, type. Lost: the clean single object; the fan+knot below the shadow is a visible failure in both poster versions. No viewer feedback on file.

## Keep — what works
- The exact family: ~40 loops, tips at u 0.08/0.93, dome at v 0.25 — instantly the Luminet silhouette, with no furniture needed.
- Flux → pen: the warm inner-left vs navy outer-right is beaming made visible without a caption.
- The white arch between the dome and the shadow (u 0.42–0.64, v 0.38–0.47) — the best negative space on the sheet.
- From `flow`: flux as dash duty on one pen — plottable tone with bounded density.

## Weak — what doesn't
- [craft] The overlap zone under the shadow (u 0.42–0.60, v 0.58–0.68) is three families stacked — near-side lines, ghost rings, photon edge — at sub-mm spacing: guaranteed flood and paper wear.
- [craft] The α-seam at u 0.50 leaves a dotted vertical scar through the dome.
- [tension] Subject centred on the sheet, even empty bands above and below — "floating dead-centre".
- [hierarchy] Four pens of roughly equal line weight; at 3 m it is a pale many-coloured hat; the shadow (the subject) is only a thin outline.
- [concept] It is the textbook Luminet figure reproduced faithfully — honest, but a scientific figure by §6; no order beyond the data's own, no twist.
- [depth] Depth comes only from occlusion order of the data; no weight falloff with distance; the far (dome) and near (flat) sides are drawn at the same weight.
- (poster branch) [space] The perspective fan tangles into a knot under the shadow; star crosses and planets are decoration carrying nothing.

## Next versions
- **PLATE BY DUTY** (faithful) — keep the exact family and compose it as Luminet's photographic plate in pen: tone drives dash duty (never spacing), one black + one warm pen, near-side lines drawn heavier than far-side (depth), the ghost ring and near side de-conflicted by occlusion (near side wins, ghost cut where it passes behind), seam closed. Subject scaled so the tips crop the left and right frame edges. Fixes craft and depth while staying the most faithful plate.
- **HAT OF LIGHT** (abstract) — orbital/nested order at full bleed: only every third isoradial, drawn 3× passes on the approaching side and single on the receding, the shadow a solid black disc (the only black mass), the whole figure pushed to v≈0.62 so the dome sits in the sheet's upper half and the lower third is a quiet field. One line of type on the horizon axis.
- **THE BACK IS IN FRONT** (lens) — the twist the Luminet image already contains: you see the far side of the disk arching OVER the hole. Draw the disk twice, as flat concentric rings in true plan view on the left third, and its lensed image on the right two-thirds, the same pens per radius so each ring can be followed from plan to lensed image; the eye discovers the back of the disk climbing over the top.

**If only iterating:**
1. Cut the ghost rings where they pass behind the near-side lines and keep ≥0.8 mm spacing everywhere under the shadow.
2. Close the α=0 seam so no vertical gap crosses the dome at u 0.50.
3. Fill the shadow as one black mass (or bold the photon-ring edge to 3 passes) and scale the figure until the tips touch the side margins.
