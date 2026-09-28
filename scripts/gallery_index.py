"""Rebuild gallery/**/manifest.json and gallery/INDEX.md from what is on disk.

Idempotent: promoting a future render is a move plus a re-run of this script.

The archived GCode carries no provenance header (see CLAUDE.md "Gallery and feedback"), so
everything here is derived -- stats by replaying the toolpath, seed by reading
the filename. Files written after the provenance-header fix will carry their own
metadata and this script prefers that when present.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STUDIO = REPO / "studio"

sys.path.insert(0, str(Path(__file__).resolve().parent))
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
        if path.is_dir() and path.name in ("promoted", "variants", "candidates", "current", "trials", "cut"):
            if path.parent not in out:
                out.append(path.parent)
    if (GALLERY / "references").is_dir():
        out.append(GALLERY / "references")
    return sorted(out)


TIER_RANK = {"current": 0, "promoted": 1, "candidates/prior-approved": 2,
             "candidates": 3, "variants": 4, "trials": 5, "cut": 6}


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


def build_manifest(subject: Path) -> dict:
    records = []
    for path in sorted(subject.rglob("*")):
        if not path.is_file() or path.name in ("manifest.json", "README.md"):
            continue
        rel_tier = path.parent.relative_to(subject)
        rec = {
            "file": path.name,
            "tier": str(rel_tier) if str(rel_tier) != "." else "loose",
            "rel": str(path.relative_to(subject)),
            "kind": "gcode" if path.suffix == ".gcode" else "render",
            "bytes": path.stat().st_size,
            # Local time to the second, with its offset: the viewer compares it
            # against feedback `when` stamps (naive local) to decide what is NEW.
            "mtime": datetime.fromtimestamp(path.stat().st_mtime)
            .astimezone().isoformat(timespec="seconds"),
            "sha256": sha256(path),
            "seed": seed_from(path.name),
        }
        if path.suffix == ".gcode":
            rec["stats"] = gcode_stats(path)
        counterpart = path.with_suffix(".png" if path.suffix == ".gcode" else ".gcode")
        rec["pair"] = counterpart.name if counterpart.exists() else None
        records.append(rec)
    return {
        "subject": str(subject.relative_to(GALLERY)),
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "count": len(records),
        "files": records,
    }


def write_index(manifests: list[dict]) -> None:
    lines = [
        "# Gallery index",
        "",
        "Generated by `scripts/gallery_index.py` — do not edit by hand.",
        "",
        f"{sum(m['count'] for m in manifests)} files across {len(manifests)} subjects. "
        "Tiers record where a file came from, not a quality judgement: "
        "`promoted` was already moved out of staging, `variants` was a loose working file, "
        "`candidates` came from `_staging/` and is **not** approved.",
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
            if f["kind"] != "gcode" or not f.get("stats"):
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


def feedback_snapshot() -> dict:
    """The latest verdict per plate, inlined so NEW works over file:// too.

    The viewer decides NEW itself (so a verdict recorded in the page updates it
    instantly); this is only its starting data. `subjects` and `global` are the
    latest verdict per subject and anywhere -- the global one is Juan's last
    review, the cutoff for subjects he has never judged.
    """
    records, subjects = [], {}
    for r in fb.latest_by_target().values():
        w = _epoch(r.get("when", ""))
        if w is None:
            continue
        records.append({"p": r["target"], "s": r.get("subject"), "w": w, "v": r.get("verdict")})
        s = r.get("subject") or ""
        subjects[s] = max(subjects.get(s, 0), w)
    return {"records": records, "subjects": subjects,
            "global": max(subjects.values(), default=0)}


_ROUND = re.compile(r"^r?(\d+)$", re.I)
_PNG = re.compile(r"[\w.\-]+\.png", re.I)


def ledger_rows(subject: str) -> dict[str, dict]:
    """render basename -> {round, thesis, scores} from studio/<slug>/LEDGER.md.

    The studio lead keeps a `## Rounds` table (round | parent | thesis | render |
    art avg/min | sci t/f/l | verdict | note). Columns are found by header name,
    and a missing or malformed ledger yields nothing -- never an error.
    """
    path = STUDIO / fb.slug_for(subject) / "LEDGER.md"
    try:
        text = path.read_text()
    except OSError:
        return {}
    out: dict[str, dict] = {}
    head: list[str] | None = None
    in_rounds = False
    for line in text.splitlines():
        if line.startswith("#"):
            in_rounds = line.lstrip("#").strip().lower().startswith("rounds")
            head = None
            continue
        if not in_rounds or not line.strip().startswith("|"):
            continue
        cells = [c.strip().strip("`* ") for c in line.strip().strip("|").split("|")]
        if head is None:
            head = [c.lower() for c in cells]
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue

        def col(name: str, head: list[str] = head, cells: list[str] = cells) -> str:
            for i, h in enumerate(head):
                if h.split()[:1] == [name] and i < len(cells):
                    return cells[i]
            return ""

        rnd = col("round")
        m = _ROUND.match(rnd)
        rnd = f"r{int(m.group(1)):02d}" if m else rnd
        scores = " · ".join(
            f"{k} {v}" for k, v in (("art", col("art")), ("sci", col("sci"))) if v and v != "—"
        )
        row = {"r": rnd or None, "th": col("thesis") or None, "sc": scores or None,
               "vd": col("verdict") or None}
        for name in _PNG.findall(col("render")):
            out[name.rsplit("/", 1)[-1]] = row
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


def write_viewer(manifests: list[dict]) -> None:
    """A browser for the gallery: a hero carousel over a filmstrip of trials.

    Metadata is INLINED rather than fetched — over file:// a fetch of
    manifest.json is CORS-blocked and the page would come up empty. Images are
    referenced by relative path, never embedded; the gallery is ~400 MB.

    Feedback is the one thing fetched at runtime, because it changes between
    regenerations. Served (via scripts/gallery_serve.py) it round-trips to disk;
    opened straight off file:// the fetch fails and the page degrades to
    localStorage plus a clipboard copy.
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
                }
            )
        if not shots:
            continue
        shots.sort(key=lambda x: (TIER_RANK.get(x["t"], 9), x["n"]))
        group = {"s": subject, "series": subject.split("/")[0], "shots": shots}
        if subject == "references":
            group["ref"] = True  # inputs to reconstruct from, never NEW
        groups.append(group)
    groups.sort(key=lambda g: g["s"])

    opts = "".join(f"<option>{x}</option>" for x in sorted({g["series"] for g in groups}))
    html = TEMPLATE.replace("__DATA__", json.dumps(groups, separators=(",", ":")))
    html = html.replace("__FEEDBACK__", json.dumps(feedback_snapshot(), separators=(",", ":")))
    html = html.replace("__SERIES__", opts)
    (GALLERY / "viewer.html").write_text(html)


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PromptPlot Gallery</title>
<style>
:root{--bg:#e6e7ea;--card:#fafafa;--ink:#15181e;--dim:#69707c;--line:#c9ced6;
--ring:#2f6df6;--keep:#1b7038;--rework:#b26a00;--cut:#9a1b2f;--sheet:#f1eee5;--new:#7c3aed}
@media(prefers-color-scheme:dark){:root{--bg:#0e1116;--card:#171b21;--ink:#e5e8ec;
--dim:#828b98;--line:#272d36;--ring:#5c9cff;--keep:#4fbe77;--rework:#e0a33c;--cut:#ff7089;
--new:#b196ff}}
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
.verdicts{display:flex;gap:5px}
.verdicts button{flex:1;font-size:10.5px;text-transform:uppercase;letter-spacing:.05em;padding:6px 0}
.verdicts button[aria-pressed=true]{color:#fff;border-color:transparent;font-weight:650}
.verdicts button[data-v=promote][aria-pressed=true]{background:var(--keep)}
.verdicts button[data-v=rework][aria-pressed=true]{background:var(--rework)}
.verdicts button[data-v=cut][aria-pressed=true]{background:var(--cut)}
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
.dot.promote{background:var(--keep)}.dot.rework{background:var(--rework)}.dot.cut{background:var(--cut)}
dialog{border:0;padding:0;background:transparent;max-width:99vw;max-height:99vh}
dialog::backdrop{background:rgba(5,7,10,.92)}
dialog img{max-width:99vw;max-height:94vh;background:var(--sheet);display:block}
dialog p{color:#ddd;font-size:12px;text-align:center;margin:6px 0 0}
@media(max-width:900px){.hero{grid-template-columns:40px 1fr}.fb{display:none}}
</style></head><body>
<header>
  <h1>PromptPlot Gallery</h1>
  <button id="newbtn" class="newbtn" aria-pressed="false"
    title="Only renders made since the last verdict on their drawing (n = next new)">New · 0</button>
  <input id="q" placeholder="filter drawings…">
  <select id="ser"><option value="">all series</option>__SERIES__</select>
  <label style="font-size:12.5px;color:var(--dim)">
    <input type="checkbox" id="plot"> plottable only</label>
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
    <div class="verdicts" id="verdicts"></div>
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
        <button id="plstop">Stop</button>
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
<script>
const GROUPS = __DATA__;
const FEED0 = __FEEDBACK__;   // verdict snapshot from index time, so file:// works
const KEY = 'ppgallery.v3';
const SEEN_KEY = 'ppgallery.seen.v1';
let FB = {};        // target -> saved record (from disk when served)
let online = false; // true once /feedback.json answers
let view = GROUPS, gi = 0, si = 0, focus = 'hero';
let draft = {};     // target -> {verdict, note} not yet saved
let BASE = FEED0.global || 0;  // Juan's last review; frozen once the page has loaded
let newOnly = false, NEWN = 0, seenTimer = null;
let SEEN = {};      // path -> 1 once shown in the hero >1 s; styling only, never clears NEW
try { SEEN = JSON.parse(localStorage.getItem(SEEN_KEY) || '{}') || {}; } catch (_) {}

const $ = id => document.getElementById(id);
const el = (t, c, x) => { const n = document.createElement(t); if (c) n.className = c;
  if (x != null) n.textContent = x; return n; };
const cur = () => view.length ? view[gi].shots[si] : null;

const ALL_PATHS = [];
for (const g of GROUPS) for (const s of g.shots) ALL_PATHS.push(s.p);

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

function verdicts() {   // snapshot + disk/browser records, newest per target
  const by = {};
  for (const r of FEED0.records) by[r.p] = { p: r.p, s: r.s, w: r.w };
  for (const t in FB) {
    const r = FB[t] || {}, w = Date.parse(r.when) / 1000;
    if (isFinite(w) && (!by[t] || w >= by[t].w)) by[t] = { p: t, s: r.subject, w };
  }
  return Object.values(by);
}

function fmtTime(ts) {
  if (!ts) return '';
  const d = new Date(ts * 1000), z = n => String(n).padStart(2, '0');
  return d.getFullYear() + '-' + z(d.getMonth() + 1) + '-' + z(d.getDate()) + ' '
       + z(d.getHours()) + ':' + z(d.getMinutes());
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
  $('live').textContent = online ? 'saving to disk' : 'offline — clipboard only';
  $('live').className = 'live' + (online ? ' on' : '');
}

function markdownFor(rec) {
  return ['### ' + rec.verdict.toUpperCase() + ' — ' + rec.target,
          rec.refs.length ? 'see also: ' + rec.refs.join(', ') : '',
          '', rec.note].filter(Boolean).join('\\n');
}

async function save() {
  const s = cur(); if (!s) return;
  const d = draft[s.p] || {};
  const verdict = d.verdict || (FB[s.p] || {}).verdict;
  if (!verdict) { $('savedmsg').textContent = 'pick a verdict first'; return; }
  const note = $('note').value;
  const refs = (note.match(/@[^\\s,;]+/g) || []).map(x => x.slice(1));
  const rec = { target: s.p, subject: view[gi].s, verdict, note, refs };
  if (online) {
    try {
      const r = await fetch('/feedback', { method: 'POST',
        headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(rec) });
      const out = await r.json();
      if (!r.ok) throw new Error(out.error || r.status);
      FB[s.p] = out.entry;
      delete draft[s.p];
      $('savedmsg').textContent = 'saved · ' + (out.entry.piece || 'no source on disk');
    } catch (e) { $('savedmsg').textContent = 'save failed: ' + e.message; }
  } else {
    FB[s.p] = Object.assign({}, rec, { when: new Date().toISOString() });
    try { localStorage.setItem(KEY, JSON.stringify(FB)); } catch (_) {}
    try { await navigator.clipboard.writeText(markdownFor(rec));
          $('savedmsg').textContent = 'no server — copied to clipboard'; }
    catch (_) { $('savedmsg').textContent = 'stored in this browser only'; }
  }
  rebuild(true);
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
function buildView() {
  const q = $('q').value.toLowerCase(), ser = $('ser').value, only = $('plot').checked;
  let v = GROUPS.filter(g => {
    if (ser && g.series !== ser) return false;
    if (q && !g.s.toLowerCase().includes(q)) return false;
    if (only && !g.shots.some(s => s.g)) return false;
    if (newOnly && !g.fresh) return false;
    return true;
  });
  if (newOnly) v = v.map(g => Object.assign({}, g, { shots: g.shots.filter(s => s.fresh) }));
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
  NEWN = markNew(GROUPS, verdicts(), BASE);
  view = buildView();
  const b = $('newbtn');
  b.textContent = 'New · ' + NEWN;
  b.classList.toggle('none', !NEWN);
  b.setAttribute('aria-pressed', newOnly);
  if (!keep) { firstNew(); draw(); return; }
  gi = view.findIndex(g => g.s === gs);
  if (gi < 0) { gi = Math.min(ogi, Math.max(0, view.length - 1)); si = 0; }
  else { si = view[gi].shots.indexOf(s); if (si < 0) si = Math.min(osi, view[gi].shots.length - 1); }
  draw();
}

function applyFilter() { rebuild(false); }

/* n: the next NEW render after the current one, across subjects, wrapping. */
function nextNew() {
  if (!view.length) return;
  const total = view.reduce((a, g) => a + g.shots.length, 0);
  let g = gi, k = si;
  for (let i = 0; i < total; i++) {
    if (++k >= view[g].shots.length) { g = (g + 1) % view.length; k = 0; }
    if (view[g].shots[k].fresh) { gi = g; si = k; draw(); return; }
  }
  $('pos').textContent = 'no new renders';
}

function setFocus(f) { focus = f; draw(); }

function draw() {
  $('hero').classList.toggle('focused', focus === 'hero');
  $('strip').classList.toggle('focused', focus === 'strip');
  $('keys').textContent = (focus === 'hero'
    ? '\u2190\u2192 drawing  \u00b7  \u2193 to versions'
    : '\u2190\u2192 version  \u00b7  \u2191 to drawings') + '  \u00b7  n next new';

  if (!view.length) {
    $('title').textContent = newOnly ? 'nothing new — every render has a verdict after it'
                                     : 'nothing matches';
    $('big').removeAttribute('src');
    $('rail').textContent = ''; $('pos').textContent = ''; $('sub').textContent = '';
    $('stats').textContent = ''; $('round').textContent = '';
    $('striphead').textContent = ''; watchSeen(null); return;
  }
  const g = view[gi], s = g.shots[si];
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
  $('pos').textContent = (gi + 1) + ' / ' + view.length;

  const saved = FB[s.p], d = draft[s.p] || {};
  const verdict = d.verdict || (saved || {}).verdict || null;
  const vs = $('verdicts'); vs.textContent = '';
  for (const k of ['promote', 'rework', 'cut']) {
    const b = el('button', null, k); b.dataset.v = k;
    b.setAttribute('aria-pressed', verdict === k);
    b.onclick = () => { draft[s.p] = Object.assign({}, draft[s.p],
      { verdict: verdict === k ? null : k }); draw(); };
    vs.append(b);
  }
  $('note').value = d.note != null ? d.note : ((saved || {}).note || '');
  $('savedmsg').textContent = saved
    ? 'on record ' + (saved.when || '').slice(0, 16).replace('T', ' ') : '';

  $('striphead').textContent = newOnly
    ? g.shots.length + ' new version' + (g.shots.length > 1 ? 's' : '') + ' — no verdict since'
    : (g.shots.length > 1
       ? g.shots.length + ' versions — final first, then every trial'
       : 'only one version of this drawing') + (g.fresh ? '  ·  ' + g.fresh + ' new' : '');
  const rail = $('rail'); rail.textContent = '';
  g.shots.forEach((sh, k) => {
    const t = el('div', 'thumb' + (k === si ? ' on' : '') + (sh.fresh ? ' fresh' : ''));
    t.dataset.p = sh.p;
    const im = el('img'); im.src = sh.p; im.alt = sh.n; im.loading = 'lazy';
    t.append(im, el('div', 'lb', sh.t));
    if (sh.fresh) t.append(el('div', 'nw' + (SEEN[sh.p] ? ' seen' : ''), 'NEW'));
    const v = (FB[sh.p] || {}).verdict;
    if (v) t.append(el('div', 'dot ' + v));
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
$('save').onclick = save;
$('note').addEventListener('input', () => {
  const s = cur(); if (s) draft[s.p] = Object.assign({}, draft[s.p], { note: $('note').value });
  acUpdate();
});
$('note').addEventListener('blur', acHide);
$('note').addEventListener('keydown', e => {
  if (!acItems.length) { if (e.key === 'Escape') $('note').blur(); return; }
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    e.preventDefault(); acSel = (acSel + (e.key === 'ArrowDown' ? 1 : -1) + acItems.length) % acItems.length;
    [...$('ac').children].forEach((c, i) => c.className = i === acSel ? 'sel' : '');
  } else if (e.key === 'Enter' || e.key === 'Tab') { e.preventDefault(); acPick(acSel); }
  else if (e.key === 'Escape') { acHide(); }
});

document.addEventListener('keydown', e => {
  const t = e.target.tagName;
  if (t === 'INPUT' || t === 'SELECT' || t === 'TEXTAREA') return;
  const map = {
    ArrowUp:    () => setFocus('hero'),
    ArrowDown:  () => setFocus('strip'),
    ArrowLeft:  () => focus === 'hero' ? step(-1) : shot(-1),
    ArrowRight: () => focus === 'hero' ? step(1)  : shot(1),
    n:          nextNew,
  };
  if (e.key === 'n' && (e.metaKey || e.ctrlKey || e.altKey)) return;  // leave cmd-n alone
  const fn = map[e.key];
  if (!fn) return;
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
['q', 'ser', 'plot'].forEach(id =>
  $(id).addEventListener(id === 'q' ? 'input' : 'change', applyFilter));
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
  $('plstop').disabled = !busy;
  $('pllog').textContent = (PL.log || []).slice(-8).join('\\n');

  // Poll only while something is moving.
  if (busy && !plTimer) plTimer = setInterval(plState, 1200);
  if (!busy && plTimer) { clearInterval(plTimer); plTimer = null; }
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

loadFeedback().then(() => {
  // Freeze the review cutoff now: a verdict recorded on one drawing in this
  // session must not make every never-judged drawing stop being NEW.
  for (const v of verdicts()) BASE = Math.max(BASE, v.w);
  rebuild(false);   // lands on the first NEW render when there is one
  plState();
});
</script></body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.WARNING if args.quiet else logging.INFO,
                        format="%(message)s")

    if not GALLERY.is_dir():
        logger.error("no gallery/ yet — run scripts/gallery_import.py first")
        return 1

    manifests = []
    paired = 0
    for subject in subject_dirs():
        paired += colocate_pairs(subject)
        m = build_manifest(subject)
        (subject / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
        manifests.append(m)
        logger.info("%4d  %s", m["count"], m["subject"])

    write_index(manifests)
    write_print_queue(manifests)
    write_viewer(manifests)
    if paired:
        logger.info("co-located %d gcode file(s) with their render", paired)
    logger.info("--- %d subjects, %d files -> gallery/INDEX.md ---",
                len(manifests), sum(m["count"] for m in manifests))
    return 0


if __name__ == "__main__":
    sys.exit(main())
