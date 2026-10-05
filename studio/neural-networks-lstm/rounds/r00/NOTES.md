# neural-networks-lstm r00 — FROZEN ORIGINAL (PROMOTED by Juan 2026-09-20) · do not edit

New versions go in r01+; this round is the original and is never modified.

## What this is
The twisted-helix LSTM plate (DESCRIPTION.md variant C): the two-strand braided column
from INPUT to OUTPUT, crimson UPDATE GATE spiral, black FORGET GATE and CELL STATE VORTEX
spirals, `PERSISTING INFORMATION` footer with the helix → spiral → helix strip.
Promoted render: `gallery/neural-networks/lstm/candidates/pp_bauhaus_memory_LSTM_v3_seed1.png`.

## Where it was restored from
- The code was **never committed**. It existed only as an uncommitted edit to
  `promptplot/generative/bauhaus.py::bauhaus_memory` on top of commit **2597b31**
  ("feat(generative): architecture series — settling, relevance, conveyor, memory,
  locality", 2026-09-13 13:26 +0200).
- Source of the body: session transcript `2918d2df-1d19-45d0-9f06-22f9ca365dd1.jsonl`,
  the `Edit` at 2026-09-13T11:38:18Z (line 8876). The render ran 73 s later (11:39:31Z,
  PNG mtime 13:39:42 local); the next edit (11:54:02Z) replaced it, and the figure-8 in
  58bdb22 overwrote the function for good. No other file was edited between 2597b31 and
  the render.
- Reconstruction: detached worktree at 2597b31 + that single edit applied (old_string
  matched exactly once).

## Original render command (2026-09-13, verbatim from the transcript)
```python
cfg = PromptPlotConfig(); cfg.paper = PaperConfig.from_size('a4', orientation='portrait', margin=15)
cfg.color.enabled=True; cfg.color.palette=['dodgerblue','crimson','black']
b=cfg.paper.get_drawable_area()                    # (15, 15, 195, 282)
raw=run_generator('bauhaus_memory',b,1,colors=3,params={})
GCodeVisualizer(cfg).preview(merge_chunks([raw],cfg), '.../pp_bauhaus_memory_LSTM_v3_seed1.png')
```

## Render this round
```
.venv/bin/python scripts/render_candidate.py studio/neural-networks-lstm/rounds/r00/piece.py \
    --fn bauhaus_memory_helix --seed 1 --paper a4 --palette dodgerblue,crimson,black \
    --out <somewhere>/r00.png
```
`--palette dodgerblue,crimson,black` matters: the piece draws on pen 1 (crimson) and
pen 2 (black); the script's default palette would paint pen 2 forestgreen. The seed is
irrelevant (the piece never touches `rng`).

## Comparison result — IDENTICAL
- Old code (worktree 2597b31 + edit) vs. the gallery PNG: the preview's stats box matches
  exactly (Draw 6061.9 mm, Travel 5252.7 mm, 2 colours, 11354 commands) and the geometry
  overlays by eye; residual pixel difference (mean |Δ| 4.5/255 after a 1 px / 2 px
  alignment shift, 3.9 % of pixels > 32) is matplotlib canvas size only (614×836 vs
  615×834), not drawing.
- r00 (today's package + this piece) vs. the old code:
  - raw piece output: 10951 commands, draw 6061.942 mm, travel 6278.053 mm (raw, before
    merge), pens {1, 2}, sha256 of every (cmd, x, y, z, f, colour) `fa2e2b29f2348148` —
    **identical** (both through render_candidate's 10 mm-margin bounds and with the
    original bounds + `margin_mm=None`);
  - merged GCode after `merge_chunks`: 11354 lines, sha256 `42abae32dd527e43` —
    **byte-identical** to the old-commit program (provenance header excluded).

## What was vendored / changed
- Vendored in `piece.py` (as at 2597b31): `_stroke_text` (the package version has since
  gained case-aware lookup, missing-glyph warnings and `proportional=`), the 20 `_GLYPHS`
  it uses (unchanged today, frozen anyway), and `type_block` (same source today but it
  must call the vendored `_stroke_text`).
- Imported from today's package (source verified identical to 2597b31): `_poly`
  (generators), `_pen`, `_spaced`, `fill_disc`, `circle` (engine.kit). PINK=1, BLACK=2
  pinned as constants.
- Added, geometry-neutral: rename to `bauhaus_memory_helix`; `margin_mm=15.0` — the plate
  was composed on A4 at a 15 mm margin, so the piece recovers the sheet from the symmetric
  bounds it receives and re-insets at 15 mm (render_candidate uses a 10 mm margin).
  `margin_mm=None` draws into the bounds as given. The function body is otherwise
  verbatim (diffed against the transcript edit).
