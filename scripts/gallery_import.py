"""Move the plot archive out of ~/Downloads into gallery/.

Routing has two axes:

  subject  -- from the filename, via SUBJECT_RULES (first match wins)
  tier     -- from the source folder, recording what Juan had already promoted:
                promoted/                  was at leo/ root or leo/<topic>/
                variants/                  was loose at the ~/Downloads top level
                candidates/                was loose in leo/_staging/
                candidates/prior-approved/ was in leo/_staging/approved/

Nothing from _staging is promoted; the tier only records provenance.
Every move is appended to gallery/MOVES.tsv so the whole import is reversible.
"""

from __future__ import annotations

import argparse
import logging
import re
import shutil
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

DOWNLOADS = Path.home() / "Downloads"
REPO = Path(__file__).resolve().parent.parent
GALLERY = REPO / "gallery"

# (regex on the basename, destination subject folder). First match wins, so the
# specific patterns must precede the general ones -- manifold_MLP is manifold,
# not mlp; attention_matrix is attention-matrix, not attention-topography.
SUBJECT_RULES: list[tuple[str, str]] = [
    # --- neural networks -------------------------------------------------
    (r"manifold", "neural-networks/manifold"),
    (r"decision", "neural-networks/decision-surface"),
    (r"loom|forwardpass|perceptron|settling", "neural-networks/perceptron"),
    (r"conveyor|longnow", "neural-networks/lstm"),
    (r"residual_river", "neural-networks/transformer/residual-stream"),
    (r"pe_carpet", "neural-networks/transformer/positional-encoding"),
    (r"attention_(matrix|chord)|attention_gpt2|attn", "neural-networks/transformer/attention-matrix"),
    (r"weights_block|bauhaus_weights", "neural-networks/transformer/weights"),
    (r"attention|xfmr|relevance", "neural-networks/transformer/attention-topography"),
    (r"lstm|memory", "neural-networks/lstm"),
    (r"cnn|locality", "neural-networks/cnn"),
    (r"mlp", "neural-networks/mlp"),
    (r"watershed|_ws_|^pp_ws_|gradient", "neural-networks/optimization/watershed"),
    # --- physics ---------------------------------------------------------
    (r"gw150914|gravitational", "physics/gravitational-waves"),
    (r"big_bang", "physics/big-bang"),
    (r"warped_frame", "physics/warped-frame"),
    (r"black_hole_bauhaus", "physics/black-hole/bauhaus"),
    (r"^pp_bh_", "physics/black-hole/engine"),
    (r"^eh_|eventhorizon|^blackhole_", "physics/eventhorizon"),
    (r"black_hole", "physics/black-hole/luminet"),
    (r"attractor", "attractors"),
    # --- generators, grouped by family -----------------------------------
    (r"iso_city", "generative/city"),
    (r"truchet|maze|rounded_circuits|sparkle|comic_panels", "generative/tilings"),
    (r"crosshatch_weave|turning_weave|hitomezashi|moire_layers", "generative/weaves"),
    (r"harmonograph|lissajous|superformula|stipple|resonance", "generative/curves"),
    (r"halftone|portrait|scribble|einstein|alexanderplatz|anyphoto|bridge|eye",
     "pictures"),
    (r"field|warp|wave|lens|ripple|vortex|contour|interference|tiled",
     "generative/fields"),
    # --- everything else -------------------------------------------------
    (r"^pp_fx_|glitch", "effects"),
    (r"^pp_plate_", "plates"),
]

REFERENCE_DIR = "references"


def tier_for(rel: Path) -> str:
    """Map the source location to a status tier."""
    parts = rel.parts
    if parts[0] == "leo" and "_staging" in parts:
        return "candidates/prior-approved" if "approved" in parts else "candidates"
    if parts[0] == "leo":
        return "promoted"
    if parts[0] == "eh-plots":
        return "promoted"
    return "variants"  # loose at the Downloads top level


def subject_for(rel: Path) -> str | None:
    if "references_pixel_not_penplotter" in rel.parts:
        return REFERENCE_DIR
    name = rel.name.lower()
    for pattern, dest in SUBJECT_RULES:
        if re.search(pattern, name):
            return dest
    return None


def collect() -> list[Path]:
    """Every archive file, as a path relative to ~/Downloads."""
    found: list[Path] = []
    for root in ("leo", "eh-plots"):
        base = DOWNLOADS / root
        if base.is_dir():
            found += [p.relative_to(DOWNLOADS) for p in base.rglob("*") if p.is_file()]
    for pattern in ("pp_*.gcode", "pp_*.png"):
        found += [p.relative_to(DOWNLOADS) for p in DOWNLOADS.glob(pattern)]
    return sorted(p for p in found if p.name != ".DS_Store")


def plan_moves() -> tuple[list[tuple[Path, Path]], list[Path]]:
    moves: list[tuple[Path, Path]] = []
    unmatched: list[Path] = []
    for rel in collect():
        subject = subject_for(rel)
        if subject is None:
            unmatched.append(rel)
            continue
        if subject == REFERENCE_DIR:
            dest = GALLERY / REFERENCE_DIR / rel.name
        else:
            dest = GALLERY / subject / tier_for(rel) / rel.name
        moves.append((DOWNLOADS / rel, dest))
    return moves, unmatched


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="print the plan, move nothing")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    moves, unmatched = plan_moves()

    by_subject: dict[str, int] = {}
    for _src, dst in moves:
        key = str(dst.parent.relative_to(GALLERY))
        by_subject[key] = by_subject.get(key, 0) + 1
    for key in sorted(by_subject):
        logger.info("%4d  %s", by_subject[key], key)
    logger.info("--- %d files routed, %d unmatched ---", len(moves), len(unmatched))
    for rel in unmatched:
        logger.warning("UNMATCHED  %s", rel)

    if args.dry_run:
        return 1 if unmatched else 0
    if unmatched:
        logger.error("refusing to move with unmatched files; add a rule first")
        return 1

    collisions = [d for _s, d in moves if d.exists()]
    if collisions:
        for dst in collisions:
            logger.error("COLLISION  %s", dst)
        return 1

    log_path = GALLERY / "MOVES.tsv"
    GALLERY.mkdir(parents=True, exist_ok=True)
    with log_path.open("a") as log:
        for src, dst in moves:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            log.write(f"{src}\t{dst}\n")
    logger.info("moved %d files; reversal log at %s", len(moves), log_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
