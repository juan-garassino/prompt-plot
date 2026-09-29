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
import filecmp
import logging
import re
import shutil
import time
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


GALLERY = REPO / "gallery"
STUDIO = REPO / "studio"
TIERS = ("current", "trials")


def plate_targets() -> dict[str, Path]:
    """Filename key (underscored studio slug or gallery family) -> gallery subject dir.

    A studio round renders as ``pp_<slug>_<thesis>_v<N>``. Without this table the
    thesis was read as part of the family, so every thesis became its own gallery
    drawing, away from its originals, and feedback on it resolved to a studio
    folder no agent reads. Package plates (studio/neural-networks-cnn) file into
    the gallery subject that already holds their originals (neural-networks/cnn).
    """
    targets: dict[str, Path] = {}
    if DEST.is_dir():
        for d in DEST.iterdir():
            if d.is_dir():
                targets[d.name] = d
    by_slug = {}
    for series in ("neural-networks", "physics"):
        root = GALLERY / series
        if root.is_dir():
            for m in root.rglob("manifest.json"):
                subject = m.parent.relative_to(GALLERY)
                by_slug[str(subject).replace("/", "-")] = m.parent
    if STUDIO.is_dir():
        for d in STUDIO.iterdir():
            if not d.is_dir() or not ((d / "rounds").is_dir() or (d / "DESCRIPTION.md").exists()):
                continue
            key = d.name.replace("-", "_")
            targets.setdefault(key, by_slug.get(d.name, DEST / key))
            if d.name in by_slug:
                targets[key] = by_slug[d.name]
    return targets


def resolve(stem: str, targets: dict[str, Path]) -> tuple[str, Path, str]:
    """-> (plate key, gallery subject dir, thesis/variant) for one render stem."""
    base = family_of(stem)
    for key in sorted(targets, key=len, reverse=True):
        if base == key or base.startswith(key + "_"):
            return key, targets[key], base[len(key) + 1:]
    return base, DEST / base, ""


def plan(only: set[str] | None = None, min_age_min: float = 0.0) -> tuple[dict, list]:
    targets = plate_targets()
    groups: dict[tuple[str, Path, str], list[Path]] = {}
    # a png and its gcode move together or not at all: judge freshness on the newer of the pair
    newest: dict[str, float] = {}
    for q in DOWNLOADS.glob("pp_*"):
        if q.suffix in (".png", ".gcode"):
            newest[q.stem] = max(newest.get(q.stem, 0.0), q.stat().st_mtime)
    cutoff = time.time() - min_age_min * 60
    for pat in ("pp_*.png", "pp_*.gcode"):
        for p in DOWNLOADS.glob(pat):
            if min_age_min and newest.get(p.stem, 0.0) > cutoff:
                continue   # still being iterated or critiqued: leave it for the next sync
            key, dest, variant = resolve(p.stem, targets)
            if only and key not in only:
                continue
            groups.setdefault((key, dest, variant), []).append(p)

    moves: list[tuple[Path, Path]] = []
    summary: dict[str, dict] = {}
    for (key, dest, variant), paths in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][2])):
        pngs = [p for p in paths if p.suffix == ".png" and not _DIAGNOSTIC.search(p.stem)]
        best = max(pngs, key=lambda p: rank_of(p.stem, p)) if pngs else None
        # the current render's gcode travels with it; latest is kept PER thesis
        keep = {best.stem} if best else set()
        for p in sorted(paths):
            moves.append((p, dest / ("current" if p.stem in keep else "trials") / p.name))
        label = f"{key}{' · ' + variant if variant else ''}"
        summary[label] = {"files": len(paths), "dest": str(dest.relative_to(GALLERY)),
                          "latest": best.name if best else "—"}
    return summary, moves


def rewrite_refs(placed: dict[str, Path] | None = None) -> int:
    """Point studio notes at a render's archive path instead of ~/Downloads.

    Ledgers, handoffs, NOTES and critiques cite renders by their staging path; after a
    move those paths would dangle and a critic mid-review would lose its render. Any
    Downloads reference whose file is archived anywhere in gallery/ is rewritten (files
    placed by this run win; otherwise current/ beats trials/).
    """
    index: dict[str, Path] = {}
    for q in sorted(GALLERY.rglob("pp_*"), key=lambda q: "current" not in q.parts):
        index.setdefault(q.name, q)
    index.update(placed or {})
    pat = re.compile(r"(?:~|/Users/[^/\s`]+|\$HOME)/Downloads/(pp_[^\s`'\")\],;*]+?)(?=[.]?(?:[\s`'\")\],;*]|$))")
    changed = 0
    for md in (REPO / "studio").rglob("*.md"):
        text = md.read_text()
        new = pat.sub(lambda m: str(index[m[1]].relative_to(REPO)) if m[1] in index else m[0], text)
        if new != text:
            md.write_text(new)
            changed += 1
    return changed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print the plan, move nothing")
    ap.add_argument("--copy", action="store_true",
                    help="copy instead of move — safe while agents still render into "
                    "~/Downloads (they pick their next _vN from what is there)")
    ap.add_argument("--only", help="comma-separated plate keys (e.g. ising,gan) to limit the sync")
    ap.add_argument("--fix-refs", action="store_true",
                    help="only rewrite ~/Downloads references in studio notes to archived gallery paths")
    ap.add_argument("--min-age", type=float, default=0.0, metavar="MIN",
                    help="skip renders newer than MIN minutes (the live working set of running "
                    "agents) so a sync can run while they work")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if args.fix_refs:
        logger.info("rewrote Downloads references in %d studio notes", rewrite_refs())
        return 0

    only = {k.strip().replace("-", "_") for k in args.only.split(",")} if args.only else None
    summary, moves = plan(only, args.min_age)
    for label, s in summary.items():
        logger.info("%-44s %3d files -> %-32s latest: %s", label, s["files"], s["dest"], s["latest"])
    logger.info("--- %d plates/theses, %d files ---", len(summary), len(moves))

    if args.dry_run:
        return 0

    log = DEST / "MOVES.tsv"
    DEST.mkdir(parents=True, exist_ok=True)
    op = shutil.copy2 if args.copy else shutil.move
    placed: dict[str, Path] = {}
    kept_both = deduped = 0
    with log.open("a") as fh:
        for src, dst in moves:
            if not src.exists():
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            # a file that was current on an earlier (copy) run and is a trial now
            # must not stay behind in the other tier
            for tier in TIERS:
                twin = dst.parent.parent / tier / dst.name
                if twin != dst and twin.exists():
                    if filecmp.cmp(twin, src, shallow=False):
                        twin.unlink()
            if dst.exists():
                if filecmp.cmp(dst, src, shallow=False):
                    # already archived byte-identical: the staging copy is redundant
                    if not args.copy:
                        src.unlink()
                        deduped += 1
                    placed[src.name] = dst
                    fh.write(f"{src}\t{dst}\tdedup\n")
                    continue
                # never overwrite a different render: keep both
                k = 2
                while (alt := dst.with_name(f"{dst.stem}__alt{k}{dst.suffix}")).exists():
                    k += 1
                dst = alt
                kept_both += 1
            op(str(src), str(dst))
            placed[src.name] = dst
            fh.write(f"{src}\t{dst}\t{'copy' if args.copy else 'move'}\n")
    logger.info("%s %d files (%d already archived, %d name clashes kept as __alt); log at %s",
                "copied" if args.copy else "moved", len(moves), deduped, kept_both, log)
    if not args.copy and placed:
        logger.info("rewrote Downloads references in %d studio notes", rewrite_refs(placed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
