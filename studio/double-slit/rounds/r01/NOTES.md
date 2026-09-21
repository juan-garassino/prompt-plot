# THE DOUBLE SLIT — round r01 notes

Piece: `piece.py` → `double_slit_cross_term(rng, bounds, colors=3)`
Brief: `studio/quantum-01/double-slit.md`
Render: `~/Downloads/pp_double_slit_s7.png` (A4 portrait, 2 pens, 15 738 commands,
draw 8 620 mm, travel 8 243 mm). Seeds 3 / 7 / 21 produce **byte-identical** PNGs —
the piece is deterministic and effectively seed-free (the physics is exact; `rng`
is accepted for the contract and never consulted).

---

## 1. The exact physics

**Apparatus (stated, not cited).** λ = 633 nm, slit width a = 100 µm,
centre-to-centre separation d = 300 µm, screen distance L = 2.000 m, one quantum
at a time. `d = 3a` exactly, so the third principal maximum lands on the first
envelope zero and is annihilated — the *missing order*. Fresnel number
N_F = a²/(λL) = 7.9 × 10⁻³.

**Amplitudes — Rayleigh–Sommerfeld / Fresnel–Kirchhoff aperture integral**, one
per slit, evaluated by 96-node Gauss–Legendre quadrature over the aperture. No
far-field approximation anywhere in the drawn geometry:

```
psi_j(x) = INT[x_j-a/2 .. x_j+a/2]  exp(i k (r - L)) * (L/r) * r^(-1/2)  dx'
r        = sqrt(L^2 + (x - x')^2)
r - L    = (x - x')^2 / (r + L)          <- used verbatim
k        = 2 pi / lambda
```

The `r − L = (x−x')²/(r+L)` identity matters: k·r ≈ 2 × 10⁷ rad here, so forming
`r − L` by subtraction would throw away ~8 significant digits of the phase. The
common piston factor exp(ikL) divides out of every intensity.

Screen angle is exact, not small-angle: `sin θ = x / sqrt(x² + L²)`, and the plate
coordinate is the dimensionless envelope unit `u = a sin θ / λ` (so u = ±1 ARE the
first envelope zeros, and the plate is cropped to exactly the central lobe).

**The three quantities, all from the same two complex arrays:**

```
I_quantum(x)   = |psi1 + psi2|^2          paths indistinguishable   -> plate 2
I_classical(x) = |psi1|^2 + |psi2|^2      which-path known          -> plate 1
Delta(x)       = 2 Re(psi1 conj(psi2))    the cross term            -> DRAWN NOWHERE
```

Both plates are normalised by the SAME constant (`max I_quantum`) and drawn with
the same mm-per-unit height gain, so the 2 : 1 height ratio on paper IS the physics.

## 2. Verification receipts (all reproduced by the script in §6)

| Check | Result |
|---|---|
| Quadrature convergence, 96 vs 192 nodes | max relative difference **1.8 × 10⁻¹⁴** (machine) |
| Exact RS vs far-field closed form `sinc²(πa sinθ/λ)·cos²(πd sinθ/λ)` | max relative deviation **2.35 × 10⁻⁴** — the closed form is an oracle, not the drawn quantity |
| `max(I_classical) / max(I_quantum)` | **0.500000000000** (12 digits; theory ½ — at a bright fringe the cross term supplies exactly half the probability) |
| peak cross term / peak quantum intensity | **0.500000** |
| Nulls, found by golden-section on the computed intensity | −0.83345499, −0.5, −0.16666507 and mirrors; vs `(m+½)·a/d` max deviation **1.2 × 10⁻⁴** in envelope units |
| Fringe visibility `(Imax−Imin)/(Imax+Imin)` | **0.9999197** — deepest null is 4.0 × 10⁻⁵ of the peak, NOT identically zero, because |ψ₁| ≠ |ψ₂| at x ≠ 0 (different obliquity and 1/√r). That residual is real physics and is the reason the nulls are found rather than assumed. |
| Conservation: `∫Δ dx / ∫I_classical dx` over the plotted crop | **2.25 × 10⁻⁴** (0.02 %) — interference redistributes; it does not create. The 0.02 % is the honest boundary term of a finite crop, not an error. |

## 3. Engine primitives used

- `Scene3D(px=(560,420), fit="rescue", tip=0.45)` — one scene, two surfaces.
- `Scene3D.surface(SX, SY, DEP, pen=…, thin=ScreenThin(gap_mm=3.0, far_mult=1.25))`
  — the z-buffer hidden-line renderer plus the engine's native depth-aware
  screen-space thinning. **No z-buffer, no thinning and no occlusion logic is
  hand-rolled in the piece** (house law). The plate declares (SX, SY, DEP); the
  engine decides what survives.
- `Scene3D.halo_labels(...)` before any surface call, so both meshes and the
  ground rules part around every label; glyphs draw last, on top.
- `Scene3D.poly(...)` for the ground lines, front rims (2 passes = line weight),
  crimson ground rules and plumbs — all at depth 0, where nothing can occlude them.
- `kit._spaced / _stroke_text / _text_width` for the spaced-caps type, with a
  local `line()` helper that shrinks a line until it fits its column (this is what
  stops one long string from triggering a global `fit="rescue"` downscale — that
  bug cost three rounds).

**Axonometry.** One cabinet-oblique basis for the whole scene:
`u → (ax, 0)`, `probability → (0, gain)`, `depth → (dx, dy)`. The subordinate
plate shrinks its world FOOTPRINT (`z_dune = 0.34`) and never the projection
constants. Plate spacing is derived from the real projected extents
(`up_hero`, `up_dune`, `dn`), so no parameter change can make the stages
interpenetrate. Registration is by **dotted** vertical projection lines (the wy
axis): black at the two envelope zeros and the optic axis, crimson at each null.
No arrows anywhere. No trajectories, no source, no slit icon, no apparatus.

## 4. What was missing / what fought back

- **`surface()` couples the two mesh families' density.** Both the fall-line
  (constant-u) family and the profile (constant-z) family come off one grid and
  share one `ScreenThin`. For a relief whose flanks are near-vertical (peak 66 mm
  over a 11 mm half-fringe → 84°) that is the whole design problem: rows and
  columns need opposite densities. Worked around with a very fine `nu = 460` plus
  a coarse `gap_mm = 3.0`, which lets the engine thin the flats hard while keeping
  every sample on the flanks. A per-family gap on `ScreenThin` would have made
  this a one-liner.
- **The extrusion direction must not be near-parallel to the steepest rim
  tangent.** When it was (`dx=2.2, dy=20` → 84° vs 83°), adjacent fall lines
  collapsed to ~0.2 mm apart and the ridges rendered as black mud; when it was
  far too shallow (`dx=32, dy=17` → 28°) the whole plate sheared up-right and the
  envelope's symmetry stopped reading. The shipped value (14, 22) ≈ 58° is the
  compromise. This constraint is not documented anywhere in the engine; it cost
  four rounds. It belongs in the engine docs as a rule of thumb:
  *keep |angle(depth basis) − angle(steepest surface tangent)| ≳ 20°.*
- **`pens=` colouring a single mesh column breaks the crossing family's runs**
  (`_emit_runs` splits on pen change and drops 1-sample runs), so a crimson
  constant-u line punches a visible gap through every profile line it crosses.
  Two adjacent red columns fix the gap but then collide with `ScreenThin`, which
  can thin the red line away entirely. Crimson was therefore moved out of the
  mesh onto always-visible depth-0 geometry (ground rules + plumbs), which is a
  better design anyway. An "exempt from thinning" flag on `pens` would help.
- **A single over-long type string silently rescales the entire plate**, because
  `fit="rescue"` fits the global bbox. There is no warning. The `line()` helper
  here should probably be promoted into `kit`.
- `Scene3D.visible()`'s `bias = 0.02 * dspan` means a grid with more than ~25 rows
  in depth z-fights against itself. Not documented.

## 5. Honest self-critique vs DESIGN_RUBRIC.md

| Dimension | Self-score | Reasoning |
|---|---|---|
| **1 Hierarchy** | 8 | The comb is unmistakably the dominant mass at 3 m (≈150 × 88 mm, twice the dune's height by physics, not by choice); the dune is a clear second; the crimson plumbs and the rim's dives to ground reward 30 cm. The giant DOUBLE/SLIT stack competes for first place — deliberate, but a critic could fairly call it two dominants. |
| **2 Grid & alignment** | 8 | Everything hangs on one flush-left axis (x₀): title stack, stage labels, note block, first footer column. Both plates share one cx, one u→x mapping and one height scale, so the registration verticals are truly vertical. Footer is three columns on a 0.335 W module. |
| **3 Tension & asymmetry** | **5 — the weakest dimension** | The physics is mirror-symmetric in u and I refused to crop it asymmetrically, so both reliefs are near-symmetric masses sitting centred on the sheet. The only working asymmetries are the oblique lean, the flush-left type against the right-hand standfirst, and the stacked (not side-by-side) plates. Nothing crops at the frame. A critic would mark this down hard, and would be right. |
| **4 Negative space** | 7 | The valleys between ridges are genuine shaped voids and they carry the argument (they are the cross term). Quiet bands above plate 1, below plate 2, and the top-right corner. Not *generous* — the sheet is fairly full. |
| **5 Craft for pen** | 8 | 2 pens (1 swap), ~8.6 m draw. Rims 2 passes, ground lines 1. Engine thinning holds the flats at ~3 mm and the flanks at ~1.2 mm perpendicular — above the 0.8 mm gate everywhere. Some residual hidden-line "hair" on the steep flanks: correct output, slightly scruffy. No ink-on-ink. |
| **6 Concept legibility** | 7 | A smooth unbroken dune above; the same quantity below, twice as tall and cut to the floor at regular intervals; crimson plumbs standing on the dune with no counterpart on the comb. The one-glance reading — *the same stuff, rearranged* — does land. The risk: **this is a relief of an intensity function, and a hostile critic can call it an axis plot in disguise** (the rubric's NO-SCHEMATICS clause). I argue it is the phenomenon (the landing-probability landscape) and not the apparatus — there is no source, no slit, no arrow, no axis, no tick, no legend — and it is the same idiom as the shipped `bauhaus_relevance`. But I flag it rather than hide it. |
| **7 Depth & dimensionality** | 7 | Genuine 3D: shared cabinet-oblique basis, true hidden-line occlusion (the far rows are culled behind the near ridges), the dune's slab overlapping its own flank, dotted projection lines. Not flat, and not declared flat. Weaker than it could be because the depth axis carries no second variable — it is an honest extrusion of a 1-D pattern. |

**Average ≈ 7.1 — this does NOT clear the bar** (avg ≥ 8, nothing below 7).
Tension & asymmetry at 5 is a hard fail and is the single thing to fix in r02.

**The single biggest weakness: the composition is symmetric and centred.**

Three concrete moves for r02:
1. Rotate to A3/A4 **landscape** and put the two plates side by side, sharing one
   ground line but offset in depth along the shared basis — the comparison becomes
   one continuous screen instead of an exploded stack, and the sheet gets a working
   diagonal.
2. Crop the interference relief at the right frame edge (honest: the screen is
   wider than the paper — but then the "central lobe" colophon line must change,
   and the missing order must stay visible on the left).
3. Let the depth axis carry the **distinguishability** D (Englert's D² + V² ≤ 1,
   with I(x) = |ψ₁|² + |ψ₂|² + 2V·Re(ψ₁ψ₂*), V = √(1−D²)). Then the surface
   morphs continuously from comb to dune across its own depth — one object, the
   two named laws as its two edges, real information on every axis, and a
   naturally asymmetric form. This is the strongest of the three and the one I
   would take.

## 6. Reproducing the receipts

```bash
.venv/bin/python scripts/render_candidate.py studio/double-slit/rounds/r01/piece.py \
    --fn double_slit_cross_term --seed 7 --paper a4 --out ~/Downloads/pp_double_slit_s7.png
```

The table in §2 comes from a throwaway script that imports `piece.py` and calls
`_intensities`, `_find_nulls`, `_psi` directly; every number there is a live
computation on the shipped code, not a remembered value.

## 7. Provenance note (read before any gallery print)

An earlier draft of the brief proposed the **Zeilinger et al. 1988** neutron
double-slit geometry (Rev. Mod. Phys. 60, 1067). Those numbers could only have
been recalled, not read, so they were dropped. The plate now states an ordinary
optical-bench geometry and claims **no measured data** — what is asserted as exact
is the computation, and §2 proves it. If the piece is ever relabelled with a real
experiment's numbers, they must be read off the paper first.

Dossier compliance (`studio/quantum-01/dossier.md` §4 "Lies"): no trajectories, no
drawn travelling wave, no source, no slit icon, no arrows. The which-path plate is
labelled `PATHS DISTINGUISHED` — a prediction, not data. The dossier's
"no sinc² envelope" rule is specific to the Tonomura **biprism**, which has no slit
width; this is a real two-aperture screen, so its envelope is genuinely there, and
the colophon says `NOT A BIPRISM: THE ENVELOPE IS REAL` so the science critic does
not cross-apply the rule.
