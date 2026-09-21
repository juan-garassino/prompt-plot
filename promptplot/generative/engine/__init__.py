"""generative.engine — the composition engine for pen-plotter diagrams.

Pieces DECLARE (surfaces, forms, line families, labels, pens); the engine renders
with the house artistic policies natively ON: hidden-line occlusion,
anti-crowding (depth-aware screen thinning, pause-resume line separation),
text halos and fit-to-page. Opt-OUT for exact/legacy modes, never opt-in.

The layers, innermost first — each uses only the ones above it:

    geometry.py   exact 2D kernel: Region algebra, clip/trim, offset/erode,
                  Bezier flattening, arc-length resampling, ring smoothing
    forms.py      WHAT the shapes are: lobed/hourglass/funnel/rect rings, the
                  three nesting rules (field_nest = constant PHYSICAL gap and
                  the right default; contour_nest = offset, folds past the
                  tightest valley; radial_nest = self-similar, gap scales with
                  radius), dissolve, clouds, bursts, ribbons
    material.py   HOW a mark is made, per material: hatch + physical clearance,
                  cut_tone duty cycles, flow_family, surface_grid, brush/image
    kit.py        2D furniture: fills, type, swatches, marks, clipping helpers
    policies.py   guardrails: crossing occlusion, line spacing, ink density
    looks.py      whole-sheet effects: anaglyph, echo, dash rain, glitch
    scene3d.py    3D composition: projection + z-buffer hidden-line removal

``promptplot.scene`` sits above this as the 2D authored-scene composition layer
(named objects, cover/paint occlusion, the compiler to colour-layered GCode).
"""

from .scene3d import HIDE, Iso, Camera, Occupancy, PolarLOD, ScreenThin, Scene3D
from .forms import (  # WHAT the shapes are: rings, nests, dissolves, clouds
    close_ring,
    contour_nest,
    dissolve,
    dot_cloud,
    field_nest,
    funnel_ring,
    hourglass_ring,
    lobed_ring,
    max_erode,
    radial_burst,
    radial_nest,
    ribbon,
    rounded_rect_ring,
)
from .material import (  # how a MARK is made, per material
    ImageGrid,
    brush_family,
    cut_tone,
    flow_family,
    flow_strokes,
    gauss_tone,
    hatch_polygon,
    load_image_grid,
    physical_inset,
    physical_spacing,
    quantize_palette,
    shadow_cross,
    snap_color,
    suppress_parallel,
    surface_grid,
)

__all__ = [
    # composition
    "HIDE", "Iso", "Camera", "Occupancy", "PolarLOD", "ScreenThin", "Scene3D",
    # forms — what the shapes are
    "close_ring", "contour_nest", "dissolve", "dot_cloud", "field_nest", "funnel_ring",
    "hourglass_ring",
    "lobed_ring", "max_erode", "radial_burst", "radial_nest", "ribbon", "rounded_rect_ring",
    # material — how a mark is made
    "ImageGrid", "brush_family", "cut_tone", "flow_family", "flow_strokes", "gauss_tone",
    "hatch_polygon", "load_image_grid", "physical_inset", "physical_spacing",
    "quantize_palette", "shadow_cross", "snap_color", "suppress_parallel", "surface_grid",
]
