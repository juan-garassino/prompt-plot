# resonance-ffn r10 — continuous-dots · parent: r01 · 2026-09-29

Made by hand in the curator session, applying Juan's family-wide note ("the original was much
more beautiful — we just needed the dot lines to be more continuous, not to remove the
waves"). This round is r01 byte for byte except `_dash_mm`: a dot-sized mark
(dash <= 0.6 mm) is one round tip-scale dot at an even 1.0 mm arclength pitch, anchored at
both ends. Longer dashes and every other element are unchanged. Same change as
resonance r10.

The old helper sampled every 0.20 mm and drew each dot as a micro-dash followed by paper — the same broken-dash look as resonance v13.

## Render
```
.venv/bin/python scripts/render_candidate.py studio/resonance-ffn/rounds/r10/piece.py \
  --fn attention_as_resonance_ffn --seed 7 --colors 6 --paper a4 --orientation portrait \
  --palette crimson,dodgerblue,goldenrod,forestgreen,darkviolet,black \
  --out ~/Downloads/pp_res_ffn_continuous-dots_v1.png
```

## Plot budget (vs r01)
| | r01 | r10 |
|---|---|---|
| draw mm |  |  |
| travel mm | 12071.03 | 12844.11 |
| pen cycles | 12190.79 | 13446.65 |

Each extra cycle is one dot lift; Juan accepts the longer plot. Knobs: `DOT_PITCH`, `DOT_R`.
