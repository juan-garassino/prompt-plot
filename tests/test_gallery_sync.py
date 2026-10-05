"""Downloads -> gallery sync (scripts/studio_sync.py): never resurrect a parked render."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import studio_sync  # noqa: E402


@pytest.fixture
def env(tmp_path, monkeypatch):
    dl, st, gal = tmp_path / "Downloads", tmp_path / "studio", tmp_path / "gallery"
    dl.mkdir()
    (st / "ising" / "rounds").mkdir(parents=True)
    (gal / "studio" / "ising" / "current").mkdir(parents=True)
    for name, val in (("DOWNLOADS", dl), ("STUDIO", st), ("GALLERY", gal),
                      ("DEST", gal / "studio")):
        monkeypatch.setattr(studio_sync, name, val)
    return dl


def _stage(dl: Path, stem: str, body: bytes) -> None:
    (dl / f"{stem}.png").write_bytes(body)
    (dl / f"{stem}.gcode").write_bytes(body + b" gcode")


def _sync(copy: bool = False) -> dict:
    _summary, moves = studio_sync.plan()
    return studio_sync.execute(moves, copy=copy)


def test_plan_files_by_plate_and_version(env):
    _stage(env, "pp_ising_COASTLINE_v1", b"a")
    _stage(env, "pp_ising_COASTLINE_v2", b"b")
    st = _sync()
    gal = studio_sync.GALLERY / "studio" / "ising"
    assert st["placed"] == 4
    assert (gal / "current" / "pp_ising_COASTLINE_v2.png").exists()
    assert (gal / "trials" / "pp_ising_COASTLINE_v1.gcode").exists()
    assert not list(env.iterdir())


@pytest.mark.parametrize("tier", ["archive", "cut", "promoted"])
def test_identical_parked_render_is_deduped_not_resurrected(env, tier):
    gal = studio_sync.GALLERY / "studio" / "ising"
    (gal / tier).mkdir()
    (gal / tier / "pp_ising_COASTLINE_v1.png").write_bytes(b"a")
    (gal / tier / "pp_ising_COASTLINE_v1.gcode").write_bytes(b"a gcode")
    _stage(env, "pp_ising_COASTLINE_v1", b"a")
    st = _sync()
    assert st["parked"] == 2 and st["placed"] == 0
    assert not (gal / "current" / "pp_ising_COASTLINE_v1.png").exists()
    assert not (gal / "trials" / "pp_ising_COASTLINE_v1.png").exists()
    assert not list(env.iterdir())                      # move mode drops the staging copy
    assert "dedup-parked" in (studio_sync.DEST / "MOVES.tsv").read_text()


def test_copy_mode_keeps_the_staging_copy(env):
    gal = studio_sync.GALLERY / "studio" / "ising"
    (gal / "archive").mkdir()
    (gal / "archive" / "pp_ising_COASTLINE_v1.png").write_bytes(b"a")
    _stage(env, "pp_ising_COASTLINE_v1", b"a")
    st = _sync(copy=True)
    assert st["parked"] == 1
    assert (env / "pp_ising_COASTLINE_v1.png").exists()
    assert not (gal / "current" / "pp_ising_COASTLINE_v1.png").exists()
    assert (gal / "current" / "pp_ising_COASTLINE_v1.gcode").exists()   # not parked: placed


def test_different_bytes_under_a_parked_name_is_new_work(env):
    gal = studio_sync.GALLERY / "studio" / "ising"
    (gal / "archive").mkdir()
    (gal / "archive" / "pp_ising_COASTLINE_v1.png").write_bytes(b"old")
    _stage(env, "pp_ising_COASTLINE_v1", b"new")
    st = _sync()
    assert st["parked"] == 0
    assert (gal / "current" / "pp_ising_COASTLINE_v1.png").read_bytes() == b"new"
    assert (gal / "archive" / "pp_ising_COASTLINE_v1.png").read_bytes() == b"old"


def test_downloads_refs_rewritten_to_gallery(env):
    note = studio_sync.STUDIO / "ising" / "NOTES.md"
    note.write_text("render: ~/Downloads/pp_ising_COASTLINE_v1.png.\n")
    _stage(env, "pp_ising_COASTLINE_v1", b"a")
    assert _sync()["refs"] == 1
    assert note.read_text() == "render: gallery/studio/ising/current/pp_ising_COASTLINE_v1.png.\n"


def test_rewrite_refs_extra_only(env):
    note = studio_sync.STUDIO / "ising" / "LEDGER.md"
    note.write_text("`gallery/studio/ising/current/pp_a_v1.png` ~/Downloads/pp_zz_v1.png\n")
    new = studio_sync.GALLERY / "studio" / "ising" / "archive" / "pp_a_v1.png"
    assert studio_sync.rewrite_refs(extra={"studio/ising/current/pp_a_v1.png": new}) == 1
    assert note.read_text() == "`gallery/studio/ising/archive/pp_a_v1.png` ~/Downloads/pp_zz_v1.png\n"
