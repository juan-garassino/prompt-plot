"""scripts/prints_export.py — publish verdicts -> catalog.json + site assets -> GCS.

The catalog is consumed by the portfolio site (career-navigator's Prints
section), so the v1 contract asserted here is the wire format: asset paths are
relative to the catalog, ``pens[]`` is per layer index, ``pen_count`` counts
unique names, ``plotted`` is null or an object, ``sheet_raster`` is null unless
the SVG tripped the size guard.

Fixtures follow tests/test_prints_publish.py:env — every module global is
repointed at tmp, so the real feedback log and gallery are never touched. The
subject manifest is written by gallery_index.build_manifest itself, so it has
the real shape. No real gcloud: push() is exercised through a recording stub.
"""

from __future__ import annotations

import json
import logging
import re
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import gallery_feedback as fb  # noqa: E402
import gallery_index as gi  # noqa: E402
import prints_export as pe  # noqa: E402
import prints_render as pr  # noqa: E402

SUBJECT = "studio/fam"
STEM = "pp_fam_wave_v3"
NAME = f"{STEM}.png"

GCODE = """\
; promptplot render
; piece     /somewhere/else/001-PromptPlot/studio/fam-slug/rounds/r02/piece.py
; function  fam_wave
; seed      7
; paper     a6 landscape
; pens      {pens}
; colors    2
; rendered  2026-09-20T12:16:38
; commands  12
M5
G0 X10 Y20
M3 S1000 ; color=0
G1 X30 Y20 F2200 ; color=0
G1 X30 Y40 F2200 ; color=0
M5
; color=1
G0 X50 Y60
M3 S1000
G1 X70 Y80 F2200
M5
"""

DESCRIPTION = """\
# THE WAVE FAMILY — description

<!-- written by a test -->

## In one line
A wave drawn as two pens.

Second paragraph that is not the one line.

## What is on the sheet
- crimson crests
- black troughs

## The science it encodes
Superposition, honestly.

## Keep — what works
- everything
"""

TOP_KEYS = ["version", "generated", "count", "prints"]
PRINT_KEYS = ["id", "subject", "basename", "slug", "family", "title", "one_line", "sections",
              "paper", "pens", "pen_count", "stats", "seed", "piece", "rendered",
              "published_at", "order", "size", "detail", "plotted", "assets", "bytes"]


def pub(verdict: str = "publish", name: str = NAME, subject: str = SUBJECT,
        when: str = "2026-10-01T22:14:03") -> dict:
    return {"when": when, "scope": "publish", "subject": subject, "basename": name,
            "target": f"{subject}/@publish/{name}", "verdict": verdict}


def write_log(log: Path, *records: dict) -> None:
    log.write_text("".join(json.dumps(r) + "\n" for r in records))


def index(gal: Path, subject: str = SUBJECT) -> None:
    sub = gal / subject
    (sub / "manifest.json").write_text(json.dumps(gi.build_manifest(sub), indent=2))


def plate(gal: Path, tier: str = "current", stem: str = STEM, pens: str = "crimson,black",
          gcode: bool = True, subject: str = SUBJECT) -> None:
    d = gal / subject / tier
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{stem}.png").write_bytes(b"png")
    if gcode:
        (d / f"{stem}.gcode").write_text(GCODE.format(pens=pens))


@pytest.fixture
def env(tmp_path, monkeypatch):
    st, gal = tmp_path / "studio", tmp_path / "gallery"
    (st / "fam-slug").mkdir(parents=True)
    (st / "fam-slug" / "DESCRIPTION.md").write_text(DESCRIPTION)
    log = st / "feedback.jsonl"
    # the gallery family `fam` resolves to the studio slug `fam-slug`
    monkeypatch.setitem(fb._ALIAS, "fam", "fam-slug")
    for mod, name, val in ((fb, "REPO", tmp_path), (fb, "STUDIO", st), (fb, "GALLERY", gal),
                           (fb, "LOG", log), (gi, "GALLERY", gal), (pe, "REPO", tmp_path),
                           (pe, "STUDIO", st), (pe, "OVERRIDES", st / "prints.json")):
        monkeypatch.setattr(mod, name, val)
    plate(gal)
    (gal / SUBJECT / "trials").mkdir()
    index(gal)
    write_log(log, pub())
    return {"tmp": tmp_path, "studio": st, "gallery": gal, "log": log, "out": tmp_path / "out"}


def export(env, **kw) -> dict:
    return pe.build_catalog(env["out"], env["gallery"], **kw)


def asset_mtimes(out: Path) -> dict:
    return {p: p.stat().st_mtime_ns for p in sorted((out / "assets").rglob("*")) if p.is_file()}


# ----------------------------------------------------------------- the contract


def test_catalog_matches_the_v1_contract(env):
    cat = export(env)
    on_disk = json.loads((env["out"] / "catalog.json").read_text())
    assert on_disk == cat
    assert list(cat) == TOP_KEYS
    assert cat["version"] == 1 and cat["count"] == 1
    assert cat["generated"][-6] in "+-"  # ISO with a tz offset
    (p,) = cat["prints"]
    assert list(p) == PRINT_KEYS

    assert p["id"] == "fam-wave-v3"
    assert (p["subject"], p["basename"], p["slug"], p["family"]) == (
        SUBJECT, NAME, "fam-slug", "fam")
    assert p["title"] == "THE WAVE FAMILY"
    assert p["one_line"] == "A wave drawn as two pens."
    assert p["sections"] == [
        {"heading": "What is on the sheet", "md": "- crimson crests\n- black troughs"},
        {"heading": "The science it encodes", "md": "Superposition, honestly."},
    ]
    assert p["paper"] == {"size": "a6", "orientation": "landscape", "w_mm": 148, "h_mm": 105,
                          "margin_mm": 10}
    assert p["pens"] == [
        {"index": 0, "name": "crimson", "css": "#dc143c", "width_mm": 0.35},
        {"index": 1, "name": "black", "css": "#000000", "width_mm": 0.35},
    ]
    assert p["pen_count"] == 2
    gstats = json.loads((env["gallery"] / SUBJECT / "manifest.json").read_text())["files"]
    st = next(f for f in gstats if f["kind"] == "gcode")["stats"]
    assert p["stats"] == {"draw_mm": st["draw_mm"], "travel_mm": st["travel_mm"],
                          "commands": st["commands"], "pen_cycles": st["pen_cycles"],
                          "est_minutes": round(gi.plot_minutes(st))}
    assert p["seed"] == 7
    assert p["piece"] == "studio/fam-slug/rounds/r02/piece.py::fam_wave"
    assert p["rendered"] == "2026-09-20T12:16:38"
    assert p["published_at"] == "2026-10-01T22:14:03"
    assert p["order"] == 1000 and p["size"] == "s" and p["detail"] is None and p["plotted"] is None

    sha = gi.sha256(env["gallery"] / SUBJECT / "current" / f"{STEM}.gcode")
    a = p["assets"]
    m = re.fullmatch(rf"assets/fam-wave-v3/({sha}-r{pr.RENDER_VERSION}-[0-9a-f]{{6}})\.svg",
                     a["sheet"])
    assert m, a["sheet"]
    base = f"assets/fam-wave-v3/{m.group(1)}"
    assert list(a) == ["sheet", "sheet_raster", "thumb", "technical", "photo", "thumb_px"]
    assert a["sheet"] == f"{base}.svg" and a["sheet_raster"] is None
    assert a["thumb"] == f"{base}.thumb.webp" and a["technical"] == f"{base}.tech.webp"
    assert a["photo"] is None
    with Image.open(env["out"] / a["thumb"]) as im:
        assert list(im.size) == a["thumb_px"] and max(im.size) == 640
    for key in ("sheet", "thumb", "technical"):
        assert p["bytes"][key] == (env["out"] / a[key]).stat().st_size > 0
    assert list(p["bytes"]) == ["sheet", "thumb", "technical"]
    svg = (env["out"] / a["sheet"]).read_text()
    assert svg.count("<path ") == 2 and 'viewBox="0 0 148 105"' in svg


def test_pens_are_per_layer_and_pen_count_is_unique_names(env):
    plate(env["gallery"], pens="black,black")
    index(env["gallery"])
    (p,) = export(env)["prints"]
    assert [(x["index"], x["name"]) for x in p["pens"]] == [(0, "black"), (1, "black")]
    assert p["pen_count"] == 1


def test_id_is_stable_when_the_render_sits_in_trials(env):
    first = export(env)["prints"][0]["id"]
    gal = env["gallery"] / SUBJECT
    for ext in (".png", ".gcode"):
        (gal / "current" / f"{STEM}{ext}").rename(gal / "trials" / f"{STEM}{ext}")
    index(env["gallery"])
    (p,) = export(env)["prints"]
    assert p["id"] == first == "fam-wave-v3"


def test_resolve_render_prefers_the_best_tier(env):
    plate(env["gallery"], tier="trials")
    index(env["gallery"])
    render, gcode = pe.resolve_render(env["gallery"], SUBJECT, NAME)
    assert render["rel"] == f"current/{NAME}"
    assert gcode["rel"] == f"current/{STEM}.gcode"
    assert pe.resolve_render(env["gallery"], SUBJECT, "pp_nope.png") is None
    assert pe.resolve_render(env["gallery"], "studio/missing", NAME) is None


def test_slugify_strips_pp_and_the_repeated_family():
    assert pe.print_id("attention_DAG", "pp_attention_DAG_landscape.png") == \
        "attention-dag-landscape"
    assert pe.print_id("cnn_passes", "pp_cnn_passes_abstract_v10.png") == \
        "cnn-passes-abstract-v10"
    assert pe.print_id("head", "pp-head-v2.png") == "head-v2"
    assert pe.print_id("weights", "bauhaus_weights_seed3.png") == "weights-bauhaus-weights-seed3"
    assert pe.slugify("--Hello__World!!") == "hello-world"


def test_describe_falls_back_when_there_is_no_description(env):
    assert pe.describe("nope", family="fam") == {"title": "fam", "one_line": "", "sections": []}
    d = pe.describe("fam-slug")
    assert d["title"] == "THE WAVE FAMILY" and d["one_line"] == "A wave drawn as two pens."


def test_a_missing_description_warns_and_humanises_the_title(env, caplog, capsys):
    plate(env["gallery"], subject="studio/res_backprop", stem="pp_res_backprop_v3")
    index(env["gallery"], subject="studio/res_backprop")
    write_log(env["log"], pub(), pub(subject="studio/res_backprop", name="pp_res_backprop_v3.png"))
    with caplog.at_level(logging.WARNING, logger="prints_export"):
        cat = export(env)
    p = next(x for x in cat["prints"] if x["family"] == "res_backprop")
    assert p["title"] == "res backprop" and p["one_line"] == "" and p["sections"] == []
    assert "no studio/resonance-backprop/DESCRIPTION.md" in caplog.text
    assert "set title in prints.json" in caplog.text
    assert pe.main(["--gallery", str(env["gallery"]), "--out", str(env["out"]), "--list"]) == 0
    lines = capsys.readouterr().out.splitlines()
    gcode_lines = [l for l in lines if "gcode" in l]
    assert any("res_backprop" in l and "no description" in l for l in gcode_lines)
    assert any("studio/fam/" in l and "no description" not in l for l in gcode_lines)


def test_piece_drops_the_plate_writer_annotation():
    head = {"piece": "/x/repo/studio/resonance-backprop/rounds/r04/piece.py (plate.py)",
            "function": "attention_as_resonance"}
    assert pe._piece(head) == \
        "studio/resonance-backprop/rounds/r04/piece.py::attention_as_resonance"


def test_a_plate_magic_header_is_exported_as_headered(env):
    g = env["gallery"] / SUBJECT / "current" / f"{STEM}.gcode"
    g.write_text(GCODE.format(pens="crimson,black").replace(
        "; promptplot render", "; promptplot PLATE (stream order kept)"))
    index(env["gallery"])
    (p,) = export(env)["prints"]
    assert p["seed"] == 7 and p["paper"]["size"] == "a6"


def test_one_line_falls_back_to_the_first_sentence_of_the_title(env):
    (env["studio"] / "fam-slug" / "DESCRIPTION.md").write_text(
        "# THE WAVE. A FAMILY — description\n\n## What is on the sheet\nwaves\n")
    d = pe.describe("fam-slug")
    assert d["title"] == "THE WAVE. A FAMILY"
    assert d["one_line"] == "THE WAVE."
    assert d["sections"] == [{"heading": "What is on the sheet", "md": "waves"}]


# ---------------------------------------------------------------- overrides


def test_overrides_title_order_widths_and_plotted_photo(env):
    photo = env["gallery"] / SUBJECT / "plotted" / "IMG_2231.jpg"
    photo.parent.mkdir()
    Image.new("RGB", (40, 30), (200, 10, 10)).save(photo)
    key = f"{SUBJECT}/{NAME}"
    env["studio"].joinpath("prints.json").write_text(json.dumps({key: {
        "id": "the-wave", "title": "The Wave", "order": 10, "pen_widths_mm": [0.3, 0.5],
        "plotted": {"date": "2026-09-13", "paper": "A3 Fabriano", "pens": ["Staedtler 0.3"],
                    "photo": f"gallery/{SUBJECT}/plotted/IMG_2231.jpg"}}}))
    (p,) = export(env)["prints"]
    assert p["id"] == "the-wave" and p["title"] == "The Wave" and p["order"] == 10
    assert [x["width_mm"] for x in p["pens"]] == [0.3, 0.5]
    rel = p["plotted"]["photo"]
    assert rel == p["assets"]["photo"]
    assert rel.startswith("assets/the-wave/") and rel.endswith(".photo.webp")
    assert (env["out"] / rel).is_file()
    assert p["plotted"] == {"date": "2026-09-13", "paper": "A3 Fabriano",
                            "pens": ["Staedtler 0.3"], "photo": rel}
    assert p["assets"]["sheet"].startswith("assets/the-wave/")
    assert 'stroke-width="0.5"' in (env["out"] / p["assets"]["sheet"]).read_text()


@pytest.mark.parametrize("size, expected, warns", [
    ("l", "l", False), ("m", "m", False), ("s", "s", False), ("xl", "s", True), (None, "s", False)])
def test_override_size_sets_the_mosaic_tile(env, caplog, size, expected, warns):
    ov = {"title": "x"} if size is None else {"size": size}
    env["studio"].joinpath("prints.json").write_text(json.dumps({f"{SUBJECT}/{NAME}": ov}))
    with caplog.at_level(logging.WARNING, logger="prints_export"):
        (p,) = export(env)["prints"]
    assert p["size"] == expected
    assert ("is not one of" in caplog.text) is warns


@pytest.mark.parametrize("detail, expected, warns", [
    ({"u": 0.72, "v": 0.3}, {"u": 0.72, "v": 0.3, "zoom": 2.4}, False),
    ({"u": 0.5, "v": 0.5, "zoom": 3}, {"u": 0.5, "v": 0.5, "zoom": 3.0}, False),
    ({"u": 1.4, "v": 0.3}, None, True),
    ({"u": 0.5, "v": 0.5, "zoom": 9}, None, True),
    ({"x": 0.5}, None, True),
    ("centre", None, True)])
def test_override_detail_is_where_the_site_crop_looks(env, caplog, detail, expected, warns):
    env["studio"].joinpath("prints.json").write_text(json.dumps({f"{SUBJECT}/{NAME}": {"detail": detail}}))
    with caplog.at_level(logging.WARNING, logger="prints_export"):
        (p,) = export(env)["prints"]
    assert p["detail"] == expected
    assert ("detail" in caplog.text) is warns


def test_plotted_without_a_photo_on_disk_keeps_photo_null(env, caplog):
    env["studio"].joinpath("prints.json").write_text(json.dumps({f"{SUBJECT}/{NAME}": {
        "plotted": {"date": "2026-09-13", "photo": "gallery/studio/fam/plotted/gone.jpg"}}}))
    with caplog.at_level(logging.WARNING, logger="prints_export"):
        (p,) = export(env)["prints"]
    assert p["plotted"] == {"date": "2026-09-13", "photo": None}
    assert p["assets"]["photo"] is None
    assert "gone.jpg" in caplog.text


def test_overrides_paper_and_pens_only_without_a_header(env):
    g = env["gallery"] / SUBJECT / "current" / f"{STEM}.gcode"
    g.write_text("\n".join(l for l in GCODE.format(pens="x").splitlines()
                           if not l.startswith("; ") or "color" in l) + "\n")
    index(env["gallery"])
    assert export(env)["prints"] == []  # neither header nor override: skipped

    env["studio"].joinpath("prints.json").write_text(json.dumps({f"{SUBJECT}/{NAME}": {
        "paper": "a5 portrait", "pens": ["gold", "black"]}}))
    (p,) = export(env)["prints"]
    assert p["paper"] == {"size": "a5", "orientation": "portrait", "w_mm": 148, "h_mm": 210,
                          "margin_mm": 10}
    assert [x["name"] for x in p["pens"]] == ["gold", "black"]
    assert p["seed"] is None and p["piece"] == "" and p["rendered"] == ""


def test_override_paper_is_ignored_when_the_header_has_one(env):
    env["studio"].joinpath("prints.json").write_text(json.dumps({f"{SUBJECT}/{NAME}": {
        "paper": "a3 portrait", "pens": ["gold", "gold"]}}))
    (p,) = export(env)["prints"]
    assert p["paper"]["size"] == "a6" and [x["name"] for x in p["pens"]] == ["crimson", "black"]


def test_override_keys_not_published_or_not_on_disk_warn(env, caplog):
    env["studio"].joinpath("prints.json").write_text(json.dumps({
        f"{SUBJECT}/pp_fam_ghost.png": {"title": "x"}}))
    with caplog.at_level(logging.WARNING, logger="prints_export"):
        cat = export(env)
    assert cat["count"] == 1
    assert "pp_fam_ghost.png" in caplog.text and "not published" in caplog.text
    assert "not on disk" in caplog.text


def test_load_overrides_missing_file_is_empty(env, tmp_path):
    assert pe.load_overrides(tmp_path / "nope.json") == {}
    assert pe.load_overrides() == {}


# ------------------------------------------------------------ skip, guard, idempotency


def test_a_published_render_without_gcode_is_skipped_with_a_warning(env, caplog):
    plate(env["gallery"], stem="pp_fam_bare_v1", gcode=False)
    index(env["gallery"])
    write_log(env["log"], pub(), pub(name="pp_fam_bare_v1.png", when="2026-10-02T09:00:00"))
    with caplog.at_level(logging.WARNING, logger="prints_export"):
        cat = export(env)
    assert [p["basename"] for p in cat["prints"]] == [NAME]
    assert "pp_fam_bare_v1.png" in caplog.text and "no gcode" in caplog.text


def test_svg_over_the_size_guard_also_ships_a_raster(env, monkeypatch):
    monkeypatch.setattr(pe, "SVG_LIMIT", 10)
    (p,) = export(env)["prints"]
    raster = p["assets"]["sheet_raster"]
    assert raster == p["assets"]["sheet"].replace(".svg", ".raster.webp")
    with Image.open(env["out"] / raster) as im:
        assert max(im.size) == 2600


def _redraw(env, paper: str, x: float) -> None:
    g = env["gallery"] / SUBJECT / "current" / f"{STEM}.gcode"
    g.write_text(GCODE.format(pens="crimson,black").replace("a6 landscape", paper)
                 .replace("G1 X70 Y80", f"G1 X{x} Y80"))
    index(env["gallery"])


def test_a_transposed_sheet_is_fitted_to_the_strokes(env, caplog):
    _redraw(env, "a6 portrait", 140)  # 105 x 148 declared, strokes reach x=140
    with caplog.at_level(logging.WARNING):
        (p,) = export(env)["prints"]
    assert p["paper"] == {"size": "a6", "orientation": "landscape", "w_mm": 148, "h_mm": 105,
                          "margin_mm": 10}
    assert 'viewBox="0 0 148 105"' in (env["out"] / p["assets"]["sheet"]).read_text()
    assert "transposing" in caplog.text and "overflow the 148x105" not in caplog.text


def test_strokes_overflowing_the_sheet_warn(env, caplog):
    _redraw(env, "a6 landscape", 200)
    with caplog.at_level(logging.WARNING, logger="prints_export"):
        (p,) = export(env)["prints"]
    assert p["paper"]["w_mm"] == 148
    assert "overflow the 148x105 mm sheet" in caplog.text


def test_second_run_renders_nothing(env, monkeypatch):
    export(env)
    before = asset_mtimes(env["out"])
    assert len(before) == 3

    def boom(*a, **k):
        raise AssertionError("rendered on a cached run")

    for fn in ("parse_polylines", "write_svg", "write_thumb", "write_technical", "write_raster"):
        monkeypatch.setattr(pr, fn, boom)
    cat = export(env)
    assert asset_mtimes(env["out"]) == before
    assert cat["prints"][0]["assets"]["thumb_px"] == [640, 454]


def test_force_rerenders(env):
    export(env)
    before = asset_mtimes(env["out"])
    export(env, force=True)
    after = asset_mtimes(env["out"])
    assert set(after) == set(before)
    assert all(after[p] >= before[p] for p in before) and after != before


def test_a_changed_gcode_gets_new_asset_names(env):
    old = export(env)["prints"][0]["assets"]["sheet"]
    g = env["gallery"] / SUBJECT / "current" / f"{STEM}.gcode"
    g.write_text(g.read_text() + "G0 X0 Y0\n")
    index(env["gallery"])
    new = export(env)["prints"][0]["assets"]["sheet"]
    assert new != old and (env["out"] / new).is_file()


def _override(env, **fields) -> None:
    env["studio"].joinpath("prints.json").write_text(json.dumps({f"{SUBJECT}/{NAME}": fields}))


def test_a_width_edit_gets_new_asset_names_and_leaves_the_old_ones(env):
    _override(env, pen_widths_mm=[0.3, 0.5])
    old = export(env)["prints"][0]["assets"]
    before = asset_mtimes(env["out"])
    _override(env, pen_widths_mm=[0.3, 0.8])
    new = export(env)["prints"][0]["assets"]
    for k in ("sheet", "thumb", "technical"):
        assert new[k] != old[k] and (env["out"] / new[k]).is_file()
        assert new[k].split("-r")[0] == old[k].split("-r")[0]  # same gcode sha
    assert 'stroke-width="0.8"' in (env["out"] / new["sheet"]).read_text()
    # the old objects are immutable on the bucket: never rewritten
    assert {p: m for p, m in asset_mtimes(env["out"]).items() if p in before} == before


def test_a_headerless_pens_edit_gets_new_asset_names(env):
    g = env["gallery"] / SUBJECT / "current" / f"{STEM}.gcode"
    g.write_text("M5\nG0 X10 Y20\nM3 S1000 ; color=0\nG1 X30 Y20 ; color=0\nM5\n")
    index(env["gallery"])
    _override(env, paper="a6 landscape", pens=["gold", "black"])
    a = export(env)["prints"][0]["assets"]["sheet"]
    _override(env, paper="a6 landscape", pens=["crimson", "black"])
    b = export(env)["prints"][0]["assets"]["sheet"]
    assert a != b and "#dc143c" in (env["out"] / b).read_text()


def test_one_broken_plate_is_skipped_not_fatal(env, caplog):
    plate(env["gallery"], stem="pp_fam_two_v1")
    index(env["gallery"])
    write_log(env["log"], pub(), pub(name="pp_fam_two_v1.png"))
    _override(env, pen_widths_mm=["fat"])
    skipped: list = []
    with caplog.at_level(logging.ERROR, logger="prints_export"):
        cat = pe.build_catalog(env["out"], env["gallery"], skipped=skipped)
    assert [p["id"] for p in cat["prints"]] == ["fam-two-v1"]
    assert skipped == [f"{SUBJECT}/{NAME}"] and "export failed" in caplog.text


def test_a_manifest_that_is_not_an_object_resolves_to_nothing(env):
    (env["gallery"] / SUBJECT / "manifest.json").write_text("[1, 2]")
    assert pe.resolve_render(env["gallery"], SUBJECT, NAME) is None


def test_piece_never_leaks_an_absolute_path():
    assert pe._piece({"piece": "/Users/me/tmp/scratch/thing.py", "function": "f"}) == \
        "thing.py::f"
    assert pe._piece({"piece": "/x/repo/studio/a/rounds/r01/piece.py", "function": "f"}) == \
        "studio/a/rounds/r01/piece.py::f"
    assert pe._piece({}) == ""


def test_unpublish_removes_the_print(env):
    plate(env["gallery"], stem="pp_fam_two_v1")
    index(env["gallery"])
    write_log(env["log"], pub(), pub(name="pp_fam_two_v1.png", when="2026-10-02T09:00:00"))
    assert {p["basename"] for p in export(env)["prints"]} == {NAME, "pp_fam_two_v1.png"}
    write_log(env["log"], pub(), pub(name="pp_fam_two_v1.png", when="2026-10-02T09:00:00"),
              pub("unpublish", when="2026-10-03T09:00:00"))
    cat = export(env)
    assert [p["basename"] for p in cat["prints"]] == ["pp_fam_two_v1.png"] and cat["count"] == 1


def test_sort_is_order_then_newest_published(env):
    for stem in ("pp_fam_a", "pp_fam_b", "pp_fam_c"):
        plate(env["gallery"], stem=stem)
    index(env["gallery"])
    write_log(env["log"], pub(name="pp_fam_a.png", when="2026-10-01T10:00:00"),
              pub(name="pp_fam_b.png", when="2026-10-02T10:00:00"),
              pub(name="pp_fam_c.png", when="2026-10-03T10:00:00"))
    env["studio"].joinpath("prints.json").write_text(json.dumps({
        f"{SUBJECT}/pp_fam_a.png": {"order": 5}}))
    ids = [p["id"] for p in export(env)["prints"]]
    assert ids == ["fam-a", "fam-c", "fam-b"]


def test_only_filters_by_id(env):
    plate(env["gallery"], stem="pp_fam_two_v1")
    index(env["gallery"])
    write_log(env["log"], pub(), pub(name="pp_fam_two_v1.png"))
    cat = export(env, only={"fam-two-v1"})
    assert [p["id"] for p in cat["prints"]] == ["fam-two-v1"]
    assert not (env["out"] / "assets" / "fam-wave-v3").exists()


# ------------------------------------------------------------------- push


def test_push_runs_assets_first_then_catalog(tmp_path, monkeypatch):
    calls = []

    def run(cmd, check):
        calls.append((cmd, check))
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(pe.subprocess, "run", run)
    (tmp_path / "assets" / "x").mkdir(parents=True)
    (tmp_path / "assets" / "x" / "a.svg").write_text("<svg/>")
    pe.push(tmp_path, "my-bucket")
    assert calls == [
        (["gcloud", "storage", "cp", "-r", "--no-clobber", "--gzip-local=svg,json",
          "--cache-control=public, max-age=31536000, immutable",
          str(tmp_path / "assets"), "gs://my-bucket/"], True),
        (["gcloud", "storage", "cp", "--gzip-local=json",
          "--cache-control=public, max-age=300",
          str(tmp_path / "catalog.json"), "gs://my-bucket/catalog.json"], True),
    ]


def test_push_with_no_assets_uploads_only_the_catalog(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(pe.subprocess, "run", lambda cmd, check: calls.append(cmd))
    pe.push(tmp_path, "b")
    assert [c[-1] for c in calls] == ["gs://b/catalog.json"]


# -------------------------------------------------------------------- CLI


def test_dry_run_writes_nothing(env, capsys):
    assert pe.main(["--out", str(env["out"]), "--gallery", str(env["gallery"]),
                    "--dry-run"]) == 0
    assert not env["out"].exists()
    out = capsys.readouterr().out
    assert "fam-wave-v3" in out and "render" in out


def test_list_prints_the_published_set(env, capsys):
    assert pe.main(["--gallery", str(env["gallery"]), "--out", str(env["out"]),
                    "--list"]) == 0
    out = capsys.readouterr().out
    assert f"{SUBJECT}/{NAME}" in out and f"current/{STEM}.gcode" in out
    assert "header ok" in out
    assert not env["out"].exists()


def test_exit_1_when_nothing_is_published(env, capsys):
    write_log(env["log"], pub(), pub("unpublish"))
    for extra in ([], ["--list"], ["--dry-run"]):
        assert pe.main(["--out", str(env["out"]), "--gallery", str(env["gallery"]),
                        *extra]) == 1
    assert not env["out"].exists()


def test_main_pushes_and_exit_2_on_push_failure(env, monkeypatch):
    calls = []

    def ok(cmd, check):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(pe.subprocess, "run", ok)
    argv = ["--out", str(env["out"]), "--gallery", str(env["gallery"]), "--push",
            "--bucket", "b"]
    assert pe.main(argv) == 0
    assert [c[-1] for c in calls] == ["gs://b/", "gs://b/catalog.json"]

    def fail(cmd, check):
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(pe.subprocess, "run", fail)
    assert pe.main(argv) == 2


def _recorder(monkeypatch) -> list:
    calls: list = []

    def run(cmd, check):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(pe.subprocess, "run", run)
    return calls


def test_push_refuses_with_skipped_plates_unless_allowed(env, monkeypatch, capsys):
    calls = _recorder(monkeypatch)
    write_log(env["log"], pub(), pub(name="pp_fam_gone.png"))
    argv = ["--out", str(env["out"]), "--gallery", str(env["gallery"]), "--push"]
    assert pe.main(argv) == 3
    assert calls == []
    assert f"{SUBJECT}/pp_fam_gone.png" in capsys.readouterr().out
    assert pe.main(argv + ["--allow-skips"]) == 0
    assert [c[-1] for c in calls] == ["gs://garassino-ai-prints/",
                                      "gs://garassino-ai-prints/catalog.json"]
    # without --push the skip is reported, not fatal
    assert pe.main(argv[:-1]) == 0


def test_push_refuses_an_empty_catalog_unless_allowed(env, monkeypatch):
    calls = _recorder(monkeypatch)
    write_log(env["log"], pub(), pub("unpublish"))
    argv = ["--out", str(env["out"]), "--gallery", str(env["gallery"]), "--push"]
    assert pe.main(argv) == 1 and calls == []
    assert pe.main(argv + ["--allow-empty"]) == 0
    assert [c[-1] for c in calls] == ["gs://garassino-ai-prints/catalog.json"]
    cat = json.loads((env["out"] / "catalog.json").read_text())
    assert cat["count"] == 0 and cat["prints"] == []


def test_only_and_push_together_are_refused(env):
    with pytest.raises(SystemExit) as e:
        pe.main(["--gallery", str(env["gallery"]), "--only", "fam-wave-v3", "--push"])
    assert e.value.code == 2
