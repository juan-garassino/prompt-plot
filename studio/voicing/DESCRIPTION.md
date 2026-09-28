# VOICING — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/voicing` |
| current render | `gallery/studio/voicing/current/pp_voicing_v7.png` |
| source | `studio/reaction-diffusion/rounds/r02/piece.py::studio_pipe_rank` (round 02 of the REACTION-DIFFUSION family). Brief: `studio/physics/reaction-diffusion.md` (titled "VOICING — THE RANK A REACTION CUTS FOR ITSELF"). The v7 draw length (8,923.8 mm) equals the regression baseline for this function at A4 portrait, seed 7, so the code on disk reproduces the current render. There are no r02 NOTES on disk. The brief cites `rounds/r02/NOTES.md`, but it is missing. |
| paper · pens | A4 portrait (210 × 297, drawable 10–200 × 10–287), white · 0 black = pipes, wrapped pattern, chest, wind, all type · 1 crimson = only "what went in and what was predicted": the germ blocks on the chest and the √D ladders on the pipes |
| status | unreviewed (no feedback) · 8 renders on disk (v1–v7, seed19) |

## In one line
Gray–Scott wavelength selection drawn as a **rank of five flue organ pipes (a stepped skyline / lattice of lengths)**: each pipe's speaking length is eight measured wavelengths of its own solved field wrapped round its body, and the red ladder up its front marks eight predicted wavelengths from λ ∝ √D.

## What is on the sheet
- **The rank (dominant mass).** Five vertical cylinders in one axonometric basis (verticals unforeshortened, ground raked), standing left to right on a sloping chest. Each is a top ellipse, two silhouette verticals and a wrapped pattern.

  | pipe | u | top v | label |
  |---|---|---|---|
  | 1 | ≈ 0.24–0.33 (the thinnest) | ≈ 0.49 | D 0.4 |
  | 2 | ≈ 0.38–0.50 | ≈ 0.35 | G 8 |
  | 3 | ≈ 0.51–0.63 | ≈ 0.35 | D 1.0 |
  | 4 | ≈ 0.65–0.76 | ≈ 0.36 | G 50 |
  | 5 | ≈ 0.78–0.94 (the widest) | ≈ 0.18 | D 2.0 |

  - Pipes 2–4 form a **flat plateau** of equal height. Pipe 1 steps down and pipe 5 towers.
  - Bodies end at v ≈ 0.73.
  - Silhouette edges are drawn as dense beaded strokes (a heavy double edge in the preview).
- **Wrapped pattern.** Black marching-squares isolines of the v-field on each body: labyrinthine worms and closed blobs, not horizontal bands.
  - Pipe 1: fine, tight worms, pitch ≈ 3 mm.
  - Pipes 2–4: medium worms.
  - Pipe 5: fat closed loops ("O" shapes), pitch ≈ 9–10 mm.
  - A few isolines cross over the top ellipse rim (pipe 1, pipe 2).
- **Red ladders.** Eight short crimson arcs (≈ 5–10 mm long, curved to the cylinder) stacked up the centre front of each pipe, evenly spaced. They are spaced ≈ 8 mm on pipe 1 and ≈ 19 mm on pipe 5. The rungs float independently of the black pattern; they do not register with any stripe.
- **Feet.** Under each body a conical foot (trapezoid) with a small rectangular mouth at its top (the languid/mouth) and a toe ellipse at the bottom, at v ≈ 0.73–0.78.
- **Chest.**
  - Three long near-parallel sloping lines across the full width: the back edge from (u 0, v 0.76) to (u 1, v 0.79), the front top edge at v ≈ 0.87–0.90, and the bottom edge at v ≈ 0.93–0.96.
  - Between the back and front edges, the **wind**: a band of broken black noise-isoline scraps (u 0–1, v 0.78–0.84).
  - Below the wind, the **germs**: five crimson rhombi with 2–4 serpentine hatch strokes, one under each pipe at v ≈ 0.85–0.88. The first, third and fifth are equal; G 8 is a tiny diamond; G 50 is a large rhombus (≈ 27 mm across) spilling under pipes 3–4.
- **Nameplates.** A row on the chest front face at v ≈ 0.90 and 0.92: `D 0.4 / 7.5` · `G 8 / 12.2` · `D 1.0 / 12.1` · `G 50 / 12.0` · `D 2.0 / 17.4` (the second number is the measured λ in cells). The chest's front-top edge line runs **through** this row, broken only by label halos: `D 1.0 —— G 50 —— D 2.0`.
- **Title block, top-left** (u 0.05–0.60, v 0.04–0.10):
  - `V O I C I N G` in ≈ 9 mm hairline spaced caps.
  - `THE RANK A REACTION CUTS FOR ITSELF` (≈ 2.6 mm).
  - Three lines at ≈ 1.9 mm: `EVERY PIPE IS EIGHT WAVELENGTHS OF THE` / `PATTERN WRAPPED ROUND IT. THE LADDER` / `IS CUT FROM SQRT D.`
- **Parameter deck, left column** (u 0.05–0.30, v 0.20–0.38, ≈ 1.6 mm): `GRAY-SCOTT` · `DU 0.16  DV 0.08` · `F 0.030` · `K 0.057` · `GRID 128  PBC` · `DT 0.75` · `STEPS 7000` · `LAMBDA FROM S Q` · `LADDER MISS 3 PCT` · `TOEPFER SCALING` · `LENGTH IS DATA` · `GERMS AT HALF SCALE`.
- **Chest captions, left** (u 0.05–0.25, v 0.78–0.86), interleaved with the wind scraps: `ONE WIND` (≈ 2.6 mm) · `NO PITCH IN IT` · `RED WENT IN` · `BLACK CAME OUT`.
- **Furniture.** A tiny swatch bar (black + red stubs) top-right at (u 0.97, v 0.03). A plus mark bottom-right at (u 0.98, v 0.97).
- **Empty zones.** The left column below the deck (u 0.05–0.23, v 0.40–0.73) and the band above pipes 1–4 (v 0.15–0.33) are bare.

## The science it encodes
From the docstring and brief:

- **Model.** Gray–Scott, du/dt = Du∇²u − uv² + F(1−u), dv/dt = Dv∇²v + uv² − (F+k)v. Explicit Euler, 5-point periodic Laplacian, 128² torus, F 0.030, k 0.057, Du 0.16, Dv 0.08, dt 0.75, 7000 steps, one shared noise realization for all five runs.
- **Measurement.** λ = N / q\*, where q\* is the intensity-weighted first moment of the radial structure factor.
- **Crossed design:**
  - The three middle pipes share D = 1.0 and differ 6× in germ size (8 vs 20 vs 50 cells). They come out the same height (12.2 / 12.1 / 12.0 cells), which is the control.
  - The outer two share germ 20 and have D ×0.4 and ×2.0. They give 7.5 and 17.4 cells against a predicted 7.65 and 17.1 from √D, and the sheet says `LADDER MISS 3 PCT`.
- **What is data vs. chosen.** Pipe length = 8 × λ × 1.10 mm/cell. Diameter follows Toepfer's organ-building rule d ∝ L^0.72 and is decorative-by-rule; the sheet says "only LENGTH is data". Wrapping the torus on a cylinder is topologically honest (the domain is periodic).
- **What the render does NOT show:**
  - The "eight wavelengths wrapped round it" are not countable. The pattern is labyrinthine, so the eye cannot see eight bands up a pipe.
  - The red rungs do not visibly coincide with anything in the black pattern.
  - The "eighth rung lands on the cut" claim is not legible: the top rung sits ≈ 5–10 mm below each top ellipse.
- **Twist, unwritten.** √(1/0.4) = 1.581 is within 0.4 % of an equal-tempered minor sixth (2^(8/12) = 1.587). √2 is exactly the equal-tempered tritone. The organ-pipe carrier could say that, and the sheet does not.

## How it got here
- **v1.** Pipes stood straight on the ground with plain rectangular bases. The parameter deck sat mid-left next to pipe 1. Nameplates ran together in one row (`D 0.4GERM 8D 1.0 GERM 50 2.0`). Captions at the bottom-left (`RED IS WHAT WENT IN`, `... IS THE RESULT`) collided with a dense wind scribble.
- **v2.** Conical feet with mouths were added; the sloped chest with the wind band appeared. Germs became red diamond outlines scattered over the wind. The deck moved top-left.
- **v3.** Germ diamonds overlapped labels (the G 50 diamond crossed `12.0`).
- **v4.** Germs became hatched masses in a row, but the G 50 rhombus overran its neighbours. The deck dropped next to pipe 1.
- **v5.** The rank shifted left, so the deck crowded pipe 1.
- **v6.** The rank moved right and `GERMS AT HALF SCALE` was added. This is essentially the final layout.
- **seed19.** The same layout on another noise realization. λ for G 50 is 11.9 instead of 12.0, and pipe heights are unchanged to the eye (a good sign for the physics).
- **v7 (current).** Cleaner, smaller germ rhombi; otherwise v6.
- **After this.** The family moved on: round 03 is `RULED` (`studio/ruled/DESCRIPTION.md`), the same mechanism transposed to a lattice-with-defects page. No Juan feedback recorded.

## Keep — what works
- **The skyline is the result.** A flat three-pipe plateau (the germ control) flanked by a step down (D 0.4) and a tower (D 2.0) reads in one glance at 3 m without reading a number.
- **Pattern coarsening across the rank.** Fine worms on pipe 1 to fat loops on pipe 5 is visible at 1 m and matches √D.
- **Red semantics.** Red only for what was put in (germs) and what was predicted (ladders). One scarce, loud pen with a stated meaning.
- **Germ rhombi at true (half) scale.** They make the 6× germ ratio physically obvious under three equal pipes.
- **The axonometric rank.** One shared basis, near pipes occluding far ones (exact clipping via silhouette regions). It gives real depth: cylinders, foreshortened chest and ellipses.
- **The chest captions `RED WENT IN / BLACK CAME OUT`.** A good two-line summary of the pen semantics.

## Weak — what doesn't
- [concept] It is an **illustration**. A viewer can name an object that is not the mechanism: organ pipes, a windchest. The rubric (§6) says to cut it. The carrier is defended in the docstring, but the defence is an analogy, and the sheet does not cash it with a twist (no musical interval, no note names).
- [concept] "Eight wavelengths wrapped round it" is uncountable. The labyrinth never presents as eight bands, and the red rungs float free of the black pattern, so the falsification ("you would see it without reading a number") is not visible.
- [space] The chest's front-top edge runs straight through the nameplate row (`D 1.0 —— G 50 —— D 2.0`), a label grazing geometry. `ONE WIND / NO PITCH IN IT` sits inside the wind scraps, and fragments touch the letters.
- [hierarchy] The title `VOICING` is 9 mm hairline spaced caps; nothing but the rank has mass. The 12-line parameter deck is the "scientific figure" furniture the brief says it abandoned.
- [space] Leftover emptiness: the left column under the deck (u 0.05–0.23, v 0.40–0.73) and the zone above pipes 1–4 are unshaped. They are what was left after placing the rank right of centre.
- [craft] Pipe silhouettes are beaded double strokes. Isolines cross over the top-ellipse rims on pipes 1–2, so the pattern is not clipped to the body.
- [grid] Pipes, nameplates, germs and captions do not share axes. Germ rhombi are offset from their pipe centres; the deck and title share only a left edge.
- [depth] Cylinders have outlines but no tonal turn. The wrapped pattern does not compress toward the silhouettes enough to read as curvature, so bodies read as flat panels with round caps.

## Next versions
1. **tritone** (lens) — Keep the rank but make the carrier earn its keep: the λ ratios are musical intervals.
   - Doubling D multiplies λ by √2, exactly the equal-tempered tritone. D × 0.4 gives 1/√0.4 = 1.581 ≈ a minor sixth.
   - Label pipes by the interval they sound against the reference: `UNISON` ×3 for the germ control, `MINOR SIXTH UP`, `TRITONE DOWN`, with `DIABOLUS IN MUSICA` for D 2.0.
   - The red ladder becomes the ruler on the pipe's front silhouette (ticks on the edge, not floating arcs).
   - Delete the parameter deck.

   The viewer already holds "longer pipe = lower note"; the reaction supplies which note. This is the twist the rubric asks for.
2. **one ring** (abstract) — Drop the object. Gray–Scott power lives on a ring in Fourier space, so draw **RADIAL / NESTED** order:
   - Five concentric rings of the actual isolines, each annulus cropped from its field with radius ∝ 1/λ.
   - The three D 1.0 fields land on the **same** radius and superpose into one heavy triple-drawn ring (the control as overdraw).
   - D 0.4 and D 2.0 sit outside and inside it.
   - Red germ squares go at the centre, at true scale.

   No pipes, no deck: pitch is radius, germ is centre mass.
3. **eight bands** (faithful) — Keep pipes and fix the claim:
   - Lay each pipe's field so its dominant stripe direction is horizontal (rotate the torus crop to the maximal-q orientation), so eight bands are countable.
   - Snap the red rungs to the measured stripe phases (the rung sits on a black band), and let the 8th rung meet the top ellipse exactly.
   - Scale the rank up to fill u 0.05–0.95 and push the deck to a single footer line.

**If only iterating:**
- Move the nameplate row off the chest front-top edge (engrave it between the front-top and bottom edges with ≥ 2 mm clearance), so no black line passes through any label.
- Put the eight red rungs on the pipe's right silhouette as ticks, with the top tick exactly at the top ellipse, so "the eighth rung lands on the cut" is checkable by eye.
- Replace the 12-line parameter deck with one footer line and enlarge the rank by ≥ 20 % so pipes 1–5 span u 0.08–0.95.
