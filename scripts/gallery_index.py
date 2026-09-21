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
            "mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            .date().isoformat(),
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
                }
            )
        if not shots:
            continue
        shots.sort(key=lambda x: (TIER_RANK.get(x["t"], 9), x["n"]))
        groups.append({"s": subject, "series": subject.split("/")[0], "shots": shots})
    groups.sort(key=lambda g: g["s"])

    opts = "".join(f"<option>{x}</option>" for x in sorted({g["series"] for g in groups}))
    html = TEMPLATE.replace("__DATA__", json.dumps(groups, separators=(",", ":")))
    html = html.replace("__SERIES__", opts)
    (GALLERY / "viewer.html").write_text(html)


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PromptPlot Gallery</title>
<style>
:root{--bg:#e6e7ea;--card:#fafafa;--ink:#15181e;--dim:#69707c;--line:#c9ced6;
--ring:#2f6df6;--keep:#1b7038;--rework:#b26a00;--cut:#9a1b2f;--sheet:#f1eee5}
@media(prefers-color-scheme:dark){:root{--bg:#0e1116;--card:#171b21;--ink:#e5e8ec;
--dim:#828b98;--line:#272d36;--ring:#5c9cff;--keep:#4fbe77;--rework:#e0a33c;--cut:#ff7089}}
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
const KEY = 'ppgallery.v3';
let FB = {};        // target -> saved record (from disk when served)
let online = false; // true once /feedback.json answers
let view = GROUPS, gi = 0, si = 0, focus = 'hero';
let draft = {};     // target -> {verdict, note} not yet saved

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
  draw();
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
function applyFilter() {
  const q = $('q').value.toLowerCase(), ser = $('ser').value, only = $('plot').checked;
  view = GROUPS.filter(g => {
    if (ser && g.series !== ser) return false;
    if (q && !g.s.toLowerCase().includes(q)) return false;
    if (only && !g.shots.some(s => s.g)) return false;
    return true;
  });
  gi = 0; si = 0; draw();
}

function setFocus(f) { focus = f; draw(); }

function draw() {
  $('hero').classList.toggle('focused', focus === 'hero');
  $('strip').classList.toggle('focused', focus === 'strip');
  $('keys').textContent = focus === 'hero'
    ? '\u2190\u2192 drawing  \u00b7  \u2193 to versions'
    : '\u2190\u2192 version  \u00b7  \u2191 to drawings';

  if (!view.length) {
    $('title').textContent = 'nothing matches'; $('big').removeAttribute('src');
    $('rail').textContent = ''; $('pos').textContent = ''; $('sub').textContent = '';
    $('stats').textContent = ''; $('striphead').textContent = ''; return;
  }
  const g = view[gi], s = g.shots[si];
  $('big').src = s.p; $('big').alt = s.n;
  $('title').textContent = g.s;
  const sub = el('span'); sub.append(el('span', 'tier ' + s.t.split('/')[0], s.t), s.n);
  $('sub').textContent = ''; $('sub').append(sub);
  $('stats').textContent = statline(s);
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

  $('striphead').textContent = g.shots.length > 1
    ? g.shots.length + ' versions — final first, then every trial'
    : 'only one version of this drawing';
  const rail = $('rail'); rail.textContent = '';
  g.shots.forEach((sh, k) => {
    const t = el('div', 'thumb' + (k === si ? ' on' : ''));
    const im = el('img'); im.src = sh.p; im.alt = sh.n; im.loading = 'lazy';
    t.append(im, el('div', 'lb', sh.t));
    const v = (FB[sh.p] || {}).verdict;
    if (v) t.append(el('div', 'dot ' + v));
    t.onclick = () => { si = k; focus = 'strip'; draw(); };
    rail.append(t);
  });
  const on = rail.children[si];
  if (on) on.scrollIntoView({ block: 'nearest', inline: 'nearest' });

  if (gcodeOf(s) !== plTarget) plLoadLayers();
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
  };
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
  $('pllog').textContent = (PL.log || []).slice(-8).join('\n');

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
  if (!confirm('INK colour ' + plPick + ' (' + (L.strokes || '?') + ' strokes) onto the sheet?\n\n'
               + plTarget)) return;
  await plPost('/plotter/job',
               { action: 'layer', target: plTarget, color: plPick, confirm: true });
  plState();
};
$('plstop').onclick = () => plPost('/plotter/stop', {});

loadFeedback().then(() => { draw(); plState(); });
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
