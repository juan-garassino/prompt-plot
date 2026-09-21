"""Act on recorded PROMOTE / CUT verdicts by moving plates between tiers.

The viewer's buttons only ever RECORD a judgement — nothing moves when you
click. This is the separate, deliberate step that carries them out, so a
misclick in the browser cannot reorganise the archive.

CUT moves to a `cut/` tier. It never deletes: a cut plate stays on disk and can
be walked back. Every move is appended to MOVES.tsv, matching
`gallery_import.py` and `studio_sync.py`, so the whole thing is reversible.

Idempotent — a plate already in its target tier is skipped, so re-running is
safe and the append-only feedback log needs no "applied" bookkeeping.
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gallery_feedback as fb  # noqa: E402

logger = logging.getLogger(__name__)
REPO = Path(__file__).resolve().parent.parent
GALLERY = REPO / "gallery"
MOVES = GALLERY / "MOVES.tsv"


def target_tier(subject: str, verdict: str) -> str | None:
    if verdict == "cut":
        return "cut"
    if verdict == "promote":
        # studio families keep their winner in current/; the older series use promoted/
        return "current" if (GALLERY / subject / "current").exists() \
            or subject.startswith("studio/") else "promoted"
    return None  # rework changes nothing on disk — it is work to do, not a place


def plan() -> list[tuple[Path, Path, str]]:
    moves: list[tuple[Path, Path, str]] = []
    for rec in fb.latest_by_target().values():
        tier = target_tier(rec["subject"], rec["verdict"])
        if not tier:
            continue
        src = GALLERY / rec["target"]
        if not src.exists():
            logger.warning("missing, skipped: %s", rec["target"])
            continue
        if f"/{tier}/" in f"/{rec['target']}":
            continue  # already there
        dst_dir = GALLERY / rec["subject"] / tier
        for f in (src, src.with_suffix(".gcode")):   # a plate travels with its gcode
            if f.exists():
                moves.append((f, dst_dir / f.name, rec["verdict"]))
    return moves


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print the plan, move nothing")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    moves = plan()
    if not moves:
        logger.info("nothing to apply — no promote/cut verdicts pending")
        return 0

    for src, dst, verdict in moves:
        logger.info("%-8s %s  ->  %s", verdict.upper(),
                    src.relative_to(GALLERY), dst.relative_to(GALLERY))
    logger.info("--- %d file(s) ---", len(moves))

    if args.dry_run:
        logger.info("dry run — nothing moved. Re-run without --dry-run to apply.")
        return 0

    MOVES.parent.mkdir(parents=True, exist_ok=True)
    with MOVES.open("a") as log:
        for src, dst, _v in moves:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                dst.unlink()
            shutil.move(str(src), str(dst))
            log.write(f"{src}\t{dst}\n")
    logger.info("moved %d file(s); reversal log at %s", len(moves), MOVES)
    logger.info("now re-run: python scripts/gallery_index.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
