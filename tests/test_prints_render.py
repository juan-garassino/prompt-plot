"""scripts/prints_render.py — clean SVG, WebP thumbs and a technical plate from gcode.

The gcode shape (provenance header + ``; color=N`` tagged layers, M3/M5 pen
state, G0 travel, G1 draw) is the one scripts/render_candidate.py:main writes
(header at L140-156); the stroke state machine follows
studio/millennium-p-vs-np/rounds/r03/render_truewidth.py:parse.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pytest
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import prints_render as pr  # noqa: E402

HEADER = """\
; promptplot render
; piece     /abs/studio/demo/rounds/r02/piece.py
; function  demo
; seed      7
; paper     {paper}
; pens      goldenrod,dodgerblue,forestgreen,crimson,darkviolet,black
; colors    6
; rendered  2026-09-29T04:37:03
; commands  96753
"""

TINY = """\
; promptplot render
; paper     a4 portrait
; pens      black,gold
M5
G4 P0.2 ; pen up dwell
G0 X10 Y20
M3 S1000 ; color=0
G1 X30 Y20 F2200 ; color=0
G1 X30 Y40 F2200 ; color=0
M5
; color=1
G0 X50.004 Y60
M3 S1000
G1 X70.126 Y80.5 F2200
M5
"""

TINY_POLYS = {
    0: [[(10.0, 20.0), (30.0, 20.0), (30.0, 40.0)]],
    1: [[(50.004, 60.0), (70.126, 80.5)]],
}

TINY_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100mm" height="100mm">\n'
    '<path d="M 10.00 80.00 L 30.00 80.00 30.00 60.00" fill="none" stroke="#000000" '
    'stroke-width="0.35" stroke-linecap="round" stroke-linejoin="round"/>\n'
    '<path d="M 50.00 40.00 L 70.13 19.50" fill="none" stroke="#d4af37" '
    'stroke-width="0.5" stroke-linecap="round" stroke-linejoin="round"/>\n'
    "</svg>\n"
)

CREAM = (244, 239, 228)


def _write(tmp_path: Path, text: str, name: str = "p.gcode") -> Path:
    p = tmp_path / name
    p.write_text(text)
    return p


# ---------------------------------------------------------------- parse_header


@pytest.mark.parametrize(
    "paper, expected",
    [
        ("a4 portrait", {"size": "a4", "orientation": "portrait", "margin_mm": 10}),
        ("24x30 portrait", {"size": "24x30", "orientation": "portrait", "margin_mm": 10}),
        (
            "a3 portrait, margin 15",
            {"size": "a3", "orientation": "portrait", "margin_mm": 15},
        ),
    ],
)
def test_parse_header_paper_shapes(tmp_path, paper, expected):
    head = pr.parse_header(_write(tmp_path, HEADER.format(paper=paper) + "M5\n"))
    assert head == {
        "piece": "/abs/studio/demo/rounds/r02/piece.py",
        "function": "demo",
        "seed": 7,
        "paper": expected,
        "pens": ["goldenrod", "dodgerblue", "forestgreen", "crimson", "darkviolet", "black"],
        "colors": 6,
        "rendered": "2026-09-29T04:37:03",
        "commands": 96753,
    }


def test_parse_header_without_provenance_is_none(tmp_path):
    assert pr.parse_header(_write(tmp_path, "M5\nG0 X1 Y2\n")) is None


def test_paper_mm_uses_paper_config():
    assert pr.paper_mm("a4", "portrait") == (210.0, 297.0)
    assert pr.paper_mm("a3", "landscape") == (420.0, 297.0)
    assert pr.paper_mm("24x30", "portrait") == (240.0, 300.0)


# ------------------------------------------------------------- parse_polylines


def test_parse_polylines_two_pens(tmp_path):
    assert pr.parse_polylines(_write(tmp_path, TINY)) == TINY_POLYS


def test_parse_polylines_defaults_to_pen_zero(tmp_path):
    g = "G0 X1 Y2\nM3\nG1 X3 Y4\nM5\n"
    assert pr.parse_polylines(_write(tmp_path, g)) == {0: [[(1.0, 2.0), (3.0, 4.0)]]}


# --------------------------------------------------------------------- pen_css


def test_pen_css_aliases_names_and_unknown(caplog):
    assert pr.pen_css("gold") == "#d4af37"
    assert pr.pen_css("Copper") == "#b87333"
    assert pr.pen_css("dodgerblue") == "#1e90ff"
    with caplog.at_level(logging.WARNING, logger="prints_render"):
        assert pr.pen_css("not-a-pen") == "#000000"
    assert "not-a-pen" in caplog.text


# --------------------------------------------------------------------- writers


def test_write_svg_is_byte_exact(tmp_path):
    out = tmp_path / "p.svg"
    n = pr.write_svg(TINY_POLYS, ["black", "gold"], 100.0, 100.0, {1: 0.5}, out)
    assert out.read_text() == TINY_SVG
    assert n == len(TINY_SVG.encode())
    assert "<rect" not in TINY_SVG


def test_write_svg_is_deterministic_and_sorts_pens(tmp_path):
    shuffled = {1: TINY_POLYS[1], 0: TINY_POLYS[0]}
    a, b = tmp_path / "a.svg", tmp_path / "b.svg"
    pr.write_svg(shuffled, ["black", "gold"], 100.0, 100.0, {1: 0.5}, a)
    pr.write_svg(TINY_POLYS, ["black", "gold"], 100.0, 100.0, {1: 0.5}, b)
    assert a.read_bytes() == b.read_bytes()


def test_write_thumb_keeps_aspect_and_draws_on_cream(tmp_path):
    w_mm, h_mm = pr.paper_mm("a4", "portrait")
    polys = {0: [[(20.0, 150.0), (190.0, 150.0)]]}
    out = tmp_path / "t.webp"
    size = pr.write_thumb(polys, ["black"], w_mm, h_mm, {0: 10.0}, out, long_edge=64)
    assert size == (45, 64)
    with Image.open(out) as im:
        assert im.format == "WEBP"
        assert im.size == (45, 64)
        rgb = im.convert("RGB")
        k = 64 / 297
        on_stroke = rgb.getpixel((round(100 * k), round((297 - 150) * k)))
        corner = rgb.getpixel((1, 1))
    assert on_stroke != CREAM and sum(on_stroke) < 300
    assert all(abs(a - b) <= 4 for a, b in zip(corner, CREAM))  # webp is lossy


def test_write_raster_is_the_large_thumb(tmp_path):
    out = tmp_path / "r.webp"
    size = pr.write_raster(TINY_POLYS, ["black", "gold"], 100.0, 50.0, {}, out, long_edge=80)
    assert size == (80, 40)
    with Image.open(out) as im:
        assert im.size == (80, 40)


def test_write_technical_produces_a_webp(tmp_path):
    pytest.importorskip("matplotlib", reason="technical plate needs matplotlib")
    out = tmp_path / "tech.webp"
    pr.write_technical(TINY_POLYS, ["black", "gold"], 100.0, 100.0, {1: 0.5}, out, dpi=50)
    assert out.stat().st_size > 0
    with Image.open(out) as im:
        assert im.format == "WEBP"
        side = round((100 + 24) / 25.4 * 50)
        assert abs(im.size[0] - side) <= 1 and abs(im.size[1] - side) <= 1


def test_write_photo_transposes_and_resizes(tmp_path):
    src = tmp_path / "photo.jpg"
    Image.new("RGB", (400, 200), (120, 30, 30)).save(src, "JPEG")
    out = tmp_path / "photo.webp"
    assert pr.write_photo(src, out, long_edge=100) == (100, 50)
    with Image.open(out) as im:
        assert im.format == "WEBP" and im.size == (100, 50)
