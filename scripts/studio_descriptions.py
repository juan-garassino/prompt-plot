"""Rebuild studio/DESCRIPTIONS.md — one row per plate from every studio/<slug>/DESCRIPTION.md.

A DESCRIPTION.md is the vision-reviewed spec of a plate's current version (what is on
the sheet, what to keep, what is weak, candidate next theses). This index is what a
studio workflow reads to choose which plates to iterate and with which theses:

    python scripts/studio_descriptions.py            # rewrite the index
    python scripts/studio_descriptions.py --json     # print rows as JSON (workflow args)
    python scripts/studio_descriptions.py --census   # how circular is the collection?

The JSON rows also carry Juan's steering from the gallery viewer (see
``gallery_feedback.steering``): ``directions`` {works, maybe, dead_end},
``avoid_parents`` (rounds never to fork from), ``protected`` (KEEP renders),
each thesis's ``direction`` + ``verdict``, and ``blocked_theses`` — theses whose
direction Juan called a DEAD END, dropped from ``theses``.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STUDIO = REPO / "studio"
OUT = STUDIO / "DESCRIPTIONS.md"

logger = logging.getLogger(__name__)

_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$")
# DESIGN_RUBRIC § CIRCLES MUST BE EARNED: the vocabulary that gives the circle default away
_CIRCULAR = re.compile(
    r"\b(concentric|rings?|spirals?|orbits?|orbital|radial|whorls?|vortex|vortices|circles?|"
    r"discs?|annul\w*|helix|bullseye)\b", re.I)
_ORDER_LINE = re.compile(r"^order:\s*(.+)$", re.M)
_SRC = re.compile(r"(studio/[\w\-/.]+/piece\w*\.py(?:::\w+)?|promptplot/generative/[\w\-/.]+\.py::\w+)")
_THESIS = re.compile(r"^\s*(?:[-*]|\d+\.)?\s*\*\*([^*]+?)\*\*\s*\(([^)]*)\)")


def _section(text: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def _rel(path: Path) -> str:
    for base in (REPO, STUDIO.parent):
        try:
            return str(path.relative_to(base))
        except ValueError:
            continue
    return str(path)


def _scripts() -> None:
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)


def _steering(slug: str) -> dict:
    """Juan's direction/render verdicts for this plate (empty when there are none)."""
    _scripts()
    import gallery_feedback as fb  # lazy: tests repoint its globals

    try:
        return fb.steering(slug)
    except Exception:  # steering is advice; a broken log must not break the index
        logger.exception("steering unreadable for %s", slug)
        return {"directions": {"works": [], "maybe": [], "dead_end": []},
                "avoid_parents": [], "protected": [], "verdicts": {}}


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _judge_theses(slug: str, theses: list[dict], steer: dict) -> tuple[list[dict], list[dict]]:
    """Tag each thesis with its direction + verdict; drop the dead ends.

    A thesis names its direction by a round in its kind (``flavour, r06``), else
    by its name matching a direction's slug or label.
    """
    _scripts()
    import gallery_directions as gd  # lazy

    try:
        dirs = gd.directions_for_slug(slug)
    except Exception:
        logger.exception("directions unreadable for %s", slug)
        dirs = {}
    verdicts = steer.get("verdicts", {})
    keep, blocked = [], []
    for t in theses:
        key = None
        m = re.search(r"\br(\d{1,3})\b", t["kind"], re.I)
        if m:
            key = gd.direction_of_round(slug, f"r{int(m.group(1)):02d}")
        if key is None:
            ns = _slugify(t["name"])
            for k, d in dirs.items():
                ls = _slugify(d.get("label", ""))
                if ns and (ns == d.get("slug") or ns == ls or ns in ls or (ls and ls in ns)):
                    key = k
                    break
        out = {**t, "direction": key, "verdict": verdicts.get(key) if key else None}
        (blocked if out["verdict"] == "dead_end" else keep).append(out)
    return keep, blocked


def parse(path: Path) -> dict:
    text = path.read_text()
    title = re.search(r"^# (.+?)(?: — description)?\s*$", text, re.M)
    table = {}
    for line in text.splitlines():
        m = _ROW.match(line)
        if m and not set(m.group(1)) <= {"-", " "} and m.group(1).strip():
            table.setdefault(m.group(1).strip().lower(), m.group(2).strip())
    theses = []
    for line in _section(text, "Next versions").splitlines():
        m = _THESIS.match(line)
        if m and not m.group(1).lower().startswith("if only"):
            theses.append({"name": m.group(1).strip(), "kind": m.group(2).strip()})
    one_line = " ".join(_section(text, "In one line").split())
    source = table.get("source", "").replace("`", "")
    rounds = sorted(int(d.name[1:]) for d in (path.parent / "rounds").glob("r[0-9]*") if d.name[1:].isdigit())
    path_m = _SRC.search(source)
    parent = None
    if path_m:
        parent = path_m.group(1)
        own = re.match(rf"studio/{re.escape(path.parent.name)}/rounds/(r\d+)/", parent)
        parent = own.group(1) if own else parent
    steer = _steering(path.parent.name)
    theses, blocked = _judge_theses(path.parent.name, theses, steer)
    return {
        "slug": path.parent.name,
        "title": title.group(1).strip() if title else path.parent.name,
        "one_line": one_line,
        "status": table.get("status", ""),
        "source": source,
        "parent": parent,
        "next_round": (rounds[-1] + 1) if rounds else 1,
        "current": table.get("current render", ""),
        "theses": theses,
        "blocked_theses": blocked,
        "directions": {v: [{k: d[k] for k in ("key", "label", "rounds")} for d in ds]
                       for v, ds in steer["directions"].items()},
        "avoid_parents": steer["avoid_parents"],
        "protected": steer["protected"],
        "path": _rel(path),
    }


def rows() -> list[dict]:
    return [parse(p) for p in sorted(STUDIO.glob("*/DESCRIPTION.md"))]


def _short(status: str) -> str:
    return status.replace("*", "").split("·")[0].split("(")[0].strip() or "—"


def render(items: list[dict]) -> str:
    lines = [
        "# Studio descriptions",
        "",
        "Generated by `scripts/studio_descriptions.py` — do not edit by hand; edit the",
        "per-plate `studio/<slug>/DESCRIPTION.md` and re-run.",
        "",
        f"{len(items)} plates. Each DESCRIPTION.md is the starting spec a studio round iterates from.",
        "",
        "| plate | in one line | status | next theses |",
        "|---|---|---|---|",
    ]
    for r in items:
        theses = " · ".join(f"`{t['name']}` ({t['kind']})" for t in r["theses"]) or "—"
        one = r["one_line"].replace("|", "/")
        lines.append(f"| [{r['title']}]({r['slug']}/DESCRIPTION.md) `{r['slug']}` | {one} | {_short(r['status'])} | {theses} |")
    return "\n".join(lines) + "\n"


def census() -> str:
    """Circle share of the plate descriptions and the order lines of every studio round."""
    heavy = []
    for p in sorted(STUDIO.glob("*/DESCRIPTION.md")):
        text = p.read_text()
        sheet = _section(text, "What is on the sheet") + _section(text, "In one line")
        hits = len(_CIRCULAR.findall(sheet))
        if hits >= 3:
            heavy.append((hits, p.parent.name))
    total = len(list(STUDIO.glob("*/DESCRIPTION.md")))
    orders: dict[str, int] = {}
    for h in STUDIO.glob("*/rounds/*/HANDOFF.md"):
        m = _ORDER_LINE.search(h.read_text())
        key = (m.group(1).split("·")[0].strip().lower() if m else "(no order line)")
        orders[key] = orders.get(key, 0) + 1
    lines = [f"descriptions: {len(heavy)}/{total} plates use circular vocabulary 3+ times",
             "most circular: " + ", ".join(f"{n} ({h})" for h, n in sorted(heavy, reverse=True)[:8]),
             "round orders (HANDOFF order: lines):"]
    lines += [f"  {n:3}  {k}" for k, n in sorted(orders.items(), key=lambda kv: -kv[1])]
    return "\n".join(lines)


def main() -> None:
    logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s", level=logging.INFO)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="print the rows as JSON instead of writing the index")
    ap.add_argument("--census", action="store_true", help="report the circle share and round orders")
    args = ap.parse_args()
    if args.census:
        print(census())
        return
    items = rows()
    if args.json:
        print(json.dumps(items, indent=1, ensure_ascii=False))
        return
    OUT.write_text(render(items))
    logger.info("%d plates -> %s", len(items), OUT.relative_to(REPO))


if __name__ == "__main__":
    main()
