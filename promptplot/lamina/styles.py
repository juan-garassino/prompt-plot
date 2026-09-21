"""Style presets — the movement canons applied at the LAMINA level.

The semantic-pen convention (kit slots): pieces emit pen INDICES with the kit
meaning — slot 0 = cool/secondary (BLUE), slot 1 = the scarce accent (PINK),
slot 2 = structure/type (BLACK), slot 3 = extra content pen. Preset ``pens``
are ordered BY SLOT, so a plate maps semantics to physical pens simply via
``config.color.palette = preset.pens`` before ``merge_chunks``. Two-pen styles
put structure at slot 0 (``_pen`` wraps BLACK→0 when colors=2). One piece →
many styled plates.

Presets encode the canons in ``promptplot/generative/STYLES.md``; the critic
notes there remain the judging authority.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class PenRule:
    """One semantic rule: an object whose name matches ``name`` (regex, searched)
    and whose mark role matches ``role`` ("" = any) gets this ``ink`` and/or
    ``width_mm``. Ink rules and width rules are separate lists; each is
    first-match-wins, mirroring the reference plates' ``color_for`` /
    ``line_weight``."""

    name: str = ""
    role: str = ""
    ink: Optional[str] = None
    width_mm: Optional[float] = None

    def matches(self, obj_name: str, mark_role: str) -> bool:
        if self.role and self.role != mark_role:
            return False
        return not self.name or re.search(self.name, obj_name) is not None


@dataclass(frozen=True)
class PenRules:
    """Semantic name → (ink, width). This is what lets an authored scene say
    "this is `queen veil plane`, therefore red at 0.10" without the designer
    tagging every mark."""

    ink_rules: Tuple[PenRule, ...] = ()
    width_rules: Tuple[PenRule, ...] = ()

    def resolve(self, obj_name: str, mark_role: str) -> Tuple[Optional[str], Optional[float]]:
        ink = next((r.ink for r in self.ink_rules if r.ink is not None and r.matches(obj_name, mark_role)), None)
        width = next(
            (r.width_mm for r in self.width_rules if r.width_mm is not None and r.matches(obj_name, mark_role)), None
        )
        return ink, width

    def as_compile_rules(self):
        """Adapter for ``scene.compile_scene(rules=...)``."""

        def f(obj, mark):
            return self.resolve(obj.name, mark.role)

        return f


@dataclass(frozen=True)
class StylePreset:
    name: str
    pens: List[str]  # physical palette; index == semantic pen index
    paper: str  # "cream" | "white" (paper stock note, not rendered)
    furniture: Tuple[str, ...]  # which furniture elements the plate draws
    type_align: str  # "left" | "center"
    rule_passes: int = 1  # passes for gutter rules / hairlines
    accent_pen: int = 1  # semantic index reserved for the scarce accent
    notes: str = ""  # one-line canon reminder
    rules: Optional[PenRules] = None  # semantic name → ink/width, for authored scenes


# The cubist reference plate's semantic rules, as a reusable preset. Inks are
# names the Scene must declare (black/red/yellow/blue). Widths are TARGETS the
# compiler snaps to the nearest available nib. Order matters: first match wins.
CUBIST_RULES = PenRules(
    ink_rules=(
        PenRule(r"^queen.*(veil plane|left lapel|cheek dark triangle)", ink="red"),
        PenRule(r"^king.*(outer cloak|cheek shade)", ink="blue"),
        PenRule(r"^cello.*(shade|facet|tail)", ink="yellow"),
        PenRule(r"^musician.*(neck|ear|head stripe)", ink="yellow"),
        PenRule(r"^(bridge token|ffn output|ffn input)", ink="yellow"),
        PenRule(r"^Q label", ink="red"),
        PenRule(r"^K label", ink="blue"),
        PenRule(r"^V label", ink="yellow"),
        PenRule("", ink="black"),
    ),
    width_rules=(
        PenRule("", role="hatch", width_mm=0.10),
        PenRule(r"(expand label|nonlinear label|project label|ffn output|softmax label)", role="label", width_mm=0.40),
        PenRule(r"(fraction bar|root radical|d lowercase)", role="label", width_mm=0.50),
        PenRule("", role="label", width_mm=0.18),
        PenRule(r"^(query stroke|key stroke)", role="flow", width_mm=0.10),
        PenRule(r"^(value stream|attention output stream|ffn return|residual inner)", role="flow", width_mm=0.50),
        PenRule("", role="flow", width_mm=0.22),
        PenRule(r"^arcade empty", width_mm=0.48),
        PenRule(r"pupil", width_mm=0.50),
        PenRule(r"^registration", width_mm=0.10),
        PenRule(r"(hatch|seam|facet|shade|fold|collar|rim|mullion|shelf|tread|paving|brow|eye|mouth|ear|features|string|pegs|cut|cross|stem|crown base)", width_mm=0.18),
        PenRule(r"^board (rank|file)", width_mm=0.16),
        PenRule(r"^title", width_mm=0.50),
        PenRule(r"^(paper frame|board surface|board front apron|bridge body|bridge walkway|residual bypass|softmax bowl|cello body)$", width_mm=0.50),
        PenRule(r"^(queen|king|musician|input (first|second|third)).*(silhouette|cloak|robe|body|hair|face|crown|outer|forearm|arm)", width_mm=0.48),
        PenRule(r"^(queen|king|musician|input (first|second|third))", width_mm=0.18),
        PenRule(r"^(board piece|bridge token|ffn input|ffn output).*(outline|body|head)", width_mm=0.40),
        PenRule(r"^(board piece|bridge token|ffn input|ffn output)", width_mm=0.16),
        PenRule(r"(nonlinear outer|expanded outline|lintel|housing front|tablet|arch|opening|support|slab|upright|buttress|dove)", width_mm=0.40),
        PenRule("", width_mm=0.24),
    ),
)


STYLE_PRESETS: Dict[str, StylePreset] = {
    "bauhaus": StylePreset(
        name="bauhaus",
        pens=["dodgerblue", "deeppink", "black"],
        paper="cream",
        furniture=("title", "swatch_bar", "scale_footer", "number_chips"),
        type_align="left",
        notes="geometry as ideology; asymmetric balance; accent scarce",
    ),
    "swiss": StylePreset(
        name="swiss",
        pens=["black", "red"],
        paper="white",
        furniture=("title", "gutter_rules", "scale_footer"),
        type_align="left",
        notes="the grid is the artwork; one HUGE element; centered = fail",
    ),
    "deco": StylePreset(
        name="deco",
        pens=["goldenrod", "darkred", "black"],
        paper="cream",
        furniture=("title", "gutter_rules", "scale_footer", "number_chips"),
        type_align="center",
        rule_passes=2,
        notes="machine-age luxury; ray fans; symmetry allowed; exact spacing",
    ),
    "pop": StylePreset(
        name="pop",
        pens=["blue", "red", "black", "gold"],
        paper="white",
        furniture=("title", "gutter_rules", "number_chips"),
        type_align="left",
        rule_passes=3,
        notes="benday dots; fat outlines; repetition must vary meaningfully",
    ),
    "radial_viz": StylePreset(
        name="radial_viz",
        pens=["steelblue", "indianred", "black", "darkseagreen"],
        paper="cream",
        furniture=("title", "scale_footer", "swatch_bar"),
        type_align="left",
        notes="data as concentric arcs; annotation is the point, gridded",
    ),
    "science_poster": StylePreset(
        name="science_poster",
        pens=["dodgerblue", "crimson", "black", "forestgreen"],
        paper="cream",
        furniture=("title", "gutter_rules", "scale_footer", "number_chips"),
        type_align="left",
        notes="one dominant body; field density IS the data; data footer",
    ),
    "cubist_plate": StylePreset(
        name="cubist_plate",
        pens=["black", "red", "yellow", "blue"],
        paper="cream",
        furniture=("title",),
        type_align="left",
        notes="authored planes; one hatch direction per plane; lit planes bare; ink is semantic",
        rules=CUBIST_RULES,
    ),
}


def get_style(name: str) -> StylePreset:
    if name not in STYLE_PRESETS:
        raise KeyError(f"Unknown style {name!r}. Available: {sorted(STYLE_PRESETS)}")
    return STYLE_PRESETS[name]
