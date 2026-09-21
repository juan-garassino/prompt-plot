"""STABLE DIFFUSION AS TOPOGRAPHY — v4, every mass a distance-field nest.

v3 nested every mass with `radial_nest`, whose gap scales with the local
radius: on these shapes it measured a 0.66 mm minimum against a 1.01 mm median,
so the masses inked solid and the plate went black. Every nest here is a
`field_nest` instead — level sets of the distance field, so the gap is a
PHYSICAL constant, set once below from the paper scale.

The forward row is still ONE nest walked through `dissolve`; the U-Net is an
hourglass, encoder / decoder / conditioning are funnels. Nothing is traced.
"""
import math, sys
from promptplot.config import PromptPlotConfig
from promptplot.generative.engine.forms import (
    close_ring, dissolve, dot_cloud, field_nest, funnel_ring, hourglass_ring,
    lobed_ring, ribbon)
from promptplot.generative.engine.kit import _stroke_text, _spaced
from promptplot.generative.rng import SeededRNG
from promptplot.scene import Scene, SceneObject, Mark, compile_to_program
from promptplot.visualizer import GCodeVisualizer

W, H = 1672.0, 941.0          # source canvas, y DOWN like the reference

# The one number that decides whether this plate reads or blots. The compiler
# fits the source canvas uniformly inside the drawable area, so convert the
# physical gap we want on paper back into source units once, here.
PAPER_W, PAPER_H, MARGIN = 420.0, 297.0, 12.0
SCALE = min((PAPER_W - 2 * MARGIN) / W, (PAPER_H - 2 * MARGIN) / H)
GAP_MM = 1.6                  # comfortably above a 0.1-0.3 mm nib
PITCH = GAP_MM / SCALE

objs = []

def add(name, marks, ink=None, role="contour", width=None):
    ms = [Mark(role=role, points=m) for m in marks if len(m) >= 2]
    if ms:
        objs.append(SceneObject(name=name, ink=ink, width_mm=width, marks=ms))

def blob(name, cx, cy, r, ink, *, lobes=4, amp=0.17, rings=None, t=0.0, scatter=0.0, seed=1):
    ring = lobed_ring(cx, cy, r, lobes=lobes, amp=amp, wobble=0.07, rng=SeededRNG(seed))
    nest = field_nest(ring, pitch=PITCH, n=rings)
    add(name, dissolve(nest, t, SeededRNG(seed + 100), scatter=scatter) if t else nest, ink)

def text(s, x, y, h, ink=None):
    runs, run = [], []
    for c in _stroke_text(_spaced(s), x, H - y, h):
        if c.command == "G0":
            if len(run) >= 2: runs.append(run)
            run = [(c.x, H - c.y)]
        elif c.command == "G1":
            run.append((c.x, H - c.y))
    if len(run) >= 2: runs.append(run)
    add(f"label {s[:14]}", runs, ink, role="label")

# ---- pixel space: x and x~ (red) -------------------------------------------
blob("x data mass",   135, 330, 88, "red", seed=3)
blob("x tilde mass", 1545, 330, 88, "red", seed=9)

# ---- encoder / decoder / conditioning towers --------------------------------
add("encoder E",      field_nest(funnel_ring(255, 330, 385, 330, 150, 22), pitch=PITCH))
add("decoder D",      field_nest(funnel_ring(1425, 330, 1295, 330, 150, 22), pitch=PITCH))
add("conditioning T", field_nest(funnel_ring(266, 700, 390, 700, 116, 20), pitch=PITCH))

# ---- conditioning input y, and c (blue) -------------------------------------
blob("y prompt mass", 150, 700, 70, "blue", lobes=3, amp=0.20, seed=5)
blob("c vector",      442, 702, 29, "blue", lobes=3, amp=0.20, seed=6)

# ---- forward process: ONE nest dissolving left to right ---------------------
ROW = 175
XS  = [470, 640, 800, 955, 1105]
TS  = [0.0, 0.24, 0.48, 0.72, 0.93]
RS  = [56, 54, 52, 50, 48]
for k, (x, t, r) in enumerate(zip(XS, TS, RS)):
    blob(f"z step {k}", x, ROW, r, "ochre" if t < 0.55 else "black",
         t=t, scatter=22.0 * t, seed=11 + k)
add("z_T isotropic", dot_cloud(1105, ROW, 74, 340, SeededRNG(77), falloff=0.45), "black")

# ---- the denoiser: an hourglass nest ----------------------------------------
add("unet epsilon", field_nest(hourglass_ring(830, 500, 404, 272, 26, power=2.3), pitch=PITCH))

# ---- recovered latent (ochre) ------------------------------------------------
blob("z0 recovered", 1215, 500, 58, "ochre", seed=21)

# ---- flows -------------------------------------------------------------------
add("flow encode", ribbon((232, 330), (262, 330), 1, bow=0.0), role="flow")
add("flow to z0",  ribbon((392, 330), (455, 205), 1, bow=0.12), role="flow")
for k, x in enumerate(XS):
    add(f"drop {k}", [[(x, ROW + RS[k] + 12), (x, 372)]], role="construction")
add("flow condition", ribbon((476, 702), (640, 585), 5, bow=-0.14, spread=22), "blue", role="flow")
add("flow t",        [[(430, 500), (612, 500)]], role="flow")
add("sample loop",   ribbon((1065, 600), (645, 620), 4, bow=0.26, spread=18), "ochre", role="flow")
add("flow decode",   ribbon((1278, 500), (1310, 380), 1, bow=0.10), "ochre", role="flow")
add("flow out",      ribbon((1448, 330), (1470, 330), 1, bow=0.0), role="flow")

# ---- furniture ----------------------------------------------------------------
reg = []
for cx, cy in ((78, 78), (1594, 78), (78, 863), (1594, 863)):
    reg += [[(cx - 15, cy), (cx + 15, cy)], [(cx, cy - 15), (cx, cy + 15)]]
add("registration", reg, role="construction")

text("STABLE DIFFUSION", 70, 74, 21)
text("AS TOPOGRAPHY",    70, 104, 21)
for i, s in enumerate(("NOISE", "CONDITION", "DENOISE", "GENERATE")):
    text(s, 70, 838 + i * 21, 12)
for i, s in enumerate(("IMAGES", "THROUGH", "LATENT", "LANDSCAPES")):
    text(s, 1408, 838 + i * 21, 12)

s = Scene(canvas=(W, H), paper="a3", orientation="landscape", margin_mm=12,
          inks={"black": "#1b1b1b", "red": "#c0392b", "ochre": "#c8892a", "blue": "#2d6fa8"},
          widths_mm=[0.1, 0.3], objects=objs, title="STABLE DIFFUSION AS TOPOGRAPHY")
cfg = PromptPlotConfig()
prog, plan = compile_to_program(s, cfg)
passes = [p for p in plan if "pen" in p]
out = sys.argv[1] if len(sys.argv) > 1 else "/Users/juan-garassino/Downloads/pp_latent_topography_v4.png"
GCodeVisualizer(cfg).preview(prog, out, pen_widths={p["pen"]: p["width_mm"] for p in passes})
print(f"objects {len(objs)} | passes {len(passes)} | commands {len(prog.commands)}")
print("->", out)
