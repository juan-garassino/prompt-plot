# Ledger — millennium-navier-stokes
**Best so far:** r01 — art 6.71/6 · sci 9/9/8 (PASS) — `gallery/studio/millennium_navier_stokes/current/pp_millennium_navier_stokes_faithful_v6.png` (gcode `_v6.gcode`). Art FAILs it.
- r03 ties it on verdict (art FAIL, sci PASS 9/9/8) but loses on art min (5 against 6), so r01 stays rank 1 by the ledger rule.
- r03 is the **science-clean code state**. Every S* mandate is closed on it, and it is the code parent for whatever comes after the translator.

**Route:** translator (after r03). Next designer round is **r04**, and it runs on the amended encoding.

**Round cap:** 5 designer rounds per encoding (DESIGN_RUBRIC). Encoding v1 has used 3 (r01 and r02 in parallel, then r03). If the translator issues **v2**, the cap resets per the rubric. The lead still intends to take v2 to at most **two** rounds (r04, r05) and then go to `vote` with an honest note.

Context: this is plate 3 of the MILLENNIUM series. There is no FEEDBACK.md, DESCRIPTION.md or BRIEF.md for this slug, so there are no J* mandates. The binding brief is `encoding.md` v1 plus the curator note:
- series grammar: cream sheet, spaced-caps title top-left, a one-line statement, small corner captions, one loud accent;
- the reference is interpreted, never traced;
- streamlines come from a real velocity field;
- the cascade is real structure;
- the plate is honest that the open question is 3D;
- one clean layer per pen, in a stated order, with streamlines ≥ 0.8 mm and batchable, and minutes per layer stated;
- the lineage is named (Riley).

**Translator watch → fired after r03.** The "separate badges / specimen board" diagnosis has now been given three times. r01 called it "a specimen board, 7 round exhibits". r02 called it "a string of blue badges". r03 called it "rungs 1–4 are still round cut-outs on a ruler line… badges on a string", and the critic flagged it for the lead's weight.
- It was the headline of r02's SYNTH, and r03 did not fix it. That is NOT FIXED in two consecutive rounds (r02 → r03), so route rule 2 applies. It is now mandate A7.
- The art critic scored tension 7, so the watch's letter (≤ 6) is not met. The lead routes anyway, for two reasons. The r02 SYNTH promised the translator "if the new crop does not dissolve it; say so in NOTES", and the r03 designer said so explicitly: "inside those constraints I could not make them one surface."
- The r03 designer also showed that the failure is an encoding constraint, not an effort problem. Encoding §4 has discrete circular rungs with self-similar rim gaps, and A2 required ≥ 8 mm hero → rung-1 clearance.

## Rounds
| round | parent | thesis | render | art avg/min | sci t/f/l | verdict | note |
|---|---|---|---|---|---|---|---|
| r01 | — | faithful: Burgers hero plus a λ=2 ladder on a curled similarity orbit (Δφ −20°), a 22-ring Lamb–Oseen disc, and a Monge side view r²\|z\|=C in a circular window. Lineage Riley, *Blaze 1* (1962) | `gallery/studio/millennium_navier_stokes/current/pp_millennium_navier_stokes_faithful_v6.png` | 6.71/6 | 9/9/8 | art FAIL · sci PASS · **rank 1 (best so far)** | Every family is exact to µm. Art: a specimen board of 7 round exhibits, grey hairline rings, "4/3 T0" reads as "TO", 8 caption blocks. ≈ 2 h plot. Keep on disk as the **faithful flavour** (the side view is its signature) |
| r02 | — | abstract: the same families. Straight diagonal orbit (factor 1.20, δ₀ 20), no side view, type on the 15 / 282 axes, and the hero cropped 33 mm on the left | `gallery/studio/millennium_navier_stokes/trials/pp_millennium_navier_stokes_abstract_v15.png` (+ `_v16_a4`) | 7.14/6 | 7/7/7 | FAIL · rank 3 | Science FAIL on words (a headline asserting the open answer) and density (reversal at rungs 3–4). Art: badges, pale hero. **But its hero is the best hero so far.** The eye is on paper at (62, 272) with 2+ turns visible, and the disc sits off-axis at x 228 with its caption beside it. r03 regressed both |
| r03 | r02 (merge with r01 wording) | iterate: hero at R_out = 5δ with its eye 12 mm off the left frame; the hero on its own 0.5 mm blue nib; the disc moved to (178, 298) on the hero's row; one terminus block on x = 282; conditional statement; blow-up defined; the cull minimum scaled per rung; δ₀ 18 | `gallery/studio/millennium_navier_stokes/current/pp_millennium_navier_stokes_iterate_v8.png` (tone: `_v8_phys.png`) | 6.00/5 | 9/9/8 | art FAIL · sci **PASS** · rank 2 | **All S* closed** (S1, S2, S3 by the declared branch), and A1 and A3 fixed. Density 0.370/0.739/0.825/0.790/0.773, floor 0.824 mm, red 0.93 %, ring at L to 0.001 mm. **Art regressions against r02:** (1) the crop took the hero's eye, so it reads as a radial fan and rung 1 becomes the protagonist (hierarchy 5); (2) the disc drifted to the centre and its caption sits 57 mm away; (3) type is 57 of 104 min. Unchanged: the red ring (r 12.9) is larger than rungs 3–4, so the ladder "ends at a bigger circle". The badges diagnosis is repeated, so the route is translator. 17.5 m draw, 14.9 m travel, ≈ 104 min, 3 swaps |

**Ranking.** r01 > r03 > r02 by the rule (verdict, then art min, then sci min, then art avg).
- **Code parent after the translator: r03.** It is science PASS with every word and density fix in it.
- **Restore r02's hero geometry and disc placement** into it (see the Preserve list in `rounds/r03/SYNTH.md`).

Flavours to keep on disk:
- r01 as the *faithful* flavour (the Monge side view);
- r02/r03 as the *abstract* line. Only the best of that line is carried forward.

## Mandates
| id | raised | by | mandate | status | closed |
|---|---|---|---|---|---|
| A7 | r01, r02, r03 | art (+ both designers) | **The ladder is one surface, not badges.** Rungs must not read as free-standing round discs on a line with self-similar white gaps. Merges r01's "specimen board", r02's "string of badges" and r03's "badges on a string". This is an **encoding-level** mandate: the translator must amend §4/§5 (the rung boundary and the rim-gap rule) | open, NOT FIXED ×2 (r02, r03), so route translator | |
| A8 | r03 | art (+ science advisory 1) | **The hero's eye is on paper.** C₀ is inside the drawable area (art: 25–35 mm inside x = 15; science: x ≥ 18 is enough for the eye, and ≥ 1 core wrap), cropped only by far-field arms. The hero is the largest complete spiral, and pen-0 draw length > rung 1's (r03: 3.86 against 4.69 m). This is a **regression from r02**, where the eye was at (62, 272) with 2+ turns visible. Supersedes the part of A2 that put the eye off the frame | open (regression) | |
| A9 | r02 (noted), r03 | art | **The terminus continues the diminishing series.** Going down the diagonal, every closed form is smaller than the one before, the red mark included. r03's ring is r 12.94 against rung 3's R 11.25 and rung 4's 5.63, so at 3 m it reads as a target or bubble. The encoding §4 rule r = \|C₅ − L\| + R₅ produces this, so it goes to the translator with A7 | open → translator | |
| A10 | r03 | art | **Captions anchored and the disc back off-axis.** Disc centre ≥ 65 mm right of the sheet centreline (x ≥ 213.5), right rim ≤ 10 mm from x = 282 (r02 placement). Its caption within 12 mm of its rim, flush on 282. Ladder caption within 15 mm of the rung it names. No caption > 15 mm from its element. Type < 35 % of plot minutes (r03: 57/104): one 2-pass title, single-pass captions, ladder caption ≤ 3 lines | open | |
| A2 | r02 | art | Grow the hero to R_out = 5δ, crop hard on x = 15 (≥ 170 mm of height), ≤ ½ rim visible, far arms ≥ 8 mm from rung 1, the orbit carried, the hero not the palest | open (partial) | Letter met in r03: chord 178 mm, rim 45.7 %, 27 mm to rung 1, hero on a 0.5 nib. The spirit failed, because the crop went through the core. The eye clause is now A8. The ≥ 8 mm hero → rung-1 gap is **suspended pending the translator** (A7 may make rungs share boundaries) |
| S1 | r02 | science | Headline truth: the statement is conditional | **fixed** | r03 science pass 2: "WHETHER IT CAN SHRINK TO A POINT ON ITS OWN IS OPEN." The art critic concurs |
| S2 | r01, r02 | science | Name what blows up, once, in words; not turbulence | **fixed** | r03 science pass 2: "VORTICITY ×4 EACH RUNG, INFINITE AT ONE POINT. THAT BLOW-UP, NOT TURBULENCE, IS THE QUESTION." |
| S3 | r02 | science | Rung ink density non-decreasing, or declared as the pen floor | **fixed** (declared branch) | r03 science: 0.370/0.739/0.825/0.790/0.773. The floor binds at ¼ (×1.12). The caption "FROM 1/4 ON, THE INK IS THE 0.8 MM PEN FLOOR" is present. The residual −4/−6 % is measured and the designer showed it cannot be culled (the eye's share of a shrinking rung) |
| A1 | r01, r02 | art | Black rings on the 0.3 nib, preview at physical widths | **fixed** | r03 art: the pen plan lists black 0.3, `_v8_phys.png` exists, and the disc weight sits between 0.5 and 0.3 |
| A3 | r01, r02 | art | Terminus + stamp as one block on x = 282, ≤ 7 blocks, red < 1 %, type inside [15, 282] | **fixed** | r03 art and science: type x [15.00, 282.00], 7 blocks, red 0.93 % |
| A5 | r01 | art | Unambiguous time symbol | **fixed** (holds r02, r03) | "IN 4/3 OF THE FIRST RUNG'S TIME" |
| S6 | r03 | science (advisory) | Within-rung perpendicular spacing stays within ±10 % of d_sep. Arm-halving radii make gaps cycle 0.96–1.43 mm, giving 3–4 faint spiral void bands at ρ 0.6–0.8 that suggest arm structure the field does not have. Fix by staggering terminations or J–L seeding | deferred | Advisory under a PASS. Carry it into r04 only if the translator's new rung boundary keeps the halving cull |
| S5 | r01, r02, r03 | science | Encoding housekeeping. Record what was built: orbit factor 1.20, δ₀ 18 mm, R_out 5δ, the hero on its own 0.5 nib, the status stamp black (red = the L mark only), and §2's headline still reading "…and it can keep shrinking" (the S1 lie lives on in the encoding text) | open → translator | Deferred through r03. Now bundled into the translator pass |
| A6 | r02 | art (craft) | Travel is heavy (r03: 14.9 m travel against 17.5 m draw) | deferred | The type-minutes half moved into A10. Travel comes back once the composition holds; the rim → eye returns are mandated |
| A4 | r01 | art | Rectangular side-view window | dropped | The abstract thesis has no elevation. Valid if the faithful flavour is revived |
| S4 | r01 | science | 6 mm stray type dash | dropped | Superseded (the block is gone since r02) |
