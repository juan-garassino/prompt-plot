"""Site-ready renders of a PromptPlot gcode: clean SVG, WebP thumbs, technical plate.

The gallery PNGs are matplotlib previews wearing chart chrome (title, stats
box, travel lines, dashed frames) — useful for judging a plate, wrong as
artwork. The portfolio site wants three things instead, all built here from the
gcode itself:

* ``write_svg``       — a clean vector sheet, one ``<path>`` per pen, no
  background (the site supplies the cream paper);
* ``write_thumb`` / ``write_raster`` — anti-aliased WebP on cream, the raster
  being the fallback when an SVG is too heavy to ship;
* ``write_technical`` — a hi-res plate that keeps only the mm axes and a legend
  with the real pen names and colours.

Pure functions, no gallery globals: scripts/prints_export.py orchestrates.
The sheet for a plate is ``paper_mm(size, orientation)`` from its header,
then ``fit_sheet(polys, w, h)``: plates rendered before
``PaperConfig.from_size`` normalised custom sizes (2026-09-21) were drawn on
the transposed sheet (``42x24 landscape`` on 240x420), and ``fit_sheet``
swaps the sheet back when only the transposed one holds the strokes.
Outputs are deterministic (sorted pens, fixed float formatting) so the tests
can compare bytes.

The gcode shape is the one scripts/render_candidate.py:main writes — a
``; promptplot render`` provenance header, ``; color=N`` tagged layers, M3 pen
down, M5 pen up, G0 travel, G1 draw.
"""

from __future__ import annotations

import io
import logging
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

from promptplot.config import PaperConfig
from promptplot.visualizer import GCodeVisualizer

logger = logging.getLogger(__name__)

RENDER_VERSION = 1

MAGIC = "; promptplot render"
CREAM = (244, 239, 228)
DEFAULT_WIDTH_MM = 0.35
DEFAULT_MARGIN_MM = 10
TECH_MARGIN_MM = 12.0
SHEET_TOLERANCE_MM = 0.01

Polylines = dict[int, list[list[tuple[float, float]]]]

_COLOR_TAG = re.compile(r"color=(\d+)")
_AXIS = re.compile(r"([XY])(-?\d+(?:\.\d+)?)")


# ----------------------------------------------------------------------- parse


def _num(text: str) -> int | float:
    v = float(text)
    return int(v) if v.is_integer() else v


def _parse_paper(value: str) -> dict:
    """``a4 portrait`` / ``24x30 portrait`` / ``a3 portrait, margin 15``."""
    main, _, rest = value.partition(",")
    size, _, orientation = main.strip().partition(" ")
    margin: int | float = DEFAULT_MARGIN_MM
    m = re.search(r"margin\s+(\d+(?:\.\d+)?)", rest)
    if m:
        margin = _num(m.group(1))
    return {
        "size": size.strip().lower(),
        "orientation": orientation.strip().lower() or "portrait",
        "margin_mm": margin,
    }


def parse_header(path: Path) -> dict | None:
    """The provenance header, or ``None`` when the file does not carry one."""
    fields: dict[str, str] = {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        # round-local wrappers annotate the magic line:
        # "; promptplot render (round-local wrapper: F600, G4 P1.0 pen dwells)"
        if not fh.readline().startswith(MAGIC):
            return None
        for line in fh:
            if not line.startswith(";"):
                break
            key, _, value = line[1:].strip().partition(" ")
            fields[key] = value.strip()
    return {
        "piece": fields.get("piece", ""),
        "function": fields.get("function", ""),
        "seed": int(fields["seed"]) if fields.get("seed") else None,
        "paper": _parse_paper(fields.get("paper", "a4 portrait")),
        "pens": [p.strip() for p in fields.get("pens", "").split(",") if p.strip()],
        "colors": int(fields["colors"]) if fields.get("colors") else None,
        "rendered": fields.get("rendered", ""),
        "commands": int(fields["commands"]) if fields.get("commands") else None,
    }


def paper_mm(size: str, orientation: str) -> tuple[float, float]:
    """(width, height) of the sheet in mm."""
    paper = PaperConfig.from_size(size, orientation)
    return (float(paper.width), float(paper.height))


def fit_sheet(polys: Polylines, w_mm: float, h_mm: float) -> tuple[float, float]:
    """The sheet the strokes were actually drawn on: (w, h), or (h, w) when the
    strokes overflow (w, h) but fit the transposed sheet — a plate rendered
    before ``PaperConfig.from_size`` normalised custom sizes. Logs a warning
    when it transposes; a plate that fits neither way keeps (w, h)."""
    pts = [pt for lines in polys.values() for poly in lines for pt in poly]
    if not pts:
        return (w_mm, h_mm)
    eps = SHEET_TOLERANCE_MM
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)

    def fits(w: float, h: float) -> bool:
        return x0 >= -eps and y0 >= -eps and x1 <= w + eps and y1 <= h + eps

    if not fits(w_mm, h_mm) and fits(h_mm, w_mm):
        logger.warning(
            "strokes (x %.1f-%.1f, y %.1f-%.1f) overflow the %gx%g sheet but fit "
            "%gx%g: transposing (plate predates the paper-size normalisation)",
            x0, x1, y0, y1, w_mm, h_mm, h_mm, w_mm,
        )
        return (h_mm, w_mm)
    return (w_mm, h_mm)


def parse_polylines(path: Path) -> Polylines:
    """Pen index -> drawn polylines, in plotter coordinates (Y up).

    A ``color=N`` tag anywhere on a line (inline on M3/G1, or a bare comment
    line) selects the pen; pen 0 until the first tag. M3 starts a stroke at the
    current position, G1 extends it while the pen is down, M5 ends it. G0 is
    travel and never draws. Strokes with no G1 (a bare dip) are dropped.
    """
    polys: Polylines = {}
    pen, stroke_pen, down = 0, 0, False
    x = y = 0.0
    stroke: list[tuple[float, float]] | None = None

    def close() -> None:
        nonlocal stroke
        if stroke is not None and len(stroke) > 1:
            polys.setdefault(stroke_pen, []).append(stroke)
        stroke = None

    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            code, _, comment = line.partition(";")
            tag = _COLOR_TAG.search(comment)
            if tag:
                pen = int(tag.group(1))
            word = code.split(maxsplit=1)[0].upper() if code.strip() else ""
            if word == "M3":
                close()
                down, stroke, stroke_pen = True, [(x, y)], pen
            elif word == "M5":
                close()
                down = False
            elif word in ("G0", "G1"):
                for axis, val in _AXIS.findall(code):
                    if axis == "X":
                        x = float(val)
                    else:
                        y = float(val)
                if word == "G1" and down and stroke is not None:
                    stroke.append((x, y))
                elif down:  # travel with the pen down: restart, never draw it
                    close()
                    stroke, stroke_pen = [(x, y)], pen
    close()
    return polys


# ------------------------------------------------------------------------ pens


def pen_css(name: str) -> str:
    """Hex colour of a pen name: metallic aliases first, then matplotlib."""
    from matplotlib.colors import to_hex

    key = name.strip().lower()
    alias = GCodeVisualizer._COLOR_ALIASES.get(key)
    if alias:
        return alias
    try:
        return to_hex(key)
    except ValueError:
        logger.warning("unknown pen colour %r — drawing it black", name)
        return "#000000"


def _pen_name(pens: list[str], idx: int) -> str:
    if 0 <= idx < len(pens):
        return pens[idx]
    logger.warning("pen index %d outside the %d header pens — drawing it black", idx, len(pens))
    return "black"


def _fmt(v: float) -> str:
    return f"{round(v, 2) + 0.0:.2f}"  # + 0.0 folds -0.00 into 0.00


# --------------------------------------------------------------------- writers


def write_svg(
    polys: Polylines,
    pens: list[str],
    w_mm: float,
    h_mm: float,
    widths_mm: dict[int, float],
    out: Path,
) -> int:
    """One ``<path>`` per pen (sorted), Y flipped to SVG, no background. Bytes written."""
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_mm:g} {h_mm:g}" '
        f'width="{w_mm:g}mm" height="{h_mm:g}mm">'
    ]
    for idx in sorted(polys):
        subpaths = []
        for poly in polys[idx]:
            pts = [f"{_fmt(px)} {_fmt(h_mm - py)}" for px, py in poly]
            subpaths.append(f"M {pts[0]} L {' '.join(pts[1:])}")
        if not subpaths:
            continue
        width = widths_mm.get(idx, DEFAULT_WIDTH_MM)
        lines.append(
            f'<path d="{" ".join(subpaths)}" fill="none" '
            f'stroke="{pen_css(_pen_name(pens, idx))}" stroke-width="{width:g}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )
    lines.append("</svg>")
    data = ("\n".join(lines) + "\n").encode("utf-8")
    out.write_bytes(data)
    return len(data)


def write_thumb(
    polys: Polylines,
    pens: list[str],
    w_mm: float,
    h_mm: float,
    widths_mm: dict[int, float],
    out: Path,
    long_edge: int = 640,
    ss: int = 3,
) -> tuple[int, int]:
    """WebP on cream at ``long_edge`` px. Drawn at ``ss``x and LANCZOS-downscaled,
    because ImageDraw has no anti-aliasing. Returns (w_px, h_px)."""
    px_per_mm = long_edge / max(w_mm, h_mm)
    size = (max(1, round(w_mm * px_per_mm)), max(1, round(h_mm * px_per_mm)))
    k = px_per_mm * ss
    im = Image.new("RGB", (size[0] * ss, size[1] * ss), CREAM)
    draw = ImageDraw.Draw(im)
    for idx in sorted(polys):
        colour = pen_css(_pen_name(pens, idx))
        width = max(1, round(widths_mm.get(idx, DEFAULT_WIDTH_MM) * px_per_mm * ss))
        r = width / 2
        for poly in polys[idx]:
            pts = [(px * k, (h_mm - py) * k) for px, py in poly]
            draw.line(pts, fill=colour, width=width, joint="curve")
            if width > 2:  # round caps
                for ex, ey in (pts[0], pts[-1]):
                    draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=colour)
    im.resize(size, Image.LANCZOS).save(out, "WEBP", quality=82)
    return size


def write_raster(
    polys: Polylines,
    pens: list[str],
    w_mm: float,
    h_mm: float,
    widths_mm: dict[int, float],
    out: Path,
    long_edge: int = 2600,
    ss: int = 3,
) -> tuple[int, int]:
    """The large thumb — the fallback when an SVG is too heavy to ship."""
    return write_thumb(polys, pens, w_mm, h_mm, widths_mm, out, long_edge=long_edge, ss=ss)


def write_technical(
    polys: Polylines,
    pens: list[str],
    w_mm: float,
    h_mm: float,
    widths_mm: dict[int, float],
    out: Path,
    dpi: int = 240,
) -> None:
    """Hi-res WebP plate at 1:1 mm: mm axes, the sheet outline and a pen legend.

    Deliberately no title, stats box, travel lines or drawable-area frame — the
    chrome the gallery previews carry is exactly what this replaces.
    """
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.collections import LineCollection
    from matplotlib.figure import Figure
    from matplotlib.lines import Line2D
    from matplotlib.patches import Rectangle
    from matplotlib.ticker import MultipleLocator

    m = TECH_MARGIN_MM
    fw, fh = w_mm + 2 * m, h_mm + 2 * m
    fig = Figure(figsize=(fw / 25.4, fh / 25.4), dpi=dpi, facecolor="white")
    FigureCanvasAgg(fig)  # explicit Agg, no pyplot global state
    ax = fig.add_axes((m / fw, m / fh, w_mm / fw, h_mm / fh))
    ax.set_xlim(0, w_mm)
    ax.set_ylim(0, h_mm)
    ax.set_aspect("equal")
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(False)
    grey = "#9a9a9a"
    for axis in (ax.xaxis, ax.yaxis):
        axis.set_major_locator(MultipleLocator(50))
    ax.tick_params(labelsize=6, colors=grey, length=2, width=0.4, pad=1.5)
    ax.set_xlabel("mm", fontsize=6, color=grey, labelpad=1)
    ax.set_ylabel("mm", fontsize=6, color=grey, labelpad=1)
    ax.add_patch(
        Rectangle((0, 0), w_mm, h_mm, fill=False, edgecolor="#cfcfcf", linewidth=0.5, clip_on=False)
    )

    pt_per_mm = 72 / 25.4  # the figure is 1:1, so a pen's nib maps to points
    handles: list[Line2D] = []
    seen: set[str] = set()
    for idx in sorted(polys):
        name = _pen_name(pens, idx)
        colour = pen_css(name)
        lw = widths_mm.get(idx, DEFAULT_WIDTH_MM) * pt_per_mm
        ax.add_collection(
            LineCollection(
                polys[idx],
                colors=colour,
                linewidths=lw,
                capstyle="round",
                joinstyle="round",
                clip_on=False,
            )
        )
        if name not in seen:
            seen.add(name)
            handles.append(Line2D([], [], color=colour, linewidth=1.6, label=name))
    if handles:
        ax.legend(
            handles=handles,
            loc="lower right",
            bbox_to_anchor=(1.0, 1.0),
            ncol=min(len(handles), 6),
            fontsize=6,
            frameon=False,
            borderaxespad=0.3,
            handlelength=1.6,
            columnspacing=1.2,
            labelcolor="#555555",
        )

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, facecolor="white")
    buf.seek(0)
    with Image.open(buf) as png:
        png.convert("RGB").save(out, "WEBP", quality=85)


def write_photo(src: Path, out: Path, long_edge: int = 1600) -> tuple[int, int]:
    """A photo of the physical plot: EXIF-upright, downscaled (never upscaled) to
    ``long_edge``, transparency flattened on white, WebP."""
    with Image.open(src) as raw:
        im = ImageOps.exif_transpose(raw)
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        rgba = im.convert("RGBA")
        flat = Image.new("RGB", rgba.size, (255, 255, 255))
        flat.paste(rgba, mask=rgba.getchannel("A"))
        im = flat
    else:
        im = im.convert("RGB")
    scale = min(1.0, long_edge / max(im.size))
    size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    if size != im.size:
        im = im.resize(size, Image.LANCZOS)
    im.save(out, "WEBP", quality=85)
    return size
