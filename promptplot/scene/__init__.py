"""Authored scenes — one model for the cubist, engraving and acrylic grammars.

    Scene → compile_scene(scene, config) → (commands, pen_plan)
          → compile_to_program(...)     → (GCodeProgram, pen_plan)
"""

from .compile import compile_scene, compile_to_program
from .models import HatchRule, Mark, Scene, SceneObject
from .occlusion import cover_walk, erode_ring, paint_walk

__all__ = [
    "HatchRule",
    "Mark",
    "Scene",
    "SceneObject",
    "compile_scene",
    "compile_to_program",
    "cover_walk",
    "erode_ring",
    "paint_walk",
]
