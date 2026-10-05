# ORBITAL RESONANCE — r01 notes

Piece: `piece.py` → `orbital_resonance_belt(rng, bounds, colors=3)`.
Brief: `studio/astro-01/orbital-resonance.md`.
Render (A4 portrait, seeds 7 / 3 / 11):

```
.venv/bin/python scripts/render_candidate.py studio/orbital-resonance/rounds/r01/piece.py \
    --fn orbital_resonance_belt --seed 7 --paper a4 \
    --palette black,crimson,black \
    --out gallery/studio/orbital_resonance/trials/pp_orbital_resonance_r01_s7.png
```

`--palette black,crimson,black` matters: pen **2 is the type/furniture layer** and is a
black nib (a finer one on the machine), not the harness's default forestgreen.

---

## 1. The physics, exactly

**Model.** Planar circular restricted three-body problem. Units G(M☉+m_J) = 1, a_J = 1,
so n_J = 1 and T_J = 2π. μ = m_J/(M☉+m_J) = **9.5388e-4**. Barycentric inertial frame:

```
r☉(t) = −μ (cos t, sin t)          r_J(t) = (1−μ)(cos t, sin t)
r̈ = −(1−μ)(r − r☉)/|r − r☉|³ − μ (r − r_J)/|r − r_J|³
```

**Integrator.** Velocity-Verlet (the hint from the dead run — correct, and the right
choice here: it is symplectic for this prescribed-Jupiter Hamiltonian, so it introduces
no secular drift in *a*, and *a*-drift is the entire signal). `dt = 0.02` ≈ 130 steps per
asteroid orbit at the belt's inner edge; `t_end = 300·2π` (300 Jupiter years); state
sampled every 10 steps. Integrating in the inertial frame rather than the rotating one is
deliberate: no velocity-dependent Coriolis term, so plain velocity-Verlet applies without
a predictor.

**Initial conditions.** 225 test particles, semimajor axes a uniform on
[1.70, 3.80] AU (a_J = 5.2028 AU), e₀ = 0.18 for every one, mean anomaly and longitude of
perihelion drawn from the seeded `rng.np`. Kepler's equation solved by 40 Newton steps.
*The comb is uniform in a by construction* — the only thing the seed changes is phase, so
every structure on the sheet was carved by the dynamics.

**Measurement.** Osculating semimajor axis each sample from the heliocentric vis-viva
`a = 1/(2/|r_h| − |v_h|²/(1−μ))`, boxcar-averaged over one orbital period (`per/dts`
samples) to strip the short-period terms; then

- **libration width** Δa = max ā − min ā over the run, in AU — the signal;
- **background** bg(a) = running median of Δa over ±0.22 AU — the non-resonant floor,
  which genuinely grows with a as Jupiter is approached;
- **excess** X = Δa / bg — "louder than its neighbours"; **lanes** L = Δa / (2.1 · pitch)
  — "wanders out of its own lane" (pitch = 0.00938 AU = 1.2 mm on the sheet).

**Drop rule.** An orbit is drawn only if `max(L, (X−1)/1.4) < 1`. The void mask is then
morphologically closed over ±4 lanes: the stable island *centre* inside a separatrix has
small Δa and would otherwise leave a stranded ring inside a gap — it is in the resonance,
so it goes.

**Ink rule (the density ramp).** dash length fixed at 5.2 mm; period = 5.2/duty with
`duty = 1 − 0.85·max(0.45·L, (X−1)/0.7)`, floored at 0.20. Ink fades faster than the
orbit dies, so every void arrives with a shoulder of fraying arcs. Dash phase is
randomised per arc — without that, dashes register vertically across neighbouring arcs
and the field turns into a false lattice (visible in v1, fixed in v2).

**Crimson.** Five arcs at `a_J (q/p)^(2/3)` for 4:1, 3:1, 5:2, 7:3, 2:1 — Kepler III and
nothing else, no integration. They land at 2.065 / 2.501 / 2.825 / 2.958 / 3.278 AU.

**Measured voids** (seed 7, A4): 4:1 → 2.04–2.06 · 3:1 → **2.47–2.52** · 5:2 → 2.81–2.83 ·
7:3 → 2.94–2.95 · and everything from **3.10 AU outward** (the 2:1's zone, wider than its
own libration width — resonance overlap). 140 of 225 orbits survive. Seeds 3 and 11 give
142 / 142 with the same void boundaries: the gaps are physics, not sampling.

**Runtime.** ~9 s integration (225 particles vectorised over one numpy array), ~25 s
total render. Determinism verified: two runs at seed 7 produce byte-identical GCode.

---

## 2. Engine primitives used

- `Scene3D(rng, bounds, fit="none")` — as the halo/label/emit host. `fit="none"` is
  load-bearing: the radial scale is data, so the scene must not rescale anything.
- `scene.halo_labels(...)` — every label reserves a knockout box **before** any arc is
  drawn, so the field opens around type instead of crossing it.
- `scene.poly(pts, pen=…)` — halo-aware polyline emit (it densifies at 0.8 mm and cuts at
  the halo boundary, which is why a 190 mm arc loses only the label's width).
- `scene.render()` — draws the glyphs last, on top.
- `kit._poly / _spaced / _text_width` — strokes, spaced caps, width metrics.

Piece-local helpers (deliberately not pushed into the engine — they are this piece's
idiom, not a house one): `_arc_runs` (circle ∩ drawable, run-split), `_dash`
(fixed-length dash, growing gap, phased), `_arc_point`, `_fit`, `_colons`.

Nothing under `promptplot/` was modified.

## 3. What was missing

- **The stroke font has no `:` glyph.** `_GLYPHS` covers A–Z, 0–9, `-`, `.`, space only;
  `:` advances the cursor and draws nothing, so `3:1` came out as `3 1`. Worked around
  with `_colons()`, which emits the two dots into the (correctly sized) advance the font
  already leaves. A `:` and a `/` in `promptplot/generative/generators.py::_GLYPHS` would
  be a two-line fix and would help any piece that labels a ratio.
- **No dash primitive.** `engine/policies.py` has `occlude_crossings`, `enforce_line_spacing`,
  `limit_ink_density` — all subtractive by *space*, none by *duty*. A dash/duty operator is
  the plotter's native density ramp and every piece that wants tone reinvents it.
- **`scene.poly` has no bounds clip**, only halo cutting, so a piece must pre-clip or the
  postprocessor clamps points onto the margin and leaves a pile of stacked strokes on the
  edge (that was the visible artifact in v3, and the a5 overflow later).
- Scene3D's fit modes are all-or-nothing; a "fit the type, not the data" mode would have
  saved the hand-rolled `_fit`.

## 4. Self-critique against DESIGN_RUBRIC.md

Honest scores, judging the seed-7 png as a critic would.

| Dimension | Score | Why |
|---|---|---|
| Hierarchy | 7 | The field dominates at 3 m, the canyons and the outer void are the clear second read, type and the fraying detail are third. But the dominant element is a *texture*, not a form — there is no single mass with a silhouette. |
| Grid & alignment | 8 | One flush-left column carries the title, the four caption lines, all five ratio labels and the left footer; KIRKWOOD and the right footer hang on x1; the scale ray is the second axis and terminates exactly on the 2:1 radius. Margins exact. |
| Tension & asymmetry | 8 | The focus is off the sheet past the bottom-left corner, so every arc runs one way and nothing is centred; the field crops at three edges; the quiet wedge bottom-left plays against the growing void top-right. |
| Negative space | 9 | The strongest dimension and the reason the subject suits a pen: four canyons the pen never enters, a bottom-left inner void, and a top-right void that is a third of the sheet and is itself a measured result. |
| Craft for pen | 6 | 1.2 mm ring pitch (floor is 0.8) ✓, three pens / two swaps ✓, no ink-on-ink ✗ nothing overlaps. But **24.6 m of draw against 28.3 m of travel** — the dashes cost ~9 k pen lifts, which is slow and, on Leo, risks ink drag on every lift. This is the real craft debt. |
| Concept legibility | 7 | "Orbits, emptied where periods lock to small integers" lands, helped by the countable ratio column. No boxes, no arrows, no axis rectangle. But a radial field with a tick axis flirts with the schematic line, and a viewer who ignores the type could read it as decorative banding. |
| Depth & dimensionality | 6, **declared flat** | The style is RADIAL DATA-VIZ (STYLES.md §5), flat by canon, and the concept demands it: the subject is coplanar and the quantity is a radius, so any axonometric tilt would foreshorten the gaps — the one thing the piece exists to show. Layering exists only as halo knockouts and the ink ramp. Under the rubric's declared-flatness clause this should not be a fail, but it is the lowest ceiling in the piece. |

**Single biggest weakness:** the field is a *texture* rather than a form. There is no
dominant mass with a silhouette, and Jupiter — the cause of everything on the sheet —
never appears, because at any scale where the 3:1 gap is 5 mm wide, 5.2 AU is 400 mm off
the page. The piece therefore states the effect beautifully and leaves the agent implicit.

**Three changes I would make in r02:**
1. Kill the travel: draw the frayed arcs as *shorter continuous runs with real gaps*
   (segment the arc once per libration excursion) instead of a uniform dash comb, or
   accept 2 mm pitch and half the orbits.
2. Give the top void one loud crimson mass — Jupiter cropped at the top-right corner on a
   second, *declared* radial break — or drop the ambition and put a real Trojan/Hilda
   inset there. The void is currently carrying no information at its far end.
3. Push the inner belt darker and the outer belt lighter than the physics alone gives
   (still monotone in Δa, just a steeper ramp) so the field reads as a *body* with a lit
   edge rather than an even slab.

## 5. Honest caveats, stated in the piece's own footer

- Sun and Jupiter only: no Saturn, so the **ν₆ secular resonance** that actually cuts the
  belt's inner edge at ~2.1 AU is absent — orbits inside 2.0 AU are drawn as stable
  because in *this* model they are.
- 300 Jupiter years shows the **lock**, not the **removal**. The real clearing is Myr-scale
  chaotic eccentricity growth followed by a planet-crossing encounter (Wisdom 1982). What
  is drawn is the libration that starts it.
- The belt's outer edge comes out at 3.10 AU rather than the observed 3.28 with a sparse
  Cybele group beyond — at e₀ = 0.18 the 2:1's overlap zone reaches further in than the
  real population's. Lower e₀ pushes the edge out but costs the 5:2 and 7:3 gaps entirely
  (they are 3rd and 4th order, so their strength goes as e³ᐟ² and e²). e₀ = 0.18 was chosen
  as the setting where all five gaps appear at once; it is a real belt eccentricity, not a
  tuned one, but it is a choice and it is the reason the outer edge is early.
- **A 3:2 Hilda counterpoint was attempted and honestly abandoned.** Resonance also
  *protects* — the Hildas at 3.97 AU survive next to Jupiter — but protection requires the
  resonant argument to librate about a specific value, and a uniform comb with random
  phases at e₀ = 0.18 puts almost nothing in that island: the scan of 3.60–4.20 AU came
  back entirely chaotic (Δa of 0.1–5 AU, several particles unbound). Claiming a Hilda
  triangle would have meant hand-picking an initial phase, so it is not in the piece.
