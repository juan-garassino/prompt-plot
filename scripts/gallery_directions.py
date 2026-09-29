"""Which DIRECTION a render belongs to — the approach behind it, not the file.

A plate's studio history is a tree of rounds (``studio/<slug>/LEDGER.md``, the
``## Rounds`` table): each round names a parent and a free-text thesis. A
direction is one root of that tree plus every round that continued it — an
``ITERATE`` / ``MERGE`` / ``polish`` of its parent, or a thesis whose head names
the parent's direction again. A ``WILDCARD`` is always its own root, whatever
its nominal parent. A root whose render has no filename variant
(``pp_<fam>_vN``) is the plate's ``original``.

Keys are stable and short: the ROOT ROUND (``r02``), ``original``, or
``x-<variant>`` for a render no ledger knows about. Labels are the cleaned
thesis head (``COOLING STRIP``, ``THE SUNBURST``).

A leaf module: stdlib only at import time; ``gallery_feedback`` and
``studio_sync`` are imported lazily inside functions, and every path is read
from the module globals at CALL time so tests can repoint them.

    python scripts/gallery_directions.py --audit      # every plate, row -> direction
    python scripts/gallery_directions.py --audit ising gan
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

REPO = Path(__file__).resolve().parent.parent
STUDIO = REPO / "studio"
GALLERY = REPO / "gallery"

_SCRIPTS = str(Path(__file__).resolve().parent)

KEY_RE = re.compile(r"(r\d{2,3}|original|x-[a-z0-9-]{1,40})")
_ROUND_CELL = re.compile(r"r?(\d+)", re.I)
_PARENT = re.compile(r"\br(\d+)\b", re.I)
_FILE = re.compile(r"[\w.\-]+\.(?:png|gcode)", re.I)
_RTOKEN = re.compile(r"(?:^|_)r(\d{2,3})(?=_|$)", re.I)
_VERSION_TOKEN = re.compile(r"^(?:v\d+|r\d+|s\d+|seed\d+)$", re.I)
_PYREF = re.compile(r"\S+?\.py::(\w+)")
_NUM = re.compile(r"\d+(?:\.\d+)?")
_CONTINUE_WORDS = {"iterate", "merge", "polish", "refine"}
_HEAD_CUTS = (":", " (", " [", ",", ". ", ' "', " —")
_HANDOFF_KEYS = ("render", "seeds", "canon", "order", "lineage", "thesis", "direction")

# canon free text -> one of the STYLES.md families (first keyword hit wins)
_CANON_WORDS: tuple[tuple[str, str], ...] = (
    ("science-poster", r"science[ _-]?poster"),
    ("de-stijl", r"de[ _-]?stijl|mondrian|boogie"),
    ("deco", r"\bdeco\b|art[ _-]deco"),
    ("psychedelic", r"psychedel"),
    ("swiss", r"\bswiss\b|international typographic"),
    ("memphis", r"memphis|sottsass"),
    ("constructivism", r"constructiv"),
    ("pop", r"\bpop\b|lichtenstein|ben[ _-]?day"),
    ("radial", r"radial"),
    ("bauhaus", r"bauhaus"),
)


# order free text -> DESIGN_RUBRIC's twelve non-circular orders, or "circular" (the studio's old
# default: rings, spirals, orbits, radial bursts) — so the board can count the circle share
_ORDER_WORDS: tuple[tuple[str, str], ...] = (
    ("ruled field", r"ruled|rulings?\b|line field"),
    ("ridge stack", r"ridge|joy division|unknown pleasures|profiles?"),
    ("orthogonal partition", r"partition|mondrian|orthogonal subdivision|belts?"),
    ("tessellation", r"tessellat|voronoi|truchet|lattice|tiling|stitch"),
    ("branching", r"branch|tree|delta|dendrit"),
    ("folding", r"fold|crease|origami|pleat"),
    ("straight-line moiré", r"moir"),
    ("network", r"network|graph\b|lewitt"),
    ("scatter gradient", r"scatter|schotter|stipple"),
    ("interlacing", r"interlac|weav|braid|knot"),
    ("projective", r"projective|axonometr|vanishing|proun|perspective"),
    ("typographic", r"typograph|glyph"),
    ("circular", r"radial|concentric|spiral|orbit|ring|whorl|vortex|sunburst|nested|circle|helix"),
)


def order_norm(text: str) -> str:
    low = (text or "").lower()
    for name, pat in _ORDER_WORDS:
        if re.search(pat, low):
            return name
    return ""


# ---------------------------------------------------------------------------
# small text helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _clean(text: str) -> str:
    """Strip markdown emphasis and code ticks; `path.py::name` -> name."""
    text = text.replace("*", "").replace("`", "")
    text = _PYREF.sub(r"\1", text)
    return " ".join(text.split())


def _head(clean: str) -> str:
    cut = len(clean)
    for tok in _HEAD_CUTS:
        i = clean.find(tok)
        if 0 < i < cut:
            cut = i
    return clean[:cut].strip(" \t.:;,-—()[]\"'")


def _wildcard_label(clean: str) -> str:
    rest = clean[len("wildcard"):]
    rest = rest.lstrip(" \t.:;,-—()[]\"'“”")
    cut = len(rest)
    for tok in (":", ". ", ", "):   # ", " too: a wildcard label is a name, not a sentence
        i = rest.find(tok)
        if 0 <= i < cut:
            cut = i
    label = rest[:cut].strip(" \t.:;,-—()[]\"'“”")
    if len(label) > 48:
        label = label[:48].rsplit(" ", 1)[0].rstrip(" ,;:-—") + "…"
    return label


def _norm_round(cell: str) -> str:
    m = _ROUND_CELL.fullmatch(cell.replace("*", "").strip())
    return f"r{int(m.group(1)):02d}" if m else cell.strip()


def _first_parent(cell: str) -> str | None:
    m = _PARENT.search(cell.replace("*", ""))
    return f"r{int(m.group(1)):02d}" if m else None


def _split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", body)]


def canon_norm(text: str) -> str:
    low = (text or "").lower()
    for name, pat in _CANON_WORDS:
        if re.search(pat, low):
            return name
    return ""


# ---------------------------------------------------------------------------
# parsers
# ---------------------------------------------------------------------------

def parse_ledger(text: str) -> list[dict[str, Any]]:
    """Rows of the ``## Rounds`` table. Columns are found by the header's first word."""
    rows: list[dict[str, Any]] = []
    head: list[str] | None = None
    in_rounds = False
    for line in text.splitlines():
        if line.startswith("#"):
            in_rounds = line.lstrip("#").strip().lower().startswith("rounds")
            head = None
            continue
        if not in_rounds or not line.strip().startswith("|"):
            continue
        cells = _split_row(line)
        if head is None:
            head = [(c.replace("*", "").strip().lower().split() or [""])[0] for c in cells]
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue

        def col(name: str, head: list[str] = head, cells: list[str] = cells) -> str:
            for i, h in enumerate(head):
                if h == name and i < len(cells):
                    return cells[i]
            return ""

        rnd = _norm_round(col("round"))
        if not re.fullmatch(r"r\d+", rnd):
            continue
        render = _FILE.search(col("render").replace("`", ""))
        rows.append({
            "round": rnd,
            "parent": _first_parent(col("parent")),
            "thesis": col("thesis"),
            "canon": col("canon"),
            "render": render.group(0).rsplit("/", 1)[-1] if render else "",
            "art": col("art"),
            "sci": col("sci"),
            "verdict": col("verdict"),
            "note": col("note"),
        })
    return rows


def parse_handoff(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for key in _HANDOFF_KEYS:
        m = re.search(rf"^\s*[-*]?\s*\**({key})\**\s*:\**\s*(.+)$", text, re.M | re.I)
        out[key] = m.group(2).strip().strip("*").strip() if m else ""
    return out


def _files_in(text: str) -> list[str]:
    return [f.rsplit("/", 1)[-1] for f in _FILE.findall(text.replace("`", ""))]


# ---------------------------------------------------------------------------
# per-plate context (cached on the files' mtimes)
# ---------------------------------------------------------------------------

_CACHE: dict[tuple[str, str], tuple[tuple, dict[str, Any]]] = {}


def _slug(subject: str) -> str:
    if _SCRIPTS not in sys.path:
        sys.path.insert(0, _SCRIPTS)
    import gallery_feedback as fb  # lazy: keeps this module a leaf

    return fb.slug_for(subject)


def _signature(d: Path) -> tuple:
    files = [d / "LEDGER.md", *sorted((d / "rounds").glob("r*/HANDOFF.md"))]
    sig = []
    for f in files:
        try:
            sig.append((str(f), f.stat().st_mtime_ns))
        except OSError:
            continue
    return tuple(sig)


def _context(slug: str) -> dict[str, Any]:
    d = STUDIO / slug
    key = (str(STUDIO), slug)
    sig = _signature(d)
    hit = _CACHE.get(key)
    if hit and hit[0] == sig:
        return hit[1]
    try:
        rows = parse_ledger((d / "LEDGER.md").read_text())
    except OSError:
        rows = []
    handoffs: dict[str, dict[str, str]] = {}
    for h in sorted((d / "rounds").glob("r*/HANDOFF.md")):
        rnd = _norm_round(h.parent.name)
        try:
            handoffs[rnd] = parse_handoff(h.read_text())
        except OSError:
            continue
    ctx = {"slug": slug, "rows": rows, "handoffs": handoffs}
    ctx["dirs"], ctx["round_key"] = _classify(slug, rows, handoffs)
    _CACHE[key] = (sig, ctx)
    return ctx


def _prefixes(slug: str, subject: str = "") -> list[str]:
    """Filename prefixes a plate's renders use: slug, gallery family, aliases."""
    if _SCRIPTS not in sys.path:
        sys.path.insert(0, _SCRIPTS)
    import gallery_feedback as fb  # lazy

    cands = {slug.replace("-", "_"), slug}
    cands |= {fam for fam, s in getattr(fb, "_ALIAS", {}).items() if s == slug}
    if subject:
        if subject.startswith("studio/"):
            cands.add(subject.split("/", 1)[1])
        else:
            cands.add(subject.replace("/", "_").replace("-", "_"))
            cands.add(subject.rsplit("/", 1)[-1].replace("-", "_"))
    return sorted((c.lower() for c in cands if c), key=len, reverse=True)


def variant_of(stem: str, prefixes: list[str]) -> str:
    """The thesis/variant part of a render stem, cut at its first version token.

    Uses ``studio_sync.resolve`` restricted to this plate's own filename prefixes
    (the gallery family and the underscored slug), so a stem cannot resolve into
    another plate; a stem with none of the prefixes keeps its whole family as
    the variant.
    """
    if _SCRIPTS not in sys.path:
        sys.path.insert(0, _SCRIPTS)
    from studio_sync import family_of, resolve  # lazy, stdlib-only

    targets = {p: Path(p) for p in prefixes}
    key, _dest, rest = resolve(stem, targets)
    if key not in targets:
        low = stem.lower()
        rest = None
        for p in prefixes:       # resolve is case-sensitive; retry folded
            if low.startswith("pp_" + p + "_"):
                rest = family_of(stem)[len(p) + 1:]
                break
        if rest is None:
            rest = family_of(stem)
    toks = [t for t in rest.split("_") if t]
    while toks and re.fullmatch(r"r\d+", toks[0], re.I):   # a leading round tag is not a variant
        toks = toks[1:]
    out = []
    for t in toks:
        if _VERSION_TOKEN.match(t):
            break
        out.append(t)
    return "_".join(out)


def _vnorm(v: str) -> str:
    return v.lower().replace("_", "-")


def _classify(slug: str, rows: list[dict], handoffs: dict[str, dict[str, str]]
              ) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    by_round = {r["round"]: r for r in rows}
    prefixes = _prefixes(slug)
    info: dict[str, dict[str, Any]] = {}
    for r in rows:
        clean = _clean(r["thesis"])
        if clean in ("", "—", "-"):
            clean = ""
        variant = variant_of(Path(r["render"]).stem, prefixes) if r["render"] else ""
        head = _head(clean) if clean else ""
        if not head:
            head = variant.replace("_", " ") if variant else f"(untitled {r['round']})"
        first = (re.split(r"[\s:,.(\[]+", clean.lower(), maxsplit=1) or [""])[0]
        info[r["round"]] = {"clean": clean, "head": head, "first": first,
                            "variant": variant,
                            "wild": clean.lower().startswith("wildcard")}

    root_of: dict[str, str] = {}
    label_of: dict[str, str] = {}   # root round -> label

    def root(rnd: str, seen: frozenset = frozenset()) -> str:
        if rnd in root_of:
            return root_of[rnd]
        i, row = info[rnd], by_round[rnd]
        parent = row["parent"]
        res = rnd
        # a HANDOFF `direction: rNN` line overrides the ledger's reading
        want = handoffs.get(rnd, {}).get("direction", "").strip()
        tok = want.split()[0].strip("`*,;.").lower() if want else ""
        forced = f"r{int(tok[1:]):02d}" if re.fullmatch(r"r\d+", tok) else None
        if forced and forced in by_round and forced != rnd and forced not in seen:
            res = root(forced, seen | {rnd})
        elif i["wild"]:
            label_of[rnd] = _wildcard_label(i["clean"]) or f"wildcard {rnd}"
        elif parent and parent in by_round and parent != rnd and parent not in seen:
            proot = root(parent, seen | {rnd})
            plabel = slugify(label_of.get(proot, ""))
            hslug = slugify(i["head"])
            if (i["first"] in _CONTINUE_WORDS
                    or (hslug and (hslug == plabel or hslug == proot or hslug in plabel))):
                res = proot
            else:
                label_of[rnd] = i["head"]
        else:
            label_of[rnd] = i["head"]
        root_of[rnd] = res
        return res

    for r in rows:
        root(r["round"])

    keys: dict[str, str] = {}
    have_original = False
    for r in rows:                      # table order: the earliest bare root is the original
        rr = r["round"]
        if root_of[rr] != rr:
            continue
        if not have_original and not info[rr]["wild"] and not info[rr]["variant"] and r["render"]:
            keys[rr] = "original"
            have_original = True
        else:
            keys[rr] = rr
    round_key = {rnd: keys[root_of[rnd]] for rnd in root_of if root_of[rnd] in keys}

    dirs: dict[str, dict[str, Any]] = {}
    for rr, key in keys.items():
        rounds = sorted((x for x in root_of if root_of[x] == rr), key=lambda x: int(x[1:]))
        chain = [rr] + [x for x in rounds if x != rr]
        meta = {}
        for field in ("canon", "order", "lineage"):
            val = ""
            for x in chain:
                val = (by_round[x].get(field, "") if field == "canon" else "") \
                    or handoffs.get(x, {}).get(field, "")
                if val:
                    break
            meta[field] = val
        label = label_of.get(rr, info[rr]["head"])
        dirs[key] = {
            "label": label,
            "slug": slugify(label),
            "plate": slug,
            "root": rr,
            "rounds": rounds,
            "parent_of_root": by_round[rr]["parent"],
            "canon": meta["canon"],
            "canon_norm": canon_norm(meta["canon"]),
            "order": meta["order"],
            "order_norm": order_norm(meta["order"]),
            "lineage": meta["lineage"],
            "best": _best([by_round[x] for x in rounds]),
        }
    return dirs, round_key


def _nums(cell: str) -> list[float]:
    return [float(x) for x in _NUM.findall(cell.replace("*", ""))]


def _best(rows: list[dict]) -> dict[str, Any]:
    def score(r: dict) -> tuple:
        art = _nums(r.get("art", ""))
        sci = _nums(r.get("sci", ""))
        passes = len(re.findall(r"\bPASS\b", r.get("verdict", "")))
        a_avg = art[0] if art else -1.0
        a_min = art[1] if len(art) > 1 else a_avg
        s_min = min(sci) if sci else -1.0
        return passes, a_min, s_min, a_avg

    if not rows:
        return {"round": None, "art_avg": None, "art_min": None, "sci": None}
    b = max(rows, key=lambda r: (score(r), int(r["round"][1:])))
    _p, a_min, s_min, a_avg = score(b)
    return {"round": b["round"],
            "art_avg": a_avg if a_avg >= 0 else None,
            "art_min": a_min if a_min >= 0 else None,
            "sci": s_min if s_min >= 0 else None}


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------

def directions(subject: str) -> dict[str, dict[str, Any]]:
    """{key: direction} for a gallery subject's plate. Empty without a ledger."""
    ctx = _context(_slug(subject))
    return {k: dict(v) for k, v in ctx["dirs"].items()}


def directions_for_slug(slug: str) -> dict[str, dict[str, Any]]:
    """``directions`` keyed by studio slug instead of gallery subject."""
    return {k: dict(v) for k, v in _context(slug)["dirs"].items()}


def ledger(slug: str) -> list[dict[str, Any]]:
    """The plate's parsed ``## Rounds`` rows (see ``parse_ledger``)."""
    return [dict(r) for r in _context(slug)["rows"]]


def direction_of_round(slug: str, rnd: str) -> str | None:
    """The direction key a ledger round belongs to."""
    return _context(slug)["round_key"].get(_norm_round(rnd))


def _resolve(subject: str, render_name: str) -> tuple[str | None, str, bool]:
    """-> (key, how, ambiguous). ``how`` names the rule that matched."""
    slug = _slug(subject)
    ctx = _context(slug)
    rows, handoffs, rk = ctx["rows"], ctx["handoffs"], ctx["round_key"]
    name = render_name.rsplit("/", 1)[-1]
    stem = Path(name).stem

    def override(rnd: str | None) -> str | None:
        want = handoffs.get(rnd or "", {}).get("direction", "").strip()
        if not want:
            return None
        tok = want.split()[0].strip("`*,;.").lower()
        if KEY_RE.fullmatch(tok) and (tok in ctx["dirs"] or tok.startswith("x-")):
            return tok
        if re.fullmatch(r"r\d+", tok):
            return rk.get(f"r{int(tok[1:]):02d}")
        return None

    # 1. the ledger's render cell, or a HANDOFF render:/seeds: line
    rnd = None
    for r in rows:
        if r["render"] and Path(r["render"]).stem == stem:
            rnd = r["round"]
            break
    if rnd is None:
        for hr, h in handoffs.items():
            if stem in {Path(f).stem for f in _files_in(h.get("render", "") + " " + h.get("seeds", ""))}:
                rnd = hr
                break
    if rnd is None:  # 2. an rNN token in the stem
        m = _RTOKEN.search(stem)
        if m:
            t = f"r{int(m.group(1)):02d}"
            if t in rk or t in handoffs:
                rnd = t
    if rnd is not None:
        ov = override(rnd)
        if ov:
            return ov, "handoff-direction", False
        if rnd in rk:
            return rk[rnd], "ledger", False

    # 3. filename variant against the ledger renders' variants
    prefixes = _prefixes(slug, subject)
    var = variant_of(stem, prefixes)
    if var:
        hits = [r for r in rows if r["render"]
                and _vnorm(variant_of(Path(r["render"]).stem, prefixes)) == _vnorm(var)
                and r["round"] in rk]
        roots = {rk[r["round"]] for r in hits}
        if len(roots) == 1:
            return roots.pop(), "variant", False
        if len(roots) > 1:
            latest = max(hits, key=lambda r: int(r["round"][1:]))
            return rk[latest["round"]], "variant", True
        # 5. a variant nobody recorded
        xs = slugify(var)[:40].strip("-")
        return (f"x-{xs}" if xs else None), "x", False
    # 4. no variant at all: the pre-studio original
    return "original", "original", False


def direction_of(subject: str, render_name: str) -> str | None:
    """The direction key for one render of ``subject``; None only if nothing resolves."""
    return _resolve(subject, render_name)[0]


# ---------------------------------------------------------------------------
# --audit
# ---------------------------------------------------------------------------

def _subjects_by_slug() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    sroot = GALLERY / "studio"
    if sroot.is_dir():
        for d in sorted(sroot.iterdir()):
            if d.is_dir():
                subj = f"studio/{d.name}"
                out.setdefault(_slug(subj), []).append(subj)
    for series in ("neural-networks", "physics"):
        root = GALLERY / series
        if root.is_dir():
            for m in sorted(root.rglob("manifest.json")):
                subj = str(m.parent.relative_to(GALLERY))
                out.setdefault(subj.replace("/", "-"), []).append(subj)
    return out


def audit(only: list[str] | None = None) -> str:
    lines: list[str] = []
    subjects = _subjects_by_slug()
    for led in sorted(STUDIO.glob("*/LEDGER.md")):
        slug = led.parent.name
        if only and slug not in only:
            continue
        ctx = _context(slug)
        lines.append(f"=== {slug}")
        for r in ctx["rows"]:
            key = ctx["round_key"].get(r["round"], "?")
            d = ctx["dirs"].get(key, {})
            mark = "root" if d.get("root") == r["round"] else "  ← "
            lines.append(f"  {r['round']:4} parent={r['parent'] or '—':4} -> {key:10} {mark} "
                         f"{d.get('label', '')!r}")
        for key, d in ctx["dirs"].items():
            lines.append(f"  [{key}] {d['label']!r} rounds={','.join(d['rounds'])} "
                         f"canon={d['canon_norm'] or '—'} best={d['best']['round']}")
        counts: dict[str, int] = {}
        amb: list[str] = []
        xs: dict[str, int] = {}
        for subj in subjects.get(slug, []):
            for f in sorted((GALLERY / subj).rglob("pp_*.png")):
                key, how, ambiguous = _resolve(subj, f.name)
                counts[how] = counts.get(how, 0) + 1
                if ambiguous:
                    amb.append(f.name)
                if key is None:
                    counts["unresolved"] = counts.get("unresolved", 0) + 1
                elif key.startswith("x-"):
                    xs[key] = xs.get(key, 0) + 1
        lines.append(f"  renders: {counts or '(no gallery subject)'}  "
                     f"ambiguous={len(amb)} unresolved={counts.get('unresolved', 0)}")
        if xs:
            lines.append("  x-directions: " + ", ".join(f"{k}×{n}" for k, n in sorted(xs.items())))
        for a in amb[:5]:
            lines.append(f"    ambiguous: {a}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audit", action="store_true",
                    help="print each plate's ledger rows -> direction and render resolution counts")
    ap.add_argument("slugs", nargs="*", help="limit the audit to these studio slugs")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    if not args.audit:
        ap.print_help()
        return 0
    print(audit(args.slugs or None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
