# neural-networks-manifold r00 — FROZEN ORIGINAL · do not edit

The MLP "FOLD braid", restored from git history. Reproduces
`gallery/neural-networks/manifold/candidates/pp_bauhaus_manifold_MLP_FOLD_v1_seed{3,8}.png`
(the two files are byte-identical).

New versions go in r01+; this round is the original and is never modified.

## Provenance
- **Code:** interim `bauhaus_manifold` in `promptplot/generative/bauhaus.py` at commit
  **`58bdb22`** (2026-09-13 14:03 +0200). Replaced in `232622c` (14:16) by the
  petal-saddle 3D engine.
- **But the render predates that commit.** PNG mtimes are 13:49; session transcript
  `2918d2df-…jsonl` shows the render at 11:49:36Z (13:49 local), and 60 s later an edit
  changed the default `twist: 2.0 → 1.6` before the commit. The committed default does
  **not** reproduce the sheet; `twist=2.0` does. No other edit touched this function
  between the render and the commit. The function uses no randomness — every seed
  gives the same sheet, which is why seed 3 and seed 8 are identical.
- **Original render command** (from the transcript, run from the repo root):

  ```python
  cfg = PromptPlotConfig(); cfg.paper = PaperConfig.from_size('a4', orientation='portrait', margin=15)
  cfg.color.enabled = True; cfg.color.palette = ['dodgerblue', 'crimson', 'black']
  b = cfg.paper.get_drawable_area()                      # (15, 15, 195, 282)
  raw = run_generator('bauhaus_manifold', b, seed, colors=3, params={})   # twist was 2.0 on disk
  prog = merge_chunks([raw], cfg)
  GCodeVisualizer(cfg).preview(prog, f'.../pp_bauhaus_manifold_MLP_FOLD_v1_seed{seed}.png')
  ```

## Render this round
Studio harness (margin 10 by default — see "frame" below):

```
.venv/bin/python scripts/render_candidate.py studio/neural-networks-manifold/rounds/r00/piece.py \
    --fn bauhaus_manifold_fold --seed 8 --paper a4 --palette dodgerblue,crimson,black --out <png>
```

Pass `--palette dodgerblue,crimson,black`: the piece addresses pens as `_pen(PINK=1)` /
`_pen(BLACK=2)` with `colors=3`; the harness default palette would paint the black
strands forestgreen.

**Frame.** The original sheet is A4 portrait with a **15 mm** margin, bounds
(15, 15, 195, 282). `render_candidate.py` has no margin flag and uses 10 mm, so its
output is the same composition re-fitted to (10, 10, 200, 287): same 14 810 commands,
draw 39 556.8 mm / travel 36 711.9 mm, not the original's coordinates. For the exact
original, call `bauhaus_manifold_fold(SeededRNG(8), (15, 15, 195, 282), colors=3)` and
`merge_chunks` with a `margin=15` A4 config (as in the command above).

## Comparison result (2026-09-28)
- Old code (worktree at `58bdb22`, `params={'twist': 2.0}`) re-rendered with today's
  matplotlib: stats box identical to the gallery PNG — **draw 38 188.5 mm, travel
  35 574.5 mm, 14 810 commands**. The PNG is not byte-identical (834×615 vs 836×614;
  matplotlib 3.11.2 in today's `.venv` vs whatever the Sep-13 pyenv had). Registered on
  the green drawable box: mean |diff| 14.8/255, ink IoU 0.813. The committed default
  `twist=1.6` gives mean |diff| 41.1/255, IoU 0.490 — so 2.0 is the value.
- **r00 with today's package, original frame:** raw piece output **identical** to the
  58bdb22 function (13 675 commands, every command/x/y/z/f/color equal; raw hash
  `b1b74e7f1cd65b1c`). After `merge_chunks`: **identical** to 58bdb22's pipeline
  (14 810 commands, all fields equal; merged hash `751ac3d21a34dd8e`), draw 38 188.5 mm,
  travel 35 574.5 mm. Feeding r00's merged program through the 58bdb22 visualizer gives
  a PNG **byte-identical** to the old-commit render.
- seed 3 == seed 8 (raw and merged).

## What was vendored (frozen in piece.py)
- `_stroke_text` — the package version has since changed (takes characters as written,
  capitals as fallback, logs missing glyphs, optional proportional advance); the
  58bdb22 version upper-cases and drops unknown glyphs silently.
- `_GLYPHS` — only the 21 characters this sheet draws, copied from 58bdb22
  (currently the same as the package, but glyphs get edited).
- `type_block` — vendored so it calls the vendored `_stroke_text`.
- Imported from today's package (behaviour unchanged): `_poly`, `_dot`
  (`generators`), `_pen`, `_spaced`, `PINK`, `BLACK` (`engine.kit`). If either `_poly`
  or `_dot` ever changes, vendor it here rather than editing the body.
- The function body is verbatim from 58bdb22; the only differences are the name, the
  untyped `rng` argument and the `twist` default (2.0).

## Known flaws (kept — this is the original)
- **Ink beyond the margin:** the three right labels start at `cx + 0.34·W` (u ≈ 0.77)
  and run past the drawable edge. The postprocess bounds stage clamps each `G1` to the
  margin but leaves `G0` travel positions out to the paper edge, so every glyph stroke
  past the margin becomes a smeared bar from the clamped x back to its out-of-margin
  start (132 bounds violations at margin 10). The labels read `LINEAR TR…` / `NONLINEAR…`.
- Type collisions: `INPUT SPACE` over the subtitle; the caption overprinted by the
  lower strand fan and the OUTPUT box edge; `OUTPUT SPACE` on the box line.
- The middle third floods (tens of hairlines crossing at points on the centre line);
  draw ≈ travel.
- Concept: a twist is not a fold — no crease, no many-to-one mapping (see
  DESCRIPTION.md § The science it encodes).
- No hidden-line removal: back strands draw over front ones.
- The `rng` argument is unused.
