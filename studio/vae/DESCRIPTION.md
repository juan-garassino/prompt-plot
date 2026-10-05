# LATENT BOTTLENECK — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/vae` |
| current render | `gallery/studio/vae/current/pp_vae_v1.png` |
| source | `studio/vae/rounds/r01/piece.py::studio_vae` |
| paper · pens | a4 portrait (210×297 mm), white preview · as rendered: 2 forestgreen = prior energy bowl + most type + correspondence lines + ring labels · 0 black = the posterior σ-ellipses, `SIGMA / ZERO BITS` label, the master target's dotted rings · 1 crimson = reparameterized samples (short darts) + the `z = μ + σ·ε` line. (The docstring's colour law is black = prior surface/type, red = samples, blue = σ-ellipses; the preview shows the default palette.) |
| status | unreviewed (no feedback on file) · 1 render on disk |

## In one line
A VAE's converged posteriors drawn as a **nested / packed** order on the prior's exact energy bowl — each posterior an ellipse stamped with the one ε-constellation that trained it (z = μ + σ·ε), the constellation's master copy on a flat N(0,I) target below — meant to show the collapsed zero-bit posterior as the hero and the unvisited prior wedge as bare paper.

## Lede
A variational autoencoder's learned guesses, drawn as small ellipses inside the **bowl** that pulls them all toward its centre.

## On the sheet
A green wireframe bowl fills most of the sheet. Inside it, a crescent of black ellipses, each with a small green plus at its centre, is speckled with short crimson darts. Bottom left, three dotted black rings hold a star-like scatter of crimson darts, the master noise set. Two dashed green lines climb from it to the bowl. The title sits top left; a rate readout runs along the bottom.

## The science
A variational autoencoder squeezes each example through a narrow channel and must describe it as a small cloud of likely positions. The bowl is the model's idea of where positions should sit; climbing its walls costs more. Each ellipse is one example's cloud, placed by the real training objective, and the one that collapsed to carrying no information at all is the hero. The numbers are computed; that claim is stated in text, not visible.

## What is on the sheet
- **The prior bowl (dominant mass).** A green wireframe paraboloid seen from above-front, ~0.75 of sheet width, spanning u≈0.17–0.92, v≈0.30–0.57: 22 concentric rings × ~108 radials, the far rim a wide open ellipse (top at v≈0.30), the near side a deep curved wall dropping to the floor at u≈0.54, v≈0.57. The rim band's radials read as a picket fence; rings compress toward the front wall.
- **The posteriors.** ~13 black ellipse outlines of broadly similar size (~0.10–0.20 of width) overlapping in a crescent inside the bowl, u≈0.26–0.81, v≈0.39–0.54: a clockwise sweep from lower-left (tilted, elongated, u≈0.26–0.45) through upright ellipses at the top centre (u≈0.45–0.68, v≈0.39–0.47) to very flat slivers bunched at the lower right (u≈0.62–0.80, v≈0.49–0.54). Each carries a small green `+` at its mean. Crimson darts (~0.5 mm) are scattered through the ellipses — at sheet scale a light red speckle.
- **Ring labels.** Small green `2.0 NAT` and `1.05 NAT` set along bowl rings at u≈0.23–0.35, v≈0.43–0.48, broken by ellipses crossing them.
- **Hero label.** `SIGMA  0.46` / `ZERO  BITS` (black, u≈0.73–0.91, v≈0.48–0.49) at the right lip; its text runs straight over the bowl wall and ellipse slivers, with a dashed leader underneath.
- **Correspondence.** Two long green dashed lines climb from the master target at lower-left (u≈0.18–0.26, v≈0.79–0.81) to the right lip of the bowl (u≈0.76–0.81, v≈0.49–0.50), the one visible diagonal on the sheet.
- **Master constellation (second mass).** At u≈0.09–0.27, v≈0.78–0.91: three concentric black dotted circles (the N(0,I) target) around a green `+` (u≈0.18, v≈0.84), holding ~44 crimson darts in a star-like scatter. `N  0  I` above it (u≈0.09–0.18, v≈0.75). `ONE NOISE SET` / `COPIED EVERYWHERE` under it (u≈0.09–0.25, v≈0.91–0.93).
- **Title block.** `LATENT` / `BOTTLENECK` (giant thin spaced caps, u≈0.07–0.49, v≈0.05–0.09), `THE CHANNEL IS AS WIDE AS THE NOISE ALLOWS` (green, u≈0.07–0.70, v≈0.115), crimson `Z  MU PLUS SIGMA TIMES EPSILON` (u≈0.07–0.51, v≈0.13; the `=` does not render). Right, floating: `PRIOR MASS` / `NO POSTERIOR` (u≈0.59–0.72, v≈0.175–0.19), pointing at nothing visible.
- **Footer.** `RATE  2.58 NATS PER SAMPLE` (u≈0.07–0.46, v≈0.95); `GAMMA  0.21` (u≈0.79–0.94, v≈0.95). Three-pen swatch stack at u≈0.92, v≈0.06–0.09.
- **Quiet zones.** v≈0.20–0.29 across the top; a large empty lower-right field u≈0.30–0.92, v≈0.58–0.93 crossed only by the two dashed lines.

## The science it encodes
From the module docstring of `studio/vae/rounds/r01/piece.py`: a fixed saturating decoder g(z)=M·tanh(z) (R²→R²), 13 data points on an open arc (span 236°), free diagonal-Gaussian posteriors optimised by analytic gradient descent (900 steps, lr 0.055) on the exact reparameterised ELBO with one fixed set of 44 ε samples, γ=0.21. The prior is drawn as −log p(z)=½‖z‖², rings are iso-KL contours in nats. Where the decoder saturates, dF/dσ → σ − 1/σ so σ → 1 and that posterior carries zero bits — "the largest mass on the sheet, the hero". The open arc leaves a wedge of prior no posterior visits — "blank paper as the hole". Footer reports rate 2.58 nats/sample.

Not visible on the render: the hero. The label says `SIGMA 0.46`, not ≈1, and it sits on the flattest slivers, not on a dominant ellipse; no single posterior is visibly larger than the rest. The prior-hole wedge is also not identifiable — the ellipses crowd the bowl in a crescent and the open floor at the front reads as the bowl's own interior. `PRIOR MASS / NO POSTERIOR` floats above the rim instead of labelling a gap. The brief (`studio/nets/vae.md`) asked for encoder/decoder funnels with a latent point-cloud core; this round replaced it with the ELBO solution on the prior bowl.

## How it got here
Single render (v1, round r01); no trials on disk and no feedback from Juan.

## Keep — what works
- The prior as a literal energy bowl with the posteriors lying in it — the one image where "prior" and "posterior" share a surface.
- One ε-constellation stamped into every posterior with a master copy on a flat target and dashed correspondence lines — `ONE NOISE SET / COPIED EVERYWHERE` is a genuinely good idea, legible in the lower-left.
- The crescent sweep of ellipses from tilted/elongated to upright to flat slivers — a real rotation/scale progression across the arc.
- Tagline `THE CHANNEL IS AS WIDE AS THE NOISE ALLOWS`.
- The long dashed diagonal from lower-left target to bowl lip — it ties two masses across the sheet.

## Weak — what doesn't
- [concept] No hero: the collapsed σ→1 posterior is not the largest mass, and the label reads `SIGMA 0.46`, contradicting the docstring's claim.
- [concept] The prior hole (unvisited wedge) is not visible; `PRIOR MASS / NO POSTERIOR` (u≈0.59–0.72, v≈0.18) labels empty sky.
- [craft] `SIGMA 0.46 / ZERO BITS` is written over the bowl wall and ellipse slivers; ring labels `2.0 NAT` / `1.05 NAT` are broken by ellipses; the formula loses `=`.
- [craft] The right-front slivers (u≈0.62–0.80, v≈0.49–0.54) stack into a near-solid black wedge; the green bowl's rim radials form a picket fence.
- [hierarchy] Bowl mesh (green) out-weighs the posteriors (the subject); darts at ~0.5 mm vanish.
- [space] The lower-right field (u≈0.30–0.92, v≈0.58–0.93) is a large unshaped void; the bowl sits centred with a symmetric rim.
- [grid] `PRIOR MASS`, `GAMMA 0.21`, the swatch and `N 0 I` float on unrelated lines.
- [depth] The bowl has projected depth, but ellipses are drawn flat on top without foreshortening onto the surface or occlusion by the front wall.

## Next versions
1. **hero-and-hole** (mechanism) — Tune the arc/decoder so the saturated posterior truly converges to σ≈1 and draw it as the one big ellipse (≥3× the others' area) resting on the bowl, darts densest there; carve the unvisited prior wedge as a sector of bowl with its mesh removed (bare paper cut into the surface) and put `PRIOR MASS / NO POSTERIOR` inside it. Both claims become visible; hierarchy gets its 3:1.
2. **constellation-packing** (abstract) — Transpose to PACKED: drop the bowl; the whole sheet is the flat N(0,I) disc (1σ, 2σ, 3σ dotted rings at full width) packed with the 13 posterior ellipses as stamped copies of the ε-constellation, sizes from σ, the gap sector left as blank paper, one huge σ≈1 copy filling the prior like a watermark. Flat by declaration (Swiss). Everything is the one noise set copied.
3. **funnel-bottleneck** (faithful) — Return to the brief: encoder and decoder funnels (ruled hyperboloid) meeting at a waist, the waist being the latent disc with the posterior ellipses and the ε-darts shooting through it in red; the correspondence master target sits beside the waist.

**If only iterating:**
- Make the zero-bit posterior the largest ellipse on the sheet (target σ→1) and move its label onto a halo-cleared patch beside it; test: at 3 m one ellipse dominates and its label is clear of all strokes.
- Remove the bowl mesh inside the unvisited wedge so it reads as bare paper, and relocate `PRIOR MASS / NO POSTERIOR` into that wedge; test: a viewer can point to the hole.
- Drop mesh density to ≤16 rings with no rim picket-fence and make the darts 1 mm dots; spend the lower-right void by moving the master target to u≈0.60–0.85, v≈0.70–0.88 so the correspondence lines become a short steep diagonal.
