"""Backfill GCode for gallery/studio pieces whose current/ holds only a PNG.

A render with no GCode cannot be plotted. `render_candidate.py` used to write
GCode only when asked, so most studio pieces ended up PNG-only. That default is
fixed going forward; this regenerates what was already stranded.

Recipes carry paper, orientation and palette because those are NOT recoverable
from a PNG — the new provenance header exists so this never has to be guessed
again.
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)
REPO = Path(__file__).resolve().parent.parent
PY = REPO / ".venv" / "bin" / "python"
FIVE = "crimson,dodgerblue,goldenrod,forestgreen,black"

# family -> (piece, fn, paper, orientation, palette)
RECIPES: dict[str, tuple] = {
    "res_ffn": ("resonance-ffn", "attention_as_resonance_ffn", "a4", "portrait",
                "crimson,dodgerblue,goldenrod,forestgreen,darkviolet,black"),
    "res_backprop": ("resonance-backprop", "attention_as_resonance", "a4", "portrait", FIVE),
    "massredist": ("mass-redistribution", "mass_redistribution", "a4", "portrait", FIVE),
    "double_slit": ("double-slit", "double_slit_cross_term", "a4", "portrait", FIVE),
    "ds_abacus": ("double-slit", "double_slit_cross_term", "a4", "portrait", FIVE),
    "ds_psy": ("double-slit", "double_slit_cross_term", "a4", "portrait", FIVE),
    "ds_lattice": ("double-slit", "double_slit_cross_term", "a4", "portrait", FIVE),
    "reaction_diffusion": ("reaction-diffusion", "studio_reaction_diffusion", "a4", "portrait", FIVE),
    "bacterio": ("reaction-diffusion", "studio_reaction_diffusion", "a4", "portrait", FIVE),
    "ssm_mamba": ("ssm-mamba", "receding_horizon", "a4", "portrait", FIVE),
    "gan": ("gan", "minimax_duel", "a4", "portrait", FIVE),
    "gnn": ("gnn", "studio_gnn", "a4", "portrait", FIVE),
    "moe": ("moe", "studio_moe", "a4", "portrait", FIVE),
    "vae": ("vae", "studio_vae", "a4", "portrait", FIVE),
    "diffusion": ("diffusion", "diffusion_transport", "a4", "portrait", FIVE),
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="one family")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    scratch = REPO / "gallery" / ".regen"
    scratch.mkdir(parents=True, exist_ok=True)
    ok = fail = skip = 0

    for fam, (slug, fn, paper, orient, palette) in sorted(RECIPES.items()):
        if args.only and fam != args.only:
            continue
        cur = REPO / "gallery" / "studio" / fam / "current"
        if not cur.is_dir():
            skip += 1
            continue
        if list(cur.glob("*.gcode")):
            skip += 1
            continue
        png = next(iter(cur.glob("*.png")), None)
        if png is None:
            skip += 1
            continue
        piece = REPO / "studio" / slug / "rounds" / "r01" / "piece.py"
        if not piece.exists():
            logger.warning("%-22s no piece at %s", fam, piece)
            fail += 1
            continue
        cmd = [
            str(PY), str(REPO / "scripts" / "render_candidate.py"), str(piece),
            "--fn", fn, "--seed", "7", "--paper", paper, "--orientation", orient,
            "--palette", palette,
            "--out", str(scratch / f"{fam}.png"),
            "--gcode", str(cur / png.with_suffix(".gcode").name),
        ]
        if args.dry_run:
            logger.info("%-22s %s", fam, " ".join(cmd[2:]))
            continue
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        if r.returncode == 0:
            logger.info("%-22s OK   %s", fam, (r.stdout.strip().splitlines() or [""])[-1])
            ok += 1
        else:
            logger.warning("%-22s FAIL %s", fam, (r.stderr.strip().splitlines() or [""])[-1][:120])
            fail += 1

    logger.info("--- regenerated %d, failed %d, skipped %d ---", ok, fail, skip)
    return 0


if __name__ == "__main__":
    sys.exit(main())
