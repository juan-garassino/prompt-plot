"""scripts/gallery_index.py: the manifest cache, the archive tier, the inlined
snapshots and the two generated pages (gallery/viewer.html, gallery/board.html).

Every test builds a tiny gallery under tmp_path and monkeypatches the module
globals (GALLERY, STUDIO, gallery_feedback's LOG, the directions module), which
gallery_index reads at call time. Direction data comes from a stub class so the
pages are deterministic; one test runs against the real
scripts/gallery_directions.py when it is importable.

Why these tests exist:
- a full index run is ~10 min (sha256 + GCode replay); the cache makes the
  re-tier after gallery_apply.py take seconds, and must never go stale;
- the viewer TEMPLATE is a plain Python string, and a raw newline inside a JS
  string literal once killed the whole viewer — so every <script> is parsed by
  node, and a node-free lexer checks the templates too;
- ledger thesis text is free prose inlined into a <script>: a `</script>` in it
  must not end the script.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import gallery_feedback as fb  # noqa: E402
import gallery_index as gi  # noqa: E402

GCODE = (
    "M5\nG0 X10 Y10\nM3 S1000 ; color=0\nG1 X50 Y10 F600 ; color=0\n"
    "G1 X50 Y40 ; color=0\nM5\nG0 X0 Y0\n"
)
PNG = b"\x89PNG\r\n\x1a\n" + b"\0" * 32  # never decoded, only listed
HOSTILE = "EVIL </script><script>window.PWNED=1</script> <!-- __FEEDBACK__"


class _StubDirections:
    """Stands in for gallery_directions: two directions on studio/foo (one with
    a label that tries to break out of the <script>), nothing elsewhere."""

    def __init__(self) -> None:
        self.calls: list[tuple] = []

    def parse_ledger(self, text: str) -> list[dict]:
        self.calls.append(("parse_ledger", len(text)))
        return [{"round": "r01", "parent": None, "thesis": "ART DECO", "render":
                 "pp_foo_A_v2.png", "art": "7.0/6", "sci": "8/8/8", "verdict": "PASS",
                 "canon": "deco", "note": ""}]

    def directions(self, subject: str) -> dict[str, dict]:
        self.calls.append(("directions", subject))
        if subject != "studio/foo":
            return {}
        return {
            "r01": {"label": HOSTILE, "slug": "foo", "root": "r01", "rounds": ["r01"],
                    "parent_of_root": None, "canon": "Art Deco", "canon_norm": "deco",
                    "order": "circles", "lineage": "Cassandre",
                    "best": {"round": "r01", "art_avg": 7.0, "art_min": 6, "sci": "8/8/8"}},
            "r02": {"label": "SWISS GRID", "slug": "foo", "root": "r02", "rounds": ["r02"],
                    "parent_of_root": "r01", "canon": "Swiss", "canon_norm": "swiss",
                    "order": "grid", "lineage": "", "best": {}},
        }

    def direction_of(self, subject: str, name: str) -> str | None:
        self.calls.append(("direction_of", subject, name))
        if subject == "studio/foo":
            return "r02" if "_B_" in name else "r01"
        if subject == "physics/bar":
            return "original"
        return None


def _put(root: Path, rel: str, gcode: bool = True) -> None:
    png = root / f"{rel}.png"
    png.parent.mkdir(parents=True, exist_ok=True)
    png.write_bytes(PNG)
    if gcode:
        (root / f"{rel}.gcode").write_text(GCODE)


@pytest.fixture
def gallery(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    g = tmp_path / "gallery"
    studio = tmp_path / "studio"
    foo = g / "studio" / "foo"
    for rel in ("current/pp_foo_A_v2", "trials/pp_foo_A_v1", "trials/pp_foo_B_v1",
                "archive/pp_foo_B_v0", "cut/pp_foo_A_v0"):
        _put(foo, rel)
    _put(g / "physics" / "bar", "current/bar_v1", gcode=False)
    (foo / "trials" / ".DS_Store").write_bytes(b"\0")
    (studio / "foo").mkdir(parents=True)
    (studio / "foo" / "LEDGER.md").write_text("## Rounds\n| round | render |\n|---|---|\n")
    monkeypatch.setattr(gi, "GALLERY", g)
    monkeypatch.setattr(gi, "STUDIO", studio)
    monkeypatch.setattr(fb, "GALLERY", g)
    monkeypatch.setattr(fb, "STUDIO", studio)
    monkeypatch.setattr(fb, "LOG", studio / "feedback.jsonl")
    monkeypatch.setattr(gi, "gd", _StubDirections())
    return g


def _log(studio: Path, *records: dict) -> None:
    with (studio / "feedback.jsonl").open("a") as fh:
        for r in records:
            fh.write(json.dumps(r) + "\n")


def _scripts(page: str) -> list[str]:
    return re.findall(r"<script>(.*?)</script>", page, re.S)


def _manifest(g: Path, subject: str) -> dict:
    return json.loads((g / subject / "manifest.json").read_text())


# ---------------------------------------------------------------------------
# manifests: tiers and the cache
# ---------------------------------------------------------------------------

def test_archive_and_cut_are_indexed_but_not_printable(gallery: Path) -> None:
    gi.build()
    tiers = {f["rel"]: f["tier"] for f in _manifest(gallery, "studio/foo")["files"]}
    assert tiers["archive/pp_foo_B_v0.png"] == "archive"
    assert tiers["cut/pp_foo_A_v0.gcode"] == "cut"
    assert gi.TIER_RANK["archive"] == 6 and gi.TIER_RANK["cut"] == 7
    printq = (gallery / "PRINT.md").read_text()
    assert "archive/" not in printq and "cut/" not in printq
    assert "current/pp_foo_A_v2.gcode" in printq
    assert "`archive`" in (gallery / "INDEX.md").read_text()


def test_cached_run_never_hashes_or_replays(gallery: Path, monkeypatch) -> None:
    gi.build()
    first = _manifest(gallery, "studio/foo")

    def boom(*_a, **_k):
        raise AssertionError("cache miss: recomputed an unchanged file")

    monkeypatch.setattr(gi, "gcode_stats", boom)
    monkeypatch.setattr(gi, "sha256", boom)
    gi.build()
    again = _manifest(gallery, "studio/foo")
    assert again["files"] == first["files"]
    assert all("mtime_ns" in f for f in again["files"])


def test_cache_survives_a_tier_move_and_legacy_manifests(gallery: Path, monkeypatch) -> None:
    gi.build()
    foo = gallery / "studio" / "foo"
    # gallery_apply moves with a rename: name, size and mtime are unchanged
    (foo / "trials" / "pp_foo_B_v1.png").rename(foo / "archive" / "pp_foo_B_v1.png")
    (foo / "trials" / "pp_foo_B_v1.gcode").rename(foo / "archive" / "pp_foo_B_v1.gcode")
    # a manifest written before mtime_ns existed still seeds the cache
    m = _manifest(gallery, "studio/foo")
    for f in m["files"]:
        f.pop("mtime_ns")
    (foo / "manifest.json").write_text(json.dumps(m))

    def boom(*_a, **_k):
        raise AssertionError("cache miss")

    monkeypatch.setattr(gi, "gcode_stats", boom)
    monkeypatch.setattr(gi, "sha256", boom)
    gi.build()
    tiers = {f["rel"]: f["tier"] for f in _manifest(gallery, "studio/foo")["files"]}
    assert tiers["archive/pp_foo_B_v1.gcode"] == "archive"


def test_changed_file_and_full_recompute(gallery: Path, monkeypatch) -> None:
    gi.build()
    calls: list[str] = []
    real = gi.gcode_stats
    monkeypatch.setattr(gi, "gcode_stats", lambda p: calls.append(p.name) or real(p))
    g = gallery / "studio" / "foo" / "trials" / "pp_foo_A_v1.gcode"
    g.write_text(GCODE + "G1 X60 Y60 ; color=0\n")
    gi.build()
    assert calls == ["pp_foo_A_v1.gcode"]
    calls.clear()
    gi.build(full=True)
    assert len(calls) == 5  # every gcode under studio/foo


def test_views_only_reads_manifests_and_drops_missing(gallery: Path, caplog) -> None:
    gi.build()
    manifest = gallery / "studio" / "foo" / "manifest.json"
    before = manifest.stat().st_mtime_ns
    (gallery / "studio" / "foo" / "trials" / "pp_foo_A_v1.png").unlink()
    (gallery / "viewer.html").unlink()
    (gallery / "board.html").unlink()
    with caplog.at_level("WARNING", logger="gallery_index"):
        gi.build(views_only=True)
    assert manifest.stat().st_mtime_ns == before
    assert "gone from disk" in caplog.text
    page = (gallery / "viewer.html").read_text()
    assert "trials/pp_foo_A_v1.png" not in page
    assert (gallery / "board.html").exists()


# ---------------------------------------------------------------------------
# snapshots
# ---------------------------------------------------------------------------

def test_snapshot_keeps_render_scope_only(gallery: Path) -> None:
    studio = gi.STUDIO
    _log(studio,
         {"when": "2026-09-01T10:00:00", "target": "studio/foo/current/pp_foo_A_v2.png",
          "subject": "studio/foo", "verdict": "promote", "note": "old record, no scope"},
         {"when": "2026-09-02T10:00:00", "target": "studio/foo/trials/pp_foo_B_v1.png",
          "subject": "studio/foo", "verdict": "keep", "note": "", "scope": "render"},
         {"when": "2026-09-05T10:00:00", "target": "studio/foo/@direction/r01",
          "subject": "studio/foo", "scope": "direction", "direction": "r01",
          "label": "x", "root": "r01", "verdict": "dead_end", "note": "circles again"})
    snap = gi.feedback_snapshot()
    assert {r["p"] for r in snap["records"]} == {
        "studio/foo/current/pp_foo_A_v2.png", "studio/foo/trials/pp_foo_B_v1.png"}
    assert {r["n"] for r in snap["records"]} == {"pp_foo_A_v2.png", "pp_foo_B_v1.png"}
    # the direction verdict is newer, but it must not move the NEW cutoff
    assert snap["global"] == gi._epoch("2026-09-02T10:00:00")
    dirs = gi.direction_snapshot()
    assert dirs["studio/foo"]["r01"]["v"] == "dead_end"
    assert dirs["studio/foo"]["r01"]["note"] == "circles again"


# ---------------------------------------------------------------------------
# the generated pages
# ---------------------------------------------------------------------------

def test_pages_are_filled_and_escaped(gallery: Path) -> None:
    gi.build()
    for name in ("viewer.html", "board.html"):
        page = (gallery / name).read_text()
        for ph in ("__DATA__", "__FEEDBACK__", "__DIRV__", "__SERIES__", "__ROWS__"):
            # the hostile label spells __FEEDBACK__ inside the data on purpose
            assert page.count(ph) == (1 if ph == "__FEEDBACK__" else 0), (name, ph)
        # only `</script` ends a script (an opening tag inside a JS string is inert)
        assert page.count("</script>") == 1 and len(_scripts(page)) == 1, name
        assert "<\\/script>" in page and "<\\!--" in page
        assert "PWNED" in _scripts(page)[0]  # still inside the one script


def test_viewer_data_carries_directions(gallery: Path) -> None:
    gi.build()
    groups = gi.build_groups(gi.load_manifests())
    foo = next(g for g in groups if g["s"] == "studio/foo")
    assert set(foo["dirs"]) == {"r01", "r02"}
    dk = {s["n"]: s["dk"] for s in foo["shots"]}
    assert dk["pp_foo_B_v1.png"] == "r02" and dk["pp_foo_A_v2.png"] == "r01"
    assert [s["t"] for s in foo["shots"]][:1] == ["current"]
    assert foo["shots"][-1]["t"] == "cut"  # archive and cut rank last


def test_board_rows(gallery: Path) -> None:
    gi.build()
    rows = {r["s"]: r for r in gi.board_rows(gi.build_groups(gi.load_manifests()))}
    foo = rows["studio/foo"]
    assert foo["main"] and foo["ledger"]
    assert [c["k"] for c in foo["cards"]] == ["r01", "r02"]
    r02 = next(c for c in foo["cards"] if c["k"] == "r02")
    assert r02["canon_norm"] == "swiss" and len(r02["shots"]) == 2
    assert not any(sh[1] == ".DS_Store" for c in foo["cards"] for sh in c["shots"])
    # a plate whose every render is `original` is behind the "every plate" toggle
    assert rows["physics/bar"]["main"] is False


class _BrokenDirections(_StubDirections):
    def directions(self, subject: str) -> dict[str, dict]:
        raise RuntimeError("bad ledger")

    def direction_of(self, subject: str, name: str) -> str | None:
        raise RuntimeError("bad ledger")


def test_a_broken_directions_module_never_takes_the_index_down(gallery: Path, monkeypatch) -> None:
    monkeypatch.setattr(gi, "gd", _BrokenDirections())
    gi.build()
    page = (gallery / "viewer.html").read_text()
    assert '"dk":null' in page and '"dirs":{}' in page


def test_real_directions_module(gallery: Path, monkeypatch, tmp_path: Path) -> None:
    import gallery_directions

    monkeypatch.setattr(gi, "gd", gallery_directions)
    monkeypatch.setattr(gallery_directions, "GALLERY", gi.GALLERY)
    monkeypatch.setattr(gallery_directions, "STUDIO", gi.STUDIO)
    (gi.STUDIO / "foo" / "LEDGER.md").write_text(
        "## Rounds\n"
        "| round | parent | thesis | render | art avg/min | sci t/f/l | verdict | note |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| r01 | — | FIRST: the baseline | pp_foo_A_v2.png | 6.0 / 5 | 7 / 7 / 7 | FAIL | x |\n"
        "| r02 | r01 | SWISS GRID: </script> in a thesis | pp_foo_B_v1.png | 7.5 / 7 | 8 / 8 / 8 "
        "| PASS | y |\n")
    gi.build()
    groups = gi.build_groups(gi.load_manifests())
    foo = next(g for g in groups if g["s"] == "studio/foo")
    assert foo["dirs"], "the real module found no directions in the ledger"
    for g in groups:
        assert isinstance(g["dirs"], dict)
        assert all(s["dk"] is None or isinstance(s["dk"], str) for s in g["shots"])
    for name in ("viewer.html", "board.html"):
        page = (gallery / name).read_text()
        assert page.count("</script>") == 1
        _node_check(page, tmp_path, name)


# ---------------------------------------------------------------------------
# the scripts parse
# ---------------------------------------------------------------------------

def _node() -> str | None:
    found = shutil.which("node")
    if found:
        return found
    for cand in sorted(Path.home().glob(".nvm/versions/node/*/bin/node"), reverse=True):
        return str(cand)
    for cand in ("/usr/local/bin/node", "/opt/homebrew/bin/node"):
        if os.access(cand, os.X_OK):
            return cand
    return None


def _node_check(page: str, tmp: Path, name: str) -> None:
    node = _node()
    if node is None:
        pytest.skip("no node binary (PATH, ~/.nvm, /usr/local/bin) to syntax-check with")
    scripts = _scripts(page)
    assert scripts, name
    for i, js in enumerate(scripts):
        f = tmp / f"{name}.{i}.js"
        f.write_text(js)
        out = subprocess.run([node, "--check", str(f)], capture_output=True, text=True)
        assert out.returncode == 0, f"{name} script {i}:\n{out.stderr}"


def test_every_script_passes_node_check(gallery: Path, tmp_path: Path) -> None:
    _log(gi.STUDIO, {"when": "2026-09-01T10:00:00",
                     "target": "studio/foo/current/pp_foo_A_v2.png",
                     "subject": "studio/foo", "verdict": "promote", "note": "a\nb 'q' </script>"})
    gi.build()
    viewer = (gallery / "viewer.html").read_text()
    for needle in ("function enterSwipe", "function swipeKey", "function recordRender",
                   "function recordDirection", "function goTo", "/* ---------- plotter"):
        assert needle in viewer, needle
    _node_check(viewer, tmp_path, "viewer")
    _node_check((gallery / "board.html").read_text(), tmp_path, "board")


def _bad_literals(js: str) -> list[str]:
    """Quoted string / regex literals that contain a raw newline.

    A small JS lexer: comments, '…' "…" `…` strings (template literals may span
    lines), and regex literals (a `/` where an operand is expected)."""
    bad: list[str] = []
    i, n, prev = 0, len(js), ""
    while i < n:
        c = js[i]
        if js.startswith("//", i):
            j = js.find("\n", i)
            i = n if j < 0 else j
            continue
        if js.startswith("/*", i):
            j = js.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if c in "'\"`":
            j = i + 1
            while j < n and js[j] != c:
                j += 2 if js[j] == "\\" else 1
            if c != "`" and "\n" in js[i:j]:
                bad.append(js[i:j + 1])
            i, prev = j + 1, "a"
            continue
        if c == "/" and (prev == "" or prev in "(,=:[!&|?{};+-*%<>~^"):
            j, in_class = i + 1, False
            while j < n:
                ch = js[j]
                if ch == "\\":
                    j += 2
                    continue
                if ch == "\n":
                    bad.append(js[i:j])
                    break
                if ch == "[":
                    in_class = True
                elif ch == "]":
                    in_class = False
                elif ch == "/" and not in_class:
                    break
                j += 1
            i, prev = j + 1, "a"
            continue
        if not c.isspace():
            prev = "a" if (c.isalnum() or c in "_$)]") else c
        i += 1
    return bad


def test_lexer_catches_the_old_bug() -> None:
    assert _bad_literals("const a = 'x\ny';")
    assert _bad_literals('const r = s.match(/@[^\n,;]+/g);')
    assert not _bad_literals("const a = 'x\\ny', b = c / d / e, t = `\n`;")
    assert not _bad_literals("x = y.match(/[/]a/) // it's fine\n")


@pytest.mark.parametrize("name", ["TEMPLATE", "BOARD"])
def test_templates_have_no_raw_newline_in_a_js_literal(name: str) -> None:
    page = getattr(gi, name)
    scripts = _scripts(page)
    assert scripts
    for js in scripts:
        assert _bad_literals(js) == []
