# millennium-navier-stokes — Navier–Stokes existence & smoothness: in the plane a whirlpool can only open its eye; the spiral is the third dimension
**Field expert:** mathematical physics (fluid dynamics, PDE regularity) · **Date:** 2026-09-28 · **Status:** dossier v1

> **STATUS CHANGED THIS MONTH. Read before writing any caption.** On 8 Sep 2026 OpenAI posted a
> 166-page paper plus a Lean 4 formalisation, *Finite time blowup for Navier–Stokes*, claiming
> Fefferman's alternatives **(C) and (D)**: blow-up in finite time **with a smooth external
> force**, on R³ and on T³. It has not been independently verified or peer-reviewed. On 11 Sep
> the Clay Institute said the problem "has apparently been settled", called its evaluation
> "deliberately unhurried", and made no award. The **unforced** question (alternatives A/B: can
> smooth decaying data with **no push** blow up?) is still unresolved. "Nobody knows" is now
> false, and so is "solved". The only honest wording is **dated and conditional** (§4, §7-C10).

---

## 1. The phenomenon (≤5 lines)

A viscous incompressible fluid obeys Newton's law, and friction smooths it. The open question is
whether, in **three** dimensions, a smooth, finite-energy flow can concentrate itself until the
velocity is **infinite at a point in finite time**. In 2D this is proved impossible (Ladyzhenskaya).
The difference is **vortex stretching**, the term (ω·∇)u, which is identically zero in the plane. A
stretched vortex spins faster and gets thinner, and that is the only way 3D can escape the 2D proof.

### Governing math

- **Navier–Stokes** (Fefferman's statement, eqs. 1–3, n = 3):
  ∂ₜu + (u·∇)u = ν∆u − ∇p + f, ∇·u = 0, u(x,0) = u°(x).
  u [m/s], p [m²/s², kinematic], ν > 0 [m²/s], f [m/s²].
  Physically reasonable = smooth p, u on R³×[0,∞) with bounded energy ∫|u|²dx < C (eq. 7).
- **Vorticity form**, ω = ∇×u:
  **Dω/Dt = (ω·∇)u + ν∆ω**. In 2D, ω ⟂ plane and (ω·∇)u ≡ 0, so ω is only carried and diffused. A
  maximum principle holds and ‖ω‖∞ can never grow. In 3D the first term can amplify ω.
- **Blow-up criterion.** Beale–Kato–Majda, as quoted by Fefferman for Euler: blow-up at T requires
  ∫₀ᵀ sup|ω| dt = ∞. For NS with ν > 0, finite-time blow-up means the velocity becomes unbounded
  (Fefferman, pp. 2–3).
- **Scaling symmetry.** If u(x,t) solves NS then so does **u_λ(x,t) = λ·u(λx, λ²t)**, with the same ν.
  Lengths go as 1/λ, times as 1/λ², vorticity as λ², and circulation Γ is invariant.
- **Exact 3D solution, Burgers vortex** (Burgers 1948). A strain rate α > 0 [1/s] with circulation Γ [m²/s]:
  u_r = −αr/2, u_z = αz, v_θ = Γ/(2πr)·(1 − e^{−r²/δ²}), **δ² = 4ν/α**.
  ω = ω_z ẑ with ω_z = (Γ/πδ²)e^{−r²/δ²}, peak **ω₀ = Γα/(4πν)**.
  This is a steady balance of three effects: inward flow concentrates the vorticity, axial
  stretching amplifies it, viscosity spreads it out.
- **Exact 2D solution, Lamb–Oseen vortex** (classical: Oseen 1911, Lamb *Hydrodynamics*):
  u_r = 0, v_θ = Γ/(2πr)·(1 − e^{−r²/r_c²}), **r_c = √(4νt)**, ω_max = Γ/(4πνt).
  Stream function **ψ = (Γ/4π)[ln s + E₁(s)]**, s = r²/r_c². Verified: dψ/dr = v_θ to 3×10⁻¹¹.
- **Streamlines of the Burgers vortex in closed form.** This is the drawable object. The flow is steady, so streamlines are exactly
  the path-lines. With s = r²/δ² and Re_Γ = Γ/ν:
  **θ(s) = θ₀ + (Re_Γ/8π)·[(1 − e^{−s})/s + E₁(s)]**, r(t) = r₀e^{−αt/2}, **z(t) = z₀e^{αt}**.
  In the core (s→0) this becomes a **logarithmic spiral**: dθ/d ln r = −Re_Γ/(4π), so the pitch angle is
  **tan β₀ = 4π/Re_Γ**. That pitch **does not depend on α**: the shape depends only on Re_Γ, and δ
  only sets its size. In the side (meridional) view: **r²z = const**, a saddle.

---

## 2. Three candidate visual truths (ranked)

### (a) CIRCLES IN THE PLANE, SPIRALS IN SPACE — the whirlpool spiral is itself the third dimension ★ RANK 1

**The relationship.** In 2D incompressible flow, a vortex's streamlines are **closed circles**.
Lamb–Oseen's ψ-isolines are exactly concentric, and a spiral into a point is impossible, because a
converging spiral needs a planar sink and 2D incompressibility forbids one (planar ∇·u = 0). The
Burgers vortex is an exact 3D NS solution, and seen down its axis its streamlines **are** converging
spirals. The planar divergence is −α. The fluid that vanishes into the eye leaves **through the
page** along z = z₀e^{αt}. So the spiral is the visible footprint of the stretching term, which is
the only mechanism by which 3D could beat the 2D regularity proof.

The two eyes behave in opposite directions, and both are exact:
- **2D eye (Lamb–Oseen): it only opens.** r_c = √(4νt) grows, and ω_max = Γ/(4πνt) falls. Quadrupling
  the time doubles the eye. This is the proved-smooth world.
- **3D eye (Burgers): stretching closes it.** δ = √(4ν/α), so quadrupling the strain halves the eye and
  quadruples ω₀. That is "large scales to smaller ones", and here it is real. The open question is
  whether a flow can keep doing this to itself without end, in finite time, with nobody pushing.

**Why it is visually potent.** Viewers already own the whirlpool spiral: the plughole, Hokusai,
the Van Gogh sky. They believe it is a flat picture, and the mechanism breaks that belief. Every
inward-winding whirlpool is a 3D object. The flat version of a vortex is a set of rings. One glance
reads *rings versus spiral* with no caption, and the caption only has to say which is which. It also
reinterprets the reference honestly. The poster's hero is a converging spiral, and its inset "X"
is exactly the Burgers **side view**: the meridional streamlines r²z = C form a saddle at the axis.
So *spiral from above, saddle from the side, one stagnation point*. The poster's red-circled saddle
becomes the same point seen edge-on, not a second object.

**Abstract order:** **RADIAL / flow-to-an-attractor that is not a sink.** The whole family runs to
one point that swallows nothing. The attractor is an exit perpendicular to the sheet. Its paired
counter-order is **NESTED rings**: the 2D vortex as concentric equal-Δψ isolines.

**The twist, and the lineage (Bridget Riley, *Blaze 1*, 1962, Scottish National Gallery).** The
NGS text: "Although it appears to be a spiral, *Blaze 1* is formed from a succession of concentric
circles made of zigzags". The eye invents a vortex that is not there. The plate answers Riley
exactly. In the plane, a vortex really **is** concentric circles, and any spiral you see is an
illusion, as in *Blaze*. Only the third dimension makes the spiral real. The order taken from Riley
is one line family whose phase or spacing drift makes the surface move, with no figure drawn. Riley's
*Current* (1964) is the fallback reference if the translator wants the laminar reading.

### (b) THE LADDER THAT WOULD HAVE TO FINISH — one vortex at scales 1, ½, ¼ … ★ RANK 2

**The relationship.** Under NS scaling λ = 2, a Burgers vortex maps **exactly** onto another Burgers
vortex with the same Γ: δ → δ/2, α → 4α, ω₀ → 4ω₀, and a congruent spiral (same Re_Γ, same pitch).
The equations cannot tell the rungs apart except by size. A finite-time blow-up of self-similar
type means **sliding down this ladder in finite time**. Rung n lasts T₀·4⁻ⁿ, so the whole ladder
takes **4/3·T₀**. Each rung contributes the same ∫ω dt (ω ∝ 4ⁿ, duration ∝ 4⁻ⁿ), so infinitely many
rungs make ∫sup|ω|dt diverge, which is exactly the BKM signature.

This is the structure the 2026 claim describes. Its core is "self-similar", "fluid spirals inward
toward the axis" with "axial outflow" (Burgers-like). The radius is ℓ_r ≍ τ^{1/2} (the λ² ladder,
τ = 1−t), with ℓ_z ≍ τ^{1/2−h} and 0<h<1/100. Tao (2016) had already made an *averaged* NS blow up
by passing energy down a dyadic ladder (a Katz–Pavlović-type ODE system).

**Why it is visually potent.** The reference's zoom inset becomes a true statement: **the zoom
changes nothing**. It also carries its own honest limit. With δ₀ = 22 mm the rungs are 22, 11, 5.5,
2.75, 1.375 and **0.69 mm**, and rung 5 falls under the 0.8 mm pen floor. *The pen runs out of
resolution before the mathematics does.*

**Abstract order:** **NESTED / self-similar zoom.** It can be a sequence along a driving diagonal,
or rung n+1 drawn inside the blank eye of rung n. The second option is honest only if captioned as
*scaling copies*, never as one flow at one instant (§4). It composes naturally as the second read of (a).

### (c) THE CASCADE RUNS BACKWARDS IN THE PLANE — a solved 2D field coarsening ★ RANK 3

**The relationship.** Seeded 2D decaying turbulence, as a pseudo-spectral vorticity solve. Like-sign
vortices merge and the count falls. The energy spectrum's centroid moves to **lower** k: this is the
**inverse energy cascade** (Kraichnan 1967, Phys. Fluids 10:1417–1423, E ∝ k^{−5/3} with a
*backward* energy transfer). Enstrophy goes forward into thin filaments. Streamlines are ψ-isolines.

**Why it is visually potent.** The reference's caption "large scales to smaller ones" is **false in
2D for energy**. The one dimension where regularity is proved runs the cascade backwards. A
Nees-*Schotter* reversal would put many small eddies at the top of the sheet and few large ones at
the bottom.

**Abstract order:** **LAMINAR / stratified coarsening**, order out of disorder down the sheet.

**Cost and weakness.** It needs a real solve. A 256² run is minutes on an idle machine, but my
check run on today's load-400 machine did not finish, so no seeded numbers are quoted here. The
designer must generate them and record the seed. Its weakness is that it shows what 2D does, not
the 3D mechanism, so it can only be the counter-panel to (a), never the plate on its own.

*Not ranked.* Kolmogorov −5/3 drawn as a slope, any axis chart of energy spectra, a "Navier–Stokes
equation" typeset as the image, the 2026 paper's Figure 1 (it is explicitly a schematic: "this
difference is exaggerated in the schematic"), and curl-noise or decorative swirl fields.

---

## 3. Real data — verified

No dataset: **exact closed-form solutions** plus the primary texts. Every formula was checked in
`.venv/bin/python` (numpy only; E₁ by quadrature, checked against E₁(1) = 0.2193839344).

| item | source | verified how |
|---|---|---|
| Problem statement, alternatives (A)–(D), eqs. (1)–(11), BKM, 2D (Ladyzhenskaya) | C. L. Fefferman, *Existence and smoothness of the Navier–Stokes equation*, Clay official description — https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf | text extracted 2026-09-28; the (A)–(D) wording was read directly |
| 2026 claim: Thm 1.1 (smooth compactly-supported f, u(·,0)=0, bounded energy, lim sup‖u‖∞=∞ at t=1; (C) and (D) via Cor. 10.6); §2 physical description; ℓ_r≍τ^{1/2}, ℓ_z≍τ^{1/2−h}, 0<h<1/100, Re_θ≍τ^{−h}, core energy ≍τ^{1/2−3h} | OpenAI, *Finite time blowup for Navier–Stokes* — https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf ; Lean repo https://github.com/openai/NavierStokesAndEuler (also claims unforced **Euler** blow-up on R³) | PDF text extracted and read, 2026-09-28 |
| Clay's response, 11 Sep 2026 | https://www.claymath.org/news/navier-stokes-announcement/ ("apparently been settled", "deliberately unhurried") | fetched |
| Priority dispute (Buckmaster–Alpöge, 7 Sep), unverified status | https://en.wikipedia.org/wiki/Navier%E2%80%93Stokes_priority_controversy | fetched; this is a secondary source, so do not quote it on the sheet |
| Burgers vortex | J. M. Burgers, *A mathematical model illustrating the theory of turbulence*, Adv. Appl. Mech. 1 (1948) 171–199 | exact: steady ω-equation residual 3×10⁻⁸ (finite-difference floor); closed-form θ(s) vs RK4 path-line to 5 digits |
| Averaged-NS blow-up | T. Tao, *Finite time blowup for an averaged three-dimensional Navier–Stokes equation*, arXiv:1402.0290 (J. AMS 29, 2016) | abstract fetched |
| Euler with boundary | J. Chen & T. Y. Hou, arXiv:2210.07191 (v4 Aug 2026) | abstract fetched |
| Unstable singularities (ML + Gauss–Newton) | Y. Wang et al., *Discovery of unstable singularities*, arXiv:2509.14185 (Sep 2025) | abstract fetched |
| 2D inverse cascade | R. H. Kraichnan, Phys. Fluids 10 (1967) 1417–1423 | citation confirmed by search |
| Lineage | Bridget Riley, *Blaze 1* (1962), emulsion on board, National Galleries of Scotland — https://www.nationalgalleries.org/art-and-artists/159569 | fetched |

**How to compute the drawable geometry (designer).** Work in units of δ (hero rung δ₀ = 18–24 mm on A3).
Streamline k of N: θ_k(s) = 2πk/N + (Re_Γ/8π)[(1−e^{−s})/s + E₁(s)], r = δ√s, s from s_out = (R_out/δ)²
down to the eye. Implement E₁ without scipy: `np.trapezoid(np.exp(-x*np.exp(u)), u)` with u∈[0,14].
Alternatively, use Jobard–Lefebvre evenly spaced seeding (the engine has it) on the planar field
(u_r, v_θ). Every curve is then an exact streamline and termination handles the eye. Elevation:
r²|z| = C. Helix in oblique projection: (r₀e^{−αt/2}cos θ(t), r₀e^{−αt/2}sin θ(t), z₀e^{αt}).
2D rings: invert ψ(r) at equal Δψ.

**Recommended Re_Γ:** 50–200. At 100 the core wraps 1.27 turns per e-fold of radius (β₀ = 7.16°).
At 50 the spiral is more open (0.63 turns, 14.1°). At 200 it is tighter (2.53 turns, 3.6°) and the
blank eye grows to about 2.5 mm. State the chosen value in NOTES.

---

## 4. Simplifications allowed vs. lies

**Allowed (honest):**
- The plan view is the projection of 3D helices down the axis (z dropped). Say "seen down the
  stretching axis" once.
- Nondimensional units: δ is the unit, Re_Γ is stated in NOTES. Burgers extends to r→∞, so truncate
  at R_out ≈ 4–6 δ.
- Leave the eye **blank** below the pen floor (where the spacing of the spiral's own wraps drops
  under d_sep). That blank is the pen's resolution limit, which is the truth.
- Seed by rotated-copy arms (N equal shares of the axisymmetric inflow) or by Jobard–Lefebvre with
  termination. Both give exact streamlines.
- A ladder of rungs at a stated exact ratio (λ = 2, or any stated λ), captioned as the same solution at
  scales 1, 1/λ, 1/λ², … (NS scaling).
- Using the Burgers vortex as **the steady prototype** of the claimed 2026 core (inward spiral plus
  axial outflow), labelled as a prototype.
- 2D rings at equal Δψ, so ring spacing encodes speed (Δr = Δψ/v_θ), tightest at r = 1.121 r_c.
  Equal-radius rings are also acceptable if spacing is declared meaningless.
- Elevation as meridional streamlines r²z = C (swirl omitted) or as oblique helices.

**Lies (binding on everyone):**
1. **A converging spiral presented as a 2D or planar flow.** Impossible: planar ∇·u = 0 allows no sink.
2. **Spiral streamlines for the 2D vortex.** Lamb–Oseen streamlines are exact circles. The 2D panel
   must be rings.
3. **A 2D eye that shrinks with time.** r_c = √(4νt) only grows and ω_max only falls. The closing eye
   belongs to the 3D panel only.
4. **Calling Burgers a blow-up, a singularity, or a Clay counterexample.** It is steady, with bounded
   ω₀ = Γα/4πν, and has infinite energy (the strain grows linearly to ∞), so it lies outside the Clay
   class.
5. **Fake spirals.** Archimedean r = aθ, hand-tuned logarithmic spirals, `vortex_field`,
   Gaussian-swirled scanlines or curl noise may not be captioned as Navier–Stokes. Every curve must
   come from θ(s) or from integrating the stated field.
6. **Ladder geometry off the stated ratio**, or rungs with visibly different pitch. Congruence is
   the point. The 2026 core's tightening Re_θ ≍ τ^{−h} (h < 1/100) is at most **1.4% per λ=2 rung
   and ≤ 8.7% over 6 rungs**, invisible at pen scale. Drawing dramatically tightening rungs "to show
   blow-up" is a lie.
7. **Nested rungs presented as one flow at one instant.** They are scaling copies, or successive
   times in a hypothetical collapse. The caption must say which.
8. **Status lies.** "Unsolved / nobody knows" without the 2026 note. "Solved / proved" without
   "claimed, not yet verified". Implying that the forced result settles the unforced question.
   Captioning it an AI breakthrough "confirmed by Clay".
9. **"Large scales → smaller ones" on a 2D field.** In 2D, energy goes to larger scales.
10. **Marking a 2D saddle between two vortices as "where it breaks".** A saddle is a smooth strain
    point. In (a) the one special point is the axis stagnation point of a *3D* flow, which is also
    smooth in Burgers.
11. **"Turbulence is the unsolved problem."** See §5.

---

## 5. The misconception to quietly correct

**"The Navier–Stokes problem is that turbulence is too chaotic for the equations — we can't solve
fluids."** Every simulated turbulent flow is smooth. The Clay question asks something else: can a
smooth flow with finite energy produce **infinite velocity at a point in finite time**? Its
decisive fact is geometric. **In the plane this is proved impossible, because a 2D vortex can only
spread.** Its streamlines are circles and its eye only opens. So the question lives entirely in the
third dimension, in stretching.

The plate corrects a second belief without saying so: the whirlpool spiral everyone draws is a 3D
object. A flat vortex is rings, as in Riley's *Blaze*, where the spiral is only in your eye.

The second-order correction, for caption or NOTES only: the "cascade to small scales" is a 3D fact.
In 2D, energy goes the other way (Kraichnan 1967).

---

## 6. Pen-plotter fit

**Naturally a LINE here:**
- **Streamlines.** Burgers is steady, so streamline = path-line = closed form. One stroke per arm,
  from R_out to the eye. At Re_Γ = 100, δ₀ = 22 mm, R_out = 5δ₀, an arm is **300 mm** long and
  makes **3.39 turns** down to the 1.83 mm eye. That was computed by summing θ(s) over 4000
  geometric radii. That is a good batch unit, with no stroke longer than one arm.
- **2D rings.** ψ-isolines, closed circles, one stroke each.
- **The side view.** Hyperbolas r²|z| = C (or helices in oblique projection, tightening as
  r = r₀√(z₀/z)). The axis itself is the straight vortex line (ω is purely axial).
- **Not lines:** vorticity fields, pressure, speed shading. If speed must show, it shows through
  ring spacing (equal Δψ) or spiral spacing, never as hatching.

**Density risks:**
- **The eye floods.** With rotated-copy arms the perpendicular spacing is (2πr/N)·sin β → 0 as r → 0.
  Terminate by spacing. A single arm's successive wraps sit ≥ d_sep apart only for
  r ≥ d_sep/(1−e^{−2π tan β₀}). At Re 100 that is **1.47 mm (d_sep 0.8)** and 1.83 mm (d_sep 1.0).
  Maximum arms that fit at d_sep = 1 mm with δ = 22 mm: about 27 at r = δ, 10 at δ/2, 4 at δ/4.
  Jobard–Lefebvre does this for free.
- **Far field.** Burgers arms are almost radial outside 3δ (β = 48.5° at 3δ, 72° at 5δ for Re 100),
  so they converge like spokes. Spacing is fine outside and tightens only inside δ.
- **2D rings.** Equal-Δψ rings crowd at r = 1.121 r_c. Choose Δψ so that gap is ≥ 0.8 mm (≥ 1.2 mm
  preferred).
- **Field length.** A J–L disc of radius R at spacing d costs about πR²/d of line. For R = 110 mm
  that is **47.5 m at 0.8 mm, 31.7 m at 1.2 mm, 23.8 m at 1.6 mm, 15.8 m at 2.4 mm**. At Leo's
  F600 (10 mm/s): **79 / 53 / 40 / 26 min**, plus pen cycles. Recommend d_sep 1.6–2.4 mm in the
  field. That is Riley's spacing, not an engraving's. Tighten only where the physics tightens.

**Must stay blank paper:**
- The eye of every spiral, below the resolution floor. Say so; it is the pen's honest limit.
- The eye of the 2D vortex, where ψ is flat. At equal Δψ, the rings are widest there.
- A generous silence between the 2D (rings) and 3D (spiral) statements, so the eye compares them.
  The two must not merge into one texture.
- Around the title and the status stamp.

**Suggested pen meanings.** Suggestion only; the translator owns the encoding.
- **Layer 1, blue:** the 3D Burgers streamlines. This is the dominant mass.
- **Layer 2, black hairline:** the 2D rings, the side view, and the type.
- **Layer 3, red (scarce, loud):** the one open point, the axis stagnation point / eye, plus the
  dated status stamp. At most a few strokes.

Order: blue → black → red (dark after light, and the accent last so it is never overdrawn).
Each layer is streamed once, with strokes ordered by angle within the layer, so there is no
sheet-crossing travel.

---

## 7. Check numbers

Units: δ = 1, ν = 1 unless stated. Default plate: Re_Γ = Γ/ν = 100, δ₀ = 22 mm. Every line was run
in `.venv/bin/python` (numpy only). Helper: `E1=lambda x: np.trapezoid(np.exp(-x*np.exp(np.linspace(0,14,400001))), np.linspace(0,14,400001))`.

| # | quantity | value | one-liner |
|---|---|---|---|
| C1 | radius of max swirl / core scale (Burgers r/δ, and Lamb–Oseen r/r_c) | **1.12091** (s = 1.25643) | Newton on `1+2s-exp(s)=0`, then `sqrt(s)` |
| C2 | max swirl speed | **v_max = 0.63817·Γ/(2πδ)** | `(1-exp(-s))/sqrt(s)` at s = 1.25643 |
| C3 | core spiral pitch (log spiral) | dθ/d ln r = −Re_Γ/4π = **−7.9577 rad = 1.2665 turns per e-fold**; tan β₀ = 4π/Re_Γ = 0.12566, **β₀ = 7.162°** | `100/(4*np.pi)`, `degrees(arctan(4*pi/100))` |
| C4 | closed-form streamline vs integration | start r₀ = 3δ, αT = 4: **r = 0.406006δ, turned angle 8.73230 rad**. RK4 and θ(s) agree to 5 digits | θ(s) above; `3*exp(-2)` = 0.406006 |
| C5 | planar divergence of the plan-view field | **−α** (2D Lamb–Oseen: **0**). A converging spiral ⇔ nonzero | `(1/r) d(r·(−αr/2))/dr = −α` |
| C6 | peak vorticity | **ω₀ = Γα/(4πν) = Γ/(πδ²)**; Re 100, α = ν = 1: 7.95775 | `100/(4*np.pi)` |
| C7 | ladder λ = 2 | δₙ = δ₀/2ⁿ, ω₀ × 4ⁿ, rung time T₀·4⁻ⁿ, cumulative **→ 4/3·T₀** (1.33325 after 7 rungs). δ₀ = 22 mm → **22, 11, 5.5, 2.75, 1.375, 0.6875 mm**. **Rung 5 is below the 0.8 mm floor** | `[22/2**n for n in range(6)]`, `sum(4.**-k for k in range(7))` |
| C8 | Burgers dissipation per unit length (swirl) | **Γ²α/(8π), independent of ν.** The integral ∫[e^{−s}−(1−e^{−s})/s]²ds = ½ exactly (½ − 2ln2 + 2ln2). Numerics 0.49966, with the truncated 1/s tail | Frullani + ∫(1−e^{−s})²/s² = 2 ln 2 |
| C9 | 2D eye | r_c = √(4νt): **t × 4 ⇒ eye × 2**; ω_max = Γ/(4πνt), **t × 2 ⇒ halves**. Equal-Δψ rings (24 rings, 0.05–4 r_c) have their **tightest gap at r ≈ 1.12 r_c** | invert ψ = (Γ/4π)[ln s + E₁(s)] |
| C10 | 2026 claim (text of Thm 1.1 / §2) | forced (f ∈ C_c^∞), u(·,0) = 0, blow-up at **t = 1**, bounded energy; alternatives **(C)+(D)**; ℓ_r ≍ τ^{1/2}; Re_θ ≍ τ^{−h} with h < 1/100 ⇒ **≤ 1.40% per λ=2 rung** (4^{0.01} = 1.0140), **≤ 8.7% over 6 rungs** (4^{0.06} = 1.0867). Status: **claimed, unverified**; Clay 11 Sep 2026 "apparently been settled", no award; **unforced (A)/(B) unresolved** | `4**0.01`, `4**0.06` |
| C11 | inner-spiral blank eye (single arm, wraps ≥ d_sep) | Re 100: **1.465 mm** (d 0.8), 1.832 mm (d 1.0); Re 200: 2.453 mm (d 0.8) | `d/(1-exp(-2*pi*4*pi/Re))` |
| C12 | turns from 5δ to 0.5δ | Re 50: 0.598; **Re 100: 1.196**; Re 200: 2.393 | θ(0.25) − θ(25), divided by 2π |
| C13 | one arm, Re 100, δ₀ = 22 mm, 5δ₀ → 1.83 mm eye | **300 mm, 3.39 turns** (one batchable stroke) | polyline length of r·(cos θ, sin θ) over `geomspace(110, 1.83, 4000)` |

What a critic measures off the render and gcode: the spiral arms' pitch inside the core (C3: about
7° to the circle at Re 100), rung ratios exactly 2:1 (C7), 2D rings closed and concentric (C5,
lie 2), minimum gcode spacing ≥ 0.8 mm near the eye (C11), and the status stamp wording (C10).
