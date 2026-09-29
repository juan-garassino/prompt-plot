# millennium-hodge — the Hodge conjecture: a circle is two straight lines

**Field expert:** mathematics (algebraic geometry) · **Date:** 2026-09-28 · **Status:** dossier v1

**Brief.** Plate 5 of the MILLENNIUM series. The reference (`ref/reference.png`, an AI poster)
has the right atmosphere and the wrong mathematics. Its hero is a hand-swept twisted ribbon that
is not any variety. Its blue/gold split claims blue = "Hodge structure" and gold = "algebraic
cycles", but a Hodge structure is not a surface. Its row "C0 sphere, C1 torus, C2 genus-2, C3,
C4" and its "Σ aᵢCᵢ = [Z]" are overlapping blobs that are not cycles on anything. Keep the
premise ("can the invisible be built?") and its restraint (cream, blue + gold, fine line). Replace
every form with a real one. The honest move is this: **you can only draw where the conjecture is
already a theorem, so draw a theorem, exactly, and say that the open part cannot be seen.**

---

## 1. The phenomenon (≤5 lines)

Take X, a smooth complex projective variety. Its rational cohomology splits by complex type,
H^k(X,ℂ) = ⊕_{p+q=k} H^{p,q}. A *Hodge class* is a rational class that lies entirely in the
middle piece H^{p,p}. Every complex subvariety of codimension p gives such a class. The conjecture
says the converse holds: **every rational Hodge class is a ℚ-linear combination (fractions and
differences allowed) of classes of subvarieties.** Topology proposes the class and geometry has
to build it. The case p = 1 is a theorem, Lefschetz (1,1) of 1924. So is every variety of dimension ≤ 3.
It is open from codimension-2 classes on 4-folds upward, which is real dimension 8, and nobody can draw that.

### Governing math

- **Statement (Clay, P. Deligne; wording as on Wikipedia):** "Let X be a non-singular complex
  projective manifold. Then every Hodge class on X is a linear combination with rational
  coefficients of the cohomology classes of complex subvarieties of X."
  Hodge classes: Hdg^p(X) = H^{2p}(X,ℚ) ∩ H^{p,p}(X).
- **Known:** p = 1 (Lefschetz (1,1): every class in H²(X,ℤ) ∩ H^{1,1} is the class of a divisor);
  dim X ≤ 3 (hard Lefschetz moves the result to degree 2n−2); many abelian varieties; abelian
  fourfolds of Weil type (Markman, arXiv:2502.03415 v2, Jun 2025, preprint; separately
  Floccari–Fu for discriminant 1).
- **False variants (why the statement says ℚ and "projective"):** integral coefficients fail
  (Atiyah–Hirzebruch, torsion classes; Totaro 1997; Kollár). Compact Kähler instead of projective
  fails (Voisin 2002).
- **The drawable instance — the smooth quadric surface Q ≅ ℙ¹×ℙ¹.** Its real form is the
  hyperboloid of one sheet
  **x² + y² − z² = 1**, carrying two families of straight lines (rulings):
  - A (blue): **A(α,s) = (cos α − s sin α, sin α + s cos α, s)**
  - B (gold): **B(β,s) = (cos β + s sin β, sin β − s cos β, s)**

  Here α, β ∈ S¹ is where the string crosses the waist circle, and s = z.
  H²(Q,ℤ) = ℤ[A] ⊕ ℤ[B] with intersection form [A]² = [B]² = 0 and [A]·[B] = 1.
  h^{2,0} = 0, so H² = H^{1,1}: **every** class is a Hodge class, and every class is built from
  the two strings. This is the conjecture holding, visibly, on one surface.
- **Coordinates on the torus.** Every point lies on exactly one A-string and one B-string:
  P(α,β) = A(α, tan((β−α)/2)). The projective real hyperboloid is therefore the torus S¹×S¹.
  β − α = π is the conic at infinity.
- **Curves of class a[A] + b[B]** (bidegree (a,b)). A curve of this class meets every A-string b
  times and every B-string a times, and every plane a + b times.
  - (1,1) = the plane sections (conics). The horizontal circles z = c are α ↦ (α, α + 2 arctan c).
  - (p,q) with gcd(p,q) = 1 is the rational curve **α = q·u, β = p·u, u ∈ [0,2π)**, a (p,q)
    torus curve. Implicit form, with t = tan(α/2) and t′ = tan(β/2):
    **Im[(1+it)^p (1−it′)^q] = 0**, a real polynomial of bidegree (p,q). Its real locus is exactly
    that one closed curve.
  - (1,2) = twisted cubic, (2,3) = rational quintic of arithmetic genus 2.

  Self-intersection 2pq, degree p+q, arithmetic genus (p−1)(q−1).
- **The pencil that squares the circle.** Rotate a plane about the tangent line ℓ = {x=1, z=0}:
  **z = tan ψ · (x − 1)**, ψ ∈ [0°, 90°]. Every member is a (1,1) curve through p = (1,0,0),
  tangent to ℓ there.
  - ψ = 0: the waist circle.
  - 0 < ψ < 45°: ellipses.
  - ψ = 45°: a parabola.
  - 45° < ψ < 90°: hyperbolas.
  - ψ = 90°: the tangent plane x = 1, which cuts the surface in y = ±z. That is exactly
    **A(0) ∪ B(0), two straight strings crossing at p**.

  One continuous algebraic family carries the circle into the pair of lines, so in cohomology
  **[circle] = [A] + [B]**.
- **Rank-3 instance — Clebsch diagonal cubic:** in ℙ⁴, Σxᵢ = 0 and Σxᵢ³ = 0 (Clebsch 1871).
  All **27 lines are real**:
  - 15 lines are S₅-images of (a : −a : b : −b : 0).
  - 12 lines involve the golden ratio. One passes through (0 : 1/φ : −1/φ : 1 : −1) and
    (−1/φ : 0 : 1 : −1 : 1/φ); the other 11 are its S₅-images.

  H² has rank 7 (χ = 9), h^{2,0} = 0, and the line classes span H²(ℤ).

---

## 2. Three candidate visual truths (ranked)

### (a) A circle is two straight lines — the pencil on the string hyperboloid ★ RANK 1

**Relationship.** On x²+y²−z²=1, drawn only as its two rulings (blue A, gold B), one plane turns
about the tangent line ℓ. It cuts circle → ellipses → parabola (ψ=45°) → hyperbolas → at ψ=90° the
**X of one blue and one gold string**. Every member has the same class h = [A]+[B]. Cohomology
cannot tell the smooth circle from the two lines. The conjecture's "built from algebraic
cycles", performed. The Lefschetz (1,1) theorem is what lets it happen here.

**Why potent.** The viewer knows a circle is the one figure with no straight part, and knows
"squaring the circle" is impossible. The mechanism breaks that: here, exactly and provably, a
circle *is* two straight lines. That is the **twist**, and it is also the literal content of the
conjecture's answer on this surface. The surface itself is never outlined. Its curvature appears
only as the envelope of straight strings. That is the second truth the viewer gets for free: a
curved surface built entirely from straight lines, as algebraic cycles build classes.

**Order.** INTERLACED (two ruling families crossing at every point, so the surface is a weave)
carrying a NESTED FAN (the conic pencil hinged at p and closing onto the X, like flow to an
attractor). One line of mapping: *blue is [A], gold is [B], a curve's colour-mix is its class.*

**Lineage.** Naum Gabo, *Linear Construction in Space No. 1* (1942–43, nylon strings; Tate
T00191). Gabo possibly took stringing from mathematical models; Moore said outright that his
*Stringed Figures* (1937–40) came from the Science Museum's string models. The plate returns
the construction to its source: the strings *are* the mathematics. Man Ray's *Objets
mathématiques* (Institut Poincaré models, *Cahiers d'Art* 1936) is the second conversation.

### (b) Every winding is a sum of strings — (p,q) curves on the same torus ★ RANK 2

**Relationship.** On the same hyperboloid, the curve α = q·u, β = p·u is a real algebraic curve of
class **p[A] + q[B]** (verified: degree p+q, q hits per A-string, p per B-string). Shown as a
sequence:
- [A] (one blue string)
- [B] (one gold string)
- [A]+[B] (the waist circle, and beside it the X)
- [A]+2[B] (twisted cubic)
- 2[A]+3[B] (quintic)
- 3[A]+4[B] (degree 7)

This is the honest version of the reference's "simple cycles combine" row. Each cell shows a
genuine cycle on a genuine surface with its exact class as caption.

**Why potent.** A torus-knot winding looks like a new, complicated shape. Its class is two
integers, and those integers count strings crossed. Complexity of shape and complexity of class
come apart.

**Order.** ORBITAL / interlaced winding on one lattice. Best as the plate's lower row under (a),
or as a stand-alone plate: one (2,3) curve wound on the string hyperboloid in a third ink.

**Caveat.**
- On an affine sheet every (p,q) curve with p≠q leaves through a rim |p−q| times. For H = 2, only
  70.5 % of the parameter lies inside |z| ≤ 2.
- Not every crossing is visible: at H=2, a (2,3) curve shows all 3 crossings on only 83/720
  A-strings. Captions state the class; they never ask the eye to count crossings.

### (c) Twenty-seven straight lines hold the whole cohomology — Clebsch diagonal cubic ★ RANK 3

**Relationship.** A smooth cubic surface with all 27 lines real:
- each line meets exactly 10 others (135 pairs);
- 10 Eckardt points where three lines meet (the S₅-orbit of (1:−1:0:0:0));
- 105 ordinary double crossings.

Its H² has rank 7, all Hodge, all spanned by the line classes. Again a theorem made visible.

**Why potent.** A bulging curved cubic shell that contains 27 perfectly straight lines is a
genuine shock. 10 triple points give natural focal nodes.

**Order.** Manfred Mohr's rule-generated projection: the 27 lines and their incidence graph *are*
the image, and the surface is at most a ghost mesh.

**Why only rank 3.**
- The surface has no simple parametrisation. It needs marching-cubes or a blow-up parametrisation
  for hidden-line work.
- Several lines run off to infinity in any affine chart.
- The class story ("27 lines span rank 7") is less one-glance than "circle = two lines".

---

## 3. Real data — verified

Exact math only; no datasets. Every number below was recomputed in `.venv/bin/python` on
2026-09-28. The scripts are at the session scratchpad (`hyp2.py`, `cl4.py`); the one-liners in §7
reproduce each number.

- **Statement and status.** The Clay problem page (https://www.claymath.org/millennium/hodge-conjecture/)
  names Deligne's official description, https://www.claymath.org/wp-content/uploads/2022/06/hodge.pdf.
  The verbatim statement, the known cases (Lefschetz 1924, dim ≤ 3) and the counterexamples
  (Atiyah–Hirzebruch integral; Voisin 2002 Kähler) are from https://en.wikipedia.org/wiki/Hodge_conjecture.
  Abelian fourfolds: https://arxiv.org/abs/2502.03415 (Markman, submitted 2025-02-05, v2
  2025-06-08; preprint).
- **Hyperboloid rulings.** Residual of x²+y²−z²−1 along A and B was 1.8e-15 and 3.6e-15.
  P(α,β) lies on B(β) to 2.2e-16.
- **(p,q) curves** (homogeneous form (cos(α+d), sin(α+d), sin d, cos d), d = (β−α)/2):

  | (p,q) | on quadric | max real plane hits (= degree p+q) | hits per A / B string | through plane at ∞ (= \|p−q\|) |
  |---|---|---|---|---|
  | (1,0) | ≤4e-16 | 1 | 0 / 1 | 1 |
  | (1,1) | ≤4e-16 | 2 | 1 / 1 | 0 |
  | (1,2) | ≤4e-16 | 3 | 2 / 1 | 1 |
  | (2,3) | ≤4e-16 | 5 | 3 / 2 | 1 |
  | (1,3) | ≤4e-16 | 4 | 3 / 1 | 2 |
  | (3,4) | ≤4e-16 | 7 | 4 / 3 | 1 |

  The implicit Im[(1+it)²(1−it′)³] on the (2,3) curve has residual 1.2e-13.
- **Clebsch:**
  - 27 lines built explicitly (15 + S₅-orbit of the golden line, deduplicated). max |Σx|, |Σx³|
    along all lines is 5.8e-16.
  - Every line meets exactly 10 others; 135 pairs.
  - 115 distinct intersection points = 10 Eckardt (3 lines) + 105 ordinary; 10·3 + 105 = 135 ✓.
  - The Eckardt points are the 10 permutations of (1:−1:0:0:0), matching Wikipedia (Clebsch
    surface).
- **Lineage facts.**
  - Gabo, *Linear Construction No. 1*, 1942–43 (Tate T00191; Guggenheim 1383; "possibly
    inspired by mathematical models").
  - Moore's *Stringed Figure* 1938 (Tate T00386): Moore cited Science Museum models.
  - Man Ray photographed the Poincaré Institute models, published in *Cahiers d'Art* 1936.
  - Source: Royal Society *Intersections: Henry Moore and Stringed Surfaces* (2012).

---

## 4. Simplifications allowed vs. lies

**Allowed (honest):**
- Drawing **real points only**. The complex quadric is S²×S², a real 4-manifold, and its real
  points are the torus drawn. The complex conic is a 2-sphere; its real points are the circle. One
  corner caption says "real points of complex surfaces".
- Clipping to rims |z| ≤ H, which must be stated. Any H is allowed; H = 2 gives the golden
  coincidence in §7.
- Any finite number N of strings per family, evenly spaced in α (resp. β). Strings end at the rims
  or, near the silhouette, where the spacing floor forces it.
- Hidden-line removal: the surface occludes its own back strings. Or a declared "transparent
  string model", with back strings as a lighter separate layer, which is how Gabo's nylon reads.
- Any rigid view, and uniform scale. Orthographic or perspective, stated once.
- Showing a finite sample of the continuous pencil (e.g. ψ = 0°, 15°, 30°, 45°, 60°, 75°, 90°).
- Swapping the hyperboloid for the hyperbolic paraboloid z = xy (also a doubly ruled real quadric
  with the same H², rulings x = c and y = c) if a saddle composes better. Say which.
- Captions using the reference's formula H^k(X,ℂ) = ⊕ H^{p,q}, as text only.

**Lies (binding on everyone):**
1. **An invented ribbon or blob presented as a variety.** Every drawn surface satisfies a stated
   polynomial equation. Every drawn curve is on it, to machine precision.
2. **Colour meaning "cohomology vs cycles".** Blue and gold are both algebraic cycles, [A] and
   [B]. No pen may stand for H^{p,q} or "the Hodge structure": those are vector spaces, not
   shapes.
3. **Bent strings.** Rulings are straight segments, one G1 each. A curved "string" is a lie about
   the whole point.
4. **The reference's row.** No sphere/torus/genus-2 blobs labelled C₀…C₄, and no "a₁C₀+a₂C₁" over
   overlapping decorative shapes. Every Cᵢ is a curve on the drawn surface with its class a[A]+b[B]
   written exactly.
5. **A non-algebraic winding captioned as a cycle.** No irrational slope, no non-coprime (p,q) drawn
   as one curve, no curve that leaves the surface.
6. **Closing clipped curves.** A hyperbola or (p,q) arc that exits a rim is not joined back with an
   invented arc; it goes through infinity.
7. **"The picture proves the conjecture."** Everything drawn is a theorem (Lefschetz (1,1),
   dimension 2). The plate must not show or claim an "open case" or a "non-algebraic Hodge class".
   None is known over ℚ, and the open cases live in real dimension ≥ 8.
8. **ℤ instead of ℚ** in the stated conjecture. The integral version is false (Atiyah–Hirzebruch).
   **Kähler instead of projective** is also false (Voisin 2002).
9. **Positive-only "gluing".** A Hodge class may need negative and fractional coefficients. Do not
   caption the conjecture as "every shape is assembled from simple shapes".
10. **Crossing counts as evidence.** Do not invite the eye to count crossings in the clipped,
    occluded render as proof of a class (see 2(b) caveat).

---

## 5. The misconception to quietly correct

**"The Hodge conjecture asks whether complicated shapes can be assembled from simple shapes"**,
which is the reference's own reading: spheres + tori → a big twisted form. It is not about
assembling shapes.
- It asks whether a cohomology class, an invisible *bookkeeping* object singled out by the complex
  structure, is **represented** by algebraic subvarieties, with rational coefficients.
- "Represented" is far looser than "made of". Cohomology forgets everything but class, which is
  why the smooth circle and the two crossing straight strings are **the same class**. That is the
  one correction the plate makes without a word: two things that look nothing alike are equal to
  the question being asked.
- The second correction: the difficulty is not that the shapes are complicated. Where we can
  draw, the answer is a theorem. The conjecture is open only past real dimension 8.

---

## 6. Pen-plotter fit

**Naturally a line.**
- Every ruling is ONE straight G1 segment, rim to rim. That is the cheapest possible stroke: no
  resampling, no dash logic. It batches trivially: sort by α within the A layer, by β within the
  B layer, so consecutive strokes are neighbours and travel is short.
- Conics and (p,q) curves are single smooth polylines, resampled by arclength at ≤ 0.3 mm chord
  error.
- Rims are (1,1) circles. Draw them only if they carry meaning: they are themselves conics of
  class [A]+[B].

**Density risks (hard).**
1. **Silhouette envelope.** In any projection the rulings are tangent to the outline, so projected
   spacing → 0 at the contour. Floods are guaranteed there without a rule. Terminate each
   string where its projected distance to its neighbour drops under 0.8 mm, or where the
   z-buffer hides it. Never let strings pile onto the outline. Honest, and it is the Gabo look.
2. **Pencil hinge.** All conics of the pencil pass through p and are tangent to ℓ there, so near
   p they converge to zero separation. Break each conic at a halo around p; the halo radius is
   where adjacent members reach 0.8 mm. p itself is the X's crossing point: the focal node.
3. **Waist spacing** (perpendicular, front-on) = 2πk/(N√2) mm, for k mm per unit radius and N
   strings per family:
   - k=30, N=96: 1.39 mm, safe.
   - k=25, N=120: 0.93 mm, marginal.
   - At k=30, the front-on floor breaks above N≈166. Oblique views foreshorten the flanks, so
     budget N ≤ ~100.
4. **Blue × gold crossings** are intended, since the surface IS the weave. But the two families plus
   a third-ink class curve crossing the same spot is ink-on-ink. Occlude the strings under the
   class curve (policy `occlude_crossings`) or accept one deliberate crossing.

**Must stay blank.**
- The throat: the view through the waist from slight elevation. It is the plate's quiet eye.
- The halo around p.
- The field outside the string construction, since the surface has no outline stroke.
- Generous paper between hero and row.

**Layers (proposed, light → dark; translator decides):**

| # | layer | contents |
|---|---|---|
| 1 | gold | [B] strings |
| 2 | blue | [A] strings |
| 3 | class-curve ink | pencil conics / (p,q) curves: a curve that is a *sum* gets its own pen, not either generator's |
| 4 | black | type, captions, class labels |

Each layer is entered once. Time ≈ Σlength / (600 mm/min at Leo's F600) + strokes × ~2.5 s
(lift+drop dwells + short travel). Example: 96 front-visible strings × ~100 mm ≈ 9.6 m, so
≈ 16 min drawing + 4 min cycles ≈ **20 min per ruling layer**. The class-curve layer is a few
metres and ~10 strokes, about 5 min. Report measured numbers in HANDOFF.

---

## 7. Check numbers

| # | value | reproduce |
|---|---|---|
| 1 | Rulings lie on the surface: residual < 1e-14 | `s=np.linspace(-3,3,99); P=np.stack([np.cos(a)-s*np.sin(a), np.sin(a)+s*np.cos(a), s],-1); abs(P[:,0]**2+P[:,1]**2-P[:,2]**2-1).max()` |
| 2 | A string turns **2·arctan H = 126.87°** of azimuth from bottom rim to top rim (H=2). Rim radius **√(1+H²) = 2.2361**; waist radius 1. 3D length 2H√2 = 5.657 units | `np.degrees(2*np.arctan(2)), np.hypot(1,2), 4*np.sqrt(2)` |
| 3 | Tangent plane x=1 cuts the surface in **y = ±z**, i.e. A(0,s) = (1,s,s) and B(0,s) = (1,−s,s). The X is one blue + one gold string | substitute x=1: y²−z²=0 |
| 4 | Pencil z = tanψ(x−1): ellipse ψ<45°, **parabola at ψ=45°**, hyperbola 45°<ψ<90°, **X at ψ=90°**. Far vertex at z = −tan 2ψ | asymptotic directions y² = (tan²ψ−1)x² |
| 5 | Last pencil ellipse wholly inside \|z\|≤2: **tanψ = 1/φ = 0.6180, ψ = 31.72°** (= ½·arctan 2) | `np.tan(np.arctan(2)/2), np.degrees(np.arctan(2)/2)` |
| 6 | Curve α=qu, β=pu has class **p[A]+q[B]**: degree p+q (1,2→3; 2,3→5; 3,4→7), q hits/A-string, p hits/B-string, \|p−q\| passes through ∞ | §3 table; count sign changes of `curve(p,q) @ random_plane` |
| 7 | Fraction of a p≠q curve inside \|z\|≤H: **2·arctan(H)/π = 0.7048** (H=2) | `2*np.arctan(2)/np.pi` |
| 8 | Intersection numbers: [A]²=[B]²=0, [A]·[B]=1. (p,q)² = 2pq; arithmetic genus (p−1)(q−1): (2,3) → 12 and 2 | `(a[A]+b[B])·(c[A]+d[B]) = ad+bc` |
| 9 | Betti/Hodge: quadric b₂ = 2 (χ=4), cubic surface b₂ = 7 (χ=9); h^{2,0}=0 for both, so H² is all Hodge and all algebraic | χ(ℙ¹×ℙ¹)=2·2; χ(Bl₆ℙ²)=3+6 |
| 10 | Clebsch: **27 real lines**, each meets **10**, **135** pairs, **10 Eckardt** points (perms of (1:−1:0:0:0)), 105 ordinary points. Golden line through (0:1/φ:−1/φ:1:−1), (−1/φ:0:1:−1:1/φ) | build 15 + S₅-orbit, test rank of [P₁,Q₁,P₂,Q₂] < 4 |
| 11 | Waist ruling spacing 2πk/(N√2): **k=30 mm, N=96 → 1.39 mm** (floor 0.8 mm → N ≤ 166 at k=30 front-on; silhouette always below floor → trim) | `2*np.pi*30/(96*np.sqrt(2))` |
