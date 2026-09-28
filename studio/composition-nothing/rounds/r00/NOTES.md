# composition-nothing r00 — FROZEN ORIGINAL (v2) · do not edit

This round is **COMPOSITION WITH RED YELLOW BLUE AND NOTHING v2**, the plate at
`gallery/studio/composition_nothing/current/pp_composition_nothing_v2.png`
(caption `28 OF 96 LANES SWEPT.  THE WHITE IS THE BELT.`), restored as runnable code.

## Where the code came from

v2 was **never committed**. The only committed copy is
`studio/orbital-resonance/rounds/r04/piece.py` (first seen in `8ff2ceb`). By then it had
already drifted to 240 lanes, a wider enclosure rule and the `PERCENT OF THE BELT SWEPT`
caption.

The v2 source was rebuilt from the session transcript of the subagent that made it:
`~/.claude/projects/-Users-juan-garassino-Code-005-products-004-creative-tools-001-PromptPlot/148aba30-cc80-456f-bd65-efcd569cff02/subagents/agent-a88bdb972e3e0c8e9.jsonl`
(2026-09-18). It is built from two recorded steps:

1. the `Write` of `studio/orbital-resonance/rounds/r04/piece.py` (transcript line 361, 20:04:10Z), which rendered v1;
2. the in-place patch at line 373 (20:05:12Z), which rendered `pp_composition_nothing_v2.png`. The patch did three things:
   - clamped band edges to [a_lo, a_hi];
   - stopped the vertical rules at the field line, except the strongest band's inner edge, which stays full height;
   - set the fill spacing to 0.62.

**Proof that the reconstruction is complete:** the transcript also records the next patch
(line 392: `n_cols` 96→240, `close`-lane enclosure, PERCENT caption). Replaying
Write + 373 + 392 gives a file **byte-identical to the committed r04 `piece.py`**. So
no edit was missed, and Write + 373 is exactly v2.

`piece.py` here is that v2 file byte-for-byte. The one exception is a 9-line
"FROZEN ORIGINAL" note at the top of the module docstring.

## Render command

```
.venv/bin/python scripts/render_candidate.py studio/composition-nothing/rounds/r00/piece.py \
    --fn composition_with_nothing --seed 7 --colors 4 --paper a4 --orientation landscape \
    --palette black,crimson,gold,dodgerblue --out <out>.png
```

This is the same seed, paper and palette as the original v2 call. The original wrote to
`~/Downloads/pp_composition_nothing_v2.png`.

## Comparison with the gallery v2 PNG (both 2283 × 1703)

| check | result |
|---|---|
| commands after merge | 8427, the same as the transcript's v2 run (`8427 commands`) |
| stats box | Draw 23,964.3 mm · Travel 8,310.0 mm · Colors 4 · Commands 8427. Identical to the gallery PNG. |
| r00 raw fn output vs the transcript-v2 source run today | identical command list (JSON-equal) |
| merged GCode, today's pipeline vs the 2026-09-17 (`20c9e17`) pipeline | identical, 8427 lines, sha256 `142cb0d2f263b8ad` |
| **PNG through the 2026-09-17 visualizer vs gallery v2** | **pixel-identical: 0 of 3.89 M pixels differ (max Δ 0)** |
| PNG through today's visualizer vs gallery v2 | 0.96 % of pixels differ (37,177 px, 23,034 by more than 32/255, mean \|Δ\| 0.69). Every difference is at stroke ends. |

The residual difference in today's render is not geometry. It comes from
`GCodeVisualizer._render_color_layers`, which since 2026-09-21 (`5b93e0c`) draws with
`capstyle="round", joinstyle="round"`. The pen paths are identical. There was no v2
`.gcode` on disk to compare against: v2 was rendered PNG-only. Instead, the GCode was
rendered through the old visualizer, and that reproduces the PNG exactly.

Regression fingerprint (the `scripts/studio_regression.py` shape, raw fn output,
A4 landscape, seed 7, colors 4):
`commands 7630 · draw 23964.3 mm · travel 10161.2 mm · pens [0,1,2,3] · hash 67dd324074315bd9`.
Note that the regression tool's DEFAULTS may be A4 portrait. Pin these params if you add r00 to
`studio/REGRESSION.json`.

## What was vendored

**Nothing.** The piece imports `_poly`, `_spaced`, `_stroke_text`, `_text_width`, `fill_rect`,
`giant_type` and `giant_type_width` from `promptplot.generative.engine.kit`. It also imports
`SeededRNG` and `GCodeCommand`. Today these produce output identical to 2026-09-18 for this
piece, as the byte-identical GCode above shows, so under the restore rule none needed
vendoring. The orbit simulation (planar CR3BP, velocity-Verlet, dt 0.02,
300 Jupiter years, 96 lanes, e₀ 0.18) and the libration and band logic are local to the file
and unchanged.

A quirk to keep: the `_colons` docstring says "the stroke font has no ':' glyph". That was
already out of date at v2. The (then uncommitted, now committed) font had a `:` glyph, and
`giant_type` draws it. So the ratio labels carry **both** the font colon and the hand-drawn
`_colons` squares, overlapping. That overlap is part of the v2 plate, as the pixel identity
proves. Do not "fix" it here.

Drift risk: all seven helpers are shared package code. If the kit's glyph table or fill
routine changes, the fingerprint above changes. If that happens, vendor the helper here
**as it is at `ac7eff8`** (the HEAD this restore was verified on).

New versions go in r01+; this round is the original and is never modified.
