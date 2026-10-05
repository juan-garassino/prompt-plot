# millennium-yang-mills — Yang–Mills existence and mass gap: the light cone with its tip cut out
**Field expert:** mathematical physics (quantum Yang–Mills gauge theory) · **Date:** 2026-09-28 · **Status:** dossier v1

Plate 4 of the MILLENNIUM series. The reference (`ref/reference.png`, AI poster) is an
interpretation brief, never a trace — audited at the end of §2. Verified numbers live in
`data/glueball_spectrum.json` (written from the papers' LaTeX tables, not from memory).

---

## 1. The phenomenon (≤5 lines)

The classical Yang–Mills equations, like Maxwell's, describe **massless waves moving at the
speed of light**, and the action has no mass term and no length scale. The quantum theory is
nevertheless believed to have **no massless particles**: every excitation of the vacuum costs at
least Δ > 0, the lightest being a *glueball* (a bound state of gluons; no free gluon exists).
Lattice simulations settle the physics (Δ = 3.405 √σ for SU(3)). The Clay problem asks for a
*proof* that the quantum theory exists on R⁴ as a rigorous QFT **and** that Δ > 0.

Official wording (Jaffe & Witten, CMI problem description §4, extracted from the PDF):
"A quantum field theory has a mass gap Δ if H has no spectrum in the interval (0, Δ) for some
Δ > 0. … Prove that for any compact simple gauge group G, a non-trivial quantum Yang–Mills
theory exists on R⁴ and has a mass gap Δ > 0." CMI's own one-liner: *the quantum particles have
positive masses, even though the classical waves travel at the speed of light* — that sentence
is the plate's twist.

### Governing math          (natural units ħ = c = 1; masses/energies/momenta in units of Δ)

- **Field and action.** Connection A (Lie-algebra valued 1-form, [A] = mass), curvature
  F = dA + A∧A, i.e. F_μν = ∂_μA_ν − ∂_νA_μ + [A_μ, A_ν]. Action S = (1/4g²)∫ (F, F) d⁴x.
  In 4D g is dimensionless → the classical theory has **no scale** (conformal).
- **Dimensional transmutation.** Quantum running coupling, one loop:
  μ dg/dμ = −b₀ g³/(16π²), b₀ = 11N/3 (pure SU(N)) = **11 for SU(3)** → asymptotic freedom and
  a generated scale Λ = μ·exp(−8π²/(b₀ g²(μ))). Every mass is a pure number × Λ. Pure YM therefore
  has **no MeV**: only ratios (M/√σ, M/Δ) are physical.
- **Spectral condition (Wightman).** Joint spectrum of (H, **P**) lies in the closed forward cone
  E ≥ |**p**|. Unique vacuum Ω: HΩ = 0, **P**Ω = 0 — one point, the cone's apex.
- **Mass gap.** spec(H) ∩ (0, Δ) = ∅. Δ = mass of the lightest state (the 0⁺⁺ glueball).
- **One-particle shells** (each glueball of mass M_i): E = √(|**p**|² + M_i²) — a hyperbola
  (hyperboloid in 3+1) inside the cone, asymptotic to it, vertex at E = M_i.
  Far from the vertex: E − |**p**| ≈ M_i²/(2|**p**|).
- **Multi-particle continuum.** Two particles of mass Δ with total momentum **p** have
  E ≥ √(|**p**|² + (2Δ)²); the whole region above that hyperbola is spectrum. So the mass
  operator √(H² − P²) has spectrum {0} ∪ {isolated masses in [Δ, 2Δ)} ∪ [2Δ, ∞) (with
  symmetry-protected discrete masses embedded above 2Δ).
- **Clustering** (JW §5, eq. 2): for any C < Δ and local O with ⟨Ω,OΩ⟩ = 0,
  |⟨Ω, O(x)O(y)Ω⟩| ≤ exp(−C|x−y|) for |x−y| large. By Källén–Lehmann the 0⁺⁺ channel decays
  asymptotically as the Euclidean massive propagator G_Δ(r) = Δ·K₁(Δr)/(4π² r); a massless
  theory decays as a power (free: 1/(4π² r²)).
- **BPST instanton** (SU(2), for §2 context only): charge density
  q(x) = (6/π²) ρ⁴/(x² + ρ²)⁴, ∫q d⁴x = 1, action 8π²/g²; ρ is a free modulus — classical
  solutions exist at every size, which is exactly why the gap is "not classically visible" (JW §6.6).

---

## 2. Three candidate visual truths (ranked)

### (a) THE EMPTY TIP — the real glueball spectrum as nested mass shells inside the light cone ★ RANK 1

**The relationship.** The joint energy–momentum spectrum of pure SU(3) Yang–Mills, exactly:
one **point** (the vacuum, at the apex of the cone E = |p|), a family of **lines** (one hyperbola
E = √(p² + M_i²) per glueball, M_i from Athenodorou–Teper 2020), and a **plane** (the two-glueball
continuum, the whole region above E = √(p² + 4Δ²)). Between the apex and the lowest hyperbola
(0⁺⁺, vertex at E = Δ) there is **nothing** — an empty lens of paper, the mass gap made visible.
The light cone itself is drawn only as asymptotes: **no state of the theory lies on it**, though
every shell leans toward it at large |p|.

In units of Δ the vertices are (AT2020 continuum limit, SU(3)):

| state | M/√σ | **M/Δ** | note |
|---|---|---|---|
| vacuum | 0 | **0** | the apex, one point |
| 0⁺⁺ | 3.405(21) | **1.0000** | defines Δ — the gap's upper edge |
| 2⁺⁺ | 4.894(22) | **1.4373** | 5-fold (2J+1) |
| 0⁻⁺ | 5.276(45) | **1.5495** | |
| 0⁺⁺* | 5.855(41) | **1.7195** | first radial excitation |
| 1⁺⁻ | 6.065(40) | **1.7812** | lightest C-odd, stable |
| 2⁻⁺ | 6.32(9) | **1.8561** | |
| 2⁺⁺* | 6.788(40) | **1.9935** | on the threshold within errors |
| continuum | 6.810 | **2.0000** | two-0⁺⁺ threshold |
| embedded (sym.-protected) | 7.27…9.02 | 2.135…2.649 | 3⁺⁻, 0⁻⁺*, 4⁺⁺, 3⁺⁺, 1⁺⁻*, 2⁻⁻, 2⁻⁺*, 1⁻⁻, 1⁻⁺, 2⁺⁻, 4⁺⁻ |

**Why visually potent — and the exact coincidence it hands the designer.** The empty band
(0 → Δ) is **exactly as tall** as the band of isolated shells (Δ → 2Δ). The plate is three
equal-pitch zones by physics, not by taste: silence, lines, plane. The irregular vertex rhythm
(1, 1.44, 1.55, 1.72, 1.78, 1.86) is real data and reads like an unequal musical staff — never a
ladder.

**THE TWIST.** Everyone holds Minkowski's light cone — the icon of relativity, "where light
lives". Draw it, then let the mechanism finish the sentence: in a theory whose classical waves
*are* light-like, the cone is **empty**. Nothing sits on it; its tip holds only the vacuum;
every real thing floats a finite distance Δ above it. "Massless equations, massive world" —
CMI's own sentence — told by a picture everyone thinks they already know.

**Abstract order: NESTED** (a family of curves sharing asymptotes, around an isolated point),
read through Kandinsky's triad — **point / line / plane** — which here is not a metaphor but the
literal dimension of each spectral component in the (p, E) plane.

**Lineage.** Wassily Kandinsky, *Point and Line to Plane* (1926): the ORDER taken is point,
line and plane as the three elementary forces with weight and direction — vacuum = point,
one-particle shells = lines, continuum = plane. Take the treatise's order, not its colour-block
look (that look belongs to the KANDINSKY SET plates; this one stays in the Millennium series
grammar). Fallback if the curator wants no overlap: Bridget Riley, *Current* (1964) — one line
family whose spacing drift makes the surface (the shells' convergence onto the asymptotes).

**Geometry options for the translator.** 2D section (p = p_x, E up): hyperbolae in a 45° V.
Or 3D (p_x, p_y, E): nested hyperboloid cups inside a cone, hidden-line — buys depth (rubric
§7) and the gap becomes a void between the apex and the bottom of the innermost cup. Both exact.

**Transposition warning (DESIGN_RUBRIC §6).** Drawn with axes, ticks and a J^PC legend this is
the Streater–Wightman textbook figure. It passes only as an ORDER: no axes, no gridlines, no
tick labels — the cone's rulings are the only frame, Δ is the only measure.

### (b) THE RULER — exponential clustering: the gap is a length the theory draws for itself ★ RANK 2

**The relationship.** Correlations of a gauge-invariant field (e.g. tr F², 0⁺⁺ channel) fall off
as G_Δ(r) = Δ·K₁(Δr)/(4π² r) at large r (Källén–Lehmann, exact asymptotically; the prefactor
|⟨0|O|0⁺⁺⟩|² is a single constant). Draw iso-correlation rings around one source at an
**e-fold ladder** of levels (C_k = C₀·e^{−k}): in a gapped theory the ring pitch tends to a
**constant, 1/Δ** (exact pitch 1/(Δ + 1.5/r)); in a massless theory (power law) the rings spread
geometrically forever — scale-free, a Droste nest. Computed: from r = 0.25/Δ the rings sit at
0.25, 0.40, 0.62, 0.92, 1.32, 1.80, 2.36, 2.99, 3.66, 4.38, 5.13, 5.91, 6.71, 7.54 … with pitch
climbing 0.15 → 0.85 and locking toward 1.0; the massless ladder at the same levels:
0.25, 0.41, 0.68, 1.12, 1.85, 3.05, 5.02, 8.28 (×e^{1/2} each).

**Why potent / twist.** The viewer holds ripples on a pond: rings spread and thin out. Here the
quantum theory, with no scale in its equation, **locks its ripples to a fixed pitch** — it builds
its own ruler (ξ = 1/Δ = 0.294/√σ ≈ 0.12 fm if QCD's scale is borrowed). Near the source the
rings are geometric (short distances look scale-free — the honest UV); far out they are
arithmetic. The transition itself is the gap.

**Abstract order:** NESTED → LAMINAR (a geometric nest that settles into equal strata).
Lineage: Agnes Martin's grids (tone by density alone, a hand-ruled equal pitch).
**Caveat:** the exact tr F² correlator is not known in closed form; only its large-r form is
exact. The inner rings must be labelled/treated as the single-state asymptotic form.

### (c) THE CONTINUUM LIMIT — eight real lattices, finer and finer, one gap that does not move ★ RANK 3

**The relationship.** Real lattice data (AT2020 Table `table_param`): as β goes 5.6924 → 6.50 the
lattice spacing shrinks a√σ = 0.3999 → 0.1038 and the gap **in lattice units closes**
(a·m_G = 0.987 → 0.347), while the gap **in physical units converges**:
m_G/√σ = 2.468, 2.867, 3.060, 3.205, 3.269, 3.312, 3.308, 3.346 → 3.405 (continuum).
Correlation length in sites 1/(a m_G) = 1.01 → 2.88.

**Why potent / twist.** This is the *existence* half of the problem made visible: zoom in until
the grid vanishes — the gap stays. Nested grids at true relative pitch (8 lattices, pitch ∝ a√σ),
each carrying a disc of physical radius 1/m_G(β) that converges. Order: LATTICE (tessellated,
nested scales). Lineage: Vera Molnár, *(Dés)Ordres*. Weakness: needs a reading step ("the grid
is the regulator"); rank 3.

### Rejected carriers (do not rank)
- **Instanton knots / Hopf tori** (the reference's tangled rings). Exact classical solutions,
  but they carry topology, not the gap; worse, ρ is free — they are the *proof* that the classical
  theory has no scale. Using them as "glueballs" is a lie (§4).
- **Running coupling α(μ) curve** — a plot of a function; fails §6.
- **Knotted-flux-tube glueball models** (Buniy–Kephart-type) — speculative; not data.

### Reading the reference poster (audit — interpret, never trace)
What it gets right and we keep: energy runs **up the sheet**; vacuum below, excitations above; a
wide **silent zone** in the middle; **one loud accent (red) for Δ**; a small spaced title.
What is wrong and must be corrected:
1. The excitations' heights encode nothing — knots scattered at arbitrary heights. Every state
   must sit at its measured M/Δ on ONE uniform vertical scale.
2. The red Δ measure does not end on the lowest state. Its top must touch the 0⁺⁺ vertex
   exactly; its bottom must touch the vacuum point exactly.
3. The vacuum is drawn as a wide band of field lines with a bump. The vacuum is **one** unique
   Poincaré-invariant state — a point. A band reads as a range of vacuum energies.
4. Gold orbits/ellipses imply classical orbital motion — decoration; cut.
5. Proportions: the gap is drawn ~0.6× the excitation zone at random. The truth is the gap
   (0→Δ) equals the isolated-shell band (Δ→2Δ), with the continuum above.
6. Knot shapes vary with no J^PC meaning — a glueball has no classical field-line picture.

---

## 3. Real data — verified

All read on 2026-09-28 from the arXiv **LaTeX sources** (`https://arxiv.org/e-print/<id>`), not
from memory; mirrored in `data/glueball_spectrum.json`.

1. **Primary spectrum** — A. Athenodorou & M. Teper, *The glueball spectrum of SU(3) gauge theory
   in 3+1 dimensions*, JHEP 11 (2020) 172, arXiv:2007.06422, doi:10.1007/JHEP11(2020)172.
   Table `table_MK_J` (continuum limit, M_G/√σ, identified J^PC) — the values in §2(a).
   Stars: 3⁺⁺, 4⁺⁺, 2⁺⁻, 1⁻⁺ ex1/ex2 "likely"; 4⁺⁻ "significant uncertainty".
   GeV conversion (their Table `table_MGeV_J`, r₀ = 0.472(5) fm, √σ = 485(6) MeV): 0⁺⁺ = 1.653(26)
   GeV, 2⁺⁺ = 2.376(32), 0⁻⁺ = 2.561(40). The paper itself says this "is not possible" strictly —
   pure gauge and QCD are different theories.
2. **Continuum approach** — same paper, Table `table_param`: β, a√σ, a·m_G (numbers in §2(c)).
3. **Cross-check** — Y. Chen et al., Phys. Rev. D 73, 014516 (2006), hep-lat/0510074, Table
   `summary1`, r₀M_G: 0⁺⁺ 4.16(11), 2⁺⁺ 5.83(5), 0⁻⁺ 6.25(6), 1⁺⁻ 7.27(4), 2⁻⁺ 7.42(7), 3⁺⁻ 8.79(3),
   3⁺⁺ 8.94(6), 1⁻⁻ 9.34(4), 2⁻⁻ 9.77(4), 3⁻⁻ 10.25(4), 2⁺⁻ 10.32(7), 0⁺⁻ 11.66(7).
   Ratios to 0⁺⁺: 2⁺⁺ 1.401, 0⁻⁺ 1.502, 1⁺⁻ 1.748, 2⁻⁺ 1.784 — agree with AT2020 at the few-%
   level (Chen's 0⁺⁺ carries 2.6 %). **Use AT2020 as the drawn set; do not mix the two.**
4. **Problem statement** — A. Jaffe & E. Witten, *Quantum Yang–Mills Theory*, CMI official problem
   description, `https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf` (§4 definition
   of the gap and the problem; §5 clustering; §6.6 "the mass gap is not classically visible").
   Text extracted from the PDF streams on 2026-09-28.

How to compute every drawn quantity: M_i/Δ = (M_i/√σ)/3.405; shell E_i(p) = √(p² + (M_i/Δ)²);
threshold E(p) = √(p² + 4); cone E = |p|. One uniform scale s (mm per Δ) on BOTH axes.

---

## 4. Simplifications allowed vs. lies

**Allowed (honest):**
- A 2D section (one momentum component) or the 3D (p_x, p_y, E) version of the joint spectrum.
- Drawing a subset of states: the seven below 2Δ are the core; embedded states above 2Δ optional.
- Omitting error bars. The 2⁺⁺* (1.9935 ± 0.017 Δ) may be merged into the threshold line or
  omitted — say which. Error bars as a faint line-weight halo are allowed if uniform.
- The continuum as an honest uniform **plane** texture (tone_dots or tone_hatch at fixed pitch,
  or hyperbola-following hatch declared as a fill) — bounded density, every point "occupied".
- Truncating shells at the frame or where neighbour spacing would fall under 0.8 mm.
- 2J+1 multiplicity as an optional channel (pass count or dash count) — never as extra shells.
- Presenting SU(3) as the representative gauge group (the problem is for any compact simple G).

**Lies (binding on everyone):**
1. **Anything inside the cone below the 0⁺⁺ shell except the vacuum point and the Δ measure.**
   No hatch, dash rain, texture, gridline, label or ornament in the gap lens. It is blank paper.
2. **Anything drawn ON the light cone as a state.** The cone is asymptote only (dotted/ghost).
   No gluon line, no "massless mode".
3. **Non-uniform or log energy scale**, or different scales on E and p (the cone must be 45°;
   anisotropic scaling reshapes every shell).
4. **Equally spaced levels** ("a ladder", "a harmonic series"). The vertex rhythm is 1, 1.437,
   1.550, 1.720, 1.781, 1.856 — irregular, measured.
5. **The vacuum as a band, a field of lines, a sea, or a wavy ground.** One point.
6. **The continuum starting anywhere but exactly 2Δ**, or rendered as more discrete shells that
   read as particles.
7. **Calling any line a gluon**, or drawing glueballs as knots / flux loops / instantons as if
   that were their shape, or implying instantons cause the gap.
8. **Δ in MeV/GeV without the borrowed-scale caveat.** On the plate, Δ is the unit.
9. **"Proven"**: the gap is established numerically (lattice); the proof is the open problem.
   No caption may claim the theorem.
10. **Mixing data sets** (AT2020 and Chen on the same shell set), or using experimental QCD
    candidates (f₀(1710) etc.) as pure-YM glueballs.
11. Claiming the shells' approach to the cone *is* asymptotic freedom (it is kinematics,
    E − |p| ≈ M²/2|p|).

---

## 5. The misconception to quietly correct

**"Gluons are massless like photons, so the mass gap must be the gluon's mass"** — or its twin,
"the strong force should reach forever like light." The truth: there is no gluon in the
spectrum at all and **nothing on the light cone**; the lightest physical thing is a glueball
whose mass is manufactured by the quantum theory from an equation with no mass and no scale in
it. The plate corrects this by drawing the cone faithfully and leaving it empty. Secondary,
for the caption only: the gap is the distance from the **vacuum** to the first state — not the
spacing between levels — and physicists are not in doubt that it exists; the prize is for the
proof (existence on R⁴ + Δ > 0).

---

## 6. Pen-plotter fit

**Naturally a line here:** each mass shell is one exact curve (a hyperbola: few points, no
noise, zero pen lifts per shell). The vacuum is a single small ring/dot. The continuum is the
only area. The cone is a pair of dotted rulings (or, in 3D, a sparse fan of generators).

**Must stay blank paper:** the gap lens — the whole cone interior below the 0⁺⁺ shell. The
gap is the largest quiet zone on the sheet by physics. Conversely, do NOT leave a blank margin
between the 2Δ threshold line and the continuum texture: the continuum begins ON the threshold.

**Scale & density (worked at s = 60 mm/Δ, |p| ≤ 2.2Δ, E ≤ 2.7Δ):**
- Vertex gaps: apex→0⁺⁺ 60 mm; 0⁺⁺→2⁺⁺ 26.2; 2⁺⁺→0⁻⁺ 6.73; 0⁻⁺→0⁺⁺* 10.2; 0⁺⁺*→1⁺⁻ **3.70**
  (tightest); 1⁺⁻→2⁻⁺ 4.49; 2⁻⁺→2Δ 8.63. 2⁺⁺*→2Δ = **0.39 mm** — under the 0.8 mm floor: merge
  or omit (still 0.65 mm at s = 100).
- Shells converge on each other along the arms (gap ∝ ΔM²/2p): the first pair to cross the
  0.8 mm perpendicular floor is 0⁺⁺*/1⁺⁻ at |p| ≈ 5.6Δ — far off-sheet at this scale. Check
  again if the translator widens the p range.
- Aspect: the 2D section with |p| ≤ 2.2Δ, E ≤ 2.7Δ is ≈ 1.6:1 landscape; a portrait sheet takes
  |p| ≤ ~1.3Δ (shells still visibly curve; cone rulings exit the sides).
- Draw length at that scale: six shells ≈ 1.74 m; cone rulings ≈ 0.37 m (less if dotted);
  continuum as 1.2 mm horizontal-pitch plane ≈ 5.0 m (35 strokes). Continuum dominates the time.

**Pens (one layer per meaning, light → dark, red last):**
1. ghost pen (fine grey/blue 0.1): cone asymptotes — the classical promise, empty.
2. black fine (0.1–0.2): continuum plane (tone by duty, fixed pitch ≥ 0.8 mm; 2.4× nib for hatch).
3. black (0.3): the isolated shells 2⁺⁺ … 2⁻⁺ + the 2Δ threshold + vacuum point.
4. red (loud, scarce): the Δ measure from apex to 0⁺⁺ vertex, and the 0⁺⁺ shell itself (the
   gap's edge). Last, so nothing inks over it.
Minutes per layer ≈ draw length / feed (+ pen cycles × dwell): at Leo's slow F600 the plane is
≈ 8–9 min, shells ≈ 3 min, cone < 1 min, red < 1 min, plus lifts — a dotted cone costs a pen
cycle per dot, so prefer ≤ 40 long dashes per ruling. Strokes batch naturally: each shell and
each hatch row is a single stroke, ordered bottom→top.

---

## 7. Check numbers

Units: Δ = M(0⁺⁺). Data: `data/glueball_spectrum.json` (AT2020). Reproduce with `.venv/bin/python`.

| # | value | one-liner |
|---|---|---|
| 1 | Δ/√σ = **3.405(21)**; drawn Δ = 1 unit = s mm, apex → 0⁺⁺ vertex | AT2020 `table_MK_J` |
| 2 | M(2⁺⁺)/Δ = **1.4373**, M(0⁻⁺)/Δ = **1.5495**, M(0⁺⁺*)/Δ = **1.7195**, M(1⁺⁻)/Δ = **1.7812**, M(2⁻⁺)/Δ = **1.8561** | `[m/3.405 for m in (4.894,5.276,5.855,6.065,6.32)]` |
| 3 | continuum threshold at exactly **2Δ = 6.810 √σ**; states strictly below it: **7** (incl. 0⁺⁺ and 2⁺⁺* at 1.9935) | `sum(m<6.81 for m in json masses)` |
| 4 | gap height = isolated band height: (Δ−0) : (2Δ−Δ) = **1 : 1** — measure both on the render | ratio of apex→0⁺⁺ and 0⁺⁺→threshold vertex distances |
| 5 | cone half-angle **45°** (E and p on one scale); 0⁺⁺ shell at p = 3Δ sits **√10 − 3 = 0.1623Δ** above the cone (≈ 1/(2·3) = 0.1667) | `np.sqrt(10)-3` |
| 6 | lens tip: 0⁺⁺ shell at p = 1Δ is at E = **√2 = 1.4142Δ**, 0.4142Δ above the cone | `np.sqrt(2)` |
| 7 | nothing inked inside {E < √(p²+1)} ∩ {E > |p|} except the vacuum point and the red Δ segment — **0 strokes** | clip the gcode's G1 segments against that region |
| 8 | Chen 2006 cross-check: 2⁺⁺/0⁺⁺ = **1.401**, 0⁻⁺/0⁺⁺ = **1.502** (AT2020 1.437 / 1.550 — few-% agreement; drawn set must be AT2020) | `5.83/4.16, 6.25/4.16` |
| 9 | lattice approach (if §2c used): m_G/√σ = am_G/(a√σ) = **2.468 (β 5.6924) … 3.346 (β 6.50)** → 3.405 | `0.987/0.3999, 0.3474/0.10383` |
| 10 | clustering length ξ = 1/Δ = **0.2937/√σ** (≈ **0.119 fm** only with √σ = 485 MeV borrowed; ħc = 197.327 MeV·fm); e-fold ring pitch → 1/(Δ + 1.5/r): **0.851/Δ at r ≈ 8.4/Δ** | `197.327/(3.405*485)`; K₁ ring solve |
| 11 | BPST: ∫(6/π²)ρ⁴/(x²+ρ²)⁴ d⁴x = **1.000**; half-max radius **0.435ρ** | `np.sqrt(2**0.25-1)` |
| 12 | one-loop b₀ = 11N/3 = **11** for SU(3) | `11*3/3` |
