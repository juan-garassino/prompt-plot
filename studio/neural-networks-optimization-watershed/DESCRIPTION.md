# WATERSHED — EVERY START FINDS THE VALLEY — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/neural-networks/optimization/watershed` |
| current render | `gallery/neural-networks/optimization/watershed/promoted/pp_wave_gradient_seed3.png` (A · the file in `promoted/` — **a `wave_gradient` render, not WATERSHED**, see below) · `gallery/neural-networks/optimization/watershed/candidates/prior-approved/pp_ws_s19_v4.png` (B · the latest WATERSHED render; gcode `pp_ws_s19_v4.gcode`) · plottable WATERSHED gcodes without png in `variants/` (`pp_watershed*`, `pp_ws_s19_*`, `pp_ws_s42_sink`) |
| source | A: `promptplot/generative/generators.py::wave_gradient` · B: `promptplot/generative/pieces/ml.py::bauhaus_gradient` (retired predecessor `bauhaus_gradient_v1` in the same file) |
| paper · pens | A: a4 portrait, one pen (goldenrod in preview), no type · B: 240 × 170 mm landscape (the 17×24 cm sheet), cream · 0 cyan = deep global sink + streamline tails into it · 1 magenta = shallow local sink + tails into it · 2 black = plateau streamlines, plus mark · 3 dimgray = type · 4 royalblue = the momentum channel |
| status | A sits in `promoted/` with no verdict (almost certainly misfiled here by name — `wave_gradient` has no relation to the watershed piece). B: no FEEDBACK.md; the project CLAUDE.md lists `bauhaus_gradient` WATERSHED as **APPROVED** · 6 png renders on disk (+ 14 gcode variants) |

## In one line
B (the actual piece) draws gradient descent as **flow to attractors** — the whole plane rains downhill along exact RK4 streamlines into a deep cyan well and a shallow magenta trap, each line inking its last stretch in its destination's hue, the separatrix left as unpainted paper and one royal-blue heavy-ball channel overshooting the deep well and ringing back; A is an unrelated **laminar** seismograph (60 wave rows whose amplitude grows top → bottom).

## What is on the sheet

### A · `pp_wave_gradient_seed3.png` (promoted, misfiled)
1. **Sixty horizontal wave rows** filling the whole drawable area, u 0.07–0.93, v 0.06–0.94, rows ≈ 4.4 mm apart. Top rows (v 0.06–0.30) are nearly flat, sub-millimetre ripples; amplitude grows accelerating downward (frac^2.3), so from v ≈ 0.60 the rows become tall cusped, upward-pointing spikes (up to ≈ 16 mm) and from v ≈ 0.70 down adjacent rows **interpenetrate** — spikes of each row cross two or three rows above it, forming a dense tangled band v 0.75–0.94. Frequency also increases downward.
2. One pen only, no title, no type, no accent. Travel 11.0 m for 19.0 m of ink; 60 pen cycles.
3. Quiet zone: the top third is quiet by virtue of flat rows, but still ruled edge to edge.

### B · `pp_ws_s19_v4.png` (latest WATERSHED)
Coordinates normalised to the 240 × 170 mm landscape sheet (u → right, v → down); drawable area u 0.04–0.96, v 0.06–0.94.
1. **The deep well (dominant mass, cyan)** — a nest of 5 concentric cyan rings, outer r ≈ 14 mm (0.06 W), centred at u 0.38, v 0.61, with a small cyan spiral at the centre and a dotted cyan circle r ≈ 19 mm around it (the capture radius). Rings are continuous, ≈ 3 mm apart.
2. **The shallow trap (magenta)** — two magenta rings (r ≈ 3 and 7 mm) at u 0.68, v 0.41, inside a dotted magenta circle r ≈ 10 mm. About ⅓ the visual weight of the deep well.
3. **Streamlines (black)** — ≈ 120 short curved segments (10–35 mm each, ≈ 2.4 mm separation), covering u 0.07–0.93, v 0.20–0.86. They fan radially into the deep well from the left, bottom and top (a sunburst of lines stopping ≈ 8 mm short of the dotted circle) and curve in long arcs from the right half toward the magenta trap. Each line's last stretch before its sink is a short dash in the sink's colour — cyan dashes ringing the deep well, magenta dashes scattered around and below the trap (u 0.60–0.80, v 0.30–0.75).
4. **The separatrix** — no line is drawn there; it shows only as the place where neighbouring streamlines diverge: a loose curving gap from the top edge near u 0.50, v 0.20 down through u 0.52, v 0.45 toward the lower right. Weakly legible — the streamline gaps elsewhere are nearly as wide.
5. **The momentum channel (royal blue)** — one line entering from the lower right (u 0.85, v 0.87), sweeping up-left in a long arc through u 0.58 v 0.60 and u 0.44 v 0.48, **overshooting** the deep well across its top (u 0.25–0.45, v 0.46–0.49), swinging round its left side (u 0.26, v 0.52–0.58) and back under it (u 0.33–0.40, v 0.66–0.68), then ringing inward as a broken spiral inside the cyan rings. The only long continuous line on the sheet and the working diagonal of the composition.
6. **Plus mark** — a small black `+` at u 0.53, v 0.51, on the channel near the saddle.
7. **Type (dimgray)** — `W A T E R` / `S H E D` (≈ 5 mm caps, two lines, u 0.06–0.18, v 0.09–0.13) with a short underline under `S`; `E V E R Y   S T A R T   F I N D S   T H E   V A L L E Y` (≈ 2.5 mm, u 0.06–0.49, v 0.18). Footer bottom-right: `D T H       - G R A D   L   .   D T` (u 0.63–0.95, v 0.93) — the formula (dθ = −∇L·dt) with its `=` and θ lost.
8. **Swatch** — a tiny stacked cyan/magenta/black tick column at the top-right corner (u 0.92, v 0.09–0.12), half under the preview legend.
9. **Quiet zones** — the band v 0.20–0.30 over the left half (under the subtitle), the paper inside each dotted capture circle, and the bottom-left corner u 0.04–0.15, v 0.86–0.94. Plot stats: draw 3.2 m, **travel 5.8 m**, 4 435 commands.

## The science it encodes
`bauhaus_gradient` docstring (`promptplot/generative/pieces/ml.py`): "gradient descent as a BASIN OF ATTRACTION. The whole parameter plane rains downhill (exact RK4 on an analytic 2-Gaussian loss) into two sinks; the separatrix is left as a knife of blank paper. Each streamline is black on the plateau and inks its last stretch in its destination's hue (blue = deep global well, pink = shallow local trap). One blue heavy-ball-momentum channel visibly OVERSHOOTS the deep sink and rings back — the optimizer, not decorative flow." Parameters: 220 seeds, `min_sep` 2.4 mm, RK4 dt 0.9, depths 1.0 / 0.55, momentum 0.9; project CLAUDE.md adds `fill_spacing` (sink-disc spiral pitch, set > pen tip, e.g. 3 mm for a 2 mm POSCA) and `sink_scale`.
- **Computed exactly:** every streamline (RK4 on the analytic loss), the destination colour of each line (which basin it actually ends in), the momentum trajectory (heavy-ball ODE with β = 0.9), the capture circles.
- **Seeded:** only the streamline start points (seeds 1, 7, 19 render almost identically).
- **Not visible:** the "knife of blank paper" separatrix is too weak on v4 to read as a knife; the loss surface's depth is carried only by ring count at the sinks.
- A (`wave_gradient` docstring, `generators.py`): "Rows of horizontal wavy lines whose amplitude grows top→bottom… seismograph-like" — a seeded generative texture; it encodes no optimisation.

## How it got here
- **v1 (`bauhaus_gradient_WATERSHED_v1_seed1/7/19`, prior-approved, a4 portrait, 3 pens)** — the same field with the deep well as a **solid filled blue disc** (r ≈ 7 mm, black ring around it) at u 0.39 v 0.61 and a solid pink disc at u 0.66 v 0.38; streamlines long and continuous, many (~150), extending to the sheet edges; momentum channel in bold blue from the lower-right corner looping around the well; type `WATER / SHED / EVERY START FINDS THE VALLEY` top-left and the same footer. Strong, dark, legible attractor; the filled discs risked flooding with a POSCA.
- **v2/v3 (`variants/pp_ws_s19_v2/v3`, `_slow`, `_sink`, `pp_watershed_17x24*`, `pp_watershed_leo`)** — gcode only, not viewed here; the names indicate the move to the 17×24 cm sheet, Leo-ready slow feeds and sink-fill tuning (`fill_spacing` / `sink_scale`).
- **v4 (`pp_ws_s19_v4`, B)** — landscape 17×24, five pens: the discs open into ring nests with a centre spiral (plottable with a 2 mm POSCA), dotted capture circles, separate royal-blue pen for the momentum channel, type in dimgray. Gained: pen-safe sinks, a clearer momentum loop inside the well. Lost: the solid black-and-blue mass that made the deep well dominate at 3 m, and stream continuity (lines are now short segments; travel > draw).
- **A (`pp_wave_gradient_seed3`)** — appears in `promoted/` of this subject with no verdict; it is the `wave_gradient` generator (listed separately in CLAUDE.md "Generative art") and does not belong to the WATERSHED lineage.
- No FEEDBACK.md from Juan for this subject.

## Keep — what works
### B · WATERSHED
- **The royal-blue momentum channel**: one long continuous diagonal from the lower-right corner that overshoots the well and rings back inside it — it is the mechanism (heavy-ball overshoot) and the composition's working diagonal at once. Never cut it.
- **Colour = destination, exactly**: every streamline's tail dash is the colour of the basin it really ends in — the separatrix is readable by colour even where the gap is weak.
- **Two unequal sinks, off-centre** (deep at u 0.38 v 0.61, shallow at u 0.68 v 0.41) on a rising diagonal — asymmetric balance with a clear 3:1 weight ratio.
- **Ring-nest sinks with a centre spiral** at ≥ 3 mm pitch — plottable with a POSCA, reads as depth.
- The subtitle `EVERY START FINDS THE VALLEY` — the proverb-like line the rubric's "twist" asks for; it already half-lands.
### A · wave_gradient
- The accelerating amplitude (calm → seismic) is a clean one-parameter density gradient; the flat top third is a genuine quiet zone.

## Weak — what doesn't
### B · WATERSHED
- [concept] The separatrix — the piece's promised "knife of blank paper" — does not read: the gap between basins (u 0.50–0.55) is barely wider than ordinary streamline spacing. Without it, the plate is a generic vector-field plot with two sinks (rubric § 6, the scientific figure).
- [craft] Streamlines are chopped into short separate segments (10–35 mm) — **travel 5.8 m vs 3.2 m draw**; the "rain downhill" continuity of v1 is gone and the field reads as hatching.
- [hierarchy] The deep well is no longer the darkest mass: 5 thin cyan rings (a light pen) lose to the black streamline field at 3 m. v1's filled disc read first; v4's rings read third.
- [craft] Magenta tail-dashes are scattered as isolated specks across u 0.60–0.80, v 0.30–0.75 — they read as noise, not as a basin boundary. Footer formula loses `=` and θ (`D T H   - G R A D   L . D T`).
- [grid] Title top-left, swatch top-right, footer bottom-right, plus mark mid-field — the furniture checklist; the title block's left edge (u 0.06) aligns with nothing in the field.
- [depth] Declared-flat? No: the loss is a surface but only ring count hints at depth; no tone gradient toward the wells.
- [space] The streamline field is evenly dense everywhere except the capture circles — no shaped void besides the (failed) separatrix.
### A · wave_gradient
- [concept] Carries no optimisation idea at all, and it is filed as this subject's promoted plate.
- [craft] Rows below v ≈ 0.70 interpenetrate: spikes cross 2–3 rows above, so the bottom quarter is a tangle of ink-on-ink crossings.
- [hierarchy] [grid] [tension] No focal point, no type, edge-to-edge uniform ruling — a texture swatch, not a composition.

## Next versions
1. **the-knife** (faithful) — B with the separatrix made the hero: compute the basin boundary exactly (backward-integrate from the saddle's stable manifold) and clear a constant-width blank band (≈ 6 mm) along it by stopping every streamline at the band; restore long continuous streamlines (one polyline each, seeded along the sheet edge, `min_sep` kept) so travel drops below draw; darken the deep well back to a solid mass (dense ring nest at 3 mm pitch + a black keyline) so it dominates at 3 m. Everything else (momentum channel, colour-by-destination) unchanged.
2. **rain-tone** (mechanism) — Replace the 120 black arrows with a tone field of short dashes whose duty rises with |∇L| (steep slopes ink darker), coloured by destination basin over the whole plane (cyan half, magenta half, black only on the plateau); the separatrix appears as the colour edge plus a blank seam. The two basins become two coloured territories — a partition, the De Stijl reading of the same maths — and the momentum channel is the single long line across the border.
3. **one-drop** (lens) — The proverb as the composition: a single enormous deep well cropping the bottom-left frame, the shallow trap tiny near the top-right, and only ~15 streamlines, each launched from the top edge a few mm apart, visibly splitting at the separatrix — most fall into the well, a few are captured by the trap, and the momentum line is the one that escapes the trap. `EVERY START FINDS THE VALLEY` set large along the separatrix, with the trapped lines as the punchline that contradicts it.
(Separately: move `pp_wave_gradient_seed3.png` out of this subject — it belongs with the `wave_gradient` generator, not with WATERSHED.)

**If only iterating:** (on B)
1. Clear a constant-width blank seam (≥ 5 mm) along the true separatrix so the boundary between the cyan and magenta basins reads as a knife of paper at arm's length.
2. Draw each streamline as one continuous polyline from its seed to its capture circle (no segmenting), with the destination-colour tail as its last 15 % — target travel < draw.
3. Make the deep well the darkest mass on the sheet (tighter 3 mm ring nest + a black keyline or a heavier cyan pass) and fix the footer to render `=` and θ.
