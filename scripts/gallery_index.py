"""Rebuild gallery/**/manifest.json, INDEX.md, PRINT.md, viewer.html and board.html.

Idempotent: promoting a future render is a move plus a re-run of this script.

A full run hashes and replays every GCode (~10 min). Runs reuse `sha256` and
`stats` from the existing manifests when a file's name, size and mtime are
unchanged, so re-tiering after `gallery_apply.py` takes seconds; `--full` forces
the recompute and `--views-only` rewrites just viewer.html + board.html from
the manifests already on disk.

The archived GCode carries no provenance header (see CLAUDE.md "Gallery and feedback"), so
everything here is derived -- stats by replaying the toolpath, seed by reading
the filename. Files written after the provenance-header fix will carry their own
metadata and this script prefers that when present.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import logging
import math
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STUDIO = REPO / "studio"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gallery_directions as gd  # noqa: E402  (direction keys + LEDGER parsing)
import gallery_feedback as fb  # noqa: E402  (stdlib-only, like this script)

logger = logging.getLogger(__name__)

# Deliberately standalone: promptplot.models needs pydantic, and the project env
# does not currently resolve (requires-python >=3.9 vs mcp>=1.0 needing >=3.10).
# Replaying a toolpath only needs G0/G1/M3, so this tool stays dependency-free
# and runnable from any interpreter.
_WORD = re.compile(r"([A-Z])(-?\d*\.?\d+)")
_COLOR = re.compile(r";\s*color\s*=\s*(\d+)")


def parse_line(line: str) -> tuple[str, dict[str, float], int | None] | None:
    """-> (verb, {axis: value}, color) for one GCode line, or None to skip."""
    color_m = _COLOR.search(line)
    color = int(color_m.group(1)) if color_m else None
    code = line.split(";", 1)[0].strip().upper()
    if not code:
        return None
    words = dict(_WORD.findall(code))
    verb = code.split()[0]
    if not re.fullmatch(r"[GM]\d+", verb):
        return None
    axes = {k: float(v) for k, v in words.items() if k in ("X", "Y")}
    return verb, axes, color

GALLERY = REPO / "gallery"
TIERS = ("promoted", "variants", "candidates", "candidates/prior-approved")
PAPERS = {  # (w, h) mm -> name, matched against the drawn bbox
    "a3": (297, 420), "a4": (210, 297), "a5": (148, 210), "a6": (105, 148),
    "17x24": (170, 240),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()[:16]


def gcode_stats(path: Path) -> dict:
    """Replay the toolpath: draw/travel distance, pen cycles, colours, bbox."""
    draw = travel = 0.0
    pen_cycles = 0
    colors: set[int] = set()
    xs: list[float] = []
    ys: list[float] = []
    x = y = 0.0
    total = 0

    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        parsed = parse_line(line)
        if parsed is None:
            continue
        verb, axes, color = parsed
        total += 1
        if verb == "M3":
            pen_cycles += 1
        if color is not None:
            colors.add(color)
        if verb in ("G0", "G1"):
            nx = axes.get("X", x)
            ny = axes.get("Y", y)
            dist = math.hypot(nx - x, ny - y)
            if verb == "G1":
                draw += dist
                xs.append(nx); ys.append(ny); xs.append(x); ys.append(y)
            else:
                travel += dist
            x, y = nx, ny

    bbox = None
    paper = None
    if xs:
        bbox = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        best, best_err = None, 1e9
        for name, (pw, ph) in PAPERS.items():
            for cand in ((pw, ph), (ph, pw)):
                err = abs(w - cand[0]) + abs(h - cand[1])
                if err < best_err:
                    best, best_err = name, err
        paper = best if best_err < 90 else None

    return {
        "draw_mm": round(draw, 1),
        "travel_mm": round(travel, 1),
        "travel_ratio": round(travel / draw, 3) if draw else None,
        "commands": total,
        "pen_cycles": pen_cycles,
        "colors": len(colors) or 1,
        "bbox_mm": bbox,
        "paper_guess": paper,
    }


def seed_from(name: str) -> int | None:
    m = re.search(r"seed(\d+)", name, re.I)
    return int(m.group(1)) if m else None


def subject_dirs() -> list[Path]:
    """Every leaf subject folder -- one that directly contains a tier folder."""
    out = []
    for path in GALLERY.rglob("*"):
        if path.is_dir() and path.name in (
            "promoted", "variants", "candidates", "current", "trials", "archive", "cut"
        ):
            if path.parent not in out:
                out.append(path.parent)
    if (GALLERY / "references").is_dir():
        out.append(GALLERY / "references")
    return sorted(out)


TIER_RANK = {"current": 0, "promoted": 1, "candidates/prior-approved": 2,
             "candidates": 3, "variants": 4, "trials": 5, "archive": 6, "cut": 7}
# ARCHIVE ("not now", recoverable) and CUT (dropped, never deleted): kept on disk
# and in the manifests, but off the print queue and hidden in the viewer by default.
SHELVED_TIERS = ("archive", "cut")


def _shelved(tier: str) -> bool:
    return tier.split("/", 1)[0] in SHELVED_TIERS


def colocate_pairs(subject: Path) -> int:
    """Pull a .gcode up to the tier of the render that shares its stem.

    The import routes by source folder, so a promoted render and its GCode can
    land in different tiers (the render was in leo/, the GCode was loose in
    ~/Downloads). The canonical piece is more useful with both files together.
    """
    renders: dict[str, Path] = {}
    gcodes: dict[str, Path] = {}
    for path in subject.rglob("*"):
        if not path.is_file():
            continue
        tier = str(path.parent.relative_to(subject))
        if tier not in TIER_RANK:
            continue
        if path.suffix == ".png":
            cur = renders.get(path.stem)
            if cur is None or TIER_RANK[tier] < TIER_RANK[str(cur.parent.relative_to(subject))]:
                renders[path.stem] = path
        elif path.suffix == ".gcode":
            gcodes[path.stem] = path

    moved = 0
    for stem, gpath in gcodes.items():
        render = renders.get(stem)
        if render is None:
            continue
        if render.parent == gpath.parent:
            continue
        if TIER_RANK[str(render.parent.relative_to(subject))] < TIER_RANK[
            str(gpath.parent.relative_to(subject))
        ]:
            gpath.rename(render.parent / gpath.name)
            moved += 1
    return moved


def load_cache(subject: Path) -> dict[tuple, dict]:
    """(file name, bytes, mtime) -> the record the last run wrote for it.

    Keyed by NAME, not path: `gallery_apply.py` moves a file between tiers with
    a rename, which keeps its size and mtime, so the hash and the toolpath
    replay carry over. Each record is keyed twice -- by `mtime_ns` (exact) and by
    the second-precision `mtime` string, so manifests written before `mtime_ns`
    existed still seed the cache.
    """
    try:
        m = json.loads((subject / "manifest.json").read_text())
    except (OSError, ValueError):
        return {}
    out: dict[tuple, dict] = {}
    for f in m.get("files") or []:
        if not isinstance(f, dict) or not f.get("sha256"):
            continue
        if f.get("mtime_ns") is not None:
            out[(f.get("file"), f.get("bytes"), f["mtime_ns"])] = f
        out.setdefault((f.get("file"), f.get("bytes"), f.get("mtime")), f)
    return out


def build_manifest(subject: Path, cache: dict[tuple, dict] | None = None) -> dict:
    """One subject's manifest. `cache` (from load_cache) skips hashing and replay
    for unchanged files; the counters of what was reused land in `_cache`."""
    cache = cache or {}
    records = []
    hits = 0
    for path in sorted(subject.rglob("*")):
        if not path.is_file() or path.name in ("manifest.json", "README.md"):
            continue
        rel_tier = path.parent.relative_to(subject)
        st = path.stat()
        # Local time to the second, with its offset: the viewer compares it
        # against feedback `when` stamps (naive local) to decide what is NEW.
        mtime = datetime.fromtimestamp(st.st_mtime).astimezone().isoformat(timespec="seconds")
        old = cache.get((path.name, st.st_size, st.st_mtime_ns)) or (
            cache.get((path.name, st.st_size, mtime)))
        if old and path.suffix == ".gcode" and not old.get("stats"):
            old = None
        rec = {
            "file": path.name,
            "tier": str(rel_tier) if str(rel_tier) != "." else "loose",
            "rel": str(path.relative_to(subject)),
            "kind": "gcode" if path.suffix == ".gcode" else "render",
            "bytes": st.st_size,
            "mtime": mtime,
            "mtime_ns": st.st_mtime_ns,  # exact, for the cache; `mtime` is for people
            "sha256": old["sha256"] if old else sha256(path),
            "seed": seed_from(path.name),
        }
        if path.suffix == ".gcode":
            rec["stats"] = old["stats"] if old else gcode_stats(path)
        hits += bool(old)
        counterpart = path.with_suffix(".png" if path.suffix == ".gcode" else ".gcode")
        rec["pair"] = counterpart.name if counterpart.exists() else None
        records.append(rec)
    return {
        "subject": str(subject.relative_to(GALLERY)),
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "count": len(records),
        "cached": hits,
        "files": records,
    }


def load_manifests() -> list[dict]:
    """The manifests already on disk, for `--views-only`.

    A file listed but gone from disk (moved or deleted since the last full run)
    is dropped with a warning -- a broken thumbnail helps nobody -- and a
    subject folder with no manifest is skipped the same way.
    """
    out = []
    for subject in subject_dirs():
        try:
            m = json.loads((subject / "manifest.json").read_text())
        except (OSError, ValueError):
            logger.warning("no manifest for %s -- run without --views-only",
                           subject.relative_to(GALLERY))
            continue
        files = m.get("files") or []
        kept = [f for f in files if (subject / f.get("rel", "")).is_file()]
        if len(kept) != len(files):
            gone = [f.get("rel") for f in files if f not in kept]
            logger.warning("%s: %d file(s) in manifest.json are gone from disk (e.g. %s) "
                           "-- run without --views-only to re-index",
                           m.get("subject"), len(gone), gone[0])
            m = dict(m, files=kept, count=len(kept))
        out.append(m)
    return out


def write_index(manifests: list[dict]) -> None:
    lines = [
        "# Gallery index",
        "",
        "Generated by `scripts/gallery_index.py` — do not edit by hand.",
        "",
        f"{sum(m['count'] for m in manifests)} files across {len(manifests)} subjects. "
        "Tiers record where a file came from, not a quality judgement: "
        "`current` is the latest version of a studio drawing and `trials` every earlier "
        "attempt, `promoted` was already moved out of staging, `variants` was a loose "
        "working file, `candidates` came from `_staging/` and is **not** approved. "
        "Two tiers are Juan's verdicts, applied by `scripts/gallery_apply.py`: `archive` "
        "is *not now* (recoverable, hidden in the viewer until \"show archived\") and "
        "`cut` is dropped (never deleted). Neither is listed in PRINT.md.",
        "",
    ]
    series: dict[str, list[dict]] = {}
    for m in manifests:
        series.setdefault(m["subject"].split("/")[0], []).append(m)

    for name in sorted(series):
        lines += [f"## {name}", ""]
        for m in sorted(series[name], key=lambda x: x["subject"]):
            gcodes = [f for f in m["files"] if f["kind"] == "gcode"]
            renders = [f for f in m["files"] if f["kind"] == "render"]
            lines.append(f"### `{m['subject']}` — {len(renders)} renders, {len(gcodes)} gcode")
            lines.append("")
            if gcodes:
                lines += [
                    "| file | tier | draw mm | travel | ratio | pen cycles | colors | paper |",
                    "|---|---|---|---|---|---|---|---|",
                ]
                for f in sorted(gcodes, key=lambda x: x["file"]):
                    s = f["stats"]
                    ratio = f"{s['travel_ratio']:.0%}" if s["travel_ratio"] else "—"
                    lines.append(
                        f"| `{f['file']}` | {f['tier']} | {s['draw_mm']:.0f} | "
                        f"{s['travel_mm']:.0f} | {ratio} | {s['pen_cycles']} | "
                        f"{s['colors']} | {s['paper_guess'] or '—'} |"
                    )
                lines.append("")
            if renders:
                by_tier: dict[str, list[str]] = {}
                for f in renders:
                    by_tier.setdefault(f["tier"], []).append(f["file"])
                for tier in sorted(by_tier):
                    names = ", ".join(f"`{n}`" for n in sorted(by_tier[tier]))
                    lines.append(f"- **{tier}** ({len(by_tier[tier])}): {names}")
                lines.append("")
    (GALLERY / "INDEX.md").write_text("\n".join(lines) + "\n")


# Leo's measured plotting behaviour: F600 draw, ~F2000 travel, 1.0 s dwell each
# side of a pen move. Overhead dominates on dense plates, so it is priced in.
LEO_DRAW_MM_MIN, LEO_TRAVEL_MM_MIN, LEO_DWELL_S = 600.0, 2000.0, 2.0


def plot_minutes(st: dict) -> float:
    return (
        st["draw_mm"] / LEO_DRAW_MM_MIN
        + st["travel_mm"] / LEO_TRAVEL_MM_MIN
        + st["pen_cycles"] * LEO_DWELL_S / 60.0
    )


def write_print_queue(manifests: list[dict]) -> None:
    """Everything plottable, cheapest first — the sheet to pick a job from."""
    rows = []
    for m in manifests:
        for f in m["files"]:
            if f["kind"] != "gcode" or not f.get("stats") or _shelved(f["tier"]):
                continue
            st = f["stats"]
            if not st.get("draw_mm"):
                continue
            rows.append((plot_minutes(st), m["subject"], f["rel"], f["file"], st))
    rows.sort()

    out = [
        "# Print queue",
        "",
        "Generated by `scripts/gallery_index.py` — do not edit by hand.",
        "",
        f"{len(rows)} plottable files. Time is estimated for Leo at "
        f"F{int(LEO_DRAW_MM_MIN)} draw, F{int(LEO_TRAVEL_MM_MIN)} travel and "
        f"{LEO_DWELL_S:.0f}s of dwell per pen cycle — on dense plates the dwell "
        "dominates, which is why pen cycles matter more than metres.",
        "",
        "Always trace the pen-up frame before inking: `promptplot plot frame`.",
        "",
        "| est. | draw | travel | pens | cycles | paper | plate |",
        "|---:|---:|---:|---:|---:|---|---|",
    ]
    for mins, subject, rel, name, st in rows:
        hm = f"{int(mins // 60)}h{int(mins % 60):02d}" if mins >= 60 else f"{mins:.0f}m"
        out.append(
            f"| {hm} | {st['draw_mm'] / 1000:.1f} m | {st['travel_ratio']:.0%} | "
            f"{st['colors']} | {st['pen_cycles']} | {st['paper_guess'] or '—'} | "
            f"`{subject}/{rel}` |"
        )
    total = sum(r[0] for r in rows)
    out += ["", f"Total if you plotted every one: **{total / 60:.0f} hours**."]
    (GALLERY / "PRINT.md").write_text("\n".join(out) + "\n")


def _epoch(stamp: str) -> int | None:
    """ISO stamp -> epoch seconds. A naive stamp (feedback `when`) is local time,
    which is also how the viewer's `Date.parse` reads it."""
    try:
        dt = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return int(dt.astimezone().timestamp())


def _is_render_record(r: dict) -> bool:
    """Records from before scopes existed have none: they are render verdicts."""
    return (r.get("scope") or "render") == "render"


def feedback_snapshot() -> dict:
    """The latest RENDER verdict per plate, inlined so NEW works over file:// too.

    The viewer decides NEW itself (so a verdict recorded in the page updates it
    instantly); this is only its starting data. `subjects` and `global` are the
    latest verdict per subject and anywhere -- the global one is Juan's last
    review, the cutoff for subjects he has never judged. Direction verdicts are
    left out on purpose: judging a direction is not looking at a render, so it
    must neither clear NEW nor move the cutoff (see direction_snapshot).
    """
    records, subjects = [], {}
    for r in fb.latest_by_target().values():
        if not _is_render_record(r):
            continue
        w = _epoch(r.get("when", ""))
        if w is None or not r.get("target"):
            continue
        records.append({"p": r["target"], "n": r["target"].rsplit("/", 1)[-1],
                        "s": r.get("subject"), "w": w, "v": r.get("verdict"),
                        "note": r.get("note") or ""})
        s = r.get("subject") or ""
        subjects[s] = max(subjects.get(s, 0), w)
    return {"records": records, "subjects": subjects,
            "global": max(subjects.values(), default=0)}


def direction_snapshot() -> dict:
    """{subject: {direction key: {v, note, w}}} -- the latest direction verdicts."""
    out: dict[str, dict] = {}
    for r in fb.latest_by_target().values():
        if r.get("scope") != "direction" or not r.get("direction"):
            continue
        w = _epoch(r.get("when", ""))
        if w is None:
            continue
        out.setdefault(r.get("subject") or "", {})[r["direction"]] = {
            "v": r.get("verdict"), "note": r.get("note") or "", "w": w}
    return out


def publish_snapshot() -> dict:
    """{"<subject>|<basename>": {v, w}} -- the plates currently published to the site."""
    out: dict[str, dict] = {}
    for (subject, name), r in fb.latest_published().items():
        w = _epoch(r.get("when", ""))
        if w is None:
            continue
        out[f"{subject}|{name}"] = {"v": r["verdict"], "w": w}
    return out


def ledger_rows(subject: str) -> dict[str, dict]:
    """render basename -> {round, thesis, scores} from studio/<slug>/LEDGER.md.

    The studio lead keeps a `## Rounds` table (round | parent | thesis | render |
    art avg/min | sci t/f/l | verdict | note), parsed by
    `gallery_directions.parse_ledger`. A missing or malformed ledger yields
    nothing -- never an error.
    """
    path = STUDIO / fb.slug_for(subject) / "LEDGER.md"
    try:
        text = path.read_text()
    except OSError:
        return {}
    try:
        rows = gd.parse_ledger(text)
    except Exception:  # a bad ledger must never take the index down
        logger.exception("could not parse %s", path)
        return {}
    out: dict[str, dict] = {}
    for row in rows or []:
        scores = " · ".join(
            f"{k} {v}" for k, v in (("art", row.get("art")), ("sci", row.get("sci")))
            if v and v != "—"
        )
        rec = {"r": row.get("round") or None, "th": row.get("thesis") or None,
               "sc": scores or None, "vd": row.get("verdict") or None}
        render = str(row.get("render") or "").rsplit("/", 1)[-1]
        if render:
            # a row may name the .gcode; the viewer looks renders up by .png
            out[render] = rec
            if render.endswith(".gcode"):
                out.setdefault(render[:-len(".gcode")] + ".png", rec)
    return out


def studio_tag(subject: str, name: str, ledger: dict[str, dict]) -> dict | None:
    """Round / thesis / scores for a studio render, from its LEDGER row or its name.

    Renders are named `pp_<family>_<thesis>_v<N>[_r<NN>]...`; the ledger, when a
    row names this file, wins because it also carries the critics' scores.
    """
    tag: dict = {}
    stem = name.rsplit(".", 1)[0]
    fam = subject.rsplit("/", 1)[-1]
    if stem.startswith("pp_"):
        rest = stem[3:]
        if rest == fam or rest.startswith(fam + "_"):
            toks = [t for t in rest[len(fam):].split("_") if t]
            thesis = []
            for t in toks:
                if re.fullmatch(r"(v|r|s|seed)\d+", t, re.I):
                    break
                thesis.append(t)
            if thesis:
                tag["th"] = "_".join(thesis)
            for t in toks:
                if re.fullmatch(r"v\d+", t, re.I):
                    tag["v"] = int(t[1:])
                elif re.fullmatch(r"r\d+", t, re.I):
                    tag["r"] = f"r{int(t[1:]):02d}"
    row = ledger.get(name)
    if row:
        tag.update({k: v for k, v in row.items() if v})
    return tag or None


def _directions(subject: str) -> dict:
    """gd.directions(subject): {} when the plate has no ledger, and never raises."""
    try:
        return gd.directions(subject) or {}
    except Exception:
        logger.exception("directions failed for %s", subject)
        return {}


def _direction_of(subject: str, name: str) -> str | None:
    try:
        return gd.direction_of(subject, name)
    except Exception:
        logger.exception("direction_of failed for %s/%s", subject, name)
        return None


def _inline(obj) -> str:
    """JSON safe to paste inside <script>: ledger text is free prose, and a
    `</script>` (or `<!--`) in it would otherwise end or derail the script."""
    text = json.dumps(obj, separators=(",", ":"), default=str)
    return text.replace("</", "<\\/").replace("<!--", "<\\!--")


def _fill(template: str, values: dict[str, str]) -> str:
    """Replace every __NAME__ in ONE pass, so a placeholder spelled inside the
    inlined data (a note quoting `__FEEDBACK__`) is never substituted again."""
    return re.sub(r"__([A-Z]+)__",
                  lambda m: values.get(m.group(1), m.group(0)), template)


def build_groups(manifests: list[dict]) -> list[dict]:
    """The viewer's data: one group per subject, its renders ranked by tier.

    Each shot carries `dk`, the key of the DIRECTION it belongs to (a root
    round like `r02`, `original`, or `x-<variant>`), and each group carries
    `dirs`, that plate's directions from gallery_directions.
    """
    groups = []
    for m in manifests:
        subject = m["subject"]
        ledger = ledger_rows(subject)
        # Key on the full relative path, not the stem: the same stem can exist in
        # two tiers (a promoted copy plus an older variant) and a render must pair
        # only with the GCode sitting beside it.
        by_rel = {f["rel"]: f for f in m["files"] if f["kind"] == "gcode"}
        shots = []
        for f in m["files"]:
            if f["kind"] != "render":
                continue
            g = by_rel.get(f["rel"].rsplit(".", 1)[0] + ".gcode")
            st = (g or {}).get("stats") or {}
            shots.append(
                {
                    "n": f["file"],
                    "t": f["tier"],
                    "p": f"{subject}/{f['rel']}",
                    "g": g["file"] if g else None,
                    "d": st.get("draw_mm"),
                    "r": st.get("travel_ratio"),
                    "c": st.get("pen_cycles"),
                    "k": st.get("colors"),
                    "m": round(plot_minutes(st)) if st.get("draw_mm") else None,
                    "ts": _epoch(f["mtime"]) or 0,
                    "st": studio_tag(subject, f["file"], ledger),
                    "dk": _direction_of(subject, f["file"]),
                }
            )
        if not shots:
            continue
        shots.sort(key=lambda x: (TIER_RANK.get(x["t"], 9), x["n"]))
        group = {"s": subject, "series": subject.split("/")[0], "shots": shots,
                 "dirs": _directions(subject)}
        if subject == "references":
            group["ref"] = True  # inputs to reconstruct from, never NEW
        groups.append(group)
    groups.sort(key=lambda g: g["s"])
    return groups


def _series_options(groups: list[dict]) -> str:
    return "".join(f"<option>{html.escape(x)}</option>"
                   for x in sorted({g["series"] for g in groups}))


def write_viewer(groups: list[dict]) -> None:
    """A browser for the gallery: a hero carousel over a filmstrip of trials.

    Metadata is INLINED rather than fetched — over file:// a fetch of
    manifest.json is CORS-blocked and the page would come up empty. Images are
    referenced by relative path, never embedded; the gallery is ~400 MB.

    Feedback is the one thing fetched at runtime, because it changes between
    regenerations. Served (via scripts/gallery_serve.py) it round-trips to disk;
    opened straight off file:// the fetch fails and the page degrades to
    localStorage plus a clipboard copy.
    """
    page = _fill(TEMPLATE, {
        "DATA": _inline(groups),
        "FEEDBACK": _inline(feedback_snapshot()),
        "DIRV": _inline(direction_snapshot()),
        "PUBV": _inline(publish_snapshot()),
        "SERIES": _series_options(groups),
    })
    (GALLERY / "viewer.html").write_text(page)


_IMAGE_EXT = (".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif")
_DIR_FIELDS = ("label", "root", "rounds", "parent_of_root", "canon", "canon_norm",
               "order", "order_norm", "lineage", "best")


def board_rows(groups: list[dict]) -> list[dict]:
    """One row per plate that has directions, one card per direction.

    `main` is what the board shows by default: a plate with a ledger or at
    least two directions, unless every render on it is `original` (pre-studio
    work with nothing to steer). The rest appear behind "every plate".
    """
    rows = []
    for g in groups:
        if g.get("ref"):
            continue
        dirs = g.get("dirs") or {}
        by_key: dict[str, list] = {}
        for s in g["shots"]:
            if not s["n"].lower().endswith(_IMAGE_EXT):  # a stray .DS_Store is no direction
                continue
            by_key.setdefault(s.get("dk") or "", []).append([s["p"], s["n"], s["t"], s["ts"]])
        keys = list(dirs) + sorted(k for k in by_key if k and k not in dirs)
        if not keys:
            continue
        cards = []
        for k in keys:
            info = dirs.get(k) or {}
            card = {f: info.get(f) for f in _DIR_FIELDS if info.get(f) not in (None, "", [])}
            card["k"] = k
            # no ledger row: the key is a filename variant (`x-faithful`)
            card.setdefault("label", k[2:] if k.startswith("x-") else k)
            card["shots"] = by_key.get(k, [])
            cards.append(card)
        cards.sort(key=lambda c: (c["k"] != "original", str(c.get("root") or c["k"])))
        all_original = set(keys) <= {"original"}
        rows.append({
            "s": g["s"], "series": g["series"], "ledger": bool(dirs),
            "main": (bool(dirs) or len(keys) >= 2) and not all_original,
            "loose": len(by_key.get("", [])),
            "cards": cards,
        })
    # ledgered studio plates are what the board is for: they come first
    rows.sort(key=lambda r: (not r["ledger"], r["s"]))
    return rows


def write_board(groups: list[dict]) -> None:
    """gallery/board.html: every plate's directions side by side, to judge
    approaches (WORKS / MAYBE / DEAD END) rather than single renders."""
    page = _fill(BOARD, {
        "ROWS": _inline(board_rows(groups)),
        "FEEDBACK": _inline(feedback_snapshot()),
        "DIRV": _inline(direction_snapshot()),
        "SERIES": _series_options(groups),
    })
    (GALLERY / "board.html").write_text(page)


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PromptPlot Gallery</title>
<style>
:root{--bg:#e6e7ea;--card:#fafafa;--ink:#15181e;--dim:#69707c;--line:#c9ced6;
--ring:#2f6df6;--keep:#1b7038;--rework:#b26a00;--cut:#9a1b2f;--sheet:#f1eee5;--new:#7c3aed;
--flavour:#1f6f8b;--archive:#5f6773;--pub:#b0197e}
@media(prefers-color-scheme:dark){:root{--bg:#0e1116;--card:#171b21;--ink:#e5e8ec;
--dim:#828b98;--line:#272d36;--ring:#5c9cff;--keep:#4fbe77;--rework:#e0a33c;--cut:#ff7089;
--new:#b196ff;--flavour:#5bbcd8;--archive:#9aa3ae;--pub:#f07ccf}}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);display:flex;flex-direction:column;
font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
header{background:var(--card);border-bottom:1px solid var(--line);padding:9px 16px;
display:flex;gap:10px;align-items:center;flex-wrap:wrap;flex:0 0 auto}
h1{font-size:14px;margin:0;font-weight:650;letter-spacing:-.01em}
input,select,button,textarea{font:inherit;padding:5px 9px;border:1px solid var(--line);
border-radius:4px;background:var(--bg);color:var(--ink)}
button{cursor:pointer}
.keys{margin-left:auto;color:var(--dim);font-size:11.5px;white-space:nowrap}
.pos{color:var(--dim);font-size:12.5px;font-variant-numeric:tabular-nums}
.live{font-size:11px;padding:2px 7px;border-radius:3px;border:1px solid var(--line);color:var(--dim)}
.live.on{border-color:var(--keep);color:var(--keep)}

.hero{flex:1 1 auto;min-height:0;display:grid;grid-template-columns:48px 1fr 320px;
align-items:center;gap:10px;padding:10px 12px;border:2px solid transparent;border-radius:6px}
.hero.focused{border-color:var(--ring)}
.hero img{max-width:100%;max-height:100%;object-fit:contain;background:var(--sheet);
display:block;margin:0 auto;border:1px solid var(--line);cursor:zoom-in}
.nav{height:80px;font-size:22px;color:var(--dim);background:var(--card)}
.nav:hover{color:var(--ink)}
.stage{min-width:0;min-height:0;height:100%;display:flex;flex-direction:column;gap:6px}
.frame{flex:1 1 auto;min-height:0;display:flex;align-items:center;justify-content:center}
.cap{flex:0 0 auto;text-align:center}
.cap .t{font-size:13px;font-weight:650}
.cap .s{font-size:11.5px;color:var(--dim)}
.cap .x{font-size:11.5px;color:var(--dim);font-variant-numeric:tabular-nums}
.tier{display:inline-block;font-size:10px;text-transform:uppercase;letter-spacing:.06em;
padding:1px 6px;border-radius:3px;border:1px solid var(--line);color:var(--dim);margin-right:6px}
.tier.current,.tier.promoted{border-color:var(--keep);color:var(--keep)}
.tier.cut{border-color:var(--cut);color:var(--cut)}
.tier.archive{border-color:var(--archive);color:var(--archive)}
header a{color:var(--ring);font-size:12.5px;text-decoration:none}
header a:hover{text-decoration:underline}
header label{font-size:12.5px;color:var(--dim)}
.toast{position:fixed;left:50%;bottom:170px;transform:translateX(-50%);z-index:30;
background:var(--ink);color:var(--bg);padding:6px 12px;border-radius:4px;font-size:12px;
opacity:0;transition:opacity .2s;pointer-events:none;max-width:80vw}
.toast.on{opacity:.95}
.swipebtn{font-size:12.5px;font-weight:650;border-color:var(--ink)}
.swipebtn[aria-pressed=true]{background:var(--ink);color:var(--bg)}

/* ---- swipe mode: one render fills the viewport ---- */
.swipe{position:fixed;inset:0;z-index:25;background:var(--sheet);display:none;
overscroll-behavior:none;user-select:none;-webkit-user-select:none;color:#1a1d22}
.swipe.on{display:block}
.swtop,.swbot{position:absolute;left:0;right:0;display:flex;gap:12px;align-items:center;
padding:0 16px;font-size:12px;background:rgba(241,238,229,.9);z-index:3}
.swtop{top:0;height:38px;border-bottom:1px solid rgba(0,0,0,.08)}
.swbot{bottom:0;height:32px;border-top:1px solid rgba(0,0,0,.08);color:#5b616b}
.swplate{font-weight:650;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.swpos{font-variant-numeric:tabular-nums;color:#5b616b;white-space:nowrap}
.swtop button{font-size:11px;padding:3px 8px;background:transparent;color:#1a1d22;border-color:rgba(0,0,0,.2)}
.swdir{position:absolute;top:38px;left:0;right:0;z-index:3;display:flex;gap:6px;align-items:center;
flex-wrap:wrap;padding:5px 16px;font-size:11.5px;background:rgba(241,238,229,.75)}
.swdir:empty{display:none}
.swdir .swlab{font-weight:650}
.swdir .chip{border-color:rgba(0,0,0,.18);color:#5b616b}
.swdir .chip b{color:#1a1d22}
.swdir .chip.was{border-color:var(--rework);color:#8a5200}
.swcard{position:absolute;inset:70px 16px 40px;display:flex;align-items:center;justify-content:center;
touch-action:none;cursor:grab;will-change:transform}
.swcard.drag{cursor:grabbing}
.swcard.snap{transition:transform .18s ease-out}
.swcard img{max-width:100%;max-height:100%;object-fit:contain;display:block;pointer-events:none;
-webkit-user-drag:none;box-shadow:0 2px 14px rgba(0,0,0,.14)}
.swcard.fly{z-index:2;pointer-events:none;transition:transform .42s ease-in,opacity .42s ease-in .1s}
.stamp{position:absolute;top:16%;left:50%;transform:translateX(-50%) rotate(-11deg);opacity:0;
font:800 44px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
letter-spacing:.08em;text-transform:uppercase;padding:6px 16px;border:5px solid currentColor;
border-radius:8px;background:rgba(255,255,255,.72);pointer-events:none}
.stamp.promote{color:#1b7038}.stamp.keep{color:#1f6f8b}.stamp.rework{color:#b26a00}
.stamp.archive{color:#5f6773}.stamp.cut{color:#9a1b2f}
.swend{position:absolute;inset:0;display:none;align-items:center;justify-content:center;
color:#5b616b;font-size:14px}
.swend.on{display:flex}
.swnotebox{position:absolute;left:50%;bottom:48px;transform:translateX(-50%);z-index:4;
width:min(640px,calc(100vw - 32px));display:none}
.swnotebox.on{display:block}
.swnotebox input{width:100%;font-size:14px;padding:9px 12px;background:#fff;color:#1a1d22;
border:2px solid #b26a00;border-radius:5px}
.swtally{display:flex;gap:6px;align-items:center;font-variant-numeric:tabular-nums;white-space:nowrap}
.swtally b{color:#1a1d22;font-weight:650}
.tv{padding:0 5px;border-radius:3px;color:#fff}
.tv.promote{background:#1b7038}.tv.keep{background:#1f6f8b}.tv.rework{background:#b26a00}
.tv.archive{background:#5f6773}.tv.cut{background:#9a1b2f}
.swkeys{margin-left:auto;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
@media(max-width:700px){.swkeys{display:none}}

/* ---- NEW: rendered since the last verdict on its drawing ---- */
.newbtn{font-size:12.5px;font-weight:650;border-color:var(--new);color:var(--new);
font-variant-numeric:tabular-nums}
.newbtn[aria-pressed=true]{background:var(--new);color:#fff;border-color:transparent}
.newbtn.none{border-color:var(--line);color:var(--dim);font-weight:400}
.tier.new{border-color:var(--new);background:var(--new);color:#fff;font-weight:650}
.tier.new.seen{background:transparent;color:var(--new)}
.newdot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--new);
margin-right:7px;vertical-align:1px}
.cap .t .n{font-size:11px;font-weight:500;color:var(--new);margin-left:7px}
.thumb.fresh{outline:2px solid var(--new);outline-offset:-2px}
.thumb .nw{position:absolute;top:3px;left:3px;font-size:8.5px;font-weight:700;
letter-spacing:.05em;padding:0 3px;border-radius:2px;border:1px solid var(--new);
background:var(--new);color:#fff}
.thumb .nw.seen{background:var(--card);color:var(--new)}

/* ---- feedback panel ---- */
.fb{min-width:0;height:100%;display:flex;flex-direction:column;gap:8px;
background:var(--card);border:1px solid var(--line);border-radius:5px;padding:10px}
.fb h2{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--dim);margin:0}
.pub{font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;padding:5px 0;font-weight:600;
background:transparent;border:1px solid var(--pub);color:var(--pub)}
.pub[aria-pressed=true]{background:var(--pub);color:#fff;border-color:transparent}
.verdicts{display:flex;gap:4px}
.verdicts button{flex:1;min-width:0;font-size:9.5px;text-transform:uppercase;letter-spacing:.03em;
padding:6px 0;position:relative}
.verdicts button{padding-top:9px}
.verdicts button sup{position:absolute;top:1px;left:0;right:0;font-size:7.5px;line-height:1;color:var(--dim)}
.verdicts button[aria-pressed=true]{color:#fff;border-color:transparent;font-weight:650}
.verdicts button[aria-pressed=true] sup{color:#fff}
.verdicts button[data-v=promote][aria-pressed=true]{background:var(--keep)}
.verdicts button[data-v=keep][aria-pressed=true]{background:var(--flavour)}
.verdicts button[data-v=rework][aria-pressed=true]{background:var(--rework)}
.verdicts button[data-v=archive][aria-pressed=true]{background:var(--archive)}
.verdicts button[data-v=cut][aria-pressed=true]{background:var(--cut)}

/* ---- direction: the approach behind this render ---- */
.dir{border:1px solid var(--line);border-radius:4px;padding:6px 8px;display:flex;
flex-direction:column;gap:4px;font-size:11.5px}
.dir .dhead{display:flex;gap:6px;align-items:baseline}
.dir .dlabel{font-weight:650;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.dir .dmeta{color:var(--dim);font-size:10.5px;font-variant-numeric:tabular-nums}
.chips{display:flex;gap:4px;flex-wrap:wrap}
.chip{font-size:10px;padding:0 5px;border-radius:3px;border:1px solid var(--line);color:var(--dim)}
.chip b{font-weight:600;color:var(--ink)}
.dv{font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;padding:1px 6px;
border-radius:3px;border:1px solid var(--line);color:var(--dim);white-space:nowrap}
.dv.works{background:var(--keep);color:#fff;border-color:transparent}
.dv.maybe{background:var(--rework);color:#fff;border-color:transparent}
.dv.dead_end{background:var(--cut);color:#fff;border-color:transparent}
.dbtns{display:flex;gap:4px}
.dbtns button{flex:1;font-size:9.5px;text-transform:uppercase;letter-spacing:.04em;padding:4px 0}
.dbtns button[aria-pressed=true]{color:#fff;border-color:transparent;font-weight:650}
.dbtns button[data-d=works][aria-pressed=true]{background:var(--keep)}
.dbtns button[data-d=maybe][aria-pressed=true]{background:var(--rework)}
.dbtns button[data-d=dead_end][aria-pressed=true]{background:var(--cut)}
.noteWrap{position:relative;flex:1 1 auto;display:flex}
textarea{width:100%;resize:none;line-height:1.45;font-size:12.5px}
.ac{position:absolute;left:0;right:0;bottom:100%;margin-bottom:4px;max-height:190px;
overflow:auto;background:var(--card);border:1px solid var(--ring);border-radius:4px;
display:none;z-index:9}
.ac.on{display:block}
.ac div{padding:4px 8px;font-size:11.5px;cursor:pointer;white-space:nowrap;
overflow:hidden;text-overflow:ellipsis}
.ac div.sel,.ac div:hover{background:var(--ring);color:#fff}
.fb .hint{font-size:10.5px;color:var(--dim)}
.fb .save{font-weight:650}
.saved{font-size:11px;color:var(--dim);min-height:15px}

/* ---- plot panel ---- */
.pl{border-top:1px solid var(--line);padding-top:8px;display:flex;flex-direction:column;gap:6px}
.pl h2{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--dim);margin:0}
.plstate{font-size:11px;color:var(--dim)}
.plstate.ready{color:var(--keep)}
.plstate.warn{color:var(--rework)}
.plstate.err{color:var(--cut)}
.pllayers{display:flex;gap:4px;flex-wrap:wrap}
.pllayers button{font-size:10.5px;padding:3px 7px;font-variant-numeric:tabular-nums}
.pllayers button[aria-pressed=true]{background:var(--ring);color:#fff;border-color:transparent}
.plbtns{display:flex;gap:5px}
.plbtns button{flex:1;font-size:10.5px;text-transform:uppercase;letter-spacing:.05em;padding:6px 0}
.plbtns button:disabled{opacity:.4;cursor:not-allowed}
#plgo{font-weight:650}
.plopts{display:flex;gap:6px;font-size:10.5px;color:var(--dim)}
.plopts label{display:flex;align-items:center;gap:3px}
.plopts input{width:52px;font-size:10.5px}
.plwait{font-size:11.5px;font-weight:650;color:var(--rework);display:none}
.plwait.on{display:block}
.plprog{font-size:10.5px;color:var(--dim);font-variant-numeric:tabular-nums}
#plbar{width:100%;height:6px}
.pljobs{display:flex;gap:5px}
.pljobs select{flex:1;font-size:10.5px;min-width:0}
.pljobs button{font-size:10.5px;text-transform:uppercase;letter-spacing:.05em;padding:4px 8px}
.pllog{margin:0;font:10.5px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--dim);
max-height:84px;overflow:auto;white-space:pre-wrap;word-break:break-word}

.strip{flex:0 0 auto;background:var(--card);border-top:1px solid var(--line);padding:7px 12px;
border:2px solid transparent}
.strip.focused{border-color:var(--ring)}
.striphead{font-size:11px;color:var(--dim);text-transform:uppercase;letter-spacing:.07em;
margin-bottom:5px}
.rail{display:flex;gap:8px;overflow-x:auto;padding-bottom:4px}
.thumb{flex:0 0 auto;width:88px;cursor:pointer;border:1px solid var(--line);
border-radius:4px;overflow:hidden;background:var(--sheet);position:relative}
.thumb.on{border-color:var(--ink);border-width:2px}
.thumb img{width:100%;height:104px;object-fit:contain;display:block;background:var(--sheet)}
.thumb .lb{font-size:9.5px;color:var(--dim);padding:2px 4px;background:var(--card);
white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.thumb .dot{position:absolute;top:3px;right:3px;width:8px;height:8px;border-radius:50%}
.dot.promote{background:var(--keep)}.dot.keep{background:var(--flavour)}
.dot.rework{background:var(--rework)}.dot.archive{background:var(--archive)}.dot.cut{background:var(--cut)}
.thumb .dot.pub{top:14px;background:var(--pub)}
.thumb.shelved img{opacity:.5}
dialog{border:0;padding:0;background:transparent;max-width:99vw;max-height:99vh}
dialog::backdrop{background:rgba(5,7,10,.92)}
dialog img{max-width:99vw;max-height:94vh;background:var(--sheet);display:block}
dialog p{color:#ddd;font-size:12px;text-align:center;margin:6px 0 0}
@media(max-width:900px){.hero{grid-template-columns:40px 1fr}.fb{display:none}}
</style></head><body>
<header>
  <h1>PromptPlot Gallery</h1>
  <button id="swipebtn" class="swipebtn" aria-pressed="false"
    title="Swipe through undecided renders, newest first (s)">Swipe</button>
  <button id="newbtn" class="newbtn" aria-pressed="false"
    title="Only renders made since the last verdict on their drawing (n = next new)">New · 0</button>
  <input id="q" placeholder="filter drawings…">
  <select id="ser"><option value="">all series</option>__SERIES__</select>
  <select id="status" title="Render verdict">
    <option value="">every verdict</option><option value="undecided">undecided</option>
    <option value="promote">promote</option><option value="keep">keep</option>
    <option value="rework">rework</option><option value="archive">archive</option>
    <option value="cut">cut</option><option value="published">published</option></select>
  <select id="dirv" title="Verdict on the render's direction">
    <option value="">any direction</option><option value="works">works</option>
    <option value="maybe">maybe</option><option value="dead_end">dead end</option>
    <option value="unjudged">unjudged</option></select>
  <label title="Show renders in the archive/ and cut/ tiers">
    <input type="checkbox" id="arch"> show archived</label>
  <label><input type="checkbox" id="plot"> plottable only</label>
  <a href="board.html" title="Every plate's directions side by side">Directions board &#8599;</a>
  <span class="live" id="live">offline</span>
  <span class="keys" id="keys"></span>
  <span class="pos" id="pos"></span>
</header>

<div class="hero focused" id="hero">
  <button class="nav" id="prev" title="previous">&#8249;</button>
  <div class="stage">
    <div class="frame"><img id="big" alt=""></div>
    <div class="cap">
      <div class="t" id="title"></div>
      <div class="s" id="sub"></div>
      <div class="x" id="stats"></div>
      <div class="x" id="round"></div>
    </div>
  </div>
  <div class="fb">
    <h2>Feedback</h2>
    <button id="pub" class="pub" aria-pressed="false"
      title="Publish this plate to the portfolio site, or take it down (p)">Publish to site</button>
    <div class="verdicts" id="verdicts"></div>
    <div class="dir" id="dir"></div>
    <div class="noteWrap">
      <textarea id="note" placeholder="What should change? Type @ to reference another plate."></textarea>
      <div class="ac" id="ac"></div>
    </div>
    <div class="hint">@ references another plate · agents read these before reworking</div>
    <button class="save" id="save">Save feedback</button>
    <div class="saved" id="savedmsg"></div>

    <div class="pl" id="pl">
      <h2>Plot</h2>
      <div class="plstate" id="plstate">checking…</div>
      <div class="pllayers" id="pllayers"></div>
      <div class="plbtns">
        <button id="plframe" title="Mandatory pen-up trace of the paper edge and margin">Trace frame</button>
        <button id="plgo">Send layer</button>
        <button id="plplate" disabled title="Every layer as one job: frame, then a pen-swap wait per layer">Plot plate</button>
      </div>
      <div class="plopts">
        <label title="Strokes per batch: the pause / resume granularity">batch
          <input id="plbatch" type="number" min="0" step="50" value="400"></label>
        <label title="Park at (0,0) for an origin check every N strokes (0 = never)">re-zero
          <input id="plrezero" type="number" min="0" step="250" value="2000"></label>
      </div>
      <div class="plwait" id="plwait"></div>
      <div class="plbtns">
        <button id="plcont" disabled title="Pen swapped / origin checked — carry on">Continue</button>
        <button id="plpause" disabled title="Stop at the end of this batch; the job stays resumable">Pause</button>
        <button id="plstop">Stop</button>
      </div>
      <progress id="plbar" max="1" value="0"></progress>
      <div class="plprog" id="plprog"></div>
      <div class="pljobs">
        <select id="pljobs"><option value="">no saved jobs</option></select>
        <button id="plresume" disabled title="Reopen the port on a saved job and continue from its cursor">Resume</button>
      </div>
      <pre class="pllog" id="pllog"></pre>
    </div>
  </div>
</div>

<div class="strip" id="strip">
  <div class="striphead" id="striphead"></div>
  <div class="rail" id="rail"></div>
</div>

<dialog id="lb"><img id="lbi" alt=""><p id="lbc"></p></dialog>
<div class="swipe" id="swipe" aria-hidden="true">
  <div class="swtop">
    <span class="swplate" id="swplate"></span>
    <span class="swpos" id="swpos"></span>
    <button id="swexit" title="Back to the viewer at this render (Esc)">esc &#183; viewer</button>
  </div>
  <div class="swdir" id="swdir"></div>
  <div class="swcard" id="swcard"><img id="swimg" alt="" draggable="false">
    <div class="stamp" id="swstamp"></div></div>
  <div class="swend" id="swend">Esc to go back to the viewer</div>
  <div class="swnotebox" id="swnotebox"><input id="swnote" autocomplete="off"
    placeholder="rework — what should change? Enter saves · Esc cancels"></div>
  <div class="swbot"><span class="swtally" id="swtally"></span>
    <span class="swkeys">&#8594; keep &#183; &#8592; archive &#183; &#8593; promote &#183;
      &#8595; rework &#183; x cut &#183; space skip &#183; z undo &#183; w m d direction &#183;
      p publish</span></div>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
const GROUPS = __DATA__;
const FEED0 = __FEEDBACK__;   // render-verdict snapshot from index time, so file:// works
const DIRV0 = __DIRV__;       // direction verdicts at index time: {subject: {key: {v, note, w}}}
const PUBV0 = __PUBV__;       // plates published to the site at index time: {"subject|name": {v, w}}
const KEY = 'ppgallery.v3';
const SEEN_KEY = 'ppgallery.seen.v1';
const RVERDICTS = ['promote', 'keep', 'rework', 'archive', 'cut'];   // keys 1..5
const DKEYS = { w: 'works', m: 'maybe', d: 'dead_end' };
const DLABEL = { works: 'works', maybe: 'maybe', dead_end: 'dead end' };
let FB = {};        // target -> saved record (from disk when served); render AND direction scope
let online = false; // true once /feedback.json answers
let view = GROUPS, gi = 0, si = 0, focus = 'hero';
let draft = {};     // target -> {verdict, note} not yet saved
let BASE = FEED0.global || 0;  // Juan's last review; frozen once the page has loaded
let newOnly = false, NEWN = 0, seenTimer = null;
let SEEN = {};      // path -> 1 once shown in the hero >1 s; styling only, never clears NEW
let RV = {}, RN = {}, DV = {};  // render verdict by path / by subject|name; direction verdicts
let PV = {};        // "subject|name" -> {v, w} for every plate published to the site
let judged = [];    // paths judged in this session, for z (back)
try { SEEN = JSON.parse(localStorage.getItem(SEEN_KEY) || '{}') || {}; } catch (_) {}

const $ = id => document.getElementById(id);
const el = (t, c, x) => { const n = document.createElement(t); if (c) n.className = c;
  if (x != null) n.textContent = x; return n; };
const cur = () => view.length ? view[gi].shots[si] : null;
const isRender = r => !!r && (!r.scope || r.scope === 'render');   // old records have no scope
const shelved = t => /^(archive|cut)([/]|$)/.test(String(t));

const ALL_PATHS = [], SHOT_AT = {};
for (const g of GROUPS) for (const s of g.shots) { ALL_PATHS.push(s.p); SHOT_AT[s.p] = s; }

function statline(s) {
  if (s.d == null) return 'render only — no gcode';
  return (s.d / 1000).toFixed(1) + ' m drawn · ' + Math.round(s.r * 100) + '% travel · '
       + s.c + ' pen cycles · ' + s.k + ' pen' + (s.k > 1 ? 's' : '') + ' · ~' + s.m + ' min on Leo';
}

/* NEW-RULE — pure, so scripts can extract and test this block on its own.
   A render is NEW until a verdict on its subject is recorded after it, on it or
   on a newer render. A subject never judged uses `base` (Juan's last review)
   instead. Viewing never clears it; references are never NEW. verdicts: [{p: target, s: subject, w: epoch s}]. */
const IMG = /[.](png|jpe?g|svg|webp|gif)$/i;   // stray .DS_Store etc. are never NEW
function markNew(groups, verdicts, base) {
  const bySub = {}, byPath = {}, byS = {};
  for (const g of groups) { byS[g.s] = g; for (const s of g.shots) byPath[s.p] = g; }
  for (const v of verdicts) {
    const g = byPath[v.p] || byS[v.s];
    if (!g) continue;
    // the judged render's own time; a moved file is found by name in its subject
    const name = v.p.split('/').pop(), exact = g.shots.find(s => s.p === v.p);
    let t = exact ? exact.ts : null;
    if (t == null) for (const s of g.shots) if (s.n === name && (t == null || s.ts > t)) t = s.ts;
    (bySub[g.s] = bySub[g.s] || []).push({ w: v.w, t: t == null ? v.w : t });
  }
  let n = 0;
  for (const g of groups) {
    const vs = bySub[g.s];
    g.fresh = 0;
    for (const s of g.shots) {
      s.fresh = !g.ref && IMG.test(s.p)
             && (vs ? !vs.some(v => v.w >= s.ts && v.t >= s.ts) : s.ts > base);
      if (s.fresh) { g.fresh++; n++; }
    }
  }
  return n;
}
/* /NEW-RULE */

const epochOf = r => { const w = Date.parse((r || {}).when) / 1000; return isFinite(w) ? w : Infinity; };

function verdicts() {   // RENDER scope only: snapshot + disk/browser records, newest per target
  const by = {};
  for (const r of FEED0.records) by[r.p] = { p: r.p, s: r.s, w: r.w };
  for (const t in FB) {
    const r = FB[t];
    if (!isRender(r)) continue;
    const w = Date.parse(r.when) / 1000;
    if (isFinite(w) && (!by[t] || w >= by[t].w)) by[t] = { p: t, s: r.subject, w };
  }
  return Object.values(by);
}

/* PUBLISH-RULE — pure, so a test can run this block in node. The index-time
   snapshot, then the live publish-scope records, newest per plate; an unpublish
   removes the plate. Render and direction records are never looked at. */
function publishIndex(base, fb) {
  const pv = Object.assign({}, base);
  for (const t in fb) {
    const r = fb[t];
    if (!r || r.scope !== 'publish' || !r.basename) continue;
    let w = Date.parse(r.when) / 1000;
    if (!isFinite(w)) w = Infinity;
    const k = (r.subject || '') + '|' + r.basename, old = pv[k];
    if (old && old.w > w) continue;
    if (r.verdict === 'publish') pv[k] = { v: 'publish', w }; else delete pv[k];
  }
  return pv;
}
/* /PUBLISH-RULE */

/* Verdict lookup. RV: by path. RN: by subject|basename, so a verdict survives
   gallery_apply moving the file to another tier. DV: direction verdicts. */
function reindex() {
  RV = {}; RN = {}; DV = {};
  const put = r => {
    if (!RV[r.p] || r.w >= RV[r.p].w) RV[r.p] = r;
    const k = r.s + '|' + r.n;
    if (!RN[k] || r.w >= RN[k].w) RN[k] = r;
  };
  for (const r of FEED0.records)
    put({ p: r.p, s: r.s, n: r.n || r.p.split('/').pop(), v: r.v, w: r.w, note: r.note || '' });
  for (const t in FB) {
    const r = FB[t];
    if (!isRender(r)) continue;
    put({ p: t, s: r.subject, n: t.split('/').pop(), v: r.verdict, w: epochOf(r),
          note: r.note || '', when: r.when });
  }
  for (const s in DIRV0) for (const k in DIRV0[s]) (DV[s] = DV[s] || {})[k] = DIRV0[s][k];
  for (const t in FB) {
    const r = FB[t];
    if (!r || r.scope !== 'direction' || !r.direction) continue;
    const s = r.subject || '', w = epochOf(r), old = (DV[s] || {})[r.direction];
    if (!old || w >= old.w) (DV[s] = DV[s] || {})[r.direction] = { v: r.verdict, note: r.note || '', w };
  }
  PV = publishIndex(PUBV0, FB);
}
const recOf = (g, s) => RV[s.p] || RN[g.s + '|' + s.n] || null;
const verdictOf = (g, s) => (recOf(g, s) || {}).v || null;
const dirOf = (g, s) => (s.dk && (DV[g.s] || {})[s.dk]) || null;
const isPublished = (g, s) => !!PV[g.s + '|' + s.n];

function fmtTime(ts) {
  if (!ts) return '';
  const d = new Date(ts * 1000), z = n => String(n).padStart(2, '0');
  return d.getFullYear() + '-' + z(d.getMonth() + 1) + '-' + z(d.getDate()) + ' '
       + z(d.getHours()) + ':' + z(d.getMinutes());
}
function localStamp() {   // naive local ISO, the shape the server writes in `when`
  const d = new Date(), z = n => String(n).padStart(2, '0');
  return d.getFullYear() + '-' + z(d.getMonth() + 1) + '-' + z(d.getDate()) + 'T'
       + z(d.getHours()) + ':' + z(d.getMinutes()) + ':' + z(d.getSeconds());
}

function roundline(s) {
  const t = s.st || {}, parts = [];
  if (t.r) parts.push(t.r);
  if (t.th) parts.push(t.th);
  if (t.v != null) parts.push('v' + t.v);
  if (t.sc) parts.push(t.sc);
  if (t.vd) parts.push('lead: ' + t.vd);
  if (s.ts) parts.push('rendered ' + fmtTime(s.ts));
  return parts.join('  ·  ');
}

let toastTimer = null;
function toast(msg) {
  const t = $('toast'); t.textContent = msg; t.classList.add('on');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => t.classList.remove('on'), 3200);
}

/* Styling only: mark a NEW render seen once it has held the hero for 1 s.
   Patches the badge in place — a full redraw would reset a note being typed. */
function watchSeen(s) {
  clearTimeout(seenTimer);
  if (!s || !s.fresh || SEEN[s.p]) return;
  seenTimer = setTimeout(() => {
    if (cur() !== s) return;
    SEEN[s.p] = 1;
    try { localStorage.setItem(SEEN_KEY, JSON.stringify(SEEN)); } catch (_) {}
    const b = $('newbadge');
    if (b) { b.classList.add('seen'); b.title = 'new — seen, no verdict yet'; }
    for (const t of $('rail').children)
      if (t.dataset.p === s.p) { const x = t.querySelector('.nw'); if (x) x.classList.add('seen'); }
  }, 1000);
}

/* ---------- feedback load / save ---------- */
function liveBadge() {
  const n = POSTQ.length + (posting ? 1 : 0);
  $('live').textContent = online ? (n ? 'saving… ' + n : 'saving to disk') : 'offline — clipboard only';
  $('live').className = 'live' + (online ? ' on' : '');
}

async function loadFeedback() {
  try {
    const r = await fetch('/feedback.json', { cache: 'no-store' });
    if (!r.ok) throw new Error(r.status);
    FB = (await r.json()).records || {};
    online = true;
  } catch (e) {
    // file:// or no server — fall back to the browser store so the page still works
    online = false;
    try { FB = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (_) { FB = {}; }
  }
  reindex();
  liveBadge();
}

function markdownFor(rec) {
  return ['### ' + rec.verdict.toUpperCase() + ' — ' + rec.target,
          rec.refs.length ? 'see also: ' + rec.refs.join(', ') : '',
          '', rec.note].filter(Boolean).join('\\n');
}

/* One POST at a time, in order: a fast run of keypresses must reach the log in
   the order they were made. */
const POSTQ = [];
let posting = false;
function enqueue(body, ok, fail) { POSTQ.push({ body, ok, fail }); liveBadge(); pump(); }
async function pump() {
  if (posting) return;
  posting = true;
  while (POSTQ.length) {
    const job = POSTQ.shift();
    liveBadge();
    try {
      const r = await fetch('/feedback', { method: 'POST',
        headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(job.body) });
      let out = {};
      try { out = await r.json(); } catch (_) {}
      if (!r.ok) throw new Error(out.error || ('HTTP ' + r.status));
      job.ok(out);
    } catch (e) { job.fail(e); }
  }
  posting = false;
  liveBadge();
}

function persistLocal() { try { localStorage.setItem(KEY, JSON.stringify(FB)); } catch (_) {} }

/* Record FB[target] = rec now (optimistic), then send it. On a refusal the
   previous record comes back and `onFail` says so. */
function commit(target, body, onFail) {
  const had = Object.prototype.hasOwnProperty.call(FB, target), prev = FB[target];
  const mine = Object.assign({}, body, { when: localStamp() });
  if (!mine.scope) mine.scope = 'render';
  FB[target] = mine;
  if (!online) { persistLocal(); return; }
  enqueue(body,
    out => { if (FB[target] === mine && out.entry) { FB[target] = out.entry; reindex(); } },
    e => {
      if (FB[target] === mine) { if (had) FB[target] = prev; else delete FB[target]; }
      onFail(e);
    });
}

/* Tonight's decisions by render, for the swipe overlay's counter. A "night"
   runs 06:00 to 06:00, so a session past midnight keeps counting. */
const TONIGHT_KEY = 'ppgallery.tonight.v1';
const nightOf = d => { const x = new Date(d.getTime() - 6 * 3600e3);
  return x.getFullYear() + '-' + (x.getMonth() + 1) + '-' + x.getDate(); };
let TONIGHT = { night: nightOf(new Date()), m: {} };
try { const t = JSON.parse(localStorage.getItem(TONIGHT_KEY) || 'null');
      if (t && t.night === TONIGHT.night && t.m) TONIGHT = t; } catch (_) {}
function saveTonight() { try { localStorage.setItem(TONIGHT_KEY, JSON.stringify(TONIGHT)); } catch (_) {} }

/* The one path every render verdict takes (buttons, keys 1-5, swipes). */
function saveRender(g, s, verdict, note, onFail) {
  const refs = (note.match(/@[^\\s,;]+/g) || []).map(x => x.slice(1));
  const body = { target: s.p, subject: g.s, verdict, note, refs };
  const night = TONIGHT.m[s.p];
  commit(s.p, body, e => {
    if (night === undefined) delete TONIGHT.m[s.p]; else TONIGHT.m[s.p] = night;
    saveTonight(); reindex(); onFail(e);
  });
  TONIGHT.night = nightOf(new Date()); TONIGHT.m[s.p] = verdict; saveTonight();
  delete draft[s.p];
  judged.push(s.p);
  if (judged.length > 500) judged.shift();
  reindex();
  if (!online && note.trim() && navigator.clipboard) {
    navigator.clipboard.writeText(markdownFor(body)).then(
      () => toast('no server — note copied to clipboard'),
      () => toast('no server — stored in this browser only'));
  } else if (!online) toast(verdict + ' — stored in this browser only (no server)');
  return body;
}

/* Save the render verdict (the drafted one when `verdict` is null) with the note
   on screen. advance=true moves to the next undecided render. */
function recordRender(verdict, advance) {
  const s = cur(); if (!s) return;
  const g = view[gi], d = draft[s.p] || {};
  verdict = verdict || d.verdict || verdictOf(g, s);
  if (!verdict) { $('savedmsg').textContent = 'pick a verdict first'; return; }
  const note = $('note').value;
  saveRender(g, s, verdict, note, e => {
    draft[s.p] = { verdict, note };   // keep what was typed
    rebuild(true);
    toast('NOT saved — ' + s.n + ': ' + e.message);
  });
  const next = advance ? nextUndecidedPath() : null;   // before the view reshuffles
  rebuild(true);
  if (next) goTo(next);
  else if (advance) toast('nothing undecided left in this view');
}

/* W / M / D: a verdict on the DIRECTION of a render (the one on screen). */
function recordDirection(v, g, s) {
  if (!s) { s = cur(); if (!s) return; g = view[gi]; }
  if (!s.dk) { toast('this render has no direction'); return; }
  const info = (g.dirs || {})[s.dk] || {};
  const target = g.s + '/@direction/' + s.dk;
  const body = { scope: 'direction', target, subject: g.s, direction: s.dk,
                 label: info.label || s.dk, root: info.root || null, verdict: v,
                 note: ((DV[g.s] || {})[s.dk] || {}).note || '' };
  const redraw = () => { reindex(); if (SW.on) swShow(); else rebuild(true); };
  commit(target, body, e => { redraw();
    toast('direction NOT saved — ' + (info.label || s.dk) + ': ' + e.message); });
  redraw();
  toast((info.label || s.dk) + ' — ' + DLABEL[v] + (online ? '' : ' (this browser only)'));
}

/* p / "Publish to site": toggle whether this plate goes to the portfolio site.
   The exporter ships the render with its gcode, so a render without one cannot. */
function recordPublish(g, s) {
  if (!s) { s = cur(); if (!s) return; g = view[gi]; }
  if (!s.g) { toast('no gcode beside this render — nothing to export'); return; }
  const target = g.s + '/@publish/' + s.n, verdict = isPublished(g, s) ? 'unpublish' : 'publish';
  const body = { scope: 'publish', target, subject: g.s, basename: s.n, verdict, note: '' };
  const redraw = () => { reindex(); if (SW.on) swShow(); else rebuild(true); };
  commit(target, body, e => { redraw();
    toast('publish NOT saved — ' + s.n + ': ' + e.message); });
  redraw();
  toast(s.n + (verdict === 'publish' ? ' — published to site' : ' — taken off the site')
        + (online ? '' : ' (this browser only)'));
}

/* ---------- @ autocomplete ---------- */
let acItems = [], acSel = 0;
function acHide() { $('ac').className = 'ac'; acItems = []; }
function acUpdate() {
  const ta = $('note'), upto = ta.value.slice(0, ta.selectionStart);
  const m = upto.match(/@([^\\s,;]*)$/);
  if (!m) return acHide();
  const term = m[1].toLowerCase();
  acItems = ALL_PATHS.filter(p => p.toLowerCase().includes(term)).slice(0, 40);
  if (!acItems.length) return acHide();
  acSel = 0;
  const box = $('ac'); box.textContent = '';
  acItems.forEach((p, i) => {
    const d = el('div', i === acSel ? 'sel' : '', p);
    d.onmousedown = e => { e.preventDefault(); acPick(i); };
    box.append(d);
  });
  box.className = 'ac on';
}
function acPick(i) {
  const ta = $('note'), start = ta.selectionStart;
  const upto = ta.value.slice(0, start), m = upto.match(/@([^\\s,;]*)$/);
  if (!m) return acHide();
  const before = upto.slice(0, upto.length - m[0].length);
  ta.value = before + '@' + acItems[i] + ' ' + ta.value.slice(start);
  ta.selectionStart = ta.selectionEnd = (before + '@' + acItems[i] + ' ').length;
  acHide(); ta.focus();
}

/* ---------- render ---------- */
function shotOk(g, s, st, dv) {
  if (!$('arch').checked && shelved(s.t)) return false;
  if (newOnly && !s.fresh) return false;
  if (st === 'published') { if (!isPublished(g, s)) return false; }
  else if (st) {
    const v = verdictOf(g, s);
    if (st === 'undecided' ? (v || g.ref) : v !== st) return false;
  }
  if (dv) {
    const x = (dirOf(g, s) || {}).v || null;
    if (dv === 'unjudged' ? x : x !== dv) return false;
  }
  return true;
}

function buildView() {
  const q = $('q').value.toLowerCase(), ser = $('ser').value, only = $('plot').checked;
  const st = $('status').value, dv = $('dirv').value;
  const v = [];
  for (const g of GROUPS) {
    if (ser && g.series !== ser) continue;
    if (q && !g.s.toLowerCase().includes(q)) continue;
    if (only && !g.shots.some(s => s.g)) continue;
    const shots = g.shots.filter(s => shotOk(g, s, st, dv));
    if (!shots.length) continue;
    v.push(shots.length === g.shots.length ? g : Object.assign({}, g, { shots }));
  }
  // subjects with NEW renders first; otherwise the alphabetical order is kept
  return v.map((g, i) => [g, i]).sort((a, b) => (b[0].fresh > 0) - (a[0].fresh > 0) || a[1] - b[1])
          .map(x => x[0]);
}

function firstNew() {
  gi = 0; si = 0;
  if (view.length && view[0].fresh) si = Math.max(0, view[0].shots.findIndex(s => s.fresh));
}

/* Recompute NEW and the view. keep=true holds the current drawing/version when it
   survives the filter; otherwise lands on the one that slid into its place. */
function rebuild(keep) {
  const s = cur(), gs = view.length ? view[gi].s : null, ogi = gi, osi = si;
  reindex();
  NEWN = markNew(GROUPS, verdicts(), BASE);
  view = buildView();
  const b = $('newbtn');
  b.textContent = 'New · ' + NEWN;
  b.classList.toggle('none', !NEWN);
  b.setAttribute('aria-pressed', newOnly);
  if (!keep) { firstNew(); draw(); return; }
  gi = view.findIndex(g => g.s === gs);
  if (gi < 0) { gi = Math.min(ogi, Math.max(0, view.length - 1)); si = 0; }
  else {
    si = view[gi].shots.findIndex(x => s && x.p === s.p);
    if (si < 0) si = Math.min(osi, view[gi].shots.length - 1);
  }
  draw();
}

function applyFilter() { rebuild(false); }

/* Walk the view from the current render, wrapping, and return the first path
   that passes `test` (the current render itself is never returned). */
function scanFrom(test) {
  if (!view.length) return null;
  const total = view.reduce((a, g) => a + g.shots.length, 0);
  let g = gi, k = si;
  for (let i = 0; i < total; i++) {
    if (++k >= view[g].shots.length) { g = (g + 1) % view.length; k = 0; }
    if (g === gi && k === si) break;
    if (test(view[g], view[g].shots[k])) return view[g].shots[k].p;
  }
  return null;
}

/* n: the next NEW render after the current one, across subjects, wrapping. */
function nextNew() {
  const p = scanFrom((g, s) => s.fresh);
  if (p) goTo(p); else $('pos').textContent = 'no new renders';
}

const nextUndecidedPath = () => scanFrom((g, s) => !verdictOf(g, s) && !g.ref);
function nextUndecided() {
  const p = nextUndecidedPath();
  if (p) goTo(p); else toast('nothing undecided left in this view');
}

function locate(path) {
  for (let a = 0; a < view.length; a++) {
    const k = view[a].shots.findIndex(x => x.p === path);
    if (k >= 0) return [a, k];
  }
  return null;
}

/* Show `path`. force=true (deep links) loosens the filters until it is visible:
   an archived render turns on "show archived"; anything else clears the rest. */
function goTo(path, force) {
  let at = locate(path);
  if (!at && force) {
    const s = SHOT_AT[path];
    if (!s) { toast('not in the gallery: ' + path); return false; }
    if (shelved(s.t) && !$('arch').checked) { $('arch').checked = true; rebuild(true); at = locate(path); }
    if (!at) {
      $('q').value = ''; $('ser').value = ''; $('plot').checked = false;
      $('status').value = ''; $('dirv').value = ''; newOnly = false;
      rebuild(true); at = locate(path);
    }
  }
  if (!at) return false;
  gi = at[0]; si = at[1];
  draw();
  return true;
}

function back() {   // z: the last render judged in this session
  while (judged.length) {
    const p = judged.pop();
    if (!cur() || cur().p !== p) { goTo(p, true); return; }
  }
  toast('nothing judged yet in this session');
}

function hashPath() {
  const m = location.hash.match(/^#p=(.+)$/);
  if (!m) return null;
  try { return decodeURIComponent(m[1]); } catch (_) { return null; }
}

function setFocus(f) { focus = f; draw(); }

function drawDirection(g, s) {
  const box = $('dir'); box.textContent = '';
  if (!s.dk) {
    box.append(el('div', 'dmeta', 'no direction — no ledger row or variant for this render'));
    return;
  }
  const info = (g.dirs || {})[s.dk] || {}, dv = dirOf(g, s);
  const head = el('div', 'dhead');
  const lab = el('span', 'dlabel', info.label || s.dk.replace(/^x-/, ''));
  lab.title = 'direction ' + s.dk;
  head.append(lab, el('span', 'dv ' + (dv ? dv.v : ''), dv ? (DLABEL[dv.v] || dv.v) : 'unjudged'));
  const meta = [];
  if (info.root) meta.push('root ' + info.root);
  if ((info.rounds || []).length) meta.push('rounds ' + info.rounds.join(' '));
  const best = info.best || {};
  if (best.round) meta.push('best ' + best.round
    + (best.art_avg != null ? ' · art ' + best.art_avg + (best.art_min != null ? '/' + best.art_min : '') : '')
    + (best.sci != null ? ' · sci ' + best.sci : ''));
  const chips = el('div', 'chips');
  for (const k of ['canon', 'order', 'lineage']) {
    if (!info[k]) continue;
    const c = el('span', 'chip'); c.title = k + ': ' + info[k];
    const txt = String(info[k]);
    c.append(el('b', null, k + ' '), txt.length > 60 ? txt.slice(0, 59) + '…' : txt);
    chips.append(c);
  }
  const btns = el('div', 'dbtns');
  for (const key of ['w', 'm', 'd']) {
    const v = DKEYS[key], b = el('button', null, key.toUpperCase() + ' · ' + DLABEL[v]);
    b.dataset.d = v; b.title = 'direction verdict (key ' + key + ')';
    b.setAttribute('aria-pressed', !!dv && dv.v === v);
    b.onclick = () => recordDirection(v);
    btns.append(b);
  }
  box.append(head);
  if (meta.length) box.append(el('div', 'dmeta', meta.join('  ·  ')));
  if (chips.children.length) box.append(chips);
  box.append(btns);
}

function draw() {
  $('hero').classList.toggle('focused', focus === 'hero');
  $('strip').classList.toggle('focused', focus === 'strip');
  $('keys').textContent = (focus === 'hero'
    ? '←→ drawing  ·  ↓ versions'
    : '←→ version  ·  ↑ drawings')
    + '  ·  1–5 promote/keep/rework/archive/cut  ·  w m d direction'
    + '  ·  p publish  ·  z back  ·  n new';

  if (!view.length) {
    $('title').textContent = newOnly ? 'nothing new — every render has a verdict after it'
                                     : 'nothing matches';
    $('big').removeAttribute('src');
    $('rail').textContent = ''; $('pos').textContent = ''; $('sub').textContent = '';
    $('stats').textContent = ''; $('round').textContent = ''; $('dir').textContent = '';
    $('striphead').textContent = ''; watchSeen(null); return;
  }
  const g = view[gi], s = g.shots[si];
  try { history.replaceState(null, '', '#p=' + encodeURIComponent(s.p)); } catch (_) {}
  $('big').src = s.p; $('big').alt = s.n;
  $('title').textContent = '';
  if (g.fresh) $('title').append(el('span', 'newdot'));
  $('title').append(g.s);
  if (g.fresh) $('title').append(el('span', 'n', g.fresh + ' new'));
  const sub = el('span');
  if (s.fresh) {
    const nb = el('span', 'tier new' + (SEEN[s.p] ? ' seen' : ''), 'new');
    nb.id = 'newbadge';
    nb.title = SEEN[s.p] ? 'new — seen, no verdict yet' : 'new — not looked at yet';
    sub.append(nb);
  }
  sub.append(el('span', 'tier ' + s.t.split('/')[0], s.t), s.n);
  $('sub').textContent = ''; $('sub').append(sub);
  $('stats').textContent = statline(s);
  $('round').textContent = roundline(s);
  $('pos').textContent = (gi + 1) + ' / ' + view.length
                       + ' · ' + Object.keys(PV).length + ' published';

  const saved = recOf(g, s), d = draft[s.p] || {};
  const verdict = d.verdict || (saved || {}).v || null;
  const pub = isPublished(g, s);
  $('pub').setAttribute('aria-pressed', pub);
  $('pub').title = (pub ? 'Published — take this plate off the portfolio site'
                        : 'Publish this plate to the portfolio site')
                 + (s.g ? '' : ' (no gcode beside this render: cannot export)') + ' (p)';
  const vs = $('verdicts'); vs.textContent = '';
  RVERDICTS.forEach((k, i) => {
    const b = el('button', null, k); b.dataset.v = k;
    b.prepend(el('sup', null, String(i + 1)));
    b.title = k + ' — key ' + (i + 1) + ' saves now and moves to the next undecided render';
    b.setAttribute('aria-pressed', verdict === k);
    b.onclick = () => { draft[s.p] = Object.assign({}, draft[s.p],
      { verdict: verdict === k ? null : k }); draw(); };
    vs.append(b);
  });
  $('note').value = d.note != null ? d.note : ((saved || {}).note || '');
  $('savedmsg').textContent = saved
    ? 'on record: ' + saved.v + ' · ' + (saved.when ? saved.when.slice(0, 16).replace('T', ' ')
                                                    : fmtTime(saved.w))
      + (saved.p !== s.p ? ' (as ' + saved.p.split('/').slice(-2).join('/') + ')' : '')
    : '';
  drawDirection(g, s);

  $('striphead').textContent = newOnly
    ? g.shots.length + ' new version' + (g.shots.length > 1 ? 's' : '') + ' — no verdict since'
    : (g.shots.length > 1
       ? g.shots.length + ' versions — final first, then every trial'
       : 'only one version of this drawing') + (g.fresh ? '  ·  ' + g.fresh + ' new' : '');
  const rail = $('rail'); rail.textContent = '';
  g.shots.forEach((sh, k) => {
    const t = el('div', 'thumb' + (k === si ? ' on' : '') + (sh.fresh ? ' fresh' : '')
                        + (shelved(sh.t) ? ' shelved' : ''));
    t.dataset.p = sh.p;
    const im = el('img'); im.src = sh.p; im.alt = sh.n; im.loading = 'lazy';
    t.append(im, el('div', 'lb', sh.t));
    if (sh.fresh) t.append(el('div', 'nw' + (SEEN[sh.p] ? ' seen' : ''), 'NEW'));
    const v = verdictOf(g, sh);
    if (v) { const dot = el('div', 'dot ' + v); dot.title = v; t.append(dot); }
    if (isPublished(g, sh)) { const pd = el('div', 'dot pub'); pd.title = 'published to site'; t.append(pd); }
    t.onclick = () => { si = k; focus = 'strip'; draw(); };
    rail.append(t);
  });
  const on = rail.children[si];
  if (on) on.scrollIntoView({ block: 'nearest', inline: 'nearest' });

  if (gcodeOf(s) !== plTarget) plLoadLayers();
  watchSeen(s);
}

function step(d) { gi = (gi + d + view.length) % view.length; si = 0; draw(); }
function shot(d) { if (!view.length) return;
  const n = view[gi].shots.length; si = (si + d + n) % n; draw(); }

$('prev').onclick = () => { focus = 'hero'; step(-1); };
$('next') && ($('next').onclick = () => { focus = 'hero'; step(1); });
$('save').onclick = () => recordRender(null, false);
$('pub').onclick = () => recordPublish();
$('note').addEventListener('input', () => {
  const s = cur(); if (s) draft[s.p] = Object.assign({}, draft[s.p], { note: $('note').value });
  acUpdate();
});
$('note').addEventListener('blur', acHide);
$('note').addEventListener('keydown', e => {
  if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {   // save with the drafted verdict
    e.preventDefault(); acHide(); $('note').blur(); recordRender(null, false); return;
  }
  if (!acItems.length) { if (e.key === 'Escape') $('note').blur(); return; }
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    e.preventDefault(); acSel = (acSel + (e.key === 'ArrowDown' ? 1 : -1) + acItems.length) % acItems.length;
    [...$('ac').children].forEach((c, i) => c.className = i === acSel ? 'sel' : '');
  } else if (e.key === 'Enter' || e.key === 'Tab') { e.preventDefault(); acPick(acSel); }
  else if (e.key === 'Escape') { acHide(); }
});

document.addEventListener('keydown', e => {
  // Cmd+W, Cmd+D, Ctrl+1... belong to the browser: never a verdict.
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  const t = e.target.tagName;
  if (t === 'INPUT' || t === 'SELECT' || t === 'TEXTAREA') return;
  if (SW.on) { swipeKey(e); return; }   // arrows are swipe gestures there
  const map = {
    s:          enterSwipe,
    ArrowUp:    () => setFocus('hero'),
    ArrowDown:  () => setFocus('strip'),
    ArrowLeft:  () => focus === 'hero' ? step(-1) : shot(-1),
    ArrowRight: () => focus === 'hero' ? step(1)  : shot(1),
    n:          nextNew,
    z:          back,
    w:          () => recordDirection('works'),
    m:          () => recordDirection('maybe'),
    d:          () => recordDirection('dead_end'),
    p:          () => recordPublish(),
  };
  RVERDICTS.forEach((v, i) => { map[String(i + 1)] = () => recordRender(v, true); });
  const fn = map[e.key];
  if (!fn || e.repeat && /^[1-5wmdp]$/.test(e.key)) return;   // a held key records once
  // Without preventDefault the page scrolls and a focused button eats the key.
  e.preventDefault();
  fn();
});
// A clicked control keeps focus and would otherwise swallow the next arrow.
document.addEventListener('click', e => {
  if (e.target.tagName === 'BUTTON') e.target.blur();
});
$('big').onclick = () => { const s = cur(); if (!s) return;
  $('lbi').src = s.p; $('lbc').textContent = s.p + (s.g ? '   ·   ' + s.g : '');
  $('lb').showModal(); };
$('lb').onclick = e => { if (e.target.id !== 'lbi') e.target.close && e.target.close(); };
$('newbtn').onclick = () => { newOnly = !newOnly; rebuild(!newOnly); };
['q', 'ser', 'plot', 'status', 'dirv', 'arch'].forEach(id =>
  $(id).addEventListener(id === 'q' ? 'input' : 'change', applyFilter));
window.addEventListener('hashchange', () => {
  const p = hashPath();
  if (p && (!cur() || cur().p !== p)) goTo(p, true);
});
/* ---------- swipe mode ---------- */
/* A fast pass over the art: one undecided, un-archived render at a time,
   newest first across every plate that passes the series / direction / search
   filters. → keep · ← archive · ↑ promote · ↓ rework (+ one-line note) ·
   x cut · space skip · z undo · w m d direction · esc back to the viewer. */
const SW = { on: false, deck: [], i: 0, noteOpen: false, pre: [] };
const SW_FLY = { keep: [1, 0], archive: [-1, 0], promote: [0, -1], rework: [0, 1] };

function buildDeck() {
  const q = $('q').value.toLowerCase(), ser = $('ser').value, only = $('plot').checked;
  const dv = $('dirv').value, out = [];
  for (const g of GROUPS) {
    if (g.ref || (ser && g.series !== ser) || (q && !g.s.toLowerCase().includes(q))) continue;
    for (const s of g.shots) {
      if (shelved(s.t) || !IMG.test(s.p) || verdictOf(g, s) || (only && !s.g)) continue;
      if (dv) { const x = (dirOf(g, s) || {}).v || null; if (dv === 'unjudged' ? x : x !== dv) continue; }
      out.push([g, s]);
    }
  }
  return out.sort((a, b) => (b[1].ts - a[1].ts) || (a[1].p < b[1].p ? -1 : 1));
}

function nextOpen(i) {   // the next deck index still undecided (deck.length = the end)
  for (let j = i + 1; j < SW.deck.length; j++) if (!verdictOf(SW.deck[j][0], SW.deck[j][1])) return j;
  return SW.deck.length;
}

function enterSwipe() {
  reindex();
  SW.deck = buildDeck(); SW.i = 0; SW.on = true;
  $('swipe').classList.add('on');
  $('swipe').setAttribute('aria-hidden', 'false');
  $('swipebtn').setAttribute('aria-pressed', 'true');
  document.documentElement.style.overscrollBehavior = 'none';   // no back-swipe navigation
  swShow();
}

function leaveSwipe() {
  if (SW.noteOpen) swNoteClose();
  const e = SW.deck[Math.min(SW.i, SW.deck.length - 1)];
  SW.on = false;
  $('swipe').classList.remove('on');
  $('swipe').setAttribute('aria-hidden', 'true');
  $('swipebtn').setAttribute('aria-pressed', 'false');
  document.documentElement.style.overscrollBehavior = '';
  rebuild(true);
  if (e) goTo(e[1].p, true);
}

function swTally() {
  const n = {}, box = $('swtally');
  let all = 0;
  for (const p in TONIGHT.m) { n[TONIGHT.m[p]] = (n[TONIGHT.m[p]] || 0) + 1; all++; }
  box.textContent = '';
  box.append(el('b', null, 'tonight ' + all));
  for (const v of RVERDICTS) if (n[v]) box.append(el('span', 'tv ' + v, n[v] + ' ' + v));
}

function swStamp(v, alpha) {
  const st = $('swstamp');
  st.className = 'stamp' + (v ? ' ' + v : '');
  st.textContent = v || '';
  st.style.opacity = v ? String(alpha) : '0';
}

function swShow() {
  const card = $('swcard');
  card.classList.remove('drag');
  card.style.transform = '';
  swStamp(null);
  swTally();
  const e = SW.deck[SW.i], dir = $('swdir');
  dir.textContent = '';
  if (!e) {
    $('swimg').removeAttribute('src');
    $('swplate').textContent = SW.deck.length ? 'all caught up — nothing undecided left here'
                                              : 'nothing undecided matches the filters';
    $('swpos').textContent = SW.deck.length + ' / ' + SW.deck.length + ' undecided';
    $('swend').classList.add('on');
    return;
  }
  $('swend').classList.remove('on');
  const g = e[0], s = e[1];
  $('swimg').src = s.p; $('swimg').alt = s.n;
  $('swplate').textContent = g.s + '  ·  ' + s.n;
  if (s.dk) {
    const info = (g.dirs || {})[s.dk] || {}, dv = dirOf(g, s);
    dir.append(el('span', 'swlab', info.label || s.dk.replace(/^x-/, '')),
               el('span', 'dv ' + (dv ? dv.v : ''), dv ? (DLABEL[dv.v] || dv.v) : 'unjudged'));
    for (const k of ['canon', 'order']) if (info[k]) {
      const c = el('span', 'chip'); c.append(el('b', null, k + ' '), info[k]); dir.append(c);
    }
  }
  const was = verdictOf(g, s);
  if (was) dir.append(el('span', 'chip was', 'judged ' + was + ' — a new verdict replaces it'));
  $('swpos').textContent = (SW.i + 1) + ' / ' + SW.deck.length + ' undecided';
  // preload the next two so the following card appears instantly
  SW.pre = [];
  for (let j = SW.i, k = 0; k < 2; k++) {
    j = nextOpen(j);
    if (j >= SW.deck.length) break;
    const im = new Image(); im.src = SW.deck[j][1].p; SW.pre.push(im);
  }
}

function swFly(v) {   // the decided card leaves in its direction, stamped
  const card = $('swcard'), c = card.cloneNode(true);
  c.removeAttribute('id');
  c.querySelectorAll('[id]').forEach(n => n.removeAttribute('id'));
  c.className = 'swcard fly';
  const st = c.querySelector('.stamp');
  st.className = 'stamp ' + v; st.textContent = v; st.style.opacity = '1';
  $('swipe').append(c);
  const d = SW_FLY[v];
  requestAnimationFrame(() => requestAnimationFrame(() => {
    c.style.transform = d ? 'translate(' + d[0] * 110 + 'vw,' + d[1] * 110 + 'vh) rotate(' + d[0] * 16 + 'deg)'
                          : 'scale(.55)';
    c.style.opacity = '0';
  }));
  setTimeout(() => c.remove(), 520);
}

function swCommit(v, note) {
  const e = SW.deck[SW.i]; if (!e) return;
  const g = e[0], s = e[1];
  if (note == null) note = (recOf(g, s) || {}).note || (draft[s.p] || {}).note || '';
  saveRender(g, s, v, note, err => {
    toast('NOT saved — ' + s.n + ': ' + err.message + ' (z to go back)');
    if (SW.on) swTally();
  });
  swFly(v);
  SW.i = nextOpen(SW.i);
  swShow();
}

function swDecide(v) {
  if (!SW.deck[SW.i]) return;
  if (v === 'rework') { swNoteOpen(); return; }
  swCommit(v, null);
}

function swSkip() {
  if (!SW.deck[SW.i]) return;
  SW.i = nextOpen(SW.i);
  swShow();
}

function swUndo() {
  while (judged.length) {
    const p = judged.pop();
    let j = SW.deck.findIndex(x => x[1].p === p);
    if (j < 0) {   // judged before swipe mode began: put it back in front of us
      let hit = null;
      for (const g of GROUPS) for (const s of g.shots) if (s.p === p) hit = [g, s];
      if (!hit) continue;
      SW.deck.splice(Math.min(SW.i, SW.deck.length), 0, hit);
      j = Math.min(SW.i, SW.deck.length - 1);
    }
    SW.i = j;
    swShow();
    return;
  }
  toast('nothing to undo');
}

function swNoteOpen() {
  const e = SW.deck[SW.i]; if (!e) return;
  SW.noteOpen = true;
  $('swcard').style.transform = 'translateY(36px)';
  swStamp('rework', 0.9);
  $('swnotebox').classList.add('on');
  const inp = $('swnote');
  inp.value = (recOf(e[0], e[1]) || {}).note || '';
  inp.focus();
}

function swNoteClose() {
  SW.noteOpen = false;
  $('swnotebox').classList.remove('on');
  $('swnote').blur();
}

$('swnote').addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    e.preventDefault();
    const note = $('swnote').value.trim();
    swNoteClose(); swCommit('rework', note);
  } else if (e.key === 'Escape') {
    e.preventDefault(); e.stopPropagation();
    swNoteClose(); swShow();
  }
});

function swipeKey(e) {
  if (SW.noteOpen) {   // focus left the note box: only Esc means something
    if (e.key === 'Escape') { e.preventDefault(); swNoteClose(); swShow(); }
    return;
  }
  const map = {
    ArrowRight: () => swDecide('keep'),
    ArrowLeft:  () => swDecide('archive'),
    ArrowUp:    () => swDecide('promote'),
    ArrowDown:  () => swDecide('rework'),
    x:          () => swDecide('cut'),
    ' ':        swSkip,
    z:          swUndo,
    w: () => { const c = SW.deck[SW.i]; if (c) recordDirection('works', c[0], c[1]); },
    m: () => { const c = SW.deck[SW.i]; if (c) recordDirection('maybe', c[0], c[1]); },
    d: () => { const c = SW.deck[SW.i]; if (c) recordDirection('dead_end', c[0], c[1]); },
    p: () => { const c = SW.deck[SW.i]; if (c) recordPublish(c[0], c[1]); },
    Escape:     leaveSwipe,
    s:          leaveSwipe,
  };
  const fn = map[e.key];
  if (!fn) return;
  e.preventDefault();
  if (e.repeat) return;   // a held arrow decides once
  fn();
}

/* Drag (mouse, trackpad click-drag, touch): the card follows the pointer and
   shows the stamp it would get; past the threshold on release it decides. */
function gestureOf(dx, dy, th) {
  if (Math.max(Math.abs(dx), Math.abs(dy)) < th) return null;
  if (Math.abs(dx) >= Math.abs(dy)) return dx > 0 ? 'keep' : 'archive';
  return dy < 0 ? 'promote' : 'rework';
}
function swMove(dx, dy) {
  $('swcard').style.transform = 'translate(' + dx + 'px,' + dy + 'px) rotate(' + dx / 28 + 'deg)';
  const v = gestureOf(dx, dy, 24);
  swStamp(v, Math.min(1, Math.max(Math.abs(dx), Math.abs(dy)) / 130));
}
function swRelease(dx, dy, th) {
  const v = gestureOf(dx, dy, th);
  if (v) { swDecide(v); return; }
  const card = $('swcard');
  card.classList.add('snap'); card.style.transform = ''; swStamp(null);
  setTimeout(() => card.classList.remove('snap'), 200);
}
let swDrag = null;
$('swcard').addEventListener('pointerdown', e => {
  if (!SW.on || SW.noteOpen || !SW.deck[SW.i] || e.button > 0) return;
  swDrag = { x: e.clientX, y: e.clientY };
  $('swcard').setPointerCapture(e.pointerId);
  $('swcard').classList.add('drag');
});
$('swcard').addEventListener('pointermove', e => {
  if (swDrag) swMove(e.clientX - swDrag.x, e.clientY - swDrag.y);
});
$('swcard').addEventListener('pointerup', e => {
  if (!swDrag) return;
  const dx = e.clientX - swDrag.x, dy = e.clientY - swDrag.y;
  swDrag = null; $('swcard').classList.remove('drag');
  swRelease(dx, dy, Math.min(140, window.innerWidth / 5));
});
$('swcard').addEventListener('pointercancel', () => {
  swDrag = null; $('swcard').classList.remove('drag'); swRelease(0, 0, 1);
});
/* Two-finger trackpad swipe: HORIZONTAL only (keep / archive). A vertical
   wheel is too easy to fire by accident to be allowed to promote. */
const SW_WHEEL = { dx: 0, t: null, cool: 0 };
$('swipe').addEventListener('wheel', e => {
  if (!SW.on) return;
  e.preventDefault();
  if (SW.noteOpen || !SW.deck[SW.i] || Date.now() < SW_WHEEL.cool) return;
  if (Math.abs(e.deltaX) <= Math.abs(e.deltaY)) return;
  SW_WHEEL.dx -= e.deltaX * (e.deltaMode === 1 ? 16 : 1);
  clearTimeout(SW_WHEEL.t);
  if (Math.abs(SW_WHEEL.dx) > 240) {
    const v = SW_WHEEL.dx > 0 ? 'keep' : 'archive';
    SW_WHEEL.dx = 0; SW_WHEEL.cool = Date.now() + 700;   // swallow the momentum tail
    swDecide(v);
    return;
  }
  swMove(SW_WHEEL.dx, 0);
  SW_WHEEL.t = setTimeout(() => { SW_WHEEL.dx = 0; swRelease(0, 0, 1); }, 160);
}, { passive: false });
$('swipebtn').onclick = () => (SW.on ? leaveSwipe() : enterSwipe());
$('swexit').onclick = leaveSwipe;
/* ---------- plotter ---------- */
let PL = { enabled: false, busy: false, frame_ok: false };
let plLayers = [], plPick = null, plTarget = null, plTimer = null;

const gcodeOf = s => (s && s.g) ? s.p.replace(/[^/]+$/, '') + s.g : null;

function plSay(msg, cls) {
  const n = $('plstate'); n.textContent = msg; n.className = 'plstate' + (cls ? ' ' + cls : '');
}

async function plState() {
  try {
    const r = await fetch('/plotter/state', { cache: 'no-store' });
    PL = await r.json();
  } catch (_) { PL = { enabled: false, reason: 'no server' }; }
  plRender();
}

async function plLoadLayers() {
  const s = cur(), t = gcodeOf(s);
  plLayers = []; plPick = null; plTarget = t;
  if (t && PL.enabled) {
    try {
      const r = await fetch('/plotter/layers?target=' + encodeURIComponent(t),
                            { cache: 'no-store' });
      const j = await r.json();
      if (r.ok) { plLayers = j.layers || []; if (plLayers.length) plPick = plLayers[0].color; }
    } catch (_) {}
  }
  plRender();
}

function plRender() {
  const s = cur(), t = gcodeOf(s), busy = PL.busy;
  if (!PL.enabled) {
    plSay(PL.reason || 'plotting disabled', 'warn');
  } else if (!t) {
    plSay('no gcode for this render', 'warn');
  } else if (busy && (PL.job || {}).action === 'plate') {
    const j = PL.job;
    plSay(j.waiting_for ? 'waiting for you' : (j.state || '').replace('_', ' ') + '…',
          j.waiting_for ? 'warn' : '');
  } else if (busy) {
    const j = PL.job || {}, p = j.progress;
    plSay((j.action === 'frame' ? 'tracing frame' : 'plotting colour ' + j.color)
          + (p ? ' — ' + p[0] + '/' + p[1] : '') + '…');
  } else if (!PL.frame_ok) {
    plSay('trace the frame first (' + PL.paper + ')', 'warn');
  } else {
    const j = PL.job || {};
    plSay(j.state === 'error' ? j.message
        : (j.message ? j.message + ' · ready' : 'ready · ' + PL.paper), 
          j.state === 'error' ? 'err' : 'ready');
  }

  const box = $('pllayers'); box.textContent = '';
  plLayers.forEach(L => {
    const b = el('button', null, '#' + L.color + ' · ' + L.strokes + ' str');
    b.setAttribute('aria-pressed', plPick === L.color);
    b.onclick = () => { plPick = L.color; plRender(); };
    box.append(b);
  });

  $('plframe').disabled = !PL.enabled || busy;
  $('plgo').disabled = !PL.enabled || busy || plPick == null || !PL.frame_ok;
  $('plplate').disabled = !PL.enabled || busy || !t || !plLayers.length;
  $('plstop').disabled = !busy;
  plRenderJob(busy);
  $('pllog').textContent = (PL.log || []).slice(-8).join('\\n');

  // Poll only while something is moving.
  if (busy && !plTimer) plTimer = setInterval(plState, 1200);
  if (!busy && plTimer) { clearInterval(plTimer); plTimer = null; plLoadJobs(); }
}

function plRenderJob(busy) {
  const j = (PL.job && PL.job.action === 'plate') ? PL.job : null;
  const w = $('plwait');
  w.textContent = (j && j.waiting_for) ? j.message : '';
  w.className = 'plwait' + ((j && j.waiting_for) ? ' on' : '');
  $('plcont').disabled = !(busy && j && j.waiting_for);
  $('plpause').disabled = !(busy && j);
  const pr = j && j.progress, bar = $('plbar');
  if (pr && pr.overall && pr.overall[1]) {
    const u = j.cursor || {}, n = (j.units || []).length;
    bar.max = pr.overall[1]; bar.value = pr.overall[0];
    $('plprog').textContent = 'layer ' + Math.min((u.unit || 0) + 1, n) + '/' + n
      + ' · strokes ' + pr.layer[0] + '/' + pr.layer[1]
      + ' · plate ' + pr.overall[0] + '/' + pr.overall[1]
      + (j.eta_min != null ? ' · ~' + Math.round(j.eta_min) + ' min left' : '')
      + ' · ' + j.id;
  } else { bar.value = 0; $('plprog').textContent = ''; }
  $('plresume').disabled = !PL.enabled || busy || !$('pljobs').value;
}

async function plLoadJobs() {
  if (!PL.enabled) return;
  try {
    const r = await fetch('/plotter/jobs', { cache: 'no-store' });
    const js = ((await r.json()).jobs || []).filter(x => x.resumable);
    const sel = $('pljobs'); sel.textContent = '';
    if (!js.length) sel.append(new Option('no resumable jobs', ''));
    js.forEach(x => {
      const o = (x.progress || {}).overall || [0, 0];
      sel.append(new Option(x.id + ' · ' + x.state + ' · ' + o[0] + '/' + o[1]
        + ' · ' + String(x.target).split('/').pop(), x.id));
    });
  } catch (_) {}
  plRender();
}

async function plPost(url, body) {
  try {
    const r = await fetch(url, { method: 'POST',
      headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) });
    const j = await r.json();
    if (!r.ok) { plSay(j.error || ('HTTP ' + r.status), 'err'); return null; }
    return j;
  } catch (e) { plSay(e.message, 'err'); return null; }
}

$('plframe').onclick = async () => {
  if (!confirm('Trace the paper frame with the pen UP on ' + PL.paper + '?')) return;
  await plPost('/plotter/job', { action: 'frame', confirm: true });
  plState();
};
$('plgo').onclick = async () => {
  const L = plLayers.find(x => x.color === plPick) || {};
  if (!confirm('INK colour ' + plPick + ' (' + (L.strokes || '?') + ' strokes) onto the sheet?\\n\\n'
               + plTarget)) return;
  await plPost('/plotter/job',
               { action: 'layer', target: plTarget, color: plPick, confirm: true });
  plState();
};
$('plstop').onclick = () => plPost('/plotter/stop', {});
$('plplate').onclick = async () => {
  const n = plLayers.length, str = plLayers.reduce((a, L) => a + L.strokes, 0);
  if (!confirm('Plot the WHOLE plate: ' + n + ' layers, ' + str + ' strokes on ' + PL.paper
               + '?\\n\\nIt traces the frame (pen up) first, then parks at (0,0) and waits '
               + 'for you before each pen.\\n\\n' + plTarget)) return;
  await plPost('/plotter/job', { action: 'plate', target: plTarget, confirm: true,
    batch_strokes: +$('plbatch').value || 0, rezero_every: +$('plrezero').value || 0 })
    && plState();   // on a refusal, keep the reason on screen
};
$('plcont').onclick = async () => {
  const j = PL.job || {};
  if (!confirm((j.message || 'Continue?') + '\\n\\nContinue?')) return;
  (await plPost('/plotter/continue', { wait_seq: j.wait_seq })) && plState();
};
$('plpause').onclick = async () => { (await plPost('/plotter/pause', {})) && plState(); };
$('pljobs').onchange = () => plRender();
$('plresume').onclick = async () => {
  const id = $('pljobs').value;
  if (!id) return;
  const retrace = !PL.frame_ok;
  if (!confirm('Resume ' + id + '?\\n\\n' + (retrace
      ? 'No frame traced in this session: it will trace the frame (pen up) first. '
      : '') + 'It waits for you to confirm the head is on the paper corner before inking.'))
    return;
  (await plPost('/plotter/resume', { job_id: id, confirm: true, retrace: retrace }))
    && plState();
};

const DEEP = hashPath();   // #p=<path> (a board card, a shared link): read before draw() rewrites it
loadFeedback().then(() => {
  // Freeze the review cutoff now: a verdict recorded on one drawing in this
  // session must not make every never-judged drawing stop being NEW.
  for (const v of verdicts()) BASE = Math.max(BASE, v.w);
  rebuild(false);   // lands on the first NEW render when there is one
  if (DEEP) goTo(DEEP, true);
  // draw() asked for layers before the server said plotting is enabled; ask again.
  plState().then(plLoadLayers).then(plLoadJobs);
});
</script></body></html>
"""



# The Directions board. A RAW string on purpose: the viewer TEMPLATE above is a
# normal string, so every JS escape in it must be doubled (a raw newline in a JS
# literal once killed the whole viewer). Here JS is written exactly as it runs.
BOARD = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PromptPlot Directions</title>
<style>
:root{--bg:#e6e7ea;--card:#fafafa;--ink:#15181e;--dim:#69707c;--line:#c9ced6;
--ring:#2f6df6;--keep:#1b7038;--rework:#b26a00;--cut:#9a1b2f;--sheet:#f1eee5;--new:#7c3aed;
--flavour:#1f6f8b;--archive:#5f6773}
@media(prefers-color-scheme:dark){:root{--bg:#0e1116;--card:#171b21;--ink:#e5e8ec;
--dim:#828b98;--line:#272d36;--ring:#5c9cff;--keep:#4fbe77;--rework:#e0a33c;--cut:#ff7089;
--new:#b196ff;--flavour:#5bbcd8;--archive:#9aa3ae}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--card);border-bottom:1px solid var(--line);
padding:9px 16px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
h1{font-size:14px;margin:0;font-weight:650;letter-spacing:-.01em}
a{color:var(--ring);text-decoration:none}
a:hover{text-decoration:underline}
select,button{font:inherit;padding:5px 9px;border:1px solid var(--line);border-radius:4px;
background:var(--bg);color:var(--ink);max-width:100%}
header select{max-width:220px}
button{cursor:pointer}
button:disabled{opacity:.45;cursor:not-allowed}
label{font-size:12.5px;color:var(--dim)}
.live{font-size:11px;padding:2px 7px;border-radius:3px;border:1px solid var(--line);color:var(--dim);
margin-left:auto}
.live.on{border-color:var(--keep);color:var(--keep)}
main{padding:12px 16px 40px;max-width:1500px;margin:0 auto}
.totals{font-size:12.5px;color:var(--dim);margin:2px 0 10px;font-variant-numeric:tabular-nums}
.totals b{color:var(--ink);font-weight:650}
.patterns{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:10px;margin-bottom:14px}
.pat{background:var(--card);border:1px solid var(--line);border-radius:5px;padding:8px 10px}
.pat h2,.plate h2{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--dim);
margin:0 0 6px;font-weight:600}
.pat .none{font-size:12px;color:var(--dim)}
.prow{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:8px;align-items:center;
font-size:12.5px;padding:2px 0;border-top:1px solid var(--line)}
.prow:first-of-type{border-top:0}
.prow .nm{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.prow .w{color:var(--keep);font-variant-numeric:tabular-nums;font-weight:650}
.prow .d{color:var(--cut);font-variant-numeric:tabular-nums;font-weight:650}
.plate{margin:0 0 18px}
.plate h2{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;font-size:12px;
text-transform:none;letter-spacing:0;color:var(--ink);font-weight:650}
.plate h2 .sub{color:var(--dim);font-weight:400;font-size:11.5px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px}
.card{background:var(--card);border:1px solid var(--line);border-radius:5px;overflow:hidden;
display:flex;flex-direction:column;min-width:0}
.card.works{border-color:var(--keep);box-shadow:inset 0 3px 0 var(--keep)}
.card.maybe{border-color:var(--rework);box-shadow:inset 0 3px 0 var(--rework)}
.card.dead_end{border-color:var(--cut);box-shadow:inset 0 3px 0 var(--cut)}
.card.dead_end img{opacity:.55}
.card a.open{color:inherit;display:block;text-decoration:none}
.card a.open:hover .lab{text-decoration:underline}
.card img{width:100%;height:190px;object-fit:contain;background:var(--sheet);display:block;
border-bottom:1px solid var(--line)}
.card .noimg{height:190px;display:flex;align-items:center;justify-content:center;color:var(--dim);
font-size:12px;background:var(--sheet);border-bottom:1px solid var(--line)}
.card .shelvedimg{opacity:.5}
.body{padding:7px 9px 9px;display:flex;flex-direction:column;gap:5px;flex:1}
.head{display:flex;gap:6px;align-items:baseline}
.lab{font-weight:650;font-size:13px;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;
display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.root{font-size:10.5px;color:var(--dim);font-variant-numeric:tabular-nums;white-space:nowrap}
.chips{display:flex;gap:4px;flex-wrap:wrap}
.chip{font-size:10px;padding:0 5px;border-radius:3px;border:1px solid var(--line);color:var(--dim);
max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.chip b{font-weight:600;color:var(--ink)}
.meta{font-size:11px;color:var(--dim);font-variant-numeric:tabular-nums}
.tally{display:flex;gap:4px;flex-wrap:wrap;font-size:10.5px;font-variant-numeric:tabular-nums}
.tally span{padding:0 5px;border-radius:3px;border:1px solid var(--line);color:var(--dim)}
.tally .promote{border-color:var(--keep);color:var(--keep)}
.tally .keep{border-color:var(--flavour);color:var(--flavour)}
.tally .rework{border-color:var(--rework);color:var(--rework)}
.tally .archive{border-color:var(--archive);color:var(--archive)}
.tally .cut{border-color:var(--cut);color:var(--cut)}
.dvrow{display:flex;gap:4px;align-items:center;margin-top:auto;padding-top:3px}
.dv{font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;padding:1px 6px;
border-radius:3px;border:1px solid var(--line);color:var(--dim);white-space:nowrap;margin-right:auto}
.dv.works{background:var(--keep);color:#fff;border-color:transparent}
.dv.maybe{background:var(--rework);color:#fff;border-color:transparent}
.dv.dead_end{background:var(--cut);color:#fff;border-color:transparent}
.dvrow button{font-size:10px;padding:3px 8px;font-weight:650}
.dvrow button[aria-pressed=true]{color:#fff;border-color:transparent}
.dvrow button[data-d=works][aria-pressed=true]{background:var(--keep)}
.dvrow button[data-d=maybe][aria-pressed=true]{background:var(--rework)}
.dvrow button[data-d=dead_end][aria-pressed=true]{background:var(--cut)}
.empty{color:var(--dim);font-size:13px;padding:30px 0;text-align:center}
.msg{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:9;background:var(--ink);
color:var(--bg);padding:6px 12px;border-radius:4px;font-size:12px;opacity:0;transition:opacity .2s;
pointer-events:none;max-width:90vw}
.msg.on{opacity:.95}
@media(max-width:600px){.cards{grid-template-columns:1fr 1fr}.card img,.card .noimg{height:140px}
.live{margin-left:0}}
</style></head><body>
<header>
  <h1>Directions</h1>
  <a href="viewer.html">&#8592; viewer</a>
  <select id="ser"><option value="">all series</option>__SERIES__</select>
  <select id="dirv" title="Direction verdict">
    <option value="">any verdict</option><option value="works">works</option>
    <option value="maybe">maybe</option><option value="dead_end">dead end</option>
    <option value="unjudged">unjudged</option></select>
  <select id="canon" title="Style canon"><option value="">any canon</option></select>
  <select id="order" title="Abstract order"><option value="">any order</option></select>
  <label title="Also plates with a single direction, or only pre-studio (original) renders">
    <input type="checkbox" id="all"> every plate</label>
  <span class="live" id="live">offline</span>
</header>
<main>
  <div class="totals" id="totals"></div>
  <div class="patterns" id="patterns"></div>
  <div id="rows"></div>
</main>
<div class="msg" id="msg" role="status" aria-live="polite"></div>
<script>
const ROWS = __ROWS__;
const FEED0 = __FEEDBACK__;
const DIRV0 = __DIRV__;
const DLABEL = { works: 'works', maybe: 'maybe', dead_end: 'dead end' };
const RVERDICTS = ['promote', 'keep', 'rework', 'archive', 'cut'];
let FB = {}, online = false, RV = {}, RN = {}, DV = {};

const $ = id => document.getElementById(id);
const el = (t, c, x) => { const n = document.createElement(t); if (c) n.className = c;
  if (x != null) n.textContent = x; return n; };
const isRender = r => !!r && (!r.scope || r.scope === 'render');
const shelved = t => /^(archive|cut)([/]|$)/.test(String(t));
const epochOf = r => { const w = Date.parse((r || {}).when) / 1000; return isFinite(w) ? w : Infinity; };
const canonOf = c => c.canon_norm || 'unknown';
const orderOf = c => c.order_norm || 'unknown';

let msgTimer = null;
function say(m) { const n = $('msg'); n.textContent = m; n.classList.add('on');
  clearTimeout(msgTimer); msgTimer = setTimeout(() => n.classList.remove('on'), 3200); }

function reindex() {
  RV = {}; RN = {}; DV = {};
  const put = r => {
    if (!RV[r.p] || r.w >= RV[r.p].w) RV[r.p] = r;
    const k = r.s + '|' + r.n;
    if (!RN[k] || r.w >= RN[k].w) RN[k] = r;
  };
  for (const r of FEED0.records) put({ p: r.p, s: r.s, n: r.n || r.p.split('/').pop(), v: r.v, w: r.w });
  for (const t in FB) {
    const r = FB[t];
    if (isRender(r)) put({ p: t, s: r.subject, n: t.split('/').pop(), v: r.verdict, w: epochOf(r) });
  }
  for (const s in DIRV0) for (const k in DIRV0[s]) (DV[s] = DV[s] || {})[k] = DIRV0[s][k];
  for (const t in FB) {
    const r = FB[t];
    if (!r || r.scope !== 'direction' || !r.direction) continue;
    const s = r.subject || '', w = epochOf(r), old = (DV[s] || {})[r.direction];
    if (!old || w >= old.w) (DV[s] = DV[s] || {})[r.direction] = { v: r.verdict, note: r.note || '', w };
  }
}
const renderVerdict = (s, sh) => (RV[sh[0]] || RN[s + '|' + sh[1]] || {}).v || null;
const dirVerdict = (s, k) => ((DV[s] || {})[k] || {}).v || null;

async function load() {
  try {
    const r = await fetch('/feedback.json', { cache: 'no-store' });
    if (!r.ok) throw new Error(r.status);
    FB = (await r.json()).records || {};
    online = true;
  } catch (_) {
    online = false;   // file://: the snapshot baked in at index time is all there is
    FB = {};
  }
  $('live').textContent = online ? 'saving to disk' : 'offline — read only';
  $('live').className = 'live' + (online ? ' on' : '');
  reindex();
  render();
}

/* One POST at a time; optimistic, rolled back on a refusal. */
const Q = [];
let busy = false;
async function pump() {
  if (busy) return;
  busy = true;
  while (Q.length) {
    const job = Q.shift();
    try {
      const r = await fetch('/feedback', { method: 'POST',
        headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(job.body) });
      let out = {};
      try { out = await r.json(); } catch (_) {}
      if (!r.ok) throw new Error(out.error || ('HTTP ' + r.status));
      job.ok(out);
    } catch (e) { job.fail(e); }
  }
  busy = false;
}

function judge(row, card, v) {
  if (!online) { say('open the board through gallery_serve.py to record verdicts'); return; }
  const target = row.s + '/@direction/' + card.k;
  const body = { scope: 'direction', target, subject: row.s, direction: card.k,
                 label: card.label || card.k, root: card.root || null, verdict: v,
                 note: ((DV[row.s] || {})[card.k] || {}).note || '' };
  const had = Object.prototype.hasOwnProperty.call(FB, target), prev = FB[target];
  const mine = Object.assign({}, body, { when: new Date().toISOString() });
  FB[target] = mine;
  reindex(); render();
  Q.push({ body,
    ok: out => { if (FB[target] === mine && out.entry) { FB[target] = out.entry; reindex(); } },
    fail: e => { if (FB[target] === mine) { if (had) FB[target] = prev; else delete FB[target]; }
                 reindex(); render(); say('NOT saved — ' + (card.label || card.k) + ': ' + e.message); } });
  pump();
}

function pick(shots) {   // the latest render not shelved, from current/ when there is one
  const open = shots.filter(x => !shelved(x[2])), pool = open.length ? open : shots;
  const curr = pool.filter(x => x[2] === 'current'), from = curr.length ? curr : pool;
  return from.reduce((a, b) => (b[3] > a[3] ? b : a), from[0]);
}

function fillSelect(id, values) {
  const sel = $(id), keep = sel.value;
  while (sel.options.length > 1) sel.remove(1);
  for (const v of values) sel.append(new Option(v, v));
  sel.value = values.includes(keep) ? keep : '';
}

function patterns(allCards) {
  const box = $('patterns'); box.textContent = '';
  for (const [title, keyOf] of [['by canon', canonOf], ['by order', orderOf]]) {
    const agg = {};
    for (const [row, c] of allCards) {
      const v = dirVerdict(row.s, c.k);
      if (v !== 'works' && v !== 'dead_end') continue;
      const a = agg[keyOf(c)] = agg[keyOf(c)] || { works: 0, dead_end: 0 };
      a[v]++;
    }
    const pat = el('div', 'pat');
    pat.append(el('h2', null, 'Works vs dead end, ' + title));
    const names = Object.keys(agg).sort((a, b) =>
      (agg[b].works + agg[b].dead_end) - (agg[a].works + agg[a].dead_end) || a.localeCompare(b));
    if (!names.length) pat.append(el('div', 'none', 'no WORKS or DEAD END verdicts yet'));
    for (const n of names) {
      const r = el('div', 'prow');
      const nm = el('span', 'nm', n); nm.title = n;
      r.append(nm, el('span', 'w', agg[n].works + ' works'), el('span', 'd', agg[n].dead_end + ' dead end'));
      pat.append(r);
    }
    box.append(pat);
  }
}

function render() {
  const ser = $('ser').value, dv = $('dirv').value, cn = $('canon').value, od = $('order').value;
  const every = $('all').checked;
  const pool = ROWS.filter(r => every || r.main);
  const allCards = [];
  for (const r of pool) for (const c of r.cards) allCards.push([r, c]);
  fillSelect('canon', [...new Set(allCards.map(x => canonOf(x[1])))].sort());
  fillSelect('order', [...new Set(allCards.map(x => orderOf(x[1])))].sort());

  const tally = { works: 0, maybe: 0, dead_end: 0 };
  let renders = 0;
  for (const [r, c] of allCards) {
    const v = dirVerdict(r.s, c.k); if (v) tally[v]++;
    renders += c.shots.length;
  }
  const t = $('totals'); t.textContent = '';
  const judgedN = tally.works + tally.maybe + tally.dead_end;
  for (const [n, lab] of [[pool.length, ' plates · '], [allCards.length, ' directions · '],
                          [renders, ' renders  —  '], [tally.works, ' works · '],
                          [tally.maybe, ' maybe · '], [tally.dead_end, ' dead end · '],
                          [allCards.length - judgedN, ' unjudged']]) {
    t.append(el('b', null, String(n)), lab);
  }
  patterns(allCards);

  const out = $('rows'); out.textContent = '';
  let shown = 0;
  for (const row of pool) {
    if (ser && row.series !== ser) continue;
    const cards = row.cards.filter(c => {
      const v = dirVerdict(row.s, c.k);
      if (dv && (dv === 'unjudged' ? v : v !== dv)) return false;
      if (cn && canonOf(c) !== cn) return false;
      if (od && orderOf(c) !== od) return false;
      return true;
    });
    if (!cards.length) continue;
    shown++;
    const sec = el('section', 'plate');
    const h = el('h2', null, row.s);
    h.append(el('span', 'sub', row.cards.length + ' direction' + (row.cards.length > 1 ? 's' : '')
      + (row.ledger ? ' · ledger' : ' · no ledger') + (row.loose ? ' · ' + row.loose + ' unassigned' : '')));
    sec.append(h);
    const grid = el('div', 'cards');
    for (const c of cards) grid.append(cardEl(row, c));
    sec.append(grid);
    out.append(sec);
  }
  if (!shown) out.append(el('div', 'empty', 'no direction matches these filters'));
}

function cardEl(row, c) {
  const v = dirVerdict(row.s, c.k);
  const card = el('div', 'card' + (v ? ' ' + v : ''));
  const best = c.shots.length ? pick(c.shots) : null;
  const a = el('a', 'open');
  if (best) {
    a.href = 'viewer.html#p=' + encodeURIComponent(best[0]);
    a.title = 'open ' + best[0] + ' in the viewer';
    const im = el('img', shelved(best[2]) ? 'shelvedimg' : null);
    im.src = best[0]; im.alt = best[1]; im.loading = 'lazy';
    a.append(im);
  } else {
    a.append(el('div', 'noimg', 'no render on disk'));
  }
  const body = el('div', 'body');
  const head = el('div', 'head');
  head.append(el('span', 'lab', c.label || c.k));
  if (c.root) head.append(el('span', 'root', c.root));
  head.title = 'direction ' + c.k;
  a.append(body);
  body.append(head);
  const chips = el('div', 'chips');
  for (const k of ['canon', 'order', 'lineage']) {
    if (!c[k]) continue;
    const ch = el('span', 'chip'); ch.title = k + ': ' + c[k];
    ch.append(el('b', null, k + ' '), String(c[k]));
    chips.append(ch);
  }
  if (chips.children.length) body.append(chips);
  const meta = [];
  if ((c.rounds || []).length) meta.push('rounds ' + c.rounds.join(' '));
  const b = c.best || {};
  if (b.round) meta.push('best ' + b.round
    + (b.art_avg != null ? ' · art ' + b.art_avg + (b.art_min != null ? '/' + b.art_min : '') : '')
    + (b.sci != null ? ' · sci ' + b.sci : ''));
  if (meta.length) body.append(el('div', 'meta', meta.join('  ·  ')));
  const tl = el('div', 'tally'), n = {};
  let open = 0;
  for (const sh of c.shots) { const x = renderVerdict(row.s, sh); if (x) n[x] = (n[x] || 0) + 1; else open++; }
  tl.append(el('span', null, c.shots.length + ' render' + (c.shots.length === 1 ? '' : 's')));
  for (const k of RVERDICTS) if (n[k]) tl.append(el('span', k, n[k] + ' ' + k));
  if (open && c.shots.length) tl.append(el('span', null, open + ' undecided'));
  body.append(tl);

  const dvr = el('div', 'dvrow');
  dvr.append(el('span', 'dv' + (v ? ' ' + v : ''), v ? DLABEL[v] : 'unjudged'));
  for (const [key, val] of [['W', 'works'], ['M', 'maybe'], ['D', 'dead_end']]) {
    const btn = el('button', null, key);
    btn.dataset.d = val;
    btn.title = online ? DLABEL[val] : 'read only — open via scripts/gallery_serve.py to record';
    btn.disabled = !online;
    btn.setAttribute('aria-pressed', v === val);
    btn.onclick = e => { e.preventDefault(); e.stopPropagation(); judge(row, c, val); };
    dvr.append(btn);
  }
  card.append(a, dvr);
  return card;
}

['ser', 'dirv', 'canon', 'order', 'all'].forEach(id => $(id).addEventListener('change', render));
// Back from the viewer with new verdicts: pick them up.
document.addEventListener('visibilitychange', () => { if (!document.hidden && online) load(); });
reindex();
render();
load();
</script></body></html>
"""

def build(full: bool = False, views_only: bool = False) -> list[dict]:
    """Everything main() does, callable from tests. Returns the manifests."""
    if views_only:
        manifests = load_manifests()
    else:
        manifests = []
        paired = 0
        for subject in subject_dirs():
            paired += colocate_pairs(subject)
            m = build_manifest(subject, None if full else load_cache(subject))
            hits = m.pop("cached", 0)
            (subject / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
            manifests.append(m)
            logger.info("%4d  %s%s", m["count"], m["subject"],
                        "" if hits == m["count"] else f"  ({m['count'] - hits} indexed)")
        write_index(manifests)
        write_print_queue(manifests)
        if paired:
            logger.info("co-located %d gcode file(s) with their render", paired)
    groups = build_groups(manifests)
    write_viewer(groups)
    write_board(groups)
    return manifests


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--full", action="store_true",
                    help="re-hash and re-replay every file instead of reusing the manifests")
    ap.add_argument("--views-only", action="store_true",
                    help="only rewrite viewer.html + board.html from the manifests on disk")
    args = ap.parse_args()
    logging.basicConfig(level=logging.WARNING if args.quiet else logging.INFO,
                        format="%(message)s")

    if not GALLERY.is_dir():
        logger.error("no gallery/ yet — run scripts/gallery_import.py first")
        return 1
    t0 = time.monotonic()
    manifests = build(full=args.full, views_only=args.views_only)
    logger.info("--- %d subjects, %d files -> %s (%.1f s) ---",
                len(manifests), sum(m["count"] for m in manifests),
                "viewer.html + board.html" if args.views_only else "gallery/INDEX.md",
                time.monotonic() - t0)
    return 0


if __name__ == "__main__":
    sys.exit(main())
