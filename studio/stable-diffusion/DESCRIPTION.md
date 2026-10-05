# STABLE DIFFUSION AS TOPOGRAPHY / TWICE HERE — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/stable_diffusion` |
| current render | `gallery/studio/stable_diffusion/current/pp_stable_diffusion_faithful_v1.png` (STABLE DIFFUSION AS TOPOGRAPHY — reference recreation) |
| | `gallery/studio/stable_diffusion/current/pp_stable_diffusion_abstract_v1.png` (TWICE HERE — nested De Stijl subdivision) |
| source | faithful: `studio/stable-diffusion/rounds/r01/piece.py::stable_diffusion` · abstract: `studio/stable-diffusion/rounds/r03/piece.py::stable_diffusion` · numbers engine (no render): `studio/stable-diffusion/rounds/r02/mechanism.py` |
| reference | `studio/stable-diffusion/ref/reference.png` (1672×941) |
| paper · pens | faithful: custom 420 × 240 mm landscape, cream · 0 black = horns, bowtie ε_θ, type, furniture · 1 crimson = pixel space x, x̃ · 2 goldenrod = latent z, forward row, sampling loop · 3 dodgerblue = conditioning y, τ, c. abstract: custom **240 × 420 mm portrait**, cream · 0 black = x (subdivision as it went in), type · 1 crimson = x̃ (decoded, displaced) · 2 goldenrod = the latent room / fog / loop · 3 dodgerblue = the condition comb |
| status | unreviewed (no FEEDBACK.md) · 2 renders on disk |

## In one line
Latent diffusion drawn two ways: the faithful plate keeps the reference's **left-to-right dataflow of contour nests** (image x → encoder horn → small latent z₀ → noising row → bowtie denoiser with a sampling loop → decoder horn → x̃), while TWICE HERE transposes it to a **nested orthogonal subdivision** — a De Stijl field of black rules redrawn at 1/8 inside one of its own blocks, where area is dimensionality, pen passes are visits, and crimson rules are the lossy round trip.

## Lede
Latent diffusion drawn two ways: as a **flow of contour landscapes** from image to latent and back, and as a subdivision nested inside itself at one eighth.

## On the sheet
The landscape plate runs left to right: crimson contour nests for the image and its decoded copy, goldenrod nests for the latent and its noising row, a central black bowtie for the denoiser, and blue nests for the text condition. The portrait plate is a field of black rules with crimson twins, a small gold-filled room with a blue comb on its edge, and giant black lettering.

## The science
Both plates encode the same pipeline: an image is compressed eight times per side into a small latent, noised and denoised there under a text condition, then decoded with some loss. The second plate turns that into numbers: area as dimensionality, pen passes as denoising visits, crimson displacement as the round-trip error. No neural network is drawn; some printed ratios do not match the stated targets.

## What is on the sheet

### faithful v1 — STABLE DIFFUSION AS TOPOGRAPHY (landscape)
- **Title** `STABLE DIFFUSION` / `AS TOPOGRAPHY` in stroke caps at u 0.04–0.19, v 0.09–0.12, rule under it.
- **Encoder (upper-left)**: `x` — a crimson four-lobed contour nest (~12 rings) at u 0.045–0.16, v 0.22–0.40, crimson dashed arrowheads on its right; → a black **horn** `E` (a fan of ~30 straight lines converging to a point, u 0.16–0.26, v 0.22–0.40) → `z₀`, a smaller goldenrod four-lobed nest (u 0.28–0.34, v 0.30–0.38).
- **Forward row (top, v 0.25–0.42)**: five goldenrod nests at u≈0.31, 0.40, 0.49, 0.58, 0.66 that progressively wobble, break and fill with black/gold dots, joined by `•••`, ending in `z_T`, a black isotropic dot cloud (u 0.70–0.82). Dotted arcs link consecutive states above; `q(z_t | z_{t−1})` (u 0.47–0.52, v 0.18) over a dotted → arrow (u 0.40–0.64, v 0.19); labels `z_t` (u≈0.51, v 0.38) and `z_T` (u≈0.76, v 0.40). Dotted droplines with open arrowheads fall from three states into the bowtie; a heavy double arrow falls from z_t into the waist.
- **Denoiser (centre, dominant, u 0.36–0.64, v 0.43–0.68)**: a black horizontal **bowtie** of ~20 dense concentric contours — two wide wings with small inner eyes, a pinched waist at u≈0.50 holding a small nest; label `Cθ` (ε rendered as C) at u≈0.52, v≈0.47. `t` with a dot and solid arrow enters the left tip (u 0.25–0.36, v 0.57).
- **Sampling loop**: three goldenrod arrowed arcs drawn **across the lower half of the bowtie's contours** (u 0.38–0.62, v 0.52–0.64), plus a gold zig-zag from a gold dot below the waist (u 0.50, v 0.72) up to the right wing; `••• z_{t−1} •••` at u 0.45–0.55, v 0.80.
- **Conditioning (lower-left)**: `y` — a blue three-lobed nest (u 0.04–0.16, v 0.65–0.82) with blue dashed arrowheads → black horn `τ` (u 0.16–0.26) → `c`, a small blue nest (u≈0.31, v 0.74) → a tight bundle of ~8 blue dashed curves rising steeply into the bowtie's lower-left flank (u 0.35–0.37, v 0.58–0.72).
- **Decoder (right)**: a gold curve from under the bowtie (u 0.60–0.70, v 0.72–0.77) rises to `z₀`, goldenrod nest (u≈0.74, v 0.57) → black horn `D` (u 0.77–0.83) with crimson dashed arrowheads → `x̃`, a crimson four-lobed nest rotated relative to x (u 0.84–0.955, v 0.50–0.67), label `x̃` at u≈0.97.
- **Corners**: `N O I S E` / `CONDITION` / `DENOISE` / `GENERATE` (u 0.04–0.09, v 0.86–0.93); `I M A G E S` / `THROUGH` / `L A T E N T` / `LANDSCAPES` (u 0.88–0.94, v 0.86–0.93); ~8 plus marks, loose dots and short dashed ticks.

### abstract v1 — TWICE HERE (portrait)
- **Header**: a crimson rule across the top (v≈0.11, u 0.04–0.96); `L A T E N T   D I F F U S I O N` spaced caps (u 0.07–0.49, v≈0.14); two lines `A SUBDIVISION NESTED INSIDE ITSELF AT ONE EIGHTH` / `THE COMPOSITION IS NEVER MADE IN THE BIG PICTURE` (v 0.15–0.17), the second sitting on the field's top black rule.
- **The field (u 0.04–0.96, v 0.16–0.98)**: a Mondrian-style subdivision in **black hairline rules** — a full-width top rule (v≈0.157); verticals at u≈0.54 (full height), u≈0.78 (v 0.16–0.69), u≈0.25 (v 0.54–0.98), u≈0.69 (v 0.69–0.98); horizontals at v≈0.39 (right), v≈0.54 (left), v≈0.69 (right), v≈0.79 (lower-left block). Each black rule has a **crimson twin** displaced by 1–22 mm (e.g. verticals at u≈0.56, 0.825, 0.26, 0.69; horizontals at v≈0.33, 0.47, 0.70, 0.84). No blocks are filled; the planes are empty cream paper.
- **`TWICE` / `HERE`** — giant black stroke type, u 0.075–0.63, v 0.36–0.52; `TWICE` runs across the u≈0.54 black and u≈0.56 crimson verticals, and the crimson horizontal at v≈0.47 cuts through `HERE` at mid-height.
- **The room (u 0.575–0.69, v 0.55–0.67, ≈27 × 50 mm, ≈0.11 sheet width)**: a goldenrod-outlined rectangle — the ring — containing the same subdivision at 1/8 in black and gold rules, every cell packed with gold dotted/dashed fill (the fog); a comb of 9 short blue ticks stands on its top edge and 7 blue ticks touch its right edge. Beside it: `FIFTY` / `TIMES` / `HERE` (u 0.72–0.76, v 0.63–0.67), and a blue line `c TOUCHES THE RING. NEVER THE…` (u 0.72–0.96, v≈0.58) that runs out through the right frame into a blue scribble.
- **Data column (lower-left block, u 0.08–0.44, v 0.56–0.76)**: `PIXEL SPACE  512 × 512 × 3 = 786432 DIM` / `LATENT SPACE  64 × 64 × 4 = 16384 DIM` / `f = 8   AREA 64 : 1   DIM 48 : 1` / `VISITS  PIXEL 2  LATENT 50   25 : 1` / `INK  FIELD 2.98 M   ROOM 1.10 M` / `MEASURED 2.72 : 1   WANTED 1.92 : 1` / `DENSITY  0.034  0.80 MM/MM2` / `23 : 1` / `SCHEDULE  COSINE s 0.008   T 1000   50 STEPS` / `LATENT CELL 3.44 MM OUT   0.43 MM IN` / `ROUND TRIP  RMS 15.5 MM OUT   1.93 MM IN` / `LOST BELOW 3.44 MM  -  NO RED TWIN RETURNS`; then a four-swatch legend `x  THE SUBDIVISION AS IT WENT IN` / `x~  DECODED BACK OUT - DISPLACED` / `z  THE LATENT. ITS FOG. ITS LOOP` / `c  CONDITION - TOUCHES THE RING`. The black and crimson verticals at u≈0.25–0.26 run straight through these lines.
- **Right column texts**: `NO NETWORK IS DRA…` / `THE RING IS THE …` (u 0.79–0.96, v 0.42–0.43) and `THE SAME LOOP RUN OUT HE…` / `50 VISITS TO 786432 NUMB…` / `OF INK AND 2 H 14 M AT F…` / `IN THERE IT IS 1.10 M. T…` / `DRAWS IN 12 MIN.` / `THE PEN IS THE GPU.` (u 0.77–0.96, v 0.71–0.80) — every long line is **cut at the frame** and its overflow is drawn as a solid black scribble beyond u≈0.96; a black tick crosses the `G` of `GPU`.
- **Sub-cell detail ticks**: small clusters of 3–5 short black ticks scattered in the field (e.g. u≈0.5 v 0.16, u≈0.87 v 0.39, u≈0.30 v 0.51, u≈0.38 v 0.76, u≈0.76 v 0.86) — the marks with no red twin.
- Everything else is empty paper: the upper-left panel (u 0.04–0.54, v 0.16–0.35), the tall right panel (u 0.56–0.78, v 0.16–0.55) and the lower blocks are bare.

## The science it encodes
Latent diffusion (Stable Diffusion): encode the image into a small latent (f = 8), run the noising/denoising chain there with a text-conditioned denoiser ε_θ(z_t, t, c), decode back out lossily. The brief's invariants: latent visibly smaller than pixel space; the loop is a loop; conditioning enters the denoiser not the noise; t is a third input; forward follows √ᾱ; x̃ ≈ x but not equal.
- **faithful** (`r01/piece.py` docstring): placement measured off the reference and five crowding fixes (three separated input docks for t / c / loop return, forward-row pitch 0.6× → 1.4× state width, an 11 mm band above the bowtie, ONE sampling circulation with one direction, z_T and recovered z₀ on one vertical axis at u = 0.760). Observed: the loop is drawn over the bowtie's contours rather than around its underside; z_T is at u≈0.76 but the recovered z₀ at u≈0.74 — close to the stated shared axis.
- **abstract** (`r03/piece.py` docstring, "TWICE HERE"): area = dimension (512×512×3 → 64×64×4 is 48 : 1); pen passes = visits (pixel space drawn twice, latent fifty times), so ink(field) : ink(room) is *solved* to 1.92 : 1; crimson displacement = the latent can only place a cut on its 8-pixel grid AND the loop returned a different sample; gold fog = q(z_t | z₀) for all 50 steps; the room's boundary is the loop; blue comb = c, touching the ring only; sub-cell ticks have no red twin; "NO NETWORK IS DRAWN". The twist: a Mondrian — the most composed image the viewer knows — whose composition is never made in the big picture. Observed: the sheet itself prints `MEASURED 2.72 : 1   WANTED 1.92 : 1` (the ink ratio is not held) and `23 : 1` density where the docstring claims 33×; the "fifty inward ticks on the ring spaced by noise level" are not visible — the ring carries only the 16 blue comb ticks.
- **r02 mechanism.py**: a real toy latent-diffusion system in numpy (8×8 images, 3 classes, PCA autoencoder to d = 6, cosine schedule, ridge-regression conditioning over a 36-prompt corpus, analytic latent score with classifier-free guidance, strided ancestral DDPM). No render in the gallery uses it.

## How it got here
Two renders, no trials, no NOTES.md, no feedback. r01 is the faithful recreation (landscape, as the brief specifies); r02 built the numbers engine but produced no gallery render; r03 abandoned the reference for the abstract order and turned the sheet to portrait.

## Keep — what works

### faithful v1
- The **bowtie ε_θ** (u 0.36–0.64, v 0.43–0.68) is the densest, largest mass — a clear dominant with continuous contours and a readable waist.
- **Latent smaller than pixel**: x and x̃ nests (~47 mm) vs z nests (~26 mm) — the brief's key size claim holds.
- **Colour = space**: crimson pixel, gold latent, blue condition, black networks — consistent everywhere.
- **Horns as compression**: straight-line fans narrowing to a point read as "squeeze" without labels.
- **Forward row decay**: nests go from clean to dotted to an isotropic black cloud across u 0.31 → 0.82.
- x̃ is visibly a rotated cousin of x, not a copy.

### abstract v1
- **The order is right and witty**: a Mondrian redrawn at 1/8 inside itself, "the composition is never made in the big picture" — an abstract order with a twist, no network, no arrows.
- **Scale contrast**: a ~226 mm field against a 27 mm room; the room is the only dense ink on the sheet and pulls the eye immediately (u≈0.63, v≈0.61).
- **Black vs crimson twin rules**: the lossy round trip as a displacement you can measure with a ruler.
- **Blue comb touching only the ring**: conditioning stops at the loop's boundary — stated by geometry.
- **Huge quiet planes**: the empty field is the argument (the big picture is only visited twice).
- **`TWICE HERE` / `FIFTY TIMES HERE`** — the headline pair is the whole thesis in four words.

## Weak — what doesn't

### faithful v1
- [concept] It is the reference's dataflow diagram: horns labelled E/τ/D, arrows, droplines, a labelled bowtie — a schematic by § 6.
- [space] The gold sampling loop is drawn **across** the bowtie's lower contours (u 0.38–0.62, v 0.52–0.64) with a zig-zag from a dot below the waist — the loop collides with the network instead of circulating around it, the opposite of the r01 docstring's fix #4.
- [space] The blue conditioning sheaf arrives as a tight tangle of ~8 dashed curves in a 3 mm band (u 0.35–0.37, v 0.58–0.72) — collision, not a sheaf.
- [craft] `ε_θ` renders as `Cθ`; the forward row's late states mix gold and black dots into a muddy grey.
- [grid] Plus marks, dots and dashed ticks float with no shared axes (the furniture checklist).
- [tension] Symmetric left/right horns and nests about a centred bowtie.

### abstract v1
- [craft] Text overflows the frame on the right in three places (`NO NETWORK IS DRA…`, `THE RING IS THE …`, `c TOUCHES THE RING. NEVER THE…`, and four lines of the lower paragraph) — the clipped overflow plots as **solid black/blue scribbles** at u≈0.96–0.98.
- [space] `TWICE` crosses the black and crimson verticals at u≈0.54–0.56; the crimson horizontal at v≈0.47 cuts through `HERE`; the lower-left verticals at u≈0.25–0.26 run through the data column; the subtitle's second line sits on the top rule.
- [concept] The ink ratio the piece claims to solve is printed as failed on the sheet (`MEASURED 2.72 : 1  WANTED 1.92 : 1`).
- [hierarchy] Only one dense element (the room) and it is small; the giant type is the actual dominant mass, so at 3 m the plate reads as a type poster with a gold stamp.
- [concept] The room's gold fog is a uniform dotted fill — the "hard core with a thin halo" cosine marginal is not visible, and the fifty ring ticks are absent.
- [craft] Hairline rules only; De Stijl without any filled plane loses the canon's mass (no primary block anywhere).
- [grid] The data column, the right-hand paragraphs and `FIFTY TIMES HERE` sit on three different left edges.

## Next versions
- **clean-room** (abstract) — Branch r04 from `r03/piece.py`. Keep the order exactly. Budget every text line to its block's width (hard error on overflow, as THE LONG WAY BACK's `col()` does); move `TWICE HERE` into a block it does not cross; fill two field planes with one primary each (crimson and blue, serpentine fill) so De Stijl has mass; enlarge the room to ~0.2 width and draw its fog as the real cosine marginal (dense core, flat halo via `tone_dots`) with 50 ticks on the ring. Fix the ink ratio so the sheet prints `MEASURED = WANTED`. Same thesis, with the craft of the two approved abstract plates.
- **measured-mondrian** (mechanism × abstract) — Drive TWICE HERE with `r02/mechanism.py`: the field's subdivision is the real 8×8 image class structure, the crimson displacement is the actual PCA round-trip residual per cut, the blue comb positions are the conditioning's class logits, and the room's fog is the real latent marginal at each step. Every rule becomes a measured number; the twist survives.
- **latent-pocket** (lens) — Return to landscape 420 × 240 and zoom the faithful's bowtie + loop into the dominant mass (0.6 width), drawn as a single closed gold circulation around (not across) the network, with x and x̃ shrunk to thumbnails at the far edges and the forward row reduced to a single dissolving band above. The latent loop becomes the subject; horns and furniture are cut.
- **If only iterating:** (on the abstract)
  1. Rewrap every right-column line to end at least 5 mm inside the frame (u ≤ 0.94) so no overflow scribbles plot.
  2. Move `TWICE / HERE` so no letter crosses a rule (fit it inside the upper-left block u 0.05–0.52, v 0.18–0.35), and shift the data column right of the u≈0.26 verticals.
  3. Put 50 goldenrod inward ticks on the room's ring, spaced by the cosine schedule, and double the room to ~55 × 100 mm.
