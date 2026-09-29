# Art critique — ising r03 · canon: Bauhaus (lineage Kandinsky, *Point and Line to Plane*; twist Mandelbrot coastline) · 2026-09-28
render: gallery/studio/ising/current/pp_ising_COASTLINE_v8.png  (gcode gallery/studio/ising/current/pp_ising_COASTLINE_v8.gcode, A4 portrait, cream, 2 pens)

## Scores

| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 5 | Crimson is the only loud thing, but it is broken into ~8 separate fragments (top-left stubs, top-right loop, a mid-right tongue, the lower band, edge stubs at x=10 and x=200) and carries ~30 % of the ink — not scarce, not one mass. The 3-pass black domain at (80–110, 210–240 mm) competes with it. No second/third level reads at 1 m: every black domain is the same 5–15 mm size class scattered evenly. |
| 2 | grid & alignment | 5 | Field is a full-bleed rectangle hard-clipped at all four margins: walls are sliced along the frame (black runs lying ON the right margin at y≈100 and y≈125; crimson stubs cut at x=10, y=160–180 and y=235–245; black caps cut at the top edge at x≈40, 190). Title starts on the left margin but stops at x≈172 while the two caption lines run to x=200 — three lines, two right edges. |
| 3 | tension & asymmetry | 5 | A weak rising diagonal exists (crimson band from (15,90) up to (200,190)), but the top-right crimson loop and the edge stubs dilute it; overall the sheet is an even all-over texture, which is the opposite of Kandinsky's directed forces. |
| 4 | negative space | 4 | There is no quiet zone. Dust dots (the "points") are sprinkled at uniform density over every square cm, so the largest wall-free areas (60–130 × 150–210, 150–200 × 190–230) are still grey with specks. Title band is crowded: crimson and black stubs come down to y≈27–28, 3–4 mm above the 5 mm title cap line at y≈22. |
| 5 | craft for pen | 6 | 2 pens, 1 swap — good. But the 4 crimson passes are not coincident: at corners they splay into doubled parallel strokes ~0.4–0.6 mm apart (dense crop, e.g. (160–170, 85–95)), and where the coastline necks to one lattice site (~1.1 mm) the two crimson sides nearly merge into a solid bar. Black dashed divider chords are drawn straight across crimson walls — black-on-crimson ink crossings at ~20 points. 3-pass black walls show the same corner splay. |
| 6 | concept legibility | 6 | "Clusters of every size, scattered points below a cut-off" reads as scale-free domains once you know Ising; the coastline twist does NOT land without the caption: the 17 mm dotted walk reads as a connecting polygon, and the 1.1 mm / 4.3 mm rulers exist only as text. The caption explains rather than confirms. Close to a snapshot-with-annotations (a figure) rather than a transposed order. |
| 7 | depth & dimensionality | 7 | Flat declared; Bauhaus is flat by nature; the 1/2/3/4-pass weight ladder gives a real scale-depth read. Acceptable. |

**avg 5.43 · min 4 · VERDICT: FAIL**

## Reads at a glance
At 3 m: a map-like scatter of black and red jagged outlines on a speckled page with a line of type at the foot — "islands on a chart", not a composed plate.

## Acceptance checks
No `encoding.md` and no `BRIEF.md` for ising — no §11 checks exist; judged on rubric + HANDOFF only. No reference in play (AUTHORING §6 N/A).
Rubric LINEAGE / plottability checks from the HANDOFF:
- lineage stated (Kandinsky + Mandelbrot twist) — PASS
- would hold its own hung beside *Point and Line to Plane* — FAIL (Kandinsky's plates are sparse, directed, with one dominant force; this is all-over texture; "plane" is only a line-weight, never a mass)
- ≤ 4 pens, each with stated meaning — PASS (2)
- spacing ≥ 0.8 mm — PARTIAL (lattice pitch ~1.1 mm OK; 4-pass crimson splay at corners and one-site necks approaches flood)
- no floods — PARTIAL (see necks)
- bounds clean on A4 — PASS (inside the green frame)
- known failure mode "colour as category not weight" — FAIL (crimson is a category — "the big interface" — spread over the whole sheet, not scarce)
- known failure mode "all elements at similar scale" — FAIL (black domains one size class)

## Biggest weakness
No composition: the sheet is an evenly-dusted, edge-to-edge lattice snapshot with the red interface shattered into fragments, so nothing dominates, nothing is quiet, and the Mandelbrot twist is carried by the caption instead of the drawing.

## Mandates
1. **One continuous crimson coast, and only one.** Choose a crop/seed/window in which the macroscopic interface is a single unbroken crimson line that enters at one frame edge and exits another (e.g. left edge at y≈90 → right edge at y≈190, the existing rising diagonal); no other crimson on the sheet — the top-right loop, the x=10 stubs and the top-left fragment must be gone. Test: count connected crimson polylines = 1.
2. **Carve one quiet zone of bare paper ≥ 25 % of the drawable area.** Drop the dust dots (and the smallest black domains) out of one contiguous region on the side of the coast opposite the densest black clusters — e.g. above the crimson diagonal in the upper-left — so the page reads "dense phase / empty phase" across the red line. Test: a 60 × 80 mm rectangle containing zero marks exists; the title band (y < 32 mm) also carries zero geometry within 6 mm above the cap line.
3. **Draw the ruler joke, don't write it.** Put the three rulers on the coast itself as visible geometry: the 17 mm dotted walk in the black pen offset clear of the crimson (no black dash may touch a crimson stroke), plus the 4.3 mm walk as a second, finer walk on one stretch of the coast, with the three lengths set as short labels at the walks' ends on the title's left-margin axis; make the title's right edge land on x=200 like the caption lines. Test: zero black–crimson crossings; three visible walks of three step sizes; all three type lines share both margins.

## Follow-up on open mandates
No `studio/ising/LEDGER.md` or `FEEDBACK.md` exists, and r02 has no critique on file — there are no open A*/J* mandates to track. The parent's DESCRIPTION.md "If only iterating" notes and the COASTLINE plan are checked instead:

| id | status | evidence |
|---|---|---|
| DESC-it1 delete the chart, footer to two lines in the title's spaced caps on the same left axis | PARTIAL | Chart gone; footer is two lines on the left margin, but set in a condensed bold mono, not the title's spaced hairline caps — still two type systems |
| DESC-it2 1–2-site loops out / rendered as dots | FIXED | Specks are now single dust dashes; the 1-pass/2-pass domains separate from the dust at 1 m |
| DESC-it3 fill the 0.75 plate / close the v 0.50–0.58 gap | N/A | Deck removed under the COASTLINE direction |
| COASTLINE: full-bleed, drop deck/chart/footer, weight ladder is the whole design, crimson 4 passes | PARTIAL | Executed literally, but the full bleed killed the composition (see regressions); crimson at 4 passes splays at corners |

## Regressions vs compare-to (gallery/studio/ising/current/pp_ising_v6.png)
- **Keep #1 REGRESSED — the one coastline.** v6's crimson read as one long interface from the top edge across to the right/bottom; r03's crimson is ~8 disconnected fragments (top-left stubs, top-right loop, x=10 edge stubs, lower band, mid-right tongue). The "single long-range object, scarce and loud" is gone.
- **Keep #3 REGRESSED — the cropped window / main asymmetry.** v6's field was a window flush to the top and right edges with a left column of type and paper; r03 bleeds to all four margins, so the sheet's only asymmetry vanished and the field is now even all-over texture.
- **Negative space REGRESSED.** v6 had a real quiet zone (the left column under the title, x 10–62, y 150–240); r03 has none — dust dots cover every square centimetre.
- **Title scale REGRESSED.** v6's CRITICAL at ~10 mm caps dominated the upper-left; r03's HOW LONG IS THE COAST at ~5 mm is crowded into a 20 mm foot band 3–4 mm under the field.
- Keep #2 (weight ladder) — still true, and clearer now that specks are dots.
- Keep #4 (empty 1.00 plate) — lost by design (deck removed); nothing on the sheet replaces its "Tc IS the sheet" wit — the Mandelbrot twist that was meant to replace it lives only in the caption.
- Keep #5 (dual-lattice staircases, ≥1.07 mm) — still true for black; crimson 4-pass corner splay and one-site necks now threaten it.
- Improvements vs parent (credit): the scientific-figure lower half, chart and six-line colophon are gone; no halo hole.
