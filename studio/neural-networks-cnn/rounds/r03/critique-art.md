# Art critique — neural-networks-cnn r03 · canon: none declared (lineage: Nees, *Schotter*) · 2026-09-28
render: ~/Downloads/pp_neural_networks_cnn_iterate_v5.png

This slug has no `encoding.md` or `BRIEF.md`, so the plate is judged against the HANDOFF thesis, its lineage and DESIGN_RUBRIC. Coordinates are sheet mm as shown on the preview axes (x right, y up). The drawable area is x 10–200, y 10–287. The preview is on white; per A12 that is not held against the plate.

## Scores
| dim | score | why |
|---|---|---|
| 1 hierarchy | 6 | At 3 m you see a diagonal staircase of four hatched parallelograms first and the stencil title second. The crimson summit coil (x 132–146, y 246–276) is the loudest single mark, but it has no black body under it, so it reads as a floating spring rather than the peak everything climbs to. The top 7² plane was meant to be the destination. Instead it is the weakest part of the sheet: three or four sparse profiles, broken, plus a flat baseline (x 90–176, y ≈ 204). The climax is the least resolved zone on the plate. |
| 2 grid & alignment | 7 | The right edges of the four lower planes share x ≈ 195, which is a real axis. The inter-layer gaps are equal. The title and caption share one flush-left axis at x ≈ 14.5. That axis misses the input plane's left corner (x ≈ 17.5) by 3 mm: close enough to look like an error, too far apart to count as shared. The top plane follows no edge of the stack; its baseline ends at x ≈ 176 and its rows at x ≈ 193. |
| 3 tension & asymmetry | 7 | A strong diagonal runs from the full-width input at the bottom left up to the summit at the top right. The heavy title block in the upper left counterweights it. Nothing crops at the frame. |
| 4 negative space | 7 | The empty wedge under the title (x 10–70, y 60–215) is shaped by the stagger. The four equal gaps of ≈ 11 mm are now a declared rhythm. The crimson ERF loops lie across the black rows. That overlap is defensible, because the loop is on the surface. |
| 5 craft for pen | 7 | 2 pens, no floods, 9,826 commands, and 3.5 m of travel against 13.3 m of draw, a large improvement. Problems: (a) orphan stubs and torn rows. On the top plane these sit at x 117–119 / y 232–237 and x ≈ 131 / y 239–245. On the 28² plane some dashes are under 3 mm, there is a near-vertical spike at x 76–81 / y 143–150, and the front-left corner is torn at x ≈ 50 / y ≈ 115. (b) A black ridge (x 145–148, y 243–259) runs along the right tips of the crimson rings, so black and red will touch there. (c) The title glyphs are still doubled strokes about 0.6 mm apart, and they will merge. |
| 6 concept legibility | 6 | Read bottom to top, "fine noise settles into one red summit" lands without labels. With the rails gone, the apparatus has gone too. But the form is still stacked projected activation reliefs of shrinking size, which is the CNN-hierarchy figure made of data. The *Schotter* order breaks in two places. The disorder is not monotone: the 28² plane is more chaotic than the 56² plane below it. And the 7² plane switches register, to fat isolated hills, instead of finishing the gradient. There is no twist. |
| 7 depth & dimensionality | 7 | Hidden-line profiles make planes 1–4 read as surfaces; the 14² hill occludes its far rows properly. The oblique basis is shared across planes and the planes shrink. There is no weight or density falloff between planes, and the top plane loses solidity. |

avg **6.71** · min **6** · **VERDICT: FAIL**

## Reads at a glance
A stranger at 3 m sees a staircase of scan-line landscapes that start dense and noisy at the bottom left and thin out toward a small red coil at the top right, next to a big letter-spaced title.

## Acceptance checks
(There is no encoding §11. These checks come from the HANDOFF claims and the open ledger wording.)
- Every map drawn only as horizontal hidden-line profile rows: **PASS** (no mesh, no ticks, apart from the spike at x 76–81 / y 143–150).
- Row pitch ≥ 1.0 mm and no run shorter than 3 mm: **FAIL**. The pitch passes, but there are stubs on the 28² and 7² planes.
- Commands < 12,000: **PASS** (9,826).
- One closed crimson loop on each of the 4 lower maps: **PASS**.
- Crimson loops hidden behind nearer terrain: **FAIL**. None of the loops breaks anywhere. On the 14² plane the back arc runs over the hill crest (x 105–125, y 185–192).
- 9 summit isolines, wholly crimson: **PASS** on count and pen. They read as open front arcs, like a coil, not as rings on a hill.
- Nothing crimson between layers / no frustum: **PASS**.
- Equal inter-layer gaps (≈ 10.9 mm): **PASS**.
- Plane widths shrink monotonically in one basis: **PASS**.
- Frame clearance (title ≥ 6 mm under the top margin; no edge on a margin line): **PASS** (title top y ≈ 281, right edges x ≈ 195).
- *Schotter* order: one element, one parameter, monotone order→disorder: **FAIL**. The element is right, but the gradient is non-monotone at 28², and the top plane is a different language.
- Stands up hung beside Nees: **FAIL**. As an idea it would hold. The unresolved top would not.

## Biggest weakness
The destination fails. "Meaning" should be the one resolved form the stack climbs to, but the 7² plane is a few broken profiles and a flat baseline, with a crimson coil hovering over them. The strongest part of the idea is drawn with the least conviction.

## Mandates
1. **Finish the top plane as the climax.** All 7 profile rows are visible, each running continuously across the plane (x ≈ 93 → 193). The argmax hill has a black hidden-line silhouette, so the crimson isolines sit on a visible mountain rather than floating. Remove every top-plane fragment shorter than 4 mm (x 117–119 / y 232–237, x ≈ 131 / y 239–245). No black stroke comes within 1 mm of a crimson ring (the ridge at x 145–148, y 243–259). Test: count 7 rows; the summit has a black outline from base to cap; no black/red contact.
2. **Make the *Schotter* gradient monotone.** Stroke fragmentation must fall strictly from bottom to top. The 28² plane (y 110–150) must look calmer than the 56² plane (y 60–100), with fewer and longer strokes, and the top plane calmest of all. Use per-plane height exaggeration or roughness, not new marks. Remove the spike at x 76–81 / y 143–150 and the torn corner at x ≈ 50 / y ≈ 115. No stroke anywhere is under 3 mm. Test: side by side, each plane has visibly fewer breaks per row than the one below it.
3. **Put the crimson loops through the hidden-line.** Wherever a nearer ridge of the same map rises in front of a loop, the loop breaks with a clear gap of at least 0.8 mm on each side, as the black rows already do. The first place to check is the 14² plane's back arc over the hill (x 105–125, y 185–192). Test: at least one visible occlusion break on the 14² and 28² loops; no crimson line crosses the face of a nearer black ridge.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| A1 no schematics / no rails / nothing crimson between layers | FIXED (on the letter) | No rails, frustum or card edges; all crimson sits on a plane. The stack of shrinking reliefs still recalls the hierarchy figure (concept 6). |
| A2 one grammar, pitch ≥ 1.0, no run < 3 mm, < 12k commands | PARTIAL | Rows only on every plane and 9,826 commands. Stubs under 3 mm remain on the 28² and 7² planes, plus the spike at x 76–81 / y 143–150. |
| A3 crimson scarce, closed, occluded, wholly-crimson isolines | PARTIAL | One closed loop per lower map and wholly-crimson isolines are both fixed. Occlusion is not: no loop breaks behind nearer ridges. |
| A4 top-terrain hidden-line (was regressed) | PARTIAL | Far rows no longer run through the hill, but the top surface no longer reads as a surface at all: broken rows, stubs, and black touching the crimson cap. |
| A5 vertical rhythm | FIXED | Four equal gaps of ≈ 11 mm. |
| A6 frame clearance | FIXED | Title top y ≈ 281 (6 mm clear); plane right edges x ≈ 195; input bottom y ≈ 15. |
| A11 doubled title strokes / close front-row pairs | PARTIAL | The front-row pairs on the input plane are resolved. The title is still doubled strokes about 0.6 mm apart (deferred per ledger, still open). |
| A12 cream preview | argued, not docked | Still renders on white. |
| S1 top plane whole, width ≤ 14² plane | FIXED (visual) | The 7² plane is ≈ 100 mm wide, fully inside the frame and nothing is clipped. |
| S2 resolution keys + crimson key + ERF contrast | FIXED (visual) | The caption reads 224²…7², "50% of ∂CAM(4,3) gradient mass" and "~26% of image vs cell 1/49". |
| S3 disclose the transform | FIXED (visual) | "CAM − MEAN, CLIPPED AT 0" is printed. |
| S7 preprocessing word | NOT FIXED | The caption does not mention the centre-crop or resize. |

DESCRIPTION § Keep:
- Morphology gradient up the stack: **partly true.** It still reads bottom to top, but it is non-monotone at 28² and breaks register at 7².
- Single crimson summit as the scarce, loud accent: **weakened.** It is still the loudest crimson, but it now floats as a coil with no mountain under it.
- Dashed rails fanning upward: **deliberately gone** (A1).
- Rightward stagger: **still true.**
- Hidden-line occlusion on the terrains: **true for planes 1–4, lost on the top plane.**

## Regressions vs compare-to (r02, pp_neural_networks_cnn_one-valley_v12)
- **The summit lost its mountain.** In r02 the CAM peak (x 115–160, y 190–268) was one solid hidden-line mountain carrying a crimson cap, and it was the plate's dominant mass. In r03 it is a crimson coil floating over three broken black profiles. Hierarchy is down, and so is the plate's reading destination.
- **The top plane stopped reading as a plane.** r02's 7² terrain had a bottom edge and a continuous surface. r03 has one bare baseline and scattered hills.
- **The top of the sheet got lighter than the middle.** Visual weight now peaks at the 56²/28² planes, and the stack tails off instead of arriving.
- Banked gains: rails gone; one grammar; commands 26.6k → 9.8k; travel 12.6 m → 3.5 m; equal gaps; frame clearance; honest caption keys.
