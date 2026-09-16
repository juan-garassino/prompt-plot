# CAD_RESEARCH — What PromptPlot's Engine Should Steal from FreeCAD, LibreCAD, and Blender

**Status:** roadmap for review. Synthesized 2026-09-15 from three completed source-level research
reports (FreeCAD Draft/TechDraw, LibreCAD/QCad core, Blender Line Art/Freestyle/Geometry Nodes).
Items are individually pickable — each carries what / why-for-plotter / algorithm sketch / effort /
landing spot. Source tags: **F** = FreeCAD, **L** = LibreCAD, **B** = Blender.

**Engine today (baseline these items build on):** polyline-only strokes → GCode; exact region-clip
module `generative/geometry.py` (Circle/HalfPlane/Band/Rect + Union/Intersect/Complement,
`clip`/`trim_to`/`offset`); from-scratch z-buffer hidden-line terrain engine
`generative/engine3d.py` (isometric, per-piece heightfields — **recently proved too dense to
plot**: full wireframes crowd into black patches); semantic pen slots → physical pens via lamina
style presets; fills limited to rect-serpentine / disc-spiral / quarter / rings; guardrails
(`enforce_line_spacing`, `limit_ink_density`, `occlude_crossings`); single global
`PenConfig.tip_width` (no per-layer width); no arcs/splines, no fillet/chamfer, no general
hatch-region API, no polygon regions, no silhouette/contour extraction, no DXF layer→pen
round-trip.

---

## 1. Executive summary

Three tools, three eras of 2D/3D line-drawing engineering, one striking result: **they converge on
the same two answers to PromptPlot's two biggest gaps.**

**Convergence 1 — the fill language is PAT.** The AutoCAD PAT hatch format (line families:
`angle, x-origin, y-origin, delta-x, delta-y, [dash, gap, …]`, clipped to a region) appears
independently as FreeCAD TechDraw's GeometricHatch **and** as LibreCAD/QCad's hatch engine
(LibreCAD explicitly rejects its own nonstandard DXF-tile hatch in favor of PAT). Two mature
codebases arriving at the same declarative fill spec is a high-confidence signal: PAT is the
correct hatch API for a pen plotter, and its dash specs are literally pen-up/pen-down sequences.

**Convergence 2 — the 3D fix is feature edges + analytic occlusion, not a better z-buffer.** Both
FreeCAD TechDraw's HLR pipeline (HLRBRep_PolyAlgo → 5 edge classes × visible/hidden) and Blender
Line Art (edge_flag_result classification + Appel Quantitative-Invisibility occlusion) solve
"3D model → sparse plottable lines" the same way: **classify edges** (silhouette, crease,
boundary), then **compute per-edge visibility analytically** as integer occlusion counters on
segment lists — never rasterize. This is the direct cure for the too-dense neural-net mesh
series: 5–20% of the ink carries the same 3D read, and hidden lines become *stylable* (QI==1
ghost lines on a light pen) instead of merely deleted.

**Three-phase roadmap:**

| Phase | Theme | Effort | Headline items |
|---|---|---|---|
| **1** | Quick wins — construction & line-quality toolbox | 5 × S | trim/extend wrappers, Upgrade chaining (soup→regions), resample+RDP, dash walker, Path/PolarArray |
| **2** | Fills & regions — the declarative fill language | mostly M | PAT hatch, polygon Region, concentric fill, intersection catalog, fillet/chamfer, bulge arcs → G2/G3 |
| **3** | The 3D rework — engine3d.py successor | M/L | feature-edge classification, Appel QI occlusion, Line-Art chaining, Freestyle style contract, light contours, intersection lines |

Phase 1 items are independent and land inside existing modules. Phase 2 turns `geometry.py` into a
real 2D CAD kernel (the intersection catalog is the enabler for trim/fillet/offset exactness).
Phase 3 is a coherent unit — classification → occlusion → chaining → styling is a fixed pipeline —
and is **the** fix for the density problem; it should be built as a new module beside (not inside)
`engine3d.py`, with pieces migrated one by one.

---

## 2. Phase 1 — Quick wins (all S effort)

Independent, small, each immediately usable by existing pieces.

**1.1 Trim / Extend / Trim-Two wrappers** (source: F Draft Trimex + L trim semantics)
- *What:* shorten or extend a polyline endpoint to its intersection with another entity;
  trim-two cuts both; divide breaks an entity at a point; per-segment mode for polylines.
- *Why for plotter:* the vocabulary of diagram construction — clean T-junctions, exact frame
  meets, closing gaps without eyeballed coordinates. Every piece currently hand-computes these.
- *Algorithm:* extend last segment as a ray → intersect against the target (use `geometry.py`
  clip machinery now; upgrade to the Phase-2 closed-form catalog for arcs) → keep nearest hit →
  rewrite endpoint. Thin functional wrappers; no entity tree.
- *Effort:* **S** (on today's line/region intersections; arc targets arrive free with 3.4).
- *Lands in:* `generative/geometry.py` (new `trim_to_entity`, `extend_to`, `trim_two`, `divide`).

**1.2 Upgrade/Downgrade normalization ladder** (source: F Draft Upgrade)
- *What:* loose edges → joined wires → closed wires → regions; Downgrade explodes back.
  Endpoint-tolerance chaining, closure detection, orientation fix.
- *Why for plotter:* "take any generator's stroke soup and give me a hatchable region." This is
  the bridge between every existing generator and the Phase-2 fill engine — without it, PAT hatch
  only fills shapes we constructed by hand.
- *Algorithm:* hash endpoints on a tolerance grid → chain segments sharing endpoints → detect
  closure (first==last within tol) → fix winding (signed area) → emit closed polygons + leftovers.
- *Effort:* **S**.
- *Lands in:* `generative/geometry.py` (`chain_strokes`, `close_wires`) — feeds the Phase-2
  polygon Region.

**1.3 Resample-by-length + RDP simplify with sharp-corner guard** (source: B Geometry Nodes
resample + GP Simplify)
- *What:* uniform arc-length resampling; Ramer–Douglas–Peucker decimation with a Sharp Threshold
  that exempts real corners; merge-by-distance to kill micro-segments.
- *Why for plotter:* fewer `G1`s → smoother Grbl look-ahead planning and shorter files; uniform
  sampling before any per-point styling (jitter, dashes) so effects are density-independent.
  Immediately useful for `strange_attractor` / `harmonograph` output.
- *Algorithm:* walk cumulative arc length, emit points at fixed step; RDP with per-vertex turning
  angle check — vertices sharper than threshold are pinned and never removed.
- *Effort:* **S**.
- *Lands in:* `generative/kit.py` (or a small `generative/strokeops.py` shared with 4.4's
  pipeline idiom).

**1.4 Shared arc-length dash walker (the linetype engine)** (source: L linetype engine + B dash
shader)
- *What:* one dash-pattern walker parameterized by `[dash, gap, dash, gap, …]` in mm, walked by
  arc length along any polyline, **with phase continuity across polyline joints**.
- *Why for plotter:* dashed/dotted linetypes become a per-layer attribute instead of per-piece
  hand-rolled loops (the black-hole `flow` mode, dash_rain, and future QI ghost lines all want
  this). Phase continuity is what makes a dashed curve look intentional rather than chopped.
- *Algorithm:* carry residual pattern-position across segments; emit sub-polylines for "pen down"
  spans. Same walker later consumes PAT dash specs (3.1) and renders QI==1 hidden lines (4.2).
- *Effort:* **S**.
- *Lands in:* `generative/kit.py` (`walk_dashes(stroke, pattern, phase=0)`); consumed by lamina
  layer linetypes (§5).
- *Note:* cap total repetitions per entity, LibreCAD-style, so a degenerate pattern can't spin.

**1.5 PathArray / PolarArray with alignment modes** (source: F Draft PathArray/PolarArray)
- *What:* stamp a motif N times along a path by arc length (with start/end offsets), oriented
  **Original** (fixed), **Frenet** (rotation from local tangent/normal), or **Tangent**
  (pre-rotated by a fixed offset from tangent); PolarArray = copies around a center.
- *Why for plotter:* ornament borders, ticks along curves, radial furniture — currently
  re-implemented ad hoc in every piece that wants them (sparkle_grid shells, plate furniture).
- *Algorithm:* arc-length parameterization of the spine (reuse 1.3's walker) → per-copy 2×2
  rotation from local tangent → translate motif copy.
- *Effort:* **S**.
- *Lands in:* `generative/kit.py`.

---

## 3. Phase 2 — Fills & regions (mostly M effort)

This phase turns `geometry.py` into a small exact 2D kernel and gives the engine a declarative
fill language. Item 3.4 (intersection catalog) is the load-bearing enabler: 3.5 and full-strength
1.1 sit on top of it.

**3.1 PAT declarative hatch engine** (source: **F + L — convergent, adopt with confidence**)
- *What:* fill any closed region with **line families**, each declared as
  `angle, x-origin, y-origin, delta-x, delta-y, [dash, gap, …]`. `delta-y` = perpendicular
  spacing between family lines, `delta-x` = stagger between successive lines (what makes brick /
  dashed patterns tile), dash spec = the linetype along each line. Standard AutoCAD `.pat` files
  parse directly.
- *Why for plotter:* this **is** the pen-plotter fill vocabulary — every family line is a pen
  stroke, every dash spec is pen-up/pen-down, spacing is guaranteed ≥ declared (plays exactly
  into `enforce_line_spacing` and the tip-width guardrail). Replaces the closed set
  {serpentine, spiral, quarter, rings} with an open, seedable, textual language; ships with
  decades of existing `.pat` libraries.
- *Algorithm:* PAT parser → for each family, generate the infinite line family over the region's
  bbox (index range from bbox projected onto the family normal) → apply `delta-x` stagger per
  line index → clip each line to the region (existing `geometry.clip`; polygon regions via 3.2,
  even-odd spans for holes) → apply dash spec via the 1.4 walker. Cap family iterations
  (LibreCAD hard-limits repetition — keep that guard).
- *Effort:* **M** (S once 1.4 + 3.2 exist; the parser and family generator are simple).
- *Lands in:* new `generative/hatch.py`; exposed to pieces through `kit.py`; pattern choice
  becomes a lamina style attribute (§5).

**3.2 Polygon Region — face-from-wires + even-odd containment** (source: F Part face-from-wires)
- *What:* a `Polygon` region type: one outer closed polyline + zero or more hole wires,
  implementing the same region protocol as Circle/HalfPlane/Band/Rect (containment test +
  boundary clip), plus Union/Intersect/Cut between polygon regions.
- *Why for plotter:* today only analytic shapes can clip/mask. With 1.2 producing closed wires
  from any stroke soup, this makes **every generator's output a maskable, hatchable region** —
  halos around text, hatch-inside-silhouette, negative-space cuts on arbitrary shapes.
- *Algorithm:* even-odd point-in-polygon for containment (holes fall out for free);
  segment-vs-polygon clipping for boundaries. Booleans by segment splitting at crossings +
  containment classification; reach for Greiner–Hormann only if exactness becomes a problem.
  Use LibreCAD's **randomized ray casting** (≥2 rays, random directions, majority vote) for the
  containment test to dodge vertex/tangency degeneracies (see 3.4).
- *Effort:* **M**.
- *Lands in:* `generative/geometry.py` (extends the existing region algebra — this is its
  natural home).

**3.3 Concentric inward-offset fill** (source: F Offset2D iteration + L exact offset)
- *What:* repeatedly offset a closed wire inward by the fill pitch until it collapses —
  concentric fill for arbitrary closed regions (the generalization of the existing disc-spiral
  and rings fills).
- *Why for plotter:* concentric fill reads calmer than hatch on organic shapes, keeps the pen
  moving in long continuous loops (fewer lifts), and doubles as multi-pass fat-stroke: offsetting
  a single open stroke by ±k·tip_width gives any effective line weight from one pen (feeds §5's
  lineweight-as-passes).
- *Algorithm:* per-segment parallel offset + joint resolution (miter below angle threshold, else
  arc/bevel) → **cull self-intersection loops shorter than the pen tip** (both F and L flag
  this; the tip-width cull is the cheap 90% of a full self-intersection cleanup) → recurse until
  area or perimeter collapses.
- *Effort:* **M** for convex/monotone-ish regions (the practical case); **L** only if we chase
  global self-intersection robustness — explicitly don't (see §6).
- *Lands in:* `generative/geometry.py` (`offset_closed`, iterating wrapper in `kit.py` beside the
  existing fills).

**3.4 Closed-form intersection catalog** (source: L `rs_information.cpp` — copy the structure
verbatim)
- *What:* exact pairwise intersections: line–line (parametric), line–arc/circle (project center →
  quadratic), arc–arc (radical line); ellipse pairs only if a piece ever demands them.
- *Why for plotter:* the enabler under 1.1 (exact trim/extend to arcs), 3.5 (fillet centers),
  3.3 (offset joint trims), and precise construction generally. Closed-form = no iteration, no
  tolerance drift.
- *Algorithm:* copy LibreCAD's two battle-tested patterns wholesale: (a) the **onEntities
  filter** — compute intersections on the infinite carriers first, then filter with
  `isPointOnEntity(tol≈1e-4)` per entity, after a bbox pre-filter; (b) **randomized ray
  casting** with ≥2 rays for point-in-contour, to dodge rays grazing vertices or tangent points.
- *Effort:* **S** for the line/arc/circle triangle (all we need); **M** was LibreCAD's full
  catalog with ellipse quartics — skip.
- *Lands in:* `generative/geometry.py` (`intersect(a, b) -> list[Point]`).

**3.5 Fillet / chamfer between entities** (source: L)
- *What:* insert a tangent arc (or straight chamfer) of radius r between two entities, trimming
  both to the tangent points.
- *Why for plotter:* **physical** value, not just cosmetic: a filleted corner keeps the pen
  moving through the turn instead of a full direction reversal — no dwell, no ink pooling at
  sharp vertices (a documented Leo problem: slow feeds + dwells exist precisely because of ink
  pooling). Also the joint-resolution primitive 3.3 wants.
- *Algorithm:* offset both entities by r (3.3's per-segment offset) → intersect the offsets
  (3.4) → that's the arc center → tangent points by perpendicular projection onto each entity →
  trim both (1.1) → insert arc (bulge vertex, 3.6).
- *Effort:* **M** (S once 3.3 + 3.4 exist).
- *Lands in:* `generative/geometry.py`; auto-fillet-all-corners helper in `kit.py`
  (`round_corners(stroke, r)`), attractive as a default postprocess for boxy pieces.
- *Note:* the current instruction not to reverse direction sharply overlaps with `postprocess`
  pen-dwell logic — filleting removes the need for the dwell at that corner; don't double-apply.

**3.6 Per-vertex bulge arcs + G2/G3 emission** (source: L bulge polylines, DXF group code 42)
- *What:* optional `bulge = tan(θ/4)` per polyline vertex (sign = CW/CCW, bulge 1 = semicircle):
  the segment to the next vertex is a circular arc, not a chord. Tessellate **only** at
  GCode/preview time — or emit native `G2`/`G3` when the firmware path allows.
- *Why for plotter:* exact arcs survive offset/trim/fillet downstream (concentric offset of an
  arc is just r±d — trivial and exact); native G2/G3 gives shorter files and physically smoother
  motion (no facet chatter at Leo's slow feeds). This is the one representational change in the
  whole roadmap, and it's what makes 3.3/3.5 exact instead of approximate.
- *Algorithm:* extend the stroke model with an optional per-vertex bulge (absent = 0 = straight —
  fully backward compatible; every existing generator is untouched). Arc geometry from bulge:
  included angle θ = 4·atan(bulge), radius from chord length and θ. Emission: G2/G3 with IJ
  offsets behind a config flag, default off until validated on Grbl; simulator/visualizer
  tessellate at preview resolution.
- *Effort:* **M** (touches models, postprocess bounds-checking of arcs, visualizer, validator).
- *Lands in:* `models.py` (vertex bulge) + `generative/geometry.py` (arc math) + `postprocess.py`
  (G2/G3 emission + arc-aware bounds). **Sequencing:** do this early in Phase 2 if 3.3/3.5
  exactness matters, or late as an optimization — both orders work because bulge=0 is the
  degenerate case.

---

## 4. Phase 3 — The 3D rework (M/L): feature edges + analytic occlusion

**This is the fix for the too-dense neural-net series.** `engine3d.py`'s z-buffer draws the whole
wireframe and merely hides what's behind — density is O(mesh resolution) no matter what.
The F+L+B convergent answer: draw only edges that *mean* something (silhouettes, creases,
boundaries), and compute visibility analytically per edge. Blender's Line Art is the reference
implementation (it's polyline-native, CPU, and readable); FreeCAD's TechDraw PolyAlgo path
independently confirms every stage. Build as a new module; migrate pieces one at a time;
keep `engine3d.py` for pieces where dense terrain mesh *is* the aesthetic.

Pipeline order is fixed: **4.1 classify → 4.2 occlude → 4.3 chain → 4.4 style.**

**4.1 Feature-edge classification — "represent, don't enumerate"** (source: **B Line Art + F
TechDraw HLR — convergent, high confidence**)
- *What:* classify mesh edges into: **silhouette/contour** (`dot(view,n1)·dot(view,n2) ≤ 0`
  between the two faces sharing the edge; per-vertex view vector under perspective), **crease**
  (`dot(n1,n2) < cos(threshold)` — dihedral), **boundary** (one face), **region/material
  boundary** (faces belong to different semantic regions), **marked** (piece explicitly tags an
  edge). Maps 1:1 onto TechDraw's hard/outline/smooth/seam classes — two codebases, same taxonomy.
- *Why for plotter:* the wireframe disappears; 5–20% of the ink carries the same 3D read. Each
  class can go to its own pen/style (silhouette heavy, crease fine, boundary medium) — which is
  exactly the semantic-pen-slot model lamina already implements.
- *Algorithm:* engine3d heightfields already yield a quad/tri mesh with normals. One pass over
  edges: compute the two face-normal dot products against the (per-vertex, for perspective) view
  vector; sign flip → silhouette; dihedral test → crease; single-face → boundary. Emit edges
  tagged with class. Blender reference: `lineart_cpu.cc` `edge_flag_result` (~L1610).
- *Effort:* **S** (the engine has normals; this is a classification pass, no new geometry).
- *Lands in:* new `generative/edges.py` (or `generative/hlr.py` — one module for 4.1–4.3).

**4.2 Appel Quantitative-Invisibility occlusion** (source: B Line Art; F PolyAlgo's
split-and-depth-test is the same idea) — **highest-leverage item in the roadmap**
- *What:* replace the raster z-buffer for *lines*: each projected edge carries a segment list
  with an **integer occlusion counter** per segment. QI==0 → visible; QI==1 → hidden behind
  exactly one surface — plot as dashed ghost lines on a light pen; QI≥2 → drop.
- *Why for plotter:* analytic and resolution-independent (no raster stair-stepping into GCode);
  works directly on polylines; and hidden lines become a *stylistic resource* — the classic
  technical-drawing dashed-hidden-line convention lands for free via the 1.4 dash walker, giving
  cheap depth on a second pen instead of dead ink.
- *Algorithm:* for each classified edge, for every triangle overlapping it in screen space,
  compute the parametric interval [l, r] of the edge covered by the triangle *and in front of
  it* (Blender: `lineart_triangle_edge_image_space_occlusion`); splice cut points into the
  edge's segment list (`lineart_edge_cut`), incrementing the integer counter on covered spans.
  Early-out an edge when its minimum occlusion exceeds the max level we render (2). Brute force
  O(edges × tris) — Blender's screen-space tile acceleration is explicitly deferred (§6);
  at PromptPlot mesh scales (10²–10⁴ tris) brute force is fine. Profile before optimizing.
- *Effort:* **M**.
- *Lands in:* `generative/edges.py`. Interplay: this replaces `_zbuf_terrain` occlusion for the
  new path; the 2D `occlude_crossings` effect stays — it solves a different problem (pen-over-pen
  opacity faking between layers, post-projection).

**4.3 Chaining pipeline — fixed stage order** (source: B `lineart_chain.cc`)
- *What:* turn the occlusion-cut segment soup into long strokes, in Blender's exact stage order:
  **(a)** chain edges sharing exact endpoints → **(b)** split where occlusion level changes →
  **(c)** connect chain ends by image-space proximity (tolerates short occlusion zigzags) →
  **(d)** smooth via a collinearity tolerance filter that guards real features → **(e)** split at
  sharp angles.
- *Why for plotter:* **each chain = one pen-down stroke.** Fewer lifts and fewer stroke starts —
  directly attacking Leo's known ink-pooling-on-lift problem — and RDP-style smoothing (1.3)
  shrinks the GCode. The stage order matters: proximity-connect before smooth, split-on-QI-change
  before connect; don't improvise it.
- *Algorithm:* as listed; (a) reuses 1.2's endpoint hashing; (d) reuses 1.3's guarded simplify.
  Output: chains tagged (edge class, QI level) — the neutral input to 4.4.
- *Effort:* **M**.
- *Lands in:* `generative/edges.py`; chains then flow through normal postprocess.

**4.4 Freestyle style contract — Style = (selection, chaining params, shaders, pen)**
(source: B Freestyle architecture; mostly reorganizing existing effects)
- *What:* the *contract*, not the code: extraction (4.1–4.3) produces **neutral tagged chains**;
  a **Style** owns aesthetics = (selection predicates over class/QI/length, chaining parameters,
  an ordered list of stroke shaders, a pen). Shaders compose in order: resample, thickness
  (constant or along-stroke → N offset passes via 3.3), dashes (1.4), noise jitter/wobble, tip
  remover, simplify.
- *Why for plotter:* this is the missing seam between geometry and lamina. Today every piece
  bakes its ink decisions into generation; with the contract, pieces emit sparse feature chains +
  declare a style pipeline, and lamina style presets gain a stroke-level vocabulary
  (silhouette→pen0 heavy double-pass, crease→pen1, QI1-ghost→pen2 dashed). Restyling a piece =
  swapping a preset, zero regeneration. Slots directly onto the existing semantic→physical pen
  mapping.
- *Algorithm:* `StrokeOp = Callable[[list[Stroke]], list[Stroke]]`; pipelines are plain Python
  lists of ops (`postprocess.py` already is this idiom — extend it upstream; explicitly **no**
  node graph, see §6). Existing effects (echo, wobble, dash_rain) refactor into shaders
  approximately for free.
- *Effort:* **M**, mostly reorganization.
- *Lands in:* `lamina/styles.py` (Style dataclass + per-class line-style table) + a small shader
  registry in `generative/kit.py` or `strokeops.py`.

**4.5 Light contour — light as a second camera** (source: B `use_contour_secondary`)
- *What:* run the same 4.1 sign-flip test with the **light direction** in place of the view
  vector: one clean stroke exactly where lit surface turns to shadow. Optionally hatch (3.1) only
  inside the shadow region.
- *Why for plotter:* cheap tonal depth — one terminator line plus optional shadow hatch reads as
  full shading for a fraction of the ink. On the neural-net terrains this replaces entire dense
  mesh regions with a single contour + a light PAT fill.
- *Algorithm:* on heightfields, even simpler than the mesh test: `dot(light_dir, normal)` is a
  scalar field → its zero-crossing via marching squares — the `contour_field` machinery already
  exists. Shadow region = the negative side, closed via 1.2 → polygon Region (3.2) → hatch.
- *Effort:* **S–M** (S for the terminator line alone).
- *Lands in:* `generative/edges.py` (test) + `contour_field` helpers; shadow-hatch wiring via
  3.1/3.2. **Explicitly skip full cast shadows** — needs a complete second occlusion pass from
  the light (Blender's `lineart_shadow.cc`); §6.
- *Note:* light-contour is independent of 4.2/4.3 — it can ship right after 4.1 as an early win.

**4.6 Intersection lines — reduced cases only** (source: B intersection strokes + F Part
Section)
- *What:* where two surfaces cross, the intersection curve becomes a first-class chain. Take
  only the reduced cases: **heightfield-vs-plane** (= FreeCAD Part Section; a stack of planes
  gives the sliced-form aesthetic) and **heightfield-vs-heightfield**. Skip general mesh–mesh.
- *Why for plotter:* section stacks are a proven plotter aesthetic (generalizes the existing
  marching-squares `contour_field` from top-down level sets to arbitrary section planes); surface
  crossings on composite pieces (e.g. a plane slicing a loss surface) get a crisp drawn seam
  instead of a visual mush.
- *Algorithm:* both reduced cases are **marching squares on a difference field**
  (`h1(x,y) − plane(x,y)` or `h1 − h2` = 0) — machinery that exists. Chain via 1.2, project,
  tag as its own edge class into 4.2 occlusion.
- *Effort:* **M** as scoped (**L** only if general tri–tri is attempted — don't).
- *Lands in:* `generative/edges.py` + `contour_field` helpers.

---

## 5. Layer→pen model (source: L layer model + QCad plotter heritage; S–M)

LibreCAD's layer model is a direct pen-plotter inheritance — QCad documentation is explicit that
the plotter picked its physical tool from an entity's **lineweight / colour / layer name**. The
mapping table *is* the deliverable. PromptPlot already has half of this (semantic pen slots →
physical pens in lamina); the missing attributes:

| Layer attribute | Today | Adopt | Plotter meaning |
|---|---|---|---|
| pen / color index | ✅ per-stroke `color` | keep — becomes `ByLayer` default with per-entity override | which physical pen |
| **lineweight** | ❌ single global `PenConfig.tip_width` | **per-layer width** | ceil(width / tip_width) = number of offset passes (via 3.3) — fat strokes from any pen |
| **linetype** | ❌ hand-rolled per piece | per-layer dash pattern | rendered by the 1.4 walker at postprocess, phase-continuous |
| **construction / no-print** | ❌ (scaffolding strokes get manually dropped) | boolean `plot=False` | guides, registration aids, layout scaffolding flow through preview but never reach GCode |
| name / semantic role | ✅ lamina semantic slots | keep; layers *are* the semantic slots | style presets map role → (pen, weight, linetype) |

- *What:* a `Layer` record `(name, pen, lineweight_mm, linetype, plot: bool)`; entities resolve
  attributes `ByLayer` with optional per-entity override (LibreCAD's exact resolution rule).
  **Text-as-layer is first-class**: labels live on their own layer with their own pen/weight —
  which formalizes what the MLP-manifold piece's halo/label logic already does by hand.
- *Why for plotter:* per-layer lineweight is the single biggest expressive unlock here — the
  Phase-3 style contract wants silhouettes heavier than creases, and today that's impossible
  without changing physical pens. Construction layers formalize the trace-limits/registration
  workflow. And the layer table closes the **DXF round-trip**: `importers/dxf_import.py` already
  groups by DXF layer — importing layer attributes (and exporting them back) makes PromptPlot ↔
  CAD a lossless loop.
- *Algorithm:* dataclass + resolution function; `postprocess` consumes lineweight → multi-pass
  offset (3.3) and linetype → dash walker (1.4); `plot=False` layers filtered before GCode
  emission but rendered (faintly) in the visualizer.
- *Effort:* **S** for the model + ByLayer resolution; **M** total once weight→passes and
  linetype rendering are wired.
- *Lands in:* `lamina/styles.py` (layer table lives with the presets) + `models.py` (entity
  layer ref) + `postprocess.py` (weight/linetype realization) + `importers/dxf_import.py`
  (round-trip).

---

## 6. NOT porting (with reasons)

Explicit rejections — each was considered in at least one source report.

| Rejected | Source | Reason |
|---|---|---|
| OCCT exact kernel / `HLRBRep_Algo` exact HLR path | F | Exact B-rep HLR needs the whole OCCT geometry stack. TechDraw itself ships the polygonal `PolyAlgo` path, and Draft Shape2DView flattens to polylines anyway — even FreeCAD's productized answer is the one we're building in 4.1–4.3. |
| NURBS / Béziers / splines as modeling entities | F, L, B | Polylines + bulge arcs (3.6) cover the plotter's expressive range; splines drag in knot math, fragile offsets, and tessellation policy for zero pen-visible gain. Tessellate at import instead. |
| Sketcher constraint solver | F | DogLeg/LM over constraint Jacobians is a project in itself; lamina layout + `reserve_bands`/`split_panels` already solve our placement problems. Escape hatch if ever truly needed: `pip install planegcs`. |
| `bpy` / scene graph / depsgraph; node-graph eval with fields/lazy DAGs | B | We need the *ops*, not the runtime. Plain `list[StrokeOp]` pipelines (4.4) capture the composability with zero infrastructure — postprocess.py proves the idiom already. |
| Snapping, working planes, action framework, Stretch — interactive UI machinery | F, L | PromptPlot constructs programmatically; there is no cursor. |
| Document/undo model, `RS_Entity` OO tree | L | Keep the engine functional and pure-data; versioning is git's job. |
| Dimensions / MTEXT | F, L | Technical-drawing annotation, not generative art; lamina type blocks cover captions. |
| Blocks / inserts | L | Motif reuse is a Python function call; PathArray (1.5) covers stamped repetition. |
| LibreCAD's nonstandard DXF-tile hatch | L | LibreCAD's own report says adopt PAT instead (3.1). |
| Freestyle ViewMap curvature lines (suggestive contours, ridges/valleys) | B | Per-vertex curvature estimation is numerically fragile — partly why Freestyle was deprecated in favor of Line Art. 4.1's five edge classes carry the read. |
| Tile/quadtree screen-space acceleration, multithreaded occlusion | B | Premature at PromptPlot mesh scales; brute-force O(edges×tris) first, profile, then decide. |
| Full cast shadows (`lineart_shadow.cc` generality) | B | Requires a complete second occlusion pass from the light. 4.5's light-contour + shadow-region hatch delivers most of the tonal value for a fraction of the cost. |
| DXF R12 ACI color baggage | L | Layer→pen table (§5) maps semantics directly; no need to inherit the 256-color ACI palette. |
| Ellipse–ellipse / quartic intersections | L | No piece needs them; the line/arc/circle triangle (3.4) is the working set. |

---

## 7. Suggested sequencing & dependencies

```
Phase 1 (parallel, independent):  1.1  1.2  1.3  1.4  1.5
Phase 2:  3.4 ──► 3.5            3.2 ◄── 1.2
          3.6 (early or late)     3.1 ◄── 1.4 + 3.2
          3.3 ──► §5 lineweight   3.3 ◄── 3.4 (joint trims)
Phase 3 (fixed order):  4.1 ──► 4.2 ──► 4.3 ──► 4.4
                        4.1 ──► 4.5 (early win, independent of 4.2/4.3)
                        4.6 after 4.2 (needs occlusion for seams)
§5 layer model: model is S anytime; realization needs 1.4 (linetype) + 3.3 (weight passes)
```

First plate-visible payoffs, in order: **1.4 + 1.3** (cleaner lines everywhere, same day),
**4.1 + 4.5 on one neural-net piece** (the density fix demonstrated), **3.1 + 3.2** (hatch any
shape), then the full 4.2/4.3/4.4 pipeline migration.

---

## 8. Sources

**FreeCAD** — github.com/FreeCAD/FreeCAD `src/Mod/TechDraw/App/GeometryObject.cpp` (HLR
pipeline); FreeCAD-documentation wiki mirrors: `Draft_Workbench`, `Draft_Trimex`,
`Draft_Upgrade`, `Draft_PathArray`, `Draft_Shape2DView`, `TechDraw_GeometricHatch`,
`Part_Section`; occt3d.com `HLRBRep_HLRToShape` refman; pypi.org/project/planegcs.

**LibreCAD / QCad** — docs.librecad.org fundamentals + tool references; github.com/LibreCAD
`rs_information.cpp` (intersection catalog, onEntities pattern, randomized ray casting); ezdxf
lwpolyline bulge docs; afralisp bulge tutorial; qcad.org layer tutorials + plotter-heritage
forum thread.

**Blender** — docs.blender.org Line Art manual;
`source/blender/modifiers/intern/lineart/lineart_cpu.cc`
(`MOD_lineart_compute_feature_lines_v3`, `edge_flag_result` ~L1610,
`lineart_triangle_edge_image_space_occlusion`, `lineart_edge_cut`), `lineart_chain.cc`,
`MOD_lineart.hh`, `lineart_shadow.cc` (rejected); LANPR GSoC proposal (Yiming Wu); Freestyle
python / line-set / geometry-modifier docs; Geometry Nodes resample + Grease Pencil Simplify
docs; generativehut obj→plotter workflow; FreePencil2-svg.

**Shared** — AutoCAD PAT hatch-pattern spec (help.autodesk.com GUID-A6F2E6FF); Bénard &
Hertzmann, *Line Drawings from 3D Models: A Tutorial*, arXiv:1810.01175 (the QI / feature-edge
canon); Quantitative Invisibility (Appel 1967) reference article.
