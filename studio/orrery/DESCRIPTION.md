# ATTENTION (the orrery) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/orrery` |
| current render | `gallery/studio/orrery/current/pp_orrery_v6.png` |
| source | `studio/orrery/rounds/r01/piece.py::orrery_attention` |
| reference | `studio/orrery/ref/reference.png` |
| paper · pens | A4 portrait, cream · 0 crimson = Q system + bundle · 1 blue = K · 2 ochre = V · 3 green = Z · 4 black = central system, enclosing circles, axes, stars, moons, corner marks, title |
| status | unreviewed (no FEEDBACK.md) · 6 renders on disk |

## In one line
Attention drawn as **an orbital system**: four planetary systems (Q, K, V, Z) circle a central Q·Kᵀ/softmax sun inside one big dotted orbit, and coloured bundles of curves carry Q, K and V into the central rings and Z out of them. It is an exact reproduction of an engraved orrery reference.

## What is on the sheet
Coordinates are (u, v) on the 210 × 297 sheet.

- **Central system (dominant mass).** Concentric rings centred at (0.50, 0.43), about 17 of them from r ≈ 12 mm to r ≈ 41 mm, some solid and some dotted, with the r ≈ 41 mm ring double-passed as the heavy rim (spanning u 0.30–0.70, v 0.29–0.57). Seeded black nodes of 1–3 mm sit on the solid rings, a few hollow, a few joined by short links. Centred type: `Q · Kᵀ` at (0.50, 0.42) (the middle dot renders as a tiny stray mark, not a centred dot), an open circle on the axis, and `SOFTMAX` in caps at (0.50, 0.46).
- **Enclosing orbits.** A large dotted circle about the same centre, radius ~85 mm (u 0.10–0.92, v 0.20–0.77), crossing behind Q, K, V and Z. Two medium dotted arcs inside it, open at the lower-left and lower-right.
- **Axes.** A dash-dot horizontal through the centre at v 0.43 (u 0.14–0.86), with dots and open circles where it crosses rings. A fine dotted vertical centreline at u 0.50 from the title rule (v 0.17) to the bottom mark (v 0.88).
- **Q system (upper-left, crimson).** Hub disc at (0.21, 0.32), ~5 eccentric orbits out to r ≈ 17 mm, satellite dots, a dotted outer arc trailing down-left to (0.16, 0.42). A vertical axis runs through the hub from v 0.26 to 0.43, with a six-point star at (0.21, 0.22). `Q` at (0.16, 0.19). A bundle of five crimson curves with nodes leaves the hub and lands on the central rim at u 0.35–0.38, v 0.32–0.43.
- **K system (upper-right, blue).** Hub at (0.79, 0.27), orbits to r ≈ 23 mm plus a dotted outer ring, and a star on its vertical at (0.79, 0.16). `K` at (0.89, 0.30). An open circle at (0.90, 0.24). A bundle of six blue curves sweeps down-left onto the central rim's upper-right quadrant (u 0.57–0.72, v 0.30–0.43).
- **V system (lower-right, ochre).** Hub at (0.81, 0.58), orbits to r ≈ 17 mm, dotted outer, and a star at (0.83, 0.48). `V` at (0.88, 0.56) sits on its own outer orbit. Five straight ochre lines fan from the hub up-left to the central rim's lower-right (u 0.60–0.70, v 0.48–0.55).
- **Z system (bottom-centre, green).** Hub at (0.50, 0.76), orbits to r ≈ 12 mm, a dotted outer ring, short horizontal ticks either side. Five green curves rise from the hub, fanning out to the central rim's bottom (u 0.36–0.60, v 0.52–0.55): a narrow stem widening like a wineglass. `Z = AV` at (0.50, 0.84).
- **Furniture.** Plain `+` corner marks at (0.09, 0.12) and (0.91, 0.12). Circle-in-cross marks at (0.09, 0.88) and (0.91, 0.88), and a diamond-cross at (0.50, 0.88). The title `ATTENTION` in spaced monoline caps at (0.35–0.65, 0.12), with a rule and an open circle at v 0.15. Three moon-phase discs with hatched shadow: (0.10, 0.51), (0.14, 0.61) inside a dotted ring and tied by a dash-dot sight line to the central rim, and a small one at (0.70, 0.64). A star on a vertical line at (0.81, 0.82). Ten scattered field dots.
- **Empty bands.** The top (v 0.03–0.11) and bottom (v 0.89–0.97) are bare cream: the reference's 4:5 fitted to A4.

## The science it encodes
From `rounds/r01/NOTES.md`: nothing is computed. It is an **exact recreation** of the reference, with every hub, orbit radius and satellite measured off the bitmap (colour-masked components, ray scans, least-squares circle fit) except the ~70 central nodes, which are seeded to match the reference's statistics, not its positions. The mapping of attention to orbits is metaphorical: Q, K, V and Z as bodies and the bundles as flows. No weight, score or softmax value drives any radius. The notes list what could not be matched: serif/italic type, four ink weights per colour, the reference's hand-drawn bundle curvature, and moon hatching at 0.4 mm. The node fills deliberately go under the pitch floor (0.32 mm serpentine) inside ≤ 3 mm discs. Plot: 21.4k commands, 7.7 m draw, 7.4 m travel, ~1 900 pen cycles, mostly dots.

## How it got here
- **v2–v5**: the V bundle curved: arcs left the central system's lower rim, swung down and around, and entered the V hub from the left, as in the reference. The Z bundle rose from Z and curled up into the central rings. v2's central rings were heavier (more double passes) and the node fills were spirals (34k commands).
- **v6 (current)**: the node fills became serpentines (21k commands), and the V bundle became a straight radial fan from the V hub to the rim. That loses the reference's swinging sweep and makes V the most mechanical element. The Z stem is now a clean converging fan.
- No feedback from Juan.

## Keep — what works
- The central system as the dominant mass. At ~40 % of sheet width it is the only element in this family of attention plates that clearly wins at 3 m.
- The asymmetric placement of the four satellites (Q high-left, K higher-right, V low-right, Z bottom-centre) gives real off-axis balance around a centred sun: the reference's best compositional idea.
- The big dotted enclosing orbit tying all four systems into one field.
- Economy: 5 pens, 7.7 m of ink, mostly single-weight hairlines, with scarce, clearly distinct colour per system.
- The engraver's furniture (stars on verticals, moons, corner marks) is consistent, sparse, and on shared verticals (the Q and K stars sit on their hub axes).

## Weak — what doesn't
- [concept] It is an illustration: the viewer names an object (an orrery or astrolabe) and hangs attention on it. No quantity sets any radius, orbit or bundle width, so the metaphor carries no data (§ 6: "decoration is cut").
- [craft] Monoline caps for `SOFTMAX` and a broken `Q · Kᵀ` (the dot renders as a stray mark) at the heart of the sheet. The type is the weakest ink on the plate.
- [depth] One ink weight. The central sun is 17 near-equal rings, which reads as a flat target rather than the reference's layered grey-to-black depth.
- [craft] The V bundle (v6) is five straight lines, which clash with every other connector's curve. `V` sits on its own orbit at (0.88, 0.56), a label grazing geometry.
- [space] The empty top and bottom bands (~22 mm each) are letterbox residue, not shaped space. The dotted enclosing circle stops short of using the sheet.
- [hierarchy] The satellites are all similar size (Q ≈ V ≈ Z, K slightly bigger), with no ranking among the second tier.
- [grid] The title sits on the centreline, but the corner `+` marks sit at v 0.12 and the circle marks at v 0.88. The frame is 76 % of the sheet height and lines up with nothing else.

## Next versions
1. **orbits-that-mean** (mechanism) — keep the orrery composition and make it data. Each satellite's orbit radii are the norms of real Q/K/V rows (e.g. one GPT-2 head). The central rings are softmax weights (ring radius ∝ cumulative attention, ring weight ∝ weight), and bundle widths are attention weights. The plate stops being decoration without losing its best-in-family hierarchy.
2. **resonant-orbits** (abstract) — join this to the resonance family's order: Q and K as two orbiting bodies whose period ratio is the dot product, drawn as a single long spirograph trace that closes (resonance, high attention) or fills an annulus (no resonance). An ORBITAL order where the mechanism is the geometry, and the drawing is one continuous line.
3. **orrery-restored** (faithful) — revert V to the v2–v5 swinging arcs, fit the composition to A4 height (a slightly wider enclosing circle cropped at the side margins) to kill the letterbox, and set `Q · Kᵀ` and `softmax` in the new lowercase glyphs from `studio/resonance`.

**If only iterating:**
1. Restore the curved V bundle from v5 (arcs leaving the central rim's lower edge and swinging into the V hub from the left), and move `V` clear of its orbit.
2. Scale the whole composition 1.2× about (0.50, 0.45) so the enclosing dotted circle crops at the left and right margins and the top/bottom letterbox bands vanish.
3. Fix the central type: a real centred dot in `Q · Kᵀ` and a lowercase `softmax`, each knocked out of the rings by a halo.
