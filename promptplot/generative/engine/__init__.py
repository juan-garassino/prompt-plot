"""generative.engine — the composition engine for pen-plotter diagrams.

Pieces DECLARE (surfaces, line families, labels, pens); the engine renders
with the house artistic policies natively ON: hidden-line occlusion,
anti-crowding (depth-aware screen thinning, pause-resume line separation),
text halos and fit-to-page. Opt-OUT for exact/legacy modes, never opt-in.
"""

from .scene3d import HIDE, Iso, Camera, ScreenThin, Scene3D

__all__ = ["HIDE", "Iso", "Camera", "ScreenThin", "Scene3D"]
