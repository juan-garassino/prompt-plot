"""Verdict records and the markdown views agents read (scripts/gallery_feedback.py).

Every path the module touches is a module global read at call time, so each
test repoints them at a tmp studio/ + gallery/ — the real feedback log is never
written.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import gallery_directions as gd  # noqa: E402
import gallery_feedback as fb  # noqa: E402

LEDGER = """# Ledger

## Rounds
| round | parent | thesis | render | art avg/min | sci t/f/l | verdict | note |
|---|---|---|---|---|---|---|---|
| r01 | — | CRITICAL: Tc hero | gallery/studio/ising/current/pp_ising_v6.png | — | — | uncritiqued | seed |
| r02 | r01 | COOLING STRIP: one lattice | gallery/studio/ising/current/pp_ising_COOLING_STRIP_v9.png | 5.86 / 4 | 8 / 7 / 7 | FAIL / FAIL | n |
| r03 | r01 | COASTLINE: full-bleed torus | gallery/studio/ising/current/pp_ising_COASTLINE_v8.png | 5.43 / 4 | 7 / 7 / 6 | FAIL / FAIL | n |
| r04 | r02 | MERGE: r02 sheet + hulls | gallery/studio/ising/current/pp_ising_r04_iterate_v5.png | 6.71 / 6 | 8 / 7 / 7 | FAIL / FAIL | n |
| r06 | r04 (nominal) | WILDCARD: THE SUNBURST. RG flow | gallery/studio/ising/current/pp_ising_r06_wildcard_v11.png | 7.00 / 6 | 7 / 7 / 8 | FAIL / FAIL | n |
"""


@pytest.fixture
def env(tmp_path, monkeypatch):
    st, gal = tmp_path / "studio", tmp_path / "gallery"
    (st / "ising" / "rounds" / "r06").mkdir(parents=True)
    (st / "ising" / "LEDGER.md").write_text(LEDGER)
    (st / "ising" / "rounds" / "r06" / "HANDOFF.md").write_text(
        "canon: art_deco (STYLES.md §2)\norder: radial + nested\nlineage: Van Alen, Chrysler crown\n")
    gal.mkdir()
    monkeypatch.setattr(fb, "REPO", tmp_path)
    monkeypatch.setattr(fb, "STUDIO", st)
    monkeypatch.setattr(fb, "GALLERY", gal)
    monkeypatch.setattr(fb, "LOG", st / "feedback.jsonl")
    monkeypatch.setattr(gd, "STUDIO", st)
    monkeypatch.setattr(gd, "GALLERY", gal)
    return st


def render(verdict: str, name: str = "pp_ising_v6.png", tier: str = "current", **kw) -> dict:
    return {"target": f"studio/ising/{tier}/{name}", "subject": "studio/ising",
            "verdict": verdict, **kw}


def direction(verdict: str, key: str, **kw) -> dict:
    return {"scope": "direction", "subject": "studio/ising", "direction": key,
            "target": f"studio/ising/@direction/{key}", "verdict": verdict, **kw}


# ---------------------------------------------------------------------------
# append: validation
# ---------------------------------------------------------------------------

def test_verdict_vocabularies():
    assert fb.RENDER_VERDICTS == ("promote", "keep", "rework", "archive", "cut")
    assert fb.DIRECTION_VERDICTS == ("works", "maybe", "dead_end")
    assert set(fb.VERDICTS) == set(fb.RENDER_VERDICTS) | set(fb.DIRECTION_VERDICTS)
    assert fb.CURATION_EQUIV == {"promote": "KEEP", "keep": "FLAVOUR", "rework": "REWORK",
                                 "archive": "PARKED", "cut": "KILL"}


@pytest.mark.parametrize("v", fb.RENDER_VERDICTS)
def test_render_verdicts_accepted(env, v):
    e = fb.append(render(v.upper(), note="  hi  "))
    assert e["scope"] == "render" and e["verdict"] == v and e["note"] == "hi"
    assert e["subject"] == "studio/ising"


@pytest.mark.parametrize("v", fb.DIRECTION_VERDICTS)
def test_direction_verdicts_accepted(env, v):
    e = fb.append(direction(v, "r02", label="COOLING STRIP", root="r02"))
    assert (e["scope"], e["direction"], e["label"], e["root"]) == \
        ("direction", "r02", "COOLING STRIP", "r02")
    assert e["target"] == "studio/ising/@direction/r02"


@pytest.mark.parametrize("record,match", [
    (render("works"), "render verdict"),                          # direction verdict on a render
    (render("maybe"), "render verdict"),
    (render("bogus"), "render verdict"),
    (direction("keep", "r02"), "direction verdict"),              # render verdict on a direction
    (direction("promote", "r02"), "direction verdict"),
    ({**render("keep"), "scope": "plate"}, "scope"),
    (render("keep", target="studio/ising/../../etc/passwd"), "bad target"),
    ({"verdict": "keep", "target": ""}, "bad target"),
    ({**render("keep"), "target": "studio/ising/@direction/r02"}, "@ segment"),
    ({**render("keep"), "target": "studio/ising/@x/pp.png"}, "@ segment"),
    (direction("works", "R02"), "bad direction key"),
    (direction("works", "cooling-strip"), "bad direction key"),
    (direction("works", "r2"), "bad direction key"),
    (direction("works", "x-" + "a" * 41), "bad direction key"),
    ({**direction("works", "r02"), "target": "studio/ising/@direction/r03"}, "direction target"),
    ({**direction("works", "r02"), "target": "studio/gan/@direction/r02"}, "direction target"),
    ({**direction("works", "r02"), "subject": ""}, "plain subject"),
    ({**direction("works", "r02"), "subject": "studio/../x",
      "target": "studio/../x/@direction/r02"}, "bad target"),
])
def test_rejections(env, record, match):
    with pytest.raises(ValueError, match=match):
        fb.append(record)
    assert not fb.LOG.exists()


@pytest.mark.parametrize("key", ["r02", "r123", "original", "x-brand-new", "x-a"])
def test_direction_keys(env, key):
    assert fb.append(direction("maybe", key))["direction"] == key


# ---------------------------------------------------------------------------
# latest-record-wins, scopes kept apart
# ---------------------------------------------------------------------------

def test_latest_wins_and_scopes_apart(env):
    fb.append(render("rework", note="first"))
    fb.append(render("keep", note="second"))
    fb.append(direction("maybe", "r02"))
    fb.append(direction("works", "r02", note="yes"))
    fb.append(direction("dead_end", "r03"))
    by_target = fb.latest_by_target()
    assert by_target["studio/ising/current/pp_ising_v6.png"]["verdict"] == "keep"
    assert by_target["studio/ising/@direction/r02"]["verdict"] == "works"
    assert {k: r["verdict"] for k, r in fb.latest_by_render().items()} == \
        {("studio/ising", "pp_ising_v6.png"): "keep"}
    assert {k: r["verdict"] for k, r in fb.latest_directions().items()} == \
        {("ising", "r02"): "works", ("ising", "r03"): "dead_end"}


def test_old_records_without_scope_are_render(env):
    env.mkdir(exist_ok=True)
    old = {"when": "2026-09-20T14:10:12", "target": "studio/ising/current/pp_ising_v6.png",
           "subject": "studio/ising", "verdict": "promote", "note": "legacy", "refs": [],
           "piece": None, "applied": False}
    fb.LOG.write_text(json.dumps(old) + "\nnot json\n\n")
    assert list(fb.latest_by_render()) == [("studio/ising", "pp_ising_v6.png")]
    assert fb.latest_directions() == {}
    assert fb.scope_of(old) == "render"


def test_render_verdict_survives_a_tier_move(env):
    fb.append(render("archive", tier="trials"))
    fb.append(render("keep", tier="archive"))          # same basename, new path
    (rec,) = fb.latest_by_render().values()
    assert rec["verdict"] == "keep"


# ---------------------------------------------------------------------------
# views
# ---------------------------------------------------------------------------

def test_views(env):
    fb.append(render("rework", note="fix the footer"))
    fb.append(render("keep", name="pp_ising_COASTLINE_v8.png", note="a flavour"))
    fb.append(render("cut", name="pp_ising_COOLING_STRIP_v9.png"))
    fb.append(render("archive", name="pp_ising_r06_wildcard_v11.png"))
    fb.append(direction("works", "r02", label="COOLING STRIP", note="continue this"))
    fb.append(direction("dead_end", "r03", label="COASTLINE", note="no more tori"))
    stats = fb.write_views()
    assert stats["queued"] == 1 and stats["directions"] == 2 and stats["plates"] == 4

    plate = (env / "ising" / "FEEDBACK.md").read_text()
    body = plate.split("## Directions", 1)[1]
    assert plate.index("## Directions") < plate.index("## Renders")    # the table opens the file
    assert "| **WORKS** | `r02` | COOLING STRIP | r02, r04 |" in body
    assert "| **DEAD END** | `r03` | COASTLINE | r03 |" in body
    assert "| unjudged | `r06` | THE SUNBURST | r06 | art_deco (STYLES.md §2) / radial + nested" in body
    # dead-end rounds + rounds whose ledger render is CUT (r02) or ARCHIVEd (r06)
    assert "**Rounds not to fork from:** r02, r03, r06" in plate
    assert "KEEP = a flavour worth keeping" in plate and "that one is PROMOTE" in plate
    for v in ("PROMOTE", "KEEP", "REWORK", "ARCHIVE", "CUT"):
        assert f"{v} =" in plate
    assert "### REWORK — `pp_ising_v6.png`" in plate
    assert "@direction" not in plate.split("## Renders", 1)[1]           # no direction sections

    roll = (env / "FEEDBACK.md").read_text()
    assert "## Directions" in roll and "| `ising` | `r03` | COASTLINE | **DEAD END** |" in roll
    assert "@direction" not in roll.split("## Directions", 1)[0]

    dirs = (env / "DIRECTIONS.md").read_text()
    lines = [ln for ln in dirs.splitlines() if ln.startswith("| **")]
    assert lines[0].startswith("| **WORKS** | `ising` | `r02` | COOLING STRIP |")
    assert lines[1].startswith("| **DEAD END** | `ising` | `r03` | COASTLINE |")
    assert "no more tori" in lines[1]

    queue = (env / "QUEUE.md").read_text()
    assert "1 drawing(s) awaiting rework" in queue and "fix the footer" in queue
    assert "@direction" not in queue and "a flavour" not in queue


def test_views_direction_only_plate_and_unknown_key(env):
    fb.append(direction("maybe", "x-side-quest", label="side quest"))
    fb.write_views()
    plate = (env / "ising" / "FEEDBACK.md").read_text()
    assert "| **MAYBE** | `x-side-quest` | side quest |" in plate
    assert "_no render verdicts yet_" in plate
    assert "0 drawing(s) awaiting rework" in (env / "QUEUE.md").read_text()


def test_views_merge_aliased_subjects(env, monkeypatch):
    (env / "resonance-backprop").mkdir()
    fb.append({"target": "studio/res_backprop/current/pp_res_backprop_v5.png", "verdict": "keep"})
    fb.append({"target": "studio/resonance_backprop/trials/pp_resonance_backprop_the-fold_v5.png",
               "verdict": "rework"})
    fb.write_views()
    text = (env / "resonance-backprop" / "FEEDBACK.md").read_text()
    assert "pp_res_backprop_v5.png" in text and "the-fold_v5" in text   # one file, both subjects


def test_steering(env):
    fb.append(render("keep", name="pp_ising_COASTLINE_v8.png"))
    fb.append(render("cut", name="pp_ising_r04_iterate_v5.png"))
    fb.append(direction("dead_end", "r06"))
    fb.append(direction("works", "r02"))
    s = fb.steering("ising")
    assert s["avoid_parents"] == ["r04", "r06"]
    assert s["protected"] == ["pp_ising_COASTLINE_v8.png"]
    assert s["directions"]["works"][0]["key"] == "r02"
    assert s["directions"]["works"][0]["rounds"] == ["r02", "r04"]
    assert s["directions"]["dead_end"][0]["label"] == "THE SUNBURST"
    assert s["verdicts"] == {"r02": "works", "r06": "dead_end"}


# ---------------------------------------------------------------------------
# steering the studio: studio_descriptions --json
# ---------------------------------------------------------------------------

DESCRIPTION = """# ISING — description

| field | value |
|---|---|
| status | iterating |
| source | `studio/ising/rounds/r04/piece.py` |

## In one line
The Ising model.

## Next versions
- **SUNBURST** (flavour, r06): the deco reading.
- **COASTLINE** (flavour, r03): the torus.
- **cooling-strip** (abstract): continue the strip.
- **brand-new** (lens): nothing like it yet.
"""


def test_descriptions_json_steering(env, monkeypatch):
    import studio_descriptions as sd

    monkeypatch.setattr(sd, "STUDIO", env)
    (env / "ising" / "DESCRIPTION.md").write_text(DESCRIPTION)
    fb.append(direction("dead_end", "r03", label="COASTLINE"))
    fb.append(direction("works", "r02", label="COOLING STRIP"))
    fb.append(render("keep", name="pp_ising_r06_wildcard_v11.png"))
    fb.append(render("archive", name="pp_ising_r04_iterate_v5.png"))
    (row,) = sd.rows()
    assert row["slug"] == "ising" and row["parent"] == "r04"
    theses = {t["name"]: (t["direction"], t["verdict"]) for t in row["theses"]}
    assert theses == {"SUNBURST": ("r06", None), "cooling-strip": ("r02", "works"),
                      "brand-new": (None, None)}
    assert [(t["name"], t["direction"], t["verdict"]) for t in row["blocked_theses"]] == \
        [("COASTLINE", "r03", "dead_end")]
    assert row["directions"]["works"] == [{"key": "r02", "label": "COOLING STRIP",
                                           "rounds": ["r02", "r04"]}]
    assert row["directions"]["dead_end"][0]["key"] == "r03"
    assert row["directions"]["maybe"] == []
    assert row["avoid_parents"] == ["r03", "r04"]         # dead end + the archived r04 render
    assert row["protected"] == ["pp_ising_r06_wildcard_v11.png"]
    json.dumps(row)                                        # the workflow reads it as JSON


def test_descriptions_without_feedback(env, monkeypatch):
    import studio_descriptions as sd

    monkeypatch.setattr(sd, "STUDIO", env)
    (env / "ising" / "DESCRIPTION.md").write_text(DESCRIPTION)
    (row,) = sd.rows()
    assert len(row["theses"]) == 4 and row["blocked_theses"] == []
    assert row["directions"] == {"works": [], "maybe": [], "dead_end": []}
    assert row["avoid_parents"] == [] and row["protected"] == []
