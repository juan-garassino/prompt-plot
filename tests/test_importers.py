"""SVG + DXF import: parsing, color/layer grouping, fitting to paper."""

import pytest

from promptplot.config import PromptPlotConfig, PaperConfig
from promptplot.importers import parse_file, import_file
from promptplot.orchestrate import merge_chunks, split_color_layers

SVG_TWO_COLORS = """<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <line x1="10" y1="10" x2="90" y2="10" stroke="red"/>
  <polyline points="10,30 90,30 90,60" stroke="blue" fill="none"/>
  <rect x="20" y="70" width="40" height="20" stroke="red" fill="none"/>
</svg>
"""

DXF_TWO_LAYERS = """0
SECTION
2
ENTITIES
0
LINE
8
frame
10
0.0
20
0.0
11
50.0
21
0.0
0
LINE
8
detail
10
0.0
20
10.0
11
50.0
21
40.0
0
LWPOLYLINE
8
frame
10
0.0
20
0.0
10
50.0
20
0.0
10
50.0
20
50.0
0
ENDSEC
0
EOF
"""


def _cfg():
    cfg = PromptPlotConfig()
    cfg.paper = PaperConfig.from_size("a5")
    return cfg


def test_parse_svg_groups_by_stroke_color(tmp_path):
    f = tmp_path / "two.svg"
    f.write_text(SVG_TWO_COLORS)
    result = parse_file(str(f))
    assert result.y_down is True
    colors = {p.color for p in result.paths}
    assert "red" in colors and "blue" in colors
    # 3 shapes: line, polyline, rect
    assert len(result.paths) == 3


def test_import_svg_builds_color_layers(tmp_path):
    f = tmp_path / "two.svg"
    f.write_text(SVG_TWO_COLORS)
    cfg = _cfg()
    commands, palette, _ = import_file(str(f), cfg, group_by="color")
    assert set(palette) == {"red", "blue"}
    cfg.color.enabled = True
    cfg.color.palette = palette
    prog = merge_chunks([commands], cfg)
    layers = split_color_layers(prog)
    assert len({c for c, _ in layers}) == 2


def test_import_fits_within_drawable_area(tmp_path):
    f = tmp_path / "two.svg"
    f.write_text(SVG_TWO_COLORS)
    cfg = _cfg()
    commands, _, _ = import_file(str(f), cfg, fit=True)
    dx0, dy0, dx1, dy1 = cfg.paper.get_drawable_area()
    for c in commands:
        if c.x is not None:
            assert dx0 - 0.5 <= c.x <= dx1 + 0.5
        if c.y is not None:
            assert dy0 - 0.5 <= c.y <= dy1 + 0.5


def test_parse_dxf_groups_by_layer(tmp_path):
    f = tmp_path / "two.dxf"
    f.write_text(DXF_TWO_LAYERS)
    result = parse_file(str(f))
    assert result.y_down is False
    layers = {p.layer for p in result.paths}
    assert "frame" in layers and "detail" in layers


def test_import_dxf_layer_grouping(tmp_path):
    f = tmp_path / "two.dxf"
    f.write_text(DXF_TWO_LAYERS)
    cfg = _cfg()
    commands, palette, _ = import_file(str(f), cfg, group_by="layer")
    assert set(palette) == {"frame", "detail"}
    assert any(c.command == "G1" for c in commands)


# --- the oracle-drawing shape: layered groups, group stroke, Beziers, mm viewBox ---

SVG_ORACLE_STYLE = """<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     width="297mm" height="420mm" viewBox="0 0 297 420">
  <g id="01_black" inkscape:groupmode="layer" inkscape:label="01 | black | 0.10 mm"
     fill="none" stroke="#16191b" stroke-width="0.1">
    <path d="M 10,10 L 90,10" />
    <path d="M 10,50 C 30,10 70,10 90,50" />
  </g>
  <g id="02_red" inkscape:groupmode="layer" inkscape:label="02 | red | 0.50 mm"
     fill="none" stroke="#cb292a" stroke-width="0.5">
    <path d="M 10,100 Q 50,60 90,100 T 170,100" />
    <path d="M 100,10 c 20,-40 60,-40 80,0 s 40,40 80,0" />
  </g>
</svg>
"""


def test_svg_group_inherited_stroke_and_inkscape_layer(tmp_path):
    f = tmp_path / "oracle.svg"
    f.write_text(SVG_ORACLE_STYLE)
    r = parse_file(str(f))
    assert len(r.paths) == 4
    by_layer = {}
    for p in r.paths:
        by_layer.setdefault(p.layer, set()).add(p.color)
    assert by_layer == {
        "01 | black | 0.10 mm": {"#16191b"},
        "02 | red | 0.50 mm": {"#cb292a"},
    }


def test_svg_cubic_bezier_is_flattened_not_chorded(tmp_path):
    f = tmp_path / "curve.svg"
    f.write_text(SVG_ORACLE_STYLE)
    r = parse_file(str(f))
    curve = [p for p in r.paths if p.layer.startswith("01") and len(p.points) > 2][0]
    assert len(curve.points) >= 9  # the 8-step floor, never a 2-point chord
    assert curve.points[0] == (10.0, 50.0)
    assert curve.points[-1] == (90.0, 50.0)
    # the curve bows toward its control points (y decreases toward 10) — a chord would stay at 50
    assert min(y for _, y in curve.points) < 40.0
    # and it is symmetric about x = 50
    ys = [y for _, y in curve.points]
    assert ys == pytest.approx(ys[::-1], abs=1e-9)


def test_svg_quadratic_smooth_and_relative_curves(tmp_path):
    f = tmp_path / "curve.svg"
    f.write_text(SVG_ORACLE_STYLE)
    r = parse_file(str(f))
    red = [p for p in r.paths if p.layer.startswith("02")]
    qt = [p for p in red if p.points[0] == (10.0, 100.0)][0]
    assert qt.points[-1] == pytest.approx((170.0, 100.0))
    assert len(qt.points) > 10
    cs = [p for p in red if p.points[0] == (100.0, 10.0)][0]
    assert cs.points[-1] == pytest.approx((260.0, 10.0))  # relative c then s, back to baseline


def test_svg_reads_viewbox_and_physical_units(tmp_path):
    f = tmp_path / "oracle.svg"
    f.write_text(SVG_ORACLE_STYLE)
    r = parse_file(str(f))
    assert r.viewbox == (0.0, 0.0, 297.0, 420.0)
    assert r.unit_scale == pytest.approx(1.0)  # 297mm across 297 units

    g = tmp_path / "px.svg"
    g.write_text(SVG_TWO_COLORS)  # width="100" (px) viewBox 0 0 100 100
    r2 = parse_file(str(g))
    assert r2.viewbox == (0.0, 0.0, 100.0, 100.0)
    assert r2.unit_scale == pytest.approx(25.4 / 96.0)


def test_import_no_fit_is_mm_native_when_page_is_declared(tmp_path):
    f = tmp_path / "oracle.svg"
    f.write_text(SVG_ORACLE_STYLE)
    cfg = _cfg()
    cfg.paper = PaperConfig.from_size("a3", "portrait")
    commands, palette, r = import_file(str(f), cfg, group_by="layer", fit=False)
    assert palette == ["01 | black | 0.10 mm", "02 | red | 0.50 mm"]
    # the straight black line M10,10 L90,10 must land at x 10..90 and y = 420-10 = 410:
    # page origin honoured, y flipped within the PAGE, no recentring.
    xs = [c.x for c in commands if c.x is not None]
    assert min(xs) == pytest.approx(10.0, abs=1e-6)
    # (the relative cubic bows above the page to y≈-20, i.e. ~440 mm after the
    # flip — that is correct passthrough, so no global max-y assertion here)
    line_pts = [(c.x, c.y) for c in commands[:4] if c.x is not None]
    assert line_pts[0] == pytest.approx((10.0, 410.0))
    assert line_pts[1] == pytest.approx((90.0, 410.0))


def test_import_no_fit_without_viewbox_falls_back_to_legacy_centring(tmp_path):
    svg = SVG_TWO_COLORS.replace(' viewBox="0 0 100 100"', "")
    f = tmp_path / "novb.svg"
    f.write_text(svg)
    cfg = _cfg()
    commands, _, r = import_file(str(f), cfg, fit=False)
    assert r.viewbox is None
    # legacy: scale 1, centred in the a5 drawable area — must NOT sit at the raw coordinates
    dx0, dy0, dx1, dy1 = cfg.paper.get_drawable_area()
    xs = [c.x for c in commands if c.x is not None]
    assert dx0 <= min(xs) and max(xs) <= dx1
