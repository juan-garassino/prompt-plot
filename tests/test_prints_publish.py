"""The `publish` verdict: which plates go to the portfolio site.

A publish record is its own scope with the virtual target
``<subject>/@publish/<basename>`` — inside gallery/, never a file — so it rides
the existing feedback log, server and viewer without touching render verdicts:

- scripts/gallery_feedback.py validates it and answers ``latest_published()``
  (the contract the site exporter reads);
- scripts/gallery_serve.py accepts it on POST /feedback with no code change;
- scripts/gallery_apply.py plans no move from it (it iterates render scope only);
- scripts/gallery_index.py inlines ``publish_snapshot()`` as ``__PUBV__`` and the
  viewer toggles it with "Publish to site" / ``p``.

Fixtures are adapted from tests/test_gallery_feedback.py:env,
tests/test_gallery_serve_feedback.py:server and tests/test_gallery_views.py:
every module global is repointed at tmp, so the real log is never written.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import gallery_apply as ga  # noqa: E402
import gallery_directions as gd  # noqa: E402
import gallery_feedback as fb  # noqa: E402
import gallery_index as gi  # noqa: E402
import gallery_serve  # noqa: E402
import studio_sync  # noqa: E402

NAME = "pp_ising_v6.png"
TARGET = f"studio/ising/@publish/{NAME}"


def publish(verdict: str = "publish", basename: str = NAME, subject: str = "studio/ising",
            target: str | None = None, **kw) -> dict:
    return {"scope": "publish", "subject": subject, "basename": basename,
            "target": target if target is not None else f"{subject}/@publish/{basename}",
            "verdict": verdict, "note": "", **kw}


@pytest.fixture
def env(tmp_path, monkeypatch):
    st, gal = tmp_path / "studio", tmp_path / "gallery"
    (st / "ising").mkdir(parents=True)
    cur = gal / "studio" / "ising" / "current"
    cur.mkdir(parents=True)
    (cur / NAME).write_bytes(b"png")
    (cur / "pp_ising_v6.gcode").write_text("G0 X0\n")
    for mod, name, val in ((fb, "REPO", tmp_path), (fb, "STUDIO", st), (fb, "GALLERY", gal),
                           (fb, "LOG", st / "feedback.jsonl"), (gd, "STUDIO", st),
                           (gd, "GALLERY", gal), (ga, "GALLERY", gal),
                           (ga, "MOVES", gal / "MOVES.tsv"), (studio_sync, "GALLERY", gal),
                           (studio_sync, "STUDIO", st), (studio_sync, "DEST", gal / "studio")):
        monkeypatch.setattr(mod, name, val)
    return st


# ---------------------------------------------------------------------------
# gallery_feedback: vocabulary, record shape, latest_published
# ---------------------------------------------------------------------------

def test_publish_vocabulary():
    assert fb.PUBLISH_VERDICTS == ("publish", "unpublish")
    assert fb.SCOPES["publish"] == fb.PUBLISH_VERDICTS
    assert set(fb.PUBLISH_VERDICTS) <= set(fb.VERDICTS)
    # the render and direction vocabularies are untouched
    assert fb.SCOPES["render"] == ("promote", "keep", "rework", "archive", "cut")
    assert fb.SCOPES["direction"] == ("works", "maybe", "dead_end")


def test_publish_record_shape(env):
    e = fb.append(publish("PUBLISH"))
    assert e["scope"] == "publish" and e["verdict"] == "publish"
    assert e["target"] == TARGET and e["subject"] == "studio/ising"
    assert e["basename"] == NAME
    assert e["note"] == "" and e["refs"] == [] and e["applied"] is False
    assert "piece" in e and e["when"]
    line = json.loads((env / "feedback.jsonl").read_text().splitlines()[-1])
    assert line == e
    assert set(line) == {"when", "scope", "target", "subject", "basename", "verdict",
                         "note", "refs", "piece", "applied"}


def test_publish_unpublish_republish(env):
    key = ("studio/ising", NAME)
    assert fb.latest_published() == {}
    fb.append(publish())
    pub = fb.latest_published()
    assert set(pub) == {key} and pub[key]["verdict"] == "publish"
    assert pub[key]["basename"] == NAME
    fb.append(publish("unpublish"))
    assert fb.latest_published() == {}
    fb.append(publish())
    assert set(fb.latest_published()) == {key}


def test_latest_published_takes_records_and_is_per_basename(env):
    recs = [
        {**publish(), "when": "2026-10-01T10:00:00"},
        {**publish(basename="pp_ising_v7.jpg"), "when": "2026-10-01T10:01:00"},
        {**publish("unpublish", basename="pp_ising_v7.jpg"), "when": "2026-10-01T10:02:00"},
        {"when": "2026-10-01T10:03:00", "scope": "render", "subject": "studio/ising",
         "target": f"studio/ising/current/{NAME}", "verdict": "cut"},
    ]
    assert set(fb.latest_published(recs)) == {("studio/ising", NAME)}
    assert not (env / "feedback.jsonl").exists()  # records= never reads the log


def test_render_verdict_on_the_same_png_does_not_shadow_publish(env):
    fb.append(publish())
    fb.append({"target": f"studio/ising/current/{NAME}", "subject": "studio/ising",
               "verdict": "archive"})
    assert fb.latest_published()[("studio/ising", NAME)]["verdict"] == "publish"
    renders = fb.latest_by_render()
    assert set(renders) == {("studio/ising", NAME)}
    assert renders[("studio/ising", NAME)]["verdict"] == "archive"
    # and a publish AFTER the render verdict does not shadow the render verdict
    fb.append(publish("unpublish"))
    fb.append(publish())
    assert fb.latest_by_render()[("studio/ising", NAME)]["verdict"] == "archive"
    assert fb.latest_directions() == {}


def test_latest_by_render_ignores_publish_only(env):
    fb.append(publish())
    assert fb.latest_by_render() == {}


def test_publish_accepts_every_image_extension_case_insensitively(env):
    for name in ("a.png", "b.JPG", "c.jpeg", "d.WebP"):
        assert fb.append(publish(basename=name))["basename"] == name
    assert len(fb.latest_published()) == 4


@pytest.mark.parametrize("rec", [
    publish(basename="sub/pp_ising_v6.png", target="studio/ising/@publish/sub/pp_ising_v6.png"),
    publish(basename="pp_ising_v6.gcode"),
    publish(basename="pp_ising_v6"),
    publish(basename=""),
    publish(basename=".png"),
    publish(basename=".JPG"),
    publish(target="studio/ising/@publish/pp_other.png"),
    publish(target=f"studio/ising/current/{NAME}"),
    publish(subject="studio/@ising"),
    publish(subject="studio/../ising"),
    publish(subject=""),
    publish("keep"),
    publish("works"),
], ids=["slash", "gcode", "noext", "empty-basename", "bare-ext", "bare-ext-upper", "target-mismatch", "render-target",
        "at-subject", "dotdot-subject", "empty-subject", "render-verdict", "direction-verdict"])
def test_invalid_publish_records(env, rec):
    with pytest.raises(ValueError):
        fb.append(rec)
    assert not (env / "feedback.jsonl").exists()


def test_a_render_verdict_cannot_use_the_publish_target(env):
    with pytest.raises(ValueError):
        fb.append({"target": TARGET, "subject": "studio/ising", "verdict": "keep"})


def test_publish_records_never_reach_the_markdown_views(env):
    fb.append({"target": "studio/ising/current/pp_ising_COASTLINE_v8.png",
               "subject": "studio/ising", "verdict": "rework", "note": "tighten"})
    fb.append(publish())
    stats = fb.write_views()
    assert stats["plates"] == 1 and stats["queued"] == 1
    for view in (env / "ising" / "FEEDBACK.md", env / "FEEDBACK.md", env / "QUEUE.md",
                 env / "DIRECTIONS.md"):
        text = view.read_text()
        assert NAME not in text and "@publish" not in text, view
        assert "PUBLISH" not in text, view
    assert "pp_ising_COASTLINE_v8.png" in (env / "ising" / "FEEDBACK.md").read_text()


def test_a_publish_only_plate_writes_no_feedback_stub(env):
    # a gallery-only subject (no studio/ folder) that is only ever published:
    # write_views used to give it a studio/<slug>/FEEDBACK.md reading
    # "_no render verdicts yet_"
    fb.append(publish(subject="physics/big-bang", basename="pp_big_bang_v2.png"))
    stats = fb.write_views()
    assert stats["subjects"] == 0 and stats["plates"] == 0
    assert not (env / "physics-big-bang").exists()
    assert not (env / "ising" / "FEEDBACK.md").exists()


# ---------------------------------------------------------------------------
# gallery_apply: a publish record moves nothing
# ---------------------------------------------------------------------------

def test_apply_plans_no_move_from_a_publish_only_log(env):
    fb.append(publish())
    fb.append(publish("unpublish"))
    fb.append(publish())
    assert ga.plan() == []


# ---------------------------------------------------------------------------
# gallery_serve: POST /feedback and GET /feedback.json
# ---------------------------------------------------------------------------

@pytest.fixture
def server(env, monkeypatch):
    from http.server import ThreadingHTTPServer

    gal = fb.GALLERY
    (gal / "viewer.html").write_text("<html></html>")
    monkeypatch.setattr(gallery_serve, "GALLERY", gal)
    srv = ThreadingHTTPServer(("127.0.0.1", 0), gallery_serve.Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"

    def call(route: str, body: dict | None = None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(base + route, data=data,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            with e:
                return e.code, json.loads(e.read())

    try:
        yield call, env
    finally:
        srv.shutdown()
        srv.server_close()


def test_post_publish_and_read_back(server):
    call, st = server
    code, out = call("/feedback", publish())
    assert code == 200 and out["entry"]["scope"] == "publish"
    assert out["entry"]["basename"] == NAME
    lines = (st / "feedback.jsonl").read_text().splitlines()
    assert len(lines) == 1 and json.loads(lines[0])["target"] == TARGET
    code, out = call("/feedback.json")
    assert code == 200
    rec = out["records"][TARGET]
    assert rec["scope"] == "publish" and rec["verdict"] == "publish"
    assert rec["basename"] == NAME


def test_post_bad_publish_is_refused(server):
    call, st = server
    code, out = call("/feedback", publish(target="studio/ising/@publish/other.png"))
    assert code == 400 and out["error"]
    assert not (st / "feedback.jsonl").exists()


# ---------------------------------------------------------------------------
# gallery_index: publish_snapshot and the viewer
# ---------------------------------------------------------------------------

class _NoDirections:
    """Stands in for gallery_directions: no ledgers, no directions."""

    def parse_ledger(self, text: str) -> list[dict]:
        return []

    def directions(self, subject: str) -> dict:
        return {}

    def direction_of(self, subject: str, name: str) -> str | None:
        return None


@pytest.fixture
def gallery(env, monkeypatch) -> Path:
    gal = fb.GALLERY
    (gal / "physics" / "bar" / "current").mkdir(parents=True)
    (gal / "physics" / "bar" / "current" / "bar_v1.png").write_bytes(b"png")
    monkeypatch.setattr(gi, "GALLERY", gal)
    monkeypatch.setattr(gi, "STUDIO", env)
    monkeypatch.setattr(gi, "gd", _NoDirections())
    return gal


def test_publish_snapshot_shape(gallery):
    assert gi.publish_snapshot() == {}
    fb.append(publish())
    fb.append({"target": f"studio/ising/current/{NAME}", "subject": "studio/ising",
               "verdict": "keep"})
    snap = gi.publish_snapshot()
    assert list(snap) == [f"studio/ising|{NAME}"]
    entry = snap[f"studio/ising|{NAME}"]
    assert entry["v"] == "publish" and isinstance(entry["w"], int) and entry["w"] > 0
    assert set(entry) == {"v", "w"}
    fb.append(publish("unpublish"))
    assert gi.publish_snapshot() == {}


def test_render_snapshot_leaves_publish_records_out(gallery):
    fb.append(publish())
    snap = gi.feedback_snapshot()
    assert snap["records"] == [] and snap["global"] == 0


def test_viewer_inlines_the_publish_snapshot(gallery):
    fb.append(publish())
    gi.build()
    page = (gallery / "viewer.html").read_text()
    assert "__PUBV__" not in page
    m = re.search(r"const PUBV0 = (\{.*?\});", page)
    assert m, "PUBV0 not inlined"
    assert json.loads(m.group(1)) == gi.publish_snapshot()
    for needle in ('id="pub"', "Publish to site", "function recordPublish",
                   '<option value="published">published</option>', "isPublished",
                   "no gcode beside this render"):
        assert needle in page, needle


# ---------------------------------------------------------------------------
# the viewer's publish index, run in node (skipped without a node binary)
# ---------------------------------------------------------------------------

def _node() -> str | None:
    found = shutil.which("node")
    if found:
        return found
    for cand in sorted(Path.home().glob(".nvm/versions/node/*/bin/node"), reverse=True):
        return str(cand)
    for cand in ("/usr/local/bin/node", "/opt/homebrew/bin/node"):
        if Path(cand).exists():
            return cand
    return None


def test_publish_index_rule_in_node(tmp_path):
    node = _node()
    if node is None:
        pytest.skip("no node binary to run the viewer's publish rule with")
    m = re.search(r"/\* PUBLISH-RULE.*?\*/(.*?)/\* /PUBLISH-RULE \*/", gi.TEMPLATE, re.S)
    assert m, "PUBLISH-RULE block missing from the viewer template"
    probe = m.group(1) + """
const base = {'studio/a|x.png': {v: 'publish', w: 100}, 'studio/a|y.png': {v: 'publish', w: 100}};
const fb = {
  'studio/a/@publish/y.png': {scope: 'publish', subject: 'studio/a', basename: 'y.png',
                              verdict: 'unpublish', when: '2100-01-01T00:00:00'},
  'studio/a/@publish/z.png': {scope: 'publish', subject: 'studio/a', basename: 'z.png',
                              verdict: 'publish', when: '2100-01-01T00:00:00'},
  'studio/a/@publish/old.png': {scope: 'publish', subject: 'studio/a', basename: 'old.png',
                                verdict: 'unpublish', when: '1970-01-01T00:00:10'},
  'studio/a/current/x.png': {scope: 'render', subject: 'studio/a', verdict: 'cut',
                             when: '2100-01-01T00:00:00'},
  'studio/a/current/w.png': {subject: 'studio/a', verdict: 'promote', when: '2100-01-01T00:00:00'},
};
base['studio/a|old.png'] = {v: 'publish', w: 9e12};   // newer than its live unpublish
const pv = publishIndex(base, fb);
console.log(JSON.stringify(Object.keys(pv).sort()));
"""
    f = tmp_path / "pub.js"
    f.write_text(probe)
    out = subprocess.run([node, str(f)], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    assert json.loads(out.stdout) == ["studio/a|old.png", "studio/a|x.png", "studio/a|z.png"]
