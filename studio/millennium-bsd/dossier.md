# millennium-bsd — Birch and Swinnerton-Dyer: one point, one crossing — zero means infinitely many
**Field expert:** mathematics (arithmetic geometry, elliptic curves) · **Date:** 2026-09-28 · **Status:** dossier v1

Plate 7 of the MILLENNIUM series. Reference: `ref/reference.png` (AI poster, an interpretation
brief, not ground truth). It gets the curve right (y² + y = x³ − x **is** Cremona 37a1, verified)
and gets **six** things wrong, listed in §4. Every number below was computed here, in
`.venv/bin/python`, and cross-checked against LMFDB 37.a1 / 11.a2 / 389.a1 / 5077.a1.
Reproduce with `studio/millennium-bsd/data/verify_bsd.py` (≈12 s, `--edsac` adds the Euler
product). Exact orbit + L table: `data/curve_37a1.json`.

Sibling plates checked (`grep` of `studio/millennium-*/dossier.md`, pieces/): nothing in the
collection draws an elliptic curve or an L-function at s = 1. Two near-neighbours to stay clear of:
**millennium-riemann** draws where ζ's zeros *lie* (a vertical line, Re s = ½) — this plate is about
the *order* of one zero at one point on the real axis, and that zero is *forced*. **millennium-hodge**
RANK 1 is a pencil of straight strings on a hyperboloid — the chord pencil here also converges on a
point, so the designer must not let it read as the same string-art (see §6). Lineages already taken:
LeWitt (Riemann), Riley *Blaze 1* (Navier–Stokes), Mohr (P vs NP), Gabo (Hodge), Kandinsky
(Yang–Mills). This plate proposes **Morellet** (§2a).

---

## 1. The phenomenon (≤5 lines)

A cubic curve E over ℚ has a group of rational points: draw a line through two of them and the
third intersection is rational too (chord-and-tangent). Mordell: E(ℚ) ≅ ℤ^r ⊕ T, finitely
generated; r is the **rank**. From the primes one builds an analytic function L(E,s) = ∏_p (local
point count at p). BSD: **r = ord_{s=1} L(E,s)**, and the leading coefficient is an exact product
of geometric invariants. For 37a1 one point P = (0,0) generates infinitely many, and L vanishes to
order exactly 1 at s = 1 — proven for this curve (Gross–Zagier + Kolyvagin, rank ≤ 1 case).

### Governing math

- **The curve.** E: y² + y = x³ − x, a-invariants [0,0,1,−1,0], conductor N = 37, Δ = 37,
  j = 110592/37. Completing the square: (2y+1)² = f(x) := 4x³ − 4x + 1.
- **Real locus.** f has three real roots e₃ = −1.1071599, e₂ = 0.2695944, e₁ = 0.8375654 (Δ > 0 ⇒
  **two components**): a closed **egg** over x ∈ [e₃, e₂] and an unbounded **branch** over
  x ≥ e₁. **Nothing** for e₂ < x < e₁. Mirror axis y = −½ (not y = 0). Egg height
  y ∈ [−1.296806, +0.296806], extremes at x = −1/√3.
- **Group law.** O = point at infinity. −(x,y) = (x, −1−y) (reflection in y = −½).
  P + Q: λ = (y₂−y₁)/(x₂−x₁) (or (3x₁²−1)/(2y₁+1) for doubling), x₃ = λ² − x₁ − x₂,
  y₃ = −(λx₃ + y₁ − λx₁) − 1. Three collinear points sum to O.
- **Mordell–Weil.** E(ℚ) = ℤ·P, P = (0,0), torsion trivial. First multiples (exact):
  P (0,0) · 2P (1,0) · 3P (−1,−1) · 4P (2,−3) · 5P (1/4,−5/8) · 6P (6,14) · 7P (−5/9, 8/27) ·
  8P (21/25, −69/125) · 9P (−20/49, −435/343) · 10P (161/16, −2065/64).
  **Odd multiples lie on the egg, even multiples on the branch** (P is on the egg, the egg is the
  non-identity coset of E(ℝ) ≅ ℝ/ℤ × ℤ/2).
- **Heights.** Denominator of x(nP) is W_n² where W_n is the elliptic divisibility sequence
  1,1,1,1,2,1,3,5,7,4,23,29,59,129,314,65,1529,… (OEIS A006769, Somos-4:
  W_n W_{n−4} = W_{n−1}W_{n−3} + W_{n−2}², up to sign). Canonical height
  ĥ(P) = lim h(x(nP))/n² = **0.05111140824** (h = log max(|num|, den)); digits grow
  **quadratically**: den x(100P) has 221 digits, x(200P) 887.
- **Real period.** Ω₀ = π / AGM(√(e₁−e₃), √(e₁−e₂)) = 2.9934586462 per component;
  Ω_E = 2Ω₀ = **5.9869172925** (LMFDB's convention, counts both components).
- **Orbit as a rotation.** Elliptic log on the identity component, z(Q) = ∫_x^∞ dt/√f(t)
  (Ω₀ − that when 2y+1 < 0), measured in turns u = z/Ω₀: u(2kP) = k·θ mod 1 with
  **θ = 0.378917282552** (irrational ⇔ P non-torsion). The egg orbit is the same rotation run
  backwards from u(P) = 0.310541 (in the egg parametrisation ∫_{e₃}^x dt/√f). Continued fraction
  θ = [0; 2, 1, 1, 1, 3, 2, 1, 2, 1, …] ⇒ three-gap theorem: the first K points on a component
  split it into ≤ 3 distinct gap lengths.
- **Invariant measure.** The orbit equidistributes in the Haar measure, which per unit arclength is
  **ds/|∇F|**, F = y² + y − x³ + x. So points crowd where |∇F| is small (egg right tip 1/|∇F| =
  1.279; egg left tip 0.374; branch at (1,0) 0.447; at (6,14) 0.0090; at (10.06,−32.3) 0.0032) —
  the orbit rarely escapes up the branch, but it does, arbitrarily far.
- **L-function.** a_p = p + 1 − #E(𝔽_p) (a₂…a₁₃ = −2, −3, −2, −1, −5, −2; a₃₇ = −1, non-split
  multiplicative). L(E,s) = ∏_{p∤37}(1 − a_p p^{−s} + p^{1−2s})^{−1} · (1 + p^{−s})^{−1}|_{p=37},
  absolutely convergent only for Re s > 3/2. Modularity continues it: Λ(s) = 37^{s/2}(2π)^{−s}Γ(s)L(E,s)
  satisfies **Λ(2−s) = −Λ(s)** (root number ε = −1; ε = +1 fails to reproduce the Dirichlet series at
  s = 3: 0.73809 vs 0.68343). Computed on the real line by the smoothed series
  Λ(s) = Σ a_n[(√37/2π)^s n^{−s} Γ(s, 2πn/√37) + ε(√37/2π)^{2−s} n^{s−2} Γ(2−s, 2πn/√37)].
- **The zero.** Λ is odd about s = 1 ⇒ L(E,1) = 0 is **forced by the sign**.
  L′(E,1) = 2Σ a_n/n · E₁(2πn/√37) = **0.3059997738** (LMFDB 0.30599977383405).
- **BSD formula, exact for this curve:** L′(E,1) = Ω_E · Reg · #Ш · ∏c_p / #T² =
  5.98691729 × 0.05111140824 × 1 × 1 / 1 = **0.3059997738** (agreement 1 − 2·10⁻¹⁵ with LMFDB Reg).
  **The slope of the crossing is the circumference of the real curve times the height of the generator.**

---

## 2. Three candidate visual truths (ranked)

### (a) ZERO MEANS INFINITY — one point's orbit on the curve, one forced crossing on the line ★ RANK 1

**The relationship.** Two exact objects and the exact identity that binds them:

1. *Geometry.* The whole of E(ℚ) is the orbit {nP : n ∈ ℤ} of one point, built by one rule:
   **draw the line through P and nP; it meets E once more at −(n+1)P; reflect in y = −½ to get
   (n+1)P.** Every chord passes through the single point P = (0,0) — a pencil. The orbit hops
   egg → branch → egg (odd/even), turns each component by the irrational angle θ = 0.378917 per
   two steps, never closes, fills both ovals densely in the measure ds/|∇F|, and every so often
   flings a point far up the branch (6P at (6,14), 10P at (10.06,−32.27), 16P at (113.6, 1210.8))
   while its coordinates' digit strings lengthen as n² (ĥ = 0.0511).
2. *Analysis.* L(E,s) on the real segment [0,2] is **point-symmetric** about (1,0) (in Λ-form):
   it starts at a trivial zero at s = 0, stays **negative** on (0,1) (minimum −0.08924 at s ≈ 0.478),
   **crosses** zero at s = 1 with slope 0.30600, and rises to +0.38158 at s = 2. One crossing, not a
   bounce.
3. *The bridge.* slope at the crossing = Ω_E × ĥ(P) — the invariant length of the real curve times
   the growth rate of the orbit's digits. The angle is arctan(0.30600) = **17.014°** when s and L
   share one mm scale.

**The twist.** Everyone holds "zero = nothing". Here the analytic function vanishes *because*
there are infinitely many rational points; a curve with finitely many (rank 0, e.g. 11a1,
L(1) = 0.25384) has L(1) ≠ 0. **Zero is the fingerprint of infinity** — and the second joke: the
sign of the functional equation makes L odd about s = 1, so it *cannot avoid* zero: an odd function
must cross its centre. Parity forced the rank to be odd before a single point was found.

**Why visually potent.** Everything is a straight line or a single exact curve — perfect pen
material. The pencil through one point is a hub with a load: the one gold point from which every
other rational point on the sheet is ruled. The orbit's density law (thick at the egg's right tip,
thinning to nothing up the branch) is a free, *true* tone gradient. The crossing at 17.0° is one
loud diagonal — the only thing on the analytic side that matters.

**Abstract order: ORBITAL (an irrational rotation on two circles, alternating by parity) seeded
from a RADIAL pencil through one point** — the analytic half is a single point-symmetric line
through a centre. Suggested lineage: **François Morellet, *Répartition aléatoire de 40 000 carrés
suivant les chiffres pairs et impairs d'un annuaire de téléphone* (1961, 80 × 80 cm, 50 %/50 %
two colours)** — the ORDER taken is *a number sequence's parity deciding which of two families each
mark joins*: here n odd → egg, n even → branch, and ε = (−1)^rank. Not his look (squares), his rule.

**Weakness.** Two halves (curve | line) invite the reference's "diagram + graph side by side".
The translator must make the two halves one construction (e.g. the crossing at 17° sharing the
chord pencil's angular vocabulary, or the s-axis laid on the mirror line y = −½), not a figure pair.

### (b) THE MACHINE THAT SAW IT — the Birch–Swinnerton-Dyer Euler product, prime by prime ★ RANK 2

**The relationship.** The conjecture was *discovered* on EDSAC 2 at Cambridge (Birch &
Swinnerton-Dyer, *Notes on elliptic curves II*, J. reine angew. Math. 218 (1965)) by counting
points mod p and multiplying: ∏_{p≤X} N_p/p ~ C·(log X)^r. For 37a1 (computed here, p ∤ 37):

| X | ∏ N_p/p | ÷ log X |
|---|---|---|
| 10² | 30.573 | 6.639 |
| 10³ | 45.685 | 6.614 |
| 10⁴ | 74.746 | 8.115 |
| 3·10⁴ | 89.792 | 8.710 |
| 10⁵ | 92.320 | 8.019 |

Exponent 1 = rank; the ratio wanders toward Goldfeld's constant √2·e^γ / L′(1) = 8.2314 —
notoriously slowly. Each prime is a finite-field "shadow" of the curve: #E(𝔽_p) = p + 1 − a_p,
|a_p| ≤ 2√p (Hasse; 0 violations for p < 10⁵), and the angles θ_p = arccos(a_p/2√p) follow
Sato–Tate (E[cos²θ] = 0.2489 → ¼ over 9 591 primes; 37a1 is non-CM). Rational points *inflate*
N_p (every rational point reduces to a point mod p), which is exactly why the product grows.

**Why potent.** It is the real "flow between geometry and analysis" — the gold threads the
reference drew, made honest: one thread per prime, each carrying N_p/p. And the lineage is the
plotter's own: a 1960s computer found this by printing numbers. **Order:** LAMINAR /
flow-to-attractor — strands (one per prime) whose cumulative product climbs a straight line in
log-log. Lineage: **Georg Nees, *Schotter* (c. 1968)** — a controlled drift down the sheet.
**Weakness:** easily becomes a log-log plot (a figure); convergence is ugly and non-monotone,
which is honest but hard to make legible.

### (c) ORDER OF CONTACT — the rank ladder 0, 1, 2, 3 at s = 1 ★ RANK 3

**The relationship.** Four real curves, their L-functions near s = 1:
11a1 (r = 0) **misses** the axis, L(1) = 0.253842; 37a1 (r = 1) **crosses**, slope 0.306000;
389a1 (r = 2) **kisses** from above, L″(1)/2 = 0.759317, L(0.5) = +0.20995; 5077a1 (r = 3)
**crosses flat**, L‴(1)/6 = 1.73185 (LMFDB 1.7318499), L(0.5) = −0.49206. Root number
(−1)^r: mirror-symmetric Λ for even rank, point-symmetric for odd.

**Why potent:** the order of vanishing *is* the order of contact of a line with an axis — a pure
geometric idea every eye reads. **Order:** STRATIFIED/nested — four strata, one contact each.
Lineage: **Frieder Nake, *Hommage à Paul Klee* (1965)** — horizontal strata each carrying its own
bounded line. **Weakness:** it is four function graphs; without a transposition it is a textbook
figure (fails § 6 outright). Only viable as a sub-element of (a) (e.g. a margin ladder).

---

## 3. Real data — verified

All computed here (pure numpy + `fractions`; no PARI/Sage available), then checked against LMFDB:

| quantity | computed here | LMFDB (fetched 2026-09-28) |
|---|---|---|
| 37a1 a-invariants, N, Δ, j | [0,0,1,−1,0], 37, 37, 110592/37 | https://www.lmfdb.org/EllipticCurve/Q/37/a/1 — same |
| generator, torsion | (0,0), trivial | same |
| Reg = ĥ(P) | 0.051111408 (h(x(2¹⁰P))/4¹⁰) | 0.051111408239968840 |
| Ω_E | 5.986917292463918 (AGM) | 5.9869172924639192 |
| L′(E,1) | 0.3059997738340524 | 0.30599977383405230 |
| Ш, c₃₇, #T | — | 1, 1, 1 |
| 11a1 L(E,1) | 0.25384186085591065 | 0.25384186085591068 (…/Q/11/a/2) |
| 389a1 L″(1)/2! | 0.7593165 | 0.75931650028842677 (…/Q/389/a/1) |
| 5077a1 L‴(1)/3! | 1.73189 (fit) | 1.7318499001193007 (…/Q/5077/a/1) |

(LMFDB's rendered "root number" line was mis-summarised by the fetch tool as +1; the sign used
here, ε = −1 for 37a1/5077a1 and +1 for 11a1/389a1, is fixed by reproducing the absolutely
convergent Dirichlet series at s = 3 to 10 digits: Σ_{n≤10⁵} a_n n⁻³ = 0.6834342901.)

- **EDS:** OEIS A006769, https://oeis.org/A006769 — matches |W_n| computed from √den x(nP) for n ≤ 24.
- **History/lineage facts:** Birch & Swinnerton-Dyer, J. reine angew. Math. 212 (1963) and 218 (1965);
  Gross–Zagier (Invent. Math. 84, 1986) + Kolyvagin (1988–90) prove BSD rank for analytic rank ≤ 1 —
  so for 37a1 "rank 1 = order 1" is a *theorem*, the Clay problem is the general case.
  Morellet 1961 series: e.g. Annely Juda Fine Art,
  https://www.annelyjudafineart.co.uk/artworks/38071-francois-morellet-repartition-aleatoire-de-40-000-carres-d-apres-les-1961/ ;
  Sotheby's 2023 lot (50 % bleu, 50 % rouge),
  https://www.sothebys.com/buy/fbb01a05-1290-4476-a6d7-cd1d99e7b7a8/lots/e8a471a3-d5ba-4173-a38e-c7c31083e3ed
- **How to compute:** `data/verify_bsd.py` (group law in Fractions; a_p by Legendre counting;
  Γ(a,x) by double-exponential Simpson, error < 2·10⁻¹⁴ vs closed forms). `data/curve_37a1.json`
  holds ±nP for n ≤ 30 (exact strings + floats + component), e_i, Ω, θ, ĥ, and L(E,s) at 81 points
  on [0,2].

---

## 4. Simplifications allowed vs. lies

**Allowed**
- Draw only a window of the real plane (e.g. x ∈ [−1.3, 2.6]); orbit points outside it may be
  represented by their chords running off the sheet edge (crop at frame) — the point exists, it is
  just far away.
- Draw the first K multiples (K ≈ 12–30) and ±n; say "…" in type, never imply the orbit ends.
- Draw L on [0,2] only (the critical strip's real segment) — or just a neighbourhood of s = 1.
- Plot Λ(s) instead of L(s) if the odd symmetry is the point (state which one is drawn).
- Independent vertical scaling of L vs s **only if** the 17.0° claim is dropped from the plate.
- Truncate digit strings in type with "…" once they pass a stated length (the length IS data).
- Use a curve with larger rank in a margin (§2c) as a foil, labelled by Cremona label.

**Lies (binding on everyone)**
1. **Points not on E.** The reference's (1,1) and (1,−2) are not on the curve (1+1 ≠ 0;
   4−2 ≠ 0). Every marked point must satisfy y² + y = x³ − x exactly; use `data/curve_37a1.json`.
2. **One connected wiggly curve.** E(ℝ) has **two** components with a gap for 0.2696 < x < 0.8376;
   the reference's dip joining them is false. The egg is closed; the branch is open.
3. **Symmetry about the x-axis.** The mirror is y = −½. Negation is (x,y) ↦ (x, −1−y).
4. **L large at s = 0 / positive left of 1.** L(E,0) = 0 (trivial zero) and L < 0 on (0,1).
5. **A V-bounce at s = 1.** A simple zero is a transversal **sign change**; a tangential touch is the
   picture of an even-order zero (rank 2, 389a1). The reference's cusp/V is a lie twice (no corners;
   no bounce).
6. **Decorative flow.** Gold threads that carry no quantity (the reference fans them from the
   non-point (1,1)) are banned. Any line joining the geometric and analytic halves must be an exact
   object: an Euler factor (§2b), the chord pencil, the crossing tangent, or the Ω × ĥ identity.
7. **Leftmost point (−1,0).** The egg's leftmost point is (e₃, −½) = (−1.10716, −0.5); (−1,0) = −3P is
   just above it. Don't label the tip as a rational point — the tips are irrational.
8. **Orbit as a closed polygon / periodic pattern.** The orbit never repeats (θ irrational); no
   n-fold symmetry, no evenly spaced beads.
9. **"Rank = how many points".** Rank 1 has infinitely many points; rank counts independent
   generators.
10. **Dirichlet series evaluated at s = 1.** Σ a_n/n is not how L(E,1) is defined; the value comes
    from analytic continuation (modularity). Don't write L(E,1) = Σ a_n/n on the plate.

---

## 5. The misconception to quietly correct

**"A zero means there is nothing there."** At s = 1 it means the opposite: L vanishes exactly when
the curve carries infinitely many rational points, and to the order of how many independent
directions they spread in. Secondary: people picture rational points as rare, isolated dots; the
orbit of one point is **dense** on the real curve while each point's coordinates grow
quadratically in digit length — dense in the plane, astronomically complex in arithmetic. The
plate should let a viewer see both: points pile up on the curve, digit strings lengthen in the type.

---

## 6. Pen-plotter fit

**Naturally a LINE here:** the two real components (one closed, one open curve); the chords of the
pencil through P (straight, exact); the negation step (a short vertical segment from −(n+1)P to
(n+1)P, bisected by y = −½); the single L curve and its crossing tangent; the mirror y = −½ as a
hairline. Points are small circles (≥1.2 mm Ø) or ticks across the curve, never filled blobs.

**Density risks (measured):**
- **The hub at P.** All chords go through (0,0). Minimum angular gap between chords n = 1..K:
  K = 6 → 11.31°, K = 10 → 4.48°, K ≥ 14 → 2.59°. At 0.8 mm spacing that needs a **void radius**
  around P of 4.1 mm (K = 6), 10.2 mm (K = 10), 17.7 mm (K ≥ 14) at plate scale — or end each chord
  at its two non-P points where P is not between them (e.g. n = 4, 7, 8, 11). The gold generator
  disc can occupy the void.
- **Chord spans explode.** Unclipped spans (plane units): n = 5, 6 ≈ 16; n = 9, 10 ≈ 34; K = 20 total
  2 573 units. Clip to the window; long chords crop at the frame (intended tension, not residue).
- **Orbit crowding.** In a window x ∈ [−1.2, 2.5], y ∈ [−3, 2], 152 of the first 200 multiples land
  inside; they bunch at the egg's right tip (1/|∇F| = 1.28) — the tick spacing there sets K.
- **Type as data.** Writing x(nP) exactly: cumulative digits n ≤ 12: 35, ≤ 16: 72, ≤ 20: 135,
  ≤ 24: 227, ≤ 30: 431; x(24P) = 4881674119706/5677664356225 (27 chars). A ragged-right block whose
  line lengths grow as n² is honest texture; cap it and state the cap.
- **Hodge collision.** Hodge's plate is also a pencil of straight lines. Differentiate: our lines
  all pass through ONE point and each skewers exactly two orbit points of index sum −1; no ruling
  surface, no envelope curve.

**Must stay blank paper:** the gap 0.2696 < x < 0.8376 between the components (it is the most
common lie — let it be visibly empty); the interior of the egg except chords genuinely crossing
it; the region between L and the axis (no hatching under the curve — a hatch is a plot).

**Plotting (Leo, batched plate jobs).** Suggested meanings: black fine (real locus, chords,
negation ticks, type) · gold (P, the crossing at s = 1, the Ω·ĥ bridge — scarce). A second
neutral only if parity is carried by pen rather than by position (not needed: position already
carries parity). Order: black hairline first, gold last so the accent sits on top. Scale guide: at
45 mm/unit the egg is 208 mm of line (perimeter 4.6170 units), the branch in x ≤ 2.5 is 362 mm
(8.0552 units); at F600 (10 mm/s) each metre of ink ≈ 1.7 min plus pen-cycle dwells.

---

## 7. Check numbers

| # | value | reproduce |
|---|---|---|
| 1 | Marked points satisfy y²+y = x³−x: P..8P = (0,0),(1,0),(−1,−1),(2,−3),(1/4,−5/8),(6,14),(−5/9,8/27),(21/25,−69/125); (1,1),(1,−2) do **not** | `verify_bsd.py` lines 1–9 |
| 2 | Real roots of 4x³−4x+1: −1.10716, 0.26959, 0.83757; mirror y = −½; egg y ∈ [−1.29681, 0.29681]; empty band 0.2696 < x < 0.8376 | bisection on f; y = (−1 ± √f(−1/√3))/2 |
| 3 | Odd nP on the egg (x ≤ 0.2696), even nP on the branch (x ≥ 0.8376) | `verify_bsd.py` component column |
| 4 | Chord through P and nP meets E at −(n+1)P, e.g. line y = 0 through −3P = (−1,0), P, 2P; tangent at P is y = −x, meets (1,−1) = −2P | slope of line through (0,0),(x,y) |
| 5 | ĥ(P) = 0.051111408; den x(100P) has **221** digits (≈ ĥ·10⁴/ln 10 = 222.0) | `verify_bsd.py` |
| 6 | Rotation θ = 0.378917283 per 2P (6P at u = 0.136752, 4P at 0.757835); CF [0;2,1,1,1,3,2,…] | ∫_1^∞ dt/√(4t³−4t+1) ÷ Ω₀ |
| 7 | Ω₀ = 2.993458646, Ω_E = 5.986917292 | π/AGM(√(e₁−e₃), √(e₁−e₂)), ×2 |
| 8 | L(E,1) = 0, L′(E,1) = 0.3059997738 = Ω_E·Reg; crossing angle 17.014° at equal s/L scale | `verify_bsd.py`; atan(0.306) |
| 9 | L on [0,2]: L(0) = 0, min −0.08924 at s ≈ 0.478, L(0.5) = −0.089049, L(1.5) = +0.183965, L(2) = +0.381575; Λ(1.5) = −Λ(0.5) = 0.155297; L′(0) = −(37/4π²)L(2) = −0.35762 | `verify_bsd.py`, `data/curve_37a1.json` |
| 10 | a₂,a₃,a₅,a₇,a₁₁,a₁₃ = −2,−3,−2,−1,−5,−2 → N_p = 5,7,8,9,17,16; ∏_{p≤10⁴} N_p/p = 74.746 (÷ log X = 8.115; Goldfeld C = 8.2314) | `verify_bsd.py --edsac` |
| 11 | Rank ladder at s = 1: 11a1 L = 0.253842 (miss) · 389a1 L″/2 = 0.759317, L(0.5) = +0.2100 (kiss) · 5077a1 L‴/6 = 1.73185, L(0.5) = −0.4921 (flat cross) | `Lfun('389a1').L(0.5, +1)` etc. in `data/lfun_lib.py` |
