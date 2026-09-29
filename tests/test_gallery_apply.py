"""Tier moves for recorded render verdicts (scripts/gallery_apply.py), on a tmp gallery."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import gallery_apply as ga  # noqa: E402
import gallery_feedback as fb  # noqa: E402
import studio_sync  # noqa: E402


@pytest.fixture
def env(tmp_path, monkeypatch):
    st, gal = tmp_path / "studio", tmp_path / "gallery"
    (st / "ising").mkdir(parents=True)
    for tier, names in {"current": ["pp_ising_v6", "pp_ising_COASTLINE_v8"],
                        "trials": ["pp_ising_COASTLINE_v1", "pp_ising_COOLING_STRIP_v2"]}.items():
        d = gal / "studio" / "ising" / tier
        d.mkdir(parents=True)
        for n in names:
            (d / f"{n}.png").write_bytes(b"png " + n.encode())
            (d / f"{n}.gcode").write_text(f"G0 X0 ; {n}\n")
    series = gal / "physics" / "big-bang" / "variants"
    series.mkdir(parents=True)
    (series / "pp_big_bang_a.png").write_bytes(b"a")
    for mod, name, val in ((fb, "STUDIO", st), (fb, "GALLERY", gal), (fb, "REPO", tmp_path),
                           (fb, "LOG", st / "feedback.jsonl"), (ga, "GALLERY", gal),
                           (ga, "MOVES", gal / "MOVES.tsv"), (studio_sync, "GALLERY", gal),
                           (studio_sync, "STUDIO", st), (studio_sync, "DEST", gal / "studio")):
        monkeypatch.setattr(mod, name, val)
    return gal


def vote(verdict: str, rel: str, subject: str = "studio/ising") -> None:
    fb.append({"target": rel, "subject": subject, "verdict": verdict})


def run() -> dict:
    return ga.apply(ga.plan())


def test_target_tier():
    assert ga.target_tier("studio/x", "archive") == "archive"
    assert ga.target_tier("studio/x", "cut") == "cut"
    assert ga.target_tier("studio/x", "promote") == "current"
    assert ga.target_tier("studio/x", "keep", "trials") is None
    assert ga.target_tier("studio/x", "rework", "current") is None
    assert ga.target_tier("studio/x", "keep", "archive") == "trials"
    assert ga.target_tier("physics/y", "rework", "cut") == "variants"
    assert ga.target_tier("studio/x", "works", "archive") is None


def test_archive_moves_the_pair_and_is_idempotent(env):
    vote("archive", "studio/ising/trials/pp_ising_COASTLINE_v1.png")
    moves = ga.plan()
    assert sorted(dst.relative_to(env).as_posix() for _s, dst, _v in moves) == [
        "studio/ising/archive/pp_ising_COASTLINE_v1.gcode",
        "studio/ising/archive/pp_ising_COASTLINE_v1.png"]
    assert run()["moved"] == 2
    assert not (env / "studio/ising/trials/pp_ising_COASTLINE_v1.gcode").exists()
    assert (env / "studio/ising/archive/pp_ising_COASTLINE_v1.gcode").exists()
    assert ga.plan() == []                                 # second run: a no-op
    assert len((env / "MOVES.tsv").read_text().splitlines()) == 2


def test_cut_and_promote(env):
    vote("cut", "studio/ising/current/pp_ising_COASTLINE_v8.png")
    vote("promote", "studio/ising/trials/pp_ising_COOLING_STRIP_v2.png")
    vote("promote", "physics/big-bang/variants/pp_big_bang_a.png", subject="physics/big-bang")
    run()
    assert (env / "studio/ising/cut/pp_ising_COASTLINE_v8.png").exists()
    assert (env / "studio/ising/current/pp_ising_COOLING_STRIP_v2.gcode").exists()
    assert (env / "physics/big-bang/promoted/pp_big_bang_a.png").exists()
    assert ga.plan() == []


def test_restore_after_keep(env):
    vote("archive", "studio/ising/current/pp_ising_COASTLINE_v8.png")
    run()
    assert (env / "studio/ising/archive/pp_ising_COASTLINE_v8.png").exists()
    vote("keep", "studio/ising/archive/pp_ising_COASTLINE_v8.png")
    moves = ga.plan()
    assert {dst.parent.name for _s, dst, _v in moves} == {"current"}   # back where it came from
    run()
    assert (env / "studio/ising/current/pp_ising_COASTLINE_v8.png").exists()
    assert (env / "studio/ising/current/pp_ising_COASTLINE_v8.gcode").exists()
    assert ga.plan() == []


def test_restore_without_history_goes_to_trials_or_variants(env):
    parked = env / "studio/ising/cut"
    parked.mkdir()
    (parked / "pp_ising_old_v1.png").write_bytes(b"x")
    vote("rework", "studio/ising/cut/pp_ising_old_v1.png")
    series = env / "physics/big-bang/archive"
    series.mkdir()
    (series / "pp_big_bang_b.png").write_bytes(b"b")
    vote("keep", "physics/big-bang/archive/pp_big_bang_b.png", subject="physics/big-bang")
    run()
    assert (env / "studio/ising/trials/pp_ising_old_v1.png").exists()
    assert (env / "physics/big-bang/variants/pp_big_bang_b.png").exists()


def test_keep_and_direction_verdicts_move_nothing(env):
    vote("keep", "studio/ising/current/pp_ising_v6.png")
    vote("rework", "studio/ising/trials/pp_ising_COASTLINE_v1.png")
    fb.append({"scope": "direction", "subject": "studio/ising", "direction": "r03",
               "target": "studio/ising/@direction/r03", "verdict": "dead_end"})
    assert ga.plan() == []


def test_missing_and_ambiguous_are_skipped(env, caplog):
    vote("archive", "studio/ising/current/pp_ising_gone_v1.png")
    (env / "studio/ising/archive").mkdir()
    (env / "studio/ising/archive/pp_ising_twice_v1.png").write_bytes(b"1")
    (env / "studio/ising/cut").mkdir()
    (env / "studio/ising/cut/pp_ising_twice_v1.png").write_bytes(b"2")
    vote("promote", "studio/ising/current/pp_ising_twice_v1.png")
    with caplog.at_level("WARNING"):
        assert ga.plan() == []
    assert "missing" in caplog.text and "2 files named pp_ising_twice_v1.png" in caplog.text


def test_dry_run_moves_nothing(env, monkeypatch):
    vote("cut", "studio/ising/current/pp_ising_v6.png")
    monkeypatch.setattr(sys, "argv", ["gallery_apply.py", "--dry-run"])
    assert ga.main() == 0
    assert (env / "studio/ising/current/pp_ising_v6.png").exists()
    assert not (env / "MOVES.tsv").exists()


def test_studio_notes_are_repointed(env):
    st = fb.STUDIO
    note = st / "ising" / "LEDGER.md"
    note.write_text("| r03 | gallery/studio/ising/current/pp_ising_COASTLINE_v8.png |\n"
                    "see gallery/studio/ising/current/pp_ising_COASTLINE_v8.gcode and "
                    "gallery/studio/ising/current/pp_ising_COASTLINE_v80.png\n")
    vote("archive", "studio/ising/current/pp_ising_COASTLINE_v8.png")
    assert run()["refs"] == 1
    text = note.read_text()
    assert "gallery/studio/ising/archive/pp_ising_COASTLINE_v8.png |" in text
    assert "gallery/studio/ising/archive/pp_ising_COASTLINE_v8.gcode" in text
    assert "gallery/studio/ising/current/pp_ising_COASTLINE_v80.png" in text   # a different file
