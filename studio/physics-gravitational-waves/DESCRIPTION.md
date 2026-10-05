# GW150914 — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/physics/gravitational-waves` |
| current render | `gallery/physics/gravitational-waves/candidates/prior-approved/pp_gw150914_v1.png` |
| source | `promptplot/generative/pieces/physics.py::gw150914` · data `studio/astro-01/data/fig1-observed-H.txt`, `fig1-waveform-H.txt` · spec `studio/astro-01/encoding.md`, `studio/astro-01/dossier.md` |
| paper · pens | a4 landscape (297×210, 15 mm margins), cream · only 2 pen indices are used: 1 (preview "crimson"; the code's GOLD role) = NR template, rule, medallion spirals · 2 black = measured strain, horizons, all type. The code's CRIMSON role collapses onto the black pen at `colors=3` (`CRIMSON = 2 % 3 == BLACK`), so the "touching horizons" are drawn black. |
| status | unreviewed in the viewer (tier: prior-approved; listed as "earlier approved" in the 2026-09-13 checkpoint) · 1 render on disk |

## In one line
The first gravitational-wave chirp drawn as **one horizontal signal line swelling to a single peak (laminar, a time series)** — x is time (1.27 mm/ms), y is strain (27 mm per 10⁻²¹), black measurement over crimson/gold prediction, with a two-horizon medallion hung over the merger instant.

## What is on the sheet
- **Strain traces (dominant, full width u 0.05–0.95, baseline v 0.55).** A black line enters at the left margin in jittery noise (±5–11 mm), stays low through u 0.05–0.60, gathers into three growing swells at u 0.62–0.78 and peaks at (u 0.79, v 0.41) with the deepest trough at (u 0.78, v 0.68); two quick ringdown wiggles by u 0.84, then low noise to the right margin. A crimson smooth line (the template) runs under it: nearly flat through the left half, matching the black line cycle-for-cycle through the swell, overshooting it at the peak (crimson tip at v 0.40, trough at v 0.69).
- **Title block (u 0.05–0.47, v 0.15–0.26).** `G W 1 5 0 9 1 4` black stroke caps ~9 mm tall (double pass). Under it, ~2.5 mm spaced caps: `T H E   F I R S T   G R A V I T A T I O N A L - W A V E   C H I R P` (v 0.23) and `L I G O   H A N F O R D   3 5 - 3 5 0   H Z   0 . 2 1   S` (v 0.26).
- **Crimson rule (u 0.05–0.37, v 0.31).** A hairline pointing right across an empty span toward the medallion.
- **Medallion (centre u 0.79, v 0.31, Ø≈36 mm ≈ 0.12 W).** A crimson spiral of ~7 turns (r ≈ 18 → 8 mm), not centred on the pair; two black circles, r≈12 mm (centre u 0.75) and r≈9.5 mm (centre u 0.82), which **overlap** by a lens ~3 mm wide rather than touch; a short black diameter tick through each.
- **Anatomy labels (black, ~2.5 mm spaced caps, no leaders).** `I N S P I R A L` at (u 0.19–0.30, v 0.47). `M E R G E R` at (u 0.72–0.81, v 0.40) — its final `R` is touched by the crimson template's peak. `R I N G D O W N` at (u 0.82–0.95, v 0.47).
- **Footers (v 0.91, ~2 mm spaced caps).** Left: `G W O S C     P R L   1 1 6   0 6 1 1 0 2`. Right: `F U L L   H E I G H T      S T R A I N   1 E - 2 1`.
- **Quiet zones.** A full-width empty band v 0.70–0.88 under the trace, and an empty rectangle u 0.40–0.70, v 0.08–0.30 between title and medallion.
- **Absent (though coded/specified):** no zero-crossing colonnade of vertical hairlines is visible anywhere; no dotted plumb line from the medallion to the peak is legible.

## The science it encodes
Docstring (`pieces/physics.py::gw150914`) and `studio/astro-01/encoding.md`: the real bandpassed LIGO Hanford strain (GWOSC, PRL 116 061102) as the dominant black line, the numerical-relativity template underneath ("where they disagree, gold shows: the residual draws itself"), a zero-crossing colonnade whose spacing ramp IS the chirp clock (18.2 mm at 35 Hz → 2.5 mm at 250 Hz), and a medallion where the two horizons at true 106:86 km scale touch at the merger instant. Exact: both traces are real data at stated scales (x 1.271 mm/ms, y 27 mm per 10⁻²¹). The render shows the two traces faithfully, but NOT the colonnade, NOT touching horizons (they overlap), NOT the crimson "contact" colour (pen collision), and the medallion sits at v 0.31 (y≈145 mm) rather than the spec's y=160 title axis. An analytic chirp fallback exists in code (`_analytic_chirp`) but the render's noisy inspiral shows the real data file was used.

## How it got here
One render. It predates or diverges from the full encoding spec (colonnade, longer footers with the "1/400 of a proton" fact, `14 SEPTEMBER 2015` subtitle are in the spec but not on the sheet). No viewer feedback on file.

## Keep — what works
- The real trace as the only element touching both side margins, entering and leaving in noise — the frame slices an ongoing quiet; the swell at u 0.62–0.84 reads at 3 m.
- The template-under-measurement duet: crimson peeking out only where theory and data disagree (the inspiral noise, the peak overshoot) — an emergent residual with no extra mark.
- Medallion hung on the merger's x (u 0.79 over the peak at u 0.79) — alignment as simultaneity.
- The rule at v 0.31 pointing across empty paper to the medallion — shaped negative space.
- Big 9 mm title against 2.5 mm tracking caps — the only real type hierarchy in the physics set.

## Weak — what doesn't
- [concept] It is a time-series plot: one wiggly line on a baseline with INSPIRAL / MERGER / RINGDOWN labels — the LIGO press-release figure (§6 NO SCHEMATICS: an axis plot minus the axes). The colonnade, the one Deco device that would lift it out of the figure, is missing.
- [craft] Pen mapping bug: at `colors=3` CRIMSON == BLACK, so the "contact" colour never appears and the horizons are black; the "gold" template shows as crimson in preview.
- [concept] The horizons overlap (≈3 mm lens) instead of touching — the one true geometric claim of the medallion is visibly false; the spiral is off-centre relative to the pair.
- [space] Template peak runs into the `R` of `MERGER` (u 0.80, v 0.40) — label grazing geometry.
- [space] The band v 0.70–0.88 is empty leftover across the full width — not shaped, just unused (the spec's colonnade was meant to live there).
- [depth] Entirely flat and undeclared: no occlusion except trace-over-trace, no weight change between inspiral and merger.
- [hierarchy] The medallion (Ø 36 mm, thin lines) is too faint to be the clear second read at 1 m.

## Next versions
- **CHIRP COLONNADE** (abstract) — the plate becomes the colonnade: one vertical line per measured zero crossing, full sheet height, spacing ramping 18 mm → 2.5 mm left to right (the chirp clock, measured), and each line's ink length (or a break in it) set by the strain at that half-cycle — the waveform survives only as the edge where the colonnade's lines stop. Laminar order, Deco's signature ornament made of data, no plot left. Title set vertically on the silent right after ringdown.
- **FLEXING RULER** (lens) — the encoding's own one-glance line, taken literally: the plate is a ruler — a long run of millimetre ticks across the sheet whose spacing is stretched and squeezed by the strain (exaggerated 10¹⁹×), calm on the left, violently accordion-folded at the merger, then still. Everyone knows a ruler; the twist is that the ruler itself flexed. Footer: "each 4 km arm changed by 1/400 of a proton".
- **SPEC COMPLETE** (faithful) — implement encoding v1 exactly: fix the pen map (black / gold / crimson distinct), horizons tangent at true 106:86 radii with centres 17 mm apart, medallion centre on the title axis y=160, dotted gold plumb to the peak, colonnade in band y 34–78 under the trace, spec footers.

**If only iterating:**
1. Fix the pen collision so crimson (horizons) and black (data) are different pens, and make the two horizons tangent, not overlapping.
2. Draw the zero-crossing colonnade in the empty band v 0.70–0.88 with its 18 → 2.5 mm spacing ramp stopping at the end of ringdown.
3. Lift `MERGER` ≥ 3 mm clear of the template peak (or right-align it to x = 231 per spec).
