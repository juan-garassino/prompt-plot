# CONVOLUTIONS — r01

Recreation of `studio/convolutions/ref/reference.png` (1536×1024) with an explicit
licence to fix the reference's crowding.

- **Piece**: `studio/convolutions/rounds/r01/piece.py`, entry point `convolutions`.
- **Render**: `~/Downloads/pp_convolutions_v1.png`
- **Command**:
  ```
  .venv/bin/python scripts/render_candidate.py studio/convolutions/rounds/r01/piece.py \
    --fn convolutions --seed 7 --colors 4 --paper a4 --orientation landscape \
    --palette black,crimson,dodgerblue,olive --out ~/Downloads/pp_convolutions_v1.png
  ```
- **Pens**: 0 black · 1 red · 2 blue · 3 olive. A4 landscape, cream.

## Plot budget

| | |
|---|---|
| commands | 125,727 |
| pen-down cycles | 5,465 |
| draw | 18.63 m |
| travel | 12.98 m (0.70 × draw) |
| bounds violations | **0** (the one the validator reports is the pipeline's own final `G0 X0 Y0` park move, not artwork) |
| ink bbox | x 13.0…284.3, y 13.0…197.0 — 13 / 12.7 / 13 / 12.7 mm clear on all four sheet edges |

Measured minimum spacing inside each dense line family (interiors only, dots excluded):

| family | chains | min gap | median nearest-neighbour |
|---|---|---|---|
| blob X rings | 11 | 0.92 mm | 0.92 mm |
| blob Y rings | 11 | 0.95 mm | 0.96 mm |
| cone teardrop nest | 10 | 0.86 mm | 0.86 mm |
| feature maps 1/2/3 | 10/10/7 | 0.92 / 1.18 / 0.95 mm | 1.24 / 1.34 / 1.16 mm |

All ≥ 0.86 mm, i.e. ≥ 1.7 × the 0.5 mm pen tip.

---

## THE LAYOUT CHANGES

I measured the reference off the raster rather than eyeballing it — long-run scans of
the strong-black mask for every tile border, colour masks for the blobs, row-band
profiles for the type. Those numbers are recorded at the top of `piece.py`. Positions
below are normalised `(u, v)`, u = 0 left…1 right, v = 0 top…1 bottom, mapped onto a
composition frame inset 13 mm inside the sheet.

### 1. Nothing is clipped any more

The reference's kernel bank runs off the bottom (its bottom row reaches y = 1008–1016 px
of 1024, and there is a further row of marks and a caption cut off entirely below it).
Its bottom margin is **zero** while its left margin is 31 px.

Everything now lives inside a frame with **13 mm on all four edges**. The price is that
the kernel bank is 62 × 54 mm instead of the reference's 67 × 62 mm equivalent. I took
that over letting it bleed.

### 2. The dashed ellipses are routed *behind* the tile strip

In the reference the five big dashed ellipses cut straight across all five tiles,
putting noise exactly where the plate's main statement is. They are now clipped out of
three regions:

- the **tile-strip slab** (the strip's bounding box + 2.6 mm) — so they pass behind it
  and do not even show in the gaps;
- the **two display-label boxes** (`K * X`, `σ(·)`) — the reference lets its dashed
  centre spine run straight through the "K";
- **everything below the flow band**, so the new gutter stays empty paper.

What survives is the part that arcs over and under the strip, which is the reading
worth keeping: overlapping receptive fields.

### 3. The connector bundles pass behind each tile — kept deliberately

The sweeping curve families are clipped out of each tile rectangle (+1.1 mm) rather
than off the strip entirely. A curve disappears behind a tile and reappears in the
8 mm gap. This overlap I would defend out loud: it builds depth and it ties the input
to the whole chain instead of to one tile, which is what the reference's long sweeps do.
The curves no longer cross the tile *contents*, which is what made the reference
illegible there.

### 4. The three lower zones get equal gutters and a shared baseline

| | reference (scaled to this sheet) | r01 |
|---|---|---|
| kernel bank → cone gutter | 33 mm | **36.1 mm** |
| cone → feature maps gutter | 17 mm | **36.1 mm** |
| zone bottoms | three different (y = 1008 / 955 / 937 px) | **one baseline, y = 26.8 mm** |
| captions | two baselines; the kernel bank's is cut off | **one baseline, y = 20.3 mm, all three labelled** |

The two gutters are equal **by construction, not by fiddling**: the cone sits on the
sheet centreline and the two outer zones are built from the same `3 × ZONE_CELL_W +
2 × CELL_GAP`, so their widths — and therefore the gutters — are identical whatever
the cell size. Change one number and the symmetry holds.

### 5. A real gutter between the flow band and the lower band

The reference has the blobs ending at v = 0.61 and the kernel bank starting at v = 0.657
— about 1.3 mm of air at this scale, and that sliver is full of dashed arcs and
droplines. r01 reserves **v = 0.538…0.615, 14.2 mm of paper**, and treats it as a zone:
the floating-dot scatter, the dashed ellipses and the furniture are all excluded from
it. Keeping it *empty* is what makes it read as a gutter rather than as more background.

### 6. The five tiles are spaced on a clear rhythm

Tile gap goes from **0.28 × tile width** (5.6 mm at this scale) to **0.43 ×** (8.0 mm).
The strip is centred at u = 0.500, which is the midpoint of the two blobs' inner edges,
so the clearance is **27.7 mm on both sides** (the reference's is 18 mm left, 35 mm right).
That same u = 0.500 carries the dashed spine and the cone apex, so the strip, the spine
and the receptive field share one axis.

### 7. Gaps are a module, not leftovers

- one `CELL_GAP = 3.2 mm` inside **both** the kernel bank and the feature-map strip;
- one `TILE_GAP = 8.0 mm` in the strip;
- one gutter value between the lower zones, equal on both sides;
- three vertical anchors: **u = 0** (title, the three lowercase lines, blob X, the
  `input x` crosshair, the kernel bank), **u = 0.5** (spine, tile strip, cone,
  `receptive field`), **u = 1** (the stride/padding block, blob Y, the feature maps).

### 8. Smaller collisions relieved (the nudge test)

Each of these was a case where moving an element a few millimetres relieved the
crowding and nothing was lost — so it was crowding, not composition:

- **Centre spine through the "K"** → the upper spine now stops at v = 0.232, above the
  label, and resumes below the strip.
- **"X" and "Y" grazing their blobs** → the label slot is now *searched for*
  (`_label_slot` scans the blob's silhouette for the height with the largest gap to the
  box edge and places the label with 3 mm clearance), so a reshaped blob cannot collide
  with its own label.
- **Blob X's top lobe 3.5 mm under "continuous perception"** → blob tops dropped from
  v = 0.145 to v = 0.170, buying 8.7 mm at the cost of 4 mm of blob height.
- **An L-bracket landing on the third feature map and running 1.5 mm off the sheet** →
  moved and shortened.
- **Three floating dots landing in a clump** → the scatter is now dart-thrown with a
  9 mm minimum separation.

Overlaps deliberately **kept**: connectors behind tiles (depth); the two dashed spines
crossing the whole sheet including blob Y (registration lines, and the reference has
them); black dots sitting on the blobs' fingerprint rings (the reference does exactly
this — measured 0.05 mm, and that is the point).

---

## Construction notes

**Contour rings come from conical fields, never Gaussian ones.**

- The **blobs** are filled with the contours of the *distance to their own outline*.
  `|∇d| = 1` everywhere, so a uniform level ladder gives a ring pitch of exactly the
  level step (0.95 mm), tight all the way to the medial axis. A small fbm wobble
  (±0.30 × pitch at a 13 mm scale, gradient ≈ 0.07) keeps the worst case at 0.89 mm.
- The outline is a **trefoil**, `r(θ) = 1 + 0.46 cos(3θ + φ) + …`. That dominant k = 3
  term is the whole trick: a near-convex blob's distance field has one long medial
  ridge and the rings come out as a plain onion, which is what my first two rounds
  produced. Waists deep enough to pinch give a **Y-shaped medial axis**, and the rings
  split into the reference's three fingerprint eyes. `φ₃` places the lobes; for X it is
  −2.356 (peaks at 45 / 165 / 285°, which the box's vertical stretch turns into the
  reference's upper-right, upper-left and long lower lobe).
- **Level ladders on conical fields must be geometric, not uniform.** For
  `F = a·e^(−r/σ)` a uniform *level* step puts the radii at `σ·ln((k+1)/k)` apart —
  0.69σ for the first gap but only `σ/k` near the summit. At 16 uniform levels on a
  σ = 5.4 mm cusp the innermost gap is **0.33 mm** and the eye floods. `_cone_levels()`
  builds `F_k = a·e^(−k·pitch/σ)` instead, which puts the rings exactly `pitch` apart
  everywhere. Used by the tile whorls, the kernel taps and the feature maps.
- Corollary that bit once: **a level ladder is set by the tightest cusp in the field.**
  A σ = 2.1 secondary eye next to a σ = 5.4 primary forced the primary down to 0.37 mm
  to keep the secondary legal; the secondaries are now σ 3.6–4.6. Same reason the
  feature maps' anisotropy was pulled from 0.62/1.5 to 0.85/1.25 — at a 2.4 ratio the
  ladder that kept the tight axis legal left six lonely contours per tile.
- Where the convergence is **geometric rather than a parameter** — two branches of one
  contour running together to nothing just before they merge at a blob waist — the
  house guardrail `enforce_line_spacing(min_dist=0.80)` thins it, wrapped in
  `_guard_spacing()` which re-emits from runs (the raw policy can drop the `G0` that
  positions a stroke, which shows up as a stray point at the machine origin).
- **All tonal fills are `kit.tone_dots()`**, so tone drives the probability a cell is
  inked and density is capped at 1/cell² however dark the tone goes. Nothing in this
  plate can flood.
- The **receptive field** is a dashed **parabola** envelope over a nest of closed
  teardrops, measured off the reference crop: the solid nest reaches ~0.5 of the
  envelope's half-width, the stipple ~0.65, and most of the figure is white paper. Two
  earlier rounds contoured a radial field inside a triangular wedge and both came out
  as a solid black triangle. The teardrops are drawn explicitly — `hw(u) ∝ u^0.85
  (1−u)^0.5`, zero at the crown, zero at the mouth, widest 63 % down — with the three
  growth rates set so the pitch is ≥ 1.1 mm at the crown (the only place a nested
  family can crowd), 1.9 mm across and 5.1 mm at the mouth.

## Font gaps (for central fixing — not worked around locally)

- **`σ` (U+03C3) and `·` (U+00B7) are missing** from the shared 78-glyph font, so the
  `σ(·)` activation label degrades to `o(.)`. I drew the sigma as **one stroked mark**
  (`_sigma()`, same 4×6 metric) and the middle dot as a plotted dot — a mark, not a
  local glyph table. Please add both centrally and I will delete `_sigma`.
- **`∗` (U+2217, asterisk operator) is missing**; `K * X` uses the ASCII `*`, which is
  close enough here but is the wrong mark for a convolution.
- Lowercase renders correctly (78 glyphs, no forced caps) — `_stroke_text(...,
  proportional=True)` with uniform tracking to hit a measured target width, so cap
  heights stay at the measured value instead of being scaled up. Measured sizes used:
  title caps 3.0 mm, the three lowercase lines 2.5 mm, the stride/padding block 1.85 mm,
  `X` 3.95 mm, `Y` 4.65 mm, display labels 3.95 mm, captions 2.5 mm.

## Three things furthest from the reference

1. **Blob proportion and ring count.** The reference's blob X is 0.75 wide/tall and
   holds ~15 rings with a fine grey tonal wash between them. Mine is 0.82 and holds
   11–12 at the 0.95 mm pitch. This is a direct cost of the brief: shortening the flow
   band to buy the 14.2 mm gutter took 4–5 mm off the blob, and `rings × pitch ≈ σ`
   means the only way to buy rings back at a fixed pitch floor is to make the blob
   physically bigger. The reference's grey is also finer than a 0.5 mm pen can hold.
2. **Serif / italic type.** The reference sets its lowercase in a serif-ish face with
   real italic; the shared single-stroke font is a geometric sans. **Known permanent
   gap — recorded, not chased.**
3. **The five tile interiors.** The reference's whorls are denser and finer, carry two
   or three clearly separate secondary eyes each, and their radial rays break out
   through the tile border into the surrounding field. Mine are cleaner, have one or
   two secondaries, and the rays stop at the border — partly a deliberate consequence
   of treating each tile as a protected rectangle (fix #2), partly a pen-tip limit.

## Rounds

1. First full layout. `_dash` stalled on a float-modulo phase walk (the step collapsed
   to ~1e-16 and never terminated); rewritten as an explicit on/off state machine.
2. Gaps turned into a module; ellipses routed off the strip; sigma mark added; dots
   made solid (the spiral was too loose and every dot read as a little target).
3. Blobs via cone metaballs — collapsed to a convex egg, reverted. Cone contoured
   inside a triangular wedge — came out a solid black triangle.
4. Trefoil blobs (tested four harmonic sets side by side before committing);
   cone rebuilt from measurements off the reference crop as parabola + teardrops.
5. Teardrops fixed to close at the mouth; blob boxes dropped to clear the title block;
   two long dashed over-arcs added.
6. Geometric level ladders everywhere; spacing measured and verified.
