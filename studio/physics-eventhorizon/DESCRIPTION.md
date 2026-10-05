# EVENT HORIZON (screen renders) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/physics/eventhorizon` |
| current render | `gallery/physics/eventhorizon/promoted/blackhole_lines_i80.png` |
| other renders | `promoted/blackhole_lines_i60.png`, `promoted/blackhole_dots_i80.png`, `promoted/eh_scatter_hot_FIXED2.png`, `promoted/eh_scatter_inferno_FIXED2.png`, `promoted/eh_scatter_white_FIXED2.png` |
| source | `promptplot/generative/generators.py::black_hole` for the `blackhole_*` images (their titles read "PromptPlot black_hole()"); the black-background display script is **none on disk**. The `eh_scatter_*` images come from the sibling project `../007-eventHorizon` (scatter mode, `eventHorizon/visualization/mode_router.py`) — not dug further. |
| paper · pens | not a plotter preview: a raster on black, 1350×623 (≈2.17:1), matplotlib "hot"-style colour map by flux (white → orange → red → black). No pens. |
| status | PROMOTED tier (no viewer verdict text on file) · 6 renders on disk |

## In one line
The Luminet black hole drawn as **nested lensed orbits glowing on black (orbital / nested)** — each line is one exact isoradial whose brightness is its observed flux; the i80 lines render is the current, i60 shows the same disk less edge-on, the dots and scatter renders trade lines for a flux-weighted photographic grain.

## What is on the sheet
### `blackhole_lines_i80` (current)
- **Title (u 0.25–0.75, v 0.04).** White sans-serif: `PromptPlot black_hole()  |  isoradial lines, inclination 80 deg`.
- **Direct image (dominant, u 0.06–0.94, v 0.14–0.75).** ~18 nested isoradials in a wide "hat": pointed tips at u 0.06 / 0.94 on v≈0.58, dome peaking at v 0.14. Brightness is a strong left/right asymmetry: the inner-left loops (u 0.28–0.42) are white-hot, the left outers orange-red, the whole right half fades from red to near-black and the outermost right loops almost vanish into the background.
- **Shadow (u 0.50, v 0.58, Ø≈0.16 W).** Pure black disc, edged by a thin red photon ring; the inner loops arch over it leaving a black gap.
- **Near side + ghost (u 0.38–0.62, v 0.6–0.92).** Flat red near-side lines cross the lower half of the shadow; beneath, a thick red U-shaped ghost ring bottoms at v 0.92, brightest (pink-white) on its right flank (u 0.58–0.61, v 0.6–0.78). The overlap under the shadow is a dense red moiré.
- **Background.** Solid black everywhere else; no frame, no type besides the title.
### `blackhole_lines_i60`
Same family at 60°: loops are nearly closed ellipses (u 0.03–0.47 of its half-sheet), the ghost image a narrow red crescent hugging the shadow's lower edge, white-hot inner loops on the left.
### `blackhole_dots_i80`
Same geometry as flux-weighted dots: a white-hot clot left of the shadow, red grain elsewhere, a thin red arc over the shadow and a bright red near-side band across it.
### `eh_scatter_hot / inferno / white _FIXED2`
Square 1580×1580, subject small in the centre (≈0.4 of the width), dense dot scatter: hot (yellow-white hot spot at left), inferno (purple/orange), white (monochrome) — each with a bright photon arc over the shadow and a dotted ghost below.

## The science it encodes
Same solver as `physics-black-hole-luminet` (`generators.py::black_hole` docstring: exact Luminet eq. 13 impact parameters, eq. 19 redshift, Page–Thorne flux; n=0 direct + n=1 ghost), here at fixed inclinations 80° and 60°. The colour map is the observed flux — the left/right brightness contrast is Doppler beaming plus gravitational redshift, computed, not decorated. The `eh_scatter_*` plates are the eventHorizon project's own renderer (same physics lineage, per the port note). None of these are plotter-ready: luminance on black cannot be drawn by a pen on white paper as-is.

## How it got here
These are reference/validation renders, the "look" the pen plates chase: eventHorizon scatter (FIXED2 = second fix of the scatter mode), then PromptPlot `black_hole()` lines at i60 and i80, then dots at i80. The pen translations of this look live in `physics-black-hole-luminet` (flux-binned pens, flow dashes, scatter). No viewer feedback on file.

## Keep — what works
- Luminance = flux, so beaming is the dominant read: white-hot inner-left loops (u 0.28–0.42) against a right half dissolving into black — the mechanism lands at 3 m with zero text.
- The black shadow as the true void (u 0.50, v 0.58) — the subject is absence.
- Outermost right loops fading until they disappear into the ground: depth and falloff for free.
- The i60 vs i80 pair: inclination as the one variable that changes the ghost from a crescent to a full U.

## Weak — what doesn't
- [craft] Not a plate: raster luminance on black with a matplotlib title; nothing here can be plotted without a translation (line brightness → passes/duty, black ground → paper or dark stock).
- [craft] The overlap under the shadow (u 0.4–0.6, v 0.6–0.72) is a red moiré of near-side + ghost lines — would flood in ink.
- [tension] Subject centred with symmetric margins; the scatter squares shrink it to 0.4 of the frame.
- [hierarchy] The title is the only type and it is a debug label.
- [concept] A faithful rendering of Luminet's figure — honest science, still a figure (§6).

## Next versions
- **DARK STOCK** (faithful) — plot it as it looks: black paper, white + orange + red gel/POSCA pens; flux drives passes (white 3×, orange 2×, red 1×) and dash duty on the receding side so the right half literally fades into the paper; near-side lines occlude the ghost (cut behind), ≥0.8 mm everywhere. The one plate in the collection whose ground is the void.
- **INCLINATION SWEEP** (mechanism) — laminar/stratified order: the same hole at five inclinations (30°→85°) stacked in horizontal bands, each band a thin slice of the image, so reading down the sheet the ghost ring is born out of the shadow's lower edge and grows into the U. Real variable, real data, no axis.
- **SHADOW ONLY** (abstract) — draw nothing but the isoradials' *occlusion*: bare paper everywhere the disk is, ink only where lines pass BEHIND the hole's silhouette (dashed, in navy) — the shadow defined by the lines it swallows.

**If only iterating:**
1. Translate luminance into pen passes/duty (3 flux bands → 3, 2, 1 passes) and remove the matplotlib title.
2. Cut the ghost rings where the near-side lines cross them so the region under the shadow keeps ≥0.8 mm spacing.
3. Scale the figure so the tips crop the left and right frame edges and drop the dome's top to v≈0.2.
