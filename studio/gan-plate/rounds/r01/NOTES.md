# GAN plate — round 1 (r01)

Exact recreation of `studio/gan-plate/ref/reference.png`. Reproduction, not design.

```
.venv/bin/python scripts/render_candidate.py studio/gan-plate/rounds/r01/piece.py \
  --fn gan_plate --seed 7 --colors 5 --paper a4 --orientation landscape \
  --palette crimson,dodgerblue,goldenrod,olive,black \
  --out gallery/studio/gan_plate/current/pp_gan_plate_v1.png
```

Render: `gallery/studio/gan_plate/current/pp_gan_plate_v1.png` · GCode: `gallery/studio/gan_plate/trials/pp_gan_plate_v1.gcode`

## Numbers

| | |
|---|---|
| commands | 48 933 |
| draw | 7 843 mm |
| travel | 10 454 mm (post-optimise) |
| pen cycles (M3) | 5 022 |
| per pen (M3) | red 3 347 · blue 3 631 · yellow 3 741 · olive 1 798 · black 16 325 |
| ink bbox | x 13.2–282.6 mm, y 16.6–195.7 mm inside the 10–287 / 10–200 drawable |

## Method: measure, never judge

`Ref` is an affine map from reference pixels onto the drawable area
(`x = 10 + px·0.18344`, `y = 200 − py·0.18252`). The reference raster is
1510×1041 (aspect 1.4505) and the A4-landscape drawable is 277×190 mm
(aspect 1.4579) — 0.5 % apart, so the raster *is* the drawable area and every
literal in the piece is a pixel measured with a probe:

* knot centres from a densest-ink window — generator row all at y = 373,
  x = 284/374/461/545/628; discriminator row at y ≈ 397, x = 957/1041/1131/1209/1305;
  x̂ at (737, 388); real data at (266, 594);
* kernel tiles: left edges 177/281/385/490/594, width 73, top row y 748–822,
  bottom row y 831–902, pitch 104.2 — all read off horizontal/vertical run scans;
* dashed arcs fitted as circles by least squares (e.g. upper-left: centre
  (404, 147), r = 110, 148°→0°);
* every label placed by its measured ink box, and **sized** by it. `_fit_height`
  solves the cap height that makes the string exactly as wide as the reference
  ink, so a label cannot be 30 % oversize while "looking right". Text blocks
  take one height from their widest line.

Verification was a rasteriser that replays the emitted GCode back into
reference-pixel space, so every comparison was a stack, not an impression.

## The lobed blob (the whole plate is twelve of these)

`_blob(...)`. `u = |P−C| / R(θ)` is the normalised radius, so every iso-line of
`u` is a scaled copy of the outline — rings follow the boundary by construction.

1. **Conical cusp, not Gaussian.** Levels are the evenly-spaced iso-values of
   `exp(−u/σ)`. Gaps in `u` shrink toward the centre, so rings tighten into the
   knot and open toward the rim. A Gaussian spreads its rings at the summit,
   which is precisely where the knot has to be dense.
2. **Spacing gated PERPENDICULAR to the contour, not radially.** This was the
   single biggest correctness fix. Stepping `u` by `du` moves a point
   `du·|V|` along the radius, but two contours are only `du·|V·n̂|` apart
   measured across them. Wherever the boundary runs steeply — every neck — the
   radius is far from the normal and the true gap is a fraction of the radial
   one. Gating radially looked fine and flooded the necks: near-parallel ink
   closer than 0.8 mm went from **37 % → 19 %** of all ink the moment the gate
   switched to `perp[i]`. Same rule as `kit.even_contour_levels` (choose by
   gradient, not by value), written out for an analytic contour family.
3. **Per-angle, not per-ring.** Each angle keeps its own last-drawn level, so a
   ring survives on the fat lobes and stops existing across the necks. Gating a
   whole ring on the narrowest neck deleted every ring everywhere — round 1 was
   twelve empty outlines.
4. **Beads cut by ANGLE.** A fixed angular period with a golden-ratio phase
   drift per ring gives the reference's radial/spiral weave and shortens beads
   toward the centre. A low-order drift (0.41) resonates every ~2.4 rings and
   prints visible radial stripes.
5. **The core is a polar-LOD fan, not more rings.** Level L has `base·2^L`
   spokes starting at `pitch·n/2π` — exactly the radius where that many spokes
   are still `pitch` apart — so the fan darkens toward the cusp without ever
   crowding, and the finest levels fall off the end of the blob by themselves.
   Each spoke runs out to wherever the rings actually stopped at *that* angle,
   so the fan fills the necks the rings could not reach. Spokes are radial and
   rings tangential: the two never crowd each other.
6. **Lobes never point straight up.** Under the 2:1 vertical stretch a lobe on
   the vertical axis is drawn into a blade — rounds 1–3 produced exactly that.
   The reference uses two mirrored arrangements, lobes at 0/120/240 or
   60/180/300, so one lobe always runs horizontally and stays compact.

## Spacing and overlap

* `MIN_SEP = 0.8 mm` is the floor for every ring, hatch and field.
* `TIP = 0.5 mm` is used **only** for deliberately solid marks — the twelve
  knots, the kernel weight dots, the flow nodes. One pass, no overlap; it is the
  only place on the plate where lines sit closer than `MIN_SEP`.
* **The row pitch is the blob width.** Measured on the raster, consecutive
  stages are tangent (blob 1 ends at x = 331, blob 2 begins at x = 330). Blobs
  are sized by the half-extent their outline actually reaches — not by a nominal
  radius, since the lobe harmonic swings the radius ±45 % — and capped at
  half-pitch plus a constant `INTERLOCK_PX = 8` (1.4 mm). One rhythm everywhere:
  the stages touch at their single widest point and nowhere else. No stage
  crowds its neighbour, and there is no leftover slack either.
* Flow curves are emitted **before** the blobs so they read as passing behind
  the stages, as they do on the reference.
* The real-data bundle's control points are placed low and far right on purpose:
  a symmetric bow cut straight through x̂ and through the "generated sample"
  caption. It now clears the caption by a full line.
* Remaining sub-0.35 mm parallel ink is concentrated at (a) the latent stipple,
  where the "violations" are dot outlines, not parallel lines, and (b) the flow
  bundles converging on a node — which is the drawing's subject and is equally
  dense on the reference.

## Three things still furthest from the reference

1. **Interior ring density in the necks.** The reference is a raster and runs
   its contours at 0.55–1.1 mm (measured: 3–6 px). At a hard 0.8 mm perpendicular
   floor the necks legitimately cannot hold as many rings, so mine reads with a
   denser outer band and a lighter middle where the reference is uniformly dark.
   This is a physical limit of the pen, not a bug — loosening it would flood.
2. **Serif/italic type.** `z ~ p(z)`, `x ~ p_data(x)`, `x̂`, `D(x̂)`, `L_D`, and
   the italic `G`/`D` after the stage headings are set in the shared single-
   stroke sans. Known permanent gap; recorded, not chased. Hats and subscripts
   are layout (same glyph, smaller, offset), and the multiplication sign in
   "3 × 3" is drawn as two strokes because the font has none.
3. **Flow-curve character.** The reference's curves are dash-**dot** (long dash,
   gap, dot) and cross each other more freely inside the bundles; mine are plain
   dashes on smooth béziers, so the inter-stage bundles read tidier and slightly
   sparser than the reference's tangle.

## Notes for the caller

* Nothing under `promptplot/` was modified. The piece imports only from
  `promptplot.generative.kit` and `promptplot.models`.
* `_fit_height` measures glyph ink at runtime rather than assuming side
  bearings, so the plate is immune to the shared font's bearing constants
  changing underneath it.
