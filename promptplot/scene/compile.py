"""Scene → colour-layered GCode + a pen plan.

    occlusion (cover or paint, by grammar)
    → source units to mm (uniform fit, margin on the tighter axis, centred, y flipped)
    → width snapped to the nearest available nib/brush
    → exact duplicate removal, widest pass wins
    → passes ordered (stage, width ascending, ink)  — fine-before-broad for pens,
      stage order dominating for paint
    → one colour index per pass, handed to the normal colour-layer pipeline

The pen plan says what each index physically is, the way ``lamina.plate`` does.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, List, Optional, Tuple

from ..config import PaperConfig, PromptPlotConfig
from ..generative.engine.geometry import Poly
from ..models import GCodeCommand, GCodeProgram
from .models import Mark, Scene, SceneObject
from .occlusion import cover_walk, paint_walk

# (object_name, role) -> (ink | None, width_mm | None). Phase 3 supplies real
# semantic rules from lamina.styles; until then this hook lets a caller inject them.
Rules = Callable[[SceneObject, Mark], Tuple[Optional[str], Optional[float]]]

PassKey = Tuple[int, float, str]  # (stage index, width mm, ink name)


def _resolve(scene: Scene, obj: SceneObject, m: Mark, rules: Optional[Rules]) -> Tuple[str, float, int]:
    r_ink, r_w = rules(obj, m) if rules else (None, None)
    ink = m.ink or obj.ink or r_ink or scene.default_ink
    width = scene.snap_width(m.width_mm if m.width_mm is not None else obj.width_mm if obj.width_mm is not None else r_w)
    stage = scene.stage_index(m.stage or obj.stage)
    return ink, width, stage


def _fit(scene: Scene, config: PromptPlotConfig) -> Tuple[float, float, float]:
    """(scale, off_x, off_y): source units → paper mm, centred with the margin
    honoured on the tighter axis. Source y is DOWN; paper y is UP."""
    pw, ph = config.paper.width, config.paper.height
    cw, ch = scene.canvas
    m = scene.margin_mm
    scale = min((pw - 2 * m) / cw, (ph - 2 * m) / ch)
    off_x = (pw - cw * scale) / 2.0
    off_y = (ph - ch * scale) / 2.0
    return scale, off_x, off_y


def _key(poly: Poly, nd: int = 3) -> Tuple:
    r = tuple((round(x, nd), round(y, nd)) for x, y in poly)
    return min(r, tuple(reversed(r)))


def _expand_fills(scene: Scene, page_scale: float, rules: Optional[Rules]) -> Scene:
    """Return a copy of the scene with every ``fills`` rule turned into hatch marks
    clipped exactly to the object's cover. Spacing is floored at 2.4 × the finest
    nib and the inset at ½ border + ½ hatch + 0.035 mm, both in source units via
    ``page_scale`` (mm per unit). ``shadow`` adds the +67° ×1.5 cross family."""
    if not any(o.fills for o in scene.objects):
        return scene
    from ..generative.engine.material import hatch_polygon, physical_inset, physical_spacing, shadow_cross

    out = scene.model_copy(deep=True)
    fine = scene.finest_width
    for obj in out.objects:
        if not obj.fills or not obj.cover:
            continue
        # the outline nib bounding this plane: explicit, else the rules', else the finest
        r_ink, r_w = rules(obj, Mark(role="contour", points=[(0, 0), (1, 1)])) if rules else (None, None)
        border = scene.snap_width(obj.width_mm if obj.width_mm is not None else r_w)
        new_marks: List[Mark] = []
        for rule in obj.fills:
            hatch_w = scene.snap_width(rule.width_mm) if rule.width_mm is not None else fine
            base = {
                "spacing": physical_spacing(rule.spacing, hatch_w, page_scale),
                "angle": rule.angle,
                "inset": physical_inset(rule.inset, border, hatch_w, page_scale),
            }
            families = [base, shadow_cross(base)] if rule.shadow else [base]
            for fam in families:
                for run in hatch_polygon(obj.cover, fam["spacing"], fam["angle"], fam["inset"]):
                    new_marks.append(
                        Mark(role="hatch", points=run, ink=rule.ink, width_mm=hatch_w, stage=obj.stage)
                    )
        obj.marks = list(obj.marks) + new_marks
        obj.fills = []
    return out


def compile_scene(
    scene: Scene,
    config: Optional[PromptPlotConfig] = None,
    *,
    rules: Optional[Rules] = None,
    feed: Optional[int] = None,
    min_len_mm: float = 0.15,
) -> Tuple[List[GCodeCommand], List[Dict]]:
    """-> (commands, pen_plan). Commands are colour-tagged strokes ready for
    ``orchestrate.merge_chunks``; the pen plan is one entry per pass."""
    config = config or PromptPlotConfig()
    config.paper = PaperConfig.from_size(scene.paper, scene.orientation, margin=scene.margin_mm)
    f = feed or config.pen.feed_rate
    scale, off_x, off_y = _fit(scene, config)
    ch = scene.canvas[1]

    def to_mm(poly: Poly) -> Poly:
        return [(off_x + x * scale, off_y + (ch - y) * scale) for x, y in poly]

    # 0. expand declared fills into hatch marks over each object's cover, with the
    #    physical clearance floors, BEFORE occlusion so fronts hide them properly.
    scene = _expand_fills(scene, scale, rules)

    # 1. occlusion in source units (pen grammars), then to mm
    strokes: List[Tuple[PassKey, str, Poly]] = []  # (pass key, role, polyline mm)
    if scene.occlusion == "cover":
        for idx, m, runs in cover_walk(scene):
            ink, w, st = _resolve(scene, scene.objects[idx], m, rules)
            for r in runs:
                strokes.append(((st, w, ink), m.role, to_mm(r)))
    else:
        for obj in scene.objects:
            for m in obj.marks:
                ink, w, st = _resolve(scene, obj, m, rules)
                strokes.append(((st, w, ink), m.role, to_mm(list(m.points))))

    # 2. paint occlusion in mm, in paint order (stage, then declared object order)
    if scene.occlusion == "paint" and strokes:
        order = sorted(range(len(strokes)), key=lambda i: (strokes[i][0][0], i))
        keep = paint_walk([(strokes[i][0][1], strokes[i][2]) for i in order])
        alive = {order[k] for k, ok in enumerate(keep) if ok}
        culled = len(strokes) - len(alive)
        strokes = [s for i, s in enumerate(strokes) if i in alive]
    else:
        culled = 0

    # 3. exact dedup, widest pass wins (process widths descending)
    seen: set = set()
    kept: List[Tuple[PassKey, str, Poly]] = []
    for key, role, poly in sorted(strokes, key=lambda s: -s[0][1]):
        if sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(poly, poly[1:])) < min_len_mm:
            continue
        k = _key(poly)
        if k in seen:
            continue
        seen.add(k)
        kept.append((key, role, poly))

    # 4. passes: (stage, width asc, ink order as declared)
    ink_rank = {name: i for i, name in enumerate(scene.inks)}
    pass_keys = sorted({k for k, _, _ in kept}, key=lambda k: (k[0], k[1], ink_rank[k[2]]))
    pass_index = {k: i for i, k in enumerate(pass_keys)}

    commands: List[GCodeCommand] = []
    counts: Dict[PassKey, int] = {k: 0 for k in pass_keys}
    for key in pass_keys:
        ci = pass_index[key]
        for k2, _role, poly in kept:
            if k2 != key:
                continue
            counts[key] += 1
            commands.append(GCodeCommand(command="G0", x=round(poly[0][0], 3), y=round(poly[0][1], 3)))
            commands.append(GCodeCommand(command="M3", s=1000, color=ci))
            for x, y in poly[1:]:
                commands.append(GCodeCommand(command="G1", x=round(x, 3), y=round(y, 3), f=f, color=ci))
            commands.append(GCodeCommand(command="M5"))

    pen_plan = [
        {
            "pen": pass_index[k],
            "stage": scene.stages[k[0]],
            "ink": k[2],
            "hex": scene.inks[k[2]],
            "width_mm": k[1],
            "strokes": counts[k],
        }
        for k in pass_keys
    ]
    if culled:
        pen_plan.append({"culled_hidden_strokes": culled})
    return commands, pen_plan


def compile_to_program(
    scene: Scene, config: Optional[PromptPlotConfig] = None, **kw
) -> Tuple[GCodeProgram, List[Dict]]:
    """compile_scene + the normal colour-layer pipeline. Sets ``config.color`` so
    the palette is the pen plan's hexes in pass order."""
    from ..orchestrate import merge_chunks

    config = config or PromptPlotConfig()
    commands, pen_plan = compile_scene(scene, config, **kw)
    passes = [p for p in pen_plan if "pen" in p]
    config.color.enabled = len(passes) > 1
    config.color.palette = [p["hex"] for p in passes] or ["#111111"]
    program = merge_chunks([commands], config)
    program.metadata["pen_plan"] = pen_plan
    program.metadata["scene_title"] = scene.title
    return program, pen_plan
