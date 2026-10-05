"""Prompt templates for the native studio loop (designer → critic → synth).

Each template inlines the governance canon — the chosen style's section from
``promptplot/generative/STYLES.md`` and the full ``DESIGN_RUBRIC.md`` — so the
loop enforces the same bar as the human-run studio. Scene mode also inlines
``studio/AUTHORING.md``, the reconstruction playbook. Replies must be a single
JSON object (parsed with the agent protocol's tolerant extractor).
"""

from __future__ import annotations

import re
from pathlib import Path

_GEN_DIR = Path(__file__).resolve().parents[1] / "generative"
_REPO_DIR = Path(__file__).resolve().parents[2]


def _read_doc(name: str) -> str:
    p = _GEN_DIR / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


def style_canon(style: str) -> str:
    """The one style's section from STYLES.md (falls back to the whole doc)."""
    text = _read_doc("STYLES.md")
    if not text:
        return ""
    pattern = rf"^##\s+\d+\.\s+.*{re.escape(style)}.*?$\n(.*?)(?=^##\s|\Z)"
    m = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
    return m.group(0) if m else text


def rubric() -> str:
    return _read_doc("DESIGN_RUBRIC.md")


def authoring() -> str:
    """The reconstruction playbook (studio/AUTHORING.md), inlined in scene mode."""
    p = _REPO_DIR / "studio" / "AUTHORING.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


DESIGNER_PROMPT = """You are a DESIGNER in the PromptPlot studio, designing for a REAL pen
plotter (lines only — no gradients, no fills except line-fills; tone = line density).

THE BRIEF:
{brief}
{reference_block}
STYLE CANON (obey it):
{style_canon}

DESIGN RUBRIC (you will be scored against this; pass = avg>=8, no dimension <7;
the no-schematics rule is absolute — draw the phenomenon, not the apparatus):
{rubric}

{mode_instructions}

{feedback}

Reply with EXACTLY ONE JSON object, nothing else:
{{"concept": "<one-paragraph concept>", "payload": {payload_schema}}}
"""

REFERENCE_BLOCK = """
A REFERENCE IMAGE is attached. You are reconstructing it as an authored plotter
drawing — an illustrator's interpretation, NOT a trace. Decide what makes it
recognisable, keep that, drop the rest. Coordinates you emit are in the source
canvas you declare.
"""

PARAMS_MODE_INSTRUCTIONS = """MODE: params. Propose a rendering of EXISTING registry pieces.
Available pieces and their parameter schemas:
{schemas}
Your payload selects piece(s), seeds, and parameter overrides to realize the brief."""

PARAMS_PAYLOAD_SCHEMA = (
    '{"panels": [{"generator": "<registry name>", "seed": <int>, '
    '"params": {"<param>": <value>}, "label": "<optional caption>"}], '
    '"title": "<spaced caps>", "subtitle": "<spaced caps>"}'
)

CODE_MODE_INSTRUCTIONS = """MODE: code. Write a NEW piece as one Python function
`def {fn_name}(rng, bounds, colors=3, feed=2200) -> list` following the house
conventions: all randomness via the passed SeededRNG; emit GCodeCommand lists via
the kit helpers (import from promptplot.generative.bauhaus: _poly, _pen, BLUE/PINK/BLACK,
fill_disc, circle, type_block, _stroke_text, _spaced, scale_footer, _zbuf_terrain for 3D). PREFER the Scene3D engine for anything 3D or line-family heavy: from promptplot.generative.engine import Scene3D, PolarLOD, ScreenThin — scene.surface(SX,SY,DEP, pens=..., lod=..., thin=...), scene.lines(families, mode='pause_resume'), scene.halo_labels([...]), return scene.render(); anti-crowding is native default-on.
Stay inside `bounds`; deterministic; black+red palette unless the brief says otherwise."""

CODE_PAYLOAD_SCHEMA = '{"function_name": "<name>", "source": "<complete python source>"}'

SCENE_MODE_INSTRUCTIONS = """MODE: scene. You author the DRAWING PLAN as a Scene; the engine
executes it (exact hidden-line removal by cover, mm mapping, nib snapping, pass order).

THE PLAYBOOK (follow its steps in order — inspect, plan depth, contours first, then material):
{authoring}

SCENE RULES
- `objects` are listed BACK TO FRONT. Order IS the occlusion order.
- Every object has a functional `name` (it drives ink/width rules), an optional
  `cover` polygon (its occluder, in source units, never drawn as a fill), a `material`,
  and `marks`. A mark is a polyline with a `role` (contour|hatch|label|flow|construction|accent).
- Declare `canvas` = [width, height] in your source units (y DOWN like an image),
  `inks` = {{name: hex}}, `widths_mm` = the physical nibs/brushes available, and
  `stages` (["main"] for pen work; ["underpainting","body","accents"] for paint).
- `occlusion`: "cover" for pen work (facets hide what is behind them), "paint" for
  brushwork (later strokes hide earlier ones), "none" to draw everything.
- Keep the total under ~{max_marks} marks in one reply. Contours and structure first;
  hatch only the planes that need tone; lit planes stay bare paper.
- Author lettering as `label` marks made of straight strokes in a 4x6 cell.
"""

SCENE_PAYLOAD_SCHEMA = (
    '{"canvas": [<w>, <h>], "paper": "a3", "orientation": "portrait", '
    '"inks": {"black": "#111111", "red": "#cb292a"}, "widths_mm": [0.1, 0.5], '
    '"stages": ["main"], "occlusion": "cover", "title": "<spaced caps>", '
    '"objects": [{"name": "<functional name>", "material": "<skin|hair|cloth|cubist_plane|stone|painterly|background>", '
    '"cover": [[x, y], ...] | null, "ink": "<ink name>", "width_mm": <mm>, "stage": "<stage>", '
    '"marks": [{"role": "contour|hatch|label|flow|construction|accent", "points": [[x, y], ...], '
    '"ink": "<optional>", "width_mm": <optional>}]}]}'
)

CRITIC_PROMPT = """You are the STUDIO CRITIC PANEL (art director + science critic) judging a
pen-plotter render against the brief and rubric. Be harsh.
{reference_block}
THE BRIEF:
{brief}

DESIGN RUBRIC:
{rubric}

Score all 7 dimensions 0-10 (pass = avg>=8 AND none <7). Apply the no-schematics
rule ruthlessly. Reply with EXACTLY ONE JSON object:
{{"scores": {{"hierarchy": n, "grid_alignment": n, "tension_asymmetry": n,
"negative_space": n, "pen_craft": n, "concept_legibility": n,
"depth_dimensionality": n}}, "verdict": "pass|revise|fail",
"top_fixes": ["..."], "one_line": "..."}}
"""

CRITIC_REFERENCE_BLOCK = """
TWO images are attached. The FIRST is the reference the designer was reconstructing;
the SECOND is the plotter render. Judge the render as an INTERPRETATION of the
reference, not a pixel match. Ask, explicitly:
1. Can the main forms be recognised without colour fills?
2. Do shadow lines follow the surface instead of forming a random mesh?
3. Are any fine lines really the two sides of one thick source stroke?
4. Are the blackest regions intended, or accidental hatch congestion?
5. Do labels stay readable at the real pen width?
6. Does a thicker pen create black knots at corners or fill eye highlights?
7. Are there long empty travels or excessive tiny marks with no visible benefit?
Put the failed questions, by number, at the front of `top_fixes`.
"""

CRITIC_RENDER_ONLY_BLOCK = """
The render is attached.
"""

SYNTH_PROMPT = """You are the STUDIO LEAD. Fold this critique into ONE concrete instruction
for the designer's next round (or declare the piece done).

CONCEPT: {concept}
CRITIQUE: {critique}

Reply with EXACTLY ONE JSON object:
{{"done": true|false, "instruction": "<the single most important change for the next round>"}}
"""
