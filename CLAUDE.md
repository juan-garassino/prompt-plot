# promptplot

## What this project is
A system that takes a text description and turns it into a physical drawing
made by a pen plotter (a robot that holds a real pen and draws on real paper).

You describe something — "draw a spiral", "write my name", "draw a mountain range" —
and the system:
1. Sends the description to an AI (LLM)
2. The AI generates movement instructions for the plotter (GCode)
3. Those instructions get sent to the physical machine over a cable

## What GCode is (plain language)
GCode is a simple language for telling machines where to move.
Each line is a movement instruction, like:
- `G0 Z5` = lift the pen up
- `G0 X50 Y30` = move to position (50mm, 30mm) without drawing
- `G1 X80 Y30 F3000` = draw a line to (80mm, 30mm) at speed 3000

The machine reads these one line at a time and moves accordingly.

## The pipeline (in order)
1. User types a description
2. LLM receives the description + instructions on how to draw
3. LLM generates GCode
4. GCode gets validated (check nothing will break the machine)
5. GCode gets sent to the plotter over USB/serial cable
6. Plotter draws it on paper

## Hardware
- A pen plotter connected via USB (serial port)
- The machine speaks a firmware language (Grbl or similar)
- It replies "ok" after each instruction to say it's ready for the next one
- Canvas size is physical paper — A3 (297mm × 420mm) or similar

## Stack
- Python (>=3.9), `uv`-managed. `click` CLI, `rich` output, `pydantic` v2 models.
- `pyserial` / `pyserial-asyncio` — for talking to the plotter over USB
- LLM SDKs are optional extras (`openai`, `anthropic`, `google-generativeai`); `matplotlib`+`numpy` are the `viz` extra; `svgpathtools`+`ezdxf` are the `io` extra (SVG/DXF import — stdlib fallback parsers ship built-in)
- GCode as the intermediate format

## Commands
- `make dev` — install editable with dev+viz extras (`uv pip install -e ".[dev,viz]"`). Optional extras: `uv pip install -e ".[openai,anthropic,gemini,vision,io]"` (`io` = svgpathtools+ezdxf for full-fidelity SVG/DXF import).
- `make check` — **the gate: `test-ci` + `studio-check`.** Run it before calling
  anything done. `studio-check` (`scripts/studio_regression.py`) fingerprints the 51
  studio pieces, which live outside the package and which no test imports.
- `make test` — runs the full suite (~630 tests). Note: pytest `addopts` **always** runs coverage (`--cov`, html+xml reports) and treats warnings as errors (`filterwarnings = ["error", ...]`) — a new `DeprecationWarning` will fail CI unless whitelisted. One pre-existing failure (`test_refinement.py::test_batch_refinement_prefers_improved_result`, a stub-queue exhaustion) predates the v3.1 work; `make test-ci` deselects it.
- Single test: `python3 -m pytest tests/test_primitives.py::test_name -v`. By marker: `-m "not requires_hardware and not requires_llm"` to skip hardware/LLM-gated tests.
- `make lint` (ruff) / `make format` (black + isort). Line length 100.
- Run the tool: `python3 -m promptplot ...` or the `promptplot` entry point (`cli:main`).

## Skills available

### Runtime skills (for when you're actually drawing)
- `pp-stream` — sends GCode to the plotter, handles errors if it jams
- `pp-validate` — checks GCode won't crash or go off the paper before sending
- `pp-simulate` — shows you what the drawing will look like before running it

### Dev agents (for improving the code — these are **agents**, not skills)
- `pp-improve` — diagnoses a quality complaint, fixes the cause, runs `make check`
- `pp-optimize` — toolpath ordering (never reorders across a colour boundary)
- `pp-prompt` — the drawing-DSL prompts; a missing primitive usually beats more prompt text

All seven pp-* skills/agents were rewritten 2026-09-21: the earlier versions called
`scripts/{validate,simulate,serial_stream,detect_ports,orchestrate}.py`, none of which
exist, and `pp-stream` streamed whole files with no frame trace.

### Studio agents (design new plates — project agents in `.claude/agents/`)
- `studio-expert` — field expert → `studio/<slug>/dossier.md` (truths, lies list, check numbers)
- `studio-translator` — dossier → `encoding.md` (canon, abstract order, mapping, acceptance checks)
- `studio-designer` — builds one round `studio/<slug>/rounds/rNN/` by thesis (faithful / mechanism / abstract / lens), self-iterates on its PNG
- `studio-art-critic` / `studio-science-critic` — blind to code; cold score, 3 mandates, follow-up on open mandates
- `studio-lead` — keeps `LEDGER.md`, writes `SYNTH.md` (next work order), routes, runs the fabrication gate

The main session is the curator; `.claude/workflows/studio.js` runs the whole loop per plate
(parallel theses → both critics → lead → follow-up rounds → stop at vote). Every plate has a
vision-reviewed `studio/<slug>/DESCRIPTION.md` (sheet in (u,v), Keep, Weak, three next
theses) — the starting spec; `python scripts/studio_descriptions.py [--json]` rebuilds the
`studio/DESCRIPTIONS.md` index and emits workflow args. Protocol:
`promptplot/generative/STUDIO.md` § Iteration protocol.

### Controller skills (drive PromptPlot from Claude Code)
- `pp-orchestrate` — supervisor-worker loop for dense (10k+) drawings: plan
  regions → generate per region → validate → score → retry weak → stream →
  checkpoint. Uses the public `promptplot.orchestrate` API.

## ⚡ AGENT BEHAVIOR — READ THIS FIRST

When the user says anything like:
- "the drawings don't look right" / "it's not working"
- "the pen lifts too much" / "it's drawing wrong"
- "the AI keeps getting it wrong"
- "make it better" / "improve this" / "fix this"
- "something is broken"

**Do NOT just give advice. Immediately launch the `pp-improve` agent.**
Run it autonomously: generate test drawings, validate GCode, simulate
toolpaths, score quality, diagnose failures, apply fixes, report what changed.

When the user says:
- "send this to the plotter" / "run this drawing" / "start drawing"

Run `pp-validate` first, then `pp-stream` if it passes.

When the user says:
- "show me what this will look like" / "preview this"

Run `pp-simulate`.

When the user says:
- "explain how X works" / "why is X happening"

Use skills interactively to explain — don't launch agents.

## How to ask (no jargon needed)
- "The drawings don't match what I described" → launches pp-improve
- "The pen is lifting too much" → launches pp-improve
- "Send this file to the plotter" → pp-validate then pp-stream
- "Show me what this will draw" → pp-simulate
- "The plotter isn't connecting" → interactive, uses pp-stream

## Things that can go wrong (and what they mean)
- "ALARM" from the machine → emergency stop, something hit the edge
- "error:X" from the machine → bad GCode instruction, pp-validate would have caught it
- Pen dragging between strokes → missing pen lift (G0 Z5) in the GCode
- Drawing goes off the paper → bounds not set correctly in the LLM prompt
- One side of a shape looks different → the AI doesn't understand the geometry

## Current status
v3.1 — organized into subpackages (`llm/`, `workflow/`, `cli/`, `generative/`, `importers/`) plus
core flat modules, 7 LLM providers (OpenAI, Azure OpenAI, Gemini, Ollama, Anthropic, OpenRouter, NVIDIA NIM),
a PRIMITIVE/FREEFORM drawing DSL with self-describing prompt schemas (see "Drawing DSL"),
figurative/abstract/hybrid creative-mode routing,
config-aware prompts, bounds validation, multimodal vision feedback, style presets
(artistic/precise/sketch/minimal), 6-stage postprocessing pipeline
(arcs → bounds → pen safety → stroke optimization → paint dips → pen dwells),
**multi-color pen layers** (group by color → park + keypress swap → next color, with color-coded preview),
**seeded generative art** (deterministic-from-seed `art` command: tiled_field, ripple_field, flow_field,
maze, truchet, wave_bands, stipple, waves_with_circles, crosshatch_weave, turning_weave, wave_gradient,
interference_field, frequency_lens, hitomezashi, harmonograph, vortex_field, moire_layers,
strange_attractor (11 systems), domain_warp, contour_field, superformula_bloom, lissajous_carpet,
scribble_halftone (shape-aware), comic_panels, line_halftone, scribble_portrait, sparkle_grid,
iso_city, rounded_circuits, lissajous_swarm, black_hole,
pe_carpet, attention_arcs, residual_river — 37 total;
plus effects applicable to any generator: `--anaglyph`/`--glitch`, `--echo N`, `--dash-rain`, `--occlude MM`, `--glitch-slice`, and `--max-ink N` / default tip-width overlap guardrail — see "Effects"),
**SVG + DXF import** (split by stroke color / DXF layer → color layers),
selectable paper size (A3/A4/A5/A6 or custom `WxH` via `--paper`), native paper tones for previews (`--paper-color cream|white|<any>`, `VisualizationConfig.paper_color`),
quality scoring with letter grades (A–F), drawing memory for few-shot learning,
multi-pass generation, diagnostic retry, style transfer, brush/paint mode,
first-class pen state tracking (PenState), validated phase transitions
(IDLE → PLANNING → GENERATING → STREAMING → PAUSED → DONE),
plotter connection state machine (DISCONNECTED → CONNECTING → IDLE → STREAMING → ALARM → RECOVERY),
resumable drawing checkpoints, and LLM-driven composition planning.

Main commands:
- `promptplot draw "prompt" --simulate` (batch) / `--live` (real-time) / `--colors N` (multi-color) / `--paper a4`.
- `promptplot art <generator> --seed N --colors K --simulate --preview` (seeded generative, no LLM).
- `promptplot import file.svg|file.dxf --simulate --preview` (vector file → color layers).
- `promptplot plot frame --paper a4:landscape --margin 15` (MANDATORY pen-up paper-edge+margin trace, 3s hold on first edge) · `promptplot plot layer file.gcode 1 [--strokes S:E] [--dry-run]` (guardrailed per-colour streaming with batches, 60s acks, park (0,0)) · `promptplot plot plate file.gcode [--layers 0,2,3] [--batch-strokes 400] [--rezero-every 2000] [--resume JOB_ID] [--retrace] [--jobs] [--port …] [--paper …] [--dry-run]` (a WHOLE multi-pen plate as one resumable job — frame, per-layer park + pen-swap wait, pen-up approach, batches, re-zero checks, job file `~/.promptplot/plot_jobs/<id>.json` after every batch; Enter/p/s at waits, Ctrl-C once = pause, twice = stop; draws capped F500 + dwells floored 1.0s by default; engine `promptplot/plotjob.py`, spec + status `studio/PLOT_JOBS.md`) · `promptplot plot file.gcode` (legacy full-file plot).

New flags on `draw`: `--plan` (LLM plans composition first), `--resume` (resume interrupted drawing),
`--orchestrate --regions N` (supervisor-worker fan-out), `--colors N` (LLM assigns colors, plotter pauses
for swaps), `--paper a3|a4|a5|a6 --orientation portrait|landscape`.

### Four controllers
PromptPlot can be driven three ways, sharing the same postprocess/scoring/plotter primitives:
- **File** — replay curated .gcode from `~/.promptplot/library/` (`promptplot library list|play <name>`).
- **LLM** — `SupervisorWorkerWorkflow` runs the plan→workers→merge→critique→retry loop in one
  Python process. Drive via `promptplot draw "..." --orchestrate --regions N`.
- **PromptPlot Agent** — the built-in agentic controller (`promptplot agent`, package
  `promptplot/agent/`): an LLM-agnostic chat loop (any of the 7 providers via a strict JSON
  tool-call envelope in `agent/protocol.py`) over a typed toolbox (`agent/tools.py`:
  list/render generators, render DSL blocks, score, validate, import, memory search, plus the
  framework tools: `studio_list_briefs`/`studio_get_brief`/`studio_design` (the native design
  loop) and `compose_plate` (lamina → gcode+png+pen plan; plot via `stream_to_plotter`)).
  Sessions persist to `~/.promptplot/agent_sessions/<id>/` (transcript.json + trace.jsonl +
  renders/ + report.md); resume with `--session <id>`. Headless: `promptplot agent -p "..."`.
  Tools are tiered safe/confirm: `critique_render` sends a png to the provider's vision model
  (`acomplete_multimodal`; NVIDIA default vision model llama-3.2-11b-vision), and the confirm
  tier (`stream_to_plotter`, `save_to_library`) always traces the pen-up frame first and needs
  an interactive y/N or `--yes-plot`. OpenAI/NVIDIA use native function calling
  (`acomplete_tools` on the provider base, `_openai_native_tools` helper); every other provider
  falls back to the JSON envelope automatically. Tests: `tests/test_agent.py` (stub providers,
  no keys/hardware). Proven live: the agent on NVIDIA rendered, vision-critiqued its own png,
  adjusted a param and re-rendered autonomously.
  MCP surface: `promptplot mcp` serves the same toolbox over stdio (`agent/mcp_server.py`,
  FastMCP; optional extra `pip install -e ".[agent]"`): 15 tools with ToolAnnotations
  (readOnlyHint / destructiveHint), error envelope with `remediation`, inline `Image`
  previews via `preview_image`, `plot://renders` + `plot://render/{file}` resources, and
  hardware gated behind an explicit `confirm=true` argument — any MCP client can drive
  the plotter.
- **Claude Code** — external orchestrator using the public `promptplot.orchestrate` API
  (`plan_regions`, `generate_region`, `validate_chunk`, `score_chunk`, `merge_chunks`,
  `stream_chunk`, `load_and_continue`). The `pp-orchestrate` skill teaches the loop.

## Drawing DSL: how LLM output becomes GCode
The LLM does **not** emit raw GCode for shapes. It emits a `DrawProgram` (`models.py`) whose
commands are one of three kinds, expanded deterministically by `primitives.py`:
- **PRIMITIVE** — parametric shapes expanded to exact `G1` segments. Registry: `circle`,
  `ellipse`, `polygon`, `hatch`, `crosshatch`, `filled_polygon`, `stipple`, `spiral`, `flow_field`.
- **FREEFORM** — organic/expressive marks: `contour_path`/`silhouette_outline`, `texture_strokes`,
  `accent_marks`, `hatch_region`, `negative_space_region`, and abstract fields (`field_stack`,
  `moire_grid`, `radial_field`, etc.).
- Raw `G0`/`G1` GCode dicts for anything the DSL doesn't cover.

`expand_primitives(draw_program, pen_config)` turns a DrawProgram into a `GCodeProgram`.
Primitive/freeform **schemas are introspected from function signatures** and injected into the
prompt (`get_all_primitive_schemas`, `format_schemas_for_prompt` in `primitives.py`) — adding a
new primitive means writing an `expand_*` function and registering it; the prompt updates itself.
`llm.classify_creative_mode(prompt)` routes to **figurative / abstract / hybrid** prompt variants.

**Claude-Code-as-LLM path**: hand-build `blocks` of PRIMITIVE/FREEFORM dicts and call
`orchestrate.compose_and_stream(blocks, plotter, config)` — expand → merge → postprocess → stream,
with no intermediate `.gcode` file. See `scripts/cc_draw_*.py` for working examples.

## BAUHAUS UNIVERSUM (collection)
`generative/bauhaus.py` — a design-language kit (serpentine/spiral/quarter fills, dotted
orbits, plus marks, swatch bars, crosshair rules, spaced-caps `type_block`/`scale_footer`,
`BAUHAUS_PALETTE` blue|pink|black) plus poster pieces built on it: `bauhaus_attractor`
(SENSITIVE DEPENDENCE — one Lorenz line, solid discs in the lobe eyes), `bauhaus_attention`
(GPT-2 sink chords in bold pink), `bauhaus_weights` (PARAMETER FIELD — Q|K|V Hinton discs
from the trained checkpoint), `bauhaus_gradient`
(WATERSHED — gradient descent as a basin of attraction: the whole plane raining downhill via
exact RK4 on an analytic 2-Gaussian loss into two sinks, the separatrix left as blank paper,
one blue heavy-ball-momentum channel overshooting the deep sink and ringing back; APPROVED;
params `fill_spacing` (sink-disc spiral pitch — set > pen tip, e.g. 3mm for a 2mm POSCA), `sink_scale`
(enlarge the sinks so a coarse spiral still fills them), `min_sep` (streamline separation)),
`bauhaus_resonance` (harmonograph),
`bauhaus_loom` (FORWARD PASS — the perceptron rethought as an Anni-Albers weaving: a real
weight matrix woven warp/weft, over/under by sign, float by magnitude; APPROVED),
`bauhaus_decision` (DECISION SURFACE — the network drawn as its FUNCTION not its wiring: the
exact iso-0 marching-squares knife through input space, ±margin shoulders opening a corridor,
support-vector discs on the shoulders, point clouds coloured by the true sign of f; trained
query directions from the checkpoint drive the readout when `weights=` is given; APPROVED),
`bauhaus_warped_frame` (WARPED FRAME — gravity is the grid: a straight Bauhaus lattice bent by
an exact closed-form Schwarzschild point-lens around an unpainted void, one loud pink photon
ring at b=3√3·M; a fresh, disk-less black hole distinct from `black_hole_bauhaus`).
Retired: `bauhaus_perceptron` and `bauhaus_gradient_v1` (kept in-file for version history,
deregistered — superseded by the loom+decision and WATERSHED reworks).
Related one-off: `black_hole_bauhaus`. Renders go to ~/Downloads for voting; winners move
to `leo/bauhaus/`.

### Abstract neural-net series (3D pen-plotter engine)
A sub-series of "abstract neural representations for penplotters" (fine-line, black+red on
cream, +blue/green where a piece needs it): `bauhaus_locality` (CNN — stacked feature-map
terrains, pixels→meaning), `bauhaus_memory` (LSTM — precessing figure-8 helix connecting
INPUT·LATENT·OUTPUT), `bauhaus_relevance` (TRANSFORMER — ATTENTION AS TOPOGRAPHY: QKᵀ cones →
softmax contours → V green → O), `bauhaus_manifold` (MLP — a folded petal-saddle; 3 pens: surface
mesh + INPUT/OUTPUT planes on slot 0 (fine 0.1 pen), red fold-ridges/flow on slot 1, the rest black
on slot 2; text labels use a **halo** — the mesh/streamlines/dots skip a box around each label so it
stays legible over the busy surface — and a final uniform fit-transform scales the whole composition
into the drawable area, so it is paper-size-agnostic. **Adaptive-density policies** (the anti-crowding
engine decisions, all structural): polar LOD — radials thin toward the pole in halving levels and the
finest level exists only on the open outer band; per-sample screen-space thinning in BOTH grid
directions with a 2× coarser floor on the far (lowest-depth) half; streamlines keep `stream_sep` mm
separation at generation and PAUSE-AND-RESUME through congested stretches instead of dying; red
streamlines cross-register against red fold-ridges so same-color lines never shadow; `mesh_weave>0`
optionally alternates ring/radial leadership in checkerboard patches). ALL of these are now SHORT DECLARATIONS on the Scene3D engine (see `engine/`) — the piece
builds fields/labels/pens, the engine renders with native anti-crowding. Current line-up:
`bauhaus_relevance` = the isometric DIAMOND STACK (QUERY+KEY wells → DOT PRODUCT similarity →
SOFTMAX rings → red VALUES terrain → green OUTPUT peak, dashed Q/K droplines);
`bauhaus_memory` = the precessing FIGURE-8 (REMEMBER/FORGET lobes, engine pause-resume keeps the
waist and rims clean); `lstm_gates` = the gate-mandala sibling (CELL STATE hub, four gate discs
with 0→1 sliders, log-spiral bundles); `bauhaus_locality` = CNN terrains with sparse-dash
receptive-field rails. These share
a from-scratch **3D engine**: `_zbuf_terrain(out, SX, SY, DEP, feed, PENV=, pen=)` rasterizes
surface quads into a numpy z-buffer for **true hidden-line occlusion** and draws only visible
mesh (near ridges hide far → solid surfaces); build `SX/SY/DEP` via an isometric `proj`+`dep`
and a per-piece height field. Per-architecture design briefs (built + to-build: GAN, diffusion,
VAE, GNN, MoE, SSM/Mamba, flow-matching, ViT, DINO, RL) live in `studio/nets/*.md` with the
shared conventions in `studio/nets/README.md`.

## Multi-color pen layers
Every drawing source (LLM, manual scripts, generative, imported files) can tag commands with a
`color` index. When `config.color.enabled`, `postprocess.reorder_by_color` groups strokes by pen and
optimizes **within** each color (never reordering across a color). `orchestrate.stream_pen_layers`
then streams color-by-color: after each layer it lifts, parks at `config.color.park_position`, and
(if `pause_for_swap`) blocks for a keypress before the next pen. `visualizer` renders each pen in its
palette color with a legend. Color sources: `draw --colors N` (LLM assigns), `art --colors K`,
`import` (SVG stroke / DXF layer), or hand-tagged `GCodeCommand(color=…)` in a script (see
`scripts/cc_colors_test.py`). Color survives a save→reload round-trip as a `; color=N` comment.

## Generative art (seeded)
`promptplot art <generator> --seed N|now --colors K --paper a4 --simulate --preview`. Fully
**deterministic**: same seed + params + version → identical GCode (all randomness flows through one
`SeededRNG`; no global random). `--seed now` uses a timestamp seed that is printed and embedded in the
output filename for later reproduction. Generators live in `generative/generators.py` and are registered
in `generative/registry.py` (`GENERATOR_REGISTRY`); param schemas are introspected from signatures, so
adding a generator + registering it updates `art --list` automatically — mirrors the primitives pattern.
Generators: `tiled_field` (dense directional-tile grid), `ripple_field` (concentric ripples → noise
peaks), `flow_field` (evenly-spaced non-overlapping streamlines, Jobard–Lefebvre), `maze`, `truchet`,
`wave_bands`, `stipple`, `waves_with_circles`, `crosshatch_weave` (±45° woven plaid, black-dominant),
`turning_weave` (grid-aligned diagonal L-paths that enter an edge, turn at lattice nodes, exit another edge; single-pass ink — a lane registry gives each lattice hop tiered offset lanes so shared diagonals become tight parallel bundles instead of stacked/overdrawn lines; `lane_gap` sets the offset),
`wave_gradient` (rows of waves, calm at top → tall spiky peaks at bottom),
`interference_field` (scanlines displaced by interfering circular ripples from N seeded 'drops' — ripple-tank/moiré; frequency varies within each wave),
`frequency_lens` (rows of sine with circular 'lenses' where the local frequency drops — phase-integrated so waves stay continuous across the edge),
`hitomezashi` (Japanese stitch grid — emergent staircase mazes from seeded binary offsets),
`harmonograph` (one continuous damped double-pendulum curve),
`vortex_field` (scanlines swirled around seeded whirlpool centers),
`moire_layers` (same line grid per pen at tiny rotations — physical moiré on paper),
`strange_attractor` (lorenz/rossler/halvorsen/aizawa, RK4, ported from `008-formCollapse` — 'controlled chaos'),
`domain_warp` (scanlines through warped fbm — liquid marble),
`contour_field` (marching-squares topographic isolines of noise/blobs/ridge fields),
`superformula_bloom` (nested rotating superformula shells — botanical mandala),
`lissajous_carpet` (the classic Lissajous frequency table as a grid of curve cells),
`scribble_halftone` / `line_halftone` / `scribble_portrait` (image-driven: photo tones → dashes / line-screen / continuous scribble; `--param image=path`, Pillow via the `vision` extra; procedural fbm fallback without an image).
Image fit rule: pictures **cover-fit** the drawable area — auto-rotated 90° to match the paper's orientation, filling everything inside the margins, center-cropping overflow (`_image_tone_grid`).
`scribble_halftone` is **shape-aware** by default: dash direction follows the image's contour tangents (Sobel + structure tensor), blends into a noise field in flat tone, cross-hatches darks. `line_halftone` plays with effective pen width (dark runs drawn as doubled/tripled parallel passes). `scribble_portrait` leaves highlights as blank paper (steep capacity curve).
`comic_panels` (seeded comic-page layout, max 3 panels, default pool vortex+contours; `subs` overrides),
`sparkle_grid` (mid-century atomic stars on a STRICT grid; tight shells (`shell_gap`), slim arms (`slim` exponent), per-gridline interval registry keeps spur arms from overlapping ink; tip relief avoids pooling),
`iso_city` (voxel city, unit-gridded faces, hidden lines removed via front-to-back occupancy-mask claiming; `projection=2pt|1pt|iso` — real vanishing-point perspective by default, `persp` controls strength),
`rounded_circuits` (guillotine regions filled with serpentine conveyor-belt bands — parallel lines snaking through rounded U-turns, pink/blue interlock),
`lissajous_swarm` (phase-swept Lissajous family — sheared 3D tube/butterfly moiré; near-camera curves double-pass for depth thickness),
`black_hole` (Luminet 1979 — EXACT elliptic-integral solver verified against bgmeulem/luminet at machine precision: direct + n=1 ghost images, near-side ellipse fallback, flux-binned pens in lines mode, photographic-plate `mode=dots` with hot/inferno pen palettes, `mode=flow` — flux-duty dashes riding the lensed isoradials with screen-space stroke spacing (`flow_spacing` mm) and variable dash lengths, photon ring double-passed in every mode),
`pe_carpet` (sinusoidal positional-encoding matrix as a waveform carpet),
`attention_arcs` (attention as a score of arcs: pen per head, ink passes ∝ weight; `weights=ckpt.keras` uses trained Q/K via h5py, `attn_npz=...` uses real GPT-2 attention — extract with `scripts/extract_gpt2_attention.py`),
`residual_river` (transformer residual stream: channel lines weave at attention stations, band expands through FFN lenses, skip arcs per block).
Picture generators accept ANY photo: `--param channels=cmyk` splits a color image into cyan/magenta/yellow/black pen passes (Golden-Gate-style multicolor portraits).
`rounded_circuits` is ONE closed self-crossing belt with concentric constant-offset lines and big round turns. `iso_city` defaults to terraced plateau masses (fill/void space) with window details, cover-fit immersion (`zoom`, `height`, `lod`).
The `--anaglyph` glitch defaults to 4 pens (cyan/red/yellow/black); `--max-ink N --max-ink-cell MM` caps pen passes per spot on any generator.
`strange_attractor` systems (formCollapse catalog; divergent variants replaced with classical dynamics): lorenz, rossler, halvorsen, aizawa, rabinovich_fabrikant, chen, newton_leipnik, burke_shaw, finance, three_scroll, qi.
Effects (`generative/effects.py`, all seeded, apply to ANY generator): `anaglyph_layers` (`--anaglyph [--anaglyph-offset MM] [--glitch N]` red/cyan offset), `echo_layers` (`--echo N [--echo-wobble MM]` — redraw the whole piece N times, one pen each, per-copy drift + hand wobble: the POSCA misregistered-multiples look), `dash_rain` (`--dash-rain [--dash-rain-near MM]` — vertical dashes fill negative space, near-halo pen vs far pen, never touching the ink), `occlude_crossings` (`--occlude MM` — cut a gap where a lower pen crosses a higher pen, faking marker opacity; only cuts between DIFFERENT pens, so run it after echo/glitch), `glitch_slice` (`--glitch-slice [--glitch-slice-bands N]` — Rick-style horizontal tear bands + chromatic outline copies + speed-dashes), and `limit_ink_density` (`--max-ink N --max-ink-cell MM`).
Overlap guardrail (ON by default in `art`): with no `--max-ink`, the pipeline applies `limit_ink_density(max_passes=1, cell=config.pen.tip_width)` so no spot is inked twice within the pen tip — protects paper and stops attractor/harmonograph loop saturation. Override the tip with `--pen-tip MM` (0 disables).
Custom paper: `--paper WxH` on `art`/`draw`/`import` (`17x24` read as cm → 170×240 mm, `170x240` as mm) in addition to a3/a4/a5/a6; `PaperConfig.from_size` parses both.
Paper safety: `harmonograph`/`strange_attractor` have an `overdraw` cap (default 6 hits per 0.8mm cell) so converging lines can't chew through the paper.
`art --port …` streams Leo-ready: heartbeat off + mandatory pen-up limits trace before inking.

### Streaming guardrails (safety, in `orchestrate.py`, all regression-tested)
Three defenses make single-layer / per-pen streaming safe through ANY path — never hand-roll around them:
- `split_color_layers` keeps each colour layer's pen-up positioning travel attached to it, so streaming one layer alone can't drop the pen at home and drag to the first stroke.
- `stream_pen_layers` lifts + rapids to each layer's first drawn point (`_first_drawn_point`) before drawing.
- `stream_chunk(enforce_pen_state=True)` tracks pen state and injects the missing `M5`/`M3` (+settle dwell) so a `G0` travel is never inked and a `G1` draw never floats. **The pen convention is load-bearing: `G0`=travel(pen up), `G1`=draw(pen down); never emit `G1` for a pen-up move.**

## File import (SVG/DXF)
`promptplot import file.svg|file.dxf --group-by color|layer|auto --paper a4 --simulate --preview`.
`importers/svg_import.py` groups by SVG stroke color; `importers/dxf_import.py` groups by DXF layer.
Both ship **stdlib parsers** (work with no extra deps) and use `svgpathtools`/`ezdxf` for full
curve/entity fidelity when the `io` extra is installed (`pip install -e ".[io]"`). `importers/layers.py`
fits paths into the drawable area (uniform scale, centered, SVG Y flipped) and emits color-tagged strokes
that flow through the same color-layer pipeline.

## State management
- **PenState** — tracks pen up/down, validates commands (G0 requires UP, G1 requires DOWN), used across postprocess, workflow, and plotter
- **Phase transitions** — validated state machine: IDLE → PLANNING → GENERATING → STREAMING ↔ PAUSED → DONE. Invalid transitions raise `IllegalTransitionError`.
- **Connection SM** — plotter connection lifecycle: DISCONNECTED → CONNECTING → IDLE → STREAMING. Handles ALARM detection and recovery.
- **Checkpoints** — interrupted drawings save state to `~/.promptplot/checkpoints/`. Resume with `--resume`.

## Gallery and feedback

Every render and GCode this project has made lives in `gallery/` — 63 drawings, 578 files,
**entirely gitignored** (it is ~400 MB of images). It is a local working archive; Claude Code
reads the filesystem, so nothing is lost by not tracking it.

```
gallery/
  INDEX.md      every subject and file, with per-file plot stats — for curating
  PRINT.md      everything plottable, cheapest first — for picking a job for Leo
  viewer.html   the browser: a hero carousel over a filmstrip of that drawing's trials
  <series>/     neural-networks · physics · generative · attractors · pictures · effects
  studio/<fam>/ current/  the latest version        trials/  every earlier attempt
```

Regenerate all three views with `python scripts/gallery_index.py`. Pull new renders out of
`~/Downloads` with `python scripts/studio_sync.py` (files each
render under its PLATE, thesis as a variant, latest per thesis in `current/`; `--min-age 30`
makes it safe while agents render — it never overwrites and rewrites Downloads paths in studio
notes; `--copy --only <plates>` previews a batch; `--fix-refs` repairs stale Downloads paths) — Downloads is staging, the gallery is the
archive.

**NEW renders** (computed in the viewer from file mtime vs `studio/feedback.jsonl`): a render
stays NEW until a verdict on its drawing is recorded after it, on it or on a newer render. A drawing
never judged uses Juan's last verdict anywhere, frozen at page load. Viewing never clears NEW.
Header **New · N** filters to NEW only, `n` jumps to the next one, and the page opens on the first.

### Don't break the studio pieces

The 51 candidate pieces under `studio/<slug>/rounds/<rN>/piece.py` live OUTSIDE the package
and are not in `GENERATOR_REGISTRY`, so `make test` never touches them — yet they import
`engine.geometry`, `engine.kit`, `engine.policies` and the private helpers `_poly`, `_dot`,
`_stroke_text`, `_text_width`, `_chain_segments` from `generators.py`. An edit to any of
those can change an approved plate with nothing going red.

```
python scripts/studio_regression.py            # compare against the baseline
python scripts/studio_regression.py --write    # re-record it (only when the change is intended)
```

**`rounds/r00/` is a FROZEN ORIGINAL** restored from history (LSTM helix, manifold fold
braid, composition-nothing v2 — each verified identical to its gallery render); never edit
one, new versions go in r01+. Re-render with `scripts/render_candidate.py ... --margin 15`
(those three were drawn at a 15 mm margin; `--margin` defaults to the paper config's 10).

Each piece is fingerprinted by command count, draw/travel length, pens and a hash of every
coordinate, so any geometry change shows up even when the totals match. Baseline:
`studio/REGRESSION.json`. **Run it after touching anything under `generative/engine/` or
`generators.py`.**

### Juan's feedback — READ THIS BEFORE CHANGING ANY PIECE

Juan reviews plates in the viewer and records a verdict plus a note. **Those notes are
instructions, and they live in tracked files under `studio/`** (not in `gallery/`, which is
gitignored and would lose them):

| file | what it is |
|---|---|
| `studio/<slug>/FEEDBACK.md` | **the one to read before working on that drawing** — every judgement on it, newest first, and the source file to edit |
| `studio/FEEDBACK.md` | the roll-up across all drawings, in `CURATION.md`'s column shape |
| `studio/QUEUE.md` | open reworks — the worklist agents get dispatched against |
| `studio/feedback.jsonl` | the append-only log the three views are generated from |

**Before you touch a piece, read its `studio/<slug>/FEEDBACK.md` if one exists.** It names the
exact render Juan was looking at, what he wants changed, and any other plates he referenced
with `@`. Treat a REWORK note the same way you would treat a brief.

Render verdicts (keys 1–5 in the viewer; save at once and jump to the next undecided render),
mapped to `promptplot/generative/CURATION.md`'s vocabulary:

- **PROMOTE** (= CURATION's KEEP) — this is the final version of that drawing
- **KEEP** (= FLAVOUR) — good, keep it as a flavour; *not* CURATION's KEEP
- **REWORK** (= REWORK) — good bones, fix what the note says
- **ARCHIVE** (= PARKED) — not now: `gallery_apply` moves it to `archive/`, hidden unless
  "show archived"; a later KEEP/REWORK restores it
- **CUT** (= KILL) — drop it (`cut/`, never deleted)

**Direction verdicts** judge the approach behind a set of renders — a direction is keyed by its
root round (`r02`, `original`, a wildcard's round, or `x-<variant>` without a ledger), parsed from
the LEDGERs by `scripts/gallery_directions.py` (`--audit` prints them): **WORKS / MAYBE / DEAD
END** (keys `w`/`m`/`d`). They are stored as their own scope (target
`<subject>/@direction/<key>`), never clear NEW, open each `studio/<slug>/FEEDBACK.md` as a
Directions table with "rounds not to fork from", roll up in `studio/DIRECTIONS.md`, and **steer
the studio**: `studio_descriptions.py --json` drops dead-end theses and lists `avoid_parents`,
the workflow refuses a dead-end/archived/cut parent, and the lead and designer agents obey them.

**Publish verdicts** pick the plates that go to Juan's portfolio site: **PUBLISH / UNPUBLISH**
(the "Publish to site" toggle or `p`; only a render with its gcode beside it). Their own scope,
target `<subject>/@publish/<basename>`, field `basename`; `gallery_feedback.latest_published()`
(newest per plate, an unpublish removes it) is what the site exporter reads. They never move a
file, never clear NEW and never appear in the markdown views. Status filter "published"; a
magenta rail dot marks a published render.

`scripts/prints_render.py` turns a published plate's gcode into site renders — pure
functions, no gallery globals: `parse_header` (the `; promptplot render` provenance block),
`parse_polylines` (pen → polylines), `write_svg` (clean vector sheet, one `<path>` per pen, no
background — the site supplies cream paper), `write_thumb`/`write_raster` (anti-aliased WebP on
cream), `write_technical` (1:1 mm plate: mm axes + legend with the real pen colours, none of the
preview's title/stats/travel chrome), `write_photo`. Deterministic, so outputs compare byte-exact.

Viewer keys: `1–5` verdict · `w m d` direction · `p` publish · `z` back to the last judged · `n` next NEW ·
`s` **swipe mode** (a full-screen card deck of undecided renders, newest first: → keep ·
← archive · ↑ promote · ↓ rework + note · `x` cut · space skip · `z` undo · `p` publish · Esc back);
Cmd/Ctrl/Alt never record anything. Filters: status, direction verdict, series, NEW, show
archived; `#p=<path>` deep links. **`gallery/board.html`** is the directions board: a row per
plate, a card per direction (latest render, canon/order/lineage chips, best critic scores,
verdict tallies, W/M/D), and a patterns strip counting WORKS/DEAD END by canon and by order
(`order_norm`: the twelve non-circular orders or "circular"). `python scripts/gallery_index.py`
reuses cached hashes/stats (seconds; `--full` recomputes, `--views-only` rewrites only the two
pages).

To review: `python scripts/gallery_serve.py` opens the viewer on localhost and saves feedback
straight to disk. The viewer's **Plot** panel can also send the plate on screen to the machine
— it lists the gcode's colour layers, traces the frame and streams one layer at a time:

```
python scripts/gallery_serve.py --allow-plot --paper a5:landscape \
    --serial-port /dev/cu.usbserial-14120
```

**Plot plate** runs the whole plate as one job (the same `promptplot/plotjob.py` engine as
`promptplot plot plate`): it traces the frame first, then per layer parks at (0,0) and waits
for **Continue** (pen swap), streams batches of `batch_strokes`, parks for a re-zero check
every `rezero_every` strokes, and rewrites `~/.promptplot/plot_jobs/<id>.json` after every
batch. Endpoints: `POST /plotter/job {action: "plate", target, layers?, batch_strokes?,
rezero_every?, max_feed?, min_dwell?, confirm}`, `POST /plotter/continue {wait_seq}` (must
name the wait on screen), `POST /plotter/pause` (stop at the batch boundary, resumable),
`POST /plotter/resume {job_id, retrace?, confirm}`, `GET /plotter/jobs`; `GET /plotter/state`
adds `waiting_for`, `cursor`, `progress`, `eta_min`. One job owns the port (an `flock` shared
with the terminal command). Built/not-built and the saturation argument: `studio/PLOT_JOBS.md`
(queue + sort-by-cost are still planned).

Plotting is **off unless `--allow-plot` is passed**, every request must carry `confirm: true`,
the target must resolve inside `gallery/` and end in `.gcode`, the layer is bounds-checked
before a command goes out, and **the pen-up frame trace is enforced by the server, not by
convention** — an ink job is refused until a frame has been traced for that paper *in this
process* (`promptplot plot frame` in another terminal does not satisfy it). Endpoints live in
`scripts/gallery_plotter.py`; `promptplot` is imported lazily so the server still runs on a
bare interpreter. Opened as a plain `file://` page it still browses, but a `file://` page
cannot write, so saving there falls back to the clipboard.

Verdicts only *record* a decision — nothing moves until
`python scripts/gallery_apply.py --dry-run` is checked and re-run without the flag. PROMOTE,
ARCHIVE and CUT move files (`current`/`promoted`, `archive/`, `cut/`), KEEP/REWORK restore a
parked one; nothing is ever deleted, every move is appended to `MOVES.tsv` and is reversible,
and studio notes are repointed to the new paths. `studio_sync` never resurrects a parked render.

## Authored scenes — how a reference picture becomes a plotted drawing

The three reference reconstructions ChatGPT made (cubist plate · Dalí engraving · acrylic
Van Gogh) are the bar, and their packages are our oracles in
`gallery/references/oracles/` (gitignored; read-only; never import their code). The
method they used is now native here. **It is an illustrator's reconstruction, never a
trace** — see `studio/AUTHORING.md` (the playbook) and `DESIGN_RUBRIC.md` § TRACING IS
NOT AUTHORING + § MATERIAL GRAMMAR.

**The model** — `promptplot/scene/` (`models.py`): a `Scene` is an ordered list of named
`SceneObject`s, **back to front**, each with an occlusion `cover` polygon (source units,
never drawn), a `material`, and `Mark`s that carry a `role`
(contour|hatch|label|flow|construction|accent), an `ink`, a physical `width_mm` (nib OR
brush footprint) and a `stage`. Pen work has one stage; acrylic has
`underpainting → body → accents`. `name` is functional — ink/width rules key on it.

**The compiler** — `compile_scene(scene, config) -> (commands, pen_plan)` and
`compile_to_program(...) -> (GCodeProgram, pen_plan)`: occlusion → source units to mm
(uniform fit, centred, y flipped) → width snapped to the nearest available nib/brush →
exact dedup (widest wins) → passes ordered `(stage, width asc, ink)` → one colour index
per pass → normal colour-layer pipeline. The pen plan says what each index physically is.
Two occlusion modes: `cover` (pen — a hatch stops ON the facet edge in front of it, via
`geometry.Polygon`) and `paint` (brush — later footprints hide earlier strokes;
fully-hidden strokes are culled). Unused ink×width combinations never produce empty layers.

**Two seats, one engine.** (1) In-app: `promptplot studio design <slug> --mode scene
--reference img.png` — the designer LLM (any of the 7 providers) *sees* the reference and
emits Scene JSON; the critic sees reference + render side by side and runs the seven
acceptance questions. A reference at `studio/<slug>/ref/reference.png` is picked up
automatically. (2) Claude Code in conversation: author the Scene JSON directly and compile
it — same engine, same pen plan. `code` mode still exists for pieces needing bespoke
computation (THE MIRROR FORGETS). Previews draw each pass at its physical width
(`GCodeVisualizer.preview(pen_widths=)`) so a 4 mm underpainting reads as paint.

**Engine additions for this:** `geometry.Polygon` (concave-capable exact Region),
`bezier_flatten` (the oracles are 80k+ cubic segments — the SVG importer now flattens
them instead of chording), `resample_by_arclength`. SVG import is **mm-native** with
`--no-fit` when the file declares a viewBox + physical width (the three oracle SVGs land at
exact `[0,297]×[0,420]` with 7,118 / 24,678 / 11,163 paths and 8 / 4 / 32 layers).

## File structure
All source lives in `promptplot/`. Three formerly-monolithic modules are now **subpackages** whose
`__init__.py` re-exports the same public names (so `from promptplot.llm import X` etc. are unchanged):
- `llm/` — `base.py` (LLMProvider ABC, errors), `providers.py` (7 providers + `create_llm_provider`/`get_llm_provider`), `prompts.py` (all `build_*_prompt`, `classify_creative_mode`, presets, few-shot, palette color block).
- `workflow/` — `events.py`, `_shared.py` (helpers + `diagnose_failure` + console/logger), `batch.py`, `supervisor.py`, `streaming.py`, `livedraw.py`.
- `cli/` — `_group.py` (the `cli` click group + `main` + `_get_config`/`_print_score`), `draw.py`, `generate.py`, `art.py`, `import_cmd.py`, `manage.py` (config/plotter/interactive/ui/library). `__main__.py` enables `python -m promptplot`.
- `generative/` — `rng.py` (`SeededRNG`: seeded Random + numpy + value/fbm noise), `generators.py` (30+ parametric generators), `registry.py` (`GENERATOR_REGISTRY` + signature-introspected schemas + `run_generator`), **`engine/`** (THE composition engine — `scene3d.py`: `Scene3D` builder with native default-ON anti-crowding — z-buffer hidden-line `surface()` w/ `ScreenThin` (depth-aware both-family floors, weave) + `PolarLOD` (spider-web polar meshing, ridge registration), `Occupancy` + `lines(mode="pause_resume")` crowd control, `halo_labels`, `poly/emit`, `fit="fill"|"rescue"|"none"`, `prime_scale`; plus `geometry.py` (moved), `kit.py` (moved), `policies.py` (occlude_crossings, enforce_line_spacing, focal_void, limit_ink_density), `looks.py` (anaglyph, echo, dash_rain, glitch_slice); old paths `engine3d.py`/`kit.py`/`geometry.py`/`effects.py` are compat shims, single def-sites in `engine/`; pieces are SHORT declarations on Scene3D — never hand-roll z-buffers/thinning in a piece), **`engine3d.py`** (compat wrapper: `_zbuf_terrain` = Scene3D exact mode + `_fit_out`), **`geometry.py`** (exact 2D diagram ops, FreeCAD-vocabulary: composable `Region`s — `Circle`/`HalfPlane`/`Band`/`Rect` with `|`/`&`/`~` — plus `clip(poly, region, keep='outside'|'inside')`, `trim_to`, `offset`; segment↔boundary intersections are closed-form so clipped curves stop exactly ON lines/circles, no sample-snap stagger — use this instead of hand-rolled `hidden=` conditionals; adoption roadmap for more CAD ops in `studio/engine/CAD_RESEARCH.md`), **`kit.py`** (the 2D design kit: fills, type, furniture, clipping — one import site incl. generators low-level helpers), **`pieces/{ml,abstract,physics}.py`** (the science compositions by domain; `bauhaus.py` + `physics.py` are compat shims re-exporting every historical name — the framework is style-NEUTRAL, style is chosen at the lamina level; new pieces get subject-based names, `bauhaus_*` is legacy). See "Generative art".
- `lamina/` — **the finished-sheet layer.** `styles.py` (6 `StylePreset`s from STYLES.md: bauhaus, swiss, deco, pop, radial_viz, science_poster; semantic-pen → physical-pen mapping), `layout.py` (`reserve_bands`, `split_panels`, gutter rules, number chips), `plate.py` (`Panel`, `PlateSpec` + JSON round-trip, `compose_plate(spec, config) -> (GCodeProgram, pen_plan)`). CLI: `promptplot plate cnn:7 lstm:7 mlp:7 --style science_poster --paper a3` (single- or multi-panel; `--preview/--save/--simulate/--port` with the mandatory limits trace).
- `studio/` (package) — **the native design layer.** `briefs.py` (parses `studio/<domain>/*.md` briefs: title—tagline, Essence/Status, sections), `prompts.py` (designer/critic/synth templates inlining the STYLES.md canon + DESIGN_RUBRIC.md), `loop.py` (`run_design_loop`: designer → render → vision-critic → synth on any of the 7 LLM providers; `params` mode renders existing pieces, `code` mode writes candidate piece source under `studio/<slug>/rounds/` — never inside the package). CLI: `promptplot studio list | brief <slug> | design <slug> --style --mode --rounds --provider`. **New pieces should go through this loop** — it consistently outperforms one-shot design.
- `scene/` — **the authored-scene layer** (see "Authored scenes"). `models.py` (`Scene`/`SceneObject`/`Mark`/`HatchRule`, pydantic, JSON round-trip — what an LLM emits in scene mode; an object's `fills` are `HatchRule`s the compiler expands over its `cover`), `occlusion.py` (`cover_walk` exact reverse-walk hidden-line removal with label protection; `paint_walk` footprint-raster culling for brushwork), `compile.py` (`compile_scene` → colour-tagged commands + pen plan; `compile_to_program`; `rules=` accepts `lamina.styles.PenRules.as_compile_rules()`).
- `generative/engine/` — **the drawing engine, in layers** (innermost first; each uses only the ones above it, and `engine/__init__` re-exports all of it from one import site):
  `geometry.py` exact 2D kernel (Region algebra + `clip`/`trim_to`, `offset`/`erode_ring` with miter-or-smooth joins and fold pruning, `bezier_flatten`, `resample_by_arclength`, `smooth_ring`) · `forms.py` **what the shapes are** · `material.py` **how a mark is made** · `kit.py` 2D furniture and type · `policies.py` guardrails · `looks.py` sheet effects · `scene3d.py` 3D composition with z-buffer hidden-line. `promptplot/scene/` sits above as the 2D authored-scene layer.
- `generative/engine/forms.py` — **the form vocabulary**: the closed shapes technical plates are built from. Rings (`lobed_ring`, `hourglass_ring`, `funnel_ring`, `rounded_rect_ring`) and **three nesting rules that are not interchangeable**. **`field_nest` is the default and the only one that holds a constant PHYSICAL gap**: it walks level sets of the shape's distance field, where `|grad d| = 1` makes every level exactly `pitch` from the last, in every direction, all the way to the medial axis — so it neither folds nor leaves a hollow centre, and a pinched mass splits into components on its own. `pitch` is in caller units; set it above the pen tip or the mass inks solid. The other two are kept for the cases they suit and **must not be used for a filled contour mass**: `contour_nest` offsets inward (exact gap, but dies at the tightest valley — measured 0.32 mm minimum where it folds), and `radial_nest` scales about the centroid (never folds, but the gap runs with the local radius — measured 1.9x across a 4-lobe blob, and 0.66 mm minimum at 26 rings, which is what turned the v3 latent-topography masses into black blots). `max_erode` measures a shape's real offset limit by bisection. Plus `dissolve` (a nest walked from solid contours → broken → dots → scatter: the diffusion forward process as one drawing op), `dot_cloud`, `radial_burst`, `ribbon`.
- `generative/engine/material.py` — **how a MARK is made, per material** (the layer the engine lacked; algorithms + constants from the reference reconstructions, on exact `geometry` Regions, no shapely). Cubist: `hatch_polygon` (exact clip, grid phase-locked to the origin so adjacent facets stay collinear), `physical_spacing` (floor 2.4 × finest nib), `physical_inset` (½ border + ½ hatch + 0.035 mm), `shadow_cross` (+67°, ×1.5). Engraving: `cut_tone` (tone → arc-length duty cycle: `(t−0.06)/0.65`, ink floor 0.13, solid at 0.71), `flow_family` (two guides → tracks; count = 76th-percentile width ÷ spacing; travelling highlight σ 0.026; `dark_edge` rims; `count=` override), `surface_grid` (warped (u,v) net `bend·sin(πu)sin(πv) + slope·(u−½)`, golden-ratio row phase, cross family only in shadow, elliptical `protect` holes), `gauss_tone`. Painterly: `brush_family`, `load_image_grid` (cover-fit reference → per-cell RGB + tone + structure-tensor tangent/coherence), `quantize_palette` (median-cut, dark→light) + `snap_color`, `flow_strokes` (short curved strokes riding the tangent field, seeded on a jittered lattice so density is bounded, colour sampled then snapped). De-crowding: `suppress_parallel` (drop only if too close AND |cos θ| > 0.93 — crossings may touch). `lamina/styles.py` gained `PenRule`/`PenRules` (semantic name+role → ink, width; first match wins per list) and the `cubist_plate` preset carrying the oracle's `CUBIST_RULES`.
- `importers/` — `svg_import.py` (stdlib default: group-inherited stroke, Inkscape layers, Bezier via `bezier_flatten`, viewBox + physical units), `dxf_import.py`, `layers.py` (fit-to-paper + color/layer grouping; **mm-native passthrough** for `fit=False` when the page is declared), `__init__.py` (`import_file`, `parse_file`). See "File import".

Core flat modules:
- `config.py` — **Dataclass** config tree (paper, pen, brush, **color**, bounds, vision, serial, LLM, workflow). `ColorConfig` (palette, park_position, pause_for_swap, assign_mode) and `PaperConfig.from_size("a4")`. Not pydantic-BaseSettings and not `PROMPTPLOT_`-prefixed — LLM keys read direct env vars: `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `ANTHROPIC_API_KEY`, `GPT4_API_KEY`/`GPT4_ENDPOINT`/`GPT4_API_VERSION` (Azure). Don't "modernize" to the workspace env_prefix convention without being asked.
- `engine.py` — Workflow engine, PenState, Phase enum, validated transitions, DrawingSession
- `models.py` — Pydantic models: GCodeCommand (has a `color` field, emitted as a `; color=N` comment), GCodeProgram, DrawProgram/DrawCommand, PrimitiveCommand/FreeformCommand (carry a `color`), WorkflowResult, CompositionPlan (+figurative/abstract variants), Region, ChunkMetrics
- `primitives.py` — PRIMITIVE/FREEFORM registries and `expand_primitives` (propagates a block-level `color` onto emitted strokes); schemas introspected from `expand_*` signatures and injected into prompts (see "Drawing DSL")
- `orchestrate.py` — pure-function public API: `plan_regions`, `generate_region`, `validate_chunk`, `score_chunk`, `merge_chunks`, `stream_chunk`, `stream_pen_layers`/`split_color_layers` (multi-color), `load_and_continue`, `compose_and_stream`
- `pipeline.py` — FilePipeline: load .gcode → postprocess → preview → stream
- `plotter.py` — ConnectionState SM, BasePlotter ABC, SerialPlotter (ALARM/recovery/pause/resume), SimulatedPlotter
- `plotjob.py` — **plate jobs**: `build_plan` (colour runs → prepared, every layer bounds-checked up front), `PlateJob` + `JobStore` (`~/.promptplot/plot_jobs/<id>.json`, atomic, `flock` port lock), `JobControl`/`KeypressControl`/`AutoContinueControl`, `PlateJobRunner` (frame → park + swap wait → pen-up approach → batches via `stream_chunk` → re-zero waits → park; stop/pause/resume, abort on the first failed ack), the Leo ETA model. Used by `plot plate` and `scripts/gallery_plotter.py`. Never writes to the port itself — every line goes through `plotter.send_command`.
- `postprocess.py` — pipeline: arcs, bounds, pen safety, stroke optimization (or `reorder_by_color` when multi-color → per-color optimize, never across a color), dips, dwells; plus `validate_chunk`
- `checkpoint.py` — CheckpointManager for resumable drawings
- `visualizer.py` — matplotlib GCode renderer with stats; color-coded per-pen preview when a program has color layers
- `scoring.py` — Quality scorer (A–F grades), style profile extractor, `score_chunk`
- `memory.py` — Drawing memory (JSONL) for few-shot retrieval
- `tui.py` — Rich-based TUI with planning/paused phase display
- `logger.py` — Rich-based terminal output
- `__init__.py` — Public API exports (the stable surface for the `orchestrate`/`compose_and_stream` controller path)
- `scripts/` — standalone Claude-Code controller scripts (`cc_draw_*.py`, `cc_colors_test.py`, `cc_brush_test.py`, `cc_llm_stream.py`) using the `orchestrate` API directly against hardware

## Serial port
- macOS: `/dev/cu.usbserial-*` (e.g. `/dev/cu.usbserial-1420`)
- Linux: `/dev/ttyUSB0`
- Windows: `COM3`
