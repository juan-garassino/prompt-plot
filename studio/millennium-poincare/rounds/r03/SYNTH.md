# Synth — millennium-poincare after r03 · 2026-09-29
route: designer
next round: r04 · parent: r03 (best so far)
- r03 ties r02 on art min (7) and science min (7) and beats it on art avg (7.71 > 7.43).
- r03 is not worse than r02 by rule, but one element regressed: the 3.05 mm keyline moat (science fidelity 9/8/7 → 8/7/8). This work order reverses exactly that element and keeps everything else r03 won.

thesis: abstract (flatness stays declared)
round: 4 of 5. r05 is the last designer round; after it, `vote` with an honest note.

## The instruction
Let the heavy line stand out by weight, not by silence, and let every other line touch it. Fork `rounds/r03/piece.py`.

1. **Remove the keyline moat.** The 3.05 mm keep-out grid goes, and the keyline's clearance becomes the encoding's own merge floor: 0.8 mm edge to edge at true nib widths, about 1.2 mm centre to centre for 0.5 against 0.3. Each Δt line then lives right up to the instant of the cut:
   - t_s − 0.01 runs again along both lobes and continuously through the waist, as in r02;
   - A t_s + 0.01/0.02 and B t_s + 0.01 come back on the equators.
2. **Make every halo line land.** Every past line that the time-occlusion stack clips ends tucked at that same floor against the line that covers it, so each pole reads as cards sliding under one another, not as loose hairs.
3. **Clear the waist.** The waist is left with three things: the heavy 0.5 outline, the red circle and continuous parallel halo lines. There are no orphan stubs and no hooked ring tips.

The keyline keeps its own black 0.5 layer and single pass, and its 8.7 mm per-flank pause where the red caps take the neck. The 0.5 weight against 0.3 carries the "one heavy instant" read at 1 m.

Finish with two items:
- extinction dots at Ø 2.6–3.0 mm;
- pen order 0 → 2 → 1 → 3.

Nothing in the flow data, scale, diagonal or type columns moves. `dossier.md` (v1.1) and the Errata block at the top of `encoding.md` are now the corrected source. Read them first.

## Mandates to close
1. **S4.** Δt grid integrity at the keyline (supersedes A1(a)). The keyline clearance is the 0.8 mm edge floor only. No blanking beyond it and no re-spacing. Gcode tests:
   - equator-ray counts **A 33 · B 6**, on rays through each extinction point ⟂ to the axis;
   - first gap inside the keyline 1.34 ± 0.3 mm (A) and 2.09 ± 0.3 mm (B);
   - **t_s − 0.01 ≥ 65 % drawn**;
   - no layer-0 ink closer to the keyline than the 0.8 mm edge floor.
2. **A8.** Every past line lands. At A's west pole (x 25–45, y 115–150), B's crown (x 170–200, y 278–298) and B's NE flank (x 225–245, y 225–275), each clipped halo end is tucked at a uniform clearance against its covering line (the next-later halo line or the keyline). Test: every open pen-0 halo endpoint lies within **1.0 mm edge to edge** of another drawn black line, keyline included. Today there are floats of 6.0 / 7.2 mm at (30.7, 124.3) and (235.0, 269.4).
3. **A9.** Waist = keyline + red circle + continuous halo bundles. The t_s − 0.01 stubs at (152.1, 199.7) and (177.9, 200.3) come back as continuous lines (via S4), and they are not deleted. No first-ring tip hooks toward the circle as an orphan. Test: no pen-0 stroke < 30 mm has any point within 15 mm of the cut centre (165, 200).
4. **A5.** Extinction points Ø 2.6–3.0 mm solid (spiral fill, red 0.5). Keep ≥ 5 mm bare where the rings allow. Where they do not (B is expected ≈ 4.7 mm), HANDOFF states the achieved dot-to-ring bare gap for both lobes.
5. **A10.** Pen order **0 → 2 → 1 → 3**: lines 0.3, type 0.3 (same physical pen, adjacent), keyline 0.5, red 0.5. That is 2 swaps. HANDOFF re-quotes per-layer minutes from `.venv/bin/python -m promptplot plot plate <gcode> --layers 0,2,1,3 --batch-strokes 40 --paper a3:portrait --margin 15 --dry-run`.

Deferred:
- **A11** (trim the footer toward 5–7 data lines). Take it only if every S1 clause survives.
- **S5** (dossier corrections). Folded by the lead into dossier v1.1 and the encoding Errata; science confirms in pass 2.

## Preserve
Everything r03 closed, confirmed by both critics:
- **Keyline (A1 b, c).** Its own black 0.5 layer, single pass, 2 strokes. The caption clause "OUTSIDE THE HEAVY LINE: BEFORE THE CUT · INSIDE: AFTER" stays in the footer.
- **Red cut (A3).** Caps at centre-line radius exactly h = 7.422 mm about (165, 200). The keyline pauses symmetrically, 8.7 mm per flank. Red → any black ≥ 0.8 mm edge to edge. The cut interior stays bare.
- **No rim stutter (A2).** Zero layer-0 strokes < 15 mm (r03 shortest 20.7 mm). Keep the ARC clause (a paused ring never re-enters a crowded arc) and the capped TWIN clause (≤ 30 mm; t_s − 0.05 merges into t = 0). Whole rings are never swallowed. **The restored lines must obey ARC too.**
- **Footer (S1).** "NECK −62 % · SMALL LOBE −30 % · LARGE LOBE −12 % · CUT AND CAPPED AT t = 0.055" and "OUTERMOST LINE: t = 0 (OFF THE GRID)", computed at render time from `snapshots.npz`.
- **Series caption (A4).** "MILLENNIUM PRIZE PROBLEMS 6 / 7" / "CLAY MATHEMATICS INSTITUTE, 2000", 2.2 mm caps, on x 205–282, registered on the statement's baselines.
- **From r02 (the regressed element, to restore).** The equator truth of all 33 A + 6 B rings, and a continuous halo fan through the waist, with steps 3.49 · 2.53 · 2.07 · 1.76 mm accelerating inward.
- **Data and geometry.** `snapshots.npz`, byte-identical, not re-solved: t_s = 0.054647, Δt 0.01 anchored at t_s, neck pinned pre-surgery, ψ²ds centroids held post-surgery. 62 mm/u, axis at 62°, cut (165, 200). Upper-left quiet zone bare. Floor ≥ 0.8 mm (r03 min 0.847).
- **Type.** Title, statement and red SOLVED stamp flush at x = 15. Corner caption and footer column flush at x = 205.
- **Lineage.** Vera Molnár, *(Dés)Ordres* (1974), named in HANDOFF. Canon 6 on cream; red only for the caps, the 2 points and SOLVED.

## Do not
- Do not keep any keep-out band around the keyline wider than the 0.8 mm edge floor. The r03 moat read as elapsed time and cost 33 → 31 and 6 → 5 on the equators (lie 6).
- Do not make the keyline heavier than 0.5 to compensate. At A's equator the true first gap is 1.34 mm, and a wider nib breaks the floor. Weight plus the floor is the whole distinction.
- Do not delete the waist stubs to "clean" the waist. The fix is to draw t_s − 0.01 continuously (S4), not to lose a Δt line.
- Do not buy landing (A8) by extending lines past where the occlusion stack clips them, or by respacing. An end moves only to where its own isochrone meets the covering line's floor.
- Do not reintroduce dash stutter while restoring lines (A2 must hold).
- Do not shrink or offset the red caps, add a second accent, draw the r01 shell or CSF loop, or quote minutes from `audit.py` alone.

## Gate
Not run: no double PASS yet (r01, r02 and r03 are all FAIL/FAIL). It runs on the first double PASS. Curator plotting items in scope:
- layers 0 → 2 → 1 → 3;
- ≥ 0.8 mm spacing;
- batchable strokes;
- minutes per layer;
- A3 paper. Leo's A5 landscape is still an open question for Juan (LEDGER).
