"""Act on recorded render verdicts by moving plates between tiers.

The viewer's buttons only ever RECORD a judgement — nothing moves when you
click. This is the separate, deliberate step that carries them out, so a
misclick in the browser cannot reorganise the archive.

    PROMOTE  -> current/ (studio families) or promoted/ (the older series)
    ARCHIVE  -> archive/   not now: hidden by default, recoverable
    CUT      -> cut/       never deleted: a cut plate stays on disk
    KEEP / REWORK on an archived or cut plate -> RESTORE it to the tier it came
             from (the most recent MOVES.tsv entry), else trials/ (studio) or
             variants/ (older series). Otherwise KEEP / REWORK move nothing.

Direction verdicts never move files. A png and its gcode travel together.
Every move is appended to MOVES.tsv, matching `gallery_import.py` and
`studio_sync.py`, so the whole thing is reversible; after moving, every
`gallery/<old path>` in studio/**/*.md is rewritten to the new path.

Idempotent — a plate already in its target tier is skipped (it is found by
basename when the recorded target has moved), so re-running is a no-op and the
append-only feedback log needs no "applied" bookkeeping.
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gallery_feedback as fb  # noqa: E402
import studio_sync  # noqa: E402

logger = logging.getLogger(__name__)
REPO = Path(__file__).resolve().parent.parent
GALLERY = REPO / "gallery"
MOVES = GALLERY / "MOVES.tsv"
PARKED = ("archive", "cut")


def _tier_of(path: Path, subject: str) -> str | None:
    """The tier folder right under the subject in a (possibly foreign-rooted) path."""
    parts = Path(path).parts
    sub = Path(subject).parts
    for i in range(len(parts) - len(sub)):
        if parts[i:i + len(sub)] == sub and i + len(sub) < len(parts) - 1:
            return parts[i + len(sub)]
    return None


def restore_tier(subject: str, name: str) -> str | None:
    """The most recent non-parked tier MOVES.tsv shows this file leaving."""
    if not MOVES.exists():
        return None
    found = None
    stem = Path(name).stem
    for line in MOVES.read_text().splitlines():
        cols = line.split("\t")
        if len(cols) < 2:
            continue
        src, dst = Path(cols[0]), Path(cols[1])
        if dst.stem != stem or _tier_of(dst, subject) is None:
            continue
        tier = _tier_of(src, subject)
        if tier and tier not in PARKED:
            found = tier
    return found


def target_tier(subject: str, verdict: str, cur_tier: str | None = None,
                name: str = "") -> str | None:
    if verdict == "archive":
        return "archive"
    if verdict == "cut":
        return "cut"
    if verdict == "promote":
        # studio families keep their winner in current/; the older series use promoted/
        return "current" if (GALLERY / subject / "current").exists() \
            or subject.startswith("studio/") else "promoted"
    if verdict in ("keep", "rework") and cur_tier in PARKED:
        return (restore_tier(subject, name) if name else None) \
            or ("trials" if subject.startswith("studio/") else "variants")
    return None  # keep / rework change nothing on disk — they are a flavour or work to do


def locate(rec: dict) -> Path | None:
    """The file a render verdict is about: its recorded path, else its basename under the subject."""
    src = GALLERY / rec["target"]
    if src.exists():
        return src
    name = rec["target"].rsplit("/", 1)[-1]
    root = GALLERY / rec["subject"]
    hits = sorted(root.rglob(name)) if root.is_dir() else []
    if len(hits) == 1:
        return hits[0]
    if hits:
        logger.warning("%d files named %s under %s, skipped: %s", len(hits), name,
                       rec["subject"], ", ".join(str(h.relative_to(GALLERY)) for h in hits))
    else:
        logger.warning("missing, skipped: %s", rec["target"])
    return None


def plan() -> list[tuple[Path, Path, str]]:
    moves: list[tuple[Path, Path, str]] = []
    for rec in fb.latest_by_render().values():
        if rec["verdict"] not in ("promote", "archive", "cut", "keep", "rework"):
            continue
        src = locate(rec)
        if src is None:
            continue
        cur = _tier_of(src.relative_to(GALLERY), rec["subject"])
        tier = target_tier(rec["subject"], rec["verdict"], cur, src.name)
        if not tier or tier == cur:
            continue  # nothing to do, or already there
        dst_dir = GALLERY / rec["subject"] / tier
        for f in (src.with_suffix(".png"), src.with_suffix(".gcode")):  # a plate travels with its gcode
            if f.exists():
                moves.append((f, dst_dir / f.name, rec["verdict"]))
    return moves


def apply(moves: list[tuple[Path, Path, str]]) -> dict[str, int]:
    """Move the files, log every move, and repoint studio notes at the new paths."""
    MOVES.parent.mkdir(parents=True, exist_ok=True)
    renamed: dict[str, Path] = {}
    with MOVES.open("a") as log:
        for src, dst, _v in moves:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                dst.unlink()
            old = src.relative_to(GALLERY).as_posix()
            shutil.move(str(src), str(dst))
            log.write(f"{src}\t{dst}\n")
            renamed[old] = dst
    refs = studio_sync.rewrite_refs(extra=renamed) if renamed else 0
    return {"moved": len(renamed), "refs": refs}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print the plan, move nothing")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    moves = plan()
    if not moves:
        logger.info("nothing to apply — no promote/archive/cut/restore pending")
        return 0

    for src, dst, verdict in moves:
        logger.info("%-8s %s  ->  %s", verdict.upper(),
                    src.relative_to(GALLERY), dst.relative_to(GALLERY))
    logger.info("--- %d file(s) ---", len(moves))

    if args.dry_run:
        logger.info("dry run — nothing moved. Re-run without --dry-run to apply.")
        return 0

    st = apply(moves)
    logger.info("moved %d file(s); reversal log at %s; repointed %d studio note(s)",
                st["moved"], MOVES, st["refs"])
    logger.info("now re-run: python scripts/gallery_index.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
