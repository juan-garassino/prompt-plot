# Synth — attention-weaving after r07 + r08 (parallel theses) · 2026-09-29
route: translator
next round: r09 · parent: r07 (best so far: art 6.71/6 · sci 8/8/7, `gallery/studio/attention_weaving/current/pp_attention_weaving_iterate_v23.png`)

## Ranking of the two theses

Both critics gave FAIL on both rounds.

**r07 (iterate on encoding Revision 1): rank 1, the parent.**
- Art min is 6, the first 6 on this plate. Science is 8/8/7.
- It closes twelve mandates: A7, A11, A13, A14, A20, A21, A22, S5, S6, S8, S10, S11.
- It keeps every DESCRIPTION § Keep element: the storm, the wall with one hole, the exact hill, the bold principal thread, and the giant flush-left type.

**r08 (wildcard, "attention is typesetting"): rank 2.**
- Art 6.29/5, science 7/7/8.
- It is a real transposition: a justified line is a partition of one.
- But it deletes the storm Juan praised, the wall, the principal thread and the giant type.
- It prints a false formula (√d is missing), and its widths are exact only on unmarked line centres.
- **Not merged.** The two orders cannot share a sheet: r08 has no top and bottom for J1 to act on, and grafting its type onto r07 would add a second subject.
- **Keep r08 on disk as the `typeset` flavour.** Its critic mandates are parked in the LEDGER in case Juan picks it.

## Why translator (rule 2)
**A19 was not fixed in two consecutive rounds:** open in r06 (regression), PARTIAL in r07. The r07 build shows why.
- r07 designer: "a near-vertical rise of 3.71 mm at each jamb is forced by the data … §11.3 'from zero height with no vertical step' cannot be met."
- r07 science critic, independently: "**mathematically impossible** under exact area + strict unimodality … The designer drew the truth. Expected: translator deletes §9.4 / §11.3's 'no step'."
- r07 art critic: "the raised shelf and the two vertical jamb steps still echo the ziggurat base". This is J2 PARTIAL, and a designer cannot fix it without breaking "sums to one exactly".

**J1 is PARTIAL for the fifth round.**
- r07 art: "it reads as sparse gold staples on a band ~40 % of the storm's width, not as a woven fan equal to the top".
- Two of the causes are in the encoding:
  - §5's lane extent (exits y 56–172) puts lane 0 inside the A21 void, which is why the designer built the cloth higher and smaller.
  - The merge-under rule, combined with 216/352 entries below 1/16, hides about 61 % of the weft by construction.

This is an amendment to Revision 1, not a new order. Everything that closed in r07 stays.

**Fabrication gate:** not run (no double PASS). r07's plotting report already meets the curator's plotting law and must keep doing so: one clean layer per meaningful pen, stated order light → dark, serpentine batchable strokes, and minutes per layer. The layers are gold 3.9 min, blue 6.6, crimson 7.5, green 12.5, black 14.4 and text 16.6, about 62 min in total.

## The instruction
Amend `studio/attention-weaving/encoding.md` to **Revision 1.1** (the header says so; r09 is then round 2 of 5 under Revision 1). Keep the storm, the reed, R1 (one weft), R2 (order-only lanes) and the 52 mm slit. Rewrite only the three places where the encoding and the data or the sheet contradict each other.

1. **The hill floor (S12, A19 residual, J2).**
   - Delete §9.4 and §11.3's "zero height, no step".
   - Decide what the unavoidable rise means:
     - (a) Area stays ∝ a (so Σ area = 1 exactly, which is Juan's J2 word). The floor is then named in the footer, `a MIN 0.034 — NO KEY GETS ZERO`. You must also specify a drawn form for the rise that reads as intended at 3 m and not as r06's table: for example, the hill's tails and the jamb corners as one continuous stroke with a stated fillet radius, or some other form you justify.
     - (b) Area ∝ (a − a_min), printed in the footer. Say what this costs the "sums to one" reading.
   - Rewrite §11.3 so the art critic can PASS it from the png.
   - Define "the hill stands above the 1/16 tick over bins 6–9" as a test the eye and the gcode agree on. Today art reads bin 9 as below the tick pointwise, while science finds bin 9's mean above it and 53 % of it above pointwise.
2. **The cloth's size and the weft's visibility (J1, A24).**
   - Reconcile §5 with the A21 void: give lane extents, the lane-exit span on the right frame, and the weft end ticks. These must let the cloth fill about x 135–230 and reach down toward the `Z = AV` band, while lane 0 stays out of the crop x 10–90, y 100–150.
   - Then decide the under-rule so that a pick reads as ONE gold thread:
     - Target: gold draw ≥ 1.5 m (r07: 1.1 m), and the longest hidden run on any pick ≤ 25 mm (r07: 33 mm on pick 1).
     - The arithmetic: breaking gold only at each lane it passes under (a 2.2 mm gap, no merging) leaves pieces of (pitch along pick − 2.2) mm. The 5 mm floor then needs ≥ 7.2 mm pitch along the pick; the ≈ 5.5 mm pitch leaves 3.3 mm pieces.
     - So either say where that pitch comes from, or restate the gold floor for a piece that is flanked by green gaps on both sides. The A7 floor was written against crumbs in open paper, not against woven cells. Say which, and why.
   - Specify the turns (A23): one radius, apex ≤ 2.5 mm outside the selvage, apexes on curves parallel to lanes 0 and 21.
3. **Sheet truth (S13, S14).**
   - Put §8's count balance in footer line 2, e.g. `22 Q · 16 K → 22 Z WARPS × 16 V PICKS`.
   - Correct §4: the entry nearest 1/16 is Q15×k2 = 0.062462, not Q5×k3. Correct the R2 centroid numbers to 1.88 bins spread and 0.006 bin minimum separation, bin-ordered.
   - Update §11 so every check above is PASS/FAIL-able from the png.

If the cloth cannot be made to answer the storm inside this order, report **UNWORKABLE** with the reason. Do not paper over it.

## Mandates to close (the translator encodes; r09 builds)
1. **J1 + A24.** Bring the bottom up to the top: the cloth takes its encoded size, gold draw ≥ 1.5 m, longest hidden run ≤ 25 mm, weft ends at the encoded ticks. Only Juan closes J1.
2. **S12 + A19 + J2.** An honest hill floor: the encoding is amended, the floor is named or re-mapped on the sheet, and the rise reads as intended. The 1/16 test is defined so art and science agree.
3. **S9 (build, r09).** Every crimson arrives vertical at its own slot x = 103.5 + (k − 11)·2.25 and stops 1.25 mm above the hill. Slot 0 lands inside the slit above bin 0 (r07: at (76.21, 187.29), on the wall arm). The limit is 22/22 ≤ 0.5 mm.
4. **A23.** A woven selvage: one turn radius, apexes ≤ 2.5 mm outside lanes 0 and 21, on curves parallel to them.
5. **S13 + S14.** The count balance goes in the footer, and the encoding errata are corrected.

**Deferred, with reasons:**
- **S15 (`dossier.md`):** a standing gap, not blocking. The encoding carries the data. It is written at the next expert route or at vote.
- **A15:** argued. The §8 twist is the answer, flagged for Juan.
- **A16:** argued (BRIEF: five inks).

## Preserve (r07, `gallery/studio/attention_weaving/current/pp_attention_weaving_iterate_v23.png`)
- **The storm, y 186–290.** 22 Q + 16 K. The storm crossings are 111 by NOTES (min angle 36.4°, min piece 2.29 mm, 0 stubs) and 109 by the science critic's count, all 109 correct. K closes at the top and right reeds; mouths are ≥ 3.2 mm apart; 38 ticks for 38 strands (A8, A22).
- **The wall and the throat.**
  - The wall is a 5-pass rule at y 183.6 with one 52 mm slit, x 77.5–129.5, and 16 equal bins of 3.25 mm.
  - The hill is area-exact, with the crown in bin 7 and the summit under the bold Q11 at x 103.5.
  - The 1/16 tick sits outside the right jamb at x 129.9–132.9.
  - `SOFTMAX` sits on the open right arm.
  - There is no chart furniture in the throat (A9, A10).
- **The weft.** One gold thread, 16 picks and 15 turns, with both ends on frame ticks. 0 gold ends in open paper, min piece 5.01 mm, and 352/352 crossings obey a > 1/16 with 0 overrides (A7, S11). Z11 is under gold at exactly picks 7–10.
- **The lanes.** 22 at equal 2.25 mm pitch, seriated, captioned `ORDER ONLY`. Lane rows are an exact bijection onto the queries. There are 0 lane–lane crossings, 22/22 exits are ticked, and `11` marks the bold exit (S8, S10).
- **The left L void.** The crop x 10–90, y 100–150 holds 0 marks, and the gold lead-in is its floor (A21).
- **Type.** The giant `SUMS / TO ONE` is flush-left with uniform filled strokes (A13). `Z = AV` sits on the TO ONE baseline in open paper (A11). The footer has 4 lines, every number true (S4), and there is no text above the wall except `Q`, `K` and `SOFTMAX` (A20).
- **Plotting.** Travel is 7.04 m against 13.23 m of draw (A14). Six layers run light → dark, each one clean pass with serpentine emission, and minutes are reported per layer.

## Do not
- Do not touch the storm, the slit width or the bin count (translator and r09 alike).
- Do not buy a step-free hill by breaking exact area, unequal bins or ringing. J2's "exactly" outranks the art clause. Name the floor instead.
- Do not grow the cloth into the A21 crop, and do not buy weft visibility by overriding the a > 1/16 rule at any crossing.
- Do not graft r08's type-as-data onto this plate. It is its own flavour.
- Do not judge the gold from a hairline preview. The art critic re-rendered at physical nib widths, and r09 should report a nib-width preview (engine request: `render_candidate.py --pen-widths`).
- Do not print a formula or count on the sheet that was not recomputed in the same call (r08's `SOFTMAX(QKᵀ/T)` lie).

**Flags for Juan at vote:**
- §8 re-reads the BRIEF's count rule as 38 in = 38 out (Q+K in, Z warps + V picks out).
- The hill's jamb rise is forced by exact area.
- r08 `typeset` is available as an alternative flavour.
