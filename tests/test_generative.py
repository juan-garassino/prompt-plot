"""Seeded generative pillar: determinism, bounds-safety, colors, schema introspection."""

import pytest

from promptplot.config import PromptPlotConfig, PaperConfig
from promptplot.generative import (
    SeededRNG,
    list_generators,
    run_generator,
    get_generator_schema,
    get_all_generator_schemas,
)
from promptplot.orchestrate import merge_chunks, split_color_layers

BOUNDS = (10.0, 10.0, 138.0, 200.0)  # A5 drawable


def test_rng_is_deterministic():
    a = SeededRNG(42)
    b = SeededRNG(42)
    assert [a.random() for _ in range(5)] == [b.random() for _ in range(5)]
    assert a.noise2d(1.5, 2.5) == b.noise2d(1.5, 2.5)


def test_all_generators_registered():
    gens = list_generators()
    for expected in [
        "tiled_field",
        "ripple_field",
        "flow_field",
        "maze",
        "truchet",
        "wave_bands",
        "stipple",
        "waves_with_circles",
        "crosshatch_weave",
        "turning_weave",
        "wave_gradient",
        "interference_field",
        "frequency_lens",
        "hitomezashi",
        "harmonograph",
        "vortex_field",
        "moire_layers",
        "strange_attractor",
        "domain_warp",
        "contour_field",
        "superformula_bloom",
        "lissajous_carpet",
        "scribble_halftone",
        "comic_panels",
        "line_halftone",
        "scribble_portrait",
        "sparkle_grid",
        "iso_city",
        "rounded_circuits",
        "lissajous_swarm",
        "black_hole",
        "pe_carpet",
        "attention_arcs",
        "residual_river",
        "weight_matrix",
        "attention_matrix",
        "black_hole_bauhaus",
        "big_bang",
        "big_bang_v1",
        "bauhaus_attractor",
        "bauhaus_attention",
        "bauhaus_weights",
        "bauhaus_gradient",
        "bauhaus_resonance",
        "bauhaus_loom",
        "bauhaus_decision",
        "bauhaus_conveyor",
        "bauhaus_settling",
        "bauhaus_relevance",
        "bauhaus_memory",
        "bauhaus_locality",
        "bauhaus_memory_v1",
        "bauhaus_locality_v1",
        "bauhaus_relevance_v1",
        "gw150914",
    ]:
        assert expected in gens


@pytest.mark.parametrize(
    "name",
    [
        "tiled_field",
        "ripple_field",
        "flow_field",
        "maze",
        "truchet",
        "wave_bands",
        "stipple",
        "waves_with_circles",
        "crosshatch_weave",
        "turning_weave",
        "wave_gradient",
        "interference_field",
        "frequency_lens",
        "hitomezashi",
        "harmonograph",
        "vortex_field",
        "moire_layers",
        "strange_attractor",
        "domain_warp",
        "contour_field",
        "superformula_bloom",
        "lissajous_carpet",
        "scribble_halftone",
        "comic_panels",
        "line_halftone",
        "scribble_portrait",
        "sparkle_grid",
        "iso_city",
        "rounded_circuits",
        "lissajous_swarm",
        "black_hole",
        "pe_carpet",
        "attention_arcs",
        "residual_river",
        "weight_matrix",
        "attention_matrix",
        "black_hole_bauhaus",
        "big_bang",
        "bauhaus_attractor",
        "bauhaus_attention",
        "bauhaus_weights",
        "bauhaus_gradient",
        "bauhaus_resonance",
    ],
)
def test_generator_deterministic_and_nonempty(name):
    a = run_generator(name, BOUNDS, seed=123)
    b = run_generator(name, BOUNDS, seed=123)
    assert a and b, f"{name} produced no commands"
    assert [c.to_gcode() for c in a] == [c.to_gcode() for c in b], f"{name} not deterministic"


@pytest.mark.parametrize(
    "name",
    [
        "tiled_field",
        "ripple_field",
        "flow_field",
        "waves_with_circles",
        "crosshatch_weave",
        "turning_weave",
        "wave_gradient",
        "interference_field",
        "frequency_lens",
        "hitomezashi",
        "harmonograph",
        "vortex_field",
        "strange_attractor",
        "domain_warp",
        "contour_field",
        "superformula_bloom",
        "attention_arcs",
        "residual_river",
        "weight_matrix",
        "attention_matrix",
    ],
)
def test_different_seed_differs(name):
    a = run_generator(name, BOUNDS, seed=1)
    b = run_generator(name, BOUNDS, seed=2)
    assert [c.to_gcode() for c in a] != [c.to_gcode() for c in b]


@pytest.mark.parametrize(
    "name",
    [
        "tiled_field",
        "ripple_field",
        "flow_field",
        "maze",
        "truchet",
        "wave_bands",
        "stipple",
        "waves_with_circles",
        "crosshatch_weave",
        "turning_weave",
        "wave_gradient",
        "interference_field",
        "frequency_lens",
        "hitomezashi",
        "harmonograph",
        "vortex_field",
        "moire_layers",
        "strange_attractor",
        "domain_warp",
        "contour_field",
        "superformula_bloom",
        "lissajous_carpet",
        "scribble_halftone",
        "comic_panels",
        "line_halftone",
        "scribble_portrait",
        "sparkle_grid",
        "iso_city",
        "rounded_circuits",
        "lissajous_swarm",
        "black_hole",
        "pe_carpet",
        "attention_arcs",
        "residual_river",
        "weight_matrix",
        "attention_matrix",
        "black_hole_bauhaus",
        "big_bang",
        "bauhaus_attractor",
        "bauhaus_attention",
        "bauhaus_weights",
        "bauhaus_gradient",
        "bauhaus_resonance",
    ],
)
def test_generator_within_bounds(name):
    x0, y0, x1, y1 = BOUNDS
    cmds = run_generator(name, BOUNDS, seed=7)
    for c in cmds:
        if c.x is not None:
            assert x0 - 0.5 <= c.x <= x1 + 0.5, f"{name} x={c.x} out of bounds"
        if c.y is not None:
            assert y0 - 0.5 <= c.y <= y1 + 0.5, f"{name} y={c.y} out of bounds"


def test_bauhaus_decision_deterministic_in_bounds():
    x0, y0, x1, y1 = BOUNDS
    a = run_generator("bauhaus_decision", BOUNDS, seed=7, colors=3)
    b = run_generator("bauhaus_decision", BOUNDS, seed=7, colors=3)
    assert a and b, "bauhaus_decision produced no commands"
    assert [c.to_gcode() for c in a] == [c.to_gcode() for c in b], "bauhaus_decision not deterministic"
    for c in a:
        if c.x is not None:
            assert x0 - 0.5 <= c.x <= x1 + 0.5, f"x={c.x} out of bounds"
        if c.y is not None:
            assert y0 - 0.5 <= c.y <= y1 + 0.5, f"y={c.y} out of bounds"


def test_colors_produce_layers():
    cmds = run_generator("tiled_field", BOUNDS, seed=5, colors=3)
    cfg = PromptPlotConfig()
    cfg.paper = PaperConfig.from_size("a5")
    cfg.color.enabled = True
    cfg.color.palette = ["black", "red", "blue"]
    prog = merge_chunks([cmds], cfg)
    layers = split_color_layers(prog)
    # at least 2 distinct color layers should appear
    assert len({c for c, _ in layers}) >= 2


def test_schema_introspection_skips_rng_bounds():
    schema = get_generator_schema("ripple_field")
    assert "rng" not in schema["params"] and "bounds" not in schema["params"]
    assert "wavelength" in schema["params"]
    assert schema["doc"]
    assert len(get_all_generator_schemas()) == len(list_generators())


def test_params_are_applied():
    few = run_generator("wave_bands", BOUNDS, seed=1, params={"bands": 3})
    many = run_generator("wave_bands", BOUNDS, seed=1, params={"bands": 20})
    assert len(many) > len(few)


def test_anaglyph_layers_duplicates_with_pen_tags():
    from promptplot.generative import SeededRNG, anaglyph_layers, run_generator

    cmds = run_generator("vortex_field", BOUNDS, seed=5, params={"line_count": 10})
    n = len(cmds)
    out = anaglyph_layers(cmds, SeededRNG(99), layers=2, glitch_bands=2, bounds=BOUNDS)
    assert len(out) == 2 * n
    pens = {c.color for c in out if c.command == "G1"}
    assert pens == {0, 1}
    # deterministic
    out2 = anaglyph_layers(cmds, SeededRNG(99), layers=2, glitch_bands=2, bounds=BOUNDS)
    assert [c.to_gcode() for c in out] == [c.to_gcode() for c in out2]
    # in bounds
    for c in out:
        if c.x is not None:
            assert BOUNDS[0] - 0.5 <= c.x <= BOUNDS[2] + 0.5


def _mk_gradient_png(tmp_path, name="grad.png", dark_left=True):
    PIL = pytest.importorskip("PIL.Image")
    img = PIL.new("L", (60, 40))
    for x in range(60):
        v = int(255 * (x / 59)) if dark_left else int(255 * (1 - x / 59))
        for y in range(40):
            img.putpixel((x, y), v)
    p = tmp_path / name
    img.save(p)
    return str(p)


def test_line_halftone_stays_inside_image_band(tmp_path):
    img = _mk_gradient_png(tmp_path)
    from promptplot.generative.generators import _image_tone_grid
    from promptplot.generative import SeededRNG

    rng = SeededRNG(3)
    gw, gh, off_x, off_y, _ = _image_tone_grid(SeededRNG(3), BOUNDS, img, 1.6, False)
    top = off_y + gh * 1.6
    cmds = run_generator("line_halftone", BOUNDS, seed=3, params={"image": img, "pitch": 1.6})
    assert cmds
    for c in cmds:
        if c.y is not None:
            assert c.y <= top + 0.6, f"command above image band: y={c.y} top={top}"


def test_line_halftone_dark_runs_are_multi_pass(tmp_path):
    img = _mk_gradient_png(tmp_path)
    cmds = run_generator("line_halftone", BOUNDS, seed=3, params={"image": img, "pitch": 1.6})
    # count distinct x positions per ~vertical stroke: dark side should produce
    # parallel passes offset by <1mm around some lines
    xs = sorted({c.x for c in cmds if c.command == "G0" and c.x is not None})
    close_pairs = sum(1 for a, b in zip(xs, xs[1:]) if 0.1 < b - a < 0.6)
    assert close_pairs >= 3, f"expected multi-pass offsets, close pairs={close_pairs}"


def test_sparkle_grid_spurs_never_overlap():
    cmds = run_generator("sparkle_grid", BOUNDS, seed=9, params={"fill": 1.0})
    # collect 2-point axis-aligned strokes (the spurs) grouped by their line
    horiz = {}
    vert = {}
    stroke = []
    for c in cmds:
        if c.command == "G0":
            stroke = [c]
        elif c.command == "G1":
            stroke.append(c)
        elif c.command == "M5" and len(stroke) == 2:
            a, b = stroke
            if a.y == b.y:
                horiz.setdefault(a.y, []).append(tuple(sorted((a.x, b.x))))
            elif a.x == b.x:
                vert.setdefault(a.x, []).append(tuple(sorted((a.y, b.y))))
    for groups in (horiz, vert):
        for key, ivs in groups.items():
            ivs = sorted(ivs)
            for (a1, b1), (a2, b2) in zip(ivs, ivs[1:]):
                assert a2 >= b1 - 0.01, f"overlapping spurs on line {key}: {(a1,b1)} vs {(a2,b2)}"


@pytest.mark.parametrize(
    "system",
    [
        "lorenz",
        "rossler",
        "halvorsen",
        "aizawa",
        "rabinovich_fabrikant",
        "chen",
        "newton_leipnik",
        "burke_shaw",
        "finance",
        "three_scroll",
        "qi",
    ],
)
def test_every_attractor_system_healthy(system):
    cmds = run_generator(
        "strange_attractor", BOUNDS, seed=5, params={"system": system, "steps": 6000}
    )
    a = [c.to_gcode() for c in cmds]
    b = [
        c.to_gcode()
        for c in run_generator(
            "strange_attractor", BOUNDS, seed=5, params={"system": system, "steps": 6000}
        )
    ]
    assert len(cmds) > 50, f"{system} produced too little"
    assert a == b, f"{system} not deterministic"
    for c in cmds:
        if c.x is not None:
            assert BOUNDS[0] - 0.5 <= c.x <= BOUNDS[2] + 0.5
        if c.y is not None:
            assert BOUNDS[1] - 0.5 <= c.y <= BOUNDS[3] + 0.5


def test_black_hole_retro80_smoke():
    a = run_generator(
        "black_hole",
        BOUNDS,
        seed=5,
        params=dict(
            mode="flow",
            bg_lines=8,
            backdrop="grid",
            stars=6,
            sun_slits=True,
            legend=True,
            glitch_strip=True,
            samples=40,
            n_iso=8,
            flow_rings=24,
        ),
    )
    b = run_generator(
        "black_hole",
        BOUNDS,
        seed=5,
        params=dict(
            mode="flow",
            bg_lines=8,
            backdrop="grid",
            stars=6,
            sun_slits=True,
            legend=True,
            glitch_strip=True,
            samples=40,
            n_iso=8,
            flow_rings=24,
        ),
    )
    assert a and [c.to_gcode() for c in a] == [c.to_gcode() for c in b]
    for c in a:
        if c.x is not None:
            assert BOUNDS[0] - 0.5 <= c.x <= BOUNDS[2] + 0.5
        if c.y is not None:
            assert BOUNDS[1] - 0.5 <= c.y <= BOUNDS[3] + 0.5


def test_shim_reexports_are_identities():
    """The bauhaus.py compat shim re-exports the SAME objects as the new homes."""
    from promptplot.generative import bauhaus, engine3d, kit
    from promptplot.generative.pieces import ml, physics as pieces_physics
    from promptplot.generative import physics as physics_shim

    assert bauhaus.bauhaus_memory is ml.bauhaus_memory
    assert bauhaus.type_block is kit.type_block
    assert bauhaus._zbuf_terrain is engine3d._zbuf_terrain
    assert physics_shim.gw150914 is pieces_physics.gw150914


def test_turning_weave_single_pass_ink():
    """Lane registry: no two drawn legs may ever be coincident (stacked ink)."""
    from collections import Counter

    for seed in (5, 8, 123):
        cmds = run_generator("turning_weave", BOUNDS, seed, colors=4)
        segs = Counter()
        prev = None
        for c in cmds:
            if c.command == "G1" and prev is not None:
                key = tuple(
                    sorted(
                        [
                            (round(prev[0], 2), round(prev[1], 2)),
                            (round(c.x, 2), round(c.y, 2)),
                        ]
                    )
                )
                segs[key] += 1
            prev = (c.x, c.y) if c.x is not None else (None if c.command == "M5" else prev)
        dups = [k for k, v in segs.items() if v > 1]
        assert not dups, f"seed {seed}: coincident legs {dups[:3]}"


def test_echo_layers_deterministic_and_penned():
    from promptplot.generative import SeededRNG, echo_layers

    base = run_generator("harmonograph", BOUNDS, 7)
    a = echo_layers(base, SeededRNG(1), copies=3, bounds=BOUNDS)
    b = echo_layers(base, SeededRNG(1), copies=3, bounds=BOUNDS)
    assert [c.to_gcode() for c in a] == [c.to_gcode() for c in b]
    pens = {c.color for c in a if c.command == "M3"}
    assert pens == {0, 1, 2}
    for c in a:
        if c.x is not None:
            assert BOUNDS[0] <= c.x <= BOUNDS[2] and BOUNDS[1] <= c.y <= BOUNDS[3]


def test_dash_rain_avoids_ink_and_is_deterministic():
    import math as _m

    from promptplot.generative import SeededRNG, dash_rain

    base = run_generator("superformula_bloom", BOUNDS, 3)
    a = dash_rain(base, SeededRNG(2), BOUNDS, clearance=2.0)
    b = dash_rain(base, SeededRNG(2), BOUNDS, clearance=2.0)
    assert [c.to_gcode() for c in a] == [c.to_gcode() for c in b]
    dashes = a[len(base):]
    assert dashes, "dash_rain added no dashes"
    # every dash endpoint keeps clearance from every base ink vertex
    ink = [
        (c.x, c.y) for c in base if c.command == "G1" and c.x is not None
    ]
    step = max(1, len(ink) // 400)
    ink = ink[::step]
    for c in dashes:
        if c.command == "G1" and c.x is not None:
            dmin = min(_m.hypot(c.x - px, c.y - py) for px, py in ink)
            assert dmin >= 0.9, f"dash at ({c.x},{c.y}) only {dmin:.2f}mm from ink"


def test_occlude_crossings_deterministic_and_cuts():
    from promptplot.generative import SeededRNG, echo_layers, occlude_crossings

    # occlusion only cuts where DIFFERENT pens cross → run after echo (multi-pen)
    base = run_generator("harmonograph", BOUNDS, 3)
    multi = echo_layers(base, SeededRNG(5), copies=3, bounds=BOUNDS)
    a = occlude_crossings(multi, gap=1.2)
    b = occlude_crossings(multi, gap=1.2)
    assert [c.to_gcode() for c in a] == [c.to_gcode() for c in b]
    n_m3_multi = sum(1 for c in multi if c.command == "M3")
    n_m3_out = sum(1 for c in a if c.command == "M3")
    assert n_m3_out > n_m3_multi  # cuts split polylines → more strokes

    # same-pen-only input must be left untouched (nothing is "on top")
    same = occlude_crossings(base, gap=1.2)
    assert sum(1 for c in same if c.command == "M3") == sum(
        1 for c in base if c.command == "M3"
    )


def test_glitch_slice_deterministic_and_penned():
    from promptplot.generative import SeededRNG, glitch_slice

    base = run_generator("harmonograph", BOUNDS, 3)
    a = glitch_slice(base, SeededRNG(1), BOUNDS, copies=2)
    b = glitch_slice(base, SeededRNG(1), BOUNDS, copies=2)
    assert [c.to_gcode() for c in a] == [c.to_gcode() for c in b]
    pens = {c.color for c in a if c.command == "M3"}
    assert pens == {0, 1}
    for c in a:
        if c.x is not None:
            assert BOUNDS[0] <= c.x <= BOUNDS[2]


def test_color_layers_never_drag_from_park():
    """GUARDRAIL: every color layer must position the pen (a travel coordinate)
    BEFORE its first M3, so streaming a layer alone can't drag from home."""
    from promptplot.config import PromptPlotConfig
    from promptplot.orchestrate import merge_chunks, split_color_layers, _first_drawn_point

    cfg = PromptPlotConfig()
    cfg.color.enabled = True
    cfg.color.palette = ["cyan", "magenta", "black"]
    raw = run_generator("bauhaus_gradient", BOUNDS, 19, colors=3)
    program = merge_chunks([raw], cfg)  # runs reorder_by_color
    layers = split_color_layers(program)
    assert len(layers) >= 2, "need a multi-color program to test the guardrail"

    # concatenating layers must reproduce the program exactly (no lost commands)
    flat = [c for _, cmds in layers for c in cmds]
    assert [c.to_gcode() for c in flat] == [c.to_gcode() for c in program.commands]

    for color, cmds in layers:
        # the first M3 must be preceded by a positioning coordinate in-layer
        idx_m3 = next((i for i, c in enumerate(cmds) if c.command == "M3"), None)
        if idx_m3 is None:
            continue
        assert _first_drawn_point(cmds) is not None, (
            f"color {color}: first stroke has no pen-up travel — would drag from park"
        )
        # and that positioning coordinate must appear before the first M3
        assert any(
            c.x is not None for c in cmds[:idx_m3]
        ), f"color {color}: M3 fires before any travel"


def test_stream_chunk_enforces_pen_state():
    """GUARDRAIL: stream_chunk lifts before a travel and lowers before a draw,
    even if the g-code violates the pen convention."""
    import asyncio
    from promptplot.models import GCodeCommand
    from promptplot.orchestrate import stream_chunk

    class _Rec:
        def __init__(self):
            self.sent = []
        async def send_command(self, g):
            self.sent.append(g)
            return True

    # deliberately broken order: draw with pen never lowered, then travel while down
    bad = [
        GCodeCommand(command="G1", x=10, y=10, f=500),   # draw with pen UP → must inject M3
        GCodeCommand(command="G0", x=50, y=50),          # travel with pen DOWN → must inject M5
        GCodeCommand(command="G1", x=60, y=60, f=500),   # draw again → inject M3
    ]
    rec = _Rec()
    asyncio.run(stream_chunk(bad, rec, verbose=False))
    seq = [g.split()[0] for g in rec.sent if g and g != "COMPLETE"]
    # first draw must be preceded by M3; the travel by M5
    assert seq[0] == "M3", seq
    assert "M5" in seq, seq
    i_travel = seq.index("G0")
    assert seq[i_travel - 1] in ("M5", "G4"), seq  # lifted (with optional settle) before travel

    # a correct chunk should NOT get spurious pen commands
    good = [
        GCodeCommand(command="M3", s=1000),
        GCodeCommand(command="G1", x=10, y=10, f=500),
        GCodeCommand(command="M5"),
        GCodeCommand(command="G0", x=50, y=50),
    ]
    rec2 = _Rec()
    asyncio.run(stream_chunk(good, rec2, verbose=False))
    assert [g.split()[0] for g in rec2.sent] == ["M3", "G1", "M5", "G0"], rec2.sent


def test_overlap_guardrail_thins_saturating_attractor():
    """The tip-width overlap guardrail (limit_ink_density max_passes=1) must
    deterministically thin a loop-saturating attractor and never grow it."""
    from promptplot.generative import limit_ink_density

    raw = run_generator("strange_attractor", BOUNDS, 3)
    a = limit_ink_density(raw, max_passes=1, cell=2.0)
    b = limit_ink_density(raw, max_passes=1, cell=2.0)
    assert [c.to_gcode() for c in a] == [c.to_gcode() for c in b], "not deterministic"
    assert 0 < len(a) < len(raw), "guardrail should reduce a saturating piece"


def test_enforce_line_spacing_prevents_crowding():
    """The line-crowding guardrail must be deterministic and actually enforce
    the minimum separation between non-consecutive drawn points (no black patch)."""
    import math as _m
    from promptplot.generative import enforce_line_spacing

    raw = run_generator("strange_attractor", BOUNDS, 3)
    md = 0.6
    a = enforce_line_spacing(raw, min_dist=md, lookback_mm=3.0, short_exempt=0.0)
    b = enforce_line_spacing(raw, min_dist=md, lookback_mm=3.0, short_exempt=0.0)
    assert [c.to_gcode() for c in a] == [c.to_gcode() for c in b], "not deterministic"

    # collect drawn points in order; a cell may not hold two points that are far
    # apart in draw order yet within min_dist (that would be a crowding violation)
    cell = md
    grid = {}
    idx = 0
    lookback = max(2, int(3.0 / 0.5))
    violations = 0
    for c in a:
        if c.command == "G1" and c.x is not None:
            ci, cj = int(c.x / cell), int(c.y / cell)
            for x in (ci - 1, ci, ci + 1):
                for y in (cj - 1, cj, cj + 1):
                    for px, py, pidx in grid.get((x, y), ()):
                        if idx - pidx > lookback and (px - c.x) ** 2 + (py - c.y) ** 2 < (md * md) * 0.8:
                            violations += 1
            grid.setdefault((ci, cj), []).append((c.x, c.y, idx))
            idx += 1
    # allow a tiny tolerance for resampling/rounding at run boundaries
    assert violations < idx * 0.02, f"{violations} crowding violations of {idx} points"


def test_geometry_clip_exact_and_inside():
    """Geometry engine: exact clip at line/circle, and the fully-inside case
    (regression for the HalfPlane interval-clamp bug that dropped inside runs)."""
    from promptplot.generative.geometry import Circle, Band, Rect, clip, offset

    line = [(-10.0, 0.0), (10.0, 0.0)]
    # exact stop on the circle radius
    out = clip(line, Circle(0, 0, 5), keep="outside")
    assert [[(round(x, 3), round(y, 3)) for x, y in r] for r in out] == [
        [(-10.0, 0.0), (-5.0, 0.0)],
        [(5.0, 0.0), (10.0, 0.0)],
    ]
    # union of bar-band and circle
    u = clip(line, Band("x", -3, 3) | Circle(0, 0, 5), keep="outside")
    assert len(u) == 2
    # REGRESSION: a segment fully inside a Rect must be kept whole (not dropped)
    inside = clip([(-8.0, 0.0), (8.0, 0.0)], Rect(-20, -20, 20, 20), keep="inside")
    assert inside == [[(-8.0, 0.0), (8.0, 0.0)]]
    # offset moves perpendicular
    assert offset([(0, 0), (10, 0)], 1.0) == [(0.0, 1.0), (10.0, 1.0)]


def test_occlude_weave_mode_cuts_both_pens():
    """Weave mode: deterministic, and the cuts land on MULTIPLE pens
    (sometimes one line yields, sometimes the other) — never same-pen cuts."""
    from collections import Counter

    from promptplot.generative import SeededRNG, echo_layers, occlude_crossings

    base = run_generator("harmonograph", BOUNDS, 3)
    multi = echo_layers(base, SeededRNG(5), copies=3, bounds=BOUNDS)
    a = occlude_crossings(multi, gap=1.2, mode="weave")
    b = occlude_crossings(multi, gap=1.2, mode="weave")
    assert [c.to_gcode() for c in a] == [c.to_gcode() for c in b]

    before = Counter(c.color for c in multi if c.command == "M3")
    after = Counter(c.color for c in a if c.command == "M3")
    grew = [p for p in before if after.get(p, 0) > before[p]]
    assert len(grew) >= 2, f"weave should cut >=2 pens, got {grew}"


def test_focal_void_clears_knot_keeps_heroes():
    """Engine artistic policy: focal_void clears the convergence disc, strokes
    stop on the rim, `keep` heroes pass through. Synthetic star: N lines
    through one centre."""
    import math as _m

    from promptplot.generative import focal_void
    from promptplot.models import GCodeCommand

    cx, cy, R = 70.0, 100.0, 40.0
    star = []
    for k in range(8):
        a = _m.pi * k / 8
        x0_, y0_ = cx - R * _m.cos(a), cy - R * _m.sin(a)
        x1_, y1_ = cx + R * _m.cos(a), cy + R * _m.sin(a)
        star.append(GCodeCommand(command="G0", x=x0_, y=y0_))
        star.append(GCodeCommand(command="M3", s=1000, color=k % 3))
        star.append(GCodeCommand(command="G1", x=x1_, y=y1_, f=1500, color=k % 3))
        star.append(GCodeCommand(command="M5"))

    a1 = focal_void(star, r=10.0, cx=cx, cy=cy, keep=2)
    a2 = focal_void(star, r=10.0, cx=cx, cy=cy, keep=2)
    assert [c.to_gcode() for c in a1] == [c.to_gcode() for c in a2]

    # count strokes whose sampled path enters the void
    def entering(cmds):
        n, cur, pos = 0, None, None
        for c in cmds:
            if c.command == "M3":
                cur = [pos] if pos else []
            elif c.command == "M5" and cur is not None:
                hit = False
                for p0, p1 in zip(cur, cur[1:]):
                    for t in range(21):
                        x = p0[0] + (p1[0] - p0[0]) * t / 20
                        y = p0[1] + (p1[1] - p0[1]) * t / 20
                        if _m.hypot(x - cx, y - cy) < 10.0 - 0.3:
                            hit = True
                n += 1 if hit else 0
                cur = None
            elif cur is not None and c.command == "G1" and c.x is not None:
                cur.append((c.x, c.y))
            if c.x is not None:
                pos = (c.x, c.y)
        return n

    assert entering(star) == 8
    assert entering(a1) == 2, "exactly the 2 heroes may cross the void"


def test_enforce_line_spacing_never_eats_glyphs():
    """Short strokes (stroke-font letters) are exempt from thinning — text must
    survive the guardrail verbatim (regression: broken letters on the MLP)."""
    from promptplot.generative import enforce_line_spacing
    from promptplot.generative.generators import _stroke_text

    text = _stroke_text("NONLINEAR TRANSFORMATION", 20.0, 100.0, 2.0, color=0, f=1500)
    kept = enforce_line_spacing(text, min_dist=0.45)
    assert [c.to_gcode() for c in kept] == [c.to_gcode() for c in text]
