# Synth — millennium-yang-mills after r03 · 2026-09-29
route: designer
next round: r04 · parent: **r03** (best so far). This is round 4 of 5.

**Standing.** r03 is the new best: art 7.43/7 FAIL, science 10/9/8 PASS. The science critic has no mandates. The art critic puts every dimension at ≥ 7 and fails the plate on average alone. Its diagnosis is single and clear: **the plate is over-captioned.** The geometry now reads as Kandinsky on its own. The science fixes (S1, S2) arrived as volume:
- the statement grew from 1 line to 3, sitting 9 mm off the plane;
- the key grew from 4 lines to 7, climbing to y≈52 in the quiet zone the diagonal points into;
- TEXT grew from 21 to 44 min, the longest layer on the plate. Encoding §10 budgeted ≈ 15 min.

The translator watch is closed: concept legibility is 7, and the pull comes from the text, not the hyperbolae.

**Fabrication gate:** not run (art FAIL). A pre-gate flag is recorded as G1: the gcode draws at F1800/F2200, while NOTES quotes minutes "at F600". No `promptplot/` files changed during this piece.

## The instruction
Fork `rounds/r03/piece.py` to `rounds/r04/piece.py` and **change only the words and the `*` glyph. This is a subtraction round that gives the silence back.** Every curve, the point, the red, the strata, the cone, the crop, the gutter tags and the layer order stay byte-identical outside TEXT (and the star inside the `0⁺⁺*` tag).

Return the text to the series grammar's volume: a title, a statement of **at most two lines**, and two small corner blocks. The words keep all of S1/S2's content and lose the sentences.

The statement's lowest ink must sit ≥ 14 mm above the plane top, at y ≥ 384. It must still say three things:
- the classical waves run on the dashed line at light speed;
- the quantum theory puts no state there, with no massless gluon;
- the cone holds only its tip, then nothing up to Δ.

The bottom-right key becomes **at most 4 lines**, flush-right on 282, set wholly below the point (top ink y ≤ 40, disc bottom 45.4). Its last baseline sits on the colophon's last baseline. It is narrow enough never to meet the colophon's right end. It still names:
- the point, the vacuum;
- the curves *below the plane* as glueballs, each one's mass being its height above the point in Δ (S5: the rim is **not** "a glueball");
- red = the lightest, 0⁺⁺, mass Δ;
- the ruled plane = glueball pairs from its rim at exactly 2Δ;
- the data source;
- "2⁺⁺* LIES ON 2Δ WITHIN ERRORS" and "states above 2Δ omitted".

Move any of these into the colophon rather than cut it. Cap height stays at 1.8 mm or above. Fit by merging and rewording, never by shrinking type.

Then make the `*` a real star (S3). Finally, restate the plot budget honestly (G1).

## Mandates to close
1. **A10 — statement ≤ 2 lines, band opened.** S2's twist is intact in fewer words, with no "proven" and no MeV. Tests:
   - count the lines;
   - min y of statement ink ≥ 384 (plane top 370);
   - the title/statement/plane no longer read as one block on the phys preview.
2. **A9 + S5 — key ≤ 4 lines below the point.** Tests:
   - count the lines;
   - max y of text ink with x > 150 and y < 100 is ≤ 40;
   - the key's last baseline equals the colophon's last baseline;
   - key and colophon ink do not overlap in x on any shared baseline;
   - "GLUEBALL" and "PAIR" are still present;
   - the words that name glueballs exclude the rim, and the rim/plane is named as 2Δ.

   Total text lines on the sheet: ≤ 9. r03 had 13, r02 had 7.
3. **S3 — `*` unmistakable from `+`** in `0⁺⁺*` (gutter tag) and `2⁺⁺*` (key). Draw it as a 6-arm star: 3 strokes at 90° / 30° / 150°, no horizontal arm. It is ≥ 1.2× the `+` height, with ≥ 0.8 mm clear after the preceding `+`. The tag stays centred on its line end at 330.8 ± 0.3, and its gaps to the 1⁺⁻ (334.6) and 2⁺⁺ tags stay ≥ 0.5 mm. Tests:
   - a 25 % downsample of the phys preview reads "0++*", not "0+++";
   - decode the star strokes from the gcode and show that none is horizontal.
4. **G1 — minutes that match the file.** In NOTES/HANDOFF, give per-layer minutes in the stated order (GHOST → PLANE → TEXT → SPECTRUM → RED) twice:
   - at the gcode's own feeds (F1800/F2200 as rendered);
   - at Leo's plotting feed (F600 draw, slowed travel, with the pen-cycle dwell).

   Say which feed the job will run at. TEXT must come in at ≤ 30 min at F600 with cycles. Also state the A5 reflow's minutes. Do not edit the render pipeline to change feeds.

Deferred, tracked in the LEDGER:
- A7 (strata tangent to the rim near its vertex) is **argued and accepted**, because horizontal iso-energy strata against a horizontal-tangent rim is the physics.
- The colophon at x=15, off the spine grid, is noted and not mandated.

## Preserve
Everything from r03 except TEXT. The critics measured all of it as PASS, so none of it may move:
- **The point:** a Ø9.5 spiral disc in the 0.3 black at (40, 50). The red bar starts 0.05 mm clear of its ink, and the first grey dash starts on its edge.
- **1 : 1:** vacuum 50 → red vertex 150.000 → rim vertex 250, i.e. 100 : 100 mm. s = 100 mm/Δ on both axes, with the cone at 45.000°.
- **The empty lens:** 0 non-red segments in {p < E < √(p²+1)}. This is the plate's truth, and the curator's "the gap is the visible truth".
- **Exact data:**
  - AT2020 is read from `data/glueball_spectrum.json` and asserted;
  - shell vertices at y 193.73 / 204.95 / 221.95 / 228.12 / 235.61;
  - the rim fits M = 2.00000;
  - 2⁺⁺* is merged into the rim and declared.
- **The plane:** 120 strata at 1.000 mm, y 251 → 370, flat top at 370, vertical right edge at the crop, each ending on the rim at a 0.29 mm perpendicular inset. Boustrophedon, batched every 20.
- **One crop at x = 262** for every drawn element. J^PC tags are flush-left at x = 265, each centred on its own line end (2⁺⁺ 314.47, 0⁻⁺ 320.73, 0⁺⁺* 330.81, 1⁺⁻ 334.62, 2⁻⁺ 339.37, 2Δ 348.80). 0⁺⁺ stays untagged.
- **The red:** the bar plus the 0⁺⁺ shell as one red stroke, and the red Δ glyph in the left column (x≈27–37, y≈95–105). One red group, and red last. Red on the sheet: 0.59 m.
- **Cone dashes** 6.05 / 4.04 mm, fitted to end on the crop at (262, 272).
- **Layers:** 5 layers on 4 inks, 3 swaps, order GHOST grey 0.1 → PLANE black 0.2 → TEXT black 0.2 (same pen, own layer) → SPECTRUM black 0.3 → RED red 0.5. Byte-identical across seeds.
- **Type craft:** authored superscript signs (1.32 mm, 1.0 mm path gap), slashless zero, spaced-caps title flush-left on the spine.
- **Lineage:** Wassily Kandinsky, *Punkt und Linie zu Fläche* (Bauhausbuch 9, 1926). Point = vacuum, lines = mass shells, plane = continuum; flat by declaration. It stays on the sheet (colophon) and in NOTES/HANDOFF.
- **Deliverables:** the phys-width preview ships again, and the HANDOFF points reviewers at `_phys.png` first (sci advisory 2).

## Do not
- Do not touch any geometry to make room for words. The words make room for the geometry.
- Do not shrink caps below 1.8 mm or tighten the leading to fit the old sentences. That is the same volume, only smaller.
- Do not put any text, halo or key line into the plane, the lens, above the cone's apex in the void (y > 45 in the lower-right), or on the cone's extension below the apex.
- Do not drop "GLUEBALL", "PAIR", "no massless gluon", "within errors" or the lineage in the compression. Re-home them (colophon) instead.
- Do not tag the 0⁺⁺ at the crop, add leaders, or rotate tags.
- Do not add ornament to "fix" the chart read: no knots, orbits, field lines or second accent.
- Do not judge tone on the stock preview. Ship and cite the nib-width preview.
- Do not quote minutes at a feed the file does not carry (G1).
