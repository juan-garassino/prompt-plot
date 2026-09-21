"""SVG → ImportResult.

Groups paths by stroke color (or Inkscape layer). The stdlib parser handles
line/polyline/polygon/rect/circle/ellipse, path data including cubic and
quadratic Beziers (flattened exactly, via the engine's ``bezier_flatten``),
group-inherited stroke colour, Inkscape layers, and the page ``viewBox`` +
physical width so an import can be mm-native.
"""

from __future__ import annotations

import math
import re
import xml.etree.ElementTree as ET
from typing import List, Optional

from .layers import ImportedPath, ImportResult

_NUM = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")


def _local(tag: str) -> str:
    return tag.split("}")[-1]


def _stroke_of(el, inherited: str) -> str:
    stroke = el.get("stroke")
    style = el.get("style", "")
    if not stroke and "stroke:" in style:
        m = re.search(r"stroke:\s*([^;]+)", style)
        if m:
            stroke = m.group(1).strip()
    if not stroke or stroke.lower() == "none":
        return inherited
    return stroke.strip()


def _points_attr(s: str) -> List:
    nums = [float(n) for n in _NUM.findall(s)]
    return [(nums[i], nums[i + 1]) for i in range(0, len(nums) - 1, 2)]


def _circle(cx, cy, r, n=48):
    return [
        (cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n))
        for k in range(n + 1)
    ]


def _ellipse(cx, cy, rx, ry, n=48):
    return [
        (cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n))
        for k in range(n + 1)
    ]


def _parse_path_d(d: str, max_seg: float = 2.0) -> List[List]:
    """Parse an SVG path 'd' into polylines.

    Line commands (M/L/H/V/Z) are exact. Cubic (C/S) and quadratic (Q/T) Beziers
    are flattened with ``bezier_flatten`` at ``max_seg`` user units per step —
    the oracle drawings are 80k+ cubic segments, and keeping only their
    endpoints (the old behaviour) turned every brush stroke into a chord.
    Elliptical arcs (A) are still approximated by their chord; no oracle uses them.
    """
    from ..generative.engine.geometry import bezier_flatten

    tokens = re.findall(r"[MmLlHhVvCcSsQqTtAaZz]|[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", d)
    polylines: List[List] = []
    cur: List = []
    x = y = 0.0
    start = (0.0, 0.0)
    last_ctrl = None  # previous curve's last control point, for S/T reflection
    last_kind = None  # "C" or "Q" — reflection only applies to the same family
    i = 0
    cmd = None

    def nxt():
        nonlocal i
        v = float(tokens[i])
        i += 1
        return v

    def pt(rel: bool):
        px, py = nxt(), nxt()
        return (x + px, y + py) if rel else (px, py)

    def extend_curve(ctrl):
        # flatten and append everything but the first point (already in cur)
        cur.extend(bezier_flatten(ctrl, max_seg=max_seg)[1:])

    while i < len(tokens):
        t = tokens[i]
        if t.isalpha():
            cmd = t
            i += 1
        rel = cmd.islower()
        c = cmd.upper()
        if c == "M":
            if cur:
                polylines.append(cur)
            x, y = pt(rel)
            start = (x, y)
            cur = [(x, y)]
            cmd = "l" if rel else "L"  # subsequent implicit lineto
            last_kind = None
        elif c == "L":
            x, y = pt(rel)
            cur.append((x, y))
            last_kind = None
        elif c == "H":
            px = nxt()
            x = x + px if rel else px
            cur.append((x, y))
            last_kind = None
        elif c == "V":
            py = nxt()
            y = y + py if rel else py
            cur.append((x, y))
            last_kind = None
        elif c == "C":
            p0 = (x, y)
            c1 = pt(rel)
            c2 = pt(rel)
            end = pt(rel)
            extend_curve([p0, c1, c2, end])
            x, y = end
            last_ctrl, last_kind = c2, "C"
        elif c == "S":
            p0 = (x, y)
            c1 = (2 * x - last_ctrl[0], 2 * y - last_ctrl[1]) if last_kind == "C" else p0
            c2 = pt(rel)
            end = pt(rel)
            extend_curve([p0, c1, c2, end])
            x, y = end
            last_ctrl, last_kind = c2, "C"
        elif c == "Q":
            p0 = (x, y)
            c1 = pt(rel)
            end = pt(rel)
            extend_curve([p0, c1, end])
            x, y = end
            last_ctrl, last_kind = c1, "Q"
        elif c == "T":
            p0 = (x, y)
            c1 = (2 * x - last_ctrl[0], 2 * y - last_ctrl[1]) if last_kind == "Q" else p0
            end = pt(rel)
            extend_curve([p0, c1, end])
            x, y = end
            last_ctrl, last_kind = c1, "Q"
        elif c == "A":
            for _ in range(5):
                nxt()  # rx ry rotation large-arc sweep
            x, y = pt(rel)
            cur.append((x, y))
            last_kind = None
        elif c == "Z":
            if cur:
                cur.append(start)
                polylines.append(cur)
                cur = []
            x, y = start
            last_kind = None
        else:
            i += 1
    if cur:
        polylines.append(cur)
    return polylines


_UNIT_MM = {"mm": 1.0, "cm": 10.0, "in": 25.4, "pt": 25.4 / 72.0, "pc": 25.4 / 6.0,
            "px": 25.4 / 96.0, "": 25.4 / 96.0}


def _page_geometry(root):
    """(viewbox, mm_per_unit) from the root element, or (None, None).

    ``width="297mm" viewBox="0 0 297 420"`` → 1 mm per unit. Unitless or px
    widths are read at CSS 96 dpi. Without a viewBox nothing is knowable.
    """
    vb = root.get("viewBox")
    if not vb:
        return None, None
    nums = [float(n) for n in _NUM.findall(vb)]
    if len(nums) != 4 or nums[2] <= 0 or nums[3] <= 0:
        return None, None
    viewbox = (nums[0], nums[1], nums[2], nums[3])
    w = root.get("width", "")
    m = re.fullmatch(r"\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*([a-zA-Z%]*)\s*", w or "")
    if not m or m.group(2) == "%":
        return viewbox, None
    unit = m.group(2).lower()
    if unit not in _UNIT_MM:
        return viewbox, None
    return viewbox, float(m.group(1)) * _UNIT_MM[unit] / viewbox[2]


def _parse_stdlib(path: str):
    """-> (paths, viewbox, unit_scale). Walks <g> so a stroke or Inkscape layer
    set on the group is inherited by every path inside it."""
    tree = ET.parse(path)
    root = tree.getroot()
    viewbox, unit_scale = _page_geometry(root)
    out: List[ImportedPath] = []

    def walk(el, layer: str, stroke: str):
        tag = _local(el.tag)
        if tag == "g":
            # Inkscape layer?
            label = None
            for k, v in el.attrib.items():
                if k.endswith("label"):
                    label = v
            if (
                el.get("{http://www.inkscape.org/namespaces/inkscape}groupmode") == "layer"
                and label
            ):
                layer = label
            stroke = _stroke_of(el, stroke)
            for child in el:
                walk(child, layer, stroke)
            return

        s = _stroke_of(el, stroke)
        polys: List[List] = []
        if tag == "line":
            polys = [
                [
                    (float(el.get("x1", 0)), float(el.get("y1", 0))),
                    (float(el.get("x2", 0)), float(el.get("y2", 0))),
                ]
            ]
        elif tag in ("polyline", "polygon"):
            pts = _points_attr(el.get("points", ""))
            if tag == "polygon" and pts:
                pts = pts + [pts[0]]
            polys = [pts]
        elif tag == "rect":
            x, y = float(el.get("x", 0)), float(el.get("y", 0))
            w, h = float(el.get("width", 0)), float(el.get("height", 0))
            polys = [[(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]]
        elif tag == "circle":
            polys = [_circle(float(el.get("cx", 0)), float(el.get("cy", 0)), float(el.get("r", 0)))]
        elif tag == "ellipse":
            polys = [
                _ellipse(
                    float(el.get("cx", 0)),
                    float(el.get("cy", 0)),
                    float(el.get("rx", 0)),
                    float(el.get("ry", 0)),
                )
            ]
        elif tag == "path":
            polys = _parse_path_d(el.get("d", ""))

        for poly in polys:
            if len(poly) >= 2:
                out.append(ImportedPath(points=poly, color=s, layer=layer))

        for child in el:
            walk(child, layer, s)

    walk(root, "default", "black")
    return out, viewbox, unit_scale


def _parse_svgpathtools(path: str, samples: int = 24) -> Optional[List[ImportedPath]]:
    """Opt-in alternative parser. NOT the default: it ignores group-inherited
    stroke and Inkscape layers (every path comes back ``layer="default"``) and
    samples every subpath at a fixed 24 points regardless of length. The stdlib
    parser now flattens Beziers itself, so this has no remaining advantage."""
    try:
        from svgpathtools import svg2paths2
    except ImportError:
        return None
    paths, attrs, _svg_attr = svg2paths2(path)
    out: List[ImportedPath] = []
    for p, attr in zip(paths, attrs):
        stroke = attr.get("stroke", "black") or "black"
        style = attr.get("style", "")
        if "stroke:" in style:
            m = re.search(r"stroke:\s*([^;]+)", style)
            if m:
                stroke = m.group(1).strip()
        for sub in p.continuous_subpaths():
            pts = [
                (sub.point(k / samples).real, sub.point(k / samples).imag)
                for k in range(samples + 1)
            ]
            out.append(ImportedPath(points=pts, color=stroke, layer="default"))
    return out


def parse_svg(path: str, prefer_lib: bool = False) -> ImportResult:
    """Parse an SVG file into an ImportResult (paths grouped by stroke color).

    The stdlib parser is the default: it honours group-inherited stroke,
    Inkscape layers, Bezier curves and the page viewBox. ``prefer_lib=True``
    uses svgpathtools when installed, losing layers and group colour.
    """
    if prefer_lib:
        paths = _parse_svgpathtools(path)
        if paths:
            return ImportResult(paths=paths, y_down=True, source=path)
    paths, viewbox, unit_scale = _parse_stdlib(path)
    return ImportResult(
        paths=paths, y_down=True, source=path, viewbox=viewbox, unit_scale=unit_scale
    )
