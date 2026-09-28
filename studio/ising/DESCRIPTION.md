# CRITICAL — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/ising` |
| current render | `gallery/studio/ising/current/pp_ising_v6.png` |
| source | `studio/ising/rounds/r01/piece.py::ising_critical` |
| paper · pens | a4 portrait, cream · 0 black = domain walls (1–3 passes by domain scale), deck, type, chart · 1 crimson = the macroscopic interface, the empty Tc plate, the `1.00` tick, the Tc line in the chart |
| status | unreviewed (no feedback) · 8 renders on disk |

## In one line
The 2D Ising model at Tc drawn as a **lattice-with-defects** — the dual-lattice domain walls of a real Wolff-sampled 128² configuration, where pen passes = the size of the smaller domain a wall separates and crimson = the one wall between two macroscopic domains — with a small temperature deck and an order-parameter chart underneath.

## What is on the sheet
Reading order: the big wall field upper right, the crimson interface meandering through it, then the diagonal temperature deck lower left, then the footer and chart.

- **Hero field** (dominant mass, ≈0.65 of sheet width): a square window u 0.30–0.95, v 0.03–0.50, flush to the drawable top and right edges, its left and bottom edges defined only by where the walls stop (a short black baseline stub at u 0.30–0.37 and u 0.87–0.95, v 0.50). Contents: staircase polylines on a ~1.07 mm lattice —
  - hundreds of tiny closed rectangular loops (1–3 sites, 1 pass) scattered evenly over the whole window;
  - mid-size ragged islands in 2 passes (e.g. u 0.35–0.45, v 0.20–0.30);
  - a few bold 3-pass continents in black (u 0.47–0.55, v 0.24–0.32; u 0.75–0.90, v 0.38–0.47; u 0.62–0.68, v 0.07–0.13);
  - **the crimson interface**: one long branching staircase wall that enters at the top edge (u 0.32 and u 0.64), wanders down the right half with fjords and peninsulas, reaches the right edge at v≈0.15–0.25, and a second crimson strand crosses the lower half from the left edge (u 0.30, v 0.33) to the bottom edge (u 0.55–0.85, v 0.50). It is the longest and most continuous line on the sheet.
- **Title block over the field's upper-left**, flush left at u 0.06: `C R I T I C A L` (hairline spaced caps, ~7 mm, u 0.06–0.62, v 0.10–0.13), `DOMAIN WALLS AT EVERY SCALE` (v 0.16), `ONE RULE     NO LENGTH SCALE` (v 0.18). The walls stop around the type (a halo) — the field is carved out behind the words from u 0.30 to u 0.66, v 0.08–0.20; left of u 0.30 the title sits on bare paper.
- **Quiet band** v 0.50–0.58 across the full width, crossed by two black dotted blow-up rays from the empty Tc plate to the hero's bottom corners (to u 0.30 and to u 0.95).
- **Temperature deck** (second mass), lower left, running as a descending diagonal: label `T IN UNITS OF TC` (u 0.06, v 0.58); an axis line from u 0.06, v 0.64 to u 0.57, v 0.83 with ticks and labels `0.75`, `0.90`, crimson `1.00`, `1.20`, `1.80`; five equal parallelogram plates (≈0.28 wide) stepping down-right along it:
  - `0.75` (u 0.10–0.38, v 0.60–0.68): almost empty, two specks.
  - `0.90` (u 0.19–0.48, v 0.64–0.72): a handful of small loops.
  - `1.00` (u 0.29–0.59, v 0.67–0.75): **empty**, outlined in crimson dashes — "its content is the hero".
  - `1.20` (u 0.38–0.67, v 0.71–0.80): a labyrinth of mid-size walls.
  - `1.80` (u 0.47–0.72, v 0.74–0.83): dense short fragments, overlapping (and occluding) the 1.20 plate's corner.
- **Footer**, u 0.07–0.66, v 0.84–0.95, under a black rule, set in a plain (non-spaced) mono stroke font: `WOLFF AND METROPOLIS   L 128   PBC   SEED 7   SYMMETRIC SECTOR` / `TC 2.269185   ONSAGER 1944   EXACT` / `UNSATISFIED BONDS   CHAIN 0.1501   ONSAGER 0.1464` / `THIS CONFIGURATION   M 0.018   464 DOMAINS` / `LINE WEIGHT   THE SIZE OF THE DOMAIN THE WALL ENCLOSES` / `RED   BOTH DOMAINS OVER 3 PCT OF THE LATTICE`.
- **Order-parameter chart**, u 0.74–0.95, v 0.80–0.94: `ORDER PARAMETER` / `EXACT   PLATES L 24`; an L-axis, the exact Onsager–Yang m(T) curve falling vertically at Tc, a crimson dashed vertical at Tc, four `+` markers for the plates, axis labels `0.55` and `1.95`.

## The science it encodes
From `r01/NOTES.md` and the docstring: 2D Ising, J = 1, zero field, periodic 128² lattice at Tc = 2/ln(1+√2) = 2.269185 exactly; checkerboard Metropolis burn-in then Wolff single-cluster (P_add = 1−exp(−2βJ)); domains are exact 4-connected components; walls are dual-lattice edges, wrap bonds counted but not drawn. Pen weight = min(|A|,|B|): 1 pass < 10 sites, 2 < 120, 3 above; crimson when the smaller domain ≥ 3 % of the lattice. Exact check printed on the sheet: unsatisfied-bond fraction 0.1501 (chain) vs Onsager 0.146447. Hero picked as the least-magnetised of 16 decorrelated samples from one seeded chain (declared "symmetric sector", |m| = 0.018). Plates L = 24 at T/Tc 0.75, 0.90, 1.20, 1.80 (m 0.99, 0.88, 0.18, 0.06). NOTES are candid that big spin clusters persist above Tc, so red is not by itself a critical signature; the critical claim rests on the weight ladder and the bond fraction.
Visibility: the three weight rungs are present, but at 3 m the field reads as even confetti plus one red line — the ladder is a 1 m read, and the 1-pass specks outnumber everything, so "structure at every scale" reads more as "noise plus a coastline".

## How it got here
Six versions plus a seed sweep (v5 s3/s7/s13), all on one layout. v4: plates at 0.70/0.90/1.00/1.15/1.60, chart to 1.75. v5 seeds 3/7/13: same composition, different configurations — s3 (m 0.165, 501 domains) had a sparser field with more red; s13 filled the window more evenly. v6: plates moved to 0.75/0.90/1.00/1.20/1.80 and the chart axis extended to 1.95; seed 7 retained. Gained: a stronger contrast between the near-empty cold plates and the busy hot ones. Nothing structural changed across the round. Juan's feedback: none recorded.

## Keep — what works
- The crimson interface: one long fractal coastline winding from the top edge to the right and bottom edges — the single long-range object, scarce and loud.
- Line weight = domain scale (1/2/3 passes): a real data-carrying weight ladder; the bold continents (u 0.47–0.55, v 0.24–0.32; u 0.75–0.90, v 0.38–0.47) give the field depth planes.
- The hero cropped flush at the top and right drawable edges — a window onto the torus, and the sheet's main asymmetry.
- The empty crimson-dashed `1.00` plate in the deck with blow-up rays to the hero — the best idea on the lower half: Tc is not in the row, it IS the sheet.
- Walls drawn exactly on the dual lattice as staircases — honest to the model, crisp to plot, no crowding (≥1.07 mm).

## Weak — what doesn't
- [concept] The lower half is the scientific figure: parameter deck of labelled plates + an axis chart (m vs T with markers) + six-line colophon. The chart alone fails § 6.
- [hierarchy] At 3 m the field is uniform-grey confetti: hundreds of 1-site square loops at equal spacing drown the mid rung; only the red line separates out.
- [grid] Two type systems: spaced hairline caps for the title vs. a plain condensed mono in the footer and deck labels; the chart sits on its own baseline, not the footer's.
- [space] The band v 0.50–0.58 and the area right of the deck (u 0.72–0.95, v 0.55–0.78) are leftover, crossed only by dotted rays.
- [craft] The halo cut behind the title leaves a ragged hole in the field's upper-left (u 0.30–0.66, v 0.08–0.20) that reads as a missing rectangle, not as the title owning the space.
- [depth] The field is flat line work; depth exists only as the thin deck cards. Not declared flat.
- [concept] The 0.75 and 0.90 plates are nearly blank and read as empty frames rather than "order" — the cold phase has no visual body (no fill for the majority domain).

## Next versions
1. **COASTLINE** (abstract) — Full-bleed the critical configuration at a larger L across the entire sheet, drop the deck, chart and footer (one line of colophon), and make the weight ladder the whole design: 1-site specks removed or rendered as single dots, mid domains 1 pass, continents 3 passes, the crimson interface 4 passes. Lattice-with-defects at every scale with nothing else on the sheet; hierarchy and concept both rise.
2. **COOLING STRIP** (mechanism) — One continuous lattice whose temperature ramps across the sheet (a real simulated gradient from 0.7 Tc at left to 1.8 Tc at right, or a quench): ordered sea on one side, confetti on the other, and at the Tc column the crimson interface runs vertically as the frontier. Replaces five plates and a chart with one field where the transition is a place you can point at.
3. **NO LENGTH SCALE** (lens) — Nested windows: the same configuration shown at three zooms (full, ¼, 1/16) as concentric/cascading squares cropped into one another, each rescaled so the pictures look statistically identical — scale invariance as a self-similar nest. Twist: the caption asks "which one is the close-up?"

**If only iterating:**
- Delete the order-parameter chart and cut the footer to two lines set in the title's spaced caps on the same left axis.
- Remove 1–2-site loops from the hero (or render them as dots) so the 2- and 3-pass domains read at 3 m.
- Fill the majority domain of the 0.75 plate with a sparse hatch so the cold side of the deck has mass, and pull the deck up to close the v 0.50–0.58 gap.
