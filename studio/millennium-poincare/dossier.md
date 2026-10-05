# millennium-poincare — the Poincaré conjecture: to prove it is one sphere, the flow cuts it in two
**Field expert:** mathematics (geometric topology, Ricci flow) · **Date:** 2026-09-28 · **Status:** dossier v1.1 (errata folded by studio-lead 2026-09-29 from science critiques r02 + r03: R_min, lie 4 / §2(a) relative race)

Plate 6 of the MILLENNIUM series, and the only one of the seven that may say **SOLVED**.
Reference: `ref/reference.png` (AI poster: a dumbbell wireframe with red loops shrinking to a
gold point, "A loop contracts to a point", a row of seven shrinking ellipses). It is an
interpretation brief. Its good instinct is the dumbbell; its mistake is that every loop in it
shrinks politely and the dumbbell never changes. The mathematics says the opposite: one loop
**cannot** be shrunk by the flow, and the proof works by moving the space, not the loops.

Every number below comes from code in `studio/millennium-poincare/data/`. It is pure numpy,
deterministic and has no seed:

| file | what it computes |
|---|---|
| `ricci_rot.py` | rotationally symmetric Ricci flow on S^(n+1), arc-length gauge; validated on round spheres |
| `dumbbell.py` | the initial asymmetric dumbbell 3-sphere (analytic, R > 0, embeds) |
| `run_neckpinch.py` | neckpinch, surgery, both extinctions, plus the 2-D control. Writes `neckpinch.npz` (all isochrone profiles) |
| `csf.py` | curve-shortening checks: plane loop, parallels on the dumbbell, Gauss–Bonnet |

Overlap check: `grep -rniE "ricci|poincar|curve.shortening|grayson|neckpinch|perelman"`
over `promptplot/generative/` and `studio/` finds nothing, so no existing piece draws this.

---

## 1. The phenomenon (≤5 lines)

Poincaré (1904): if every loop in a closed 3-dimensional space can be shrunk to a point, is
that space the 3-sphere? Hamilton (1982) proposed deforming the space's own geometry by
**Ricci flow**, a heat equation for curvature. In 3-D the flow develops singularities: thin
**necks pinch** off. Perelman (arXiv 2002–03) showed you can **cut** at each neck, **cap** the
ends and continue. On a simply connected space the pieces all become round and **vanish in
finite time**. Every piece was a sphere, so the original was a sphere. Solved; Clay Prize
awarded 18 Mar 2010, declined 1 Jul 2010.

### Governing math

- **Ricci flow** (Hamilton 1982): ∂g/∂t = −2 Ric(g). This is dimensionless geometry, with
  time in units of length².
- **Rotationally symmetric S³.** Take g = ds² + ψ(s,t)² g_{S²} for s ∈ [0, L(t)] with
  ψ = 0 at both poles. Each value of s is a **round 2-sphere of radius ψ**. From Angenent &
  Knopf, *Math. Res. Lett.* 11 (2004) 493–518, with n = 2:
  **ψ_t = ψ_ss − (n−1)(1 − ψ_s²)/ψ**, ∂_t(ds) = n (ψ_ss/ψ) ds.
  The term −(n−1)(1−ψ_s²)/ψ is the **pinching force**. It behaves like −1/ψ at a neck and
  **vanishes when n = 1**, which is 2-D Ricci flow on a surface (ψ_t = ψ_ss).
- **Scalar curvature:** R = −2n ψ_ss/ψ + n(n−1)(1−ψ_s²)/ψ². At a thin neck R ≈ 2/ψ², which
  blows up.
- **Exact solutions.** A round S³ of radius r has **r² = r₀² − 4t**, so it is extinct at
  T = r₀²/4. A neck (the cylinder S²×ℝ) has **ψ² = ψ₀² − 2t**. A round S² under 2-D flow has
  r² = r₀² − 2t. The area of any 2-D surface metric on S² obeys **dA/dt = −8π** exactly
  (Gauss–Bonnet).
- **Curve-shortening flow (CSF)** is the 1-D model: X_t = κN. For any embedded closed plane
  curve, **dA/dt = −2π exactly**, so T = A₀/2π. Such a curve stays embedded, becomes convex,
  and then shrinks to a **round** point (Gage–Hamilton, *JDG* 23 (1986) 69–96; Grayson, *JDG*
  26 (1987) 285–314). On a curved surface a loop either shrinks to a point or converges to a
  **closed geodesic** (Grayson, *Ann. Math.* 129 (1989) 71–111). A parallel of
  ds² + ψ²dθ² has geodesic curvature ψ_s/ψ, so it moves by **ds/dt = −ψ_s/ψ**.
- **The same 2π inside the proof.** Perelman, *Finite extinction time…* (math/0307245) takes
  the area A of a minimal disc spanning a loop that evolves by a curve-shortening flow. He
  proves **dA/dt ≤ −2π − ½ R_min A**, with R_min ≥ −(3/2)/(t + const). The −2π that kills a
  plane loop is the −2π that forces a simply connected 3-manifold to die in finite time.
  Colding–Minicozzi, *JAMS* 18 (2005) 561–569, give an independent proof of finite extinction.

---

## 2. Three candidate visual truths (ranked)

### (a) NECKPINCH → SURGERY → EXTINCTION: one nest of time-lines that branches into two, each dying at a point ★ RANK 1

**The relationship.** The real Ricci-flow solution for an asymmetric dumbbell 3-sphere,
computed by `run_neckpinch.py`, runs in four stages:

1. At t = 0 the neck radius is 0.3143 and the lobe radii are 1.4139 and 0.6765.
2. The **neck races while the lobes shrink far less, in relative terms.** Between t = 0 and surgery at
   t_s = 0.05465, the neck loses **62 %** of its radius (0.3143 → 0.1197) and the big lobe
   loses **12 %** (1.4139 → 1.2447). The neck would pinch completely at T_pinch ≈ 0.0628;
   near that point ψ_min² falls at a rate that tends to 2.
3. **Surgery** at neck radius h = 0.12 cuts the space and caps both ends with round
   hemispheres.
4. **Two round spheres, two extinctions.** Piece B (small) is extinct at **t = 0.1171** and
   piece A (big) at **t = 0.3873**. Each obeys r² ≈ r₀² − 4t (measured slopes −3.91 and
   −4.00) and each turns round (length/ψ_max → π) before it vanishes.

The event order is fixed: **pinch before either lobe dies, small sphere before big.**

**Why it is visually potent.** Drawn as isochrones (the profile, or its hidden-line wireframe,
at equal time steps) it becomes a single figure. One nest of lines crowds at the neck, **breaks**
there and becomes two nests, and each nest spirals in on its own point. You can read the whole
proof as ink: a complicated shape is simplified by cutting, and every piece dies round. The
spacing tells the physics without a caption. Where time-lines pile up, the geometry is
standing still (the lobes before surgery). Where they spread, it is racing (the neck, and each
sphere's last moments, because r ∝ √(T−t) accelerates at the end).

**The twist.** The viewer holds the statement "it's all one sphere". The plate shows the flow
**tearing it into two**, and that tear *is* the proof: a sphere cut along a sphere and capped
is two spheres (S³ # S³ = S³). The only Millennium problem that fell was solved by making a
singularity on purpose and walking through it. This is the plate that says SOLVED, and the
drawing is the solution.

**Abstract order:** **BRANCHING NEST → FLOW-TO-ATTRACTOR.** Nested isochrones, one branch
event, and two point attractors. It is not a plot, because nothing is extruded. The lines are
the object itself at successive instants, in the way growth rings are a tree.

### (b) THE LOOP THAT WILL NOT SHRINK: curve-shortening on the dumbbell ★ RANK 2

**The relationship.** Put loops on the dumbbell and move them by curve-shortening flow. This
is `csf.py`, on the drawn t = 0 surface ds² + ψ²dθ², held static. The surface has exactly
**three closed-geodesic parallels**, the critical points of ψ:

| arc length s | ψ | what the parallel is | stability |
|---|---|---|---|
| 1.601 | 1.4139 | big equator | unstable |
| 3.856 | 0.3143 | **neck** | stable |
| 5.141 | 0.6765 | small equator | unstable |

(Lusternik–Schnirelmann's three geodesics, found by Grayson's flow.) Parallels move by
gradient descent on log ψ:

- A parallel started between the two equators converges to the **neck** and stays there forever.
  Its length stops at 2π·0.3143 = **1.975**. It is topologically contractible, since this is a
  sphere, but the flow will never contract it.
- A parallel outside an equator runs to its pole and dies. The one started 0.05 inside the big
  equator dies at t ≈ 1.57.
- Small loops on a lobe shrink to round points.

Gauss–Bonnet explains why the neck loop stops. The cap it bounds carries total curvature
∫K dA = 2π(1 − ψ_s) = **exactly 2π**, so the loop's area rate dA/dt = −(2π − ∫K dA) is
**zero**.

**Why potent.** It contradicts the reference's own caption ("A loop contracts to a point"),
and it is the honest reason Perelman needed surgery. When the geometry is fixed, the natural
flow of loops gets stuck on a neck. Only moving the geometry (Ricci flow) kills the neck.

**Twist:** the red loop sits in the middle of the plate and refuses to shrink.

**Order:** FLOW-TO-ATTRACTOR with a **separatrix**. The two equators are watersheds between
pole basins and the neck basin, and they could be left as blank paper. Lineage hint: Vera
Molnár, *(Dés)Ordres* (1974). Her concentric, disturbed squares are exactly what CSF does to
a loop: disorder decays inward until it is round.

**It composes with (a).** The stuck neck loop in (b) is the loop that (a) cuts. A plate can
carry (a) as the body and put (b)'s neck loop in red as its hinge. That is the recommended
fusion.

### (c) ONE TERM: the same dumbbell in 2-D rounds out; in 3-D it pinches ★ RANK 3

**The relationship.** Run the identical initial profile under n = 1, which is 2-D Ricci flow
of the drawn surface itself.

- **The neck WIDENS:** 0.3143 → 0.3554 at t = 0.0547, the moment the 3-D neck is at 0.1197.
- The neck is gone entirely (profile monotone) by t = 0.2405.
- Area falls at exactly −8π. Measured −25.117 against −25.133.
- Extinction comes at A₀/8π = **1.0085**, as one round sphere with no singularity (Hamilton
  1988, Chow 1991).

The only difference between the two outcomes is the term −(n−1)(1−ψ_s²)/ψ.

**Potent because** it exposes the hidden dimension. The surface you are shown would never
pinch. The pinch is the signature of each ring secretly being a whole 2-sphere.

**Weakness:** it is a two-panel comparison, which risks reading as a figure. Use it as a
caption fact or a small quiet counterpoint, not as the plate.

**Order:** INTERFERING / mirrored laminar pair.

---

## 3. Real data — verified

There is no downloadable dataset for this problem. The data is **exact math, computed here**.

Reproduce with:

```
.venv/bin/python studio/millennium-poincare/data/ricci_rot.py      # round-sphere validation
.venv/bin/python -W ignore studio/millennium-poincare/data/run_neckpinch.py  # ~15 min
.venv/bin/python -W ignore studio/millennium-poincare/data/csf.py            # ~2 min
```

- **Solver validation** (`ricci_rot.py`, N = 200, run to t = 0.75·T):
  - n = 1: r² = 0.250030 against exact 0.249996.
  - n = 2: r² = 0.250010 against exact 0.249977.
  - Length/r = 3.14146 (π = 3.14159).
- **Initial dumbbell** (`dumbbell.py`): ρ(z) = √(ℓ²−z²)·(α + β(z/ℓ − ζₙ)²) with ℓ = 2.0,
  α = 0.16, β = 1.05, ζₙ = 0.18.
  - The √ factor is a round sphere, so both poles are smooth round caps.
  - Initial R_min = **0.2167 > 0** (analytic minimum, at the poles; v1 said 0.2213, corrected 2026-09-29 by science r02 + r03), so this is Angenent–Knopf's positive-curvature setting,
    and |ψ_s| ≤ 1.
  - L₀ = 6.0059, volume 44.574.
- **npz contents** (`neckpinch.npz`): `snap_tag` ∈ {pre, surgery, A, B}, `snap_t`, `snap_L`,
  `snap_psi` (N+1 samples on a uniform s-grid). Isochrones are every Δt = 0.005, and
  `neck_hist` holds (t, ψ_neck, lobe A, lobe B, L).
  - Embed a snapshot with `ricci_rot.embed(psi, L)` → (z, ρ). Rotate about the z-axis for the
    surface picture.
  - Choose a **stated** alignment between snapshots, because Ricci flow is intrinsic and has no
    ambient position. Recommended: pin the neck before surgery, and after surgery pin each
    piece's ψ²-weighted centroid (the limit is the extinction point).
- **Sources:**
  - Clay problem page https://www.claymath.org/millennium/poincare-conjecture/ (award
    18 Mar 2010).
  - Perelman, arXiv math/0211159 (11 Nov 2002), math/0303109 (10 Mar 2003), math/0307245
    (17 Jul 2003).
  - Decline announced 1 Jul 2010. Perelman said Hamilton's contribution was no less than his.
    https://phys.org/news/2010-07-russian-mathematician-million-prize.html
  - Angenent–Knopf 2004 (MRL 11:4) and *Precise asymptotics of the Ricci flow neckpinch*,
    arXiv math/0511247.
  - Tao, 285G lecture 6 (the −2π inequality):
    https://terrytao.wordpress.com/2008/04/18/285g-lecture-6-finite-time-extinction-of-the-third-homotopy-group-ii/
  - Colding–Minicozzi arXiv math/0308090.
  - Grayson 1989: https://annals.math.princeton.edu/1989/129-1/p03

---

## 4. Simplifications allowed vs. lies

**Allowed (honest):**
- **Drawing the 3-sphere by its profile.** Rotate the warping function ψ(s) about an axis into
  a surface of revolution in ℝ³, and say that **each ring stands for a round 2-sphere of radius
  ψ**. This is legitimate because |ψ_s| ≤ 1 holds here, so the profile embeds isometrically in
  the (z, ρ) half-plane.
- Rotational symmetry. The real theorem needs no symmetry, but the symmetric neckpinch is the
  standard rigorous model (Angenent–Knopf).
- **Surgery simplified.** Cut at the neck minimum and cap with a round hemisphere of the neck
  radius (C^{1,1} join) instead of Perelman's standard solution, and pick the surgery scale
  h = 0.12. Stating "cut at radius h" is enough.
- Any stated alignment between isochrones, and any uniform scale.
- Loops drawn by CSF on the **static** t = 0 surface as the 2-D model of the proof's
  loop/minimal-disc argument.
- Captioning the 1-D/2-D models as "the model problem" rather than as the 3-D proof.

**Lies (binding on everyone):**
1. **Loops shrinking in a tidy geometric row that stay elongated to the end.** The reference's
   seven ellipses do this. Real CSF loops **turn round before they vanish**: the isoperimetric
   ratio rises from 0.650 to 0.9999 by 5 % of the area. Equal-Δt loops enclose **equal-area
   decrements** (ΔA = 2πΔt), so their radii go as √(T−t) and the **gaps widen toward the end**,
   not shrink.
2. **Shrinking the loop around the neck to a point by curve-shortening.** It converges to the
   neck geodesic and stops, with length 1.975 at t = 0. Only Ricci flow pinching the neck
   removes it.
3. **A neck that pinches under the 2-D flow of the drawn surface.** In 2-D the same neck
   **widens** (0.3143 → 0.3554). If the plate shows a pinch, it must be the 3-D profile, with
   rings meaning 2-spheres.
4. **Wrong order of events.** The neck pinches (t ≈ 0.063) **before** either lobe dies, and
   the small sphere dies (0.117) before the big one (0.387). Do not let a lobe vanish first,
   and do not misstate the race. *(Corrected 2026-09-29, science r02 + r03: v1 said "do not show
   the lobes shrinking visibly", which is false in absolute terms.)* The race is **relative**:
   neck −62 % (−0.195 u, 12.1 mm at 62 mm/u), small lobe −30 %, big lobe −12 % (−0.169 u,
   10.5 mm). The big lobe's absolute loss is 87 % of the neck's. Draw the true loss; state the
   race as percentages.
5. **Surgery on a fat neck.** The cut happens only on a thin, nearly cylindrical neck. Here the
   cap radius is 0.12 against a lobe of 1.24, about 1 : 10. A scissor cut through a waist the
   size of the reference's is false.
6. **Isochrones at uneven, undeclared time steps, or re-spaced for looks.** Spacing is the
   time encoding. A line family that looks evenly spaced here is a lie, because the true
   spacing is not even.
7. **Presenting the drawn surface as "the 3-sphere"**, or drawing a 3-sphere as a ball or a
   globe. S³ cannot sit in ℝ³.
8. **Calling "every loop contracts" the proof.** That is the **hypothesis** (simply connected).
   The proof moves the metric.
9. **Credit and history errors.** Saying Perelman accepted the prize or the Fields Medal (2006,
   declined), or leaving Hamilton out of Ricci flow. Also calling the conjecture open, or
   saying it was proved by "smoothing" with no singularities.
10. **Decorative extra pinches, holes or handles.** A handle would make it a non-sphere, which
    is the opposite claim.

---

## 5. The misconception to quietly correct

**"The proof shows loops shrinking to a point."** Everyone, the reference poster included,
pictures the conjecture as a rubber band sliding off a ball. That picture is the *hypothesis*
(simply connected), and on a surface it is a 19th-century fact, not the conjecture. The actual
proof never touches the loops. It lets the **space itself** flow. The flow tears the space at
its necks, the pieces round up and each one vanishes. Space being cut is the step nobody
expects. It is also why the obvious approach fails: shrink the loops directly and the neck
loop gets stuck (2(b)).

A second, quieter misconception: the picture is not the 3-sphere. Each drawn circle is a
2-sphere, and that hidden dimension is exactly what makes the neck pinch (2(c)).

---

## 6. Pen-plotter fit

**What is naturally a line:**
- **Parallels** (ψ = const rings), each honestly "one 2-sphere".
- **Meridians/profiles.**
- **Isochrones:** the profile at equal Δt, the natural line family for truth (a).
- **CSF loops:** closed curves, one pen-down each.
- The surgery cut and the extinction points (dots) are events, not fields. They take the
  accent.

A hidden-line wireframe of the dumbbell (Scene3D `surface()`) with parallels at equal Δs and
meridians at equal Δθ is the reference's language and is exact. Back-face lines may be dashed
as the reference does, or dropped.

**Density risks (measured on `neckpinch.npz`):**
- **Before surgery, isochrones at Δt = 0.005 are 0.015 units apart** (median) and **touch** near
  the pinned neck and on the barely-moving big lobe (min gap ≈ 0.0001–0.005). At 75 mm/unit
  that is 1.1 mm median and 0 mm minimum.
  - Rule: **isochrones must merge into one line wherever they would fall under 0.8 mm.** That
    merge is true (the geometry is not moving there), so draw it as a merge, not a crowd.
    The neck is where they separate.
- **After surgery, piece A at Δt = 0.005 starts 0.0005–0.0015 units apart and ends 0.03–0.04
  apart.** It needs **Δt ≥ 0.02** (then 0.0008 → 0.13) and must still merge early rings.
  - For a round sphere, consecutive equal-Δt radii differ by ≈ 2Δt/r. Choose Δt so that
    2Δt/r_max·(mm/unit) ≥ 0.8.
- **The wireframe crowds at the silhouette.** Parallels at equal Δs bunch in projection where
  the surface turns away. Thin them in screen space (Scene3D ScreenThin) and keep ≥ 0.8 mm.
- **Neck scale:** the neck at surgery is 0.12 units, about 9 mm at 75 mm/unit, and the probe
  neck is 0.05, about 3.7 mm. Parallels through the neck must be sparser than on the lobes.
  Otherwise the most important 10 mm of the plate floods.

**What must stay blank paper:**
- **The surgery gap** between the two caps. That is the one cut, and nothing is drawn in it.
- **The watersheds** (the two unstable equators, if truth (b) is used).
- The space around each extinction point, so the final ring and the dot read as a distinct
  **ending**.

**Pens (layer discipline, stated meanings):**
- Black hairline: the space (wireframe and isochrones).
- **Red: the topology events.** The neck loop that will not shrink, the cut, and the capping
  hemispheres. Scarce and loud, per the series grammar.
- Optional ochre: two extinction dots, echoing the reference's gold point. It is one pen only
  if it means "extinct here".

Layer order: black → red → ochre (dark structure first, the accent lands on top and stays
unmuddied). Each layer is strokes of closed loops or open profile polylines: spatially
orderable, batchable, with no sheet-crossing travels.

Lineage candidates for the translator:
- **Vasarely, *Vega*** — a lattice swollen by a hidden volume. This is exactly a wireframe
  whose rings stand for a hidden dimension.
- **Molnár, *(Dés)Ordres*** — nested loops losing their disorder, for the CSF loops.

---

## 7. Check numbers

Each value is reproduced by the script named. Tolerances are numerical, not physical.

| # | quantity | value | reproduce |
|---|---|---|---|
| 1 | Round S³ extinction law r² = r₀² − 4t; post-surgery slopes | exact −4; measured A −4.003, B −3.908 (fit on ψ_max < 0.12) | `ricci_rot.py` (validation), `run_neckpinch.py` `slope_ext_*` |
| 2 | Initial dumbbell radii: neck / big lobe / small lobe | 0.3143 / 1.4139 / 0.6765 (neck/big = **0.2223**); R_min = **0.2167** > 0 (v1: 0.2213, corrected 2026-09-29) | `run_neckpinch.py` (`neck0`, `lobeA0`, `lobeB0`, `Rmin0`) |
| 3 | Pre-surgery disparity: neck vs big lobe radius loss, t = 0 → t_s = 0.05465 | neck **−62 %** (0.3143 → 0.1197), big lobe **−12 %** (1.4139 → 1.2447), small lobe 0.6765 → 0.4709 | `neck_hist` in `neckpinch.npz` |
| 4 | Neckpinch time and rate | T_pinch ≈ **0.0628**; d(ψ_min²)/dt = −1.74 (ψ ≈ 0.085) → −1.78 (ψ ≈ 0.052), tending to −2(n−1) = **−2** (cylinder law, log-corrected) | polyfit of `neck_hist` |
| 5 | Order of events | T_pinch 0.063 < T_ext(small) **0.1171** < T_ext(big) **0.3873** | `run_neckpinch.py` `T_ext_A/B` |
| 6 | Roundness at death: length/ψ_max → π | A **3.140**, B **3.185** at ψ_max ≈ 0.10 (B: 4.57 at surgery → 3.48 at 0.28 → 3.16 at 0.07) | `run_neckpinch.py` `roundA/roundB` |
| 7 | 2-D control (same profile, n = 1) | neck **widens** 0.3143 → 0.3554 at t = 0.0547; neck gone at t = 0.2405; dA/dt = −25.117 (−8π = −25.133); T = A₀/8π = **1.0085** (A₀ = 25.346) | `run_neckpinch.py` (`*_2d`) |
| 8 | Planar CSF | dA/dt = −2π = **−6.2832** (measured −6.2885); test loop r = 1 + 0.3cos3θ + 0.15sin5θ: A₀ = 3.3180, T = A₀/2π = **0.5281** (numerical 0.5257); isoperimetric 0.650 → 0.9999 | `csf.py` |
| 9 | Closed geodesics on the t = 0 dumbbell and the stuck loop | parallels at s = 1.601 (unstable), **3.856 (neck, stable)**, 5.141 (unstable); a parallel started at s = 1.651 ends at 3.8553 with length **1.975 = 2π·0.3143**, forever | `csf.py` |
| 10 | Gauss–Bonnet on the drawn surface | ∫K dA pole → any geodesic parallel = **2π** (6.29–6.31 numerically); whole surface **4π = 12.5664** | `csf.py` |

Constants a critic can check by hand:
- Clay award 18 Mar 2010, declined 1 Jul 2010.
- Perelman arXiv v1 dates 11 Nov 2002 / 10 Mar 2003 / 17 Jul 2003.
- Poincaré 1904.
- Perelman's disc-area inequality dA/dt ≤ −2π − ½R_min·A.
