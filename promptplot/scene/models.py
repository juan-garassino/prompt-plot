"""The authored scene: what an LLM (or a hand) emits, what the compiler executes.

One model for all three drawing grammars. Two things are first-class so the
cubist plate, the Dalí engraving and the acrylic painting all fit:

* a mark's **physical width** — a 0.10 mm nib and a 4 mm brush footprint are the
  same field;
* a mark's **stage** — paint order. Pen work has one stage; acrylic has
  underpainting → body → accents, and later stages cover earlier ones.

Objects are listed BACK TO FRONT. ``name`` is functional, not commentary: it is
what ink/width rules key on ("queen veil plane" → red, 0.10). ``cover`` is the
object's occlusion region in source units — never exported as a fill.
"""

from __future__ import annotations

from typing import Dict, List, Literal, Optional, Tuple

from pydantic import BaseModel, Field, field_validator, model_validator

Point = Tuple[float, float]
Role = Literal["contour", "hatch", "label", "flow", "construction", "accent"]
Occlusion = Literal["cover", "paint", "none"]


class Mark(BaseModel):
    """One pen or brush movement: a polyline with a role and physical attributes."""

    role: Role = "contour"
    points: List[Point]
    ink: Optional[str] = None  # name in Scene.inks; None → object → default
    width_mm: Optional[float] = None  # nib or brush footprint; None → object → finest
    stage: Optional[str] = None  # name in Scene.stages; None → object → first

    @field_validator("points")
    @classmethod
    def _at_least_two(cls, v):
        if len(v) < 2:
            raise ValueError("a mark needs at least 2 points")
        return [(float(x), float(y)) for x, y in v]


class HatchRule(BaseModel):
    """A procedural fill the compiler expands over the object's ``cover`` with
    ``material.hatch_polygon`` — so a designer declares a plane's tone in one
    line instead of emitting hundreds of hatch points. Spacing/inset are in
    source units and are floored by the physical nib rules at compile time."""

    spacing: float
    angle: float = 0.0
    inset: float = 0.0
    shadow: bool = False  # add the +67°, ×1.5 cross family
    ink: Optional[str] = None
    width_mm: Optional[float] = None

    @field_validator("spacing")
    @classmethod
    def _positive(cls, v):
        if v <= 0:
            raise ValueError("hatch spacing must be > 0")
        return float(v)


class SceneObject(BaseModel):
    """A named thing in the drawing, with its occluder and its marks."""

    name: str
    material: Optional[str] = None  # skin | hair | cubist_plane | painterly | ... (advisory)
    cover: Optional[List[Point]] = None  # occlusion polygon, source units, >= 3 vertices
    ink: Optional[str] = None
    width_mm: Optional[float] = None
    stage: Optional[str] = None
    marks: List[Mark] = Field(default_factory=list)
    fills: List[HatchRule] = Field(default_factory=list)  # expanded over ``cover`` at compile

    @model_validator(mode="after")
    def _fills_need_cover(self):
        if self.fills and not self.cover:
            raise ValueError(f"{self.name}: fills need a cover polygon to hatch")
        return self

    @field_validator("cover")
    @classmethod
    def _cover_ok(cls, v):
        if v is None:
            return v
        if len(v) < 3:
            raise ValueError("cover needs at least 3 vertices")
        return [(float(x), float(y)) for x, y in v]


class Scene(BaseModel):
    """The whole authored drawing, in source units, with its physical intent."""

    canvas: Tuple[float, float]  # (width, height) in source units, y DOWN like SVG
    paper: str = "a3"
    orientation: str = "portrait"
    margin_mm: float = 10.0
    inks: Dict[str, str] = Field(default_factory=lambda: {"black": "#111111"})  # name → hex
    widths_mm: List[float] = Field(default_factory=lambda: [0.1, 0.5])  # available nibs/brushes
    stages: List[str] = Field(default_factory=lambda: ["main"])  # paint order
    occlusion: Occlusion = "cover"
    objects: List[SceneObject] = Field(default_factory=list)  # BACK TO FRONT
    title: Optional[str] = None

    @field_validator("widths_mm")
    @classmethod
    def _widths_sorted_positive(cls, v):
        if not v or any(w <= 0 for w in v):
            raise ValueError("widths_mm must be non-empty and positive")
        return sorted(v)

    @model_validator(mode="after")
    def _names_resolve(self):
        stage_set = set(self.stages)
        for o in self.objects:
            for who, ink, stage in [(o.name, o.ink, o.stage)] + [
                (f"{o.name}/mark", m.ink, m.stage) for m in o.marks
            ]:
                if ink is not None and ink not in self.inks:
                    raise ValueError(f"{who}: unknown ink {ink!r}; declared: {sorted(self.inks)}")
                if stage is not None and stage not in stage_set:
                    raise ValueError(f"{who}: unknown stage {stage!r}; declared: {self.stages}")
        return self

    # -- convenience -------------------------------------------------------
    @property
    def default_ink(self) -> str:
        return next(iter(self.inks))

    @property
    def finest_width(self) -> float:
        return self.widths_mm[0]

    def snap_width(self, w: Optional[float]) -> float:
        if w is None:
            return self.finest_width
        return min(self.widths_mm, key=lambda a: abs(a - w))

    def stage_index(self, name: Optional[str]) -> int:
        return 0 if name is None else self.stages.index(name)
