"""GAN — GENERATIVE ADVERSARIAL NETWORKS, from the same form vocabulary.

Panels are rounded-rect rings with radial bursts; data masses are radial nests;
the latent space is a dot cloud; every connection is a ribbon. Same primitives
as the topography plate, different composition — that is the point.
"""
import sys
from promptplot.config import PromptPlotConfig
from promptplot.generative.engine.forms import (
    dot_cloud, lobed_ring, radial_burst, radial_nest, ribbon, rounded_rect_ring, close_ring)
from promptplot.generative.engine.geometry import Polygon
from promptplot.generative.engine.kit import _stroke_text, _spaced
from promptplot.generative.rng import SeededRNG
from promptplot.scene import Scene, SceneObject, Mark, compile_to_program
from promptplot.visualizer import GCodeVisualizer

W, H = 1510.0, 1041.0
objs = []

def add(name, marks, ink=None, role="contour"):
    ms = [Mark(role=role, points=m) for m in marks if len(m) >= 2]
    if ms: objs.append(SceneObject(name=name, ink=ink, marks=ms))

def text(s, x, y, h, ink=None):
    runs, run = [], []
    for c in _stroke_text(_spaced(s), x, H - y, h):
        if c.command == "G0":
            if len(run) >= 2: runs.append(run)
            run = [(c.x, H - c.y)]
        elif c.command == "G1":
            run.append((c.x, H - c.y))
    if len(run) >= 2: runs.append(run)
    add(f"label {s[:12]}", runs, ink, role="label")

def mass(name, cx, cy, r, ink, *, rings=22, lobes=3, seed=1):
    ring = lobed_ring(cx, cy, r, lobes=lobes, amp=0.30, wobble=0.10, rng=SeededRNG(seed))
    add(name, radial_nest(ring, n=rings, inner=0.08, gamma=0.9), ink)

def panel(name, x0, y0, x1, y1, ink, seed, rays=54):
    ring = rounded_rect_ring(x0, y0, x1, y1)
    add(f"{name} frame", [close_ring(ring)])
    add(f"{name} burst", radial_burst((x0+x1)/2, (y0+y1)/2, (x1-x0)*0.92, rays,
                                      SeededRNG(seed), region=Polygon(ring),
                                      dash=2.4, gap=2.2), ink)

# ---- latent space + real data -------------------------------------------------
add("latent space", dot_cloud(150, 430, 62, 300, SeededRNG(2), falloff=1.3), "black")
mass("real data mass", 245, 690, 96, "black", rings=26, seed=4)

# ---- generator + discriminator stacks ----------------------------------------
GY0, GY1 = 355, 545
for i, (x, ink) in enumerate(zip((330, 415, 500, 585), ("red", "black", "blue", "ochre"))):
    panel(f"G layer {i}", x, GY0, x + 62, GY1, ink, 10 + i)
for i, (x, ink) in enumerate(zip((900, 985, 1070, 1155, 1240), ("red", "black", "blue", "ochre", "black"))):
    panel(f"D layer {i}", x, GY0, x + 62, GY1, ink, 30 + i)

# ---- generated sample ---------------------------------------------------------
mass("generated sample", 760, 430, 86, "red", rings=24, seed=7)

# ---- flows ---------------------------------------------------------------------
add("z to G", ribbon((215, 430), (322, 445), 6, bow=0.10, spread=44), "black", role="flow")
for a, b in ((392, 415), (477, 500), (562, 585)):
    add("G hop", ribbon((a + 62 - 62, 450), (b, 450), 1, bow=0.0), role="flow")
add("G to xhat", ribbon((650, 450), (690, 440), 3, bow=0.10, spread=26), "red", role="flow")
add("xhat to D", ribbon((840, 440), (896, 450), 5, bow=0.10, spread=34), "red", role="flow")
add("real to D", ribbon((330, 700), (896, 470), 5, bow=0.16, spread=30), "black", role="flow")
add("D to fake", ribbon((1305, 470), (1375, 420), 1, bow=0.08), role="flow")
add("D to real", ribbon((1305, 450), (1375, 520), 1, bow=-0.08), role="flow")
add("adversarial loss", ribbon((1380, 400), (470, 250), 1, bow=0.10), role="construction")

# ---- sample strips --------------------------------------------------------------
for i, ink in enumerate(("red", "black", "blue", "ochre", "red", "black")):
    x = 330 + i * 92
    panel(f"gen sample {i}", x, 830, x + 74, 930, ink, 60 + i, rays=38)
for i in range(3):
    x = 940 + i * 92
    panel(f"real sample {i}", x, 830, x + 74, 930, "black", 80 + i, rays=38)

# ---- furniture + type -------------------------------------------------------------
reg = []
for cx, cy in ((70, 70), (1440, 70), (70, 971), (1440, 971), (795, 300), (795, 790)):
    reg += [[(cx - 14, cy), (cx + 14, cy)], [(cx, cy - 14), (cx, cy + 14)]]
add("registration", reg, role="construction")
add("centre rule", [[(795, 330), (795, 760)]], role="construction")

text("GAN", 70, 118, 26)
text("GENERATIVE", 70, 156, 12); text("ADVERSARIAL", 70, 176, 12); text("NETWORKS", 70, 196, 12)
text("GENERATOR  G", 330, 300, 16); text("DISCRIMINATOR  D", 900, 300, 16)
text("LATENT SPACE", 92, 530, 11); text("REAL DATA", 180, 810, 11)
text("GENERATED SAMPLES", 640, 545, 11)
text("GENERATED SAMPLES", 400, 965, 11); text("REAL SAMPLES", 980, 965, 11)
text("PEN PLOTTER", 70, 980, 12)
for i, s in enumerate(("NOISE", "GENERATION", "ADVERSARY", "LEARNING", "SYNTHESIS")):
    text(s, 1300, 880 + i * 19, 10)

s = Scene(canvas=(W, H), paper="a3", orientation="landscape", margin_mm=12,
          inks={"black": "#1b1b1b", "red": "#c0392b", "blue": "#2d6fa8", "ochre": "#c8892a"},
          widths_mm=[0.1, 0.3], objects=objs, title="GAN")
cfg = PromptPlotConfig()
prog, plan = compile_to_program(s, cfg)
passes = [p for p in plan if "pen" in p]
out = sys.argv[1] if len(sys.argv) > 1 else "/Users/juan-garassino/Downloads/pp_gan_plate_v1.png"
GCodeVisualizer(cfg).preview(prog, out, pen_widths={p["pen"]: p["width_mm"] for p in passes})
print(f"objects {len(objs)} | passes {len(passes)} | commands {len(prog.commands)}")
print("->", out)
