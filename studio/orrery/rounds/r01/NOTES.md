# ORRERY / ATTENTION — r01

Exact-recreation round. `piece.py::orrery_attention`. Reference:
`studio/orrery/ref/reference.png` (1122 × 1402 px).

Render:

```
.venv/bin/python scripts/render_candidate.py studio/orrery/rounds/r01/piece.py \
  --fn orrery_attention --seed 7 --colors 5 --paper a4 --orientation portrait \
  --palette crimson,dodgerblue,goldenrod,forestgreen,black \
  --out ~/Downloads/pp_orrery_v6.png
```

Plot cost: **21 425 commands · draw 7 683.7 mm · travel 7 449.5 mm · 1 887 pen
cycles.** The travel is almost all dash gaps — this plate is ~1 200 dotted
segments (the big enclosing circle alone is ~240) and each dot is its own pen
cycle. Non-dotted work is ~700 strokes. Rounds 1→2 cut it from 34 275 by
replacing spiral node fills with serpentine fills and dropping ring resolution.

## Method

Everything is authored in **reference-pixel space** (x right, y down, origin
top-left of the bitmap) and mapped once by `_Map`: aspect-preserving, fitted to
the drawable width, centred vertically. 1 ref px = 0.169 mm on A4. Every
coordinate below was measured off the bitmap, not invented — hub centres and
satellite dots by colour-masked connected components after a 1-px erosion, orbit
radii by radial ray-scans through each hub, the enclosing circle by an
outlier-rejecting least-squares circle fit (centre 0.513 W, 0.493 H, R 0.450 W).

## What is matched

- **Plate**: A4 portrait, corner registration (plain `+` top corners,
  cross-in-circle bottom corners, cross-in-diamond bottom centre), title
  `ATTENTION` letter-spaced to the measured 359-px span with the rule + open
  circle beneath, the big dotted enclosing circle, two medium dotted orbits and
  three dotted network arcs, one long dash-dot sight line, plate-wide dash-dot
  horizontal axis and fine-dotted vertical centreline.
- **Four systems**, each: filled hub disc (26 px Ø), 4–6 eccentric concentric
  orbits, a faint inner rosette, a vertical axis with terminal dots, a dotted
  outer orbit, and satellite nodes. Measured radii (ref px):
  Q 29/45.5/62/79.5/102 · K 24/43/64/86/108 · V 27/43/58.5/80.5/104 ·
  Z 25/38.5/50/75. Eccentricity drifts outward (up to −6 px) as in the reference.
- **Central system**: 17 orbits from r = 68 to 241 px, seven dotted, ten solid,
  the r = 208 orbit double-passed as the one heavy ring. `Q · K^T` over a rule
  with a midpoint open circle, `SOFTMAX` spaced beneath, the row of nodes where
  the horizontal axis crosses the orbits, and the two half-shaded discs on that
  axis at r = ±236.
- **Bundles**: 5 red Q→centre, 6 blue K→centre, 5 ochre V→centre, 5 green
  centre→Z, each a cubic Bézier fan with the departure headings aimed at the
  measured endpoints, coloured nodes along each arc and a node at each terminus.
  The Z bundle keeps the reference's long parallel "wineglass stem".
- **Furniture**: four six-point engraver's stars on their vertical lines, three
  moon-phase discs (outline + terminator + hatched shadow), the standalone open
  circles east of K and on the top centreline, ten scattered field dots.

## Orbit-node placement

- **Q, K, V, Z** — transcribed. Each satellite's `(radius, angle, diameter)` was
  read off the bitmap (eroded colour masks → blob centroid + bbox), converted to
  polar about the measured hub and hard-coded in the piece. Z's eight nodes sit
  on the r = 75 orbit at exact 45° steps, which is what the reference does.
- **Central system** — *generated, not transcribed*. The reference has ~70 black
  nodes and reading each one was not worth the budget, so they are placed from
  the seeded RNG: for each solid orbit, `k = 2 + round(6·(r−92)/149)` candidates
  at random angles, rejected if within 15 px of an already-placed node, diameter
  drawn from the measured size ladder (3–15 px). That reproduces the reference's
  *statistics* — thinner toward the middle, crowded at the rim, wide size
  variety — but no individual node lands where the reference's does. Five are
  drawn hollow and three short "constellation" links join neighbours, both
  features of the original.

## What I could not match, and why

1. **Typography.** The reference sets a true Didone-ish serif: modulated
   thick/thin `ATTENTION`, an *italic* `Q · K^T`, **lowercase** spaced
   `softmax`, serif `Q`/`K`/`V`/`Z = AV`. The stroke font in `generators.py`
   is monoline, caps-only and has no italic, so the title reads stencil-like,
   `softmax` is set as caps, and the labels lose their serifs. Double-stroking
   for weight was rejected: it would put ink lines 0.25 mm apart, well under the
   0.8 mm floor.
2. **Line-weight tonality.** The reference uses at least four ink weights per
   colour — hairline ghost orbits, mid orbits, one heavy orbit, plus grey
   "atmosphere" around each hub. One pen per colour gives one weight. The only
   weight trick used is a second pass over the identical r = 208 path (same path,
   so no crowding). The central system therefore reads flatter and more uniform
   than the reference's airy grey mesh.
3. **Bundle arcs are approximated.** The reference's connectors look drawn by
   hand — curvature varies subtly along each arc and the five members are not a
   regular family. Mine are a parametric Bézier fan; K is close, Q and V read a
   little more mechanical and their termini on the central orbits are at
   plausible rather than traced positions.
4. **Plate proportion.** The reference bitmap is 4:5; A4 is 1:1.414. Fitting to
   the drawable width (the only aspect-preserving option that uses the full
   sheet) leaves ~20 mm of cream above and below the composition. Stretching to
   fill would turn every circle into an ellipse, so it was not done.
5. **Moon hatching** is at 0.82 mm pitch; the reference's is ~0.4 mm, which no
   pen can hold on an 3 mm disc. The discs read lighter than the original.
6. **Node fills** use a 0.32 mm serpentine pitch — deliberately below the 0.8 mm
   floor, because a 1.5 mm dot cannot read as solid at 0.8 mm. This is the one
   place the piece goes under the floor, and only inside discs ≤ 3 mm.

## Differences a viewer would notice

- The type, immediately: monoline vs engraved serif; `SOFTMAX` in caps.
- The central system is a single ink weight, so it reads as one dense black mass
  rather than the reference's layered grey-to-black depth.
- The central node field is statistically right but positionally different.
- Cream bands top and bottom that the reference does not have.
- The red Q bundle's top arc has less lift than the original's, and the ochre
  V bundle is tidier/more regular than the reference's looser sweep.
- The moon discs are lighter; their hatching is coarser and reads as lines.
- The reference's grey "ghost" arcs around each hub and inside the central
  system are represented by a single faint rosette per system, not a field.
