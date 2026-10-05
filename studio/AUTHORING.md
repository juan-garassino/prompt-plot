# AUTHORING — how a picture becomes a plotted drawing

This is the method behind the three reference reconstructions (cubist plate, Dalí
engraving, acrylic Van Gogh) and the method every seat uses here: the in-app
`promptplot studio design --mode scene` loop and Claude Code agents alike. It is
an **illustrator's reconstruction, not an edge map.** Read `TRACING IS NOT
AUTHORING` in `promptplot/generative/DESIGN_RUBRIC.md` first.

The unit of work is a `Scene` (`promptplot/scene/models.py`): an ordered list of
**named objects**, back to front, each with an occlusion `cover`, a `material`, and
`marks` that carry a role, an ink, a physical width and a paint stage. The engine
compiles it (`compile_scene`) — occlusion, mm mapping, nib snapping, pass ordering.
You author the *what*; the engine executes the *how*.

---

## 1. Inspect and decide

Open the reference with vision. Inspect meaningful crops: faces, one repeated
object, the principal flow, a shadowed material, the lettering. Decide **which
elements make this image recognisable** and write them down before drawing
anything. A useful plan is more specific than "this is a face":

- Queen: tall asymmetric crown; turned profile; exposed eye and nose; draped left silhouette.
- Board: four projected corners, regular grid underneath, pieces occluding the grid.
- Flow: a few deliberate smooth curves — not every side of every coloured ribbon.
- Background: omit most of it; keep only the major arches and horizon landmarks.

Pick a **source canvas** in units (the reference's pixel size is fine) and record
approximate landmark coordinates in it. One coordinate system, stated once.

## 2. Write the layer / depth plan

List objects **background first, foreground last**. For each decide:

| field | meaning |
|---|---|
| `name` | functional, not commentary — it drives ink and width rules (`queen veil plane`, `board piece 3`) |
| `cover` | its occlusion polygon. Clipping only — never exported as a fill. A glass pane is not a cover. |
| `material` | `skin` · `hair` · `cloth` · `cubist_plane` · `stone` · `painterly` · `background` |
| light side | which planes are lit and stay **bare paper** |
| guides | for hair/flow: two authored curves the family runs between; for skin: bend + slope of the surface net |
| protect | eyes, lips, highlights, labels — regions no hatch may enter |
| ink, width role | `contour` / `hatch` / `label` / `flow` / `construction` / `accent` |

## 3. Build contours only, first

A small number of confident curves for organic edges; explicit straight segments
for real geometry. Reusable symbols for repeated pieces. Reconstruct a perspective
grid mathematically from its four corners. Author a nose or a fold as a curve —
do not recover the outline of a dark paint patch.

**Render and look.** Crown/profile identity, overlap order, the board's plane,
object scale, label legibility, whether connecting lines actually reach their
targets. Do not hide bad geometry under thousands of hatch paths.

## 4. Add a material grammar

One grammar per material. They are different, on purpose.

**Skin, cloth** — `surface_grid` + `cut_tone`: a warped (u,v) net over the form
whose rows break into dashes by an authored low-frequency tone function. The
oblique cross family is admitted **only in shadow**. Eyes and lips are protected
holes. Phase-stagger adjacent rows (golden ratio) so highlights never form a fence.

**Hair, metal, flowing surfaces** — `flow_family`: two authored guide curves,
interpolated into a coherent family, clipped to the surface. A travelling
highlight interrupts each track at a slightly different point. Reserve strong
edge accents for real dark boundaries; never outline a highlight.

**Cubist planes** — `hatch_polygon` with `physical_hatch` clearance: one hatch
direction per plane, aligned to that plane; cross only selected shadows; **lit
planes stay bare**. Prefer large intentional facets to outlines of pigment speckle.
Name planes carefully — ink rules are semantic.

**Painterly / acrylic** — `brush_family` around authored flow guides, plus
`flow_strokes` on the image's orientation field. Each mark is **one centerline
with a brush width**, never two edges around a paint blob. Stages: underpainting
(broad, low-frequency masses) → body (flow-defining) → accents (high-frequency
highlights). Sample colour from the intended region, **quantise** to a limited
palette. Broad strokes establish area; narrow strokes describe orientation. Later
passes cover earlier ones — cull what is fully hidden.

**Background atmosphere** — usually omit, or a few quiet horizon lines. Nothing
is owed a mark merely because the raster contains it.

## 5. Make pens physical

Widths are millimetres of real nib or brush. Hatch spacing floor is **2.4 × the
finest nib**; hatch inset from an outline is **½ border + ½ hatch + 0.035 mm** of
guaranteed white paper. A finer *stroke width* in a preview does not create a
finer pen. State the total ink count explicitly ("black plus red, yellow, blue =
four inks"). Never quietly drop black or recolour the whole structure.

## 6. Clip, audit, render, and actually look

The compiler removes hidden line segments with exact geometry and keeps hatch
strokes continuous across intersections. Open the render at full page and at
detail. Check at least: a face or organic contour, a hatch intersection, the
lettering, a shadow recess, a flow junction. Compare against the reference **as an
interpretation, not as pixel texture.**

The seven acceptance questions:

1. Can the main forms be recognised without colour fills?
2. Do shadow lines follow the surface instead of forming a random mesh?
3. Are any fine lines really the two sides of one thick source stroke?
4. Are the blackest regions intended, or accidental hatch congestion?
5. Do labels stay readable when the displayed width matches the actual pen?
6. Does a thicker pen create black knots at corners or fill eye highlights?
7. Are there long empty travels or excessive tiny marks with no visible benefit?

No single similarity score answers these.

## 7. Report truthfully

Say which shapes were authored from vision, which repeated objects are procedural,
and what remains simplified. Do not describe edge maps as understood forms. Do not
claim a preview is a physical plot. Deliver the scene JSON, the render, the pen
plan and the reference provenance together.

---

## Where the rules came from

Distilled from the recovered `interpretive_plotter` package (cubist + engraving
scenes, with constants) and the acrylic `AGENT.md` (method prose; its generator was
never saved). Oracle outputs and their previews live in
`gallery/references/oracles/` for comparison. Their own `LIMITATIONS.md` is worth a
read: tracing was tried first and rejected there too.
