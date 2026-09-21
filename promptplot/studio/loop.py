"""The native studio design loop: designer → render → critic → synth.

Provider-injected (any of PromptPlot's LLM providers; tests use a stub). Two
payload modes:

- ``params`` (default, safe): the designer proposes panels of EXISTING registry
  pieces (seeds + parameter overrides); the harness renders them.
- ``code`` (new-piece path): the designer emits one Python piece function; it is
  written under ``studio/<slug>/rounds/rNN/piece.py`` (never inside the
  package), imported from that file, and rendered. Promoting a winner into
  ``promptplot/generative`` is a separate, human-confirmed step.
- ``scene`` (authored-reconstruction path): the designer emits a ``Scene`` JSON —
  named objects back-to-front with covers, materials and marks — and the engine
  compiles it (``promptplot.scene``). The LLM authors WHAT to draw; the engine
  decides HOW. This is the seat that reproduces a reference image.

With a reference image (``reference=`` or ``studio/<slug>/ref/reference.png``)
the designer receives it and the critic judges the render against it.

Artifacts per round: ``studio/<slug>/rounds/rNN/{payload.json|piece.py|scene.json,
render.png, critique.json}``; the final state lands in
``studio/<slug>/final/PROPOSAL.md``.
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..agent.protocol import _extract_json
from ..config import PaperConfig, PromptPlotConfig
from ..generative import get_all_generator_schemas, run_generator
from ..orchestrate import merge_chunks
from .briefs import Brief, get_brief
from . import prompts as P

logger = logging.getLogger(__name__)


@dataclass
class RoundResult:
    index: int
    concept: str
    payload: Dict[str, Any]
    render_path: Optional[Path]
    critique: Dict[str, Any] = field(default_factory=dict)
    verdict: str = ""
    instruction: str = ""


@dataclass
class LoopResult:
    slug: str
    rounds: List[RoundResult]
    out_dir: Path
    final_verdict: str

    @property
    def best(self) -> Optional[RoundResult]:
        order = {"pass": 2, "revise": 1, "fail": 0, "": 0}
        return max(self.rounds, key=lambda r: order.get(r.verdict, 0)) if self.rounds else None


def _schemas_text(limit: int = 80) -> str:
    lines = []
    for s in get_all_generator_schemas()[:limit]:
        pstr = ", ".join(f"{k}={v}" for k, v in s["params"].items())
        lines.append(f"- {s['name']}: {s['doc']}  ({pstr})")
    return "\n".join(lines)


def _render_params_payload(payload: Dict[str, Any], config: PromptPlotConfig, out_png: Path) -> int:
    """Render a params-mode payload (panels of registry pieces) to a preview."""
    from ..visualizer import GCodeVisualizer

    panels = payload.get("panels") or []
    if not panels:
        raise ValueError("payload has no panels")
    bounds = config.paper.get_drawable_area()
    x0, y0, x1, y1 = bounds
    n = len(panels)
    gutter = 6.0
    pw = (x1 - x0 - gutter * (n - 1)) / n
    chunks = []
    for i, p in enumerate(panels):
        pb = (x0 + i * (pw + gutter), y0, x0 + i * (pw + gutter) + pw, y1)
        chunks.append(
            run_generator(
                str(p["generator"]), pb, int(p.get("seed", 7)),
                colors=len(config.color.palette) or 3, params=p.get("params") or {},
            )
        )
    prog = merge_chunks(chunks, config)
    GCodeVisualizer(config).preview(prog, str(out_png))
    return len(prog.commands)


def _render_code_payload(payload: Dict[str, Any], config: PromptPlotConfig, round_dir: Path, out_png: Path, seed: int = 7) -> int:
    """Write the designer's piece source under the round dir, import + render it."""
    import sys

    from ..generative.rng import SeededRNG
    from ..visualizer import GCodeVisualizer

    fn_name = str(payload.get("function_name") or "piece")
    source = str(payload.get("source") or "")
    if not source.strip():
        raise ValueError("code payload has empty source")
    piece_py = round_dir / "piece.py"
    piece_py.write_text(source, encoding="utf-8")
    name = f"studio_piece_{fn_name}"
    spec = importlib.util.spec_from_file_location(name, piece_py)
    mod = importlib.util.module_from_spec(spec)
    # register before exec so @dataclass resolves, and let the piece import a sibling
    sys.modules[name] = mod
    sys.path.insert(0, str(round_dir))
    try:
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
    finally:
        sys.path.pop(0)
    fn = getattr(mod, fn_name)
    bounds = config.paper.get_drawable_area()
    cmds = fn(SeededRNG(seed), bounds, colors=len(config.color.palette) or 3)
    prog = merge_chunks([cmds], config)
    GCodeVisualizer(config).preview(prog, str(out_png))
    return len(prog.commands)


def _render_scene_payload(payload: Dict[str, Any], config: PromptPlotConfig, round_dir: Path, out_png: Path) -> int:
    """Validate the designer's Scene JSON, compile it, write scene.json + pen_plan.json,
    and preview each pass at its physical width in its declared ink."""
    from ..scene import Scene, compile_to_program
    from ..visualizer import GCodeVisualizer

    scene = Scene.model_validate(payload)
    (round_dir / "scene.json").write_text(scene.model_dump_json(indent=2), encoding="utf-8")
    prog, pen_plan = compile_to_program(scene, config)
    (round_dir / "pen_plan.json").write_text(json.dumps(pen_plan, indent=2), encoding="utf-8")
    passes = [p for p in pen_plan if "pen" in p]
    widths = {p["pen"]: float(p["width_mm"]) for p in passes}
    GCodeVisualizer(config).preview(prog, str(out_png), pen_widths=widths)
    return len(prog.commands)


def _find_reference(slug: str, brief: Brief, base: Path, reference: Optional[Path]) -> Optional[Path]:
    """An explicit path wins; else the on-disk convention studio/<slug>/ref/reference.png."""
    if reference is not None:
        p = Path(reference)
        if not p.exists():
            raise FileNotFoundError(f"reference image not found: {p}")
        return p
    candidates = [base / "ref" / "reference.png"]
    if brief.path is not None:
        candidates.append(brief.path.parent.parent / slug / "ref" / "reference.png")
    for c in candidates:
        if c.exists():
            return c
    return None


async def run_design_loop(
    slug: str,
    provider: Any,
    style: str = "bauhaus",
    mode: str = "params",
    rounds: int = 3,
    out_dir: Optional[Path] = None,
    config: Optional[PromptPlotConfig] = None,
    brief: Optional[Brief] = None,
    paper: str = "a4",
    orientation: str = "portrait",
    reference: Optional[Path] = None,
    seed: int = 7,
    max_marks: int = 400,
) -> LoopResult:
    """``mode`` is ``params`` | ``code`` | ``scene``. With a ``reference`` image (or
    one found at ``studio/<slug>/ref/reference.png``) the designer SEES it and the
    critic judges the render against it."""
    brief = brief or get_brief(slug)
    config = config or PromptPlotConfig()
    config.paper = PaperConfig.from_size(paper, orientation=orientation, margin=15)
    config.color.enabled = True
    if not config.color.palette:
        config.color.palette = ["dodgerblue", "crimson", "black"]
    base = Path(out_dir) if out_dir is not None else (brief.path.parent / brief.slug if brief.path else Path(slug))
    base.mkdir(parents=True, exist_ok=True)
    ref = _find_reference(slug, brief, base, reference)

    if mode == "params":
        mode_instr = P.PARAMS_MODE_INSTRUCTIONS.format(schemas=_schemas_text())
        payload_schema = P.PARAMS_PAYLOAD_SCHEMA
    elif mode == "scene":
        mode_instr = P.SCENE_MODE_INSTRUCTIONS.format(authoring=P.authoring(), max_marks=max_marks)
        payload_schema = P.SCENE_PAYLOAD_SCHEMA
    else:
        mode_instr = P.CODE_MODE_INSTRUCTIONS.format(fn_name=f"studio_{slug.replace('-', '_')}")
        payload_schema = P.CODE_PAYLOAD_SCHEMA

    canon, rub = P.style_canon(style), P.rubric()
    ref_block = P.REFERENCE_BLOCK if ref is not None else ""
    critic_block = P.CRITIC_REFERENCE_BLOCK if ref is not None else P.CRITIC_RENDER_ONLY_BLOCK
    feedback = ""
    results: List[RoundResult] = []

    for i in range(rounds):
        rdir = base / "rounds" / f"r{i + 1:02d}"
        rdir.mkdir(parents=True, exist_ok=True)

        designer_prompt = P.DESIGNER_PROMPT.format(
            brief=brief.to_context(), reference_block=ref_block, style_canon=canon, rubric=rub,
            mode_instructions=mode_instr,
            feedback=(f"FEEDBACK FROM THE PREVIOUS ROUND (address it):\n{feedback}" if feedback else ""),
            payload_schema=payload_schema,
        )
        if ref is not None:
            reply = await provider.acomplete_multimodal(designer_prompt, image_paths=[ref])
        else:
            reply = await provider.acomplete(designer_prompt)
        obj = _extract_json(reply)
        if obj is None or "payload" not in obj:
            logger.warning("round %d: designer reply was not valid JSON; skipping round", i + 1)
            results.append(RoundResult(i + 1, concept="(invalid designer reply)", payload={}, render_path=None, verdict="fail"))
            feedback = "Your previous reply was not the required single JSON object. Follow the schema exactly."
            continue
        concept = str(obj.get("concept", ""))
        payload = obj["payload"] if isinstance(obj["payload"], dict) else {}
        (rdir / "payload.json").write_text(json.dumps({"concept": concept, "payload": payload}, indent=2), encoding="utf-8")

        render_path: Optional[Path] = rdir / "render.png"
        try:
            if mode == "params":
                _render_params_payload(payload, config, render_path)
            elif mode == "scene":
                _render_scene_payload(payload, config, rdir, render_path)
            else:
                _render_code_payload(payload, config, rdir, render_path, seed=seed)
        except Exception as e:
            logger.exception("round %d render failed", i + 1)
            results.append(RoundResult(i + 1, concept, payload, None, verdict="fail", instruction=f"render failed: {e}"))
            feedback = f"Your payload failed to render: {e}. Fix it."
            continue

        critic_prompt = P.CRITIC_PROMPT.format(brief=brief.to_context(), reference_block=critic_block, rubric=rub)
        critic_images = [ref, render_path] if ref is not None else [render_path]
        critique_raw = await provider.acomplete_multimodal(critic_prompt, image_paths=critic_images)
        critique = _extract_json(critique_raw) or {"verdict": "revise", "one_line": critique_raw[:300]}
        (rdir / "critique.json").write_text(json.dumps(critique, indent=2), encoding="utf-8")
        verdict = str(critique.get("verdict", "revise"))

        synth_raw = await provider.acomplete(P.SYNTH_PROMPT.format(concept=concept, critique=json.dumps(critique)))
        synth = _extract_json(synth_raw) or {}
        instruction = str(synth.get("instruction", ""))

        results.append(RoundResult(i + 1, concept, payload, render_path, critique, verdict, instruction))
        if verdict == "pass" and bool(synth.get("done")):
            break
        feedback = instruction or json.dumps(critique.get("top_fixes", []))

    final = base / "final"
    final.mkdir(parents=True, exist_ok=True)
    res = LoopResult(slug=slug, rounds=results, out_dir=base, final_verdict=(results[-1].verdict if results else "fail"))
    best = res.best
    proposal = [f"# STUDIO PROPOSAL — {brief.title} ({slug})", "", f"Style: {style} · Mode: {mode} · Rounds: {len(results)}", ""]
    if ref is not None:
        proposal.append(f"Reference: {ref}")
        proposal.append("")
    for r in results:
        proposal.append(f"## Round {r.index} — {r.verdict or 'n/a'}")
        proposal.append(r.concept or "")
        if r.critique:
            proposal.append(f"Critique: {r.critique.get('one_line', '')}")
        if r.instruction:
            proposal.append(f"Next: {r.instruction}")
        proposal.append("")
    if best is not None and best.render_path is not None:
        proposal.append(f"**Best round:** r{best.index:02d} ({best.verdict}) — {best.render_path}")
    (final / "PROPOSAL.md").write_text("\n".join(proposal), encoding="utf-8")
    return res


def run_design_loop_sync(*args: Any, **kwargs: Any) -> LoopResult:
    return asyncio.run(run_design_loop(*args, **kwargs))
