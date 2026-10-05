# Science critique — lstm-spirals r03 · machine learning (LSTM recurrent memory) · 2026-09-29
render: gallery/studio/lstm_spirals/current/pp_lstm_spirals_forget-gate-vortex_v20.png (+ .gcode, 20309 cmds, 3 pens, draw 13224.7 mm — re-summed from gcode: 2990.9 blue + 4061.9 red + 6172.0 black = 13224.8)

Pass 1 (cold). There is no `dossier.md`, no `encoding.md` and no `LEDGER.md` for this slug. The only
claims available are HANDOFF.md and the sheet's own footer. The one data artifact in r03 is a `.py`
(train_lstm.py). I did not open or run it, and I did not run check_plate.py either, because the blindness rule forbids it. **No
§7 check number exists to recompute. That is finding #0: the plate's central quantity (the per-step
i_t / f_t / o_t trace) has no independent source a referee can check.** (r04/lstm_weights.json
belongs to a later round: a 45-char target, so 44 or 45 steps. It cannot be r03's 36-step trace and was not used as evidence.)

## Check numbers   quantity | dossier | recomputed | measured on sheet | OK?
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| number of time steps T | — (none) | not recomputable | 36 radial slots: 27 red closed rings + 3 blue bands × 3 slots | UNVERIFIABLE |
| red "keep" rings (f>i) | — | — | 27 closed circles (sweep 360°, end gap 0.00), r = 3.12 → 43.41 mm about (114.5, 91.2) | UNVERIFIABLE |
| step sequence rim→eye (B=i>f, R=f>i) | — | — | B3 · R9 · B3 · R12 · B3 · R6 (blue bands r 43.7–47.2, 28.7–32.6, 9.9–13.9 mm; the red gaps 32.95→27.91 and 14.23→9.28 are each 5.0 mm = 4 pitches, so 3 slots each) | UNVERIFIABLE; all three blue runs are exactly 3 steps long, which looks like quantization |
| ring pitch (one step) | — | constant if radius = time | 1.36 mm at rim → 1.28 → 1.25 → 1.23 at eye; smooth and continuous across the red/blue boundaries | encodes nothing, and the ~10% warp is not declared |
| ring concentricity | — | concentric annuli | ring centre drifts 1.4 mm (y 92.55 outer → 91.15 inner); outer ring r-span 2.44 mm, so the rings are egg-shaped | minor |
| blue "write" marks | "annuli where i_t>f_t" | one annulus per step | 108 dashes, each exactly 14.0 mm long. Each dash is a log-spiral arc (~14° pitch) that crosses the WHOLE 3.4 mm band, so there are 0 annuli and the steps cannot be counted | NO |
| h_t vortex (black) | "hidden state h_t" | per-step o_t / h_t channel | 93 streamlines, 100% drawn inward and counter-clockwise, ending ≥6.5 mm from the eye at (115, 215). No turn/step structure and no quantity | decorative |
| o_t ("BLACK: o_t LETS GO") | — | — | no mark on the sheet carries o_t | NO |
| c_t → h_t coupling (h = o·tanh c) | — | — | no drawn link between the two eyes; the only contact is streams bending away at y≈150 | absent |

## Lies list       item | clean / VIOLATED (where)
(There is no dossier §4. These items are derived from HANDOFF plus the standard LSTM lies.)
| item | status |
|---|---|
| gate values invented or stylised rather than computed from a model | UNVERIFIABLE: there is no trace outside a .py; the 3/3/3 blue runs are suspiciously regular |
| "one turn = one step" | VIOLATED for blue: the write steps are one band of dashes per 3 steps (r 9.9–13.9, 28.7–32.6, 43.7–47.2 mm). It holds for red |
| gates as binary switches (keep XOR write) | VIOLATED: only sign(f_t − i_t) is drawn. In a real LSTM f and i are independent sigmoids and a step can keep AND write. Magnitude is lost everywhere (the pitch ignores the gates) |
| "the forget gate is a drain" (title, top-left y≈262) | VIOLATED: f_t is the retention fraction and the drain is (1 − f_t). The title contradicts its own footer "RED: f_t KEEPS" (y≈12). The drain-like inward marks are the blue i_t bands, not f_t |
| o_t shown (footer "BLACK: o_t LETS GO") | VIOLATED: the black vortex is a plain inward sink with no o_t quantity and no step structure. "Lets go" is drawn as inflow |
| c_t labelled as a state but drawn as a value | clean: radius = time, and no magnitude is claimed |

## Scores          truth · fidelity · legibility · VERDICT: PASS | FAIL
- truth **5**: the gate trace has no verifiable source; the title inverts f_t's role; o_t is claimed but not drawn.
- encoding fidelity **5**: red rings are an honest 1-ring-per-step channel. But blue collapses 3 steps into one band of 14 mm dashes, gate magnitude appears in no channel, and the black mass carries no data.
- insight legibility **6**: the Rotorelief reads as a sheet of time for the red keep-runs. But a stranger gets title and footer that contradict each other, and there is no c→h link, so h_t = o_t·tanh(c_t) is not visible.
- **VERDICT: FAIL**

## Mandates        1. … 2. … 3. …
1. **Make the gate trace checkable, and make the sheet match it step for step.** Ship dossier §7 (or a data file, not .py) with T, seed and the per-step (i_t, f_t, o_t, c_t) of the trained model. On the sheet I measure T = 36 with rim→eye sequence B3·R9·B3·R12·B3·R6: 27 red rings r = 3.12–43.41 mm, and blue bands at r 43.7–47.2 / 28.7–32.6 / 9.9–13.9 mm around the cell eye (114.5, 91.2). The expected value is the recomputed trace, which does not exist today. The perfectly periodic 3-step writes must be shown to be the model's output and not a quantization.
2. **Blue must be one annulus per step, and gate magnitude must enter a channel.** Each blue write step is currently unreadable: 108 identical 14.0 mm spiral dashes each cross a whole 3.4 mm, 3-slot band. Expected: 9 individually countable blue annuli at the 1.25 mm step pitch, like the red ones. In addition, give the gates a quantitative channel: ring pitch, ink duty or dash length ∝ f_t (and i_t for blue). Today the pitch runs 1.36 → 1.23 mm smoothly and ignores the red/blue boundaries, so only sign(f_t − i_t) is encoded.
3. **Fix the o_t / drain claims on the black vortex and in the title.** Footer "BLACK: o_t LETS GO" (y≈12 mm): the black vortex (eye (115, 215), 93 streamlines, all inward and counter-clockwise, ending 6.5 mm from the eye) has no o_t value and no 36-step structure. Expected: an o_t channel per step, and a visible c_t → h_t coupling (h_t = o_t·tanh c_t) between the two eyes on the x = 114.5 axis, which are 124 mm apart. Title "THE FORGET GATE IS A DRAIN" (y≈262): f_t is retention and the drain is 1 − f_t. Reword it so it agrees with "RED: f_t KEEPS".

## Follow-up on open mandates   id | status | evidence
No LEDGER.md exists for lstm-spirals, so this is the first science pass. There are no open S* mandates.
