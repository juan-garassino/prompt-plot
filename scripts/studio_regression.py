"""Fingerprint every studio piece so a shared-engine change cannot silently ruin one.

The studio pieces live outside the package (``studio/<slug>/rounds/<rN>/piece.py``)
and are not in ``GENERATOR_REGISTRY``, so ``make test`` never touches them — yet
they import ``engine.geometry``, ``engine.kit``, ``engine.policies`` and a handful
of private helpers from ``generators.py``. An edit to any of those can change or
break an approved plate with nothing going red.

    python scripts/studio_regression.py --write    # record the baseline
    python scripts/studio_regression.py            # compare against it

Baseline: ``studio/REGRESSION.json``. A piece is fingerprinted by its command
count, draw/travel length, pens used and a hash of every coordinate, so any
change in geometry shows up even when the totals happen to match.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import inspect
import json
import math
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

BASELINE = REPO / "studio" / "REGRESSION.json"
DEFAULTS = {"seed": 7, "paper": "a4", "orientation": "portrait", "colors": 4}


def discover_entry(mod) -> Optional[str]:
    """A piece's entry point is the public ``(rng, bounds, colors=...)`` function."""
    declared = getattr(mod, "ENTRY_POINT", None)
    if declared and hasattr(mod, declared):
        return declared
    doc = (mod.__doc__ or "")
    for line in doc.splitlines():
        if "Entry point:" in line:
            cand = line.split("Entry point:", 1)[1].strip().strip("`.,")
            if hasattr(mod, cand):
                return cand
    cands: List[str] = []
    for name, obj in vars(mod).items():
        if name.startswith("_") or not inspect.isfunction(obj):
            continue
        if getattr(obj, "__module__", None) != mod.__name__:
            continue
        params = list(inspect.signature(obj).parameters)
        if len(params) >= 2 and params[0] == "rng" and params[1] == "bounds":
            cands.append(name)
    if len(cands) == 1:
        return cands[0]
    # Several match: prefer the one named after the folder, else the last defined.
    slug = Path(mod.__file__).parent.parent.parent.name.replace("-", "_")
    for c in cands:
        if c == slug:
            return c
    return cands[-1] if cands else None


def load_piece(path: Path):
    name = "ppreg_" + hashlib.md5(str(path).encode()).hexdigest()[:10]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.pop(0)
    return mod


def fingerprint(cmds) -> Dict[str, Any]:
    draw = travel = 0.0
    x = y = 0.0
    pens = set()
    h = hashlib.sha256()
    for c in cmds:
        cx = c.x if c.x is not None else x
        cy = c.y if c.y is not None else y
        d = math.hypot(cx - x, cy - y)
        if c.command == "G1":
            draw += d
        elif c.command == "G0":
            travel += d
        if c.color is not None:
            pens.add(int(c.color))
        h.update(f"{c.command}|{cx:.4f}|{cy:.4f}|{c.color}".encode())
        x, y = cx, cy
    return {
        "commands": len(cmds),
        "draw_mm": round(draw, 1),
        "travel_mm": round(travel, 1),
        "pens": sorted(pens),
        "hash": h.hexdigest()[:16],
    }


def render(path: Path, params: Dict[str, Any]) -> Dict[str, Any]:
    from promptplot.config import PaperConfig, get_config
    from promptplot.generative.rng import SeededRNG

    config = get_config()
    config.paper = PaperConfig.from_size(params["paper"], params["orientation"])
    config.color.enabled = True
    mod = load_piece(path)
    fn_name = params.get("fn") or discover_entry(mod)
    if fn_name is None:
        return {"status": "no-entry-point"}
    fn = getattr(mod, fn_name)
    cmds = fn(SeededRNG(params["seed"]), config.paper.get_drawable_area(),
              colors=params["colors"])
    out = fingerprint(cmds)
    out["fn"] = fn_name
    out["status"] = "ok"
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help="record the baseline")
    ap.add_argument("--only", help="substring filter on the piece path")
    args = ap.parse_args()

    base: Dict[str, Any] = {}
    if BASELINE.exists():
        base = json.loads(BASELINE.read_text())

    pieces = sorted(REPO.glob("studio/*/rounds/*/piece.py"))
    if args.only:
        pieces = [p for p in pieces if args.only in str(p)]

    results: Dict[str, Any] = {}
    changed: List[Tuple[str, str]] = []
    broke: List[Tuple[str, str]] = []

    for p in pieces:
        key = str(p.relative_to(REPO))
        params = dict(DEFAULTS)
        params.update((base.get(key) or {}).get("params", {}))
        try:
            got = render(p, params)
        except Exception as exc:  # a piece that raises IS the regression
            got = {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
            if not args.write:
                traceback.print_exc(limit=3)
        got["params"] = params
        results[key] = got

        prev = base.get(key)
        if prev and not args.write:
            if got.get("status") != "ok" and prev.get("status") == "ok":
                broke.append((key, got.get("error", got["status"])))
            elif got.get("hash") != prev.get("hash") and prev.get("status") == "ok":
                changed.append((key,
                                f"{prev['commands']}cmd/{prev['draw_mm']}mm -> "
                                f"{got.get('commands')}cmd/{got.get('draw_mm')}mm"))

    ok = sum(1 for r in results.values() if r.get("status") == "ok")
    noentry = sum(1 for r in results.values() if r.get("status") == "no-entry-point")
    err = sum(1 for r in results.values() if r.get("status") == "error")

    if args.write:
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
        print(f"baseline written: {ok} ok, {noentry} no-entry-point, {err} error "
              f"-> {BASELINE.relative_to(REPO)}")
        for k, r in sorted(results.items()):
            if r.get("status") == "error":
                print(f"  ERROR {k}: {r['error']}")
            elif r.get("status") == "no-entry-point":
                print(f"  SKIP  {k}: no (rng, bounds, colors) function")
        return 0

    print(f"{ok} ok, {noentry} no-entry-point, {err} error")
    for k, why in broke:
        print(f"  BROKE   {k}: {why}")
    for k, why in changed:
        print(f"  CHANGED {k}: {why}")
    if broke or changed:
        print("\nA studio piece changed. If the change is intended, re-run with "
              "--write; otherwise revert the engine edit.")
        return 1
    print("no drift")
    return 0


if __name__ == "__main__":
    sys.exit(main())
