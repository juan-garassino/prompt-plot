# millennium-navier-stokes — encoding (VISUAL TRANSLATOR)   · Status: encoding v1 · 2026-09-28

Source of truth: `studio/millennium-navier-stokes/dossier.md` v1 (Fefferman / Clay; Burgers 1948;
Lamb–Oseen; OpenAI claim 8 Sep 2026, unverified). Reference: `ref/reference.png`, an AI poster.
Treat it as an interpretation brief and do not trace it (`studio/AUTHORING.md`).
Plate 3 of the MILLENNIUM series. The series grammar is a cream sheet, a spaced-caps title
top-left with a one-line statement, small corner captions, and one loud accent colour.
Truths built: **(a) rings in the plane, spiral in space** carries the plate; **(b) the ladder**
is its second read. (c) (2D inverse cascade) is NOT drawn and appears only as one caption clause
plus NOTES.

Theses in flight: **faithful** and **abstract**. Everything below binds both unless a line says
`[faithful]` or `[abstract]`.

---

## 1. STYLE assignment

**Stated hybrid: OP ART line field (Riley) on a BAUHAUS poster sheet.** Riley's order is "one line
family whose drift makes the surface move, no figure drawn". That order is exactly an evenly
spaced streamline field, and this plate's whole argument is a rings-versus-spiral optical
question. The Bauhaus sheet (cream, spaced caps, asymmetric diagonal, one scarce loud accent)
is the series grammar, and it contributes furniture and type only. It never contributes
shapes: no discs, bars or quarter-circles.

Why not Deco (radiating fans), the runner-up: a Deco fan radiates from a point, and here that
would read as an explosion. It is also the wrong direction. The flow runs INTO the axis and
leaves through the page.

**Lineage: Bridget Riley, *Blaze 1* (1962), National Galleries of Scotland.** The NGS text says
it "appears to be a spiral" but "is formed from a succession of concentric circles". The eye
supplies a vortex that is not there. The plate answers her literally. In the plane a vortex
really IS concentric circles, so any spiral there is an illusion, as in *Blaze*. Only the third
dimension makes the spiral real. The order taken from her is one line family at constant
spacing, whose curvature drift alone makes the surface turn. Fallback reference: *Current* (1964).
(If a sibling Millennium plate also claims Riley, this plate keeps it because it is
dossier-sourced. The lead arbitrates.)

---

## 2. The one-glance statement

**Flat, a whirlpool is only rings. The spiral you know is the third dimension, and it can keep
shrinking.**

- **3 m:** a large blue inward spiral that tapers down a diagonal into smaller and smaller
  copies of itself, ending at a tiny red ring. Off to one side, alone, a calm black target of
  closed circles.
- **1 m:** the black disc is rings with no spiral anywhere, and its eye is wide open. The blue
  copies are the same vortex at exactly ½, ¼, ⅛… The last one frays into stubs before the red ring.
- **30 cm:** the ring spacing is tightest in one band (1.12 r_c, the speed maximum). The captions
  say which is 2D, which is 3D, what "same solution at half the size" means, and the dated
  status stamp.

---

## 3. The abstract ORDER

**RADIAL flow-to-an-attractor that is not a sink (3D, blue) set against NESTED rings (2D, black),
with the radial form repeated as a SELF-SIMILAR ladder converging on one empty point.**

Exact mapping in one line: **curl shape = dimension (rings are the plane, a spiral is space);
each rung = the same Burgers vortex at exactly ½ the size (NS scaling); the empty red ring =
where the ladder would have to finish, and nothing drawable is inside it.**

This names neither a plot nor an object. There is no axis, no chart, no drain, no wave and no
tornado.

---

## 4. Channel mapping (Tufte: nothing drawn that encodes nothing)

Units: δ = Burgers core scale, Re_Γ = Γ/ν = **100 (fixed, stated in NOTES)**. Hero δ₀ = **22 mm**
on A3 (any δ₀ ∈ [12.8, 25.6) mm keeps rung 5 as the first rung below the 0.8 mm floor, which is
the claim in §4 row 7).

| quantity | channel | exact rule / range |
|---|---|---|
| 3D velocity, plan view (Burgers u_r = −αr/2, v_θ = Γ/2πr·(1−e^{−r²/δ²})) | **blue streamlines**, each one continuous stroke | exact streamlines: closed form θ(s) = θ₀ + (Re_Γ/8π)[(1−e^{−s})/s + E₁(s)], or RK4 on (u_r, v_θ). Seeding by Jobard–Lefebvre on the planar field, run **once in δ-units** (d_sep = 2.4 mm/δ₀ = 0.109 δ, d_test = ⅔ d_sep). Truncated at R_out = 4δ (5–6δ allowed where the frame crops it). |
| Swirl-to-inflow balance (pitch) | curvature of the blue lines | falls out of the field. At the core β → 7.16° to the circle; ≈11° at r = δ, 27° at 2δ, 48.5° at 3δ, 64° at 4δ (verified). Identical in every rung. |
| "Flow leaves through the page" (planar ∇·u = −α) | the spiral itself converging to a blank eye | nothing added. The eye stays bare paper. |
| Pen resolution (0.8 mm floor) | **blank eye radius + stroke termination** | J–L termination at d_test. Single-arm eye = d/(1−e^{−2π·4π/Re}): hero ≈ **2.9 mm** at d_test 1.6. A blue stroke dies at the floor and never resumes (no pause-resume dashes). |
| 2D vortex, same Γ, r_c = δ₀ (Lamb–Oseen ψ = (Γ/4π)[ln s + E₁(s)]) | **black closed circles** | rings at **equal Δψ** out to R = 2 r_c = 44 mm. Tightest gap **1.5 mm at r ≈ 25 mm (1.12–1.14 r_c)**, **22 rings**, inner ring 6.6 mm, outer gap 1.9 mm (verified). Spacing = speed (Δr = Δψ/v_θ). Recommended at 1.5; 1.2 (28 rings) is allowed. |
| NS scaling u_λ = λu(λx, λ²t), λ = 2 | **rung size** | rung n = the rung-0 streamline set scaled by 2⁻ⁿ about its own centre. R_n = 88·2⁻ⁿ mm, δ_n = 22, 11, 5.5, 2.75, 1.375 mm. Rungs 0–4 are drawn. Rung 5 (δ = 0.69 mm) is under the floor and is not drawn. |
| Rung order (hypothetical collapse sequence; rung n lasts T₀·4⁻ⁿ) | **position on a similarity orbit** converging to L | centres C_n on the orbit of "scale ½ (+ optional rotate Δφ) about L". Rim gaps are self-similar: \|C_n − C_{n+1}\| = 1.10·(R_n + R_{n+1}), so the gaps are 13.2, 6.6, 3.3, 1.65, 0.83 mm. Chain length from C₀ to L = 1.10 · 3R₀ = **290 mm**. `[abstract]` Δφ = 0 (straight diagonal). `[faithful]` Δφ is allowed (the orbit curls like the reference's right lobe) if the value is stated. |
| Vorticity ω₀ × 4 per rung | **ink density per rung** | comes free from the scaling: J–L spacing scales with the rung (2.4 → 1.2 → 0.6 mm), then a **cull pass** at the 0.8 mm floor. Strokes are processed longest first, and each is shortened from its inner end until it clears every kept stroke by 0.8 mm. Rungs 0–1 are exact congruent copies. From rung 2 the floor bites, so the darkening saturates. That saturation is the pen's limit, drawn. |
| Where the ladder would finish (Σ rung times → 4/3 T₀, BKM ∫sup\|ω\| = ∞) | **one empty red ring** around L | centre L, radius = \|C₅ − L\| + R₅ (it encloses every rung ≥ 5, i.e. everything the pen cannot draw). Two passes, nothing inside. |
| Epistemic status (dossier C10) | **red type**, one line | dated and conditional, see §6. Red appears only here and at L. |
| `[faithful]` Meridional flow, swirl omitted (r²\|z\| = C) | black hairline **hyperbola family + one straight vertical axis** (the vortex line) | Monge elevation at the **same scale as the plan** (shared basis: a smaller window, never a smaller projection). The axis is collinear with the hero centre through **one dotted projection line** (no arrows, no zoom cone). Window ≤ 90 × 70 mm. |

Deliberately not encoded: pressure, a speed/vorticity hatch, rung outline circles, axes, ticks,
scale bars and a legend box. Pen meanings are given in one caption line.

---

## 5. Composition sketch — A3 portrait 297 × 420 mm, margin 15 (drawable x[15,282] y[15,405], origin bottom-left, y up)

Shared axes: x = 15 (title, bottom-left caption, the hero's left crop) · x = 282 (right
captions, stamp right edge) · the **orbit line C₀ → L** (the plate's one driving diagonal).

| element | where (mm) | size |
|---|---|---|
| Title `NAVIER–STOKES`, spaced caps | top-left, baseline y ≈ 390, x = 15 | cap height 8–10 mm, 2 passes |
| One-line statement | y ≈ 380, x = 15 | 3–3.5 mm caps |
| **Hero rung 0 (DOMINANT)** | C₀ ≈ (72, 258); R₀ = 88; the left frame crops ~30 mm of far-field arms | ~65 % of the blue ink |
| Rungs 1–4 | on the orbit from C₀ to L; `[abstract]` L ≈ (255, 40), straight | R = 44, 22, 11, 5.5 |
| Red ring at L + status stamp | bottom-right corner; stamp right-aligned at x = 282, baseline ≈ 20–24 | ring ≈ 7 mm radius |
| **2D ring disc** | upper-right, centre ≈ (228, 295), R = 44 | ≥ 25 mm bare paper to any blue stroke, ≥ 10 mm to the frame |
| Captions (3–4) | each sits in bare paper beside its element, never over lines | 2.2–2.8 mm caps |
| **Quiet zone** | the lower-left triangle under the orbit line (≈ x 15–130, y 15–160) | stays empty `[abstract]`. `[faithful]` it may hold the elevation, but ≥ 40 % of it stays bare. |

- **Dominance:** hero : ring disc = hero : rung 1 = 88² : 44² = **4 : 1** by area.
- **Tension:** the hero is cropped by the frame, the mass runs down one diagonal, and the calm
  black disc sits off-axis opposite it. Nothing is centred.
- **Reading path:** title (TL) → hero → down the ladder → red ring + stamp (BR). The ring disc is
  the side glance that makes the spiral mean something.
- `[faithful]` Follow the reference's geography. The hero sits mid-left and its own far-field
  arms, cropped by the left and bottom frames, stand in for the reference's inflow "wave"
  (R_out up to 6δ there). The ladder curls up or down the right side where the reference's
  eddies were, as a stated Δφ. The red ring sits at the ladder's limit. The reference's circular
  zoom inset becomes the Monge elevation (the X saddle is r²|z| = C). Its axis goes directly
  below the hero, joined by the dotted projection line. Rewrite the corner captions honestly
  (e.g. "SAME EQUATIONS · EVERY SCALE").
- `[abstract]` Riley purity: only the three line families (spiral ladder, rings, red ring) plus
  minimal type. The hero may grow to R_out = 5δ and crop on two frames. No elevation.
- **A4 portrait fallback:** scale the layout by 0.707 but keep every mm floor (δ₀ = 15.5 mm, which
  is still within [12.8, 25.6)). The culling then removes more lines, and that is correct.
  **Confirm with Juan that Leo takes A3 before the plot job.** Leo's logged sessions are A4/A5
  landscape.

---

## 6. Pen budget — 3 inks, 4 layers (order stated)

| layer | pen | meaning | content |
|---|---|---|---|
| L1 | **BLUE** 0.3 mm fineliner | **space: flow that leaves the plane (3D)** | hero + rungs 1–4. Batched per rung (hero · rung 1 · rungs 2–4). Nothing else is blue. |
| L2 | **BLACK** 0.1–0.2 mm hairline | **the plane: proved smooth (2D)**, plus `[faithful]` the side view | 22 rings (inner → outer); elevation hyperbolas + axis + the one dotted projection line |
| L3 | BLACK 0.3 mm (same ink, own layer, may be the same pen, no swap needed) | **type** | title, statement, captions, NOTES line. Halos (the geometry skips a box) only where a label unavoidably overlaps lines. Default placement is bare paper. |
| L4 | **RED** 0.3–0.5 mm | **the open question**, in space and in time | the empty ring at L (2 passes) + the status stamp. **< 1 % of total ink.** |

Order: blue → black → type → red. The light, dominant mass goes first, dark ink lands after it,
and the accent goes last and is never overdrawn. Red and blue never touch: the ring clears rung
4's rim by ≥ 0.8 mm.

Status stamp (red). The wording must be dated and conditional. Candidates:
`8 SEP 2026 · BLOW-UP WITH A SMOOTH PUSH CLAIMED, NOT YET VERIFIED · WITHOUT A PUSH: OPEN`
or `CLAIMED 8 SEP 2026 (FORCED, UNVERIFIED) · CLAY: NO AWARD · UNFORCED CASE OPEN`.

Caption kernels (black):
- ring disc: `IN THE PLANE: RINGS · (ω·∇)u = 0 · THE EYE ONLY OPENS (t ×4 → EYE ×2) · PROVED SMOOTH`
- hero: `IN SPACE: A SPIRAL · SEEN DOWN THE STRETCHING AXIS · FLUID LEAVES THROUGH THE PAGE`
- ladder: `THE SAME SOLUTION AT ½, ¼, ⅛ … (NS SCALING — COPIES, NOT ONE INSTANT)`
- at L: `IF THE LADDER FINISHES, IT FINISHES HERE, IN 4⁄3 T₀ · THE PEN STOPS AT 0.8 MM FIRST`
- NOTES corner: `BURGERS 1948 · LAMB–OSEEN · Re_Γ = 100 · δ₀ = 22 MM · 2D ENERGY RUNS TO LARGER SCALES (KRAICHNAN 1967)`

---

## 7. Expressive levers (one decision each)

- **Proportion:** exact 2:1 steps down the ladder, with 4:1 hero dominance. The ratios are the
  physics, so none is tuned by eye.
- **Fill / void:** voids are data. They are the spiral eyes (pen floor), the ring-disc eye (ψ is
  flat there), the empty red ring (below the floor) and the lower-left silence. No void gets a mark.
- **Density gradient:** there are two, both real. Ring spacing gives speed in the black disc.
  Rung-to-rung darkening gives ω₀ × 4, saturating at the pen floor. Within a rung the spacing is
  constant (Riley).
- **Colour play:** blue is the mass, black the calm counter-weight, red one pinpoint. Colour is
  dimension (3D / 2D / open), not a decorative category.
- **Texture direction:** every blue stroke follows the flow. The black rings run across the grain
  of the hero's nearly radial far field, but they never meet it (the gap is the comparison). Type
  is horizontal.
- **Depth (declared):** the plan view is flat by lineage (Riley is flat) and by honesty (it is a
  stated projection down the axis). Depth is carried by the ladder's recession along a similarity
  orbit to a vanishing point, and `[faithful]` by the Monge elevation. No fake perspective and no
  tilted disc.

---

## 8. The twist

The viewer already holds two things: the whirlpool spiral (plughole, Hokusai, Van Gogh's sky)
as a flat picture, and Riley's *Blaze* as "circles that look like a spiral". The mechanism breaks
both. Flat, a vortex can only be rings, so the spiral is the third dimension showing (planar
∇·u = −α). The poster's zoom inset becomes a ladder where **the zoom changes nothing** except
the one thing the viewer did not expect: the pen, not the mathematics, gives out first.

---

## 9. Forbidden list

1. **No spiral, ring break or ring end in the black disc.** Rings are closed and concentric, one stroke each.
2. **No converging spiral without the 3D caption.** The blue hero must be declared "seen down the stretching axis".
3. **No hand-tuned spirals.** No Archimedean or tuned-log spirals, curl noise, `vortex_field`, swirled scanlines or decorative eddies. Every blue line is an exact Burgers streamline.
4. **No pitch drift across rungs.** Rungs 0–1 are exact congruent copies, and later rungs differ only by floor culling. No "tightening to show blow-up".
5. **No rung drawn below the floor, and nothing blue inside the red ring.**
6. **No arrows anywhere.** That includes flow arrows, zoom arrows, zoom cones and the reference's dashed inset cone. The only dotted line is the single Monge projection line `[faithful]`.
7. **No outlines.** No circle around a rung, the ring disc or the eye. The rim is where strokes start.
8. **No fills or hatching** for speed, vorticity or pressure. No stipple in the eyes.
9. **No red** beyond the L ring and the stamp. The eye of the hero is not red, because Burgers is smooth (lie 4).
10. **No schematic furniture.** No axes, ticks, legend boxes, energy-spectrum slope, typeset NS equation as an image, or Clay logo. The sheet border is allowed only if the series lead adopts it for all seven plates.
11. **No status lies.** Never "SOLVED", never "NOBODY KNOWS", and never an unforced claim.
12. **No "large → small" on anything 2D.** That caption belongs to the ladder only.
13. **No pause-resume dashing on streamlines.** A stroke terminates and never resumes, because dashes would read as a texture Riley never used.

---

## 10. Fabrication

- **Floor:** every blue stroke is ≥ 0.8 mm from every other blue stroke, measured on the gcode.
  The field d_sep is 2.4 mm in the hero, and this is Riley's spacing, not an engraving's. Rings:
  tightest gap 1.5 mm (1.2 at minimum). Pens 0.3 mm, so 2.4 × nib = 0.72 < 0.8, and 0.8 governs.
- **Stroke direction:** each streamline is drawn **rim → eye** (the fluid's own direction). The
  pen-down dwell then lands in the sparse far field, and the lift happens in the core. Within a
  rung, strokes are ordered by seed angle (an angular sweep around the rim) so there is no
  cross-rung travel. Rings are drawn inner → outer.
- **Batching:** the longest stroke is ≈ 300 mm (one hero arm, ≈ 30 s), so every stroke is a
  clean batch boundary. There are natural re-zero points between rungs.
- **Budget** (Leo F600 = 10 mm/s, ≈ 2.5 s per lift/drop cycle with the G4 P1.0 dwells):

| layer | draw length | strokes | ≈ minutes |
|---|---|---|---|
| L1 blue | hero ≈ 8.5 m (cropped) + rung 1 ≈ 5 m + rungs 2–4 ≈ 2.5 m ≈ **16 m** | ≈ 650–750 | 27 draw + 28 cycles ≈ **55** |
| L2 black | rings 3.5 m (+ `[faithful]` elevation ≈ 2 m) | 22 (+ ≈ 40) | **7–12** |
| L3 type | ≈ 3 m | ≈ 350 | **≈ 18** |
| L4 red | < 0.3 m | ≈ 60 | **≈ 4** |
| **total** | **≈ 23–25 m** | | **≈ 1 h 25 – 1 h 35, 2 swaps** (blue → black → red) |

  The designer reports the measured numbers. If blue cycles exceed 900, raise d_sep toward 2.8 mm
  before touching anything else.
- **Flood risks:** (1) the hero eye, handled by the termination rule and the stated eye radius;
  (2) rungs 2–4, handled by the cull pass, which must run on the final mm geometry and not on the
  δ-unit geometry; (3) the ring band at 1.12 r_c, handled by the Δψ choice; (4) the red ring
  against rung 4's rim, which needs a ≥ 0.8 mm gap (set by the 1.10 orbit factor).
- **Determinism:** J–L seed order is fixed (start at θ = 0 on the rim, sweep counter-clockwise),
  and Re_Γ, δ₀, d_sep and Δφ are recorded in NOTES. `.gcode` goes beside every render.

---

## 11. Acceptance checks (the critic marks each pass/fail on the png)

1. **Rings vs spiral at 3 m.** The black disc reads as closed concentric circles (no ends, no
   spiral) and the blue hero as an inward spiral. At least 25 mm of bare paper separates them,
   and they never share a texture.
2. **The ladder is exact.** At least 5 blue rungs (0–4). Successive radii are 2.00 ± 0.03 : 1,
   and the centres lie on one stated similarity orbit (collinear `[abstract]`). Rung 1 overlaid
   ×2 on the hero coincides stroke for stroke outside the frame crop. The core arms meet the
   circle at ≈ 7–11° in every rung that shows its core.
3. **The pen floor is honest.** Every spiral has a bare eye (hero ≈ 3 mm radius). Nothing blue
   lies inside the red ring. The red ring is empty and is the only red besides the stamp. The
   minimum blue–blue gap on the gcode is ≥ 0.8 mm.
4. **Hierarchy and silence.** The hero is ≥ 3× the area of any other mass. The lower-left quiet
   zone is ≥ 1/6 of the sheet and is bare (`[faithful]`: ≥ 40 % of it bare). No caption sits on
   lines, and nothing is pressed against the frame except the hero's intended crop.
5. **Status wording.** The stamp has a date, "claimed/unverified", "forced/with a push", and says
   that the unforced case is open. There is no "solved", no "nobody knows", and nothing in the 2D
   disc says "large → small".
