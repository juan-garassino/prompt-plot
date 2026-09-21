"""Move versioned render output out of ~/Downloads into gallery/studio/.

Downloads is the staging folder: every render lands there as `pp_<family>_v<N>`.
This files them by family, keeps the LATEST version in `current/` and every
earlier attempt in `trials/`, and is safe to re-run — a new render simply
becomes the new current and the old one drops into trials.

    gallery/studio/<family>/
        current/   the highest version, png + gcode
        trials/    every earlier version, and diagnostics
        manifest.json

Nothing here is committed; gallery/ is gitignored.
"""

from __future__ import annotations

import argparse
import logging
import re
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

DOWNLOADS = Path.home() / "Downloads"
REPO = Path(__file__).resolve().parent.parent
DEST = REPO / "gallery" / "studio"

# Suffixes that mark a variant of the SAME piece rather than a different piece.
# Stripped to find the family; the version they carry is read separately.
_STRIP = re.compile(
    r"(_v\d+|_s\d+|_seed\d+|_r\d+|_a[34]|_landscape|_portrait|_flat|_cmp"
    r"|_overlay|_inspect|_aligned|_slow|_final|_fixed\d*|_clean|_changes"
    r"|_original|_check|_trim\d*|_g0|_sink|_corner|_leo)+$",
    re.I,
)
_DIAGNOSTIC = re.compile(r"_(flat|cmp|overlay|inspect)$", re.I)


def family_of(stem: str) -> str:
    prev = None
    out = stem
    while out != prev:            # suffixes stack: _v7_s3, _r02_a4
        prev = out
        out = _STRIP.sub("", out)
    return out.removeprefix("pp_") or stem


def rank_of(stem: str, path: Path) -> tuple:
    """Sort key for 'latest': version, then round, then mtime."""
    v = re.search(r"_v(\d+)", stem, re.I)
    r = re.search(r"_r(\d+)", stem, re.I)
    return (
        int(v.group(1)) if v else -1,
        int(r.group(1)) if r else -1,
        path.stat().st_mtime,
    )


def plan() -> tuple[dict, list]:
    families: dict[str, list[Path]] = {}
    for pat in ("pp_*.png", "pp_*.gcode"):
        for p in DOWNLOADS.glob(pat):
            families.setdefault(family_of(p.stem), []).append(p)

    moves: list[tuple[Path, Path]] = []
    summary: dict[str, dict] = {}
    for fam, paths in sorted(families.items()):
        pngs = [p for p in paths if p.suffix == ".png" and not _DIAGNOSTIC.search(p.stem)]
        best = max(pngs, key=lambda p: rank_of(p.stem, p)) if pngs else None
        keep = {best.stem} if best else set()
        n_cur = 0
        for p in sorted(paths):
            tier = "current" if p.stem in keep else "trials"
            if tier == "current":
                n_cur += 1
            moves.append((p, DEST / fam / tier / p.name))
        # the current render's gcode travels with it
        if best:
            g = best.with_suffix(".gcode")
            if g.exists():
                moves = [(s, DEST / fam / "current" / s.name) if s == g else (s, d)
                         for s, d in moves]
                n_cur += 1
        summary[fam] = {"files": len(paths), "current": n_cur,
                        "latest": best.name if best else "—"}
    return summary, moves


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print the plan, move nothing")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    summary, moves = plan()
    for fam, s in summary.items():
        logger.info("%-28s %3d files   latest: %s", fam, s["files"], s["latest"])
    logger.info("--- %d families, %d files ---", len(summary), len(moves))

    if args.dry_run:
        return 0

    log = DEST / "MOVES.tsv"
    DEST.mkdir(parents=True, exist_ok=True)
    with log.open("a") as fh:
        for src, dst in moves:
            if not src.exists():
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                dst.unlink()          # re-run: newer copy wins
            shutil.move(str(src), str(dst))
            fh.write(f"{src}\t{dst}\n")
    logger.info("moved %d files; reversal log at %s", len(moves), log)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
