# resonance r10 — continuous-dots · parent: r01 (v13) · 2026-09-28

Made by hand in the curator session, not by the workflow: Juan, looking at the workflow's
reworks, said "the original was much more beautiful — we just needed the dot lines to be more
continuous, not to remove the waves". So this round is v13 byte for byte except `_dash_mm`.

## Render
```
.venv/bin/python scripts/render_candidate.py studio/resonance/rounds/r10/piece.py \
  --fn attention_as_resonance --seed 7 --colors 6 --paper a4 --orientation portrait \
  --palette crimson,dodgerblue,goldenrod,forestgreen,darkviolet,black \
  --out ~/Downloads/pp_resonance_continuous-dots_v1.png
```

## The one change
A dot-sized mark (`dash <= DOT_MAX = 0.6` mm) is now one round dot (`_dot`, r = 0.15 mm —
a tip-scale tick) laid at an even arclength pitch `DOT_PITCH = 1.0` mm with a dot on both
ends. v13 drew each "dot" as a 0.42–0.5 mm micro-dash followed by 1.35–2.1 mm of paper, which
read as a broken dashed line. Longer dashes (the 0.85/1.55 envelope) and every other element
are unchanged. Measured before the change: v13's dot pitch was already regular (2.22 ±
0.05 mm), so the fault was the mark and the gap, not the spacing.

## Plot budget (vs v13)
| | v13 (r01) | r10 |
|---|---|---|
| draw | 10.26 m | 10.99 m |
| travel | 11.30 m | 12.89 m |
| pen cycles | 3471 | 6092 |
| commands | 58 991 | 71 828 |

Each extra cycle is one dot lift; Juan accepts the longer plot. Tuning knobs: `DOT_PITCH`
(tighter = more continuous, more lifts), `DOT_R`.
