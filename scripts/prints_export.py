"""Juan's ``publish`` verdicts -> the portfolio site's print catalog -> GCS.

The site (career-navigator's Prints section) reads one file, ``catalog.json``
v1, plus the assets it points at, from the public bucket
``gs://garassino-ai-prints``. This script builds both:

1. ``gallery_feedback.latest_published()`` — the plates currently published;
2. each one resolves to its render + gcode through the subject's
   ``gallery/<subject>/manifest.json`` (best tier wins, so a plate keeps its id
   when it moves between ``current/`` and ``trials/``);
3. ``scripts/prints_render.py`` draws the site assets from the gcode — clean
   SVG, WebP thumb, technical plate (+ a raster when the SVG is too heavy, + a
   photo of the physical plot when ``studio/prints.json`` names one);
4. ``studio/<slug>/DESCRIPTION.md`` supplies title, one-liner and two sections;
   the gcode header and manifest stats supply paper, pens and plot numbers;
5. ``catalog.json`` is written beside ``assets/``, and ``--push`` uploads
   assets first, catalog last.

Assets are content-addressed — ``<gcode sha16>-r<RENDER_VERSION>-<inp6>``, inp6
hashing pens, widths and sheet — and never re-rendered while the file exists, so
a re-run costs a few stats and the bucket can cache them forever. A changed gcode
or render input gets new names; bump ``prints_render.RENDER_VERSION`` to re-render
all. ``--force`` rebuilds local files under the SAME names: it does not refresh
the site (the bucket serves those names as immutable).

Exit: 0 ok · 1 nothing published / nothing exportable · 2 push failed (or an
argparse usage error) · 3 ``--push`` refused because published plates were skipped.

    python scripts/prints_export.py --list         # what is published, resolved
    python scripts/prints_export.py --dry-run      # what would be exported
    python scripts/prints_export.py                # build build/prints/
    python scripts/prints_export.py --push         # ...and upload (make prints-export)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from PIL import Image

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import gallery_feedback as fb  # noqa: E402
import gallery_index as gi  # noqa: E402
import prints_render as pr  # noqa: E402
from studio_descriptions import _section  # noqa: E402

logger = logging.getLogger(__name__)

REPO = HERE.parent
STUDIO = REPO / "studio"
OVERRIDES = STUDIO / "prints.json"
DEFAULT_OUT = REPO / "build" / "prints"
DEFAULT_BUCKET = "garassino-ai-prints"
CATALOG_VERSION = 1
DEFAULT_ORDER = 1000
TILE_SIZES = ("s", "m", "l")  # the site's mosaic tile size, from prints.json "size"
SVG_LIMIT = 3_000_000  # bytes; above it the site gets sheet_raster as well
SECTIONS = ("What is on the sheet", "The science it encodes")
ASSET_CACHE = "public, max-age=31536000, immutable"  # content-addressed names
CATALOG_CACHE = "public, max-age=300"  # the catalog changes; 5 minutes

_TITLE = re.compile(r"^#\s+(.+?)\s+—\s+description\s*$", re.M)


# ------------------------------------------------------------------- naming


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def print_id(family: str, basename: str) -> str:
    """``attention_DAG`` + ``pp_attention_DAG_landscape.png`` -> ``attention-dag-landscape``.

    The ``pp_`` prefix and the family name the stem repeats are dropped, so the
    id reads as family + variant and does not depend on the tier.
    """
    fam = slugify(family)
    stem = slugify(re.sub(r"^pp[-_]", "", Path(basename).stem, flags=re.I))
    if stem == fam:
        return fam
    if fam and stem.startswith(fam + "-"):
        stem = stem[len(fam) + 1:]
    return slugify(f"{fam}-{stem}")


def _num(v: float) -> int | float:
    return int(v) if float(v).is_integer() else v


# --------------------------------------------------------------------- inputs


def load_overrides(path: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    """``studio/prints.json``: ``<subject>/<basename>`` -> optional fields. Missing -> {}."""
    path = OVERRIDES if path is None else path
    if not path.exists():
        return {}
    data = json.loads(path.read_text() or "{}")
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object keyed by <subject>/<basename>")
    return data


def _manifest(gallery: Path, subject: str) -> Optional[dict]:
    try:
        m = json.loads((gallery / subject / "manifest.json").read_text())
    except (OSError, ValueError):
        return None
    return m if isinstance(m, dict) else None


def _resolve(gallery: Path, subject: str, basename: str) -> Tuple[Optional[dict],
                                                                  Optional[dict], str]:
    """resolve_render plus, when it fails, why — for the skip warnings and --list."""
    m = _manifest(gallery, subject)
    if m is None:
        return None, None, f"no {subject}/manifest.json (run scripts/gallery_index.py)"
    files = [f for f in m.get("files") or [] if isinstance(f, dict)]
    rank = lambda f: gi.TIER_RANK.get(f.get("tier", ""), 99)  # noqa: E731
    renders = sorted((f for f in files if f.get("kind") == "render" and f.get("file") == basename
                      and (gallery / subject / f["rel"]).is_file()), key=rank)
    if not renders:
        return None, None, "render not on disk or not in its manifest (run scripts/gallery_index.py)"
    render = renders[0]
    by_rel = {f["rel"]: f for f in files if f.get("kind") == "gcode"
              and (gallery / subject / f["rel"]).is_file()}
    gcode = by_rel.get(render["rel"].rsplit(".", 1)[0] + ".gcode")
    if gcode is None and (render.get("pair") or "").endswith(".gcode"):
        gcode = by_rel.get(str(Path(render["rel"]).with_name(render["pair"])))
    if gcode is None:
        stem = Path(basename).stem + ".gcode"
        same = sorted((f for f in by_rel.values() if f.get("file") == stem), key=rank)
        gcode = same[0] if same else None
    if gcode is None:
        return render, None, f"no gcode for {render['rel']}"
    return render, gcode, ""


def resolve_render(gallery: Path, subject: str, basename: str) -> Optional[Tuple[dict, dict]]:
    """(render record, gcode record) from the subject manifest, or None.

    The render is the entry with that basename at the best ``TIER_RANK``; its
    gcode is the same stem beside it (``pair``), falling back to the same stem in
    the best tier that has one (the import can split a pair across tiers).
    Both must still be on disk — a stale manifest resolves to None.
    """
    render, gcode, _ = _resolve(gallery, subject, basename)
    return (render, gcode) if render is not None and gcode is not None else None


def describe(slug: str, family: Optional[str] = None) -> Dict[str, Any]:
    """{title, one_line, sections} from ``studio/<slug>/DESCRIPTION.md``."""
    path = STUDIO / slug / "DESCRIPTION.md"
    if not path.is_file():
        return {"title": family or slug, "one_line": "", "sections": []}
    text = path.read_text()
    m = _TITLE.search(text)
    title = m.group(1).strip() if m else (family or slug)
    one_line = _section(text, "In one line").split("\n\n")[0].strip()
    if not one_line:
        first = re.match(r".+?[.!?](?=\s|$)", title)
        one_line = first.group(0) if first else title
    sections = [{"heading": h, "md": md} for h in SECTIONS if (md := _section(text, h))]
    return {"title": title, "one_line": one_line, "sections": sections}


def _piece(header: dict) -> str:
    """The header's absolute piece path made repo-relative, plus ``::function``.

    Anchored at the innermost ``studio/`` or ``promptplot/`` segment; a path with
    neither is reduced to its file name rather than leaking a local path."""
    raw = header.get("piece") or ""
    if not raw:
        return ""
    parts = Path(raw).parts
    rel = Path(raw).name  # never ship an absolute local path to the site
    for anchor in ("studio", "promptplot"):
        if anchor in parts:
            i = len(parts) - 1 - parts[::-1].index(anchor)  # innermost: the repo's own
            rel = "/".join(parts[i:])
            break
    fn = header.get("function") or ""
    return f"{rel}::{fn}" if fn and "::" not in rel else rel


def _tile(key: str, size: Any) -> str:
    if size is None:
        return TILE_SIZES[0]
    if size not in TILE_SIZES:
        logger.warning("prints.json: %s size %r is not one of %s — using %r",
                       key, size, TILE_SIZES, TILE_SIZES[0])
        return TILE_SIZES[0]
    return size


def _local(path: str, gallery: Path) -> Path:
    """A repo-relative path from prints.json; ``gallery/...`` follows ``--gallery``."""
    p = Path(path)
    if p.is_absolute():
        return p
    if p.parts and p.parts[0] == "gallery":
        return gallery.joinpath(*p.parts[1:])
    return REPO / p


# -------------------------------------------------------------------- export


def _sheet(key: str, paper: dict, bbox: Optional[list]) -> Tuple[float, float, str]:
    """(w_mm, h_mm, orientation) of the sheet the strokes were drawn on.

    ``prints_render.fit_sheet`` transposes the declared sheet for plates drawn
    before the paper-size normalisation. It only reads the strokes' extent, so
    it gets the manifest's ``bbox_mm`` as a one-segment stand-in instead of the
    parsed toolpath — a cached re-run never parses a gcode (25 MB ones take 7 s).
    A bbox that still overflows the final sheet is warned about, not fixed.
    """
    w, h = pr.paper_mm(paper["size"], paper["orientation"])
    orientation = paper["orientation"]
    if bbox:
        x0, y0, x1, y1 = bbox
        w, h = pr.fit_sheet({0: [[(x0, y0), (x1, y1)]]}, w, h)
        eps = pr.SHEET_TOLERANCE_MM
        if x0 < -eps or y0 < -eps or x1 > w + eps or y1 > h + eps:
            logger.warning("%s: strokes (x %g-%g, y %g-%g) overflow the %gx%g mm sheet — "
                           "the site will crop them", key, x0, x1, y0, y1, w, h)
    if w != h:
        orientation = "landscape" if w > h else "portrait"
    return w, h, orientation


def _render_if_missing(path: Path, force: bool, draw) -> bool:
    if path.exists() and not force:
        return False
    draw(path)
    return True


def _inputs(key: str, gcode_rec: dict, override: Dict[str, Any],
            gallery: Path, subject: str) -> Optional[Dict[str, Any]]:
    """Everything the assets are drawn from, and the asset basename it hashes to.

    ``<gcode sha16>-r<RENDER_VERSION>-<inp6>``: inp6 is the first 6 hex of a
    sha256 over the other render inputs (pen names, per-index widths, the final
    sheet), so a ``pen_widths_mm`` or header-less ``paper``/``pens`` edit gets a
    new name instead of rewriting an object the bucket serves as immutable.
    None (logged) when there is neither a header nor override paper + pens.
    """
    gpath = gallery / subject / gcode_rec["rel"]
    header = pr.parse_header(gpath)
    if header is not None:
        paper, pens = header["paper"], header["pens"] or list(override.get("pens") or [])
    elif override.get("paper") and override.get("pens"):
        paper, pens = pr._parse_paper(str(override["paper"])), list(override["pens"])
    else:
        logger.warning("skip %s: %s has no provenance header and prints.json gives no "
                       "paper + pens", key, gcode_rec["rel"])
        return None
    st = gcode_rec.get("stats") or gi.gcode_stats(gpath)
    w_mm, h_mm, orientation = _sheet(key, paper, st.get("bbox_mm"))
    widths_list = [float(w) for w in override.get("pen_widths_mm") or []]
    widths = dict(enumerate(widths_list))
    per_index = [widths.get(i, pr.DEFAULT_WIDTH_MM)
                 for i in range(max(len(pens), len(widths_list)))]
    inp = json.dumps({"pens": pens, "widths": per_index, "w_mm": w_mm, "h_mm": h_mm},
                     sort_keys=True)
    sha = gcode_rec.get("sha256") or gi.sha256(gpath)
    base = f"{sha}-r{pr.RENDER_VERSION}-{hashlib.sha256(inp.encode()).hexdigest()[:6]}"
    return {"gpath": gpath, "header": header or {}, "paper": paper, "pens": pens,
            "widths": widths, "w_mm": w_mm, "h_mm": h_mm, "orientation": orientation,
            "stats": st, "base": base}


def build_print(subject: str, basename: str, render_rec: dict, gcode_rec: dict,
                override: Dict[str, Any], out_dir: Path, gallery: Path, force: bool = False,
                published_at: str = "") -> Optional[Dict[str, Any]]:
    """One catalog entry, rendering whichever of its assets are missing. None = skipped."""
    key = f"{subject}/{basename}"
    inp = _inputs(key, gcode_rec, override, gallery, subject)
    if inp is None:
        return None
    gpath, header, paper, pens = inp["gpath"], inp["header"], inp["paper"], inp["pens"]
    widths, w_mm, h_mm, orientation = inp["widths"], inp["w_mm"], inp["h_mm"], inp["orientation"]
    st, base = inp["stats"], inp["base"]

    family = subject.rsplit("/", 1)[-1]
    slug = fb.slug_for(subject)
    pid = override.get("id") or print_id(family, basename)
    adir = out_dir / "assets" / pid
    adir.mkdir(parents=True, exist_ok=True)
    names = {"sheet": f"{base}.svg", "sheet_raster": f"{base}.raster.webp",
             "thumb": f"{base}.thumb.webp", "technical": f"{base}.tech.webp"}
    files = {k: adir / v for k, v in names.items()}

    polys: Dict[int, list] = {}

    def lazy_polys() -> Dict[int, list]:
        if not polys:
            polys.update(pr.parse_polylines(gpath))
        return polys

    args = lambda: (lazy_polys(), pens, w_mm, h_mm, widths)  # noqa: E731
    drawn = []
    if _render_if_missing(files["sheet"], force, lambda p: pr.write_svg(*args(), p)):
        drawn.append("sheet")
    raster = files["sheet"].stat().st_size > SVG_LIMIT
    if raster and _render_if_missing(files["sheet_raster"], force,
                                     lambda p: pr.write_raster(*args(), p)):
        drawn.append("sheet_raster")
    if _render_if_missing(files["thumb"], force, lambda p: pr.write_thumb(*args(), p)):
        drawn.append("thumb")
    if _render_if_missing(files["technical"], force, lambda p: pr.write_technical(*args(), p)):
        drawn.append("technical")
    with Image.open(files["thumb"]) as im:
        thumb_px = list(im.size)

    plotted = None
    photo_rel = None
    if isinstance(override.get("plotted"), dict):
        plotted = dict(override["plotted"])
        src = plotted.get("photo")
        if src:
            spath = _local(str(src), gallery)
            if spath.is_file():
                photo = adir / f"{gi.sha256(spath)}.photo.webp"
                if _render_if_missing(photo, force, lambda p: pr.write_photo(spath, p)):
                    drawn.append("photo")
                photo_rel = f"assets/{pid}/{photo.name}"
            else:
                logger.warning("%s: plotted photo %s is not on disk", key, src)
        plotted["photo"] = photo_rel
    if drawn:
        logger.info("rendered %s: %s", pid, ", ".join(drawn))

    desc = describe(slug, family)
    rel = lambda k: f"assets/{pid}/{names[k]}"  # noqa: E731
    return {
        "id": pid,
        "subject": subject,
        "basename": basename,
        "slug": slug,
        "family": family,
        "title": override.get("title") or desc["title"],
        "one_line": desc["one_line"],
        "sections": desc["sections"],
        "paper": {"size": paper["size"], "orientation": orientation,
                  "w_mm": _num(w_mm), "h_mm": _num(h_mm),
                  "margin_mm": paper.get("margin_mm", pr.DEFAULT_MARGIN_MM)},
        "pens": [{"index": i, "name": name, "css": pr.pen_css(name),
                  "width_mm": widths.get(i, pr.DEFAULT_WIDTH_MM)} for i, name in enumerate(pens)],
        "pen_count": len(set(pens)),
        "stats": {"draw_mm": st["draw_mm"], "travel_mm": st["travel_mm"],
                  "commands": st["commands"], "pen_cycles": st["pen_cycles"],
                  "est_minutes": round(gi.plot_minutes(st))},
        "seed": header.get("seed") if header.get("seed") is not None else gcode_rec.get("seed"),
        "piece": _piece(header),
        "rendered": header.get("rendered") or "",
        "published_at": published_at,
        "order": int(override.get("order", DEFAULT_ORDER)),
        "size": _tile(key, override.get("size")),
        "plotted": plotted,
        "assets": {"sheet": rel("sheet"), "sheet_raster": rel("sheet_raster") if raster else None,
                   "thumb": rel("thumb"), "technical": rel("technical"), "photo": photo_rel,
                   "thumb_px": thumb_px},
        "bytes": {k: files[k].stat().st_size for k in ("sheet", "thumb", "technical")},
    }


def _published() -> List[Tuple[str, str, dict]]:
    pub = fb.latest_published()
    return [(s, b, rec) for (s, b), rec in sorted(pub.items())]


def _check_overrides(overrides: dict, published: List[Tuple[str, str, dict]],
                     gallery: Path) -> None:
    keys = {f"{s}/{b}" for s, b, _ in published}
    for key in overrides:
        if key not in keys:
            logger.warning("prints.json: %s is not published", key)
        subject, _, basename = key.rpartition("/")
        if not subject or resolve_render(gallery, subject, basename) is None:
            logger.warning("prints.json: %s is not on disk (no render + gcode in its manifest)",
                           key)


def _sort(prints: List[dict]) -> List[dict]:
    prints = sorted(prints, key=lambda p: p["published_at"], reverse=True)
    return sorted(prints, key=lambda p: p["order"])  # stable: newest first within an order


def build_catalog(out_dir: Path, gallery: Path, only: Optional[Iterable[str]] = None,
                  force: bool = False, overrides: Optional[dict] = None,
                  skipped: Optional[List[str]] = None) -> Dict[str, Any]:
    """Export every published plate (or just ``only`` ids) and write ``catalog.json``.

    Each published plate that could not be exported is logged and its key is
    appended to ``skipped`` (when given) — the caller decides whether a catalog
    missing it may go live. One broken plate never aborts the rest.
    """
    skipped = [] if skipped is None else skipped
    overrides = load_overrides() if overrides is None else overrides
    published = _published()
    _check_overrides(overrides, published, gallery)
    want = set(only) if only else None
    prints: List[dict] = []
    seen: set = set()
    for subject, basename, rec in published:
        key = f"{subject}/{basename}"
        ov = overrides.get(key) or {}
        pid = ov.get("id") or print_id(subject.rsplit("/", 1)[-1], basename)
        if want is not None and pid not in want:
            continue
        render, gcode, why = _resolve(gallery, subject, basename)
        if gcode is None:
            logger.warning("skip %s: %s", key, why)
            skipped.append(key)
            continue
        if pid in seen:
            logger.warning("skip %s: id %r is taken — give it an id in prints.json", key, pid)
            skipped.append(key)
            continue
        try:
            entry = build_print(subject, basename, render, gcode, ov, out_dir, gallery,
                                force=force, published_at=rec.get("when", ""))
        except Exception:  # one corrupt gcode/override must not sink the export
            logger.exception("skip %s: export failed", key)
            entry = None
        if entry is None:
            skipped.append(key)
            continue
        seen.add(pid)
        prints.append(entry)
    catalog = {
        "version": CATALOG_VERSION,
        "generated": datetime.now().astimezone().isoformat(timespec="seconds"),
        "count": len(prints),
        "prints": _sort(prints),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "catalog.json").write_text(json.dumps(catalog, indent=1) + "\n")
    logger.info("catalog: %d print(s) -> %s", len(prints), out_dir / "catalog.json")
    return catalog


def push(out_dir: Path, bucket: str) -> None:
    """Upload assets first (immutable), then the catalog (5 min) — never a catalog
    that points at assets not yet in the bucket."""
    cmds = [
        ["gcloud", "storage", "cp", "-r", "--gzip-local=svg,json",
         f"--cache-control={ASSET_CACHE}", str(out_dir / "assets"), f"gs://{bucket}/"],
        ["gcloud", "storage", "cp", "--gzip-local=json", f"--cache-control={CATALOG_CACHE}",
         str(out_dir / "catalog.json"), f"gs://{bucket}/catalog.json"],
    ]
    assets = out_dir / "assets"
    if not (assets.is_dir() and any(p.is_file() for p in assets.rglob("*"))):
        cmds = cmds[1:]  # an empty catalog: nothing to upload but the catalog itself
    for cmd in cmds:
        logger.info("$ %s", " ".join(f"'{c}'" if " " in c else c for c in cmd))
        subprocess.run(cmd, check=True)


# ----------------------------------------------------------------------- CLI


def _report(gallery: Path, out_dir: Path, published: List[Tuple[str, str, dict]],
            overrides: dict, want: Optional[set], dry_run: bool) -> None:
    """--list (paths + header status) and --dry-run (ids + render status). Writes nothing."""
    for subject, basename, rec in published:
        key = f"{subject}/{basename}"
        ov = overrides.get(key) or {}
        pid = ov.get("id") or print_id(subject.rsplit("/", 1)[-1], basename)
        if want is not None and pid not in want:
            continue
        render, gcode, why = _resolve(gallery, subject, basename)
        if gcode is None:
            print(f"SKIP  {key}  — {why}")
            continue
        gpath = gallery / subject / gcode["rel"]
        header = pr.parse_header(gpath)
        hstat = ("header ok" if header else
                 "no header, prints.json paper+pens" if ov.get("paper") and ov.get("pens")
                 else "NO HEADER — would skip")
        if not dry_run:
            print(f"{key}  [{rec.get('when', '')}]\n"
                  f"      render {subject}/{render['rel']}\n"
                  f"      gcode  {subject}/{gcode['rel']}  ({hstat})")
            continue
        try:
            inp = _inputs(key, gcode, ov, gallery, subject) if "skip" not in hstat else None
        except Exception as exc:  # report it, as the export would skip it
            inp, hstat = None, f"would skip: {type(exc).__name__}: {exc}"
        svg = out_dir / "assets" / pid / f"{inp['base']}.svg" if inp else None
        state = "cached" if svg is not None and svg.exists() else "would render"
        print(f"{'SKIP' if 'skip' in hstat else 'OK  '}  {pid:40} {state:13} {key}  ({hstat})")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT,
                    help="build directory for catalog.json + assets/ (default build/prints)")
    ap.add_argument("--gallery", type=Path, default=None,
                    help="the gallery to export from (default REPO/gallery)")
    ap.add_argument("--bucket", default=DEFAULT_BUCKET,
                    help=f"GCS bucket to push to (default {DEFAULT_BUCKET})")
    ap.add_argument("--push", action="store_true", help="upload assets, then catalog.json")
    ap.add_argument("--dry-run", action="store_true",
                    help="list what would be exported; render nothing, write nothing")
    ap.add_argument("--only", help="comma-separated print ids to export (not with --push)")
    ap.add_argument("--force", action="store_true",
                    help="rebuild local asset files under the same names (does not refresh "
                         "the site; changed inputs or a RENDER_VERSION bump do)")
    ap.add_argument("--list", action="store_true",
                    help="print the published set with resolved paths and header status")
    ap.add_argument("--allow-skips", action="store_true",
                    help="push even when some published plates could not be exported")
    ap.add_argument("--allow-empty", action="store_true",
                    help="write (and with --push upload) an empty catalog when nothing is "
                         "exportable, so the site shows its empty state")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    if args.only and args.push:
        ap.error("--only writes a partial catalog; pushing it would unpublish the rest")
    logging.basicConfig(level=logging.WARNING if args.quiet else logging.INFO,
                        format="%(levelname)s %(message)s")

    gallery = args.gallery or fb.GALLERY
    want = {x.strip() for x in args.only.split(",") if x.strip()} if args.only else None
    published = _published()
    if not published and (args.list or args.dry_run or not args.allow_empty):
        logger.error("nothing is published — mark plates with `p` in the gallery viewer "
                     "(%s holds no current publish verdict); nothing exported%s", fb.LOG,
                     "" if args.list or args.dry_run else
                     " (--allow-empty publishes an empty catalog)")
        return 1
    overrides = load_overrides()
    if args.list or args.dry_run:
        _report(gallery, args.out, published, overrides, want, dry_run=args.dry_run)
        return 0

    skipped: List[str] = []
    catalog = build_catalog(args.out, gallery, only=want, force=args.force, overrides=overrides,
                            skipped=skipped)
    if skipped:
        print(f"{len(skipped)} published plate(s) NOT in the catalog:")
        for key in skipped:
            print(f"  {key}")
        if args.push and not args.allow_skips:
            logger.error("not pushing: the site would silently lose them — fix them, unpublish "
                         "them, or pass --allow-skips")
            return 3
    if not catalog["prints"] and not args.allow_empty:
        logger.error("no published plate could be exported (see the warnings above); "
                     "--allow-empty writes an empty catalog")
        return 1
    if args.push:
        try:
            push(args.out, args.bucket)
        except (subprocess.CalledProcessError, OSError) as exc:
            logger.error("push failed: %s", exc)
            return 2
        logger.info("pushed %d print(s) to gs://%s", catalog["count"], args.bucket)
    return 0


if __name__ == "__main__":
    sys.exit(main())
