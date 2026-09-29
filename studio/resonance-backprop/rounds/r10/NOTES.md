# resonance-backprop r10 — continuous-dots · parent: r01 · 2026-09-29

Made by hand in the curator session, applying Juan's family-wide note ("the original was much
more beautiful — we just needed the dot lines to be more continuous, not to remove the
waves"). This round is r01 byte for byte except `rdotted`: a dot-sized mark
(dash <= 0.6 mm) is one round tip-scale dot at an even 1.0 mm arclength pitch, anchored at
both ends. Longer dashes and every other element are unchanged. Same change as
resonance r10.

The old helper sampled every 0.30 mm and DROPPED every one-sample run, so dot-sized marks (0.4–0.55 mm) went missing at random — two dotted wave halos around the interference field were nearly invisible. With continuous dots they appear in full; that is the original's intended waves returning, not an addition.

## Render
```
.venv/bin/python scripts/render_candidate.py studio/resonance-backprop/rounds/r10/piece.py \
  --fn attention_as_resonance --seed 7 --colors 5 --paper a4 --orientation portrait \
  --palette crimson,dodgerblue,goldenrod,forestgreen,black \
  --out ~/Downloads/pp_res_backprop_continuous-dots_v1.png
```

## Plot budget (vs r01)
| | r01 | r10 |
|---|---|---|
| draw mm |  |  |
| travel mm | 11389.5 | 11994.19 |
| pen cycles | 11902.34 | 13335.68 |

Each extra cycle is one dot lift; Juan accepts the longer plot. Knobs: `DOT_PITCH`, `DOT_R`.
