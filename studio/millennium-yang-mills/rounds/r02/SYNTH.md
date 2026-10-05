# Synth — millennium-yang-mills after r01 ∥ r02 (parallel) · 2026-09-29
route: designer
next round: r03 · parent: **r02** (best so far). It borrows named craft from r01 and none of r01's layout.

**Ranking.** r02 (art 7.00/5 · sci 9/9/7) beats r01 (6.71/4 · 9/8/7). Both FAIL, and art min decides. r01's own art mandate #1 (move the axis to x ≤ 85, no mirror partner) asks for what r02's half-section already is. r01 stays on disk as the **faithful flavour** (centred I-beam, symmetric bowl); it is not a candidate.

Both science critics PASS truth (9) and fidelity (8/9). Every §11 acceptance check PASSES in both rounds. Both FAILs come from **legibility**:
- **art:** "the textbook spectral figure with the axes erased" (concept 4 and 5);
- **science:** a stranger is never told what the point, lines and plane are, or why an empty light cone is surprising (legibility 7).

r03 is a de-charting move plus words. It changes no physics.

Fabrication gate: not run (no double PASS).

## The instruction
Fork `rounds/r02/piece.py` to `rounds/r03/piece.py`. Keep the half-section, the scale and every exact curve. **Take the chart furniture off the spine, so that Kandinsky's point / line / plane is the first read.**

1. **The point becomes a full-stop.** Make the vacuum a solid Ø 9–10 mm disc (0.3 black, concentric rings/spiral at pitch ≥ 0.45 mm, centre still exactly at (40, 50)). The heavy red bar and the ghost cone both start at its edge.
2. **The spine becomes the root of point and line, not an axis.** Move the J^PC tags off it. Shells, rim, red 0⁺⁺, strata and the ghost cone all stop at one x = 262 (p = 2.22). The tags sit flush-left at x = 265, each centred on its own line's end. The 0⁺⁺ gets no tag there: the lens ceiling at the stop (y ≈ 305 over x 265–275) and the 2⁺⁺ tag (≈ 314) leave no room. The red Δ glyph, still in the left column mid-gap, and the caption name it.
3. **The sheet says what it shows.**
   - The statement carries the twist: classical waves on the dashed light line, nothing there in the quantum theory, no massless gluon, only massive glueballs.
   - The bottom-right corner caption names the point, lines, red and plane in words.
   - Both stay in the E < 0 band and the title band, so nothing enters the lens or the plane.
4. **Restate the plot budget.** In NOTES, give the budget per layer in the stated order, with minutes, including the text layer's new cycle count.
5. **Ship a physical-width preview** next to the stock png.

## Mandates to close
1. **A1** — the vacuum as a Ø 9–10 mm solid point. Tests:
   - at a 10 % downsample it is a distinct full-stop ≥ 4× the red bar's width, not the bar's foot;
   - 1 : 1 is still 100.0 : 100.0 mm centre-to-vertex.
2. **A2** — tags off the spine, one crop at x = 262 for every element, tags in the gutter [265, 282]. Tests:
   - zero glyph ink left of x = 40 between y 140–260;
   - no comb of line-ends at the frame;
   - no unstrata'd continuum inside the crop;
   - no tag ink inside {E < √(p²+1)} for any p.
3. **S1** — name the carriers in the corner caption. "GLUEBALL" and "PAIR" (or "TWO GLUEBALLS") appear. It says what the point, a line, the red line (0⁺⁺, mass Δ) and the ruled plane (from exactly 2Δ) are.
4. **S2** — the twist in the statement: "classical Yang–Mills waves run at light speed (the dashed line); the quantum theory puts no state there: no massless gluon, only massive glueballs". No "proven", no MeV.
5. **S3** — J^PC legible at 30 cm with a 0.2 nib:
   - superscripts ≥ 1.3 mm;
   - sign gap ≥ 0.8 mm;
   - `*` drawn as a 3-stroke star;
   - "⁻⁺" does not fuse into an arrow.

   The gutter's tightest vertical pitch is 0⁺⁺*/1⁺⁻ ≈ 3.8 mm. If the stack must relax, move tags vertically in order, ≥ 0.5 mm apart, and never add leaders.

Deferred, tracked in the LEDGER: A4 (concept ≥ 7, the translator trigger), A7 (rim/strata tangency near the vertex).

## Preserve
- **The half-section composition** (r02):
  - spine x = 40, never drawn;
  - vacuum (40, 50), 0⁺⁺ vertex (40, 150), rim vertex (40, 250), s = 100 mm/Δ on both axes;
  - the plane cut flat at y = 370 in the upper-left;
  - the one ghost 45° diagonal splitting the sheet;
  - the open lower-right spacelike void as the quiet zone.
- **The heavy red line** (r02): one 3-pass bar from the disc edge to the 0⁺⁺ vertex, turning into the 0⁺⁺ shell as one red stroke. One red group, and red last.
- **The empty lens** (both rounds): 0 non-red segments in {p < E < √(p²+1)}. This is the plate's truth, and the curator's "gap is the visible truth".
- **Exact data** (both rounds):
  - AT2020 read from `data/glueball_spectrum.json` at import and asserted;
  - vertices +43.73 / 54.95 / 71.95 / 78.12 / 85.61 mm above red;
  - 2⁺⁺* merged into the rim and declared;
  - strata horizontal at 1.000 mm pitch, ending 0.29 mm ⟂ off the rim.
- **Layer discipline** (r02):
  - 5 layers on 4 inks, 3 swaps, order GHOST → PLANE → TEXT (same 0.2, own layer) → SPECTRUM → RED;
  - boustrophedon strata batched every 20;
  - byte-identical across seeds;
  - A5 reflow keeps the 1.0 mm physical pitch.
- **Title and statement flush-left on the spine** in the band [380, 405]. The colophon sits on the 15 mm margin.
- **Lineage**: Kandinsky, *Punkt und Linie zu Fläche* (Bauhausbuch 9, 1926), point / line / plane. Restate it in NOTES and HANDOFF, with "flat by declaration".
- **From r01, take only these:**
  - the physical-width preview method (`phys_preview_*.png`);
  - the slashless zero;
  - the glyph re-origin fix for proportional punctuation.

## Do not
- Do not tag the 0⁺⁺ at the stop, perch a tag inside the lens's continuation, or rotate tags along curves. r01 v4/v5 detached the names that way.
- Do not leave the cone dashes at 9/3. Encoding §4 is **6.0 mm dash / 4.0 mm gap**, first dash at the disc edge (A3).
- Do not write "2⁺⁺* SITS ON 2Δ". Write "LIES ON 2Δ WITHIN ERRORS" (S4; it is 1.9935 ± 0.017).
- Do not answer the "chart" read with ornament: no knots, orbits, field lines or second accent (§9). The fix is removing the axis furniture and weighting the point, not adding objects.
- Do not add any drawn axis, tick, number or frame. Do not let text or a halo enter the plane or the lens.
- Do not judge tone on the stock preview. The 0.2 strata flood there, so ship the nib-width preview.
