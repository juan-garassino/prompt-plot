# Synth — resonance after r06 · 2026-09-29
route: **translator** (rule 2), then designer
next round: **r07** · parent: **r06** (best so far: art 5.71/3 · sci 5/5/6, the first critiqued round that keeps every v13 element and draws J1's mark). The next step is a translator pass. r07 is the designer round that follows it, and must read the new `encoding.md` first.

## Why translator
**S0** ("no dossier.md or encoding.md, so no stated claim set") was NOT FIXED in r04, r05 and r06. The r06 science critic promoted it to mandate 3:

> "The plate is on its third workflow round with no stated science, and it shows on the sheet … Anything declared schematic stops being scored as a lie. Anything declared computed must then measure true."

The art critic points the same way. Encoding §11 lists no acceptance checks, so it could only fall back on AUTHORING §6. It also names the lock:

> "The schematic apparatus (dim 6) caps this plate under the rubric, and J2 locks that apparatus in … Juan has to rule on that."

The three science mandates blocked by J2 (S1c Z scale, S2 key counts, S3a crest stretch and halos) cannot resolve until someone writes down which claims are computed and which are reproduction. That is the translator's document. This is not a request to redesign.

## The instruction (translator)
Write `studio/resonance/encoding.md` v1 as the **codification of v13**, deriving it from DESCRIPTION.md because there is no dossier.

1. Keep v13's composition verbatim. J2 is Juan's binding note and outranks the rubric.
   - §5 is v13's measured layout in mm.
   - §1 keeps the lineage **Thomas Young, *Lectures on Natural Philosophy* (1807), Plate XX Fig. 267: the INTERFERING order**, with a canon only if it does not move anything.
2. Put the family grammar in §6. It is shared with resonance-backprop and resonance-ffn and must hold across all three:
   - Q crimson, K blue, V goldenrod, Z green, MoE/FFN violet, black for the field, softmax and type.
   - Six pens, each one clean layer, streamed light→dark (gold, blue, green, crimson, violet, black).
   - Per-layer minutes come from `promptplot plot plate <gcode> --paper a4:portrait --dry-run`, not a hand model.
3. Split every claim on the sheet into two classes in §3–§4:
   - **COMPUTED.** These must measure true, with exact rules and §7-style check numbers: d = 35·L; crests m 1–21 solid and 22–51 as dotted continuations on r = m·L; field-dot size = f(|A|) in the drawn metric; one gold link per non-zero softmax weight; every forward leader landing on its target's axis.
   - **REPRODUCTION.** These are traced from the reference and stated as such, so they are no longer scored as lies: packet parameters; the 5 K / 3 V / 6 + 3 softmax counts and heights; Z's and Y's size; the MoE fork.
4. Decide S3a honestly. Either declare the hero's drawn metric (a 7:6 vertical scale, in which the crests are exact circles and every hero computation is made), or declare the halos reproduction. Change no v13 geometry.
5. Write §9 Forbidden from this plate's actual traps:
   - no micro-dashes, no re-pitched textures;
   - no deleting or thinning to save time;
   - no crest lens past m 21;
   - no leader landing on ink;
   - no horizontal gold fence.
6. Write §11 as 4–5 png-checkable tests drawn from the r07 mandates below.
7. Add §12, "Open for Juan": dim 6 (NO SCHEMATICS) is fixed at ≤ 3 by J2, so the art verdict cannot PASS unless Juan waives it for the benchmark.

Do not pick a canon, add a twist or write a forbidden list that deletes the apparatus. Those roads were r04, and they are the `one-field` flavour.

## The instruction (designer r07, after the encoding lands)
Fork r06 and keep its Stroke IR, dot resolver and tour. Make one move: **re-wire the lower half so every forward and backward leader lands on bare ink-free axis at its true target, then translate the whole sheet into the plate-job frame.**

1. **Forward pass.**
   - Give each of the six SOLID softmax peaks exactly one gold link, and give the three ghosts none.
   - End each link on a small open gold node on Z's axis, inside the bare carrier gaps (x ≈ 72–80 and 90–97).
   - Redraw V's connector as ONE continuous sweep to Z's axis, with no reversal and no horizontal run over 30 mm. Starting from V row 3's left node instead of its right end is authorised. It is wiring, like S1a, not a composition move.
2. **Backward pass.**
   - Start the blue tap on Z's axis, as red does.
   - End ∂L/∂A (black) and ∂L/∂Z (green) at the router node from below, as the reference does.
   - Where the Q/K/V return curves overrun into the MoE block, end them at their Z taps.
   - Re-aiming or shortening a leader to its reference target is authorised. Deleting one is not.
3. **Packets.** Separate touching rows (K 1/2, V 2/3) by re-pitching rows ≤ 2 mm inside their block. Keep each block's outer extents within ±2 mm. Never shrink amplitudes or delete a packet.
4. **Whole sheet.** Translate everything by ≈ (−2.15, +0.5) mm, so the ink is centred (≈ 15.95 mm each side) and lies wholly inside A4 portrait at a 15 mm margin (x 15–195, y 15–282). That fixes the plate-job refusal and A12's uneven margins in one move.

## Mandates to close (r07; J first; max 5)
1. **J2**: keep the original, and repair r06's three exposures.
   - (a) The V connector is one arc again (A14c).
   - (b) Each halo reads as a whole ellipse passing *behind* the ring field. Carry every halo arc until it meets actual black crest or cap ink (occluded), not a keep-out circle short of it. Test: each halo's visible arcs cover ≥ 70 % of its perimeter, and every arc end lies ≤ 1.0 mm from black ink.
   - (c) Restore v13's ◎ spoke glyphs on the rails as open circle + dot, not plain solid dots.
   - Element-for-element count against v13 stays as in r06 (caps ≥ 220, field ≥ 179, 20 fans, 14 droplines, 8 ∂L fractions with heads).
2. **J1**: the convergence clause, in the Q/K funnel braid.
   - Test: 0 same-pen dots within 0.6 mm of a dot on a *different* path (≈ 67 now).
   - Where two fans of one pen run closer than 2 mm, either merge them onto one shared dot track over that stretch (as r06 does for the ghost rails) or bend control points ≤ 1 mm to hold ≥ 2 mm.
   - Keep all 20 fans. The mark and the 1.0 mm pitch do not change.
3. **A14**: gold wiring.
   - (a) One link per solid peak at x 76.2 / 90.4 / 97.4 / 104.6 / 119.2 / 132.6, none from 83.0 / 111.8 / 125.9.
   - (b) Landings are open gold nodes on Z's axis in bare gaps, with 0 gold dots within 0.8 mm of green ink other than the terminal node.
   - (c) The V connector is one sweep, with no reversal and no horizontal run > 30 mm.
   - Everything stays gold (S1b closed).
4. **A5**: collisions, all without deleting.
   - (a) No packet ink within 1.5 mm of another row's ink in the Q, K and V blocks.
   - (b) ≥ 1 mm clear round `router` and `experts`, and 0 non-violet dots within 0.5 mm of violet ink (11 now).
   - (c) ∂L/∂A and ∂L/∂Z end at the router from below.
   - (d) The blue tap starts on Z's axis (y 75).
5. **A4**: plate-job ready.
   - The sheet translation above. `.venv/bin/python -m promptplot plot plate <gcode> --paper a4:portrait --dry-run` must **plan without refusal at the default `--margin 15`**. r06 is refused: violet X 195.9, green Y 15.0.
   - NOTES states the planner's per-layer minutes and total ETA (F500 draw cap, ≥ 1 s dwells, 90 s swaps), not the 2 s/cycle hand model.
   - Give the exact plate command with `--layers 0,1,2,3,4,5 --batch-strokes 300`.
   - Keep 0 invisible cycles, 0 co-incident ink, travel ≤ 75 %, and in-layer hops ≤ 80 mm except the two argued floors (blue 87.5, crimson 88.3).

Deferred (in the ledger, with reasons):
- S3b |A|-sized field dots → r08. It is a size channel only; the mandate cap is 5.
- A12's right ∂L common edge → r08.
- S1c, S2, S3a wait for encoding v1's declarations and the science critic's pass 2.

## Preserve
- **v13's whole composition**, now on r06's sheet:
  - the title with its rule and dot (v 0.06);
  - Q (u 0.09–0.36) and K (u 0.64–0.91) blocks, with guides and node columns;
  - `Q·Kᵀ/√d_k` with the dotted stub above it (v13 has it; keep it);
  - the hero at (0.40/0.60, 0.44): crests m 1–21 solid at 1.41 mm pitch, d = 35·L (the critic measured 34.995), the `_Guard`, the diamond clusters, axis and end circles;
  - the caps as v13's own 220 mark positions (not r10's mud);
  - softmax with 6 peaks + 3 ghosts;
  - V, Z = AV, the MoE with 2 solid + 3 ghost lanes, and Y;
  - the ∂L band with its 8 solid arrowheads.
- **r06 craft, critic-confirmed:**
  - one dot mark (a 0.2 mm touch, ⌀ ≈ 0.55 mm inked) at a median 1.000 mm pitch in all six pens, 0 micro-dashes and 0 `-` ticks;
  - the ∂L stack at ≈ 10 mm pitch with 3 mm clear air;
  - the carrier IS the axis (no co-incident ink);
  - label halos and node keep-outs;
  - V rows no longer crossing;
  - the red and gold taps joined into their return curves as one dotted run;
  - S1a landings on y = 75.00;
  - light→dark streaming, each pen one contiguous layer never re-entered;
  - travel 70 % and 0 invisible cycles.
- **The funnel.** Ten crimson and ten blue dotted fans dive into the upper ring nest. At 1 mm they read as drawn curves.
- **The family grammar** (resonance, resonance-backprop and resonance-ffn hang as one series): Q crimson, K blue, V goldenrod, Z green, MoE violet, black field and type. Six pens, six meanings.

## Do not
- Do not run a horizontal gold "fence" through the band between softmax and `MoE` (r06's y ≈ 108 run), and do not reverse a leader near the margin.
- Do not land any leader's dots on another pen's packet ink (r06: 11 gold dots on green).
- Do not stop halo arcs at an invisible keep-out circle (r06's C-arcs). They pass behind the field and end on ink.
- Do not thin, re-pitch or delete anything to meet a test (J2). Re-aim, re-route, occlude or share a track instead.
- Do not quote minutes from a hand model when `plot plate --dry-run` gives the real ones. Do not ship ink outside the 15 mm plate-job margin.
- Do not change Z's size, the element counts or the hero's stretch. Those are declarations for the encoding, not moves for the designer.

## Fabrication gate
Not a double PASS, so this was not run as a gate. Baseline read on r06's gcode (`gallery/studio/resonance/current/pp_resonance_iterate_v5.gcode`) for r07 to hold or beat:

- `preview --stats --score`:
  - 4,618 pen cycles, 11,800 mm draw, 8,559 mm travel (8,235 mm without the final 323.6 mm park);
  - bounds X 0–196.2, Y 0–280.3 (0 is the park);
  - grade A, efficiency 0.586.
- `plot layer --list`: colour 0 has 620 strokes, 1 has 1,033, 2 has 239, 3 has 991, 4 has 525 and 5 has 1,210. That makes 6 clean layers, each streamed once.
- `plot plate … --paper a4:portrait --dry-run`:
  - at the default `--margin 15`: **REFUSED**. Colour 2 has 4 points at Y 15.0 and colour 4 has 49 points at X 195.9 > 195.
  - at `--margin 10`: planned and rehearsed clean (96,825 commands, 6 swaps, state done). Layers take 23 / 39 / 10 / 38 / 21 / 51 min, and the **ETA is ~191 min** (F500 cap, ≥ 1 s dwells, 90 s swaps).
- Engine and curator flag, outside the designer's scope: Leo mounts paper **landscape** (house memory), while this plate is A4 portrait, and `plot plate` has no rotate-into-machine-frame option. Before this plate is plotted, either the sheet is mounted portrait on Leo, with the frame trace confirming, or the plate job gains a 90° rotation. Record the choice in `studio/PLOT_JOBS.md`.
- Nothing under `promptplot/` changed in this piece's rounds, so regression and `make check` were not needed.
