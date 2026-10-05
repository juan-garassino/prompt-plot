# ORBITAL RESONANCE (the organ rank) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/resonance_rank` |
| current render | `gallery/studio/resonance_rank/current/pp_resonance_rank_v5_a3.png` (no gcode beside it; the latest gcode is `trials/pp_resonance_rank_r02_a4_s7.gcode`) |
| source | `studio/orbital-resonance/rounds/r02/piece.py::resonance_rank` (the batch listed none: this is round r02 of the **orbital-resonance** family, not a sibling of the attention "resonance" plates) |
| paper · pens | A3 landscape, cream (earlier trials A4 landscape) · 0 black = pipes, rack and toe boards · 1 crimson = four ghost pipes + interval caption · 2 black (finer nib) = type |
| status | unreviewed (no FEEDBACK.md) · 10 renders on disk |

## In one line
Kirkwood gaps drawn as **a rank with missing members**: a row of flue pipes whose speaking lengths rise with orbital period, with four sockets standing empty exactly where the period is a small-integer ratio of Jupiter's — "a pipe is its orbit, length is period".

## What is on the sheet
Coordinates are (u, v) on the 420 × 297 sheet.

- **The rank (dominant mass).** About 68 black pipes stand side by side from u 0.04 to u 0.75. Each pipe is a double-walled cylinder with an elliptical lip at the top, a mouth cut-out at the rack board, and a conical foot tapering to a point on the toe board. Tops climb in a straight rising line from v ≈ 0.50 at the left to v ≈ 0.32 at the right, so the rank is a long wedge. The walls are dense polylines that preview as beaded black bars, and at 1 m the rank reads as a picket fence.
- **The gaps.** One pipe is missing at u ≈ 0.245 (label `3 : 1` above it at v ≈ 0.43, beside a thin crimson ghost pipe of the same height). At u ≈ 0.52 (`5 : 2`, v ≈ 0.36) and u ≈ 0.62 (`7 : 3`, v ≈ 0.33) the crimson ghost is reduced to a tiny crimson double-arrow at the lip height and a crimson foot below, with a black pipe standing hard beside it. Right of u 0.75 there are no pipes at all.
- **The empty half of the rack.** From u 0.75 to 0.96 the rack board carries only a row of empty elliptical socket holes, and the toe board carries a dotted row where feet would stand. One tall crimson ghost pipe rises at u ≈ 0.89 up to v ≈ 0.28, labelled `2 : 1` at v ≈ 0.25. It is the tallest mark on the sheet.
- **Libration marks.** Short black paired verticals ("H" marks) stand proud of the lips of several pipes near the 5:2, 7:3 and the right end of the rank (u 0.62–0.75, v 0.32–0.35).
- **Rack board and toe board.** Two long isometric slabs across the full drawable width: the rack board at v 0.75–0.81 (holes on top, pipe mouths on its front face), and the toe board at v 0.87–0.95. Both are drawn as planks with a 30° end return at the right.
- **Title block (top-left).** `ORBITAL` / `RESONANCE` large spaced monoline caps, u 0.04–0.40, v 0.05–0.17. Caption at v 0.20–0.26: `A PIPE IS ITS ORBIT. LENGTH IS PERIOD.` / `THE CONSONANCES WITH JUPITER ARE MISSING.` / crimson `3:1 TWELFTH   5:2 MAJOR TENTH` / crimson `7:3 SEPTIMAL TENTH   2:1 OCTAVE`.
- **Top-right.** `KIRKWOOD 1866` (u 0.77–0.95, v 0.06) and `MAIN BELT   96 SOCKETS   68 SPEAKING` (u 0.65–0.98, v 0.08). The second line runs into the right margin.
- **Footer**, set on the toe board's front face at v 0.93–0.95: `CIRCULAR RESTRICTED 3-BODY. MU 9.5388E-4. VERLET DT 0.02. 300 JUPITER YEARS.` / `DOTTED COLLAR IS THE LIBRATION OF THE SPEAKING LENGTH. MAGNIFIED 6 TIMES.`
- **Quiet zone.** The upper-right quadrant (u 0.42–0.95, v 0.10–0.30) is empty except the 2:1 label.

## The science it encodes
From the r02 docstring: the same integration as r01 of the family (planar CR3BP, μ = 9.5388e-4, velocity-Verlet, 300 Jupiter years), here with **96** test particles. A pipe's speaking length is the asteroid's orbital period. Its libration width decides whether the pipe stands, and the "dotted collar", magnified ×6, shows how far its length wanders. The four crimson ghost pipes are placed by Kepler III only (a = a_J (q/p)^(2/3)) and named as musical intervals with Jupiter's pipe (2:1 octave, 7:3 septimal tenth, 5:2 major tenth, 3:1 twelfth). The claim "length ∝ period is an identity, not a resemblance" is true of organ ranks. On the render, though, the libration collars are too small to read, and the 5:2 / 7:3 sockets do not visibly empty: a black pipe stands hard against each crimson ghost.

## How it got here
- **v1 (A4 landscape)**: shorter pipes; a dashed black diagonal ran over the pipe tops; crimson interval names (`TWELFTH`, `OCTAVE`...) floated in the rank and over pipe tops; the 2:1 ghost stood beside `2:1 OCTAVE`.
- **v3–v4**: interval names moved into the crimson caption, labels became `3 : 1` etc. above the gaps, and the diagonal was removed.
- **r02 s3/s7/s11, r02_a4_s7**: seed studies, same layout (A4: 24.4 m draw, 9.7 m travel, 1 045 pen cycles — much cheaper travel than the arc belt).
- **v5 (A3)**: current; scaled to A3 with taller pipes and a longer empty rack.
- No feedback from Juan.

## Keep — what works
- The empty right-hand quarter of the rack (u 0.75–0.96): a row of empty sockets with one crimson 2:1 ghost towering over it. This is the plate's best image of "swept".
- The rising lip line from v 0.50 to v 0.32 is a real, readable monotone (period grows with a) and gives the sheet its diagonal.
- The music/orbit identity (octave = 2:1) is the "twist" the rubric asks for, and the caption states it in two lines.
- The crimson is scarce: four ghosts and two caption lines.
- The travel budget: roughly 0.4× draw on A4, compared with 1.15× on the arc belt.

## Weak — what doesn't
- [concept] It is an illustration. A viewer names an object (an organ, a pipe rank), and DESIGN_RUBRIC § 6 says cut it. The isometric rack and toe boards are pure carrier furniture carrying no data.
- [concept] The 5:2 and 7:3 gaps do not read: a black pipe stands against each tiny crimson mark, so only 3:1 and the outer edge look empty. The collars ("magnified 6 times") are invisible at viewing distance.
- [hierarchy] Sixty-eight near-identical pipes give one mid-grey mass with no dominant form. The only standout is a hairline crimson pipe.
- [craft] Pipe walls are two lines ~0.8 mm apart plus a dense lip ellipse, so each pipe is a solid ink bar. The foot cones converge into black spikes at the toe board (u 0.04–0.75, v 0.85–0.89).
- [grid] `MAIN BELT 96 SOCKETS 68 SPEAKING` presses into the right margin. The title block and the top-right block share no baseline.
- [space] The rack board and toe board span the full width while the pipes stop at u 0.75. The planks read as leftover floor, not as shaped emptiness.
- [depth] The planks are isometric and the pipes are frontal, so it is two projections on one sheet (the axo shared-basis law).

## Next versions
1. **silent-ranks** (abstract) — drop the organ and keep the one idea that works: a single row of vertical strokes whose lengths are the periods, uniform in a, with vacancies at the resonances and the outer 2:1 zone as a long silence. Ink weight carries libration, and there are no boards or lips. That turns it into a LATTICE-WITH-DEFECTS barcode, legible at 3 m, and the rubric's figuration objection disappears.
2. **the octave** (lens) — keep the musical joke but make it the carrier: a stave/score in which each surviving asteroid is a sustained note at its period-pitch, and the four consonances with Jupiter are bars of rest. The twist lands harder than the organ drawing, and rests are the absence the physics predicts.
3. **rank-cleaned** (faithful) — keep the organ, but widen the voids so each consonance is at least 3 pipe pitches wide, draw the crimson ghost full-length in every gap, and delete the toe board and the empty rack board.

**If only iterating:**
1. At 5:2 and 7:3, remove the black pipe adjacent to each crimson ghost (or widen the socket by one pitch) so four clear gaps read at 1 m.
2. Delete the lower toe board slab and set the footer on a plain baseline at v 0.94. The pipe feet end on a single hairline.
3. Draw each pipe wall as a single stroke with an open lip circle, so the rank reads as lines rather than black bars.
